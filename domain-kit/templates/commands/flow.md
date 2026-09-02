---
name: domain-flow
description: Um fluxo entregável (fluxo-NN) — perguntas inline, plan mode.
---

## Explain to user

Trabalho **um fluxo** por vez: deps, perguntas se faltar contexto, rascunho do MD. **Só gravo no hub após seu OK.**

Contrato: [plan-mode.md](../../references/plan-mode.md)

## User Input

```text
$ARGUMENTS
```

Formato: `{NN}` ou `fluxo-{NN}` + produto opcional.

## Steps

1. Resolver produto e `fluxo-{NN}`.
2. `flow_deps.py` — se FAIL, listar deps e parar.
3. **Perguntas inline** — [flow.md](../../templates/clarify/flow.md) se ambíguo (máx. 3/turno).
4. Wrapper [fluxos-entregaveis.md](../../wrappers/fluxos-entregaveis.md).
5. Propor MD → `.draft/02-capabilities/{bc}/fluxos/{NN}-{slug}.md` + preview chat.
6. Propor updates registry / `fluxos-aplicacao.md` / D-n como drafts.
7. **Aguardar OK** → promote todos; `flows-registry.yml` status `ready`.
8. **Changelog** — [changelog.md](../../templates/clarify/changelog.md) → append em `CHANGELOG.md`; exibir no checkpoint.
9. Regenerar dashboard; sugerir próximo fluxo.
