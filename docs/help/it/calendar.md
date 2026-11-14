---
title: Calendario
area: calendar
summary: La settimana che arriva in un solo posto: riunioni, attività in scadenza, attività posticipate e promesse.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py
order: 1
translated: 0f6b54ba94a7cdcc
---
## Cosa mostra

I tuoi giorni da oggi in poi, con:

- le riunioni dai calendari che hai collegato,
- le attività in scadenza quel giorno, e le attività posticipate nel giorno in cui tornano,
- i controlli sul lavoro che hai passato ad altri,
- le promesse con una data.

Una riunione presente su due calendari compare una volta sola. Un calendario che qualcuno ha condiviso con te mostra i suoi eventi attenuati, con il nome di quella persona; quelli non generano mai un’attività. Gli eventi di un giorno intero o di più giorni compaiono come giornata intera, in ogni giorno che coprono.

Un piano fatto insieme è una sola promessa, segnata "Con" e il nome dell’altra persona. Una promessa su una riunione di quel giorno con la stessa persona sta sulla riga di quella riunione.

**In ritardo** viene per primo. Una riunione con un’attività aperta la mostra: **Preparazione pronta**, **In preparazione** o **Attività**. Un’attività che sembra fatta (hai già risposto, o la sua esecuzione l’ha trovata fatta) non appare con una **Scadenza**.

## Agenda, settimana o mese

- **Agenda** elenca ogni giorno. Scorri in basso per i giorni successivi, in alto (o **Mostra giorni precedenti**) per quelli precedenti. Arriva fino a una settimana prima che collegassi il calendario, e una riga in alto dice da quale giorno. Quando arriva la sua [cronologia](history.md), torna indietro di circa un anno.
- **Settimana** mostra una griglia, da lunedì a domenica. Su un telefono mostra tre giorni.
- **Mese** mostra il mese intero. Un computer mostra fino a tre elementi al giorno; un telefono mostra dei punti, e un tocco elenca quel giorno.

**Oggi**, ‹ e › in alto scorrono le settimane o i mesi. La vista scelta viene ricordata su quel dispositivo.

Nella griglia della settimana, gli eventi alla stessa ora stanno affiancati finché restano leggibili. Gli altri compaiono come **+N**, che apre quel giorno nell’agenda.

## Apri qualcosa

Fai clic su una riga per aprire la chat della sua attività, la promessa o la riunione nel suo calendario. In una riunione, chi il tuo Graph conosce, e le organizzazioni e i progetti di cui tratta, sono link alla loro pagina. Guardare non cambia nulla.

Una sala riunioni prenotata compare nel luogo, mai come persona né nel tuo Graph.

Un link alla riunione compare come il suo servizio, come Zoom, Google Meet o Teams, o come **Videochiamata**. Apri la riunione per partecipare.

## Note e trascrizione della riunione

I dettagli di una riunione hanno due parti. **Note** è il riepilogo: decisioni e azioni. **Trascrizione** è ciò che è stato detto, parola per parola. All’inizio è chiusa, con la sua durata; **Mostra** la apre.

Se non si caricano (per esempio mentre la tua Machine si riavvia), la riunione riprova da sola per circa mezzo minuto, e di nuovo quando torni alla finestra. Dopo lo dice, con **Riprova**.

Ognuna ha il suo **Aggiungi note** o **Aggiungi trascrizione**, **Carica file** per un file Markdown o di testo, **Modifica** e **Rimuovi** (tocca due volte). Quello che va in una resta lì. Su una riunione che puoi modificare, **Note** sotto il suo modulo le apre.

Con [Zoom](zoom.md) o [Google Meet](google-meet.md) collegato, le sue note compaiono in Note e la sua trascrizione in Trascrizione, segnate **Da Zoom** o **Da Google Meet**. Non sostituiscono mai ciò che hai aggiunto: quando ci sono entrambi, si vedono entrambi.

Le note possono anche essere nell’evento del calendario stesso, aggiunte dopo l’inizio, o arrivare via email da Zoom o Gemini. Dopo la riunione, The Machine ne ricava to-do solo per prossimi passi chiari. Le stesse note arrivate in due modi fanno un solo to-do, con la riunione come fonte: **Note da** e il suo nome.

Una riunione con trascrizione e senza note ha **Genera note**. The Machine le scrive dalla trascrizione: un breve riepilogo, le decisioni e le azioni con chi le fa, nella lingua della riunione.

The Machine mostra **Sto scrivendo le note…** e continua anche se chiudi la riunione; una lunga richiede qualche minuto. Usa il tuo modello e aspetta se raggiungi il limite di utilizzo. Le note riportano **Scritte da The Machine**, non sostituiscono mai quelle che hai aggiunto, e i follow-up nascono da loro come da quelle di Zoom.

Anche The Machine può aggiungerle. Chiediglielo su un’attività, come "aggiungi questa trascrizione al consiglio di amministrazione di oggi". Una trascrizione va in Trascrizione, un riepilogo in Note. Una riunione che le ha mostra **Note** o **Trascrizione** nel calendario.

The Machine le legge entrambe per i passi successivi della riunione. Sono Lavoro o Personali come la riunione, e vanno al tuo team solo quando ci va la riunione.

Una riunione si apre con questi dettagli ovunque la trovi: in una cronologia, in una ricerca tra i messaggi o come fonte di un to-do. **Invito originale** in fondo mostra l’invito così come è arrivato.

## Aggiungi o modifica un evento

Quando un calendario si può modificare da qui, **Nuovo evento** ne aggiunge uno (sul telefono è sotto **+** nella barra in alto): scegli il calendario, un titolo e l’ora. Fai clic su un evento senza invitati in quel calendario per modificarlo, oppure **Elimina** (tocca due volte).

**Dove** suggerisce luoghi mentre scrivi: prima quelli che hai già usato e le tue organizzazioni, poi indirizzi da [OpenStreetMap](https://www.openstreetmap.org) tramite Photon, una ricerca di mappe gratuita. La tua Machine la interroga solo con le parole che hai scritto. Scegline uno o tieni il tuo testo.

**Invita** aggiunge persone dal tuo Graph, o qualsiasi indirizzo email. C’è solo sul tuo calendario. Chi riceve un invito è elencato sopra il pulsante, e il pulsante dice quanti sono: **Aggiungi e invita 2**. Google invia gli inviti quando lo tocchi, non prima. Senza invitati nessuno viene invitato o riceve aggiornamenti.

Anche un’attività può proporre una modifica, come un ritiro da aggiungere. Mostra esattamente cosa cambia, e lo fa solo il tuo **Aggiungi**, **Salva** o **Elimina**.

Ancora nessuna riunione? Senza calendario, **Collega il tuo calendario** apre Connessioni: collega [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) o [un altro calendario](other-calendars.md).

## Sovrapposizioni con l’altro calendario

Quando una riunione di lavoro si sovrappone a qualcosa nel tuo calendario personale, o viceversa, The Machine crea un’attività sul più recente dei due. Può preparare una bozza breve per spostarlo, o proporre di rifiutare. Non parte nulla finché non approvi.

Gli eventi di tutto il giorno, liberi o provvisori non contano mai, e ogni sovrapposizione compare una volta sola. Un’attività di Lavoro dice solo che c’è un conflitto, così il tuo team non vede mai l’evento personale. Solo tu vedi con cosa si sovrappone.

## Pronto per le tue riunioni

Prima di una riunione con persone esterne alla tua azienda, The Machine crea un’attività: **Preparare** la riunione. È un breve briefing:

- **Chi:** chi sono, dal tuo Graph.
- **Ultimo contatto:** il tuo ultimo scambio con loro. Quel messaggio è la fonte dell’attività, dopo la riunione.
- **Promesse aperte:** cosa tu o loro dovete ancora.
- **Domande aperte:** cosa resta senza risposta.
- **Da decidere o portare:** cosa decidere o portare.

Arriva la mattina di un giorno lavorativo: il giorno stesso se la riunione è nel pomeriggio, altrimenti il giorno lavorativo prima. Usa solo quello che è già sulla tua Machine. È solo da leggere: **Fatto** quando l’hai letta. Una promessa o una domanda che richiede qualcosa ha la sua attività.

Senza una storia utile, nessuna attività. Le riunioni ricorrenti, interne, personali e rifiutate non ne hanno. Una riunione spostata tiene la sua unica attività, al nuovo orario. Una scartata non torna, e quella di una riunione annullata si chiude da sola.

I dettagli della riunione mostrano la sua attività sotto **Attività**, a un tocco dalla chat.
