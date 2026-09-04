# Clarify: /domain.change — abertura de sessão evolutiva

Roteiro interno — carregado por `domain-change` skill.

## Objetivo

Classificar intenção (problema novo, problema existente, evolução), registrar P-n ou E-n, preencher `activeChange` e rotear para o comando de fase correto.

## Perguntas (máx. 3 por turno)

1. **O que mudou ou precisa mudar?** (contexto em 1–2 frases)
2. **É defeito/lacuna ou mudança intencional?** → sugere `problem-new` vs `evolution`
3. **Já existe P-n ou E-n?** → se sim, `--kind problem --id Pnn` ou retomar E-n

## Classificação

| Sinal | `--kind` |
| --- | --- |
| Algo errado, incompleto, métrica fora do esperado | `problem-new` ou `problem` |
| Novo canal, meta, escopo, feature deliberada | `evolution` |
| Retomar item já catalogado | `problem` ou `evolution` + `--id` |

## Impacto por fase

Declarar explicitamente no chat:

| Mudança | Fases impactadas | Handoff |
| --- | --- | --- |
| Fonte externa nova | evidencias | `/domain.scan` |
| Meta, prioridade, escopo | estrategico | `/domain.discover --stage contexts` |
| Regra/comportamento de domínio | descoberta (+ operacional) | `/domain.discover --stage stories` |
| Cenário ponta a ponta | operacional | `/domain.flow` |
| SLA, volume, compliance | operacional | `/domain.model` |
| Trade-off formal | registry | `/domain.decision` |

## Registro

- **P-n** → append/atualizar `01-product/02-domain/abertos.md` (plan mode)
- **E-n** → append/atualizar `01-product/02-domain/evolucoes.md` (plan mode)
- **activeChange** → `domain-status.json` após promote do registro

## Fechamento de sessão

Ao resolver ou pausar:

1. Atualizar status P-n/E-n (fechada / em-andamento / concluída)
2. Changelog com referência ao id (P-n ou E-n)
3. Refresh `product-README.md` se visão ou benefícios mudaram
4. `activeChange.status` → `paused` ou limpar (`null`)
