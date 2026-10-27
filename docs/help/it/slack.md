---
title: Slack
area: connections
summary: I canali e i messaggi diretti di cui fai parte. Invia un messaggio diretto solo dopo la tua approvazione.
covers: connector:slack
code: assistant.py, next_actions.py, onboarding.py
site: Connect, More sources, Remove
---
## Cosa legge

Le conversazioni di cui fai parte: canali, canali privati, messaggi diretti e messaggi di gruppo, gli ultimi 7 giorni quando ti colleghi, poi tutto quello che arriva di nuovo. Non entra mai in un canale e non apre conversazioni da solo.

## Cosa può inviare

Un messaggio diretto a una persona, a nome tuo, e solo dopo che l’hai approvato nell’attività. Non pubblica mai in un canale.

## Collegalo

Slack viene letto tramite Maton, che custodisce l’accesso a Slack.

1. Accedi su maton.ai, collega Slack lì e copia la tua chiave API di Maton dalla Home.
2. Su una Machine in hosting: apri la tua pagina di configurazione su app.themachine.computer/setup, vai su **Altre fonti**, apri Slack, incolla la chiave e premi **Collegati**.
3. Sul tuo computer: esegui `assistant connect slack`, oppure **Connessioni**, **+ Aggiungi**, Slack.

## Rimuovilo

- Nella dashboard: **Connessioni**, apri Slack, **Dettagli**, poi **Disconnetti**. Quello che ha già portato dentro resta.
- Su una Machine in hosting puoi anche premere **Rimuovi** accanto a Slack nella tua pagina di configurazione.

## Disinstallalo su Slack

Rimuovi la connessione Slack in Maton ed elimina la chiave API di Maton che hai fornito. Anche un admin di Slack può rimuovere l’app dal workspace, sotto Gestisci app.
