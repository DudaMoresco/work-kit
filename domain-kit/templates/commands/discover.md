---
name: domain-discover
description: Orquestra descoberta de domínio batch — estratégico, ES, BCs.
---

## Explain to user

Vou conduzir a **descoberta** em etapas (estratégico, histórias, event storming, BCs), pausando para confirmar a cada artefato importante.

## Pre-hook

Executar `/domain.clarify discover` se G0 scan pendente revisão ou fatos faltando.

## Steps

1. Ler `00-scan/README.md` se existir.
2. Sequência com wrappers (read-only skills):
   - ddd-design-estrategico
   - domain-storytelling (1+ histórias por sessão)
   - event-storming (1 workshop por sessão)
   - ddd-linguagem-e-contextos
3. Validar Gate G1 via `validate_gate.py --gate G1`.
4. Emitir Handoff H1 → `/domain.model` ou `/domain.flow 01`.
