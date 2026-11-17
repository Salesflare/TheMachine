---
title: Calendario
area: calendar
summary: La settimana che ti aspetta, tutta in un unico posto: riunioni, attività in scadenza, attività posticipate e promesse.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: c1941aa6ca09b134
---
## Cosa mostra

I tuoi giorni a partire da oggi, con:

- le riunioni dei calendari che hai collegato,
- le attività in scadenza quel giorno e quelle posticipate, nel giorno in cui ricompaiono,
- i promemoria sulle attività che hai delegato,
- le promesse con una data,
- [viaggi ed eventi](calendar.md#trips-and-events) ricavati dalle email di prenotazioni e biglietti.

Una riunione presente in due calendari viene mostrata una sola volta. Gli eventi di un calendario condiviso con te sono attenuati e riportano il nome di chi lo ha condiviso; non generano mai un’attività. Gli eventi che durano tutto il giorno o più giorni vengono mostrati come eventi di un’intera giornata in ciascun giorno interessato. In **Agenda**, un viaggio è il primo elemento di ciascuno dei suoi giorni; in **Settimana** e **Mese** è una fascia che copre tutti i giorni, per esempio «Viaggio a Lisbona».

Un piano concordato insieme è una sola promessa, contrassegnata da «Con» e dal nome dell’altra persona. Se una promessa riguarda una riunione di quel giorno con la stessa persona, viene mostrata sulla riga della riunione.

**In ritardo** viene mostrato per primo. Una riunione con un’attività ancora aperta mostra il relativo stato: **Preparazione pronta**, **In preparazione** o **Attività**. Un’attività che risulta completata, perché hai già risposto o perché un’esecuzione ha rilevato che è stata completata, non viene mostrata come **Scadenza**.

## Agenda, settimana o mese

- **Agenda** mostra un elenco di ogni giorno. Scorri verso il basso per vedere i giorni successivi, oppure verso l’alto (o tocca **Mostra giorni precedenti**) per quelli precedenti. Torna indietro fino a una settimana prima di quando hai collegato il calendario e mostra una riga in alto che indica da quale giorno. Quando è disponibile la [cronologia](history.md), torna indietro di circa un anno.
- **Settimana** mostra una griglia, da lunedì a domenica. Sul telefono mostra tre giorni.
- **Mese** mostra tutto il mese. Sul computer mostra fino a tre elementi al giorno; sul telefono mostra dei puntini. Tocca un giorno per vedere l’elenco dei suoi elementi.

**Oggi**, ‹ e › in alto ti permettono di spostarti tra le settimane o i mesi. La visualizzazione scelta viene ricordata su quel dispositivo.

Nella griglia settimanale, gli eventi che si svolgono alla stessa ora sono affiancati e restano leggibili. Gli altri sono indicati con **+N**. Toccalo per aprire quel giorno nell’agenda.

## Aprire un elemento

Fai clic su una riga per aprire la chat dell’attività, la promessa, il viaggio o l’evento, oppure la riunione. Una riunione che non puoi modificare qui, per esempio perché appartiene a un’altra persona o ha degli invitati, mostra i dettagli: quando, dove e chi. Le persone che Graph conosce, le organizzazioni e i progetti a cui è associata la riunione sono link alle rispettive pagine. **Apri in Google Calendar** (o **Apri in Outlook**) sotto i dettagli apre la riunione nel relativo calendario. Aprire una riunione non modifica nulla.

Una sala prenotata per una riunione viene mostrata sotto «Dove», mai come persona o in Graph.

Un link alla riunione è indicato dal nome del servizio, per esempio Zoom, Google Meet o Teams, oppure da **Videochiamata**. Apri la riunione per partecipare.

## Viaggi ed eventi

Quando ricevi un’email con una prenotazione per un volo, un hotel, una casa vacanze, un treno, un autobus, un traghetto, un’auto a noleggio, un taxi o un parcheggio in aeroporto, la tua Machine la aggiunge a un viaggio. Le prenotazioni dello stesso itinerario vengono riunite in un solo viaggio, da qualsiasi casella email provengano: il treno per l’aeroporto, i voli, l’auto, il soggiorno e il viaggio di ritorno. Le prenotazioni vengono unite se i giorni si sovrappongono o se una inizia quando finisce l’altra.

Il viaggio appare come una fascia che copre tutti i suoi giorni. Aprilo per vedere ogni prenotazione in ordine cronologico, con orari, indirizzo, codice di prenotazione e posto.

I biglietti per un concerto, una partita, un festival o una conferenza creano un evento, uno per ogni occasione, con luogo, codice di prenotazione, posto e numero di biglietti. Un secondo ordine per lo stesso evento viene aggiunto a quello esistente. Un evento prenotato dalla tua casella di lavoro è contrassegnato come Work, altrimenti come Personal. I biglietti per un evento durante un viaggio vengono aggiunti al viaggio.

Per un viaggio futuro, la tua Machine indica cosa manca, per esempio **Nessun alloggio prenotato per 2 notti** oppure che non hai prenotato nulla per andare dall’aeroporto all’hotel. Queste righe sono attenuate e contrassegnate con **Nessuna prenotazione**. Se il viaggio non prevede pernottamenti, non viene mostrato alcun avviso sulle notti.

- Ogni riga indica da chi proviene la prenotazione, per esempio **Da Example Tickets**, e apre l’email.
- Se dall’email è stata creata un’attività, per esempio per pagare i biglietti, **Apri l’attività** la mostra.
- Se una prenotazione cambia, la relativa riga viene aggiornata; se viene annullata, la riga scompare. Quando tutte le prenotazioni vengono annullate, scompare anche il viaggio o l’evento.
- Una prenotazione per un’altra persona, per esempio il volo di un collega che ti è stato inoltrato, non viene aggiunta ai tuoi viaggi.

La maggior parte delle conferme contiene i dettagli in un formato che la tua Machine può leggere senza AI. Per quelle che non lo fanno, per esempio un’email inoltrata o proveniente da un piccolo sito di prenotazioni, il tuo [modello](model.md) legge l’email in background, poche alla volta, e aspetta se sei vicino al limite di utilizzo. Le email di prenotazione dell’anno incluso nella [cronologia](history.md) della tua Machine vengono lette in background quando la cronologia è disponibile.

## Note e trascrizione della riunione

I dettagli di una riunione sono divisi in due parti. **Note** contiene il riepilogo: decisioni e azioni da svolgere. **Trascrizione** riporta parola per parola ciò che è stato detto. All’inizio è chiusa e mostra la durata; tocca **Mostra** per aprirla.

Se non si caricano, la riunione riprova automaticamente per circa mezzo minuto. Poi tocca **Riprova**.

Per ciascuna sezione puoi usare **Aggiungi note** o **Aggiungi trascrizione**, **Carica file** per caricare un file Markdown o di testo, **Modifica** e **Rimuovi** (tocca due volte). Il contenuto di una sezione resta lì. In una riunione che puoi modificare, **Note** sotto il modulo le apre.

Se hai collegato [Zoom](zoom.md), [Google Meet](google-meet.md) o [Granola](granola.md), le relative note appaiono in Note e la trascrizione in Trascrizione, contrassegnate con **Da Zoom**, **Da Google Meet** o **Da Granola**. Non sostituiscono mai ciò che hai aggiunto tu: se sono presenti entrambe, vengono mostrate entrambe.

Le note possono anche essere aggiunte all’evento della riunione nel calendario dopo il suo inizio, oppure arrivare via email da Zoom o Gemini. Quando la riunione termina, The Machine crea attività a partire da queste note solo se contengono passi successivi chiari. Se le stesse note arrivano in due modi, viene creata una sola attività, con la riunione come fonte: «Fonte: note della» riunione.

Una riunione con una trascrizione ma senza note mostra **Genera note**. The Machine crea le note a partire dalla trascrizione: un breve riepilogo, le decisioni e le azioni da svolgere con i rispettivi responsabili, nella lingua della riunione.

Viene mostrato **Sto scrivendo le note…** e la generazione continua anche se chiudi la riunione. Per una riunione lunga possono servire alcuni minuti; viene usato il tuo modello. Le note riportano **Scritte da The Machine** e non sostituiscono mai quelle che hai aggiunto tu.

Puoi anche chiedere a The Machine di aggiungerle. Per esempio, chiedi in un’attività: «Aggiungi la trascrizione alla riunione della bacheca di oggi». La trascrizione viene aggiunta in Trascrizione, il riepilogo in Note. Nel Calendario, una riunione che le contiene mostra **Note** o **Trascrizione**.

The Machine legge entrambe per individuare le attività successive alla riunione. Sono contrassegnate come Work o Personal, come la riunione, e vengono condivise con il tuo team solo se lo è anche la riunione.

I dettagli della riunione sono disponibili ovunque la trovi: nella cronologia, nei risultati di ricerca dei messaggi o come fonte di un’attività. **Invito originale** in fondo mostra l’invito così come è arrivato.

## Aggiungere o modificare un evento

Da qui puoi modificare il tuo calendario Google. Outlook e gli altri calendari sono di sola lettura. **Nuovo evento** ne aggiunge uno (sul telefono si trova sotto **+** nella barra superiore): scegli il calendario, un titolo e l’orario. Fai clic su un evento senza invitati in quel calendario per modificarlo o **Elimina** per cancellarlo (tocca due volte).

**Dove** suggerisce luoghi mentre scrivi: prima quelli che hai già usato e le tue organizzazioni, poi gli indirizzi di [OpenStreetMap](https://www.openstreetmap.org), una mappa gratuita. Per cercare vengono inviate solo le parole che digiti. Scegli un suggerimento oppure lascia il testo che hai inserito.

**Invita** aggiunge persone da Graph o qualsiasi indirizzo email. Questa opzione è disponibile solo nel tuo calendario. Le persone che riceveranno un invito sono elencate sopra il pulsante, che indica anche quante sono: **Aggiungi e invita 2**. Google invia gli inviti quando tocchi il pulsante, non prima. Se non ci sono invitati, nessuno riceve un invito o un aggiornamento.

Un’attività può anche proporti una modifica, per esempio aggiungere un ritiro. Mostra esattamente cosa cambierà; la modifica viene applicata solo se tocchi **Aggiungi**, **Salva** o **Elimina**.

Non hai ancora riunioni? Se non hai collegato un calendario, **Collega il tuo calendario** apre Connessioni. Collega [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) o [un altro calendario](other-calendars.md).

## Conflitti con l’altro calendario

Quando una riunione di lavoro si sovrappone a un impegno nel tuo calendario personale, o viceversa, The Machine crea un’attività sulla più recente delle due. Può preparare una breve nota per spostarla oppure proporti di rifiutarla. Non viene inviato nulla finché non approvi.

Gli eventi che durano tutto il giorno, quelli segnati come libero e quelli provvisori non vengono considerati. Ogni conflitto viene segnalato una sola volta. Un’attività Work indica solo che c’è un conflitto, così il tuo team non vede mai l’evento personale. Solo tu puoi vedere con quale evento è in conflitto.

## Preparati alle riunioni

Prima di una riunione con persone esterne alla tua azienda, The Machine crea un’attività: **Preparati per** la riunione. È un breve briefing:

- **Chi:** chi sono, in base a Graph.
- **Ultimo contatto:** l’ultimo scambio di messaggi con loro. Dopo la riunione, quel messaggio diventa la fonte dell’attività.
- **Promesse aperte:** cosa dovete ancora fare tu o loro.
- **Domande aperte:** quali domande sono ancora senza risposta.
- **Decidere o portare:** cosa decidere o portare con te.

L’attività arriva la mattina di un giorno lavorativo: il giorno stesso se la riunione è nel pomeriggio, altrimenti il giorno lavorativo precedente. Usa solo le informazioni già presenti nella tua Machine. Serve solo per consultarla: tocca **Fatto** dopo averla letta. Se contiene una promessa o una domanda che richiede un’azione, viene creata un’attività apposita.

Se non ci sono informazioni utili nella cronologia, non viene creata alcuna attività. Le riunioni ricorrenti, interne, personali o rifiutate non ne generano. Se una riunione viene spostata, la sua attività resta la stessa e viene aggiornata al nuovo orario. Un’attività scartata non ricompare; quella di una riunione annullata si chiude automaticamente.

I dettagli della riunione mostrano la relativa attività sotto **Attività**. Tocca per aprire la chat.
