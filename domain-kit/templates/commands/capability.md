---
name: domain-capability
description: Design tático DDD de um bounded context.
---

## Explain to user

Vou modelar **um BC**: camadas, agregados e README da capability. Uma sessão, com confirmação antes de gravar.

## User Input

```text
$ARGUMENTS
```

`{bc}` slug — ex.: `ordem-de-servico`

## Steps

1. Validar BC em `bounded-contexts.md`.
2. clarify bc {bc} se termos/fronteiras ambíguos.
3. Seguir [ddd-design-tatico.md](../../wrappers/ddd-design-tatico.md).
4. Gravar após confirmação.
5. Atualizar `domain-status.json` model.capabilities[{bc}].
6. Regenerar dashboard.
