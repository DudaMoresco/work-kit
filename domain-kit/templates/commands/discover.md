---
name: domain-discover
description: Descoberta DDD — lacunas (0b) + 1 estágio por sessão; Gate G1.
---

## Explain to user

Vou conduzir a **descoberta de domínio** em **sessões curtas** — não tudo numa conversa só.

A **síntese de evidências** já veio do `/domain.init`. Nesta sessão:

1. **Primeiro** fecho **lacunas de negócio** (máx. 3 perguntas por turno, só o que falta na síntese)
2. **Depois** proponho **um estágio DDD** por sessão (rascunho → seu OK → grava)

Se G0 ou síntese ainda não existem, aviso para rodar **`/domain.init`** primeiro (ou `/domain.scan` se fontes mudaram depois).

Contrato: [plan-mode.md](../../references/plan-mode.md) · Estágios: [discovery-workflow.md](../../references/discovery-workflow.md)

## User Input

```text
$ARGUMENTS
```

Flags:

- `--mode full|minimal|as-is-first|incremental`
- `--bc {bc}` (obrigatório em incremental)
- `--stage auto|strategic|stories|event-storming|contexts|full|brief`

**Default:** `--stage auto` — infere o próximo estágio pendente (ver tabela abaixo).

`--stage brief` é **recovery legado** — só síntese, se init antigo não gerou `sintese-evidencias.md`. Caso normal: `/domain.init`.

## Plan mode (obrigatório)

1. Rascunhos em `products/{p}/.draft/` + preview no chat.
2. Registrar em `.draft/manifest.json` cada artefato pendente.
3. **Aguardar** confirmação antes de promote para path canônico.
4. Após OK: copiar draft → target (ou `promote_draft.py`), regenerar dashboard.
5. **Checkpoint de sessão** — ao fechar um `--stage`, informar próximo comando sugerido (`/domain.status` ou discover com próximo stage).

## Pré-condições

### Gate G0

1. Rodar `validate_gate.py --gate G0 --product {p}`.
2. Se **FAIL**: handoff **`/domain.init {p}`** (ou `/domain.scan` se índices existem mas fontes mudaram).
3. Se **PASS**: perguntar *"Fontes mudaram desde o último scan?"* — se sim, sugerir `/domain.scan` antes de continuar.

### Síntese de evidências

1. Verificar `01-product/00-scan/sintese-evidencias.md` promovido.
2. Se **ausente**: handoff **`/domain.init {p}`** (completar Fase 0c) — ou `--stage brief` só em recovery legado.

## Modelo de sessões (regra #1 do discover)

| `--stage` | Entrega da sessão | Artefato(s) |
| --- | --- | --- |
| _(abertura)_ | Lacunas de negócio (0b) | `02-domain/abertos.md` se necessário |
| `strategic` | Estágio 1 | `01-product/01-vision/01-design-estrategico.md` |
| `stories` | Estágio 2 (1+ história por sessão) | `03-discovery/02-domain-storytelling/{NN}-{slug}.md` |
| `event-storming` | Estágio 5 (1 workshop por sessão) | `03-discovery/01-event-storming/` |
| `contexts` | Estágio 3 | `02-domain/desafio-negocio.md`, `linguagem-ubiqua.md`, `bounded-contexts.md` |
| `auto` | 0b (se lacunas) ou próximo DDD pendente | conforme linha |
| `full` | 0b + todos os estágios DDD | **com checkpoint explícito** entre cada estágio |
| `brief` | **Recovery** — só síntese | `sintese-evidencias.md` (preferir `/domain.init`) |

**Não fazer numa sessão só:** lacunas + estratégico + stories + ES + BCs. Modo `full` = mesma sequência, **pausas** entre estágios.

Ordem lógica (`full` / `auto`): **0b lacunas** → `strategic` → `stories` → `event-storming` → `contexts` (stories e ES podem inverter se o domínio pedir; declarar no chat).

## Modos

| Modo | Quando | Comportamento |
| --- | --- | --- |
| `full` (default) | Produto novo | 0b → sequência completa por estágios DDD |
| `minimal` | CRUD simples, 1 BC | 0b → `strategic` → `contexts` (pula stories/ES) |
| `as-is-first` | Legado em produção | 0b → fluxogramas-decisao por BC → `contexts` mínimos |
| `incremental` | Nova capability pós-G2 | 0b (delta) → discovery para `{bc}` apenas |

Declarar modo e `--stage` no início da sessão.

## Steps

### Fase 0b — Lacunas de negócio (abertura obrigatória)

[discover.md](../../templates/clarify/discover.md) — ler lacunas em `sintese-evidencias.md`; máx. 3 perguntas/turno; draft `abertos.md` se necessário.

Se lacunas já fechadas, declarar e seguir para o `--stage` DDD pendente.

### Fase 1–N — DDD (1 estágio por sessão, plan mode)

1. Criar pastas canônicas no promote (mkdir sob demanda).
2. Wrappers read-only; **propor** conteúdo → `.draft/01-product/…`
3. Preview no chat; aguardar OK; promote.
4. **Encerrar sessão** com próximo `--stage` sugerido.

**Sequência por modo** (cada linha DDD = sessão separada, salvo `--stage full` com checkpoints):

- `full`: 0b → estratégico → stories → ES → linguagem + BCs
- `minimal`: 0b → estratégico (resumido) → linguagem + BCs
- `as-is-first`: 0b → fluxogramas-decisao por BC → UL + BCs mínimos
- `incremental`: 0b (delta) → discovery para `{bc}` apenas

5. Gate G1 via `validate_gate.py --gate G1 --product {p}` (só paths promovidos contam) — tipicamente após `--stage contexts`.
6. **Changelog** — após cada promote material ou G1: [changelog.md](../../templates/clarify/changelog.md) → append em `CHANGELOG.md`; exibir no checkpoint de sessão.
7. Handoff H1 → `/domain.model` ou `/domain.flow 01`

**Re-sync de fontes:** `/domain.scan` atualiza `sintese-evidencias.md`; lacunas novas tratadas na próxima sessão discover.
