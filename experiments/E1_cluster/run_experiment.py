#!/usr/bin/env python
"""E1 — Texto Sujo: compara pipelines de embeddings + clusterização.

Regras:
- Sem limpeza agressiva (apenas trim e lower opcional).
- Sem expansão manual de abreviações.
- Sem tuning exaustivo.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import adjusted_rand_score

import hdbscan
from sentence_transformers import SentenceTransformer

# ============================================================================
# Constantes de Configuração
# ============================================================================

# Caminho padrão para o dataset CSV contendo os relatos a serem analisados
# O dataset deve conter as colunas: id, texto, setor
DEFAULT_DATASET = (
    Path(__file__).resolve().parents[1] / "E0_dataset_goldset" / "dataset.csv"
)

# Caminho padrão para o arquivo de saída onde será gerado o relatório em Markdown
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "output_report.md"

# Caminho padrão para o arquivo de stopwords em português brasileiro
# Cada stopword deve estar em uma linha separada
DEFAULT_STOPWORDS = (
    Path(__file__).resolve().parents[1] / "E0_dataset_goldset" / "stopwords_ptbr.txt"
)

# Nome do modelo de embeddings do SentenceTransformer
# Modelo multilíngue que inclui português brasileiro, leve e rápido, adequado para MVP
# Alternativas para português BR:
# - "paraphrase-multilingual-MiniLM-L12-v2" (multilíngue, inclui PT-BR)
# - "paraphrase-multilingual-mpnet-base-v2" (multilíngue, melhor qualidade)
# - "rufimelo/bert-large-portuguese-cased-sts2" (específico PT-BR, melhor qualidade)
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

# Número de clusters para o algoritmo KMeans
# Valor fixo escolhido baseado na expectativa de 5-8 temas operacionais em ~100 relatos
KMEANS_K = 6

# Seed primária para reprodutibilidade dos experimentos
# Usada como seed padrão para todas as operações aleatórias
SEED_PRIMARY = 42

# Seed secundária para avaliar estabilidade dos algoritmos
# Compara resultados entre duas execuções com seeds diferentes
SEED_SECONDARY = 99


# ============================================================================
# Estruturas de Dados
# ============================================================================

@dataclass
class ClusterReport:
    """Representa um cluster individual com suas características e análise.
    
    Atributos:
        label: Identificador numérico do cluster (pode ser -1 para ruído)
        size: Número de textos pertencentes a este cluster
        top_terms: Lista dos termos mais relevantes identificados via TF-IDF
        examples: Lista com até 5 exemplos de textos representativos do cluster
        summary: Resumo textual gerado automaticamente descrevendo o cluster
        generic_or_incoherent: Flag indicando se o cluster é genérico ou incoerente
    """
    label: int
    size: int
    top_terms: List[str]
    examples: List[str]
    summary: str
    generic_or_incoherent: bool


@dataclass
class PipelineReport:
    """Relatório completo de um pipeline de clusterização.
    
    Atributos:
        name: Nome descritivo do pipeline (ex: "Pipeline A — Baseline de MVP")
        num_clusters: Número total de clusters identificados (excluindo ruído se aplicável)
        clusters: Lista de ClusterReport, um para cada cluster encontrado
        stability_ari: Adjusted Rand Index medindo estabilidade entre execuções (None se não aplicável)
        noise_ratio: Proporção de textos marcados como ruído (None se não aplicável)
        notes: Lista de observações e notas sobre o pipeline e seus resultados
    """
    name: str
    num_clusters: int
    clusters: List[ClusterReport]
    stability_ari: float | None
    noise_ratio: float | None
    notes: List[str]


# ============================================================================
# Funções de Configuração e Carregamento
# ============================================================================

def set_seed(seed: int) -> None:
    """Define a seed para garantir reprodutibilidade dos experimentos.
    
    Configura as seeds tanto para o módulo random do Python quanto para numpy,
    garantindo que operações aleatórias (como inicialização do KMeans) sejam
    reproduzíveis entre execuções.
    
    Args:
        seed: Valor inteiro usado como seed para geradores aleatórios
    """
    random.seed(seed)
    np.random.seed(seed)


def load_dataset(path: Path) -> pd.DataFrame:
    """Carrega o dataset CSV e valida se contém as colunas esperadas.
    
    O dataset deve conter obrigatoriamente as colunas:
    - id: Identificador único de cada relato
    - texto: Conteúdo textual do relato a ser analisado
    - setor: Setor/categoria do relato (usado para validação, se disponível)
    
    Args:
        path: Caminho para o arquivo CSV do dataset
        
    Returns:
        DataFrame do pandas com os dados carregados
        
    Raises:
        ValueError: Se o dataset não contiver todas as colunas esperadas
    """
    df = pd.read_csv(path)
    expected_cols = {"id", "texto", "setor"}
    missing = expected_cols - set(df.columns)
    if missing:
        raise ValueError(f"Dataset missing columns: {sorted(missing)}")
    return df


def build_embeddings(texts: List[str]) -> np.ndarray:
    """Gera embeddings vetoriais para os textos usando SentenceTransformer.
    
    Os embeddings são representações numéricas densas dos textos que capturam
    significado semântico. São normalizados (vetores unitários) para melhorar
    a qualidade da clusterização baseada em distâncias.
    
    Args:
        texts: Lista de strings contendo os textos a serem convertidos em embeddings
        
    Returns:
        Array numpy de shape (n_texts, embedding_dim) com os embeddings normalizados
    """
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(
        texts,
        show_progress_bar=False,
        normalize_embeddings=True,
    )
    return np.array(embeddings)


def load_stopwords(path: Path) -> List[str]:
    """Carrega lista de stopwords do arquivo de texto.
    
    Stopwords são palavras comuns (como "o", "a", "de") que geralmente não
    carregam informação semântica relevante e são filtradas na análise de termos.
    
    Args:
        path: Caminho para o arquivo de texto com uma stopword por linha
        
    Returns:
        Lista de strings contendo as stopwords (linhas vazias são ignoradas)
    """
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


# ============================================================================
# Funções de Análise de Texto
# ============================================================================

def top_terms_for_texts(
    texts: List[str],
    stopwords: List[str],
    top_n: int = 6,
) -> List[str]:
    """Identifica os termos mais relevantes em uma coleção de textos usando TF-IDF.
    
    TF-IDF (Term Frequency-Inverse Document Frequency) mede a importância de
    termos considerando tanto sua frequência nos textos quanto sua raridade
    no corpus. Termos com alto TF-IDF são mais distintivos e informativos.
    
    Args:
        texts: Lista de textos a serem analisados
        stopwords: Lista de palavras a serem ignoradas na análise
        top_n: Número máximo de termos a retornar (padrão: 6)
        
    Returns:
        Lista de strings com os top_n termos mais relevantes, ordenados por relevância
        Retorna lista vazia se não houver textos ou se não houver termos válidos
    """
    if not texts:
        return []
    # Configura TF-IDF para unigramas e bigramas (palavras e pares de palavras)
    # Limita a 50 features para evitar sobrecarga com vocabulários muito grandes
    vectorizer = TfidfVectorizer(
        stop_words=stopwords,
        ngram_range=(1, 2),
        max_features=50,
    )
    tfidf = vectorizer.fit_transform(texts)
    if tfidf.shape[1] == 0:
        return []
    # Calcula a média dos scores TF-IDF para cada termo e seleciona os top_n
    mean_scores = np.asarray(tfidf.mean(axis=0)).ravel()
    indices = np.argsort(mean_scores)[::-1][:top_n]
    terms = vectorizer.get_feature_names_out()
    return [terms[i] for i in indices if mean_scores[i] > 0]


def summarize_cluster(top_terms: List[str], example: str) -> str:
    """Gera um resumo textual descritivo de um cluster.
    
    Cria uma descrição legível combinando os termos mais relevantes com um
    exemplo representativo do cluster, facilitando a interpretação humana
    dos resultados.
    
    Args:
        top_terms: Lista dos termos mais relevantes do cluster
        example: Texto exemplo representativo do cluster
        
    Returns:
        String com resumo descritivo do cluster
    """
    if not top_terms:
        return "Cluster sem termos dominantes; relatos variados ou muito curtos."
    # Usa apenas os 3 primeiros termos para manter o resumo conciso
    terms = ", ".join(top_terms[:3])
    return (
        f"Relatos focados em {terms}. "
        f"Exemplo representativo: \"{example}\"."
    )


def build_cluster_reports(
    texts: List[str],
    labels: np.ndarray,
    stopwords: List[str],
    noise_label: int | None = None,
) -> Tuple[List[ClusterReport], List[str]]:
    """Constrói relatórios detalhados para cada cluster identificado.
    
    Agrupa os textos por cluster, extrai termos relevantes, identifica exemplos
    e gera resumos. Também marca clusters genéricos ou incoerentes baseado em
    critérios como tamanho pequeno ou ausência de termos distintivos.
    
    Args:
        texts: Lista de textos originais (mesma ordem dos labels)
        labels: Array numpy com os labels de cluster para cada texto
        stopwords: Lista de stopwords para filtrar na análise de termos
        noise_label: Label usado para marcar ruído (geralmente -1), None se não aplicável
        
    Returns:
        Tupla contendo:
        - Lista de ClusterReport, um para cada cluster encontrado
        - Lista de strings com notas e observações sobre os clusters
    """
    # Agrupa textos por cluster
    clusters: Dict[int, List[str]] = {}
    for text, label in zip(texts, labels):
        clusters.setdefault(label, []).append(text)

    reports: List[ClusterReport] = []
    notes: List[str] = []
    # Processa cada cluster em ordem crescente de label
    for label, cluster_texts in sorted(clusters.items(), key=lambda x: x[0]):
        top_terms = top_terms_for_texts(cluster_texts, stopwords)
        examples = cluster_texts[:5]  # Até 5 exemplos representativos
        summary = summarize_cluster(top_terms, examples[0])
        is_noise = noise_label is not None and label == noise_label
        # Marca como genérico/incoerente se for ruído, muito pequeno ou sem termos distintivos
        generic_or_incoherent = is_noise or len(cluster_texts) < 3 or not top_terms
        if is_noise:
            notes.append("Cluster -1 representa ruído/itens não agrupados.")
        if generic_or_incoherent:
            notes.append(
                f"Cluster {label} marcado como genérico/incoerente "
                "(tamanho pequeno ou termos fracos)."
            )
        reports.append(
            ClusterReport(
                label=label,
                size=len(cluster_texts),
                top_terms=top_terms,
                examples=examples,
                summary=summary,
                generic_or_incoherent=generic_or_incoherent,
            )
        )
    return reports, notes


# ============================================================================
# Funções de Clusterização
# ============================================================================

def run_kmeans(embeddings: np.ndarray, seed: int) -> np.ndarray:
    """Executa clusterização KMeans nos embeddings.
    
    KMeans é um algoritmo de clusterização particional que divide os dados
    em k clusters pré-definidos, minimizando a variância intra-cluster.
    É determinístico quando a seed é fixa, permitindo reprodutibilidade.
    
    Args:
        embeddings: Array numpy de shape (n_samples, n_features) com os embeddings
        seed: Seed para garantir reprodutibilidade da inicialização
        
    Returns:
        Array numpy com os labels de cluster para cada embedding (0 a k-1)
    """
    kmeans = KMeans(n_clusters=KMEANS_K, random_state=seed, n_init=10)
    return kmeans.fit_predict(embeddings)


def run_hdbscan(embeddings: np.ndarray) -> np.ndarray:
    """Executa clusterização HDBSCAN nos embeddings.
    
    HDBSCAN (Hierarchical Density-Based Spatial Clustering) identifica clusters
    baseado em densidade, sem precisar especificar o número de clusters a priori.
    Itens que não se encaixam em clusters densos são marcados como ruído (label -1).
    
    Args:
        embeddings: Array numpy de shape (n_samples, n_features) com os embeddings
        
    Returns:
        Array numpy com os labels de cluster (pode incluir -1 para ruído)
    """
    # min_cluster_size=5: clusters devem ter pelo menos 5 itens
    # min_samples=2: ponto precisa de pelo menos 2 vizinhos para ser core
    clusterer = hdbscan.HDBSCAN(min_cluster_size=5, min_samples=2)
    return clusterer.fit_predict(embeddings)


# ============================================================================
# Pipelines de Clusterização
# ============================================================================

def pipeline_a(
    texts: List[str],
    embeddings: np.ndarray,
    stopwords: List[str],
) -> PipelineReport:
    """Pipeline A: Baseline usando KMeans com embeddings do SentenceTransformer.
    
    Este é o pipeline mais simples e direto, adequado como baseline para MVP.
    Usa KMeans com k fixo, permitindo avaliação de estabilidade via ARI
    (Adjusted Rand Index) entre execuções com seeds diferentes.
    
    Args:
        texts: Lista de textos originais
        embeddings: Embeddings vetoriais dos textos
        stopwords: Lista de stopwords para análise de termos
        
    Returns:
        PipelineReport com resultados e métricas do Pipeline A
    """
    # Executa KMeans duas vezes com seeds diferentes para medir estabilidade
    labels_primary = run_kmeans(embeddings, SEED_PRIMARY)
    labels_secondary = run_kmeans(embeddings, SEED_SECONDARY)
    # ARI mede a concordância entre as duas execuções (1.0 = idêntico, 0.0 = aleatório)
    stability = adjusted_rand_score(labels_primary, labels_secondary)
    clusters, notes = build_cluster_reports(texts, labels_primary, stopwords)
    notes.append(
        "KMeans com k fixo (k=6) por simplicidade e alinhamento com "
        "expectativa de 5-8 temas operacionais em ~100 relatos."
    )
    return PipelineReport(
        name="Pipeline A — Baseline de MVP (KMeans)",
        num_clusters=KMEANS_K,
        clusters=clusters,
        stability_ari=stability,
        noise_ratio=None,  # KMeans não identifica ruído explicitamente
        notes=notes,
    )


def pipeline_b(
    texts: List[str],
    embeddings: np.ndarray,
    stopwords: List[str],
) -> PipelineReport:
    """Pipeline B: Clusterização baseada em densidade usando HDBSCAN.
    
    HDBSCAN identifica clusters naturalmente baseado em densidade, sem precisar
    especificar o número de clusters. Itens que não se encaixam em clusters
    densos são marcados como ruído, o que é útil para identificar outliers
    ou relatos que não se encaixam em nenhum tema claro.
    
    Args:
        texts: Lista de textos originais
        embeddings: Embeddings vetoriais dos textos
        stopwords: Lista de stopwords para análise de termos
        
    Returns:
        PipelineReport com resultados e métricas do Pipeline B
    """
    labels_primary = run_hdbscan(embeddings)
    # HDBSCAN pode retornar -1 para ruído, então passamos noise_label=-1
    clusters, notes = build_cluster_reports(texts, labels_primary, stopwords, noise_label=-1)
    # Conta apenas clusters válidos (excluindo ruído)
    num_clusters = len({label for label in labels_primary if label != -1})
    # Calcula proporção de textos marcados como ruído
    noise_ratio = float(np.mean(labels_primary == -1))
    notes.append(
        "HDBSCAN identifica clusters densos e marca itens dispersos como ruído (-1)."
    )
    notes.append("Estabilidade deve ser avaliada qualitativamente via ruído e coerência.")
    return PipelineReport(
        name="Pipeline B — Densidade e ruído (HDBSCAN)",
        num_clusters=num_clusters,
        clusters=clusters,
        stability_ari=None,  # HDBSCAN não-determinístico, não calculamos ARI
        noise_ratio=noise_ratio,
        notes=notes,
    )


# ============================================================================
# Funções de Formatação e Relatório
# ============================================================================

def format_cluster(cluster: ClusterReport) -> str:
    """Formata um ClusterReport em uma string legível para o relatório.
    
    Args:
        cluster: ClusterReport a ser formatado
        
    Returns:
        String formatada com informações do cluster em Markdown
    """
    terms = ", ".join(cluster.top_terms) if cluster.top_terms else "(sem termos fortes)"
    examples = "\n".join([f"      - {example}" for example in cluster.examples])
    return (
        f"    - Cluster {cluster.label} (n={cluster.size})\n"
        f"      • top termos: {terms}\n"
        f"      • exemplos:\n{examples}\n"
        f"      • resumo: {cluster.summary}\n"
        f"      • genérico/incoerente: {cluster.generic_or_incoherent}\n"
    )


def format_pipeline(report: PipelineReport) -> str:
    """Formata um PipelineReport completo em uma string legível.
    
    Args:
        report: PipelineReport a ser formatado
        
    Returns:
        String formatada com todas as informações do pipeline em Markdown
    """
    clusters_text = "\n".join(format_cluster(cluster) for cluster in report.clusters)
    # Formata métricas opcionais (podem ser None)
    stability = (
        f"{report.stability_ari:.3f}" if report.stability_ari is not None else "n/a"
    )
    noise_text = (
        f"{report.noise_ratio:.1%}" if report.noise_ratio is not None else "n/a"
    )
    notes = "\n".join([f"  - {note}" for note in report.notes])
    return (
        f"Pipeline: {report.name}\n"
        f"  - nº de clusters: {report.num_clusters}\n"
        f"  - estabilidade (ARI entre duas execuções): {stability}\n"
        f"  - % de ruído (aprox.): {noise_text}\n"
        f"{clusters_text}\n"
        f"  - notas:\n{notes}\n"
    )


def build_report(reports: List[PipelineReport]) -> str:
    """Constrói o relatório final completo combinando todos os pipelines.
    
    Gera um relatório em Markdown contendo:
    - Resultados detalhados de cada pipeline
    - Comparação e insights gerais
    - Seção para decisões manuais sobre qual pipeline usar
    
    Args:
        reports: Lista de PipelineReport, um para cada pipeline executado
        
    Returns:
        String completa do relatório em formato Markdown
    """
    # Seção de comparação com insights gerais sobre os pipelines
    comparison = (
        "Comparação e Insights\n"
        "- KMeans tende a gerar temas consistentes e explicáveis.\n"
        "- HDBSCAN destaca ruído, útil para ver itens fora do padrão.\n"
        "- Avalie: quais clusters são mais explicáveis para um gestor.\n"
        "- Avalie: qual pipeline mistura menos temas distintos.\n"
        "- Avalie: qual parece mais simples de manter no MVP.\n"
        "- Avalie: trade-offs claros entre qualidade e complexidade.\n"
    )
    # Seção para preenchimento manual com decisões sobre qual pipeline adotar
    decisions = (
        "Decisão (preencher manualmente):\n"
        "- Base do MVP: ______________________________\n"
        "- Útil para exploração: ______________________\n"
        "- Evitar neste momento: ______________________\n"
        "Próxima iteração sugerida:\n"
        "- ___________________________________________\n"
        "- ___________________________________________\n"
    )
    pipelines_text = "\n\n".join(format_pipeline(report) for report in reports)
    return f"{pipelines_text}\n\n{comparison}\n{decisions}\n"


# ============================================================================
# Funções Principais
# ============================================================================

def parse_args() -> argparse.Namespace:
    """Parse dos argumentos de linha de comando.
    
    Permite customizar caminhos de entrada/saída. Todos os argumentos têm
    valores padrão baseados nas constantes globais, permitindo execução sem parâmetros.
    
    Returns:
        Namespace do argparse contendo todos os argumentos parseados
    """
    parser = argparse.ArgumentParser(description="E1 - Texto sujo")
    parser.add_argument(
        "--dataset",
        type=Path,
        default=DEFAULT_DATASET,
        help="Caminho do dataset.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Arquivo de saída markdown",
    )
    parser.add_argument(
        "--stopwords",
        type=Path,
        default=DEFAULT_STOPWORDS,
        help="Arquivo com stopwords pt-br (1 por linha)",
    )
    return parser.parse_args()


def main() -> None:
    """Função principal que orquestra a execução completa do experimento.
    
    Fluxo de execução:
    1. Parse dos argumentos de linha de comando
    2. Configuração de seeds para reprodutibilidade
    3. Carregamento e pré-processamento básico dos dados (trim + lowercase)
    4. Geração de embeddings uma única vez (compartilhado entre pipelines A e B)
    5. Execução dos pipelines de clusterização
    6. Geração e salvamento do relatório final
    
    O pré-processamento é intencionalmente mínimo (apenas trim e lowercase)
    para testar a capacidade dos modelos de lidar com "texto sujo" sem
    limpeza agressiva.
    """
    args = parse_args()
    # Define seed para garantir reprodutibilidade
    set_seed(SEED_PRIMARY)
    
    # Carrega dataset e valida estrutura
    df = load_dataset(args.dataset)
    # Pré-processamento mínimo: apenas trim e lowercase (sem limpeza agressiva)
    texts = df["texto"].astype(str).str.strip().str.lower().tolist()
    stopwords = load_stopwords(args.stopwords)

    # Gera embeddings uma única vez (compartilhado entre pipelines A e B)
    embeddings = build_embeddings(texts)
    
    # Executa pipelines (A e B)
    reports = [
        pipeline_a(texts, embeddings, stopwords),
        pipeline_b(texts, embeddings, stopwords),
    ]

    # Gera relatório final e salva em arquivo
    report_text = build_report(reports)
    args.output.write_text(report_text, encoding="utf-8")
    # Também imprime no console para visualização imediata
    print(report_text)


if __name__ == "__main__":
    main()
