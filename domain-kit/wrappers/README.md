# Wrappers de skills — domain-kit

## Regra

**Nunca editar** a skill original em `~/.cursor/skills/{nome}/SKILL.md` ou `skills/{nome}/SKILL.md`.

Este diretório contém **contratos de invocação** para o domain-kit: pré-condições, paths no hub, comando que chama, handoff pós-execução.

O agente deve:

1. Ler o **wrapper** quando executar um comando `domain-*`
2. Ler a **skill original** read-only para know-how DDD completo
3. Gravar artefatos apenas nos paths indicados no wrapper

---

## Índice

| Wrapper | Skill original | Comandos |
| --- | --- | --- |
| [ddd-design-estrategico.md](ddd-design-estrategico.md) | `ddd-design-estrategico` | discover |
| [domain-storytelling.md](domain-storytelling.md) | `domain-storytelling` | discover |
| [event-storming.md](event-storming.md) | `event-storming` | discover, flow |
| [event-storming-to-scenario-tables.md](event-storming-to-scenario-tables.md) | `event-storming-to-scenario-tables` | discover |
| [ddd-linguagem-e-contextos.md](ddd-linguagem-e-contextos.md) | `ddd-linguagem-e-contextos` | discover |
| [ddd-integracao-contextos.md](ddd-integracao-contextos.md) | `ddd-integracao-contextos` | model |
| [ddd-design-tatico.md](ddd-design-tatico.md) | `ddd-design-tatico` | model, capability |
| [levantamento-requisitos.md](levantamento-requisitos.md) | `levantamento-requisitos` | model |
| [fluxos-entregaveis.md](fluxos-entregaveis.md) | `fluxogramas-decisao` / fluxos | flow, model |
| [scan-github.md](scan-github.md) | MCP user-github | discover (fase 0), scan (re-sync) |
| [scan-gitlab.md](scan-gitlab.md) | glab / dalvito / manual | discover (fase 0), scan (re-sync) |
| [scan-confluence.md](scan-confluence.md) | imports / futuro MCP | discover (fase 0), scan (re-sync) |

---

## Template para novo wrapper

```markdown
# Wrapper: {nome}

**Skill original:** `~/.cursor/skills/{nome}/SKILL.md` — NÃO editar.

**Invocada por:** `/domain.{comando}`

**Pré-condições:** {gates, paths}

**Inputs:** {lista}

**Outputs no hub:** {paths relativos a products/{produto}/}

**Pós-execução:** atualizar domain-status.json; regenerate dashboard
```
