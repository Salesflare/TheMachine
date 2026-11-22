---
title: Notifiche
area: settings
summary: Cosa ti arriva, dove e quando: solo ciò che non può aspettare ti avvisa subito, il resto è nel riepilogo del mattino.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 4a782ad03270e7b0
---
Vuoi meno notifiche o notifiche diverse? In **Impostazioni** > **Notifiche**, scegli dove ricevere ogni tipo:

- **Nuove attività**: solo ciò che non può aspettare, come un’attività in scadenza oggi o urgente.
- **Risultati e domande**: una risposta pronta da inviare, un accesso richiesto per un’attività o una domanda di Fleet.
- **Promemoria**: le attività posticipate e le risposte che stai aspettando, quando tornano.
- **Riepilogo del mattino**: un breve riepilogo della giornata. Vedi sotto.
- **Riepilogo della sera**: cosa hai fatto oggi e cosa resta da fare domani. Vedi sotto.

Per ogni tipo puoi attivare o disattivare **Push** (l’app sul telefono o sul computer), **Telegram** una volta configurato e **Email** su una Machine ospitata o su una Machine collegata a The Machine Network. Sono tutti attivi, tranne i riepiloghi su Telegram.

Nella stessa scheda trovi anche l’**Orario di lavoro**: i giorni lavorativi, quando possono arrivare le notifiche, quando tornano le attività posticipate, gli orari dei riepiloghi e il fuso orario. Vedi [Orario di lavoro](work-hours.md).

## Solo ciò che non può aspettare

Ricevi una notifica push, un avviso su Telegram o un’email solo per:

- un’attività in scadenza oggi o contrassegnata come urgente;
- una risposta che qualcuno sta aspettando, preparata e pronta da inviare;
- un’attività per cui devi accedere;
- un’attività posticipata che torna all’ora scelta.

Tutto il resto compare senza avvisi sulla dashboard (e senza notifiche su Telegram) e aspetta il riepilogo del mattino. Nei giorni non lavorativi ricevi un avviso solo per ciò che è urgente o in scadenza oggi. Al massimo 8 notifiche push al giorno. Se non apri la dashboard per 3 giorni, ricevi solo il riepilogo del mattino finché non torni.

## Quando arrivano le notifiche

Il sistema controlla se stai usando davvero la dashboard, non solo se è aperta:

- Se la stai usando, cioè è in primo piano e hai cliccato, digitato o scorso la pagina negli ultimi 10 minuti, non ricevi avvisi. Su Telegram le notifiche arrivano senza suono. Aprire o ricaricare la pagina non basta.
- Se non ci sei, cioè la dashboard è in background, chiusa o inattiva da 10 minuti, ricevi una notifica push un minuto dopo averla lasciata, a meno che tu non sia tornato e l’abbia vista.
- Se dopo 15 minuti non l’hai ancora vista e non può aspettare, ricevi un’email, al massimo una all’ora. Le attività che hai già gestito non vengono incluse. Quasi sempre, l’unica email che ricevi è il riepilogo del mattino.
- Se un collega ti assegna un’attività e la tua Machine non ha un telefono o Telegram su cui raggiungerti, ricevi un’email con il titolo e un link, dopo 15 minuti se non l’hai ancora vista. Disattiva **Email** per **Risultati e domande** per non riceverla.
- Fuori dal tuo orario di lavoro non ricevi nulla. L’attività sarà nel riepilogo del mattino.
- Una nuova attività di lavoro in un giorno non lavorativo aspetta l’orario del riepilogo del tuo prossimo giorno lavorativo. L’attività mostra quando ti verrà inviata la notifica, per esempio: Notifica lun 2 nov · 08:30.

Gli aggiornamenti sullo stato e le modifiche non generano notifiche. Se arriva un nuovo risultato per un’attività che non hai ancora visto, l’attività si aggiorna senza una nuova notifica. Se arrivano più notifiche insieme, ne ricevi una sola. L’icona dell’app mostra quante attività richiedono il tuo intervento.

## Pulsanti nelle notifiche

Ogni notifica ha pulsanti per il passaggio successivo. Nell’app per telefono:

- Nuova attività: **Fallo**, **Posticipa**, **Segna come fatto**.
- Bozza pronta: **Apri bozza**, **Posticipa**, **Segna come fatto**.
- Risultato pronto: **Apri**, **Segna come fatto**, **Posticipa**.
- Domanda, attività bloccata o richiesta di accesso: **Rispondi**, **Apri** o **Accedi**, poi **Posticipa** e **Segna come fatto**.
- Promemoria: **Segna come fatto**, **Posticipa**, **Apri**.
- Riepilogo del mattino: toccalo per aprirlo.

Nel browser e su Telegram ne compaiono due. Per le domande di Fleet restano disponibili **Rispondi una volta** e **Rifiuta**.

Non viene inviato, pagato o inoltrato nulla da una notifica. Le bozze si aprono sempre prima, così puoi controllarle prima dell’invio. **Apri bozza** mostra l’attività nell’elenco con la bozza completa. **Fallo** avvia il lavoro solo per una nuova attività.

Nell’app per telefono, **Posticipa** e **Segna come fatto** ti chiedono prima di sbloccare il telefono. Nel browser aprono la dashboard, dove puoi completare l’azione e vedere **Annulla**. **Posticipa** fa tornare l’attività tra due ore o, per un promemoria, domani mattina.

Le email hanno link **Apri** (e **Posticipa** per ciò che stai aspettando). Aprono solo la dashboard.

Toccando una notifica, oppure **Apri** in un’email o su Telegram, vedrai l’attività evidenziata nel tuo elenco, ovunque si trovi in quel momento: **Appena fatto**, **Fatto**, **Torna più tardi** o un’altra vista. Non si apre mai la chat. Se la pagina non si è ancora aggiornata, seguirà l’attività appena sarà aggiornata.

## Il riepilogo del mattino

Arriva nei giorni lavorativi all’orario del **Riepilogo del mattino**, a meno che non ci sia nulla da segnalare. Se l’orario è precedente a **I posticipi arrivano alle**, aspetta fino a 5 minuti dopo, così include le attività che tornano quella mattina. **Anteprima** lo mostra senza inviarlo. Per impostazione predefinita arriva come notifica push e come email, ed è abbastanza breve da leggere al volo:

- un saluto con le informazioni importanti della giornata, per esempio «Buongiorno Sam, ci sono 2 risposte pronte da inviare» oppure, se c’è una sola attività, «Buongiorno Sam, serve la tua approvazione: invia il modulo d’ordine». Sono considerate pronte solo le attività con una bozza o un risultato da approvare; quelle che richiedono prima una tua risposta non lo sono;
- le attività incluse nel saluto, ognuna con un link **Apri**, e quelle in scadenza oggi; altrimenti, al massimo tre attività da fare;
- fino a cinque attività che hai aggiunto tu e che aspettano il tuo intervento, indipendentemente da quelle incluse nel saluto;
- quante altre attività possono aspettare e quanto tempo richiedono al tuo ritmo, per esempio «Altre 12 possono aspettare, circa 5 min per smaltirle». Le attività in attesa di una tua risposta non rientrano nel tempo indicato. Un’attività in scadenza oggi ma posticipata a più tardi, o su cui la Machine sta ancora lavorando, non viene conteggiata finché non richiede il tuo intervento. Il conteggio corrisponde alle attività in attesa nel tuo elenco;
- le riunioni, in una sola riga.

**Apri** mostra l’attività evidenziata nel tuo elenco, anche se è stata completata o posticipata. Una promessa apre la relativa attività oppure, se non ne ha ancora una, la sua pagina.

La notifica push riporta le stesse informazioni senza link. Toccala, oppure usa il link in fondo all’email, per rileggere il riepilogo in **Attività**.

## Il riepilogo della sera

Arriva una volta nei giorni lavorativi, all’orario impostato in **Orario di lavoro** e, per impostazione predefinita, 15 minuti prima di **Fino alle**, nei canali scelti nella relativa riga qui sopra. Arriva solo nei giorni in cui eri presente: hai usato la dashboard o hai scelto cosa fare per un’attività lì, su Telegram, in chat o con la voce. Non arriva nei giorni in cui non hai completato attività né partecipato a riunioni.

Inizia con un conteggio della giornata, per esempio «Buonasera Sam, oggi hai completato 4 attività», poi una sezione **Lavoro** e una **Personale**. Le sezioni vuote non vengono mostrate. Ognuna contiene:

- **Fatto oggi**: fino a tre attività completate da te o dalla tua Machine, poi «+12 altre» e le riunioni della giornata, per esempio «+3 riunioni: chiamata sui prezzi e altre 2»;
- **Aperto per domani** (il prossimo giorno lavorativo, se è venerdì): le prime riunioni e le attività in scadenza.

Termina indicando quante attività richiedono ancora il tuo intervento. Tocca la notifica push o il link in fondo all’email per rileggerlo, con **Copia Lavoro** e **Copia Personale**. Per non riceverlo più, disattiva la relativa riga.

## Privacy

Le notifiche push vengono inviate direttamente dalla tua Machine al dispositivo e sono cifrate per quel dispositivo. Le email passano dal server di posta di The Machine e dal tuo provider di posta. Quando [Prudente](security-levels.md) nasconde il testo delle attività nelle notifiche, le email mostrano solo i conteggi. Disattiva **Email** per un tipo di notifica per non riceverlo via email.

Attiva le notifiche push per un dispositivo in **Questo dispositivo** oppure consulta [Installa l’app](phone-app.md). L’[app mobile](mobile-app.md) invia una semplice notifica tramite Apple o Google, poi chiede alla tua Machine il titolo e il passaggio successivo.
