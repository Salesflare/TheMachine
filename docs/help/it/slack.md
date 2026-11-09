---
title: Slack
area: connections
summary: I canali e i messaggi diretti di cui fai parte. Invia un messaggio diretto solo dopo la tua approvazione.
covers: connector:slack
code: assistant.py, next_actions.py, onboarding.py, slack_api.py
site: Connect, Remove
---
## Cosa legge

Le conversazioni di cui fai parte: canali, canali privati, messaggi diretti e messaggi di gruppo, gli ultimi 7 giorni quando ti colleghi, poi tutto quello che arriva di nuovo. Non entra mai in un canale e non apre conversazioni da solo. Un canale tranquillo viene letto circa una volta al giorno; quando un'attività ha bisogno dei suoi messaggi più recenti, The Machine lo legge subito.

Circa un anno di messaggi più vecchi arriva dopo, un po’ alla volta, come [cronologia](history.md).

Le persone compaiono con il loro nome e le app con il proprio, mai con un ID Slack. Chi non ha più un account Slack compare come ex utente di Slack.

## Cosa può inviare

Un messaggio diretto a una persona, a nome tuo, e solo dopo che l’hai approvato nell’attività. Una risposta al messaggio Slack da cui è nata un’attività va nel thread di quel messaggio, nel messaggio diretto o nel canale; la bozza dice **Nel thread**. Non avvia mai un nuovo post in un canale.

## Collegalo

1. **Connessioni**, **+ Aggiungi**, **Slack**, poi **Accedi con Slack**, e consentilo in Slack. Sul tuo computer, prima abbinalo al tuo account su themachine.computer.
2. I messaggi nuovi e i messaggi diretti arrivano per primi. Slack lascia leggere alle app circa una conversazione al minuto, quindi i messaggi più vecchi arrivano nel giro di qualche ora.

Oppure usa una chiave API di Maton: accedi su maton.ai, collega Slack lì e copia la tua chiave API di Maton dalla Home. Poi apri **Oppure usa una chiave API di Maton** sotto Slack e incollala, oppure esegui `assistant connect slack` sul tuo computer. Uno Slack collegato tramite Maton continua a funzionare così com’è.

## Rimuovilo

- Nella dashboard: **Connessioni**, apri Slack, **Dettagli**, poi **Disconnetti**. Quello che ha già portato dentro resta.
- Su una Machine in hosting puoi anche premere **Rimuovi** accanto a Slack nella tua pagina di configurazione.

## Disinstallalo su Slack

Con l’accesso a Slack: apri la pagina Gestisci app del tuo workspace in Slack e rimuovi The Machine. Tramite Maton: rimuovi la connessione Slack in Maton ed elimina la chiave API di Maton che hai fornito. Anche un admin di Slack può rimuovere l’una o l’altra app dal workspace, sotto Gestisci app.
