---
name: domain-status
description: Progresso domain-kit — gates, fluxos, gaps e próximo comando sugerido.
---

## Explain to user

Vou resumir onde o produto está: gates G0–G2, fluxos prontos vs bloqueados, gaps e **próximo comando sugerido**.

## User Input

```text
$ARGUMENTS
```

## Steps

1. Resolver `{produto}` (argumento ou produto ativo no hub).
2. Ler `products/{produto}/domain-status.json` e `flows-registry.yml`.
3. Rodar `validate_gate.py --hub {hub} --product {p} --json --suggest`.
4. Se produto tem artefatos mas índices incompletos, sugerir `/domain.init {p} --adopt`.
5. Listar fluxos bloqueados por deps (`flow_deps.py` se disponível).
6. Emitir markdown com:
   - Tabela gates G0–G2 (PASS/FAIL + issues)
   - Gaps por fase (scan, discover, model)
   - **Próximo comando sugerido** (de `validate_gate.py --suggest`)
   - Link para `dashboard.html`

## Interpretação rápida

| Gate | Significa | Se FAIL |
| --- | --- | --- |
| G0 | Primeiro scan ok | `/domain.init` ou `/domain.scan` |
| G1 | Discover ok (BCs, ES/stories) | `/domain.discover` (+ modo adequado) |
| G2 | Model ok (tático, fluxos, D-n) | `/domain.flow`, `/domain.capability`, `/domain.model --finalize` |
| Todos PASS | Pronto para arch-kit | `/arch.route` |
