---
title: Notifiche
area: settings
summary: Cosa ti arriva, dove e quando: solo ciò che non può aspettare ti avvisa subito, il resto è in un unico riepilogo mattutino.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: dc56a77907df5da0
---
Vuoi meno notifiche o notifiche diverse? In **Impostazioni**, **Notifiche**, scegli dove ricevere ogni tipo:

- **Nuove attività**: solo ciò che non può aspettare, come un’attività in scadenza oggi o urgente.
- **Risultati e domande**: una risposta pronta da inviare, un’attività che richiede l’accesso o una domanda di Fleet.
- **Promemoria**: attività posticipate e risposte che stai aspettando, quando tornano.
- **Riepilogo del mattino**: un breve riepilogo della giornata. Vedi sotto.
- **Riepilogo della sera**: cosa hai fatto oggi e cosa resta da fare domani. Vedi sotto.

Per ogni tipo puoi attivare o disattivare **Push** (l’app sul telefono o sul computer), **Telegram** dopo averlo configurato e **Email** su una Machine ospitata o su una Machine nel The Machine Network. Sono tutti attivi, tranne i riepiloghi su Telegram.

Nella stessa scheda trovi anche il tuo **Orario di lavoro**: i giorni lavorativi, quando possono arrivare le notifiche, quando arrivano le attività posticipate, gli orari dei riepiloghi e il tuo fuso orario. Vedi [Orario di lavoro](work-hours.md).

## Solo ciò che non può aspettare

Una notifica push, un avviso su Telegram o un’email arrivano solo per:

- un’attività in scadenza oggi o contrassegnata come urgente;
- una risposta che qualcuno sta aspettando, preparata e pronta da inviare;
- un’attività per cui devi accedere;
- un’attività posticipata che torna all’orario scelto.

Tutto il resto compare senza avvisi sulla dashboard e in silenzio su Telegram, in attesa del riepilogo del mattino. Nei giorni non lavorativi ricevi avvisi solo per ciò che è urgente o in scadenza oggi. Al massimo 8 notifiche push al giorno. Se non apri la dashboard per 3 giorni, ricevi solo il riepilogo del mattino, finché non torni.

## Quando arrivano le notifiche

Il sistema controlla se stai usando davvero la dashboard, non solo se è aperta:

- Se la stai usando (è in primo piano e hai fatto clic, digitato o scorruto negli ultimi 10 minuti), non ricevi avvisi. I messaggi su Telegram arrivano in silenzio. Aprire o ricaricare la pagina, da solo, non conta.
- Se non ci sei (la dashboard è in secondo piano, chiusa o inattiva da 10 minuti), la notifica push arriva un minuto dopo che te ne sei andato, a meno che tu non sia tornato e l’abbia vista.
- Se dopo 15 minuti non ti è arrivato nulla e l’attività non può aspettare, ricevi un’email, al massimo una all’ora. Ciò che hai visto o gestito non viene incluso e ogni attività compare una sola volta, aggiornata a quel momento. Nella maggior parte dei giorni, il riepilogo del mattino è l’unica email.
- Per “arrivata” si intende una notifica mostrata sul telefono o nel browser, oppure un messaggio ricevuto da Telegram. Un telefono spento, offline o con le notifiche disattivate non conta. Nemmeno Telegram conta se stai usando la dashboard. Se la notifica è stata mostrata solo sul computer, ciò che è urgente o in scadenza oggi ti viene comunque inviato via email: potresti non esserci.
- Se non hai l’app per il telefono, le notifiche del browser o Telegram, ricevi un’email per tutti i casi descritti sopra.
- Se Telegram non è raggiungibile, la notifica push parte comunque, una sola volta, e il sistema riprova a inviare il messaggio su Telegram.
- Se un collega ti assegna un’attività e la tua Machine non può raggiungerti né sul telefono né su Telegram, ricevi un’email con il titolo e un link, dopo 15 minuti se non l’hai ancora vista. Disattiva **Email** per **Risultati e domande** per non riceverla.
- Se l’accesso a Claude scade entro 3 giorni o è già scaduto, ricevi un’email con **Accedi di nuovo**, una volta per ogni accesso. Disattiva **Email** per **Risultati e domande** per non riceverla.
- Fuori dal tuo orario di lavoro non arriva nulla. Trovi tutto nel riepilogo del mattino.
- Una nuova attività di lavoro assegnata in un giorno non lavorativo aspetta l’orario del riepilogo del tuo prossimo giorno lavorativo. L’attività indica quando ti verrà inviata, per esempio: Notifica lun 2 nov · 08:30.

I progressi e le modifiche non generano notifiche. Se arriva un nuovo risultato per un’attività che non hai ancora visto, questa si aggiorna senza una nuova notifica. Una serie di avvisi ravvicinati genera una sola notifica. L’icona dell’app mostra quante attività richiedono la tua attenzione.

## Pulsanti nelle notifiche

Ogni notifica ha pulsanti per il passaggio successivo. Nell’app per il telefono:

- Nuova attività: Fallo, Posticipa, Segna come fatto.
- Bozza pronta: Apri bozza, Posticipa, Segna come fatto.
- Risultato pronto: Apri, Segna come fatto, Posticipa.
- Serve una risposta, c’è un problema o devi accedere: Rispondi, Apri o Accedi, poi Posticipa e Segna come fatto.
- Promemoria: Segna come fatto, Posticipa, Apri.
- Riepilogo del mattino: toccalo per aprirlo.

Nel browser e su Telegram ne compaiono due. Per le domande di Fleet puoi sempre scegliere Rispondi o Rifiuta.

Da una notifica non viene inviato, pagato o inoltrato nulla. Una bozza si apre sempre prima, così puoi controllarla prima dell’invio. Apri bozza mostra l’attività nella tua lista con la bozza completa. Fallo avvia il lavoro solo per una nuova attività.

Nell’app per il telefono, Posticipa e Segna come fatto ti chiedono prima di sbloccare il telefono. Nel browser si apre la dashboard, che esegue l’azione e mostra Annulla. Posticipa fa tornare l’attività tra due ore o, per un promemoria, il mattino seguente.

Le email hanno link Apri (e Posticipa per ciò che è in attesa). Aprono solo la dashboard.

Toccando una notifica, oppure scegliendo Apri in un’email o su Telegram, l’attività viene mostrata nella tua lista, evidenziata e nella posizione in cui si trova in quel momento: **Appena fatto**, **Fatto**, **Torna più tardi** o un’altra vista. La chat non si apre mai. Se la pagina non è ancora aggiornata, segue l’attività appena lo è.

## Il riepilogo del mattino

Arriva nei giorni lavorativi all’orario impostato per **Riepilogo del mattino**, a meno che non ci sia nulla da segnalare. Se l’orario è prima di **I posticipi arrivano alle**, aspetta fino a 5 minuti dopo quell’orario, così include le attività che tornano quella mattina. **Anteprima** lo mostra senza inviarlo. Per impostazione predefinita arriva come notifica push e come email, ed è abbastanza breve da leggere al volo:

- un saluto con le informazioni importanti per oggi, per esempio «Buongiorno Sam, ci sono 2 risposte pronte da inviare» oppure, se c’è una sola attività, «Buongiorno Sam, serve la tua conferma: Invia il modulo d’ordine». Sono considerate pronte solo le attività con una bozza o un risultato da approvare. Un’attività che richiede prima una tua risposta non conta;
- le attività incluse nel saluto, ciascuna con un link Apri, e le attività in scadenza oggi. Se non ce ne sono, al massimo tre attività da svolgere;
- fino a cinque attività che hai aggiunto tu e che aspettano un tuo intervento, indipendentemente da quelle incluse nel saluto;
- quante altre attività possono aspettare e quanto tempo ti serve per gestirle al tuo ritmo, per esempio «Altre 12 possono aspettare, ci vorranno circa 5 min». Le attività in attesa di una tua risposta non rientrano nel calcolo. Un’attività in scadenza oggi ma posticipata a più tardi, o su cui The Machine sta ancora lavorando, non viene conteggiata finché non richiede un tuo intervento. Il numero corrisponde alle attività in attesa nella tua lista;
- le tue riunioni, in una sola riga.

Apri mostra l’attività nella tua lista, evidenziata, anche se è stata completata o posticipata. Una promessa apre la relativa attività oppure, se non ne ha ancora una, la sua pagina.

La notifica push contiene le stesse informazioni, senza link. Tocca la notifica o il link in fondo all’email per rileggere il riepilogo in **Attività**.

## Il riepilogo della sera

Arriva una volta nei giorni lavorativi, all’orario indicato in **Orario di lavoro**, per impostazione predefinita 15 minuti prima di **Fino alle**, nei modi che hai scelto nella riga qui sopra. Arriva solo nei giorni in cui eri presente: hai usato la dashboard o hai scelto cosa fare per un’attività lì, su Telegram, in chat o a voce. Se non hai completato attività e non hai partecipato a riunioni, non ricevi il riepilogo.

Inizia con un conteggio della giornata, per esempio «Buonasera Sam, hai completato 4 attività oggi», poi una sezione **Lavoro** e una **Personale**. Le sezioni vuote non vengono mostrate. Gli avvisi sulla tua Machine non sono inclusi in nessuna delle due. Ogni sezione contiene:

- **Fatto oggi**: fino a tre attività completate da te o dalla tua Machine, poi «+12 altre» e le riunioni della giornata, per esempio «+3 riunioni: chiamata sui prezzi e altre 2»;
- **Aperto per domani** (il tuo prossimo giorno lavorativo se è venerdì): le prime riunioni e le attività in scadenza.

Alla fine trovi il numero di attività che richiedono ancora la tua attenzione. Tocca la notifica push o il link in fondo all’email per rileggerlo, con **Copia Lavoro** e **Copia Personale**. Per non riceverlo più, disattiva la relativa riga.

## Privacy

La notifica push viene inviata dalla tua Machine direttamente al tuo dispositivo, con crittografia. L’email passa dal server di posta di The Machine e dal tuo provider. Quando [Attenta](security-levels.md) nasconde il testo delle attività nelle notifiche, le email mostrano solo i conteggi. Disattiva **Email** per un tipo di notifica per escluderlo dalle email.

Attiva le notifiche push per un dispositivo in **Questo dispositivo** oppure vedi [Installa l’app](phone-app.md). L’[app per dispositivi mobili](mobile-app.md) invia una semplice notifica tramite Apple o Google, poi chiede alla tua Machine il titolo e il passaggio successivo.
