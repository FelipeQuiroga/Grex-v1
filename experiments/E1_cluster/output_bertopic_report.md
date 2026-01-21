Pipeline: Pipeline BERTopic — Exploração rápida de tópicos
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

