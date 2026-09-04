---
name: domain-model
description: Fase Operacional — requisitos NFR de produto e finalize; sem design tático.
---

## Explain to user

Fecho artefatos da **fase Operacional**: requisitos não-funcionais de **produto** (SLA percebido, volume de negócio, compliance) e validação da fase.

**Não entrega:** design tático, integração técnica, C4, ADR — isso é **arch-kit** após Operacional PASS.

Cada artefato: **rascunho → preview → OK → hub**.

Contrato: [plan-mode.md](../../references/plan-mode.md)

## User Input

```text
$ARGUMENTS
```

Flags: `--finalize`, `--mode full|incremental`

## Steps

0. Se `activeChange` em `domain-status.json`, citar P-n/E-n no chat e changelog.

### Sem `--finalize`

- Sugerir `/domain.flow` pendente conforme gaps da fase Operacional
- Draft requisitos NFR se ausente → OK → promote em `04-platform/01-non-functional/01-requisitos.md`

### Com `--finalize`

1. Draft requisitos se ausente → OK → promote
2. Sweep registry D-n (decisions via plan mode)
3. Validar fase Operacional: `validate_gate.py --phase operacional --product {p}`
4. **Changelog** após cada promote material
5. Refresh `product-README.md` (status por fase, benefícios se NFRs mudaram)
6. Handoff → `/arch.route` quando Operacional PASS
7. Regenerar dashboard

**Aguardar OK** para cada artefato antes de promote.

**Integração técnica:** se necessário, propor em `.draft/arch/01-integration/` — não em `01-product/04-integration/` (stub apenas).
