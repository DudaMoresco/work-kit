# Templates — fluxos (know-how)

No domain-kit, preferir [`../../../templates/fluxo-operacional.md`](../../../templates/fluxo-operacional.md)
em `01-product/03-operacional/fluxos/`. Os templates abaixo servem quando o time
pede sequência PlantUML rica (negócio ou arch).

**Paths:** ver [`../../../wrappers/fluxos-entregaveis.md`](../../../wrappers/fluxos-entregaveis.md).

---

## README.md (mapa opcional)

```markdown
# Fluxos operacionais — <Feature>

Cenários ponta a ponta (camada negócio). Detalhe técnico → `arch/fluxos/`.
Cada MD: cenário de **sucesso** + **alternativos**.
Explicitar **status** e **eventos de domínio**.

Fontes: event-storming, domain stories, bounded-contexts, …

| Campo | Valor |
| --- | --- |
| Momento | To-be (MVP entregável) |
| Última atualização | YYYY-MM-DD |
| Fora de escopo código | <lista curta> |

## Mapa

\`\`\`plantuml
@startuml mapa-fluxos-entregaveis
skinparam shadowing false
left to right direction

rectangle "Gatilhos" {
  (<Gatilho A>) as G1
}

(<01 Fluxo A>) as F1
G1 --> F1
@enduml
\`\`\`

## Índice

| Doc | Gatilho | Serviços de aplicação | ES / tático |
| --- | --- | --- | --- |
| [01 — <Nome>](./01-<slug>.md) | <gatilho> | `<Service>` | ES nn; tático §n |

## Convenção dos diagramas

- Participantes: atores + application services + agregados + **`DomainEvents`**.
- `box "Application"` = orquestração; agregados fora do box.
- Toda sequência: **status** (`De -> Para` ou inalterado) + **publish/on**.
- Alternativos: segundo diagrama com `alt` / `else`.

## Núcleo vs suporte

| Tipo | Fluxos |
| --- | --- |
| **Compõem** o ciclo | … |
| **Suporte** | … |
```

---

## NN-slug.md

```markdown
# NN — <Título>

## Descrição do fluxo

<1–2 parágrafos: quando dispara.>

1. <passo>
2. <passo>

**Não faz:** <fora de escopo + link>.

Fontes: …

## Entrada / saídas

| | |
| --- | --- |
| **Entrada** | … |
| **Saídas** | status finais; eventos publicados; persistência |
| **Não faz** | … |

## Status envolvidos

| Agregado | De | Para | Quando |
| --- | --- | --- | --- |
| OrdemDeServico | EmDiagnostico | AguardandoAprovacao | apos enviar orcamento |

*(Sucesso; nos alternativos, documentar na seção ou no diagrama.)*

## Sequência — cenário de sucesso

\`\`\`plantuml
@startuml seq-NN-sucesso
skinparam shadowing false
autonumber

actor "Ator" as A
participant "Agregado" as Agg

box "Application"
  participant "XxxService" as App
end box

participant "DomainEvents" as Ev

A -> App : comando(...)
App -> Agg : metodoDeDominio()
note over Agg : StatusA -> StatusB
Agg --> App : ok
App -> Ev : publish EventoNoPassado
Ev --> App : on EventoNoPassado
App -> Agg : reacao(...)
note over Agg : StatusB -> StatusC
App --> A : resultado
@enduml
\`\`\`

## Sequência — cenários alternativos

\`\`\`plantuml
@startuml seq-NN-alternativos
skinparam shadowing false
autonumber

' mesmos participantes + DomainEvents

alt <nome do cenario>
  ' status De->Para e publish/on deste ramo
  ' ou note: status inalterado / sem publish
else <outro>
  …
end
@enduml
\`\`\`

## Regras importantes

- …

## Eventos

| Evento | Produzido por | Consumido por | Quando |
| --- | --- | --- | --- |
| `OrcamentoEnviado` | Orcamento / App | OS (via App) | apos enviar() |
| — | — | — | nenhum evento de dominio (se aplicavel) |
```

---

## Checklist rápido por MD

- [ ] Título `NN —` e slug alinhados ao README
- [ ] Tabela Status envolvidos (sucesso)
- [ ] Sequência sucesso: status + publish/on
- [ ] Sequência alternativos: diferenças de status/evento nos `alt`
- [ ] Tabela Eventos alinhada ao PlantUML
- [ ] `check_syntax` ok
