---
name: workkit-init
description: "[DEPRECATED] Alias de /domain.install — instala domain-kit no hub."
---

## Explain to user

**Este comando está deprecado.** Use **`/domain.install`** — mesmo efeito, nome alinhado ao domain-kit.

Vou executar a instalação do framework e avisar sobre a migração de nome.

## Steps

1. Avisar: *"Use `/domain.install`. `/workkit.init` será removido em versão futura."*
2. Seguir os steps de [domain-install.md](domain-install.md) — rodar `install-domain-kit.sh`.
3. Reportar `.domain/mcp-status.json`.
4. Handoff: **`/domain.init {produto}`**
