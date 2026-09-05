---
name: levantamento-requisitos
description: >-
  Levanta requisitos de produto/sistema: riscos Cagan (valor, negócio,
  usabilidade, técnico), persona, problema, objetivos, jornada, RF/RNF; gera
  doc com PlantUML da jornada. Acione apenas pelo nome `levantamento-requisitos`
  (não auto-invocar).
disable-model-invocation: true
---

# Levantamento de Requisitos

## Purpose

Transforma demanda de negócio em **documento de requisitos** (upstream), com
riscos, persona, jornada, RF/RNF e **PlantUML** da jornada.

Idioma: **pt-BR**. Não cria cards no Jira — isso é `task-refinement`.

Relacionadas:

- `event-storming` / `event-storming-to-scenario-tables` — processo de domínio
- `domain-storytelling` — narrativa
- Design de solução / tático — **fora do escopo do domain-kit** (após requisitos claros)
- `task-refinement` — refinamento técnico + backlog (depois)
- `request-for-comments` — decisão de produto controversa

Templates: [template.md](template.md) · Exemplos: [examples.md](examples.md) ·  
PlantUML: [references/plantuml-conventions.md](references/plantuml-conventions.md)

---

## Quando usar

- Usuário citar **`levantamento-requisitos`**
- Pedir spec de requisitos, riscos Cagan, persona, jornada, RF/RNF (antes do
  grooming técnico)

**Não usar** para só quebrar em tarefas Jira (`task-refinement`).

---

## Why decisions

- Riscos Cagan (valor, negócio, usabilidade, técnico) forçam validação antes
  de backlog — evita “spec que ninguém quer”.
- Persona + problema + objetivos amarram RF à dor, não a features soltas.
- Jornada com PlantUML torna o fluxo revisável com PM/UX sem código.
- RF/RNF no mesmo doc evita NFR esquecido até a véspera do go-live.
- Upstream: mapear e validar ideias **antes** da execução / task-refinement.
- Path canônico em `04-operacional/requisitos.md` alinha NFR de produto ao hub.
- Em `/domain.model` (e demais `domain-*`), o **wrapper vence** a skill se houver
  conflito de path ou ordem.

---

## Conceitos (obrigatório)

### Riscos (Marty Cagan)

| Risco | Pergunta-chave | Quem costuma validar |
| --- | --- | --- |
| **Valor** | O usuário precisa / pagaria / adotaria? | PM / PO |
| **Negócio** | Alinha à estratégia? Viável financeiramente? Risco legal? | Negócio / jurídico |
| **Usabilidade** | A experiência permite adoção? | UX / testes de usabilidade |
| **Técnico** | Time tem recursos (técnicos, $$, gente) para construir? | Engenharia |

### Elementos essenciais do doc

1. Persona  
2. Problema  
3. Objetivos da solução  
4. Jornada do usuário  
5. Requisitos funcionais  
6. Requisitos não funcionais  

---

## Outputs canônicos

Mapa: [references/hub-paths.md](../../references/hub-paths.md). Em comando
`domain-*` (incl. `/domain.model`), o **wrapper vence** se houver conflito.

1. Path explícito do usuário (se houver).
2. Hub:

```text
products/{produto}/01-product/04-operacional/requisitos.md
```

   (ou pasta `requisitos/` com jornada + RF separados, ainda sob `04-operacional/`).

3. Fora do hub: `docs/requisitos-<slug>.md`.

**Não** inventar path fora de [hub-paths.md](../../references/hub-paths.md). Confirmar `{produto}`
antes da 1ª gravação. Usar [template.md](template.md).

---

## Workflow

```
Progresso:
- [ ] 1. Intake (problema, stakeholders, path)
- [ ] 2. Riscos Cagan (status: aberto / mitigado / hipotese)
- [ ] 3. Persona + problema + objetivos
- [ ] 4. Jornada (passos) + PlantUML
- [ ] 5. RF e RNF
- [ ] 6. Abertos + apontar task-refinement
```

Validar PlantUML com MCP **`user-plantuml`**.

---

## Anti-patterns

- Pular riscos e ir direto a lista de RF.
- Misturar design tático / camadas / agregados no doc de requisitos.
- Criar cards Jira nesta skill (`task-refinement` é depois).
- Tratar hipóteses de risco como requisitos fechados.
- Inventar path fora de [hub-paths.md](../../references/hub-paths.md).
- Ignorar o wrapper em sessão `domain.model` e sobrescrever paths do comando.

---

## Exit

Saída no chat:

1. Path gravado  
2. Riscos em 4 linhas  
3. Lista curta de RF + abertos  
4. Sinalizar `task-refinement` / RFC se houver decisão aberta  

Exemplo: [examples.md](examples.md) (gestão de tarefas colaborativas / CRM).
