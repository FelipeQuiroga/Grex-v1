from __future__ import annotations

import json
from pathlib import Path

import yaml

from e2.aggregate import aggregate_topics
from e2.io import (
    ensure_output_dir,
    filter_dataframe,
    load_csv,
    normalize_dataframe,
    write_json,
    write_text,
)
from e2.llm_client import LLMClient, LLMConfig, generate_with_retry
from e2.postprocess import compute_metrics
from e2.prompt_builder import build_prompt, build_repair_prompt
from e2.schema import parse_and_validate
from e2.versioning import create_run_dir, generate_run_id, write_manifest


def load_config(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def run_pipeline(config_path: str | Path) -> int:
    config = load_config(config_path)
    run_id = generate_run_id()
    outputs_dir = ensure_output_dir(config["run"]["outputs_base_dir"])
    run_dir = create_run_dir(outputs_dir, run_id)

    df = load_csv(config["source"]["e1_csv_path"])
    df = normalize_dataframe(df)
    df = filter_dataframe(
        df,
        min_relato_len=config["aggregation"]["min_relato_len"],
        drop_noise=config["aggregation"]["drop_noise"],
    )

    topics_payload = aggregate_topics(
        df,
        examples_per_topic=config["aggregation"]["examples_per_topic"],
        top_terms_k=config["aggregation"]["top_terms_k"],
        sample_method=config["aggregation"]["sample_method"],
    )
    write_json(run_dir / "input_topics.json", topics_payload)

    prompt = build_prompt(topics_payload, config["rules"])
    write_text(run_dir / "prompt.txt", prompt)

    llm_config = LLMConfig(
        provider=config["llm"]["provider"],
        model=config["llm"]["model"],
        timeout_sec=config["llm"]["timeout_sec"],
        retries=config["llm"]["retries"],
    )
    client = LLMClient(llm_config)
    raw_response = ""
    validated = None
    errors: list[str] = []
    topic_ids = [topic["topic_id"] for topic in topics_payload["topics"]]
    try:
        raw_response, _ = generate_with_retry(client, prompt, llm_config.retries)
        write_text(run_dir / "llm_raw.txt", raw_response)
        validated, errors = parse_and_validate(
            raw_response, topic_ids=topic_ids, rules=config["rules"]
        )
    except Exception as exc:
        errors = [f"Falha na chamada LLM: {exc}"]

    if errors and raw_response:
        repair_prompt = build_repair_prompt(raw_response, errors)
        write_text(run_dir / "prompt_repair.txt", repair_prompt)
        try:
            repair_response, _ = generate_with_retry(client, repair_prompt, 0)
            write_text(run_dir / "llm_raw_retry.txt", repair_response)
            validated, errors = parse_and_validate(
                repair_response, topic_ids=topic_ids, rules=config["rules"]
            )
        except Exception as exc:
            errors = errors + [f"Falha no repair prompt: {exc}"]

    status = "SUCCESS" if not errors else "FAILED"
    if validated:
        write_json(run_dir / "result.json", validated)
        metrics = compute_metrics(validated, topics_payload)
        write_json(run_dir / "metrics.json", metrics)
    if errors:
        write_text(run_dir / "validation_errors.txt", json.dumps(errors, indent=2))

    write_manifest(run_dir, config, status)
    return 0 if status == "SUCCESS" else 1


if __name__ == "__main__":
    raise SystemExit(run_pipeline(Path(__file__).parent / "config.yaml"))
