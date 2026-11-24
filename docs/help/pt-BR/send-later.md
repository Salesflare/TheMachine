---
title: Enviar mais tarde
area: cards
summary: Clique em **Enviar mais tarde**, ao lado de **Enviar agora**, para agendar um e-mail ou uma mensagem. Você aprova o envio agora e escolhe quando ele será feito. Se a pessoa escrever primeiro, a mensagem volta para você.
covers: send-later
code: machine/store/send_later.py, machine/app/send_later.py, dashboard/todos-send-later.js
order: 13
keywords: schedule, scheduled, schedule an email, send at a time, delay, tomorrow morning, unsend, take back
translated: 6fa6af155c337981
---
## Agendar uma mensagem

Na janela em que você revisa uma mensagem, clique em **Enviar mais tarde**, ao lado de **Enviar agora**. Escolha **Em 2 horas**, **Amanhã**, **Segunda-feira** ou **Escolher data** e clique em **Salvar horário**. A mensagem será enviada exatamente como você a viu, no horário escolhido e de acordo com o seu fuso horário.

O recurso funciona com e-mail, Slack, WhatsApp, Telegram, Signal, Teams e Intercom. Não funciona com LinkedIn e X, porque sua Machine não consegue verificar se há uma mensagem nova logo antes do envio. Também não funciona para respostas em documentos.

O recurso também aparece em **Novo e-mail**. Se você revisar várias mensagens juntas, todas serão enviadas no horário escolhido.

## Enquanto a mensagem aguarda

A tarefa fica em **Volta mais tarde** e no dia correspondente do [Calendário](calendar.md), junto com a mensagem e o horário de envio: "Envia qui., 26 de nov., 09:30". **Enviar agora** envia a mensagem na hora, **Mudar horário** permite escolher outro horário e **Cancelar** transforma a mensagem em rascunho novamente. O mesmo aparece no chat.

Se você editar o rascunho, concluir a tarefa, dispensá-la ou trazê-la de volta, a mensagem não será enviada. Você precisará aprová-la novamente.

## Se a pessoa escrever primeiro

Se a pessoa escrever antes do envio, sua Machine não envia a mensagem. A tarefa volta com a mensagem dela, como "Não enviada: Sam Lee escreveu primeiro.", e você recebe a notificação que receberia para uma tarefa adiada. No caso de e-mail, isso vale para qualquer endereço que sua Machine conheça dessa pessoa, em qualquer caixa de e-mail conectada. A resposta de outra pessoa na conversa também conta.

Uma resposta automática, como uma mensagem de ausência, não impede o envio. Uma mensagem sua também não.

Logo antes do envio, sua Machine verifica a conversa novamente. Se não conseguir, a tarefa mostra "Ainda não foi possível verificar se há uma mensagem nova." e tenta de novo por uma hora. Depois disso, ela pergunta a você em vez de enviar.

No WhatsApp, sua Machine verifica as mensagens que o WhatsApp vinculado a você recebeu até então.

## Se a Machine estiver desligada

Se sua Machine estiver desligada, em repouso ou com a sessão encerrada no horário do envio, a mensagem será enviada quando ela voltar, com até uma hora de atraso. Depois desse prazo, a tarefa volta com "Não enviada: o atraso passou de uma hora." e você decide o que fazer.

Quando você muda para outro computador, as mensagens agendadas pedem sua aprovação novamente. Veja [Mudança de computador](moving.md).

## Quem pode agendar

Só você pode agendar mensagens, pelo painel ou pelo app. Sua Machine, o chat dela, uma IA que você conectou e outras Machines não podem agendar mensagens. [Atividade](activity.md) mostra quando uma mensagem foi agendada, alterada, cancelada, enviada ou não enviada.
