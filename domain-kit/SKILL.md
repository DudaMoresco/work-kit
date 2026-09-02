---
name: domain-kit
description: >-
  Orquestra mapeamento de negócio no architecture-hub: init, scan, clarify,
  discover, model, flow por fluxo. Use for domain mapping, DDD, bounded contexts.
disable-model-invocation: true
---

# Domain-Kit

Framework para **negócio → domínio** no architecture-hub.

- [GUIDE.md](GUIDE.md) — usuário
- [ONBOARDING.md](ONBOARDING.md) — setup
- [HOW-IT-WORKS.md](HOW-IT-WORKS.md) — internals
- [wrappers/](wrappers/) — contratos (**não editar** skills DDD originais)

## Comandos

| Camada | Comando |
| --- | --- |
| Meta | `workkit.init`, `domain.init`, `domain.scan`, `domain.clarify`, `domain.status` |
| Macro | `domain.discover`, `domain.model --finalize` |
| Micro | `domain.flow`, `domain.capability`, `domain.decision` |

## Regras

1. Ler **wrapper**; skill original read-only
2. **Clarify** + confirmar antes de gravar
3. **Scan** cita fontes; GitHub MCP / GitLab-Confluence fallback manual
4. Regenerar dashboard após mudanças

Instalação: `bash domain-kit/scripts/install-domain-kit.sh {hub}`
