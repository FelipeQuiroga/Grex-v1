from __future__ import annotations

import json
import re
from typing import Iterable


def parse_json(raw: str) -> tuple[dict | None, list[str]]:
    cleaned_text = raw.strip()

    if "```" in cleaned_text:
        match = re.search(r"```(?:json)?(.*?)```", cleaned_text, re.DOTALL | re.IGNORECASE)
        if match:
            cleaned_text = match.group(1).strip()
    else:
        match = re.search(r"(\{.*\})", cleaned_text, re.DOTALL)
        if match:
            cleaned_text = match.group(1).strip()

    try:
        payload = json.loads(cleaned_text)
        return payload, []
    except json.JSONDecodeError as exc:
        return None, [f"JSON invalido: {exc}", f"raw text: {cleaned_text!r}"]


def _as_int_topic_id(value: object) -> tuple[int | None, str | None]:
    if isinstance(value, bool):
        return None, "topic_id invalido: boolean nao e aceito."
    try:
        return int(value), None
    except (TypeError, ValueError):
        return None, f"topic_id invalido: {value!r}"


def _allowed_macrothemes(rules: dict) -> set[str]:
    taxonomy = rules.get("taxonomy")
    if isinstance(taxonomy, dict) and taxonomy:
        return set(taxonomy.keys())
    macro_taxonomy = rules.get("macro_taxonomy", [])
    return set(macro_taxonomy)


def validate_payload(
    payload: dict,
    *,
    topic_ids: Iterable[int],
    rules: dict,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["Payload deve ser um objeto JSON."]

    allowed_top_level = {"classifications"}
    top_level_keys = set(payload.keys())
    extra_top_level = sorted(top_level_keys - allowed_top_level)
    if extra_top_level:
        errors.append(
            f"Campos de topo nao permitidos: {extra_top_level}. Use apenas 'classifications'."
        )

    classifications = payload.get("classifications")
    if not isinstance(classifications, list):
        errors.append("Campo classifications ausente ou invalido.")
        return errors

    forbid_new_macrothemes = bool(rules.get("forbid_new_macrothemes", True))
    allowed_macrothemes = _allowed_macrothemes(rules)

    expected_keys = {"topic_id", "macro_theme", "rationale"}
    mapping_ids: list[int] = []
    for item in classifications:
        if not isinstance(item, dict):
            errors.append("Cada classificacao deve ser um objeto JSON.")
            continue

        extra_keys = sorted(set(item.keys()) - expected_keys)
        if extra_keys:
            errors.append(
                f"Campos extras na classificacao de topic_id {item.get('topic_id')}: {extra_keys}"
            )

        missing_keys = sorted(expected_keys - set(item.keys()))
        if missing_keys:
            errors.append(
                "Campos obrigatorios ausentes na classificacao de "
                f"topic_id {item.get('topic_id')}: {missing_keys}"
            )
            continue

        topic_id, topic_error = _as_int_topic_id(item.get("topic_id"))
        if topic_error:
            errors.append(topic_error)
        else:
            mapping_ids.append(topic_id)

        macro_theme = item.get("macro_theme")
        if not isinstance(macro_theme, str) or not macro_theme.strip():
            errors.append(f"macro_theme invalido para topic_id {item.get('topic_id')}.")
        elif forbid_new_macrothemes and macro_theme not in allowed_macrothemes:
            errors.append(
                f"Macrotema invalido para topic_id {item.get('topic_id')}: '{macro_theme}'."
            )

        rationale = item.get("rationale")
        if not isinstance(rationale, str) or not rationale.strip():
            errors.append(f"rationale invalido para topic_id {item.get('topic_id')}.")
        elif len(rationale) > 280:
            errors.append(
                f"rationale muito longo para topic_id {item.get('topic_id')} (max 280 chars)."
            )

    duplicate_ids = sorted(
        topic_id for topic_id in set(mapping_ids) if mapping_ids.count(topic_id) > 1
    )
    if duplicate_ids:
        errors.append(f"topic_ids duplicados no mapeamento: {duplicate_ids}")

    topic_ids_set = set(topic_ids)
    missing_ids = sorted(topic_ids_set - set(mapping_ids))
    if missing_ids:
        errors.append(f"Topicos sem classificacao: {missing_ids}")

    extra_ids = sorted(set(mapping_ids) - topic_ids_set)
    if extra_ids:
        errors.append(f"Topicos inesperados na classificacao: {extra_ids}")

    return errors


def parse_and_validate(
    raw: str,
    *,
    topic_ids: Iterable[int],
    rules: dict,
) -> tuple[dict | None, list[str]]:
    payload, parse_errors = parse_json(raw)
    if parse_errors:
        return None, parse_errors
    errors = validate_payload(payload, topic_ids=topic_ids, rules=rules)
    if errors:
        return None, errors
    return payload, []
