---
title: Ricontatti
area: graph
summary: Ricontatta da sola chi non risponde, per un’intera bacheca o un solo progetto. Chiede prima, a meno che tu non dica altro.
covers: follow-ups
code: follow_ups.py, assistant.py, dashboard.html
order: 4
---
Quando qualcuno su una bacheca smette di rispondere, la tua Machine scrive il ricontatto per te, con il tuo stile e nella stessa conversazione. Disattivati finché non li attivi. Se una delle tue skill è adatta alla bacheca, le bozze la seguono, anche in ciò che viene prima nell’email.

## Attivarli

**⋯** su una bacheca, poi **Ricontatti…**, e spunta **Ricontatta se non c’è risposta**. Vale per tutti i progetti di quella bacheca. Oppure tocca **Ricontatti disattivati** sotto il nome della bacheca, o **Ricontattali** in una fase con progetti senza risposta da oltre 10 giorni.

Per un solo progetto, **Ricontatti…** nel **⋯** della sua scheda o nella sua pagina. **Per questo progetto** sceglie **Attivo**, **Disattivata** o l’impostazione della bacheca. L’impostazione del progetto ha la precedenza su quella della bacheca.

## Impostazioni

- Aspetta da 3 a 7 giorni senza risposta. Dopo l’attesa più breve viene scritta una bozza. La più lunga è il limite entro cui parte, anche quando sei vicino al limite di utilizzo.
- Ricontatta almeno 1 e al massimo 3 volte. Il minimo parte sempre. Nel mezzo, scrive comunque ogni ricontatto. Se pensa che sia meglio fermarsi, la bozza dice perché (“The Machine si fermerebbe qui: 9 email senza risposta da agosto”) e non è spuntata: inviala, saltala o scegli **Ferma i ricontatti qui**. Se ne chiedi uno comunque nella chat di un ricontatto, lo scrive. Mai oltre il massimo.
- **Fasi**: **Tutte le fasi aperte**, quindi né l’ultima fase della bacheca né Fermi o rifiutati. **Personalizza** attiva o disattiva le fasi e dà a una fase la sua attesa.
- **Canali**: quelli collegati che possono inviare. Un ricontatto parte sullo stesso canale dell’ultimo messaggio. **Cambia canale se non c’è risposta** prova il successivo consentito.
- **Sposta in Fermi o rifiutati dopo l’ultimo**: attivo se la bacheca ha quella riga.

## Chiedere o inviare da sola

**Chiedimi prima di inviare** è l’impostazione predefinita: le bozze aspettano nelle tue attività. **Invia senza chiedere** è un sì permanente per quella bacheca o quel progetto. Ciò che è insolito aspetta comunque te, e così ciò che non va a buon fine. Con la modalità Prudente attiva, chiede sempre. Un ricontatto non parte mai due volte.

Subito prima dell’invio il thread viene ricontrollato, e se qualcuno ha scritto dopo la bozza non parte: «Non inviato: nuovo messaggio nel thread».

## Rivederli

I ricontatti di una bacheca arrivano come un’unica attività, mai una per email. Mentre li scrive mostra “Scrittura di 3 ricontatti…”, poi “8 ricontatti pronti per Alpha testers”.

**Rivedi** li mostra interi, uno sotto l’altro, così li leggi tutti scorrendo una volta. **Invia**, **Modifica** e **Salta** compaiono su quello attuale. Da tastiera, j e k (o le frecce) per spostarti, Invio invia, e modifica, s salta e c cambia. **Invia tutti i selezionati** invia quelli ancora spuntati.

**Salta** toglie la spunta a una bozza e la sposta in fondo, segnata come Saltata con **Annulla**; viene saltata davvero solo quando chiudi la revisione. Un ricontatto saltato torna con **Ripristina** nei ricontatti del progetto o sulla sua attività in Fatto, finché non ne arriva uno più recente. Il ricontatto di un singolo progetto è un’attività normale.

**Cambia…** riscrive tutte le bozze selezionate, o solo quella attuale, come dici tu; non viene inviato nulla e **Annulla modifica** riporta il testo di prima. Finché il riquadro Cambia è aperto o una riscrittura è in corso non parte nulla, e una bozza cambiata ti viene mostrata di nuovo prima di partire.

Quando ne partono diversi di seguito, anche con Invia senza chiedere, ogni casella ne invia uno ogni 30-45 secondi e l’attività mostra a che punto è: “Invio 3 di 8…”. **Interrompi l’invio** ferma il resto: quello già in uscita parte comunque, gli altri tornano come bozze nella revisione, da inviare più tardi (“Interrotto. Inviati: 1. 11 tenuti come bozze.”).

## Email inviate prima della tua Machine

Contano anche le email inviate da un’altra app, prima che la tua Machine leggesse quella casella. Legge la conversazione (o, se non può, le email precedenti citate nella tua ultima), quindi tre email senza risposta contano come tre, e “Nessuna risposta da” conta dalla prima. Se hai già raggiunto il massimo, non ne scrive un altro.

## Quando si fermano

I ricontatti si fermano quando la persona risponde, quando il progetto è vinto, perso, archiviato o spostato in una fase chiusa, e quando ne posticipi o salti uno. Prima di scrivere, la tua Machine controlla se nella conversazione c’è qualcosa di più recente, così non insiste con chi ha già risposto altrove.

**Metti in pausa** in **Ricontatti…** ferma una bacheca o un progetto senza disattivare i ricontatti: niente viene scritto o inviato, nessun giro finisce e le attività aperte restano aperte. Scegli un giorno per riprendere, o tocca **Riprendi** quando vuoi. L’attesa riparte da dove era, e ciò che era dovuto arriva uno alla volta. Nel frattempo si vede **In pausa**.

Dopo l’ultimo ricontatto senza risposta, il progetto mostra “Nessuna risposta dopo 3 ricontatti” e passa a Fermi o rifiutati, se è attivo. Se si fermano prima che ne parta uno, mostra “Ricontatti fermati” e resta nella sua fase.

Se la sua email è stata respinta e c'è un altro indirizzo, il ricontatto va lì ("Respinto, ora a <indirizzo>"). Una bozza il cui indirizzo viene respinto prima dell'invio resta ferma: "Non inviato: <indirizzo> è stato respinto", e passa all'altro indirizzo, dove aspetta il tuo invio.

Senza un altro indirizzo, i ricontatti passano a LinkedIn o WhatsApp quando è permesso e vi scrivete lì. Altrimenti si fermano con "Email non recapitata". Quando il progetto conta, ricevi un to-do per trovare un nuovo indirizzo.

## Dove lo vedi

L’intestazione della bacheca dice “Ricontatti attivi, il prossimo Gio”. La scheda di un progetto mostra il prossimo ricontatto, o che ce n’è uno pronto. La pagina del progetto elenca cosa è partito, anche ciò che è stato inviato in automatico.

I ricontatti aspettano mentre la tua Machine è impegnata con le tue attività o vicina al limite di utilizzo, e poi recuperano. Su una bacheca condivisa ricontatta solo la Machine del proprietario del progetto.
