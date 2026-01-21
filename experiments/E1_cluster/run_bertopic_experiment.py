#!/usr/bin/env python
"""E1 — BERTopic: Pipeline dedicado para modelagem de tópicos usando BERTopic.

Este script executa exclusivamente o pipeline BERTopic para análise de tópicos
em textos operacionais. O BERTopic é uma solução completa que combina múltiplas
técnicas de processamento de linguagem natural para gerar tópicos interpretáveis
automaticamente.

Diferenças em relação ao script principal (run_experiment.py):
- Este script foca exclusivamente no BERTopic, enquanto o principal compara
  KMeans e HDBSCAN
- BERTopic gera seus próprios embeddings internamente, não compartilha embeddings
  com outros pipelines
- BERTopic é mais "caixa-preta" mas gera tópicos mais legíveis rapidamente
- Este script é útil quando você quer explorar tópicos sem executar os outros
  pipelines, economizando tempo e recursos computacionais

Quando usar este script:
- Quando você quer apenas resultados do BERTopic sem comparar com outros métodos
- Para exploração rápida de tópicos em novos datasets
- Quando você precisa de tópicos mais interpretáveis e legíveis
- Para análise independente focada em modelagem de tópicos

⚠️  TROCAR MODELO DE EMBEDDINGS:
- Veja a seção "CONFIGURAÇÃO DO MODELO DE EMBEDDINGS" nas constantes (linha ~85)
- Ou veja a função run_bertopic() onde o BERTopic é inicializado (linha ~446)
- Você pode usar modelos do SentenceTransformer ou Hugging Face
- Exemplos: "paraphrase-multilingual-MiniLM-L12-v2", "neuralmind/bert-base-portuguese-cased"

Regras:
- Sem limpeza agressiva (apenas trim e lower opcional).
- Expansão de abreviações comuns (maq → maquina, dnv → de novo).
- Configuração otimizada para datasets pequenos (50-200 textos).
"""

from __future__ import annotations

import argparse
import re
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score

# Importação do BERTopic - biblioteca especializada em modelagem de tópicos
# BERTopic combina embeddings, redução de dimensionalidade, clusterização e
# extração de termos em uma solução integrada
from bertopic import BERTopic
from hdbscan import HDBSCAN
from umap import UMAP

# ============================================================================
# Constantes de Configuração
# ============================================================================

# Caminho padrão para o dataset CSV contendo os relatos a serem analisados
# O dataset deve conter as colunas: id, texto, setor
# Este caminho é relativo ao diretório do script, permitindo execução de
# qualquer localização do sistema de arquivos
DEFAULT_DATASET = (
    Path(__file__).resolve().parents[1] / "E0_dataset_goldset" / "dataset.csv"
)

# Caminho padrão para o arquivo de saída onde será gerado o relatório em Markdown
# O relatório contém análise detalhada dos tópicos identificados pelo BERTopic
# Por padrão, salva como output_bertopic_report.md no mesmo diretório do script
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "output_bertopic_report.md"

# Caminho padrão para o arquivo CSV de saída com os resultados da clusterização
# O CSV contém id, texto, setor, topic_id e top_terms para cada documento
# Por padrão, salva como output_bertopic_clusters.csv no mesmo diretório do script
DEFAULT_CSV_OUTPUT = Path(__file__).resolve().parent / "output_bertopic_clusters.csv"

# Caminho padrão para o arquivo de stopwords em português brasileiro
# Cada stopword deve estar em uma linha separada
# Stopwords são palavras comuns que geralmente não carregam informação semântica
# relevante (ex: "o", "a", "de", "em"). Embora o BERTopic tenha seu próprio
# processamento, mantemos esta constante para consistência com outros scripts
DEFAULT_STOPWORDS = (
    Path(__file__).resolve().parents[1] / "E0_dataset_goldset" / "stopwords_ptbr.txt"
)

# Seed primária para reprodutibilidade dos experimentos
# Usada como seed padrão para todas as operações aleatórias
# Importante: BERTopic não aceita seed diretamente, mas configuramos seeds
# para outras operações (como numpy) para garantir reprodutibilidade parcial
SEED_PRIMARY = 42

# Seed secundária para avaliar estabilidade dos algoritmos
# Compara resultados entre duas execuções com seeds diferentes
# A estabilidade é medida via Adjusted Rand Index (ARI), que compara a
# concordância entre duas clusterizações (1.0 = idêntico, 0.0 = aleatório)
SEED_SECONDARY = 99


@dataclass
class ClusterReport:
    """Representa um cluster (tópico) individual com suas características e análise.
    
    No contexto do BERTopic, cada cluster representa um tópico identificado
    automaticamente. Esta estrutura organiza as informações de forma padronizada
    para facilitar a análise e geração de relatórios.
    
    Atributos:
        label: Identificador numérico do cluster/tópico (pode ser -1 para ruído)
               O BERTopic atribui IDs numéricos aos tópicos, sendo -1 reservado
               para textos que não se encaixam em nenhum tópico (ruído/outliers)
        size: Número de textos pertencentes a este cluster/tópico
        top_terms: Lista dos termos mais relevantes do tópico, extraídos pelo
                   BERTopic usando c-TF-IDF (class-based TF-IDF). Estes termos
                   são calculados especificamente para cada tópico, não para o
                   corpus inteiro, o que os torna mais representativos
        examples: Lista com até 5 exemplos de textos representativos do cluster
                  Estes exemplos ajudam a entender o contexto e conteúdo dos
                  textos agrupados em cada tópico
        summary: Resumo textual gerado automaticamente descrevendo o cluster
                 Combina os termos mais relevantes com um exemplo para criar
                 uma descrição legível para humanos
        generic_or_incoherent: Flag indicando se o cluster é genérico ou incoerente
                              Clusters pequenos, sem termos distintivos, ou marcados
                              como ruído são considerados genéricos/incoerentes
    """
    label: int
    size: int
    top_terms: List[str]
    examples: List[str]
    summary: str
    generic_or_incoherent: bool


@dataclass
class PipelineReport:
    """Relatório completo do pipeline BERTopic de clusterização.
    
    Esta estrutura agrega todos os resultados e métricas do pipeline BERTopic,
    organizando as informações de forma estruturada para análise e comparação.
    
    Atributos:
        name: Nome descritivo do pipeline (ex: "Pipeline BERTopic — Exploração rápida")
        num_clusters: Número total de clusters/tópicos identificados (excluindo ruído)
                      O BERTopic determina automaticamente o número de tópicos
                      baseado na estrutura dos dados, sem necessidade de especificar
                      k a priori (diferente do KMeans)
        clusters: Lista de ClusterReport, um para cada tópico encontrado
                  Inclui tanto tópicos válidos quanto o tópico de ruído (-1) se existir
        stability_ari: Adjusted Rand Index medindo estabilidade entre execuções
                      Calculado comparando duas execuções do BERTopic com seeds
                      diferentes. Valores próximos de 1.0 indicam alta estabilidade,
                      enquanto valores baixos sugerem que os resultados podem variar
                      significativamente entre execuções
        noise_ratio: Proporção de textos marcados como ruído (tópico -1)
                     Textos marcados como ruído são aqueles que não se encaixam
                     bem em nenhum tópico identificado. Uma proporção alta pode
                     indicar que os dados são muito heterogêneos ou que os parâmetros
                     do BERTopic precisam ser ajustados
        notes: Lista de observações e notas sobre o pipeline e seus resultados
               Inclui informações sobre características específicas do BERTopic,
               limitações, e insights sobre os resultados obtidos
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
    
    A reprodutibilidade é crucial em experimentos científicos para permitir
    validação e comparação de resultados. Esta função configura as seeds tanto
    para o módulo random do Python quanto para numpy, garantindo que operações
    aleatórias sejam reproduzíveis entre execuções.
    
    Nota importante: O BERTopic não aceita seed diretamente como parâmetro,
    então a reprodutibilidade completa não é garantida. No entanto, configurar
    seeds para outras operações (como numpy) ajuda a reduzir variabilidade.
    
    Args:
        seed: Valor inteiro usado como seed para geradores aleatórios
              Valores comuns: 42 (padrão em muitos experimentos), 99 (secundário)
    """
    random.seed(seed)
    np.random.seed(seed)


def load_dataset(path: Path) -> pd.DataFrame:
    """Carrega o dataset CSV e valida se contém as colunas esperadas.
    
    O dataset é a base de dados para análise. Esta função garante que o arquivo
    existe e contém a estrutura esperada antes de processar os dados.
    
    Estrutura esperada do dataset:
    - id: Identificador único de cada relato (usado para rastreamento)
    - texto: Conteúdo textual do relato a ser analisado (campo principal)
    - setor: Setor/categoria do relato (usado para validação, se disponível)
    
    Args:
        path: Caminho para o arquivo CSV do dataset
        
    Returns:
        DataFrame do pandas com os dados carregados e validados
        
    Raises:
        ValueError: Se o dataset não contiver todas as colunas esperadas
                   Esta validação previne erros durante o processamento e
                   ajuda a identificar problemas de formato do dataset
    """
    df = pd.read_csv(path)
    expected_cols = {"id", "texto", "setor"}
    missing = expected_cols - set(df.columns)
    if missing:
        raise ValueError(f"Dataset missing columns: {sorted(missing)}")
    return df


def load_stopwords(path: Path) -> List[str]:
    """Carrega lista de stopwords do arquivo de texto.
    
    Stopwords são palavras comuns (como "o", "a", "de", "em") que geralmente
    não carregam informação semântica relevante e são filtradas na análise
    de termos. Embora o BERTopic tenha seu próprio processamento interno e
    não use diretamente esta lista de stopwords, mantemos esta função para
    consistência com outros scripts e para uso em análises auxiliares.
    
    O arquivo deve conter uma stopword por linha, com codificação UTF-8.
    Linhas vazias são automaticamente ignoradas.
    
    Args:
        path: Caminho para o arquivo de texto com uma stopword por linha
        
    Returns:
        Lista de strings contendo as stopwords (linhas vazias são ignoradas)
    """
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


# ============================================================================
# Funções de Análise de Texto
# ============================================================================

def summarize_cluster(top_terms: List[str], example: str) -> str:
    """Gera um resumo textual descritivo de um cluster/tópico.
    
    Esta função cria uma descrição legível combinando os termos mais relevantes
    com um exemplo representativo do cluster. O resumo facilita a interpretação
    humana dos resultados, permitindo que gestores e analistas entendam rapidamente
    o que cada tópico representa sem precisar examinar todos os textos.
    
    Estratégia de resumo:
    - Usa apenas os 3 primeiros termos para manter o resumo conciso e focado
    - Inclui um exemplo representativo para fornecer contexto
    - Trata casos especiais (sem termos) de forma clara
    
    Args:
        top_terms: Lista dos termos mais relevantes do cluster/tópico
                   Estes termos são extraídos pelo BERTopic usando c-TF-IDF,
                   que calcula a importância dos termos especificamente para
                   cada tópico, não para o corpus inteiro
        example: Texto exemplo representativo do cluster
                 Geralmente o primeiro texto do cluster, usado para fornecer
                 contexto sobre o tipo de conteúdo agrupado
        
    Returns:
        String com resumo descritivo do cluster em linguagem natural
    """
    if not top_terms:
        return "Cluster sem termos dominantes; relatos variados ou muito curtos."
    # Usa apenas os 3 primeiros termos para manter o resumo conciso
    # Mais termos tornariam o resumo verboso sem adicionar muito valor
    terms = ", ".join(top_terms[:3])
    return (
        f"Relatos focados em {terms}. "
        f"Exemplo representativo: \"{example}\"."
    )


def build_cluster_reports(
    texts: List[str],
    labels: np.ndarray,
    topic_terms: Dict[int, List[str]],
    noise_label: int | None = None,
) -> Tuple[List[ClusterReport], List[str]]:
    """Constrói relatórios detalhados para cada cluster/tópico identificado.
    
    Esta função processa os resultados do BERTopic e organiza as informações
    em estruturas padronizadas (ClusterReport) para facilitar análise e
    geração de relatórios. Ela agrupa textos por tópico, identifica exemplos
    representativos, e marca clusters genéricos ou incoerentes.
    
    Processo de construção:
    1. Agrupa textos por tópico (label)
    2. Para cada tópico, extrai termos relevantes (já fornecidos pelo BERTopic)
    3. Seleciona até 5 exemplos representativos
    4. Gera resumo descritivo
    5. Marca clusters genéricos/incoerentes baseado em critérios objetivos
    
    Critérios para marcar como genérico/incoerente:
    - Tópico de ruído (label == -1)
    - Tamanho muito pequeno (< 3 textos)
    - Ausência de termos distintivos
    
    Args:
        texts: Lista de textos originais (mesma ordem dos labels)
        labels: Array numpy com os labels de tópico para cada texto
                Gerado pelo BERTopic, pode incluir -1 para ruído
        topic_terms: Dicionário mapeando topic_id para lista dos termos mais
                     relevantes. Fornecido pelo BERTopic via c-TF-IDF, não
                     precisamos calcular via TF-IDF tradicional
        noise_label: Label usado para marcar ruído (geralmente -1), None se não aplicável
                     O BERTopic usa -1 para marcar textos que não se encaixam
                     em nenhum tópico identificado
        
    Returns:
        Tupla contendo:
        - Lista de ClusterReport, um para cada tópico encontrado (incluindo ruído)
        - Lista de strings com notas e observações sobre os tópicos
    """
    # Agrupa textos por tópico para análise individual
    clusters: Dict[int, List[str]] = {}
    for text, label in zip(texts, labels):
        clusters.setdefault(label, []).append(text)

    reports: List[ClusterReport] = []
    notes: List[str] = []
    # Processa cada tópico em ordem crescente de label para relatório organizado
    for label, cluster_texts in sorted(clusters.items(), key=lambda x: x[0]):
        # BERTopic já fornece os termos mais relevantes via c-TF-IDF
        # Não precisamos calcular via TF-IDF tradicional como nos outros pipelines
        top_terms = topic_terms.get(label, [])
        examples = cluster_texts[:5]  # Até 5 exemplos representativos
        summary = summarize_cluster(top_terms, examples[0]) if examples else "Sem exemplos."
        is_noise = noise_label is not None and label == noise_label
        # Marca como genérico/incoerente se for ruído, muito pequeno ou sem termos distintivos
        generic_or_incoherent = is_noise or len(cluster_texts) < 3 or not top_terms
        if is_noise:
            notes.append("Tópico -1 representa ruído/itens não atribuídos a nenhum tópico.")
        if generic_or_incoherent:
            notes.append(
                f"Tópico {label} marcado como genérico/incoerente "
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
# Funções de Clusterização com BERTopic
# ============================================================================


# Para usar um modelo específico, descomente UMA das linhas abaixo e modifique
# a função run_bertopic() para usar EMBEDDING_MODEL_NAME ao invés de language="portuguese"
#
# MODELOS SENTENCETRANSFORMER (RECOMENDADO):
# EMBEDDING_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"  # Leve, rápido, multilíngue
# EMBEDDING_MODEL_NAME = "paraphrase-multilingual-mpnet-base-v2"  # Melhor qualidade, multilíngue
EMBEDDING_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"	# rufimelo/bert-large-portuguese-cased-sts"
#paraphrase-multilingual-mpnet-base-v2
# MODELOS HUGGING FACE (via SentenceTransformer):
# EMBEDDING_MODEL_NAME = "neuralmind/bert-base-portuguese-cased"  # BERT base para PT-BR
# EMBEDDING_MODEL_NAME = "neuralmind/bert-large-portuguese-cased"  # BERT large para PT-BR
# EMBEDDING_MODEL_NAME = "pierreguillou/bert-base-cased-pt-lenerbr"  # BERT para NER em PT-BR
# EMBEDDING_MODEL_NAME = "bert-base-multilingual-cased"  # BERT multilíngue
# EMBEDDING_MODEL_NAME = "xlm-roberta-base"  # XLM-RoBERTa base (multilíngue)
# EMBEDDING_MODEL_NAME = "xlm-roberta-large"  # XLM-RoBERTa large (multilíngue, melhor qualidade)


def run_bertopic(texts: List[str], seed: int) -> Tuple[np.ndarray, Dict[int, List[str]]]:
    """Executa clusterização e modelagem de tópicos usando BERTopic."""
    
    # Importa SentenceTransformer
    from sentence_transformers import SentenceTransformer
    
    # Instancia o modelo com o nome CORRETO
    hf_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    
    # Configuração para dataset PEQUENO (50-200 textos)
    hdbscan_model = HDBSCAN(
        min_cluster_size=3,        # ⬅️ MÍNIMO possível
        min_samples=1,             # ⬅️ MÍNIMO possível
        cluster_selection_epsilon=0.5,  # ⬅️ IMPORTANTE: relaxa critério
        metric='euclidean'
    )
    
    umap_model = UMAP(
        n_neighbors=5,             # ⬅️ BAIXO: foco local
        n_components=3,            # ⬅️ BAIXO: menos compressão
        min_dist=0.0,
        metric='cosine'
    )
    
    # Configura o BERTopic com o modelo customizado e modelos de clusterização
    topic_model = BERTopic(
        embedding_model=hf_model,
        language=None,  # IMPORTANTE: None quando usar embedding_model customizado
        hdbscan_model=hdbscan_model,  # ⬅️ HDBSCAN configurado para dataset pequeno
        umap_model=umap_model,         # ⬅️ UMAP configurado para dataset pequeno
        calculate_probabilities=False,
        verbose=False,
        nr_topics=None,
    )
    
    # Executa o pipeline completo do BERTopic
    topics, _ = topic_model.fit_transform(texts)
    
    # Extrai os termos mais relevantes de cada tópico
    topic_terms: Dict[int, List[str]] = {}
    for topic_id in sorted(set(topics)):
        if topic_id == -1:
            topic_terms[topic_id] = []
            continue
        terms = [term for term, _ in topic_model.get_topic(topic_id)[:6]]
        topic_terms[topic_id] = terms
    
    return np.array(topics), topic_terms


def pipeline_bertopic(texts: List[str], stopwords: List[str]) -> Tuple[PipelineReport, np.ndarray, Dict[int, List[str]]]:
    """Pipeline completo de modelagem de tópicos usando BERTopic.
    
    Esta função orquestra a execução completa do pipeline BERTopic, incluindo:
    - Execução do BERTopic duas vezes (com seeds diferentes) para medir estabilidade
    - Cálculo de métricas (estabilidade via ARI, proporção de ruído)
    - Construção de relatórios detalhados para cada tópico
    - Organização dos resultados em estrutura padronizada
    
    Diferenças em relação aos outros pipelines (KMeans, HDBSCAN direto):
    - BERTopic gera seus próprios embeddings internamente, não usa embeddings
      compartilhados. Isso permite otimização específica para modelagem de tópicos
    - BERTopic determina automaticamente o número de tópicos, não requer k fixo
    - BERTopic combina múltiplas técnicas (UMAP + HDBSCAN + c-TF-IDF) em uma
      solução integrada, tornando-o mais "caixa-preta" mas também mais completo
    - BERTopic extrai termos representativos via c-TF-IDF, que é otimizado para
      modelagem de tópicos, diferente do TF-IDF tradicional usado em outros pipelines
    
    Processo de estabilidade:
    - Executa BERTopic duas vezes (com seeds diferentes para outras operações)
    - Compara resultados via Adjusted Rand Index (ARI)
    - ARI mede concordância entre duas clusterizações (1.0 = idêntico, 0.0 = aleatório)
    - Valores altos indicam que resultados são consistentes entre execuções
    
    Args:
        texts: Lista de textos originais a serem analisados
               Devem estar pré-processados (trim, lowercase) se desejado
        stopwords: Lista de stopwords (usado apenas para consistência)
                   O BERTopic tem seu próprio processamento interno e não usa
                   diretamente esta lista, mas mantemos o parâmetro para
                   consistência com outros pipelines e análises auxiliares
        
    Returns:
        Tupla contendo:
        - PipelineReport com resultados completos e métricas do pipeline BERTopic
          Inclui todos os tópicos identificados, métricas de estabilidade e ruído,
          e observações sobre os resultados
        - Array numpy com os labels de tópico para cada documento (execução primária)
        - Dicionário mapeando topic_id para lista dos termos mais relevantes (execução primária)
    """
    # BERTopic gera seus próprios embeddings internamente
    # Diferente dos outros pipelines que compartilham embeddings, o BERTopic
    # otimiza os embeddings especificamente para modelagem de tópicos
    # Isso pode resultar em embeddings diferentes, mas potencialmente melhores
    # para a tarefa específica de identificação de tópicos
    labels_primary, topic_terms_primary = run_bertopic(texts, SEED_PRIMARY)
    labels_secondary, topic_terms_secondary = run_bertopic(texts, SEED_SECONDARY)
    
    # Calcula estabilidade entre duas execuções
    # Adjusted Rand Index (ARI) mede a concordância entre duas clusterizações
    # - 1.0: Clusterizações idênticas (máxima estabilidade)
    # - 0.0: Clusterizações aleatórias (sem estabilidade)
    # - Valores negativos: Clusterizações piores que aleatório (raro)
    # Valores altos (> 0.7) indicam que o BERTopic produz resultados consistentes
    # Valores baixos podem indicar que os dados são muito heterogêneos ou que
    # os parâmetros precisam ser ajustados
    stability = adjusted_rand_score(labels_primary, labels_secondary)

    clusters: List[ClusterReport] = []
    notes: List[str] = [
        "BERTopic gera tópicos legíveis rápido, mas é mais caixa-preta e pesado.",
        "BERTopic combina embeddings, UMAP, HDBSCAN e c-TF-IDF em uma solução integrada.",
        "Número de tópicos é determinado automaticamente pelo algoritmo.",
    ]
    
    # Calcula proporção de ruído (tópico -1)
    # Ruído são textos que não se encaixam bem em nenhum tópico identificado
    # Uma proporção alta (> 30%) pode indicar:
    # - Dados muito heterogêneos
    # - Parâmetros do HDBSCAN muito restritivos
    # - Necessidade de ajuste dos hiperparâmetros do BERTopic
    noise_ratio = float(np.mean(labels_primary == -1))
    
    # Constrói relatórios para cada tópico identificado
    # Usamos os termos da primeira execução (primary) para consistência
    for label in sorted(set(labels_primary)):
        # Agrupa textos por tópico
        cluster_texts = [text for text, topic in zip(texts, labels_primary) if topic == label]
        # BERTopic já fornece os termos mais relevantes via c-TF-IDF
        # Não precisamos calcular via TF-IDF tradicional como nos outros pipelines
        # c-TF-IDF é otimizado para modelagem de tópicos, calculando a importância
        # dos termos especificamente para cada tópico, não para o corpus inteiro
        top_terms = topic_terms_primary.get(label, [])
        examples = cluster_texts[:5]  # Até 5 exemplos representativos
        summary = summarize_cluster(top_terms, examples[0]) if examples else "Sem exemplos."
        # Marca como genérico/incoerente se for ruído, muito pequeno ou sem termos distintivos
        generic_or_incoherent = label == -1 or len(cluster_texts) < 3 or not top_terms
        if label == -1:
            notes.append("Tópico -1 representa ruído/itens não atribuídos a nenhum tópico.")
        clusters.append(
            ClusterReport(
                label=label,
                size=len(cluster_texts),
                top_terms=top_terms,
                examples=examples,
                summary=summary,
                generic_or_incoherent=generic_or_incoherent,
            )
        )
    
    # Conta apenas clusters válidos (excluindo ruído)
    # O número de tópicos é determinado automaticamente pelo BERTopic baseado
    # na estrutura dos dados e parâmetros do HDBSCAN
    num_clusters = len({label for label in labels_primary if label != -1})
    
    report = PipelineReport(
        name="Pipeline BERTopic — Exploração rápida de tópicos",
        num_clusters=num_clusters,
        clusters=clusters,
        stability_ari=stability,
        noise_ratio=noise_ratio,
        notes=notes,
    )
    
    # Retorna o relatório junto com os labels e termos da execução primária
    # para permitir exportação CSV dos resultados
    return report, labels_primary, topic_terms_primary


# ============================================================================
# Funções de Formatação e Relatório
# ============================================================================

def format_cluster(cluster: ClusterReport) -> str:
    """Formata um ClusterReport em uma string legível para o relatório.
    
    Esta função converte a estrutura de dados ClusterReport em uma representação
    textual formatada em Markdown, facilitando a leitura e análise dos resultados.
    O formato é consistente e organizado, permitindo comparação rápida entre tópicos.
    
    Args:
        cluster: ClusterReport a ser formatado
                 Contém todas as informações sobre um tópico identificado
        
    Returns:
        String formatada com informações do cluster em Markdown
        Inclui label, tamanho, termos principais, exemplos, resumo e flag
        de coerência
    """
    terms = ", ".join(cluster.top_terms) if cluster.top_terms else "(sem termos fortes)"
    examples = "\n".join([f"      - {example}" for example in cluster.examples])
    return (
        f"    - Tópico {cluster.label} (n={cluster.size})\n"
        f"      • top termos: {terms}\n"
        f"      • exemplos:\n{examples}\n"
        f"      • resumo: {cluster.summary}\n"
        f"      • genérico/incoerente: {cluster.generic_or_incoherent}\n"
    )


def format_pipeline(report: PipelineReport) -> str:
    """Formata um PipelineReport completo em uma string legível.
    
    Esta função converte toda a estrutura PipelineReport em uma representação
    textual completa em Markdown, incluindo métricas, todos os tópicos identificados,
    e observações. O formato é projetado para ser legível tanto por humanos quanto
    por ferramentas de processamento de Markdown.
    
    Args:
        report: PipelineReport a ser formatado
                Contém todos os resultados e métricas do pipeline BERTopic
        
    Returns:
        String formatada com todas as informações do pipeline em Markdown
        Inclui nome, número de clusters, estabilidade, ruído, detalhes de cada
        tópico, e observações
    """
    clusters_text = "\n".join(format_cluster(cluster) for cluster in report.clusters)
    # Formata métricas opcionais (podem ser None)
    # ARI (Adjusted Rand Index) mede estabilidade entre execuções
    stability = (
        f"{report.stability_ari:.3f}" if report.stability_ari is not None else "n/a"
    )
    # Proporção de ruído indica quantos textos não se encaixam em tópicos
    noise_text = (
        f"{report.noise_ratio:.1%}" if report.noise_ratio is not None else "n/a"
    )
    notes = "\n".join([f"  - {note}" for note in report.notes])
    return (
        f"Pipeline: {report.name}\n"
        f"  - nº de tópicos: {report.num_clusters}\n"
        f"  - estabilidade (ARI entre duas execuções): {stability}\n"
        f"  - % de ruído (aprox.): {noise_text}\n"
        f"{clusters_text}\n"
        f"  - notas:\n{notes}\n"
    )


def build_report(report: PipelineReport) -> str:
    """Constrói o relatório final completo do pipeline BERTopic.
    
    Esta função gera o relatório final em Markdown contendo:
    - Resultados detalhados do pipeline BERTopic
    - Métricas de qualidade (estabilidade, ruído)
    - Análise de cada tópico identificado
    - Observações e insights sobre os resultados
    - Seção para decisões e próximos passos
    
    Diferente do script principal que compara múltiplos pipelines, este relatório
    foca exclusivamente no BERTopic, fornecendo análise mais detalhada e específica.
    
    Args:
        report: PipelineReport com todos os resultados do BERTopic
        
    Returns:
        String completa do relatório em formato Markdown
        Pronta para ser salva em arquivo ou exibida no console
    """
    # Formata o pipeline completo
    pipeline_text = format_pipeline(report)
    
    # Seção de insights específicos sobre o BERTopic
    insights = (
        "Insights sobre o BERTopic\n"
        "- BERTopic combina múltiplas técnicas (embeddings, UMAP, HDBSCAN, c-TF-IDF)\n"
        "- Número de tópicos é determinado automaticamente pelo algoritmo\n"
        "- Tópicos são mais interpretáveis que clusters de métodos tradicionais\n"
        "- Identifica ruído (textos que não se encaixam em tópicos)\n"
        "- Mais pesado computacionalmente, mas gera resultados mais legíveis\n"
        "- Menos controle sobre parâmetros individuais (mais caixa-preta)\n"
    )
    
    # Seção para preenchimento manual com decisões e próximos passos
    decisions = (
        "Decisão e Próximos Passos (preencher manualmente):\n"
        "- Qualidade dos tópicos identificados: ______________________________\n"
        "- Tópicos mais relevantes para o domínio: ____________________________\n"
        "- Ajustes necessários nos parâmetros: ________________________________\n"
        "- Próxima iteração sugerida:\n"
        "  - ___________________________________________\n"
        "  - ___________________________________________\n"
    )
    
    return f"{pipeline_text}\n\n{insights}\n{decisions}\n"


def export_clustering_csv(
    df: pd.DataFrame,
    labels: np.ndarray,
    topic_terms: Dict[int, List[str]],
    output_path: Path,
) -> None:
    """Exporta os resultados da clusterização para um arquivo CSV.
    
    Esta função cria um DataFrame com os resultados da clusterização e salva
    em formato CSV, permitindo análise posterior dos dados em ferramentas como
    Excel ou pandas. O CSV contém informações sobre cada documento e seu tópico
    atribuído, incluindo os termos mais relevantes do tópico.
    
    Estrutura do CSV gerado:
    - id: Identificador único do documento (do dataset original)
    - texto: Texto original do documento
    - setor: Setor/categoria do documento (do dataset original)
    - topic_id: ID do tópico/cluster atribuído pelo BERTopic (-1 para ruído)
    - top_terms: Termos mais relevantes do tópico (separados por vírgula)
    
    Args:
        df: DataFrame original com as colunas id, texto e setor
            Deve ter o mesmo número de linhas que o array labels
        labels: Array numpy com os labels de tópico para cada documento
                Gerado pelo BERTopic, pode incluir -1 para ruído
        topic_terms: Dicionário mapeando topic_id para lista dos termos mais
                     relevantes. Fornecido pelo BERTopic via c-TF-IDF
        output_path: Caminho onde o arquivo CSV será salvo
        
    Raises:
        ValueError: Se o número de labels não corresponder ao número de linhas do DataFrame
                   Esta validação previne erros durante a criação do DataFrame
    """
    # Valida que o número de labels corresponde ao número de documentos
    if len(labels) != len(df):
        raise ValueError(
            f"Número de labels ({len(labels)}) não corresponde ao número de "
            f"documentos no DataFrame ({len(df)})"
        )
    
    # Cria DataFrame com os dados originais
    result_df = df.copy()
    
    # Adiciona coluna com topic_id
    result_df["topic_id"] = labels
    
    # Adiciona coluna com top_terms (termos mais relevantes do tópico)
    # Para cada documento, busca os termos do seu tópico e junta com vírgula
    # Se o tópico for -1 (ruído), usa lista vazia
    result_df["top_terms"] = [
        ", ".join(topic_terms.get(topic_id, []))
        for topic_id in labels
    ]
    
    # Reordena colunas para facilitar leitura: id, texto, setor, topic_id, top_terms
    result_df = result_df[["id", "texto", "setor", "topic_id", "top_terms"]]
    
    # Salva CSV com encoding UTF-8 e sem índice
    result_df.to_csv(output_path, index=False, encoding="utf-8")


# ============================================================================
# Funções Principais
# ============================================================================

def parse_args() -> argparse.Namespace:
    """Parse dos argumentos de linha de comando.
    
    Esta função configura e processa os argumentos de linha de comando,
    permitindo customizar caminhos de entrada/saída e outros parâmetros.
    Todos os argumentos têm valores padrão baseados nas constantes globais,
    permitindo execução sem parâmetros para uso rápido e simples.
    
    Argumentos disponíveis:
    - --dataset: Caminho para o arquivo CSV do dataset
    - --output: Caminho para o arquivo de saída do relatório Markdown
    - --csv-output: Caminho para o arquivo CSV de saída com resultados da clusterização
    - --stopwords: Caminho para o arquivo de stopwords em português
    
    Returns:
        Namespace do argparse contendo todos os argumentos parseados
        Com valores padrão se não especificados na linha de comando
    """
    parser = argparse.ArgumentParser(
        description="E1 - BERTopic: Pipeline dedicado para modelagem de tópicos"
    )
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
        "--csv-output",
        type=Path,
        default=DEFAULT_CSV_OUTPUT,
        help="Arquivo CSV de saída com resultados da clusterização",
    )
    parser.add_argument(
        "--stopwords",
        type=Path,
        default=DEFAULT_STOPWORDS,
        help="Arquivo com stopwords pt-br (1 por linha)",
    )
    return parser.parse_args()


def main() -> None:
    """Função principal que orquestra a execução completa do experimento BERTopic.
    
    Esta função coordena todas as etapas do pipeline, desde o carregamento dos
    dados até a geração do relatório final. O fluxo é projetado para ser claro,
    reprodutível e fácil de entender.
    
    Fluxo de execução passo a passo:
    
    1. **Parse dos argumentos**: Processa argumentos de linha de comando ou usa
       valores padrão. Permite customização de caminhos sem modificar o código.
    
    2. **Configuração de seeds**: Define seeds para garantir reprodutibilidade
       parcial. Nota: BERTopic não aceita seed diretamente, então reprodutibilidade
       completa não é garantida, mas configurar seeds ajuda a reduzir variabilidade.
    
    3. **Carregamento de dados**: Carrega o dataset CSV e valida sua estrutura.
       O dataset deve conter as colunas: id, texto, setor.
    
    4. **Pré-processamento básico**: Aplica pré-processamento mínimo aos textos:
       - trim: Remove espaços em branco no início e fim
       - lowercase: Converte para minúsculas (opcional, mas recomendado)
       Este pré-processamento é intencionalmente mínimo para testar a capacidade
       do BERTopic de lidar com "texto sujo" sem limpeza agressiva.
    
    5. **Carregamento de stopwords**: Carrega lista de stopwords (usado para
       consistência, embora BERTopic tenha seu próprio processamento).
    
    6. **Execução do pipeline BERTopic**: Executa o pipeline completo que inclui:
       - Geração de embeddings via SentenceTransformer
       - Redução de dimensionalidade via UMAP
       - Clusterização via HDBSCAN
       - Extração de termos via c-TF-IDF
       O pipeline é executado duas vezes (com seeds diferentes) para medir estabilidade.
    
    7. **Geração do relatório**: Constrói relatório completo em Markdown contendo:
       - Métricas de qualidade (estabilidade, ruído)
       - Análise detalhada de cada tópico identificado
       - Observações e insights
       - Seção para decisões e próximos passos
    
    8. **Exportação CSV**: Exporta resultados da clusterização para CSV contendo:
       - Dados originais (id, texto, setor)
       - Tópico atribuído (topic_id)
       - Termos mais relevantes do tópico (top_terms)
    
    9. **Salvamento e exibição**: Salva o relatório em arquivo e também imprime
       no console para visualização imediata.
    
    Por que o BERTopic é executado separadamente:
    - BERTopic é mais pesado computacionalmente que KMeans/HDBSCAN direto
    - Gera seus próprios embeddings, não compartilha com outros pipelines
    - Requer biblioteca adicional (bertopic) que pode não estar sempre disponível
    - Execução separada permite análise focada sem sobrecarregar o script principal
    
    Como os dados são processados:
    - Textos são pré-processados minimamente (trim + lowercase)
    - BERTopic processa internamente: tokenização, embeddings, redução dimensional,
      clusterização, e extração de termos
    - Resultados são organizados em estruturas padronizadas para análise
    
    Estrutura do relatório gerado:
    - Informações do pipeline (nome, métricas)
    - Detalhes de cada tópico (termos, exemplos, resumo)
    - Observações sobre qualidade e coerência
    - Insights sobre o BERTopic
    - Seção para decisões manuais
    """
    # Parse dos argumentos de linha de comando
    # Permite customizar caminhos sem modificar o código
    args = parse_args()
    
    # Define seed para garantir reprodutibilidade parcial
    # Nota: BERTopic não aceita seed diretamente, mas configurar seeds para
    # outras operações (numpy) ajuda a reduzir variabilidade
    set_seed(SEED_PRIMARY)
    
    # Carrega dataset e valida estrutura
    # O dataset deve conter as colunas: id, texto, setor
    # A validação previne erros durante o processamento
    df = load_dataset(args.dataset)
    
    # Pré-processamento mínimo: apenas trim e lowercase
    # Este pré-processamento é intencionalmente mínimo para testar a capacidade
    # do BERTopic de lidar com "texto sujo" sem limpeza agressiva
    # O BERTopic tem seu próprio processamento interno que pode lidar com
    # variações de formatação, mas um pré-processamento básico ajuda
    texts = df["texto"].astype(str).str.strip().str.lower().tolist()
    
    # Carrega stopwords (usado para consistência, embora BERTopic tenha
    # seu próprio processamento interno)
    stopwords = load_stopwords(args.stopwords)
    
    # Executa pipeline BERTopic completo
    # O BERTopic gera seus próprios embeddings internamente, diferente dos
    # outros pipelines que compartilham embeddings. Isso permite otimização
    # específica para modelagem de tópicos, mas também significa que não
    # podemos reutilizar embeddings de outros pipelines
    # O pipeline retorna o relatório, os labels e os termos dos tópicos
    report, labels, topic_terms = pipeline_bertopic(texts, stopwords)
    
    # Gera relatório final e salva em arquivo
    # O relatório contém análise detalhada dos tópicos identificados, métricas
    # de qualidade, e insights sobre os resultados
    report_text = build_report(report)
    args.output.write_text(report_text, encoding="utf-8")
    
    # Exporta resultados da clusterização para CSV
    # O CSV contém id, texto, setor, topic_id e top_terms para cada documento
    # Permite análise posterior dos dados em ferramentas como Excel ou pandas
    export_clustering_csv(df, labels, topic_terms, args.csv_output)
    
    # Também imprime no console para visualização imediata
    # Útil para ver resultados rapidamente sem abrir o arquivo
    print(report_text)


if __name__ == "__main__":
    main()
