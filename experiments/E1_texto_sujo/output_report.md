Pipeline: Pipeline A — Baseline de MVP (KMeans)
  - nº de clusters: 6
  - estabilidade (ARI entre duas execuções): 0.203
  - % de ruído (aprox.): n/a
    - Cluster 0 (n=10)
      • top termos: lider, sensor, cobra, lider retorno, retorno, sensor desalinhado
      • exemplos:
      - sensor falhando toda hora
      - lider n escuta ngm
      - sensor temp bugado
      - ninguém resolve problema da maq
      - lider cobra mas n ajuda
      • resumo: Relatos focados em lider, sensor, cobra. Exemplo representativo: "sensor falhando toda hora".
      • genérico/incoerente: False

    - Cluster 1 (n=7)
      • top termos: refeitorio, refeita, sujo, refeitorio sujo, separacao, separacao refeita
      • exemplos:
      - refeitorio horrivel hj
      - comida fria no refeitorio
      - reentrega frequente
      - separacao refeita
      - rota refeita por erro
      • resumo: Relatos focados em refeitorio, refeita, sujo. Exemplo representativo: "refeitorio horrivel hj".
      • genérico/incoerente: False

    - Cluster 2 (n=19)
      • top termos: rota, maq, doca, bateria, empilhadeira, demais
      • exemplos:
      - barulho excessivo na prensa
      - maq velha demais
      - linha parada por falha eletrica
      - maq parando sempre no msm ponto
      - empilhadeira parada sem bateria
      • resumo: Relatos focados em rota, maq, doca. Exemplo representativo: "barulho excessivo na prensa".
      • genérico/incoerente: False

    - Cluster 3 (n=19)
      • top termos: turno, sistema, confuso, fila, picking, meio turno
      • exemplos:
      - prensa travou no meio do turno
      - dor nas costas depois do turno
      - troca de turno confusa
      - fila enorme no almoco
      - reclamação geral do turno da noite
      • resumo: Relatos focados em turno, sistema, confuso. Exemplo representativo: "prensa travou no meio do turno".
      • genérico/incoerente: False

    - Cluster 4 (n=16)
      • top termos: mt, linha, setup, lento, picking, erro
      • exemplos:
      - maq 3 parou dnv
      - setup lento na troca de turno
      - mt calor na linha 2
      - linha 1 atrasou dnv
      - mt retrabalho na linha 3
      • resumo: Relatos focados em mt, linha, setup. Exemplo representativo: "maq 3 parou dnv".
      • genérico/incoerente: False

    - Cluster 5 (n=29)
      • top termos: operador, pedido, estoque, palete, errado, novo
      • exemplos:
      - ambiente pesado hj
      - ritmo puxado demais
      - esteira parou 2x hoje
      - posto mal ajustado
      - operador sobrecarregado
      • resumo: Relatos focados em operador, pedido, estoque. Exemplo representativo: "ambiente pesado hj".
      • genérico/incoerente: False

  - notas:
  - KMeans com k fixo (k=6) por simplicidade e alinhamento com expectativa de 5-8 temas operacionais em ~100 relatos.


Comparação e Insights
- KMeans tende a gerar temas consistentes e explicáveis.
- HDBSCAN destaca ruído, útil para ver itens fora do padrão.
- BERTopic acelera geração de tópicos, mas adiciona complexidade.
- Avalie: quais clusters são mais explicáveis para um gestor.
- Avalie: qual pipeline mistura menos temas distintos.
- Avalie: qual parece mais simples de manter no MVP.
- Avalie: trade-offs claros entre qualidade e complexidade.

Decisão (preencher manualmente):
- Base do MVP: ______________________________
- Útil para exploração: ______________________
- Evitar neste momento: ______________________
Próxima iteração sugerida:
- ___________________________________________
- ___________________________________________

