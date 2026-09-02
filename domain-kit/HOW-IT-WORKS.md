# Domain-Kit — Como funciona por dentro

Documentação para mantenedores e arquitetos.

---

## Posição no pipeline

```text
domain-kit  →  arch-kit  →  delivery-kit  →  spec-kit  →  código
   ↑ você está aqui
```

Handoff domain → arch: **H2** quando Gate **G2** passa ([../references/handoffs.md](../references/handoffs.md)).

---

## Camadas de comandos

| Camada | Comandos | Papel |
| --- | --- | --- |
| **Meta** | init, scan, clarify, status | Setup, fontes, conversa, visibilidade |
| **Macro** | discover, model | Orquestram várias skills em batch |
| **Micro** | flow, capability, decision | Uma unidade de trabalho por sessão |

Macro = conveniente para replay; **micro = recomendado** em produtos com N fluxos.

---

## Fonte de verdade

| Arquivo | Conteúdo |
| --- | --- |
| `domain-status.json` | Fase atual, gates, scan status |
| `flows-registry.yml` | Catálogo fluxo-NN, deps, status |
| `scan-manifest.json` | Findings de fontes externas (citados) |
| `03-registry/produto.md` | Decisões D-n |
| Artefatos MD | Conteúdo; dashboard só lê |

O dashboard HTML é **read-only** — nunca inventa progresso.

---

## Gates

| Gate | Após | Critério resumido |
| --- | --- | --- |
| **G0** | scan | Manifest ou skip documentado |
| **G1** | discover | Estratégico + BCs + discovery |
| **G2** | model | Integração + tático + fluxos + D-n + RF |

Definição: [references/gates.yml](references/gates.yml) · validação: `validate_gate.py`

---

## Scan externo

```mermaid
sequenceDiagram
  participant User
  participant Scan as domain.scan
  participant MCP as GitHub_MCP
  participant Hub as architecture_hub

  User->>Scan: sources.yml
  Scan->>MCP: get_file_contents
  MCP-->>Scan: README docs
  Scan->>Hub: scan-manifest.json
  Scan->>User: clarify incorporar?
  User->>Hub: artefatos confirmados
```

GitLab/Confluence: mesmo contrato de manifest; implementação via wrapper + fallback manual ([wrappers/scan-gitlab.md](wrappers/scan-gitlab.md)).

---

## Wrappers vs skills originais

Skills DDD vivem em `~/.cursor/skills/ddd-*/SKILL.md` — **imutáveis** pelo framework.

`domain-kit/wrappers/{skill}.md` define:

- Qual comando invoca
- Pré-condições (gates, paths)
- Outputs esperados no hub
- Link read-only para skill original

Comandos em `.cursor/skills/domain-*/SKILL.md` dizem: *siga o wrapper; leia skill original se precisar do know-how completo*.

---

## Multi-fluxo

`flows-registry.yml` é o índice central:

- `fluxo-NN` com deps (`fluxo-02` depende de `fluxo-01`)
- Status: `draft` → `clarifying` → `ready`
- Link para MD em `02-capabilities/{bc}/fluxos/`

`/domain.flow NN` valida deps antes de começar.

Oficina: 7 fluxos → depois viram Tech Stories #11–#17 (delivery-kit).

---

## Dashboard

`generate_domain_dashboard.py`:

1. Lê `domain-status.json`, `flows-registry.yml`
2. Checa existência de paths canônicos
3. Opcionalmente roda `validate_gate.py`
4. Gera HTML com pipeline, grade de fluxos, tabs MD

Espelha filosofia do [spec-kit-dashboard](../../spec-kit-dashboard/).

---

## Estrutura do pacote

```text
domain-kit/
├── GUIDE.md ONBOARDING.md HOW-IT-WORKS.md
├── SKILL.md
├── wrappers/           ← contratos (não editam skills originais)
├── templates/          ← sources, registry, commands overlays
├── scripts/            ← install, dashboard, validate_gate
└── references/         ← pipeline, commands, gates, examples
```

Instalação copia para hub:

```text
architecture-hub/
├── .domain/            ← config, scripts, clarify/
└── .cursor/skills/domain-*/
```

---

## Extensão

Para nova skill DDD:

1. Criar `wrappers/nova-skill.md` (não editar SKILL.md original)
2. Referenciar no comando macro/micro adequado
3. Atualizar `references/commands.md`

Para novo provedor de scan:

1. `wrappers/scan-{provedor}.md`
2. Estender schema `sources.yml`
3. Overlay `domain.scan`
