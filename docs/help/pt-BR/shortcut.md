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

1. No Shortcut, abra Settings, Account, API Tokens e crie um token.
2. Em uma Machine hospedada: abra sua página de configuração em app.themachine.computer/setup, vá em **Mais fontes** e abra Shortcut. No seu próprio computador: **Conexões**, **+ Adicionar**, Shortcut, ou `assistant connect shortcut`.
3. Informe o endereço ou o slug do seu workspace e cole o token. Depois clique em **Conectar**.

## Remover

- No painel: **Conexões**, abra Shortcut, **Detalhes** e depois **Desconectar**. O que ele já trouxe continua.
- Em uma Machine hospedada, você também pode clicar em **Remover** ao lado dele na sua página de configuração.

## Revogar no Shortcut

Exclua o token na mesma página API Tokens.
