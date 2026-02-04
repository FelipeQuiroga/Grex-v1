from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import pandas as pd


REQUIRED_COLUMNS = ["texto", "topic_id"]


def load_csv(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"CSV missing required columns: {missing}")
    return df


def normalize_text(value: str) -> str:
    if not isinstance(value, str):
        value = "" if pd.isna(value) else str(value)
    normalized = " ".join(value.strip().split())
    return normalized


def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["texto"] = df["texto"].apply(normalize_text)
    if "top_terms" in df.columns:
        df["top_terms"] = df["top_terms"].fillna("").apply(normalize_text)
    if "setor" in df.columns:
        df["setor"] = df["setor"].fillna("").apply(normalize_text)
    return df


def filter_dataframe(
    df: pd.DataFrame,
    *,
    min_relato_len: int,
    drop_noise: bool,
) -> pd.DataFrame:
    filtered = df[df["texto"].str.len() >= min_relato_len]
    if drop_noise and "topic_id" in filtered.columns:
        filtered = filtered[filtered["topic_id"] != -1]
    return filtered


def ensure_output_dir(path: str | Path) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: str | Path, payload: dict) -> None:
    path = Path(path)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_text(path: str | Path, content: str) -> None:
    path = Path(path)
    path.write_text(content, encoding="utf-8")


def validate_min_columns(df: pd.DataFrame, required: Iterable[str]) -> None:
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
