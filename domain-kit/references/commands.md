# Comandos do domain-kit

Spec completa. Overlays: [`../templates/commands/`](../templates/commands/).

**Regra global:** ler wrapper em [`../wrappers/`](../wrappers/); skill original read-only; **pausar antes de gravar**.

---

## Meta

### `/workkit.init`

Instala framework no hub. Script: `install-domain-kit.sh`. Ver [ONBOARDING.md](../ONBOARDING.md).

### `/domain.init {produto} [--initiative {i}]`

Cria árvore produto, `sources.yml`, `flows-registry.yml`, `domain-status.json`, dashboard inicial.

**Explain to user:** Vou criar a estrutura do produto no hub e um dashboard vazio. Depois configure `sources.yml` e rode `/domain.scan`.

### `/domain.scan`

Lê [`sources.yml`](../templates/sources.yml); wrappers scan-github/gitlab/confluence.

**Saídas:** `01-product/00-scan/scan-manifest.json`, `README.md`

**Explain to user:** Vou buscar README e docs nas fontes configuradas e montar um manifesto para você revisar — nada entra no domínio sem sua confirmação.

### `/domain.clarify [discover|bc|flow|scan|open]`

Bancos: [`../templates/clarify/`](../templates/clarify/).

### `/domain.status`

Lê `domain-status.json`, `flows-registry.yml`, roda `validate_gate.py`.

---

## Macro

### `/domain.discover`

Orquestra wrappers: estratégico → stories → ES → UL/BCs. Hook: clarify discover.

**Gate G1** ao final.

### `/domain.model [--finalize]`

Integração, requisitos, ou sweep final. Com `--finalize`: valida G2 → handoff H2 arch-kit.

Micro-comandos `flow`/`capability` rodam **antes** do finalize.

---

## Micro

### `/domain.flow {NN}`

1. Validar deps (`flow_deps.py`)
2. clarify flow
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
| H0 | scan → clarify |
| H1 | discover → model |
| H2 | model --finalize → arch-kit |

Ver [../../references/handoffs.md](../../references/handoffs.md).

---

## Fluxo recomendado

```text
workkit.init → domain.init → domain.scan → clarify discover
  → domain.discover → domain.flow 01…NN
  → domain.capability {bc}? → domain.model --finalize
```
