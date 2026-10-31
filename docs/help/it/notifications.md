---
title: Notifiche
area: settings
summary: Cosa ti arriva, dove e quando: push, Telegram o email per tipo, il tuo orario di lavoro e il riepilogo del mattino.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
---
In **Impostazioni**, **Notifiche**, scegli per ogni tipo dove ti arriva:

- **Nuove attività**: una risposta che qualcuno aspetta, una richiesta, qualsiasi cosa urgente.
- **Risultati e domande**: una bozza pronta da approvare o inviare, un compito bloccato o che richiede un accesso, una domanda della Fleet.
- **Promemoria**: attività posticipate e attese che tornano.
- **Riepilogo del mattino**: le riunioni di oggi, cosa scade e cosa è arrivato durante la notte.

Ognuno ha un interruttore per **Push** (l'app sul telefono o sul computer), per **Telegram** quando è configurato e per **Email** su una Machine in hosting o su una Machine nel The Machine Network. Sono tutti attivi, tranne il riepilogo su Telegram.

L'**Orario di lavoro** è nella stessa scheda: i tuoi giorni lavorativi, le ore in cui possono partire le notifiche, quando tornano i posticipi, l'ora del riepilogo e il tuo fuso orario. Vedi [Orario di lavoro](work-hours.md).

## Quando notifica

Come Slack, guarda se stai usando la dashboard, non solo se è aperta:

- In uso: la dashboard è davanti a te, in primo piano, e negli ultimi 10 minuti hai cliccato, scritto, scorso o toccato. Non vibra niente. Telegram arriva senza suono.
- Assente: la dashboard è in secondo piano, ridotta a icona, chiusa o inattiva da 10 minuti. Una push parte un minuto dopo che l'hai lasciata, a meno che tu non torni e la veda prima.
- Ancora non vista dopo 15 minuti: una sola email con tutto ciò che ti aspetta ancora. Al massimo una all'ora. Ciò che hai gestito nel frattempo, su Telegram o altrove, resta fuori. Usare la dashboard dopo che qualcosa è arrivato conta come averlo visto: in una giornata passata sulla dashboard può non arrivare nessuna email.
- Fuori dal tuo orario di lavoro: niente. Il riepilogo del mattino contiene ciò che è arrivato.
- Una nuova attività di lavoro arrivata in un giorno libero aspetta l'ora del riepilogo del tuo prossimo giorno lavorativo. L'attività mostra dove e quando ti raggiungerà, come Notifica lun 2 nov · 08:30, secondo la riga **Nuove attività**. Con Push e Telegram entrambi spenti lì, non dice nulla.

Notifica solo ciò che ha bisogno di te. Avanzamenti e modifiche no. Una raffica vibra una volta sola. L'icona dell'app mostra quante attività hanno bisogno di te.

## Il riepilogo del mattino

Arriva nei giorni lavorativi all'ora del **Riepilogo del mattino**, e salta quando non c'è niente da dire. **Anteprima**, nella sua riga, lo mostra sulla pagina senza inviarlo. Di default è una push e un'email.

## Privacy

Le push vanno dalla tua Machine direttamente al tuo dispositivo, crittografate per quel dispositivo. Il control plane non le vede mai. Le email le invia il server di posta di The Machine all'indirizzo del tuo account, quindi il testo passa da lì e dal provider di posta. Quando [Prudente](security-levels.md) nasconde il testo delle attività nelle notifiche, le email contengono solo conteggi. Disattiva **Email** per un tipo per tenerlo del tutto fuori dalle email.

Attiva le push per un dispositivo in **Questo dispositivo**, oppure vedi [Installa l'app](phone-app.md).
