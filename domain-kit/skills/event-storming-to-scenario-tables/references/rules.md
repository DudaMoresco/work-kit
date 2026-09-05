# Regras — event-storming-to-scenario-tables

Conhecimento detalhado da skill. O orquestrador está em [../SKILL.md](../SKILL.md).
Não deletar regras daqui sem migrá-las de volta à skill ou a outro reference.

Mapa de paths: [../../../references/hub-paths.md](../../../references/hub-paths.md).

---

# 3. Conceitos usados

## Funcionalidade

Uma capacidade de produto ou sistema que entrega valor ou executa um processo relevante.

Exemplos:

- Criar conta
- Ativar assinatura premium
- Monitorar dados vazados
- Adicionar e-mail para monitoramento
- Remover elemento de identidade
- Cancelar assinatura
- Notificar usuário

A funcionalidade deve representar um fluxo manipulável e compreensível.

## Cenário principal

É o fluxo esperado, feliz ou mais representativo da funcionalidade.

O cenário principal deve aparecer diretamente abaixo da descrição da funcionalidade, em formato de tabela.

## Cenário alternativo

É uma variação do cenário principal.

Pode representar:

- erro;
- exceção;
- validação negativa;
- caminho alternativo de negócio;
- compensação;
- continuidade para outro fluxo;
- caso sem dados;
- caso duplicado;
- caso não autorizado.

Cenários alternativos devem ser descritos abaixo da tabela principal, sempre indicando de qual etapa partem.

Formato obrigatório:

```md
## Cenários alternativos

### Início etapa [n] - [Nome do cenário alternativo]
```

## Evento

Algo que aconteceu no domínio.

Exemplos:

- Conta criada
- Usuário validado
- Pagamento aprovado
- Monitoramento ativado
- Dados vazados encontrados
- Notificação enviada

Eventos devem preferencialmente ser escritos no passado.

## Comando

Uma intenção ou ação que dispara mudança no sistema.

Exemplos:

- Criar conta
- Validar usuário
- Ativar monitoramento
- Gerar relatório inicial
- Enviar notificação
- Remover elemento de identidade

Comandos devem preferencialmente ser escritos no infinitivo.

## Ator

Pessoa, sistema externo, job, automação, serviço ou política que dispara um comando.

Exemplos:

- Usuário
- Cliente
- Administrador
- Sistema
- Scheduler
- IMARS
- POL-001

Se o comando for gerado por uma política, o ator deve ser o código da política.

## Política

Regra reutilizável que explica uma decisão, reação, validação, automação, integração, notificação, compensação ou operação de dados.

Políticas podem e devem ser reutilizadas quando representarem a mesma regra de negócio.

Uma política não precisa ficar presa a um único cenário. Ela pode aparecer em várias funcionalidades.

---

# 4. Entrada visual e SVG

Esta skill deve funcionar especialmente bem com SVGs exportados de ferramentas como draw.io, Miro, Whimsical, Lucidchart ou similares.

## Processo para SVG

Ao receber SVG:

1. Abrir e inspecionar o SVG.
2. Extrair textos acessíveis em:
   - `<text>`
   - `<tspan>`
   - `<title>`
   - `<desc>`
   - conteúdo HTML embutido
3. Identificar formas, cores, agrupamentos, setas e proximidade visual.
4. Inferir a função dos elementos com cautela:
   - eventos
   - comandos
   - políticas
   - atores
   - sistemas externos
   - perguntas
   - observações
5. Reconstruir os fluxos em funcionalidades.
6. Preservar os nomes originais sempre que possível.
7. Marcar inferências visuais como Hipótese visual.
8. Não inventar fluxo que não exista no diagrama.

## Limitações com SVG

Se o SVG não possuir texto acessível, a skill deve registrar a limitação.

Não fingir precisão quando:

- textos foram convertidos em paths;
- textos estão ilegíveis;
- setas não têm direção clara;
- há sobreposição de elementos;
- o diagrama depende de legenda ausente;
- partes do fluxo estão cortadas.

Nesses casos, registrar em Perguntas em aberto ou Limitações da leitura.

---

# 5. Regras obrigatórias

1. A saída deve ser organizada por funcionalidade.
2. Não exigir nem criar obrigatoriamente coluna de contexto.
3. Sempre gerar uma tabela consolidada de políticas.
4. A tabela consolidada de políticas deve conter apenas:
   - código
   - categoria
   - descrição da política
   - observações
5. As políticas devem possuir código único no formato:
   - POL-001
   - POL-002
   - POL-003
6. Políticas podem ser reutilizadas em múltiplas funcionalidades.
7. Não criar política duplicada quando uma política existente representar a mesma regra.
8. Toda funcionalidade deve possuir:
   - código
   - nome
   - descrição
   - tabela principal
   - cenários alternativos, quando existirem
9. Os códigos de funcionalidade devem seguir o formato:
   - FUN-001
   - FUN-002
   - FUN-003
10. A tabela principal da funcionalidade deve conter:
    - etapa
    - ator
    - comando
    - evento
    - observações
11. Cenários alternativos devem ser representados abaixo da tabela principal.
12. Cenários alternativos devem indicar:
    - etapa de início;
    - nome claro do cenário alternativo;
    - tabela com etapa, ator, comando, evento e observações.
13. Não usar colunas Caminho, Condição / Gatilho ou Próxima etapa.
14. Não criar tabelas separadas chamadas Fluxos alternativos.
15. Usar o título Cenários alternativos.
16. Se o ator de uma etapa não estiver explícito, mas o comando for gerado por política, preencher o ator com o código da política.
17. Se o ator não estiver explícito e não houver política associada, preencher com `ATOR_NAO_IDENTIFICADO`.
18. Se o próximo passo for uma funcionalidade já mapeada, não duplicar essa funcionalidade inteira.
19. Quando houver continuidade em outra funcionalidade, registrar na coluna Observações:
    - `Continuar leitura em: FUN-XXX - [Nome da funcionalidade]`
20. Não inventar atores, comandos, eventos, políticas ou funcionalidades sem marcar como hipótese.
21. Preservar a linguagem do domínio fornecida no diagrama.
22. Consolidar políticas duplicadas ou equivalentes.
23. Quando políticas forem parecidas mas tiverem regras diferentes, manter políticas separadas.
24. Quando um evento disparar múltiplos comandos, usar políticas separadas, exceto quando o diagrama indicar uma política orquestradora única.
25. Quando um comando puder gerar eventos alternativos, representar o resultado principal na tabela principal e os demais resultados em cenários alternativos.
26. A tabela deve ser fácil de manipular em planilhas, evitando células excessivamente longas quando possível.

---

# 6. Reutilização de políticas

Políticas devem ser modeladas como regras reutilizáveis.

Não criar uma nova política apenas porque a mesma regra apareceu em outra funcionalidade.

## Exemplo

Se e-mail, telefone e passaporte usam a mesma regra:

Para adicionar um elemento de identidade ao monitoramento, o usuário deve ser premium, existir no IMARS e possuir monitoramento ativo.

Criar apenas uma política:

| Código | Categoria | Descrição da política | Observações |
|---|---|---|---|
| POL-010 | Segurança | Para adicionar um elemento de identidade ao monitoramento, o usuário deve ser premium, existir no IMARS e possuir monitoramento ativo. | Reutilizada em e-mail, telefone e passaporte. |

E usar POL-010 como ator nas funcionalidades correspondentes.

---

# 7. Categorias de políticas

Classifique cada política em uma das categorias abaixo:

- Automação
- Validação
- Integração
- Segurança
- Notificação
- Compensação
- Orquestração
- Temporal
- Dados
- Manual
- Hipótese

## Critério de categorização

Use:

- `Automação` quando uma reação automática transforma evento em comando.
- `Validação` quando a política verifica regra, consistência, elegibilidade ou duplicidade.
- `Integração` quando envolve sistema externo, API, fornecedor ou cliente externo.
- `Segurança` quando envolve autenticação, autorização, permissão, fraude ou controle de acesso.
- `Notificação` quando o comando gerado comunica usuário, time técnico ou sistema.
- `Compensação` quando desfaz, cancela, remove, corrige ou reverte algo.
- `Orquestração` quando coordena múltiplas etapas ou funcionalidades.
- `Temporal` quando depende de agenda, prazo, recorrência, expiração ou job.
- `Dados` quando armazena, consulta, cruza, filtra, atualiza ou remove dados.
- `Manual` quando depende de decisão ou ação humana.
- `Hipótese` quando a categoria não estiver clara.

---

# 8. Regras para tabela principal da funcionalidade

Cada funcionalidade deve ter uma tabela principal com o seguinte formato:

```md
# Funcionalidade: FUN-001 - [Nome da funcionalidade]

## Descrição

[Descrição clara da funcionalidade.]

| Etapa | Ator | Comando | Evento | Observações |
| --- | --- | --- | --- | --- |
| 1 | [Ator] | [Comando] | [Evento] | [Observações] |
```

## Regras da tabela principal

- A tabela principal deve representar o fluxo principal da funcionalidade.
- Etapas devem ser numéricas e sequenciais.
- A coluna Ator deve conter pessoa, sistema, job, automação, serviço ou código de política.
- A coluna Comando deve conter a ação executada.
- A coluna Evento deve conter o resultado da ação.
- A coluna Observações deve conter:
  - hipóteses;
  - regras relevantes;
  - endpoints;
  - limites;
  - continuação para outra funcionalidade;
  - dúvida ou lacuna;
  - indicação de fluxo encerrado.
- Se não houver observação, deixar a célula vazia.

---

# 9. Regras para cenários alternativos

Cenários alternativos devem aparecer abaixo da tabela principal da funcionalidade.

Formato obrigatório:

```md
## Cenários alternativos

### Início etapa [n] - [Nome do cenário alternativo]

| Etapa | Ator | Comando | Evento | Observações |
| --- | --- | --- | --- | --- |
| [n] | [Ator] | [Comando] | [Evento alternativo] | [Observações] |
```

## Regras dos cenários alternativos

- Sempre indicar `Início etapa [n]`.
- O número da primeira etapa do cenário alternativo deve ser o mesmo da etapa onde o fluxo alternativo nasce.
- O cenário alternativo deve reescrever a etapa que mudou e seguir com as etapas específicas daquele caminho.
- Não usar A1, B1, C1.
- Não usar coluna Caminho.
- Não usar coluna Condição / Gatilho.
- Não usar coluna Próxima etapa.
- O nome do cenário alternativo deve deixar claro o que mudou.

Exemplos:

```md
### Início etapa 4 - Erro na criação do membro IMARS
### Início etapa 6 - Não existem dados vazados para notificação
### Início etapa 3 - Usuário não autorizado
```

Quando o cenário alternativo terminar, indicar em Observações:

- `Fluxo encerrado`
- `Fluxo encerrado com alerta`
- `Continuar leitura em: FUN-XXX - [Nome da funcionalidade]`

Quando o cenário alternativo voltar ao fluxo principal, indicar em Observações:

- `Continua no fluxo principal a partir da etapa X`

---

# 10. Continuidade entre funcionalidades

Quando um fluxo continuar em outra funcionalidade já mapeada:

- Não duplicar a funcionalidade de destino.
- Registrar a continuação na coluna Observações.
- Usar o formato:
  - `Continuar leitura em: FUN-XXX - [Nome da funcionalidade]`

Exemplo:

| 4 | POL-018 | Enviar usuário para o fluxo de cancelamento de fluxo de dados vazados | Usuário enviado para o fluxo de cancelamento | Continuar leitura em: FUN-003 - Cancelar monitoramento premium |

---

# 11. Processo de execução

Ao receber um Event Storming visual:

1. Identificar o formato da entrada.
2. Se for SVG ou imagem, extrair textos, formas, cores, agrupamentos e setas.
3. Identificar a legenda visual, se existir.
4. Separar elementos por funcionalidade provável.
5. Identificar o fluxo principal de cada funcionalidade.
6. Identificar cenários alternativos, erros e compensações.
7. Extrair eventos.
8. Extrair comandos.
9. Extrair atores.
10. Extrair políticas explícitas.
11. Inferir políticas implícitas somente quando houver evidência clara de que um evento dispara um comando.
12. Consolidar políticas equivalentes e reutilizáveis.
13. Atribuir códigos às políticas.
14. Categorizar políticas.
15. Montar a tabela consolidada de políticas no formato simplificado.
16. Montar a lista de funcionalidades identificadas.
17. Para cada funcionalidade, montar:
    - título;
    - descrição;
    - tabela principal;
    - cenários alternativos.
18. Usar o código da política como ator quando a política gerar o comando.
19. Identificar continuidades entre funcionalidades.
20. Registrar continuidade na coluna Observações.
21. Listar comandos sem ator identificado.
22. Listar limitações da leitura.
23. Listar perguntas em aberto.
24. Revisar consistência antes de finalizar.

---

# 12. Formato obrigatório da resposta

A resposta deve seguir exatamente esta estrutura:

# Conversão do Diagrama Event Storming para Tabelas Descritivas

## 1. Premissas, hipóteses e limitações da leitura

Liste premissas, hipóteses visuais e limitações relevantes.

Se não houver, escreva:

"Nenhuma premissa, hipótese ou limitação adicional identificada."

## 2. Funcionalidades identificadas

| Código | Funcionalidade | Descrição | Observações |
|---|---|---|---|

Regras:

- Usar códigos:
  - FUN-001
  - FUN-002
  - FUN-003
- A descrição deve ser curta e clara.
- Se a funcionalidade foi inferida visualmente, marcar em observações.

## 3. Tabela consolidada de políticas

| Código | Categoria | Descrição da política | Observações |
|---|---|---|---|

Regras:

- Ordenar por código da política.
- Cada política deve representar uma regra reutilizável sempre que possível.
- Não criar uma nova política se uma política existente já representa a mesma regra.
- Políticas reutilizáveis devem ser referenciadas em múltiplas funcionalidades usando o mesmo código.
- A descrição da política deve ser clara o suficiente para explicar:
  - quando a política se aplica;
  - qual regra ela representa;
  - qual consequência ela gera.
- A descrição não precisa ser separada em evento, condição e comando.
- A coluna Observações pode conter:
  - endpoints;
  - limites;
  - exceções;
  - hipóteses;
  - informação de reutilização;
  - funcionalidades onde a política é usada.
- Usar `Hipótese` ou `Hipótese visual` em observações quando aplicável.

## 4. Tabelas por funcionalidade

Para cada funcionalidade, usar:

```md
# Funcionalidade: [Código] - [Nome da funcionalidade]

## Descrição

[Descrição objetiva da funcionalidade.]

| Etapa | Ator | Comando | Evento | Observações |
|---|---|---|---|---|
```

Se existirem cenários alternativos, adicionar abaixo da tabela principal:

```md
## Cenários alternativos

### Início etapa [n] - [Nome do cenário alternativo]

| Etapa | Ator | Comando | Evento | Observações |
|---|---|---|---|---|
```

Regras:

- Não criar seção de cenários alternativos se não houver cenários alternativos.
- Etapas numéricas e sequenciais.
- Não usar etapas como A1, B1, C1.
- O cenário alternativo começa com a mesma etapa onde a variação nasce.
- O ator deve ser uma pessoa, papel, sistema externo, job, serviço ou código de política.
- Se o comando for gerado por política, usar o código da política como ator.
- Se não houver ator nem política, usar `ATOR_NAO_IDENTIFICADO`.
- Eventos devem estar no passado.
- Comandos devem estar preferencialmente no infinitivo.
- Quando continuar em outra funcionalidade, registrar em Observações:
  - `Continuar leitura em: FUN-XXX - [Nome da funcionalidade]`

## 5. Mapa de continuidade entre funcionalidades

| Funcionalidade origem | Evento de transição | Continuar em funcionalidade | Observação |
|---|---|---|---|

Use esta tabela para deixar explícito quando a leitura de um fluxo deve continuar em outra funcionalidade.

Se não houver continuidade entre funcionalidades, preencher:

| Funcionalidade origem | Evento de transição | Continuar em funcionalidade | Observação |
|---|---|---|---|
| N/A | N/A | N/A | Nenhuma continuidade identificada |

## 6. Comandos sem ator identificado

| Funcionalidade | Etapa | Comando | Evento resultante | Observação |
|---|---|---:|---|---|

Liste apenas comandos cujo ator ficou como `ATOR_NAO_IDENTIFICADO`.

Se não houver comandos sem ator identificado, preencher:

| Funcionalidade | Etapa | Comando | Evento resultante | Observação |
|---|---|---:|---|---|
| N/A | N/A | N/A | N/A | Nenhum comando sem ator identificado |

## 7. Perguntas em aberto

Liste ambiguidades, lacunas e decisões pendentes.

Se não houver perguntas em aberto, escreva:

"Nenhuma pergunta em aberto identificada."

---

# 13. Regras de consistência final

Antes de finalizar, validar:

- Toda funcionalidade possui código, nome e descrição.
- Toda funcionalidade possui tabela principal.
- Toda tabela principal possui as colunas obrigatórias:
  - Etapa
  - Ator
  - Comando
  - Evento
  - Observações
- Nenhuma tabela usa as colunas:
  - Caminho
  - Condição / Gatilho
  - Próxima etapa
- Toda ramificação foi representada como cenário alternativo com `Início etapa [n]`.
- Nenhuma tabela separada de Fluxos alternativos foi criada.
- Todo comando possui ator, política ou `ATOR_NAO_IDENTIFICADO`.
- Toda política possui:
  - código
  - categoria
  - descrição da política
  - observações
- Políticas reutilizáveis não foram duplicadas.
- Toda continuidade entre funcionalidades aparece no mapa de continuidade.
- Nenhuma funcionalidade já mapeada foi duplicada desnecessariamente.
- Todas as hipóteses visuais foram marcadas.
- Todas as ambiguidades relevantes foram registradas.
- Nenhuma relação entre comando e evento foi criada sem evidência textual ou visual.
- A saída está fácil de copiar para planilha.

---

# 14. Exemplo de saída reduzido

Veja [examples.md](examples.md) para um exemplo completo de saída reduzido.

---

# 15. Prompt recomendado para uso

Use este prompt quando quiser aplicar a skill:

```
Use a skill event-storming-to-scenario-tables.

Converta o diagrama visual de Event Storming abaixo em tabelas descritivas.

Regras obrigatórias:
- Não foque em bounded contexts nesta etapa.
- Foque em funcionalidades.
- Gere uma tabela consolidada com políticas reutilizáveis.
- A tabela de políticas deve conter apenas:
  - código
  - categoria
  - descrição da política
  - observações
- Políticas podem ser reutilizadas em várias funcionalidades.
- Não duplique políticas que representam a mesma regra.
- Gere tabelas por funcionalidade.
- Cada funcionalidade deve ter uma tabela principal com:
  - etapa
  - ator
  - comando
  - evento
  - observações
- Não use as colunas:
  - caminho
  - condição / gatilho
  - próxima etapa
- Cenários alternativos devem aparecer abaixo da tabela principal.
- Cada cenário alternativo deve indicar:
  - Início etapa [n] - [Nome do cenário alternativo]
- Se não houver ator, use o código da política que gera o comando.
- Se não houver ator nem política, use ATOR_NAO_IDENTIFICADO.
- Se o próximo passo for uma funcionalidade já mapeada, indique em observações:
  - Continuar leitura em: FUN-XXX - [Nome da funcionalidade]
- Se a entrada for SVG, extraia primeiro os textos, agrupamentos, setas e relações visuais.
- Não invente elementos não presentes no fluxo.
- Marque inferências como hipótese.
- Marque inferências visuais como hipótese visual.

Event Storming:

[cole aqui o fluxo ou indique os arquivos SVG]
```
