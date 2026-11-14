---
title: Persone
area: graph
summary: Tutte le persone con cui sei in contatto: la loro pagina, il riepilogo e la cronologia, e come aggiungere, modificare, unire o eliminare una persona.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 26845dd199228f90
---
Tutte le persone con cui sei in contatto, dalle più vicine in poi, tra messaggi e riunioni. Newsletter, ricevute e altre email automatiche non aggiungono nessuno finché non rispondi. Le trovi in Mittenti nascosti, sotto l’elenco: **Mostra come persona** aggiunge una persona. Campi, tag e importazioni funzionano allo stesso modo in tutti e tre gli elenchi, e ogni elenco ha i propri filtri: vedi [The Graph](graph.md).

Una casella condivisa (info@, assistenza clienti, il nome di un negozio) è associata alla sua organizzazione, non a una persona, anche dopo che le hai scritto.

## La pagina di una persona

Inizia con foto, nome, titolo, organizzazione e luogo, seguiti da una riga che descrive il vostro rapporto ("Vi sentite ogni giorno · ultimo contatto ieri · prossima riunione mar 27 ott"). Il contatto recente è indicato come "proprio ora", "3 ore fa", "ieri" o "3 giorni fa"; per i contatti più vecchi viene mostrata una data. Passaci sopra con il puntatore per vedere la data esatta. Sotto trovi:

- **Contatto**: numeri di telefono e indirizzi email. Tocca un numero o un indirizzo per chiamare o scrivere, oppure **Copia**. Qui trovi anche il **Compleanno** e la sua fonte (Google contacts, Google Calendar, Facebook, le tue note o tu): vedi [The Graph](graph.md#birthday).
- **Con te**: che ruolo ha per te, se è un contatto di Lavoro o Personale e se fa parte della tua famiglia o del tuo Fleet, con **Vedi in Fleet**.
- **Anche su**: gli altri luoghi in cui parli con questa persona. **Slack** apre il suo profilo su Slack oppure la chat più recente che avete su Slack.
- **Persone** e **Progetti** di cui fa parte, **In sospeso tra voi** (promesse in entrambe le direzioni, con **Segna come fatto** e **Lascia perdere**) e la sua **Cronologia**.

Gli indirizzi e le chat di una persona vengono collegati automaticamente quando è chiaro che appartengono alla stessa persona, per esempio un indirizzo email di lavoro con il suo indirizzo personale in CC.

Se una pagina mostra **Impossibile caricare questa pagina.**, tocca **Riprova**. Se il messaggio continua a comparire, usa **Qualcosa non va?** in fondo alla pagina.

## Riepilogo

Poche righe all’inizio della pagina di una persona: cosa è stato deciso, chiesto, pianificato o promesso, con i nomi di tutte le persone coinvolte. The Machine lo riscrive quando ci sono novità, solo per le persone con cui sei davvero in contatto, e controlla prima ogni riga. Di solito una volta al giorno, oppure entro poche ore se cambia qualcosa che la riguarda, per esempio una nuova scadenza o una richiesta ritirata.

Le righe vaghe vengono tralasciate. Se non c’è niente di specifico da dire, il riepilogo non viene mostrato. Ogni riga rimanda alla fonte: i messaggi dello stesso giorno sono raggruppati sotto un’unica data, con il relativo conteggio, e si aprono insieme.

**Modifica** il riepilogo per esprimerti a modo tuo. Quando ci sono novità, The Machine mostra un **Aggiornamento suggerito**, con le opzioni **Usalo** e **Tieni la mia**. **Lascia che lo scriva The Machine** per affidarle di nuovo il riepilogo.

La preparazione delle riunioni usa il riepilogo, ma solo le righe relative a quell’attività (di Lavoro o Personale). Resta sulla tua Machine: il tuo team non la vede.

## Cronologia

Ogni pagina di una persona o di un’organizzazione ha una cronologia, dalla più recente: email, riunioni e relativi riepiloghi Zoom, conversazioni Intercom (con **Apri in Intercom**), chat WhatsApp, Telegram, Slack, LinkedIn e X, attività, promesse e aggiornamenti sui progetti. I filtri in alto mostrano una fonte alla volta. **Mostra altro** carica gli elementi meno recenti.

Le riunioni future sono in cima, in **In arrivo**, dalla più vicina in poi. **Mostra tutti i prossimi** mostra anche le altre. Per ogni riunione è indicato chi ha partecipato, una sola volta per persona. Se ci sono note o una trascrizione, trovi **Note** o **Trascrizione**: fai clic per leggerle.

Le tue cronologie sono private: Graph del team mostra solo ciò che consentono le tue regole di condivisione. In una pagina, **Team**, sopra la Cronologia, aggiunge i contenuti condivisi dai colleghi e indica chi li ha condivisi. **Miei** mostra solo i tuoi.

## Lavoro e Personale

Le schede **Lavoro** e **Personale** elencano le persone in base al loro Tipo, indicato nella pagina. La tua scelta (**Modifica**) ha la precedenza. Altrimenti, la tua famiglia e i tuoi amici, e le persone che sono tue amiche o fanno parte della tua famiglia (una moglie, un padre), sono considerate Personali, a prescindere dall’indirizzo da cui scrivono. Il tuo team non vede i contatti Personali.

## Aggiungere una persona

Tocca **Nuova persona** in cima a Persone, oppure **+** nella barra in alto sul telefono. Inserisci un nome e, se li hai, un indirizzo email e un’organizzazione. Se nel tuo Graph c’è già una persona simile, il modulo la mostra per prima, così puoi aprire la scheda esistente. **Aggiungi** apre la nuova pagina.

Una persona che aggiungi resta nell’elenco anche se non ci sono ancora messaggi. Il suo primo messaggio la collega agli altri dati.

## Modificare una persona

**Modifica**, in cima alla pagina, ti permette di cambiare nome, titolo, organizzazione, luogo, LinkedIn, numeri di telefono e indirizzi email, il suo ruolo per te e se è di Lavoro o Personale. Il campo **Note** serve per ricordare ciò che vuoi; le note restano anche dopo un’unione. **Salva** applica le modifiche, **Annulla** le scarta.

Le tue modifiche restano anche quando i suoi dati vengono cercati di nuovo, e dopo **Unisci** e **Annulla**. Svuota un campo per usare di nuovo il valore trovato. Se svuoti il nome, viene ripristinato quello usato nei suoi messaggi.

Per cambiare la foto, fai clic su di essa: **Carica un’immagine**, scegli una foto trovata per quella persona oppure **Rimuovi foto**. La foto resta sulla tua Machine.

## Unire due persone

Quando due persone potrebbero essere la stessa, la loro pagina chiede se sono la stessa persona e Persone le mostra sotto **Stessa persona?**. **Unisci** le collega, includendo tutti i messaggi, le note, i ruoli e i progetti. **Non è la stessa** le tiene separate in modo permanente. La tua risposta resta visibile per un po’ sulla coppia, che poi scompare dall’elenco. L’elenco scompare quando non ci sono più domande.

Una persona con un indirizzo che somiglia soltanto a uno che conosci, come acme-corp.example rispetto a acmecorp.example, non viene mai proposta come la stessa persona; solo tu puoi assegnarle un ruolo.

Un indirizzo condiviso, come info@ o una mailing list, non viene mai collegato alle persone che lo usano per scrivere. Un contatto di lavoro esterno alla tua azienda e una chat personale che hanno in comune solo il nome non vengono collegati automaticamente: vengono proposti come coppia da verificare.

**Unisci tutti** unisce subito tutte le coppie nell’elenco, tranne quelle che hai contrassegnato con **Non è la stessa**. Se tocchi subito **Annulla**, le separi di nuovo tutte.

Per unire due persone manualmente, apri la pagina di una, poi **⋯**, **Stessa persona di…** e scegli l’altra. Nella pagina della persona unita trovi il motivo sotto **Unita da**, con **Annulla** per separarle di nuovo.

## Eliminare definitivamente una persona

Nella sua pagina, apri il menu ⋯ e scegli **Elimina definitivamente…**, poi **Elimina**. La persona e tutte le informazioni che la tua Machine conosce su di lei vengono rimosse: la scheda, gli indirizzi, i dettagli trovati, i messaggi scambiati solo tra voi e le note che la riguardano.

Le attività che la coinvolgono restano, ma senza il suo nome. Non verrà aggiunta di nuovo, neanche tramite un’importazione o un’attività sui compleanni di Facebook che include il suo nome o indirizzo. L’operazione non si può annullare.

## Email respinta

Quando un’email inviata a una persona viene respinta, accanto al suo indirizzo compare **Respinta** con la data, e un suo altro indirizzo viene mostrato per primo. Le nuove bozze non vengono mai inviate a quell’indirizzo se ne è noto un altro. Se è il suo unico indirizzo, il foglio di invio ti avvisa, ma puoi comunque inviare l’email.

Un’email risulta respinta se il server di posta dice che l’indirizzo non esiste, oppure dopo 3 errori temporanei nell’arco di una settimana. L’avviso scompare quando la persona scrive di nuovo da quell’indirizzo o quando un’email inviata lì viene recapitata.

## Titolo professionale e foto

Le persone con un indirizzo aziendale hanno un titolo professionale, una foto, LinkedIn e la città, cercati come i [dati dell’organizzazione](organization-data.md). Su una Machine ospitata, la ricerca usa solo il loro nome e il dominio aziendale. Per una foto, Gravatar riceve l’hash del loro indirizzo di lavoro, mai l’indirizzo stesso. Puoi disattivare questa funzione in **Impostazioni**, nella sezione Sicurezza: **Cerca i contatti di lavoro**.

Se la ricerca trova queste informazioni, nella pagina della persona compaiono anche la descrizione, da quando ricopre il ruolo attuale e i due ruoli precedenti. Anche le preparazioni le usano, ma mostrano la descrizione solo se la persona non ha una biografia propria.

Le tue connessioni aggiungono informazioni che hanno già letto: titolo, telefono e fuso orario da Slack; biografia e luogo da X; titolo professionale e foto da LinkedIn; titoli professionali da Google contacts e Salesflare; e la foto di un contatto da Salesflare, se ne conserva una. Passa il puntatore sulla riga sotto il nome per vedere da dove provengono le informazioni.

Outlook aggiunge le foto dei colleghi della tua organizzazione e dei tuoi contatti Outlook, oltre ai titoli professionali e alle aziende dei tuoi contatti ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Le foto WhatsApp e Telegram arrivano tramite la sincronizzazione di WhatsApp e la connessione alle chat Telegram: fino a 50 al giorno per ciascun servizio, solo per le persone già presenti nel tuo Graph. A loro non viene inviato nulla. Un’importazione dei compleanni di Facebook aggiunge la foto del profilo delle persone senza foto quando la salvi ([Routine](routines.md)). Tutto resta sulla tua Machine.

Nel [Team Graph](team-graph.md) di un Fleet di Lavoro, una piccola copia della foto professionale viene inclusa nel profilo condiviso di una persona. Le foto da Google contacts, WhatsApp, Telegram o Facebook, e quelle che hai modificato o rimosso, non vengono mai condivise.

## Su di te

I tuoi indirizzi e numeri, compresi gli alias, appartengono sempre a te e non sono mai una persona nel tuo Graph. Se cerchi te stesso o aggiungi una persona con uno dei tuoi indirizzi, si apre **Su di te**; un’importazione salta la tua riga.

Su di te elenca i tuoi indirizzi e la relativa fonte. Puoi modificarli in **Impostazioni**, nella sezione Account. Per inviare il tuo contatto a un collega o a un amico, scegli **Condividi il mio contatto**. Vedi [Condividere un contatto](share-contact.md).

## Che ruolo ha per te

I ruoli che la tua Machine individua nei tuoi messaggi compaiono nella sua pagina sotto **Per te**, insieme alla frase da cui sono stati dedotti. Non serve che tu li confermi. Se un ruolo è sbagliato, correggilo con **Modifica** nella pagina oppure con **⋯** sulla relativa riga in **Modifiche recenti**. La Machine impara dalle tue modifiche.

## Cosa sa di una persona

Le informazioni su una persona si trovano nella sua pagina, sotto **Informazioni note**; Apprendimento raccoglie quelle generali. Tocca **Aggiungi** per aggiungerne una con parole tue. Ogni informazione ha un menu:

- **Modifica** per cambiarla direttamente.
- **Non riguarda** la persona per renderla di nuovo un’informazione generale, sotto **Apprendimento**, **Fatti**.
- **Rimuovi** per eliminarla ovunque.

## Modifiche recenti

**Modifiche recenti**, nella sezione a scomparsa subito sopra la cronologia di una persona, organizzazione o progetto, elenca cosa ha modificato o appreso la tua Machine: un ruolo, dove lavora una persona, il legame tra due persone, un’informazione o un cambiamento di progetto. Ogni riga mostra la data e la fonte; tocca la fonte per leggere il messaggio.

Se una riga è sbagliata, puoi correggerla direttamente con **⋯**: **Modifica**, **Rimuovi**, **Non riguarda** la persona oppure **Annulla** per riportare un progetto alla posizione precedente. Vengono mostrate tre righe; **Mostra altro** mostra le altre.

Le persone aggiornate oggi dalla tua Machine hanno un puntino nell’elenco Persone, mentre **4 persone aggiornate oggi** in cima all’elenco indica chi sono. Vedi [The Graph](graph.md).

## Un’attività su una persona

**Nuova attività** nel menu **⋯** di una persona, organizzazione o progetto crea un’attività che la riguarda.
