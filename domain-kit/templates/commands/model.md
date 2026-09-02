---
name: domain-model
description: Modelagem batch — integração, requisitos, finalize com gate G2.
---

## Explain to user

Vou fechar integração entre BCs, requisitos e (com `--finalize`) validar se o pacote está pronto para arch-kit.

## User Input

`--finalize` opcional.

## Steps

Sem `--finalize`:
- ddd-integracao-contextos
- Sugerir `/domain.capability` e `/domain.flow` por item pendente no registry

Com `--finalize`:
1. levantamento-requisitos se RF ausente
2. Sweep registry D-n
3. `validate_gate.py --gate G2`
4. Handoff H2 → `/arch.route`
5. Regenerar dashboard
