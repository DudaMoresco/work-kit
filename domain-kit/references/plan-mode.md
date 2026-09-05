# Plan mode — contrato de gravação

Todo **conteúdo de domínio** é produzido em modo **Plan** antes de entrar no hub. O usuário não precisa lembrar de comandos extras (`clarify`, `scan` separado) — perguntas e previews fazem parte do comando que está rodando.

---

## Princípio

```text
Propor → Exibir (chat e/ou .draft/) → Aguardar OK → Promover para path canônico
```

Frases de confirmação: `pode gravar`, `pode scanear`, `ok`, `aprovar`, `confirmo`.

---

## O que usa Plan mode

| Tipo | Exemplos | Grava direto? |
| --- | --- | --- |
| **Scaffolding** | Pastas vazias, `domain.init` índices vazios | Sim |
| **Conteúdo** | MD de discover/model/flow, D-n, registry updates | **Não** — Plan first |
| **Fontes** | `sources.yml`, findings incorporados | **Não** — Plan first |
| **Índices mutáveis** | `flows-registry.yml`, `domain-status.json` | Plan first quando alteração reflete conteúdo novo |

---

## Onde ficam os rascunhos

```text
products/{produto}/.draft/
├── README.md              ← explica que não é canônico
├── manifest.json          ← lista de pending promotes
└── {mirror-path}          ← espelha path final, ex.:
    01-product/01-vision/01-design-estrategico.md
    sources.yml
```

**Preferência de exibição:**

1. **Chat** — preview markdown completo ou resumo + link para `.draft/`
2. **Arquivo** — gravar em `.draft/{path}` para diff no editor
3. **Ambos** — recomendado para artefatos longos

**Proibido:** gravar em path canônico (`01-product/`, `05-decisoes/` conteúdo novo) sem OK explícito nesta sessão.

---

## manifest.json (draft)

```json
{
  "product": "{produto}",
  "updatedAt": "ISO-8601",
  "pending": [
    {
      "draftPath": ".draft/01-product/01-vision/01-design-estrategico.md",
      "targetPath": "01-product/01-vision/01-design-estrategico.md",
      "command": "domain.discover",
      "status": "awaiting_approval"
    }
  ]
}
```

Após OK: promover (copiar draft → target, remover entrada, apagar draft file).

Script helper: `.domain/scripts/promote_draft.py`

---

## Perguntas inline (ex-clarify)

Roteiros em `templates/clarify/*.md` são **bancos de prompts internos** — o comando ativo carrega e aplica, **sem** invocar `/domain.clarify`.

| Roteiro | Usado por |
| --- | --- |
| `findings-brief.md` | init fase 0c + refresh no scan |
| `scan-discover.md` | init fase 0, scan re-sync |
| `scan.md` | curadoria de findings (inline) |
| `discover.md` | discover fase 0b — perguntas de lacuna |
| `flow.md` | `/domain.flow` |
| `changelog.md` | entrada em `CHANGELOG.md` após scan ou mudança significativa |
| `visibility-checkpoint.md` | dashboard + `.draft/` após rascunhos/promote |
| `bc` prompts | `/domain.capability` |

Máximo **3 perguntas por turno**; registrar pendências em `abertos.md` (também via Plan mode).

---

## Fluxo por comando

### `/domain.init`

1. Fase 0: fontes + manifest + curadoria
2. Fase 0c: **síntese de evidências** (`findings-brief.md`) — confirmar com usuário; promote `sintese-evidencias.md`
3. **Sync visibilidade** após cada lote de rascunhos e após promotes (`sync_product_workspace.py`)
4. Validar fase Evidências; handoff `/domain.discover`

### `/domain.discover`

1. Pré-condição: `sintese-evidencias.md` promovido (senão handoff init)
2. Fase 0b: perguntas de **lacuna** (`discover.md`) — máx. 3/turno
3. **Um estágio DDD por sessão** (`--stage`); cada artefato: preview → `.draft/` → OK → promote
4. Checkpoint ao fim da sessão — sugerir próximo `--stage` ou `/domain.status`
5. `abertos.md`: promote após OK

### `/domain.flow`, `/domain.capability`, `/domain.model`, `/domain.decision`

Mesmo contrato: perguntas inline se ambíguo → preview → OK → promote.

### `/domain.scan` (re-sync)

Plan + Execute + curadoria **na mesma sessão**; refresh `sintese-evidencias.md` se manifest mudou; manifest em `.draft/` até OK; **changelog obrigatório** após promote ([changelog.md](../templates/clarify/changelog.md)).

---

## Changelog do produto

Path: `products/{p}/CHANGELOG.md`

- **Obrigatório** após todo scan e toda mudança significativa promovida
- Append **após promote** (resumo do que foi aprovado); exibir no checkpoint da sessão
- Roteiro: [templates/clarify/changelog.md](../templates/clarify/changelog.md)
- Não registrar: só drafts, typos, regenerate dashboard sem mudança canônica

## `/domain.clarify` — deprecado para usuários

Não documentar como passo do pipeline. Mantido só como skill técnica legada ou alias que redireciona: *"Use o comando principal (`discover`, `flow`, …) — clarify está inline."*

---

## Dashboard e gates

- Dashboard lê **paths canônicos** — drafts não contam como progresso
- Gate só passa com arquivos promovidos
- **Regenerar dashboard** após promote **e** após criar/atualizar rascunhos em `.draft/` — use `sync_product_workspace.py` (init/scan/discover)
- Dashboard: aba **Rascunhos** lê `.draft/manifest.json` e arquivos em `.draft/`; **CHANGELOG.md** na aba Artefatos
