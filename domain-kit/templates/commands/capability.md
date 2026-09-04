---
name: domain-capability
description: "[DEPRECATED → arch-kit] Design tático de um BC — use /arch.capability quando disponível."
---

## Explain to user

**Este comando foi movido para o arch-kit.** O domain-kit foca em modelagem de **problema/negócio** (fases Estratégico, Descoberta, Operacional).

Design tático (agregados, camadas, ports/adapters) é decisão de **arquitetura** — use `/arch.capability {bc}` quando o arch-kit estiver instalado, ou grave manualmente em `products/{p}/arch/{bc}/design-tatico.md`.

Artefatos legados em `02-capabilities/{bc}/design-tatico.md` são marcados como `arch.capabilitiesAdopted` via `adopt_product.py` e **não bloqueiam** o fechamento da fase Operacional.

## User Input

```text
$ARGUMENTS
```

## Steps

1. Informar deprecação e handoff para arch-kit.
2. Se o usuário insistir: propor conteúdo em `.draft/arch/{bc}/design-tatico.md` (não em `02-capabilities/`).
3. Atualizar `domain-status.json` → `arch.capabilitiesAdopted` após promote.
4. **Não** validar G2/operacional com design-tatico.
