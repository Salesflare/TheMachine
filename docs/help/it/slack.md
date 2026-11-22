---
title: Slack
area: connections
summary: I canali e i messaggi diretti di cui fai parte. Invia un messaggio diretto solo dopo la tua approvazione.
covers: connector:slack
code: assistant.py, next_actions.py, onboarding.py, slack_api.py
site: Connect, Remove
translated: 23f9e98f4680d23c
---
## Cosa legge

Le conversazioni di cui fai parte: canali, canali privati, messaggi diretti e messaggi di gruppo. Quando lo colleghi, legge gli ultimi 7 giorni, poi tutti i nuovi messaggi. Non entra mai in un canale né apre una conversazione da sola. Legge un canale poco attivo circa una volta al giorno; se un’attività ha bisogno dei messaggi più recenti, The Machine li legge subito.

Circa un anno di messaggi più vecchi arriva in seguito, poco alla volta, come [cronologia](history.md).

Le persone sono indicate con il loro nome e le app con il loro, mai con un ID Slack. Se l’account Slack di qualcuno non esiste più, la persona appare come ex utente Slack.

## Cosa può inviare

Un messaggio diretto a una persona, a nome tuo, e solo dopo che lo approvi nell’attività. Se un’attività nasce da un messaggio Slack, la risposta a quel messaggio viene inviata nel thread, nel messaggio diretto o nel canale da cui proviene; la bozza riporta **Nel thread**. Non pubblica mai un nuovo messaggio in un canale.

## Cosa conserva

Quello che legge resta sulla tua Machine finché non lo elimini o non elimini la Machine. Il servizio di hosting non conserva copie dei tuoi messaggi né i dati di accesso a Slack, e nessun modello di IA viene addestrato sui tuoi messaggi Slack. The Machine usa l’IA, che può sbagliare, quindi puoi vedere ogni messaggio prima che venga inviato.

## Collega Slack

1. Apri **Connessioni**, **Chat**, **Slack**, poi **Accedi con Slack** e autorizza l’accesso in Slack. Se usi il tuo computer, prima associalo al tuo account su themachine.computer.
2. Prima arrivano i nuovi messaggi e i messaggi diretti. Slack consente alle app di leggere circa una conversazione al minuto, quindi i messaggi più vecchi vengono caricati nell’arco di alcune ore.

Oppure usa una chiave API di Maton: accedi su maton.ai, connetti Slack lì e copia la tua chiave API di Maton da Home. Poi apri **Oppure usa una chiave API di Maton** sotto Slack e incollala, oppure esegui `assistant connect slack` sul tuo computer. Una connessione Slack tramite Maton continua a funzionare come prima.

## Rimuovi Slack

- Nella dashboard: apri **Connessioni**, seleziona Slack, poi **Dettagli** e **Disconnetti**. Quello che è già stato importato resta.
- Se usi una Machine ospitata, puoi anche premere **Rimuovi** accanto a Slack nella pagina di configurazione.

## Disinstalla Slack

Se hai effettuato l’accesso con Slack: apri la pagina Gestisci app del tuo spazio di lavoro in Slack e rimuovi The Machine. Smette subito di leggere e ti chiede di accedere di nuovo; quello che è già stato importato resta. Se usi Maton: rimuovi la connessione Slack in Maton ed elimina la chiave API di Maton che hai fornito. Un amministratore Slack può anche rimuovere entrambe le app dallo spazio di lavoro, da Gestisci app.
