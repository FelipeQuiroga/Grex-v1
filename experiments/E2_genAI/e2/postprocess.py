from __future__ import annotations


CONFIDENCE_SCORE = {
    "HIGH": 1.0,
    "MEDIUM": 0.5,
    "LOW": 0.0,
}


def _is_emergent_by_rule(mapping: dict, topic_info: dict, rules: dict | None) -> bool:
    thresholds = (rules or {}).get("thresholds", {})
    confidence_low_threshold = thresholds.get("confidence_low_threshold", "LOW")
    emergent_min_volume_abs = thresholds.get("emergent_min_volume_abs", 5)
    emergent_min_volume_pct = thresholds.get("emergent_min_volume_pct", 0.02)

    confidence = mapping.get("confidence")
    volume_relatos = topic_info.get("volume_relatos", 0)
    share_pct = topic_info.get("share_pct", 0.0)
    return (
        confidence == confidence_low_threshold
        and volume_relatos >= emergent_min_volume_abs
        and share_pct >= emergent_min_volume_pct
    )


def _round_pct(value: float) -> float:
    return round(value, 4)


def compute_metrics(payload: dict, topics_payload: dict, rules: dict | None = None) -> dict:
    mappings = payload.get("mappings", [])
    topics = topics_payload.get("topics", [])

    topic_by_id = {topic["topic_id"]: topic for topic in topics}
    total_topics = len(mappings)
    total_volume = sum(topic.get("volume_relatos", 0) for topic in topics)

    status_counts = {"OK": 0, "REVISAR": 0, "EMERGENTE": 0}
    confidence_sum = 0.0
    confidence_n = 0
    status_mismatch_count = 0

    ok_volume = 0
    emergent_volume = 0
    macro_volume: dict[str, int] = {}
    macro_topics: dict[str, int] = {}

    for mapping in mappings:
        topic_id = mapping.get("topic_id")
        topic_info = topic_by_id.get(topic_id, {})
        topic_volume = topic_info.get("volume_relatos", 0)

        declared_status = mapping.get("status")
        emergent_by_rule = _is_emergent_by_rule(mapping, topic_info, rules)
        if emergent_by_rule:
            effective_status = "EMERGENTE"
        elif declared_status == "OK":
            effective_status = "OK"
        else:
            effective_status = "REVISAR"

        if effective_status in status_counts:
            status_counts[effective_status] += 1
        if declared_status != effective_status:
            status_mismatch_count += 1

        if effective_status == "OK":
            ok_volume += topic_volume
        if effective_status == "EMERGENTE":
            emergent_volume += topic_volume

        confidence = mapping.get("confidence")
        if confidence in CONFIDENCE_SCORE:
            confidence_sum += CONFIDENCE_SCORE[confidence]
            confidence_n += 1

        macro_theme = mapping.get("macro_theme")
        if isinstance(macro_theme, str) and macro_theme:
            macro_topics[macro_theme] = macro_topics.get(macro_theme, 0) + 1
            macro_volume[macro_theme] = macro_volume.get(macro_theme, 0) + topic_volume

    macro_distribution = {
        macro_theme: {
            "topic_count": macro_topics.get(macro_theme, 0),
            "volume": volume,
            "volume_pct": _round_pct(volume / total_volume) if total_volume else 0.0,
        }
        for macro_theme, volume in sorted(macro_volume.items())
    }

    return {
        "total_topics": total_topics,
        "total_volume": total_volume,
        "status_pct": {
            status: _round_pct(count / total_topics) if total_topics else 0.0
            for status, count in status_counts.items()
        },
        "ok_volume_pct": _round_pct(ok_volume / total_volume) if total_volume else 0.0,
        "emergent_volume_pct": _round_pct(emergent_volume / total_volume)
        if total_volume
        else 0.0,
        "confidence_avg": _round_pct(confidence_sum / confidence_n) if confidence_n else 0.0,
        "macro_distribution": macro_distribution,
        "status_mismatch_count": status_mismatch_count,
    }
