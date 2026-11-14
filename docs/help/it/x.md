---
title: X
area: connections
summary: Le tue menzioni, risposte e messaggi diretti su X, letti nel browser della tua Machine. I messaggi vengono inviati solo dopo la tua approvazione.
covers: connector:x
code: connectors/x.py, integrations/x_inbox.py
site: Connect, More sources, Remove
translated: 5cbe43055458daf4
---
## Cosa legge

Le tue menzioni, risposte e messaggi diretti su X, nel browser della tua Machine, con la tua sessione. Non segna nulla come letto e non può leggere i messaggi crittografati di X Chat.

## Cosa può inviare

Una risposta o un messaggio diretto, solo dopo che l'approvi nell'attività.

La connessione non passa dall'API ufficiale di X. È molto improbabile che la lettura e l'invio occasionale di una risposta da te approvata causino problemi. L'invio massivo o automatico può far bloccare un account.

## Collegalo

Su una Machine ospitata:

1. Apri la pagina di configurazione su app.themachine.computer/setup e vai a **Altre fonti**.
2. Apri X, inserisci il tuo handle senza @, poi accedi a X nel browser della tua Machine quando richiesto e premi **Collegati**.

Sul tuo computer:

1. Nella dashboard, apri **Connessioni**, poi **Chat** e scegli X.
2. Scegli **Lavoro** e l'azienda, oppure **Personale**. Inserisci il tuo handle senza @ e premi **Collegati**.
3. Premi **Accedi a X** e accedi nel browser della tua Machine. La connessione si attiva automaticamente appena hai effettuato l'accesso.

Oppure esegui `assistant connect x` in un terminale.

Se X disconnette la tua Machine, consulta [Disconnessione da un sito](signed-out.md).

## Rimuovilo

- Nella dashboard: apri **Connessioni**, scegli X, poi **Dettagli** e **Disconnetti**. La Machine smette di leggere. I dati già importati restano.
- Su una Machine ospitata, puoi anche premere **Rimuovi** accanto a X nella pagina di configurazione.

## Disconnetti la sessione da X

Su X, apri Impostazioni, Sicurezza e accesso all'account, App e sessioni, Sessioni e disconnetti la sessione del browser della tua Machine.
