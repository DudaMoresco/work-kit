# Wrapper: fluxos entregáveis

**Skill original:** skills `fluxos-entregaveis` / `fluxogramas-decisao` — NÃO editar originais.

**Invocada por:** `/domain.flow {NN}`, `/domain.model`

**Pré-condições:** deps de fluxo satisfeitas (`flows-registry.yml`); clarify flow ok

**Outputs no hub:**
- `products/{produto}/02-capabilities/{bc}/fluxos/{NN}-{slug}.md`
- Atualizar seção em `fluxos-aplicacao.md` quando orquestração cross-BC
- Entrada em `flows-registry.yml` status → `ready`

**Pós-execução:** regenerate dashboard; sugerir próximo fluxo desbloqueado
