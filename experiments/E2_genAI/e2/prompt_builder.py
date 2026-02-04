from __future__ import annotations

import json


def build_prompt(payload: dict, rules: dict) -> str:
    themes_min = rules["themes_min"]
    themes_max = rules["themes_max"]
    themes_target = rules["themes_target"]
    emergent_min_count = rules["emergent_min_count"]
    emergent_min_share = rules["emergent_min_share"]
    instructions = f"""
Você é um Agente de Padronização. Sua tarefa é criar uma taxonomia canônica estável e mapear cada tópico para um único tema.

Regras obrigatórias:
- Gere entre {themes_min} e {themes_max} temas canônicos (alvo: {themes_target}).
- Cada tema deve ter nome curto (2–5 palavras) e linguagem operacional.
- Estruture a taxonomia como macrotema -> tema.
- Cada topic_id deve mapear para exatamente 1 tema canônico.
- Inclua confiança: alta | media | baixa.
- Inclua status: OK | REVISAR | EMERGENTE.
- Temas emergentes só são permitidos quando:
  * confiança for baixa, E
  * volume_relatos >= {emergent_min_count}, E
  * share_pct >= {emergent_min_share}.
- Temas emergentes NÃO entram na taxonomia canônica.
- Retorne apenas JSON válido. Nenhum texto fora do JSON.

Formato de saída (JSON estrito):
{{
  "taxonomy": {{
    "themes": [
      {{
        "macrotheme": "string",
        "theme": "string"
      }}
    ]
  }},
  "mappings": [
    {{
      "topic_id": 0,
      "macrotheme": "string",
      "theme": "string",
      "confidence": "alta|media|baixa",
      "status": "OK|REVISAR|EMERGENTE"
    }}
  ],
  "emergent_themes": [
    {{
      "name": "string",
      "reason": "string",
      "topic_ids": [0]
    }}
  ]
}}

Aqui está o payload agregado de tópicos:
{json.dumps(payload, ensure_ascii=False, indent=2)}
"""
    return instructions.strip()


def build_repair_prompt(raw_response: str, errors: list[str]) -> str:
    error_text = "\n".join(f"- {error}" for error in errors)
    return (
        "A resposta anterior falhou na validação. "
        "Corrija e devolva apenas um JSON válido seguindo exatamente o schema solicitado.\n\n"
        f"Erros encontrados:\n{error_text}\n\n"
        f"Resposta anterior:\n{raw_response}\n"
    )
