---
name: event-storming-to-scenario-tables
description: Use esta skill quando o usuário fornecer um diagrama visual de Event Storming, especialmente em SVG, e quiser convertê-lo em tabelas descritivas por funcionalidade, com políticas reutilizáveis, comandos, eventos, atores e cenários alternativos.
---

# Event Storming → tabelas de cenário

## Purpose

Transformar diagramas visuais de Event Storming em documentação tabular clara
e manipulável (funcionalidade, ator, comando, evento, política, cenários
alternativos, continuidade).

Idioma: **pt-BR**. Foco em **funcionalidades** — não exigir Bounded Context
nesta etapa. Design tático / integração técnica: **fora do escopo do domain-kit**.

**Relacionadas:**

- `event-storming` — tempestade e timeline (PlantUML) **antes**, se ainda não houver diagrama
- `ddd-linguagem-e-contextos` — BCs depois (enriquecimento opcional)
- `levantamento-requisitos` / `task-refinement` — requisitos e backlog após as tabelas

Regras completas (obrigatórias): [references/rules.md](references/rules.md) ·  
Exemplos: [examples.md](examples.md)

---

## Quando usar

- Usuário fornecer SVG / draw.io / Miro / imagem / texto de ES e pedir tabelas
- Pedir políticas reutilizáveis (POL-n), FUN-n, cenários alternativos

**Não usar** para conduzir a sessão ES do zero (`event-storming`) nem para
gravar fluxos operacionais to-be (`fluxos-entregaveis` / `/domain.flow`).

---

## Entrada esperada

- arquivo `.svg` / `.drawio.svg` / imagem exportada
- texto extraído do Event Storming ou descrição livre do fluxo
- múltiplos diagramas ou diagrama + texto complementar

Com SVG: extrair `<text>`/`<tspan>`/`<title>`/`<desc>`, inferir por cor/proximidade
com cautela, marcar **Hipótese visual**, não inventar fluxo ausente.
Detalhe e limitações: [references/rules.md](references/rules.md) §4.

A skill **não deve exigir** bounded context. Se BCs já existirem
(`ddd-linguagem-e-contextos`), anotar como enriquecimento opcional.

---

## Conceitos (resumo)

| Conceito | Regra rápida |
| --- | --- |
| Funcionalidade (FUN-n) | Capacidade manipulável; uma tabela principal + alternativos |
| Evento | Verbo no **passado** |
| Comando | Preferir **infinitivo** |
| Ator | Pessoa, sistema, job ou código **POL-n** se a política dispara |
| Política (POL-n) | Regra reutilizável; consolidar equivalentes |
| Cenário alternativo | Abaixo da tabela; título `Início etapa [n] - …` |

Definições, categorias e exemplos: [references/rules.md](references/rules.md) §3 e §6–7.

---

## Why decisions

- Tabelas por **funcionalidade** são editáveis e exportáveis para planilha/backlog.
- Políticas com código **POL-n** reutilizável evitam duplicar a mesma regra.
- Cenários alternativos sob a tabela principal (com `Início etapa n`) preservam
  ramificação sem colunas Caminho / Gatilho / Próxima etapa.
- BC opcional nesta etapa: não bloqueia conversão visual → tabela.
- Hipóteses visuais marcadas explicitamente evitam inventar fluxo.
- Path canônico em `02-domain/cenarios/` amarra as tabelas ao catálogo de domínio.
- Regras longas vivem em `references/rules.md` para a skill permanecer orquestradora.

---

## Outputs canônicos

Mapa: [references/hub-paths.md](../../references/hub-paths.md). Em comando
`domain-*`, o **wrapper vence** se houver conflito.

```text
products/{produto}/01-product/02-domain/cenarios/
├── README.md                    # índice FUN-n / link políticas
├── politicas.md                 # tabela consolidada POL-n (ou seção no README)
└── FUN-001-<slug>.md            # uma funcionalidade por arquivo (ou MD consolidado)
```

Alternativa aceitável: um único MD consolidado sob `cenarios/` se o volume for baixo.
Path explícito do usuário tem prioridade. Confirmar `{produto}` antes da 1ª gravação.

A saída no chat / MD deve seguir a estrutura de resposta em
[references/rules.md](references/rules.md) (§12 Formato obrigatório).

---

## Workflow

```
Progresso:
- [ ] 1. Intake (formato da entrada, path, recorte)
- [ ] 2. Extrair textos/formas (SVG) ou parsear texto — ver rules §4
- [ ] 3. Separar funcionalidades + fluxo principal
- [ ] 4. Políticas (consolidar, POL-n, categorias) — rules §5–7
- [ ] 5. Tabelas por FUN + cenários alternativos — rules §8–9
- [ ] 6. Continuidade entre FUNs — rules §10
- [ ] 7. Gravar sob Outputs + checklist de consistência — rules §13
- [ ] 8. Abertos / limitações / ATOR_NAO_IDENTIFICADO
```

Detalhe passo a passo: [references/rules.md](references/rules.md) §11.

---

## Anti-patterns

- Exigir ou inventar Bounded Context nesta etapa.
- Duplicar políticas equivalentes em vez de reutilizar POL-n.
- Usar colunas Caminho / Condição·Gatilho / Próxima etapa.
- Inventar atores/eventos/comandos sem marcar hipótese (visual).
- Duplicar funcionalidade inteira quando há continuidade (`Continuar leitura em: FUN-XXX`).
- Gravar sob `03-discovery/01-event-storming/` (timeline) ou `04-operacional/fluxos/` (to-be).
- Ignorar limitações de SVG (texto em path, setas ambíguas) e fingir precisão.

---

## Exit

1. Path(s) gravados sob `01-product/02-domain/cenarios/`  
2. Contagem FUN-n + POL-n  
3. Limitações / hipóteses / perguntas em aberto  
4. Sugerir `ddd-linguagem-e-contextos` ou `levantamento-requisitos` se couber  

Prompt recomendado e checklist final: [references/rules.md](references/rules.md) §13–15.
