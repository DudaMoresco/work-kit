---
name: domain-kit
description: >-
  Mapeamento negócio→domínio no hub: plan mode, install/init/discover/model.
  Sem clarify separado.
disable-model-invocation: true
---

# Domain-Kit

- [COMMAND-GUIDE.md](COMMAND-GUIDE.md) · [GUIDE.md](GUIDE.md) · [references/plan-mode.md](references/plan-mode.md)

## Pipeline

```text
domain.install → domain.init (G0 + síntese) → domain.discover (G1) → domain.flow … → domain.model --finalize (G2)
```

## Plan mode (regra #1)

```text
Propor → .draft/ + chat → OK do usuário → path canônico
```

- **Sem `/domain.clarify`** — perguntas inline no comando ativo
- **Scan + síntese (G0)** — fases 0 e 0c de `/domain.init`; `/domain.scan` = re-sync + refresh síntese
- **Changelog obrigatório** — todo scan ou mudança significativa → entrada em `products/{p}/CHANGELOG.md` ([changelog.md](templates/clarify/changelog.md))
- **`/workkit.init`** — deprecado; use `/domain.install`

## Comandos

| Comando | Plan mode |
| --- | --- |
| `domain.init` | Scan + índices draft-first |
| `domain.discover` | DDD draft-first |
| `domain.flow` | Fluxo MD draft-first |
| `domain.capability` | Tático draft-first |
| `domain.model` | Integração / RF draft-first |
| `domain.decision` | D-n draft-first |

Helper: `.domain/scripts/promote_draft.py`, `adopt_product.py`

Instalação: `/domain.install` ou `bash domain-kit/scripts/install-domain-kit.sh {hub}`
