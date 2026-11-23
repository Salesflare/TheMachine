---
title: Notifiche
area: settings
summary: Cosa ti arriva, dove e quando: solo ciò che non può aspettare ti avvisa subito, il resto è nel riepilogo del mattino.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 3faac166e8f9fa3d
---
Vuoi meno notifiche o notifiche diverse? In **Impostazioni**, **Notifiche**, scegli dove ricevere ogni tipo:

- **Nuove attività**: solo quelle che non possono aspettare, per esempio qualcosa in scadenza oggi o urgente.
- **Risultati e domande**: una risposta pronta da inviare, un accesso necessario per un’attività o una domanda di Fleet.
- **Promemoria**: attività posticipate e risposte che stai aspettando, quando tornano.
- **Riepilogo del mattino**: un breve riepilogo della giornata. Vedi sotto.
- **Riepilogo della sera**: cosa hai fatto oggi e cosa resta da fare domani. Vedi sotto.

Per ogni tipo puoi attivare o disattivare **Push** (l’app sul telefono o sul computer), **Telegram** una volta configurato e **Email** su una Machine ospitata o su una Machine collegata a The Machine Network. Sono tutti attivi, tranne i riepiloghi su Telegram.

Nella stessa scheda trovi anche il tuo **Orario di lavoro**: giorni lavorativi, orari in cui possono arrivare le notifiche, quando tornano le attività posticipate, orari dei riepiloghi e fuso orario. Vedi [Orario di lavoro](work-hours.md).

## Solo ciò che non può aspettare

Una notifica push, un avviso su Telegram o un’email arriva solo per:

- un’attività in scadenza oggi o contrassegnata come urgente;
- una risposta che qualcuno sta aspettando, preparata e pronta da inviare;
- un’attività per cui devi accedere;
- un’attività posticipata che torna all’ora scelta.

Tutto il resto compare senza avvisi nella dashboard (e senza suono su Telegram) e aspetta il riepilogo del mattino. Nei giorni liberi, ricevi un avviso solo per ciò che è urgente o in scadenza oggi. Al massimo 8 notifiche push al giorno. Se non apri la dashboard per 3 giorni, ricevi solo il riepilogo del mattino, finché non torni.

## Quando arrivano le notifiche

Controlla se stai usando davvero la dashboard, non solo se è aperta:

- Se la stai usando (è in primo piano e hai fatto clic, scritto o scorrimento negli ultimi 10 minuti), non ricevi avvisi. Su Telegram arrivano senza suono. Aprire o ricaricare la pagina non basta.
- Se non ci sei (è in secondo piano, chiusa o inattiva da 10 minuti), ricevi una notifica push un minuto dopo averla lasciata, a meno che tu non sia tornato e l’abbia vista.
- Se dopo 15 minuti non l’hai ancora vista e non può aspettare, ricevi un’email, al massimo una all’ora. Non include ciò che hai già gestito e ogni attività compare una sola volta, con lo stato aggiornato. Nella maggior parte dei giorni, il riepilogo del mattino è l’unica email.
- Se un compagno di squadra ti assegna un’attività e la tua Machine non può contattarti sul telefono o su Telegram, ricevi un’email con il titolo e un link, dopo 15 minuti se non l’hai ancora vista. Disattiva **Email** per **Risultati e domande** per non riceverla.
- Fuori dal tuo orario di lavoro non ricevi notifiche. L’attività compare nel riepilogo del mattino.
- Una nuova attività di lavoro in un giorno libero aspetta l’orario del riepilogo del tuo prossimo giorno lavorativo. L’attività indica quando ti verrà inviata, per esempio Notifica lun 2 nov · 08:30.

Gli aggiornamenti sui progressi e le modifiche non generano notifiche. Se arriva un nuovo risultato per un’attività che non hai ancora visto, questa si aggiorna senza una nuova notifica. Se arrivano più notifiche insieme, ne ricevi una sola. L’icona dell’app mostra quante attività richiedono la tua attenzione.

## Pulsanti nelle notifiche

Ogni notifica ha pulsanti per il passaggio successivo. Nell’app per telefono:

- Nuova attività: **Fallo**, **Posticipa**, **Segna come fatto**.
- Bozza pronta: **Apri bozza**, **Posticipa**, **Segna come fatto**.
- Risultato pronto: **Apri**, **Segna come fatto**, **Posticipa**.
- Serve una risposta, c’è un blocco o devi accedere: **Rispondi**, **Apri** o **Accedi**, poi **Posticipa** e **Segna come fatto**.
- Promemoria: **Segna come fatto**, **Posticipa**, **Apri**.
- Riepilogo del mattino: toccalo per aprirlo.

Il browser e Telegram ne mostrano due. Per le domande di Fleet trovi sempre **Rispondi** e **Rifiuta**.

Una notifica non invia, paga o invia nulla al posto tuo. Una bozza si apre sempre prima, così puoi controllarla prima che venga inviata. **Apri bozza** mostra l’attività nell’elenco con la bozza completa. **Fallo** avvia il lavoro solo per una nuova attività.

Nell’app per telefono, **Posticipa** e **Segna come fatto** ti chiedono prima di sbloccare il telefono. Nel browser si apre la dashboard, dove l’azione viene eseguita e puoi annullarla. **Posticipa** fa tornare l’attività tra due ore oppure, per un promemoria, il mattino dopo.

Le email contengono link **Apri** (e **Posticipa** per ciò che stai aspettando). Aprono solo la dashboard.

Toccando una notifica, oppure **Apri** in un’email o su Telegram, l’attività viene mostrata nell’elenco, evidenziata e nella sezione in cui si trova: **Appena fatto**, **Fatto**, **Torna più tardi** o un’altra vista. La chat non si apre mai. Se la pagina non era ancora aggiornata, segue l’attività non appena lo è.

## Il riepilogo del mattino

Arriva nei giorni lavorativi all’orario del **Riepilogo del mattino**, a meno che non ci sia nulla da segnalare. Se quell’orario è prima di **I posticipi arrivano alle**, aspetta fino a 5 minuti dopo, così include le attività che tornano quella mattina. **Anteprima** lo mostra senza inviarlo. Per impostazione predefinita arriva come notifica push e via email, ed è abbastanza breve da leggere in un attimo:

- un saluto con le cose importanti della giornata, per esempio «Buongiorno Sam, ci sono 2 risposte pronte da inviare» oppure, per una sola attività, «Buongiorno Sam, serve il tuo OK: invia il modulo d’ordine». Sono considerate pronte solo le attività con una bozza o un risultato da approvare; quelle che richiedono prima una tua risposta non lo sono;
- le attività conteggiate nel saluto, ognuna con un link **Apri**, e le scadenze di oggi; altrimenti, al massimo tre cose da fare;
- fino a cinque attività che hai aggiunto tu e che aspettano un tuo intervento, indipendentemente da quelle conteggiate nel saluto;
- quante altre attività possono aspettare e quanto tempo richiedono al tuo ritmo, per esempio «Altre 12 possono aspettare, circa 5 min per smaltirle». Il tempo non include le attività che aspettano una tua risposta. Le attività in scadenza oggi ma posticipate a più tardi, o su cui la Machine sta ancora lavorando, non vengono conteggiate finché non aspettano un tuo intervento. Il conteggio corrisponde alle attività in attesa nel tuo elenco;
- le tue riunioni, in una riga.

**Apri** mostra l’attività nell’elenco, evidenziata, anche se è stata completata o posticipata. Una promessa apre la relativa attività oppure, se non ne ha ancora una, la sua pagina.

La notifica push mostra le stesse informazioni, senza link. Tocca la notifica o il link in fondo all’email per rileggere il riepilogo in **Attività**.

## Il riepilogo della sera

Arriva una volta nei giorni lavorativi, all’orario impostato in **Orario di lavoro** e, per impostazione predefinita, 15 minuti prima di **Fino alle**, usando i canali scelti nella relativa riga qui sopra. Arriva solo nei giorni in cui hai usato la dashboard o hai scelto cosa fare per un’attività, lì, su Telegram, in chat o a voce. Se quel giorno non hai completato attività né partecipato a riunioni, non ne ricevi uno.

Inizia con un conteggio della giornata, per esempio «Buonasera Sam, oggi hai completato 4 attività», seguito da una sezione **Lavoro** e una **Personale**. Le sezioni vuote non vengono mostrate. Ognuna include:

- **Fatto oggi**: fino a tre attività completate da te o dalla tua Machine, poi «+12 altre» e le riunioni della giornata, per esempio «+3 riunioni: chiamata sui prezzi e altre 2»;
- **Aperto per domani** (o per il prossimo giorno lavorativo, se è venerdì): le prime riunioni e le attività in scadenza.

Alla fine indica quante attività richiedono ancora la tua attenzione. Tocca la notifica push o il link in fondo all’email per rileggerlo, con **Copia Lavoro** e **Copia Personale**. Per non riceverlo più, disattiva la relativa riga.

## Privacy

La notifica push viene inviata direttamente dalla tua Machine al dispositivo, in forma cifrata. L’email passa dal server di posta di The Machine e dal tuo provider di posta. Quando [Attento](security-levels.md) nasconde il testo delle attività nelle notifiche, le email mostrano solo i conteggi. Disattiva **Email** per un tipo di notifica per escluderlo dalle email.

Attiva le notifiche push per un dispositivo in **Questo dispositivo** oppure consulta [Installa l’app](phone-app.md). L’[app mobile](mobile-app.md) invia una semplice riga tramite Apple o Google, poi chiede alla tua Machine il titolo e il passaggio successivo.
