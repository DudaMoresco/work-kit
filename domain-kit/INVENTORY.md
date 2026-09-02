# Inventário do domain-kit

Referência completa de comandos, skills, wrappers, MCPs, scripts, templates, gates e regras que compõem o framework.

Documentação relacionada: [COMMAND-GUIDE.md](COMMAND-GUIDE.md) · [GUIDE.md](GUIDE.md) · [HOW-IT-WORKS.md](HOW-IT-WORKS.md) · [references/commands.md](references/commands.md)

---

## Visão geral

O domain-kit mapeia **negócio → domínio** no `architecture-hub`, antes do arch-kit (solução técnica) e do delivery-kit (backlog).

```text
domain-kit  →  arch-kit  →  delivery-kit  →  spec-kit  →  código
```

**Fronteira de responsabilidade:** tudo em `01-product/`, `02-capabilities/` (modelo de negócio) e `03-registry/produto.md`. O domain-kit **não** modela persistência física, stack ou C4 — isso é **arch-kit** (incluindo `database-model`).

---

## Plan mode e `/domain.clarify`

Contrato completo: [references/plan-mode.md](references/plan-mode.md)

- **Plan mode:** rascunhos em `products/{p}/.draft/`; promote após OK; dashboard ignora drafts
- **`/domain.clarify`:** deprecado — roteiros em `templates/clarify/` são internos
- **Scan + curadoria + síntese:** fases 0 e 0c de `/domain.init` (G0); `/domain.scan` para re-sync + refresh síntese

---

## 1. Comandos Cursor

Comandos são skills instaladas em `.cursor/skills/` a partir de `templates/commands/`. Invocados no chat com `/nome-do-comando`.

### 1.1 Meta — setup, fontes, conversa, visibilidade

| Comando | Skill | Descrição |
| --- | --- | --- |
| `/domain.install` | `domain-install` | **Instalação única por hub.** Executa `install-domain-kit.sh`: skills `domain-*`, scripts `.domain/`, MCP checklist. Próximo: `/domain.init`. |
| `/workkit.init` | `workkit-init` | **Deprecado** — alias de `/domain.install`. |
| `/domain.init {produto}` | `domain-init` | **Bootstrap + scan + síntese (G0).** Índices + fase 0 (sources, manifest, curadoria) + fase 0c (`sintese-evidencias.md`). `--adopt` para produto existente. Handoff: **`/domain.discover`**. |
| `/domain.discover` | `domain-discover` | **Descoberta DDD por sessão** (`--stage`). Lacunas (0b) + 1 estágio DDD/sessão. Modos: `full`, `minimal`, `as-is-first`, `incremental`. Gate G1. |
| `/domain.scan [--plan]` | `domain-scan` | **Re-sync de fontes** + refresh síntese se manifest mudou. |
| `/domain.status` | `domain-status` | Progresso; gates; **próximo comando sugerido** (`validate_gate.py --suggest`). |
| ~~`/domain.clarify`~~ | `domain-clarify` | **Deprecado** — redireciona. |

### 1.2 Macro — orquestração em batch

| Comando | Skill | Descrição |
| --- | --- | --- |
| `/domain.discover` | `domain-discover` | **Descoberta DDD por sessão** (`--stage`). Lacunas (0b) → 1 estágio DDD/sessão. Wrappers: estratégico, stories, ES, UL/BCs. Gate G1. |
| `/domain.model [--finalize]` | `domain-model` | **Modelagem.** `--mode incremental --bc {bc}` para evolução pós-G2. Gate G2 com `--finalize`. |

### 1.3 Micro — uma unidade por sessão (recomendado em produção)

| Comando | Skill | Descrição |
| --- | --- | --- |
| `/domain.flow {NN}` | `domain-flow` | Um fluxo por sessão; perguntas inline; plan mode; deps via `flow_deps.py`. |
| `/domain.capability {bc}` | `domain-capability` | **Design tático de um BC.** Cria `02-capabilities/{bc}/` se ausente. Wrapper `ddd-design-tatico`: agregados, invariantes. Outputs: `design-tatico.md` + `README.md`. |
| `/domain.decision` | `domain-decision` | **Registro de decisão de produto.** Propõe entrada D-n (capability, tema, status, decisão, link evidência) → confirma → append em `03-registry/produto.md`. |

### 1.4 Orquestrador do pacote

| Skill | Descrição |
| --- | --- |
| `domain-kit` | Skill raiz do pacote (`SKILL.md`). Índice de comandos, regras globais (wrapper read-only, clarify, scan, dashboard). `disable-model-invocation: true` — referência, não substitui comandos individuais. |

---

## 1.5 Lazy init — mapa pasta → comando

| Pasta / artefato | Criado por |
| --- | --- |
| `README.md`, `sources.yml`, `flows-registry.yml`, `domain-status.json`, `03-registry/produto.md` | `/domain.init` |
| `01-product/00-scan/` | `/domain.init` (primeiro scan, G0) ou `/domain.scan` (re-sync) |
| `01-product/01-vision/`, `02-domain/`, `03-discovery/` | `/domain.discover` |
| `02-capabilities/` (raiz) | `/domain.discover` |
| `02-capabilities/{bc}/` | `/domain.capability`, `/domain.flow` |
| `01-product/04-integration/` | `/domain.model` |
| `04-platform/01-non-functional/` | `/domain.model` |

Pastas ausentes após init são **esperadas**, não erro de setup.

---

## 2. Skills DDD externas (read-only)

Skills de know-how DDD vivem em `~/.cursor/skills/{nome}/SKILL.md`. O domain-kit **nunca as edita**; usa **wrappers** para contrato de paths, gates e handoffs.

| Skill | Papel no pipeline | Artefatos típicos |
| --- | --- | --- |
| `ddd-design-estrategico` | Classificar subdomínios (core / supporting / generic) | `01-product/01-vision/01-design-estrategico.md` |
| `domain-storytelling` | Narrar jornadas actor–work object–activity | `01-product/03-discovery/02-domain-storytelling/{NN}-{slug}.md` |
| `event-storming` | Eventos, comandos, políticas, read models | `01-product/03-discovery/01-event-storming/` |
| `event-storming-to-scenario-tables` | Converter ES visual em tabelas de cenário (opcional) | `01-product/02-domain/cenarios/` |
| `ddd-linguagem-e-contextos` | Glossário + fronteiras de BC | `desafio-negocio.md`, `linguagem-ubiqua.md`, `bounded-contexts.md` |
| `ddd-integracao-contextos` | Relações upstream/downstream, ACL, orquestração | `01-product/04-integration/01-contextos.md` |
| `ddd-design-tatico` | Agregados, entidades, value objects por BC | `02-capabilities/{bc}/design-tatico.md` |
| `levantamento-requisitos` | RF/RNF, personas, riscos (Cagan) | `04-platform/01-non-functional/01-requisitos.md` |
| `fluxos-entregaveis` | Fluxos to-be entregáveis numerados | `02-capabilities/{bc}/fluxos/{NN}-{slug}.md` |
| `fluxogramas-decisao` | Regras **as-is** (legado) por capability | `02-capabilities/{bc}/fluxogramas-decisao/` |

### Fora do domain-kit (arch-kit)

| Skill | Dono | Motivo |
| --- | --- | --- |
| `database-model` | **arch-kit** | Documenta **persistência física** (stores Mongo/Postgres, colunas, índices) a partir do código ou desenho técnico. Pertence a `04-platform/02-data/` e exige visão de infra — não é descoberta de negócio. Contrato H2: [handoffs.md § H2](../references/handoffs.md). |

---

## 3. Wrappers

Contratos em `wrappers/*.md` — instalados no hub via symlink `.domain/wrappers → domain-kit/wrappers`.

Cada wrapper define: skill original (link read-only), comando invocador, pré-condições, inputs, outputs no hub, pós-execução (status + dashboard).

| Wrapper | Invocado por | Resumo |
| --- | --- | --- |
| `ddd-design-estrategico.md` | `/domain.discover` | Visão estratégica e subdomínios |
| `domain-storytelling.md` | `/domain.discover` | Histórias de domínio (1+ por sessão) |
| `event-storming.md` | `/domain.discover`, `/domain.flow` | Workshop ES (discover) ou recorte por fluxo |
| `event-storming-to-scenario-tables.md` | `/domain.discover` | Cenários tabulares a partir de ES |
| `ddd-linguagem-e-contextos.md` | `/domain.discover` | Fechamento de glossário e BCs |
| `ddd-integracao-contextos.md` | `/domain.model` | Mapa de integração entre BCs |
| `ddd-design-tatico.md` | `/domain.model`, `/domain.capability` | Modelo tático de uma capability |
| `levantamento-requisitos.md` | `/domain.model --finalize` | Requisitos funcionais e não funcionais |
| `fluxos-entregaveis.md` | `/domain.flow`, `/domain.model` | Fluxo entregável to-be + registry |
| `scan-github.md` | `/domain.scan` | Leitura de repos via MCP GitHub |
| `scan-gitlab.md` | `/domain.scan` | GitLab via glab/dalvito ou import manual |
| `scan-confluence.md` | `/domain.scan` | Páginas exportadas em `00-scan/imports/` |

Índice e template para novos wrappers: [wrappers/README.md](wrappers/README.md).

---

## 4. MCPs e integrações externas

| Provedor | Mecanismo | Uso no domain-kit | Obrigatoriedade |
| --- | --- | --- | --- |
| **GitHub** | MCP `user-github` (`get_file_contents`, `search_code`, `list_issues`, `get_me`) | `/domain.scan` Plan (sugerir repos) + Execute (ler docs) | Recomendado |
| **PlantUML** | MCP `user-plantuml` | Validar sintaxe de diagramas em fluxos e discovery | Recomendado |
| **PlantUML server** | `.domain/scripts/start_plantuml_server.sh` | Render SVG no dashboard (porta **8765**) | Recomendado se usar preview |
| **Notion** | MCP `user-Notion` | Alternativa opcional a Confluence para requisitos | Opcional |
| **GitLab** | `glab`, `dalvito-cli` ou export → `imports/` | Sem MCP first-party; wrapper `scan-gitlab.md` | Fallback |
| **Confluence** | Export HTML/PDF → `00-scan/imports/` | Wrapper `scan-confluence.md`; futuro MCP | Fallback |

Estado registrado em `.domain/mcp-status.json` após install. Detalhes de setup: [ONBOARDING.md](ONBOARDING.md).

---

## 5. Scripts

| Script | Descrição |
| --- | --- |
| `install-domain-kit.sh` | Copia command skills, pack skill, scripts, config, clarify e symlink wrappers para o hub. Entrada de `/domain.install`. |
| `adopt_product.py` | Inventaria produto existente; gera índices faltantes; gap report. Usado por `/domain.init --adopt`. |
| `bootstrap-test-hub.sh` | Sandbox local `test-hub/`: install + produto demo + dashboard + `MANIFEST.md`. |
| `regenerate_dashboard.sh` | Wrapper shell; chama `generate_domain_dashboard.py`. |
| `sync_product_workspace.py` | Scaffold `.draft/`, registra `manifest.json`, regenera dashboard; visibilidade no init/scan. |
| `generate_domain_dashboard.py` | Dashboard dark theme: gates, pipeline, abas (incl. Rascunhos + CHANGELOG). Renderiza PlantUML via servidor local (porta **8765**). |
| `start_plantuml_server.sh` | Sobe `plantuml/plantuml-server:jetty` em Docker na porta **8765** para preview de diagramas. |
| `validate_gate.py` | Avalia G0, G1, G2; `--mode incremental --bc`; `--suggest` para próximo comando. |
| `flow_deps.py` | Valida dependências de fluxos no `flows-registry.yml`. |
| `promote_draft.py` | Copia `.draft/` → path canônico; atualiza `manifest.json`. |

---

## 6. Templates e artefatos de índice

| Template | Instalado em | Descrição |
| --- | --- | --- |
| `templates/commands/*.md` | `.cursor/skills/{nome}/SKILL.md` | Overlays de comandos Cursor |
| `templates/clarify/*.md` | `.domain/clarify/` | **`findings-brief`**, **`visibility-checkpoint`**, **`changelog`**, `discover` (0b), `flow`, `scan`, `scan-discover` |
| `templates/product-README.md` | `products/{p}/README.md` | Mapa do pipeline lazy init + próximo passo |
| `templates/CHANGELOG.md` | `products/{p}/CHANGELOG.md` | Histórico reverse-chronological de scans e mudanças significativas |
| `templates/config.yml` | `.domain/config.yml` | `skills_pack`, extensions (hooks), guide_paths |
| `templates/sources.yml` | `products/{p}/sources.yml` | Catálogo de fontes: github, gitlab, confluence, manual |
| `templates/flows-registry.yml` | `products/{p}/flows-registry.yml` | Índice central de fluxos: id, bc, deps, status, D-n |
| `templates/domain-status.json` | `products/{p}/domain-status.json` | Fase, gates, `scan: pending` inicial, progresso discover/model, `nextSuggested` |
| `templates/scan-manifest.json` | `01-product/00-scan/` | Findings do scan (estrutura vazia inicial) |
| `templates/draft-manifest.json` | `products/{p}/.draft/manifest.json` | Fila de promotes pendentes |
| `templates/draft-README.md` | `products/{p}/.draft/README.md` | Explica plan mode ao usuário |

### Fonte de verdade no hub (por produto)

**Índices (sempre após init):**

| Arquivo | Conteúdo |
| --- | --- |
| `README.md` | Mapa lazy init + próximo comando |
| `CHANGELOG.md` | Histórico de scans e mudanças significativas |
| `domain-status.json` | Fase, gates, `scan: pending\|complete\|partial\|skipped` |
| `flows-registry.yml` | Catálogo `fluxo-NN`, deps, status |
| `sources.yml` | Fontes (preenchido pelo scan wizard) |
| `03-registry/produto.md` | Decisões D-n |
| `dashboard.html` | Visão read-only — **nunca inventa progresso** |

**Artefatos sob demanda:**

| Pasta | Conteúdo | Aparece após |
| --- | --- | --- |
| `01-product/00-scan/` | `scan-manifest.json`, findings citados | `/domain.scan` |
| `01-product/` (demais) | Visão, domínio, discovery, integração | discover / model |
| `02-capabilities/{bc}/` | Tático, fluxos to-be, fluxogramas as-is | capability / flow |

---

## 7. Gates e handoffs

### Gates ([references/gates.yml](references/gates.yml))

| Gate | Nome | Quando | Critério resumido |
| --- | --- | --- | --- |
| **G0** | Scan | Após `/domain.scan` (opcional) | `scan` ∈ {complete, partial, skipped} — inicial `pending` até primeiro scan |
| **G1** | Fim discover | Após `/domain.discover` | Design estratégico + BCs + desafio + UL + (ES **ou** ≥2 stories) |
| **G2** | Fim model | Após `/domain.model --finalize` | Integração + tático por BC + ≥1 fluxo + registry + requisitos |

Modos de execução relaxam critérios: `full`, `minimal`, `incremental`, `as-is-first` (ver [references/pipeline.md](references/pipeline.md)).

### Handoffs ([../references/handoffs.md](../references/handoffs.md))

| ID | Transição | Âncora |
| --- | --- | --- |
| **H0** | init (scan G0) → discover | Primeiro scan no init; discover assume G0 |
| **H1** | discover → model | `03-discovery/` + BCs fechados |
| **H2** | model → **arch-kit** | Tático + fluxos + D-n + RF → `/arch.route` |

### IDs estáveis

| ID | Formato | Exemplo | Dono domain-kit |
| --- | --- | --- | --- |
| Decisão produto | `D-{nn}` | D-16 | `03-registry/produto.md` |
| Bounded context | `{bc}` kebab | `ordem-de-servico` | `02-capabilities/` |
| Fluxo entregável | `fluxo-{NN}` | fluxo-01 | `flows-registry.yml` + MD |

---

## 8. Extensions e hooks (`.domain/config.yml`)

| Hook | Comportamento |
| --- | --- |
| `after_any` | Roda `regenerate_dashboard.sh` após promotes (paths canônicos) |

_(Hooks `before_discover` / `before_flow` removidos — plan mode inline.)_

`skills_pack` aponta para o clone de `domain-kit` (monorepo: `../work-kit/domain-kit`; sandbox: `..`).

---

## 9. Regras globais

1. **Plan mode** — `.draft/` + preview; promote só após OK ([plan-mode.md](references/plan-mode.md)).
2. **Wrapper primeiro** — skill DDD read-only.
3. **Sem clarify separado** — perguntas inline no comando ativo.
4. **init = índices + 1o scan (G0)**; discover = DDD; scan = re-sync.
5. **Lazy init** — pastas de domínio sob demanda após init.
6. **Não inventar** — perguntar ou `abertos.md` (plan mode).
7. **Dashboard** — só paths promovidos contam.
8. **Changelog** — todo scan ou mudança significativa → entrada em `CHANGELOG.md` ([changelog.md](templates/clarify/changelog.md)).
9. **Fronteira arch-kit** — database-model, stack, C4 fora do domain-kit.

---

## 10. Documentação do pacote

| Arquivo | Audiência | Conteúdo |
| --- | --- | --- |
| [COMMAND-GUIDE.md](COMMAND-GUIDE.md) | Usuário | Comando → entrega; cenários legados; árvore de decisão |
| [GUIDE.md](GUIDE.md) | Usuário | Comandos, fluxo recomendado |
| [ONBOARDING.md](ONBOARDING.md) | Setup | MCPs, install, primeiro produto |
| [HOW-IT-WORKS.md](HOW-IT-WORKS.md) | Mantenedor | Pipeline interno, estrutura, extensão |
| [SKILL.md](SKILL.md) | Agent | Orquestrador e regras resumidas |
| [references/commands.md](references/commands.md) | Spec | Detalhe técnico por comando |
| [references/pipeline.md](references/pipeline.md) | Spec | Estágios 1–7, modos, fixture oficina |
| [references/gates.yml](references/gates.yml) | Máquina | Critérios G0–G2 executáveis |
| [references/examples-oficina.md](references/examples-oficina.md) | Exemplo | Walkthrough produto `oficina-mecanica` |
| [test-hub/README.md](test-hub/README.md) | Dev | Sandbox para iterar templates/wrappers |

---

## 11. Kits adjacentes (fora do escopo implementado)

| Kit | Comandos | Responsabilidade |
| --- | --- | --- |
| **arch-kit** | `/arch.route`, `/arch.architect` | Estilo, HLD/C4, ADRs, integração técnica, **`database-model`**, `04-platform/02-data/` |
| **delivery-kit** | `/delivery.backlog`, `/delivery.handoff` | Tech Stories a partir de fluxos, handoff spec-kit |

---

## 12. Sandbox de desenvolvimento

| Recurso | Path |
| --- | --- |
| Test hub | `domain-kit/test-hub/` |
| Bootstrap | `bash domain-kit/scripts/bootstrap-test-hub.sh` |
| Produto demo | `demo-produto` (Biblioteca Comunitária) |
| Manifest | `test-hub/MANIFEST.md` (gerado) |

Equivalente a `/domain.install` + `/domain.init` (índices); primeiro comando no chat: **`/domain.init demo-produto`** (scan G0) ou **`/domain.discover`** se G0 já ok.

---

## Changelog deste inventário

- **Changelog do produto** — `CHANGELOG.md` por produto; obrigatório após scan ou mudança significativa ([changelog.md](templates/clarify/changelog.md)).
- **Plan mode** — `.draft/` + promote após OK; `promote_draft.py`.
- **Clarify deprecado** — inline nos comandos; scan+curadoria unificados no discover.
