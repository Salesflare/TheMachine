---
title: Salesforce
area: connections
summary: Negócios, tarefas e atividade do Salesforce nas suas pessoas e projetos. Se você ativar, ele mantém os dados de contato em dia lá.
covers: connector:salesforce
code: connectors/salesforce.py, crm_sync.py, onboarding.py
site: Connect Salesforce, More sources, Remove, Sign in with Salesforce
---
## O que ele lê

Negócios novos, e negócios que mudam de fase ou de valor. Suas tarefas abertas, ligações e outras tarefas registradas como feitas com notas, e reuniões com descrição. Os últimos 7 dias quando você conecta, e depois as novas a cada 15 minutos.

Cada negócio vira um projeto no seu Graph, e os contatos dele aparecem nas pessoas, como contato do Salesforce na conta delas.

## O que ele pode mudar

Nada, até você ativar **Atualizar dados de contato**. Seu login do Salesforce fica na sua Machine.

## Conectar

Em uma Machine hospedada:

1. Abra sua página de configuração em app.themachine.computer/setup e vá em **Mais fontes**.
2. Abra o Salesforce e clique em **Conectar Salesforce**.
3. Entre no Salesforce e permita a The Machine (feita pela Salesflare).

Ou no painel: **Conexões**, **+ Adicionar**, escolha Salesforce e clique em **Entrar com Salesforce**.

Seu usuário do Salesforce precisa de acesso à API, que a maioria das edições inclui.

## Atualizar dados de contato

Quando sua Machine conhece dados mais novos de um dos seus contatos do Salesforce, ela pode atualizar esse contato lá: cargo, telefone, e o link do LinkedIn se sua org tiver um campo de LinkedIn nos contatos.

1. Em **Conexões**, abra o Salesforce e clique em **Ver o que mudaria**.
2. Confira a lista e clique em **Ativar** ou **Agora não**.

O que ela segue:

- Só dados nas palavras da própria pessoa, como o perfil dela no LinkedIn ou no Slack, ou os que você colocou na página dela. Nunca um palpite.
- Só quando o dado é mais novo que a última mudança do contato no Salesforce. Uma edição feita lá vence.
- Só campos que diferem, e nunca um valor vazio. Ela nunca muda o endereço de email nem a conta.
- Cada mudança é uma linha com data na página da pessoa.

Clique em **Desativar** para parar. Uma conexão que seu Fleet compartilha só lê.

## Remover

- No painel: **Conexões**, abra o Salesforce, **Detalhes** e depois **Desconectar**. O que ele já trouxe fica.
- Em uma Machine hospedada, você também pode clicar em **Remover** ao lado dele na sua página de configuração.

## Revogar no Salesforce

No Salesforce, abra suas configurações pessoais, depois Connected Apps OAuth Usage, ou peça ao seu admin, e revogue a The Machine. Ela não consegue mais ler nem mudar nada.
