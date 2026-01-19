# 📁 Experimento 5 — Isolamento Multitenant e RAG Seguro

## E5 — Segurança e isolamento de dados

### Contexto
Com IA generativa e chat, o risco de vazamento entre clientes é crítico.

### Hipótese (E5)
É possível usar RAG e IA generativa garantindo isolamento total entre empresas via arquitetura multi-tenant com RLS.

### O que testar
- Embeddings sempre associados a tenant_id.
- Queries filtradas por tenant.
- IA responde apenas com dados do tenant correto.

### Critério de decisão
- **Validada:** nenhuma contaminação entre tenants.
- **Rejeitada:** qualquer vazamento → produto inviável.
