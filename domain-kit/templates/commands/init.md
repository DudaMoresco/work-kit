---
name: domain-init
description: Bootstrap do produto — índices + scan (Evidências) + síntese de evidências; opcional --adopt.
---

## Explain to user

Vou criar os índices do produto, conduzir o **primeiro scan de fontes** (wizard + leitura + curadoria) e fechar com a **síntese do que foi achado** — tudo nesta sessão. **Mostro rascunhos antes de gravar** (arquivos em `.draft/` + aba **Rascunhos** no `dashboard.html`). Ao promover, **registro entrada no CHANGELOG** do produto.

Com `--adopt`: produto já existe no hub — gero índices faltantes, inventário de gaps e status atual **sem recriar conteúdo**. Se fase **Evidências** já PASS mas falta síntese, rodo só a Fase 0c.

Próximo passo após init completo: **`/domain.discover`** (lacunas de negócio + DDD).

Contrato: [plan-mode.md](../../references/plan-mode.md)

## User Input

```text
$ARGUMENTS
```

Flags: `--initiative {i}`, `--adopt`

## Plan mode (obrigatório para conteúdo)

1. Rascunhos em `products/{p}/.draft/` + preview no chat.
2. **Aguardar** confirmação antes de promote para path canônico.
3. Scaffolding (índices vazios) pode gravar direto; scan/manifest/síntese exigem OK.
4. **Visibilidade** — após índices e **cada lote de rascunhos**: [visibility-checkpoint.md](../../templates/clarify/visibility-checkpoint.md) + `sync_product_workspace.py`.

## Steps

1. Parse `{produto}`, opcional `--initiative {i}`, `--adopt`.
2. Confirmar path hub (argumento ou cwd).
3. **Workspace** — após criar/confirmar pasta do produto: `.domain/scripts/sync_product_workspace.py --hub {hub} --product {p}` (scaffold `.draft/` + 1º dashboard).

### Branch A — `--adopt` (produto já no hub)

1. Rodar `.domain/scripts/adopt_product.py --hub {hub} --product {p}`.
2. Reportar gaps por fase (Evidências → Estratégico → Descoberta → Operacional), índices criados/atualizados, próximo comando sugerido.
3. **Não** rodar fase 0 de scan se fase **Evidências** já PASS — handoff conforme gaps.
4. Se Evidências ok mas `01-product/00-scan/sintese-evidencias.md` ausente → rodar **Fase 0c** (síntese a partir do manifest existente).
5. Pular para passo 16 (sync + dashboard) se adopt completou sem scan nem síntese pendente.

### Branch B — produto novo (default)

3. Copiar templates de `domain-kit/templates/` (se ausentes):
   - `sources.yml`, `flows-registry.yml`, `domain-status.json`, `product-README.md`, `CHANGELOG.md` → `products/{produto}/`
   - Substituir `{produto}`, `{iniciativa}` nos templates.
4. Criar **somente** `05-decisoes/produto.md` (stub) e `01-product/02-domain/evolucoes.md` (via template) se ausentes.
5. `product-README.md` permanece stub até discover `--stage contexts` ou preenchimento manual.

### Fase 0 — Primeiro scan (pré-fase Evidências)

6. **Plan fontes** — se `sources.yml` vazio: [scan-discover.md](../../templates/clarify/scan-discover.md), auto-detect, `AskQuestion`, draft `sources.yml` em `.draft/`
7. **Execute** — ler fontes confirmadas; draft `scan-manifest.json` + `01-product/00-scan/README.md` em `.draft/`
8. **Sync visibilidade** — após gravar rascunhos: `sync_product_workspace.py --register` para cada par draft→target; exibir bloco de visibilidade no chat
9. **Curadoria inline** — [scan.md](../../templates/clarify/scan.md): por finding, incorporar/ignorar/pendente; preview; OK → promote manifest + sources
10. Scan vazio intencional → documentar motivo; promote `domain-status.json` com `scan: skipped` após OK.
11. **Sync** — `sync_product_workspace.py` após promote da fase 0

### Fase 0c — Síntese de evidências (0a)

12. [findings-brief.md](../../templates/clarify/findings-brief.md) — exibir `## Síntese do que já sabemos`; aguardar confirmação do usuário.
13. Draft/promote `01-product/00-scan/sintese-evidencias.md`; atualizar `domain-status.json`: `discover.evidenceBrief = complete`.
14. **Changelog** — após promotes das fases 0 e/ou 0c: [changelog.md](../../templates/clarify/changelog.md) → append em `CHANGELOG.md` (scan + síntese se aplicável); exibir no checkpoint.
15. **Sync** — `sync_product_workspace.py` após promote da síntese

### Validação e finalização

16. Validar fase Evidências via `validate_gate.py --phase evidencias --product {p}`.
17. `sync_product_workspace.py` (dashboard final) + bloco de visibilidade
18. Handoff: **`/domain.discover`** (Evidências + síntese ok) ou gaps listados se `--adopt`

**Não entrega:** perguntas de lacuna (0b), design estratégico, BCs, fluxos, tático — lacunas e DDD são `/domain.discover`; modelagem é `/domain.model`.

**Não** invocar skills DDD neste comando (exceto wrappers de scan via fase 0).
