---
name: ddd-design-estrategico
description: >-
  Mapeia domínio e subdomínios de um negócio descrito, classifica cada
  subdomínio (principal, suporte ou genérico) e gera documentação de Design
  Estratégico DDD com diagramas PlantUML. Acione apenas pelo nome
  `ddd-design-estrategico` (não auto-invocar).
disable-model-invocation: true
---

# Design Estratégico DDD

Mapeia o **domínio** e os **subdomínios** de um negócio descrito, **classifica**
cada subdomínio e grava um **doc de Design Estratégico** em Markdown com
**PlantUML**.

Idioma: **pt-BR**. Escopo: Design Estratégico (não tático: aggregates,
repositories, etc.).

Relacionadas (não substituem esta skill):

- `ddd-linguagem-e-contextos` — linguagem ubíqua e bounded contexts (**subdomínio ≠ BC**)
- `ddd-integracao-contextos` — Conformista / ACL entre BCs
- `domain-storytelling` — narrativas após o mapa estratégico
- `event-storming` — tempestade de eventos
- `event-storming-to-scenario-tables` — depois do mapa estratégico
- `request-for-comments` — proposta de mudança
- `fluxogramas-decisao` — regras as-is de um fluxo

Templates: [template.md](template.md) · Exemplos: [examples.md](examples.md) ·  
PlantUML: [references/plantuml-conventions.md](references/plantuml-conventions.md)

---

## Quando usar

- Usuário citar **`ddd-design-estrategico`**
- Pedir mapa de domínio/subdomínios, classificação principal/suporte/genérico
  ou doc de Design Estratégico DDD

**Não usar** para Event Storming tabular, RFC, diagramas de decisão de
fluxo, dicionário de linguagem ubíqua ou bounded contexts — use as skills
acima (`ddd-linguagem-e-contextos` para UL/BC).

**Nota:** classificação de subdomínios **não** define sozinha Contextos
Delimitados. Após o mapa estratégico, preferir `ddd-linguagem-e-contextos`.

---

## Conceitos (obrigatório)

### Domínio

Área de atividade/interesse do usuário à qual o software se alinha. Pode ser
física (ex.: reserva de voo) ou intangível (ex.: contabilidade).

Pergunta-guia: *qual é o negócio em uma frase?*

### Subdomínio Principal (Core)

O que **diferencia** o negócio no mercado — vantagem competitiva.

Exemplos: Escola → Aulas e Metodologias; Netflix → Vídeos; Azul → Voos;
DHL → Serviços logísticos.

### Subdomínio de Suporte

Apoia o principal **sem** vantagem estratégica. Em geral lógica simples /
CRUD operacional.

Exemplos: Escola → gestão de pais e alunos; Netflix → cadastro de títulos;
Azul → cadastro de pessoas; DHL → integração com outros sistemas logísticos.

### Subdomínio Genérico

Processos **comuns no mercado** (portal, loja, autenticação, faturamento,
criptografia, contabilidade). Podem ser complexos e ter lógica própria, mas
**não** diferenciam o produto.

**Contexto importa:** o que é genérico em um domínio pode ser principal em
outro.

Exemplos: Escola → criptografia; Netflix → faturamento; Azul → autenticação;
DHL → contabilidade.

### Domain Expert

Pessoa que conhece o Domínio/Subdomínio, descreve processos e “conta a
história”. Em um domínio há vários experts (um por área relevante).

---

## Fluxograma de classificação

Para **cada** candidato a subdomínio, aplicar nesta ordem:

```
1. Diferencia o negócio no mercado / vantagem competitiva?
   → SIM: Principal
2. É capacidade comum de mercado (auth, billing, portal, crypto, contabilidade…)?
   → SIM: Genérico
3. Apoia o principal com operações básicas / CRUD / cadastro / integração auxiliar?
   → SIM: Suporte
4. Ambíguo → marcar hipótese + Domain Expert a validar
```

PlantUML canônico do fluxograma: ver [references/plantuml-conventions.md](references/plantuml-conventions.md).

---

## Artefato (obrigatório)

Escrever arquivo Markdown no disco — não só colar no chat.

### Onde salvar

1. Path indicado pelo usuário → usar.
2. No `architecture-hub` (ou layout equivalente):

```text
products/{produto}/01-product/01-vision/01-design-estrategico.md
```

3. Fora do hub: `docs/design-estrategico-<slug>.md` na raiz do workspace
   (ou path confirmado).

Antes da primeira gravação, confirmar path se ainda não estiver claro.
Depois, informar o caminho do arquivo.

Usar a estrutura de [template.md](template.md).

Mapa de paths: [references/hub-paths.md](../references/hub-paths.md). Confirmar `{produto}` (e `{bc}` ou `{iniciativa}` quando aplicável) antes da 1ª gravação.

---

## Fluxo de trabalho

```
Progresso:
- [ ] 1. Intake
- [ ] 2. Domínio (uma frase)
- [ ] 3. Candidatos a subdomínio
- [ ] 4. Classificar (fluxograma)
- [ ] 5. Domain Experts
- [ ] 6. Diagramas PlantUML + validar MCP
- [ ] 7. Gravar design-estrategico.md
- [ ] 8. Hipóteses / abertos
```

### 1. Intake

Extrair do que já foi dito. Perguntar só o que faltar (máx. 3–5 por turno):

| Campo | Se faltar |
| --- | --- |
| Negócio / produto | O que a empresa faz |
| Diferencial | O que a torna especial no mercado |
| Capacidades / áreas | Processos, sistemas, módulos citados |
| Path do doc | Onde gravar |
| Domain Experts | Quem valida (papéis, não PII desnecessária) |

Entrada válida: narrativa livre, lista de módulos, organograma, backlog,
C4 de contexto, notas de discovery.

### 2. Domínio

Uma frase clara + 2–4 bullets do que está **dentro** / **fora** do escopo
desta análise.

### 3. Candidatos

Listar áreas/capacidades sem classificar ainda. Preferir nomes de **negócio**,
não de tecnologia (`Aulas e Metodologias`, não `SchoolService`).

### 4. Classificar

Para cada candidato: tipo + **justificativa em 1–2 frases** + evidência
(falada pelo usuário vs hipótese).

Regras:

- Preferir **poucos** Principais (idealmente 1; mais de 2 exige justificativa forte).
- Genérico ≠ “fácil”: pode ser complexo e ainda ser genérico.
- Se a classificação depender de contexto de mercado, deixar explícito.

### 5. Domain Experts

Para cada subdomínio (ou grupo), indicar o papel do expert (ex.: coordenação
pedagógica, operações, financeiro). Se desconhecido → aberto.

### 6. PlantUML

Incluir no doc, no mínimo:

1. **Mapa domínio → subdomínios** (cores por tipo)
2. **Fluxograma de classificação** (referência ou aplicado)

Validar com MCP **`user-plantuml`**: `check_syntax` → corrigir → (opcional)
`render_diagram`. Não usar `https://www.plantuml.com/plantuml`.

Convenções: [references/plantuml-conventions.md](references/plantuml-conventions.md).

### 7–8. Doc + abertos

Gravar seguindo [template.md](template.md). Seção final: hipóteses,
ambiguidades e perguntas para Domain Experts.

---

## Saída no chat

Após gravar:

1. Caminho do arquivo
2. Domínio em uma frase
3. Tabela resumida: Subdomínio | Tipo | Justificativa curta
4. Principais abertos (se houver)

---

## Exemplo rápido

Ver caso completo da Escola em [examples.md](examples.md).
