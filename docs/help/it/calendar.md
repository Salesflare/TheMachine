---
title: Calendario
area: calendar
summary: La settimana che ti aspetta, in un unico posto: riunioni, attività in scadenza, attività posticipate e promesse.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py
order: 1
translated: 9da7909bce253806
---
## Cosa mostra

I tuoi giorni da oggi in poi, con:

- le riunioni dei calendari che hai collegato,
- le attività in scadenza quel giorno e quelle posticipate nel giorno in cui tornano,
- gli aggiornamenti sulle attività che hai affidato ad altri,
- le promesse con una data.

Una riunione presente in due calendari viene mostrata una sola volta. Un calendario condiviso con te mostra gli eventi di chi l'ha condiviso in tono attenuato, con il suo nome; da questi eventi non vengono mai create attività. Gli eventi di tutto il giorno e quelli di più giorni sono mostrati come eventi di tutto il giorno, per ciascun giorno che occupano.

Un piano concordato insieme è una sola promessa, indicata con «Con» e il nome dell'altra persona. Una promessa relativa a una riunione di quel giorno con la stessa persona appare sulla riga della riunione.

**In ritardo** viene mostrato per primo. Una riunione con un'attività ancora aperta la indica: **Preparazione pronta**, **In preparazione** o **Attività**. Un'attività che sembra completata, perché hai già risposto o perché la sua esecuzione l'ha trovata completata, non viene mostrata come **Scadenza**.

## Agenda, settimana o mese

- **Agenda** elenca ogni giorno. Scorri verso il basso per vedere i giorni successivi, oppure verso l'alto (o tocca **Mostra giorni precedenti**) per quelli passati. Torna indietro fino a una settimana prima che collegassi il calendario e mostra in alto una riga che indica da quale giorno. Quando è disponibile la [cronologia](history.md), torna indietro di circa un anno.
- **Settimana** mostra una griglia da lunedì a domenica. Sul telefono mostra tre giorni.
- **Mese** mostra tutto il mese. Su computer mostra fino a tre elementi al giorno; sul telefono mostra dei puntini. Tocca un giorno per visualizzarne l'elenco.

**Oggi**, ‹ e › in alto ti permettono di spostarti tra le settimane o i mesi. La vista che scegli viene ricordata su quel dispositivo.

Nella griglia settimanale, gli eventi che si svolgono nello stesso orario sono affiancati, ma restano leggibili. Gli altri sono indicati con **+N**. Toccandolo, si apre quel giorno nell'agenda.

## Aprire un elemento

Seleziona una riga per aprire la chat dell'attività, la promessa o la riunione. Per una riunione che non puoi modificare qui, ad esempio una di un'altra persona o con invitati, vengono mostrati i dettagli: quando, dove e chi. Le persone che Graph riconosce, le organizzazioni e i progetti della riunione sono link alle rispettive pagine. **Apri in Google Calendar** (o **Apri in Outlook**) li apre lì. Visualizzare una riunione non comporta modifiche.

Una sala prenotata per una riunione appare sotto il luogo, ma non come persona né in Graph.

Un link a una riunione mostra il servizio, ad esempio Zoom, Google Meet o Teams, oppure **Videochiamata**. Apri la riunione per partecipare.

## Note e trascrizione della riunione

I dettagli di una riunione hanno due sezioni. **Note** è il riepilogo, con decisioni e attività da svolgere. **Trascrizione** riporta parola per parola ciò che è stato detto. All'inizio è chiusa e ne viene indicata la durata; tocca **Mostra** per aprirla.

Se non si caricano, la riunione riprova automaticamente per circa mezzo minuto. Dopodiché, tocca **Riprova**.

Puoi **Aggiungi note** o **Aggiungi trascrizione** separatamente, **Carica file** Markdown o di testo, **Modifica** o **Rimuovi** ciascuna sezione. Per rimuoverla, tocca due volte. Il contenuto di una sezione resta lì. In una riunione che puoi modificare, **Note** sotto il modulo apre le note.

Se hai collegato [Zoom](zoom.md) o [Google Meet](google-meet.md), le note del servizio appaiono in Note e la trascrizione in Trascrizione, con l'indicazione **Da Zoom** o **Da Google Meet**. Non sostituiscono mai ciò che hai aggiunto tu: se sono presenti entrambi, vengono mostrati entrambi.

Le note possono arrivare anche dall'evento della riunione nel calendario, se aggiunte dopo l'inizio, oppure via email da Zoom o Gemini. Dopo la riunione, The Machine crea attività a partire da queste note solo quando indicano chiaramente i prossimi passi. Se le stesse note arrivano da due fonti, viene creata una sola attività, con la riunione come origine: «Origine: note di» seguito dalla riunione.

Se una riunione ha una trascrizione ma non delle note, mostra **Genera note**. The Machine le crea a partire dalla trascrizione: un breve riepilogo, le decisioni e le attività da svolgere, con l'indicazione di chi se ne occupa, nella lingua della riunione.

Viene mostrato **Sto scrivendo le note…** e la generazione continua anche se chiudi la riunione. Per una riunione lunga possono servire alcuni minuti e viene usato il tuo modello. Le note indicano **Scritto da The Machine** e non sostituiscono mai quelle che hai aggiunto tu.

Anche The Machine può aggiungerle. Chiediglielo in un'attività, ad esempio: «aggiungi questa trascrizione alla riunione di oggi del team». La trascrizione viene inserita in Trascrizione e il riepilogo in Note. Nel Calendario, le riunioni che le includono mostrano **Note** o **Trascrizione**.

The Machine usa entrambi i contenuti per individuare le attività successive alla riunione. Sono di tipo Lavoro o Personale, come la riunione, e vengono condivise con il tuo team solo se anche la riunione lo è.

Puoi aprire i dettagli della riunione ovunque la trovi: nella cronologia, nei risultati di una ricerca nei messaggi o come origine di un'attività. **Invito originale** in fondo mostra l'invito così come è arrivato.

## Aggiungere o modificare un evento

Puoi modificare da qui i tuoi calendari Google. Outlook e gli altri calendari sono solo in visualizzazione. **Nuovo evento** ne aggiunge uno. Sul telefono, lo trovi sotto **+** nella barra in alto. Scegli il calendario, un titolo e l'orario. Seleziona un evento senza invitati in quel calendario per modificarlo o **Elimina** per cancellarlo. Per eliminarlo, tocca due volte.

**Dove** suggerisce dei luoghi mentre scrivi: prima quelli che hai già usato e le tue organizzazioni, poi gli indirizzi di [OpenStreetMap](https://www.openstreetmap.org), una mappa gratuita. Per cercarli vengono inviate solo le parole che digiti. Scegli un suggerimento o mantieni il testo che hai inserito.

**Invita** aggiunge persone da Graph o qualsiasi indirizzo email. Questa opzione è disponibile solo nel tuo calendario. Le persone che riceveranno un invito sono elencate sopra il pulsante, che indica anche quante sono: **Aggiungi e invita 2**. Google invia gli inviti quando tocchi il pulsante, non prima. Se non ci sono invitati, nessuno riceve un invito o un aggiornamento.

Un'attività può anche proporti una modifica, ad esempio aggiungere un ritiro. Ti mostra esattamente cosa cambierà e la modifica viene applicata solo quando tocchi **Aggiungi**, **Salva** o **Elimina**.

Non hai ancora riunioni? Se non hai collegato un calendario, **Collega il tuo calendario** apre Connessioni. Collega [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) o [un altro calendario](other-calendars.md).

## Sovrapposizioni con l'altro calendario

Quando una riunione di lavoro si sovrappone a un evento del tuo calendario personale, o viceversa, The Machine crea un'attività relativa a quello dei due eventi più recente. Può preparare una breve nota per spostare l'evento o proporti di rifiutarlo. Non viene inviato nulla finché non approvi.

Gli eventi di tutto il giorno, quelli con stato libero e quelli provvisori non vengono mai considerati. Ogni sovrapposizione viene segnalata una sola volta. Un'attività di Lavoro indica solo che c'è un conflitto, così il tuo team non vede mai l'evento personale. Solo tu puoi vedere con quale evento si sovrappone.

## Preparati per le riunioni

Prima di una riunione con persone esterne alla tua azienda, The Machine crea un'attività: **Preparati per** la riunione. È un breve briefing:

- **Chi:** chi sono, in base a Graph.
- **Ultimo contatto:** il tuo ultimo scambio con loro. Dopo la riunione, quel messaggio diventa l'origine dell'attività.
- **Promesse aperte:** ciò che tu o loro dovete ancora fare.
- **Domande aperte:** ciò che è ancora senza risposta.
- **Da decidere o portare:** ciò che devi definire o portare con te.

L'attività arriva la mattina di un giorno lavorativo: il giorno della riunione se si svolge nel pomeriggio, altrimenti il giorno lavorativo precedente. Vengono usate solo le informazioni già presenti sulla tua Machine. È solo da leggere: tocca **Fatto** quando l'hai letta. Le promesse o le domande che richiedono un'azione hanno una propria attività.

Se non ci sono informazioni utili, non viene creata alcuna attività. Le riunioni ricorrenti, interne, personali o rifiutate non ne ricevono una. Se una riunione viene spostata, la sua unica attività rimane e viene aggiornata al nuovo orario. Un'attività che hai scartato non ricompare; quella di una riunione annullata si chiude automaticamente.

Nei dettagli della riunione, la sua attività appare sotto **Attività**. Tocca una volta per aprire la chat.
