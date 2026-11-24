---
title: Notifiche
area: settings
summary: Cosa ricevi, dove e quando: solo ciò che non può aspettare ti avvisa, il resto è nel riepilogo del mattino.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: bdb4ecec9446aa5e
---
Vuoi ricevere meno notifiche o notifiche diverse? In **Impostazioni**, **Notifiche**, scegli dove ricevere ogni tipo:

- **Nuove attività**: solo ciò che non può aspettare, come un’attività in scadenza oggi o urgente.
- **Risultati e domande**: una risposta pronta da inviare, un accesso richiesto per un’attività o una domanda di Fleet.
- **Promemoria**: attività posticipate e risposte che stai aspettando, quando tornano.
- **Riepilogo del mattino**: un breve riepilogo della giornata. Vedi sotto.
- **Riepilogo della sera**: cosa hai completato oggi e cosa resta da fare domani. Vedi sotto.

Ogni tipo ha un interruttore per **Push** (l’app sul telefono o sul computer), **Telegram** una volta configurato e **Email** su una Machine ospitata o collegata a The Machine Network. Sono tutti attivi, tranne i riepiloghi su Telegram.

Nella stessa scheda trovi il tuo **Orario di lavoro**: i giorni lavorativi, gli orari in cui possono arrivare le notifiche, quando tornano le attività posticipate, gli orari dei riepiloghi e il fuso orario. Vedi [Orario di lavoro](work-hours.md).

## Solo ciò che non può aspettare

Una notifica push, un avviso su Telegram o un’email arriva solo per:

- un’attività in scadenza oggi o contrassegnata come urgente;
- una risposta che qualcuno sta aspettando, preparata e pronta da inviare;
- un’attività per cui devi accedere;
- un’attività posticipata che torna all’ora che hai scelto.

Tutto il resto appare senza avvisi nella dashboard (e senza suono su Telegram) e aspetta il riepilogo del mattino. Nei giorni non lavorativi, ricevi un avviso solo per ciò che è urgente o in scadenza oggi. Al massimo 8 notifiche push al giorno. Se non apri la dashboard per 3 giorni, ricevi solo il riepilogo del mattino, finché non torni.

## Quando arrivano le notifiche

Il sistema controlla se stai usando davvero la dashboard, non solo se è aperta:

- Se la stai usando (è in primo piano e negli ultimi 10 minuti hai fatto clic, digitato o scorruto): non ricevi avvisi. Su Telegram le notifiche arrivano senza suono. Aprire o ricaricare la dashboard, da solo, non conta.
- Se non ci sei (la dashboard è in secondo piano, chiusa o inattiva da 10 minuti): ricevi una notifica push un minuto dopo averla lasciata, a meno che tu non sia tornato e l’abbia già vista.
- Se dopo 15 minuti non l’hai ancora vista e non può aspettare, ricevi un’email, al massimo una all’ora. Le attività che hai già gestito non vengono incluse e ogni attività compare una sola volta, con le informazioni aggiornate. Quasi sempre, l’unica email della giornata è il riepilogo del mattino.
- Se un collega ti assegna un’attività e la tua Machine non può raggiungerti sul telefono o su Telegram, ricevi un’email con il titolo e un link dopo 15 minuti, se non l’hai ancora vista. Disattiva **Email** per **Risultati e domande** per non riceverla.
- Fuori dal tuo orario di lavoro non ricevi nulla. L’attività compare nel riepilogo del mattino.
- Una nuova attività di lavoro in un giorno non lavorativo aspetta l’orario del riepilogo del tuo prossimo giorno lavorativo. L’attività mostra quando ti verrà segnalata, ad esempio: Notifica lun 2 nov · 08:30.

I progressi e le modifiche non generano notifiche. Se arriva un nuovo risultato per un’attività che non hai ancora visto, l’attività si aggiorna senza una nuova notifica. Se arrivano più avvisi insieme, ne ricevi uno solo. L’icona dell’app mostra quante attività richiedono la tua attenzione.

## Pulsanti delle notifiche

Ogni notifica ha pulsanti per il passaggio successivo. Nell’app per telefono:

- Nuova attività: Fallo, Posticipa, Segna come fatto.
- Bozza pronta: Apri la bozza, Posticipa, Segna come fatto.
- Risultato pronto: Apri, Segna come fatto, Posticipa.
- Serve la tua risposta, c’è un blocco o devi accedere: Rispondi, Apri o Accedi, poi Posticipa e Segna come fatto.
- Promemoria: Segna come fatto, Posticipa, Apri.
- Riepilogo del mattino: toccalo per aprirlo.

Nel browser e su Telegram sono disponibili due pulsanti. Per le domande di Fleet, le opzioni Rispondi e Rifiuta restano disponibili.

Una notifica non invia, paga o invia nulla per conto tuo. Una bozza si apre sempre prima, così puoi controllarla prima dell’invio. Apri la bozza mostra l’attività nell’elenco, con la bozza completa. Fallo avvia il lavoro solo per una nuova attività.

Nell’app per telefono, Posticipa e Segna come fatto richiedono prima di sbloccare il telefono. Nel browser si apre la dashboard, dove puoi eseguire l’azione e annullarla. Posticipa fa tornare l’attività tra due ore oppure, per un promemoria, il mattino seguente.

Le email hanno link Apri (e Posticipa per ciò che è in attesa). Aprono solo la dashboard.

Toccando una notifica, oppure Apri in un’email o su Telegram, l’attività viene mostrata nell’elenco, evidenziata e nella sua posizione attuale: **Appena fatto**, **Fatto**, **Torna più tardi** o un’altra vista. La chat non si apre mai. Se la pagina non è ancora aggiornata, segue l’attività non appena lo è.

## Il riepilogo del mattino

Arriva nei giorni lavorativi all’ora impostata per **Riepilogo del mattino**, a meno che non ci sia nulla da segnalare. Se l’orario è precedente a **I posticipi arrivano alle**, il riepilogo aspetta fino a 5 minuti dopo, così include le attività che tornano quella mattina. **Anteprima** lo mostra senza inviarlo. Per impostazione predefinita arriva come notifica push e come email, ed è abbastanza breve da leggere al volo:

- un saluto con ciò che conta oggi, ad esempio «Buongiorno Sam, ci sono 2 risposte pronte da inviare» oppure, se c’è una sola attività, «Buongiorno Sam, serve la tua conferma: invia il modulo d’ordine». Sono considerate pronte solo le attività con una bozza o un risultato da approvare. Non lo sono quelle che prima richiedono una tua risposta;
- le attività conteggiate nel saluto, ognuna con un link Apri, e le attività in scadenza oggi. Se non ce ne sono, al massimo tre cose da fare;
- fino a cinque attività che hai aggiunto tu e che aspettano una tua risposta, indipendentemente da quelle conteggiate nel saluto;
- quante altre attività possono aspettare e quanto tempo serve per gestirle al tuo ritmo, ad esempio «Altre 12 possono aspettare, circa 5 min per smaltirle». Il tempo non include le attività in attesa di una tua risposta. Un’attività in scadenza oggi ma posticipata a più tardi, o su cui la Machine sta ancora lavorando, non viene conteggiata finché non aspetta una tua risposta. Il numero corrisponde alle attività in attesa nel tuo elenco;
- una riga con le tue riunioni.

Apri mostra l’attività nell’elenco, evidenziata, anche se è stata completata o posticipata. Una promessa apre l’attività corrispondente oppure, se non è ancora associata a un’attività, la sua pagina.

La notifica push riporta lo stesso contenuto, senza link. Tocca la notifica o il link alla fine dell’email per rileggere il riepilogo in **Attività**.

## Il riepilogo della sera

Arriva una volta nei giorni lavorativi, all’orario impostato in **Orario di lavoro**. Per impostazione predefinita, arriva 15 minuti prima di **Fino alle**, tramite i canali scelti nella riga qui sopra. Arriva solo nei giorni in cui eri presente: hai usato la dashboard o hai scelto cosa fare per un’attività, nella dashboard, su Telegram, in chat o a voce. Se in un giorno non hai completato attività né partecipato a riunioni, non ricevi il riepilogo.

Si apre con il conteggio della giornata, ad esempio «Buonasera Sam, oggi hai completato 4 attività», poi mostra una sezione **Lavoro** e una **Personale**. Le sezioni vuote non vengono mostrate. Gli avvisi sulla tua Machine non rientrano in nessuna delle due. Ogni sezione include:

- **Fatto oggi**: fino a tre attività completate da te o dalla tua Machine, poi «+12 altre» e le riunioni della giornata, ad esempio «+3 riunioni: chiamata sui prezzi e altre 2»;
- **Aperto per domani** (o per il tuo prossimo giorno lavorativo, se è venerdì): le prime riunioni e le attività in scadenza.

In fondo trovi il numero di attività che richiedono ancora la tua attenzione. Tocca la notifica push o il link alla fine dell’email per rileggere il riepilogo, con **Copia Lavoro** e **Copia Personale**. Per non riceverlo, disattiva la relativa riga.

## Privacy

Le notifiche push passano direttamente dalla tua Machine al tuo dispositivo, criptate per quel dispositivo. Le email passano dal server di posta di The Machine e dal tuo provider di posta. Quando [Prudente](security-levels.md) nasconde il testo delle attività nelle notifiche, le email mostrano solo i conteggi. Disattiva **Email** per un tipo di notifica per escluderlo dalle email.

Attiva le notifiche push per un dispositivo da **Questo dispositivo** oppure consulta [Installare l’app](phone-app.md). L’[app mobile](mobile-app.md) invia una semplice notifica tramite Apple o Google, poi chiede alla tua Machine il titolo e il passaggio successivo.
