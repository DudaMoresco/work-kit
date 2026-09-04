# Notificação de Dívidas e Pendências

> Cartão do produto — visão PM + índice de artefatos do domain-kit.
> Atualizado: 2026-09-03

## Visão geral

- **O que é:** Motor proativo do Serasa Premium que avisa assinantes quando há mudança em anotações financeiras do cadastro monitorado (inclusão, exclusão ou remoção de PEFIN, REFIN, protesto, ações, falência, CCF, SPC, etc.).
- **Problema que resolve:** Clientes premium pagam por monitoramento contínuo, mas sem notificação automática só descobrem alterações ao consultar relatório manualmente — o valor percebido do produto cai.
- **Onde está disponível:** Assinantes **PF e PJ premium** — push, e-mail, SMS e central de notificações do app Serasa Premium (somente notificação em tempo real; relatórios e área logada ficam fora do escopo).

## Principais benefícios

### Para o usuário

- Alerta imediato quando uma anotação financeira muda no cadastro monitorado
- Tranparência proativa sem precisar consultar relatório manualmente
- Notificação pelo canal preferido (push, e-mail, SMS, central)

### Para o negócio

- Reforço do valor premium e diferencial de retenção via proatividade
- Meta mensurável de conversão pós-elegibilidade (60,5% → **90%**)
- Visibilidade do funil para o time de Produto Premium (Datadog PRD)

### Para operações / fluxos

- Pipeline observável com event codes e skip reasons estruturados
- Priorização clara: reduzir rejeições → migração Nike → valor premium
- Separação de BCs (Orquestração + Entrega) para evolução independente

## Status do domain-kit

| Fase | Status | Próximo passo |
| --- | --- | --- |
| Evidências | PASS | Manter fontes via `/domain.scan` se repos mudarem |
| Estratégico | PASS | — |
| Descoberta | PASS | Event storming opcional (`--stage event-storming`) |
| Operacional | FAIL | NFRs de produto + primeiro fluxo operacional |

Fase atual: **operacional-in-progress** · [Dashboard](dashboard.html)

Próximo comando sugerido: `/domain.model notificacao-dividas-pendencias --finalize`

## Sessão ativa

_Nenhuma sessão evolutiva aberta._ Use `/domain.change` para registrar problema ou evolução.

## Índice de artefatos

### Evidências

- [Síntese de evidências](01-product/00-scan/sintese-evidencias.md)
- [Manifest de scan](01-product/00-scan/scan-manifest.json)
- [Fontes](sources.yml)

### Estratégico

- [Design estratégico](01-product/01-vision/01-design-estrategico.md)
- [Desafio de negócio](01-product/02-domain/desafio-negocio.md)
- [Bounded contexts](01-product/02-domain/bounded-contexts.md)
- [Linguagem ubíqua](01-product/02-domain/linguagem-ubiqua.md)
- [Lacunas e problemas (P-n)](01-product/02-domain/abertos.md)

### Descoberta

- [Inclusão débito premium PF](01-product/03-discovery/02-domain-storytelling/01-inclusao-debito-premium-pf.md)
- [Exclusão pré-negativação e rejeições](01-product/03-discovery/02-domain-storytelling/02-exclusao-pre-negativacao-rejeicoes.md)
- [Event storming](01-product/03-discovery/01-event-storming/) _(pendente)_

### Operacional

- [Fluxos de negócio](01-product/03-operacional/fluxos/) _(0 promovidos)_
- [Requisitos NFR](04-platform/01-non-functional/01-requisitos.md) _(pendente)_
- [Registry de decisões](03-registry/produto.md)
- [Catálogo de fluxos](flows-registry.yml)

### Arch-kit (legado adotado)

- [Integração técnica](arch/01-integration/01-contextos.md)
- Capabilities: `entrega-de-notificacoes`, `orquestracao-de-notificacoes`

## Problemas e evoluções em aberto

### Problemas (P-n) — top abertas

| ID | Lacuna | Owner |
| --- | --- | --- |
| P01 | Sem PRD formal | Produto Premium |
| P03 | Paridade PF vs PJ | Produto + QA |
| P05 | Atraso de dados (compliance) | Platform + Antifraude |
| P09 | Resíduos TribeCS | Engenharia |

Ver inventário completo em [abertos.md](01-product/02-domain/abertos.md).

### Evoluções (E-n)

Nenhuma evolução registrada. Ver [evolucoes.md](01-product/02-domain/evolucoes.md).

## Changelog recente

Ver [CHANGELOG.md](CHANGELOG.md).
