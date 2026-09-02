# Domain-Kit — Onboarding

Setup para **novo desenvolvedor** ou **novo produto** no architecture-hub.

---

## Pré-requisitos

- Cursor com Agent Skills habilitado
- Python 3.10+ (scripts de dashboard e gates — stdlib only)
- Clone do `architecture-hub` (ou monorepo `work-hub`)
- Skills DDD em `~/.cursor/skills/` (pacote pessoais) — **não são alteradas pelo framework**

---

## Passo 1 — Workspace (`/workkit.init`)

```bash
# Monorepo work-hub (architecture-hub + work-kit lado a lado):
bash ../work-kit/domain-kit/scripts/install-domain-kit.sh /path/to/architecture-hub

# Ou após clone do repositório:
git clone https://github.com/DudaMoresco/work-kit.git
bash work-kit/domain-kit/scripts/install-domain-kit.sh /path/to/architecture-hub
```

O script:

- Copia overlays para `architecture-hub/.domain/` e `.cursor/skills/domain-*`
- **Não** sobrescreve skills DDD originais
- Gera `.domain/mcp-status.json` com checagem de MCPs

### MCPs recomendados

| MCP | Namespace | Uso |
| --- | --- | --- |
| GitHub | `user-github` | `/domain.scan` — repos, README, docs |
| PlantUML | `user-plantuml` | Validar diagramas nos fluxos |
| Notion | `user-Notion` | Opcional — alternativa a Confluence |

Configure em **Cursor Settings → MCP**. Reexecute `workkit.init` após conectar.

### GitLab (sem MCP first-party)

1. Instale [`glab`](https://gitlab.com/gitlab-org/cli) ou use [`dalvito-cli`](../../dalvito-cli/SKILL.md) se corporativo
2. Ou: exporte docs → `products/{p}/01-product/00-scan/imports/`
3. Veja [wrappers/scan-gitlab.md](wrappers/scan-gitlab.md)

### Confluence (sem MCP no workspace padrão)

1. Exporte páginas (HTML/PDF) para `00-scan/imports/`
2. Rode `/domain.scan` — agente resume imports locais
3. Veja [wrappers/scan-confluence.md](wrappers/scan-confluence.md)

---

## Passo 2 — Novo produto (`/domain.init`)

No chat Cursor (com hub aberto):

```text
/domain.init meu-produto --initiative minha-iniciativa
```

Cria:

```text
products/meu-produto/
├── 01-product/
├── 02-capabilities/
├── 03-registry/
├── 04-platform/01-non-functional/
├── sources.yml              ← configure fontes externas
├── flows-registry.yml       ← índice de fluxos
├── domain-status.json
└── dashboard.html           ← regenerado pelos scripts
```

---

## Passo 3 — Fontes externas (`sources.yml`)

Edite `products/meu-produto/sources.yml`:

```yaml
version: 1
product: meu-produto
sources:
  github:
    - repo: org/repo
      paths: [README.md, docs/]
      purpose: visão produto
  gitlab: []
  confluence: []
  manual:
    - path: initiatives/minha-iniciativa/01-enunciado.md
      purpose: enunciado
```

Depois: `/domain.scan`

---

## Passo 4 — Primeira sessão de domínio

```text
/domain.clarify discover
/domain.discover
/domain.flow 01
```

Regenerar dashboard:

```bash
.domain/scripts/regenerate_dashboard.sh products/meu-produto
```

---

## Passo 5 — Handoff para arch-kit

Quando `domain.status` mostrar **Gate G2: PASS**:

```text
/arch.route
```

(domain-kit terminou; arch-kit assume estilo, C4, ADR)

---

## Checklist rápido

- [ ] `workkit.init` executado sem erro
- [ ] MCP GitHub verde (ou scan manual configurado)
- [ ] `domain.init` criou produto
- [ ] `sources.yml` preenchido
- [ ] `dashboard.html` abre no browser
- [ ] Leu [GUIDE.md](GUIDE.md)

---

## Suporte

- Estrutura interna: [HOW-IT-WORKS.md](HOW-IT-WORKS.md)
- Wrappers de skills: [wrappers/README.md](wrappers/README.md)
- Fixture completa: produto `oficina-mecanica` no hub
