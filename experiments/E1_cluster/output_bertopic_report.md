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

