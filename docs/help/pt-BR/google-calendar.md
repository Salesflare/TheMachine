---
title: Google Calendar
area: connections
summary: Suas reuniões, para você chegar preparado e fazer o follow-up. Ela não muda nada a menos que você toque.
covers: connector:calendar
code: onboarding.py, google_api.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google
order: 11
---
## O que ela lê

Seus eventos de 7 dias atrás até 30 dias à frente, com os eventos recorrentes preenchidos. Eles aparecem na aba [Calendário](calendar.md) e ajudam nas tarefas sobre uma reunião.

## O que ela pode fazer

Nada sozinha. Ela nunca responde a um convite e só convida as pessoas que você mesmo indicar.

Se o login puder escrever em agendas, você pode adicionar, mudar ou excluir um evento sem convidados, na sua própria agenda ou em uma compartilhada que você possa editar. Cada mudança é um toque seu: no [Calendário](calendar.md) ou em uma tarefa que ofereça isso. Um login feito com **Conectar Google** só lê.

Na sua própria agenda, você também pode convidar pessoas pelo formulário do [Calendário](calendar.md). O botão diz quantas pessoas recebem convite, e o Google envia os convites nesse toque. Uma tarefa nunca convida ninguém.

## Conecte

Em uma Machine hospedada, ela se conecta junto com o Gmail: na sua página de configuração, em **E-mail e agenda**, clique em **Conectar Google**.

No seu próprio computador, depois de [pareado com sua conta](fleet.md): abra **Conexões**, depois **+ Adicionar**, escolha Google Calendar e clique em **Entrar com Google**. Ela se conecta junto com o Gmail.

Com seu próprio app: rode `assistant connect calendar` ou abra **Usar seu próprio app** ali. Ela pergunta qual agenda ler.

## Remova

- Em uma Machine hospedada: clique em **Desconectar** ao lado do endereço na sua página de configuração. Isso remove o Gmail e o Calendar desse endereço.
- No seu próprio computador: **Conexões**, abra a agenda, **Detalhes** e depois **Desconectar**.

## Desinstale no Google

Na sua Conta do Google, abra Segurança, depois Suas conexões com apps e serviços de terceiros, e remova o app. Veja [Gmail](gmail.md).
