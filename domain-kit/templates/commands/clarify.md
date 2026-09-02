---
name: domain-clarify
description: Perguntas guiadas antes de gravar artefatos de domínio; revisão de scan.
---

## Explain to user

Vou fazer até 3 perguntas por vez sobre o que ainda não está claro. Só gravo arquivos quando você confirmar "pode gravar".

## User Input

```text
$ARGUMENTS
```

Modo: `discover` | `bc {slug}` | `flow {NN}` | `scan` | `open` (default: discover)

## Steps

1. Carregar banco em `.domain/clarify/{modo}.md` ou `domain-kit/templates/clarify/`.
2. Ler contexto: scan-manifest, abertos.md, flows-registry, produto ativo.
3. Fazer **máximo 3 perguntas** por turno.
4. Registrar respostas pendentes em `01-product/02-domain/abertos.md`.
5. Modo `scan`: para cada finding — incorporar / ignorar / pendente.
6. **Não gravar** artefatos canônicos neste comando (só abertos + notas).

## Regra

Se usuário confirmar incorporação de scan → indicar próximo comando (`discover` ou artefato específico).
