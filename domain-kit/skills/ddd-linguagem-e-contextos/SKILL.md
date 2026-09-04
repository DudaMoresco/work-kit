---
name: ddd-linguagem-e-contextos
description: >-
  Descoberta e formação de conhecimento DDD: formula o desafio do negócio,
  constrói dicionário de linguagem ubíqua (ambíguos/sinônimos), propõe bounded
  contexts e gera catálogo de documentação com PlantUML. Acione apenas pelo nome
  `ddd-linguagem-e-contextos` (não auto-invocar).
disable-model-invocation: true
---

# Linguagem ubíqua e Contextos Delimitados

Fecha a ponte entre mapa estratégico / narrativas e o modelo compartilhado:
**desafio do negócio → linguagem ubíqua → bounded contexts → catálogo**
(Wiki/Notion/MD) com **PlantUML**.

Idioma: **pt-BR**. Não classifica subdomínios nem desenha Domain Stories
completas — usa (ou pede) essas entradas.

Relacionadas (não substituem esta skill):

- `ddd-design-estrategico` — domínio/subdomínios (entrada típica)
- `domain-storytelling` — cenários; glossário alimenta o dicionário UL
- `ddd-integracao-contextos` — Conformista / ACL entre BCs (depois)
- `event-storming` — eventos para validar linguagem e limites
- `event-storming-to-scenario-tables` — eventos/comandos após limites claros
- `ddd-design-tatico` — camadas e agregados dentro dos BCs
- `request-for-comments` — decisões de fronteira controversas

Templates: [template.md](template.md) · Exemplos: [examples.md](examples.md) ·  
PlantUML: [references/plantuml-conventions.md](references/plantuml-conventions.md)

---

## Quando usar

- Usuário citar **`ddd-linguagem-e-contextos`**
- Pedir linguagem ubíqua, dicionário de termos, bounded contexts / contextos
  delimitados, desafio do negócio + catálogo de conhecimento DDD

**Não usar** para só mapear subdomínios (`ddd-design-estrategico`) ou só
narrar um cenário (`domain-storytelling`).

---

## Conceitos (obrigatório)

### Desafio do negócio

O que o negócio faz, quais processos importam e quais **dores** o Domain Expert
vê — além do desenho “ótimo” (realidade vs desejo). Escopo tipicamente um
recorte (ex.: entregas e correção de atividades), não a organização inteira.

### Linguagem ubíqua

Terminologia da realidade do negócio, compartilhada por negócio e
desenvolvimento, e depois refletida no modelo/código.

Regras ao mapear termos:

| Problema | Ação |
| --- | --- |
| **Ambíguo** (mesmo termo, vários significados no subdomínio) | Uma definição explícita por significado **ou** nomes distintos; nunca deixar implícito |
| **Sinônimo** (vários nomes / um nome para coisas diferentes, ex.: “login”) | Quebrar em termos únicos e específicos |
| Mesmo rótulo em áreas distintas (ex.: “pais” em admissão vs marketing vs secretaria) | Termo **por contexto**; registrar o conflito |

### Modelagem do domínio

Abstração do processo para resolver o problema. Iterativa: cada rodada com
experts refina o modelo com a linguagem alinhada. Documentar hipóteses vs
fatos.

### Contextos Delimitados (Bounded Contexts)

Limites **impostos no modelo** — não são os subdomínios. Contêm termos,
definições, propriedades e operações que compartilham **uma** linguagem
ubíqua.

Critérios desta skill:

- Métrica principal: **coerência da linguagem** e do tratamento dos processos
- Linguagem/processos muito parecidos → considerar **juntar**
- Distintos → **separar** para implementar sem interferência
- Tamanho: julgamento do arquiteto; grande ≠ time enorme
- Nº de BCs pode sugerir times, mas o modelo refina e pode integrar/reduzir
- Solução pequena: 1 BC possível; sistemas grandes: muitos BCs (até ~1:1 com
  sistemas)
- **Um BC = um time** (nunca compartilhado entre dois times); um time **pode**
  cuidar de vários BCs

**Subdomínio ≠ Bounded Context.** Relacionar no doc, sem forçar 1:1.

### Catálogo de conhecimento

Estrutura simples e atualizável (Wiki, Notion, MD no repo). Mínimo:

1. Hub / índice do projeto
2. Descrição do projeto e desafio
3. Times (subpáginas por área / subdomínio quando fizer sentido)
4. **Dicionário** de linguagem ubíqua
5. Cenários (premissas e limites) — links para Domain Stories
6. Links: código (Git), gestão do projeto

Manter atualizado a cada interação com experts.

---

## Artefato (obrigatório)

Escrever no disco — não só colar no chat.

### Onde salvar

1. Path do usuário → usar.
2. No `architecture-hub` (ou layout equivalente):

```text
products/{produto}/01-product/02-domain/
├── README.md                 # hub / índice do catálogo
├── desafio-negocio.md
├── linguagem-ubiqua.md       # dicionário
├── bounded-contexts.md       # BCs + PlantUML
└── cenarios/                 # links ou stubs para histórias
```

3. Fora do hub: `docs/02-domain/` na raiz do workspace (ou path
   confirmado).

Confirmar path na primeira gravação se ainda não estiver claro.

Usar [template.md](template.md) (pode ser um MD consolidado **ou** a pasta
acima; preferir pasta se houver vários BCs/cenários).

Mapa de paths: [references/hub-paths.md](../references/hub-paths.md). Confirmar `{produto}` (e `{bc}` ou `{iniciativa}` quando aplicável) antes da 1ª gravação.

---

## Fluxo de trabalho

```
Progresso:
- [ ] 1. Intake (recorte, fontes, path)
- [ ] 2. Desafio do negócio (realidade vs desejo)
- [ ] 3. Inventário de termos (cenários / experts / stories)
- [ ] 4. Resolver ambíguos e sinônimos → dicionário UL
- [ ] 5. Propor Bounded Contexts (pela linguagem)
- [ ] 6. Times × BCs
- [ ] 7. PlantUML + validar MCP
- [ ] 8. Catálogo (README + links) + abertos
```

### 1. Intake

Máx. 3–5 perguntas por turno se faltar:

| Campo | Se faltar |
| --- | --- |
| Recorte | Área/processo (ex.: entregas e correções) |
| Fontes | Design estratégico, Domain Stories, notas de expert |
| Path | Onde gravar o catálogo |
| Times | Papéis / squads conhecidos |

Se não houver mapa de subdomínios nem histórias, **inferir o mínimo** do
texto e marcar hipóteses; sugerir `ddd-design-estrategico` /
`domain-storytelling` para aprofundar.

### 2. Desafio

Preencher: o que fazem, processos-chave, dores conhecidas, desejo vs
realidade, Domain Experts do recorte.

### 3–4. Linguagem ubíqua

Para cada termo: definição, contexto/BC candidato, ambíguo?, sinônimos
descartados, evidência (fato/hipótese).

Exemplo pedagógico da aula: o ator/conceito **“pais”** muda entre admissão,
marketing e secretaria — três entradas ou um termo + qualificador por
contexto.

### 5–6. Bounded Contexts

Para cada BC proposto: nome, linguagem-núcleo (termos que “vivem” ali),
processos cobertos, subdomínios relacionados (se houver), time dono,
integrações com outros BCs (só nome da relação, sem mapa de integração
completo salvo se pedido).

### 7. PlantUML

No mínimo:

1. Mapa de Bounded Contexts (+ opcional subdomínios relacionados)
2. Times × BCs (1 time por BC; time pode ter vários BCs)

Validar com MCP **`user-plantuml`**: `check_syntax` → corrigir.
Não usar `https://www.plantuml.com/plantuml`.

Convenções: [references/plantuml-conventions.md](references/plantuml-conventions.md).

### 8. Catálogo + abertos

README hub com links; lista de hipóteses e termos ainda ambíguos.

---

## Saída no chat

1. Caminho(s) gravados
2. Desafio em 1–2 frases
3. Tabela: BC | Time | Termos-chave
4. Conflitos de linguagem ainda abertos

---

## Exemplo rápido

Escola — entregas e correção de atividades: [examples.md](examples.md).
