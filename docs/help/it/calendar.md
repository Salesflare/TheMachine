---
title: Calendario
area: calendar
summary: La settimana che ti aspetta, in un unico posto: riunioni, attività in scadenza, attività posticipate e promesse.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: f3f41306aad03084
---
## Cosa mostra

I tuoi giorni a partire da oggi, con:

- le riunioni dei calendari che hai collegato,
- le attività in scadenza quel giorno e quelle posticipate, nel giorno in cui tornano,
- i check-in sul lavoro che hai passato ad altri,
- le promesse con una data,
- [viaggi ed eventi](calendar.md#trips-and-events) dalle email di prenotazioni e biglietti.

Una riunione presente in due calendari appare una sola volta. Gli eventi di un calendario condiviso con te appaiono attenuati, con il nome di chi l’ha condiviso. Non creano mai un’attività. Gli eventi di tutto il giorno e quelli che durano più giorni appaiono come eventi di tutto il giorno, in ciascun giorno interessato. In Agenda, un viaggio compare per primo in ognuno dei suoi giorni; in Settimana e Mese, appare come una sola fascia su tutti i giorni, per esempio «Viaggio a Lisbona».

Un piano concordato insieme è una sola promessa, contrassegnata da «Con» e dal nome dell’altra persona. Se una promessa riguarda una riunione di quel giorno con la stessa persona, appare sulla riga della riunione.

**In ritardo** appare per primo. Una riunione con un’attività ancora aperta mostra il relativo stato: **Preparazione pronta**, **In preparazione** o **Attività**. Un’attività che sembra completata, perché hai già risposto o perché la sua esecuzione l’ha segnata come completata, non appare come **Scadenza**.

## Agenda, settimana o mese

- **Agenda** mostra un giorno alla volta. Scorri verso il basso per i giorni successivi o verso l’alto, oppure tocca **Mostra giorni precedenti**, per quelli precedenti. Torna indietro fino a una settimana prima di quando hai collegato il calendario e, in cima, indica da quale giorno parte. Quando è disponibile la [cronologia](history.md), arriva a circa un anno prima.
- **Settimana** mostra una griglia da lunedì a domenica. Sul telefono mostra tre giorni.
- **Mese** mostra tutto il mese. Sul computer mostra fino a tre elementi al giorno; sul telefono mostra dei punti. Toccane uno per vedere l’elenco di quel giorno.

**Oggi**, ‹ e › in alto ti permettono di spostarti tra le settimane o i mesi. La vista scelta viene salvata su quel dispositivo.

Nella griglia settimanale, gli eventi alla stessa ora appaiono affiancati, senza perdere leggibilità. Gli altri sono indicati con **+N**: toccalo per aprire quel giorno nell’agenda.

## Apri un elemento

Seleziona una riga per aprire la chat dell’attività, la promessa, il viaggio o l’evento, oppure la riunione. Per una riunione che non puoi modificare qui, per esempio perché appartiene a un’altra persona o ha ospiti, puoi vedere i dettagli: quando e dove si svolge e chi partecipa. Le persone che il tuo Graph conosce e le organizzazioni e i progetti associati alla riunione rimandano alle rispettive pagine. **Apri in Google Calendar** o **Apri in Outlook**, sotto, la apre nel relativo calendario. La visualizzazione non modifica nulla.

Se una sala riunioni è prenotata per una riunione, appare sotto «Dove», mai come persona o nel tuo Graph.

Il link a una riunione mostra il nome del servizio, per esempio Zoom, Google Meet o Teams, oppure **Videochiamata**. Apri la riunione per partecipare.

## Viaggi ed eventi

Quando ricevi un’email di prenotazione di un volo, un hotel, una casa vacanze, un treno, un autobus, un traghetto, un’auto a noleggio, un taxi o un parcheggio in aeroporto, la tua Machine la aggiunge a un viaggio. Le prenotazioni dello stesso itinerario, anche se arrivano da caselle email diverse, finiscono in un unico viaggio: il treno per l’aeroporto, i voli, l’auto, il soggiorno e il ritorno. Le prenotazioni vengono raggruppate quando le loro date si sovrappongono o quando una inizia dove finisce l’altra.

Il viaggio appare come una fascia unica su tutti i suoi giorni. Aprilo per vedere le prenotazioni in ordine cronologico, con orari, indirizzo, codice di prenotazione e posto.

I biglietti per un concerto, una partita, un festival o una conferenza creano un evento, uno per ciascun evento, con il luogo, il codice di prenotazione, il posto e il numero di biglietti. Un secondo ordine per lo stesso evento viene aggiunto a quello esistente. Un biglietto prenotato tramite la tua casella di lavoro è di Lavoro, altrimenti è Personale. I biglietti per eventi che si svolgono durante un viaggio vengono aggiunti al viaggio.

Per un viaggio ancora da fare, la tua Machine indica cosa manca, per esempio **Nessun alloggio prenotato per 2 notti** oppure che non hai prenotato il trasferimento dall’aeroporto all’hotel. Queste righe sono attenuate e contrassegnate con **Nessuna prenotazione**. Se il viaggio non prevede pernottamenti, non mostra informazioni sulle notti.

- Ogni riga indica da chi proviene la prenotazione, per esempio **Da Example Tickets**, e apre l’email corrispondente.
- Se dall’email è stata creata un’attività, per esempio per pagare i biglietti, **Apri l’attività** la mostra.
- Se una prenotazione viene modificata, la relativa riga si aggiorna; se viene annullata, scompare. Quando tutte le prenotazioni sono annullate, scompare anche il viaggio o l’evento.
- Una prenotazione per un’altra persona, per esempio il volo di un collega inoltrato a te, non viene aggiunta ai tuoi viaggi.

La maggior parte delle conferme contiene i dettagli in un formato che la tua Machine legge senza IA. Se non è così, per esempio per un’email inoltrata o un piccolo sito di prenotazioni, il tuo [modello](model.md) legge l’email in background, poche alla volta, e si mette in attesa quando ti avvicini al limite di utilizzo. Dopo che la cronologia è disponibile, la tua Machine legge in background le email di prenotazione dell’anno coperto dalla [cronologia](history.md).

## Note e trascrizione della riunione

I dettagli di una riunione hanno due sezioni. **Note** è il riepilogo, con decisioni e attività da svolgere. **Trascrizione** riporta parola per parola ciò che è stato detto. All’inizio è chiusa e ne viene mostrata la durata; tocca **Mostra** per aprirla.

Se non si caricano, la riunione riprova automaticamente per circa mezzo minuto. Dopo, tocca **Riprova**.

Per ciascuna sezione puoi usare **Aggiungi note** o **Aggiungi trascrizione**, **Carica file** per caricare un file Markdown o di testo, **Modifica** e **Rimuovi** (tocca due volte). Il contenuto di una sezione resta lì. Per una riunione che puoi modificare, apri **Note** sotto il modulo.

Se hai collegato [Zoom](zoom.md), [Google Meet](google-meet.md) o [Granola](granola.md), le note del servizio appaiono in Note e la trascrizione in Trascrizione, con l’etichetta **Da Zoom**, **Da Google Meet** o **Da Granola**. Non sostituiscono mai quello che hai aggiunto tu: se sono presenti entrambi, li vedi entrambi.

Le note possono arrivare anche dall’evento della riunione nel calendario, se aggiunte dopo l’inizio, oppure via email da Zoom o Gemini. Al termine della riunione, The Machine crea attività solo per i prossimi passi chiaramente indicati. Se le stesse note arrivano in due modi, viene creata una sola attività, con la riunione come origine: «Origine: note da» seguito dalla riunione.

Una riunione con una trascrizione ma senza note mostra **Genera note**. The Machine crea le note a partire dalla trascrizione: un breve riepilogo, le decisioni e le attività da svolgere con i relativi responsabili, nella lingua della riunione.

Appare **Sto scrivendo le note…** e la creazione continua anche se chiudi la riunione. Per una riunione lunga possono servire alcuni minuti e viene usato il tuo modello. Le note riportano **Scritte da The Machine** e non sostituiscono mai quelle che hai aggiunto tu.

Anche The Machine può aggiungere le note. Chiediglielo in un’attività, per esempio: «aggiungi questa trascrizione alla riunione del consiglio di oggi». La trascrizione viene inserita in Trascrizione e il riepilogo in Note. Nel Calendario, le riunioni con note o trascrizione mostrano **Note** o **Trascrizione**.

The Machine legge entrambe le sezioni per trovare i prossimi passi della riunione. Sono di Lavoro o Personali come la riunione e vengono condivisi con il team solo se lo è anche la riunione.

La riunione si apre con questi dettagli ovunque la trovi: nella cronologia, nei risultati di una ricerca nei messaggi o come origine di un’attività. **Invito originale** in fondo mostra l’invito così come è arrivato.

## Aggiungi o modifica un evento

Da qui puoi modificare il tuo calendario Google. Outlook e gli altri calendari sono solo in visualizzazione. **Nuovo evento** ne aggiunge uno (sul telefono lo trovi sotto **+** nella barra in alto): scegli il calendario, un titolo e un orario. Seleziona un evento senza ospiti nel calendario per modificarlo o **Elimina** per cancellarlo (tocca due volte).

Quando inizi a digitare, **Dove** suggerisce dei luoghi: prima quelli che hai già usato e le tue organizzazioni, poi gli indirizzi di [OpenStreetMap](https://www.openstreetmap.org), una mappa gratuita. Per cercarli vengono inviate solo le parole che digiti. Scegli un suggerimento o mantieni il testo che hai inserito.

**Invita** aggiunge persone dal tuo Graph o qualsiasi indirizzo email. Questa opzione è disponibile solo nel tuo calendario. Chi riceverà un invito è indicato sopra il pulsante, che mostra anche il numero di persone: **Aggiungi e invita 2**. Google invia gli inviti quando tocchi il pulsante, non prima. Se non ci sono ospiti, nessuno riceve un invito o un aggiornamento.

Anche un’attività può proporre una modifica, per esempio aggiungere un ritiro. Mostra esattamente cosa cambierà. La modifica avviene solo se scegli **Aggiungi**, **Salva** o **Elimina**.

Non hai ancora riunioni? Se non hai un calendario, **Collega il tuo calendario** apre Connessioni. Da lì puoi collegare [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) o [un altro calendario](other-calendars.md).

## Conflitti con l’altro calendario

Quando una riunione di lavoro si sovrappone a un impegno nel tuo calendario personale, o viceversa, The Machine crea un’attività relativa a quella più recente. Può preparare una breve nota per spostarla o proporti di rifiutare l’invito. Non viene inviato nulla finché non approvi.

Gli eventi di tutto il giorno, quelli in cui risulti libero e quelli provvisori non vengono considerati. Ogni conflitto viene segnalato una sola volta. Un’attività di Lavoro indica solo che c’è un conflitto, così il tuo team non vede l’evento personale. Solo tu puoi vedere con cosa è in conflitto.

## Preparati per le riunioni

Prima di una riunione con persone esterne alla tua azienda, The Machine crea un’attività: **Preparati per** la riunione. È un breve riepilogo:

- **Chi:** chi sono, in base al tuo Graph, con informazioni sul loro passato quando disponibili.
- **Organizzazione:** di cosa si occupa la loro azienda, a chi si rivolge e a quale prezzo, se è rilevante per la riunione.
- **Finora:** di cosa avete parlato, cosa avete chiesto e proposto e a che punto siete. Dopo la riunione, i messaggi pertinenti diventano le fonti dell’attività.
- **Concordato in precedenza:**, **Modificato da allora:** e **Ancora aperto:** cosa è emerso nelle riunioni precedenti con le stesse persone. Ogni riga rimanda alla riunione o al messaggio da cui proviene.
- **Promesse aperte:** ciò che tu o gli altri dovete ancora fare, in base alle promesse sulla tua Machine.
- **Questioni aperte:** ciò che è ancora senza risposta.
- **Decidi o porta con te:** cosa stabilire o portare e cosa probabilmente sarà importante per gli altri.

L’attività arriva la mattina di un giorno lavorativo: il giorno della riunione se è nel pomeriggio, altrimenti il giorno lavorativo precedente. Serve solo per consultarla: tocca **Fatto** quando l’hai letta. Una promessa o una domanda che richiede un’azione ha una sua attività.

Vengono considerate le riunioni precedenti a cui partecipava una persona esterna, anche se avevano un altro titolo o se la persona aveva usato un indirizzo diverso. La tua Machine legge le note disponibili: le tue, quelle dell’app per riunioni o quelle che ti ha inviato via email. Se non ce ne sono, usa la trascrizione o le note dell’evento nel calendario. Le note più recenti hanno più peso e un punto risolto in seguito non viene indicato come aperto.

Vengono considerate anche le note e i messaggi della [Cronologia](history.md), così il riepilogo può includere riunioni precedenti a quando hai iniziato a usare la tua Machine.

Un riepilogo di lavoro non legge note personali né contenuti dalla Machine di un’altra persona. Il testo resta con te: un passaggio non lo include e non puoi inviarlo per una revisione. Se non ci sono note, quelle righe non vengono mostrate.

Usa le informazioni già presenti sulla tua Machine. Per una prima riunione con una persona che lavora per un’azienda, legge anche la pagina iniziale del sito dell’azienda.

Se la ricerca sul web è configurata sulla tua Machine, cerca brevemente il nome della persona e dell’azienda. Una Machine ospitata non include questa funzione; sul tuo computer puoi configurarla in OpenClaw. I risultati includono un link. La ricerca riceve solo il nome pubblico della persona, il nome dell’azienda e il sito web, mai i tuoi messaggi. I risultati vengono riutilizzati per 30 giorni.

Così, prima di aver scambiato una parola, puoi ricevere un riepilogo per una prima riunione a cui hai accettato di partecipare: di cosa si occupa l’azienda, cosa significa per te e, se possibile, chi è la persona. Se hai solo il nome, conserva i risultati della ricerca solo quando rimandano a una sola persona. Se **Cerca i contatti di lavoro** è disattivato in Impostazioni, Sicurezza, non viene fatta alcuna ricerca.

Una riunione ricorrente ha un riepilogo solo se ci sono novità dall’ultima volta: un messaggio, delle note o una promessa. Il riepilogo indica cosa c’è di nuovo, non ripete quello precedente. Viene creato solo dopo la conclusione della riunione precedente e, al massimo, per due riunioni ricorrenti al giorno.

Se non c’è nulla di utile da dire, non viene creata un’attività. Le riunioni interne, personali e rifiutate non ne generano. Se una riunione viene spostata, mantiene la stessa attività, aggiornata al nuovo orario. Un’attività che hai scartato non ricompare; quella di una riunione annullata si chiude automaticamente.

Se un aggiornamento modifica il contenuto di un riepilogo, quelli delle riunioni ancora da svolgere vengono riscritti una sola volta con le nuove informazioni. Il titolo, le fonti e la posizione nell’elenco non cambiano. I riepiloghi che hai modificato, posticipato o chiuso restano invariati, così come quelli delle riunioni che iniziano nei prossimi minuti.

Nei dettagli della riunione, trovi l’attività sotto **Attività**. Tocca per aprire la chat.
