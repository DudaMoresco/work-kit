---
name: ddd-integracao-contextos
description: >-
  Mapeia integração entre Bounded Contexts (Context Mapping): Conformista,
  Customer/Supplier e Anti-Corruption Layer (ACL); gera doc com diagramas
  PlantUML. Acione apenas pelo nome `ddd-integracao-contextos` (não auto-invocar).
disable-model-invocation: true
---

# Integração de Contextos Delimitados

Define **como** Bounded Contexts se relacionam (quem manda no protocolo, se há
ACL) e grava mapa de integração em Markdown com **PlantUML**.

Idioma: **pt-BR**. Pressupõe BCs já nomeados (de `ddd-linguagem-e-contextos`).

Relacionadas:

- `ddd-linguagem-e-contextos` — propõe BCs e UL (antes)
- `ddd-design-tatico` — camadas/agregados depois das fronteiras
- `ddd-design-estrategico` — subdomínio principal (critério de ACL)
- `request-for-comments` — decisão controversa de integração

Templates: [template.md](template.md) · Exemplos: [examples.md](examples.md) ·  
PlantUML: [references/plantuml-conventions.md](references/plantuml-conventions.md)

---

## Quando usar

- Usuário citar **`ddd-integracao-contextos`**
- Pedir Context Mapping, Conformista, ACL / camada anticorrupção, integração
  entre BCs ou com fornecedor externo (OAuth, legado, SaaS)

**Não usar** para só listar BCs sem relações, nem para camadas táticas internas.

---

## Conceitos (obrigatório)

### Fornecedor (Upstream / U) e Cliente (Downstream / D)

- **U** publica o modelo/protocolo.
- **D** consome. Quem “manda” na relação define o padrão de integração.

### Conformista

Quando o fornecedor **não** adapta o protocolo às demandas do cliente, o
cliente **se conforma** e adequa sua solução ao padrão dado (ex.: OAuth 2.0 de
provedor global).

### Não-conformismo → ACL

Quando D **não** aceita o modelo de U e U **não** muda o protocolo, D cria
**Anti-Corruption Layer (ACL)**: abstrai o protocolo externo e traduz para o
modelo interno, preservando integridade do BC cliente.

### Quando usar ACL

1. O BC cliente contém **subdomínio principal** — isola o core de corrupção.
2. Modelo do fornecedor é ineficiente / incompleto (comum em **legado**).
3. Fornecedor muda protocolo com frequência — manutenção concentrada na ACL.

### Outros padrões (mínimo)

Se a narrativa pedir: Customer/Supplier (negociação de contrato entre times),
Partnership, Shared Kernel — só documentar se houver evidência; default da
aula: Conformista vs ACL.

---

## Artefato (obrigatório)

Escrever MD no disco.

### Onde salvar

1. Path do usuário → usar.
2. Hub: `products/{produto}/01-product/04-integration/01-contextos.md`  
   (ou pasta `integracao-contextos/` se houver vários mapas).
3. Senão: `docs/integracao-contextos-<slug>.md`.

Usar [template.md](template.md).

Mapa de paths: [references/hub-paths.md](../references/hub-paths.md). Confirmar `{produto}` (e `{bc}` ou `{iniciativa}` quando aplicável) antes da 1ª gravação.

---

## Fluxo

```
Progresso:
- [ ] 1. Intake (BCs, fornecedores externos, path)
- [ ] 2. Listar relações U → D
- [ ] 3. Classificar cada relação (Conformista / ACL / outro)
- [ ] 4. Justificar ACL com os 3 critérios
- [ ] 5. PlantUML + validar MCP
- [ ] 6. Gravar MD + abertos
```

Validar PlantUML com MCP **`user-plantuml`**: `check_syntax`.  
Não usar `https://www.plantuml.com/plantuml`.

---

## Saída no chat

1. Path do arquivo  
2. Tabela: Upstream | Downstream | Padrão | Motivo  
3. Abertos  

Exemplo: [examples.md](examples.md) (escola / identidade OAuth + CRM + ACL).
