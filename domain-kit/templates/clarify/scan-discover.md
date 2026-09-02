> Roteiro **interno** — fase 0 de `/domain.init` ou `/domain.scan`. Não invocar `/domain.clarify`.

Roteiro para **fase Plan** de ingestão de fontes. Invocado por:

- **`/domain.init`** fase 0 (primeiro scan)
- **`/domain.scan`** ou **`/domain.scan --plan`** (re-sync)

Não grava artefatos de domínio — só propõe `sources.yml`.

## Quando entrar em Plan

- `sources.yml` sem entradas em nenhum provedor (`github`, `gitlab`, `confluence`, `manual`)
- Usuário passou `--plan` ou pediu para reconfigurar fontes
- Scan anterior foi `skipped` sem motivo documentado

Se `sources.yml` já tem entradas e usuário não pediu `--plan`, ir direto para **Execute** (salvo manifest claramente desatualizado — perguntar).

## Auto-detecção (read-only)

Antes de perguntar, verificar candidatos **sem inventar conteúdo**:

| Candidato | Como detectar |
| --- | --- |
| Enunciado iniciativa | `initiatives/{initiative}/01-enunciado.md` onde `initiative` vem de `sources.yml` ou `domain-status.json` |
| Imports locais | Arquivos em `products/{p}/01-product/00-scan/imports/` (GitLab/Confluence export) |
| GitHub repos | MCP `user-github`: `get_me` + listar repos recentes — **sugerir**, nunca adicionar sem confirmação |

Registrar candidatos detectados no draft; marcar `detected: true` internamente.

## Perguntas (máx. 2–3 por turno)

Usar `AskQuestion` quando possível:

1. **Enunciado / manual local** — incluir paths detectados? (sim / não / adicionar outro path)
2. **GitHub** — quais repos? (lista sugerida + opção Other para `org/repo`)
3. **GitLab / Confluence / outros** — project paths, page ids ou paths manuais adicionais?

Se usuário não tiver nenhuma fonte externa, confirmar explicitamente **scan vazio intencional** antes de `skipped`.

## Draft sources.yml

Apresentar YAML proposto ao usuário. Exemplo mínimo:

```yaml
version: 1
product: "{produto}"
initiative: "{iniciativa}"

sources:
  github: []
  gitlab: []
  confluence: []
  manual:
    - path: initiatives/{iniciativa}/01-enunciado.md
      purpose: enunciado MVP
```

## Confirmação

- **Não gravar** `sources.yml` até confirmação explícita: "pode scanear", "confirmo", aprovação do plano
- Se usuário pedir ajuste, voltar às perguntas (máx. 2–3 por turno)
- Após confirmação → **Execute**

## Handoff Plan → Execute

Quando confirmado:

1. Gravar `products/{p}/sources.yml`
2. Criar `01-product/00-scan/imports/` se necessário
3. Seguir wrappers de scan (GitHub MCP, GitLab, Confluence, manual)
4. Gravar manifest + atualizar status + dashboard
5. **Init:** continuar Fase 0c (síntese via [findings-brief.md](findings-brief.md)) — **não** discover nesta sessão
6. **Scan standalone:** curadoria → refresh síntese se manifest mudou; handoff `/domain.discover` se lacunas/DDD pendentes
