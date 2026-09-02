---
name: domain-flow
description: Modela um fluxo entregável (fluxo-NN) por sessão conversacional.
---

## Explain to user

Vou trabalhar **um fluxo** por vez: validar dependências, perguntar o que falta, propor o MD do fluxo e atualizar o registry. Confirme antes de gravar.

## User Input

```text
$ARGUMENTS
```

Formato: `{NN}` ou `fluxo-{NN}` + produto opcional.

## Steps

1. Resolver produto e `fluxo-{NN}`.
2. Rodar `.domain/scripts/flow_deps.py products/{p} {NN}` — se FAIL, listar deps e parar.
3. `/domain.clarify flow {NN}` (ou incorporar se já clarificado nesta sessão).
4. Seguir [fluxos-entregaveis.md](../../wrappers/fluxos-entregaveis.md).
5. Propor MD em `02-capabilities/{bc}/fluxos/{NN}-{slug}.md`.
6. Atualizar `fluxos-aplicacao.md` se cross-BC.
7. Propor D-n → `/domain.decision` ou confirmar existentes.
8. Atualizar `flows-registry.yml` status `ready`.
9. Regenerar dashboard; sugerir próximo fluxo desbloqueado.

**Aguardar** "pode gravar" antes de write.
