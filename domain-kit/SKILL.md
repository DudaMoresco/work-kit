---
name: domain-kit
description: >-
  Modelagem de problema e domínio no hub: Evidências → Estratégico → Descoberta → Operacional.
  Design tático no arch-kit.
disable-model-invocation: true
---

# Domain-Kit

- [COMMAND-GUIDE.md](COMMAND-GUIDE.md) · [GUIDE.md](GUIDE.md) · [references/plan-mode.md](references/plan-mode.md)

## Pipeline

```text
domain.install → domain.init (evidências) → domain.discover (estratégico + descoberta)
  → domain.flow (operacional) → domain.model --finalize (operacional) → arch.route
```

## Fases (substituem gates G0–G2)

| Fase | Pergunta | Artefatos principais |
| --- | --- | --- |
| **Evidências** | O que sabemos, com fonte? | sources.yml, scan, síntese |
| **Estratégico** | Por quê? Onde? Como falamos? | design estratégico, desafio, BCs, UL |
| **Descoberta** | Como se comporta no tempo? | stories, event storming |
| **Operacional** | Quais cenários garantir? | fluxos negócio, NFRs produto, D-n |
| **Arch-kit** | Como implementar? | design tático, integração técnica |

Aliases legados: G0=Evidências, G1=Estratégico+Descoberta, G2=Operacional.

## Cartão central do produto

`products/{p}/product-README.md` — visão PM (2–3 linhas), benefícios, status por fase, índice de artefatos.

Atualizar após promote material em discover (contexts), model (--finalize) e `/domain.change`.

## Evoluções e problemas

| Mecanismo | ID | Arquivo |
| --- | --- | --- |
| Entrada de sessão | — | `domain-status.json` → `activeChange` |
| Problemas / lacunas | P-n | `01-product/02-domain/abertos.md` |
| Evoluções intencionais | E-n | `01-product/02-domain/evolucoes.md` |
| Decisões | D-n | `03-registry/produto.md` |

Ritual: `/domain.change` → handoff discover/flow/model/scan/decision. Ver `.domain/clarify/evolucao.md`.

## Plan mode (regra #1)

```text
Propor → .draft/ + chat → OK do usuário → path canônico
```

## Comandos

| Comando | Fase / papel |
| --- | --- |
| `domain.init` | Evidências |
| `domain.discover` | Estratégico + Descoberta |
| `domain.flow` | Operacional (fluxo negócio) |
| `domain.model` | Operacional (NFRs, finalize) |
| `domain.decision` | Operacional (registry D-n) |
| `domain.change` | Sessão evolutiva (P-n / E-n) |
| `domain.status` | Leitura de progresso |
| `domain.scan` | Re-sync evidências |
| `domain.capability` | **DEPRECATED** → arch-kit |

Helper: `.domain/scripts/promote_draft.py`, `adopt_product.py`, `validate_gate.py`

Know-how: `.domain/skills/` (bundled) · contratos: `.domain/wrappers/`
