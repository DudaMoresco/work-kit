# Exemplo de saída reduzido

# Conversão do Diagrama Event Storming para Tabelas Descritivas

## 1. Premissas, hipóteses e limitações da leitura

- Hipótese visual: caixas laranja representam eventos.
- Hipótese visual: caixas azuis representam comandos.
- Hipótese visual: caixas azuis claras representam políticas.

## 2. Funcionalidades identificadas

| Código | Funcionalidade | Descrição | Observações |
|---|---|---|---|
| FUN-001 | Ativar monitoramento premium | Ativa o monitoramento de vazamento de dados quando um usuário free adquire assinatura premium. | Inferida visualmente. |

## 3. Tabela consolidada de políticas

| Código | Categoria | Descrição da política | Observações |
|---|---|---|---|
| POL-001 | Automação | Quando um usuário free adquire assinatura premium, o sistema deve iniciar o processo de ativação do monitoramento premium. | Usada em FUN-001. |
| POL-002 | Validação | Para ativar o monitoramento premium, os dados PII do usuário devem ser válidos conforme os limites definidos. | Mínimo nome e sobrenome; máximo 5 e-mails, 3 telefones e 1 passaporte. |
| POL-003 | Integração | Quando um usuário válido precisa ser cadastrado no IMARS, o sistema deve enviar a requisição de criação de membro. | Endpoint IMARS 500. |
| POL-004 | Notificação | Quando ocorrer erro técnico, inconsistência cadastral, falha de integração ou dado inválido em processo crítico, o sistema deve gerar uma notificação de alerta. | Política reutilizável em fluxos de erro. |

## 4. Tabelas por funcionalidade

### Funcionalidade: FUN-001 - Ativar monitoramento premium

#### Descrição

Ativa o monitoramento de vazamento de dados quando um usuário free adquire assinatura premium.

| Etapa | Ator | Comando | Evento | Observações |
|---|---|---|---|---|
| 1 | Usuário free | Adquirir assinatura premium | Usuário adquiriu assinatura premium | |
| 2 | POL-001 | Iniciar processo de ativação de monitoramento do usuário | Pedido de assinatura no monitoramento de dados recebido | |
| 3 | POL-002 | Validar dados do usuário | Usuário válido para cadastro | Validação PII |
| 4 | POL-003 | Enviar requisição de criação do membro iMARS (500) | Membro criado no IMARS | |

#### Cenários alternativos

##### Início etapa 3 - Usuário inválido por PII

| Etapa | Ator | Comando | Evento | Observações |
|---|---|---|---|---|
| 3 | POL-002 | Validar dados do usuário | Usuário invalidado por PII | Dados não atendem critérios mínimos/máximos. |
| 4 | POL-004 | Gerar notificação de alerta | Notificação de alerta enviada | Fluxo encerrado com alerta. |

##### Início etapa 4 - Erro na criação do membro IMARS

| Etapa | Ator | Comando | Evento | Observações |
|---|---|---|---|---|
| 4 | POL-003 | Enviar requisição de criação do membro iMARS (500) | Erro na criação do membro no IMARS | |
| 5 | POL-004 | Gerar notificação de alerta | Notificação de alerta enviada | Fluxo encerrado com alerta. |

## 5. Mapa de continuidade entre funcionalidades

| Funcionalidade origem | Evento de transição | Continuar em funcionalidade | Observação |
|---|---|---|---|
| N/A | N/A | N/A | Nenhuma continuidade identificada |

## 6. Comandos sem ator identificado

| Funcionalidade | Etapa | Comando | Evento resultante | Observação |
|---|---|---:|---|---|
| N/A | N/A | N/A | N/A | Nenhum comando sem ator identificado |

## 7. Perguntas em aberto

- O alerta técnico deve ser enviado para qual canal?
