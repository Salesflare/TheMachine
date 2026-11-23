---
title: Notifiche
area: settings
summary: Cosa ti raggiunge, dove e quando: ricevi un avviso solo per ciò che non può aspettare. Il resto arriva in un unico riepilogo mattutino.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: febea6f9eb2c331a
---
Vuoi meno notifiche o notifiche diverse? In **Impostazioni**, **Notifiche**, scegli dove ricevere ogni tipo:

- **Nuove attività**: solo quelle che non possono aspettare, per esempio quelle in scadenza oggi o urgenti.
- **Risultati e domande**: una risposta pronta da inviare, un accesso richiesto per un compito o una domanda su Fleet.
- **Promemoria**: attività posticipate e risposte che stai aspettando, quando tornano.
- **Riepilogo del mattino**: un breve riepilogo della giornata. Vedi sotto.
- **Riepilogo della sera**: cosa hai completato oggi e cosa resta aperto per domani. Vedi sotto.

Ogni tipo ha un interruttore per **Push** (l’app sul telefono o sul computer), **Telegram** dopo averlo configurato ed **Email** su una Machine ospitata o su una Machine connessa a The Machine Network. Sono tutti attivi, tranne i riepiloghi su Telegram.

Nella stessa scheda trovi l’**Orario di lavoro**: i giorni lavorativi, quando possono arrivare le notifiche, quando arrivano le attività posticipate, gli orari dei riepiloghi e il tuo fuso orario. Vedi [Orario di lavoro](work-hours.md).

## Solo ciò che non può aspettare

Ricevi una notifica push, un avviso su Telegram o un’email solo per:

- un’attività in scadenza oggi o segnata come urgente;
- una risposta che qualcuno sta aspettando, preparata e pronta da inviare;
- un compito che richiede il tuo accesso;
- un’attività posticipata che torna all’orario scelto.

Tutto il resto arriva senza avvisi sulla dashboard (e senza suoni su Telegram) e aspetta il riepilogo mattutino. Nei giorni di riposo ricevi un avviso solo per ciò che è urgente o in scadenza oggi. Al massimo 8 notifiche push al giorno. Se non apri la dashboard per 3 giorni, ricevi solo il riepilogo mattutino, fino al tuo ritorno.

## Quando ricevi le notifiche

Il sistema controlla se stai usando davvero la dashboard, non solo se è aperta:

- Se la stai usando (è in primo piano e hai fatto clic, digitato o scorso la pagina negli ultimi 10 minuti), non ricevi avvisi. Su Telegram arrivano senza suono. Aprire o ricaricare la dashboard, da solo, non conta.
- Se non ci sei (la dashboard è in background, chiusa o inattiva da 10 minuti), la notifica push arriva un minuto dopo che te ne sei andato, a meno che tu non sia tornato e l’abbia vista.
- Se dopo 15 minuti non l’hai ancora vista e non può aspettare, ricevi un’email, al massimo una all’ora. Le attività che hai già gestito non vengono incluse e ogni attività compare una sola volta, con lo stato aggiornato. Nella maggior parte dei giorni, l’unica email è il riepilogo mattutino.
- Se un compagno di squadra ti assegna un’attività e la tua Machine non ha un telefono o Telegram per contattarti, ricevi un’email con il titolo e un link, dopo 15 minuti se non l’hai ancora vista. Disattiva **Email** per **Risultati e domande** per disabilitarla.
- Fuori dal tuo orario di lavoro non ricevi notifiche. L’attività compare nel riepilogo mattutino.
- Una nuova attività di lavoro in un giorno di riposo aspetta l’orario del riepilogo del prossimo giorno lavorativo. L’attività indica quando ti raggiungerà, per esempio: Notifica lun 2 nov · 08:30.

Gli aggiornamenti sui progressi e le modifiche non generano notifiche. Se arriva un nuovo risultato per un’attività che non hai ancora visto, l’attività si aggiorna senza una nuova notifica. Se arrivano più notifiche insieme, ne ricevi una sola. L’icona dell’app mostra quante attività richiedono la tua attenzione.

## Pulsanti delle notifiche

Ogni notifica ha pulsanti per l’azione successiva. Nell’app per telefono:

- Nuova attività: Fallo, Posticipa, Segna come fatto.
- Bozza pronta: Apri bozza, Posticipa, Segna come fatto.
- Risultato pronto: Apri, Segna come fatto, Posticipa.
- Domanda, problema o richiesta di accesso: Rispondi, Apri o Accedi, poi Posticipa e Segna come fatto.
- Promemoria: Segna come fatto, Posticipa, Apri.
- Riepilogo del mattino: toccalo per aprirlo.

Il browser e Telegram ne mostrano due. Per le domande su Fleet trovi sempre le opzioni Rispondi e Rifiuta.

Da una notifica non viene inviato, pagato o inoltrato nulla. Una bozza si apre sempre prima, così puoi controllarla prima dell’invio. Apri bozza mostra l’attività nella tua lista con la bozza completa. Fallo avvia il lavoro solo per una nuova attività.

Nell’app per telefono, Posticipa e Segna come fatto ti chiedono prima di sbloccare il dispositivo. Nel browser si apre la dashboard, dove puoi completare l’azione e vedere Annulla. Posticipa fa tornare l’attività dopo due ore oppure, nel caso di un promemoria, il mattino successivo.

Le email hanno link Apri (e Posticipa per ciò che è in attesa). Aprono solo la dashboard.

Toccando una notifica, o scegliendo Apri da un’email o su Telegram, l’attività viene mostrata nella tua lista, evidenziata e nella sezione in cui si trova in quel momento: **Appena fatto**, **Fatto**, **Torna più tardi** o un’altra vista. La chat non si apre mai. Se la pagina non è ancora aggiornata, segue l’attività appena lo è.

## Il riepilogo del mattino

Arriva nei giorni lavorativi all’orario del **Riepilogo del mattino**, a meno che non ci sia nulla da segnalare. Se l’orario è precedente a **I posticipi arrivano alle**, aspetta fino a 5 minuti dopo, così include le attività che tornano quella mattina. **Anteprima** lo mostra senza inviarlo. Per impostazione predefinita arriva come notifica push e via email, in un formato breve da leggere al volo:

- un saluto con le informazioni importanti della giornata, per esempio «Buongiorno Sam, ci sono 2 risposte pronte da inviare» oppure, per una sola attività, «Buongiorno Sam, serve la tua approvazione: invia il modulo d’ordine». Sono considerate pronte solo le attività con una bozza o un risultato da approvare; quelle che prima richiedono una tua risposta non lo sono;
- le attività conteggiate nel saluto, ognuna con un link Apri, e quelle in scadenza oggi; altrimenti, al massimo tre cose da fare;
- fino a cinque attività che hai aggiunto tu e che aspettano un tuo intervento, indipendentemente da quelle conteggiate nel saluto;
- quante altre attività possono aspettare e quanto tempo richiedono al tuo ritmo, per esempio «Altre 12 possono aspettare, circa 5 min per smaltirle». Le attività che aspettano una tua risposta non rientrano nel calcolo del tempo. Un’attività in scadenza oggi ma posticipata a più tardi, o a cui la Machine sta ancora lavorando, non viene conteggiata finché non richiede il tuo intervento. Il numero corrisponde alle attività in attesa nella tua lista;
- i tuoi impegni in una riga.

Apri mostra l’attività nella tua lista, evidenziata, anche se è stata completata o posticipata. Una promessa apre la relativa attività, oppure la sua pagina se non ne ha ancora una.

La notifica push contiene le stesse informazioni, senza link. Toccala, oppure seleziona il link in fondo all’email, per rileggere il riepilogo in **Attività**.

## Il riepilogo della sera

Arriva una volta nei giorni lavorativi, all’orario impostato in **Orario di lavoro**. Per impostazione predefinita, arriva 15 minuti prima di **Fino alle**, nei canali scelti nella riga qui sopra. Lo ricevi solo nei giorni in cui eri presente: hai usato la dashboard o hai scelto cosa fare per un’attività lì, su Telegram, in chat o a voce. Se in una giornata non hai completato attività né partecipato a riunioni, non ricevi il riepilogo.

Inizia con un conteggio della giornata, per esempio «Buonasera Sam, oggi hai completato 4 attività», poi include una sezione **Lavoro** e una **Personale**. Le sezioni vuote non vengono mostrate. Ognuna contiene:

- **Fatto oggi**: fino a tre attività completate da te o dalla tua Machine, poi «+12 altre» e le riunioni della giornata, per esempio «+3 riunioni: chiamata sui prezzi e altre 2»;
- **Aperto per domani** (il prossimo giorno lavorativo se è venerdì): i primi impegni e le attività in scadenza.

Alla fine trovi il numero di attività che richiedono ancora il tuo intervento. Tocca la notifica push o il link in fondo all’email per rileggerla, con **Copia Lavoro** e **Copia Personale**. Per interromperla, disattiva la relativa riga.

## Privacy

La notifica push viene inviata direttamente dalla tua Machine al dispositivo, con crittografia. Le email passano dal server di posta di The Machine e dal tuo provider email. Quando [Modalità cauta](security-levels.md) nasconde il testo delle attività nelle notifiche, le email mostrano solo i conteggi. Disattiva **Email** per un tipo di notifica per escluderlo dalle email.

Attiva le notifiche push per un dispositivo in **Questo dispositivo** oppure consulta [Installa l’app](phone-app.md). L’[app per dispositivi mobili](mobile-app.md) invia una semplice notifica tramite Apple o Google, poi chiede alla tua Machine il titolo e l’azione successiva.
