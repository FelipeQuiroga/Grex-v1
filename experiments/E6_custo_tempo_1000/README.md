# 📁 Experimento 6 — Custo e Escalabilidade

## E6 — Custo e tempo em escala

### Contexto
Antes de escalar, precisamos saber se o modelo é sustentável.

### Hipótese (E6)
A arquitetura (KMeans + IA gen por cluster) escala bem e mantém custo previsível.

### O que testar
Processar 1.000 relatos.

Medir:

- tempo total.
- custo de embeddings.
- custo de chamadas de IA gen.

Comparar:

- IA por relato ❌.
- IA por cluster ✅.

### Como decidir
- **Validada:** custo previsível e aceitável.
- **Rejeitada:** custo explode ou latência inviável.
