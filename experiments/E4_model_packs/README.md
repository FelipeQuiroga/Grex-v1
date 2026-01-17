# E4 — Model Packs setoriais são modularizáveis

## Hipótese
Model Packs por setor podem ser modularizados e melhoram clusters com 100-200 relatos sem custo excessivo.

## O que testar
- Definir um dataset mínimo e realista para a hipótese.
- Estabelecer um gold set ou rótulos de referência, quando aplicável.
- Medir uma métrica principal com alvo claro e 2 métricas secundárias.

## Como rodar (sugestão mínima)
1. Preparar os dados em `data/input.jsonl`.
2. Executar o script/nota de execução do experimento.
   - Exemplo: `python run.py --input data/input.jsonl --output resultados.json`
3. Consolidar os resultados em um resumo curto e comparável.

## Como decidir
- **Validada:** métrica principal atinge alvo + evidências qualitativas consistentes.
- **Parcialmente validada:** métrica principal próxima do alvo e ajustes claros.
- **Rejeitada:** métrica principal abaixo do mínimo aceitável ou sinais de risco.
