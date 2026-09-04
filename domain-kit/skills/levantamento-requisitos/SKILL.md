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

Transforma demanda de negócio em **documento de requisitos** (upstream), com
riscos, persona, jornada, RF/RNF e **PlantUML** da jornada.

Idioma: **pt-BR**. Não cria cards no Jira — isso é `task-refinement`.

Relacionadas:

- `event-storming` / `event-storming-to-scenario-tables` — processo de domínio
- `domain-storytelling` — narrativa
- `ddd-design-tatico` — arquitetura após requisitos claros
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

Upstream: mapear e validar ideias **antes** da execução.

---

## Artefato (obrigatório)

### Onde salvar

1. Path do usuário.
2. Hub: `products/{produto}/04-platform/01-non-functional/01-requisitos.md`  
   (ou `requisitos/` com jornada + RF separados).
3. Fora do hub: `docs/requisitos-<slug>.md`.

Mapa de paths: [references/hub-paths.md](../references/hub-paths.md). Confirmar `{produto}` (e `{bc}` ou `{iniciativa}` quando aplicável) antes da 1ª gravação.

---

## Fluxo

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

## Saída no chat

1. Path  
2. Riscos em 4 linhas  
3. Lista curta de RF + abertos  

Exemplo: [examples.md](examples.md) (gestão de tarefas colaborativas / CRM).
