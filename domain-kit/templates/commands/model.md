---
name: domain-model
description: Fase Operacional — requisitos NFR de produto e finalize; sem design tático.
---

## Explain to user

Fecho artefatos da **fase Operacional**: requisitos não-funcionais de **produto** (SLA percebido, volume de negócio, compliance) e validação da fase.

**Não entrega:** design tático, integração técnica, C4, ADR — isso fica **fora do escopo do domain-kit** (próxima etapa técnica após Operacional PASS).

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
- Draft requisitos NFR se ausente → OK → promote em `01-product/04-operacional/requisitos.md`

### Com `--finalize`

1. Draft requisitos se ausente → OK → promote
2. Sweep registry D-n (decisions via plan mode)
3. Validar fase Operacional: `validate_gate.py --phase operacional --product {p}`
4. **Changelog** após cada promote material
5. Refresh `product-README.md` (status por fase, benefícios se NFRs mudaram)
6. Se Operacional PASS: informar fim do pipeline domain-kit — próxima etapa técnica (fora deste kit)
7. Regenerar dashboard

**Aguardar OK** para cada artefato antes de promote.

**Integração técnica:** se necessário, propor em `.draft/` sob path técnico — não em `01-product/04-integration/` (stub apenas). Detalhe técnico fica fora do escopo do domain-kit.
