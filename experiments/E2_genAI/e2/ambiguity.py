from __future__ import annotations

import unicodedata


def _normalize_text(value: str) -> str:
    if not isinstance(value, str):
        value = str(value)
    normalized = unicodedata.normalize("NFKD", value)
    stripped = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    return stripped.lower()


def _match_count(terms: list[str], source_text: str) -> int:
    normalized_source = _normalize_text(source_text)
    return sum(1 for term in terms if _normalize_text(term) in normalized_source)


def _topic_source_text(topic_info: dict) -> str:
    chunks: list[str] = []
    chunks.extend(topic_info.get("top_terms", []))
    chunks.extend(topic_info.get("examples", []))
    contexto = topic_info.get("contexto_operacional", {})
    chunks.extend(contexto.get("salient_terms", []))
    setor = topic_info.get("setor", "")
    if setor:
        chunks.append(setor)
    return " | ".join(str(chunk) for chunk in chunks if chunk)


def _theme_signal(theme_name: str, taxonomy: dict, source_text: str) -> dict:
    definition = taxonomy.get(theme_name, {})
    includes = definition.get("inclui", [])
    excludes = definition.get("nao_inclui", [])

    include_hits = _match_count(includes, source_text)
    exclude_hits = _match_count(excludes, source_text)
    score = include_hits - (exclude_hits * 1.5)
    return {
        "include_hits": include_hits,
        "exclude_hits": exclude_hits,
        "score": score,
    }


def _status_from_confidence(confidence: str, topic_info: dict, rules: dict) -> str:
    thresholds = rules.get("thresholds", {})
    confidence_low_threshold = thresholds.get("confidence_low_threshold", "LOW")
    emergent_min_volume_abs = thresholds.get("emergent_min_volume_abs", 5)
    emergent_min_volume_pct = thresholds.get("emergent_min_volume_pct", 0.02)

    if (
        confidence == confidence_low_threshold
        and topic_info.get("volume_relatos", 0) >= emergent_min_volume_abs
        and topic_info.get("share_pct", 0.0) >= emergent_min_volume_pct
    ):
        return "EMERGENTE"
    if confidence == "LOW":
        return "REVISAR"
    return "OK"


def assess_ambiguity(classifications_payload: dict, topics_payload: dict, rules: dict) -> dict:
    taxonomy = rules["taxonomy"]
    topic_by_id = {topic["topic_id"]: topic for topic in topics_payload.get("topics", [])}

    analyses = []
    for classification in classifications_payload.get("classifications", []):
        topic_id = classification["topic_id"]
        macro_theme = classification["macro_theme"]
        topic_info = topic_by_id.get(topic_id, {})
        source_text = _topic_source_text(topic_info)

        selected_signal = _theme_signal(macro_theme, taxonomy, source_text)
        competitor_signals = [
            {
                "macro_theme": theme_name,
                **_theme_signal(theme_name, taxonomy, source_text),
            }
            for theme_name in taxonomy.keys()
            if theme_name != macro_theme
        ]
        competitor_signals = sorted(
            competitor_signals, key=lambda item: (item["score"], item["include_hits"]), reverse=True
        )
        top_competitor = competitor_signals[0] if competitor_signals else None

        reasons = []
        include_hits = selected_signal["include_hits"]
        exclude_hits = selected_signal["exclude_hits"]
        top_competitor_score = top_competitor["score"] if top_competitor else 0.0
        top_competitor_theme = top_competitor["macro_theme"] if top_competitor else ""

        if include_hits == 0:
            reasons.append("sem sinais fortes de inclusao para o macrotema escolhido")
        if exclude_hits > 0:
            reasons.append("ha termos de nao_inclui conflitantes com o macrotema escolhido")
        if top_competitor and top_competitor_score >= selected_signal["score"] and top_competitor_score > 0:
            reasons.append(
                f"ha competicao semantica com '{top_competitor_theme}' (score semelhante ou maior)"
            )

        if include_hits >= 2 and exclude_hits == 0 and (
            not top_competitor or selected_signal["score"] > top_competitor_score
        ):
            confidence = "HIGH"
        elif include_hits >= 1 and exclude_hits <= 1:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"

        status = _status_from_confidence(confidence, topic_info, rules)
        reason = "; ".join(reasons) if reasons else "classificacao consistente com os sinais do topico"

        analyses.append(
            {
                "topic_id": topic_id,
                "macro_theme": macro_theme,
                "confidence": confidence,
                "status": status,
                "ambiguity_reason": reason,
                "signals": {
                    "selected_theme": selected_signal,
                    "top_competitor": top_competitor,
                },
            }
        )

    analyses = sorted(analyses, key=lambda item: item["topic_id"])
    return {"ambiguity_analysis": analyses}


def merge_classification_with_ambiguity(
    classifications_payload: dict, ambiguity_payload: dict
) -> dict:
    by_topic = {
        item["topic_id"]: item
        for item in ambiguity_payload.get("ambiguity_analysis", [])
    }
    mappings = []
    for classification in classifications_payload.get("classifications", []):
        topic_id = classification["topic_id"]
        ambiguity = by_topic.get(topic_id, {})
        mappings.append(
            {
                "topic_id": topic_id,
                "macro_theme": classification["macro_theme"],
                "confidence": ambiguity.get("confidence", "LOW"),
                "status": ambiguity.get("status", "REVISAR"),
                "rationale": classification.get("rationale", ""),
                "ambiguity_reason": ambiguity.get("ambiguity_reason", ""),
                "signals": ambiguity.get("signals", {}),
            }
        )

    mappings = sorted(mappings, key=lambda item: item["topic_id"])
    return {
        "classifications": classifications_payload.get("classifications", []),
        "ambiguity_analysis": ambiguity_payload.get("ambiguity_analysis", []),
        "mappings": mappings,
    }
