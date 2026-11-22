---
title: Telegram
area: connections
summary: Receba suas tarefas no Telegram, com os mesmos botões do painel, por um bot só seu. Opcional.
covers: telegram
code: assistant.py, onboarding.py, cli.py
site: Add my bot, Add more any time, Disconnect Telegram
translated: a2b74e4831832977
---
## O que ele faz

Receba suas tarefas no Telegram, por um bot só seu, dentro do seu [horário de trabalho](work-hours.md). Cada uma vem com os botões do painel: **Fazer**, **Adiar**, **Pedir mudanças**, **Marcar como feita**, **Não precisa** e **Enviar** para uma mensagem preparada. Para a The Machine ler os seus chats do Telegram, veja [Chats do Telegram](telegram-chats.md).

É opcional: o app de celular envia as mesmas tarefas como notificações.

## O que ele pode enviar

Só mensagens para você, do seu próprio bot. Uma mensagem para qualquer outra pessoa continua precisando da sua aprovação na tarefa.

## Conectar

Em uma Machine hospedada:

1. No Telegram, mande uma mensagem para @BotFather e envie /newbot. Copie o token que ele der.
2. Na sua página de configuração, em **Adicione mais quando quiser**, abra o Telegram, cole o token e toque em **Adicionar meu bot**.

Adicione quando quiser.

No seu próprio computador, o instalador pede o token, ou rode `assistant telegram on` com o seu ID de usuário do Telegram.

## Remover

- Em uma Machine hospedada: toque em **Desconectar o Telegram** na sua página de configuração. Seu bot e o token dele são removidos da sua Machine.
- No seu próprio computador: `assistant telegram off`. Adicione `--remove-bot` para também esquecer o bot.

## Excluir o bot no Telegram

Mande uma mensagem para @BotFather, envie /deletebot e escolha o seu bot.
