# Métricas-alvo iniciais

Metas preliminares para orientar validações. Ajuste conforme os primeiros resultados.

## Qualidade de IA
- **E1 (texto sujo):** >= 0,75 de acurácia em classificação ou equivalentes.
- **E2 (temas):** >= 0,60 de pureza de cluster ou NMI.
- **E3 (resumos):** >= 70% dos resumos com ações específicas (checagem humana).

## Modularidade e segurança
- **E4 (model packs):** +10% de melhora em métricas de cluster vs. baseline.
- **E5 (isolamento):** 0 vazamentos em 1000 queries de teste.

## Performance e custo
- **E6 (1000 relatos):** <= 15 min total e custo <= R$ 0,05 por relato.
