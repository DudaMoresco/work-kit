---
name: domain-scan
description: Re-sync de fontes (opcional) — plan mode; curadoria + refresh síntese na mesma sessão.
---

## Explain to user

Atualizo fontes externas quando repos/docs mudaram. **Plan mode:** manifest e sources em `.draft/` até você aprovar. Curadoria de findings **nesta mesma conversa** — sem `/domain.clarify`.

Se o manifest mudou materialmente, **atualizo a síntese de evidências** (`sintese-evidencias.md`) e **registro entrada no CHANGELOG** do produto. Lacunas novas ficam para a próxima sessão de `/domain.discover`.

Contrato: [plan-mode.md](../../references/plan-mode.md)

## User Input

```text
$ARGUMENTS
```

Flags: `--plan`

## Quando usar

| Situação | Comando |
| --- | --- |
| Produto novo — primeiro scan + síntese | `/domain.init` (fases 0 + 0c) |
| Repo/docs mudou depois | **`/domain.scan`** (este) |

## Steps

1. Resolver `{produto}`.
2. **Plan** — se sources vazio ou `--plan`: [scan-discover.md](../../templates/clarify/scan-discover.md) → draft `sources.yml`
3. **Execute** — wrappers scan-* → draft `scan-manifest.json`, `00-scan/README.md`
4. **Curadoria inline** — [scan.md](../../templates/clarify/scan.md); preview; OK → promote manifest + sources
5. **Refresh síntese** — se findings mudaram materialmente: [findings-brief.md](../../templates/clarify/findings-brief.md) → draft/promote `sintese-evidencias.md` (plan mode). **Não** reabrir perguntas de lacuna (0b) — discover trata na próxima sessão.
6. **Changelog** — após promote: [changelog.md](../../templates/clarify/changelog.md) → append em `CHANGELOG.md` (obrigatório em todo scan); exibir no checkpoint.
7. Atualizar `domain-status.json` (via draft + promote)
8. **Sync visibilidade** — `sync_product_workspace.py` + [visibility-checkpoint.md](../../templates/clarify/visibility-checkpoint.md) após rascunhos e após promote

**Proibido:** gravar paths canônicos sem OK; inventar conteúdo não lido.
