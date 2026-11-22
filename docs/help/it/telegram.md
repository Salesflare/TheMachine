---
title: Telegram
area: connections
summary: Ricevi le tue attività su Telegram, con gli stessi pulsanti della dashboard, tramite un bot che crei tu. Facoltativo.
covers: telegram
code: assistant.py, onboarding.py, cli.py
site: Add my bot, Add more any time, Disconnect Telegram
translated: a2b74e4831832977
---
## A cosa serve

Ricevi le tue attività su Telegram, tramite un bot che crei tu, durante il tuo [Orario di lavoro](work-hours.md). Ognuna include i pulsanti della dashboard: **Fallo**, **Posticipa**, **Chiedi modifiche**, **Segna come fatto**, **Non serve** e **Invia** per un messaggio precompilato. Se invece vuoi che The Machine legga le tue chat di Telegram, consulta [Chat di Telegram](telegram-chats.md).

È facoltativo: l’app per telefono invia le stesse attività come notifiche.

## Cosa può inviare

Solo messaggi a te, dal tuo bot. Per inviare un messaggio a chiunque altro, serve comunque la tua approvazione nell’attività.

## Connetti Telegram

Su una Machine ospitata:

1. Su Telegram, scrivi a @BotFather e invia /newbot. Copia il token che ti fornisce.
2. Nella pagina di configurazione, apri Telegram sotto **Aggiungi altro quando vuoi**, incolla il token e premi **Aggiungi il mio bot**.

Puoi aggiungerlo quando vuoi.

Sul tuo computer, te lo chiederà il programma di installazione. In alternativa, esegui `assistant telegram on` con il tuo ID utente Telegram.

## Rimuovi Telegram

- Su una Machine ospitata: premi **Disconnetti Telegram** nella pagina di configurazione. Il bot e il relativo token vengono rimossi dalla tua Machine.
- Sul tuo computer: `assistant telegram off`. Aggiungi `--remove-bot` per eliminare anche il bot.

## Elimina il bot su Telegram

Scrivi a @BotFather, invia /deletebot e seleziona il tuo bot.
