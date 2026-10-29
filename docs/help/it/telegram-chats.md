---
title: Chat di Telegram
area: connections
summary: Le tue chat e i piccoli gruppi di Telegram, letti come un dispositivo del tuo account. Risponde solo dopo la tua approvazione.
covers: connector:telegram
code: onboarding.py, telegram_mirror.py, telegram_store.py, next_actions.py
---
## Cosa legge

Le tue chat private e i gruppi fino a 50 persone, come un dispositivo collegato al tuo account Telegram, come Telegram Desktop. Quando la colleghi legge gli ultimi 7 giorni, poi quello che arriva.

Non legge mai canali, bot, Messaggi salvati né i messaggi di servizio di Telegram. Salta anche le chat silenziate e archiviate.

Non tocca il tuo stato di lettura e online: niente viene segnato come letto, e il telefono continua a mostrare i messaggi nuovi come nuovi.

È separato da [Telegram](telegram.md), dove il tuo bot ti invia le tue attività.

## Cosa può inviare

Un testo in una chat che esiste già, solo dopo che l'hai approvato nell'attività. Gli invii partono uno alla volta, con una pausa in mezzo.

Se un'attività è arrivata via email ma con quella persona parli su Telegram, dillo nella chat dell'attività. The Machine trova la chat che hai già con lei e sposta la bozza su Telegram, da rivedere e inviare. Non apre mai una nuova chat.

## Collegala

1. Nella dashboard, apri **Connessioni**, poi **+ Aggiungi**, e scegli Chat di Telegram.
2. Scegli **Scansiona un codice QR in Telegram sul telefono**.
3. Sul telefono, in Telegram, apri Impostazioni, Dispositivi, **Link Desktop Device**, e scansiona il codice.
4. Se il tuo account ha una password cloud, scrivila quando te la chiede. Va a Telegram e non viene mai salvata.

Stai configurando dal telefono, senza un secondo schermo da cui scansionare? Scegli invece **Ricevi un codice in Telegram per il tuo numero**. Il modulo dice dove Telegram ha inviato il codice: alla tua app Telegram su un altro dispositivo, via SMS o alla tua email di accesso. Nessun codice? Premi **Invia di nuovo il codice**.

Sul tuo computer ti serve anche un tuo ID app di Telegram. Crealo su [my.telegram.org](https://my.telegram.org), in API development tools, e inserisci il suo api_id e api_hash nel modulo.

Oppure esegui `assistant connect telegram` in un terminale e scansiona il codice che mostra lì.

## Quando si ferma

- **Disconnessa da Telegram**: Telegram ha chiuso l'accesso di questo dispositivo, o l'hai disconnesso dal telefono. Premi **Riconnetti** sulla sua scheda.
- **Telegram non accetta più l'ID app**: Telegram non accetta più l'ID app che usa questa Machine. Niente viene letto o inviato finché non premi **Riconnetti** e aggiungi un tuo ID app.

The Machine usa l'API di Telegram per farlo. Telegram può limitare o chiudere gli accessi da app come lei.

## Foto

The Machine chiede a Telegram le foto profilo delle persone nel tuo graph che non ne hanno una, al massimo 50 al giorno, con lo stesso accesso che legge le tue chat, e solo per persone delle chat che legge. Non viene inviato nulla a loro. Chi ti nasconde la propria foto resta senza.

## Rimuovila

**Connessioni**, apri Chat di Telegram, **Dettagli**, poi **Disconnetti**. La tua Machine esce da Telegram ed elimina ciò che aveva conservato per Telegram.

Oppure chiudila dal telefono: in Telegram, apri Impostazioni, Dispositivi, tocca The Machine e termina la sessione.
