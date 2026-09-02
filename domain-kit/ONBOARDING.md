# Domain-Kit — Onboarding

Setup para **novo desenvolvedor** ou **novo produto** no architecture-hub.

**Mapa de comandos:** [COMMAND-GUIDE.md](COMMAND-GUIDE.md)

---

## Pré-requisitos

- Cursor com Agent Skills habilitado
- Python 3.10+ (scripts de dashboard e gates — stdlib only)
- **Docker** (opcional) — servidor PlantUML local para preview de diagramas no dashboard
- Clone do `architecture-hub` (ou monorepo `work-hub`)
- Skills DDD em `~/.cursor/skills/` (pacote pessoais) — **não são alteradas pelo framework**

---

## Passo 1 — Workspace (`/domain.install`)

```bash
# Monorepo work-hub (architecture-hub + work-kit lado a lado):
bash ../work-kit/domain-kit/scripts/install-domain-kit.sh /path/to/architecture-hub

# Ou após clone do repositório:
git clone https://github.com/DudaMoresco/work-kit.git
bash work-kit/domain-kit/scripts/install-domain-kit.sh /path/to/architecture-hub
```

No chat Cursor:

```text
/domain.install
```

O script:

- Copia overlays para `architecture-hub/.domain/` e `.cursor/skills/domain-*`
- **Não** sobrescreve skills DDD originais
- Gera `.domain/mcp-status.json` com checagem de MCPs

**Alias deprecado:** `/workkit.init` — mesmo efeito, use `/domain.install`.

### MCPs recomendados

| MCP | Namespace | Uso |
| --- | --- | --- |
| GitHub | `user-github` | `/domain.init` e `/domain.scan` — ler repos |
| PlantUML | `user-plantuml` | Validar diagramas nos fluxos (agente) |
| PlantUML server | `.domain/scripts/start_plantuml_server.sh` | Renderizar diagramas no **dashboard** (porta **8765**) |
| Notion | `user-Notion` | Opcional — alternativa a Confluence |

Configure MCPs em **Cursor Settings → MCP**. Reexecute `/domain.install` após conectar.

Servidor local (preview do dashboard):

```bash
.domain/scripts/start_plantuml_server.sh
```

Ver [references/plantuml-dashboard.md](references/plantuml-dashboard.md).

### GitLab (sem MCP first-party)

1. Instale [`glab`](https://gitlab.com/gitlab-org/cli) ou use [`dalvito-cli`](../../dalvito-cli/SKILL.md) se corporativo
2. Ou: exporte docs → `products/{p}/01-product/00-scan/imports/` (detectado no init)
3. Veja [wrappers/scan-gitlab.md](wrappers/scan-gitlab.md)

### Confluence (sem MCP no workspace padrão)

1. Exporte páginas (HTML/PDF) para `00-scan/imports/`
2. Incluir no wizard da fase 0 do `/domain.init`
3. Veja [wrappers/scan-confluence.md](wrappers/scan-confluence.md)

---

## Passo 2 — Novo produto (`/domain.init`)

No chat Cursor (com hub aberto):

```text
/domain.init meu-produto --initiative minha-iniciativa
```

Cria índices **e conduz o primeiro scan** (plan mode):

```text
products/meu-produto/
├── README.md
├── sources.yml
├── flows-registry.yml
├── domain-status.json
├── 03-registry/produto.md
├── 01-product/00-scan/          ← após OK do scan (G0)
│   ├── scan-manifest.json
│   └── README.md
└── dashboard.html
```

**Produto já no hub?** Use `--adopt`:

```text
/domain.init produto-existente --adopt
/domain.status
```

---

## Passo 3 — Descoberta (`/domain.discover`)

Pré-condição: Gate G0 (scan ok via init).

```text
/domain.discover
```

O agente conduz **descoberta DDD** (não refaz scan se G0 ok):

1. **Negócio** — atores, MVP, legado
2. **DDD** — estratégico, ES/stories, UL, BCs

Modos para produtos antigos: `--mode as-is-first`, `incremental`, `minimal` — ver [COMMAND-GUIDE.md](COMMAND-GUIDE.md).

**Plan mode:** artefatos em `.draft/` até OK.

**Re-sync de fontes:** `/domain.scan` se repos/docs mudaram.

---

## Passo 4 — Fluxos e modelagem

```text
/domain.flow 01
/domain.capability {bc}
/domain.model --finalize
```

Regenerar dashboard:

```bash
.domain/scripts/regenerate_dashboard.sh products/meu-produto
```

---

## Passo 5 — Handoff para arch-kit

Quando `/domain.status` mostrar **Gate G2: PASS**:

```text
/arch.route
```

(domain-kit terminou; arch-kit assume estilo, C4, ADR)

---

## Checklist rápido

- [ ] `/domain.install` executado sem erro
- [ ] MCP GitHub verde (ou fontes manuais no init)
- [ ] `/domain.init` criou produto + G0
- [ ] `/domain.discover` executado (ou em andamento)
- [ ] `dashboard.html` abre no browser
- [ ] PlantUML: `start_plantuml_server.sh` + diagramas visíveis na aba Preview (se houver)
- [ ] Leu [COMMAND-GUIDE.md](COMMAND-GUIDE.md)

---

## Suporte

- Comandos e cenários legados: [COMMAND-GUIDE.md](COMMAND-GUIDE.md)
- Estrutura interna: [HOW-IT-WORKS.md](HOW-IT-WORKS.md)
- Inventário: [INVENTORY.md](INVENTORY.md)
- Fixture completa: produto `oficina-mecanica` no hub
