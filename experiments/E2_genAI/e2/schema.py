from __future__ import annotations

import json
from typing import Iterable


VALID_CONFIDENCE = {"HIGH", "MEDIUM", "LOW"}
VALID_STATUS = {"OK", "REVISAR", "EMERGENTE"}


def parse_json(raw: str) -> tuple[dict | None, list[str]]:
    try:
        payload = json.loads(raw)
        return payload, []
    except json.JSONDecodeError as exc:
        return None, [f"JSON invalido: {exc}"]


def _as_int_topic_id(value: object) -> tuple[int | None, str | None]:
    if isinstance(value, bool):
        return None, "topic_id invalido: boolean nao e aceito."
    try:
        return int(value), None
    except (TypeError, ValueError):
        return None, f"topic_id invalido: {value!r}"


def validate_payload(
    payload: dict,
    *,
    topic_ids: Iterable[int],
    rules: dict,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["Payload deve ser um objeto JSON."]

    allowed_top_level = {"mappings"}
    top_level_keys = set(payload.keys())
    extra_top_level = sorted(top_level_keys - allowed_top_level)
    if extra_top_level:
        errors.append(
            f"Campos de topo nao permitidos: {extra_top_level}. Use apenas 'mappings'."
        )

    mappings = payload.get("mappings")
    if not isinstance(mappings, list):
        errors.append("Campo mappings ausente ou invalido.")
        return errors

    macro_taxonomy = rules["macro_taxonomy"]
    forbid_new_macrothemes = bool(rules.get("forbid_new_macrothemes", True))
    thresholds = rules.get("thresholds", {})
    confidence_low_threshold = thresholds.get("confidence_low_threshold", "LOW")
    allowed_macrothemes = set(macro_taxonomy)

    expected_keys = {"topic_id", "macro_theme", "confidence", "status"}
    mapping_ids: list[int] = []
    for mapping in mappings:
        if not isinstance(mapping, dict):
            errors.append("Cada mapping deve ser um objeto JSON.")
            continue

        extra_keys = sorted(set(mapping.keys()) - expected_keys)
        if extra_keys:
            errors.append(
                f"Campos extras no mapping de topic_id {mapping.get('topic_id')}: {extra_keys}"
            )

        missing_keys = sorted(expected_keys - set(mapping.keys()))
        if missing_keys:
            errors.append(
                f"Campos obrigatorios ausentes no mapping de topic_id {mapping.get('topic_id')}: {missing_keys}"
            )
            continue

        topic_id, topic_error = _as_int_topic_id(mapping.get("topic_id"))
        if topic_error:
            errors.append(topic_error)
        else:
            mapping_ids.append(topic_id)

        macro_theme = mapping.get("macro_theme")
        if not isinstance(macro_theme, str) or not macro_theme.strip():
            errors.append(f"macro_theme invalido para topic_id {mapping.get('topic_id')}.")
        elif forbid_new_macrothemes and macro_theme not in allowed_macrothemes:
            errors.append(
                f"Macrotema invalido para topic_id {mapping.get('topic_id')}: '{macro_theme}'."
            )

        if mapping.get("confidence") not in VALID_CONFIDENCE:
            errors.append(f"Confianca invalida para topic_id {mapping.get('topic_id')}.")

        if mapping.get("status") not in VALID_STATUS:
            errors.append(f"Status invalido para topic_id {mapping.get('topic_id')}.")
        elif mapping.get("status") == "EMERGENTE" and mapping.get(
            "confidence"
        ) != confidence_low_threshold:
            errors.append(
                f"topic_id {mapping.get('topic_id')} marcado como EMERGENTE sem confidence {confidence_low_threshold}."
            )

    duplicate_ids = sorted(
        topic_id for topic_id in set(mapping_ids) if mapping_ids.count(topic_id) > 1
    )
    if duplicate_ids:
        errors.append(f"topic_ids duplicados no mapeamento: {duplicate_ids}")

    topic_ids_set = set(topic_ids)
    missing_ids = sorted(topic_ids_set - set(mapping_ids))
    if missing_ids:
        errors.append(f"Topicos sem mapeamento: {missing_ids}")

    extra_ids = sorted(set(mapping_ids) - topic_ids_set)
    if extra_ids:
        errors.append(f"Topicos inesperados no mapeamento: {extra_ids}")

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
