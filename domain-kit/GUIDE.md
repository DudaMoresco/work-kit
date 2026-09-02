# Domain-Kit — Guia do usuário

Framework para mapear **negócio e domínio** no `architecture-hub`, antes da arquitetura técnica (arch-kit) e do código (spec-kit).

Idioma dos artefatos: **pt-BR**.

**Guia de comandos (recomendado):** [COMMAND-GUIDE.md](COMMAND-GUIDE.md)

---

## Ideia central: Plan mode

**Você não precisa lembrar de `clarify` nem de passos extras.**

Cada comando (`init`, `discover`, `flow`, …):

1. Pergunta o que falta **na mesma conversa**
2. **Mostra rascunhos** (chat + `products/{p}/.draft/` + dashboard aba **Rascunhos**)
3. **Grava no hub só quando você disser** `ok` / `pode gravar`

Detalhe: [references/plan-mode.md](references/plan-mode.md)

---

## Comandos — resumo

| Comando | O que faz |
| --- | --- |
| `/domain.install` | Instala framework no hub (1x) |
| `/domain.init {produto}` | Índices + **scan + síntese** → Gate G0 |
| `/domain.init {p} --adopt` | Produto já no hub — índices + gaps |
| `/domain.discover` | Lacunas (0b) + DDD por sessão (`--stage`) → Gate G1 |
| `/domain.scan` | Re-sync de fontes (repo/doc mudou) |
| `/domain.status` | Progresso, gates, próximo comando |
| `/domain.model` | Integração, requisitos, `--finalize` → G2 |
| `/domain.flow {NN}` | 1 fluxo por sessão |
| `/domain.capability {bc}` | Design tático de um BC |
| `/domain.decision` | Registrar D-n |

~~`/workkit.init`~~ — alias deprecado de `/domain.install`.  
~~`/domain.clarify`~~ — **não usar**; perguntas inline nos comandos acima.

---

## Fluxo recomendado — produto novo

```text
domain.install
  → domain.init meu-produto           # índices + scan + síntese (G0)
  → domain.discover                   # lacunas (0b) + próximo estágio (auto)
  → … strategic → stories → ES → contexts (G1)
  → domain.flow 01 …
  → domain.model --finalize           # G2
```

Re-sync: `/domain.scan` se repos/docs mudaram.

Produtos antigos: ver cenários em [COMMAND-GUIDE.md](COMMAND-GUIDE.md).

---

## Onde ficam os rascunhos

```text
products/{produto}/.draft/          ← aguardando seu OK (ver também dashboard → Rascunhos)
products/{produto}/dashboard.html   ← progresso + preview de rascunhos
products/{produto}/CHANGELOG.md     ← log após promotes
products/{produto}/01-product/…     ← canônico (após promote)
```

Dashboard e gates **ignoram** `.draft/` — só contam arquivos promovidos.

### PlantUML no preview

Diagramas em blocos `` `plantuml `` nos artefatos MD são renderizados na aba **Preview** do dashboard.
Requer servidor local na porta **8765** (evita conflito com 8080):

```bash
.domain/scripts/start_plantuml_server.sh
.domain/scripts/regenerate_dashboard.sh products/{produto}
```

Detalhes: [references/plantuml-dashboard.md](references/plantuml-dashboard.md)

---

## Regras de ouro

1. **Plan first** — preview antes de gravar
2. **install ≠ init** — hub vs produto; **scan ≠ discover** — fontes vs negócio
3. **Não inventar** — perguntar ou registrar em abertos
4. **init = scan + síntese** — lacunas e DDD ficam no discover; 1 estágio DDD = 1 sessão
5. **1 fluxo = 1 sessão**
6. **IDs estáveis** — D-n, fluxo-NN, {bc}
7. **Changelog** — todo scan ou mudança significativa → `products/{p}/CHANGELOG.md`

---

## Mais leitura

- [COMMAND-GUIDE.md](COMMAND-GUIDE.md) · [INVENTORY.md](INVENTORY.md) · [ONBOARDING.md](ONBOARDING.md) · [HOW-IT-WORKS.md](HOW-IT-WORKS.md)
