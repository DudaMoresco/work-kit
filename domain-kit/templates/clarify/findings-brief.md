> Roteiro **interno** — fase 0c de `/domain.init` (e refresh em `/domain.scan`). Não invocar `/domain.clarify`.

Consolida o que foi achado no scan/enunciado **antes** do discover. O usuário precisa **ver o que já sabemos**; perguntas de lacuna (0b) ficam para `/domain.discover`.

## Entrada

- `01-product/00-scan/scan-manifest.json` (findings curados: incorporar / ignorar / pendente)
- `initiatives/{i}/01-enunciado.md` ou narrativa já dada no chat
- Artefatos canônicos já promovidos (se re-sync ou adopt)

## Saída

1. **Preview no chat** — seção fixa `## Síntese do que já sabemos`
2. **Draft opcional** — `01-product/00-scan/sintese-evidencias.md` em `.draft/` se o resumo for longo
3. Após OK do usuário → promote `sintese-evidencias.md`; `discover.evidenceBrief = complete` em `domain-status.json`

## Formato da síntese (chat)

```markdown
## Síntese do que já sabemos

### Fontes consultadas
| Fonte | O que trouxe |
| --- | --- |
| … | … |

### Fatos incorporados (com evidência)
- … — `source`, path/url

### Hipóteses / inferências (não confirmadas)
- …

### Ignorado no scan (e por quê)
- …

### Lacunas — o que ainda não sabemos
- …
```

**Regra:** fatos vêm do manifest/enunciado; **não inventar**. Lacunas serão tratadas em `/domain.discover` (fase 0b).

## Checkpoint

Após exibir a síntese:

- Perguntar: *"A síntese está correta? Algo importante faltou?"*
- Após confirmação → promote e encerrar init (ou scan, se re-sync).
- **Não** fazer perguntas de lacuna aqui — isso é fase 0b do discover.

## Quando pular

- Manifest vazio **e** sem enunciado/narrativa → avisar que não há base; pedir enunciado ou fontes antes de síntese.
- `sintese-evidencias.md` promovido e scan inalterado desde então → no scan re-sync, atualizar só se findings mudaram materialmente; no discover, reexibir resumo curto (5–10 linhas) se útil.

## Recovery legado

Se produto foi iniciado antes da síntese no init: `/domain.discover --stage brief` ou `/domain.init {p} --adopt` (Fase 0c).
