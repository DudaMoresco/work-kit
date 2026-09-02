---
name: domain-status
description: Mostra progresso domain-kit — gates, fluxos, artefatos.
---

## Explain to user

Vou resumir onde o produto está: gates G0–G2, fluxos prontos vs bloqueados, e próximo comando sugerido.

## Steps

1. Ler `products/{produto}/domain-status.json` e `flows-registry.yml`.
2. Rodar `validate_gate.py --product {p}` para G0, G1, G2.
3. Listar fluxos bloqueados por deps.
4. Emitir markdown com links para `dashboard.html`.
