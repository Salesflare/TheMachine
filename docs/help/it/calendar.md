---
title: Calendario
area: calendar
summary: La settimana che ti aspetta, tutta in un posto: riunioni, attività in scadenza, attività posticipate e promesse.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 7f9f9d9e9a502b7d
---
## Cosa mostra

I tuoi giorni da oggi in poi, con:

- le riunioni dei calendari che hai collegato,
- le attività in scadenza quel giorno e quelle posticipate per il giorno in cui tornano,
- i punti di controllo sul lavoro che hai passato ad altri,
- le promesse con una data,
- [viaggi ed eventi](calendar.md#trips-and-events) presi dalle email di prenotazioni e biglietti.

Una riunione presente in due calendari viene mostrata una sola volta. Gli eventi di un calendario che qualcuno ha condiviso con te vengono mostrati attenuati, con il nome di chi l’ha condiviso; non generano mai un’attività. Gli eventi che durano tutto il giorno o più giorni sono mostrati come eventi di un’intera giornata per ciascun giorno che coprono. In Agenda, un viaggio è il primo elemento di ciascuno dei suoi giorni; in Settimana e Mese, è una sola fascia che copre tutti i giorni, come «Viaggio a Lisbona».

Un piano fatto insieme è una sola promessa, contrassegnata con «Con» e il nome dell’altra persona. Una promessa relativa a una riunione di quel giorno con la stessa persona compare nella riga della riunione.

**In ritardo** viene mostrato per primo. Una riunione con un’attività ancora aperta la mostra: **Preparazione pronta**, **In preparazione** o **Attività**. Un’attività che sembra completata (hai già risposto oppure la sua esecuzione l’ha contrassegnata come completata) non viene mostrata come **Scadenza**.

## Agenda, settimana o mese

- **Agenda** mostra ogni giorno. Scorri verso il basso per i giorni successivi o verso l’alto (oppure tocca **Mostra giorni precedenti**) per quelli passati. Mostra i giorni a partire da una settimana prima che collegassi il calendario e, in cima, indica da quale giorno. Quando è disponibile la [cronologia](history.md), risale a circa un anno fa.
- **Settimana** mostra una griglia da lunedì a domenica. Sul telefono mostra tre giorni.
- **Mese** mostra tutto il mese. Sul computer mostra fino a tre elementi al giorno; sul telefono mostra dei punti. Tocca un giorno per vedere l’elenco dei suoi eventi.

**Oggi**, ‹ e › in alto ti permettono di spostarti tra le settimane o i mesi. La vista che scegli viene ricordata su quel dispositivo.

Nella griglia settimanale, gli eventi alla stessa ora sono affiancati, ma restano leggibili. Gli altri vengono raggruppati sotto **+N**. Toccalo per aprire quel giorno nell’agenda.

## Aprire un elemento

Seleziona una riga per aprire la chat dell’attività, la promessa, il viaggio o l’evento, oppure la riunione. Una riunione che non puoi modificare qui, per esempio quella di qualcun altro o una con ospiti, mostra i dettagli: quando, dove e chi. Le persone che conosci tramite Graph e le organizzazioni e i progetti a cui è associata la riunione sono link alle rispettive pagine. Seleziona **Apri in Google Calendar** (o **Apri in Outlook**) sotto i dettagli per aprirla nel relativo calendario. La sola visualizzazione non modifica nulla.

Una sala riunioni prenotata per una riunione compare sotto «Dove», mai come persona o in Graph.

Il link a una riunione viene mostrato con il nome del servizio, per esempio Zoom, Google Meet o Teams, oppure come **Videochiamata**. Apri la riunione per partecipare.

## Viaggi ed eventi

Quando ricevi un’email con una prenotazione di un volo, un hotel, una casa vacanze, un treno, un autobus, un traghetto, un’auto a noleggio, un taxi o un parcheggio in aeroporto, la tua Machine la aggiunge a un viaggio. Le prenotazioni dello stesso itinerario, da qualsiasi tua casella di posta, vengono raggruppate in un unico viaggio: il treno per l’aeroporto, i voli, l’auto, il soggiorno e il viaggio di ritorno. Le prenotazioni vengono raggruppate quando i giorni si sovrappongono o una inizia quando finisce l’altra.

Il viaggio appare come una sola fascia che copre tutti i suoi giorni. Aprilo per vedere ogni prenotazione in ordine cronologico, con orari, indirizzo, codice di prenotazione e posto.

I biglietti per un concerto, una partita, un festival o una conferenza creano un evento, uno per ciascun evento, con il luogo, il codice di prenotazione, il posto e il numero di biglietti. Un secondo ordine per lo stesso evento viene aggiunto allo stesso evento. Un biglietto prenotato dalla tua casella di lavoro è contrassegnato come Lavoro, altrimenti come Personale. I biglietti per un evento durante un viaggio vengono aggiunti al viaggio.

Per un viaggio futuro, la tua Machine segnala cosa manca, per esempio **Nessun alloggio prenotato per 2 notti**, oppure che non hai prenotato il trasporto dall’aeroporto all’hotel. Queste righe sono attenuate e contrassegnate con **Nessuna prenotazione**. Se un viaggio non include alcun soggiorno, non vengono mostrati avvisi sulle notti.

- Ogni riga indica da chi proviene la prenotazione, per esempio **Da Example Tickets**, e apre l’email corrispondente.
- Se dall’email è stata creata un’attività, per esempio per pagare i biglietti, **Apri l’attività** la mostra.
- Se una prenotazione cambia, la relativa riga viene aggiornata; se viene annullata, la riga scompare. Quando tutte le prenotazioni sono annullate, scompare anche il viaggio o l’evento.
- Una prenotazione per un’altra persona, come il volo di un collega che ti è stato inoltrato, non compare nei tuoi viaggi.

La maggior parte delle email di conferma contiene i dettagli in un formato che la tua Machine può leggere senza IA. Se un’email non è in un formato di questo tipo, per esempio perché è stata inoltrata o proviene da un piccolo sito di prenotazioni, il tuo [modello](model.md) la legge in background, poche email alla volta, e si ferma quando sei vicino al limite di utilizzo. Quando la cronologia è disponibile, in background vengono lette anche le email di prenotazione dell’anno incluso nella [cronologia](history.md) conservata dalla tua Machine.

## Note e trascrizione delle riunioni

I dettagli di una riunione si dividono in due parti. **Note** è il riepilogo, con decisioni e azioni da svolgere. **Trascrizione** riporta parola per parola ciò che è stato detto. Inizialmente è chiusa e ne viene mostrata la durata; **Mostra** la apre.

Se le note o la trascrizione non si caricano, la pagina riprova automaticamente per circa mezzo minuto. Poi tocca **Riprova**.

Ognuna ha i propri comandi **Aggiungi note** o **Aggiungi trascrizione**, **Carica file** per caricare un file Markdown o di testo, **Modifica** e **Rimuovi** (tocca due volte). Il contenuto aggiunto a una sezione resta lì. In una riunione che puoi modificare, seleziona **Note** sotto il modulo per aprirle.

Se hai collegato [Zoom](zoom.md), [Google Meet](google-meet.md) o [Granola](granola.md), le relative note compaiono in Note e la trascrizione in Trascrizione, contrassegnate con **Da Zoom**, **Da Google Meet** o **Da Granola**. Non sostituiscono mai ciò che hai aggiunto: se sono presenti entrambi, vengono mostrati entrambi.

Puoi aggiungere note anche all’evento della riunione nel calendario, dopo che è iniziata, oppure riceverle via email da Zoom o Gemini. Dopo la riunione, The Machine crea attività dalle note solo per i passaggi successivi ben definiti. Se le stesse note arrivano in due modi, viene creata una sola attività, con la riunione come origine: «Origine: note di» seguito dalla riunione.

Una riunione con una trascrizione ma senza note mostra **Genera note**. The Machine le crea a partire dalla trascrizione: un breve riepilogo, le decisioni e le azioni da svolgere con i nomi di chi se ne occupa, nella lingua della riunione.

Viene mostrato **Sto scrivendo le note…** e la stesura continua anche se chiudi la riunione. Per una riunione lunga possono servire alcuni minuti e viene usato il tuo modello. Le note sono contrassegnate con **Scritte da The Machine** e non sostituiscono quelle che hai aggiunto.

Anche la tua assistente può aggiungere note e trascrizioni. Chiedile, in un’attività, per esempio «aggiungi la trascrizione alla riunione di oggi con il team». La trascrizione viene aggiunta a Trascrizione e il riepilogo a Note. Nel Calendario, le riunioni con note o trascrizioni mostrano **Note** o **Trascrizione**.

The Machine usa entrambe per trovare i passaggi successivi della riunione. Sono contrassegnati come Lavoro o Personale in base alla riunione e vengono condivisi con il team solo se lo è anche la riunione.

Puoi aprire i dettagli di una riunione ovunque la trovi: nella cronologia, nei risultati di una ricerca nei messaggi o come origine di un’attività. **Invito originale** in fondo mostra l’invito ricevuto.

## Aggiungere o modificare un evento

Puoi modificare il tuo calendario Google da qui. Outlook e gli altri calendari sono solo consultabili. **Nuovo evento** ne aggiunge uno (sul telefono si trova sotto **+** nella barra superiore): scegli il calendario, un titolo e l’orario. Seleziona un evento senza ospiti in quel calendario per modificarlo o **Elimina** per cancellarlo (tocca due volte).

**Dove** suggerisce luoghi mentre scrivi: prima quelli che hai già usato e le tue organizzazioni, poi gli indirizzi di [OpenStreetMap](https://www.openstreetmap.org), una mappa gratuita. Per cercarli vengono inviate solo le parole che scrivi. Scegli un suggerimento o lascia il testo che hai inserito.

**Invita** aggiunge persone da Graph o qualsiasi indirizzo email. L’opzione è disponibile solo nel tuo calendario. Le persone che riceveranno un invito sono elencate sopra il pulsante, che indica anche quante sono: **Aggiungi e invita 2**. Google invia gli inviti quando tocchi il pulsante, non prima. Se non ci sono ospiti, nessuno riceve un invito o un aggiornamento.

Un’attività può anche proporti una modifica, per esempio aggiungere un ritiro. Mostra esattamente cosa cambierà e la modifica viene applicata solo quando selezioni **Aggiungi**, **Salva** o **Elimina**.

Non hai ancora riunioni? Se non hai collegato un calendario, **Collega il tuo calendario** apre Connessioni. Puoi collegare [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) o [un altro calendario](other-calendars.md).

## Conflitti con l’altro calendario

Quando una riunione di lavoro si sovrappone a un evento nel calendario personale, o viceversa, The Machine crea un’attività relativa a quello dei due che è stato aggiunto più di recente. Può preparare un breve messaggio per spostarlo o proporti di rifiutarlo. Non viene inviato nulla finché non approvi.

Se un evento si sovrappone a più eventi, viene creata una sola attività relativa a quell’evento. Se ne sovrappone uno nuovo mentre l’attività è aperta, viene aggiunto alla stessa. Quando l’attività è completata o scartata, il conflitto viene segnalato di nuovo solo se una riunione viene creata o modificata in seguito.

Gli eventi di un’intera giornata, quelli con stato «Disponibile» e quelli provvisori non vengono considerati; ogni conflitto viene segnalato una sola volta. Non vengono considerati nemmeno la sede di lavoro, il tempo di concentrazione e l’assenza dall’ufficio impostati in Google. Non viene considerato neanche un blocco creato da te che include altre riunioni, come una giornata in ufficio: possono creare conflitti solo le riunioni al suo interno. Un blocco senza altre persone e senza riunioni, come un volo, può comunque entrare in conflitto con un evento a cui partecipano altre persone.

Un’attività di lavoro segnala solo che c’è un conflitto, così il team non vede mai l’evento personale. Solo tu puoi vedere con cosa è in conflitto: i primi due eventi, poi il numero di quelli rimanenti. Un’attività su cui non hai fatto nulla si chiude automaticamente se il suo conflitto è già segnalato in un’altra attività o se in realtà non c’era alcun conflitto.

## Preparati alle riunioni

Prima di una riunione con persone esterne alla tua azienda, The Machine crea un’attività: **Preparati per** la riunione. È un breve briefing:

- **Chi:** chi sono, in base alle informazioni di Graph, con dettagli sul loro percorso se disponibili.
- **Organizzazione:** di cosa si occupa la loro azienda, per chi e a quale prezzo, se è rilevante per la riunione.
- **Finora:** di cosa avete parlato, cosa avete chiesto e proposto e a che punto siete. Dopo la riunione, i messaggi diventano le fonti dell’attività.
- **Concordato in precedenza:**, **Modificato da allora:** e **Ancora aperto:** i risultati delle riunioni precedenti con le stesse persone, con una riga per ciascun punto e la riunione o il messaggio da cui proviene.
- **Promesse aperte:** ciò che tu o le altre persone dovete ancora fare, in base alle promesse sulla tua Machine.
- **Domande aperte:** ciò che è ancora senza risposta.
- **Da decidere o portare:** cosa definire o portare con te e cosa probabilmente interessa alle altre persone.

Il briefing arriva la mattina di un giorno lavorativo: il giorno stesso se la riunione è nel pomeriggio, altrimenti il giorno lavorativo precedente. È da leggere: quando l’hai letto, seleziona **Fatto**. Se contiene una promessa o una domanda che richiede un’azione, questa ha una sua attività.

Fai domande sulla riunione nella sua chat o aggiungi quello che sai. The Machine ti risponde o integra la tua nota nel briefing, per esempio in **Da decidere o portare**, e ne tiene conto. Dal briefing non viene inviato nulla.

Le riunioni precedenti vengono considerate se hanno avuto la partecipazione di una persona esterna in entrambi i casi, indipendentemente dal nome della riunione e dall’indirizzo usato. La tua Machine legge le note disponibili: le tue, quelle dell’app per le riunioni o quelle inviate via email. Se non ci sono, legge la trascrizione o le note nell’evento del calendario. Le note più recenti hanno più peso e un punto risolto in seguito non viene mostrato come ancora aperto.

Vengono considerate anche le note e i messaggi della [Cronologia](history.md), così il briefing può includere riunioni precedenti al tuo inizio.

Un briefing di lavoro non legge note personali né contenuti dalla Machine di qualcun altro. Il testo resta con te: il briefing non viene incluso in un passaggio e non può essere inviato per la revisione. Se non ci sono note, queste sezioni non vengono mostrate.

Il briefing usa le informazioni già presenti sulla tua Machine. Per la prima riunione con una persona di un’azienda, legge anche la pagina iniziale del sito dell’azienda.

Inoltre, cerca brevemente sul web il nome della persona e dell’azienda. Su una Machine ospitata, la ricerca usa il tuo account ChatGPT o Claude e consuma una piccola parte del relativo piano. Sul tuo computer usa il provider di ricerca configurato in OpenClaw oppure il tuo account, se attivi questa opzione (`meeting_prep_signin_search` in `config.json`). Se hai configurato un provider, viene sempre usato per primo.

Per la ricerca vengono usati solo il nome pubblico della persona, il nome dell’azienda e il suo sito web, mai i tuoi messaggi. I risultati includono un link e vengono riutilizzati per 30 giorni. Su ChatGPT, il modello indica il link, ma nessuno ne verifica il contenuto: aprilo prima di fidarti delle informazioni. La chat dell’attività mostra **Ha cercato sul web**.

Così, per una prima riunione che hai accettato, puoi ricevere un briefing prima ancora di aver scambiato una parola: cosa fa l’azienda, cosa significa per te e, se disponibili, chi sono i partecipanti. Se hai solo un nome, la ricerca viene conservata solo se individua una sola persona. Se **Cerca i contatti di lavoro** è disattivato (Impostazioni, Sicurezza), non vengono cercati né contatti né informazioni sul web.

Una riunione ricorrente riceve un briefing solo se ci sono novità dall’ultima volta: un messaggio, delle note o una promessa. Il briefing segnala le novità, non ripete quello precedente. Arriva dopo la fine dell’incontro precedente e al massimo per due riunioni ricorrenti al giorno.

Una riunione solo con il tuo team riceve un briefing solo se le note precedenti della stessa serie (o con lo stesso titolo e la partecipazione di almeno una delle stesse persone) contengono un punto che ti riguarda: un’azione da svolgere, una domanda rivolta a te, una decisione ancora da prendere o una promessa che hai fatto. Le azioni che spettano solo ai colleghi non generano un briefing. Non vengono cercate informazioni sui tuoi colleghi e il briefing arriva, se possibile, la mattina della riunione.

Se non c’è nulla di utile da segnalare, non viene creata alcuna attività. Le riunioni personali e quelle rifiutate non ne ricevono una. Se una riunione viene spostata, conserva la stessa attività al nuovo orario. Un’attività scartata non ricompare e quella di una riunione annullata si chiude automaticamente.

Se un aggiornamento modifica il contenuto di un briefing, quelli aperti per le riunioni future vengono riscritti una sola volta con le nuove informazioni. Titolo, fonti e posizione nell’elenco non cambiano. Un briefing che hai modificato, posticipato o chiuso resta com’è; lo stesso vale per quello relativo a una riunione che inizia entro pochi minuti.

Nei dettagli della riunione, la relativa attività compare sotto **Attività** e puoi aprirla con un tocco per passare alla chat.
