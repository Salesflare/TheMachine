---
title: Notificações do Android
area: connections
summary: As notificações do seu celular Android, pelo app OpenClaw. Ele só lê.
covers: connector:android
code: onboarding.py, android-notifications.mjs
site: Show a setup code, Approve, More sources, Remove
---
## O que ele lê

As notificações que chegam no seu celular Android, pelo app OpenClaw. Códigos de uso único ficam de fora, assim como as notificações do WhatsApp, Telegram, Signal e Discord.

## O que ele pode fazer

Nada no seu celular. Ele só lê notificações.

## Conectar

Em uma Machine hospedada:

1. Instale o app OpenClaw no seu celular.
2. No painel, abra **Conexões**, depois **+ Adicionar**, escolha Celular Android e toque em **Mostrar um código de configuração**.
3. Escaneie o código no app OpenClaw e toque em **Aprovar** para o pareamento.
4. No app OpenClaw, ative Forward Notification Events e permita o acesso às notificações quando o Android pedir.

No seu próprio computador, pareie o celular com o seu OpenClaw Gateway e depois rode `assistant connect android`.

## Remover

- No painel: **Conexões**, abra Android, **Detalhes** e depois **Desconectar**.
- Em uma Machine hospedada, você também pode tocar em **Remover** ao lado dele na sua página de configuração.

## Remover no celular

Desative o acesso às notificações do app OpenClaw nas configurações do Android, ou desfaça o pareamento do celular no app OpenClaw.
