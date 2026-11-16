---
title: Notifiche
area: settings
summary: Cosa ricevi, dove e quando: solo ciò che non può aspettare ti avvisa subito. Il resto arriva in un unico riepilogo del mattino.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: ee3ba81a8441704f
---
Meno notifiche o notifiche diverse? In **Impostazioni**, **Notifiche**, scegli dove ricevere ogni tipo di notifica:

- **Nuove attività**: solo ciò che non può aspettare, come qualcosa in scadenza oggi o urgente.
- **Risultati e domande**: una risposta pronta da inviare, un’attività che richiede l’accesso o una domanda di Fleet.
- **Promemoria**: le attività posticipate e le risposte che stai aspettando, quando tornano.
- **Riepilogo del mattino**: un breve riepilogo della giornata. Vedi sotto.
- **Riepilogo della sera**: cosa hai fatto oggi e cosa è ancora da fare domani. Vedi sotto.

Per ogni tipo puoi attivare le notifiche **Push** (sull’app del telefono o del computer), su **Telegram** una volta configurato e via **Email** su una Machine ospitata o su una Machine nella The Machine Network. Sono tutte attive, tranne i riepiloghi su Telegram.

Nella stessa scheda trovi anche il tuo **Orario di lavoro**: i giorni lavorativi, gli orari in cui possono arrivare le notifiche, quando tornano le attività posticipate, gli orari dei riepiloghi e il fuso orario. Vedi [Orario di lavoro](work-hours.md).

## Solo ciò che non può aspettare

Ricevi una notifica push, un avviso su Telegram o un’email solo per:

- un’attività in scadenza oggi o contrassegnata come urgente;
- una risposta che qualcuno sta aspettando, preparata e pronta da inviare;
- un compito che richiede il tuo accesso;
- un’attività posticipata che torna all’ora scelta.

Tutto il resto arriva senza avvisi sulla dashboard (e in silenzio su Telegram) e aspetta il riepilogo del mattino. Nei giorni liberi, ricevi avvisi solo per ciò che è urgente o in scadenza oggi. Al massimo 8 notifiche push al giorno. Se non apri la dashboard per 3 giorni, ricevi solo il riepilogo del mattino, finché non torni.

## Quando arrivano le notifiche

Controlla se stai davvero usando la dashboard, non solo se è aperta:

- Se la stai usando (è in primo piano e hai cliccato, scritto o scorso la pagina negli ultimi 10 minuti), non ricevi avvisi. Su Telegram arrivano in silenzio.
- Se non ci sei (è in secondo piano, chiusa o inattiva da 10 minuti), la notifica push arriva un minuto dopo che te ne sei andato, a meno che tu non sia tornato e l’abbia vista.
- Se dopo 15 minuti non l’hai ancora vista e non può aspettare, ricevi un’email, al massimo una all’ora. Le cose che hai già gestito non vengono incluse. Nella maggior parte dei giorni, l’unica email è il riepilogo del mattino.
- Se un compagno di squadra ti assegna un’attività e la tua Machine non ha un telefono o Telegram per raggiungerti, ricevi un’email con il titolo e un link, dopo 15 minuti se non l’hai ancora vista. Disattiva **Email** per **Risultati e domande** per non riceverla.
- Fuori dal tuo orario di lavoro non ricevi notifiche. L’attività comparirà nel riepilogo del mattino.
- Una nuova attività di lavoro in un giorno libero aspetta l’orario del riepilogo del tuo prossimo giorno lavorativo. L’attività indica quando ti verrà inviata, per esempio Notifica lun 2 nov · 08:30.

Gli aggiornamenti sullo stato e le modifiche non generano notifiche. Se arriva un nuovo risultato per un’attività che non hai ancora visto, l’attività si aggiorna senza inviare una nuova notifica. Un gruppo di notifiche ravvicinate genera un solo avviso. L’icona dell’app mostra quante attività richiedono la tua attenzione.

## Pulsanti nelle notifiche

Ogni notifica ha pulsanti per l’azione successiva. Nell’app per telefono:

- Nuova attività: **Fallo**, **Posticipa**, **Segna come fatto**.
- Bozza pronta: **Apri bozza**, **Posticipa**, **Segna come fatto**.
- Risultato pronto: **Apri**, **Segna come fatto**, **Posticipa**.
- Domanda, attività bloccata o richiesta di accesso: **Rispondi**, **Apri** o **Accedi**, poi **Posticipa** e **Segna come fatto**.
- Promemoria: **Segna come fatto**, **Posticipa**, **Apri**.
- Riepilogo del mattino: toccalo per aprirlo.

Il browser e Telegram mostrano due di questi pulsanti. Per le domande di Fleet, puoi sempre scegliere **Rispondi** o **Rifiuta**.

Da una notifica non viene inviato, pagato o inoltrato nulla. Una bozza si apre sempre per prima, così puoi controllarla prima dell’invio. **Apri bozza** mostra l’attività nell’elenco con la bozza completa. **Fallo** avvia il lavoro solo per una nuova attività.

Nell’app per telefono, **Posticipa** e **Segna come fatto** ti chiedono prima di sbloccare il dispositivo. Nel browser aprono la dashboard, dove l’azione viene eseguita e puoi scegliere **Annulla**. **Posticipa** fa tornare l’attività tra due ore o, per un promemoria, il mattino dopo.

Le email contengono link **Apri** (e **Posticipa** per ciò che è in attesa). Aprono solo la dashboard.

Toccando una notifica, oppure **Apri** in un’email o su Telegram, vedrai l’attività evidenziata nell’elenco, ovunque si trovi ora: **Appena fatto**, **Fatto**, **Torna più tardi** o un’altra vista. La chat non si apre mai. Se la pagina non si è ancora aggiornata, seguirà l’attività non appena lo sarà.

## Il riepilogo del mattino

Arriva nei giorni lavorativi all’ora impostata per **Riepilogo del mattino**, a meno che non ci sia niente da segnalare. Se l’orario è precedente a **I posticipi arrivano alle**, aspetta fino a 5 minuti dopo, così include le attività che tornano quel mattino. **Anteprima** lo mostra senza inviarlo. Per impostazione predefinita arriva come notifica push e via email, ed è abbastanza breve da leggere al volo:

- un saluto con le informazioni importanti della giornata, per esempio «Buongiorno Sam, ci sono 2 risposte pronte da inviare» o, se c’è una sola attività, «Buongiorno Sam, serve la tua approvazione: invia il modulo d’ordine»;
- le attività conteggiate nel saluto, ognuna con un link **Apri**, e ciò che scade oggi; se non c’è niente in scadenza, al massimo tre attività;
- fino a cinque attività che hai aggiunto tu e che aspettano il tuo intervento, indipendentemente da quelle conteggiate nel saluto;
- quante altre attività possono aspettare e quanto tempo ti servirà per gestirle al tuo ritmo, per esempio «Altre 12 possono aspettare, circa 5 min per completarle». Le attività in attesa di una tua risposta non rientrano nel tempo stimato, e un’attività posticipata in scadenza oggi non viene conteggiata finché non torna;
- le riunioni, in una sola riga.

**Apri** mostra l’attività nell’elenco, evidenziata, anche se è già stata completata o posticipata. Una promessa apre la relativa attività o, se non ne ha ancora una, la sua pagina.

La notifica push contiene le stesse informazioni senza link. Toccala, oppure tocca il link in fondo all’email, per rileggere il riepilogo in **Attività**.

## Il riepilogo della sera

Arriva una volta nei giorni lavorativi, all’orario indicato in **Orario di lavoro**. Per impostazione predefinita, viene inviato 15 minuti prima di **Fino alle**, usando i canali scelti nella relativa riga qui sopra. Se durante la giornata non hai completato attività né partecipato a riunioni, non ricevi il riepilogo. Inizia con il conteggio della giornata, per esempio «Buonasera Sam, oggi hai completato 4 attività», poi include una sezione **Lavoro** e una **Personale**. Le sezioni vuote non vengono mostrate. Ognuna include:

- **Fatto oggi**: fino a tre attività completate da te o dalla tua Machine, poi «altre 12» e le riunioni della giornata, per esempio «3 riunioni: chiamata sui prezzi e altre 2»;
- **Aperto per domani** (il prossimo giorno lavorativo, se è venerdì): le prime riunioni e le attività in scadenza.

Termina indicando quante attività richiedono ancora la tua attenzione. Tocca la notifica push o il link in fondo all’email per rileggerlo, con **Copia Lavoro** e **Copia Personale**. Per non riceverlo più, disattiva la relativa riga.

## Privacy

Le notifiche push vengono inviate direttamente dalla tua Machine al dispositivo, con crittografia. Le email passano dal server di posta di The Machine e dal tuo provider email. Quando [Attento](security-levels.md) nasconde il testo delle attività nelle notifiche, le email mostrano solo i conteggi. Disattiva **Email** per un tipo di notifica per non riceverlo via email.

Attiva le notifiche push per un dispositivo in **Questo dispositivo** oppure consulta [Installa l’app](phone-app.md). L’[app mobile](mobile-app.md) riceve una semplice notifica tramite Apple o Google, poi chiede alla tua Machine il titolo e il passaggio successivo.
