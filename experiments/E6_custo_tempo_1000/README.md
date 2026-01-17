# E6 — Custo/tempo para processar 1000 relatos é previsível

## Hipótese
Processar 1000 relatos mantém latência e custo por relato dentro de limites previsíveis, sem congestionar filas.

## O que testar
- Definir um dataset mínimo e realista para a hipótese.
- Estabelecer um gold set ou rótulos de referência, quando aplicável.
- Medir uma métrica principal com alvo claro e 2 métricas secundárias.


## Como decidir
- **Validada:** métrica principal atinge alvo + evidências qualitativas consistentes.
- **Parcialmente validada:** métrica principal próxima do alvo e ajustes claros.
- **Rejeitada:** métrica principal abaixo do mínimo aceitável ou sinais de risco.
