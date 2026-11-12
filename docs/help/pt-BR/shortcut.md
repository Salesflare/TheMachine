---
title: Shortcut
area: connections
summary: Stories que mudam de estado, com seus responsáveis e prazos. Ele só lê.
covers: connector:shortcut
code: connectors/shortcut.py
site: Connect, More sources, Remove
---
## O que ele lê

Stories no seu workspace do Shortcut que mudam de estado, com seus responsáveis e prazos.

## O que ele pode fazer

Nada no Shortcut. Ele só lê, mesmo que os tokens do Shortcut possam fazer mais.

## Conectar

1. Em uma Machine hospedada: abra sua página de configuração em app.themachine.computer/setup, vá em **Mais fontes** e abra Shortcut. No seu próprio computador: **Conexões**, **+ Adicionar**, Shortcut, ou `assistant connect shortcut`.
2. Clique em **Pegue seu token**. O Shortcut abre a página API Tokens em uma nova aba: crie um token e copie.
3. Cole e clique em **Conectar**. O token é verificado na hora, e você vê como quem e em qual workspace conectou.

Em mais de um workspace do Shortcut? Um token pertence a um só workspace, então troque para ele no Shortcut primeiro.

## Remover

- No painel: **Conexões**, abra Shortcut, **Detalhes** e depois **Desconectar**. O que ele já trouxe continua.
- Em uma Machine hospedada, você também pode clicar em **Remover** ao lado dele na sua página de configuração.

## Revogar no Shortcut

Exclua o token na mesma página API Tokens.
