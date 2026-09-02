# Domain-Kit

Framework estilo spec-kit para **mapeamento de negócio → domínio** no `architecture-hub`.

Documentação: [COMMAND-GUIDE.md](COMMAND-GUIDE.md) · [GUIDE.md](GUIDE.md) · [ONBOARDING.md](ONBOARDING.md) · [INVENTORY.md](INVENTORY.md)

## Comandos

| Camada | Comando |
| --- | --- |
| Hub | `domain.install` (`workkit.init` deprecado) |
| Meta | `domain.init`, `domain.scan`, `domain.status` |
| Macro | `domain.discover`, `domain.model` |
| Micro | `domain.flow`, `domain.capability`, `domain.decision` |

## Pipeline — produto novo

```text
domain.install → domain.init (G0) → domain.discover (G1)
  → domain.flow 01…NN → domain.capability → domain.model --finalize (G2)
  → arch-kit
```

Produtos antigos: [COMMAND-GUIDE.md](COMMAND-GUIDE.md)

## Instalação

```bash
bash domain-kit/scripts/install-domain-kit.sh /path/to/architecture-hub
```

Comando Cursor: `/domain.install`

## Sandbox local

```bash
bash domain-kit/scripts/bootstrap-test-hub.sh
```

Ver [test-hub/README.md](test-hub/README.md).
