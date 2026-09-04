---
name: domain-install
description: Instala domain-kit no architecture-hub — skills, scripts, MCPs (1x por hub).
---

## Explain to user

Vou instalar scripts, templates, comandos `domain-*` e **skills DDD bundled** no hub, e checar MCPs (GitHub, PlantUML).

O kit é autossuficiente: know-how fica em `.domain/skills/` (não depende de `~/.cursor/skills/` pessoais).

Próximo passo típico: **`/domain.init {produto}`** — bootstrap do produto + primeiro scan (fase Evidências).

## Steps

1. Rodar `bash {work-kit-root}/domain-kit/scripts/install-domain-kit.sh {hub_root}`  
   (`work-kit-root` = clone ou `../work-kit` no monorepo work-hub)
2. Confirmar `.domain/skills/` e `.domain/wrappers/` presentes.
3. Reportar `.domain/mcp-status.json` — MCPs recomendados e fallbacks manuais.
4. Apontar [ONBOARDING.md](../../ONBOARDING.md) e [COMMAND-GUIDE.md](../../COMMAND-GUIDE.md).
5. Handoff: **`/domain.init {produto}`**

**Não entrega:** nenhum artefato de produto — só infraestrutura do framework no hub.
