Pipeline: Pipeline A — Baseline de MVP (KMeans)
  - nº de clusters: 6
  - estabilidade (ARI entre duas execuções): 0.539
  - % de ruído (aprox.): n/a
    - Cluster 0 (n=183)
      • top termos: lider, maq, hj, refeita, cobra, rota
      • exemplos:
      - maq 3 parou dnv
      - mt calor na linha 2
      - lider n escuta ngm
      - maq velha demais
      - mt retrabalho na linha 3
      • resumo: Relatos focados em lider, maq, hj. Exemplo representativo: "maq 3 parou dnv".
      • genérico/incoerente: False

    - Cluster 1 (n=113)
      • top termos: carregamento, refugos, excesso, rota, excesso refugos, sobrecarregada
      • exemplos:
      - fila enorme no almoco
      - ambiente pesado hj
      - fila grande no carregamento
      - doca congestionada
      - retrabalho no carregamento
      • resumo: Relatos focados em carregamento, refugos, excesso. Exemplo representativo: "fila enorme no almoco".
      • genérico/incoerente: False

    - Cluster 2 (n=69)
      • top termos: sensor, scanner, bateria, desalinhado, sensor desalinhado, scanner bateria
      • exemplos:
      - sensor falhando toda hora
      - sensor temp bugado
      - sensor nao le direito
      - empilhadeira parada sem bateria
      - scanner nao funciona direito
      • resumo: Relatos focados em sensor, scanner, bateria. Exemplo representativo: "sensor falhando toda hora".
      • genérico/incoerente: False

    - Cluster 3 (n=250)
      • top termos: erro, operador, picking, pedido, equipe, errado
      • exemplos:
      - ninguém resolve problema da maq
      - checklist de setup incompleto
      - maq parando sempre no msm ponto
      - operador sobrecarregado
      - picking confuso
      • resumo: Relatos focados em erro, operador, picking. Exemplo representativo: "ninguém resolve problema da maq".
      • genérico/incoerente: False

    - Cluster 4 (n=175)
      • top termos: linha, turno, atrasou, frequente, separacao, linha atrasou
      • exemplos:
      - prensa travou no meio do turno
      - setup lento na troca de turno
      - linha 1 atrasou dnv
      - troca de turno confusa
      - ritmo puxado demais
      • resumo: Relatos focados em linha, turno, atrasou. Exemplo representativo: "prensa travou no meio do turno".
      • genérico/incoerente: False

    - Cluster 5 (n=210)
      • top termos: palete, mal, estoque, sistema, refeitorio, layout
      • exemplos:
      - refeitorio horrivel hj
      - barulho excessivo na prensa
      - dor nas costas depois do turno
      - linha parada por falha eletrica
      - esteira parou 2x hoje
      • resumo: Relatos focados em palete, mal, estoque. Exemplo representativo: "refeitorio horrivel hj".
      • genérico/incoerente: False

  - notas:
  - KMeans com k fixo (k=6) por simplicidade e alinhamento com expectativa de 5-8 temas operacionais em ~100 relatos.


Pipeline: Pipeline B — Densidade e ruído (HDBSCAN)
  - nº de clusters: 86
  - estabilidade (ARI entre duas execuções): n/a
  - % de ruído (aprox.): 14.8%
    - Cluster -1 (n=148)
      • top termos: lider, linha, maq, turno, retrabalho, mt
      • exemplos:
      - maq 3 parou dnv
      - linha 1 atrasou dnv
      - maq velha demais
      - mt retrabalho na linha 3
      - ninguém resolve problema da maq
      • resumo: Relatos focados em lider, linha, maq. Exemplo representativo: "maq 3 parou dnv".
      • genérico/incoerente: True

    - Cluster 0 (n=6)
      • top termos: comida, comida fria, fria, fria setor, setor, refeitorio
      • exemplos:
      - comida fria no refeitorio
      - comida fria por falha eletrica
      - comida fria toda hora
      - comida fria temp bugado
      - comida fria no setor b
      • resumo: Relatos focados em comida, comida fria, fria. Exemplo representativo: "comida fria no refeitorio".
      • genérico/incoerente: False

    - Cluster 1 (n=7)
      • top termos: sistema atualiza, sistema, atualiza, manual, aviso, atualiza manual
      • exemplos:
      - sistema nao atualiza estoque
      - sistema n atualiza sem aviso
      - sistema n atualiza no armazem 4
      - sistema n atualiza
      - sistema n atualiza
      • resumo: Relatos focados em sistema atualiza, sistema, atualiza. Exemplo representativo: "sistema nao atualiza estoque".
      • genérico/incoerente: False

    - Cluster 2 (n=10)
      • top termos: erro, mt erro, mt, erro conferencia, conferencia, conferencia erro
      • exemplos:
      - mt erro na conferencia
      - mt erro na conferencia
      - mt erro na conferencia
      - mt erro na conferencia no turno
      - mt erro na conferencia com urgencia
      • resumo: Relatos focados em erro, mt erro, mt. Exemplo representativo: "mt erro na conferencia".
      • genérico/incoerente: False

    - Cluster 3 (n=7)
      • top termos: organizacao, doca organizacao, doca, turno, organizacao turno, organizacao dnv
      • exemplos:
      - doca sem organizacao
      - doca sem organizacao
      - doca sem organizacao
      - doca sem organizacao no turno
      - doca sem organizacao
      • resumo: Relatos focados em organizacao, doca organizacao, doca. Exemplo representativo: "doca sem organizacao".
      • genérico/incoerente: False

    - Cluster 4 (n=10)
      • top termos: checklist, incompleto, checklist incompleto, barulho, incompleto barulho, prensa
      • exemplos:
      - checklist de setup incompleto
      - checklist incompleto temp bugado
      - checklist incompleto na linha 2
      - checklist incompleto hj
      - checklist incompleto da maq
      • resumo: Relatos focados em checklist, incompleto, checklist incompleto. Exemplo representativo: "checklist de setup incompleto".
      • genérico/incoerente: False

    - Cluster 5 (n=11)
      • top termos: setup, errado, setup errado, dnv, errado dnv, errado setup
      • exemplos:
      - setup feito errado
      - setup errado no setor b
      - setup errado mas n ajuda
      - setup errado dnv
      - setup errado no inicio turno
      • resumo: Relatos focados em setup, errado, setup errado. Exemplo representativo: "setup feito errado".
      • genérico/incoerente: False

    - Cluster 6 (n=21)
      • top termos: falta, falta treinamento, treinamento, insuficiente, treinamento insuficiente, turno
      • exemplos:
      - falta treinamento novo operador
      - treinamento insuficiente sempre no msm ponto
      - falta treinamento no meio do turno
      - treinamento insuficiente falhou
      - treinamento insuficiente ngm
      • resumo: Relatos focados em falta, falta treinamento, treinamento. Exemplo representativo: "falta treinamento novo operador".
      • genérico/incoerente: False

    - Cluster 7 (n=6)
      • top termos: bateria, empilhadeira, falhando bateria, empilhadeira falhando, falhando, empilhadeira parada
      • exemplos:
      - empilhadeira parada sem bateria
      - estoque mal enderecado sem bateria
      - fila grande p descarregar sem bateria
      - empilhadeira falhando sem bateria
      - empilhadeira falhando sem bateria
      • resumo: Relatos focados em bateria, empilhadeira, falhando bateria. Exemplo representativo: "empilhadeira parada sem bateria".
      • genérico/incoerente: False

    - Cluster 8 (n=8)
      • top termos: scanner funciona, scanner, funciona, urgencia, manual, funciona urgencia
      • exemplos:
      - scanner nao funciona direito
      - scanner n funciona
      - scanner n funciona manual
      - scanner n funciona com urgencia
      - scanner n funciona desnecessario
      • resumo: Relatos focados em scanner funciona, scanner, funciona. Exemplo representativo: "scanner nao funciona direito".
      • genérico/incoerente: False

    - Cluster 9 (n=14)
      • top termos: bateria, scanner bateria, scanner, bateria bateria, resultado, manual
      • exemplos:
      - scanner sem bateria
      - scanner sem bateria sem bateria
      - scanner sem bateria
      - scanner sem bateria
      - scanner sem bateria
      • resumo: Relatos focados em bateria, scanner bateria, scanner. Exemplo representativo: "scanner sem bateria".
      • genérico/incoerente: False

    - Cluster 10 (n=8)
      • top termos: calor, mt calor, mt, calor linha, linha, barulho
      • exemplos:
      - mt calor na linha 2
      - mt calor e barulho
      - mt calor sempre no msm ponto
      - mt calor puxado demais
      - mt calor na linha 3
      • resumo: Relatos focados em calor, mt calor, mt. Exemplo representativo: "mt calor na linha 2".
      • genérico/incoerente: False

    - Cluster 11 (n=6)
      • top termos: ilegivel, etiqueta ilegivel, etiqueta, ilegivel estoque, ilegivel direito, ilegivel armazem
      • exemplos:
      - etiqueta ilegivel
      - etiqueta ilegivel por estoque
      - etiqueta ilegivel direito
      - etiqueta ilegivel
      - etiqueta ilegivel no armazem 4
      • resumo: Relatos focados em ilegivel, etiqueta ilegivel, etiqueta. Exemplo representativo: "etiqueta ilegivel".
      • genérico/incoerente: False

    - Cluster 12 (n=6)
      • top termos: voltou errado, voltou, pedido voltou, pedido, errado, turno
      • exemplos:
      - pedido voltou errado
      - pedido voltou errado no turno
      - pedido voltou errado
      - pedido voltou errado
      - pedido voltou errado hj
      • resumo: Relatos focados em voltou errado, voltou, pedido voltou. Exemplo representativo: "pedido voltou errado".
      • genérico/incoerente: False

    - Cluster 13 (n=20)
      • top termos: operador, sobrecarregado, cansado, operador cansado, operador sobrecarregado, apoio
      • exemplos:
      - operador sobrecarregado
      - operador cansado
      - operador sem apoio
      - operador sem apoio pela manha
      - operador sem apoio mal ajustado
      • resumo: Relatos focados em operador, sobrecarregado, cansado. Exemplo representativo: "operador sobrecarregado".
      • genérico/incoerente: False

    - Cluster 14 (n=12)
      • top termos: operador, novo, perdido, operador novo, novo perdido, perdido aviso
      • exemplos:
      - operador novo perdido
      - operador novo perdido
      - operador novo perdido
      - operador novo perdido
      - operador novo perdido pra demanda
      • resumo: Relatos focados em operador, novo, perdido. Exemplo representativo: "operador novo perdido".
      • genérico/incoerente: False

    - Cluster 15 (n=7)
      • top termos: pedido incompleto, pedido, incompleto, manha, incompleto manha, incompleto erro
      • exemplos:
      - pedido incompleto
      - pedido incompleto por erro
      - pedido incompleto
      - pedido incompleto
      - pedido incompleto
      • resumo: Relatos focados em pedido incompleto, pedido, incompleto. Exemplo representativo: "pedido incompleto".
      • genérico/incoerente: False

    - Cluster 16 (n=9)
      • top termos: trocado, pedido trocado, pedido, trocado manual, trocado frequente, trocado estoque
      • exemplos:
      - pedido trocado
      - pedido trocado
      - pedido trocado por estoque
      - pedido trocado manual
      - pedido trocado
      • resumo: Relatos focados em trocado, pedido trocado, pedido. Exemplo representativo: "pedido trocado".
      • genérico/incoerente: False

    - Cluster 17 (n=6)
      • top termos: horas extras, horas, excesso, excesso horas, extras, confusa
      • exemplos:
      - excesso de horas extras
      - excesso de horas extras por falha eletrica
      - excesso de horas extras de setup
      - excesso de horas extras na troca de turno
      - excesso de horas extras ngm
      • resumo: Relatos focados em horas extras, horas, excesso. Exemplo representativo: "excesso de horas extras".
      • genérico/incoerente: False

    - Cluster 18 (n=5)
      • top termos: turno curto, turno, curto, resultado, curto resultado, pra demanda
      • exemplos:
      - turno curto pra demanda
      - turno curto
      - turno curto resultado
      - turno curto
      - turno curto
      • resumo: Relatos focados em turno curto, turno, curto. Exemplo representativo: "turno curto pra demanda".
      • genérico/incoerente: False

    - Cluster 19 (n=6)
      • top termos: almoco, fila, fila almoco, enorme almoco, enorme, fila enorme
      • exemplos:
      - fila enorme no almoco
      - fila no almoco p chegar
      - fila no almoco na linha 3
      - manutencao demorou enorme no almoco
      - equipe reduzida enorme no almoco
      • resumo: Relatos focados em almoco, fila, fila almoco. Exemplo representativo: "fila enorme no almoco".
      • genérico/incoerente: False

    - Cluster 20 (n=22)
      • top termos: equipe, doca equipe, doca, equipe incompleta, incompleta, reduzida
      • exemplos:
      - doca sem equipe suficiente
      - doca sem equipe
      - equipe incompleta
      - doca sem equipe enderecos
      - doca sem equipe
      • resumo: Relatos focados em equipe, doca equipe, doca. Exemplo representativo: "doca sem equipe suficiente".
      • genérico/incoerente: False

    - Cluster 21 (n=5)
      • top termos: produto danificado, produto, danificado, urgencia, enderecos, danificado urgencia
      • exemplos:
      - produto danificado com urgencia
      - produto danificado enderecos
      - produto danificado
      - refeitorio sujo por falha eletrica
      - produto danificado
      • resumo: Relatos focados em produto danificado, produto, danificado. Exemplo representativo: "produto danificado com urgencia".
      • genérico/incoerente: False

    - Cluster 22 (n=7)
      • top termos: etiqueta errada, etiqueta, errada, errada dnv, errada aviso, dnv
      • exemplos:
      - etiqueta errada
      - etiqueta errada
      - etiqueta errada
      - etiqueta errada
      - etiqueta errada dnv
      • resumo: Relatos focados em etiqueta errada, etiqueta, errada. Exemplo representativo: "etiqueta errada".
      • genérico/incoerente: False

    - Cluster 23 (n=7)
      • top termos: mt deslocamento, mt, deslocamento, manual, desnecessario, deslocamento manual
      • exemplos:
      - mt deslocamento desnecessario
      - mt deslocamento
      - mt deslocamento
      - mt deslocamento
      - mt deslocamento
      • resumo: Relatos focados em mt deslocamento, mt, deslocamento. Exemplo representativo: "mt deslocamento desnecessario".
      • genérico/incoerente: False

    - Cluster 24 (n=5)
      • top termos: inventario errado, inventario, errado, estoque, erro, errado estoque
      • exemplos:
      - inventario errado
      - inventario errado por estoque
      - inventario errado carregado
      - inventario errado
      - inventario errado por erro
      • resumo: Relatos focados em inventario errado, inventario, errado. Exemplo representativo: "inventario errado".
      • genérico/incoerente: False

    - Cluster 25 (n=9)
      • top termos: sistema bugado, sistema, bugado, urgencia, enderecos, direito
      • exemplos:
      - sistema bugado enderecos
      - sistema bugado
      - sistema bugado sem aviso
      - sistema bugado
      - sistema bugado com urgencia
      • resumo: Relatos focados em sistema bugado, sistema, bugado. Exemplo representativo: "sistema bugado enderecos".
      • genérico/incoerente: False

    - Cluster 26 (n=41)
      • top termos: sensor, desalinhado, sensor desalinhado, sensor falhando, falhando, bugado
      • exemplos:
      - sensor falhando toda hora
      - sensor temp bugado
      - sensor nao le direito
      - sensor desalinhado
      - sensor falhando pela manha
      • resumo: Relatos focados em sensor, desalinhado, sensor desalinhado. Exemplo representativo: "sensor falhando toda hora".
      • genérico/incoerente: False

    - Cluster 27 (n=7)
      • top termos: caiu, sistema caiu, sistema, turno, meio turno, meio
      • exemplos:
      - sistema caiu no meio do turno
      - sistema caiu pela manha
      - sistema caiu
      - sistema caiu enderecos
      - sistema bugado por erro
      • resumo: Relatos focados em caiu, sistema caiu, sistema. Exemplo representativo: "sistema caiu no meio do turno".
      • genérico/incoerente: False

    - Cluster 28 (n=14)
      • top termos: refugos, excesso refugos, excesso, alta, alta refugos, pressao
      • exemplos:
      - excesso de refugos
      - excesso de refugos feito errado
      - excesso de refugos de refugos
      - excesso de refugos no inicio turno
      - excesso de refugos na linha 3
      • resumo: Relatos focados em refugos, excesso refugos, excesso. Exemplo representativo: "excesso de refugos".
      • genérico/incoerente: False

    - Cluster 29 (n=5)
      • top termos: geral, reclamacao geral, reclamacao, linha, demais, geral demais
      • exemplos:
      - reclamacao geral toda hora
      - reclamacao geral mal ajustado
      - reclamacao geral na troca de turno
      - reclamacao geral na linha 3
      - reclamacao geral demais
      • resumo: Relatos focados em geral, reclamacao geral, reclamacao. Exemplo representativo: "reclamacao geral toda hora".
      • genérico/incoerente: False

    - Cluster 30 (n=5)
      • top termos: doca congestionada, doca, congestionada, estoque, dnv, congestionada estoque
      • exemplos:
      - doca congestionada
      - doca congestionada
      - doca congestionada
      - doca congestionada estoque
      - doca congestionada dnv
      • resumo: Relatos focados em doca congestionada, doca, congestionada. Exemplo representativo: "doca congestionada".
      • genérico/incoerente: False

    - Cluster 31 (n=18)
      • top termos: layout confuso, confuso, layout, ruim, layout ruim, linha
      • exemplos:
      - layout confuso
      - layout da linha ruim
      - layout confuso dnv
      - layout confuso pra demanda
      - layout ruim confusa
      • resumo: Relatos focados em layout confuso, confuso, layout. Exemplo representativo: "layout confuso".
      • genérico/incoerente: False

    - Cluster 32 (n=9)
      • top termos: reentrega frequente, reentrega, frequente, frequente armazem, armazem, turno
      • exemplos:
      - reentrega frequente
      - reentrega frequente no meio do turno
      - reentrega frequente no armazem 4
      - reentrega frequente no armazem 4
      - reentrega frequente no turno
      • resumo: Relatos focados em reentrega frequente, reentrega, frequente. Exemplo representativo: "reentrega frequente".
      • genérico/incoerente: False

    - Cluster 33 (n=5)
      • top termos: dor costas, dor, costas, turno, supervisor, prensa
      • exemplos:
      - dor nas costas depois do turno
      - dor nas costas pelo supervisor
      - dor nas costas na prensa
      - dor nas costas mal ajustado
      - dor nas costas demais
      • resumo: Relatos focados em dor costas, dor, costas. Exemplo representativo: "dor nas costas depois do turno".
      • genérico/incoerente: False

    - Cluster 34 (n=11)
      • top termos: frequente expedicao, frequente, expedicao, erro frequente, erro, expedicao estoque
      • exemplos:
      - erro frequente na expedicao
      - erro frequente na expedicao hj
      - erro frequente na expedicao por estoque
      - erro frequente na expedicao
      - erro frequente na expedicao
      • resumo: Relatos focados em frequente expedicao, frequente, expedicao. Exemplo representativo: "erro frequente na expedicao".
      • genérico/incoerente: False

    - Cluster 35 (n=8)
      • top termos: empilhadeira disputada, empilhadeira, disputada
      • exemplos:
      - empilhadeira disputada
      - empilhadeira disputada
      - empilhadeira disputada
      - empilhadeira disputada
      - empilhadeira disputada
      • resumo: Relatos focados em empilhadeira disputada, empilhadeira, disputada. Exemplo representativo: "empilhadeira disputada".
      • genérico/incoerente: False

    - Cluster 36 (n=16)
      • top termos: pesada, carga, carga pesada, pesado, ambiente pesado, ambiente
      • exemplos:
      - ambiente pesado hj
      - carga pesada
      - carga pesada
      - carga pesada
      - carga pesada
      • resumo: Relatos focados em pesada, carga, carga pesada. Exemplo representativo: "ambiente pesado hj".
      • genérico/incoerente: False

    - Cluster 37 (n=9)
      • top termos: retrabalho carregamento, retrabalho, carregamento, suficiente, direito, carregamento suficiente
      • exemplos:
      - retrabalho no carregamento
      - retrabalho no carregamento
      - retrabalho no carregamento
      - retrabalho no carregamento carregado
      - retrabalho no carregamento
      • resumo: Relatos focados em retrabalho carregamento, retrabalho, carregamento. Exemplo representativo: "retrabalho no carregamento".
      • genérico/incoerente: False

    - Cluster 38 (n=10)
      • top termos: quebrada, ferramenta, ferramenta quebrada, quebrada demais, barulho, demais
      • exemplos:
      - ferramenta quebrada temp bugado
      - ferramenta quebrada na linha 2
      - ferramenta quebrada e barulho
      - ferramenta quebrada n le direito
      - ferramenta quebrada a tarde
      • resumo: Relatos focados em quebrada, ferramenta, ferramenta quebrada. Exemplo representativo: "ferramenta quebrada temp bugado".
      • genérico/incoerente: False

    - Cluster 39 (n=11)
      • top termos: meta irreal, meta, irreal, toda hora, temp bugado, temp
      • exemplos:
      - meta irreal temp bugado
      - meta irreal hj
      - meta irreal mas n ajuda
      - meta irreal pela manha
      - meta irreal toda hora
      • resumo: Relatos focados em meta irreal, meta, irreal. Exemplo representativo: "meta irreal temp bugado".
      • genérico/incoerente: False

    - Cluster 40 (n=7)
      • top termos: quebrado, palete quebrado, palete, quebrado endereco, quebrado armazem, endereco
      • exemplos:
      - palete quebrado
      - palete quebrado no armazem 4
      - palete quebrado por endereco
      - palete quebrado
      - palete quebrado
      • resumo: Relatos focados em quebrado, palete quebrado, palete. Exemplo representativo: "palete quebrado".
      • genérico/incoerente: False

    - Cluster 41 (n=5)
      • top termos: palete errado, palete, errado, estoque, errado estoque, errado dnv
      • exemplos:
      - palete errado carregado
      - palete errado
      - palete errado por estoque
      - palete errado dnv
      - palete errado estoque
      • resumo: Relatos focados em palete errado, palete, errado. Exemplo representativo: "palete errado carregado".
      • genérico/incoerente: False

    - Cluster 42 (n=5)
      • top termos: falta caixa, falta, caixa, manha, frequente, caixa manha
      • exemplos:
      - falta caixa pra picking
      - falta caixa pela manha
      - falta caixa
      - falta caixa
      - falta caixa frequente
      • resumo: Relatos focados em falta caixa, falta, caixa. Exemplo representativo: "falta caixa pra picking".
      • genérico/incoerente: False

    - Cluster 43 (n=11)
      • top termos: refeitorio, horrivel, refeitorio horrivel, sujo, refeitorio sujo, turno
      • exemplos:
      - refeitorio horrivel hj
      - refeitorio sujo
      - refeitorio horrivel da maq
      - refeitorio sujo feito errado
      - refeitorio horrivel na troca de turno
      • resumo: Relatos focados em refeitorio, horrivel, refeitorio horrivel. Exemplo representativo: "refeitorio horrivel hj".
      • genérico/incoerente: False

    - Cluster 44 (n=14)
      • top termos: carregamento, grande carregamento, grande, fila grande, fila, descarregar
      • exemplos:
      - fila grande no carregamento
      - fila grande p descarregar
      - fila grande no carregamento
      - fila grande no carregamento hj
      - fila grande no carregamento no turno
      • resumo: Relatos focados em carregamento, grande carregamento, grande. Exemplo representativo: "fila grande no carregamento".
      • genérico/incoerente: False

    - Cluster 45 (n=6)
      • top termos: producao, falha, falha producao, turno, producao meio, meio turno
      • exemplos:
      - falha na producao mas n ajuda
      - falha na producao desalinhado
      - falha na producao pela manha
      - falha na producao no meio do turno
      - falha na producao no meio do turno
      • resumo: Relatos focados em producao, falha, falha producao. Exemplo representativo: "falha na producao mas n ajuda".
      • genérico/incoerente: False

    - Cluster 46 (n=13)
      • top termos: manual lenta, lenta, conferencia manual, conferencia, manual, picking
      • exemplos:
      - conferencia manual lenta
      - picking manual lento
      - picking manual lento
      - conferencia manual lenta pela manha
      - conferencia manual lenta
      • resumo: Relatos focados em manual lenta, lenta, conferencia manual. Exemplo representativo: "conferencia manual lenta".
      • genérico/incoerente: False

    - Cluster 47 (n=10)
      • top termos: lider, cobra, lider cobra, refeitorio, cobra refeitorio, dnv
      • exemplos:
      - lider cobra no inicio turno
      - lider cobra no refeitorio
      - lider cobra no inicio turno
      - lider cobra no refeitorio
      - lider so cobra
      • resumo: Relatos focados em lider, cobra, lider cobra. Exemplo representativo: "lider cobra no inicio turno".
      • genérico/incoerente: False

    - Cluster 48 (n=7)
      • top termos: estoque desorganizado, estoque, desorganizado, hj, direito, desorganizado hj
      • exemplos:
      - estoque desorganizado
      - estoque desorganizado direito
      - estoque desorganizado
      - estoque desorganizado hj
      - estoque desorganizado
      • resumo: Relatos focados em estoque desorganizado, estoque, desorganizado. Exemplo representativo: "estoque desorganizado".
      • genérico/incoerente: False

    - Cluster 49 (n=6)
      • top termos: picking confuso, picking, confuso, suficiente, confuso suficiente
      • exemplos:
      - picking confuso
      - picking confuso
      - picking confuso
      - picking confuso suficiente
      - picking confuso
      • resumo: Relatos focados em picking confuso, picking, confuso. Exemplo representativo: "picking confuso".
      • genérico/incoerente: False

    - Cluster 50 (n=9)
      • top termos: prensa, prensa travou, travou, turno, troca turno, troca
      • exemplos:
      - prensa travou no meio do turno
      - barulho excessivo na prensa
      - prensa travou sobrecarregado
      - prensa travou na troca de turno
      - prensa travou desconfortavel
      • resumo: Relatos focados em prensa, prensa travou, travou. Exemplo representativo: "prensa travou no meio do turno".
      • genérico/incoerente: False

    - Cluster 51 (n=26)
      • top termos: maq, parando, maq parando, parou, maq parou, velha
      • exemplos:
      - maq parando sempre no msm ponto
      - maq parando sempre no msm ponto
      - maq parando ngm
      - maq vibrando hj
      - maq velha toda hora
      • resumo: Relatos focados em maq, parando, maq parando. Exemplo representativo: "maq parando sempre no msm ponto".
      • genérico/incoerente: False

    - Cluster 52 (n=13)
      • top termos: falhou, seguranca falhou, seguranca, check, check seguranca, ajuda
      • exemplos:
      - check de seguranca falhou
      - check de seguranca falhou puxado demais
      - check de seguranca falhou mal ajustado
      - check de seguranca falhou desalinhado
      - check de seguranca falhou da maq
      • resumo: Relatos focados em falhou, seguranca falhou, seguranca. Exemplo representativo: "check de seguranca falhou".
      • genérico/incoerente: False

    - Cluster 53 (n=8)
      • top termos: parou, esteira, esteira parou, hj, parou hj, turno
      • exemplos:
      - esteira parou sem apoio
      - esteira parou hj
      - esteira parou da linha
      - esteira parou extras
      - esteira parou depois do turno
      • resumo: Relatos focados em parou, esteira, esteira parou. Exemplo representativo: "esteira parou sem apoio".
      • genérico/incoerente: False

    - Cluster 54 (n=13)
      • top termos: estoque divergente, estoque, divergente, frequente, endereco, divergente frequente
      • exemplos:
      - estoque divergente
      - estoque divergente frequente
      - estoque divergente
      - estoque divergente
      - estoque divergente
      • resumo: Relatos focados em estoque divergente, estoque, divergente. Exemplo representativo: "estoque divergente".
      • genérico/incoerente: False

    - Cluster 55 (n=7)
      • top termos: turno, turno confusa, confusa, troca turno, troca, confusa turno
      • exemplos:
      - troca de turno confusa
      - troca de turno confusa hj
      - posto mal ajustado na troca de turno
      - troca de turno confusa no meio do turno
      - troca de turno confusa desalinhado
      • resumo: Relatos focados em turno, turno confusa, confusa. Exemplo representativo: "troca de turno confusa".
      • genérico/incoerente: False

    - Cluster 56 (n=12)
      • top termos: iluminação ruim, iluminação, ruim, hj, turno noite, noite
      • exemplos:
      - iluminação ruim na linha 3
      - iluminação ruim demais
      - iluminação ruim no setor b
      - iluminação ruim 2x hj
      - iluminação ruim sujo
      • resumo: Relatos focados em iluminação ruim, iluminação, ruim. Exemplo representativo: "iluminação ruim na linha 3".
      • genérico/incoerente: False

    - Cluster 57 (n=17)
      • top termos: lider, ausente, lider ausente, lider escuta, escuta, hj
      • exemplos:
      - lider n escuta ngm
      - lider ausente
      - lider n escuta desconfortavel
      - lider n escuta pela manha
      - lider n escuta temp bugado
      • resumo: Relatos focados em lider, ausente, lider ausente. Exemplo representativo: "lider n escuta ngm".
      • genérico/incoerente: False

    - Cluster 58 (n=7)
      • top termos: retorno, lider retorno, lider, retorno manha, retorno enderecos, manha
      • exemplos:
      - lider n da retorno
      - lider n da retorno
      - lider n da retorno
      - lider n da retorno pela manha
      - lider n da retorno
      • resumo: Relatos focados em retorno, lider retorno, lider. Exemplo representativo: "lider n da retorno".
      • genérico/incoerente: False

    - Cluster 59 (n=5)
      • top termos: pra picking, pra, picking, rota, sobrecarregada pra, sobrecarregada
      • exemplos:
      - rota sobrecarregada pra picking
      - rota sobrecarregada pra picking
      - retrabalho na rota pra picking
      - rota sobrecarregada pra picking
      - empilhadeira parada pra picking
      • resumo: Relatos focados em pra picking, pra, picking. Exemplo representativo: "rota sobrecarregada pra picking".
      • genérico/incoerente: False

    - Cluster 60 (n=10)
      • top termos: ritmo puxado, ritmo, puxado, hj, puxado hj, puxado demais
      • exemplos:
      - ritmo puxado demais
      - ritmo puxado mal ajustado
      - ritmo puxado confusa
      - ritmo puxado no refeitorio
      - ritmo puxado 2x hj
      • resumo: Relatos focados em ritmo puxado, ritmo, puxado. Exemplo representativo: "ritmo puxado demais".
      • genérico/incoerente: False

    - Cluster 61 (n=11)
      • top termos: pressao meta, meta, muita pressao, muita, pressao, mt pressao
      • exemplos:
      - mt pressao por meta
      - muita pressao por meta
      - muita pressao por meta entrega
      - pressao alta p chegar
      - muita pressao por meta resultado
      • resumo: Relatos focados em pressao meta, meta, muita pressao. Exemplo representativo: "mt pressao por meta".
      • genérico/incoerente: False

    - Cluster 62 (n=12)
      • top termos: palete padrao, palete, padrao, suficiente, padrao suficiente, padrao desnecessario
      • exemplos:
      - palete fora do padrao
      - palete fora do padrao
      - palete fora do padrao
      - palete fora do padrao desnecessario
      - palete fora do padrao
      • resumo: Relatos focados em palete padrao, palete, padrao. Exemplo representativo: "palete fora do padrao".
      • genérico/incoerente: False

    - Cluster 63 (n=12)
      • top termos: falhando, empilhadeira falhando, empilhadeira, manual, falhando manual, manha
      • exemplos:
      - empilhadeira falhando
      - empilhadeira falhando pra picking
      - empilhadeira falhando
      - empilhadeira falhando
      - empilhadeira falhando
      • resumo: Relatos focados em falhando, empilhadeira falhando, empilhadeira. Exemplo representativo: "empilhadeira falhando".
      • genérico/incoerente: False

    - Cluster 64 (n=6)
      • top termos: lento, setup lento, setup, turno, manutencao, lento chegar
      • exemplos:
      - setup lento na troca de turno
      - sistema lento no turno
      - setup lento por manutencao
      - setup lento p chegar
      - setup lento na linha 2
      • resumo: Relatos focados em lento, setup lento, setup. Exemplo representativo: "setup lento na troca de turno".
      • genérico/incoerente: False

    - Cluster 65 (n=9)
      • top termos: sobrecarregada, rota sobrecarregada, rota, sobrecarregada hj, sobrecarregada endereco, hj
      • exemplos:
      - rota sobrecarregada
      - rota sobrecarregada por endereco
      - rota sobrecarregada hj
      - rota sobrecarregada
      - rota sobrecarregada
      • resumo: Relatos focados em sobrecarregada, rota sobrecarregada, rota. Exemplo representativo: "rota sobrecarregada".
      • genérico/incoerente: False

    - Cluster 66 (n=7)
      • top termos: parada, empilhadeira parada, empilhadeira, turno, meio turno, meio
      • exemplos:
      - empilhadeira parada no meio do turno
      - rota sobrecarregada no meio do turno
      - empilhadeira parada hj
      - empilhadeira parada
      - empilhadeira parada
      • resumo: Relatos focados em parada, empilhadeira parada, empilhadeira. Exemplo representativo: "empilhadeira parada no meio do turno".
      • genérico/incoerente: False

    - Cluster 67 (n=13)
      • top termos: picking, recorrente picking, recorrente, erro recorrente, erro, picking aviso
      • exemplos:
      - erro recorrente no picking
      - erro recorrente no picking sem aviso
      - erro recorrente no picking
      - erro recorrente no picking sem aviso
      - erro recorrente no picking carregado
      • resumo: Relatos focados em picking, recorrente picking, recorrente. Exemplo representativo: "erro recorrente no picking".
      • genérico/incoerente: False

    - Cluster 68 (n=12)
      • top termos: picking confunde, picking, confunde, erro, enderecos, confunde erro
      • exemplos:
      - picking confunde enderecos
      - picking confunde
      - picking confunde
      - picking confunde
      - picking confunde por erro
      • resumo: Relatos focados em picking confunde, picking, confunde. Exemplo representativo: "picking confunde enderecos".
      • genérico/incoerente: False

    - Cluster 69 (n=7)
      • top termos: faltando, material faltando, material, linha, faltando linha, sujo
      • exemplos:
      - linha parou por falta material
      - material faltando puxado demais
      - material faltando da linha
      - material faltando sujo
      - material faltando no meio do turno
      • resumo: Relatos focados em faltando, material faltando, material. Exemplo representativo: "linha parou por falta material".
      • genérico/incoerente: False

    - Cluster 70 (n=8)
      • top termos: ventilacao pessima, pessima, ventilacao, setup, pessima setup, pessima confusa
      • exemplos:
      - ventilacao pessima confusa
      - ventilacao pessima desalinhado
      - ventilacao pessima temp bugado
      - ventilacao pessima de setup
      - ventilacao pessima ngm
      • resumo: Relatos focados em ventilacao pessima, pessima, ventilacao. Exemplo representativo: "ventilacao pessima confusa".
      • genérico/incoerente: False

    - Cluster 71 (n=10)
      • top termos: mal enderecado, mal, estoque mal, estoque, enderecado, frequente
      • exemplos:
      - estoque mal enderecado
      - estoque mal enderecado
      - estoque mal enderecado
      - estoque mal enderecado desnecessario
      - estoque mal enderecado
      • resumo: Relatos focados em mal enderecado, mal, estoque mal. Exemplo representativo: "estoque mal enderecado".
      • genérico/incoerente: False

    - Cluster 72 (n=11)
      • top termos: barulho, barulho excessivo, excessivo, refeitorio, demais, excessivo demais
      • exemplos:
      - barulho excessivo confusa
      - barulho excessivo demais
      - barulho excessivo sobrecarregado
      - barulho excessivo na troca de turno
      - barulho excessivo sem aviso
      • resumo: Relatos focados em barulho, barulho excessivo, excessivo. Exemplo representativo: "barulho excessivo confusa".
      • genérico/incoerente: False

    - Cluster 73 (n=6)
      • top termos: separacao, erro separacao, erro, separacao estoque, separacao endereco, estoque
      • exemplos:
      - erro na separacao por endereco
      - erro na separacao
      - erro na separacao estoque
      - erro na separacao
      - erro na separacao
      • resumo: Relatos focados em separacao, erro separacao, erro. Exemplo representativo: "erro na separacao por endereco".
      • genérico/incoerente: False

    - Cluster 74 (n=10)
      • top termos: mal sinalizada, sinalizada, doca mal, mal, doca, sinalizada turno
      • exemplos:
      - doca mal sinalizada
      - doca mal sinalizada
      - doca mal sinalizada por erro
      - doca mal sinalizada enderecos
      - doca mal sinalizada por erro
      • resumo: Relatos focados em mal sinalizada, sinalizada, doca mal. Exemplo representativo: "doca mal sinalizada".
      • genérico/incoerente: False

    - Cluster 75 (n=7)
      • top termos: separacao lenta, separacao, lenta, lenta hj, lenta frequente, lenta entrega
      • exemplos:
      - separacao lenta hj
      - separacao lenta
      - separacao lenta frequente
      - separacao lenta
      - separacao lenta
      • resumo: Relatos focados em separacao lenta, separacao, lenta. Exemplo representativo: "separacao lenta hj".
      • genérico/incoerente: False

    - Cluster 76 (n=5)
      • top termos: caminhao atrasado, caminhao, atrasado, frequente, estoque, erro
      • exemplos:
      - caminhao atrasado estoque
      - caminhao atrasado frequente
      - caminhao atrasado
      - caminhao atrasado por erro
      - caminhao atrasado enderecos
      • resumo: Relatos focados em caminhao atrasado, caminhao, atrasado. Exemplo representativo: "caminhao atrasado estoque".
      • genérico/incoerente: False

    - Cluster 77 (n=9)
      • top termos: rota atrasou, rota, atrasou, enderecos, atrasou enderecos, resultado
      • exemplos:
      - rota atrasou entrega
      - rota atrasou frequente
      - rota atrasou
      - rota atrasou
      - rota atrasou enderecos
      • resumo: Relatos focados em rota atrasou, rota, atrasou. Exemplo representativo: "rota atrasou entrega".
      • genérico/incoerente: False

    - Cluster 78 (n=5)
      • top termos: rota, retrabalho rota, retrabalho, retrabalho manha, mt retrabalho, mt
      • exemplos:
      - retrabalho na rota
      - retrabalho na rota
      - retrabalho na rota
      - retrabalho na rota
      - mt retrabalho pela manha
      • resumo: Relatos focados em rota, retrabalho rota, retrabalho. Exemplo representativo: "retrabalho na rota".
      • genérico/incoerente: False

    - Cluster 79 (n=16)
      • top termos: mal, rota, mal planejada, rota mal, planejada, posto
      • exemplos:
      - posto mal ajustado
      - rota mal planejada
      - rota refeita por erro
      - rota mal planejada
      - posto mal ajustado n le direito
      • resumo: Relatos focados em mal, rota, mal planejada. Exemplo representativo: "posto mal ajustado".
      • genérico/incoerente: False

    - Cluster 80 (n=8)
      • top termos: posto desconfortavel, posto, desconfortavel, demais, puxado demais, puxado
      • exemplos:
      - posto desconfortavel
      - posto desconfortavel desalinhado
      - posto desconfortavel puxado demais
      - posto desconfortavel sobrecarregado
      - posto desconfortavel mas n ajuda
      • resumo: Relatos focados em posto desconfortavel, posto, desconfortavel. Exemplo representativo: "posto desconfortavel".
      • genérico/incoerente: False

    - Cluster 81 (n=11)
      • top termos: separacao atrasada, atrasada, separacao, enderecos, atrasada enderecos, suficiente
      • exemplos:
      - separacao atrasada por estoque
      - separacao atrasada
      - separacao atrasada
      - separacao atrasada
      - separacao atrasada enderecos
      • resumo: Relatos focados em separacao atrasada, atrasada, separacao. Exemplo representativo: "separacao atrasada por estoque".
      • genérico/incoerente: False

    - Cluster 82 (n=6)
      • top termos: separacao refeita, separacao, refeita
      • exemplos:
      - separacao refeita
      - separacao refeita
      - separacao refeita
      - separacao refeita
      - separacao refeita
      • resumo: Relatos focados em separacao refeita, separacao, refeita. Exemplo representativo: "separacao refeita".
      • genérico/incoerente: False

    - Cluster 83 (n=9)
      • top termos: rota refeita, rota, refeita, refeita enderecos, enderecos
      • exemplos:
      - rota refeita
      - rota refeita
      - rota refeita
      - rota refeita
      - rota refeita
      • resumo: Relatos focados em rota refeita, rota, refeita. Exemplo representativo: "rota refeita".
      • genérico/incoerente: False

    - Cluster 84 (n=13)
      • top termos: linha, atrasou, linha atrasou, atrasou linha, turno, atrasou turno
      • exemplos:
      - linha 2 atrasou por manutencao
      - linha atrasou do turno da noite
      - linha atrasou desconfortavel
      - linha atrasou a tarde
      - linha atrasou na area 1
      • resumo: Relatos focados em linha, atrasou, linha atrasou. Exemplo representativo: "linha 2 atrasou por manutencao".
      • genérico/incoerente: False

    - Cluster 85 (n=9)
      • top termos: linha, linha parada, parada, travou, linha travou, travou linha
      • exemplos:
      - linha travou da linha
      - linha travou da linha
      - linha travou hj
      - linha parada da linha
      - linha parada sujo
      • resumo: Relatos focados em linha, linha parada, parada. Exemplo representativo: "linha travou da linha".
      • genérico/incoerente: False

  - notas:
  - Cluster -1 representa ruído/itens não agrupados.
  - Cluster -1 marcado como genérico/incoerente (tamanho pequeno ou termos fracos).
  - HDBSCAN identifica clusters densos e marca itens dispersos como ruído (-1).
  - Estabilidade deve ser avaliada qualitativamente via ruído e coerência.


Comparação e Insights
- KMeans tende a gerar temas consistentes e explicáveis.
- HDBSCAN destaca ruído, útil para ver itens fora do padrão.
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

