# 📁 Experimento 2 — Interpretação com IA Generativa (Clusters → Significado)

## E2 — Interpretação dos clusters com IA generativa

### Contexto
No Experimento 1 validamos que a clusterização (KMeans) consegue organizar relatos operacionais sujos em grupos coerentes do ponto de vista humano.

Neste experimento, não alteramos a clusterização.
O foco passa a ser extrair valor dos clusters usando IA generativa.

### Hipótese (E2)
É possível usar IA generativa em cima de clusters já formados para produzir interpretações claras, confiáveis e acionáveis para gestores, sem virar consultoria.

### O que testar
Para cada cluster gerado no E1, a IA generativa deve conseguir:

- Gerar um label curto e específico.
- Produzir um resumo acionável (orientado a decisão).
- Citar evidências reais (frases do próprio cluster).
- Sugerir ações iniciais (rascunho editável).

### Entrada da IA (input obrigatório)
A IA não recebe relatos soltos.
Ela recebe um pacote estruturado por cluster:

- Top termos do cluster.
- 8–10 exemplos representativos de relatos.
- Estatísticas simples:
  - número de relatos.
  - setor (indústria / CD).
  - tendência (se disponível).
  - área/origem (se disponível).

⚠️ A IA não pode “inventar” contexto fora disso.

### Saída esperada da IA (output)
Para cada cluster:

- Label curto.

  Ex.: “Paradas por falha de sensor”.
- Resumo acionável.

  Ex.: “Paradas recorrentes na Linha 3 associadas a falhas no sensor térmico e setup inadequado na troca de turno.”
- Evidências.

  2–4 frases reais retiradas do cluster.
- Ações sugeridas (rascunho).

  Ex.: revisar checklist de setup; validar calibração do sensor; alinhar troca de turno.

### Regras importantes
- A IA não diagnostica causa raiz definitiva.
- A IA não prescreve soluções específicas.
- Tudo deve ser editável pelo gestor.
- Sempre citar evidências (grounding).

### Como decidir
- **Validada:** gestores entendem rapidamente o problema e criam ações.
- **Parcialmente validada:** resumo bom, ações genéricas demais.
- **Rejeitada:** textos vagos, genéricos ou sem confiança.

### Por que esse experimento é crítico
Aqui se valida:

- o valor real do produto.
- a entrada correta da IA generativa.
- o risco de virar consultoria (que deve ser evitado).
