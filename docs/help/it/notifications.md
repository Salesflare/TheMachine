---
title: Notifiche
area: settings
summary: Cosa ti arriva, dove e quando: notifica solo ciò che non può aspettare, il resto è in un solo riepilogo del mattino.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
---
In **Impostazioni**, **Notifiche**, scegli per ogni tipo dove ti arriva:

- **Nuove attività**: solo ciò che non può aspettare, come una scadenza di oggi o qualcosa di urgente.
- **Risultati e domande**: una risposta pronta da inviare, un accesso che serve a un compito, una domanda della Fleet.
- **Promemoria**: attività posticipate e attese che tornano.
- **Riepilogo del mattino**: un breve riepilogo della tua giornata. Vedi sotto.
- **Riepilogo della sera**: cosa è stato fatto oggi e cosa resta per domani. Vedi sotto.

Ognuno ha un interruttore per **Push** (l'app sul telefono o sul computer), per **Telegram** quando è configurato e per **Email** su una Machine in hosting o su una Machine nel The Machine Network. Sono tutti attivi, tranne i riepiloghi su Telegram.

L'**Orario di lavoro** è nella stessa scheda: i tuoi giorni lavorativi, le ore in cui possono partire le notifiche, quando tornano i posticipi, l'ora del riepilogo e il tuo fuso orario. Vedi [Orario di lavoro](work-hours.md).

## Solo ciò che non può aspettare

Una push, una notifica Telegram o un'email parte solo per:

- un'attività in scadenza oggi, o segnata come urgente;
- una risposta che qualcuno aspetta, scritta e pronta da inviare;
- un compito che ha bisogno che tu acceda;
- un'attività posticipata che torna all'ora che hai scelto.

Tutto il resto arriva in silenzio sulla dashboard (e senza suono su Telegram) e aspetta il riepilogo del mattino. In un giorno libero notifica solo ciò che è urgente o in scadenza oggi. Al massimo 8 push al giorno. Dopo 3 giorni senza aprire la dashboard arriva solo il riepilogo del mattino, finché non torni.

## Quando notifica

Come Slack, guarda se stai usando la dashboard, non solo se è aperta:

- In uso: la dashboard è davanti a te, in primo piano, e negli ultimi 10 minuti hai cliccato, scritto, scorso o toccato. Non vibra niente. Telegram arriva senza suono.
- Assente: la dashboard è in secondo piano, ridotta a icona, chiusa o inattiva da 10 minuti. Una push parte un minuto dopo che l'hai lasciata, a meno che tu non torni e la veda prima.
- Ancora non vista dopo 15 minuti, e non può aspettare: un'email per quella, al massimo una all'ora. Ciò che hai già gestito resta fuori. Quasi sempre il riepilogo del mattino è l'unica email.
- Fuori dal tuo orario di lavoro: niente. Il riepilogo del mattino contiene ciò che è arrivato.
- Una nuova attività di lavoro arrivata in un giorno libero aspetta l'ora del riepilogo del tuo prossimo giorno lavorativo. L'attività mostra dove e quando ti raggiungerà, come Notifica lun 2 nov · 08:30, secondo la riga **Nuove attività**. Con Push e Telegram entrambi spenti lì, non dice nulla.

Notifica solo ciò che ha bisogno di te. Avanzamenti e modifiche no. Un risultato più recente su un'attività che non hai ancora visto la aggiorna senza una nuova notifica. Una raffica vibra una volta sola. L'icona dell'app mostra quante attività hanno bisogno di te.

## Pulsanti nelle notifiche

Ogni notifica ha pulsanti per il passo successivo. Nell’app sul telefono:

- Nuova attività: Fallo, Posticipa, Segna come fatto.
- Bozza pronta: Apri bozza, Posticipa, Segna come fatto.
- Risultato pronto: Apri, Segna come fatto, Posticipa.
- Domanda, bloccata o accesso richiesto: Rispondi, Apri o Accedi, poi Posticipa e Segna come fatto.
- Promemoria: Segna come fatto, Posticipa, Apri.
- Riepilogo del mattino: toccalo per aprirlo.

Un browser e Telegram ne mostrano due. Le domande del Fleet mantengono Rispondi una volta e Rifiuta.

Da una notifica non si invia, non si paga e non si inoltra mai nulla. Una bozza si apre sempre prima, così la vedi prima che parta. Apri bozza mostra l’attività nella tua lista con la bozza completa. Fallo avvia solo il lavoro su una nuova attività.

Nell’app, Posticipa e Segna come fatto chiedono prima di sbloccare. In un browser aprono la dashboard, che lo fa e mostra Annulla. Posticipa riporta l’attività tra due ore, o domani mattina su un promemoria.

Le email con ciò che ti aspetta hanno i link Apri e Posticipa. Aprono solo la dashboard.

## Il riepilogo del mattino

Arriva nei giorni lavorativi all'ora del **Riepilogo del mattino**, a meno che non ci sia niente da dire. Se è prima di **I posticipi arrivano alle**, aspetta fino a 5 minuti dopo, così include le attività che tornano quella mattina. **Anteprima**, nella sua riga, lo mostra senza inviarlo. Di default è una push e un'email, brevi da leggere con un colpo d'occhio:

- un saluto con ciò che conta oggi, come "Buongiorno Sam, 2 risposte sono pronte da inviare" o, per un'attività, "Buongiorno Sam, da approvare: Invia il modulo d'ordine";
- al massimo tre cose da fare, ognuna con un link Apri: prima le bozze pronte e le promesse in scadenza oggi;
- quante altre possono aspettare e quanto ti richiedono al tuo ritmo, come "Altre 12 possono aspettare, circa 5 min per sbrigarle." Le attività che aspettano la tua risposta non contano in quel tempo.
- le tue riunioni in una riga.

Apri mostra l'attività evidenziata nel tuo elenco. Se è fatta, posticipata o in un'altra vista, si apre la sua chat. Una promessa apre la sua attività, o la sua pagina se non ne ha ancora una.

La push dice lo stesso senza link. Toccala, o tocca il link alla fine dell’email, per rileggere questo riepilogo in **Attività**.

Alla fine ci sono i tuoi riepiloghi **Lavoro** e **Personale**, lo stesso testo che copia **Riepilogo** nelle attività, senza le attività già elencate sopra. Quando il testo delle attività è nascosto nelle notifiche, non ci sono.

## Il riepilogo della sera

Arriva una volta nei giorni lavorativi alla sua ora in **Orario di lavoro**, di default 15 minuti prima di **Fino alle**, nei modi scelti nella sua riga qui sopra. Un giorno senza attività fatte né riunioni tenute non ne riceve. Inizia con la tua giornata in un numero, come "Buonasera Sam, oggi 4 attività fatte", poi una parte **Lavoro** e una parte **Personale**. Una parte vuota viene omessa. Ognuna ha:

- le riunioni del giorno su una riga a sé, come "3 riunioni: Chiamata prezzi e altre 2.";
- **Fatto oggi**: fino a tre attività che tu o la tua Machine avete finito, e quante altre;
- **Aperto per domani** (di venerdì, il tuo prossimo giorno lavorativo): le prime riunioni e cosa scade.

Finisce con quante attività hanno ancora bisogno di te. Tocca la notifica push, o il link alla fine dell’email, per rileggerlo, con **Copia Lavoro** e **Copia Personale**. Per non riceverlo, disattiva la sua riga.

## Privacy

Le push vanno dalla tua Machine direttamente al tuo dispositivo, crittografate per quel dispositivo. Il control plane non le vede mai. Le email le invia il server di posta di The Machine all'indirizzo del tuo account, quindi il testo passa da lì e dal provider di posta. Quando [Prudente](security-levels.md) nasconde il testo delle attività nelle notifiche, le email contengono solo conteggi. Disattiva **Email** per un tipo per tenerlo del tutto fuori dalle email.

Attiva le push per un dispositivo in **Questo dispositivo**, oppure vedi [Installa l'app](phone-app.md).
