---
title: Google Meet
area: connections
summary: Transcrições e notas do Gemini das reuniões do Meet que você organiza. Ele só lê.
covers: connector:google_meet
code: connectors/google_meet.py, onboarding.py
site: Sign in with Google
---
## O que ele lê

Transcrições e notas do Gemini das reuniões do Google Meet que você organizou, assim que o Meet as cria: os últimos 7 dias quando você conecta, depois as novas conforme chegam. O Meet as guarda por 30 dias.

O Meet só as cria quando transcrições ou notas do Gemini estavam ativadas durante a reunião.

Cada uma é associada à reunião da sua agenda no mesmo horário. As notas do Gemini aparecem em Notas dessa reunião e a transcrição em Transcrição, marcadas **Do Google Meet**, ao lado do que você adicionou ali; elas nunca o substituem.

## O que ele pode fazer

Nada no Meet, no Docs ou no Drive. Ele só lê e nunca ativa transcrições sozinho.

## O que ele pede

Um OK próprio, separado do seu login do e-mail. O Google pede para permitir que The Machine:

- Veja suas reuniões do Google Meet, com as transcrições e notas do Gemini.
- Veja seus Google Docs, para ler o documento com as notas do Gemini.

Ele nunca pede o seu Drive. Seu acesso ao Gmail e à Agenda continua igual.

## Conectar

Não precisa ter o Gmail conectado. Para conectar:

- Machine hospedada: no painel, abra **Conexões**, **+ Adicionar**, escolha **Google Meet** e clique em **Entrar com Google**. O Google pede o OK acima, e você volta para o painel.
- Seu próprio computador, pareado com sua conta: os mesmos passos. O login abre em uma nova aba.

Ela confere se o login pode ler o Meet. Sem esse OK, ele não é adicionado. O login continua valendo: não há nada para colar nem renovar.

Se você retirar o OK depois, o card do Google Meet pede para você entrar de novo.

## Remover

No painel: **Conexões**, abra o Google Meet, **Detalhes** e depois **Desconectar**. O que ele já trouxe fica.

## Revogar no Google

Abra myaccount.google.com/permissions e remova o acesso de The Machine ao Google Meet. O Gmail e a Agenda continuam funcionando.
