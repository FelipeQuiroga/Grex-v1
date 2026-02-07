from __future__ import annotations

import hashlib
from collections import Counter
from typing import Iterable

import pandas as pd


def _split_terms(terms: str) -> list[str]:
    if not terms:
        return []
    separators = [",", ";", "|", "/"]
    normalized = terms
    for sep in separators:
        normalized = normalized.replace(sep, ",")
    return [term.strip() for term in normalized.split(",") if term.strip()]


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _deterministic_sample(texts: Iterable[str], size: int) -> list[str]:
    items = sorted({text: _hash_text(text) for text in texts}.items(), key=lambda x: x[1])
    return [text for text, _ in items[:size]]


def _extract_top_terms(values: Iterable[str], top_k: int) -> list[str]:
    counter: Counter[str] = Counter()
    for value in values:
        for term in _split_terms(value):
            counter[term.lower()] += 1
    most_common = [term for term, _ in counter.most_common(top_k)]
    return most_common


def aggregate_topics(
    df: pd.DataFrame,
    *,
    examples_per_topic: int,
    top_terms_k: int,
    sample_method: str = "hash",
) -> dict:
    total = len(df)
    topics_payload = []
    for topic_id, group in df.groupby("topic_id"):
        volume = len(group)
        share_pct = round(volume / total, 4) if total else 0.0
        top_terms = []
        if "top_terms" in group.columns:
            top_terms = _extract_top_terms(group["top_terms"].tolist(), top_terms_k)
        examples_source = group["texto"].tolist()
        if sample_method == "head":
            examples = examples_source[:examples_per_topic]
        else:
            examples = _deterministic_sample(examples_source, examples_per_topic)
        sector = ""
        if "setor" in group.columns:
            sector_counts = group["setor"].value_counts()
            if not sector_counts.empty:
                sector = sector_counts.index[0]
        topics_payload.append(
            {
                "topic_id": int(topic_id),
                "volume_relatos": int(volume),
                "share_pct": share_pct,
                "top_terms": top_terms,
                "setor": sector,
                "examples": examples,
            }
        )
    topics_payload = sorted(topics_payload, key=lambda item: item["topic_id"])
    return {
        "total_relatos": int(total),
        "topics": topics_payload,
    }
