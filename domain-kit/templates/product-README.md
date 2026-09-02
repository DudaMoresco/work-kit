# {produto}

Pipeline domain-kit — **plan mode**: rascunhos em [`.draft/`](.draft/) até você aprovar.

## Próximo passo

Após **`/domain.init`**: scan + síntese de evidências estão no hub.

**`/domain.discover`** — lacunas de negócio e DDD por sessão; grava só após `ok`.

Re-sync: `/domain.scan` (opcional).

## Changelog

Mudanças significativas e scans ficam em [CHANGELOG.md](CHANGELOG.md) (reverse chronological).

## Canônico vs rascunho

| | Onde | Quando |
| --- | --- | --- |
| Rascunho | `.draft/` | Aguardando OK |
| Canônico | `01-product/`, `02-capabilities/`, … | Após promote |

Ver [plan-mode.md](../../domain-kit/references/plan-mode.md) no pacote work-kit.
