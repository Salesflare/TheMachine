---
title: Slack
area: connections
summary: Os canais e as mensagens diretas de que você participa. Envia uma mensagem direta só depois que você aprova.
covers: connector:slack
code: assistant.py, next_actions.py, onboarding.py, slack_api.py
site: Connect, Remove
---
## O que ele lê

As conversas de que você participa: canais, canais privados, mensagens diretas e mensagens em grupo, dos últimos 7 dias quando você conecta, e depois tudo o que for novo. Ele nunca entra em um canal nem abre uma conversa sozinho. Um canal tranquilo é lido mais ou menos uma vez por dia; quando uma tarefa precisa das mensagens mais novas dele, The Machine lê na hora.

As pessoas aparecem pelo nome e os apps pelo deles, nunca por um ID do Slack. Alguém cuja conta do Slack não existe mais aparece como ex-usuário do Slack.

## O que ele pode enviar

Uma mensagem direta para uma pessoa, em seu nome, e só depois que você aprova na tarefa. Uma resposta à mensagem do Slack de onde veio uma tarefa vai na thread dessa mensagem, na mensagem direta ou no canal; o rascunho diz **Na thread**. Ele nunca começa uma publicação nova em um canal.

## Conecte

1. **Conexões**, **+ Adicionar**, **Slack**, depois **Entrar com Slack**, e permita no Slack. No seu próprio computador, pareie ele antes com sua conta em themachine.computer.
2. Mensagens novas e mensagens diretas chegam primeiro. O Slack deixa os apps lerem mais ou menos uma conversa por minuto, então as mensagens antigas chegam ao longo de algumas horas.

Ou use uma chave de API do Maton: entre em maton.ai, conecte o Slack lá e copie sua chave de API do Maton em Home. Depois abra **Ou use uma chave de API do Maton** embaixo do Slack e cole, ou rode `assistant connect slack` no seu próprio computador. Um Slack conectado pelo Maton continua funcionando como está.

## Remova

- No painel: **Conexões**, abra o Slack, **Detalhes** e depois **Desconectar**. O que ele já trouxe continua lá.
- Em uma Machine hospedada, você também pode clicar em **Remover** ao lado dele na sua página de configuração.

## Desinstale no Slack

Com login do Slack: abra a página Manage apps do seu workspace no Slack e remova a The Machine. Pelo Maton: remova a conexão do Slack no Maton e exclua a chave de API do Maton que você forneceu. Um admin do Slack também pode remover qualquer um dos dois apps do workspace, em Manage apps.
