---
title: Calendario
area: calendar
summary: La settimana che ti aspetta, tutta in un posto: riunioni, attività in scadenza, attività posticipate e promesse.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 4b5bc600fefb624c
---
## Cosa mostra

Le tue giornate a partire da oggi, con:

- le riunioni dei calendari che hai collegato,
- le attività in scadenza quel giorno e quelle posticipate al giorno in cui tornano,
- gli aggiornamenti sul lavoro che hai passato ad altri,
- le promesse con una data,
- [viaggi ed eventi](calendar.md#trips-and-events) delle prenotazioni e dei biglietti ricevuti via email.

Una riunione presente in due calendari compare una sola volta. Un calendario condiviso con te mostra gli eventi di chi lo ha condiviso in modo attenuato, con il suo nome. Questi eventi non generano mai un’attività. Gli eventi che durano tutto il giorno o più giorni vengono mostrati come eventi di un’intera giornata in ciascun giorno interessato. In Agenda, un viaggio appare per primo in ciascuno dei suoi giorni; in Settimana e Mese è una sola fascia che li attraversa, per esempio «Viaggio a Lisbona».

Un piano fatto insieme è una sola promessa, contrassegnata da «Con» e dal nome dell’altra persona. Una promessa relativa a una riunione di quel giorno con la stessa persona compare nella riga della riunione.

**In ritardo** compare per primo. Una riunione con un’attività ancora aperta la mostra con uno di questi stati: **Preparazione pronta**, **In preparazione** o **Attività**. Un’attività che sembra completata, perché hai già risposto o perché la sua esecuzione l’ha segnata come completata, non compare come **Scadenza**.

## Agenda, settimana o mese

- **Agenda** elenca le giornate. Scorri verso il basso per vedere i giorni successivi, oppure verso l’alto o tocca **Mostra giorni precedenti** per vedere quelli passati. Torna indietro fino a una settimana prima che collegassi il calendario e mostra in alto da quale giorno parte. Quando è disponibile la [cronologia](history.md), torna indietro di circa un anno.
- **Settimana** mostra una griglia, da lunedì a domenica. Sul telefono mostra tre giorni.
- **Mese** mostra tutto il mese. Sul computer mostra fino a tre elementi al giorno; sul telefono mostra dei puntini. Tocca un giorno per vedere l’elenco degli elementi.

**Oggi**, ‹ e › in alto ti permettono di spostarti tra le settimane o i mesi. La visualizzazione scelta viene memorizzata su quel dispositivo.

Nella griglia settimanale, gli eventi alla stessa ora sono affiancati e restano leggibili. Gli altri vengono indicati con **+N**. Toccalo per aprire quel giorno nell’Agenda.

## Aprire un elemento

Fai clic su una riga per aprire la chat dell’attività, la promessa, il viaggio o l’evento, oppure la riunione. Una riunione che non puoi modificare qui, per esempio perché appartiene a un’altra persona o ha degli invitati, mostra i suoi dettagli: quando e dove si svolge e chi partecipa. Le persone che il tuo Graph conosce, le organizzazioni e i progetti associati alla riunione sono link alle rispettive pagine. **Apri in Google Calendar** o **Apri in Outlook**, sotto questi link, apre la riunione nell’app corrispondente. La sola consultazione non modifica nulla.

Se una sala riunioni è stata prenotata per una riunione, compare sotto il luogo, non come persona né nel tuo Graph.

Il link alla riunione mostra il servizio corrispondente, per esempio Zoom, Google Meet o Teams, oppure **Videochiamata**. Apri la riunione per partecipare.

## Viaggi ed eventi

Quando ricevi un’email con la prenotazione di un volo, hotel, casa vacanze, treno, autobus, traghetto, auto a noleggio, taxi o parcheggio in aeroporto, la tua Machine la aggiunge a un viaggio. Le prenotazioni dello stesso itinerario vengono riunite in un solo viaggio, da una qualsiasi delle tue caselle email: il treno per l’aeroporto, i voli, l’auto, il soggiorno e il viaggio di ritorno. Le prenotazioni vengono raggruppate se le date si sovrappongono o se una inizia quando finisce l’altra.

Il viaggio compare come un’unica fascia che attraversa i suoi giorni. Aprilo per vedere tutte le prenotazioni in ordine cronologico, con orari, indirizzo, codice di prenotazione e posto.

I biglietti per un concerto, una partita, un festival o una conferenza creano un evento, uno per ciascun evento, con il luogo, il codice di prenotazione, il posto e il numero di biglietti. Un secondo ordine per lo stesso evento viene aggiunto allo stesso evento. Un biglietto prenotato nella tua casella di lavoro è di Lavoro, altrimenti è Personale. I biglietti per qualcosa che si svolge durante un viaggio vengono aggiunti al viaggio.

Se un viaggio è imminente, la tua Machine indica cosa manca, per esempio **Nessun alloggio prenotato per 2 notti** o che non hai prenotato nulla dall’aeroporto all’hotel. Queste righe sono attenuate e contrassegnate con **Nessuna prenotazione**. Se per un viaggio non hai prenotato alcun soggiorno, non vengono mostrate informazioni sulle notti.

- Ogni riga indica da chi proviene la prenotazione, per esempio **Da Example Tickets**, e apre l’email corrispondente.
- Se dall’email è stata creata un’attività, per esempio per pagare i biglietti, **Apri l’attività** la mostra.
- Se una prenotazione cambia, la relativa riga si aggiorna. Se viene annullata, viene rimossa. Quando vengono annullate tutte le prenotazioni, viene rimosso anche il viaggio o l’evento.
- Le prenotazioni di altre persone, come il volo di un collega inoltrato a te, non vengono aggiunte ai tuoi viaggi.

La maggior parte delle conferme contiene i dettagli in un formato che la tua Machine può leggere senza IA. Se una conferma non è in quel formato, per esempio un’email inoltrata o proveniente da un piccolo sito di prenotazioni, il tuo [modello](model.md) la legge in background, poche email alla volta, e aspetta se sei vicino al limite di utilizzo. Le email di prenotazione dell’anno compreso nella [cronologia](history.md) conservata dalla tua Machine vengono lette in background quando la cronologia è disponibile.

## Note e trascrizione delle riunioni

I dettagli di una riunione hanno due parti. **Note** è il riepilogo, con decisioni e attività da svolgere. **Trascrizione** riporta parola per parola quello che è stato detto. All’inizio è chiusa e mostra la durata; **Mostra** la apre.

Se non vengono caricate, la riunione riprova automaticamente per circa mezzo minuto. Dopodiché, tocca **Riprova**.

Per ciascuna sono disponibili **Aggiungi note** o **Aggiungi trascrizione**, **Carica file** per caricare un file Markdown o di testo, **Modifica** e **Rimuovi** (tocca due volte). I contenuti aggiunti in una parte restano lì. Per una riunione che puoi modificare, **Note** sotto il modulo le apre.

Se colleghi [Zoom](zoom.md), [Google Meet](google-meet.md) o [Granola](granola.md), le note del servizio compaiono in Note e la trascrizione in Trascrizione, con l’etichetta **Da Zoom**, **Da Google Meet** o **Da Granola**. Non sostituiscono mai quello che hai aggiunto: se sono presenti entrambi, vengono mostrati entrambi.

Le note possono anche essere aggiunte all’evento della riunione nel calendario dopo il suo inizio, oppure arrivare via email da Zoom o Gemini. Al termine della riunione, The Machine crea attività dalle note solo per i passaggi successivi ben definiti. Se le stesse note arrivano in due modi, viene creata una sola attività, che indica la riunione come origine: «Origine: note della» riunione.

Una riunione con una trascrizione ma senza note mostra **Genera note**. The Machine le ricava dalla trascrizione: un breve riepilogo, le decisioni e le attività da svolgere con i nomi di chi se ne occupa, nella lingua della riunione.

Viene mostrato **Sto scrivendo le note…**. La scrittura continua anche se chiudi la riunione. Per una riunione lunga ci vogliono alcuni minuti e viene usato il tuo modello. Le note riportano **Scritte da The Machine** e non sostituiscono mai quelle che hai aggiunto.

Anche tu puoi chiedere a The Machine di aggiungerle. Per esempio, in un’attività puoi scrivere «aggiungi questa trascrizione alla riunione di oggi della bacheca». La trascrizione viene aggiunta in Trascrizione e il riepilogo in Note. Nel Calendario, una riunione con note o trascrizione mostra **Note** o **Trascrizione**.

The Machine legge entrambe per individuare le attività successive alla riunione. Sono di Lavoro o Personali, come la riunione, e vengono condivise con il team solo se lo è anche la riunione.

Puoi aprire i dettagli della riunione ovunque la trovi: nella cronologia, nei risultati di una ricerca nei messaggi o come origine di un’attività. **Invito originale** in fondo mostra l’invito così come è arrivato.

## Aggiungere o modificare un evento

Puoi modificare da qui il tuo calendario Google. Outlook e gli altri calendari sono solo consultabili. **Nuovo evento** ne aggiunge uno. Sul telefono, lo trovi sotto **+** nella barra in alto. Scegli il calendario, un titolo e l’orario. Fai clic su un evento senza invitati in quel calendario per modificarlo, oppure tocca **Elimina** (due volte) per eliminarlo.

**Dove** suggerisce i luoghi mentre scrivi: prima quelli che hai già usato e le tue organizzazioni, poi gli indirizzi di [OpenStreetMap](https://www.openstreetmap.org), una mappa gratuita. Per cercare un luogo vengono inviate solo le parole che digiti. Seleziona un suggerimento oppure lascia il testo che hai scritto.

**Invita** aggiunge persone dal tuo Graph o qualsiasi indirizzo email. Questa opzione è disponibile solo nel tuo calendario. Gli invitati sono elencati sopra il pulsante, che indica quanti sono: **Aggiungi e invita 2**. Google invia gli inviti quando tocchi il pulsante, non prima. Se non ci sono invitati, nessuno riceve un invito o un aggiornamento.

Un’attività può anche proporti una modifica, per esempio aggiungere un ritiro. Mostra esattamente cosa cambierà. La modifica viene applicata solo se tocchi **Aggiungi**, **Salva** o **Elimina**.

Non hai ancora riunioni? Se non hai collegato un calendario, **Collega il tuo calendario** apre Connessioni, da cui puoi collegare [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) o [un altro calendario](other-calendars.md).

## Conflitti con l’altro calendario

Quando una riunione di lavoro si sovrappone a qualcosa nel tuo calendario personale, o viceversa, The Machine crea un’attività relativa all’evento più recente. Può preparare una breve nota per spostarlo o proporti di rifiutare l’invito. Non viene inviato nulla finché non lo approvi.

Se un evento si sovrappone a più elementi, viene creata una sola attività relativa a quell’evento. Se la sovrapposizione è nuova, viene aggiunta all’attività finché è aperta. Dopo che l’attività è stata completata o scartata, ricompare solo se una riunione viene creata o modificata in seguito.

Gli eventi che durano tutto il giorno, quelli con disponibilità impostata su libera e quelli provvisori non vengono considerati. Ogni conflitto compare una sola volta. Anche il luogo di lavoro impostato in Google, il tempo dedicato alla concentrazione e l’assenza dall’ufficio non vengono considerati. Lo stesso vale per un blocco creato da te che contiene altre riunioni, per esempio una giornata in ufficio: solo le riunioni al suo interno possono entrare in conflitto. Un blocco senza altre persone e senza riunioni, come un volo, può comunque entrare in conflitto con un evento a cui partecipano altre persone.

Un’attività di Lavoro indica solo che c’è un conflitto, così il team non vede mai l’evento personale. Solo tu puoi vedere con cosa è in conflitto: i primi due elementi, poi quanti ce ne sono ancora. Un’attività su cui non hai fatto nulla si chiude automaticamente se il conflitto è con un’altra attività o se non c’era davvero.

## Prepararsi alle riunioni

Prima di una riunione con persone esterne alla tua azienda, The Machine crea un’attività: **Preparati per** la riunione. È un breve riepilogo:

- **Chi:** chi sono, in base al tuo Graph, con informazioni sul loro passato professionale quando disponibili.
- **Organizzazione:** di cosa si occupa la loro azienda, per chi e a quale prezzo, se è utile per la riunione.
- **Finora:** di cosa avete parlato, cosa avete chiesto e proposto e a che punto siete. Dopo la riunione, questi messaggi sono le fonti dell’attività.
- **Concordato in precedenza:**, **Modificato da allora:** e **Ancora aperto:** cosa è emerso nelle riunioni precedenti con le stesse persone. Ogni riga indica la riunione o il messaggio da cui proviene.
- **Promesse aperte:** ciò che tu o loro dovete ancora fare, in base alle promesse sulla tua Machine.
- **Domande aperte:** le questioni a cui non è ancora stata data risposta.
- **Da decidere o portare:** cosa va deciso o portato e cosa probabilmente sarà importante per gli altri partecipanti.

L’attività arriva la mattina di un giorno lavorativo: il giorno stesso della riunione se è nel pomeriggio, altrimenti il giorno lavorativo precedente. È da leggere: quando l’hai letta, tocca **Fatto**. Se contiene una promessa o una domanda che richiede un’azione, ha una propria attività.

Puoi fare domande sulla riunione nella sua chat o aggiungere quello che sai. The Machine risponde oppure integra la tua nota nel riepilogo, per esempio in **Da decidere o portare**, e ne tiene conto. Dal riepilogo non viene inviato nulla.

Le riunioni precedenti vengono considerate se hanno entrambe almeno una persona esterna, indipendentemente dal nome della riunione e dall’indirizzo usato. La tua Machine legge le note disponibili: le tue, quelle dell’app usata per la riunione o quelle che ti ha inviato via email; se non ci sono, legge la trascrizione o le note nell’evento di calendario. Le note più recenti hanno più peso e i punti risolti in seguito non vengono mostrati come aperti.

Vengono considerate anche le note e i messaggi della [Cronologia](history.md), così il riepilogo può includere riunioni precedenti a quando hai iniziato a usare la tua Machine.

Un riepilogo di lavoro non legge note personali né informazioni dalla Machine di un’altra persona. Il contenuto resta con te: un passaggio non lo include e non può essere inviato per una revisione. Se non ci sono note, queste righe non vengono mostrate.

Il riepilogo usa le informazioni già presenti sulla tua Machine. Per la prima riunione con una persona di un’azienda, legge anche la pagina iniziale del sito web dell’azienda.

Se la ricerca sul web è configurata sulla tua Machine, cerca anche brevemente il nome della persona e dell’azienda. Una Machine ospitata non include questa funzione. Sul tuo computer puoi configurarla in OpenClaw. I risultati includono un link. Per la ricerca vengono inviati solo il nome pubblico della persona, il nome dell’azienda e il suo sito web, mai i tuoi messaggi. I risultati vengono riutilizzati per 30 giorni.

Così, per una prima riunione a cui hai accettato di partecipare, puoi ricevere un riepilogo prima ancora di aver scambiato una parola: cosa fa l’azienda, cosa significa per te e, se si sa, chi è la persona. Se conosce solo il nome, la tua Machine conserva i risultati della ricerca solo quando rimandano a una sola persona. Se **Cerca i contatti di lavoro** è disattivato in Impostazioni, Sicurezza, non viene effettuata alcuna ricerca.

Una riunione ricorrente riceve un riepilogo solo se dall’ultima volta è successo qualcosa: un messaggio, delle note o una promessa. Il riepilogo indica le novità, non ripete quello precedente. Arriva dopo la riunione precedente, per un massimo di due riunioni ricorrenti al giorno.

Una riunione con solo persone del tuo team riceve un riepilogo solo se le note delle riunioni precedenti indicano una decisione aperta, un’attività che qualcuno deve ancora svolgere o novità. Le informazioni devono provenire dalla stessa serie di riunioni oppure da una riunione con lo stesso titolo e una delle stesse persone. Non vengono prese da altre riunioni con gli stessi colleghi. The Machine non presenta né cerca informazioni sui tuoi colleghi. Le normali riunioni di aggiornamento non hanno un riepilogo.

Se non c’è niente di utile da dire, non viene creata un’attività. Le riunioni personali e quelle rifiutate non ne generano. Se una riunione viene spostata, mantiene la sua attività all’orario aggiornato. Un’attività scartata non ricompare e quella di una riunione annullata si chiude automaticamente.

Se un aggiornamento modifica il contenuto di un riepilogo, i riepiloghi aperti delle riunioni future vengono aggiornati una sola volta. Titolo, fonti e posizione nell’elenco restano invariati. Un riepilogo che hai modificato, posticipato o chiuso non cambia. Non cambia nemmeno quello di una riunione che inizia nei prossimi minuti.

Nei dettagli della riunione, la relativa attività compare sotto **Attività**. Tocca per aprirne la chat.
