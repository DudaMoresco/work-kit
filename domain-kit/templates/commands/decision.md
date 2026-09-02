---
name: domain-decision
description: Registra D-n — preview obrigatório, promote após OK.
---

## Explain to user

Proponho linha D-n para o registry. Preview no chat e em `.draft/` — gravo em `produto.md` só após OK.

Contrato: [plan-mode.md](../../references/plan-mode.md)

## User Input

```text
$ARGUMENTS
```

## Steps

1. Alocar próximo D-n.
2. Capturar: capability, tema, status, texto, evidência.
3. Draft append em `.draft/03-registry/produto.md` (ou patch preview).
4. Preview markdown no chat.
5. **Aguardar OK** → promote / merge em registry canônico.
6. **Changelog** — [changelog.md](../../templates/clarify/changelog.md) → append em `CHANGELOG.md`; exibir no checkpoint.
7. Atualizar `domain-status.json`; regenerar dashboard.
