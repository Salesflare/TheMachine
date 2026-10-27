---
title: Notificações
area: settings
summary: O que chega até você, onde e quando: push, Telegram ou e-mail por tipo, o seu horário de trabalho e o resumo da manhã.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
---
Em **Configurações**, **Notificações**, escolha por tipo onde cada coisa chega até você:

- **Novas tarefas**: uma resposta que alguém está esperando, um pedido, qualquer coisa urgente.
- **Resultados e perguntas**: um rascunho pronto para aprovar ou enviar, uma tarefa travada ou que precisa de login, uma pergunta do Fleet.
- **Lembretes**: itens adiados e esperas que voltam.
- **Resumo da manhã**: as reuniões de hoje, o que vence e o que chegou durante a noite.

Cada um tem um botão para **Push** (o app no seu celular ou computador), **Telegram** quando estiver configurado e **E-mail** em uma Machine hospedada ou em uma Machine na The Machine Network. Todos ficam ativados, menos o resumo no Telegram.

O **Horário de trabalho** fica na mesma aba: os seus dias de trabalho, as horas em que as notificações podem sair, quando os itens adiados voltam, o horário do resumo e o seu fuso horário. Veja [Horário de trabalho](work-hours.md).

## Quando ele notifica

Como o Slack, ele vê se você está usando o painel, não só se ele está aberto:

- Em uso: o painel está na sua frente, em foco, e você clicou, digitou, rolou ou tocou nele nos últimos 10 minutos. Nada vibra. O Telegram chega sem som.
- Longe: o painel está em segundo plano, minimizado, fechado ou parado há 10 minutos. Um push sai um minuto depois que você deixou o painel, a menos que você volte e veja antes.
- Ainda não visto 15 minutos depois: um único e-mail com tudo o que ainda espera por você. No máximo um por hora. O que você resolveu nesse meio-tempo, no Telegram ou em outro lugar, fica de fora. Usar o painel depois que algo chegou conta como ter visto, então um dia no painel pode não ter nenhum e-mail.
- Fora do seu horário de trabalho: nada. O resumo da manhã traz o que chegou.

Só notifica o que precisa de você. Andamento e edições não. Várias de uma vez vibram uma vez só. O ícone do app mostra quantas tarefas precisam de você.

## O resumo da manhã

Ele chega nos dias de trabalho, no horário do **Resumo da manhã**, e não é enviado quando não há nada a dizer. **Prévia**, na linha dele, mostra o resumo na página sem enviar. Por padrão, ele vai por push e por e-mail.

## Privacidade

O push vai da sua Machine direto para o seu dispositivo, criptografado para esse dispositivo. O plano de controle nunca vê. O e-mail é enviado pelo servidor de e-mail da The Machine para o endereço da sua conta, então o texto passa por ele e pelo provedor de e-mail. Quando o modo [Cuidadoso](security-levels.md) esconde o texto das tarefas nas notificações, os e-mails só trazem números. Desative **E-mail** para um tipo para deixá-lo totalmente fora do e-mail.

Ative o push para um dispositivo em **Este dispositivo**, ou veja [Instalar o app](phone-app.md).
