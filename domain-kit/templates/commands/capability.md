---
name: domain-capability
description: "Fora do escopo do domain-kit — design tático de BC (próxima etapa técnica)."
---

## Explain to user

**Este comando está fora do escopo do domain-kit.** O domain-kit foca em modelagem de **problema/negócio** (fases Estratégico, Descoberta, Operacional).

Design tático (agregados, camadas, ports/adapters) é **próxima etapa técnica (fora deste kit)**. Se precisar documentar agora, grave em `products/{p}/arch/{bc}/design-tatico.md` (pasta opcional, nunca gated) — não como critério de saída do domain-kit.

## User Input

```text
$ARGUMENTS
```

## Steps

1. Informar que design tático está fora do escopo do domain-kit.
2. Se o usuário insistir: propor conteúdo em `.draft/arch/{bc}/design-tatico.md` (não inventar path fora de [hub-paths.md](../../references/hub-paths.md) para entregas do kit).
3. Atualizar `domain-status.json` → `arch.capabilitiesAdopted` após promote.
4. **Não** validar a fase Operacional com design-tatico.
