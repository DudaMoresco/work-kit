> Roteiro **interno** — fase 0b de `/domain.discover`. Não invocar `/domain.clarify`.

Perguntas de **lacuna** — primeira etapa do discover, **somente após** `sintese-evidencias.md` promovido no `/domain.init`.

## Pré-condição

- `01-product/00-scan/sintese-evidencias.md` existe (promovido no init ou refresh do scan)
- Ler seção **Lacunas** da síntese — perguntas **não repetem** fatos já documentados

## Banco de perguntas (escolher só as que faltam)

1. Qual é o negócio em **uma frase**? _(se lacuna)_
2. Quem são os **atores** principais (pessoa + papel)?
3. Qual o **escopo MVP** vs fora de escopo?
4. Existe **sistema legado** (as-is)?
5. Há **decisões já fechadas** que não devemos reabrir?

Máximo **3 por turno**. Se a síntese já cobre tudo, declarar *"lacunas de negócio fechadas"* e seguir para o `--stage` DDD pendente.

Registrar abertos em `01-product/02-domain/abertos.md` (plan mode). Atualizar lacunas na síntese se respostas fecharem itens.
