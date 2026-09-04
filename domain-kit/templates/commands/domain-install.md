---
name: domain-install
description: Instala domain-kit no architecture-hub — skills, scripts, MCPs (1x por hub).
---

## Explain to user

Vou instalar scripts, templates e comandos `domain-*` no hub e checar MCPs (GitHub, PlantUML). Skills DDD originais **não** serão alteradas.

Próximo passo típico: **`/domain.init {produto}`** — bootstrap do produto + primeiro scan (fase Evidências).

## Steps

1. Rodar `bash {work-kit-root}/domain-kit/scripts/install-domain-kit.sh {hub_root}`  
   (`work-kit-root` = clone ou `../work-kit` no monorepo work-hub)
2. Reportar `.domain/mcp-status.json` — MCPs recomendados e fallbacks manuais.
3. Apontar [ONBOARDING.md](../../ONBOARDING.md) e [COMMAND-GUIDE.md](../../COMMAND-GUIDE.md).
4. Handoff: **`/domain.init {produto}`**

**Não entrega:** nenhum artefato de produto — só infraestrutura do framework no hub.
