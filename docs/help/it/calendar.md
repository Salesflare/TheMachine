---
title: Calendario
area: calendar
summary: La settimana che ti aspetta, in un unico posto: riunioni, attività in scadenza, attività posticipate e promesse.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py
order: 1
translated: 7187a83e373922b3
---
## Cosa mostra

I tuoi giorni, da oggi in poi, con:

- le riunioni dei calendari che hai collegato,
- le attività in scadenza quel giorno e quelle posticipate nel giorno in cui tornano,
- i promemoria sul lavoro che hai delegato,
- le promesse con una data.

Una riunione presente in due calendari compare una sola volta. Un calendario condiviso con te mostra gli eventi di chi l'ha condiviso in tono attenuato, con il suo nome; questi eventi non generano mai attività. Gli eventi che durano tutto il giorno o più giorni vengono mostrati come eventi di tutto il giorno, per ogni giorno interessato.

Un piano concordato insieme è un'unica promessa, contrassegnata da «Con» e dal nome dell'altra persona. Una promessa legata a una riunione di quel giorno con la stessa persona compare nella riga della riunione.

**In ritardo** compare per primo. Una riunione con un'attività aperta mostra il relativo stato: **Preparazione pronta**, **In preparazione** o **Attività**. Un'attività che sembra completata (hai già risposto oppure la sua esecuzione ha rilevato che è già completata) non viene mostrata come **Scadenza**.

## Agenda, settimana o mese

- **Agenda** elenca i singoli giorni. Scorri verso il basso per vedere i giorni successivi o verso l'alto (oppure tocca **Mostra giorni precedenti**) per quelli passati. Risale a una settimana prima di quando hai collegato il calendario e una riga in alto indica da quale giorno. Quando è disponibile la [cronologia](history.md), risale a circa un anno fa.
- **Settimana** mostra una griglia dal lunedì alla domenica. Sul telefono mostra tre giorni.
- **Mese** mostra tutto il mese. Sul computer mostra fino a tre elementi al giorno; sul telefono mostra dei puntini e, toccandone uno, elenca gli elementi del giorno.

**Oggi**, ‹ e › in alto ti permettono di spostarti tra le settimane o i mesi. La vista che scegli viene salvata su quel dispositivo.

Nella griglia settimanale, gli eventi alla stessa ora sono affiancati e restano leggibili. Gli altri sono raggruppati sotto **+N**; toccalo per aprire quel giorno nell'agenda.

## Apri un elemento

Seleziona una riga per aprire la chat dell'attività, la promessa o la riunione. Per una riunione che non puoi modificare qui, per esempio quella di un'altra persona o con invitati, vengono mostrati i dettagli: quando, dove e chi. Le persone conosciute dal tuo Graph e le organizzazioni e i progetti associati alla riunione sono link alle rispettive pagine. **Apri in Google Calendar** (oppure **Apri in Outlook**) sotto ai dettagli apre la riunione lì. Aprirla non cambia nulla.

Una sala riunioni prenotata per una riunione compare sotto Dove, mai come persona né nel tuo Graph.

Un link alla riunione viene mostrato con il nome del servizio, per esempio Zoom, Google Meet o Teams, oppure come **Videochiamata**. Apri la riunione per partecipare.

## Note e trascrizione della riunione

I dettagli di una riunione hanno due sezioni. **Note** è il riepilogo: decisioni e attività da svolgere. **Trascrizione** riporta parola per parola ciò che è stato detto. All'inizio è chiusa e ne viene mostrata la durata; tocca **Mostra** per aprirla.

Se non si caricano, il sistema prova di nuovo automaticamente per circa mezzo minuto. Poi tocca **Riprova**.

Le due sezioni hanno ciascuna le proprie opzioni **Aggiungi note** o **Aggiungi trascrizione**, **Carica file** per un file Markdown o di testo, **Modifica** e **Rimuovi** (tocca due volte). Il contenuto di una sezione resta lì. In una riunione che puoi modificare, **Note** sotto il modulo apre le note.

Se hai collegato [Zoom](zoom.md) o [Google Meet](google-meet.md), le note del servizio compaiono in Note e la trascrizione in Trascrizione, con l'indicazione **Da Zoom** o **Da Google Meet**. Non sostituiscono mai ciò che hai aggiunto: se sono presenti entrambe, vengono mostrate entrambe.

Le note possono anche arrivare dall'evento della riunione nel calendario, se aggiunte dopo l'inizio, oppure via email da Zoom o Gemini. Dopo la riunione, The Machine crea attività a partire dalle note solo se contengono passi successivi chiari. Se le stesse note arrivano in due modi, viene creata una sola attività, con la riunione come origine: **Note dalla** riunione.

Se una riunione ha una trascrizione ma non le note, è disponibile **Genera note**. The Machine le scrive a partire dalla trascrizione: un breve riepilogo, le decisioni e le attività da svolgere con l'indicazione di chi se ne occupa, nella lingua della riunione.

Viene mostrato **Sto scrivendo le note…** e la scrittura continua anche se chiudi la riunione. Per una riunione lunga possono servire alcuni minuti; viene usato il tuo modello. Le note riportano **Scritto da The Machine** e non sostituiscono mai quelle che hai aggiunto.

Puoi anche chiedere a The Machine di aggiungerle. Per esempio, chiedile in un'attività: «aggiungi questa trascrizione alla riunione del consiglio di oggi». Una trascrizione viene inserita in Trascrizione, un riepilogo in Note. Nel Calendar, una riunione con note o trascrizione mostra **Note** o **Trascrizione**.

The Machine legge entrambe per individuare le attività successive alla riunione. Sono di lavoro o personali, come la riunione, e vengono condivise con il team solo se lo è anche la riunione.

Puoi aprire i dettagli di una riunione ovunque la trovi: nella cronologia, nei risultati di ricerca dei messaggi o come origine di un'attività. **Invito originale** in fondo mostra l'invito così come è arrivato.

## Aggiungi o modifica un evento

Da qui puoi modificare il tuo calendario Google. Outlook e gli altri calendari sono di sola lettura. **Nuovo evento** ne aggiunge uno (sul telefono, lo trovi sotto **+** nella barra in alto): scegli il calendario, il titolo e l'ora. Seleziona un evento senza invitati in quel calendario per modificarlo o per **Elimina**rlo (tocca due volte).

**Dove** suggerisce luoghi mentre scrivi: prima quelli che hai già usato e le tue organizzazioni, poi gli indirizzi di [OpenStreetMap](https://www.openstreetmap.org), una mappa gratuita. Per cercarli vengono inviate solo le parole che scrivi. Scegli un suggerimento o mantieni il testo che hai inserito.

**Invita** aggiunge persone dal tuo Graph o qualsiasi indirizzo email. Questa opzione è disponibile solo nel tuo calendario. Le persone che riceveranno un invito sono elencate sopra il pulsante, che indica quante sono: **Aggiungi e invita 2**. Google invia gli inviti quando tocchi il pulsante, non prima. Se non ci sono invitati, non viene invitato né aggiornato nessuno.

Un'attività può anche suggerirti una modifica, per esempio aggiungere un ritiro. Vengono mostrati esattamente i cambiamenti; solo toccando **Aggiungi**, **Salva** o **Elimina** li applichi.

Non hai ancora riunioni? Se non hai un calendario, **Collega il tuo calendario** apre Connessioni: collega [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) o [un altro calendario](other-calendars.md).

## Conflitti con l'altro calendario

Quando una riunione di lavoro si sovrappone a un evento nel tuo calendario personale, o viceversa, The Machine crea un'attività per l'evento più recente. Può preparare una breve nota per spostarlo oppure offrirti di rifiutarlo. Non viene inviato nulla finché non approvi.

Gli eventi di tutto il giorno, quelli con stato libero o provvisorio non vengono considerati; inoltre ogni conflitto viene segnalato una sola volta. Un'attività di lavoro segnala solo che c'è un conflitto, così il tuo team non vede mai l'evento personale. Solo tu puoi vedere con quale evento si sovrappone.

## Preparati per le riunioni

Prima di una riunione con persone esterne alla tua azienda, The Machine crea un'attività: **Preparati per** la riunione. È un breve promemoria:

- **Chi:** chi sono, secondo il tuo Graph.
- **Ultimo contatto:** il tuo ultimo scambio con loro. Dopo la riunione, quel messaggio diventa l'origine dell'attività.
- **Promesse aperte:** cosa resta da fare a te o a loro.
- **Domande aperte:** cosa è ancora senza risposta.
- **Da decidere o portare:** cosa definire o portare con te.

Arriva la mattina di un giorno lavorativo: il giorno della riunione se è nel pomeriggio, altrimenti il giorno lavorativo precedente. Usa solo le informazioni già presenti nella tua Machine. Serve solo per essere letta: tocca **Fatto** quando l'hai letta. Un'attività o una domanda che richiede un'azione ha una sua attività dedicata.

Se non ci sono informazioni utili, non viene creata alcuna attività. Le riunioni ricorrenti, interne, personali o rifiutate non ne ricevono una. Se una riunione viene spostata, la sua attività resta la stessa e viene aggiornata all'ora nuova. Un'attività scartata non ricompare; quella di una riunione annullata si chiude automaticamente.

I dettagli della riunione mostrano la relativa attività sotto **Attività**; toccala per aprirne la chat.
