# Test Hub — sandbox do domain-kit

Ambiente mínimo que **espelha** um `architecture-hub` após `/domain.install` + índices de `/domain.init`.

Use para iterar em skills, wrappers, rules e templates sem tocar no hub real.

## Setup

```bash
bash domain-kit/scripts/bootstrap-test-hub.sh
```

## Abrir no Cursor

```text
File → Open Folder → domain-kit/test-hub
```

## Comandos para testar

| Comando | O que validar |
| --- | --- |
| `/domain.install` | Skills instaladas, mcp-status.json |
| `/domain.init demo-produto` | Scan (G0) + síntese de evidências (Fase 0c) |
| `/domain.status` | Gates, próximo comando sugerido |
| `/domain.discover` | DDD (G1) — pula scan se G0 ok |
| `/domain.scan` | Re-sync de fontes |
| `/domain.init demo-produto --adopt` | Gap report para produto existente |

**Caminho padrão após bootstrap:** `/domain.init demo-produto` → scan do enunciado em `initiatives/demo-iniciativa/` → síntese → `/domain.discover`.

Fonte manual já configurada em `products/demo-produto/sources.yml` — não precisa de GitHub/GitLab para o primeiro teste.

Dashboard: `products/demo-produto/dashboard.html`

## Reset

```bash
bash domain-kit/scripts/bootstrap-test-hub.sh --clean
```
