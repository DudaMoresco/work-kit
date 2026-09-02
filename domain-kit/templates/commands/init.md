---
name: domain-init
description: Inicializa produto no architecture-hub — pastas, sources, flows-registry, dashboard.
---

## Explain to user

Vou criar a estrutura do produto no hub (`01-product/`, `02-capabilities/`, registry, índices) e um dashboard inicial. Em seguida você configura `sources.yml` e roda `/domain.scan`.

## User Input

```text
$ARGUMENTS
```

## Steps

1. Parse `{produto}` e opcional `--initiative {i}` dos argumentos.
2. Confirmar path hub (argumento ou cwd).
3. Copiar templates de `domain-kit/templates/`:
   - `sources.yml`, `flows-registry.yml`, `domain-status.json` → `products/{produto}/`
   - Substituir `{produto}`, `{iniciativa}` nos templates.
4. Criar árvore mínima se ausente: `01-product/`, `02-capabilities/`, `03-registry/produto.md` (stub), `04-platform/01-non-functional/`.
5. `mkdir -p products/{p}/01-product/00-scan/imports`
6. Rodar `.domain/scripts/regenerate_dashboard.sh products/{produto}`
7. Emitir handoff: configure `sources.yml` → `/domain.scan`

**Não** invocar skills DDD neste comando.
