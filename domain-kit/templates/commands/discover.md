---
name: domain-discover
description: Descoberta DDD — lacunas (0b) + estágios Estratégico/Descoberta; 1 sessão por estágio.
---

## Explain to user

Vou conduzir a **descoberta de domínio** em **sessões curtas** — foco em **modelagem de problema**, legível por produto e engenharia.

A **síntese de evidências** já veio do `/domain.init`. Nesta sessão:

1. **Primeiro** fecho **lacunas de negócio** (máx. 3 perguntas por turno)
2. **Depois** proponho **um estágio** por sessão (rascunho → seu OK → grava)

Se Evidências ou síntese ainda não existem, aviso para rodar **`/domain.init`** primeiro.

Contrato: [plan-mode.md](../../references/plan-mode.md)

## User Input

```text
$ARGUMENTS
```

Flags:

- `--mode full|minimal|as-is-first|incremental`
- `--bc {bc}` (obrigatório em incremental)
- `--stage auto|strategic|stories|event-storming|contexts|full|brief`

**Default:** `--stage auto` — infere o próximo estágio pendente.

## Fases do domain-kit

| Fase | Estágios deste comando |
| --- | --- |
| **Estratégico** | `strategic`, `contexts` (desafio, UL, BCs) |
| **Descoberta** | `stories`, `event-storming` |

Design tático e integração técnica → **arch-kit** (não neste comando).

## Plan mode (obrigatório)

1. Rascunhos em `products/{p}/.draft/` + preview no chat.
2. Registrar em `.draft/manifest.json` cada artefato pendente.
3. **Aguardar** confirmação antes de promote.
4. Checkpoint com próximo `--stage` sugerido.

## Pré-condições

### Fase Evidências

1. `validate_gate.py --phase evidencias --product {p}` deve PASS.
2. Se FAIL: handoff **`/domain.init {p}`**.

### Síntese

1. Verificar `01-product/00-scan/sintese-evidencias.md` promovido.
2. Se ausente: completar via `/domain.init` (Fase 0c).

## Modelo de sessões

| `--stage` | Fase | Artefato(s) |
| --- | --- | --- |
| _(abertura)_ | — | `02-domain/abertos.md` se necessário |
| `strategic` | Estratégico | `01-product/01-vision/01-design-estrategico.md` |
| `contexts` | Estratégico | `desafio-negocio.md`, `linguagem-ubiqua.md`, `bounded-contexts.md` |
| `stories` | Descoberta | `03-discovery/02-domain-storytelling/{NN}-{slug}.md` |
| `event-storming` | Descoberta | `03-discovery/01-event-storming/` |
| `auto` | — | próximo pendente em Estratégico → Descoberta |

Ordem sugerida (`full`): 0b → estratégico → contexts → stories → event-storming.

Modo `as-is-first`: stories/fluxogramas podem preceder contexts — declarar no chat.

## Steps

0. Se `domain-status.json` → `activeChange` preenchido, citar no chat: *"Sessão vinculada a {id}"*.

### Fase 0b — Lacunas

[discover.md](../../templates/clarify/discover.md) — máx. 3 perguntas/turno.

### Estágios (plan mode)

1. Propor → `.draft/01-product/…`
2. Preview; aguardar OK; promote.
3. Validar fase após contexts (Estratégico) ou após stories/ES (Descoberta):
   - `validate_gate.py --phase estrategico --product {p}`
   - `validate_gate.py --phase descoberta --product {p}`
4. **Changelog** após promote material.
5. Após `--stage contexts` promovido: refresh `product-README.md` (visão, benefícios, índice, problemas abertos).
6. Handoff: Estratégico+Descoberta ok → `/domain.flow` ou `/domain.model` (Operacional).

**bounded-contexts.md:** mapa em linguagem de negócio apenas — sem ACL/filas (detalhe em `arch/01-integration/`).
