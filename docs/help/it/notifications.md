---
title: Notifiche
area: settings
summary: Cosa ti arriva, dove e quando: solo quello che non può aspettare ti avvisa. Il resto è in un unico riepilogo mattutino.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 3c469ec1032f6bea
---
Vuoi meno notifiche o notifiche diverse? In **Impostazioni**, **Notifiche**, scegli dove ricevere ogni tipo:

- **Nuove attività**: solo quelle che non possono aspettare, per esempio qualcosa in scadenza oggi o urgente.
- **Risultati e domande**: una risposta pronta da inviare, un’attività che richiede l’accesso o una domanda su Fleet.
- **Promemoria**: le attività posticipate e le risposte che stai aspettando, quando tornano.
- **Riepilogo del mattino**: un breve riepilogo della giornata. Vedi sotto.
- **Riepilogo della sera**: cosa hai fatto oggi e cosa resta da fare domani. Vedi sotto.

Per ogni tipo puoi attivare o disattivare **Push** (l’app sul telefono o sul computer), **Telegram** dopo averlo configurato e **Email** su una Machine ospitata o su una Machine nella The Machine Network. Sono tutti attivi, tranne i riepiloghi su Telegram.

Nella stessa scheda trovi anche il tuo **Orario di lavoro**: i giorni lavorativi, quando possono arrivare le notifiche, quando tornano le attività posticipate, gli orari dei riepiloghi e il tuo fuso orario. Vedi [Orario di lavoro](work-hours.md).

## Solo quello che non può aspettare

Una notifica push, un avviso su Telegram o un’email arrivano solo per:

- un’attività in scadenza oggi o contrassegnata come urgente;
- una risposta che qualcuno aspetta, preparata e pronta da inviare;
- un’attività per cui devi accedere;
- un’attività posticipata che torna all’ora che hai scelto.

Tutto il resto compare senza avvisarti sulla dashboard (e senza avviso su Telegram) e aspetta il riepilogo del mattino. Nei giorni liberi, ricevi notifiche solo per ciò che è urgente o in scadenza oggi. Al massimo 8 notifiche push al giorno. Se non apri la dashboard per 3 giorni, ricevi solo il riepilogo del mattino finché non torni.

## Quando arrivano le notifiche

La Machine controlla se stai usando davvero la dashboard, non solo se è aperta:

- Se la stai usando (è in primo piano e hai fatto clic, digitato o scorso la pagina negli ultimi 10 minuti), non ricevi avvisi. Su Telegram arrivano senza avviso. Aprire o ricaricare la pagina, da solo, non conta.
- Se non ci sei (la dashboard è in secondo piano, chiusa o inattiva da 10 minuti), la notifica push arriva un minuto dopo che te ne sei andato, a meno che tu non sia tornato e l’abbia vista.
- Se dopo 15 minuti non hai ricevuto nulla e non può aspettare, ricevi un’email, al massimo una all’ora. Esclude ciò che hai visto o gestito e include ogni attività una sola volta, con lo stato attuale. Nella maggior parte dei giorni, l’unica email è il riepilogo del mattino.
- Una notifica è considerata ricevuta se è comparsa sul telefono o nel browser, oppure se Telegram ha ricevuto il messaggio. Un telefono spento, senza connessione o con le notifiche disattivate non conta. Lo stesso vale per Telegram mentre usi la dashboard. Se l’hai vista solo sul computer, ciò che è urgente o in scadenza oggi ti arriva comunque via email: potresti non esserci.
- Se non hai l’app sul telefono, le notifiche del browser o Telegram, ricevi un’email per tutti i casi elencati sopra.
- Se Telegram non è raggiungibile, la notifica push viene comunque inviata una volta e Telegram viene riprovato automaticamente.
- Se un compagno di squadra ti assegna un’attività e la tua Machine non ha né un telefono né Telegram per raggiungerti, dopo 15 minuti ricevi un’email con il titolo e un link, se non l’hai ancora vista. Disattiva **Email** per **Risultati e domande** per non riceverla.
- Fuori dal tuo orario di lavoro non arriva nulla. Trovi tutto nel riepilogo del mattino.
- Una nuova attività di lavoro in un giorno libero aspetta l’orario del riepilogo del tuo prossimo giorno lavorativo. Nell’attività vedi quando ti verrà notificata, per esempio Notifica lun 2 nov · 08:30.

Gli aggiornamenti e le modifiche non generano mai notifiche. Se arriva un nuovo risultato per un’attività che non hai ancora visto, l’attività si aggiorna senza una nuova notifica. Più notifiche ravvicinate vengono raccolte in un unico avviso. L’icona dell’app mostra quante attività richiedono la tua attenzione.

## Pulsanti nelle notifiche

Ogni notifica ha dei pulsanti per il passaggio successivo. Nell’app per il telefono:

- Nuova attività: **Fallo**, **Posticipa**, **Segna come fatto**.
- Bozza pronta: **Apri bozza**, **Posticipa**, **Segna come fatto**.
- Risultato pronto: **Apri**, **Segna come fatto**, **Posticipa**.
- Serve una risposta, c’è un blocco o devi accedere: **Rispondi**, **Apri** o **Accedi**, poi **Posticipa** e **Segna come fatto**.
- Promemoria: **Segna come fatto**, **Posticipa**, **Apri**.
- Riepilogo del mattino: toccalo per aprirlo.

Nel browser e su Telegram ne compaiono due. Per le domande su Fleet restano sempre disponibili **Rispondi** e **Rifiuta**.

Da una notifica non viene inviato, pagato o inoltrato nulla. Una bozza si apre sempre per prima, così puoi vederla prima che venga inviata. **Apri bozza** mostra l’attività nell’elenco con la bozza completa. **Fallo** avvia il lavoro solo per una nuova attività.

Nell’app per il telefono, **Posticipa** e **Segna come fatto** richiedono prima lo sblocco. Nel browser si apre la dashboard, dove l’azione viene eseguita e puoi annullarla. **Posticipa** fa tornare l’attività tra due ore oppure, per un promemoria, domani mattina.

Le email hanno link **Apri** (e **Posticipa** per ciò che è in attesa). Aprono solo la dashboard.

Toccando una notifica, oppure **Apri** in un’email o su Telegram, trovi l’attività evidenziata nel tuo elenco, ovunque si trovi: **Appena fatto**, **Fatto**, **Torna più tardi** o un’altra vista. La chat non si apre mai. Se la pagina non era ancora aggiornata, l’attività ti segue quando lo sarà.

## Il riepilogo del mattino

Arriva nei giorni lavorativi all’ora impostata in **Riepilogo del mattino**, a meno che non ci sia nulla da segnalare. Se quell’ora è precedente a **I posticipi arrivano alle**, aspetta fino a 5 minuti dopo, così include le attività che tornano quella mattina. **Anteprima** lo mostra senza inviarlo. Per impostazione predefinita arriva come notifica push e via email. È abbastanza breve da leggere al volo:

- un saluto con le informazioni importanti della giornata, per esempio «Buongiorno Sam, ci sono 2 risposte pronte da inviare» oppure, per una sola attività, «Buongiorno Sam, serve la tua conferma: invia il modulo d’ordine». Sono considerate pronte solo le attività con una bozza o un risultato da approvare. Non lo è un’attività che prima richiede una tua risposta;
- le attività incluse nel saluto, ognuna con un link **Apri**, e quelle in scadenza oggi; altrimenti, al massimo tre cose da fare;
- fino a cinque attività che hai aggiunto tu e che aspettano il tuo intervento, indipendentemente da quelle incluse nel saluto;
- quante altre attività possono aspettare e quanto tempo ci vorrà al tuo ritmo, per esempio «Altre 12 possono aspettare, ci vorranno circa 5 min». Il tempo non include le attività che aspettano una tua risposta. Un’attività in scadenza oggi ma posticipata a più tardi, o su cui la Machine sta ancora lavorando, non viene conteggiata finché non richiede il tuo intervento. Il numero corrisponde alle attività in attesa nel tuo elenco.
- una riga con le riunioni.

**Apri** mostra l’attività evidenziata nel tuo elenco, anche se è completata o posticipata. Una promessa apre l’attività corrispondente oppure, se non ne ha ancora una, la sua pagina.

La notifica push contiene le stesse informazioni, senza link. Toccala oppure usa il link in fondo all’email per rileggere il riepilogo in **Attività**.

## Il riepilogo della sera

Arriva una volta nei giorni lavorativi, all’ora impostata in **Orario di lavoro**. Per impostazione predefinita, arriva 15 minuti prima di **Fino alle**, usando i canali scelti nella riga qui sopra. Arriva solo nei giorni in cui eri presente: hai usato la dashboard oppure hai scelto cosa fare per un’attività, lì, su Telegram, in chat o a voce. Se non hai completato attività né partecipato a riunioni, non ricevi il riepilogo.

Inizia con un conteggio della giornata, per esempio «Buonasera Sam, oggi hai completato 4 attività», poi mostra una sezione **Lavoro** e una **Personale**. Le sezioni vuote non vengono mostrate. Gli avvisi sulla tua Machine non sono inclusi in nessuna delle due. Ogni sezione include:

- **Fatto oggi**: fino a tre attività completate da te o dalla tua Machine, poi «+altre 12» e le riunioni della giornata, per esempio «+3 riunioni: chiamata sui prezzi e altre 2»;
- **Aperto per domani** (il prossimo giorno lavorativo, se è venerdì): le prime riunioni e le attività in scadenza.

Si conclude con il numero di attività che richiedono ancora il tuo intervento. Tocca la notifica push o il link in fondo all’email per rileggerlo, con **Copia Lavoro** e **Copia Personale**. Per non riceverlo più, disattiva la relativa riga.

## Privacy

La notifica push viene inviata direttamente dalla tua Machine al dispositivo, con crittografia. L’email passa dal server di posta di The Machine e dal tuo provider email. Quando [Modalità prudente](security-levels.md) nasconde il testo delle attività nelle notifiche, le email mostrano solo i conteggi. Disattiva **Email** per un tipo di notifica per escluderlo dalle email.

Attiva le notifiche push per un dispositivo in **Questo dispositivo** oppure consulta [Installa l’app](phone-app.md). L’[app per dispositivi mobili](mobile-app.md) invia una riga di testo tramite Apple o Google, poi chiede alla tua Machine il titolo e il passaggio successivo.
