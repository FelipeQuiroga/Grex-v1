from __future__ import annotations

import json
from typing import Iterable


VALID_CONFIDENCE = {"alta", "media", "baixa"}
VALID_STATUS = {"OK", "REVISAR", "EMERGENTE"}


def _count_themes(taxonomy: dict) -> int:
    themes = taxonomy.get("themes", [])
    unique = {(theme.get("macrotheme"), theme.get("theme")) for theme in themes}
    return len([pair for pair in unique if all(pair)])


def _extract_emergent_names(payload: dict) -> set[str]:
    emergent = payload.get("emergent_themes", [])
    return {item.get("name", "") for item in emergent if item.get("name")}


def parse_json(raw: str) -> tuple[dict | None, list[str]]:
    try:
        payload = json.loads(raw)
        return payload, []
    except json.JSONDecodeError as exc:
        return None, [f"JSON inválido: {exc}"]


def validate_payload(
    payload: dict,
    *,
    topic_ids: Iterable[int],
    rules: dict,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["Payload deve ser um objeto JSON."]

    taxonomy = payload.get("taxonomy")
    if not isinstance(taxonomy, dict):
        errors.append("Campo taxonomy ausente ou inválido.")

    mappings = payload.get("mappings")
    if not isinstance(mappings, list):
        errors.append("Campo mappings ausente ou inválido.")

    emergent = payload.get("emergent_themes")
    if emergent is None:
        errors.append("Campo emergent_themes ausente.")

    if errors:
        return errors

    themes_count = _count_themes(taxonomy)
    if themes_count < rules["themes_min"] or themes_count > rules["themes_max"]:
        errors.append(
            f"Quantidade de temas ({themes_count}) fora do intervalo "
            f"{rules['themes_min']}–{rules['themes_max']}."
        )

    mapping_ids = []
    for mapping in mappings:
        if not isinstance(mapping, dict):
            errors.append("Cada mapping deve ser um objeto JSON.")
            continue
        if mapping.get("confidence") not in VALID_CONFIDENCE:
            errors.append(f"Confiança inválida para topic_id {mapping.get('topic_id')}.")
        if mapping.get("status") not in VALID_STATUS:
            errors.append(f"Status inválido para topic_id {mapping.get('topic_id')}.")
        if "topic_id" not in mapping:
            errors.append("Mapping sem topic_id.")
        else:
            mapping_ids.append(int(mapping["topic_id"]))

    missing_ids = sorted(set(topic_ids) - set(mapping_ids))
    if missing_ids:
        errors.append(f"Tópicos sem mapeamento: {missing_ids}")

    extra_ids = sorted(set(mapping_ids) - set(topic_ids))
    if extra_ids:
        errors.append(f"Tópicos inesperados no mapeamento: {extra_ids}")

    emergent_names = _extract_emergent_names(payload)
    for mapping in mappings:
        if mapping.get("status") == "EMERGENTE":
            theme_name = mapping.get("theme")
            if theme_name not in emergent_names:
                errors.append(
                    f"Tema emergente '{theme_name}' não listado em emergent_themes."
                )
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
