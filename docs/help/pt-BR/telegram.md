---
title: Telegram
area: connections
summary: Receba suas tarefas no Telegram, com os mesmos botões do painel, por um bot só seu. Opcional.
covers: telegram
code: assistant.py, onboarding.py, cli.py
site: Add my bot, Add more any time, Disconnect Telegram
---
## O que ele faz

Este Telegram é um jeito de receber suas tarefas. Para a The Machine ler os seus próprios chats do Telegram, veja [Chats do Telegram](telegram-chats.md). O seu próprio bot envia cada tarefa dentro do seu [horário de trabalho](work-hours.md), com os mesmos botões do painel: **Fazer**, **Adiar**, **Mudar**, **Marcar como feita**, **Não precisa** e **Enviar** para uma mensagem preparada.

O Telegram é opcional. O painel como app de celular envia as mesmas tarefas como notificações.

## O que ele pode enviar

Só mensagens para você, do seu próprio bot. Uma mensagem para qualquer outra pessoa continua precisando da sua aprovação na tarefa.

## Conectar

Em uma Machine hospedada:

1. No Telegram, mande uma mensagem para @BotFather e envie /newbot. Copie o token que ele der.
2. Na sua página de configuração, em **Adicione mais quando quiser**, abra Telegram, cole o token e toque em **Adicionar meu bot**.

Ele não faz parte da configuração inicial: adicione quando quiser. Seu painel sugere o Telegram quando uma tarefa adiada só voltaria por lá.

No seu próprio computador, o instalador pede o token, ou rode `assistant telegram on` com o seu ID de usuário do Telegram.

## Remover

- Em uma Machine hospedada: toque em **Desconectar Telegram** na sua página de configuração. Seu bot e o token dele são removidos da sua Machine.
- No seu próprio computador: `assistant telegram off`. Adicione `--remove-bot` para também esquecer o bot.

## Excluir o bot no Telegram

Mande uma mensagem para @BotFather, envie /deletebot e escolha o seu bot.
