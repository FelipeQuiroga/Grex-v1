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


DEFAULT_DATASET = (
    Path(__file__).resolve().parents[1] / "E0_dataset_goldset" / "dataset.csv"
)
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "output_report.md"
DEFAULT_STOPWORDS = (
    Path(__file__).resolve().parents[1] / "E0_dataset_goldset" / "stopwords_ptbr.txt"
)
MODEL_NAME = "all-MiniLM-L6-v2"
KMEANS_K = 6
SEED_PRIMARY = 42
SEED_SECONDARY = 99


@dataclass
class ClusterReport:
    label: int
    size: int
    top_terms: List[str]
    examples: List[str]
    summary: str
    generic_or_incoherent: bool


@dataclass
class PipelineReport:
    name: str
    num_clusters: int
    clusters: List[ClusterReport]
    stability_ari: float | None
    noise_ratio: float | None
    notes: List[str]


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


def load_dataset(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    expected_cols = {"id", "texto", "setor"}
    missing = expected_cols - set(df.columns)
    if missing:
        raise ValueError(f"Dataset missing columns: {sorted(missing)}")
    return df


def build_embeddings(texts: List[str]) -> np.ndarray:
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(
        texts,
        show_progress_bar=False,
        normalize_embeddings=True,
    )
    return np.array(embeddings)


def load_stopwords(path: Path) -> List[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def top_terms_for_texts(
    texts: List[str],
    stopwords: List[str],
    top_n: int = 6,
) -> List[str]:
    if not texts:
        return []
    vectorizer = TfidfVectorizer(
        stop_words=stopwords,
        ngram_range=(1, 2),
        max_features=50,
    )
    tfidf = vectorizer.fit_transform(texts)
    if tfidf.shape[1] == 0:
        return []
    mean_scores = np.asarray(tfidf.mean(axis=0)).ravel()
    indices = np.argsort(mean_scores)[::-1][:top_n]
    terms = vectorizer.get_feature_names_out()
    return [terms[i] for i in indices if mean_scores[i] > 0]


def summarize_cluster(top_terms: List[str], example: str) -> str:
    if not top_terms:
        return "Cluster sem termos dominantes; relatos variados ou muito curtos."
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
    clusters: Dict[int, List[str]] = {}
    for text, label in zip(texts, labels):
        clusters.setdefault(label, []).append(text)

    reports: List[ClusterReport] = []
    notes: List[str] = []
    for label, cluster_texts in sorted(clusters.items(), key=lambda x: x[0]):
        top_terms = top_terms_for_texts(cluster_texts, stopwords)
        examples = cluster_texts[:5]
        summary = summarize_cluster(top_terms, examples[0])
        is_noise = noise_label is not None and label == noise_label
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


def run_kmeans(embeddings: np.ndarray, seed: int) -> np.ndarray:
    kmeans = KMeans(n_clusters=KMEANS_K, random_state=seed, n_init=10)
    return kmeans.fit_predict(embeddings)


def run_hdbscan(embeddings: np.ndarray) -> np.ndarray:
    clusterer = hdbscan.HDBSCAN(min_cluster_size=5, min_samples=2)
    return clusterer.fit_predict(embeddings)


def run_bertopic(texts: List[str], seed: int) -> Tuple[np.ndarray, Dict[int, List[str]]]:
    from bertopic import BERTopic

    topic_model = BERTopic(
        language="portuguese",
        calculate_probabilities=False,
        verbose=False,
        nr_topics=None,
        seed=seed,
    )
    topics, _ = topic_model.fit_transform(texts)
    topic_terms: Dict[int, List[str]] = {}
    for topic_id in sorted(set(topics)):
        if topic_id == -1:
            topic_terms[topic_id] = []
            continue
        terms = [term for term, _ in topic_model.get_topic(topic_id)[:6]]
        topic_terms[topic_id] = terms
    return np.array(topics), topic_terms


def pipeline_a(
    texts: List[str],
    embeddings: np.ndarray,
    stopwords: List[str],
) -> PipelineReport:
    labels_primary = run_kmeans(embeddings, SEED_PRIMARY)
    labels_secondary = run_kmeans(embeddings, SEED_SECONDARY)
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
        noise_ratio=None,
        notes=notes,
    )


def pipeline_b(
    texts: List[str],
    embeddings: np.ndarray,
    stopwords: List[str],
) -> PipelineReport:
    labels_primary = run_hdbscan(embeddings)
    clusters, notes = build_cluster_reports(texts, labels_primary, stopwords, noise_label=-1)
    num_clusters = len({label for label in labels_primary if label != -1})
    noise_ratio = float(np.mean(labels_primary == -1))
    notes.append(
        "HDBSCAN identifica clusters densos e marca itens dispersos como ruído (-1)."
    )
    notes.append("Estabilidade deve ser avaliada qualitativamente via ruído e coerência.")
    return PipelineReport(
        name="Pipeline B — Densidade e ruído (HDBSCAN)",
        num_clusters=num_clusters,
        clusters=clusters,
        stability_ari=None,
        noise_ratio=noise_ratio,
        notes=notes,
    )


def pipeline_c(texts: List[str], stopwords: List[str]) -> PipelineReport:
    labels_primary, topic_terms = run_bertopic(texts, SEED_PRIMARY)
    labels_secondary, _ = run_bertopic(texts, SEED_SECONDARY)
    stability = adjusted_rand_score(labels_primary, labels_secondary)

    clusters: List[ClusterReport] = []
    notes: List[str] = [
        "BERTopic gera tópicos legíveis rápido, mas é mais caixa-preta e pesado."
    ]
    noise_ratio = float(np.mean(labels_primary == -1))
    for label in sorted(set(labels_primary)):
        cluster_texts = [text for text, topic in zip(texts, labels_primary) if topic == label]
        top_terms = topic_terms.get(label, [])
        examples = cluster_texts[:5]
        summary = summarize_cluster(top_terms, examples[0]) if examples else "Sem exemplos."
        generic_or_incoherent = label == -1 or len(cluster_texts) < 3 or not top_terms
        if label == -1:
            notes.append("Topic -1 representa ruído/itens não atribuídos.")
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
    num_clusters = len({label for label in labels_primary if label != -1})
    return PipelineReport(
        name="Pipeline C — Exploração rápida (BERTopic)",
        num_clusters=num_clusters,
        clusters=clusters,
        stability_ari=stability,
        noise_ratio=noise_ratio,
        notes=notes,
    )


def format_cluster(cluster: ClusterReport) -> str:
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
    clusters_text = "\n".join(format_cluster(cluster) for cluster in report.clusters)
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
    comparison = (
        "Comparação e Insights\n"
        "- KMeans tende a gerar temas consistentes e explicáveis.\n"
        "- HDBSCAN destaca ruído, útil para ver itens fora do padrão.\n"
        "- BERTopic acelera geração de tópicos, mas adiciona complexidade.\n"
        "- Avalie: quais clusters são mais explicáveis para um gestor.\n"
        "- Avalie: qual pipeline mistura menos temas distintos.\n"
        "- Avalie: qual parece mais simples de manter no MVP.\n"
        "- Avalie: trade-offs claros entre qualidade e complexidade.\n"
    )
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


def parse_args() -> argparse.Namespace:
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
    parser.add_argument(
        "--run-bertopic",
        action="store_true",
        help="Executa o Pipeline C (BERTopic)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    set_seed(SEED_PRIMARY)
    df = load_dataset(args.dataset)
    texts = df["texto"].astype(str).str.strip().str.lower().tolist()
    stopwords = load_stopwords(args.stopwords)

    embeddings = build_embeddings(texts)
    reports = [
        pipeline_a(texts, embeddings, stopwords),
        pipeline_b(texts, embeddings, stopwords),
    ]
    if args.run_bertopic:
        reports.append(pipeline_c(texts, stopwords))

    report_text = build_report(reports)
    args.output.write_text(report_text, encoding="utf-8")
    print(report_text)


if __name__ == "__main__":
    main()
