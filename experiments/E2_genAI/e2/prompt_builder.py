from __future__ import annotations

import json


POSITIVE_EXAMPLES = [
    {
        "input": "sensor desalinhado e esteira parando no turno da noite",
        "macro_theme": "Equipamentos e Infraestrutura",
        "porque": "o foco é falha física de sensor/esteira.",
    },
    {
        "input": "scanner sem bateria, sistema caiu e não atualiza dados",
        "macro_theme": "Sistemas e Ferramentas",
        "porque": "o problema principal é digital (scanner/sistema/dados).",
    },
    {
        "input": "líder ausente, equipe sem retorno e operador sobrecarregado",
        "macro_theme": "Pessoas e Liderança",
        "porque": "o núcleo do tema é comportamento e liderança.",
    },
    {
        "input": "setup lento, retrabalho e troca de turno desorganizada",
        "macro_theme": "Processo Operacional",
        "porque": "a causa está no fluxo e execução do processo.",
    },
    {
        "input": "check de segurança falhou com condição insegura na operação",
        "macro_theme": "Segurança e Risco",
        "porque": "há risco operacional explícito.",
    },
]


COUNTER_EXAMPLES = [
    {
        "input": "líder não escuta equipe e cobra meta",
        "nao_e": "Sistemas e Ferramentas",
        "correto": "Pessoas e Liderança",
        "porque": "não há falha de sistema/scanner, e sim liderança.",
    },
    {
        "input": "sistema lento no scanner durante separação",
        "nao_e": "Processo Operacional",
        "correto": "Sistemas e Ferramentas",
        "porque": "o fluxo sofre impacto, mas a origem é sistema/scanner.",
    },
    {
        "input": "setup lento sem risco ou incidente de segurança",
        "nao_e": "Segurança e Risco",
        "correto": "Processo Operacional",
        "porque": "lento não implica risco físico por si só.",
    },
    {
        "input": "meta alta e cobrança do líder",
        "nao_e": "Equipamentos e Infraestrutura",
        "correto": "Pessoas e Liderança",
        "porque": "não há falha de máquina/estrutura.",
    },
]


def _render_taxonomy(taxonomy: dict) -> str:
    lines: list[str] = []
    for macro_theme, definition in taxonomy.items():
        descricao = definition.get("descricao", "")
        inclui = ", ".join(definition.get("inclui", []))
        nao_inclui = ", ".join(definition.get("nao_inclui", []))
        lines.append(f"- {macro_theme}")
        lines.append(f"  descricao: {descricao}")
        lines.append(f"  inclui: {inclui}")
        lines.append(f"  nao_inclui: {nao_inclui}")
    return "\n".join(lines)


def _render_examples(title: str, examples: list[dict]) -> str:
    lines = [title]
    for idx, example in enumerate(examples, start=1):
        lines.append(f"{idx}. {json.dumps(example, ensure_ascii=False)}")
    return "\n".join(lines)


def build_prompt(payload: dict, rules: dict) -> str:
    taxonomy = rules["taxonomy"]
    taxonomy_json = _render_taxonomy(taxonomy)
    allowed_macrothemes = list(taxonomy.keys())
    output_schema = {
        "classifications": [
            {
                "topic_id": 0,
                "macro_theme": "string",
                "rationale": "curta e objetiva (max 180 chars)",
            }
        ]
    }

    instructions = f"""
Voce e um classificador tematico para operacoes industriais e logistica.
Classifique cada topic_id em exatamente 1 macrotema da taxonomia fixa.

Regras obrigatorias:
- Use TODO o contexto enviado: top_terms, examples, contexto_operacional, setor, volume_relatos e share_pct.
- Nao classifique apenas por top_terms isolados.
- Nao invente macrotema.
- Nao use categoria default por conveniencia.
- Antes de decidir, verifique sinais de "inclui" e evite termos de "nao_inclui".
- Se houver sinais mistos, escolha o macrotema dominante e registre a incerteza no campo rationale.
- Retorne apenas JSON valido. Nenhum texto fora do JSON.

Taxonomia fixa (obrigatoria):
{taxonomy_json}

Macrotemas permitidos:
{json.dumps(allowed_macrothemes, ensure_ascii=False, indent=2)}

Exemplos positivos (acerto):
{_render_examples("Casos corretos:", POSITIVE_EXAMPLES)}

Contraexemplos (erros comuns a evitar):
{_render_examples("Casos para NAO repetir:", COUNTER_EXAMPLES)}

Formato de saida (JSON estrito):
```json
{json.dumps(output_schema, ensure_ascii=False, indent=2)}
```

Payload de topicos para classificacao:
{json.dumps(payload, ensure_ascii=False, indent=2)}
"""
    return instructions.strip()


def build_repair_prompt(raw_response: str, errors: list[str]) -> str:
    error_text = "\n".join(f"- {error}" for error in errors)
    expected_schema = {
        "classifications": [
            {
                "topic_id": 0,
                "macro_theme": "string",
                "rationale": "string",
            }
        ]
    }
    return (
        "A resposta anterior falhou na validacao. "
        "Corrija e devolva apenas JSON valido seguindo exatamente o schema.\n\n"
        f"Schema esperado:\n{json.dumps(expected_schema, ensure_ascii=False, indent=2)}\n\n"
        f"Erros encontrados:\n{error_text}\n\n"
        f"Resposta anterior:\n{raw_response}\n"
    )
