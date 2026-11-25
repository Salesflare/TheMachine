---
title: Calendario
area: calendar
summary: La settimana che ti aspetta, in un unico posto: riunioni, attività in scadenza, attività posticipate e promesse.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 9b7475608bb04e5c
---
## Cosa mostra

I tuoi giorni a partire da oggi, con:

- le riunioni dei calendari che hai collegato,
- le attività in scadenza quel giorno e quelle posticipate nel giorno in cui ricompaiono,
- i promemoria sulle attività che hai passato ad altri,
- le promesse con una data,
- [viaggi ed eventi](calendar.md#trips-and-events) presi dalle email di prenotazioni e biglietti.

Una riunione presente in due calendari viene mostrata una sola volta. Un calendario condiviso con te mostra gli eventi di chi l’ha condiviso in tono attenuato, con il suo nome; questi eventi non generano mai un’attività. Gli eventi di un’intera giornata e quelli di più giorni sono indicati come eventi di un’intera giornata, in ciascun giorno interessato. In Agenda, un viaggio compare per primo in ciascuno dei suoi giorni; in Settimana e Mese, appare come una fascia che si estende per tutti i giorni del viaggio, per esempio «Viaggio a Lisbona».

Un programma concordato insieme è una sola promessa, indicata con «Con» e il nome dell’altra persona. Una promessa relativa a una riunione di quel giorno con la stessa persona compare nella riga della riunione.

**In ritardo** compare per primo. Una riunione con un’attività aperta mostra il relativo stato: **Preparazione pronta**, **In preparazione** o **Attività**. Un’attività che sembra completata, perché hai già risposto o perché la sua esecuzione l’ha trovata completata, non viene mostrata come **Scadenza**.

## Agenda, settimana o mese

- **Agenda** mostra un giorno alla volta. Scorri verso il basso per i giorni successivi o verso l’alto, oppure tocca **Mostra giorni precedenti**, per vedere i giorni passati. Risale fino a una settimana prima di quando hai collegato il calendario e in cima indica da quale giorno parte. Una volta caricata la [cronologia](history.md), risale a circa un anno fa.
- **Settimana** mostra una griglia dal lunedì alla domenica. Sul telefono mostra tre giorni.
- **Mese** mostra l’intero mese. Su computer mostra fino a tre elementi al giorno; sul telefono mostra dei punti e, toccandoli, elenca gli elementi di quel giorno.

**Oggi**, ‹ e › in alto ti permettono di passare da una settimana o da un mese all’altro. La vista scelta viene ricordata su quel dispositivo.

Nella griglia settimanale, gli eventi che si svolgono alla stessa ora appaiono affiancati e restano leggibili. Gli altri sono indicati con **+N**: toccandolo, si apre quel giorno nell’agenda.

## Aprire un elemento

Fai clic su una riga per aprire la chat dell’attività, la promessa, il viaggio o l’evento, oppure la riunione. Per una riunione che non puoi modificare qui, per esempio perché è di un’altra persona o include ospiti, vengono mostrati i dettagli: quando, dove e chi. Le persone che Graph conosce, le organizzazioni e i progetti della riunione sono link alle rispettive pagine. **Apri in Google Calendar** (o **Apri in Outlook**) sotto i dettagli apre la riunione nel relativo calendario. Consultarla non cambia nulla.

Una sala riunioni prenotata per una riunione compare sotto «Dove», mai come persona o in Graph.

Il link a una riunione mostra il servizio, per esempio Zoom, Google Meet o Teams, oppure **Videochiamata**. Apri la riunione per partecipare.

## Viaggi ed eventi

Quando nella tua posta arriva una prenotazione di un volo, un hotel, una casa vacanze, un treno, un autobus, un traghetto, un’auto a noleggio, un taxi o un parcheggio in aeroporto, la tua Machine la aggiunge a un viaggio. Le prenotazioni dello stesso itinerario vengono raggruppate in un unico viaggio, da qualsiasi casella di posta: il treno per l’aeroporto, i voli, l’auto, il soggiorno e il viaggio di ritorno. Le prenotazioni vengono raggruppate quando i giorni si sovrappongono o una inizia quando finisce l’altra.

Il viaggio appare come una fascia che si estende per tutti i suoi giorni. Aprilo per vedere ogni prenotazione in ordine cronologico, con orari, indirizzo, codice di prenotazione e posto.

I biglietti per un concerto, una partita, un festival o una conferenza creano un evento, uno per ciascun evento, con il luogo, il codice di prenotazione, il posto e il numero di biglietti. Un secondo ordine per lo stesso evento viene aggiunto allo stesso evento. Un biglietto prenotato con la casella di lavoro è di lavoro, altrimenti è personale. I biglietti per qualcosa che si svolge durante un viaggio vengono aggiunti al viaggio.

Per un viaggio futuro, la tua Machine segnala cosa manca, per esempio **Nessun alloggio prenotato per 2 notti** o nessuna prenotazione dall’aeroporto al tuo hotel. Queste righe sono in tono attenuato e contrassegnate con **Nessuna prenotazione**. Se un viaggio non include alcun pernottamento, non vengono segnalate notti mancanti.

- Ogni riga indica da chi proviene la prenotazione, per esempio **Da Example Tickets**, e apre la relativa email.
- Se dall’email è stata creata un’attività, per esempio per pagare i biglietti, **Apri l’attività** la mostra.
- Se una prenotazione cambia, la relativa riga viene aggiornata; se viene annullata, viene rimossa. Quando tutte le prenotazioni sono annullate, viene rimosso anche il viaggio o l’evento.
- Una prenotazione per qualcun altro, per esempio il volo di una persona del tuo team inoltrato a te, non viene aggiunta ai tuoi viaggi.

La maggior parte delle conferme contiene i dettagli in un formato che la tua Machine può leggere senza IA. Per le altre, per esempio un’email inoltrata o una prenotazione di un piccolo sito, il tuo [modello](model.md) legge l’email in background, poche alla volta, e aspetta se sei vicino al limite di utilizzo. Le email di prenotazione dell’anno incluso nella [cronologia](history.md) vengono lette in background una volta caricata la cronologia.

## Note e trascrizione della riunione

I dettagli di una riunione hanno due parti. **Note** è il riepilogo: decisioni e attività da svolgere. **Trascrizione** riporta parola per parola ciò che è stato detto. All’inizio è chiusa e indica la durata; tocca **Mostra** per aprirla.

Se non si caricano, la riunione riprova automaticamente per circa mezzo minuto. Dopo, tocca **Riprova**.

Per ciascuna parte puoi usare **Aggiungi note** o **Aggiungi trascrizione**, **Carica file** per un file Markdown o di testo, **Modifica** e **Rimuovi** (tocca due volte). Il contenuto di una parte resta lì. In una riunione che puoi modificare, **Note** sotto il modulo apre le note.

Se hai collegato [Zoom](zoom.md), [Google Meet](google-meet.md) o [Granola](granola.md), le relative note compaiono in Note e la trascrizione in Trascrizione, con l’indicazione **Da Zoom**, **Da Google Meet** o **Da Granola**. Non sostituiscono mai ciò che hai aggiunto: se sono presenti entrambi, vengono mostrati entrambi.

Le note possono essere aggiunte anche all’evento della riunione nel calendario, dopo il suo inizio, oppure inviate via email da Zoom o Gemini. Quando la riunione è terminata, The Machine crea attività dalle note solo per i passaggi successivi chiari. Se le stesse note arrivano in due modi, viene creata una sola attività, con la riunione come fonte: «Fonte: note di» seguito dal nome della riunione.

Una riunione con una trascrizione ma senza note mostra **Genera note**. The Machine le scrive a partire dalla trascrizione: un breve riepilogo, le decisioni e le attività da svolgere, indicando chi se ne occupa, nella lingua della riunione.

Compare **Sto scrivendo le note…** e l’elaborazione continua anche se chiudi la riunione. Per una riunione lunga possono servire alcuni minuti e viene usato il tuo modello. Le note riportano **Scritte da The Machine** e non sostituiscono mai quelle che hai aggiunto.

Puoi chiedere anche alla tua Machine di aggiungerle. Per esempio, chiedi in una chat di un’attività: «Aggiungi la trascrizione di questa riunione a quella di oggi del team». La trascrizione viene aggiunta in Trascrizione, il riepilogo in Note. Nel Calendario, una riunione che le include mostra **Note** o **Trascrizione**.

La tua Machine legge entrambe per trovare le attività successive alla riunione. Sono di lavoro o personali come la riunione e vengono condivise con il tuo team solo se lo è anche la riunione.

La riunione si apre con questi dettagli da qualsiasi punto: da una cronologia, dai risultati di una ricerca nei messaggi o come fonte di un’attività. **Invito originale** in fondo mostra l’invito così come è arrivato.

## Aggiungere o modificare un evento

Da qui puoi modificare il tuo calendario Google. Outlook e gli altri calendari sono di sola lettura. **Nuovo evento** ne aggiunge uno (sul telefono si trova sotto **+** nella barra in alto): scegli il calendario, un titolo e l’orario. Fai clic su un evento senza ospiti in quel calendario per modificarlo o **Elimina** per cancellarlo (tocca due volte).

**Dove** suggerisce luoghi mentre scrivi: prima quelli che hai già usato e le tue organizzazioni, poi gli indirizzi di [OpenStreetMap](https://www.openstreetmap.org), una mappa gratuita. Per cercarli vengono inviate solo le parole che digiti. Scegline uno o mantieni il testo che hai scritto.

**Invita** aggiunge persone da Graph o qualsiasi indirizzo email. Questa opzione è disponibile solo nel tuo calendario. Prima del pulsante sono elencate le persone che riceveranno un invito e il pulsante indica quante: **Aggiungi e invita 2**. Google invia gli inviti quando tocchi il pulsante, non prima. Se non ci sono ospiti, nessuno riceve un invito o un aggiornamento.

Un’attività può anche proporti una modifica, per esempio aggiungere un luogo di ritiro. Mostra esattamente cosa cambierà: la modifica avviene solo quando tocchi **Aggiungi**, **Salva** o **Elimina**.

Non hai ancora riunioni? Se non hai collegato un calendario, **Collega il tuo calendario** apre Connessioni: collega [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) o [un altro calendario](other-calendars.md).

## Conflitti con l’altro calendario

Se una riunione di lavoro si sovrappone a un evento del tuo calendario personale, o viceversa, The Machine crea un’unica attività sulla più recente delle due. Può preparare una breve nota per spostarla o proporti di rifiutarla. Non viene inviato nulla finché non lo approvi.

Se un evento si sovrappone a più eventi, viene creata un’unica attività relativa a quell’evento. Se si verifica una nuova sovrapposizione mentre l’attività è aperta, viene aggiunta alla stessa attività. Quando l’attività è completata o scartata, ricompare solo se in seguito viene creata o modificata una riunione.

Gli eventi di un’intera giornata, liberi o provvisori non vengono conteggiati e ogni conflitto compare una sola volta. Non vengono conteggiati nemmeno il luogo di lavoro, il tempo di concentrazione e l’assenza dall’ufficio impostati in Google. Lo stesso vale per un blocco del tuo calendario che contiene altre riunioni, per esempio una giornata in ufficio: possono sovrapporsi solo le riunioni al suo interno. Un blocco senza altre persone e senza riunioni, per esempio un volo, può invece sovrapporsi a un evento che include altre persone.

Un’attività di lavoro segnala solo che c’è un conflitto, così il tuo team non vede mai l’evento personale. Solo tu puoi vedere con quale evento si sovrappone: i primi due e poi il numero di quelli restanti. Un’attività su cui non hai fatto nulla si chiude da sola se il conflitto riguarda un’altra attività o se in realtà non c’era.

## Preparazione alle riunioni

Prima di una riunione con persone esterne alla tua azienda, The Machine crea un’attività: **Preparazione per** la riunione. È un breve briefing:

- **Chi:** chi sono, secondo Graph, con qualche informazione sul loro percorso quando disponibile.
- **Organizzazione:** di cosa si occupa la loro azienda, a chi si rivolge e a quale prezzo, se è rilevante per la riunione.
- **Finora:** cosa avete discusso, chiesto e proposto, e a che punto siete. Dopo la riunione, questi messaggi sono le fonti dell’attività.
- **Concordato in precedenza:**, **Cambiato da allora:** e **Ancora aperto:** cosa è emerso dalle riunioni precedenti con le stesse persone. Ogni riga indica la riunione o il messaggio da cui proviene.
- **Promesse ancora aperte:** cosa tu o le altre persone dovete ancora fare, secondo le promesse sulla tua Machine.
- **Questioni aperte:** cosa è ancora senza risposta.
- **Da decidere o portare:** cosa definire o portare con te e cosa probabilmente interesserà agli altri partecipanti.

Arriva la mattina di un giorno lavorativo: il giorno stesso se la riunione è nel pomeriggio, altrimenti il giorno lavorativo precedente. Serve solo per consultare le informazioni: tocca **Fatto** quando le hai lette. Una promessa o una domanda che richiede un’azione ha una propria attività.

Vengono considerate le riunioni precedenti a cui partecipava una persona esterna, indipendentemente dal titolo della riunione e dall’indirizzo usato. La tua Machine legge le note disponibili: le tue, quelle dell’app per riunioni o quelle che ti ha inviato via email; se non ce ne sono, legge la trascrizione o le note nell’evento del calendario. Le note più recenti hanno più peso e un punto risolto in seguito non viene indicato come ancora aperto.

Vengono considerate anche le note e i messaggi della [Cronologia](history.md), così il briefing include le riunioni precedenti a quando hai iniziato a usare la tua Machine.

Un briefing di lavoro non legge note personali né contenuti dalla Machine di un’altra persona. Il testo resta con te: un passaggio ad altri non lo include e non può essere inviato per una revisione. Se non ci sono note, le relative righe non compaiono.

Usa le informazioni già presenti sulla tua Machine. Per una prima riunione con una persona che lavora in un’azienda, legge anche la pagina iniziale del sito dell’azienda.

Se sulla tua Machine è configurata la ricerca sul web, cerca brevemente anche il nome della persona e dell’azienda. Una Machine ospitata non la include; sul tuo computer puoi configurarla in OpenClaw. I risultati includono un link. Alla ricerca vengono inviati solo il nome pubblico della persona, il nome dell’azienda e il sito web, mai i tuoi messaggi. I risultati vengono riutilizzati per 30 giorni.

Così, una prima riunione a cui hai dato conferma può avere un briefing prima ancora che abbiate scambiato una parola: cosa fa l’azienda, cosa significa per te e, se disponibile, chi è la persona. Se hai solo il nome, la ricerca viene usata solo quando indica una sola persona. Se **Cerca i contatti di lavoro** è disattivato (Impostazioni, Sicurezza), non viene cercato nulla.

Una riunione ricorrente genera un briefing solo se c’è qualcosa di nuovo dall’ultima volta: un messaggio, delle note o una promessa. Il briefing indica le novità, non ripete quello precedente. Viene creato dopo la fine della riunione precedente, al massimo per due riunioni ricorrenti al giorno.

Se non ci sono informazioni utili, non viene creata alcuna attività. Le riunioni interne, personali o rifiutate non ne generano. Se una riunione viene spostata, mantiene la stessa attività, con il nuovo orario. Un’attività scartata non ricompare e quella di una riunione annullata si chiude da sola.

Se un aggiornamento modifica le informazioni del briefing, i briefing aperti delle riunioni future vengono riscritti una sola volta nel nuovo formato. Titolo, fonti e posizione nell’elenco restano invariati. Un briefing che hai modificato, posticipato o chiuso resta com’è; lo stesso vale per quello di una riunione che inizia nei prossimi minuti.

I dettagli della riunione mostrano la relativa attività sotto **Attività**, raggiungibile con un tocco dalla sua chat.
