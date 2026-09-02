# Wrapper: scan-github

**Skill original:** N/A — usa MCP `user-github` (get_file_contents, search_code, list_issues)

**Invocada por:** `/domain.init` (fase 0, G0), `/domain.scan` (re-sync)

**Pré-condições:** `sources.yml` com entradas `github:`; MCP autenticado

**Fluxo:**
1. Para cada `repo` + `paths` em sources.yml
2. `get_file_contents` ou search
3. Append finding em `scan-manifest.json`: `{source, url, path, excerpt, suggested_artifact}`
4. **Não gravar** em artefatos canônicos de domínio sem curadoria — fase 0 de `/domain.init` ou `/domain.scan`

**Outputs:**
- `products/{p}/01-product/00-scan/scan-manifest.json`
- `products/{p}/01-product/00-scan/README.md`

**Fallback se MCP indisente:** status `partial` + ONBOARDING.md
