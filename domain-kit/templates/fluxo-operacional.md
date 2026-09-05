# Fluxo operacional — {titulo}

> Camada **negócio** (domain-kit). Detalhe técnico (serviços, filas, payloads) fica **fora do escopo do domain-kit**.

## Sumário

> **Por que esta seção:** ancora o fluxo (ID, BC, ator, sucesso) para navegação e registry sem reler o cenário.

| Campo | Valor |
| --- | --- |
| ID | fluxo-{NN} |
| Bounded context | {bc} |
| Ator principal | |
| Métrica de sucesso | |

## Pré-condições

> **Por que esta seção:** deixa explícito o que precisa ser verdade antes do cenário — evita ambiguidade de gatilho.

- 

## Cenário principal

> **Por que esta seção:** descreve o caminho feliz em linguagem ubíqua (Dado/Quando/Então) como contrato de negócio.

1. **Dado** que …
2. **Quando** …
3. **Então** …

## Exceções de negócio

> **Por que esta seção:** documenta ramificações esperadas pelo negócio sem misturar detalhe técnico.

| Situação | Comportamento esperado |
| --- | --- |
| | |

## Eventos de domínio (linguagem ubíqua)

> **Por que esta seção:** amarra o fluxo aos eventos nomeados na UL / Event Storming.

| Evento | Significado |
| --- | --- |
| | |

## Notas as-is (opcional)

> **Por que esta seção:** guarda referência legado sem contaminar o contrato to-be.

Referências técnicas legadas — não fazem parte do contrato de produto:

- 

## Referências

> **Por que esta seção:** aponta fontes canônicas (UL, stories, decisões) para rastreio.

- `01-product/02-domain/linguagem-ubiqua.md`
- Domain story relacionada: 
