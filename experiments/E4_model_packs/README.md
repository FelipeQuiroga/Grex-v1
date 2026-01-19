# 📁 Experimento 4 — Model Packs Setoriais

## E4 — Model Packs (Indústria vs Centro de Distribuição)

### Contexto
Clusters e interpretação funcionam, mas linguagem e contexto variam por setor.

### Hipótese (E4)
Model Packs setoriais (vocabulário, stopwords, boosting semântico) melhoram significativamente a qualidade dos clusters e da interpretação sem aumentar custo estrutural.

### O que testar
Comparar:

- Pipeline genérico.
- Pipeline com Model Pack de Indústria.
- Pipeline com Model Pack de CD.

Avaliar:

- separação temática.
- qualidade dos labels.
- clareza dos resumos.

### O que é um Model Pack
- Dicionário setorial.
- Stopwords específicas.
- Boost leve em termos críticos.
- Prompt ajustado para o setor.

### Como decidir
- **Validada:** melhoria clara sem aumento de complexidade.
- **Rejeitada:** ganho marginal ou custo alto.
