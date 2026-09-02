# Wrapper: scan-gitlab

**Skill original:** N/A — GitLab via CLI/API ou import manual

**Invocada por:** `/domain.scan`

**Opções (ordem):**
1. `glab api` / REST se token configurado
2. [`dalvito-cli`](../../dalvito-cli/SKILL.md) em ambiente corporativo ECS
3. **Fallback:** arquivos em `00-scan/imports/gitlab/`

**Pré-condições:** entradas `gitlab:` em `sources.yml`

**Contrato de saída:** igual scan-github → `scan-manifest.json` com `source: gitlab`

**Nunca** afirmar conteúdo não lido — citar project path ou arquivo local
