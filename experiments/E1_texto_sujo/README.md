# E1 — IA entende texto sujo (gírias, abreviações, erros)

## Hipótese
A IA consegue interpretar textos operacionais sujos e agrupá-los em temas coerentes, mesmo sem limpeza pesada.

## O que testar
- Definir um dataset mínimo e realista para a hipótese.
- Estabelecer um gold set ou rótulos de referência, quando aplicável.
- Medir uma métrica principal com alvo claro e 2 métricas secundárias.

## Como rodar (local)
```bash
python experiments/E1_texto_sujo/run_experiment.py \
  --dataset experiments/E0_dataset_goldset/dataset.csv \
  --stopwords experiments/E0_dataset_goldset/stopwords_ptbr.txt \
  --output experiments/E1_texto_sujo/output_report.md
```

Para habilitar o Pipeline C (BERTopic):
```bash
python experiments/E1_texto_sujo/run_experiment.py --run-bertopic
```

## Saída esperada
- Arquivo `output_report.md` com:
  - nº de clusters por pipeline
  - percentual aproximado de ruído (quando aplicável)
  - top termos por cluster
  - exemplos de relatos
  - resumo humano (1–2 frases)
  - observações de clusters genéricos ou incoerentes
  - seção final “Comparação e Insights”

## Como decidir
- **Validada:** métrica principal atinge alvo + evidências qualitativas consistentes.
- **Parcialmente validada:** métrica principal próxima do alvo e ajustes claros.
- **Rejeitada:** métrica principal abaixo do mínimo aceitável ou sinais de risco.
