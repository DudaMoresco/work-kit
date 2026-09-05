> Preâmbulo compartilhado: [plantuml-preamble.md](../../../references/plantuml-preamble.md)

# Convenções PlantUML — fluxogramas-decisao (as-is)

Alinhado aos MDs em `products/*/01-product/03-discovery/00-as-is/`.

Validar com MCP **`user-plantuml`**: `check_syntax` → corrigir → (opcional) `render_diagram`.
Não usar `https://www.plantuml.com/plantuml`.

---

## Comum a todos os diagramas

```plantuml
@startuml nome-unico-kebab
skinparam shadowing false
' ...
@enduml
```

- Um diagrama por bloco fenced ` ```plantuml `
- Nome do `@startuml` único no arquivo (ex.: `nova-assinatura`, `seq-nova-assinatura`)
- Sem PII, credenciais ou payloads sensíveis nos labels
- Preferir ASCII nos labels se acentos/quebra de linha gerarem warning no MCP

---

## Mapa (README)

```plantuml
@startuml mapa-exemplo
skinparam shadowing false
left to right direction

rectangle "Gatilhos" {
  (Gatilho A) as A
  (Gatilho B) as B
}

(Decisao 1) as D1
A --> D1
@enduml
```

- `left to right direction`
- Gatilhos dentro de `rectangle "Gatilhos"`
- Decisões como ovals `(...)`; setas gatilho → decisão (e entre decisões se houver ordem)

---

## Fluxograma de decisão (activity)

```plantuml
@startuml exemplo-decisao
skinparam shadowing false
start
:Gatilho;

if (Condicao?) then (sim)
  :Acao;
  stop
else (nao)
  :Outra acao;
  stop
endif
@enduml
```

| Elemento | Uso |
| --- | --- |
| `start` / `stop` | Entrada e fim de ramo |
| `:acao;` | Passo / efeito |
| `if (...) then (rotulo)` | Pergunta de negócio (sim/não ou ramos nomeados) |
| `elseif` / `else` | Ramos alternativos |
| `while (...) is (sim)` … `endwhile` | Loop sobre coleção |
| `\n` no texto | Quebra de linha no losango/ação |

**Conteúdo:** só decisões e efeitos de negócio — não detalhar cada chamada HTTP (isso é da sequência).

---

## Diagrama de sequência

```plantuml
@startuml seq-exemplo
skinparam shadowing false
autonumber

actor "Usuario" as User
participant "Sistema externo" as Ext
participant "SNS / SQS" as Msg

box "container-em-foco"
  participant "Adapter In" as In
  participant "Application" as App
  participant "Adapter Out" as Out
end box

participant "PostgreSQL" as PG

User -> Ext: pedido
Ext -> Msg: evento
Msg -> In: consumir
In -> App: use case
App -> Out: porta
Out -> PG: persistir

alt falha
  Note over In: retry / erro de negocio
else sucesso
  Note over App: efeito colateral
end
@enduml
```

| Regra | Detalhe |
| --- | --- |
| `autonumber` | Sempre |
| `box` | Só o container cujo interior importa |
| Fora do box | Outros containers + software systems |
| Mensagens | Intenção de negócio (`processCompanies`, `REB0 include`) |
| `alt` / `opt` / `loop` | Só ramos que mudam a regra |
| `Note over` | Silêncios importantes (“nao alerta”, “flag off”) |

Nomes de participantes = nomes do C4 da feature (Containers + component view citada no MD).

---

## Anti-padrões

- Mermaid no lugar de PlantUML nesta pasta
- Sequência sem `box` quando há componentes internos documentados no C4
- Activity que só repete a sequência passo a passo sem ramificar
- Inventar participantes que não existem no C4/código
- Um único MD gigante com todos os fluxos do domínio (preferir N arquivos + README)
- Inventar path fora de hub-paths (as-is só em `03-discovery/00-as-is/`)
