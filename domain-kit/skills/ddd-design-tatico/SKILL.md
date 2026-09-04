---
name: ddd-design-tatico
description: >-
  Design tático DDD: arquitetura em 4 camadas (Interface, Aplicação, Domínio,
  Infraestrutura) e blocos (Entidade, Value Object, Agregado); gera doc com
  PlantUML. Acione apenas pelo nome `ddd-design-tatico` (não auto-invocar).
disable-model-invocation: true
---

# Design Tático DDD

Materializa o “como”: **camadas** e **blocos de construção** dentro de um BC /
recorte, com Markdown + **PlantUML**.

Idioma: **pt-BR**. Não faz bootstrap de repo Java ECS (`java-dalvito-hexagonal-bootstrap`).

Relacionadas:

- `ddd-linguagem-e-contextos` / `ddd-integracao-contextos` — fronteiras antes
- `event-storming` — eventos alimentam agregados
- `java-dalvito-hexagonal-bootstrap` — implementação ECS depois do desenho
- `code-design-master` — princípios de design Java

Templates: [template.md](template.md) · Exemplos: [examples.md](examples.md) ·  
PlantUML: [references/plantuml-conventions.md](references/plantuml-conventions.md)

---

## Quando usar

- Usuário citar **`ddd-design-tatico`**
- Pedir camadas DDD, Entidade / VO / Agregado, arquitetura tática do domínio

**Não usar** para Context Mapping, ES workshop ou requisitos de produto.

---

## Conceitos (obrigatório)

### Quatro camadas (Evans)

| Camada | Responsabilidade |
| --- | --- |
| **Interface de Usuário** | GUI, CLI, APIs de integração |
| **Aplicação** | Mediação UI↔Domínio; **sem** lógica de negócio; não altera estado de domínio; organiza tarefas/gatilhos (ex.: job que dispara “atualizar presença”) |
| **Domínio** | “Coração do software”: regras, mudanças de estado; **não** persiste; informa a Infra o que registrar |
| **Infraestrutura** | Persistência, mensageria, capacidades técnicas de suporte |

Em algumas arquiteturas a camada de Aplicação funde-se à Interface — declarar
explicitamente se for o caso.

### Blocos de construção (mínimo desta skill)

| Bloco | Uso |
| --- | --- |
| **Entidade** | Identidade ao longo do tempo |
| **Value Object** | Sem identidade; definido por atributos; imutável na prática |
| **Agregado** | Cluster de entidades/VOs com raiz; fronteira de consistência/transação |

Outros blocos (Repositório, Serviço de domínio, Domínio Event) só se o usuário
pedir ou o modelo exigir — sem inventar catálogo completo.

### Decisões tecnológicas (registrar, não implementar)

Ex.: relacional vs NoSQL, monolito vs microsserviços/ESB — como **hipótese**
ligada ao BC, não como deploy.

---

## Artefato (obrigatório)

### Onde salvar

1. Path do usuário.
2. Hub: `products/{produto}/02-capabilities/{bc}/design-tatico.md`  
   (ou `design-tatico/<bc-slug>.md` por BC).
3. Senão: `docs/design-tatico-<slug>.md`.

Mapa de paths: [references/hub-paths.md](../references/hub-paths.md). Confirmar `{produto}` (e `{bc}` ou `{iniciativa}` quando aplicável) antes da 1ª gravação.

---

## Fluxo

```
Progresso:
- [ ] 1. Intake (BC/recorte, fontes, path)
- [ ] 2. Camadas e o que vive em cada uma
- [ ] 3. Entidades, VOs, agregados (raiz + invariantes)
- [ ] 4. PlantUML camadas + agregados; validar MCP
- [ ] 5. Decisões tech (hipóteses) + abertos
```

Validar com MCP **`user-plantuml`**. Não usar plantuml.com.

---

## Saída no chat

1. Path  
2. Agregados (raiz + membros)  
3. Abertos  

Exemplo: [examples.md](examples.md) (entregas/correções na escola).
