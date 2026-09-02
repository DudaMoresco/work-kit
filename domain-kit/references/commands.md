# Comandos do domain-kit

Spec completa. Overlays: [`../templates/commands/`](../templates/commands/).

**Guia prático:** [`../COMMAND-GUIDE.md`](../COMMAND-GUIDE.md)

**Regras globais:**

1. **[Plan mode](../references/plan-mode.md)** — conteúdo em `.draft/` + preview; promote só após OK.
2. Ler **wrapper**; skill DDD read-only; **sem `/domain.clarify`** separado.

---

## Meta — hub e produto

### `/domain.install`

Instala framework no hub (1x). Script: `install-domain-kit.sh`. Ver [ONBOARDING.md](../ONBOARDING.md).

**Entrega:** skills, scripts, MCP checklist. **Não entrega:** artefatos de produto.

### `/workkit.init` — deprecado

Alias de `/domain.install`. Redirecionar com aviso.

### `/domain.init {produto} [--initiative {i}] [--adopt]`

Bootstrap do produto: índices + **primeiro scan** (fase 0) → Gate G0.

Com `--adopt`: produto já no hub — gera índices faltantes, inventário, gaps via `adopt_product.py`.

**Entrega:** `sources.yml`, `scan-manifest.json`, índices. **Não entrega:** BCs, fluxos, tático.

**Handoff:** `/domain.discover`

### `/domain.scan [--plan]`

Re-sync de fontes quando repos/docs mudaram **sem** refazer discover.

**Saídas:** `01-product/00-scan/scan-manifest.json`, `README.md`

### `/domain.status`

Lê gates via `validate_gate.py --suggest`; lista fluxos bloqueados; próximo comando sugerido.

### `/domain.clarify` — deprecado

Redirecionar para comando principal.

---

## Macro — descoberta e modelagem

### `/domain.discover [--mode full|minimal|as-is-first|incremental] [--bc {bc}]`

Descoberta DDD → Gate G1. **Pré-condição:** G0 (scan via init). Pula fase 0 se G0 ok.

Roteiros: [`discover.md`](../templates/clarify/discover.md)

Modos: ver [COMMAND-GUIDE.md](../COMMAND-GUIDE.md)

### `/domain.model [--finalize] [--mode full|incremental] [--bc {bc}]`

Integração, requisitos, sweep. Com `--finalize`: G2 → handoff H2 arch-kit.

Micro-comandos `flow`/`capability` rodam **antes** do finalize.

---

## Micro

### `/domain.flow {NN}`

1. Validar deps (`flow_deps.py`)
2. Perguntas inline
3. Wrapper fluxos-entregaveis
4. Atualizar `flows-registry.yml` → `ready`
5. Regenerar dashboard

### `/domain.capability {bc}`

Wrapper ddd-design-tatico + README capability.

### `/domain.decision`

Propor D-n → confirmar → `03-registry/produto.md`.

---

## Handoffs

| ID | De → Para |
| --- | --- |
| H0 | init (scan G0) → discover |
| H1 | discover → model |
| H2 | model --finalize → arch-kit |

Ver [../../references/handoffs.md](../../references/handoffs.md).

---

## Fluxo recomendado — produto novo

```text
domain.install → domain.init → domain.discover
  → domain.flow 01…NN
  → domain.capability {bc}? → domain.model --finalize
```

Re-sync: `domain.scan`. Produtos antigos: [COMMAND-GUIDE.md](../COMMAND-GUIDE.md).
