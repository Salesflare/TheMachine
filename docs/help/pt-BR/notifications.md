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
- **Resumo da manhã**: as reuniões de hoje, o que vence, o que chegou durante a noite e as primeiras tarefas esperando, na ordem da sua lista de tarefas.

Cada um tem um botão para **Push** (o app no seu celular ou computador), **Telegram** quando estiver configurado e **E-mail** em uma Machine hospedada ou em uma Machine na The Machine Network. Todos ficam ativados, menos o resumo no Telegram.

O **Horário de trabalho** fica na mesma aba: os seus dias de trabalho, as horas em que as notificações podem sair, quando os itens adiados voltam, o horário do resumo e o seu fuso horário. Veja [Horário de trabalho](work-hours.md).

## Quando ele notifica

Como o Slack, ele vê se você está usando o painel, não só se ele está aberto:

- Em uso: o painel está na sua frente, em foco, e você clicou, digitou, rolou ou tocou nele nos últimos 10 minutos. Nada vibra. O Telegram chega sem som.
- Longe: o painel está em segundo plano, minimizado, fechado ou parado há 10 minutos. Um push sai um minuto depois que você deixou o painel, a menos que você volte e veja antes.
- Ainda não visto 15 minutos depois: um único e-mail com tudo o que ainda espera por você. No máximo um por hora. O que você resolveu nesse meio-tempo, no Telegram ou em outro lugar, fica de fora. Usar o painel depois que algo chegou conta como ter visto, então um dia no painel pode não ter nenhum e-mail.
- Fora do seu horário de trabalho: nada. O resumo da manhã traz o que chegou.
- Uma nova tarefa de trabalho que chega num dia de folga espera o horário do resumo do seu próximo dia útil. A tarefa mostra onde e quando vai chegar até você, como Notificação seg, 2 nov · 08:30, conforme a linha **Novas tarefas**. Com Push e Telegram desligados ali, não mostra nada.

Só notifica o que precisa de você. Andamento e edições não. Várias de uma vez vibram uma vez só. O ícone do app mostra quantas tarefas precisam de você.

## Botões nas notificações

Cada notificação tem botões para o próximo passo. No app do celular:

- Nova tarefa: Fazer, Adiar 2 h, Marcar como feita.
- Rascunho pronto: Abrir rascunho, Adiar 2 h, Marcar como feita.
- Resultado pronto: Abrir, Marcar como feita, Adiar 2 h.
- Pergunta, travada ou login necessário: Responder, Abrir ou Entrar, depois Adiar 2 h e Marcar como feita.
- Lembrete: Marcar como feita, Adiar, Abrir.
- Resumo da manhã: toque para abrir.

Um navegador e o Telegram mostram dois deles. As perguntas do Fleet mantêm Responder uma vez e Recusar.

Nada é enviado, pago ou enviado para aprovação a partir de uma notificação. Um rascunho sempre abre primeiro, para você ver antes de sair.

No app, Adiar e Marcar como feita pedem para desbloquear primeiro. No navegador, eles abrem o painel, que faz isso e mostra Desfazer. Adiar 2 h traz a tarefa de volta em duas horas, Adiar amanhã de manhã.

Os e-mails com o que espera por você têm links Abrir e Adiar. Eles só abrem o painel.

## O resumo da manhã

Ele chega nos dias de trabalho, no horário do **Resumo da manhã**, e só não é enviado quando não há nada a dizer: nenhuma reunião, nada vencendo ou novo e nenhuma tarefa esperando. **Prévia**, na linha dele, mostra o resumo na página sem enviar. Por padrão, ele vai por push e por e-mail. O push diz quantas tarefas esperam, as duas primeiras e o horário da sua primeira reunião. Tocar no push abre o dia de hoje no **Calendário**.

## Privacidade

O push vai da sua Machine direto para o seu dispositivo, criptografado para esse dispositivo. O plano de controle nunca vê. O e-mail é enviado pelo servidor de e-mail da The Machine para o endereço da sua conta, então o texto passa por ele e pelo provedor de e-mail. Quando o modo [Cuidadoso](security-levels.md) esconde o texto das tarefas nas notificações, os e-mails só trazem números. Desative **E-mail** para um tipo para deixá-lo totalmente fora do e-mail. Ele também diz quanto tempo as tarefas esperando levam, como "4 para revisar · cerca de 2 min".

Ative o push para um dispositivo em **Este dispositivo**, ou veja [Instalar o app](phone-app.md).
