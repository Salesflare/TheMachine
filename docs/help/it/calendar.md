---
title: Calendario
area: calendar
summary: La settimana che ti aspetta, tutta in un posto: riunioni, attività in scadenza, attività posticipate e promesse.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 24033419578a8c8f
---
## Cosa mostra

I tuoi giorni a partire da oggi, con:

- le riunioni dei calendari che hai collegato,
- le attività in scadenza quel giorno e quelle posticipate nel giorno in cui ricompaiono,
- gli aggiornamenti sulle attività che hai delegato,
- le promesse con una data,
- [viaggi ed eventi](calendar.md#trips-and-events) ricavati dalle email di prenotazioni e biglietti.

Una riunione presente in due calendari compare una sola volta. Un calendario condiviso con te mostra gli eventi dell’altra persona in tono attenuato, con il suo nome. Questi eventi non generano mai un’attività. Gli eventi che durano tutto il giorno o più giorni sono indicati come eventi di un’intera giornata, per ogni giorno interessato. In Agenda, un viaggio è il primo elemento di ciascuno dei suoi giorni; in Settimana e Mese appare come una fascia che li attraversa, per esempio «Viaggio a Lisbona».

Un programma concordato insieme è un’unica promessa, contrassegnata con «Con» e il nome dell’altra persona. Una promessa relativa a una riunione di quel giorno con la stessa persona compare nella riga della riunione.

**In ritardo** compare per primo. Una riunione con un’attività aperta mostra il suo stato: **Preparazione pronta**, **In preparazione** o **Attività**. Un’attività che sembra completata, perché hai già risposto o perché la sua esecuzione l’ha trovata completata, non compare come **Scadenza**.

## Agenda, settimana o mese

- **Agenda** mostra un elenco per ogni giorno. Scorri verso il basso per i giorni successivi oppure verso l’alto, o tocca **Mostra giorni precedenti**, per quelli passati. Torna indietro fino a una settimana prima che collegassi il calendario, con una riga in alto che indica da quale giorno. Una volta caricata la [cronologia](history.md), torna indietro di circa un anno.
- **Settimana** mostra una griglia dal lunedì alla domenica. Sul telefono mostra tre giorni.
- **Mese** mostra l’intero mese. Sul computer mostra fino a tre elementi al giorno; sul telefono mostra dei punti e toccandone uno vedi l’elenco di quel giorno.

**Oggi**, ‹ e › in alto ti permettono di spostarti tra le settimane o i mesi. La vista che scegli viene ricordata su quel dispositivo.

Nella griglia settimanale, gli eventi che si svolgono nello stesso momento sono affiancati e restano leggibili. Gli altri sono indicati con **+N**. Toccandolo, si apre quel giorno in Agenda.

## Aprire un elemento

Fai clic su una riga per aprire la chat dell’attività, la promessa, il viaggio o l’evento, oppure la riunione. Una riunione che non puoi modificare da qui, per esempio quella di un’altra persona o con invitati, mostra i dettagli: quando, dove e chi. Le persone che il tuo Graph conosce e le organizzazioni e i progetti associati alla riunione sono link alle rispettive pagine. **Apri in Google Calendar** (o **Apri in Outlook**) sotto i dettagli apre la riunione nel relativo servizio. Visualizzare la riunione non apporta modifiche.

Una sala riunioni prenotata per una riunione compare sotto «Dove», mai come persona o nel tuo Graph.

Il link a una riunione mostra il nome del servizio, per esempio Zoom, Google Meet o Teams, oppure **Videochiamata**. Apri la riunione per partecipare.

## Viaggi ed eventi

Quando ricevi un’email di prenotazione per un volo, un hotel, una casa vacanze, un treno, un autobus, un traghetto, un’auto a noleggio, un taxi o un parcheggio in aeroporto, la tua Machine la aggiunge a un viaggio. Le prenotazioni dello stesso itinerario, da una qualsiasi delle tue caselle email, vengono raccolte in un unico viaggio: il treno per l’aeroporto, i voli, l’auto, il soggiorno e il viaggio di ritorno. Le prenotazioni vengono unite se i giorni si sovrappongono o se una comincia quando finisce l’altra.

Il viaggio appare come una fascia che attraversa tutti i suoi giorni. Aprilo per vedere le prenotazioni in ordine cronologico, con orari, indirizzo, codice di prenotazione e posto.

I biglietti per un concerto, una partita, un festival o una conferenza creano un evento, uno per ciascun evento, con il luogo, il codice di prenotazione, il posto e il numero di biglietti. Un secondo ordine per lo stesso evento viene aggiunto allo stesso evento. Un biglietto prenotato nella casella email di lavoro è contrassegnato come Lavoro, altrimenti come Personale. I biglietti per qualcosa che si svolge durante un viaggio vengono aggiunti al viaggio.

Per un viaggio futuro, la tua Machine indica cosa manca, per esempio **Nessun alloggio prenotato per 2 notti** oppure nessuna prenotazione dall’aeroporto all’hotel. Queste righe sono attenuate e contrassegnate con **Nessuna prenotazione**. Se un viaggio non include pernottamenti, non viene indicato nulla sulle notti.

- Ogni riga indica da chi proviene la prenotazione, per esempio **Da Example Tickets**, e apre l’email.
- Se dall’email è stata creata un’attività, per esempio per pagare i biglietti, **Apri l’attività** la mostra.
- Se una prenotazione cambia, la relativa riga viene aggiornata; se viene annullata, viene rimossa. Quando tutte le prenotazioni sono annullate, viene rimosso anche il viaggio o l’evento.
- Una prenotazione per qualcun altro, per esempio il volo di un collega che ti è stato inoltrato, non compare tra i tuoi viaggi.

La maggior parte delle conferme contiene i dettagli in un formato che la tua Machine può leggere senza AI. Se non è così, per esempio per un’email inoltrata o un piccolo sito di prenotazioni, il tuo [modello](model.md) legge l’email in background, poche alla volta, e aspetta se ti stai avvicinando al limite di utilizzo. Le email di prenotazione dell’anno di [cronologia](history.md) conservato dalla tua Machine vengono lette in background una volta caricata la cronologia.

## Note e trascrizione della riunione

I dettagli di una riunione hanno due parti. **Note** è il riepilogo, con decisioni e attività da svolgere. **Trascrizione** riporta parola per parola ciò che è stato detto. All’inizio è chiusa e mostra la durata; **Mostra** la apre.

Se non si caricano, la riunione riprova automaticamente per circa mezzo minuto. Dopo, tocca **Riprova**.

Ognuna ha i propri comandi **Aggiungi note** o **Aggiungi trascrizione**, **Carica file** per un file Markdown o di testo, **Modifica** e **Rimuovi** (tocca due volte). Quello che aggiungi a una parte rimane lì. In una riunione che puoi modificare, **Note** sotto al modulo le apre.

Se hai collegato [Zoom](zoom.md), [Google Meet](google-meet.md) o [Granola](granola.md), le note del servizio compaiono in Note e la trascrizione in Trascrizione, contrassegnate con **Da Zoom**, **Da Google Meet** o **Da Granola**. Non sostituiscono mai quello che hai aggiunto: se ci sono entrambi, vengono mostrati entrambi.

Le note possono essere aggiunte anche all’evento della riunione nel calendario, dopo il suo inizio, oppure ricevute via email da Zoom o Gemini. Quando la riunione termina, The Machine crea attività da queste note solo per i passaggi successivi espliciti. Se arrivano le stesse note in due modi, viene creata una sola attività, con la riunione come fonte: «Fonte: note di» seguito dalla riunione.

Una riunione con una trascrizione ma senza note mostra **Genera note**. The Machine le scrive a partire dalla trascrizione: un breve riepilogo, le decisioni e le attività da svolgere con l’indicazione di chi se ne occupa, nella lingua della riunione.

Compare **Sto scrivendo le note…** e la generazione continua anche se chiudi la riunione. Per una riunione lunga possono servire alcuni minuti e viene usato il tuo modello. Le note sono contrassegnate con **Scritto da The Machine** e non sostituiscono mai quelle che hai aggiunto.

Puoi chiedere anche alla tua Machine di aggiungerle. Chiedile in una chat di un’attività, per esempio «aggiungi questa trascrizione alla riunione di oggi sulla bacheca». La trascrizione viene aggiunta in Trascrizione, il riepilogo in Note. Nel Calendario, una riunione con note o trascrizione mostra **Note** o **Trascrizione**.

La tua Machine legge entrambe per individuare i prossimi passi della riunione. Sono contrassegnati come Lavoro o Personale, come la riunione, e vengono condivisi con il tuo team solo se anche la riunione è condivisa.

La riunione si apre con questi dettagli ovunque la trovi: nella cronologia, nei risultati di una ricerca nei messaggi o come fonte di un’attività. **Invito originale** in fondo mostra l’invito così come l’hai ricevuto.

## Aggiungere o modificare un evento

Da qui puoi modificare il tuo calendario Google. Outlook e gli altri calendari sono di sola visualizzazione. **Nuovo evento** ne aggiunge uno (sul telefono lo trovi sotto **+** nella barra in alto): scegli il calendario, un titolo e l’orario. Fai clic su un evento senza invitati in quel calendario per modificarlo o **Elimina** per cancellarlo (tocca due volte).

**Dove** suggerisce luoghi mentre scrivi: prima quelli che hai già usato e le tue organizzazioni, poi gli indirizzi di [OpenStreetMap](https://www.openstreetmap.org), una mappa gratuita. Per cercarli vengono inviate solo le parole che scrivi. Scegli un suggerimento o lascia il testo che hai inserito.

**Invita** aggiunge persone dal tuo Graph o qualsiasi indirizzo email. È disponibile solo nel tuo calendario. Gli invitati sono elencati sopra il pulsante, che indica anche quanti sono: **Aggiungi e invita 2**. Google invia gli inviti quando tocchi il pulsante, non prima. Se non ci sono invitati, nessuno riceve un invito o un aggiornamento.

Anche un’attività può suggerire una modifica, per esempio aggiungere un ritiro. Mostra esattamente cosa cambierà; la modifica viene applicata solo se tocchi **Aggiungi**, **Salva** o **Elimina**.

Non hai ancora riunioni? Se non hai collegato un calendario, **Collega il tuo calendario** apre Connessioni. Da lì puoi collegare [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) o [un altro calendario](other-calendars.md).

## Conflitti con l’altro calendario

Se una riunione di lavoro si sovrappone a qualcosa nel tuo calendario personale, o viceversa, The Machine crea un’unica attività relativa a quella più recente. Può preparare una breve nota per spostarla oppure offrirti di rifiutarla. Non viene inviato nulla finché non lo approvi.

Gli eventi che durano tutto il giorno, quelli con stato libero e quelli provvisori non vengono conteggiati; ogni conflitto compare una sola volta. Un’attività di Lavoro indica solo che c’è un conflitto, quindi il tuo team non vede mai l’evento personale. Solo tu puoi vedere con quale evento è in conflitto.

## Preparati alle riunioni

Prima di una riunione con persone che non fanno parte della tua azienda, The Machine crea un’attività: **Preparati per** la riunione. È un breve riepilogo:

- **Chi:** chi sono, secondo il tuo Graph, e qualche informazione sul loro percorso, se disponibile.
- **Organizzazione:** cosa fa la loro azienda e perché è rilevante per la riunione.
- **Finora:** cosa avete discusso, chiesto e proposto, e a che punto siete. Dopo la riunione, quei messaggi diventano fonti dell’attività.
- **Promesse aperte:** cosa resta da fare a te o a loro.
- **Domande aperte:** cosa è ancora senza risposta.
- **Decidere o portare:** cosa definire o portare e cosa probabilmente sarà importante per loro.

L’attività arriva la mattina di un giorno lavorativo: il giorno stesso se la riunione è nel pomeriggio, altrimenti il giorno lavorativo precedente. Serve solo per consultarla: tocca **Fatto** dopo averla letta. Le promesse o le domande da seguire contenute nel riepilogo hanno una propria attività.

Usa le informazioni già presenti sulla tua Machine. Per il primo incontro con una persona di un’azienda, fa anche una breve ricerca online sul suo nome e sull’azienda e mostra un link accanto alle informazioni trovate. La ricerca usa solo il nome pubblico della persona, il nome dell’azienda e il suo sito web, mai i tuoi messaggi. I risultati della ricerca vengono riutilizzati per 30 giorni. Se disattivi **Cerca i contatti di lavoro** (Impostazioni, Sicurezza), non viene fatta alcuna ricerca.

Se non ci sono informazioni utili, l’attività non viene creata. Non viene creata per riunioni ricorrenti, interne, personali o rifiutate. Se una riunione viene spostata, la sua unica attività resta, con il nuovo orario. Un’attività scartata non ricompare e quella di una riunione annullata si chiude automaticamente.

Se un aggiornamento modifica le informazioni contenute in un riepilogo, i riepiloghi delle riunioni future ancora da svolgere vengono riscritti una sola volta con i nuovi contenuti. Titolo, fonti e posizione nell’elenco restano invariati. Un riepilogo che hai modificato, posticipato o chiuso resta com’è. Lo stesso vale per quello di una riunione che inizia tra pochi minuti.

I dettagli della riunione mostrano la relativa attività sotto **Attività**. Tocca per aprire la chat.
