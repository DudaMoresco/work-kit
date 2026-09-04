# Skills bundled — domain-kit

Know-how DDD e de modelagem **incluído no kit** (repo autossuficiente). Não depende de `~/.cursor/skills/`.

| Skill | Usada por |
| --- | --- |
| `ddd-design-estrategico` | `/domain.discover` (estratégico) |
| `domain-storytelling` | `/domain.discover` (stories) |
| `event-storming` | `/domain.discover`, `/domain.flow` |
| `event-storming-to-scenario-tables` | `/domain.discover` (opcional) |
| `ddd-linguagem-e-contextos` | `/domain.discover` (contexts) |
| `levantamento-requisitos` | `/domain.model` |
| `fluxos-entregaveis` | `/domain.flow` (know-how; paths via wrapper → `03-operacional/fluxos/`) |
| `fluxogramas-decisao` | `/domain.discover --mode as-is-first` |

## Arch-kit (bundled para referência / handoff)

| Skill | Nota |
| --- | --- |
| `ddd-design-tatico` | Preferir arch-kit; `/domain.capability` deprecated |
| `ddd-integracao-contextos` | Detalhe técnico em `arch/01-integration/` |

## Uso

1. Comando `domain-*` lê o **wrapper** em `wrappers/` (paths do hub).
2. Agente lê a skill em `skills/{nome}/SKILL.md` (ou `.domain/skills/` após install).
3. Artefatos só nos paths do wrapper.

Após `/domain.install`, cópia em `.domain/skills/`.
