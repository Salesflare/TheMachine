---
title: Google Meet
area: connections
summary: Transcrições e notas do Gemini das reuniões do Meet que você organiza. Ele só lê.
covers: connector:google_meet
code: connectors/google_meet.py
site: Connect, More sources, Remove
---
## O que ele lê

Transcrições e notas do Gemini das reuniões do Google Meet que você organizou, assim que o Meet as cria: os últimos 7 dias quando você conecta, depois as novas conforme chegam. O Meet as guarda por 30 dias.

O Meet só as cria quando transcrições ou notas do Gemini estavam ativadas durante a reunião.

## O que ele pode fazer

Nada no Meet ou no Drive. Ele só lê e nunca ativa transcrições por conta própria.

## Conectar

1. No Google Cloud, ative a API do Google Meet e a API do Google Drive.
2. No OAuth Playground, obtenha um token de acesso com os dois escopos somente leitura mostrados na tela de conexão.
3. Em uma Machine hospedada: abra sua página de configuração em app.themachine.computer/setup, vá em **Mais fontes** e abra Google Meet. No seu próprio computador: **Conexões**, **+ Adicionar**, Google Meet, ou `assistant connect google_meet`.
4. Cole o token e clique em **Conectar**.

O token expira depois de cerca de uma hora. Quando Conexões disser que ele foi rejeitado, cole um novo.

## Remover

- No painel: **Conexões**, abra Google Meet, **Detalhes** e depois **Desconectar**. O que ele já trouxe continua.
- Em uma Machine hospedada, você também pode clicar em **Remover** ao lado dele na sua página de configuração.

## Revogar no Google

Abra myaccount.google.com/permissions e remova o acesso do OAuth Playground.
