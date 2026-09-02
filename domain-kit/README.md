# Domain-Kit

Framework estilo spec-kit para **mapeamento de negócio → domínio** no `architecture-hub`.

Documentação: [GUIDE.md](GUIDE.md) · Setup: [ONBOARDING.md](ONBOARDING.md) · Internals: [HOW-IT-WORKS.md](HOW-IT-WORKS.md)

## Comandos

| Camada | Comando |
| --- | --- |
| Meta | `workkit.init`, `domain.init`, **`domain.scan`**, `domain.clarify`, `domain.status` |
| Macro | `domain.discover`, `domain.model` |
| Micro | `domain.flow`, `domain.capability`, `domain.decision` |

## Pipeline

```text
workkit.init → domain.init → domain.scan → clarify → discover
  → domain.flow 01…NN → domain.capability → domain.model --finalize
  → dashboard.html → arch-kit
```

## Princípios

- **Wrappers** em [`wrappers/`](wrappers/) — skills DDD originais **não são editadas**
- **Conversa** antes de gravar (`clarify` + confirmação humana)
- **Scan** GitHub/GitLab/Confluence via [`sources.yml`](templates/sources.yml)
- **Dashboard** read-only — [`generate_domain_dashboard.py`](scripts/generate_domain_dashboard.py)

## Instalação

```bash
bash domain-kit/scripts/install-domain-kit.sh /path/to/architecture-hub
```

## Status implementação

- [x] Docs, wrappers, templates, gates
- [x] Scripts dashboard + validate + install
- [x] Command overlays
- [x] Fixture oficina-mecanica
