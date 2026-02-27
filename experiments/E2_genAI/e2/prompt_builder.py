from __future__ import annotations

import json


def build_prompt(payload: dict, rules: dict) -> str:
    macro_taxonomy = rules["macro_taxonomy"]
    thresholds = rules["thresholds"]
    confidence_low_threshold = thresholds["confidence_low_threshold"]
    emergent_min_volume_abs = thresholds["emergent_min_volume_abs"]
    emergent_min_volume_pct = thresholds["emergent_min_volume_pct"]

    macro_taxonomy_json = json.dumps(macro_taxonomy, ensure_ascii=False, indent=2)
    instructions = f"""
Voce e um classificador de topicos para macrotemas pre-definidos.
Sua tarefa e classificar cada topic_id em exatamente um macrotema desta taxonomia fixa.

Regras obrigatorias:
- Classifique apenas dentro desses macrotemas.
- Nao crie novos macrotemas.
- Cada topic_id deve mapear para exatamente 1 macro_theme.
- confidence deve ser: HIGH | MEDIUM | LOW.
- status deve ser: OK | REVISAR | EMERGENTE.
- Regra objetiva para EMERGENTE:
  * confidence == {confidence_low_threshold}
  * volume_relatos >= {emergent_min_volume_abs}
  * share_pct >= {emergent_min_volume_pct}
- Se qualquer condicao acima falhar, nao use EMERGENTE.
- Retorne apenas JSON valido. Nenhum texto fora do JSON.

Taxonomia macro fixa (use apenas itens desta lista):
{macro_taxonomy_json}

Formato de saida (JSON estrito **SEM NENHUM TEXTO ADICIONAL**):
```json
{{
  "mappings": [
    {{
      "topic_id": 0,
      "macro_theme": "string",
      "confidence": "HIGH|MEDIUM|LOW",
      "status": "OK|REVISAR|EMERGENTE"
    }}
  ]
}}
```

Aqui esta o payload agregado de topicos:
{json.dumps(payload, ensure_ascii=False, indent=2)}
"""
    return instructions.strip()


def build_repair_prompt(raw_response: str, errors: list[str]) -> str:
    error_text = "\n".join(f"- {error}" for error in errors)
    return (
        "A resposta anterior falhou na validacao. "
        "Corrija e devolva apenas um JSON valido seguindo exatamente o schema solicitado.\n\n"
        f"Erros encontrados:\n{error_text}\n\n"
        f"Resposta anterior:\n{raw_response}\n"
    )
