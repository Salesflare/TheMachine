---
title: Notifiche
area: settings
summary: Cosa ti raggiunge, dove e quando: solo ciò che non può aspettare ti avvisa subito, il resto arriva in un unico riepilogo mattutino.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 334224e0b479ef47
---
Vuoi meno notifiche o notifiche diverse? In **Impostazioni**, **Notifiche**, scegli dove ricevere ogni tipo:

- **Nuove attività**: solo ciò che non può aspettare, per esempio qualcosa in scadenza oggi o urgente.
- **Risultati e domande**: una risposta pronta da inviare, un accesso richiesto per un compito o una domanda di Fleet.
- **Promemoria**: attività posticipate e risposte che stai aspettando, quando tornano.
- **Riepilogo del mattino**: un breve riepilogo della giornata. Vedi sotto.
- **Riepilogo della sera**: cosa hai fatto oggi e cosa è ancora da fare domani. Vedi sotto.

Ogni tipo ha un interruttore per **Push** (l'app sul telefono o sul computer), **Telegram** dopo averlo configurato ed **Email** su una Machine ospitata o su una Machine collegata a The Machine Network. Sono tutte attive, tranne i riepiloghi su Telegram.

Nella stessa scheda trovi anche il tuo **Orario di lavoro**: i giorni lavorativi, gli orari in cui possono arrivare le notifiche, quando tornano le attività posticipate, gli orari dei riepiloghi e il fuso orario. Vedi [Orario di lavoro](work-hours.md).

## Solo ciò che non può aspettare

Ricevi una notifica push, un avviso su Telegram o un'email solo per:

- un'attività in scadenza oggi o segnata come urgente;
- una risposta che qualcuno sta aspettando, preparata e pronta da inviare;
- un compito per cui devi accedere;
- un'attività posticipata che torna all'ora che hai scelto.

Tutto il resto compare senza avvisi nella dashboard (e senza notifiche su Telegram) e aspetta il riepilogo del mattino. Nei giorni liberi ricevi avvisi solo per ciò che è urgente o in scadenza oggi. Massimo 8 notifiche push al giorno. Se non apri la dashboard per 3 giorni, ricevi solo il riepilogo del mattino finché non torni.

## Quando arrivano le notifiche

La Machine controlla se stai davvero usando la dashboard, non solo se è aperta:

- Se la stai usando (è in primo piano e hai fatto clic, digitato o scorso la pagina negli ultimi 10 minuti), non ricevi avvisi. Su Telegram la notifica arriva senza suono.
- Se non ci sei (la dashboard è in background, chiusa o inattiva da 10 minuti), ricevi una notifica push un minuto dopo averla lasciata, a meno che tu non sia tornato e l'abbia vista.
- Se dopo 15 minuti non l'hai ancora vista e non può aspettare, ricevi un'email, al massimo una all'ora. Le attività di cui ti sei già occupato non vengono incluse. Quasi sempre, l'unica email che ricevi è il riepilogo del mattino.
- Se un compagno di squadra ti assegna un'attività e la tua Machine non ha un telefono né Telegram per raggiungerti, ricevi un'email con il titolo e un link, dopo 15 minuti se non l'hai ancora vista. Disattiva **Email** per **Risultati e domande** per non riceverla.
- Fuori dal tuo orario di lavoro non ricevi nulla. L'attività comparirà nel riepilogo del mattino.
- Una nuova attività di lavoro assegnata in un giorno libero aspetta l'orario del riepilogo del tuo prossimo giorno lavorativo. L'attività mostra quando ti verrà inviata una notifica, per esempio Notification Mon 2 Nov · 08:30.

Gli aggiornamenti sullo stato di avanzamento e le modifiche non generano notifiche. Se non hai ancora visto un'attività, un nuovo risultato la aggiorna senza inviare una nuova notifica. Se ne arrivano tante insieme, ricevi un solo avviso. L'icona dell'app mostra quante attività richiedono la tua attenzione.

## Pulsanti delle notifiche

Ogni notifica ha dei pulsanti per l'azione successiva. Nell'app per telefono:

- Nuova attività: **Fallo**, **Posticipa**, **Segna come fatto**.
- Bozza pronta: **Apri bozza**, **Posticipa**, **Segna come fatto**.
- Risultato pronto: **Apri**, **Segna come fatto**, **Posticipa**.
- Domanda, blocco o richiesta di accesso: **Rispondi**, **Apri** o **Accedi**, poi **Posticipa** e **Segna come fatto**.
- Promemoria: **Segna come fatto**, **Posticipa**, **Apri**.
- Riepilogo del mattino: toccalo per aprirlo.

Nel browser e su Telegram vengono mostrati due pulsanti. Per le domande di Fleet sono sempre disponibili **Rispondi** e **Rifiuta**.

Una notifica non invia, paga o invia nulla per tuo conto. Una bozza si apre sempre prima, così puoi vederla prima che venga inviata. **Apri bozza** mostra l'attività nell'elenco, con la bozza completa. **Fallo** avvia il lavoro solo per una nuova attività.

Nell'app per telefono, **Posticipa** e **Segna come fatto** ti chiedono prima di sbloccare il telefono. Nel browser aprono la dashboard, dove viene eseguita l'azione e puoi annullarla. **Posticipa** fa ricomparire l'attività dopo due ore o, se si tratta di un promemoria, il mattino seguente.

Le email hanno link **Apri** (e **Posticipa** per ciò che è in attesa). Aprono solo la dashboard.

Toccando una notifica o selezionando **Apri** in un'email o su Telegram, l'attività viene mostrata nell'elenco e messa in evidenza. Se è stata completata, posticipata o si trova in un'altra vista, si apre la chat corrispondente.

## Il riepilogo del mattino

Arriva nei giorni lavorativi all'orario impostato per **Riepilogo del mattino**, a meno che non ci sia nulla da segnalare. Se l'orario è precedente a **I posticipi arrivano alle**, aspetta fino a 5 minuti dopo, così include le attività che tornano quella mattina. **Anteprima** te lo mostra senza inviarlo. Per impostazione predefinita, arriva come notifica push e via email, ed è abbastanza breve da leggere a colpo d'occhio:

- un saluto con le informazioni importanti per oggi, per esempio "Buongiorno Sam, ci sono 2 risposte pronte da inviare" oppure, se c'è una sola attività, "Buongiorno Sam, serve il tuo OK: invia il modulo d'ordine";
- le attività incluse nel saluto, ciascuna con un link **Apri**, e quelle in scadenza oggi; altrimenti, fino a tre cose da fare;
- quante altre attività possono aspettare e quanto tempo ci vuole per completarle al tuo ritmo, per esempio "Altre 12 possono aspettare, ci vogliono circa 5 min per sbrigarsene." Le attività in attesa di una tua risposta non vengono conteggiate in questo tempo.
- le riunioni, in un'unica riga.

**Apri** mostra l'attività nell'elenco e la mette in evidenza. Se è stata completata, posticipata o si trova in un'altra vista, si apre la chat corrispondente. Una promessa apre la relativa attività o, se non ce n'è ancora una, la pagina della promessa.

La notifica push riporta le stesse informazioni, senza link. Toccala o seleziona il link in fondo all'email per rileggere il riepilogo in **Attività**.

## Il riepilogo della sera

Arriva una volta nei giorni lavorativi, all'orario impostato in **Orario di lavoro**. Per impostazione predefinita, arriva 15 minuti prima di **Fino alle**, nei canali scelti nella riga qui sopra. Se in una giornata non hai completato attività né partecipato a riunioni, non ricevi il riepilogo. Inizia con il totale della giornata, per esempio "Buonasera Sam, oggi hai completato 4 attività", poi include una sezione **Lavoro** e una **Personale**. Le sezioni vuote non vengono mostrate. Ognuna include:

- **Fatto oggi**: fino a tre attività completate da te o dalla tua Machine, poi "+12 altre" e le riunioni della giornata, per esempio "+3 riunioni: chiamata sui prezzi e altre 2";
- **Aperto per domani** (di venerdì, per il tuo prossimo giorno lavorativo): le prime riunioni e le attività in scadenza.

Il riepilogo termina con il numero di attività che richiedono ancora la tua attenzione. Tocca la notifica push o seleziona il link in fondo all'email per rileggerlo, con **Copia Lavoro** e **Copia Personale**. Per interromperlo, disattiva la relativa riga.

## Privacy

La notifica push viene inviata dalla tua Machine direttamente al tuo dispositivo e cifrata per quel dispositivo. L'email passa dal server di posta di The Machine e dal tuo provider di posta. Quando [Careful](security-levels.md) nasconde il testo delle attività nelle notifiche, le email riportano solo i totali. Disattiva **Email** per un tipo di notifica per escluderlo dalle email.

Attiva le notifiche push per un dispositivo in **Questo dispositivo** oppure consulta [Installa l'app](phone-app.md). L'[app per dispositivi mobili](mobile-app.md) riceve una riga semplice tramite Apple o Google, poi chiede alla tua Machine il titolo e il passo successivo.
