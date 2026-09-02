---
name: domain-clarify
description: >-
  DEPRECADO para usuários — perguntas e curadoria estão inline nos comandos
  discover/flow/capability. Use o comando principal.
disable-model-invocation: true
---

## Explain to user

**Clarify não é mais um passo separado.** Perguntas e curadoria rodam **dentro** do comando que você já iniciou:

| Quer… | Use |
| --- | --- |
| Fontes + descoberta | `/domain.discover` |
| Um fluxo | `/domain.flow {NN}` |
| Tático de BC | `/domain.capability {bc}` |
| Re-sync fontes | `/domain.scan` |

Roteiros em `.domain/clarify/*.md` são bancos internos — o agente carrega automaticamente.

## Se invocado mesmo assim

1. Identificar comando principal pendente (`discover`, `flow`, …).
2. Redirecionar: *"Continue com `/domain.{comando}` — clarify está inline."*
3. Não duplicar perguntas já feitas na sessão.

Ver [plan-mode.md](../../references/plan-mode.md).
