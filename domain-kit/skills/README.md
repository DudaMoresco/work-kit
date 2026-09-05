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
| `fluxos-entregaveis` | `/domain.flow` (know-how; paths via wrapper → `04-operacional/fluxos/`) |
| `fluxogramas-decisao` | `/domain.discover --mode as-is-first` → `03-discovery/00-as-is/` |

## Fora do escopo

Design tático e integração técnica (camadas, agregados, ACL detalhada) estão **fora do escopo do domain-kit** — não há skill bundled para isso. `/domain.capability` redireciona; próxima etapa técnica fica fora do kit.

## Uso

1. Comando `domain-*` lê o **wrapper** em `wrappers/` (paths do hub).
2. Agente lê a skill em `skills/{nome}/SKILL.md` (ou `.domain/skills/` após install).
3. Artefatos só nos paths do wrapper.

Após `/domain.install`, cópia em `.domain/skills/`.
