---
name: domain-storytelling
description: >-
  Conduz Domain Storytelling (narrativa de domínio): extrai atores, objetos de
  trabalho, atividades numeradas, anotações, cenários e escopo; gera doc Markdown
  com diagramas PlantUML. Acione apenas pelo nome `domain-storytelling`
  (não auto-invocar).
disable-model-invocation: true
---

# Domain Storytelling

Transforma a narrativa de um domínio/subdomínio em **histórias pictográficas
coesas**: quem faz o quê, com quais objetos, em que ordem — e grava um doc
Markdown com **PlantUML**.

Idioma: **pt-BR**. Técnica colaborativa de DDD (Hofer & Schwentner), não
substitui Event Storming nem Design Estratégico.

Relacionadas (não substituem esta skill):

- `ddd-design-estrategico` — domínio/subdomínios (antes ou em paralelo)
- `ddd-linguagem-e-contextos` — dicionário UL e BCs (glossário desta skill alimenta)
- `ddd-integracao-contextos` — mapa de integração entre BCs
- `event-storming` — tempestade de eventos
- `event-storming-to-scenario-tables` — eventos/comandos tabulares
- `fluxogramas-decisao` — árvores de regra as-is

Templates: [template.md](template.md) · Exemplos: [examples.md](examples.md) ·  
PlantUML: [references/plantuml-conventions.md](references/plantuml-conventions.md)

---

## Quando usar

- Usuário citar **`domain-storytelling`**
- Pedir narrativa de domínio, Domain Story, linguagem pictográfica, jornada
  colaborativa de atores/objetos de trabalho

**Não usar** para classificar subdomínios (`ddd-design-estrategico`),
dicionário completo de UL / bounded contexts (`ddd-linguagem-e-contextos`)
nem inventário de eventos de ES.

---

## Objetivo da técnica

Contar e ouvir histórias para:

- Entender o domínio
- Estabelecer linguagem entre Domain Experts e IT Experts
- Evitar mal-entendidos
- Esclarecer requisitos
- Implementar e estruturar software corretamente
- Desenhar processos de negócio viáveis suportados por software

(HOFER & SCHWENTNER, 2021)

A narrativa reúne pessoas com níveis distintos de conhecimento num **único
documento**, deixando claro o que é feito e **quais são os limites** da história.

---

## Conceitos (obrigatório)

### Linguagem pictográfica

Símbolos (pictogramas) + conexões + textos explicam relações. Frase básica:

```text
Ator (sujeito) → Atividade (verbo) → Objeto de trabalho (objeto)
                 [opcional: com outro ator]
```

### Atores

Quem age na história: **pessoa**, **grupo de pessoas**, **objeto** ou
**sistema**. Rotular pelo **papel** de negócio (não por nome próprio).

Tipos visuais (PlantUML): pessoa | grupo | sistema — ver convenções.

### Objetos de trabalho (work objects)

Coisas que atores criam, manipulam ou trocam: documentos, coisas físicas,
objetos digitais, informações sobre objetos. Rotular com termo da **linguagem
do domínio**.

### Atividades

Verbos da linguagem do domínio nas setas (ex.: elabora, entrega, valida).

### Números de sequência

Ordem temporal das “frases” da história (1, 2, 3…). Uma história = várias
frases em sequência.

### Anotações

Texto complementar: variações, opcionais, erros, premissas, glossário de
termos, objetivo de uma atividade.

### Cenários

Histórias **concretas** (exemplos típicos), não o processo abstrato genérico.
Preferir o caso feliz representativo; variações via anotações ou cenários
separados.

### Escopo (definir sempre)

Três eixos — escolher e declarar no doc:

| Eixo | Opções típicas |
| --- | --- |
| Granularidade | Grossa (visão) ↔ Fina (detalhe) |
| Momento | As-is (hoje) / To-be (desejado) |
| Pureza de domínio | Puro (sem software) / Digitalizado (com sistemas) |

Mudar o escopo = outra história (ou versão explícita).

### Equipe de trabalho (workshop)

Papéis mínimos:

| Papel | Função |
| --- | --- |
| Contador(es) | Domain Experts narram o cenário concreto |
| Facilitador / modelador | Registra a história ao vivo na linguagem pictográfica |
| Ouvintes (IT, PO, etc.) | Validam entendimento; perguntam só para clareza |

Se a sessão for assíncrona (só texto no chat), o agente atua como **modelador**;
marcar hipóteses e pedir validação dos experts.

---

## Artefato (obrigatório)

Escrever Markdown no disco — não só colar no chat.

### Onde salvar

1. Path do usuário → usar.
2. No `architecture-hub` (ou layout equivalente):

```text
products/{produto}/01-product/03-discovery/02-domain-storytelling/
├── README.md                 # índice de histórias + escopos
├── 01-<cenario-slug>.md      # uma história por arquivo
└── …
```

3. Caso contrário: `docs/domain-storytelling/<slug>.md` (ou path confirmado).

Confirmar path na primeira gravação se ainda não estiver claro.

Usar [template.md](template.md).

Mapa de paths: [references/hub-paths.md](../references/hub-paths.md). Confirmar `{produto}` (e `{bc}` ou `{iniciativa}` quando aplicável) antes da 1ª gravação.

---

## Fluxo de trabalho

```
Progresso:
- [ ] 1. Intake (negócio, cenário, escopo, path)
- [ ] 2. Definir escopo (3 eixos)
- [ ] 3. Extrair atores e objetos de trabalho
- [ ] 4. Montar frases numeradas (atividades)
- [ ] 5. Anotações / variações
- [ ] 6. PlantUML + validar MCP
- [ ] 7. Glossário da linguagem ubíqua
- [ ] 8. Gravar MD + abertos para Domain Experts
```

### 1. Intake

Perguntar só o que faltar (máx. 3–5 por turno):

| Campo | Se faltar |
| --- | --- |
| Negócio / subdomínio | Contexto da história |
| Cenário concreto | “Conte um exemplo típico, passo a passo” |
| Escopo | Granularidade, as-is/to-be, puro/digitalizado |
| Path | Onde gravar |
| Experts | Papéis que narram/validam |

### 2–5. Modelagem

1. Listar atores (papel + tipo: pessoa/grupo/sistema).
2. Listar objetos de trabalho (substantivos do domínio).
3. Escrever a história como frases numeradas:

   `N. <Ator> <verbo> <objeto> [para/com <Ator>]`

4. Anotar premissas, variações e limites (“esta história **não** cobre…”).

Regras:

- Uma história = **um** cenário + **um** escopo declarado.
- Preferir poucos atores bem nomeados a dezenas de detalhe irrelevante.
- Substantivos/verbos = candidatos à linguagem ubíqua.
- Se aparecer sistema demais em escopo **puro**, reclassificar escopo ou
  extrair versão digitalizada.

### 6. PlantUML

No mínimo:

1. Diagrama da história (atores + objetos + setas numeradas)
2. Opcional: tabela/lista de sequência espelhando o diagrama

Validar com MCP **`user-plantuml`**: `check_syntax` → corrigir → (opcional)
`render_diagram`. Não usar `https://www.plantuml.com/plantuml`.

Convenções: [references/plantuml-conventions.md](references/plantuml-conventions.md).

### 7–8. Glossário e abertos

Glossário curto (termo → significado no domínio). Abertos: ambiguidades,
cenários faltantes, conflitos de linguagem entre departamentos.

Se houver ambíguos/sinônimos ou vários departamentos com o mesmo rótulo,
encaminhar para `ddd-linguagem-e-contextos` (dicionário UL + BCs).

---

## Saída no chat

Após gravar:

1. Caminho do arquivo
2. Escopo (3 eixos) em uma linha
3. Lista numerada das frases da história
4. Principais abertos / hipóteses

---

## Exemplo rápido

Caso Escola (“Projeto Escola”) em [examples.md](examples.md).
