# Domain-kit — pacote de alterações (2026-09-03)

## Resumo

Redesenho do core: fases Evidências → Estratégico → Descoberta → Operacional (substituem G0/G1/G2), cartão central product-README.md, comando /domain.change para sessões evolutivas (P-n / E-n).

## Conteúdo do zip

### Framework (.domain/)
- Scripts: validate_gate.py, generate_domain_dashboard.py, adopt_product.py
- Templates: product-README.md, evolucoes.md, evolucao.md, fluxo-operacional.md, domain-status.json
- Clarify: change.md, evolucao.md, changelog.md
- Wrappers: arch-kit redirect, integração duas camadas, fluxos híbridos

### Skills (.cursor/skills/domain-*)
- Novo: domain-change
- Atualizados: kit, init, discover, model, flow, status, install, clarify, capability (deprecated)

### Produto exemplo (notificacao-dividas-pendencias)
Referência de migração: product-README.md, evolucoes.md, integração fatiada, domain-status.json

## Como aplicar
1. Extrair na raiz do hub preservando paths
2. adopt_product.py --hub . --product {slug}
3. generate_domain_dashboard.py --hub . --product {slug}
