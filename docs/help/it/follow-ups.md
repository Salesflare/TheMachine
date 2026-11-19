---
title: Ricontatti
area: graph
summary: Ricontatta automaticamente chi non risponde, per un’intera bacheca o un singolo progetto. Chiede conferma prima di inviare, a meno che tu non scelga diversamente.
covers: follow-ups
code: follow_ups.py, assistant.py, dashboard.html
order: 7
translated: 0e7bdfb2c9b2deb5
---
Quando una persona in una bacheca smette di rispondere, la tua Machine prepara una bozza di ricontatto per te, con il tuo stile e nella stessa conversazione. La funzione è disattivata finché non la attivi. Se una delle tue skill è adatta alla bacheca, le bozze la seguono, anche per quanto riguarda l’ordine dei contenuti nell’email.

## Attivarla

Tocca **⋯** su una bacheca, poi **Ricontatti…** e seleziona **Ricontatta se non c’è risposta**. La funzione si applica a tutti i progetti della bacheca. Puoi anche toccare **Ricontatti disattivati** sotto il nome della bacheca, oppure **Ricontattali** in una fase con progetti senza risposta da almeno 10 giorni.

Per un singolo progetto, tocca **Ricontatti…** nel menu **⋯** della bacheca o nella pagina del progetto. **Per questo progetto** ti permette di scegliere **Attivo**, **Disattivata** o l’impostazione della bacheca. L’impostazione del progetto prevale su quella della bacheca.

## Impostazioni

- Per impostazione predefinita, attendi da 3 a 7 giorni senza risposta. La bozza di ricontatto viene preparata dopo il tempo di attesa più breve e inviata entro quello più lungo, anche quando hai quasi esaurito il tuo utilizzo.
- **Solo nei giorni lavorativi**: nei giorni di riposo non vengono preparate né inviate bozze (in **Impostazioni** > **Notifiche** > **Orario di lavoro**). Le attività in scadenza in quei giorni aspettano la mattina del tuo prossimo giorno lavorativo. Attivo per Lavoro, disattivato per Personale.
- Per impostazione predefinita, invia da 1 a 3 ricontatti. Invia sempre il numero minimo e prepara le bozze per gli altri. Quando ritiene che sia meglio fermarsi, la bozza spiega il motivo ("La Machine si fermerebbe qui: 9 email senza risposta da agosto") e non è selezionata. Puoi inviarla, saltarla o scegliere **Ferma i ricontatti qui**. Non supererà mai il numero massimo.
- **Fasi**: **Tutte le fasi aperte**, quindi non l’ultima fase della bacheca né Fermi o rifiutati. **Personalizza** ti permette di attivare o disattivare le fasi e impostare un tempo di attesa specifico per ciascuna.
- **Canali**: quelli collegati che possono inviare messaggi. Il ricontatto viene inviato sullo stesso canale dell’ultimo messaggio. **Cambia canale se non c’è risposta** prova il successivo canale consentito.
- **Sposta in Fermi o rifiutati dopo l’ultimo**: attivo quando la bacheca include quella riga.

## Chiedere conferma o inviare automaticamente

**Chiedimi prima di inviare** è l’impostazione predefinita: le bozze restano tra le tue attività. **Invia senza chiedere** equivale a un’autorizzazione permanente per quella bacheca o quel progetto. Le situazioni insolite o gli invii non riusciti aspettano comunque una tua conferma, e il livello di cautela chiede sempre il tuo consenso. Un ricontatto non viene mai inviato due volte. I ricontatti non ti inviano notifiche, né push né email: le bozze restano nell’elenco e nel riepilogo del mattino.

Subito prima dell’invio, la conversazione viene controllata di nuovo. Se qualcuno ha scritto dopo la preparazione della bozza, il messaggio non viene inviato: "Non inviato: nuovo messaggio nella conversazione". L’attività mostra il messaggio, chi l’ha scritto e quando, con **Leggila** e **Rifai per questo messaggio**. Quest’ultima opzione chiede di preparare una nuova bozza che tenga conto del messaggio.

## Esaminarli

I ricontatti di una bacheca vengono raccolti in un’unica attività, non in una per ogni email. Mentre vengono preparati, compare "Scrittura di 3 ricontatti…", poi "8 ricontatti pronti per Alpha testers".

**Rivedi** li mostra uno sotto l’altro, per intero, così puoi scorrerli tutti. **Invia**, **Modifica** e **Salta** compaiono sul ricontatto selezionato. Da tastiera, j e k (o le frecce) passano da un ricontatto all’altro; Invio lo invia, e lo modifica, s lo salta (premi di nuovo per annullare), x lo seleziona o deseleziona e c lo modifica. **Invia tutti quelli selezionati** invia quelli che sono ancora selezionati.

Ogni ricontatto include la sua bozza. Se non è possibile prepararla, viene indicato cosa serve prima ("Nessuna bozza. Prima serve sapere a chi inviarla.") e non è selezionata. **Scrivi** chiede comunque di preparare la bozza. Se la bozza ha più destinatari possibili, compare "Destinatario: scegli al momento dell’invio" e **Invia** ti chiede di scegliere.

**Salta** deseleziona una bozza e la sposta in fondo, contrassegnandola come saltata con **Annulla**. Viene saltata definitivamente quando chiudi la revisione. Puoi ripristinare una bozza saltata con **Ripristina** nei ricontatti del progetto o nella sua attività in Fatto, se nel frattempo non è arrivato un ricontatto più recente. Il ricontatto di un singolo progetto è una normale attività.

**Chiedi modifiche…** riscrive tutte le bozze selezionate, o solo quella corrente, seguendo le tue istruzioni. Non viene inviato nulla e **Annulla modifica** ripristina il testo precedente. Finché la casella è aperta o la riscrittura è in corso, non è possibile inviare nulla. Una bozza modificata viene mostrata di nuovo prima dell’invio.

Quando vengono inviati più ricontatti di seguito, anche con Invia senza chiedere, ogni casella di posta ne invia uno ogni 30-45 secondi e l’attività mostra a che punto è: "Invio di 3 su 8…". **Interrompi l’invio** ferma i restanti. Quello già in fase di invio viene comunque inviato, mentre gli altri tornano nella revisione come bozze da inviare in seguito ("Invio interrotto. 1 inviato, 11 salvati come bozze.").

## Email inviate prima che la tua Machine le leggesse

Vengono conteggiate anche le email inviate da un’altra app prima che la tua Machine leggesse quella casella di posta. La Machine legge direttamente la conversazione oppure, se non può, le email precedenti citate nell’ultimo messaggio. Perciò tre email senza risposta vengono conteggiate come tre e il periodo "Senza risposta da" decorre dalla prima. Se hai già raggiunto il numero massimo, non viene preparata un’altra bozza.

## Quando si interrompono

I ricontatti si interrompono quando qualcuno risponde, quando il progetto viene vinto, perso, archiviato o spostato in una fase chiusa, oppure quando posticipi o salti un ricontatto. Prima di preparare una bozza, la tua Machine controlla se c’è qualcosa di nuovo nella conversazione, così non sollecita qualcuno che ha già risposto altrove.

**Metti in pausa** in **Ricontatti…** sospende una bacheca o un progetto senza disattivare i ricontatti: non vengono preparate né inviate bozze, il ciclo non termina e le attività di ricontatto aperte restano aperte. Scegli un giorno in cui riprendere, oppure tocca **Riprendi** quando vuoi. Il tempo di attesa riparte da dove si era interrotto e le attività in scadenza vengono gestite una alla volta. Nel frattempo, compare **In pausa**.

Dopo l’ultimo ricontatto senza risposta, il progetto mostra "Nessuna risposta dopo 3 ricontatti" e viene spostato in Fermi o rifiutati, se questa opzione è attiva. Se i ricontatti si interrompono prima che ne venga inviato uno, compare "Ricontatti interrotti" e il progetto resta nella sua fase.

Se l’email del destinatario non è stata recapitata e lui ha un altro indirizzo, il ricontatto viene inviato a quello ("Email non recapitata, ora a <address>"). Se l’indirizzo di una bozza risulta non valido prima dell’invio, la bozza viene messa in attesa: "Non inviato: indirizzo <address> non valido". Viene spostata sull’altro indirizzo e aspetta che tu la invii.

Se non c’è un altro indirizzo, i ricontatti passano a LinkedIn o WhatsApp, se consentito e se hai una conversazione lì. Altrimenti si interrompono con "Email non recapitata". Se il progetto è importante, ricevi un’attività per trovare un nuovo indirizzo.

## Dove li trovi

L’intestazione della bacheca mostra "Ricontatti attivi, prossimo gio". Un progetto nella bacheca mostra il prossimo ricontatto o indica che è pronto. Nella pagina del progetto trovi l’elenco dei ricontatti inviati, compresi quelli inviati automaticamente.

I ricontatti restano in attesa quando la tua Machine è occupata o vicina al limite di utilizzo, e riprendono più tardi. In una bacheca condivisa, solo la Machine del proprietario del progetto gestisce i ricontatti.
