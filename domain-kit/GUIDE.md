# Domain-Kit — Guia do usuário

Framework para mapear **negócio e domínio** no `architecture-hub`, antes da arquitetura técnica (arch-kit) e do código (spec-kit).

Idioma dos artefatos: **pt-BR**.

**Guia de comandos (recomendado):** [COMMAND-GUIDE.md](COMMAND-GUIDE.md) · Índice do pack: [SKILL.md](SKILL.md)

---

## Ideia central: Plan mode

**Você não precisa lembrar de `clarify` nem de passos extras.**

Cada comando (`init`, `discover`, `flow`, …):

1. Pergunta o que falta **na mesma conversa**
2. **Mostra rascunhos** (chat + `products/{p}/.draft/` + dashboard aba **Rascunhos**)
3. **Grava no hub só quando você disser** `ok` / `pode gravar`

Detalhe: [references/plan-mode.md](references/plan-mode.md)

---

## Fases

| Fase | Pergunta | Comando principal |
| --- | --- | --- |
| **Evidências** | O que sabemos, com fonte? | `/domain.init`, `/domain.scan` |
| **Estratégico** | Por quê? Onde? Como falamos? | `/domain.discover --stage strategic\|contexts` |
| **Descoberta** | Como se comporta no tempo? | `/domain.discover --stage stories\|event-storming` |
| **Operacional** | Quais cenários garantir? | `/domain.flow`, `/domain.model`, `/domain.decision` |
| **Arch-kit** | Como implementar? | `/arch.route` (fora do domain-kit) |

Aliases legados: G0 = Evidências · G1 = Estratégico + Descoberta · G2 = Operacional.

Cartão do produto: `products/{p}/product-README.md` (visão PM, status por fase, índice).

---

## Comandos — resumo

| Comando | O que faz |
| --- | --- |
| `/domain.install` | Instala framework no hub (1×) — skills + wrappers bundled |
| `/domain.init {produto}` | Índices + **scan + síntese** → fase **Evidências** |
| `/domain.init {p} --adopt` | Produto já no hub — índices + gaps |
| `/domain.discover` | Lacunas (0b) + DDD por sessão (`--stage`) → Estratégico / Descoberta |
| `/domain.scan` | Re-sync de fontes (repo/doc mudou) |
| `/domain.status` | Progresso por fase, gaps, próximo comando |
| `/domain.flow {NN}` | 1 fluxo **operacional de negócio** por sessão |
| `/domain.model [--finalize]` | NFRs de produto + fechar fase **Operacional** |
| `/domain.decision` | Registrar D-n |
| `/domain.change` | Sessão evolutiva (P-n / E-n) + handoff |

~~`/workkit.init`~~ — alias deprecado de `/domain.install`.  
~~`/domain.clarify`~~ — **não usar**; perguntas inline nos comandos acima.  
~~`/domain.capability`~~ — **deprecated** → arch-kit (`/arch.capability`).

---

## Fluxo recomendado — produto novo

```text
domain.install
  → domain.init meu-produto              # Evidências
  → domain.discover                      # lacunas + próximo estágio (auto)
  → … strategic → contexts → stories → ES
  → domain.flow 01 …
  → domain.model --finalize              # Operacional → /arch.route
```

Re-sync: `/domain.scan` se repos/docs mudaram.

Evolução pós-onboarding: `/domain.change` → handoff discover/flow/model/scan.

Produtos antigos: [COMMAND-GUIDE.md](COMMAND-GUIDE.md).

---

## Onde ficam os rascunhos

```text
products/{produto}/.draft/            ← aguardando seu OK
products/{produto}/product-README.md  ← cartão PM (atualizar após promotes materiais)
products/{produto}/dashboard.html     ← progresso + preview de rascunhos
products/{produto}/CHANGELOG.md       ← log após promotes
products/{produto}/01-product/…       ← canônico (após promote)
```

Dashboard e validação de fases **ignoram** `.draft/` — só contam arquivos promovidos.

### PlantUML no preview

```bash
.domain/scripts/start_plantuml_server.sh
.domain/scripts/regenerate_dashboard.sh products/{produto}
```

Detalhes: [references/plantuml-dashboard.md](references/plantuml-dashboard.md)

---

## Regras de ouro

1. **Plan first** — preview antes de gravar
2. **install ≠ init** — hub vs produto; **scan ≠ discover** — fontes vs negócio
3. **Não inventar** — perguntar ou registrar em abertos (P-n)
4. **init = scan + síntese** — lacunas e DDD ficam no discover; 1 estágio DDD = 1 sessão
5. **1 fluxo = 1 sessão** — caminhos em `01-product/03-operacional/fluxos/`
6. **IDs estáveis** — D-n, fluxo-NN, P-n, E-n, {bc}
7. **Changelog** — todo scan ou mudança significativa → `CHANGELOG.md`
8. **Wrapper = path** — skill bundled = know-how; não gravar em paths legados da skill

---

## Mais leitura

- [COMMAND-GUIDE.md](COMMAND-GUIDE.md) · [INVENTORY.md](INVENTORY.md) · [ONBOARDING.md](ONBOARDING.md) · [HOW-IT-WORKS.md](HOW-IT-WORKS.md)
- [skills/README.md](skills/README.md) · [wrappers/README.md](wrappers/README.md)
