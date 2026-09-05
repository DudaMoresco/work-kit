# {nome_legivel}

> Cartão do produto — visão PM + índice de artefatos do domain-kit.
> Atualizado: {updated_at}

## Visão geral

> **Por que esta seção:** resume o produto em uma tela para onboarding de PM/negócio.

- **O que é:** {o_que_e}
- **Problema que resolve:** {problema}
- **Onde está disponível:** {onde_disponivel}

## Principais benefícios

> **Por que esta seção:** deixa explícito valor para usuário, negócio e operação — alinha expectativa antes dos artefatos.

### Para o usuário

- {beneficio_usuario_1}

### Para o negócio

- {beneficio_negocio_1}

### Para operações / fluxos

- {beneficio_operacoes_1}

## Status do domain-kit

> **Por que esta seção:** mostra fase atual e próximo passo sem abrir o dashboard.

| Fase | Status | Próximo passo |
| --- | --- | --- |
| Evidências | {fase_evidencias} | {passo_evidencias} |
| Estratégico | {fase_estrategico} | {passo_estrategico} |
| Descoberta | {fase_descoberta} | {passo_descoberta} |
| Operacional | {fase_operacional} | {passo_operacional} |

Fase atual: **{phase}** · [Dashboard](dashboard.html)

## Sessão ativa

> **Por que esta seção:** aponta a mudança/draft em andamento para continuidade da sessão.

{active_change_section}

## Índice de artefatos

> **Por que esta seção:** mapa rápido dos paths canônicos do produto (hub-paths).

### Evidências

- [Síntese de evidências](01-product/00-scan/sintese-evidencias.md)
- [Manifest de scan](01-product/00-scan/scan-manifest.json)
- [Fontes](sources.yml)

### Estratégico

- [Design estratégico](01-product/01-vision/01-design-estrategico.md)
- [Desafio de negócio](01-product/02-domain/desafio-negocio.md)
- [Bounded contexts](01-product/02-domain/bounded-contexts.md)
- [Linguagem ubíqua](01-product/02-domain/linguagem-ubiqua.md)

### Descoberta

- [Domain stories](01-product/03-discovery/02-domain-storytelling/)
- [Event storming](01-product/03-discovery/01-event-storming/)

### Operacional

- [Fluxos de negócio](01-product/04-operacional/fluxos/)
- [Requisitos NFR](01-product/04-operacional/requisitos.md)
- [Registry de decisões](05-decisoes/produto.md)
- [Catálogo de fluxos](flows-registry.yml)

## Problemas e evoluções em aberto

> **Por que esta seção:** superfície P-n/E-n no cartão; detalhe vive em `02-domain/`.

### Problemas (P-n)

Ver inventário completo em [abertos.md](01-product/02-domain/abertos.md).

{problemas_abertos_resumo}

### Evoluções (E-n)

Ver inventário completo em [evolucoes.md](01-product/02-domain/evolucoes.md).

{evolucoes_abertas_resumo}

## Changelog recente

> **Por que esta seção:** histórico curto de mudanças de produto/docs sem abrir o CHANGELOG inteiro.

Ver [CHANGELOG.md](CHANGELOG.md).
