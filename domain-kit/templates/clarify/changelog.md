> Roteiro **interno** — registrar mudanças significativas após promote. Não invocar `/domain.clarify`.

Todo scan ou mudança material no produto **exige** entrada em `products/{p}/CHANGELOG.md`.

## Quando registrar (obrigatório)

| Gatilho | Comando típico | Registrar? |
| --- | --- | --- |
| Primeiro scan (manifest promovido) | `/domain.init` fase 0 | **Sim** |
| Re-sync de fontes (manifest ou síntese atualizada) | `/domain.scan` | **Sim** |
| Síntese de evidências promovida ou refresh material | `/domain.init` 0c, `/domain.scan` | **Sim** |
| Sessão evolutiva aberta | change | **Sim** (P-n / E-n) |
| Fase passou (Evidências, Estratégico, Descoberta, Operacional) | init, discover, model | **Sim** |
| Artefato DDD promovido (estratégico, BCs, story, ES, …) | `/domain.discover` | **Sim** |
| Fluxo operacional, requisitos NFR, registry promovidos | flow, model | **Sim** |
| Design tático ou integração técnica (fora do escopo) | etapa técnica posterior | **Sim** (se promovido no hub) |
| Decisão D-n registrada | `/domain.decision` | **Sim** |
| Registry atualizado (flows-registry, produto.md) | flow, decision, model | **Sim** |
| Modo incremental — nova capability | discover/capability/flow/model | **Sim** |
| Só rascunho em `.draft/` (sem promote) | qualquer | **Não** |
| Typo ou formatação sem impacto de domínio | qualquer | **Não** |
| Dashboard regenerado sem mudança canônica | regenerate | **Não** |

**Mudança significativa** = altera o que o hub considera verdade sobre o produto: findings, síntese, fases, BCs, fluxos, decisões, requisitos ou integração.

## Onde gravar

- Path canônico: `products/{p}/CHANGELOG.md`
- Criar a partir de `domain-kit/templates/CHANGELOG.md` no init se ausente
- **Após promote** do conteúdo que motivou a entrada (mesma sessão)
- Entrada pode ir direto no canônico — é resumo do que o usuário acabou de aprovar; **mostrar no chat** no checkpoint

## Formato da entrada

Inserir **no topo** do arquivo (abaixo do cabeçalho introdutório), uma seção por evento:

```markdown
## [YYYY-MM-DD] — {título curto}

| Campo | Valor |
| --- | --- |
| **Comando** | `/domain.scan` |
| **Tipo** | scan \| discovery \| model \| registry \| phase \| arch |
| **Fase** | evidencias \| estrategico \| descoberta \| operacional \| — |

### O que mudou
- …

### Impacto
- …

### Artefatos afetados
- `path/relativo/no/produto`
```

### Campos

- **Título curto** — uma linha (ex.: "Re-sync GitHub — 3 findings novos", "BC ordem-de-servico fechado → Estratégico PASS")
- **O que mudou** — bullets objetivos; citar findings incorporados, artefatos criados/atualizados, fases
- **Impacto** — o que muda para quem lê o hub (discover pendente, novo fluxo, decisão D-n, etc.)
- **Artefatos afetados** — paths promovidos nesta sessão

## Scan — conteúdo mínimo

Para `/domain.init` fase 0 ou `/domain.scan`:

- Fontes consultadas (repos/docs)
- Findings **incorporados** vs **ignorados** (contagem ou lista curta)
- Se síntese foi refreshada
- Próximo passo sugerido se relevante

## Checkpoint

Após append no CHANGELOG, incluir no encerramento da sessão:

```markdown
### Changelog
Entrada registrada em `CHANGELOG.md`: **{título curto}**
```

Se nada significativo foi promovido nesta sessão, declarar explicitamente: *"Nenhuma entrada de changelog — sem promote material."*
