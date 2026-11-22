---
title: Notifiche
area: settings
summary: Cosa ti raggiunge, dove e quando: solo ciò che non può aspettare ti avvisa, il resto arriva in un unico riepilogo mattutino.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: aab523e3a774400b
---
Vuoi meno notifiche o notifiche diverse? In **Impostazioni**, **Notifiche**, scegli dove ricevere ogni tipo:

- **Nuove attività**: solo ciò che non può aspettare, come qualcosa in scadenza oggi o urgente.
- **Risultati e domande**: una risposta pronta da inviare, un accesso richiesto da un’attività o una domanda di Fleet.
- **Promemoria**: attività posticipate e risposte che stai aspettando e che tornano a farsi sentire.
- **Riepilogo del mattino**: un breve riepilogo della giornata. Vedi sotto.
- **Riepilogo della sera**: cosa hai fatto oggi e cosa resta aperto per domani. Vedi sotto.

Per ogni tipo puoi attivare o disattivare **Push** (l’app sul telefono o sul computer), **Telegram** una volta configurato e **Email** su una Machine ospitata o su una collegata a The Machine Network. Sono tutti attivi, tranne i riepiloghi su Telegram.

Nella stessa scheda trovi anche il tuo **Orario di lavoro**: giorni lavorativi, orari in cui possono arrivare le notifiche, quando tornano le attività posticipate, gli orari dei riepiloghi e il fuso orario. Vedi [Orario di lavoro](work-hours.md).

## Solo ciò che non può aspettare

Ricevi una notifica push, un avviso su Telegram o un’email solo per:

- un’attività in scadenza oggi o contrassegnata come urgente;
- una risposta che qualcuno aspetta, preparata e pronta da inviare;
- un’attività che richiede il tuo accesso;
- un’attività posticipata che torna all’ora scelta.

Tutto il resto arriva senza avvisi sulla dashboard e in silenzio su Telegram, in attesa del riepilogo del mattino. Nei giorni di riposo ricevi avvisi solo per ciò che è urgente o in scadenza oggi. Al massimo 8 notifiche push al giorno. Se non apri la dashboard per 3 giorni, ricevi solo il riepilogo del mattino finché non torni.

## Quando arrivano le notifiche

Il sistema controlla se stai usando davvero la dashboard, non solo se è aperta:

- Se la stai usando, cioè è in primo piano e hai cliccato, digitato o scorso la pagina negli ultimi 10 minuti, non ricevi avvisi. Su Telegram arriva in silenzio. Aprirla o ricaricarla da solo non conta.
- Se non ci sei, cioè la dashboard è in background, chiusa o inattiva da 10 minuti, ricevi una notifica push un minuto dopo averla lasciata, a meno che tu non sia tornato e non l’abbia già vista.
- Se dopo 15 minuti non l’hai ancora vista e non può aspettare, ricevi un’email, al massimo una all’ora. Le cose che hai già gestito vengono escluse. Nella maggior parte dei giorni, l’unica email è il riepilogo del mattino.
- Se un compagno di squadra ti assegna un’attività e la tua Machine non può raggiungerti tramite telefono o Telegram, ricevi un’email con il titolo e un link, dopo 15 minuti se non l’hai ancora vista. Disattiva **Email** per **Risultati e domande** per non riceverla.
- Fuori dal tuo orario di lavoro non ricevi notifiche. L’attività sarà nel riepilogo del mattino.
- Una nuova attività di lavoro assegnata in un giorno di riposo aspetta l’orario del riepilogo del tuo prossimo giorno lavorativo. L’attività mostra quando ti raggiungerà, per esempio: Notifica lun 2 nov · 08:30.

Gli aggiornamenti sullo stato di avanzamento e le modifiche non generano notifiche. Se arriva un nuovo risultato per un’attività che non hai ancora visto, l’attività si aggiorna senza una nuova notifica. Più notifiche ravvicinate diventano un solo avviso. L’icona dell’app mostra quante attività richiedono la tua attenzione.

## Pulsanti nelle notifiche

Ogni notifica include pulsanti per il passaggio successivo. Nell’app per telefono:

- Nuova attività: **Fallo**, **Posticipa**, **Segna come fatto**.
- Bozza pronta: **Apri bozza**, **Posticipa**, **Segna come fatto**.
- Risultato pronto: **Apri**, **Segna come fatto**, **Posticipa**.
- Domanda, attività bloccata o richiesta di accesso: **Rispondi**, **Apri** o **Accedi**, poi **Posticipa** e **Segna come fatto**.
- Promemoria: **Segna come fatto**, **Posticipa**, **Apri**.
- Riepilogo del mattino: toccalo per aprirlo.

Nel browser e su Telegram ne compaiono due. Per le domande di Fleet, puoi scegliere **Rispondi** o **Rifiuta**.

Una notifica non invia, paga o inoltra nulla. Una bozza si apre sempre prima, così puoi controllarla. **Apri bozza** mostra l’attività nella tua lista con la bozza completa. **Fallo** avvia il lavoro solo per una nuova attività.

Nell’app per telefono, **Posticipa** e **Segna come fatto** ti chiedono prima di sbloccare l’app. Nel browser aprono la dashboard, che esegue l’azione e mostra **Annulla**. **Posticipa** fa ricomparire l’attività tra due ore o, per un promemoria, la mattina dopo.

Le email includono link **Apri** e, per le cose in attesa, **Posticipa**. Aprono solo la dashboard.

Se tocchi una notifica o **Apri** in un’email o su Telegram, l’attività appare nella tua lista, evidenziata e nella vista in cui si trova in quel momento: **Appena fatto**, **Fatto**, **Torna più tardi** o un’altra vista. La chat non si apre mai. Se la pagina non si è ancora aggiornata, segue l’attività non appena lo fa.

## Il riepilogo del mattino

Arriva nei giorni lavorativi all’ora impostata per **Riepilogo del mattino**, a meno che non ci sia nulla da segnalare. Se l’orario è prima di **I posticipi arrivano alle**, aspetta fino a 5 minuti dopo, così include le attività che tornano quella mattina. **Anteprima** lo mostra senza inviarlo. Per impostazione predefinita arriva come notifica push e via email, in forma abbastanza breve da leggerlo al volo:

- un saluto con ciò che conta oggi, per esempio «Buongiorno Sam, ci sono 2 risposte pronte da inviare» oppure, per una sola attività, «Buongiorno Sam, pronta per la tua conferma: invia il modulo d’ordine»;
- le attività conteggiate nel saluto, ognuna con un link **Apri**, e quelle in scadenza oggi; altrimenti, al massimo tre cose da fare;
- fino a cinque attività che hai aggiunto tu e che aspettano una tua risposta, indipendentemente da quelle conteggiate nel saluto;
- quante altre possono aspettare e quanto tempo ti serve al tuo ritmo, per esempio «Altre 12 possono aspettare, ti bastano circa 5 min per sbrigartene». Le attività in attesa di una tua risposta non rientrano nel tempo. Un’attività in scadenza oggi ma posticipata a più tardi, o su cui The Machine sta ancora lavorando, non viene conteggiata finché non aspetta una tua risposta. Il numero corrisponde alle attività in attesa nella tua lista.
- una riga con le tue riunioni.

**Apri** mostra l’attività nella tua lista, evidenziata, anche se è stata completata o posticipata. Una promessa apre la relativa attività oppure, se non ne ha ancora una, la sua pagina.

La notifica push riporta le stesse informazioni, senza link. Toccala, oppure usa il link in fondo all’email, per rileggere il riepilogo in **Attività**.

## Il riepilogo della sera

Arriva una volta nei giorni lavorativi, all’orario impostato in **Orario di lavoro**. Per impostazione predefinita, 15 minuti prima di **Fino alle**, usando i canali scelti nella riga qui sopra. Arriva solo nei giorni in cui eri presente: hai usato la dashboard oppure hai scelto cosa fare per un’attività lì, su Telegram, in chat o a voce. Se non hai completato attività né partecipato a riunioni, non lo ricevi.

Comincia con il riepilogo della giornata, per esempio «Buonasera Sam, oggi hai completato 4 attività», poi include una sezione **Lavoro** e una **Personale**. Le sezioni vuote non vengono mostrate. Ognuna include:

- **Fatto oggi**: fino a tre attività completate da te o dalla tua Machine, poi «+12 altre» e le riunioni della giornata, per esempio «+3 riunioni: chiamata sui prezzi e altre 2»;
- **Aperto per domani** (il tuo prossimo giorno lavorativo, se è venerdì): le prime riunioni e le attività in scadenza.

Termina con il numero di attività che richiedono ancora la tua attenzione. Tocca la notifica push o il link in fondo all’email per rileggerlo, con **Copia Lavoro** e **Copia Personale**. Per non riceverlo più, disattiva la relativa riga.

## Privacy

La notifica push viene inviata dalla tua Machine direttamente al dispositivo, in forma crittografata. Le email passano dal server di posta di The Machine e dal tuo provider di posta. Se [Modalità attenta](security-levels.md) nasconde il testo delle attività nelle notifiche, le email mostrano solo i numeri. Disattiva **Email** per un tipo di notifica per escluderlo dalle email.

Attiva le notifiche push per un dispositivo in **Questo dispositivo** oppure consulta [Installare l’app](phone-app.md). L’[app mobile](mobile-app.md) invia una semplice notifica tramite Apple o Google, poi chiede alla tua Machine il titolo e il passaggio successivo.
