# Experimento 2 — Interpretação com IA Generativa (Clusters → Significado)

## E2 — Interpretação dos clusters com IA generativa

### Contexto
No Experimento 1 validamos que a clusterização (Bertopic) consegue organizar relatos operacionais sujos em grupos coerentes do ponto de vista humano.

Neste experimento, não alteramos a clusterização. O foco passa a ser extrair valor dos clusters usando IA generativa.

### Hipótese (E2)
É possível usar IA generativa em cima de clusters já formados para produzir interpretações claras, confiáveis e acionáveis para gestores, sem virar consultoria.

### O que testar
Para cada cluster gerado no E1, a IA generativa deve conseguir:

- Gerar um label curto e específico.
- Produzir um resumo acionável (orientado a decisão).
- Citar evidências reais (frases do próprio cluster).
- Sugerir ações iniciais (rascunho editável).

### Entrada da IA (input obrigatório)
A IA não recebe relatos soltos. Ela recebe um pacote estruturado por cluster:

- Top termos do cluster.
- 8–10 exemplos representativos de relatos.
- Estatísticas simples:
- número de relatos.
- setor (indústria / CD).

Regra: a IA não pode “inventar” contexto fora disso.

### Saída esperada da IA (output)
Para cada cluster:

- Label curto (ex.: “Paradas por falha de sensor”).
- Resumo acionável (ex.: “Paradas recorrentes na Linha 3 associadas a falhas no sensor térmico e setup inadequado na troca de turno.”).
- Evidências (2–4 frases reais retiradas do cluster).
- Ações sugeridas (rascunho editável).

### Regras importantes
- A IA não diagnostica causa raiz definitiva.
- A IA não prescreve soluções específicas.
- Tudo deve ser editável pelo gestor.
- Sempre citar evidências (grounding).

### Como decidir
- Validada: gestores entendem rapidamente o problema e criam ações.
- Parcialmente validada: resumo bom, ações genéricas demais.
- Rejeitada: textos vagos, genéricos ou sem confiança.

### Por que esse experimento é crítico
Aqui se valida:

- o valor real do produto.
- a entrada correta da IA generativa.
- o risco de virar consultoria (que deve ser evitado).

---

## Nova estrutura (pipeline)
O E2 agora roda via `run_e2.py` e usa a pasta `e2/` como módulo interno. A execução é totalmente configurável via `config.yaml`.

### Estrutura principal
- `run_e2.py`: orquestra o pipeline completo.
- `config.yaml`: parâmetros de entrada, LLM e regras.
- `e2/`: módulos do pipeline (IO, agregação, prompt, validação, métricas, versionamento).
- `outputs/runs/`: saídas por execução (geradas automaticamente).

### Execução
No diretório `Grex-v1/experiments/E2_genAI`:

```powershell
python .\run_e2.py
```

### Principais etapas do pipeline
1. Carrega o CSV do E1.
1. Normaliza e filtra relatos.
1. Agrega tópicos (top termos + exemplos).
1. Monta prompt com regras.
1. Chama o LLM (com retry e repair prompt se necessário).
1. Valida o JSON de resposta.
1. Calcula métricas.
1. Escreve manifest e artefatos de execução.

### Configuração (config.yaml)
Campos relevantes:
- `source.e1_csv_path`: caminho do CSV do E1.
- `aggregation.*`: filtros, amostragem e termos por tópico.
- `llm.*`: provider, modelo, timeout e retries.
- `rules.*`: limites de temas e critérios de emergência.
- `run.outputs_base_dir`: pasta base das execuções.
- `run.prompt_version`: versão do prompt.

### Saídas geradas por execução
Em `outputs/runs/<run_id>/`:
- `input_topics.json`: pacote de tópicos entregue ao LLM.
- `prompt.txt`: prompt principal.
- `llm_raw.txt`: resposta bruta.
- `result.json`: resposta validada (quando válida).
- `metrics.json`: métricas de qualidade.
- `validation_errors.txt`: erros de validação (se houver).
- `prompt_repair.txt` e `llm_raw_retry.txt`: apenas se houve repair.
- `manifest.json`: metadados da execução.

### Observações
- Se houver erro de validação, o pipeline tenta um repair automático.
- O status final fica registrado no `manifest.json`.
