# Wrappers de skills — domain-kit

## Regra

Skills de know-how vivem **dentro do kit** em [`../skills/`](../skills/) (e, após install, em `.domain/skills/`).

Este diretório contém **contratos de invocação**: pré-condições, paths no hub, comando que chama, handoff pós-execução.

O agente deve:

1. Ler o **wrapper** quando executar um comando `domain-*`
2. Ler a **skill bundled** em `skills/{nome}/SKILL.md` (ou `.domain/skills/{nome}/SKILL.md` no hub)
3. Gravar artefatos apenas nos paths indicados no wrapper

---

## Índice

| Wrapper | Skill bundled | Comandos |
| --- | --- | --- |
| [ddd-design-estrategico.md](ddd-design-estrategico.md) | `skills/ddd-design-estrategico` | discover |
| [domain-storytelling.md](domain-storytelling.md) | `skills/domain-storytelling` | discover |
| [event-storming.md](event-storming.md) | `skills/event-storming` | discover, flow |
| [event-storming-to-scenario-tables.md](event-storming-to-scenario-tables.md) | `skills/event-storming-to-scenario-tables` | discover |
| [ddd-linguagem-e-contextos.md](ddd-linguagem-e-contextos.md) | `skills/ddd-linguagem-e-contextos` | discover |
| [ddd-integracao-contextos.md](ddd-integracao-contextos.md) | `skills/ddd-integracao-contextos` (arch) | arch-kit |
| [ddd-design-tatico.md](ddd-design-tatico.md) | `skills/ddd-design-tatico` (arch) | arch-kit |
| [levantamento-requisitos.md](levantamento-requisitos.md) | `skills/levantamento-requisitos` | model |
| [fluxos-entregaveis.md](fluxos-entregaveis.md) | `skills/fluxos-entregaveis` + `fluxogramas-decisao` | flow, discover as-is |
| [scan-github.md](scan-github.md) | MCP user-github | init, scan |
| [scan-gitlab.md](scan-gitlab.md) | glab / import | init, scan |
| [scan-confluence.md](scan-confluence.md) | imports / futuro MCP | init, scan |

---

## Template para novo wrapper

```markdown
# Wrapper: {nome}

**Skill:** `skills/{nome}/SKILL.md` (bundled no domain-kit).

**Invocada por:** `/domain.{comando}`

**Pré-condições:** {gates, paths}

**Inputs:** {lista}

**Outputs no hub:** {paths relativos a products/{produto}/}

**Pós-execução:** atualizar domain-status.json; regenerate dashboard
```
