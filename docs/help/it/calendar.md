---
title: Calendario
area: calendar
summary: La settimana che ti aspetta, in un unico posto: riunioni, attività in scadenza, attività posticipate e promesse.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 9f38e3718f3e8639
---
## Cosa mostra

I tuoi giorni a partire da oggi, con:

- le riunioni dei calendari che hai collegato,
- le attività in scadenza quel giorno e quelle posticipate, nel giorno in cui tornano,
- gli aggiornamenti sul lavoro che hai delegato,
- le promesse con una data,
- [viaggi ed eventi](calendar.md#trips-and-events) ricavati dalle email di prenotazioni e biglietti.

Una riunione presente in due calendari viene mostrata una sola volta. Un calendario condiviso con te mostra gli eventi di chi lo ha condiviso in tono attenuato e con il suo nome; questi eventi non generano mai attività. Gli eventi di un’intera giornata o di più giorni sono indicati come eventi di un’intera giornata in ogni giorno interessato. In Agenda, un viaggio appare per primo in ciascuno dei suoi giorni; in Settimana e Mese, è mostrato come una fascia che copre tutti i giorni, per esempio «Viaggio a Lisbona».

Un piano concordato insieme è una sola promessa, indicata con «Con» e il nome dell’altra persona. Una promessa relativa a una riunione di quel giorno con la stessa persona appare nella riga della riunione.

**In ritardo** viene prima di tutto. Una riunione con un’attività ancora aperta mostra il suo stato: **Preparazione pronta**, **In preparazione** o **Attività**. Un’attività che sembra completata, perché hai già risposto o perché l’esecuzione ha rilevato che è stata completata, non viene mostrata come **Scadenza**.

## Agenda, settimana o mese

- **Agenda** elenca i giorni. Scorri verso il basso per i giorni successivi o verso l’alto, oppure seleziona **Mostra giorni precedenti**, per quelli precedenti. Risale fino a una settimana prima di quando hai collegato il calendario e mostra in alto una riga che indica da quale giorno. Quando è disponibile la [cronologia](history.md), risale a circa un anno prima.
- **Settimana** mostra una griglia dal lunedì alla domenica. Sul telefono mostra tre giorni.
- **Mese** mostra tutto il mese. Sul computer mostra fino a tre elementi al giorno; sul telefono mostra dei punti e, toccandone uno, elenca gli eventi di quel giorno.

**Oggi**, ‹ e › in alto ti permettono di spostarti tra le settimane o i mesi. La vista che scegli viene ricordata su quel dispositivo.

Nella griglia della settimana, gli eventi che si svolgono alla stessa ora sono affiancati e restano leggibili. Gli altri sono indicati con **+N**. Selezionalo per aprire quel giorno in Agenda.

## Aprire un elemento

Seleziona una riga per aprire la chat dell’attività, la promessa, il viaggio o l’evento, oppure la riunione. Per una riunione che non puoi modificare qui, per esempio una di un’altra persona o con invitati, sono mostrati i dettagli: quando e dove si svolge e chi partecipa. Le persone che conosci tramite Graph e le organizzazioni e i progetti associati alla riunione rimandano alla rispettiva pagina. **Apri in Google Calendar** o **Apri in Outlook** li apre nel relativo calendario. La semplice visualizzazione non apporta modifiche.

Una sala prenotata per una riunione è indicata sotto il luogo, mai come persona o in Graph.

Il link di una riunione è mostrato con il nome del servizio, per esempio Zoom, Google Meet o Teams, oppure come **Videochiamata**. Apri la riunione per partecipare.

## Viaggi ed eventi

Quando ricevi un’email con una prenotazione di volo, hotel, casa vacanze, treno, autobus, traghetto, auto a noleggio, taxi o parcheggio in aeroporto, la tua Machine la aggiunge a un viaggio. Le prenotazioni dello stesso itinerario vengono raggruppate in un viaggio, da qualsiasi casella email: il treno per l’aeroporto, i voli, l’auto, il soggiorno e il viaggio di ritorno. Le prenotazioni vengono raggruppate se le date si sovrappongono o se una inizia quando finisce l’altra.

Il viaggio è mostrato come una fascia che copre tutti i suoi giorni. Aprilo per vedere le prenotazioni in ordine cronologico, con orari, indirizzo, codice di prenotazione e posto.

I biglietti per un concerto, una partita, un festival o una conferenza creano un evento, uno per ogni occasione, con il luogo, il codice di prenotazione, il posto e il numero di biglietti. Un secondo ordine per lo stesso evento viene aggiunto allo stesso evento. Un evento prenotato nella casella email di lavoro è di lavoro, altrimenti è personale. I biglietti per un evento durante un viaggio vengono aggiunti al viaggio.

Per un viaggio futuro, la tua Machine indica cosa manca, per esempio **Nessuna prenotazione di alloggio per 2 notti** o nessuna prenotazione dall’aeroporto all’hotel. Queste righe sono in tono attenuato e contrassegnate con **Nessuna prenotazione**. Se un viaggio non include pernottamenti, non vengono mostrate informazioni sulle notti.

- Ogni riga indica da chi proviene la prenotazione, per esempio **Da Example Tickets**, e apre l’email.
- Se dall’email è stata creata un’attività, per esempio per pagare i biglietti, **Apri l’attività** la mostra.
- Una prenotazione modificata aggiorna la relativa riga; una prenotazione annullata viene rimossa. Se tutte le prenotazioni sono annullate, viene rimosso anche il viaggio o l’evento.
- Una prenotazione per un’altra persona, come il volo di un collega che ti è stato inoltrato, non viene aggiunta ai tuoi viaggi.

La maggior parte delle email di conferma contiene i dettagli in un formato che la tua Machine può leggere senza IA. Per le email che non usano questo formato, come quelle inoltrate o provenienti da piccoli siti di prenotazione, il tuo [modello](model.md) legge le email in background, alcune alla volta, e si mette in pausa quando ti avvicini al limite di utilizzo. Una volta disponibile la [cronologia](history.md), le email di prenotazione dell’anno conservato dalla tua Machine vengono lette in background.

## Note e trascrizione della riunione

I dettagli di una riunione hanno due sezioni. **Note** è il riepilogo, con decisioni e attività da svolgere. **Trascrizione** riporta parola per parola ciò che è stato detto. All’inizio è chiusa e ne viene mostrata la durata; seleziona **Mostra** per aprirla.

Se non si caricano, la riunione riprova automaticamente per circa mezzo minuto. Dopo, seleziona **Riprova**.

Ognuna ha i propri comandi **Aggiungi note** o **Aggiungi trascrizione**, **Carica file** per un file Markdown o di testo, **Modifica** e **Rimuovi** (seleziona due volte). I contenuti aggiunti a una sezione restano lì. In una riunione che puoi modificare, seleziona **Note** sotto il modulo per aprirle.

Se hai collegato [Zoom](zoom.md), [Google Meet](google-meet.md) o [Granola](granola.md), le relative note vengono mostrate in Note e la trascrizione in Trascrizione, con l’indicazione **Da Zoom**, **Da Google Meet** o **Da Granola**. Non sostituiscono mai ciò che hai aggiunto: se sono presenti entrambi, vengono mostrati entrambi.

Le note possono essere aggiunte anche all’evento della riunione nel calendario, dopo il suo inizio, oppure inviate per email da Zoom o Gemini. Al termine della riunione, The Machine crea attività da queste note solo per le azioni successive chiaramente indicate. Se le stesse note arrivano in due modi diversi, viene creata una sola attività, che riporta la riunione come fonte: «Fonte: note di» seguito dal nome della riunione.

Una riunione con una trascrizione ma senza note mostra **Genera note**. The Machine le ricava dalla trascrizione: un breve riepilogo, le decisioni e le attività da svolgere con l’indicazione di chi se ne occupa, nella lingua della riunione.

Viene mostrato **Sto scrivendo le note…** e la generazione continua anche se chiudi la riunione. Per una riunione lunga possono servire alcuni minuti e viene usato il tuo modello. Le note indicano **Scritte da The Machine** e non sostituiscono mai quelle che hai aggiunto.

Puoi chiedere anche alla tua assistente di aggiungerle. Per esempio, chiedi in una chat di un’attività: «aggiungi questa trascrizione alla riunione del consiglio di oggi». Una trascrizione viene aggiunta a Trascrizione, un riepilogo a Note. Nel Calendario, una riunione con note o trascrizione mostra **Note** o **Trascrizione**.

The Machine legge entrambe per individuare le azioni successive della riunione. Sono di lavoro o personali come la riunione e vengono condivise con il tuo team solo se lo è anche la riunione.

Puoi aprire una riunione con questi dettagli da qualsiasi punto in cui la trovi: una cronologia, una ricerca nei messaggi o la fonte di un’attività. **Invito originale** in fondo mostra l’invito così come è arrivato.

## Aggiungere o modificare un evento

Puoi modificare da qui il tuo calendario Google. Outlook e gli altri calendari sono solo consultabili. **Nuovo evento** ne aggiunge uno (sul telefono si trova sotto **+** nella barra superiore): scegli il calendario, un titolo e l’orario. Seleziona un evento senza invitati in quel calendario per modificarlo o **Elimina** per cancellarlo (seleziona due volte).

**Dove** suggerisce dei luoghi mentre scrivi: prima quelli che hai già usato e le tue organizzazioni, poi gli indirizzi di [OpenStreetMap](https://www.openstreetmap.org), una mappa gratuita. Per la ricerca vengono inviate solo le parole che scrivi. Scegli un suggerimento o lascia il testo che hai scritto.

**Invita** aggiunge persone da Graph o qualsiasi indirizzo email. Questa opzione è disponibile solo nel tuo calendario. Le persone invitate sono elencate sopra il pulsante, che indica anche quante sono: **Aggiungi e invita 2**. Google invia gli inviti quando lo selezioni, non prima. Se non ci sono invitati, nessuno riceve un invito o un aggiornamento.

Anche un’attività può suggerire una modifica, per esempio aggiungere un ritiro. Mostra esattamente cosa cambierà e la modifica viene applicata solo se selezioni **Aggiungi**, **Salva** o **Elimina**.

Non hai ancora riunioni? Se non hai collegato un calendario, **Collega il tuo calendario** apre Connessioni: collega [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) o [un altro calendario](other-calendars.md).

## Conflitti con l’altro calendario

Quando una riunione di lavoro si sovrappone a un impegno nel tuo calendario personale, o viceversa, The Machine crea un’attività per quello dei due che è stato aggiunto più di recente. Può preparare un breve messaggio per spostarlo oppure proporti di rifiutarlo. Non viene inviato nulla finché non approvi.

Gli eventi di un’intera giornata, con stato libero o provvisorio non vengono conteggiati e ogni conflitto viene segnalato una sola volta. Un’attività di lavoro indica solo che c’è un conflitto, così il tuo team non vede mai l’evento personale. Solo tu puoi vedere con quale evento è in conflitto.

## Preparati alle riunioni

Prima di una riunione con persone esterne alla tua azienda, The Machine crea un’attività: **Preparati per** la riunione. È un breve riepilogo:

- **Chi:** chi sono, secondo Graph, e alcune informazioni sul loro percorso, se disponibili.
- **Organizzazione:** di cosa si occupa la loro azienda e cosa è utile sapere per la riunione.
- **Finora:** di cosa avete parlato, cosa avete chiesto e proposto e a che punto siete. Dopo la riunione, quei messaggi vengono aggiunti come fonti dell’attività.
- **Promesse aperte:** cosa tu o loro dovete ancora fare, in base alle promesse sulla tua Machine.
- **Questioni aperte:** cosa è ancora senza risposta.
- **Decisioni o materiali da portare:** cosa decidere o portare e a cosa probabilmente saranno interessati.

L’attività viene creata la mattina di un giorno lavorativo: il giorno stesso se la riunione è nel pomeriggio, altrimenti il giorno lavorativo precedente. Serve solo per consultare le informazioni: seleziona **Fatto** dopo averle lette. Le promesse o le domande che richiedono un’azione hanno una propria attività.

La tua Machine usa le informazioni che ha già. Per il primo incontro con una persona di un’azienda, cerca anche brevemente sul web il suo nome e quello dell’azienda e mostra un link accanto ai risultati. Nella ricerca vengono inviati solo il nome pubblico della persona, il nome dell’azienda e il suo sito web, mai i tuoi messaggi. I risultati della ricerca vengono riutilizzati per 30 giorni. Se disattivi **Cerca i contatti di lavoro** in Impostazioni, Sicurezza, non viene effettuata alcuna ricerca.

Se non ci sono informazioni utili sulla riunione, non viene creata alcuna attività. Non viene creata per le riunioni ricorrenti, interne o personali, né per quelle rifiutate. Se una riunione viene spostata, la sua attività resta una sola e viene aggiornata al nuovo orario. Un’attività scartata non ricompare; quella di una riunione annullata viene chiusa automaticamente.

Se un aggiornamento modifica le informazioni del riepilogo, i riepiloghi delle riunioni future vengono riscritti una sola volta con i nuovi contenuti. Il titolo, le fonti e la posizione nell’elenco restano invariati. Un riepilogo che hai modificato, posticipato o chiuso resta com’è; lo stesso vale per quello di una riunione che inizia tra pochi minuti.

I dettagli della riunione mostrano la relativa attività sotto **Attività**. Selezionala per aprire la chat.
