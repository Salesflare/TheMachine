---
title: Slack
area: connections
summary: Os canais e as mensagens diretas de que você participa. Só envia uma mensagem direta depois da sua aprovação.
covers: connector:slack
code: assistant.py, next_actions.py, onboarding.py, slack_api.py
site: Connect, Remove
translated: 23f9e98f4680d23c
---
## O que ela lê

As conversas das quais você participa: canais, canais privados, mensagens diretas e mensagens em grupo. Ela lê as dos últimos 7 dias quando você conecta e, depois, tudo o que chegar de novo. Nunca entra em um canal nem abre uma conversa por conta própria. Um canal sem atividade é lido aproximadamente uma vez por dia. Quando uma tarefa precisa das mensagens mais recentes, The Machine lê o canal na hora.

As mensagens antigas de cerca de um ano são carregadas depois, aos poucos, como [histórico](history.md).

As pessoas aparecem pelo nome e os apps, pelo nome deles, nunca por um ID do Slack. Se a conta de alguém no Slack foi removida, essa pessoa aparece como ex-usuário do Slack.

## O que ela pode enviar

Uma mensagem direta para uma pessoa, em seu nome, e somente depois que você aprovar a tarefa. A resposta à mensagem do Slack que originou uma tarefa aparece na thread dessa mensagem, na conversa direta ou no canal. O rascunho mostra **Na thread**. The Machine nunca inicia uma nova publicação em um canal.

## O que ela guarda

O que The Machine lê fica na sua Machine até você excluir o conteúdo ou a Machine. O serviço de hospedagem não guarda cópias das suas mensagens nem seus dados de acesso ao Slack, e nenhum modelo de IA é treinado com seus dados do Slack. The Machine usa IA, que pode cometer erros, então você vê cada mensagem antes que ela seja enviada.

## Conectar

1. **Conexões**, **Chat**, **Slack** e depois **Entrar com o Slack**. Em seguida, autorize o acesso no Slack. Se estiver usando seu próprio computador, primeiro pareie a Machine com sua conta em themachine.computer.
2. As mensagens novas e as mensagens diretas chegam primeiro. O Slack permite que os apps leiam cerca de uma conversa por minuto, então as mensagens antigas são carregadas ao longo de algumas horas.

Ou use uma chave de API do Maton: entre em maton.ai, conecte o Slack por lá e copie sua chave de API do Maton na página Home. Depois, abra **Ou use uma chave de API do Maton** em Slack e cole a chave, ou execute `assistant connect slack` no seu próprio computador. Uma conexão do Slack feita pelo Maton continua funcionando normalmente.

## Remover

- No painel: **Conexões**, abra Slack, selecione **Detalhes** e depois **Desconectar**. O que já foi importado continua lá.
- Em uma Machine hospedada, você também pode selecionar **Remover** ao lado da conexão na página de configuração.

## Desinstalar no Slack

Se você entrou com o Slack: abra a página Manage apps do seu workspace no Slack e remova The Machine. A leitura para na hora e você precisará entrar novamente. O que já foi importado continua lá. Se você conectou pelo Maton: remova a conexão do Slack no Maton e exclua a chave de API do Maton que você forneceu. Um administrador do Slack também pode remover qualquer um dos apps do workspace, em Manage apps.
