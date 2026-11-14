---
title: Intercom
area: connections
summary: Le conversazioni con i clienti nel tuo workspace Intercom. Risponde solo dopo che hai inviato, a nome tuo.
covers: connector:intercom
code: connectors/intercom.py, onboarding.py
site: Sign in with Intercom, More sources, Remove
translated: 2cbee87e6d24c0a9
---
## Cosa legge

Le conversazioni con i clienti nel tuo workspace Intercom: gli ultimi 7 giorni quando lo colleghi, poi le nuove man mano che arrivano. Legge anche a quale workspace e a quale admin appartiene l'accesso.

## Cosa può fare

Legge le conversazioni. Con il tuo **Accedi con Intercom**, può anche rispondere in una conversazione a nome tuo, solo dopo che premi **Invia** su quel testo esatto. Non assegna, non chiude, non aggiunge tag e non scrive note. Un Intercom condiviso con te tramite la tua Fleet legge soltanto.

## Attività da Intercom

Un’attività da una conversazione Intercom mostra da dove viene: **Leggi il messaggio** apre la conversazione, con un link a essa in Intercom, e il cliente compare sull’attività. La sua risposta è una risposta Intercom in quella conversazione, a meno che tu non chieda un’email.

Diventano attività solo le conversazioni assegnate a te, o ancora a nessuno, anche quelle in una inbox del team senza nessuno assegnato. Quando qualcuno del team prende una conversazione in Intercom, la sua attività aperta si chiude da sola, con **Annulla**. Su un Intercom condiviso con te, le tue conversazioni sono quelle assegnate all’admin con cui scrivi.

Un’attività da Intercom si chiude da sola anche quando qualcuno del team chiude la conversazione in Intercom, o risponde e il cliente non ha più scritto, se l’attività chiedeva solo una risposta. Vale anche quando hai risposto poco prima dell’attività, prima che The Machine leggesse la tua risposta. Una nota, un posticipo o la risposta di un bot non contano mai.

Quando Intercom non può rispondere dalla tua Machine (condiviso con te solo in lettura, risposte non attive o non collegato), la bozza parte via email. L’attività dice perché, e la sua revisione chiede **Inviare via email invece?** Per rispondere tu in Intercom, tocca **Collega il tuo Intercom** sull’attività e accedi. Poi l’attività viene riscritta come risposta in Intercom. Non parte nulla prima che tu lo invii.

Il tuo Intercom e uno condiviso con te per lo stesso workspace non leggono entrambi: quello condiviso resta in pausa e le sue conversazioni passano al tuo, ognuna una volta.

## Collegalo

1. Nella dashboard: **Connessioni**, **Clienti**, Intercom. Oppure nella pagina di configurazione di una Machine in hosting, su app.themachine.computer/setup: **Altre fonti**, Intercom. Sul tuo computer, abbinalo prima al tuo account.
2. Premi **Accedi con Intercom**.
3. Approva The Machine in Intercom. È fatta da Salesflare. Quando hai finito, torni da dove eri partito.

Accedere a un altro workspace aggiunge un secondo account Intercom.

Intercom conta sempre come lavoro, per l'azienda indicata dal suo workspace.

## Rimuovilo

- Nella dashboard: **Connessioni**, apri Intercom, **Dettagli**, poi **Disconnetti**. Smette di leggere. Quello che ha già portato resta.
- Su una Machine in hosting puoi anche premere **Rimuovi** accanto a esso nella tua pagina di configurazione.

## Disinstallalo da Intercom

In Intercom, apri Settings, Apps, Installed apps, e rimuovi The Machine.
