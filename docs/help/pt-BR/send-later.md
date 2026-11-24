---
title: Enviar mais tarde
area: cards
summary: Aprove uma mensagem agora e escolha quando enviá-la. Se a pessoa escrever primeiro, ela volta para você aprovar.
covers: send-later
code: machine/store/send_later.py, machine/app/send_later.py, dashboard/todos-send-later.js
order: 13
keywords: schedule, scheduled, send at a time, delay, tomorrow morning, unsend, take back
translated: 29860e4848acce2e
---
## Agendar uma mensagem

Na janela em que você confere uma mensagem, clique em **Enviar mais tarde**, ao lado de **Enviar agora**. Escolha **Em 2 horas**, **Amanhã**, **Segunda-feira** ou **Escolher data** e clique em **Salvar horário**. A mensagem será enviada exatamente como você a viu, no horário escolhido e no seu fuso horário.

Funciona com e-mail, Slack, WhatsApp, Telegram, Signal, Teams e Intercom. Não funciona com LinkedIn e X, porque sua Machine não consegue conferir se chegou uma nova mensagem antes do envio, nem com respostas em documentos.

A opção também aparece em **Novo e-mail**. Se você conferir várias mensagens juntas, todas serão enviadas no horário escolhido.

## Enquanto aguarda

A tarefa fica em **Volta mais tarde** e no dia correspondente do [Calendário](calendar.md), com a mensagem e o horário de envio: “Envia qui., 26 de nov., 09:30”. **Enviar agora** envia a mensagem na hora, **Mudar horário** permite escolher outro horário e **Cancelar** transforma a mensagem novamente em rascunho. O chat mostra as mesmas informações.

Se você editar o rascunho, concluir ou descartar a tarefa, ou trazê-la de volta, a mensagem não será enviada. Você precisa aprová-la novamente.

## Se a pessoa escrever primeiro

Se a pessoa escrever antes do envio, sua Machine não envia a mensagem. A tarefa volta com a mensagem recebida, por exemplo: “Não enviada: Sam Lee escreveu primeiro.” Você recebe o mesmo aviso de uma tarefa adiada. No caso de e-mail, isso vale para qualquer endereço que sua Machine conheça dessa pessoa, em qualquer caixa de entrada que você conectou. A resposta de outra pessoa na conversa também conta.

Uma resposta automática, como uma mensagem de ausência, não impede o envio. Uma mensagem sua também não.

Logo antes do envio, sua Machine confere a conversa novamente. Se não conseguir, a tarefa mostra “Ainda não foi possível verificar se há uma nova mensagem.” e sua Machine tenta de novo durante uma hora. Depois, pergunta a você em vez de enviar.

No WhatsApp, sua Machine verifica as mensagens recebidas até então no WhatsApp que você vinculou.

## Se a Machine estiver desligada

Se sua Machine estiver desligada, suspensa ou com a sessão encerrada no horário do envio, a mensagem será enviada quando ela voltar, com até uma hora de atraso. Depois disso, a tarefa volta com “Não enviada: o atraso passou de uma hora.” e você decide o que fazer.

Se você mudar para outro computador, as mensagens agendadas pedirão sua aprovação novamente nesse computador. Consulte [Trocar de computador](moving.md).

## Quem pode agendar

Só você, no painel ou no app. Sua Machine, o chat dela, uma IA que você conectou e outras Machines não podem agendar mensagens. [Atividade](activity.md) mostra quando uma mensagem foi agendada, alterada, cancelada, enviada ou não enviada.
