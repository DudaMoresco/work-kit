# Domain-Kit

Framework estilo spec-kit para **mapeamento de negócio → domínio** no `architecture-hub`.

**Autossuficiente:** know-how DDD em [`skills/`](skills/) — não depende de `~/.cursor/skills/` pessoais.

Documentação: [COMMAND-GUIDE.md](COMMAND-GUIDE.md) · [GUIDE.md](GUIDE.md) · [ONBOARDING.md](ONBOARDING.md) · [INVENTORY.md](INVENTORY.md)

## Comandos

| Camada | Comando |
| --- | --- |
| Hub | `domain.install` (`workkit.init` deprecado) |
| Meta | `domain.init`, `domain.scan`, `domain.status`, `domain.change` |
| Macro | `domain.discover`, `domain.model` |
| Micro | `domain.flow`, `domain.decision` (`domain.capability` → arch-kit) |

## Pipeline — produto novo

```text
domain.install → domain.init (Evidências) → domain.discover (Estratégico + Descoberta)
  → domain.flow 01…NN → domain.model --finalize (Operacional)
  → arch-kit
```

Produtos antigos / evoluções: [COMMAND-GUIDE.md](COMMAND-GUIDE.md) · `/domain.change`

## Instalação

```bash
bash domain-kit/scripts/install-domain-kit.sh /path/to/architecture-hub
```

Instala em `.domain/skills/`, `.domain/wrappers/`, scripts e comandos `/domain.*`.

Comando Cursor: `/domain.install`

## Sandbox local

```bash
bash domain-kit/scripts/bootstrap-test-hub.sh
```

Ver [test-hub/README.md](test-hub/README.md).
