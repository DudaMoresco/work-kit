---
name: domain-model
description: Modelagem — integração, requisitos, finalize G2; modos full/incremental.
---

## Explain to user

Fecho integração, requisitos e (com `--finalize`) valido G2. Cada artefato: **rascunho → preview → OK → hub**.

Com `--mode incremental`: valido G2 só para `{bc}` novo (tático + fluxos + D-n delta).

Contrato: [plan-mode.md](../../references/plan-mode.md)

## User Input

```text
$ARGUMENTS
```

Flags: `--finalize`, `--mode full|incremental`, `--bc {bc}` (obrigatório em incremental)

## Steps

### Sem `--finalize`

- Draft integração ([ddd-integracao-contextos.md](../../wrappers/ddd-integracao-contextos.md)) → OK → promote
- **Changelog** — após promote: [changelog.md](../../templates/clarify/changelog.md)
- Sugerir `/domain.capability` e `/domain.flow` pendentes conforme gaps

### Com `--finalize`

1. Draft requisitos se ausente → OK → promote
2. Sweep registry D-n (decisions via plan mode)
3. Validar G2:
   - `--mode full` (default): `validate_gate.py --gate G2 --product {p}`
   - `--mode incremental`: `validate_gate.py --gate G2 --product {p} --mode incremental --bc {bc}`
4. **Changelog** — após cada promote material ou G2: [changelog.md](../../templates/clarify/changelog.md) → append em `CHANGELOG.md`; exibir no checkpoint.
5. Handoff H2 → `/arch.route`
6. Regenerar dashboard

**Aguardar OK** para cada artefato antes de promote.

**Não entrega:** arquitetura técnica, C4, ADR, database-model — isso é arch-kit após H2.
