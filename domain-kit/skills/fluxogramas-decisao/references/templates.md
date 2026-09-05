# Templates — fluxogramas-decisao

Copiar e preencher. Manter seções na mesma ordem dos exemplos canônicos.

**Path canônico:** `products/{produto}/01-product/03-discovery/00-as-is/`  
Não inventar path fora de [hub-paths.md](../../../references/hub-paths.md).

---

## README.md

```markdown
# Fluxogramas de decisão — <Feature> (as-is)

Árvores de **regras de negócio** do sistema em produção (<contexto curto>),
derivadas do comportamento observável. Diagramas em **PlantUML**:
fluxograma de decisão + diagrama de sequência com **componentes do C4**
(Containers + <ComponentView>). Eventos gerados estão listados em cada fluxo.

**C4:** [`../../c4/`](../../c4/) · **Narrativa:** [`../<doc>.md`](../<doc>.md)

## Mapa

\`\`\`plantuml
@startuml mapa-<feature-slug>
skinparam shadowing false
left to right direction

rectangle "Gatilhos" {
  (<Gatilho A>) as A
  (<Gatilho B>) as B
}

(<Decisão 1>) as D1
(<Decisão 2>) as D2

A --> D1
B --> D2
@enduml
\`\`\`

| Doc | O que decide | Sequência (componentes C4) |
| --- | --- | --- |
| [01 — <Nome>](./01-<slug>.md) | <decisão> | <atores → containers> |
| [02 — <Nome>](./02-<slug>.md) | <decisão> | <atores → containers> |

## Convenção dos diagramas de sequência

- **Box** agrupa componentes internos do container em foco (`<nome-container>`).
- **Containers** externos ao box: listar (SNS/SQS, DBs, serviços irmãos…).
- **Software Systems** externos: listar (Assinatura, Mainframe, Split.io…).

## Núcleo vs consequência

| Tipo | Fluxos |
| --- | --- |
| **Compõem** o domínio | <lista com links> |
| **Consequência** / **Consome** | <lista com links> |

## Regras gerais (as-is)

- <regra transversal 1>
- <regra transversal 2>
```

---

## NN-slug.md (fluxo)

```markdown
# NN — <Título do fluxo>

## Descrição do fluxo

<1–2 parágrafos: quando dispara e o que decide.>

1. <passo>
2. <passo>
3. <passo>

<Opcional: fila, endpoint, cron.>

## Entrada / saídas

| | |
| --- | --- |
| **Entrada** | <gatilho / payload> |
| **Saídas** | <persistência, SNS, eventos> |
| **Não faz** | <fora de escopo + link para outro MD> |

## Fluxograma de decisão

\`\`\`plantuml
@startuml <slug>
skinparam shadowing false
start
:<Gatilho>;

if (<Pergunta de negócio?>) then (nao)
  :<efeito>;
  stop
else (sim)
  :<efeito>;
endif

stop
@enduml
\`\`\`

## Diagrama de sequência

Componentes alinhados ao C4 ([`../../c4/`](../../c4/) — Containers + <View>).

\`\`\`plantuml
@startuml seq-<slug>
skinparam shadowing false
autonumber

participant "<Sistema externo>" as Ext
participant "SNS / SQS" as Msg

box "<container-em-foco>"
  participant "<Adapter In>" as In
  participant "<Application>" as App
  participant "<Adapter Out>" as Out
end box

participant "<DB / parceiro>" as Dep

Ext -> Msg: <evento>
Msg -> In: <handler>
In -> App: <use case>
App -> Out: <porta>
Out -> Dep: <chamada>
@enduml
\`\`\`

## Regras importantes

- <regra fina 1>
- <regra fina 2>

## Eventos

| Código / tipo | Quando |
| --- | --- |
| `<code>` | <condição> |
```

---

## Checklist rápido por MD

- [ ] Título numerado e slug alinhados ao README
- [ ] Entrada / Saídas / Não faz preenchidos
- [ ] Activity cobre todos os ramos da regra (não só happy path)
- [ ] Sequência usa nomes do C4; box no container certo
- [ ] Tabela de eventos completa para o que o texto cita
- [ ] PlantUML passa em `check_syntax`
