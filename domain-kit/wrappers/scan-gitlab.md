# Wrapper: scan-gitlab

**Skill original:** N/A — GitLab via CLI/API ou import manual

**Invocada por:** `/domain.discover` (fase 0), `/domain.scan` (re-sync opcional)

**Opções (ordem):**
1. `glab api` / REST se token configurado
2. CLI corporativa (ex.: dalvito) em ambiente ECS, se disponível
3. **Fallback:** arquivos em `00-scan/imports/gitlab/`

**Pré-condições:** entradas `gitlab:` em `sources.yml`

**Contrato de saída:** igual scan-github → `scan-manifest.json` com `source: gitlab`

**Nunca** afirmar conteúdo não lido — citar project path ou arquivo local
