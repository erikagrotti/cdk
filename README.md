# Desafio Serverless

O desafio envolveu criar um sistema de gerenciamento de tarefas usando AWS: API Gateway para a API, Lambda para executar funções em Python, DynamoDB como banco de dados NoSQL, e Cognito para autenticar usuários.

## Preparado Por:
Érika Alves Grotti

## Desenvolvido em:
Junho, 2024

## Sumário
- [Visão Geral do Projeto](#visão-geral-do-projeto)
  - [Resumo](#resumo)
  - [Pré-requisitos e Limitações](#pré-requisitos-e-limitações)
- [Implementação](#implementação)
  - [Arquitetura da Solução](#arquitetura-da-solução)
  - [Metodologia](#metodologia)
- [Instruções Sobre o Projeto](#instruções-sobre-o-projeto)
  - [Introdução](#introdução)
  - [Endpoints](#endpoints)
  - [Infraestrutura](#infraestrutura)
  - [Configuração do Ambiente](#configuração-do-ambiente)

## Visão Geral do Projeto

### Resumo
O desafio propôs o desenvolvimento de um sistema de gerenciamento de tarefas, utilizando serviços e componentes da Amazon Web Services (AWS): API Gateway, Lambda, DynamoDB, e Cognito. O API Gateway cria a API para disponibilizar as rotas necessárias, o Lambda executa funções em Python nas rotas, o DynamoDB, um banco de dados NoSQL, armazena as listas de tarefas e o Cognito gerencia a autenticação dos usuários.

### Pré-requisitos e Limitações

#### Pré-requisitos
- Conta na AWS
- Conhecimento prévio de serviços AWS

#### Limitações
-  Excelente Conectividade com a Internet

## Implementação

### Arquitetura da Solução
A arquitetura AWS utilizada neste projeto inclui os seguintes componentes:

- **Amazon API Gateway**: Gerencia e protege o acesso às APIs.
- **AWS Lambda**: Serviço de computação sem servidor que executa o código sob demanda.
- **Amazon DynamoDB**: Banco de dados NoSQL para armazenar dados estruturados.
- **AWS Cognito**: Serviço para autenticação e gerenciamento de usuários.

Essa arquitetura demonstra a integração de diversos serviços AWS para construir uma aplicação robusta, escalável e segura.

### Metodologia
1. Estudo dos serviços AWS.
2. Clonagem do repositório no GitHub.
3. Instalação de dependências.
4. Configuração de variáveis de ambiente.
5. Implementação da aplicação.

## Instruções Sobre o Projeto

### Introdução
Esta API permite a disponibilização e gerenciamento de rotas para atender os requisitos do manuseio de uma lista de tarefas.

### Endpoints

#### URL Base
https://dc0y8bcyu5.execute-api.us-east-1.amazonaws.com/


#### POST /items
- **Resumo**: Gera uma lista de tarefas.
- **Corpo da Requisição**:
  - `listID` (obrigatório): ID da lista de tarefa.
  - `taskID` (obrigatório): Sort Key.
  - `title` (obrigatório): Nome da tarefa a ser realizada.
  - `description` (opcional): Descrição da tarefa.
  - `participants` (opcional): Participantes da tarefa.
- **Respostas**:
  - `200`: Resposta gerada com sucesso.
  - `400`: Solicitação inválida, como campos obrigatórios ausentes ou JSON inválido.
  - `500`: Erro interno do servidor, como falha na geração de resposta.

#### GET /items
- **Resumo**: Lista todas as listas de tarefas existentes.
- **Respostas**:
  - `200`: Operação bem-sucedida.
  - `500`: Erro interno do servidor, indicando falha no processamento da solicitação.

#### GET /items/{listID}
- **Resumo**: Lista todas as tarefas de uma lista específica.
- **Respostas**:
  - `200`: Operação bem-sucedida.
  - `500`: Erro interno do servidor, indicando falha no processamento da solicitação.

#### GET /items/{listID}/{taskID}
- **Resumo**: Lista uma tarefa específica de uma lista.
- **Respostas**:
  - `200`: Operação bem-sucedida.
  - `500`: Erro interno do servidor, indicando falha no processamento da solicitação.

#### PATCH /items/{listID}/status
- **Resumo**: Atualiza o status de uma lista de tarefas.
- **Corpo da Requisição**:
  - `status` (obrigatório): Novo status da lista.
- **Respostas**:
  - `200`: Resposta gerada com sucesso.
  - `400`: Solicitação inválida, como campos obrigatórios ausentes ou JSON inválido.
  - `500`: Erro interno do servidor, como falha na geração de resposta.

#### PATCH /items/{listID}/{taskID}/status
- **Resumo**: Atualiza o status de uma tarefa específica.
- **Corpo da Requisição**:
  - `status` (obrigatório): Novo status da tarefa.
- **Respostas**:
  - `200`: Resposta gerada com sucesso.
  - `400`: Solicitação inválida, como campos obrigatórios ausentes ou JSON inválido.
  - `500`: Erro interno do servidor, como falha na geração de resposta.

#### PATCH /items/{listID}/T000/status
- **Resumo**: Atualiza o status de uma tarefa pai.
- **Corpo da Requisição**:
  - `status` (obrigatório): Novo status da tarefa pai.
- **Respostas**:
  - `200`: Resposta gerada com sucesso.
  - `400`: Solicitação inválida, como campos obrigatórios ausentes ou JSON inválido.
  - `500`: Erro interno do servidor, como falha na geração de resposta.

#### PATCH /items/{listID}
- **Resumo**: Atualiza o título de uma lista de tarefas.
- **Corpo da Requisição**:
  - `title` (obrigatório): Novo título da lista.
- **Respostas**:
  - `200`: Resposta gerada com sucesso.
  - `400`: Solicitação inválida, como campos obrigatórios ausentes ou JSON inválido.
  - `500`: Erro interno do servidor, como falha na geração de resposta.

#### DELETE /items/{listID}
- **Resumo**: Exclui uma lista de tarefas.
- **Respostas**:
  - `200`: Operação bem-sucedida.
  - `500`: Erro interno do servidor, indicando falha no processamento da solicitação.

#### DELETE /items/{listID}/{taskID}
- **Resumo**: Exclui uma tarefa específica de uma lista.
- **Respostas**:
  - `200`: Operação bem-sucedida.
  - `500`: Erro interno do servidor, indicando falha no processamento da solicitação.

### Configuração do Ambiente
Para configurar o ambiente, adicione suas credenciais da AWS no arquivo de ambiente conforme o exemplo abaixo:

```typescript
export const environment = {
  production: false,
  aws: {
    region: '',
    userPoolId: '',
    clientId: '',
    apiUrl: ''
  }
};
