# Domain-Kit — Onboarding

Setup para **novo desenvolvedor** ou **novo produto** no architecture-hub.

**Mapa de comandos:** [COMMAND-GUIDE.md](COMMAND-GUIDE.md) · [SKILL.md](SKILL.md)

---

## Pré-requisitos

- Cursor com Agent Skills habilitados
- Python 3.10+ (scripts de dashboard e fases — stdlib only)
- **Docker** (opcional) — servidor PlantUML para preview no dashboard
- Clone do `architecture-hub` (ou monorepo `work-hub`)
- Clone do **domain-kit / work-kit** — skills DDD em `domain-kit/skills/` (sem `~/.cursor/skills/`)

---

## Passo 1 — Workspace (`/domain.install`)

```bash
# Monorepo work-hub:
bash ../work-kit/domain-kit/scripts/install-domain-kit.sh /path/to/architecture-hub

# Clone standalone:
git clone https://github.com/DudaMoresco/work-kit.git
bash work-kit/domain-kit/scripts/install-domain-kit.sh /path/to/architecture-hub
```

```text
/domain.install
```

O script:

- Copia comandos para `.cursor/skills/domain-*`
- Copia know-how para `.domain/skills/` e contratos para `.domain/wrappers/`
- Copia scripts, clarify e config para `.domain/`
- Gera `.domain/mcp-status.json`

**Alias deprecado:** `/workkit.init`.

### MCPs recomendados

| MCP | Namespace | Uso |
| --- | --- | --- |
| GitHub | `user-github` | `/domain.init` e `/domain.scan` |
| PlantUML | `user-plantuml` | Validar diagramas (agente) |
| PlantUML server | `start_plantuml_server.sh` | Preview no dashboard (porta **8765**) |
| Notion | `user-Notion` | Opcional |

```bash
.domain/scripts/start_plantuml_server.sh
```

GitLab / Confluence: [wrappers/scan-gitlab.md](wrappers/scan-gitlab.md), [wrappers/scan-confluence.md](wrappers/scan-confluence.md).

---

## Passo 2 — Novo produto (`/domain.init`) — fase Evidências

```text
/domain.init meu-produto --initiative minha-iniciativa
```

```text
products/meu-produto/
├── product-README.md            ← cartão PM
├── sources.yml
├── flows-registry.yml
├── domain-status.json
├── CHANGELOG.md
├── 03-registry/produto.md
├── 01-product/00-scan/          ← após OK do scan
│   ├── scan-manifest.json
│   ├── sintese-evidencias.md
│   └── README.md
└── dashboard.html
```

**Produto já no hub?**

```text
/domain.init produto-existente --adopt
/domain.status
```

---

## Passo 3 — Descoberta (`/domain.discover`) — Estratégico + Descoberta

Pré-condição: fase **Evidências** PASS.

```text
/domain.discover
```

1. Lacunas de negócio (0b)
2. Um estágio DDD por sessão (`--stage auto|strategic|contexts|stories|event-storming`)

Modos: `as-is-first`, `incremental`, `minimal` — [COMMAND-GUIDE.md](COMMAND-GUIDE.md).

**Re-sync de fontes:** `/domain.scan`.

---

## Passo 4 — Operacional

```text
/domain.flow 01
/domain.flow 02
/domain.model --finalize
```

Fluxos novos em `01-product/03-operacional/fluxos/` (não em `02-capabilities/`).

```bash
.domain/scripts/regenerate_dashboard.sh products/meu-produto
```

---

## Passo 5 — Handoff para arch-kit

Quando `/domain.status` mostrar **Operacional: PASS**:

```text
/arch.route
```

Design tático, integração técnica, C4, ADR → arch-kit.  
~~`/domain.capability`~~ está deprecated.

---

## Evolução depois do onboarding

```text
/domain.change --kind problem-new --title "…"
# ou --kind evolution --title "…"
```

Registra P-n / E-n e sugere o próximo comando de fase.

---

## Checklist rápido

- [ ] `/domain.install` ok (`.domain/skills/` presente)
- [ ] MCP GitHub (ou imports manuais)
- [ ] `/domain.init` → Evidências
- [ ] `/domain.discover` em andamento ou PASS Estratégico/Descoberta
- [ ] `/domain.flow` + `/domain.model --finalize` → Operacional
- [ ] `product-README.md` atualizado
- [ ] Leu [COMMAND-GUIDE.md](COMMAND-GUIDE.md)

---

## Suporte

- [COMMAND-GUIDE.md](COMMAND-GUIDE.md) · [HOW-IT-WORKS.md](HOW-IT-WORKS.md) · [INVENTORY.md](INVENTORY.md)
- Exemplo de migração: [references/examples/notificacao-dividas-pendencias/](references/examples/notificacao-dividas-pendencias/)
