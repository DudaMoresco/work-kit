---
name: domain-flow
description: Um fluxo operacional de negócio (fluxo-NN) — plan mode; detalhe técnico no arch-kit.
---

## Explain to user

Trabalho **um fluxo operacional** por vez na **camada negócio**: cenário ponta a ponta em linguagem de produto. **Só gravo no hub após seu OK.**

Detalhe técnico (serviços, filas, contratos) é opcional e fica no **arch-kit** (`arch/fluxos/`).

Contrato: [plan-mode.md](../../references/plan-mode.md)

## User Input

```text
$ARGUMENTS
```

Formato: `{NN}` ou `fluxo-{NN}` + produto opcional.

## Pré-condições

- Fases **Estratégico** e **Descoberta** PASS (`validate_gate.py --json`)
- BC e vocabulário em `bounded-contexts.md` + `linguagem-ubiqua.md`

## Steps

0. Se `activeChange` preenchido, citar no chat e changelog.

1. Resolver produto e `fluxo-{NN}`.
2. `flow_deps.py` — se FAIL, listar deps e parar.
3. **Perguntas inline** — [flow.md](../../templates/clarify/flow.md) se ambíguo (máx. 3/turno).
4. Wrapper [fluxos-entregaveis.md](../../wrappers/fluxos-entregaveis.md).
5. Propor MD → `.draft/01-product/03-operacional/fluxos/{NN}-{slug}.md` + preview chat.
6. Propor updates `flows-registry.yml` / D-n como drafts.
7. **Aguardar OK** → promote; `flows-registry.yml` status `ready`.
8. **Changelog** — [changelog.md](../../templates/clarify/changelog.md).
9. Regenerar dashboard; sugerir próximo fluxo ou `/domain.model --finalize`.

**Legado:** fluxos em `02-capabilities/{bc}/fluxos/` contam para adopt, mas novos fluxos usam `03-operacional/fluxos/`.
