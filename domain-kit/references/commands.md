# Comandos do domain-kit

Spec completa. Overlays: [`../templates/commands/`](../templates/commands/).

**Guia prático:** [`../COMMAND-GUIDE.md`](../COMMAND-GUIDE.md)

**Regras globais:**

1. **[Plan mode](../references/plan-mode.md)** — conteúdo em `.draft/` + preview; promote só após OK.
2. Ler **wrapper** em `.domain/wrappers/` (autoridade de path); skill em `.domain/skills/{nome}/`; **sem `/domain.clarify`**. Fases: Evidências → Estratégico → Descoberta → Operacional.

---

## Meta — hub e produto

### `/domain.install`

Instala o kit no hub (1x). Script: `domain-kit/scripts/install-domain-kit.sh /caminho/do/hub`. Ver [ONBOARDING.md](../ONBOARDING.md).

**Entrega:** skills, scripts, MCP checklist. **Não entrega:** artefatos de produto.

### `/domain.init {produto} [--initiative {i}] [--adopt]`

Bootstrap do produto: índices + **primeiro scan** (fase Evidências).

Com `--adopt`: produto já no hub — gera índices faltantes, inventário, gaps via `adopt_product.py`.

**Entrega:** `sources.yml`, `scan-manifest.json`, índices. **Não entrega:** BCs, fluxos, tático.

**Handoff:** `/domain.discover`

### `/domain.scan [--plan]`

Re-sync de fontes quando repos/docs mudaram **sem** refazer discover.

**Saídas:** `01-product/00-scan/scan-manifest.json`, `README.md`

### `/domain.status`

Lê fases via `validate_gate.py --suggest`; lista fluxos bloqueados; próximo comando sugerido.

### `/domain.clarify` — deprecado

Redirecionar para comando principal.

---

## Macro — descoberta e modelagem

### `/domain.discover [--mode full|minimal|as-is-first|incremental] [--bc {bc}]`

Descoberta DDD (fases Estratégico e Descoberta). **Pré-condição:** Evidências PASS (scan via init).

Roteiros: [`discover.md`](../templates/clarify/discover.md)

Modos: ver [COMMAND-GUIDE.md](../COMMAND-GUIDE.md)

### `/domain.model [--finalize] [--mode full|incremental] [--bc {bc}]`

Requisitos NFR de produto e sweep. Com `--finalize`: valida Operacional — fim do pipeline domain-kit.

Micro-comandos `flow`/`decision` rodam **antes** do finalize.

---

## Micro

### `/domain.flow {NN}`

1. Validar deps (`flow_deps.py`)
2. Perguntas inline
3. Wrapper fluxos-entregaveis
4. Atualizar `flows-registry.yml` → `ready`
5. Regenerar dashboard

### `/domain.capability {bc}`

Fora do escopo do domain-kit (próxima etapa técnica).

### `/domain.decision`

Propor D-n → confirmar → `05-decisoes/produto.md`.

---

## Handoffs

| ID | De → Para |
| --- | --- |
| H0 | init (Evidências) → discover |
| H1 | discover → model / flow |
| H2 | model --finalize → fim do domain-kit (próxima etapa técnica fora deste kit) |

Ver [../../references/handoffs.md](../../references/handoffs.md).

---

## Fluxo recomendado — produto novo

```text
domain.install → domain.init → domain.discover
  → domain.flow 01…NN
  → domain.model --finalize
```

Re-sync: `domain.scan`. Produtos antigos: [COMMAND-GUIDE.md](../COMMAND-GUIDE.md).
