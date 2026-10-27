---
title: Intercom
area: connections
summary: Le conversazioni con i clienti nel tuo workspace Intercom. Risponde solo dopo che hai inviato, a nome tuo.
covers: connector:intercom
code: connectors/intercom.py, onboarding.py
site: Sign in with Intercom, Or paste an access token, Connect, More sources, Remove
---
## Cosa legge

Le conversazioni con i clienti nel tuo workspace Intercom: gli ultimi 7 giorni quando lo colleghi, poi le nuove man mano che arrivano. Legge anche a quale workspace e a quale admin appartiene l'accesso.

## Cosa può fare

Legge le conversazioni. Con il tuo **Accedi con Intercom**, può anche rispondere in una conversazione a nome tuo, solo dopo che premi **Invia** su quel testo esatto. Non assegna, non chiude, non aggiunge tag e non scrive note. Un Intercom condiviso con te tramite la tua Fleet legge soltanto.

## Attività da Intercom

Un’attività da una conversazione Intercom mostra da dove viene: **Leggi il messaggio** apre la conversazione, con un link a essa in Intercom, e il cliente compare sull’attività. La sua risposta è una risposta Intercom in quella conversazione, a meno che tu non chieda un’email.

Quando Intercom non può rispondere dalla tua Machine (condiviso con te solo in lettura, risposte non attive o non collegato), la bozza parte via email. L’attività dice perché, e la sua revisione chiede **Inviare via email invece?** Per rispondere tu in Intercom, tocca **Collega il tuo Intercom** sull’attività e accedi. Non parte nulla prima che tu lo invii.

## Collegalo

Su una Machine in hosting:

1. Apri la tua pagina di configurazione su app.themachine.computer/setup e vai su **Altre fonti**.
2. Apri Intercom e premi **Accedi con Intercom**.
3. Approva The Machine in Intercom. È fatta da Salesflare.

Oppure nella dashboard: **Connessioni**, **+ Aggiungi**, scegli Intercom e premi **Accedi con Intercom**. Quando hai finito, torni alla dashboard.

Se l'accesso non va bene per il tuo workspace, apri invece **Oppure incolla un token di accesso**, incolla un token dal Developer Hub di Intercom e premi **Collegati**.

Sul tuo computer:

1. Nel Developer Hub di Intercom, apri la tua app, poi Authentication, e copia il suo token di accesso.
2. Nella dashboard, apri **Connessioni**, poi **+ Aggiungi**, e scegli Intercom. Oppure esegui `assistant connect intercom`.
3. Incolla il token. Un token di un altro workspace diventa un secondo account Intercom.

Intercom conta sempre come lavoro, per l'azienda indicata dal suo workspace.

## Rimuovilo

- Nella dashboard: **Connessioni**, apri Intercom, **Dettagli**, poi **Disconnetti**. Smette di leggere. Quello che ha già portato resta.
- Su una Machine in hosting puoi anche premere **Rimuovi** accanto a esso nella tua pagina di configurazione.

## Disinstallalo da Intercom

- Accesso con Intercom: in Intercom, apri Settings, Apps, Installed apps, e rimuovi The Machine.
- Un token incollato: eliminalo o rigeneralo nel Developer Hub, oppure elimina l'app in cui l'hai creato.
