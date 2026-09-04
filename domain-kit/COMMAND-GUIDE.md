# Domain-Kit — Guia de comandos

Referência rápida: **o que cada comando entrega**, quando usar, e fluxos para produtos novos vs antigos.

Idioma dos artefatos: **pt-BR**. Contrato: [references/plan-mode.md](references/plan-mode.md) · Fases: [SKILL.md](SKILL.md).

---

## Tabela — comando → entrega → o que NÃO entrega

| Comando | Entrega real (peso) | Fase | NÃO entrega |
| --- | --- | --- | --- |
| `/domain.install` | Comandos `domain-*`, `.domain/skills/`, wrappers, scripts, MCP checklist | — | Artefato de produto |
| `/domain.init {p}` | Índices + **primeiro scan** + **síntese** | **Evidências** | Lacunas (0b), BCs, ES, fluxos, tático |
| `/domain.init {p} --adopt` | Índices faltantes + inventário + gaps | — | Não recria conteúdo existente |
| `/domain.scan {p}` | Delta no manifest + refresh síntese + CHANGELOG | Evidências (re-sync) | Lacunas (0b), DDD |
| `/domain.discover {p}` | Lacunas (0b) + DDD **por estágio** (`--stage`) | **Estratégico** / **Descoberta** | Tático, fluxos to-be, integração técnica |
| `/domain.flow {NN}` | 1 fluxo **operacional de negócio** | **Operacional** | Serviços/filas (arch), outros fluxos |
| `/domain.decision` | 1 linha D-n no registry | Operacional | Texto longo duplicado |
| `/domain.model {p}` | NFRs de produto (draft) | Operacional | Finalize |
| `/domain.model {p} --finalize` | NFRs + validação Operacional | **Operacional** | C4, ADR, design tático, database-model |
| `/domain.change` | Sessão P-n / E-n + `activeChange` + handoff | Transversal | Artefatos DDD diretos |
| `/domain.status {p}` | Diagnóstico de fases + próximo comando | — | Conteúdo novo |
| ~~`/domain.capability`~~ | **Deprecated** → arch-kit | — | — |

**Alias deprecado:** `/workkit.init` → `/domain.install`.

---

## Pipeline recomendado — produto novo

```text
/domain.install                         # 1× por hub
/domain.init meu-produto                # Evidências
/domain.discover                        # lacunas + auto: próximo estágio
/domain.discover --stage strategic      # ou contexts | stories | event-storming
/domain.flow 01 … NN                    # 1 fluxo = 1 sessão (03-operacional/fluxos/)
/domain.model --finalize                # Operacional → /arch.route
```

Re-sync: `/domain.scan`. Evolução: `/domain.change`.

---

## Árvore de decisão — qual comando usar?

```text
Primeira vez no hub?
  └─ SIM → /domain.install

Produto novo no hub?
  └─ SIM → /domain.init {p} → /domain.discover

Produto JÁ existe no hub mas sem domain-kit?
  └─ SIM → /domain.init {p} --adopt → /domain.status

Sistema LEGADO em produção?
  └─ SIM → /domain.init {p} → /domain.discover --mode as-is-first

Algo mudou depois do onboarding (problema ou evolução)?
  └─ SIM → /domain.change → handoff sugerido

Nova jornada em produto com Operacional PASS?
  └─ SIM → /domain.change --kind evolution → /domain.flow {NN}

Só repo/doc MUDOU?
  └─ SIM → /domain.scan  (ou /domain.change se quiser registrar P-n/E-n)

Não sabe onde está?
  └─ /domain.status {p}
```

Design tático / integração técnica → **arch-kit**, não domain-kit.

---

## Cenários — produtos antigos

### A — Produto novo (greenfield)

Ver pipeline acima. Plan mode em cada artefato.

### B — Sistema legado em produção

```text
/domain.init legado --initiative X
/domain.discover legado --mode as-is-first
  → regras atuais (fluxogramas) + UL + BCs mínimos
/domain.flow 01 …
/domain.model --finalize
/arch.route                        → tático + database-model no arch-kit
```

### C — Produto já no hub, nunca passou pelo domain-kit

```text
/domain.init produto-existente --adopt
/domain.status                     → gaps por fase
/domain.discover --mode minimal    → preenche Estratégico
/domain.flow …
/domain.model --finalize
```

### D — Evolução pós-Operacional

| Necessidade | Comando |
| --- | --- |
| Abrir sessão | `/domain.change` |
| Doc/repo mudou | `/domain.scan` |
| Nova jornada | `/domain.flow {NN}` |
| Nova regra / lacuna | `/domain.change` → discover/decision |
| Revalidar fase | `/domain.model --finalize` |
| Implementação | `/arch.route` / arch commands |

**Não rerodar** discover completo salvo redefinição de domínio.

---

## Modos de `/domain.discover`

| Modo | Quando |
| --- | --- |
| `full` (default) | Produto novo — sequência completa |
| `minimal` | CRUD simples, 1 BC — prioriza estratégico + contexts |
| `as-is-first` | Legado — prioriza regras atuais |
| `incremental` | Delta de escopo / BC |

---

## Fases — o que significam na prática

| Fase | Após | Critério resumido |
| --- | --- | --- |
| **Evidências** | `/domain.init` | sources.yml + scan (manifest ou skip) |
| **Estratégico** | discover contexts | design estratégico + desafio + BCs + UL |
| **Descoberta** | stories / ES | event-storming **ou** domain-storytelling |
| **Operacional** | flow + model --finalize | ≥1 fluxo ready + NFR + registry |

Validação: `.domain/scripts/validate_gate.py --phase operacional --product {p} --suggest`

Aliases: `--gate G0|G1|G2` ainda funcionam. Definição: [references/gates.yml](references/gates.yml).

---

## Confusões comuns

| Confusão | Realidade |
| --- | --- |
| `init` = só índices | **Não** — inclui primeiro scan + síntese (Evidências) |
| `install` = init | **Não** — install = hub; init = produto |
| `scan` = discover | **Não** — scan = fontes; discover = negócio |
| Preciso de capability para fechar | **Não** — tático é arch-kit; Operacional = fluxos negócio + NFR |
| Fluxos em `02-capabilities/` | **Legado** — novos em `01-product/03-operacional/fluxos/` |
| `model` faz integração ACL | **Não** — integração técnica → `arch/01-integration/` |

---

## Diagrama — camadas de comando

```mermaid
flowchart TB
  subgraph hub [Hub — 1x]
    INS["/domain.install"]
  end
  subgraph product [Produto]
    INI["/domain.init\nEvidências"]
    SCN["/domain.scan"]
    CHG["/domain.change"]
    DIS["/domain.discover\nEstratégico + Descoberta"]
    FL["/domain.flow"]
    DEC["/domain.decision"]
    MOD["/domain.model --finalize\nOperacional"]
    STA["/domain.status"]
  end
  INS --> INI
  INI --> DIS
  SCN -.-> INI
  CHG --> DIS
  CHG --> FL
  CHG --> MOD
  DIS --> FL
  FL --> MOD
  DEC --> MOD
  MOD --> ARCH["/arch.route"]
  STA -.-> INI
  STA -.-> DIS
  STA -.-> MOD
```

---

## Mais leitura

- [GUIDE.md](GUIDE.md) · [ONBOARDING.md](ONBOARDING.md)
- [references/discovery-workflow.md](references/discovery-workflow.md)
- [references/pipeline.md](references/pipeline.md)
- [wrappers/README.md](wrappers/README.md) · [skills/README.md](skills/README.md)
