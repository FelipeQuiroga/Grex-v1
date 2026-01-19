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


Pipeline: Pipeline B — Densidade e ruído (HDBSCAN)
  - nº de clusters: 3
  - estabilidade (ARI entre duas execuções): n/a
  - % de ruído (aprox.): 21.0%
    - Cluster -1 (n=21)
      • top termos: maq, picking, frequente, bugado, layout, parou
      • exemplos:
      - maq 3 parou dnv
      - maq velha demais
      - sensor temp bugado
      - ninguém resolve problema da maq
      - esteira parou 2x hoje
      • resumo: Relatos focados em maq, picking, frequente. Exemplo representativo: "maq 3 parou dnv".
      • genérico/incoerente: True

    - Cluster 0 (n=5)
      • top termos: lider, cobra, retorno, lider retorno, cobra ajuda, ajuda
      • exemplos:
      - lider n escuta ngm
      - lider cobra mas n ajuda
      - lider n da retorno
      - lider ausente no turno
      - lider so cobra resultado
      • resumo: Relatos focados em lider, cobra, retorno. Exemplo representativo: "lider n escuta ngm".
      • genérico/incoerente: False

    - Cluster 1 (n=69)
      • top termos: turno, operador, estoque, linha, rota, mt
      • exemplos:
      - prensa travou no meio do turno
      - setup lento na troca de turno
      - mt calor na linha 2
      - refeitorio horrivel hj
      - barulho excessivo na prensa
      • resumo: Relatos focados em turno, operador, estoque. Exemplo representativo: "prensa travou no meio do turno".
      • genérico/incoerente: False

    - Cluster 2 (n=5)
      • top termos: sensor, scanner, nao, direito, desalinhado, sensor desalinhado
      • exemplos:
      - sensor falhando toda hora
      - sensor nao le direito
      - scanner nao funciona direito
      - sensor desalinhado
      - scanner sem bateria
      • resumo: Relatos focados em sensor, scanner, nao. Exemplo representativo: "sensor falhando toda hora".
      • genérico/incoerente: False

  - notas:
  - Cluster -1 representa ruído/itens não agrupados.
  - Cluster -1 marcado como genérico/incoerente (tamanho pequeno ou termos fracos).
  - HDBSCAN identifica clusters densos e marca itens dispersos como ruído (-1).
  - Estabilidade deve ser avaliada qualitativamente via ruído e coerência.


Pipeline: Pipeline C — Exploração rápida (BERTopic)
  - nº de clusters: 0
  - estabilidade (ARI entre duas execuções): 1.000
  - % de ruído (aprox.): 100.0%
    - Cluster -1 (n=100)
      • top termos: (sem termos fortes)
      • exemplos:
      - maq 3 parou dnv
      - prensa travou no meio do turno
      - sensor falhando toda hora
      - setup lento na troca de turno
      - mt calor na linha 2
      • resumo: Cluster sem termos dominantes; relatos variados ou muito curtos.
      • genérico/incoerente: True

  - notas:
  - BERTopic gera tópicos legíveis rápido, mas é mais caixa-preta e pesado.
  - Topic -1 representa ruído/itens não atribuídos.


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

