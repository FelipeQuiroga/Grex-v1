# 📁 Experimento 3 — Qualidade dos Resumos e Confiança do Gestor

## E3 — Resumos acionáveis e confiança

### Contexto
No E2 validamos que a IA consegue interpretar clusters.
Agora validamos se essa interpretação é boa o suficiente para gerar confiança.

### Hipótese (E3)
Os resumos gerados pela IA são claros, específicos e confiáveis o suficiente para que gestores tomem decisões sem desconfiar da ferramenta.

### O que testar
Comparar dois cenários:

- Clusters sem interpretação (apenas dados brutos).
- Clusters com label + resumo + evidências.

Avaliar:

- clareza.
- especificidade.
- confiança percebida.

### Métricas
- Gestor entende o problema em < 2 minutos.
- Gestor consegue explicar o cluster com suas próprias palavras.
- Gestor cria ao menos 1 plano de ação.

### Como decidir
- **Validada:** resumos reduzem tempo de entendimento e aumentam ação.
- **Rejeitada:** gestores preferem olhar só os relatos.
