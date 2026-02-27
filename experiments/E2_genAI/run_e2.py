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

    # --- INÍCIO DA REFATORAÇÃO DE BATCHING ---
    llm_config = LLMConfig(
        provider=config["llm"]["provider"],
        model=config["llm"]["model"],
        timeout_sec=config["llm"]["timeout_sec"],
        retries=config["llm"]["retries"],
    )
    client = LLMClient(llm_config)
    
    all_topics = topics_payload["topics"]
    batch_size = config["llm"].get("batch_size", 20) # Recomendado entre 10 e 20
    
    final_mappings = []
    global_errors = []
    
    # Fatiando a lista de tópicos em lotes
    for i in range(0, len(all_topics), batch_size):
        batch_topics = all_topics[i : i + batch_size]
        batch_payload = {"topics": batch_topics}
        batch_topic_ids = [t["topic_id"] for t in batch_topics]
        
        prompt = build_prompt(batch_payload, config["rules"])
        
        # Salva prompts por batch para debug (opcional)
        write_text(run_dir / f"prompt_batch_{i}.txt", prompt)

        batch_validated = None
        batch_errors = []
        
        try:
            raw_response, _ = generate_with_retry(client, prompt, llm_config.retries)
            batch_validated, batch_errors = parse_and_validate(
                raw_response, topic_ids=batch_topic_ids, rules=config["rules"]
            )
        except Exception as exc:
            batch_errors = [f"Falha na chamada LLM (Batch {i}): {exc}"]

        # Lógica de Repair para o Batch atual
        if batch_errors and raw_response:
            repair_prompt = build_repair_prompt(raw_response, batch_errors)
            try:
                repair_response, _ = generate_with_retry(client, repair_prompt, 0)
                batch_validated, batch_errors = parse_and_validate(
                    repair_response, topic_ids=batch_topic_ids, rules=config["rules"]
                )
            except Exception as exc:
                batch_errors = batch_errors + [f"Falha no repair prompt (Batch {i}): {exc}"]

        # Consolidando resultados ou erros
        if batch_validated and not batch_errors:
            final_mappings.extend(batch_validated["mappings"])
        else:
            global_errors.extend(batch_errors)

    # --- FIM DA REFATORAÇÃO DE BATCHING ---

    status = "SUCCESS" if not global_errors else "FAILED"
    
    if final_mappings:
        # Remonta o payload validado completo no formato esperado
        consolidated_result = {"mappings": final_mappings}
        write_json(run_dir / "result.json", consolidated_result)
        
        metrics = compute_metrics(consolidated_result, topics_payload, config["rules"])
        write_json(run_dir / "metrics.json", metrics)
        
    if global_errors:
        write_text(run_dir / "validation_errors.txt", json.dumps(global_errors, indent=2))

    write_manifest(run_dir, config, status)
    return 0 if status == "SUCCESS" else 1


if __name__ == "__main__":
    raise SystemExit(run_pipeline(Path(__file__).parent / "config.yaml"))
