---
title: Ricontatti
area: graph
summary: Ricontatta in automatico chi non risponde, per un’intera bacheca o un singolo progetto. Ti chiede prima di inviare, a meno che tu non scelga diversamente.
covers: follow-ups
code: follow_ups.py, assistant.py, dashboard.html
order: 7
translated: 76bea8f586963be1
---
Quando una persona su una bacheca smette di rispondere, la tua Machine prepara una bozza di ricontatto al posto tuo, con il tuo tono e nella stessa conversazione. La funzione è disattivata finché non la attivi. Se una delle tue skill è adatta alla bacheca, le bozze la seguono, compreso l’ordine delle informazioni nell’email.

## Attivala

Tocca **⋯** su una bacheca, poi **Ricontatti…** e seleziona **Ricontatta se non c’è risposta**. La funzione si applica a tutti i progetti della bacheca. In alternativa, tocca **Ricontatti disattivati** sotto il nome della bacheca oppure **Ricontattali** in una fase con progetti senza risposta da almeno 10 giorni.

Per un singolo progetto, tocca **Ricontatti…** nel menu **⋯** della bacheca o nella pagina del progetto. **Per questo progetto** ti permette di scegliere **Attivo**, **Disattivata** o l’impostazione della bacheca. L’impostazione del progetto ha la precedenza su quella della bacheca.

## Impostazioni

- Per impostazione predefinita, aspetta da 3 a 7 giorni senza risposta. La bozza di ricontatto viene preparata dopo l’attesa più breve e inviata entro quella più lunga, anche quando il tuo utilizzo è al limite.
- **Solo nei giorni lavorativi**: nei giorni di riposo non vengono preparati né inviati ricontatti (in **Impostazioni** > **Notifiche** > **Orario di lavoro**). Quelli in scadenza vengono rimandati alla mattina del tuo prossimo giorno lavorativo. Attivo per Lavoro, disattivato per Personale.
- Per impostazione predefinita, invia da 1 a 3 ricontatti. Invia sempre il numero minimo e prepara le bozze per gli altri. Se pensa che sia meglio fermarsi, la bozza spiega il motivo ("The Machine si fermerebbe qui: 9 email senza risposta da agosto") e non è selezionata. Puoi inviarla, saltarla o scegliere **Ferma i ricontatti qui**. Non supera mai il numero massimo.
- **Fasi**: **Tutte le fasi aperte**, quindi non l’ultima fase della bacheca né Fermi o rifiutati. **Personalizza** permette di attivare o disattivare le fasi e di impostare un’attesa diversa per ciascuna.
- **Canali**: quelli collegati che possono inviare messaggi. Il ricontatto viene inviato sullo stesso canale dell’ultimo messaggio. **Cambia canale se non c’è risposta** prova il successivo tra quelli consentiti.
- **Sposta in Fermi o rifiutati dopo l’ultimo**: attivo se la bacheca ha quella fase.

## Chiedere prima o inviare in automatico

**Chiedimi prima di inviare** è l’impostazione predefinita: le bozze restano tra le tue attività. **Invia senza chiedere** dà il consenso permanente per quella bacheca o quel progetto. Le situazioni insolite o gli invii non riusciti restano comunque in attesa di una tua decisione, e il livello Prudente chiede sempre conferma. Un ricontatto non viene mai inviato due volte. I ricontatti non ti inviano notifiche push o email: le bozze restano nell’elenco e nel riepilogo del mattino.

Subito prima dell’invio, la conversazione viene controllata di nuovo. Se qualcuno ha scritto dopo la preparazione della bozza, questa non viene inviata: "Non inviato: nuovo messaggio nella conversazione". L’attività mostra il messaggio, chi l’ha scritto e quando, con le opzioni **Leggila** e **Rifai per questo messaggio**. Quest’ultima prepara una nuova bozza che tiene conto del messaggio.

## Controllare i ricontatti

I ricontatti di una bacheca vengono raccolti in un’unica attività, mai in una per ogni email. Mentre le bozze vengono preparate, compare "Scrittura di 3 ricontatti…", poi "8 ricontatti pronti per Alpha testers".

**Rivedi** li mostra uno sotto l’altro, per intero, così puoi scorrerli tutti. Per quello selezionato compaiono **Invia**, **Modifica** e **Salta**. Da tastiera, j e k (o le frecce) spostano la selezione, Invio invia, e modifica, s salta (premilo di nuovo per annullare), x seleziona o deseleziona e c applica modifiche. **Invia tutti i selezionati** invia quelli ancora selezionati.

Ogni ricontatto include la sua bozza. Se non è possibile scriverla, viene indicato cosa serve prima ("Nessuna bozza. Prima serve sapere a chi inviarla.") e non è selezionata. **Scrivi** chiede comunque di prepararla. Se una bozza ha più di un possibile destinatario, compare "Destinatario: scegli al momento dell’invio" e **Invia** ti chiede di sceglierne uno.

**Salta** deseleziona una bozza e la sposta in fondo, con l’etichetta Saltata e l’opzione **Annulla**. Viene saltata definitivamente quando chiudi la revisione. Puoi ripristinarla con **Ripristina** nei ricontatti del progetto o nella relativa attività in Fatto, se nel frattempo non è arrivato un ricontatto più recente. Il ricontatto di un singolo progetto è una normale attività.

**Chiedi modifiche…** riscrive tutte le bozze selezionate, oppure solo quella corrente, seguendo le tue indicazioni. Non viene inviato nulla e **Annulla modifica** ripristina il testo precedente. Finché il riquadro è aperto o la riscrittura è in corso non è possibile inviare nulla. Una bozza modificata viene mostrata di nuovo prima dell’invio.

Quando ne vengono inviati diversi di seguito, anche con Invia senza chiedere, ogni casella di posta ne invia uno ogni 30-45 secondi. L’attività mostra a che punto è l’invio: "Invio di 3 su 8…". **Interrompi l’invio** ferma gli altri. Quello già in invio viene comunque spedito; gli altri tornano nella revisione come bozze, da inviare in seguito ("Invio interrotto. 1 inviato, 11 salvati come bozze.").

## Email inviate prima che la tua Machine le legga

Vengono conteggiate anche le email che hai inviato da un’altra app prima che la tua Machine leggesse quella casella di posta. Legge la conversazione stessa oppure, se non può, le email precedenti citate nell’ultima che hai inviato. Quindi tre email senza risposta vengono conteggiate come tre e il periodo "Senza risposta da" parte dalla prima. Se hai già raggiunto il limite massimo, non prepara un altro ricontatto.

## Quando si interrompono

I ricontatti si interrompono quando arriva una risposta, quando il progetto viene vinto, perso, archiviato o spostato in una fase chiusa, e quando posticipi o salti un ricontatto. Prima di preparare una bozza, la tua Machine controlla se ci sono nuovi messaggi nella conversazione, così non sollecita qualcuno che ha già risposto altrove.

Anche un ricontatto viene chiuso quando qualcuno ha già risposto nella stessa conversazione. I ricontatti di un altro progetto non vengono considerati. Se la tua Machine pensa che non serva un ricontatto per un altro motivo, l’attività resta aperta e ne spiega il motivo: decidi tu.

**Metti in pausa** in **Ricontatti…** sospende una bacheca o un progetto senza disattivare i ricontatti: non vengono preparate né inviate bozze, nessun ciclo termina e le attività di ricontatto aperte restano aperte. Scegli un giorno in cui riprendere oppure tocca **Riprendi** quando vuoi. L’attesa riparte da dove si era fermata e i ricontatti in scadenza vengono inviati uno alla volta. Nel frattempo compare **In pausa**.

Dopo l’ultimo ricontatto senza risposta, il progetto mostra "Nessuna risposta dopo 3 ricontatti" e viene spostato in Fermi o rifiutati, se l’opzione è attiva. Se i ricontatti vengono interrotti prima di inviarne uno, compare "Ricontatti interrotti" e il progetto resta nella sua fase.

Se l’email non viene recapitata e la persona ha un altro indirizzo, il ricontatto viene inviato lì ("Indirizzo non valido, ora a <address>"). Se l’indirizzo di una bozza risulta non valido prima dell’invio, la bozza resta in sospeso: "Non inviato: indirizzo <address> non valido". Viene spostata sull’altro indirizzo e resta in attesa che tu la invii.

Se non c’è un altro indirizzo, i ricontatti passano a LinkedIn o WhatsApp quando è consentito e ci scrivi. Altrimenti si interrompono con "Email non recapitata". Se il progetto è importante, ricevi un’attività per trovare un nuovo indirizzo.

## Dove li trovi

L’intestazione della bacheca mostra "Ricontatti attivi, prossimo gio". Un progetto nella bacheca mostra il prossimo ricontatto oppure indica che è pronto. La pagina del progetto elenca quelli inviati, compresi quelli inviati in automatico.

I ricontatti restano in attesa quando la tua Machine è occupata o vicina al limite di utilizzo, poi recuperano quelli in sospeso. In una bacheca condivisa, solo la Machine del proprietario del progetto invia i ricontatti.
