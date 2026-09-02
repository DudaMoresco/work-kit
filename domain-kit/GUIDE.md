# Domain-Kit — Guia do usuário

Framework para mapear **negócio e domínio** no `architecture-hub`, antes da arquitetura técnica (arch-kit) e do código (spec-kit).

Idioma dos artefatos: **pt-BR**.

---

## Para quem é

- Product owners e devs documentando um produto novo
- Times fazendo DDD + fluxos entregáveis antes de codar
- Quem já tem material em GitHub, GitLab ou Confluence e quer consolidar no hub

---

## Comandos — resumo

| Comando | O que faz |
| --- | --- |
| `/workkit.init` | 1× por máquina: instala framework, checa MCPs |
| `/domain.init {produto}` | 1× por produto: pastas, registry, dashboard vazio |
| `/domain.scan` | Lê GitHub/GitLab/Confluence configurados em `sources.yml` |
| `/domain.clarify` | Perguntas antes de gravar; revisa scan |
| `/domain.status` | Onde estamos (gates, fluxos, artefatos) |
| `/domain.discover` | Descoberta batch: estratégico, ES, BCs |
| `/domain.model` | Modelagem batch ou `--finalize` pós-fluxos |
| `/domain.flow {NN}` | **1 fluxo por sessão** (recomendado) |
| `/domain.capability {bc}` | Design tático de um bounded context |
| `/domain.decision` | Registrar decisão D-n |

---

## Fluxo recomendado

```text
workkit.init
  → domain.init meu-produto --initiative minha-iniciativa
  → domain.scan
  → domain.clarify discover
  → domain.discover
  → domain.flow 01
  → domain.flow 02
  → …
  → domain.capability {bc}   (se faltou tático)
  → domain.model --finalize
```

Abra `products/{produto}/dashboard.html` a qualquer momento.

---

## Regras de ouro

1. **Não inventar** — se faltar fato, `/domain.clarify` pergunta
2. **Confirmar antes de gravar** — agente propõe; você diz "pode gravar"
3. **Citar fontes** — scan e docs externos entram com URL/path no manifest
4. **1 fluxo = 1 conversa** — use `/domain.flow` em produtos com vários fluxos
5. **IDs estáveis** — `D-n`, `fluxo-NN`, `{bc}` — referenciados downstream

---

## Onde ficam os artefatos

| Tema | Pasta |
| --- | --- |
| Scan / fontes | `01-product/00-scan/`, `sources.yml` |
| Domínio | `01-product/01-vision/`, `02-domain/`, `03-discovery/` |
| Capabilities | `02-capabilities/{bc}/` |
| Decisões produto | `03-registry/produto.md` |
| Índice fluxos | `flows-registry.yml` |
| Progresso | `domain-status.json`, `dashboard.html` |

Paths canônicos: [references/hub-paths.md](../../references/hub-paths.md)

---

## Erros comuns

| Problema | Solução |
| --- | --- |
| Scan vazio | Preencher `sources.yml`; GitHub precisa MCP configurado |
| GitLab/Confluence sem MCP | Export manual → `00-scan/imports/`; ver ONBOARDING |
| Gate G2 falha | Falta tático, fluxo ou D-n — `domain.status` lista gaps |
| Fluxo bloqueado | Deps no `flows-registry.yml` — concluir fluxo anterior |
| Quer stack/C4 | Sair do domain-kit → **arch-kit** (`/arch.route`) |

---

## Mais leitura

- [ONBOARDING.md](ONBOARDING.md) — primeiro setup
- [HOW-IT-WORKS.md](HOW-IT-WORKS.md) — arquitetura interna
- [references/commands.md](references/commands.md) — spec técnica
- [references/examples-oficina.md](references/examples-oficina.md) — caso real
