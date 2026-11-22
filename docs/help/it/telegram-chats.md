---
title: Chat di Telegram
area: connections
summary: Le tue chat e i piccoli gruppi di Telegram, letti come dispositivo del tuo account. Le risposte vengono inviate solo dopo la tua approvazione.
covers: connector:telegram
code: onboarding.py, telegram_mirror.py, telegram_store.py, next_actions.py
translated: da17aef29a380002
---
## Cosa legge

Le tue chat private e i gruppi fino a 50 persone, come dispositivo connesso al tuo account Telegram, proprio come Telegram Desktop. Quando la colleghi, legge gli ultimi 7 giorni di messaggi e poi quelli in arrivo.

Non legge mai i canali, i bot, i Messaggi salvati o i messaggi di servizio di Telegram. Salta anche le chat silenziate e archiviate.

Non modifica il tuo stato di lettura o online: non segna nulla come letto e il tuo telefono continua a mostrare i nuovi messaggi come nuovi.

È separata da [Telegram](telegram.md), dove il tuo bot ti invia le tue attività.

## Cosa può inviare

Un messaggio di testo in una chat esistente, solo dopo che lo approvi nell’attività. I messaggi vengono inviati uno alla volta, con una pausa tra l’uno e l’altro.

Se un’attività è arrivata via email, ma parli con quella persona su Telegram, dillo nella chat dell’attività. La Machine trova la chat esistente con quella persona e passa la bozza a Telegram, così puoi controllarla e inviarla. Non avvia mai una nuova chat.

## Connettila

1. Nella dashboard, apri **Connessioni**, poi **Chat** e scegli le chat di Telegram.
2. Scegli **Scansiona un codice QR con Telegram su un altro dispositivo**.
3. Sul telefono, apri Telegram e vai su Impostazioni, Dispositivi, **Collega un dispositivo desktop**, poi scansiona il codice.
4. Se il tuo account ha una password cloud, inseriscila quando richiesto. Viene inviata a Telegram e non viene mai salvata.

Sul telefono, il modulo mostra prima **Ricevi un codice al tuo numero di telefono**, perché non puoi scansionare un codice QR dallo stesso schermo. Indica dove Telegram ha inviato il codice: all’app Telegram su un altro dispositivo, via SMS o all’email di accesso. Non hai ricevuto il codice? Premi **Invia di nuovo il codice**.

Sul tuo computer, ti serve anche un ID app Telegram personale. Creane uno su [my.telegram.org](https://my.telegram.org), nella sezione API development tools, poi inserisci api_id e api_hash nel modulo.

Oppure esegui `assistant connect telegram` in un terminale e scansiona il codice che viene mostrato.

## Quando smette di funzionare

- **Disconnessa da Telegram**: Telegram ha terminato l’accesso di questo dispositivo oppure hai chiuso la sessione dal telefono. Premi **Riconnetti** in **Connessioni**.
- **Telegram non accetta più l’ID dell’app**: Telegram non accetta più l’ID app usato da questa Machine. Non legge né invia nulla finché non premi **Riconnetti** e aggiungi un ID app personale.

Telegram può limitare o terminare gli accessi da app come The Machine.

## Immagini

La Machine chiede a Telegram le foto profilo delle persone del tuo Graph che ne sono sprovviste, fino a 50 al giorno, usando lo stesso accesso con cui legge le tue chat e solo per le persone nelle chat che legge. Non invia loro nulla. Se una persona ti nasconde la sua foto, continuerà a non averne una.

## Rimuovila

Apri **Connessioni**, le chat di Telegram, **Dettagli** e poi **Disconnetti**. La tua Machine si disconnette da Telegram ed elimina i dati che aveva conservato per Telegram.

Oppure termina la sessione dal telefono: in Telegram, apri Impostazioni, Dispositivi, tocca The Machine e termina la sessione.
