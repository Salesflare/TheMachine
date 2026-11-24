---
title: Calendario
area: calendar
summary: La settimana che ti aspetta, in un unico posto: riunioni, attività in scadenza, attività posticipate e promesse.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: d6f800709c378338
---
## Cosa mostra

Le tue giornate da oggi in poi, con:

- le riunioni dei calendari che hai collegato,
- le attività in scadenza quel giorno e quelle posticipate, nel giorno in cui tornano,
- i promemoria sulle attività che hai passato ad altri,
- le promesse con una data,
- [viaggi ed eventi](calendar.md#trips-and-events) trovati nelle email con prenotazioni e biglietti.

Una riunione presente in due calendari viene mostrata una sola volta. Gli eventi di un calendario condiviso con te sono attenuati e mostrano il nome di chi lo ha condiviso; non generano mai un’attività. Gli eventi di un’intera giornata o di più giorni sono mostrati come eventi di un’intera giornata in ciascun giorno interessato. In Agenda, un viaggio appare per primo in ciascuno dei suoi giorni; in Settimana e Mese, appare come un’unica barra che li attraversa, per esempio «Viaggio a Lisbona».

Un piano fatto insieme è una sola promessa, indicata con «Con» e il nome dell’altra persona. Una promessa relativa a una riunione di quel giorno con la stessa persona appare nella riga della riunione.

**In ritardo** appare per primo. Una riunione con un’attività aperta mostra il suo stato: **Preparazione pronta**, **In preparazione** o **Attività**. Un’attività che sembra completata, perché hai già risposto o perché l’esecuzione ha rilevato che è stata completata, non appare come **Scadenza**.

## Agenda, settimana o mese

- **Agenda** elenca i giorni. Scorri verso il basso per vedere i giorni successivi o verso l’alto, oppure tocca **Mostra giorni precedenti**, per vedere quelli passati. Torna indietro fino a una settimana prima di quando hai collegato il calendario e mostra in alto una riga che indica da quale giorno. Quando è disponibile la [cronologia](history.md), torna indietro di circa un anno.
- **Settimana** mostra una griglia da lunedì a domenica. Sul telefono mostra tre giorni.
- **Mese** mostra tutto il mese. Sul computer mostra fino a tre elementi al giorno; sul telefono mostra dei punti. Tocca un giorno per vedere il suo elenco.

**Oggi**, ‹ e › in alto ti permettono di spostarti tra le settimane o i mesi. La visualizzazione scelta viene ricordata su quel dispositivo.

Nella griglia settimanale, gli eventi alla stessa ora sono affiancati e restano leggibili. Gli altri sono indicati con **+N**. Tocca per aprire quel giorno nell’Agenda.

## Aprire un elemento

Seleziona una riga per aprire la chat dell’attività, la promessa, il viaggio o l’evento oppure la riunione. Una riunione che non puoi modificare qui, per esempio una di un’altra persona o con ospiti, mostra i dettagli: quando, dove e chi partecipa. Le persone conosciute dal tuo Graph e le organizzazioni e i progetti associati alla riunione sono collegamenti alle rispettive pagine. **Apri in Google Calendar** (o **Apri in Outlook**) apre la riunione nel calendario corrispondente. Consultarla non cambia nulla.

Una sala riunioni prenotata per una riunione appare sotto «Dove», mai come persona o nel tuo Graph.

Il link di una riunione mostra il nome del servizio, come Zoom, Google Meet o Teams, oppure **Videochiamata**. Apri la riunione per partecipare.

## Viaggi ed eventi

Quando ricevi un’email con una prenotazione di un volo, hotel, casa vacanze, treno, autobus, traghetto, auto a noleggio, taxi o parcheggio in aeroporto, la tua Machine la aggiunge a un viaggio. Le prenotazioni dello stesso itinerario, anche se arrivano da caselle email diverse, vengono raggruppate in un unico viaggio: il treno per l’aeroporto, i voli, l’auto, il soggiorno e il viaggio di ritorno. Le prenotazioni vengono raggruppate quando i giorni si sovrappongono o quando una termina il giorno in cui inizia la successiva.

Il viaggio appare come un’unica barra che attraversa i suoi giorni. Aprilo per vedere le prenotazioni in ordine cronologico, con orari, indirizzo, codice di prenotazione e posto.

I biglietti per un concerto, una partita, un festival o una conferenza creano un evento, uno per ciascun evento. Mostrano il luogo, il codice di prenotazione, il posto e il numero di biglietti. Un secondo ordine per lo stesso evento viene aggiunto all’evento esistente. Un evento prenotato dalla tua casella di lavoro è indicato come Lavoro, altrimenti come Personale. I biglietti per un evento durante un viaggio vengono aggiunti al viaggio.

Per un viaggio imminente, la tua Machine segnala cosa manca, per esempio **Nessun alloggio prenotato per 2 notti** o nessuna prenotazione dall’aeroporto all’hotel. Queste righe sono attenuate e contrassegnate con **Nessuna prenotazione**. Se il viaggio non include pernottamenti, non vengono mostrate informazioni sulle notti.

- Ogni riga indica da chi proviene la prenotazione, per esempio **Da Example Tickets**, e apre l’email corrispondente.
- Se dall’email è stata creata un’attività, per esempio per pagare i biglietti, **Apri l’attività** la mostra.
- Le modifiche aggiornano la riga della prenotazione; le prenotazioni annullate vengono rimosse. Quando sono state annullate tutte, viene rimosso anche il viaggio o l’evento.
- Le prenotazioni di altre persone, come il volo di un collega inoltrato a te, non vengono aggiunte ai tuoi viaggi.

La maggior parte delle conferme contiene i dettagli in un formato che la tua Machine può leggere senza IA. Per quelle che non lo usano, per esempio un’email inoltrata o proveniente da un piccolo sito di prenotazioni, il tuo [modello](model.md) legge l’email in background, poche alla volta, e aspetta se sei vicino al limite di utilizzo. Una volta disponibile la [cronologia](history.md), la tua Machine legge in background anche le email di prenotazione dell’anno incluso nella cronologia.

## Note e trascrizione della riunione

I dettagli di una riunione sono divisi in due parti. **Note** è il riepilogo, con decisioni e attività da svolgere. **Trascrizione** riporta parola per parola ciò che è stato detto. Inizialmente è chiusa e ne viene mostrata la durata; tocca **Mostra** per aprirla.

Se non si caricano, la riunione riprova automaticamente per circa mezzo minuto. Poi tocca **Riprova**.

Note e trascrizione hanno ciascuna i propri comandi **Aggiungi note** o **Aggiungi trascrizione**, **Carica file** per un file Markdown o di testo, **Modifica** e **Rimuovi** (tocca due volte). Ciò che aggiungi a una sezione resta lì. In una riunione che puoi modificare, tocca **Note** sotto al modulo per aprirle.

Se hai collegato [Zoom](zoom.md), [Google Meet](google-meet.md) o [Granola](granola.md), le note del servizio appaiono in Note e la trascrizione in Trascrizione, con l’indicazione **Da Zoom**, **Da Google Meet** o **Da Granola**. Non sostituiscono mai ciò che hai aggiunto: se sono presenti entrambe le versioni, vengono mostrate tutte e due.

Le note possono anche essere aggiunte all’evento della riunione nel calendario dopo il suo inizio, oppure arrivare via email da Zoom o Gemini. Quando la riunione termina, The Machine crea attività da queste note solo per i passaggi successivi ben definiti. Se le stesse note arrivano in due modi, viene creata una sola attività, che indica la riunione come origine: «Origine: note di» seguito dalla riunione.

Una riunione con una trascrizione ma senza note mostra **Genera note**. The Machine le ricava dalla trascrizione: un breve riepilogo, le decisioni e le attività da svolgere, con l’indicazione di chi se ne occupa. Le note sono nella lingua della riunione.

Appare **Sto scrivendo le note…** e il processo continua anche se chiudi la riunione. Per una riunione lunga possono volerci alcuni minuti; viene usato il tuo modello. Le note riportano **Scritte da The Machine** e non sostituiscono mai quelle che hai aggiunto.

Puoi chiedere anche alla tua Machine di aggiungere le note. Per esempio, chiedi in una chat di un’attività: «aggiungi questa trascrizione alla riunione di oggi del consiglio». La trascrizione viene aggiunta in Trascrizione e il riepilogo in Note. Nel Calendario, una riunione con note o trascrizione mostra **Note** o **Trascrizione**.

The Machine legge entrambe per individuare le attività successive alla riunione. Sono classificate come Lavoro o Personale come la riunione e vengono condivise con il tuo team solo se anche la riunione lo è.

Puoi aprire i dettagli della riunione ovunque la trovi: nella cronologia, nei risultati di una ricerca nei messaggi o come origine di un’attività. **Invito originale** in fondo mostra l’invito così come è arrivato.

## Aggiungere o modificare un evento

Puoi modificare qui il tuo calendario Google. Outlook e gli altri calendari sono di sola lettura. **Nuovo evento** ne aggiunge uno (sul telefono, lo trovi sotto **+** nella barra superiore): scegli il calendario, un titolo e l’orario. Seleziona un evento senza invitati in quel calendario per modificarlo o **Elimina** per cancellarlo (tocca due volte).

**Dove** suggerisce dei luoghi mentre scrivi: prima quelli che hai già usato e le tue organizzazioni, poi gli indirizzi di [OpenStreetMap](https://www.openstreetmap.org), una mappa gratuita. Per cercare vengono inviate solo le parole che scrivi. Scegli un suggerimento o mantieni il testo che hai inserito.

**Invita** aggiunge persone dal tuo Graph o qualsiasi indirizzo email. Questa opzione è disponibile solo nel tuo calendario personale. I destinatari dell’invito sono elencati sopra il pulsante, che mostra anche quanti sono: **Aggiungi e invita 2**. Google invia gli inviti quando tocchi il pulsante, non prima. Se non ci sono invitati, nessuno riceve un invito o un aggiornamento.

Anche un’attività può proporti una modifica, per esempio un prelievo da aggiungere. Mostra esattamente cosa cambia e la modifica viene applicata solo quando tocchi **Aggiungi**, **Salva** o **Elimina**.

Non hai ancora riunioni? Se non hai un calendario, **Collega il tuo calendario** apre Connessioni: collega [Google Calendar](google-calendar.md), [Calendario di Outlook](microsoft.md) o [un altro calendario](other-calendars.md).

## Sovrapposizioni con l’altro calendario

Quando una riunione di lavoro si sovrappone a un evento nel tuo calendario personale, o viceversa, The Machine crea un’attività relativa all’evento più recente. Può preparare una breve nota per spostarlo o proporti di rifiutare l’invito. Non viene inviato nulla finché non approvi.

Gli eventi di un’intera giornata, gli eventi in cui risulti libero e quelli provvisori non vengono mai considerati; ogni sovrapposizione viene segnalata una sola volta. Un’attività di Lavoro segnala solo la presenza di un conflitto, così il tuo team non vede mai l’evento personale. Solo tu puoi vedere con cosa si sovrappone.

## Preparazione alle riunioni

Prima di una riunione con persone esterne alla tua azienda, The Machine crea un’attività: **Preparazione per** la riunione. È un breve briefing:

- **Chi:** chi sono, in base al tuo Graph, con informazioni sul loro percorso quando disponibili.
- **Organizzazione:** di cosa si occupa la loro azienda, a chi si rivolge e a quale prezzo, quando è utile per la riunione.
- **Finora:** cosa avete discusso, chiesto e offerto e a che punto siete. Dopo la riunione, questi messaggi sono le fonti dell’attività.
- **Concordato in precedenza:**, **Modificato da allora:** e **Ancora aperto:** ciò che è emerso dalle riunioni precedenti con le stesse persone, con per ogni riga la riunione o il messaggio da cui proviene.
- **Promesse aperte:** ciò che tu o le altre persone dovete ancora fare, in base alle promesse sulla tua Machine.
- **Questioni aperte:** ciò che è ancora senza risposta.
- **Da decidere o portare:** cosa definire o portare con te e cosa probabilmente interessa agli altri partecipanti.

Arriva la mattina di un giorno lavorativo: il giorno stesso se la riunione è nel pomeriggio, altrimenti il giorno lavorativo precedente. È solo da leggere: tocca **Fatto** dopo averlo letto. Le promesse o le domande che richiedono un’azione hanno una propria attività.

Le riunioni precedenti vengono considerate quando una persona esterna partecipa a entrambe, a prescindere dal titolo della riunione e dall’indirizzo usato. La tua Machine legge le note disponibili: le tue, quelle dell’app per riunioni o quelle che ti sono arrivate via email; altrimenti, legge la trascrizione o le note nell’evento del calendario. Le note più recenti hanno più peso e un punto risolto in seguito non viene mostrato come ancora aperto.

Vengono considerate anche le note e i messaggi della [Cronologia](history.md), così il briefing può includere le riunioni avvenute prima che iniziassi a usare la Machine.

Un briefing di lavoro non legge note personali né contenuti dalla Machine di qualcun altro. Il testo resta a tua disposizione: non viene incluso in un passaggio e non può essere inviato per la revisione. Se non ci sono note, queste righe non appaiono.

Il briefing usa le informazioni già presenti sulla tua Machine. Per la prima riunione con una persona di un’azienda, legge anche la pagina iniziale del sito dell’azienda.

Se in OpenClaw è configurato un provider per la ricerca sul web (le Machine ospitate ne sono sprovviste), viene fatta anche una breve ricerca sul nome della persona e sulla sua azienda. I risultati includono un link. Alla ricerca vengono inviati solo il nome pubblico della persona, il nome dell’azienda e il sito web, mai i tuoi messaggi. I risultati vengono riutilizzati per 30 giorni.

Così, una prima riunione che hai accettato può avere un briefing prima ancora che tu abbia scambiato una parola con gli altri partecipanti: cosa fa la loro azienda, cosa significa per te e, quando è possibile saperlo, chi sono. Se è disponibile solo il nome, la ricerca viene usata solo se permette di identificare una sola persona. Se **Cerca i contatti di lavoro** è disattivato (Impostazioni, Sicurezza), non viene fatta alcuna ricerca.

Una riunione ricorrente riceve un briefing solo se dall’ultima volta ci sono novità: un messaggio, delle note o una promessa. Il briefing indica cosa c’è di nuovo, non ripete quello precedente. Viene creato dopo la fine della riunione precedente, per un massimo di due riunioni ricorrenti al giorno.

Se non c’è nulla di utile da segnalare, non viene creata alcuna attività. Le riunioni interne, personali o rifiutate non ne generano. Se una riunione viene spostata, l’attività resta la stessa e mostra il nuovo orario. Un’attività ignorata non ricompare; quella di una riunione annullata viene chiusa automaticamente.

Se un aggiornamento modifica il contenuto di un briefing, quelli delle riunioni future ancora aperti vengono riscritti una sola volta nella nuova versione. Il titolo, le fonti e la posizione nell’elenco restano invariati. Un briefing che hai modificato, posticipato o chiuso non cambia; lo stesso vale per quello di una riunione che inizia entro pochi minuti.

Nei dettagli della riunione, l’attività appare sotto **Attività**. Toccalo per aprire la chat.
