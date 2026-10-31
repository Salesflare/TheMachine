---
title: Slack
area: connections
summary: Os canais e as mensagens diretas de que você participa. Envia uma mensagem direta só depois que você aprova.
covers: connector:slack
code: assistant.py, next_actions.py, onboarding.py
site: Connect, More sources, Remove
---
## O que ele lê

As conversas de que você participa: canais, canais privados, mensagens diretas e mensagens em grupo, dos últimos 7 dias quando você conecta, e depois tudo o que for novo. Ele nunca entra em um canal nem abre uma conversa sozinho.

As pessoas aparecem pelo nome e os apps pelo deles, nunca por um ID do Slack. Alguém cuja conta do Slack não existe mais aparece como ex-usuário do Slack.

## O que ele pode enviar

Uma mensagem direta para uma pessoa, em seu nome, e só depois que você aprova na tarefa. Ele nunca publica em um canal.

## Conecte

O Slack é lido pelo Maton, que guarda o login do Slack.

1. Entre em maton.ai, conecte o Slack lá e copie sua chave de API do Maton em Home.
2. Em uma Machine hospedada: abra sua página de configuração em app.themachine.computer/setup, vá até **Mais fontes**, abra o Slack, cole a chave e clique em **Conectar**.
3. No seu próprio computador: rode `assistant connect slack`, ou **Conexões**, **+ Adicionar**, Slack.

## Remova

- No painel: **Conexões**, abra o Slack, **Detalhes** e depois **Desconectar**. O que ele já trouxe continua lá.
- Em uma Machine hospedada, você também pode clicar em **Remover** ao lado dele na sua página de configuração.

## Desinstale no Slack

Remova a conexão do Slack no Maton e exclua a chave de API do Maton que você forneceu. Um admin do Slack também pode remover o app do workspace, em Manage apps.
