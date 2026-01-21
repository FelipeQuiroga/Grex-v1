Pipeline: Pipeline A — Baseline de MVP (KMeans)
  - nº de clusters: 6
  - estabilidade (ARI entre duas execuções): 0.278
  - % de ruído (aprox.): n/a
    - Cluster 0 (n=8)
      • top termos: operador, excesso, novo, sobrecarregado, operador apoio, apoio
      • exemplos:
      - operador sobrecarregado
      - operador cansado
      - falta treinamento novo operador
      - operador novo perdido
      - operador sem apoio
      • resumo: Relatos focados em operador, excesso, novo. Exemplo representativo: "operador sobrecarregado".
      • genérico/incoerente: False

    - Cluster 1 (n=20)
      • top termos: maq, estoque, demais, lento, turno, separacao
      • exemplos:
      - maq 3 parou dnv
      - setup lento na troca de turno
      - barulho excessivo na prensa
      - ambiente pesado hj
      - ritmo puxado demais
      • resumo: Relatos focados em maq, estoque, demais. Exemplo representativo: "maq 3 parou dnv".
      • genérico/incoerente: False

    - Cluster 2 (n=10)
      • top termos: linha, parou, linha atrasou, atrasou, mt, linha parou
      • exemplos:
      - mt calor na linha 2
      - linha 1 atrasou dnv
      - mt retrabalho na linha 3
      - linha parada por falha eletrica
      - esteira parou 2x hoje
      • resumo: Relatos focados em linha, parou, linha atrasou. Exemplo representativo: "mt calor na linha 2".
      • genérico/incoerente: False

    - Cluster 3 (n=13)
      • top termos: errado, pedido, incompleto, palete, setup, erro
      • exemplos:
      - ninguém resolve problema da maq
      - checklist de setup incompleto
      - mt erro na conferencia
      - palete quebrado
      - pedido voltou errado
      • resumo: Relatos focados em errado, pedido, incompleto. Exemplo representativo: "ninguém resolve problema da maq".
      • genérico/incoerente: False

    - Cluster 4 (n=7)
      • top termos: sensor, bateria, scanner, nao, direito, scanner bateria
      • exemplos:
      - sensor falhando toda hora
      - sensor temp bugado
      - sensor nao le direito
      - empilhadeira parada sem bateria
      - scanner nao funciona direito
      • resumo: Relatos focados em sensor, bateria, scanner. Exemplo representativo: "sensor falhando toda hora".
      • genérico/incoerente: False

    - Cluster 5 (n=42)
      • top termos: turno, lider, rota, refeitorio, mal, confuso
      • exemplos:
      - prensa travou no meio do turno
      - refeitorio horrivel hj
      - lider n escuta ngm
      - dor nas costas depois do turno
      - maq velha demais
      • resumo: Relatos focados em turno, lider, rota. Exemplo representativo: "prensa travou no meio do turno".
      • genérico/incoerente: False

  - notas:
  - KMeans com k fixo (k=6) por simplicidade e alinhamento com expectativa de 5-8 temas operacionais em ~100 relatos.


Pipeline: Pipeline B — Densidade e ruído (HDBSCAN)
  - nº de clusters: 3
  - estabilidade (ARI entre duas execuções): n/a
  - % de ruído (aprox.): 26.0%
    - Cluster -1 (n=26)
      • top termos: turno, maq, excesso, mt, doca, meio turno
      • exemplos:
      - prensa travou no meio do turno
      - mt calor na linha 2
      - barulho excessivo na prensa
      - linha 1 atrasou dnv
      - dor nas costas depois do turno
      • resumo: Relatos focados em turno, maq, excesso. Exemplo representativo: "prensa travou no meio do turno".
      • genérico/incoerente: True

    - Cluster 0 (n=5)
      • top termos: operador, novo, sobrecarregado, operador apoio, apoio, cansado
      • exemplos:
      - operador sobrecarregado
      - operador cansado
      - falta treinamento novo operador
      - operador novo perdido
      - operador sem apoio
      • resumo: Relatos focados em operador, novo, sobrecarregado. Exemplo representativo: "operador sobrecarregado".
      • genérico/incoerente: False

    - Cluster 1 (n=63)
      • top termos: linha, lider, estoque, rota, picking, maq
      • exemplos:
      - maq 3 parou dnv
      - setup lento na troca de turno
      - refeitorio horrivel hj
      - lider n escuta ngm
      - mt retrabalho na linha 3
      • resumo: Relatos focados em linha, lider, estoque. Exemplo representativo: "maq 3 parou dnv".
      • genérico/incoerente: False

    - Cluster 2 (n=6)
      • top termos: sensor, scanner, nao, direito, desalinhado, sensor desalinhado
      • exemplos:
      - sensor falhando toda hora
      - sensor temp bugado
      - sensor nao le direito
      - scanner nao funciona direito
      - sensor desalinhado
      • resumo: Relatos focados em sensor, scanner, nao. Exemplo representativo: "sensor falhando toda hora".
      • genérico/incoerente: False

  - notas:
  - Cluster -1 representa ruído/itens não agrupados.
  - Cluster -1 marcado como genérico/incoerente (tamanho pequeno ou termos fracos).
  - HDBSCAN identifica clusters densos e marca itens dispersos como ruído (-1).
  - Estabilidade deve ser avaliada qualitativamente via ruído e coerência.


Pipeline: Pipeline BERTopic — Exploração rápida de tópicos
  - model:neuralmind/bert-base-portuguese-cased
  - nº de tópicos: 2
  - estabilidade (ARI entre duas execuções): 0.591
  - % de ruído (aprox.): 44.0%
    - Tópico -1 (n=44)
      • top termos: (sem termos fortes)
      • exemplos:
      - maq 3 parou dnv
      - lider n escuta ngm
      - maq velha demais
      - fila enorme no almoco
      - ambiente pesado hj
      • resumo: Cluster sem termos dominantes; relatos variados ou muito curtos.
      • genérico/incoerente: True

    - Tópico 0 (n=39)
      • top termos: linha, operador, rota, turno, na, no
      • exemplos:
      - prensa travou no meio do turno
      - sensor falhando toda hora
      - setup lento na troca de turno
      - mt calor na linha 2
      - barulho excessivo na prensa
      • resumo: Relatos focados em linha, operador, rota. Exemplo representativo: "prensa travou no meio do turno".
      • genérico/incoerente: False

    - Tópico 1 (n=17)
      • top termos: separacao, nao, na, erro, por, direito
      • exemplos:
      - refeitorio horrivel hj
      - sensor nao le direito
      - separacao lenta hj
      - mt erro na conferencia
      - mt pressao por meta
      • resumo: Relatos focados em separacao, nao, na. Exemplo representativo: "refeitorio horrivel hj".
      • genérico/incoerente: False

  - notas:
  - BERTopic gera tópicos legíveis rápido, mas é mais caixa-preta e pesado.
  - BERTopic combina embeddings, UMAP, HDBSCAN e c-TF-IDF em uma solução integrada.
  - Número de tópicos é determinado automaticamente pelo algoritmo.
  - Tópico -1 representa ruído/itens não atribuídos a nenhum tópico.


Pipeline: Pipeline BERTopic — Exploração rápida de tópicos
  - model: rufimelo/bert-large-portuguese-cased-sts
  - nº de tópicos: 3
  - estabilidade (ARI entre duas execuções): 0.499
  - % de ruído (aprox.): 36.0%
    - Tópico -1 (n=36)
      • top termos: (sem termos fortes)
      • exemplos:
      - sensor falhando toda hora
      - mt calor na linha 2
      - refeitorio horrivel hj
      - lider n escuta ngm
      - barulho excessivo na prensa
      • resumo: Cluster sem termos dominantes; relatos variados ou muito curtos.
      • genérico/incoerente: True

    - Tópico 0 (n=26)
      • top termos: turno, linha, parou, no, por, lento
      • exemplos:
      - maq 3 parou dnv
      - prensa travou no meio do turno
      - setup lento na troca de turno
      - linha 1 atrasou dnv
      - troca de turno confusa
      • resumo: Relatos focados em turno, linha, parou. Exemplo representativo: "maq 3 parou dnv".
      • genérico/incoerente: False

    - Tópico 1 (n=26)
      • top termos: erro, errado, palete, pedido, na, picking
      • exemplos:
      - checklist de setup incompleto
      - posto mal ajustado
      - sensor nao le direito
      - picking confuso
      - mt erro na conferencia
      • resumo: Relatos focados em erro, errado, palete. Exemplo representativo: "checklist de setup incompleto".
      • genérico/incoerente: False

    - Tópico 2 (n=12)
      • top termos: estoque, grande, fila, caixa, descarregar, atraso
      • exemplos:
      - estoque desorganizado
      - fila grande no carregamento
      - falta caixa pra picking
      - reentrega frequente
      - estoque divergente
      • resumo: Relatos focados em estoque, grande, fila. Exemplo representativo: "estoque desorganizado".
      • genérico/incoerente: False

  - notas:
  - BERTopic gera tópicos legíveis rápido, mas é mais caixa-preta e pesado.
  - BERTopic combina embeddings, UMAP, HDBSCAN e c-TF-IDF em uma solução integrada.
  - Número de tópicos é determinado automaticamente pelo algoritmo.
  - Tópico -1 representa ruído/itens não atribuídos a nenhum tópico.


Insights sobre o BERTopic
- BERTopic combina múltiplas técnicas (embeddings, UMAP, HDBSCAN, c-TF-IDF)
- Número de tópicos é determinado automaticamente pelo algoritmo
- Tópicos são mais interpretáveis que clusters de métodos tradicionais
- Identifica ruído (textos que não se encaixam em tópicos)
- Mais pesado computacionalmente, mas gera resultados mais legíveis
- Menos controle sobre parâmetros individuais (mais caixa-preta)

Decisão e Próximos Passos (preencher manualmente):
- Qualidade dos tópicos identificados: ______________________________
- Tópicos mais relevantes para o domínio: ____________________________
- Ajustes necessários nos parâmetros: ________________________________
- Próxima iteração sugerida:
  - ___________________________________________
  - ___________________________________________

