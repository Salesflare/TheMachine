---
title: Notifiche
area: settings
summary: Cosa ricevi, dove e quando: solo le cose che non possono aspettare ti avvisano, il resto arriva in un unico riepilogo al mattino.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 4f777fac22dba7c0
---
Vuoi meno notifiche o notifiche diverse? In **Impostazioni**, **Notifiche**, scegli dove ricevere ogni tipo:

- **Nuove attività**: solo le cose che non possono aspettare, come un’attività in scadenza oggi o urgente.
- **Risultati e domande**: una risposta pronta da inviare, un accesso richiesto per un’attività o una domanda di Fleet.
- **Promemoria**: attività posticipate e risposte che stai aspettando, quando tornano.
- **Riepilogo del mattino**: un breve riepilogo della giornata. Vedi sotto.
- **Riepilogo della sera**: cosa hai fatto oggi e cosa è ancora da fare domani. Vedi sotto.

Per ogni tipo puoi attivare o disattivare **Push** (l’app sul telefono o sul computer), **Telegram** una volta configurato e **Email** su una Machine ospitata o su una della The Machine Network. Sono tutti attivi, tranne i riepiloghi su Telegram.

Nella stessa scheda trovi anche il tuo **Orario di lavoro**: i giorni lavorativi, gli orari in cui possono arrivare le notifiche, quando tornano le attività posticipate, gli orari dei riepiloghi e il tuo fuso orario. Vedi [Orario di lavoro](work-hours.md).

## Solo le cose che non possono aspettare

Una notifica push, un avviso su Telegram o un’email arrivano solo per:

- un’attività in scadenza oggi o contrassegnata come urgente;
- una risposta che qualcuno aspetta, preparata e pronta da inviare;
- un’attività per cui devi accedere;
- un’attività posticipata che torna all’ora scelta.

Tutto il resto compare senza avvisi nella dashboard (e senza suoni su Telegram) e aspetta il riepilogo del mattino. Nei giorni liberi ti avvisiamo solo per le cose urgenti o in scadenza oggi. Al massimo 8 notifiche push al giorno. Se non apri la dashboard per 3 giorni, ricevi solo il riepilogo del mattino, finché non torni.

## Quando arrivano le notifiche

Controlla se stai usando davvero la dashboard, non solo se è aperta:

- Se la stai usando (è in primo piano e hai fatto clic, digitato o scorso la pagina negli ultimi 10 minuti), non arriva nessun avviso. Su Telegram arriva senza suono. Aprire o ricaricare la pagina, da solo, non conta.
- Se non ci sei (la dashboard è in background, chiusa o inattiva da 10 minuti), la notifica push arriva un minuto dopo che te ne sei andato, a meno che tu non sia tornato e l’abbia vista.
- Se dopo 15 minuti non l’hai ancora vista e non può aspettare, ricevi un’email, al massimo una all’ora. Non ricevi email per le cose di cui ti sei già occupato. Nella maggior parte dei giorni, il riepilogo del mattino è l’unica email.
- Se un compagno di squadra ti assegna un’attività e la tua Machine non può raggiungerti né sul telefono né su Telegram, ricevi un’email con il titolo e un link, 15 minuti dopo, se non l’hai ancora vista. Disattiva **Email** per **Risultati e domande** per non riceverla.
- Fuori dal tuo orario di lavoro non arriva nulla. Le cose da fare compaiono nel riepilogo del mattino.
- Una nuova attività di lavoro assegnata in un giorno libero aspetta l’orario del riepilogo del tuo prossimo giorno lavorativo. L’attività mostra quando ti verrà inviata, per esempio Notifica lun 2 nov · 08:30.

Gli aggiornamenti sui progressi e le modifiche non generano notifiche. Se arriva un nuovo risultato per un’attività che non hai ancora visto, la notifica esistente si aggiorna senza crearne una nuova. Un gruppo di notifiche ravvicinate genera un solo avviso. L’icona dell’app mostra quante attività richiedono il tuo intervento.

## Pulsanti nelle notifiche

Ogni notifica ha pulsanti per il passaggio successivo. Nell’app per telefono:

- Nuova attività: **Fallo**, **Posticipa**, **Segna come fatto**.
- Bozza pronta: **Apri bozza**, **Posticipa**, **Segna come fatto**.
- Risultato pronto: **Apri**, **Segna come fatto**, **Posticipa**.
- Domanda, attività bloccata o richiesta di accesso: **Rispondi**, **Apri** o **Accedi**, poi **Posticipa** e **Segna come fatto**.
- Promemoria: **Segna come fatto**, **Posticipa**, **Apri**.
- Riepilogo del mattino: toccalo per aprirlo.

Nel browser e su Telegram compaiono due di questi pulsanti. Per le domande di Fleet restano disponibili **Rispondi** e **Rifiuta**.

Da una notifica non viene inviato, pagato o inviato nulla. Una bozza si apre sempre prima, così puoi controllarla prima che parta. **Apri bozza** mostra l’attività nell’elenco con la bozza completa. **Fallo** avvia il lavoro solo per una nuova attività.

Nell’app per telefono, **Posticipa** e **Segna come fatto** richiedono prima di sbloccare il dispositivo. Nel browser aprono la dashboard, dove l’azione viene eseguita e compare **Annulla**. Con **Posticipa**, l’attività torna dopo due ore oppure la mattina dopo, se è un promemoria.

Le email hanno link **Apri** (e **Posticipa** per le cose che stai aspettando). Aprono solo la dashboard.

Toccando una notifica, o scegliendo **Apri** in un’email o su Telegram, l’attività viene evidenziata nell’elenco, ovunque si trovi in quel momento: **Appena fatto**, **Fatto**, **Torna più tardi** o un’altra vista. La chat non si apre mai. Se la pagina non è ancora aggiornata, segue l’attività appena lo è.

## Il riepilogo del mattino

Arriva nei giorni lavorativi all’orario di **Riepilogo del mattino**, a meno che non ci sia nulla da segnalare. Se quell’orario è prima di **I posticipi arrivano alle**, aspetta fino a 5 minuti dopo, così include le attività che tornano quella mattina. **Anteprima** lo mostra senza inviarlo. Per impostazione predefinita arriva come notifica push e via email, ed è abbastanza breve da leggere a colpo d’occhio:

- un saluto con le cose importanti della giornata, come «Buongiorno Sam, ci sono 2 risposte pronte da inviare» oppure, per una sola attività, «Buongiorno Sam, pronta per la tua approvazione: invia il modulo d’ordine»;
- le attività conteggiate nel saluto, ognuna con un link **Apri**, e le cose in scadenza oggi; altrimenti, al massimo tre cose da fare;
- fino a cinque attività che hai aggiunto tu e che aspettano il tuo intervento, indipendentemente da quante ne conteggia il saluto;
- quante altre possono aspettare e quanto ci metterai al tuo ritmo, per esempio «Altre 12 possono aspettare, ci vorranno circa 5 min per completarle». Le attività in attesa di una tua risposta non rientrano in questo tempo e un’attività posticipata in scadenza oggi non viene conteggiata finché non torna;
- le riunioni, in una sola riga.

**Apri** mostra l’attività nell’elenco, evidenziata, anche se è completata o posticipata. Una promessa apre la relativa attività oppure, se non ne ha ancora una, la sua pagina.

La notifica push riporta le stesse informazioni, senza link. Toccala, oppure usa il link in fondo all’email, per rileggere il riepilogo in **Attività**.

## Il riepilogo della sera

Arriva una volta nei giorni lavorativi, all’orario indicato in **Orario di lavoro**. Per impostazione predefinita, arriva 15 minuti prima di **Fino alle**, nei modi scelti nella riga qui sopra. Se in una giornata non hai completato attività né partecipato a riunioni, non ricevi il riepilogo. Inizia con un conteggio della giornata, come «Buonasera Sam, oggi hai completato 4 attività», poi include una sezione **Lavoro** e una **Personale**. Le sezioni vuote non vengono mostrate. Ognuna contiene:

- **Fatto oggi**: fino a tre attività completate da te o dalla tua Machine, poi «+12 altre» e le riunioni della giornata, per esempio «+3 riunioni: chiamata sui prezzi e altre 2»;
- **Aperto per domani** (il prossimo giorno lavorativo, se è venerdì): le prime riunioni e le attività in scadenza.

Alla fine trovi il numero di attività che richiedono ancora il tuo intervento. Tocca la notifica push o il link in fondo all’email per rileggere il riepilogo, con **Copia Lavoro** e **Copia Personale**. Per disattivarlo, spegni la relativa riga.

## Privacy

Le notifiche push passano dalla tua Machine direttamente al dispositivo e sono criptate per quel dispositivo. Le email passano dal server di posta di The Machine e dal tuo provider di posta. Quando [Careful](security-levels.md) nasconde il testo delle attività nelle notifiche, le email mostrano solo i conteggi. Disattiva **Email** per un tipo di notifica per escluderlo dalle email.

Attiva le notifiche push per un dispositivo in **Questo dispositivo** oppure vedi [Installa l’app](phone-app.md). L’[app per dispositivi mobili](mobile-app.md) invia una riga di testo tramite Apple o Google, poi chiede alla tua Machine il titolo e il passaggio successivo.
