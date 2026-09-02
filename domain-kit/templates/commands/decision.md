---
name: domain-decision
description: Registra decisão de produto D-n no registry.
---

## Explain to user

Vou propor uma linha D-n (tema, decisão, evidência) para `03-registry/produto.md`. Confirme o texto antes de gravar.

## User Input

```text
$ARGUMENTS
```

## Steps

1. Alocar próximo ID D-n (ler registry existente).
2. Capturar: capability, tema, status (`proposta`|`aceita`), texto, path evidência.
3. Apresentar preview markdown.
4. Gravar após confirmação.
5. Incrementar `domain-status.json` registry.decisoesProduto.
6. Regenerar dashboard.

Template: `architecture-hub/_conventions/decisao-template.md`
