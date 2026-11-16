---
title: Calendario
area: calendar
summary: La settimana che ti aspetta in un unico posto: riunioni, attività in scadenza, attività posticipate e promesse.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 93fe9794660b0ab2
---
## Cosa mostra

I tuoi giorni da oggi in poi, con:

- le riunioni dei calendari che hai collegato,
- le attività in scadenza quel giorno e quelle posticipate nel giorno in cui tornano,
- i check-in sul lavoro che hai delegato,
- le promesse con una data,
- [viaggi ed eventi](calendar.md#trips-and-events) dalle email di prenotazione e dei biglietti.

Una riunione presente in due calendari viene mostrata una sola volta. Un calendario condiviso con te mostra gli eventi di chi l’ha condiviso in tono attenuato, con il suo nome; questi eventi non generano mai attività. Gli eventi che durano tutto il giorno o più giorni sono indicati come eventi di un’intera giornata in ciascun giorno interessato. In **Agenda**, un viaggio è il primo elemento di ciascuno dei suoi giorni; in **Settimana** e **Mese** appare come una fascia che li attraversa, per esempio «Viaggio a Lisbona».

Un piano fatto insieme è una sola promessa, contrassegnata da «Con» e dal nome dell’altra persona. Una promessa relativa a una riunione di quel giorno con la stessa persona compare nella riga della riunione.

**In ritardo** viene prima di tutto. Una riunione con un’attività ancora aperta mostra il relativo stato: **Preparazione pronta**, **In preparazione** o **Attività**. Un’attività che sembra completata, perché hai già risposto o perché la sua esecuzione ha rilevato che è stata completata, non viene mostrata come **Scadenza**.

## Agenda, settimana o mese

- **Agenda** elenca i singoli giorni. Scorri verso il basso per vedere i giorni successivi oppure verso l’alto, o tocca **Mostra giorni precedenti**, per vedere quelli precedenti. Torna indietro fino a una settimana prima di quando hai collegato il calendario e mostra in alto una riga che indica da quale giorno parte. Una volta caricata la [cronologia](history.md), torna indietro di circa un anno.
- **Settimana** mostra una griglia dal lunedì alla domenica. Sul telefono mostra tre giorni.
- **Mese** mostra tutto il mese. Sul computer mostra fino a tre elementi al giorno; sul telefono mostra dei punti e, toccandone uno, elenca gli elementi di quel giorno.

**Oggi**, ‹ e › in alto ti permettono di spostarti tra le settimane o i mesi. La visualizzazione scelta viene ricordata su quel dispositivo.

Nella griglia settimanale, gli eventi che si svolgono alla stessa ora sono affiancati e restano leggibili. Gli altri sono indicati con **+N**; toccandolo si apre quel giorno nell’agenda.

## Apri un elemento

Tocca una riga per aprire la chat dell’attività, la promessa, il viaggio o l’evento, oppure la riunione. Se non puoi modificare una riunione, per esempio perché è di qualcun altro o ha degli invitati, ne vedi i dettagli: quando, dove e chi partecipa. Le persone che Graph riconosce e le organizzazioni e i progetti a cui è collegata la riunione rimandano alle rispettive pagine. **Apri in Google Calendar** (o **Apri in Outlook**) sotto di loro apre la riunione nel relativo servizio. Aprirla non cambia nulla.

Una sala riunioni prenotata per una riunione appare sotto **Dove**, mai come persona o in Graph.

Il link di una riunione mostra il nome del servizio, per esempio Zoom, Google Meet o Teams, oppure **Videochiamata**. Apri la riunione per partecipare.

## Viaggi ed eventi

Quando ricevi un’email di prenotazione per un volo, un hotel, un treno, un autobus, un traghetto o un’auto a noleggio, la tua Machine la aggiunge a un viaggio. Le prenotazioni dello stesso itinerario vengono raggruppate in un unico viaggio: andata, hotel e ritorno. Il viaggio appare come una fascia che attraversa i suoi giorni. Aprilo per vedere, in ordine cronologico, il codice di prenotazione, il posto e il biglietto di ciascuna prenotazione.

I biglietti per un concerto, una partita, un festival o una conferenza creano un evento, uno per ciascun evento, con il luogo, il codice di prenotazione, il posto e il numero di biglietti. Un secondo ordine per lo stesso evento viene aggiunto allo stesso evento. Un evento prenotato tramite la tua casella di lavoro è Lavoro; altrimenti è Personale.

- Ogni riga indica da chi arriva la prenotazione, per esempio **Da Example Tickets**, e apre l’email.
- Se dall’email è stata creata un’attività, per esempio per pagare i biglietti, **Apri l’attività** la mostra.
- Se una prenotazione cambia, la sua riga viene aggiornata; se viene annullata, viene rimossa. Quando tutte le prenotazioni sono annullate, viene rimosso anche il viaggio o l’evento.

La tua Machine legge i dettagli riportati nelle email di conferma di compagnie aeree, hotel, siti di prenotazione e rivenditori di biglietti, senza usare l’AI. Un’email che non contiene questi dettagli non crea nulla. Le email di prenotazione dell’anno coperto dalla [cronologia](history.md) che la tua Machine conserva vengono lette in background una volta caricata la cronologia.

## Note e trascrizione della riunione

I dettagli di una riunione hanno due sezioni. **Note** è il riepilogo: decisioni e attività da svolgere. **Trascrizione** riporta parola per parola ciò che è stato detto. All’inizio è chiusa e mostra quanto dura; **Mostra** la apre.

Se non si caricano, la riunione riprova da sola per circa mezzo minuto. Dopodiché, tocca **Riprova**.

Per ciascuna sezione puoi usare **Aggiungi note** o **Aggiungi trascrizione**, **Carica file** per un file Markdown o di testo, **Modifica** e **Rimuovi** (tocca due volte). Il contenuto di una sezione resta lì. In una riunione che puoi modificare, **Note** sotto il modulo le apre.

Se hai collegato [Zoom](zoom.md) o [Google Meet](google-meet.md), le note della riunione compaiono in Note e la trascrizione in Trascrizione, con l’indicazione **Da Zoom** o **Da Google Meet**. Non sostituiscono mai ciò che hai aggiunto: se sono presenti entrambe le versioni, vengono mostrate entrambe.

Le note possono arrivare anche dall’evento della riunione nel calendario, se aggiunte dopo l’inizio, oppure via email da Zoom o Gemini. Dopo la riunione, The Machine crea attività a partire da queste note solo per i passaggi successivi chiaramente indicati. Se le stesse note arrivano in due modi, viene creata una sola attività, con la riunione come origine: «Origine: note da» la riunione.

Se una riunione ha una trascrizione ma non ha note, trovi **Genera note**. The Machine le crea a partire dalla trascrizione: un breve riepilogo, le decisioni e le attività con le persone incaricate, nella lingua della riunione.

Viene mostrato **Sto scrivendo le note…** e la scrittura continua anche se chiudi la riunione. Per una riunione lunga possono servire alcuni minuti, usando il tuo modello. Le note riportano **Scritto da The Machine** e non sostituiscono mai quelle che hai aggiunto.

Puoi chiedere anche a The Machine di aggiungerle. Per esempio, chiedi in un’attività: «aggiungi questa trascrizione alla riunione del consiglio di oggi». La trascrizione viene inserita in Trascrizione e il riepilogo in Note. Nel Calendario, una riunione che le contiene indica **Note** o **Trascrizione**.

The Machine legge entrambe le sezioni per trovare le attività da fare dopo la riunione. Sono Lavoro o Personali a seconda della riunione e vengono condivise con il tuo team solo se lo è anche la riunione.

La riunione si apre con questi dettagli ovunque la trovi: nella cronologia, nei risultati di una ricerca nei messaggi o come origine di un’attività. **Invito originale** in fondo mostra l’invito così come è arrivato.

## Aggiungi o modifica un evento

Da qui puoi modificare il tuo calendario Google. Outlook e gli altri calendari sono di sola visualizzazione. **Nuovo evento** ne aggiunge uno (sul telefono è nel menu **+** nella barra superiore): scegli il calendario, un titolo e l’orario. Tocca un evento senza invitati in quel calendario per modificarlo oppure **Elimina** per cancellarlo (tocca due volte).

**Dove** suggerisce luoghi mentre scrivi: prima quelli che hai già usato e le tue organizzazioni, poi gli indirizzi di [OpenStreetMap](https://www.openstreetmap.org), una mappa gratuita. Per cercare vengono inviate solo le parole che scrivi. Scegli un suggerimento o lascia il testo che hai inserito.

**Invita** aggiunge persone da Graph o qualsiasi indirizzo email. È disponibile solo nel tuo calendario. Le persone che riceveranno un invito sono elencate sopra il pulsante, che indica anche quante sono: **Aggiungi e invita 2**. Google invia gli inviti quando tocchi il pulsante, non prima. Se non ci sono invitati, nessuno riceve un invito o un aggiornamento.

Anche un’attività può proporti una modifica, per esempio aggiungere un ritiro. Mostra esattamente cosa cambierà: la modifica viene applicata solo se tocchi **Aggiungi**, **Salva** o **Elimina**.

Non hai ancora riunioni? Se non hai un calendario, **Collega il tuo calendario** apre Connessioni: collega [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) o [un altro calendario](other-calendars.md).

## Conflitti con il tuo altro calendario

Se una riunione di lavoro si sovrappone a un impegno nel tuo calendario personale, o viceversa, The Machine crea un’attività sulla più recente delle due. Può preparare una breve nota per spostarla o proporti di rifiutarla. Non viene inviato nulla finché non approvi.

Gli eventi di un’intera giornata, quelli con stato libero e quelli provvisori non vengono considerati; ogni conflitto viene segnalato una sola volta. Un’attività di Lavoro indica solo che c’è un conflitto, così il tuo team non vede mai l’evento personale. Solo tu puoi vedere con quale evento si sovrappone.

## Preparati alle riunioni

Prima di una riunione con persone esterne alla tua azienda, The Machine crea un’attività: **Preparati per** la riunione. È un breve briefing:

- **Chi:** chi sono, secondo Graph.
- **Ultimo contatto:** il tuo ultimo scambio con loro. Dopo la riunione, quel messaggio viene indicato come origine dell’attività.
- **Promesse aperte:** ciò che tu o loro dovete ancora fare.
- **Domande aperte:** ciò che è ancora senza risposta.
- **Decidi o porta:** cosa definire o portare con te.

L’attività arriva la mattina di un giorno lavorativo: il giorno stesso della riunione se si svolge nel pomeriggio, altrimenti il giorno lavorativo precedente. Usa solo ciò che è già sulla tua Machine. Serve solo per consultare le informazioni: tocca **Fatto** quando l’hai letta. Se una promessa o una domanda richiede un’azione, ha una sua attività.

Se la cronologia non contiene informazioni utili, non viene creata alcuna attività. Le riunioni ricorrenti, interne, personali o rifiutate non ne generano. Se una riunione viene spostata, la sua attività resta la stessa, ma cambia orario. Un’attività scartata non ricompare e quella di una riunione annullata si chiude da sola.

Nei dettagli della riunione trovi la relativa attività sotto **Attività**, a un tocco dalla sua chat.
