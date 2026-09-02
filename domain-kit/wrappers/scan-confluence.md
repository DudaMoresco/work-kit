# Wrapper: scan-confluence

**Skill original:** N/A — import manual ou futuro MCP Confluence

**Invocada por:** `/domain.scan`

**Fluxo padrão hoje:**
1. Usuário exporta páginas → `products/{p}/01-product/00-scan/imports/confluence/`
2. Agente lê HTML/PDF/Markdown exportado
3. Resumo no manifest com `source: confluence`, `path` local

**Pré-condições:** entradas `confluence:` em sources.yml (space, page ids) **ou** imports presentes

**Clarify:** perguntar o que incorporar ao desafio/requisitos/UL
