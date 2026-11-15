---
title: Calendario
area: calendar
summary: La settimana che ti aspetta, tutta in un unico posto: riunioni, attività in scadenza, attività posticipate e promesse.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py
order: 1
translated: d85b3eff63ea503d
---
## Cosa mostra

I tuoi giorni a partire da oggi, con:

- le riunioni dei calendari che hai collegato,
- le attività in scadenza quel giorno e quelle posticipate nel giorno in cui tornano,
- i promemoria sui lavori che hai delegato,
- le promesse con una data,
- le [note](notes.md) con date, come un viaggio.

Una riunione presente in due calendari viene mostrata una sola volta. Un calendario condiviso con te mostra gli eventi di chi lo ha condiviso in tono attenuato, con il suo nome; da questi eventi non vengono mai create attività. Gli eventi di un'intera giornata e quelli di più giorni vengono mostrati come eventi di un'intera giornata in tutti i giorni interessati. In Agenda, un viaggio appare per primo in ciascuno dei suoi giorni; in Settimana e Mese, appare come una sola fascia che copre tutti i giorni, per esempio «Viaggio a Lisbona».

Un piano concordato insieme è una sola promessa, contrassegnata da «Con» e dal nome dell'altra persona. Una promessa relativa a una riunione di quel giorno con la stessa persona appare nella riga della riunione.

**In ritardo** viene mostrato per primo. Una riunione con un'attività ancora aperta mostra il suo stato: **Preparazione pronta**, **In preparazione** o **Attività**. Un'attività che sembra completata, perché hai già risposto o perché la sua esecuzione l'ha trovata completata, non viene mostrata come **Scadenza**.

## Agenda, settimana o mese

- **Agenda** elenca ogni giorno. Scorri verso il basso per i giorni successivi o verso l'alto, oppure tocca **Mostra giorni precedenti**, per i giorni passati. Torna indietro fino a una settimana prima che collegassi il calendario e una riga in alto indica da quale giorno. Una volta caricata la [cronologia](history.md), torna indietro di circa un anno.
- **Settimana** mostra una griglia dal lunedì alla domenica. Sul telefono mostra tre giorni.
- **Mese** mostra tutto il mese. Su un computer mostra fino a tre elementi al giorno; sul telefono mostra dei puntini e, toccandone uno, elenca gli elementi di quel giorno.

**Oggi**, ‹ e › in alto ti permettono di spostarti tra le settimane o i mesi. La visualizzazione scelta viene salvata su quel dispositivo.

Nella griglia settimanale, gli eventi che si svolgono allo stesso orario appaiono affiancati, ma restano leggibili. Gli altri sono indicati con **+N**: toccalo per aprire quel giorno nell'agenda.

## Aprire un elemento

Seleziona una riga per aprire la chat dell'attività, la promessa, la nota o la riunione. Se non puoi modificare una riunione da qui, per esempio perché appartiene a un'altra persona o ha degli invitati, ne vedrai i dettagli: quando, dove e chi. Le persone che Graph riconosce e le organizzazioni e i progetti associati alla riunione sono link alle rispettive pagine. **Apri in Google Calendar** o **Apri in Outlook**, sotto questi elementi, apre la riunione nel rispettivo calendario. Visualizzarla non modifica nulla.

Una sala prenotata per una riunione appare sotto «Dove», mai come persona o in Graph.

Il link della riunione mostra il nome del servizio, come Zoom, Google Meet o Teams, oppure **Videochiamata**. Apri la riunione per partecipare.

## Note e trascrizione della riunione

I dettagli di una riunione hanno due sezioni. **Note** contiene il riepilogo: decisioni e attività da svolgere. **Trascrizione** riporta parola per parola ciò che è stato detto. All'inizio è chiusa e mostra la sua durata; tocca **Mostra** per aprirla.

Se non si caricano, il sistema riprova automaticamente per circa mezzo minuto. Poi tocca **Riprova**.

Per ciascuna sezione puoi scegliere **Aggiungi note** o **Aggiungi trascrizione**, **Carica file** per un file Markdown o di testo, **Modifica** e **Rimuovi** (tocca due volte). I contenuti di una sezione non vengono spostati nell'altra. In una riunione che puoi modificare, tocca **Note** sotto il modulo per aprirle.

Se hai collegato [Zoom](zoom.md) o [Google Meet](google-meet.md), le relative note appaiono in Note e la trascrizione in Trascrizione, contrassegnate da **Da Zoom** o **Da Google Meet**. Non sostituiscono mai ciò che hai aggiunto: se sono presenti entrambi i contenuti, vengono mostrati entrambi.

Le note possono arrivare anche dall'evento della riunione nel calendario, aggiunte dopo l'inizio, oppure via email da Zoom o Gemini. Al termine della riunione, The Machine crea attività da queste note solo se indicano chiaramente i prossimi passi. Se le stesse note arrivano in due modi diversi, viene creata una sola attività, con la riunione come fonte: «Fonte: note di» seguito dal nome della riunione.

Una riunione con una trascrizione ma senza note mostra **Genera note**. The Machine le scrive a partire dalla trascrizione: un breve riepilogo, le decisioni e le attività da svolgere, con i nomi di chi se ne occupa, nella lingua della riunione.

Viene mostrato **Sto scrivendo le note…**. La generazione continua anche se chiudi la riunione. Per una riunione lunga possono volerci alcuni minuti e viene usato il tuo modello. Le note indicano **Scritte da The Machine** e non sostituiscono quelle che hai aggiunto.

Puoi anche chiedere a The Machine di aggiungerle. Per esempio, chiedile in un'attività: «aggiungi questa trascrizione alla riunione del consiglio di oggi». Una trascrizione viene inserita in Trascrizione, un riepilogo in Note. Nel Calendario, una riunione con note o trascrizione mostra **Note** o **Trascrizione**.

The Machine legge entrambi i contenuti per trovare le attività da svolgere dopo la riunione. Sono di tipo Work o Personal, come la riunione, e vengono condivise con il tuo team solo se lo è anche la riunione.

Puoi aprire una riunione con questi dettagli ovunque la trovi: in una cronologia, nei risultati di una ricerca nei messaggi o come fonte di un'attività. **Invito originale** in fondo mostra l'invito così come è arrivato.

## Aggiungere o modificare un evento

Da qui puoi modificare il tuo calendario Google. Outlook e gli altri calendari sono di sola lettura. **Nuovo evento** ne aggiunge uno (sul telefono lo trovi sotto **+** nella barra superiore): scegli il calendario, un titolo e l'orario. Seleziona un evento senza invitati in quel calendario per modificarlo, oppure tocca **Elimina** (due volte).

**Dove** suggerisce dei luoghi mentre scrivi: prima quelli che hai già usato e quelli delle tue organizzazioni, poi gli indirizzi di [OpenStreetMap](https://www.openstreetmap.org), una mappa gratuita. Per cercarli vengono inviate solo le parole che scrivi. Scegli uno dei suggerimenti o lascia il testo che hai inserito.

**Invita** aggiunge persone da Graph o qualsiasi indirizzo email. Questa opzione è disponibile solo nel tuo calendario. Chi riceverà un invito è indicato sopra il pulsante, che mostra anche il numero di invitati: **Aggiungi e invita 2**. Google invia gli inviti quando tocchi il pulsante, non prima. Se non aggiungi invitati, nessuno riceve un invito o un aggiornamento.

Un'attività può proporti anche una modifica, per esempio aggiungere un passaggio a prendere qualcuno. Mostra esattamente cosa cambierà; la modifica viene applicata solo se tocchi **Aggiungi**, **Salva** o **Elimina**.

Non hai ancora riunioni? Se non hai collegato un calendario, tocca **Collega il tuo calendario** per aprire Connessioni e collegare [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) o [un altro calendario](other-calendars.md).

## Conflitti con l'altro calendario

Quando una riunione di lavoro si sovrappone a un evento del tuo calendario personale, o viceversa, The Machine crea un'attività relativa all'evento più recente. Può preparare una breve nota per spostarlo o proporti di rifiutarlo. Non viene inviato nulla finché non approvi.

Gli eventi di un'intera giornata, quelli in cui risulti libero e quelli provvisori non vengono conteggiati. Ogni conflitto viene segnalato una sola volta. Un'attività Work indica solo che c'è un conflitto, così il tuo team non vede mai l'evento personale. Solo tu puoi vedere con quale evento è in conflitto.

## Preparati alle riunioni

Prima di una riunione con persone esterne alla tua azienda, The Machine crea un'attività: **Preparati per** la riunione. È un breve riepilogo:

- **Chi:** chi sono, secondo Graph.
- **Ultimo contatto:** l'ultimo scambio di messaggi con loro. Dopo la riunione, quel messaggio diventa la fonte dell'attività.
- **Promesse aperte:** ciò che tu o loro dovete ancora fare.
- **Domande aperte:** ciò che è ancora senza risposta.
- **Da decidere o portare:** ciò che devi definire o portare con te.

L'attività arriva la mattina di un giorno lavorativo: il giorno stesso della riunione, se è nel pomeriggio, altrimenti il giorno lavorativo precedente. Usa solo le informazioni già presenti sulla tua Machine. Serve solo per consultazione: tocca **Fatto** dopo averla letta. Se contiene una promessa o una domanda che richiede un'azione, questa ha una propria attività.

Se non ci sono informazioni utili nella cronologia, non viene creata nessuna attività. Le riunioni ricorrenti, interne, personali o rifiutate non ne generano. Se una riunione viene spostata, la sua attività resta la stessa e viene aggiornata al nuovo orario. Un'attività scartata non ricompare e quella di una riunione annullata si chiude da sola.

I dettagli della riunione mostrano l'attività sotto **Attività**; toccala per aprire la chat.
