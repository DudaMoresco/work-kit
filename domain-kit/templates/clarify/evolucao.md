# Ritual: problemas (P-n) e evoluções (E-n)

Roteiro interno — impacto por fase do domain-kit.

## Três registros, três papéis

| ID | Arquivo | Pergunta |
| --- | --- | --- |
| **P-n** | `abertos.md` | O que está errado, incompleto ou incerto? |
| **E-n** | `evolucoes.md` | O que queremos mudar de propósito? |
| **D-n** | `05-decisoes/produto.md` | O que decidimos formalmente? |

## Entrada de sessão

Sempre preferir `/domain.change` antes de discover/flow/model quando **não** for onboarding linear.

## Matriz de impacto

| Tipo de mudança | Reabre fase? | Comando |
| --- | --- | --- |
| Repo, PRD, métrica externa | Evidências | `/domain.scan` |
| Prioridade, escopo, meta | Estratégico | `/domain.discover --stage contexts` |
| Nova regra de domínio | Descoberta | `/domain.discover --stage stories` |
| Novo cenário garantido | Operacional | `/domain.flow` |
| NFR de produto | Operacional | `/domain.model` |
| Decisão irreversível | Registry | `/domain.decision` |

## Regra

Evolução **não invalida** fases automaticamente — só artefatos afetados precisam de refresh (plan mode).

## Comandos que leem `activeChange`

No início da sessão, citar no chat: *"Sessão vinculada a P04"* e incluir no changelog.

- `/domain.discover`
- `/domain.flow`
- `/domain.model`
- `/domain.decision`
