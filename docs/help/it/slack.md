---
title: Slack
area: connections
summary: I canali e i messaggi diretti di cui fai parte. Invia un messaggio diretto solo dopo la tua approvazione.
covers: connector:slack
code: assistant.py, slack_api.py, next_actions.py, onboarding.py
site: Sign in with Slack, Connect, More sources, Remove
---
## Cosa legge

Le conversazioni di cui fai parte: canali, canali privati, messaggi diretti e messaggi di gruppo, gli ultimi 7 giorni quando ti colleghi, poi tutto quello che arriva di nuovo. Non entra mai in un canale e non apre conversazioni da solo.

## Cosa può inviare

Un messaggio diretto a una persona, a nome tuo, e solo dopo che l’hai approvato nell’attività. Non pubblica mai in un canale.

## Collegalo

Accedi con Slack, il modo facile:

1. Nella dashboard: **Connessioni**, **+ Aggiungi**, Slack. Oppure nella pagina di configurazione di una Machine in hosting su app.themachine.computer/setup: **Altre fonti**, Slack. Sul tuo computer, prima associalo al tuo account.
2. Premi **Accedi con Slack**. Slack chiede quale workspace e mostra cosa The Machine può leggere e inviare.
3. Premi **Allow**. Torni da dove eri partito e Slack è collegato.

In alcuni workspace solo gli admin approvano le nuove app. Slack chiede prima a un admin; quando approva, accedi di nuovo.

Oppure usa Maton:

1. Accedi su maton.ai, collega Slack lì e copia la tua chiave API di Maton dalla Home.
2. Apri Slack come sopra (o esegui `assistant connect slack`), apri **Oppure usa una chiave API di Maton**, incolla la chiave e premi **Collegati**.

Hai già collegato Slack tramite Maton? Continua a funzionare. Connessioni mostra **Riconnetti Slack**: premilo e accedi con Slack per smettere di usare Maton. Quello che Slack ha già portato resta.

## Rimuovilo

- Nella dashboard: **Connessioni**, apri Slack, **Dettagli**, poi **Disconnetti**. Quello che ha già portato dentro resta.
- Su una Machine in hosting puoi anche premere **Rimuovi** accanto a Slack nella tua pagina di configurazione.

## Disinstallalo su Slack

- Con accesso tramite Slack: in Slack apri la pagina Manage apps del tuo workspace (o Impostazioni, App), trova The Machine e rimuovila. Un admin di Slack può anche rimuoverla per tutto il workspace.
- Tramite Maton: rimuovi il collegamento a Slack in Maton ed elimina la chiave API di Maton che hai dato.
