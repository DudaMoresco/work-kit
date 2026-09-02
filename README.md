# Work-Kit — três kits, um monorepo

Design do framework estilo spec-kit para **mapeamento de negócio → arquitetura → backlog**.

Monorepo canônico (hoje): [`architecture-hub`](../architecture-hub) (vizinho neste monorepo `work-hub`).  
Implementação (downstream): spec-kit em repositórios de código (ex.: `oficina-backend`).

Pacote raiz: **`work-kit/`** (este diretório). Subpacotes: `domain-kit/`, futuro `arch-kit/`, `delivery-kit/`.

## Três kits lógicos

| Kit | Papel | Pastas no hub | Comandos (propostos) |
| --- | --- | --- | --- |
| **[domain-kit](domain-kit/)** | Descobrir e modelar negócio | `01-product/`, `02-capabilities/` | `/domain.discover`, `/domain.model` |
| **arch-kit** | Decidir e documentar solução técnica | `04-platform/`, `03-registry/plataforma.md` | `/arch.route`, `/arch.architect` |
| **delivery-kit** | Quebrar em Tech Stories + handoff spec-kit | `initiatives/*/03-backlog/` | `/delivery.backlog`, `/delivery.handoff` |

**Transversal:** `03-registry/` (D-n), `_conventions/`, snapshots da iniciativa.

## Pipeline

```text
domain-kit → arch-kit → delivery-kit → spec-kit → código
```

Detalhe de gates e handoffs: [references/handoffs.md](references/handoffs.md).

## Status

- [x] Design de handoffs (oficina-mecanica como fixture)
- [x] **domain-kit** implementado ([domain-kit/README.md](domain-kit/README.md))
- [ ] arch-kit / delivery-kit especificados
- [x] Comandos, templates, scripts, dashboard, retrofit oficina

## Instalação

```bash
# Clone (qualquer pasta)
git clone https://github.com/DudaMoresco/work-kit.git
cd work-kit

# Instalar no architecture-hub
bash domain-kit/scripts/install-domain-kit.sh /path/to/architecture-hub
```

No monorepo `work-hub`: `architecture-hub` e `work-kit` são pastas irmãs.

Comando Cursor: `/workkit.init`

- [estagios-desenvolvimento.md](../skills/estagios-desenvolvimento.md) — pipeline completo de skills
- [references/hub-paths.md](../skills/references/hub-paths.md) — paths canônicos
- [spec-kit-dashboard](../skills/spec-kit-dashboard/) — downstream implementação
