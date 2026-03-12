from __future__ import annotations


TAXONOMY_VERSION = "macrothemes_v1_operacional_2026_03"

TAXONOMY = {
    "Equipamentos e Infraestrutura": {
        "descricao": (
            "Problemas com máquinas, sensores, esteiras, ferramentas, empilhadeiras, "
            "iluminação, ventilação, posto de trabalho e estrutura física."
        ),
        "inclui": [
            "máquina",
            "maq",
            "sensor",
            "esteira",
            "empilhadeira",
            "ferramenta",
            "posto",
            "iluminação",
            "ventilação",
        ],
        "nao_inclui": ["liderança", "cobrança", "sistema", "scanner", "meta", "processo"],
    },
    "Sistemas e Ferramentas": {
        "descricao": (
            "Problemas com sistema, scanner, atualização, travamento, falhas digitais, "
            "dados ou ferramentas de apoio operacional."
        ),
        "inclui": ["sistema", "scanner", "bugado", "travou", "caiu", "atualiza", "dados"],
        "nao_inclui": ["máquina", "empilhadeira", "liderança", "meta", "sobrecarga"],
    },
    "Pessoas e Liderança": {
        "descricao": (
            "Problemas de liderança, comunicação, apoio, escuta, sobrecarga da equipe, "
            "treinamento ou comportamento humano."
        ),
        "inclui": [
            "líder",
            "lider",
            "escuta",
            "cobra",
            "retorno",
            "equipe",
            "treinamento",
            "sobrecarregado",
            "operador",
        ],
        "nao_inclui": ["máquina", "sistema", "scanner", "infraestrutura"],
    },
    "Processo Operacional": {
        "descricao": (
            "Problemas de fluxo, setup, separação, carregamento, organização do trabalho, "
            "rota, troca de turno ou execução do processo."
        ),
        "inclui": [
            "setup",
            "separação",
            "separacao",
            "rota",
            "troca",
            "carregamento",
            "fluxo",
            "retrabalho",
            "expedição",
            "expedicao",
        ],
        "nao_inclui": ["liderança", "máquina", "scanner", "risco de segurança"],
    },
    "Segurança e Risco": {
        "descricao": (
            "Problemas com risco operacional, check de segurança, condição insegura, "
            "incidente potencial ou exposição física relevante."
        ),
        "inclui": [
            "segurança",
            "seguranca",
            "risco",
            "check",
            "falha de segurança",
            "condição insegura",
            "condicao insegura",
        ],
        "nao_inclui": ["sistema lento", "líder ausente", "setup lento"],
    },
}


TAXONOMY_REGISTRY = {
    TAXONOMY_VERSION: TAXONOMY,
}


def load_taxonomy(version: str) -> dict:
    try:
        taxonomy = TAXONOMY_REGISTRY[version]
    except KeyError as exc:
        available = ", ".join(sorted(TAXONOMY_REGISTRY.keys()))
        raise ValueError(
            f"Taxonomia '{version}' nao encontrada. Versoes disponiveis: {available}"
        ) from exc
    return taxonomy
