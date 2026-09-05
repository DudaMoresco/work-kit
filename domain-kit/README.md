# Domain-Kit

Framework para **mapeamento de negócio → domínio** em um hub de produtos (ex.: pasta raiz onde vivem `products/`).

**Autossuficiente:** know-how DDD em [`skills/`](skills/) — não depende de `~/.cursor/skills/` pessoais.

Documentação: [COMMAND-GUIDE.md](COMMAND-GUIDE.md) · [GUIDE.md](GUIDE.md) · [ONBOARDING.md](ONBOARDING.md) · [INVENTORY.md](INVENTORY.md)

## Comandos

| Camada | Comando |
| --- | --- |
| Hub | `domain.install` |
| Meta | `domain.init`, `domain.scan`, `domain.status`, `domain.change` |
| Macro | `domain.discover`, `domain.model` |
| Micro | `domain.flow`, `domain.decision` |

`domain.capability` está **fora do escopo do domain-kit**.

## Pipeline — produto novo

```text
domain.install → domain.init (Evidências) → domain.discover (Estratégico + Descoberta)
  → domain.flow 01…NN → domain.model --finalize (Operacional)
```

Após **Operacional**, a próxima etapa técnica fica **fora do escopo do domain-kit**.

Produtos antigos / evoluções: [COMMAND-GUIDE.md](COMMAND-GUIDE.md) · `/domain.change`

## Instalação

```bash
bash domain-kit/scripts/install-domain-kit.sh /caminho/do/hub
```

O hub é a raiz do diretório de produtos (ex.: `architecture-hub` se esse for o nome da pasta no seu ambiente).

Instala em `.domain/skills/`, `.domain/wrappers/`, scripts e comandos `/domain.*`.

Comando Cursor: `/domain.install`

## Sandbox local

```bash
bash domain-kit/scripts/bootstrap-test-hub.sh
```

Ver [test-hub/README.md](test-hub/README.md).
