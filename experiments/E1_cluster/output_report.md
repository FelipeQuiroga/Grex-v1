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

Pipeline: Pipeline BERTopic — Exploração rápida de tópicos
  - + ajustes para pequenos datasets 
  - model rufimelo/bert-large-portuguese-cased-sts
  - nº de tópicos: 8
  - estabilidade (ARI entre duas execuções): 0.654
  - % de ruído (aprox.): 0.0%
    - Tópico 0 (n=22)
      • top termos: turno, linha, parou, lento, atrasou, no
      • exemplos:
      - maq 3 parou dnv
      - prensa travou no meio do turno
      - setup lento na troca de turno
      - linha 1 atrasou dnv
      - troca de turno confusa
      • resumo: Relatos focados em turno, linha, parou. Exemplo representativo: "maq 3 parou dnv".
      • genérico/incoerente: False

    - Tópico 1 (n=22)
      • top termos: sensor, erro, palete, picking, confuso, layout
      • exemplos:
      - sensor falhando toda hora
      - sensor temp bugado
      - checklist de setup incompleto
      - posto mal ajustado
      - sensor nao le direito
      • resumo: Relatos focados em sensor, erro, palete. Exemplo representativo: "sensor falhando toda hora".
      • genérico/incoerente: False

    - Tópico 2 (n=16)
      • top termos: operador, doca, sem, novo, hj, separacao
      • exemplos:
      - dor nas costas depois do turno
      - ambiente pesado hj
      - reclamação geral do turno da noite
      - operador sobrecarregado
      - separacao lenta hj
      • resumo: Relatos focados em operador, doca, sem. Exemplo representativo: "dor nas costas depois do turno".
      • genérico/incoerente: False

    - Tópico 3 (n=14)
      • top termos: estoque, empilhadeira, atrasada, atualiza, caixa, enderecado
      • exemplos:
      - maq velha demais
      - empilhadeira parada sem bateria
      - estoque desorganizado
      - falta caixa pra picking
      - empilhadeira falhando
      • resumo: Relatos focados em estoque, empilhadeira, atrasada. Exemplo representativo: "maq velha demais".
      • genérico/incoerente: False

    - Tópico 4 (n=11)
      • top termos: fila, refeitorio, calor, barulho, grande, no
      • exemplos:
      - mt calor na linha 2
      - refeitorio horrivel hj
      - barulho excessivo na prensa
      - fila enorme no almoco
      - comida fria no refeitorio
      • resumo: Relatos focados em fila, refeitorio, calor. Exemplo representativo: "mt calor na linha 2".
      • genérico/incoerente: False

    - Tópico 5 (n=6)
      • top termos: lider, cobra, ausente, retorno, resultado, meta
      • exemplos:
      - lider n escuta ngm
      - lider cobra mas n ajuda
      - lider n da retorno
      - mt pressao por meta
      - lider ausente no turno
      • resumo: Relatos focados em lider, cobra, ausente. Exemplo representativo: "lider n escuta ngm".
      • genérico/incoerente: False

    - Tópico 6 (n=6)
      • top termos: rota, retrabalho, mt, desnecessario, sobrecarregada, deslocamento
      • exemplos:
      - mt retrabalho na linha 3
      - rota mal planejada
      - mt deslocamento desnecessario
      - rota refeita por erro
      - retrabalho na rota
      • resumo: Relatos focados em rota, retrabalho, mt. Exemplo representativo: "mt retrabalho na linha 3".
      • genérico/incoerente: False

    - Tópico 7 (n=3)
      • top termos: pedido, voltou, trocado, incompleto, errado, 
      • exemplos:
      - pedido voltou errado
      - pedido incompleto
      - pedido trocado
      • resumo: Relatos focados em pedido, voltou, trocado. Exemplo representativo: "pedido voltou errado".
      • genérico/incoerente: False

Pipeline: Pipeline BERTopic — Exploração rápida de tópicos
  - model paraphrase-multilingual-MiniLM-L12-v2
  - nº de tópicos: 12
  - estabilidade (ARI entre duas execuções): 0.590
  - % de ruído (aprox.): 1.0%
    - Tópico -1 (n=1)
      • top termos: (sem termos fortes)
      • exemplos:
      - sistema caiu no meio do turno
      • resumo: Cluster sem termos dominantes; relatos variados ou muito curtos.
      • genérico/incoerente: True

    - Tópico 0 (n=16)
      • top termos: palete, fila, grande, carregamento, excesso, no
      • exemplos:
      - fila enorme no almoco
      - comida fria no refeitorio
      - palete quebrado
      - fila grande no carregamento
      - doca congestionada
      • resumo: Relatos focados em palete, fila, grande. Exemplo representativo: "fila enorme no almoco".
      • genérico/incoerente: False

    - Tópico 1 (n=15)
      • top termos: estoque, lento, manual, lenta, hj, na
      • exemplos:
      - setup lento na troca de turno
      - mt retrabalho na linha 3
      - ambiente pesado hj
      - separacao lenta hj
      - estoque desorganizado
      • resumo: Relatos focados em estoque, lento, manual. Exemplo representativo: "setup lento na troca de turno".
      • genérico/incoerente: False

    - Tópico 2 (n=10)
      • top termos: lider, cobra, doca, sem, chegar, equipe
      • exemplos:
      - lider n escuta ngm
      - lider cobra mas n ajuda
      - lider n da retorno
      - mt pressao por meta
      - lider ausente no turno
      • resumo: Relatos focados em lider, cobra, doca. Exemplo representativo: "lider n escuta ngm".
      • genérico/incoerente: False

    - Tópico 3 (n=9)
      • top termos: erro, na, mal, rota, planejada, endereco
      • exemplos:
      - troca de turno confusa
      - reclamação geral do turno da noite
      - mt erro na conferencia
      - rota mal planejada
      - empilhadeira disputada
      • resumo: Relatos focados em erro, na, mal. Exemplo representativo: "troca de turno confusa".
      • genérico/incoerente: False

    - Tópico 4 (n=8)
      • top termos: pedido, incompleto, setup, errado, de, atualiza
      • exemplos:
      - checklist de setup incompleto
      - pedido voltou errado
      - empilhadeira falhando
      - pedido incompleto
      - check de seguranca falhou
      • resumo: Relatos focados em pedido, incompleto, setup. Exemplo representativo: "checklist de setup incompleto".
      • genérico/incoerente: False

    - Tópico 5 (n=7)
      • top termos: linha, parou, por, atrasou, eletrica, vezes
      • exemplos:
      - linha 1 atrasou dnv
      - linha parada por falha eletrica
      - esteira parou 2x hoje
      - linha 2 atrasou por manutencao
      - linha parou por falta material
      • resumo: Relatos focados em linha, parou, por. Exemplo representativo: "linha 1 atrasou dnv".
      • genérico/incoerente: False

    - Tópico 6 (n=7)
      • top termos: layout, posto, refeitorio, ajustado, costas, nas
      • exemplos:
      - refeitorio horrivel hj
      - dor nas costas depois do turno
      - posto mal ajustado
      - layout confuso
      - posto desconfortavel
      • resumo: Relatos focados em layout, posto, refeitorio. Exemplo representativo: "refeitorio horrivel hj".
      • genérico/incoerente: False

    - Tópico 7 (n=7)
      • top termos: demais, barulho, prensa, calor, maq, mt
      • exemplos:
      - prensa travou no meio do turno
      - mt calor na linha 2
      - barulho excessivo na prensa
      - maq velha demais
      - ritmo puxado demais
      • resumo: Relatos focados em demais, barulho, prensa. Exemplo representativo: "prensa travou no meio do turno".
      • genérico/incoerente: False

    - Tópico 8 (n=7)
      • top termos: sensor, bateria, direito, scanner, nao, sem
      • exemplos:
      - sensor falhando toda hora
      - sensor temp bugado
      - sensor nao le direito
      - empilhadeira parada sem bateria
      - scanner nao funciona direito
      • resumo: Relatos focados em sensor, bateria, direito. Exemplo representativo: "sensor falhando toda hora".
      • genérico/incoerente: False

    - Tópico 9 (n=5)
      • top termos: operador, novo, cansado, sobrecarregado, treinamento, perdido
      • exemplos:
      - operador sobrecarregado
      - operador cansado
      - falta treinamento novo operador
      - operador novo perdido
      - operador sem apoio
      • resumo: Relatos focados em operador, novo, cansado. Exemplo representativo: "operador sobrecarregado".
      • genérico/incoerente: False

    - Tópico 10 (n=4)
      • top termos: maq, resolve, ninguém, msm, ponto, parando
      • exemplos:
      - maq 3 parou dnv
      - ninguém resolve problema da maq
      - maq parando sempre no msm ponto
      - maq superaquecendo
      • resumo: Relatos focados em maq, resolve, ninguém. Exemplo representativo: "maq 3 parou dnv".
      • genérico/incoerente: False

    - Tópico 11 (n=4)
      • top termos: picking, caixa, confunde, enderecos, recorrente, confuso
      • exemplos:
      - picking confuso
      - falta caixa pra picking
      - erro recorrente no picking
      - picking confunde enderecos
      • resumo: Relatos focados em picking, caixa, confunde. Exemplo representativo: "picking confuso".
      • genérico/incoerente: False


Pipeline: Pipeline BERTopic — Exploração rápida de tópicos
model paraphrase-multilingual-MiniLM-L12-v2
  - nº de tópicos: 12
  - estabilidade (ARI entre duas execuções): 0.733
  - % de ruído (aprox.): 4.0%
    - Tópico -1 (n=4)
      • top termos: (sem termos fortes)
      • exemplos:
      - reentrega frequente
      - excesso de refugos
      - retrabalho na rota
      - excesso de horas extras
      • resumo: Cluster sem termos dominantes; relatos variados ou muito curtos.
      • genérico/incoerente: True

    - Tópico 0 (n=22)
      • top termos: estoque, fila, palete, separacao, carregamento, grande
      • exemplos:
      - mt retrabalho na linha 3
      - fila enorme no almoco
      - ambiente pesado hj
      - comida fria no refeitorio
      - separacao lenta hj
      • resumo: Relatos focados em estoque, fila, palete. Exemplo representativo: "mt retrabalho na linha 3".
      • genérico/incoerente: False

    - Tópico 1 (n=10)
      • top termos: lider, cobra, doca, sem, chegar, equipe
      • exemplos:
      - lider n escuta ngm
      - lider cobra mas n ajuda
      - lider n da retorno
      - mt pressao por meta
      - lider ausente no turno
      • resumo: Relatos focados em lider, cobra, doca. Exemplo representativo: "lider n escuta ngm".
      • genérico/incoerente: False

    - Tópico 2 (n=9)
      • top termos: erro, na, mal, rota, planejada, endereco
      • exemplos:
      - troca de turno confusa
      - reclamação geral do turno da noite
      - mt erro na conferencia
      - rota mal planejada
      - empilhadeira disputada
      • resumo: Relatos focados em erro, na, mal. Exemplo representativo: "troca de turno confusa".
      • genérico/incoerente: False

    - Tópico 3 (n=9)
      • top termos: pedido, incompleto, errado, setup, sistema, de
      • exemplos:
      - checklist de setup incompleto
      - pedido voltou errado
      - empilhadeira falhando
      - sistema caiu no meio do turno
      - pedido incompleto
      • resumo: Relatos focados em pedido, incompleto, errado. Exemplo representativo: "checklist de setup incompleto".
      • genérico/incoerente: False

    - Tópico 4 (n=7)
      • top termos: demais, barulho, prensa, calor, maq, mt
      • exemplos:
      - prensa travou no meio do turno
      - mt calor na linha 2
      - barulho excessivo na prensa
      - maq velha demais
      - ritmo puxado demais
      • resumo: Relatos focados em demais, barulho, prensa. Exemplo representativo: "prensa travou no meio do turno".
      • genérico/incoerente: False

    - Tópico 5 (n=7)
      • top termos: linha, parou, por, atrasou, eletrica, vezes
      • exemplos:
      - linha 1 atrasou dnv
      - linha parada por falha eletrica
      - esteira parou 2x hoje
      - linha 2 atrasou por manutencao
      - linha parou por falta material
      • resumo: Relatos focados em linha, parou, por. Exemplo representativo: "linha 1 atrasou dnv".
      • genérico/incoerente: False

    - Tópico 6 (n=7)
      • top termos: layout, posto, refeitorio, ajustado, costas, nas
      • exemplos:
      - refeitorio horrivel hj
      - dor nas costas depois do turno
      - posto mal ajustado
      - layout confuso
      - posto desconfortavel
      • resumo: Relatos focados em layout, posto, refeitorio. Exemplo representativo: "refeitorio horrivel hj".
      • genérico/incoerente: False

    - Tópico 7 (n=7)
      • top termos: sensor, bateria, direito, scanner, nao, sem
      • exemplos:
      - sensor falhando toda hora
      - sensor temp bugado
      - sensor nao le direito
      - empilhadeira parada sem bateria
      - scanner nao funciona direito
      • resumo: Relatos focados em sensor, bateria, direito. Exemplo representativo: "sensor falhando toda hora".
      • genérico/incoerente: False

    - Tópico 8 (n=5)
      • top termos: lento, manual, turno, demanda, curto, lenta
      • exemplos:
      - setup lento na troca de turno
      - sistema lento no turno
      - turno curto pra demanda
      - conferencia manual lenta
      - picking manual lento
      • resumo: Relatos focados em lento, manual, turno. Exemplo representativo: "setup lento na troca de turno".
      • genérico/incoerente: False

    - Tópico 9 (n=5)
      • top termos: operador, novo, cansado, sobrecarregado, treinamento, perdido
      • exemplos:
      - operador sobrecarregado
      - operador cansado
      - falta treinamento novo operador
      - operador novo perdido
      - operador sem apoio
      • resumo: Relatos focados em operador, novo, cansado. Exemplo representativo: "operador sobrecarregado".
      • genérico/incoerente: False

    - Tópico 10 (n=4)
      • top termos: maq, resolve, ninguém, msm, ponto, parando
      • exemplos:
      - maq 3 parou dnv
      - ninguém resolve problema da maq
      - maq parando sempre no msm ponto
      - maq superaquecendo
      • resumo: Relatos focados em maq, resolve, ninguém. Exemplo representativo: "maq 3 parou dnv".
      • genérico/incoerente: False

    - Tópico 11 (n=4)
      • top termos: picking, caixa, confunde, enderecos, recorrente, confuso
      • exemplos:
      - picking confuso
      - falta caixa pra picking
      - erro recorrente no picking
      - picking confunde enderecos
      • resumo: Relatos focados em picking, caixa, confunde. Exemplo representativo: "picking confuso".
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

