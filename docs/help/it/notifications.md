---
title: Notifiche
area: settings
summary: Cosa ricevi, dove e quando: solo ciò che non può aspettare ti avvisa subito, il resto arriva in un unico riepilogo del mattino.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 2146426abe3eaa50
---
Vuoi meno notifiche o notifiche diverse? In **Impostazioni**, **Notifiche**, scegli dove ricevere ogni tipo:

- **Nuove attività**: solo ciò che non può aspettare, per esempio un’attività in scadenza oggi o urgente.
- **Risultati e domande**: una risposta pronta da inviare, un accesso richiesto da un compito o una domanda di Fleet.
- **Promemoria**: le attività posticipate e le risposte che stai aspettando, quando tornano.
- **Riepilogo del mattino**: un breve riepilogo della giornata. Vedi sotto.
- **Riepilogo della sera**: cosa hai fatto oggi e cosa resta da fare domani. Vedi sotto.

Per ogni tipo puoi attivare o disattivare **Push** (l’app sul telefono o sul computer), **Telegram** quando è configurato e **Email** su una Machine ospitata o collegata a The Machine Network. Sono tutti attivi, tranne i riepiloghi su Telegram.

Nella stessa scheda trovi il tuo **Orario di lavoro**: i giorni lavorativi, gli orari in cui possono arrivare le notifiche, quando tornano le attività posticipate, gli orari dei riepiloghi e il fuso orario. Vedi [Orario di lavoro](work-hours.md).

## Solo ciò che non può aspettare

Ricevi una notifica push, un avviso su Telegram o un’email solo per:

- un’attività in scadenza oggi o contrassegnata come urgente;
- una risposta che qualcuno sta aspettando, preparata e pronta da inviare;
- un compito per cui devi accedere;
- un’attività posticipata che torna all’orario scelto.

Tutto il resto appare senza avvisi nella dashboard (e in silenzio su Telegram) e aspetta il riepilogo del mattino. Nei giorni liberi ricevi avvisi solo per ciò che è urgente o in scadenza oggi. Al massimo 8 notifiche push al giorno. Se non apri la dashboard per 3 giorni, ricevi solo il riepilogo del mattino finché non torni.

## Quando arrivano le notifiche

Il sistema controlla se stai usando davvero la dashboard, non solo se è aperta:

- Se la stai usando (è in primo piano e hai fatto clic, digitato o scorso la pagina negli ultimi 10 minuti): non ricevi avvisi. Su Telegram arriva una notifica silenziosa. Aprirla o ricaricarla, da solo, non conta.
- Se non ci sei (è in background, chiusa o inattiva da 10 minuti): ricevi una notifica push un minuto dopo averla lasciata, a meno che tu non sia tornato e l’abbia vista.
- Se dopo 15 minuti non l’hai ancora vista e non può aspettare: ricevi un’email, al massimo una all’ora. Le cose che hai già gestito sono escluse. Nella maggior parte dei giorni, l’unica email è il riepilogo del mattino.
- Se un collega ti assegna un’attività e la tua Machine non ha un telefono o Telegram per raggiungerti: ricevi un’email con il titolo e un link, dopo 15 minuti se non l’hai ancora vista. Disattiva **Email** per **Risultati e domande** per non ricevere questa email.
- Fuori dal tuo orario di lavoro non ricevi notifiche. L’attività compare nel riepilogo del mattino.
- Una nuova attività di lavoro in un giorno libero aspetta l’orario del riepilogo del tuo prossimo giorno lavorativo. Nell’attività vedi quando ti verrà inviata, per esempio: Notifica lun 2 nov · 08:30.

Gli aggiornamenti sui progressi e le modifiche non generano notifiche. Se arriva un nuovo risultato per un’attività che non hai ancora visto, l’attività si aggiorna senza una nuova notifica. Se arrivano più notifiche insieme, ne ricevi una sola. L’icona dell’app mostra quante attività richiedono la tua attenzione.

## Pulsanti delle notifiche

Ogni notifica ha dei pulsanti per il passaggio successivo. Nell’app per telefono:

- Nuova attività: **Fallo**, **Posticipa**, **Fatto**.
- Bozza pronta: **Apri bozza**, **Posticipa**, **Fatto**.
- Risultato pronto: **Apri**, **Fatto**, **Posticipa**.
- Domanda, blocco o richiesta di accesso: **Rispondi**, **Apri** o **Accedi**, poi **Posticipa** e **Fatto**.
- Promemoria: **Fatto**, **Posticipa**, **Apri**.
- Riepilogo del mattino: toccalo per aprirlo.

Il browser e Telegram ne mostrano due. Per le domande di Fleet sono sempre disponibili **Rispondi** e **Rifiuta**.

Da una notifica non viene inviato, pagato o inoltrato nulla. Una bozza si apre sempre prima, così puoi vederla prima che venga inviata. **Apri bozza** mostra l’attività nel tuo elenco con la bozza completa. **Fallo** avvia il lavoro solo per una nuova attività.

Nell’app per telefono, **Posticipa** e **Fatto** ti chiedono prima di sbloccare il dispositivo. Nel browser aprono la dashboard, dove puoi completare l’azione e annullarla. **Posticipa** fa tornare l’attività tra due ore, o il mattino dopo se si tratta di un promemoria.

Le email hanno link **Apri** (e **Posticipa** per ciò che è in attesa). Aprono solo la dashboard.

Toccando una notifica, oppure **Apri** in un’email o su Telegram, vedrai l’attività nel tuo elenco, evidenziata e nella sezione in cui si trova in quel momento: **Appena fatto**, **Fatto**, **Torna più tardi** o un’altra vista. La chat non si apre mai. Se la pagina non si è ancora aggiornata, seguirà l’attività appena lo farà.

## Il riepilogo del mattino

Arriva nei giorni lavorativi all’orario di **Riepilogo del mattino**, a meno che non ci sia nulla da segnalare. Se quell’orario è prima di **I posticipi arrivano alle**, aspetta fino a 5 minuti dopo, così include le attività che tornano quella mattina. **Anteprima** lo mostra senza inviarlo. Per impostazione predefinita arriva come notifica push e via email, ed è abbastanza breve da leggere al volo:

- un saluto con le informazioni importanti della giornata, per esempio «Buongiorno Sam, ci sono 2 risposte pronte da inviare» oppure, per una sola attività, «Buongiorno Sam, pronta per il tuo OK: invia il modulo d’ordine»;
- le attività conteggiate nel saluto, ciascuna con un link **Apri**, e ciò che è in scadenza oggi; altrimenti, al massimo tre cose da fare;
- fino a cinque attività che hai aggiunto tu e che aspettano una tua azione, indipendentemente da quelle conteggiate nel saluto;
- quante altre attività possono aspettare e quanto tempo ci vorrà al tuo ritmo, per esempio «Altre 12 possono aspettare, ci vorranno circa 5 min». Le attività in attesa di una tua risposta non rientrano in questo tempo. Un’attività in scadenza oggi ma posticipata a più tardi, o su cui The Machine sta ancora lavorando, non viene conteggiata finché non richiede una tua azione. Il totale corrisponde alle attività in attesa nel tuo elenco.
- le riunioni, tutte in una riga.

**Apri** mostra l’attività nel tuo elenco, evidenziata, anche se è completata o posticipata. Una promessa apre la relativa attività oppure, se non ne ha ancora una, la sua pagina.

La notifica push contiene lo stesso testo, senza link. Tocca la notifica o il link in fondo all’email per rileggere il riepilogo in **Attività**.

## Il riepilogo della sera

Arriva una volta nei giorni lavorativi all’orario indicato in **Orario di lavoro**. Per impostazione predefinita, arriva 15 minuti prima di **Fino alle**, nei canali che hai scelto nella relativa riga qui sopra. Se in una giornata non hai completato attività né partecipato a riunioni, non lo ricevi. Inizia con un conteggio della giornata, per esempio «Buonasera Sam, oggi hai completato 4 attività», poi mostra una sezione **Lavoro** e una **Personale**. Le sezioni vuote non vengono mostrate. Ognuna include:

- **Fatto oggi**: fino a tre attività completate da te o dalla tua Machine, poi «altre 12» e le riunioni del giorno, per esempio «altre 3 riunioni: chiamata sui prezzi e altre 2»;
- **Aperto per domani** (il prossimo giorno lavorativo, se è venerdì): le prime riunioni e le attività in scadenza.

Alla fine trovi il numero di attività che richiedono ancora la tua attenzione. Tocca la notifica push o il link in fondo all’email per rileggerlo, con **Copia Lavoro** e **Copia Personale**. Per non riceverlo più, disattiva la relativa riga.

## Privacy

Le notifiche push vanno direttamente dalla tua Machine al tuo dispositivo, in forma crittografata. Le email passano dal server di posta di The Machine e dal tuo provider email. Quando [Attenta](security-levels.md) nasconde il testo delle attività nelle notifiche, le email mostrano solo i conteggi. Disattiva **Email** per un tipo di notifica per escluderlo dalle email.

Attiva le notifiche push per un dispositivo in **Questo dispositivo** oppure scopri come [Installare l’app](phone-app.md). L’[app per dispositivi mobili](mobile-app.md) invia una riga di testo non formattata tramite Apple o Google, poi chiede alla tua Machine il titolo e il passaggio successivo.
