---
name: domain-change
description: Abre sessão evolutiva — problema novo, problema existente (P-n) ou evolução intencional (E-n); roteia para comando de fase.
---

## Explain to user

Vou **abrir uma sessão evolutiva**: classificar se é problema novo, retomada de P-n ou evolução intencional (E-n), registrar no hub e sugerir o próximo comando de fase.

**Não entrega** artefatos DDD diretamente — isso fica em discover/flow/model após o handoff.

Contrato: [plan-mode.md](../../references/plan-mode.md) · Roteiros: [change.md](../../.domain/clarify/change.md), [evolucao.md](../../.domain/clarify/evolucao.md)

## User Input

```text
$ARGUMENTS
```

Flags:

- `--kind problem-new|problem|evolution` (obrigatório se não inferível)
- `--id P04` ou `--id E02` (obrigatório para `problem`/`evolution` retomada)
- `--title "…"` (obrigatório para `problem-new` e `evolution` nova)
- `--owner Time/Platform`
- `--phases estrategico,operacional` (opcional — agente infere se omitido)
- `--handoff discover|flow|model|scan|decision` (opcional)
- `--close` — encerrar `activeChange` (pausar ou concluir sessão)

## Os três modos

| `--kind` | Registro | Arquivo |
| --- | --- | --- |
| `problem-new` | Novo P-n | `01-product/02-domain/abertos.md` |
| `problem` | Retoma P-n | `abertos.md` |
| `evolution` | Novo ou retoma E-n | `01-product/02-domain/evolucoes.md` |

## Steps

1. Resolver `{produto}` e validar que Evidências PASS (produto indexado).
2. **Perguntas inline** — `.domain/clarify/change.md` se kind/título ambíguos (máx. 3/turno).
3. Alocar próximo P-n ou E-n (scan tabelas existentes).
4. Draft registro + `activeChange` em `.draft/` → preview chat.
5. **Aguardar OK** → promote `abertos.md` ou `evolucoes.md` + atualizar `domain-status.json`.
6. Declarar fases impactadas e **handoff** (um comando sugerido).
7. **Changelog** — [changelog.md](../../templates/clarify/changelog.md), citando P-n/E-n.
8. Refresh `product-README.md` se visão/benefícios ou lista de abertos mudou materialmente.
9. Regenerar dashboard.

### `--close`

1. Atualizar status P-n/E-n (fechada, concluída ou pausada).
2. `activeChange` → `null` ou `status: paused`.
3. Changelog + dashboard.

## Handoff típico

| Cenário | Próximo comando |
| --- | --- |
| Fonte externa mudou | `/domain.scan` |
| Meta/escopo | `/domain.discover --stage contexts` |
| Comportamento de domínio | `/domain.discover --stage stories` |
| Cenário ponta a ponta | `/domain.flow {NN}` |
| NFR | `/domain.model` |
| Decisão formal | `/domain.decision` |

Ver matriz completa: `.domain/clarify/evolucao.md`.
