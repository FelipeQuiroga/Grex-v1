from __future__ import annotations


def compute_metrics(payload: dict, topics_payload: dict) -> dict:
    mappings = payload.get("mappings", [])
    status_counts = {"OK": 0, "REVISAR": 0, "EMERGENTE": 0}
    for mapping in mappings:
        status = mapping.get("status")
        if status in status_counts:
            status_counts[status] += 1

    total_topics = len(mappings)
    themes = payload.get("taxonomy", {}).get("themes", [])
    theme_count = len({(item.get("macrotheme"), item.get("theme")) for item in themes})

    volume_by_topic = {
        topic["topic_id"]: topic["volume_relatos"]
        for topic in topics_payload.get("topics", [])
    }
    total_volume = sum(volume_by_topic.values())
    ok_volume = sum(
        volume_by_topic.get(mapping.get("topic_id"), 0)
        for mapping in mappings
        if mapping.get("status") == "OK"
    )
    ok_volume_pct = round(ok_volume / total_volume, 4) if total_volume else 0.0

    return {
        "total_themes": theme_count,
        "total_topics": total_topics,
        "status_pct": {
            status: round(count / total_topics, 4) if total_topics else 0.0
            for status, count in status_counts.items()
        },
        "ok_volume_pct": ok_volume_pct,
    }
