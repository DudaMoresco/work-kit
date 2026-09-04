---
name: domain-status
description: Progresso domain-kit — fases, fluxos, gaps e próximo comando sugerido.
---

## Explain to user

Vou resumir onde o produto está: fases **Evidências → Estratégico → Descoberta → Operacional**, fluxos prontos vs bloqueados, gaps e **próximo comando sugerido**.

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
   - Tabela fases (PASS/FAIL + issues)
   - **Sessão ativa** (`activeChange`) se preenchido — P-n/E-n em andamento
   - Gaps por artefato (estratégico, descoberta, operacional)
   - Artefatos arch-kit adotados (`arch.capabilitiesAdopted`, `integrationAdopted`)
   - Link para [`product-README.md`](products/{p}/product-README.md) e `dashboard.html`
   - **Próximo comando sugerido**

## Interpretação rápida

| Fase | Significa | Se FAIL |
| --- | --- | --- |
| Evidências | Scan e fontes indexadas | `/domain.init` ou `/domain.scan` |
| Estratégico | Problema, visão, BCs, UL | `/domain.discover --stage strategic\|contexts` |
| Descoberta | Stories e/ou event storming | `/domain.discover --stage stories\|event-storming` |
| Operacional | Fluxos de negócio + NFRs + D-n | `/domain.flow`, `/domain.model --finalize` |
| Mudança / problema / evolução | Sessão evolutiva | `/domain.change` |
| Todas PASS | Handoff arch-kit | `/arch.route` |

## Aliases legados (gates)

| Gate | Equivale a |
| --- | --- |
| G0 | Evidências |
| G1 | Estratégico + Descoberta |
| G2 | Operacional |
