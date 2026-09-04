---
name: fluxogramas-decisao
description: >-
  Gera ou atualiza documentação as-is de regras de negócio em
  products/{produto}/02-capabilities/{bc}/fluxogramas-decisao/: README com mapa
  PlantUML, um MD por fluxo (árvore de decisão + sequência C4 + eventos).
  Use when the user asks for fluxogramas de decisão, árvores de regras,
  docs de fluxo as-is alinhados ao C4, ou pasta fluxogramas-decisao.
---

# Fluxogramas de decisão (as-is)

Documenta **regras de negócio** do comportamento em produção (ou legado),
não o to-be. Cada fluxo: **o que decide** + **quem chama quem** (C4).

Referência canônica no hub:

- `architecture-hub/products/monitoramento-pj/02-capabilities/{bc}/fluxogramas-decisao/`
- `architecture-hub/products/documentos-roubados/02-capabilities/{bc}/fluxogramas-decisao/`

Templates: [references/templates.md](references/templates.md) ·  
PlantUML: [references/plantuml-conventions.md](references/plantuml-conventions.md)

---

## Quando usar

- Extrair árvores de decisão do código / C4 / narrativa e publicar MDs
- Criar pasta `fluxogramas-decisao/` para uma feature
- Atualizar fluxos existentes após mudança de regra
- Separar núcleo do domínio vs consequências / consumidores

**Não usar** para desenhos to-be, ADRs ou C4 puro (use C4 / RFC / code-design).

---

## Artefato (obrigatório)

Escrever arquivos no disco — não só colar no chat.

### Onde salvar

1. Path indicado pelo usuário → usar.
2. No `architecture-hub` (ou layout equivalente):

```text
products/{produto}/02-capabilities/{bc}/fluxogramas-decisao/
├── README.md
├── 01-<slug>.md
├── 02-<slug>.md
└── …
```

3. Fora do hub: perguntar o path antes de gravar.

Mapa de paths: `work-hub/skills/references/hub-paths.md`.

Links relativos típicos no README:

- C4: `../../c4/`
- Narrativa / regras: `../….md`

---

## Fluxo de trabalho

```
Progresso:
- [ ] 1. Intake
- [ ] 2. Inventário de fluxos
- [ ] 3. README (mapa + índice)
- [ ] 4. Um MD por fluxo
- [ ] 5. Validar PlantUML (MCP)
- [ ] 6. Cross-links e regras gerais
```

### 1. Intake

Perguntar só o que faltar (máx. 3–5 por turno):

| Campo | Se faltar |
| --- | --- |
| Feature / path | Onde gravar |
| Fontes | Código, C4, narrativa, regras de negócio |
| Escopo | Domínio inteiro ou um fluxo |
| As-is vs to-be | Default: **as-is** |

### 2. Inventário

Listar fluxos pelo **gatilho** e pela **decisão**:

- Um MD = um gatilho/decisão coerente (ex.: “nova assinatura”, “expiração”).
- Não misturar cadastro com relatório se forem decisões distintas.
- Classificar: **compõem** o domínio vs **consequência** / **consome** o dado.

Numeração: `01-`, `02-`… kebab-case; título `# NN — Nome legível`.

### 3. README

Seguir o template em [references/templates.md](references/templates.md):

1. Título: `Fluxogramas de decisão — <Feature> (as-is)`
2. Parágrafo: árvores de regras + PlantUML (decisão + sequência C4)
3. Links: C4, narrativa, feature flags, etc.
4. **Mapa** PlantUML (gatilhos → decisões)
5. Tabela índice: Doc | O que decide | Sequência (componentes C4)
6. Convenção dos diagramas de sequência
7. Núcleo vs consequência
8. Regras gerais (as-is) — bullets curtos; detalhe nos MDs ou doc de regras

### 4. Um MD por fluxo

Ordem das seções (obrigatórias; extras só se agregarem):

| Seção | Conteúdo |
| --- | --- |
| `# NN — Título` | Nome do fluxo |
| `## Descrição do fluxo` | Narrativa + passos numerados; o que **não** faz (com link) |
| `## Entrada / saídas` | Tabela: Entrada, Saídas, Não faz |
| `## Fluxograma de decisão` | PlantUML activity (`start` / `if` / `stop`) |
| `## Diagrama de sequência` | PlantUML sequence alinhado ao C4 |
| `## Regras importantes` | Opcional: bullets das regras finas |
| `## Eventos` | Tabela código/tipo → quando |
| `## Código de referência` | Opcional: classes/métodos fonte |

Vários pares fluxograma/sequência no mesmo arquivo só quando forem
caminhos distintos do **mesmo** tema (ex.: PME ativar vs elegibilidade).

### 5. Validar PlantUML

Usar MCP `user-plantuml` (local — **não** plantuml.com):

1. `GetMcpTools` no servidor se ainda não souber o schema na sessão
2. `check_syntax` em cada `@startuml`…`@enduml`
3. Corrigir até `valid: true`
4. `render_diagram` se o usuário pedir preview visual

Regras de sintaxe: [references/plantuml-conventions.md](references/plantuml-conventions.md).

### 6. Fechar consistência

- README lista todos os MDs; cada MD linka irmãos quando “não faz X”
- Nomes de containers/componentes batem com o C4 da feature
- Eventos citados no texto aparecem na tabela
- Sem inventar regras: se a fonte for ambígua, declarar hipótese no texto

---

## Fontes de verdade (prioridade)

1. Código em produção / comportamento observável
2. C4 do produto (`products/{produto}/04-platform/03-architecture/c4/`)
3. Narrativa / regras de negócio já documentadas
4. Feature flags / contratos

Se código e doc divergirem: documentar o **código** e marcar a divergência.

---

## Tom e estilo

- Português; as-is; sem roadmap disfarçado de documentação
- Preferir nomes de domínio (`company.activated`) a jargão vago
- PlantUML: `skinparam shadowing false`; activity sem acentos em labels se quebrar render
- Sequência: `box` para o container em foco; externos fora do box; `autonumber`

---

## Exemplos de pedido

| Pedido | Ação |
| --- | --- |
| “Cria fluxogramas-decisao do feature X” | Intake → inventário → README + N MDs |
| “Documenta o fluxo de cancelamento” | Um MD (+ atualizar README se novo) |
| “Atualiza 04 com a regra nova do código” | Diff no MD + eventos/regras |
| “Só o mapa do domínio” | README com mapa + índice (MDs depois) |
