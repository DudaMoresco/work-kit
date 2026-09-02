---
name: domain-scan
description: Scan de fontes externas (GitHub, GitLab, Confluence) para products/{produto}/sources.yml.
---

## Explain to user

Vou ler as fontes em `sources.yml` (GitHub via MCP quando disponível; GitLab/Confluence via CLI ou pasta imports) e gerar um manifesto em `00-scan/` para você revisar. Nenhum conteúdo entra no domínio sem `/domain.clarify scan`.

## User Input

```text
$ARGUMENTS
```

## Steps

1. Resolver `{produto}` — cwd ou argumento.
2. Ler `products/{produto}/sources.yml`. Se vazio → WARN, status `skipped`, sair.
3. Seguir wrappers (read-only skills originais):
   - [scan-github.md](../../wrappers/scan-github.md) — MCP `user-github`
   - [scan-gitlab.md](../../wrappers/scan-gitlab.md)
   - [scan-confluence.md](../../wrappers/scan-confluence.md)
4. Processar `manual:` paths relativos ao hub.
5. Gravar `01-product/00-scan/scan-manifest.json` e `README.md`.
6. Atualizar `domain-status.json`: `scan: complete|partial|skipped`.
7. Regenerar dashboard.
8. Handoff → `/domain.clarify scan`

**Proibido:** inventar conteúdo de repo/wiki não lido.
