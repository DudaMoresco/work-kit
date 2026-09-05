# Inventário do domain-kit

Referência completa de comandos, skills, wrappers, MCPs, scripts, templates, fases e regras que compõem o framework.

Documentação relacionada: [COMMAND-GUIDE.md](COMMAND-GUIDE.md) · [GUIDE.md](GUIDE.md) · [HOW-IT-WORKS.md](HOW-IT-WORKS.md) · [references/commands.md](references/commands.md)

---

## Visão geral

O domain-kit mapeia **negócio → domínio** em um hub de produtos, até a fase **Operacional**.

```text
Evidências → Estratégico → Descoberta → Operacional
```

**Fronteira de responsabilidade:** tudo em `01-product/` (visão, domínio, discovery, operacional) e `05-decisoes/produto.md` — mapa: [references/hub-paths.md](references/hub-paths.md). O domain-kit **não** modela persistência física, stack ou C4 — isso fica **fora do escopo do domain-kit** (`arch/` opcional, nunca gated).

---

## Plan mode e `/domain.clarify`

Contrato completo: [references/plan-mode.md](references/plan-mode.md)

- **Plan mode:** rascunhos em `products/{p}/.draft/`; promote após OK; dashboard ignora drafts
- **`/domain.clarify`:** deprecado — roteiros em `templates/clarify/` são internos
- **Scan + curadoria + síntese:** fase **Evidências** via `/domain.init`; `/domain.scan` para re-sync + refresh síntese

---

## 1. Comandos Cursor

Comandos são skills instaladas em `.cursor/skills/` a partir de `templates/commands/`. Invocados no chat com `/nome-do-comando`.

### 1.1 Meta — setup, fontes, conversa, visibilidade

| Comando | Skill | Descrição |
| --- | --- | --- |
| `/domain.install` | `domain-install` | **Instalação única por hub.** Executa `install-domain-kit.sh`: skills `domain-*`, scripts `.domain/`, MCP checklist. Próximo: `/domain.init`. |
| `/domain.init {produto}` | `domain-init` | **Bootstrap + scan + síntese (Evidências).** Índices + fontes, manifest, curadoria + `sintese-evidencias.md`. `--adopt` para produto existente. Handoff: **`/domain.discover`**. |
| `/domain.discover` | `domain-discover` | **Descoberta DDD por sessão** (`--stage`). Lacunas (0b) + 1 estágio DDD/sessão. Modos: `full`, `minimal`, `as-is-first`, `incremental`. Fases Estratégico / Descoberta. |
| `/domain.scan [--plan]` | `domain-scan` | **Re-sync de fontes** + refresh síntese se manifest mudou. |
| `/domain.status` | `domain-status` | Progresso por fase; **próximo comando sugerido** (`validate_gate.py --suggest`). |
| ~~`/domain.clarify`~~ | `domain-clarify` | **Deprecado** — redireciona. |

### 1.2 Macro — orquestração em batch

| Comando | Skill | Descrição |
| --- | --- | --- |
| `/domain.discover` | `domain-discover` | **Descoberta DDD por sessão** (`--stage`). Lacunas (0b) → 1 estágio DDD/sessão. Wrappers: estratégico, stories, ES, UL/BCs. |
| `/domain.model [--finalize]` | `domain-model` | **Modelagem.** `--mode incremental --bc {bc}` para evolução pós-Operacional. Com `--finalize`, valida e fecha a fase **Operacional**. |

### 1.3 Micro — uma unidade por sessão (recomendado em produção)

| Comando | Skill | Descrição |
| --- | --- | --- |
| `/domain.flow {NN}` | `domain-flow` | Um fluxo por sessão; perguntas inline; plan mode; deps via `flow_deps.py`. |
| `/domain.decision` | `domain-decision` | **Registro de decisão de produto.** Propõe entrada D-n (capability, tema, status, decisão, link evidência) → confirma → append em `05-decisoes/produto.md`. |
| ~~`/domain.capability`~~ | `domain-capability` | **Fora do escopo do domain-kit.** |

### 1.4 Orquestrador do pacote

| Skill | Descrição |
| --- | --- |
| `domain-kit` | Skill raiz do pacote (`SKILL.md`). Índice de comandos, regras globais (wrapper read-only, clarify, scan, dashboard). `disable-model-invocation: true` — referência, não substitui comandos individuais. |

---

## 1.5 Lazy init — mapa pasta → comando

| Pasta / artefato | Criado por |
| --- | --- |
| `product-README.md`, `sources.yml`, `flows-registry.yml`, `domain-status.json`, `05-decisoes/produto.md` | `/domain.init` |
| `01-product/00-scan/` | `/domain.init` (primeiro scan, Evidências) ou `/domain.scan` (re-sync) |
| `01-product/01-vision/`, `02-domain/`, `03-discovery/` | `/domain.discover` |
| `01-product/03-discovery/00-as-is/` | `/domain.discover --mode as-is-first` |
| `01-product/04-operacional/fluxos/` | `/domain.flow` |
| `01-product/04-operacional/requisitos.md` | `/domain.model` |

Pastas ausentes após init são **esperadas**, não erro de setup.

---

## 2. Skills DDD bundled

Know-how DDD vive em [`skills/`](skills/) (copiado para `.domain/skills/` no install). O kit **não depende** de `~/.cursor/skills/`.

Contratos de path/fase: **wrappers** em [`wrappers/`](wrappers/). Índice: [skills/README.md](skills/README.md).

| Skill | Papel no pipeline | Artefatos típicos |
| --- | --- | --- |
| `ddd-design-estrategico` | Classificar subdomínios (core / supporting / generic) | `01-product/01-vision/01-design-estrategico.md` |
| `domain-storytelling` | Narrar jornadas actor–work object–activity | `01-product/03-discovery/02-domain-storytelling/{NN}-{slug}.md` |
| `event-storming` | Eventos, comandos, políticas, read models | `01-product/03-discovery/01-event-storming/` |
| `event-storming-to-scenario-tables` | Converter ES visual em tabelas de cenário (opcional) | `01-product/02-domain/cenarios/` |
| `ddd-linguagem-e-contextos` | Glossário + fronteiras de BC | `desafio-negocio.md`, `linguagem-ubiqua.md`, `bounded-contexts.md` |
| `levantamento-requisitos` | RF/RNF, personas, riscos (Cagan) | `01-product/04-operacional/requisitos.md` |
| `fluxos-entregaveis` | Fluxos to-be (know-how; paths via wrapper operacional) | `01-product/04-operacional/fluxos/` |
| `fluxogramas-decisao` | Regras **as-is** | `01-product/03-discovery/00-as-is/` |

### Fora do escopo do domain-kit

| Tema | Motivo |
| --- | --- |
| Design tático / integração técnica | Fora do escopo; `/domain.capability` não faz parte do pipeline (sem skill bundled) |
| Modelo de dados físico (`database-model`) | Persistência física — não é descoberta de negócio |

---

## 3. Wrappers

Contratos em `wrappers/*.md` — instalados no hub como cópia `.domain/wrappers/` (+ `.domain/skills/`).

Cada wrapper define: skill bundled, comando invocador, pré-condições, inputs, outputs no hub, pós-execução (status + dashboard).

| Wrapper | Invocado por | Resumo |
| --- | --- | --- |
| `ddd-design-estrategico.md` | `/domain.discover` | Visão estratégica e subdomínios |
| `domain-storytelling.md` | `/domain.discover` | Histórias de domínio (1+ por sessão) |
| `event-storming.md` | `/domain.discover`, `/domain.flow` | Workshop ES (discover) ou recorte por fluxo |
| `event-storming-to-scenario-tables.md` | `/domain.discover` | Cenários tabulares a partir de ES |
| `ddd-linguagem-e-contextos.md` | `/domain.discover` | Fechamento de glossário e BCs |
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
| `install-domain-kit.sh` | Copia command skills, pack skill, scripts, config, clarify, **skills/** e **wrappers/** para o hub. Entrada de `/domain.install`. |
| `adopt_product.py` | Inventaria produto existente; gera índices faltantes; gap report. Usado por `/domain.init --adopt`. |
| `bootstrap-test-hub.sh` | Sandbox local `test-hub/`: install + produto demo + dashboard + `MANIFEST.md`. |
| `regenerate_dashboard.sh` | Wrapper shell; chama `generate_domain_dashboard.py`. |
| `sync_product_workspace.py` | Scaffold `.draft/`, registra `manifest.json`, regenera dashboard; visibilidade no init/scan. |
| `generate_domain_dashboard.py` | Dashboard: fases, pipeline, abas (incl. Rascunhos + CHANGELOG). Templates em `scripts/dashboard/` (HTML/CSS/JS editáveis); sync → `dashboard-assets/`. PlantUML via servidor local (porta **8765**). |
| `start_plantuml_server.sh` | Sobe `plantuml/plantuml-server:jetty` em Docker na porta **8765** para preview de diagramas. |
| `validate_gate.py` | Avalia fases (Evidências, Estratégico, Descoberta, Operacional); `--mode incremental --bc`; `--suggest` para próximo comando. |
| `flow_deps.py` | Valida dependências de fluxos no `flows-registry.yml`. |
| `promote_draft.py` | Copia `.draft/` → path canônico; atualiza `manifest.json`. |

---

## 6. Templates e artefatos de índice

| Template | Instalado em | Descrição |
| --- | --- | --- |
| `templates/commands/*.md` | `.cursor/skills/{nome}/SKILL.md` | Overlays de comandos Cursor |
| `templates/clarify/*.md` | `.domain/clarify/` | **`findings-brief`**, **`visibility-checkpoint`**, **`changelog`**, `discover` (0b), `flow`, `scan`, `scan-discover` |
| `templates/product-README.md` | `products/{p}/product-README.md` | Cartão PM — visão, benefícios, status por fase, índice |
| `templates/CHANGELOG.md` | `products/{p}/CHANGELOG.md` | Histórico reverse-chronological de scans e mudanças significativas |
| `templates/config.yml` | `.domain/config.yml` | `skills_pack`, extensions (hooks), guide_paths |
| `templates/sources.yml` | `products/{p}/sources.yml` | Catálogo de fontes: github, gitlab, confluence, manual |
| `templates/flows-registry.yml` | `products/{p}/flows-registry.yml` | Índice central de fluxos: id, bc, deps, status, D-n |
| `templates/domain-status.json` | `products/{p}/domain-status.json` | Fases, `scan: pending` inicial, progresso discover/model, `nextSuggested` |
| `templates/scan-manifest.json` | `01-product/00-scan/` | Findings do scan (estrutura vazia inicial) |
| `templates/draft-manifest.json` | `products/{p}/.draft/manifest.json` | Fila de promotes pendentes |
| `templates/draft-README.md` | `products/{p}/.draft/README.md` | Explica plan mode ao usuário |

### Fonte de verdade no hub (por produto)

**Índices (sempre após init):**

| Arquivo | Conteúdo |
| --- | --- |
| `product-README.md` | Cartão PM — visão, status por fase, próximo comando |
| `README.md` | Opcional; preferir `product-README.md` |
| `CHANGELOG.md` | Histórico de scans e mudanças significativas |
| `domain-status.json` | Fases, `scan: pending\|complete\|partial\|skipped` |
| `flows-registry.yml` | Catálogo `fluxo-NN`, deps, status |
| `sources.yml` | Fontes (preenchido pelo scan wizard) |
| `05-decisoes/produto.md` | Decisões D-n |
| `dashboard.html` | Visão read-only — **nunca inventa progresso** |

**Artefatos sob demanda:**

| Pasta | Conteúdo | Aparece após |
| --- | --- | --- |
| `01-product/00-scan/` | `scan-manifest.json`, findings citados | `/domain.init` / `/domain.scan` |
| `01-product/` (demais) | Visão, domínio, discovery, operacional | discover / flow / model |
| `05-decisoes/produto.md` | Decisões D-n | `/domain.init` / `/domain.decision` |

---

## 7. Fases e handoffs

### Fases ([references/gates.yml](references/gates.yml))

| Fase | Quando | Critério resumido |
| --- | --- | --- |
| **Evidências** | Após `/domain.init` (scan no init ou `/domain.scan`) | `scan` ∈ {complete, partial, skipped} — inicial `pending` até primeiro scan |
| **Estratégico** | Após `/domain.discover` (contexts) | Design estratégico + BCs + desafio + UL |
| **Descoberta** | Após stories / ES | Event-storming **ou** ≥2 stories |
| **Operacional** | Após `/domain.model --finalize` | ≥1 fluxo ready + NFR + registry |

Modos de execução relaxam critérios: `full`, `minimal`, `incremental`, `as-is-first` (ver [references/pipeline.md](references/pipeline.md)).

### Handoffs internos ([references/handoffs.md](references/handoffs.md))

| Transição | Âncora |
| --- | --- |
| init (Evidências) → discover | Primeiro scan no init; discover assume Evidências ok |
| discover → flow / model | `03-discovery/` + BCs fechados |
| model --finalize → fim do kit | Operacional PASS; próxima etapa técnica **fora do escopo do domain-kit** |

### IDs estáveis

| ID | Formato | Exemplo | Dono domain-kit |
| --- | --- | --- | --- |
| Decisão produto | `D-{nn}` | D-16 | `05-decisoes/produto.md` |
| Bounded context | `{bc}` kebab | `ordem-de-servico` | `02-domain/bounded-contexts.md` |
| Fluxo entregável | `fluxo-{NN}` | fluxo-01 | `flows-registry.yml` + MD |

---

## 8. Extensions e hooks (`.domain/config.yml`)

| Hook | Comportamento |
| --- | --- |
| `after_any` | Roda `regenerate_dashboard.sh` após promotes (paths canônicos) |

_(Hooks `before_discover` / `before_flow` removidos — plan mode inline.)_

`skills_pack` aponta para o **clone do domain-kit** (path absoluto ou relativo ao hub; no sandbox de teste costuma ser `..`).

---

## 9. Regras globais

1. **Plan mode** — `.draft/` + preview; promote só após OK ([plan-mode.md](references/plan-mode.md)).
2. **Wrapper primeiro** — depois skill em `.domain/skills/` (bundled no kit).
3. **Sem clarify separado** — perguntas inline no comando ativo.
4. **init = índices + 1º scan (Evidências)**; discover = DDD; scan = re-sync.
5. **Lazy init** — pastas de domínio sob demanda após init.
6. **Não inventar** — perguntar ou `abertos.md` (plan mode).
7. **Dashboard** — só paths promovidos contam.
8. **Changelog** — todo scan ou mudança significativa → entrada em `CHANGELOG.md` ([changelog.md](templates/clarify/changelog.md)).
9. **Fronteira** — modelo de dados físico, stack, C4 e design tático ficam **fora do escopo do domain-kit**.

---

## 10. Documentação do pacote

| Arquivo | Audiência | Conteúdo |
| --- | --- | --- |
| [COMMAND-GUIDE.md](COMMAND-GUIDE.md) | Usuário | Comando → entrega; cenários; árvore de decisão |
| [GUIDE.md](GUIDE.md) | Usuário | Comandos, fluxo recomendado |
| [ONBOARDING.md](ONBOARDING.md) | Setup | MCPs, install, primeiro produto |
| [HOW-IT-WORKS.md](HOW-IT-WORKS.md) | Mantenedor | Pipeline interno, estrutura, extensão |
| [SKILL.md](SKILL.md) | Agent | Orquestrador e regras resumidas |
| [references/commands.md](references/commands.md) | Spec | Detalhe técnico por comando |
| [references/pipeline.md](references/pipeline.md) | Spec | Estágios, modos, fixture oficina |
| [references/gates.yml](references/gates.yml) | Máquina | Critérios de fase executáveis |
| [references/examples-oficina.md](references/examples-oficina.md) | Exemplo | Walkthrough produto `oficina-mecanica` |
| [test-hub/README.md](test-hub/README.md) | Dev | Sandbox para iterar templates/wrappers |

---

## 11. Sandbox de desenvolvimento

| Recurso | Path |
| --- | --- |
| Test hub | `domain-kit/test-hub/` |
| Bootstrap | `bash domain-kit/scripts/bootstrap-test-hub.sh` |
| Produto demo | `demo-produto` (Biblioteca Comunitária) |
| Manifest | `test-hub/MANIFEST.md` (gerado) |

Equivalente a `/domain.install` + `/domain.init` (índices); primeiro comando no chat: **`/domain.init demo-produto`** (fase Evidências) ou **`/domain.discover`** se Evidências já ok.

---

## Changelog deste inventário

- **Changelog do produto** — `CHANGELOG.md` por produto; obrigatório após scan ou mudança significativa ([changelog.md](templates/clarify/changelog.md)).
- **Plan mode** — `.draft/` + promote após OK; `promote_draft.py`.
- **Clarify deprecado** — inline nos comandos; scan+curadoria unificados no init / scan.
