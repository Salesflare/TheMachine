---
title: X
area: connections
summary: Menzioni, risposte e messaggi diretti su X, consultati nel browser della tua Machine. L’invio avviene solo dopo la tua approvazione.
covers: connector:x
code: connectors/x.py, integrations/x_inbox.py
site: Connect, More sources, Remove
translated: e8997ab6eb32523f
---
## Cosa legge

Le tue menzioni, le risposte e i messaggi diretti su X, nel browser della tua Machine, con il tuo account. Non segna nulla come letto e non può leggere le chat X criptate.

## Cosa può inviare

Una risposta o un messaggio diretto, solo dopo che l’hai approvato nell’attività.

X sta trasferendo gli account a una nuova app web. Se il tuo account è già stato trasferito, per ora le risposte non possono essere inviate tramite la tua Machine. Una risposta che approvi si interrompe prima della pubblicazione e te lo segnala. I messaggi diretti continuano a essere inviati.

Non passa dall’API ufficiale di X. Leggere e inviare ogni tanto una risposta che hai approvato difficilmente causa problemi. L’invio massivo o automatizzato può portare al blocco dell’account.

## Collegalo

Su una Machine ospitata:

1. Apri la pagina di configurazione all’indirizzo app.themachine.computer/setup e vai su **Altre fonti**.
2. Apri X, inserisci il tuo handle senza @ e, quando richiesto, accedi a X dal browser della tua Machine. Poi premi **Collega**.

Sul tuo computer:

1. Nella dashboard, apri **Connessioni**, poi **Chat** e seleziona X.
2. Seleziona **Lavoro** e la relativa azienda, oppure **Personale**. Inserisci il tuo handle senza @ e premi **Collega**.
3. Premi **Accedi a X** e accedi dal browser della tua Machine. La connessione viene stabilita automaticamente una volta effettuato l’accesso.

Oppure esegui `assistant connect x` in un terminale.

Se X disconnette la tua Machine, consulta [Disconnessione da un sito](signed-out.md).

## Rimuovilo

- Nella dashboard: apri **Connessioni**, seleziona X, poi **Dettagli** e **Disconnetti**. La lettura si interrompe. I contenuti già importati restano.
- Su una Machine ospitata, puoi anche premere **Rimuovi** accanto a X nella pagina di configurazione.

## Disconnetterla da X

Su X, apri Impostazioni, Sicurezza e accesso all’account, App e sessioni, Sessioni, quindi disconnetti la sessione del browser della tua Machine.
