---
title: Salesforce
area: connections
summary: Negócios, tarefas e atividades do Salesforce nos perfis das pessoas e nos projetos. Se você ativar essa opção, a assistente também pode manter os dados de contato atualizados no Salesforce.
covers: connector:salesforce
code: connectors/salesforce.py, crm_sync.py, onboarding.py
site: Connect Salesforce, More sources, Remove, Sign in with Salesforce
translated: eee5e084bac6dbd1
---
## O que ela lê

Novos negócios e negócios que mudam de etapa ou de valor. Suas tarefas em aberto, ligações e outras tarefas marcadas como Feito, com observações, além de reuniões com descrição. Os últimos 7 dias quando você conecta. Depois, novos dados a cada 15 minutos.

Cada negócio vira um projeto no seu Graph, e os contatos associados aparecem nos perfis das pessoas, como contatos do Salesforce na conta delas.

## O que ela pode alterar

Nada, até você ativar **Atualizar dados de contato**. Seu login do Salesforce fica na sua Machine.

## Conectar

Em uma Machine hospedada:

1. Abra sua página de configuração em app.themachine.computer/setup e acesse **Mais fontes**.
2. Abra o Salesforce e clique em **Conectar Salesforce**.
3. Entre no Salesforce e autorize a The Machine (feito pela Salesflare).

Ou, no painel: **Conexões**, **Clientes**, escolha Salesforce e clique em **Entrar com Salesforce**. Se estiver no seu próprio computador, primeiro vincule a Machine à sua conta.

Seu usuário do Salesforce precisa ter acesso à API, incluído na maioria das edições.

## Atualizar dados de contato

Quando sua Machine encontra dados mais recentes sobre um dos seus contatos do Salesforce, ela pode atualizar o contato por lá: cargo, telefone e link do LinkedIn, se sua organização tiver um campo do LinkedIn nos contatos.

1. Em **Conexões**, abra o Salesforce e clique em **Ver o que mudaria**.
2. Confira a lista e clique em **Ativar** ou **Agora não**.

O que ela leva em conta:

- Apenas dados escritos pela própria pessoa, como os do perfil dela no LinkedIn ou no Slack, ou dados que você adicionou à página dela. Ela nunca adivinha.
- Apenas quando o dado é mais recente do que a última alteração do contato no Salesforce. Uma edição feita por lá prevalece.
- Apenas os campos que são diferentes, e nunca um campo vazio. Ela nunca altera o endereço de e-mail nem a conta.
- Cada alteração aparece como uma linha com data na página da pessoa.

Clique em **Desativar** para parar. Uma conexão compartilhada pelo seu Fleet só lê os dados.

## Remover

- No painel: **Conexões**, abra o Salesforce, clique em **Detalhes** e depois em **Desconectar**. Os dados que ela já importou continuam lá.
- Em uma Machine hospedada, **Desconectar ↗** abre sua página de configuração. Clique em **Remover** ao lado do Salesforce.

## Revogar o acesso no Salesforce

No Salesforce, abra suas configurações pessoais e depois Acesso de OAuth a aplicativos conectados. Você também pode pedir ajuda ao administrador. Revogue o acesso da The Machine. Depois disso, ela não poderá mais ler nem alterar dados.
