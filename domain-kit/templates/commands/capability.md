---
name: domain-capability
description: Design tático de um BC — perguntas inline, plan mode.
---

## Explain to user

Modelo **um BC**: agregados, camadas, README. Rascunho primeiro; hub só após OK.

Contrato: [plan-mode.md](../../references/plan-mode.md)

## User Input

```text
$ARGUMENTS
```

`{bc}` slug — ex.: `ordem-de-servico`

## Steps

1. Validar BC em `bounded-contexts.md` (promovido).
2. **Perguntas inline** se termos/fronteiras ambíguos (máx. 3/turno).
3. Wrapper [ddd-design-tatico.md](../../wrappers/ddd-design-tatico.md).
4. Draft `design-tatico.md` + `README.md` em `.draft/02-capabilities/{bc}/`.
5. Preview chat → **aguardar OK** → promote.
6. **Changelog** — [changelog.md](../../templates/clarify/changelog.md) → append em `CHANGELOG.md`; exibir no checkpoint.
7. Atualizar `domain-status.json` após promote.
8. Regenerar dashboard.
