---
title: Telegram
area: connections
summary: Ricevi le tue attività su Telegram, con gli stessi pulsanti della dashboard, tramite un tuo bot. Facoltativo.
covers: telegram
code: assistant.py, onboarding.py, cli.py
site: Add my bot, Add more any time, Disconnect Telegram
---
## Cosa fa

Telegram è un modo per ricevere le tue attività, non qualcosa che The Machine legge. Il tuo bot invia ogni attività entro il tuo [orario di lavoro](work-hours.md), con gli stessi pulsanti della dashboard: **Fallo**, **Posticipa**, **Cambia**, **Segna come fatto**, **Non serve** e **Invia** per un messaggio preparato.

Telegram è facoltativo. La dashboard come app per il telefono invia le stesse attività come notifiche.

## Cosa può inviare

Solo messaggi a te, dal tuo bot. Un messaggio a chiunque altro richiede comunque la tua approvazione sull'attività.

## Collegalo

Su una Machine in hosting:

1. In Telegram, scrivi a @BotFather e invia /newbot. Copia il token che ti dà.
2. Nella tua pagina di configurazione, in **Aggiungi altro quando vuoi**, apri Telegram, incolla il token e premi **Aggiungi il mio bot**.

Non fa parte della configurazione: aggiungilo quando vuoi. La dashboard te lo suggerisce quando un'attività posticipata tornerebbe solo lì.

Sul tuo computer, te lo chiede il programma di installazione, oppure esegui `assistant telegram on` con il tuo ID utente di Telegram.

## Rimuovilo

- Su una Machine in hosting: premi **Disconnetti Telegram** nella tua pagina di configurazione. Il tuo bot e il suo token vengono rimossi dal tuo server.
- Sul tuo computer: `assistant telegram off`. Aggiungi `--remove-bot` per dimenticare anche il bot.

## Elimina il bot in Telegram

Scrivi a @BotFather, invia /deletebot e scegli il tuo bot.
