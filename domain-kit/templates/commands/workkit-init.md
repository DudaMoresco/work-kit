---
name: workkit-init
description: Instala work-kit (domain-kit) no architecture-hub e verifica MCPs (workspace init).
---

## Explain to user

Vou instalar scripts, templates e comandos domain-* no hub e checar MCPs (GitHub, PlantUML). Skills DDD originais **não** serão alteradas.

## Steps

1. Rodar `bash {work-kit-root}/domain-kit/scripts/install-domain-kit.sh {hub_root}`  
   (`work-kit-root` = clone ou `../work-kit` no monorepo work-hub)
2. Reportar `.domain/mcp-status.json`.
3. Apontar [ONBOARDING.md](../../ONBOARDING.md) e próximo passo `/domain.init`.
