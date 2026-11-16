---
title: Calendario
area: calendar
summary: La settimana che ti aspetta, tutto in un unico posto: riunioni, attività in scadenza, attività posticipate e promesse.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 970b39054ae39543
---
## Cosa mostra

I tuoi giorni a partire da oggi, con:

- le riunioni dei calendari che hai collegato,
- le attività in scadenza quel giorno e quelle posticipate nel giorno in cui tornano,
- gli aggiornamenti sul lavoro che hai delegato,
- le promesse con una data,
- [viaggi ed eventi](calendar.md#trips-and-events) ricavati dalle email di prenotazioni e biglietti.

Una riunione presente in due calendari viene mostrata una sola volta. Gli eventi di un calendario condiviso con te sono attenuati e riportano il nome di chi lo ha condiviso; non generano mai un’attività. Gli eventi che durano tutto il giorno o più giorni vengono mostrati come eventi di un’intera giornata, per ogni giorno interessato. In Agenda, un viaggio compare per primo in ciascuno dei suoi giorni; in Settimana e Mese appare come una fascia che copre tutti i giorni, per esempio «Viaggio a Lisbona».

Un programma concordato insieme è una sola promessa, contrassegnata da «Con» e dal nome dell’altra persona. Se una promessa riguarda una riunione di quel giorno con la stessa persona, compare sulla riga della riunione.

**In ritardo** compare per primo. Una riunione con un’attività aperta mostra il suo stato: **Preparazione pronta**, **In preparazione** o **Attività**. Un’attività che sembra completata, perché hai già risposto o perché la sua esecuzione l’ha trovata completata, non viene mostrata come **Scadenza**.

## Agenda, settimana o mese

- **Agenda** mostra i giorni uno dopo l’altro. Scorri verso il basso per i giorni successivi o verso l’alto (oppure tocca **Mostra giorni precedenti**) per quelli passati. Torna indietro fino a una settimana prima di quando hai collegato il calendario e mostra in alto il primo giorno visualizzato. Quando viene caricata la [cronologia](history.md), torna indietro di circa un anno.
- **Settimana** mostra una griglia dal lunedì alla domenica. Sul telefono mostra tre giorni.
- **Mese** mostra il mese intero. Sul computer mostra fino a tre elementi al giorno; sul telefono mostra dei punti e, toccandoli, elenca gli eventi di quel giorno.

**Oggi**, ‹ e › in alto ti permettono di spostarti tra le settimane o i mesi. La vista scelta viene ricordata su quel dispositivo.

Nella griglia della settimana, gli eventi alla stessa ora sono affiancati e restano leggibili. Gli altri sono indicati con **+N**: toccandolo, si apre quel giorno in Agenda.

## Apri un elemento

Seleziona una riga per aprire la chat dell’attività, la promessa, il viaggio o l’evento, oppure la riunione. Se non puoi modificare una riunione da qui, per esempio perché appartiene a un’altra persona o ha degli invitati, ne vedi i dettagli: quando si svolge, dove e chi partecipa. Le persone conosciute dal tuo Graph e le organizzazioni e i progetti a cui è associata la riunione rimandano alle rispettive pagine. **Apri in Google Calendar** (o **Apri in Outlook**) sotto questi link apre la riunione nel calendario corrispondente. La sola visualizzazione non comporta modifiche.

Una sala riunioni prenotata per una riunione compare sotto «Dove», mai come persona né nel tuo Graph.

Il link alla riunione viene mostrato con il nome del servizio, per esempio Zoom, Google Meet o Teams, oppure come **Videochiamata**. Apri la riunione per partecipare.

## Viaggi ed eventi

Quando nella tua posta arriva una prenotazione di un volo, hotel, treno, autobus, traghetto o auto a noleggio, la tua Machine la aggiunge a un viaggio. Le prenotazioni dello stesso itinerario vengono raggruppate in un unico viaggio: andata, hotel e ritorno. Il viaggio appare come una fascia che copre tutti i giorni interessati. Aprilo per vedere, in ordine cronologico, il codice di prenotazione, il posto e il biglietto di ogni prenotazione.

I biglietti per concerti, partite, festival o conferenze creano un evento, uno per ciascuna iniziativa, con il luogo, il codice di prenotazione, il posto e il numero di biglietti. Un secondo ordine per lo stesso evento viene aggiunto allo stesso evento. Un evento prenotato nella tua casella di lavoro è Lavoro; altrimenti è Personale.

- Ogni riga indica da chi proviene la prenotazione, per esempio **Da Example Tickets**, e apre l’email corrispondente.
- Se dall’email è stata creata un’attività, per esempio per pagare i biglietti, **Apri l’attività** la mostra.
- Se una prenotazione viene modificata, la relativa riga si aggiorna; se viene annullata, scompare. Quando tutte le prenotazioni sono annullate, scompare anche il viaggio o l’evento.

La tua Machine legge i dettagli inseriti da compagnie aeree, hotel, siti di prenotazione e rivenditori di biglietti nelle email di conferma, senza usare l’IA. Le email che non contengono questi dettagli non generano nulla. Le email di prenotazione dell’anno coperto dalla [cronologia](history.md) conservata dalla tua Machine vengono lette in background una volta caricata la cronologia.

## Note e trascrizione della riunione

I dettagli di una riunione hanno due sezioni. **Note** contiene il riepilogo: decisioni e azioni da svolgere. **Trascrizione** riporta parola per parola ciò che è stato detto. All’inizio è chiusa e mostra la durata; **Mostra** la apre.

Se non si caricano, la riunione riprova automaticamente per circa mezzo minuto. Dopodiché tocca **Riprova**.

Ognuna ha i propri comandi **Aggiungi note** o **Aggiungi trascrizione**, **Carica file** per un file Markdown o di testo, **Modifica** e **Rimuovi** (tocca due volte). Il contenuto aggiunto a una sezione resta lì. In una riunione che puoi modificare, il comando **Note** sotto il modulo le apre.

Se hai collegato [Zoom](zoom.md), [Google Meet](google-meet.md) o [Granola](granola.md), le note del servizio compaiono in Note e la trascrizione in Trascrizione, con l’indicazione **Da Zoom**, **Da Google Meet** o **Da Granola**. Non sostituiscono mai ciò che hai aggiunto: se sono presenti entrambi i contenuti, vengono mostrati entrambi.

Le note possono arrivare anche dall’evento della riunione nel calendario, se aggiunte dopo l’inizio, oppure via email da Zoom o Gemini. Al termine della riunione, The Machine crea attività da queste note solo quando contengono indicazioni chiare sui prossimi passi. Se le stesse note arrivano in due modi diversi, viene creata una sola attività, associata alla riunione come fonte: «Fonte: note di» seguito dalla riunione.

Se una riunione ha una trascrizione ma non delle note, mostra **Genera note**. The Machine le ricava dalla trascrizione: un breve riepilogo, le decisioni e le attività con l’indicazione di chi se ne occupa, nella lingua della riunione.

Compare **Sto scrivendo le note…** e la generazione continua anche se chiudi la riunione. Per una riunione lunga possono volerci alcuni minuti; viene usato il tuo modello. Le note riportano **Scritte da The Machine** e non sostituiscono mai quelle che hai aggiunto.

Anche The Machine può aggiungere le note. Chiedilo in un’attività, per esempio: «Aggiungi la trascrizione della riunione del consiglio di oggi». La trascrizione viene aggiunta in Trascrizione, il riepilogo in Note. Nel Calendario, una riunione con questi contenuti mostra **Note** o **Trascrizione**.

The Machine legge entrambi i contenuti per trovare le attività da svolgere dopo la riunione. Sono Lavoro o Personale come la riunione e vengono condivise con il tuo team solo se lo è anche la riunione.

La riunione si apre con questi dettagli ovunque la trovi: nella cronologia, tra i risultati di una ricerca nei messaggi o come fonte di un’attività. **Invito originale** in fondo mostra l’invito così come è arrivato.

## Aggiungi o modifica un evento

Da qui puoi modificare il tuo calendario Google. Outlook e gli altri calendari sono solo consultabili. **Nuovo evento** ne aggiunge uno (sul telefono, lo trovi sotto **+** nella barra in alto): scegli il calendario, un titolo e l’orario. Seleziona un evento senza invitati in quel calendario per modificarlo o **Elimina** per eliminarlo (tocca due volte).

**Dove** suggerisce luoghi mentre scrivi: prima quelli che hai già usato e le tue organizzazioni, poi gli indirizzi di [OpenStreetMap](https://www.openstreetmap.org), una mappa gratuita. Per cercare, vengono inviate solo le parole che scrivi. Scegli uno dei suggerimenti oppure inserisci il testo che preferisci.

**Invita** aggiunge persone dal tuo Graph o qualsiasi indirizzo email. È disponibile solo nel tuo calendario. Gli invitati sono elencati sopra il pulsante, che indica anche quanti sono: **Aggiungi e invita 2**. Google invia gli inviti quando tocchi il pulsante, non prima. Se non ci sono invitati, nessuno riceve un invito o un aggiornamento.

Un’attività può proporti anche una modifica, per esempio aggiungere un ritiro. Mostra esattamente cosa cambierà; la modifica viene applicata solo se selezioni **Aggiungi**, **Salva** o **Elimina**.

Non hai ancora riunioni? Se non hai un calendario, **Collega il tuo calendario** apre Connessioni: collega [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) o [un altro calendario](other-calendars.md).

## Conflitti con l’altro calendario

Quando una riunione di lavoro si sovrappone a un impegno nel tuo calendario personale, o viceversa, The Machine crea un’attività sulla più recente delle due. Può preparare una breve bozza per spostare l’impegno o proporti di rifiutare l’invito. Non viene inviato nulla finché non approvi.

Gli eventi che durano tutto il giorno, sono contrassegnati come libero o sono provvisori non vengono considerati; ogni conflitto viene segnalato una sola volta. Un’attività di Lavoro indica solo che c’è un conflitto, così il tuo team non vede mai l’evento personale. Solo tu puoi vedere con cosa è in conflitto.

## Preparati per le riunioni

Prima di una riunione con persone esterne alla tua azienda, The Machine crea un’attività: **Preparati per** la riunione. È un breve briefing:

- **Chi:** chi sono, secondo il tuo Graph.
- **Ultimo contatto:** l’ultimo scambio che hai avuto con loro. Dopo la riunione, quel messaggio diventa la fonte dell’attività.
- **Promesse aperte:** cosa resta da fare a te o a loro.
- **Domande aperte:** quali domande non hanno ancora una risposta.
- **Decidere o portare:** cosa decidere o portare con te.

L’attività arriva la mattina di un giorno lavorativo: il giorno stesso della riunione se si svolge nel pomeriggio, altrimenti il giorno lavorativo precedente. Usa solo le informazioni già presenti nella tua Machine. Serve solo per consultarla: tocca **Fatto** dopo averla letta. Le promesse o le domande che richiedono un’azione hanno una propria attività.

Se non ci sono informazioni utili, non viene creata alcuna attività. Le riunioni ricorrenti, interne, personali e rifiutate non ne generano. Se una riunione viene spostata, mantiene la stessa attività, con il nuovo orario. Se scarti l’attività, non ricompare; se la riunione viene annullata, l’attività si chiude automaticamente.

I dettagli della riunione mostrano la relativa attività sotto **Attività**; toccandola, apri la chat.
