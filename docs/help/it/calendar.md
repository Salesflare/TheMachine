---
title: Calendario
area: calendar
summary: La settimana che ti aspetta, tutta in un unico posto: riunioni, attività in scadenza, attività posticipate e promesse.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 479aa9c3fadda8bd
---
## Cosa mostra

I tuoi giorni a partire da oggi, con:

- le riunioni dei calendari che hai collegato,
- le attività in scadenza quel giorno e quelle posticipate, nel giorno in cui tornano,
- i promemoria sulle attività che hai passato ad altri,
- le promesse con una data,
- [viaggi ed eventi](calendar.md#trips-and-events) ricavati dalle prenotazioni e dai biglietti nella tua posta.

Una riunione presente in due calendari viene mostrata una sola volta. Se qualcuno ha condiviso un calendario con te, i suoi eventi sono attenuati e accompagnati dal suo nome; non generano mai un’attività. Gli eventi che durano tutto il giorno o più giorni sono mostrati come eventi di un’intera giornata, per ogni giorno che coprono. In Agenda, un viaggio compare per primo in ognuno dei suoi giorni; in Settimana e Mese è rappresentato da un’unica fascia che li attraversa, ad esempio «Viaggio a Lisbona».

Un piano concordato insieme è una sola promessa, indicata con «Con» e il nome dell’altra persona. Se una promessa riguarda una riunione di quel giorno con la stessa persona, compare nella riga della riunione.

**In ritardo** viene mostrato per primo. Una riunione con un’attività ancora aperta mostra il suo stato: **Preparazione pronta**, **In preparazione** o **Attività**. Un’attività che sembra completata, perché hai già risposto o perché la sua esecuzione l’ha trovata completata, non compare come **Scadenza**.

## Agenda, settimana o mese

- **Agenda** elenca i giorni uno dopo l’altro. Scorri verso il basso per vedere i giorni successivi o verso l’alto (oppure seleziona **Mostra giorni precedenti**) per quelli passati. Torna indietro fino a una settimana prima di quando hai collegato il calendario e mostra in alto da quale giorno parte. Quando è disponibile la [cronologia](history.md), torna indietro di circa un anno.
- **Settimana** mostra una griglia da lunedì a domenica. Sul telefono mostra tre giorni.
- **Mese** mostra il mese intero. Sul computer mostra fino a tre elementi al giorno; sul telefono mostra dei puntini. Tocca un giorno per vedere l’elenco dei suoi eventi.

**Oggi**, ‹ e › in alto ti permettono di spostarti tra le settimane o i mesi. La visualizzazione scelta viene salvata su quel dispositivo.

Nella griglia settimanale, gli eventi che si svolgono alla stessa ora sono affiancati, ma restano leggibili. Gli altri sono raccolti sotto **+N**: selezionalo per aprire quel giorno nell’Agenda.

## Aprire un elemento

Seleziona una riga per aprire la chat dell’attività, la promessa, il viaggio o l’evento, oppure la riunione. Se non puoi modificare una riunione da qui, ad esempio perché appartiene a un’altra persona o ha degli invitati, ne vedrai i dettagli: quando si svolge, dove e chi partecipa. Le persone che il tuo Graph conosce, le organizzazioni e i progetti a cui è collegata la riunione rimandano alle rispettive pagine. Seleziona **Apri in Google Calendar** (o **Apri in Outlook**) sotto questi elementi per aprire la riunione lì. Aprirla non modifica nulla.

Una sala riunioni prenotata per una riunione compare sotto il luogo, mai come persona o nel tuo Graph.

Il link a una riunione mostra il servizio corrispondente, ad esempio Zoom, Google Meet o Teams, oppure **Videochiamata**. Apri la riunione per partecipare.

## Viaggi ed eventi

Quando nella tua posta arriva una prenotazione per un volo, un hotel, una casa vacanze, un treno, un autobus, un traghetto, un’auto a noleggio, un taxi o un parcheggio in aeroporto, la tua Machine la aggiunge a un viaggio. Le prenotazioni dello stesso itinerario vengono raggruppate in un unico viaggio, da qualsiasi casella di posta provengano: il treno per l’aeroporto, i voli, l’auto, il soggiorno e il viaggio di ritorno. Le prenotazioni vengono raggruppate quando i loro giorni si sovrappongono o quando una inizia dove finisce l’altra.

Il viaggio viene mostrato come un’unica fascia che attraversa i suoi giorni. Aprilo per vedere tutte le prenotazioni in ordine cronologico, con orari, indirizzo, codice di prenotazione e posto.

I biglietti per un concerto, una partita, un festival o una conferenza creano un evento, uno per ogni occasione, con il luogo, il codice di prenotazione, il posto e il numero di biglietti. Un secondo ordine per lo stesso evento viene aggiunto allo stesso elemento. Un evento prenotato dalla tua casella di lavoro è di Lavoro, altrimenti è Personale. I biglietti per qualcosa che si svolge durante un viaggio vengono aggiunti al viaggio.

Per un viaggio ancora da fare, la tua Machine indica cosa manca, ad esempio **Nessun alloggio prenotato per 2 notti** o nessuna prenotazione dall’aeroporto all’hotel. Queste righe sono attenuate e contrassegnate con **Nessuna prenotazione**. Se per un viaggio non hai prenotato alcun soggiorno, non viene indicato nulla sulle notti.

- Ogni riga indica da chi proviene la prenotazione, ad esempio **Da Example Tickets**, e apre l’email corrispondente.
- Se dall’email è stata creata un’attività, ad esempio per pagare i biglietti, seleziona **Apri l’attività** per visualizzarla.
- Se una prenotazione cambia, la sua riga viene aggiornata; se viene annullata, viene rimossa. Quando tutte le prenotazioni sono annullate, viene rimosso anche il viaggio o l’evento.
- Una prenotazione per un’altra persona, ad esempio il volo di un collega inoltrato a te, non viene aggiunta ai tuoi viaggi.

La maggior parte delle conferme contiene i dettagli in un formato che la tua Machine può leggere senza IA. Se non è così, ad esempio per un’email inoltrata o un piccolo sito di prenotazioni, il tuo [modello](model.md) legge l’email in background, poche alla volta, e aspetta se sei vicino al limite di utilizzo. Le email di prenotazione dell’anno coperto dalla [cronologia](history.md) che la tua Machine conserva vengono lette in background quando la cronologia è disponibile.

## Note e trascrizione della riunione

I dettagli di una riunione sono divisi in due parti. **Note** è il riepilogo, con decisioni e attività da svolgere. **Trascrizione** riporta parola per parola quello che è stato detto. All’inizio è chiusa e ne viene mostrata la durata; seleziona **Mostra** per aprirla.

Se non si caricano, la riunione riprova automaticamente per circa mezzo minuto. Dopodiché, tocca **Riprova**.

Per ognuna puoi usare **Aggiungi note** o **Aggiungi trascrizione**, **Carica file** per caricare un file Markdown o di testo, **Modifica** e **Rimuovi** (tocca due volte). I contenuti di una sezione restano al suo interno. In una riunione che puoi modificare, seleziona **Note** sotto il modulo per aprirle.

Se hai collegato [Zoom](zoom.md), [Google Meet](google-meet.md) o [Granola](granola.md), le note del servizio compaiono in Note e la trascrizione in Trascrizione, con l’etichetta **Da Zoom**, **Da Google Meet** o **Da Granola**. Non sostituiscono mai quello che hai aggiunto tu: se ci sono entrambi, vengono mostrati entrambi.

Le note possono arrivare anche dall’evento della riunione nel calendario, se aggiunte dopo l’inizio, o via email da Zoom o Gemini. Dopo la riunione, The Machine crea attività da queste note solo per i prossimi passi chiari. Se le stesse note arrivano da due fonti, viene creata una sola attività, associata alla riunione come fonte: «Fonte: note di» seguito dalla riunione.

Se una riunione ha una trascrizione ma non delle note, puoi selezionare **Genera note**. The Machine le prepara a partire dalla trascrizione: un breve riepilogo, le decisioni e le attività da svolgere con i rispettivi responsabili, nella lingua della riunione.

Viene mostrato **Sto scrivendo le note…** e la scrittura continua anche se chiudi la riunione. Per una riunione lunga possono servire alcuni minuti; viene usato il tuo modello. Le note riportano **Scritto da The Machine** e non sostituiscono mai quelle che hai aggiunto tu.

Puoi chiedere alla tua Machine di aggiungerle. Per esempio, chiedi in un’attività: «Aggiungi la trascrizione della riunione di oggi del team». La trascrizione viene aggiunta in Trascrizione e il riepilogo in Note. Nel Calendario, le riunioni con note o trascrizione mostrano **Note** o **Trascrizione**.

La tua Machine legge entrambe per trovare le attività da seguire. Sono di Lavoro o Personali come la riunione e vengono condivise con il tuo team solo se lo è anche la riunione.

Puoi aprire i dettagli della riunione ovunque la trovi: nella cronologia, nei risultati di una ricerca nei messaggi o come fonte di un’attività. **Invito originale** in fondo mostra l’invito così come è arrivato.

## Aggiungere o modificare un evento

Puoi modificare da qui il tuo calendario Google. Outlook e gli altri calendari sono solo consultabili. **Nuovo evento** ne crea uno (sul telefono, si trova sotto **+** nella barra in alto): scegli il calendario, un titolo e l’orario. Seleziona un evento senza invitati nel tuo calendario per modificarlo oppure **Elimina** per cancellarlo (tocca due volte).

**Dove** suggerisce dei luoghi mentre scrivi: prima quelli che hai già usato e le tue organizzazioni, poi gli indirizzi da [OpenStreetMap](https://www.openstreetmap.org), una mappa gratuita. Per cercarli vengono inviate solo le parole che scrivi. Scegli un suggerimento o lascia il testo che hai inserito.

**Invita** aggiunge persone dal tuo Graph o qualsiasi indirizzo email. Questa opzione è disponibile solo nel tuo calendario. Gli invitati sono elencati sopra il pulsante, che mostra anche quanti sono: **Aggiungi e invita 2**. Google invia gli inviti quando tocchi il pulsante, non prima. Se non ci sono invitati, nessuno riceve un invito o un aggiornamento.

Anche un’attività può proporti una modifica, ad esempio aggiungere un ritiro. Ti mostra esattamente cosa cambierà e la modifica viene applicata solo se selezioni **Aggiungi**, **Salva** o **Elimina**.

Non hai ancora riunioni? Se non hai collegato un calendario, seleziona **Collega il tuo calendario** per aprire Connessioni e collegare [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) o [un altro calendario](other-calendars.md).

## Sovrapposizioni con l’altro calendario

Quando una riunione di lavoro si sovrappone a qualcosa nel tuo calendario personale, o viceversa, The Machine crea un’attività per quella più recente. Può preparare un breve messaggio per spostarla o proporti di rifiutarla. Non viene inviato nulla finché non approvi.

Se un evento si sovrappone a più elementi, viene creata un’unica attività per quell’evento. Se si verifica una nuova sovrapposizione mentre è ancora aperta, viene aggiunta alla stessa attività. Una volta completata o scartata, può essere riproposta solo da una riunione creata o modificata in seguito.

Gli eventi di un’intera giornata, quelli con stato Libero e quelli provvisori non vengono considerati; ogni sovrapposizione viene segnalata una sola volta. Non vengono considerati nemmeno il luogo di lavoro, il tempo di concentrazione e l’assenza dall’ufficio impostati in Google. Lo stesso vale per un blocco creato da te che contiene altre riunioni, come una giornata in ufficio: possono sovrapporsi solo le riunioni al suo interno. Un blocco senza altre persone e senza riunioni, come un volo, può comunque sovrapporsi a un evento con altre persone.

Un’attività di Lavoro segnala solo la presenza di un conflitto, quindi il tuo team non vede mai l’evento personale. Solo tu puoi vedere con cosa si sovrappone: vengono mostrati i primi due elementi e poi il numero degli altri. Un’attività su cui non hai fatto nulla si chiude automaticamente quando la sovrapposizione è già inclusa in un’altra attività o non esisteva davvero.

## Prepararsi alle riunioni

Prima di una riunione con persone esterne alla tua azienda, The Machine crea un’attività: **Preparati per** la riunione. È un breve riepilogo:

- **Chi:** chi sono, in base al tuo Graph, con alcune informazioni sul loro passato quando disponibili.
- **Organizzazione:** di cosa si occupa la loro azienda, per chi e a quale prezzo, quando è utile saperlo per la riunione.
- **Finora:** cosa avete discusso, chiesto e proposto, e a che punto siete. Dopo la riunione, quei messaggi diventano fonti dell’attività.
- **Concordato in precedenza:**, **Modifiche da allora:** e **Ancora aperto:** cosa è emerso nelle riunioni precedenti con le stesse persone, con una riga per ogni punto e un link alla riunione o al messaggio da cui proviene.
- **Promesse aperte:** cosa tu o loro dovete ancora fare, in base alle promesse sulla tua Machine.
- **Questioni aperte:** cosa è ancora senza risposta.
- **Da decidere o portare:** cosa definire o portare con te e cosa probabilmente sarà importante per loro.

L’attività compare la mattina di un giorno lavorativo: il giorno della riunione se si svolge nel pomeriggio, altrimenti il giorno lavorativo precedente. È pensata per essere letta: quando l’hai letta, seleziona **Fatto**. Le promesse o le domande che richiedono un’azione hanno una propria attività.

Fai una domanda sulla riunione nella sua chat o aggiungi quello che sai. La Machine ti risponde oppure integra le tue informazioni nel riepilogo, ad esempio in **Da decidere o portare**, e ne tiene conto. Dal riepilogo non viene inviato nulla.

Vengono considerate le riunioni precedenti a cui ha partecipato una persona esterna, indipendentemente dal nome della riunione e dall’indirizzo usato. La tua Machine legge le note disponibili: le tue, quelle dell’app per riunioni o quelle che ti ha inviato via email. Se non ci sono, usa la trascrizione o le note dell’evento nel calendario. Le più recenti contano di più e un punto risolto in seguito non viene mostrato come ancora aperto.

Vengono considerate anche le note e i messaggi della [Cronologia](history.md), così il riepilogo include le riunioni precedenti all’inizio del tuo utilizzo.

Un riepilogo di Lavoro non legge note personali né contenuti della Machine di qualcun altro. Il testo resta a tua disposizione: non viene incluso in un passaggio e non può essere inviato per una revisione. Se non ci sono note, queste sezioni non vengono mostrate.

La tua Machine usa le informazioni già presenti sulla Machine. Per una prima riunione con una persona di un’azienda, consulta anche la home page del sito dell’azienda.

Se hai configurato la ricerca sul web sulla tua Machine, cerca anche brevemente il nome della persona e dell’azienda. Una Machine ospitata non include questa funzione; sul tuo computer puoi configurarla in OpenClaw. I risultati includono un link. Per la ricerca vengono usati solo il nome pubblico della persona, il nome dell’azienda e il suo sito web, mai i tuoi messaggi. I risultati vengono riutilizzati per 30 giorni.

Così, una riunione a cui hai accettato di partecipare può avere un riepilogo prima ancora che tu abbia scambiato una parola con gli altri: di cosa si occupa la loro azienda, cosa significa per te e, quando è possibile saperlo, chi sono. Se hai solo un nome, conserva i risultati della ricerca solo quando identificano una persona precisa. Se **Cerca i contatti di lavoro** è disattivato (Impostazioni, Sicurezza), non viene effettuata alcuna ricerca.

Una riunione ricorrente riceve un riepilogo solo se c’è qualcosa di nuovo dall’ultima volta: un messaggio, delle note o una promessa. Il riepilogo indica le novità, non ripete quello precedente. Viene creato quando è finita la riunione precedente, per un massimo di due riunioni ricorrenti al giorno.

Se non c’è nulla di utile da dire, non viene creata un’attività. Le riunioni interne, personali o rifiutate non ne ricevono una. Se una riunione viene spostata, la sua attività resta la stessa e viene aggiornata all’orario nuovo. Un’attività scartata non ricompare e quella di una riunione annullata si chiude automaticamente.

Se un aggiornamento modifica il contenuto del riepilogo, quelli delle riunioni future ancora aperti vengono riscritti una sola volta con le nuove informazioni. Titolo, fonti e posizione nell’elenco restano invariati. Un riepilogo che hai modificato, posticipato o chiuso non cambia; lo stesso vale per quello di una riunione che inizia nei prossimi minuti.

Nei dettagli della riunione trovi la relativa attività sotto **Attività**, a un tocco dalla sua chat.
