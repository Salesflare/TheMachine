---
title: Notificações do Android
area: connections
summary: As notificações do seu celular Android, pelo app OpenClaw. Ela só lê.
covers: connector:android
code: onboarding.py, android-notifications.mjs
site: Show a setup code, Approve, Remove
translated: 5b08b093662393a1
---
## O que ela lê

As notificações do seu celular Android, pelo app OpenClaw. Códigos de uso único ficam de fora, assim como as notificações do WhatsApp, Telegram, Signal e Discord.

## O que ela pode fazer

Nada no seu celular. Ela só lê notificações.

## Conectar

Em uma Machine hospedada:

1. Instale o OpenClaw pelo Google Play no seu celular.
2. No painel, abra **Conexões**, depois **Outras**, escolha Notificações do Android e toque em **Mostrar um código de configuração**.
3. No app OpenClaw, adicione um Gateway e escaneie o código. Depois, volte ao painel e toque em **Aprovar**.
4. Permita o acesso às notificações quando o app pedir. Depois, ative **Encaminhar eventos de notificação** nas configurações do app, para receber as notificações assim que chegarem, e não só durante a verificação a cada 10 minutos.

No seu próprio computador, emparelhe o celular no app OpenClaw e execute `assistant connect android`.

## Remover

- No painel: abra **Conexões**, depois Android, **Detalhes** e **Desconectar**.
- Em uma Machine hospedada, você também pode tocar em **Remover** ao lado dela na página de configuração.

## Remover do celular

Desative o acesso às notificações do app OpenClaw nas configurações do Android ou desemparelhe o celular no app OpenClaw.
