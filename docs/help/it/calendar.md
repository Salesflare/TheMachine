---
title: Calendario
area: calendar
summary: La settimana che ti aspetta, in un solo posto: riunioni, attività in scadenza, attività posticipate e promesse.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: ae462ef9e7316cb6
---
## Cosa mostra

I tuoi giorni da oggi in poi, con:

- le riunioni dei calendari che hai collegato,
- le attività in scadenza quel giorno e quelle posticipate nel giorno in cui ricompaiono,
- gli aggiornamenti sul lavoro che hai delegato,
- le promesse con una data,
- [viaggi ed eventi](calendar.md#trips-and-events) tratti dalle email di prenotazioni e biglietti.

Una riunione presente in due calendari viene mostrata una sola volta. Gli eventi di un calendario condiviso con te appaiono attenuati, con il nome di chi lo ha condiviso; non generano mai un’attività. Gli eventi di un’intera giornata e quelli di più giorni sono mostrati come eventi di un’intera giornata in ciascun giorno interessato. In **Agenda**, un viaggio compare in cima a ciascuno dei suoi giorni; in **Settimana** e **Mese** è rappresentato da un’unica barra che li attraversa, per esempio «Viaggio a Lisbona».

Un programma creato insieme è un’unica promessa, contrassegnata da «Con» e dal nome dell’altra persona. Una promessa relativa a una riunione di quel giorno con la stessa persona compare sulla riga della riunione.

**In ritardo** compare per primo. Se una riunione ha un’attività ancora aperta, mostra il suo stato: **Preparazione pronta**, **In preparazione** o **Attività**. Un’attività che sembra completata, perché hai già risposto o perché l’esecuzione ha rilevato che lo è, non viene mostrata come **Scadenza**.

## Agenda, settimana o mese

- **Agenda** mostra ogni giorno. Scorri verso il basso per i giorni successivi oppure verso l’alto, o tocca **Mostra giorni precedenti**, per quelli passati. Risale a una settimana prima del collegamento del calendario e una riga in cima indica da quale giorno. Quando è disponibile la [cronologia](history.md), risale a circa un anno prima.
- **Settimana** mostra una griglia dal lunedì alla domenica. Sul telefono mostra tre giorni.
- **Mese** mostra il mese intero. Sul computer mostra fino a tre elementi al giorno; sul telefono mostra dei punti e, toccandoli, elenca gli eventi di quel giorno.

**Oggi**, ‹ e › in alto permettono di spostarti tra le settimane o i mesi. La visualizzazione che scegli viene ricordata su quel dispositivo.

Nella griglia settimanale, gli eventi alla stessa ora sono affiancati e restano leggibili. Gli altri sono indicati con **+N**: selezionalo per aprire quel giorno nell’agenda.

## Aprire un elemento

Seleziona una riga per aprire la chat dell’attività, la promessa, il viaggio o l’evento, oppure la riunione. Se non puoi modificare una riunione da qui, per esempio perché è di un’altra persona o ha degli invitati, ne vedi i dettagli: quando, dove e chi. Le persone che il tuo Graph conosce e le organizzazioni e i progetti associati alla riunione sono link alle rispettive pagine. **Apri in Google Calendar** (o **Apri in Outlook**) sotto i dettagli apre la riunione nel rispettivo servizio. Aprirla non comporta modifiche.

Una sala riunioni prenotata per una riunione compare sotto «Dove», mai come persona o nel tuo Graph.

Il link a una riunione mostra il nome del servizio, per esempio Zoom, Google Meet o Teams, oppure **Videochiamata**. Apri la riunione per partecipare.

## Viaggi ed eventi

Quando ricevi un’email con una prenotazione di volo, hotel, casa vacanze, treno, autobus, traghetto, auto a noleggio, taxi o parcheggio in aeroporto, la tua Machine la aggiunge a un viaggio. Le prenotazioni dello stesso itinerario, provenienti da qualsiasi tua casella di posta, finiscono in un unico viaggio: il treno per l’aeroporto, i voli, l’auto, il soggiorno e il viaggio di ritorno. Le prenotazioni vengono raggruppate se le date si sovrappongono o se una inizia quando termina l’altra.

Il viaggio appare come un’unica barra che attraversa i giorni interessati. Aprilo per vedere tutte le prenotazioni in ordine cronologico, con orari, indirizzo, codice di prenotazione e posto.

I biglietti per concerti, partite, festival o conferenze creano un evento per ogni occasione, con il luogo, il codice di prenotazione, il posto e il numero di biglietti. Un secondo ordine per lo stesso evento viene aggiunto a quello esistente. Un evento prenotato nella tua casella di lavoro è contrassegnato come **Lavoro**, altrimenti come **Personale**. I biglietti per un’attività durante un viaggio vengono aggiunti al viaggio.

Per un viaggio che deve ancora iniziare, la tua Machine segnala cosa manca, per esempio **Nessuna prenotazione di alloggio per 2 notti** o l’assenza di una prenotazione dall’aeroporto all’hotel. Queste righe sono attenuate e contrassegnate con **Nessuna prenotazione**. Se un viaggio non include pernottamenti, non vengono mostrati avvisi sulle notti.

- Ogni riga indica da chi proviene la prenotazione, per esempio **Da Example Tickets**, e apre l’email.
- Se dall’email è stata creata un’attività, per esempio per pagare i biglietti, **Apri l’attività** la mostra.
- Se una prenotazione cambia, la riga viene aggiornata; se viene annullata, viene rimossa. Quando tutte le prenotazioni sono annullate, viene rimosso anche il viaggio o l’evento.
- Le prenotazioni per altre persone, per esempio il volo di un collega inoltrato a te, non vengono aggiunte ai tuoi viaggi.

La maggior parte delle conferme contiene i dettagli in un formato che la tua Machine può leggere senza AI. Se non è così, per esempio per un’email inoltrata o un piccolo sito di prenotazioni, il tuo [modello](model.md) legge l’email in background, poche alla volta, e si ferma quando sei vicino al limite di utilizzo. Una volta disponibile la [cronologia](history.md), le email di prenotazione dell’anno conservato dalla tua Machine vengono lette in background.

## Note e trascrizione delle riunioni

I dettagli di una riunione sono divisi in due parti. **Note** è il riepilogo, con decisioni e attività da svolgere. **Trascrizione** riporta parola per parola ciò che è stato detto. All’inizio è chiusa e ne viene mostrata la durata; seleziona **Mostra** per aprirla.

Se non si carica, riprova automaticamente per circa mezzo minuto. Poi tocca **Riprova**.

Note e trascrizione hanno ciascuna le proprie opzioni **Aggiungi note** o **Aggiungi trascrizione**, **Carica file** per un file Markdown o di testo, **Modifica** e **Rimuovi** (tocca due volte). Il contenuto di una sezione resta lì. In una riunione che puoi modificare, **Note** sotto il modulo apre le note.

Se hai collegato [Zoom](zoom.md), [Google Meet](google-meet.md) o [Granola](granola.md), le relative note compaiono in Note e la trascrizione in Trascrizione, contrassegnate con **Da Zoom**, **Da Google Meet** o **Da Granola**. Non sostituiscono mai ciò che hai aggiunto: se sono presenti entrambi, vengono mostrati entrambi.

Le note possono anche essere aggiunte all’evento della riunione nel calendario dopo il suo inizio, oppure arrivare via email da Zoom o Gemini. Dopo la riunione, The Machine crea attività da queste note solo per i passi successivi chiaramente definiti. Se le stesse note arrivano in due modi, viene creata una sola attività, con la riunione come origine: «Origine: note di» seguito dalla riunione.

Una riunione con una trascrizione ma senza note ha l’opzione **Genera note**. The Machine le crea a partire dalla trascrizione: un breve riepilogo, le decisioni e le attività con l’indicazione di chi se ne occupa, nella lingua della riunione.

Viene mostrato **Sto scrivendo le note…** e la creazione continua anche se chiudi la riunione. Per una riunione lunga possono servire alcuni minuti e viene usato il tuo modello. Le note sono contrassegnate con **Scritte da The Machine** e non sostituiscono quelle che hai aggiunto.

Puoi chiedere anche a The Machine di aggiungerle. Per esempio, chiedi in un’attività: «aggiungi questa trascrizione alla riunione del consiglio di oggi». Una trascrizione viene aggiunta in Trascrizione, un riepilogo in Note. Nel Calendario, le riunioni con note o trascrizioni sono contrassegnate con **Note** o **Trascrizione**.

The Machine usa entrambi i contenuti per individuare le attività successive alla riunione. Sono contrassegnate come Lavoro o Personale, come la riunione, e vengono condivise con il tuo team solo se lo è anche la riunione.

Puoi aprire una riunione con questi dettagli da qualsiasi punto in cui la trovi: nella cronologia, nei risultati di una ricerca nei messaggi o come origine di un’attività. **Invito originale** in fondo mostra l’invito così come è arrivato.

## Aggiungere o modificare un evento

Da qui puoi modificare il tuo calendario Google. Outlook e gli altri calendari sono solo consultabili. **Nuovo evento** ne aggiunge uno (sul telefono si trova sotto **+** nella barra superiore): scegli il calendario, un titolo e l’orario. Seleziona un evento senza invitati in quel calendario per modificarlo oppure **Elimina** (tocca due volte).

**Dove** suggerisce dei luoghi mentre scrivi: prima quelli che hai già usato e le tue organizzazioni, poi gli indirizzi di [OpenStreetMap](https://www.openstreetmap.org), una mappa gratuita. Per cercare vengono inviate solo le parole che scrivi. Scegli un suggerimento oppure lascia il testo che hai inserito.

**Invita** aggiunge persone dal tuo Graph o qualsiasi indirizzo email. Questa opzione è disponibile solo nel tuo calendario. Gli invitati sono elencati sopra il pulsante, che indica il numero di persone, per esempio **Aggiungi e invita 2**. Google invia gli inviti quando tocchi il pulsante, non prima. Se non ci sono invitati, nessuno riceve un invito o un aggiornamento.

Anche un’attività può proporre una modifica, per esempio aggiungere un ritiro. La modifica viene mostrata in modo preciso e viene applicata solo se selezioni **Aggiungi**, **Salva** o **Elimina**.

Non hai ancora riunioni? Se non hai collegato un calendario, **Collega il tuo calendario** apre Connessioni: collega [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) o [un altro calendario](other-calendars.md).

## Sovrapposizioni con l’altro calendario

Quando una riunione di lavoro si sovrappone a qualcosa nel tuo calendario personale, o viceversa, The Machine crea un’unica attività relativa all’evento più recente. Può preparare una breve nota per spostarlo o proporti di rifiutarlo. Non viene inviato nulla finché non approvi.

Gli eventi di un’intera giornata, quelli con stato libero e quelli provvisori non vengono considerati; ogni sovrapposizione viene segnalata una sola volta. Un’attività di Lavoro segnala solo che c’è un conflitto, così il tuo team non vede mai l’evento personale. Solo tu puoi vedere con cosa si sovrappone.

## Preparati alle riunioni

Prima di una riunione con persone esterne alla tua azienda, The Machine crea un’attività: **Preparati per** la riunione. È un breve riepilogo:

- **Chi:** chi sono, in base al tuo Graph, con informazioni sul loro percorso professionale se disponibili.
- **Organizzazione:** cosa fa la loro azienda che può essere utile per la riunione.
- **Finora:** di cosa avete parlato, cosa avete chiesto e proposto e a che punto siete. Dopo la riunione, quei messaggi diventano le fonti dell’attività.
- **Promesse aperte:** cosa tu o loro dovete ancora fare.
- **Domande aperte:** cosa è ancora senza risposta.
- **Da decidere o portare:** cosa definire o portare con te e cosa probabilmente sarà importante per loro.

L’attività viene creata la mattina di un giorno lavorativo: il giorno stesso della riunione se si svolge nel pomeriggio, altrimenti il giorno lavorativo precedente. Serve solo per consultare le informazioni: seleziona **Fatto** dopo averla letta. Se contiene una promessa o una domanda che richiede un’azione, viene creata un’attività a parte.

Usa le informazioni già presenti sulla tua Machine. Per il primo incontro con una persona di un’azienda, fa anche una breve ricerca online sul suo nome e sull’azienda, mostrando un link accanto alle informazioni trovate. La ricerca usa solo il suo nome pubblico, il nome dell’azienda e il sito web, mai i tuoi messaggi. I risultati vengono riutilizzati per 30 giorni. Se **Cerca i contatti di lavoro** è disattivato (Impostazioni, Sicurezza), non viene fatta alcuna ricerca.

Se non ci sono informazioni utili nella cronologia, l’attività non viene creata. Le riunioni ricorrenti, interne, personali e rifiutate non ne generano. Se una riunione viene spostata, la sua attività rimane la stessa e viene aggiornata al nuovo orario. Se scarti un’attività, non ricompare; quella di una riunione annullata si chiude da sola.

I dettagli della riunione mostrano la relativa attività sotto **Attività**, a un tocco di distanza dalla chat.
