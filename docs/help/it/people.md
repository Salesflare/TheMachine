---
title: Persone
area: graph
summary: Tutte le persone con cui sei in contatto: la loro pagina, il riepilogo e la cronologia, e come aggiungere, modificare, unire o eliminare una persona.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: a16cc66e51a64fd2
---
Tutte le persone con cui sei in contatto, dalle più vicine in poi, in base ai tuoi messaggi e alle riunioni. Newsletter, ricevute e altri invii non aggiungono nessuno finché non rispondi. Le trovi sotto Mittenti nascosti, in fondo all’elenco: **Mostra come persona** aggiunge una persona. Campi, tag e importazioni funzionano allo stesso modo in tutti e tre gli elenchi, ognuno con i propri filtri: vedi [The Graph](graph.md).

Una casella condivisa (info@, assistenza clienti, il nome di un negozio) viene associata alla sua organizzazione, non a una persona, anche dopo che le hai scritto.

## La pagina di una persona

Inizia con la foto, il nome, il ruolo, l’organizzazione e il luogo della persona, seguiti da una riga su come siete in contatto ("Parlate ogni giorno · ultimo contatto ieri · prossima riunione mar 27 ott"). Il contatto più recente è indicato con "proprio ora", "3 ore fa", "ieri" o "3 giorni fa"; i contatti meno recenti mostrano una data. Passaci sopra con il cursore per vedere la data esatta. Sotto trovi:

- **Contatto**: i numeri di telefono e gli indirizzi email. Tocca un numero per chiamare o scrivere, oppure **Copia**. Qui trovi anche il **Compleanno** e la sua fonte (Google Contacts, Google Calendar, Facebook, le tue note o tu): vedi [The Graph](graph.md#birthday).
- **Con te**: che ruolo ha per te, se è un contatto di lavoro o personale e se fa parte della tua famiglia o del tuo Fleet, con **Vedi in Fleet**.
- **Anche su**: gli altri posti in cui parli con questa persona. **Slack** apre la persona in Slack o la tua chat più recente con lei.
- Le **Persone** e i **Progetti** di cui fa parte, le **In sospeso tra voi** (promesse da entrambe le parti, con **Segna come fatto** e **Lascia perdere**) e la sua **Cronologia**.

Gli indirizzi e le chat di una persona vengono uniti automaticamente quando è chiaro che appartengono alla stessa persona, per esempio un’email di lavoro con il suo indirizzo personale in CC.

Se compare il messaggio **Impossibile caricare questa pagina.**, tocca **Riprova**. Se il messaggio continua a comparire, tocca **Qualcosa non va?** in fondo alla pagina.

## Riepilogo

In cima alla pagina di una persona trovi alcune brevi righe su decisioni, richieste, piani o promesse, con i nomi di tutti. The Machine lo riscrive quando ci sono novità, solo per le persone con cui sei davvero in contatto, e controlla ogni riga prima di mostrarla. Di solito una volta al giorno; entro poche ore se cambia qualcosa che la riguarda, per esempio una nuova scadenza o una richiesta ritirata.

Le informazioni vaghe non vengono incluse; se non c’è niente di specifico da dire, il riepilogo non compare. Ogni riga rimanda alla fonte: i messaggi dello stesso giorno sono raggruppati sotto un’unica data, con il numero di messaggi, e si aprono insieme.

Tocca **Modifica** per riscriverlo a modo tuo. Quando ci sono novità, The Machine mostra un **Aggiornamento suggerito** con le opzioni **Usalo** e **Tieni la mia**. **Lascia che lo scriva The Machine** ripristina il testo di The Machine.

La preparazione delle riunioni lo usa, ma solo con le righe che riguardano il lato dell’attività (Lavoro o Personale). Resta sulla tua Machine: il tuo team non lo vede.

## Cronologia

Ogni pagina di una persona o organizzazione ha una cronologia, dalla più recente: email, riunioni e relativi riepiloghi Zoom, conversazioni Intercom (con **Apri in Intercom**), chat WhatsApp, Telegram, Slack, LinkedIn e X, attività, promesse e cambiamenti di progetto. I filtri in cima mostrano una fonte alla volta. **Mostra altro** carica gli elementi meno recenti.

Le riunioni future compaiono in cima sotto **In arrivo**, dalla più vicina in poi. **Mostra tutti i prossimi** mostra le altre. Per ogni riunione sono indicati i partecipanti, una sola volta ciascuno. Quelle con note o trascrizione hanno l’etichetta **Note** o **Trascrizione**; cliccaci per leggerle.

Le tue cronologie sono tue: il Graph del team mostra solo ciò che consentono le tue regole di condivisione. In una pagina, **Team** sopra la Cronologia aggiunge i contenuti condivisi dai colleghi, indicando per ognuno chi li ha condivisi; **Miei** mostra solo i tuoi.

## Lavoro e Personale

Le schede **Lavoro** e **Personale** mostrano le persone in base al loro Tipo, indicato nella pagina. Prevale la scelta che hai fatto tu (**Modifica**). Altrimenti, i tuoi familiari e amici, e i familiari o amici per cui sei tu un familiare o un amico (una moglie, un padre), sono classificati come personali, qualunque sia l’indirizzo da cui scrivono. Il tuo team non vede i contatti personali.

## Aggiungere una persona

Tocca **Nuova persona** in cima alla sezione Persone, oppure **+** nella barra superiore sul telefono. Inserisci un nome e, se li hai, un indirizzo email e un’organizzazione. Se nel tuo Graph c’è già una persona simile, il modulo la mostra per prima, così puoi aprire la scheda esistente. Tocca **Aggiungi** per aprire la nuova pagina.

La persona che aggiungi resta nell’elenco, anche se non ci sono ancora messaggi. Il primo messaggio la collega agli altri.

## Modificare una persona

**Modifica**, in cima alla pagina, ti permette di cambiare nome, ruolo, organizzazione, luogo, LinkedIn, numeri di telefono e indirizzi email, il suo ruolo per te e la classificazione come contatto di lavoro o personale. Nel campo **Note** puoi scrivere quello che vuoi ricordare; le note restano anche dopo un’unione. Tocca **Salva** per conservare le modifiche o **Annulla** per lasciarle come sono.

Le modifiche restano anche quando i dettagli vengono cercati di nuovo, e dopo **Unisci** e **Annulla**. Svuota un campo per usare di nuovo il valore trovato. Se svuoti il nome, viene ripristinato quello dei suoi messaggi.

Per cambiare la foto, cliccaci sopra: **Carica un’immagine**, scegli una delle foto trovate oppure **Rimuovi foto**. La foto resta sulla tua Machine.

## Unire due persone

Quando due persone potrebbero essere la stessa, la pagina chiede se si tratta della stessa persona e la sezione Persone le mostra sotto **Stessa persona?**. **Unisci** le riunisce, includendo tutti i messaggi, le note, i ruoli e i progetti. **Non è la stessa** le tiene separate. La tua risposta compare per un momento sulla coppia, poi la coppia scompare dall’elenco. L’elenco non viene più mostrato quando non ci sono domande.

Una persona con un indirizzo che assomiglia soltanto a uno che conosci, per esempio acme-corp.example rispetto ad acmecorp.example, non viene mai proposta come la stessa persona. Solo tu puoi assegnarle un ruolo.

Un nome da solo non basta mai per unire persone di domini diversi, perché chiunque può scriverlo. Due indirizzi di domini diversi vengono proposti solo se c’è un altro collegamento, per esempio se hanno in comune altre persone o un progetto. Non viene mai proposta una persona che usa il tuo stesso nome con un indirizzo che non è tuo. Aggiungi invece gli altri tuoi indirizzi in Impostazioni, [I tuoi indirizzi](settings.md#your-addresses).

Se tra domini diversi corrisponde solo il nome, come "Sam" e "Sam Lee", le persone vengono proposte solo se hanno lo stesso numero di telefono o profilo LinkedIn.

Un indirizzo condiviso, come info@ o una mailing list, non viene mai unito alle persone che lo usano per scrivere. Un contatto di lavoro esterno alla tua azienda e una chat personale che hanno in comune solo il nome non vengono uniti automaticamente: compaiono come una domanda.

**Unisci tutti** unisce tutte le coppie dell’elenco in una volta, tranne quelle che hai contrassegnato con **Non è la stessa**. Se tocchi **Annulla** subito dopo, le separi di nuovo tutte.

Per unire due persone manualmente, apri una delle loro pagine, poi tocca **⋯**, **Stessa persona di…** e scegli l’altra. Nella pagina della persona unita trovi i motivi sotto **Unita da**, con **Annulla** per separarle di nuovo.

## Eliminare una persona definitivamente

Nella sua pagina, apri il menu ⋯ e scegli **Elimina definitivamente…**, poi **Elimina**. La persona viene rimossa insieme a tutto ciò che la tua Machine sa su di lei: la scheda, gli indirizzi, i dettagli trovati, i messaggi scambiati solo tra voi e le note che la riguardano.

Le attività che la coinvolgono restano, ma il suo nome viene rimosso. Non verrà aggiunta di nuovo, nemmeno tramite un’importazione o un’attività per i compleanni di Facebook con il suo nome o indirizzo. L’eliminazione non si può annullare.

## Email non recapitate

Quando un’email inviata a una persona non viene recapitata, il suo indirizzo mostra **Non recapitata** con la data e un altro suo indirizzo viene messo in cima. Le nuove bozze non vengono mai inviate a quell’indirizzo se ne è noto un altro. Se è l’unico, la schermata di invio ti avvisa, ma puoi comunque inviare l’email.

Un mancato recapito viene registrato quando il server di posta comunica che l’indirizzo non esiste, oppure dopo 3 errori temporanei nell’arco di una settimana. Viene cancellato quando la persona scrive di nuovo da quell’indirizzo o quando un’email viene recapitata correttamente.

## Ruolo e foto

Alle persone con un indirizzo aziendale vengono assegnati un ruolo, una foto, un profilo LinkedIn e una città, cercati come [i dettagli dell’organizzazione](organization-data.md). Su una Machine ospitata, la ricerca usa solo il loro nome e il dominio aziendale. Per la foto, Gravatar riceve l’hash dell’indirizzo di lavoro, mai l’indirizzo stesso. Puoi disattivare questa opzione in **Impostazioni**, nella sezione Sicurezza: **Cerca i contatti di lavoro**.

Quando la ricerca trova queste informazioni, la pagina mostra anche la descrizione personale, da quando la persona ricopre il ruolo attuale e i due ruoli precedenti. Anche la preparazione delle riunioni usa queste informazioni; la descrizione personale viene inclusa solo se la persona non ha una biografia.

Le informazioni sui tuoi contatti si arricchiscono anche con quelle che hanno già condiviso: ruolo, telefono e fuso orario da Slack; biografia e luogo da X; titolo e foto da LinkedIn; ruoli da Google Contacts e Salesflare; e la foto di un contatto da Salesflare, se viene conservata lì. Passa il cursore sulla riga sotto il nome per vedere la fonte.

Outlook aggiunge le foto dei colleghi della tua organizzazione e dei tuoi contatti Outlook, oltre ai ruoli e alle aziende dei tuoi contatti ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Le foto di WhatsApp e Telegram vengono aggiunte tramite la sincronizzazione di WhatsApp e la connessione alle chat di Telegram: fino a 50 al giorno per ciascun servizio, solo per le persone già presenti nel tuo Graph. Non viene inviato loro niente. Un’importazione dei compleanni di Facebook aggiunge la foto del profilo di una persona senza foto quando la salvi ([Routine](routines.md)). Tutto resta sulla tua Machine.

Nel [Team Graph](team-graph.md) di un Fleet di lavoro, una copia ridotta di una foto di lavoro viene aggiunta alla scheda condivisa della persona. Non vengono mai condivise le foto da Google Contacts, WhatsApp, Telegram o Facebook, né le foto che hai modificato o rimosso.

## Su di te

I tuoi indirizzi e numeri, inclusi gli alias, corrispondono sempre a te, mai a una persona nel tuo Graph. Se cerchi te stesso o aggiungi una persona con uno dei tuoi indirizzi, si apre **Su di te**. Le importazioni saltano la tua riga.

La pagina Su di te mostra i tuoi indirizzi e la relativa fonte. Puoi modificarli in **Impostazioni**, nella sezione Account. Per inviare i tuoi contatti a un collega o un amico, scegli **Condividi il mio contatto**. Vedi [Condividere un contatto](share-contact.md).

## Il suo ruolo per te

I ruoli che la tua Machine riconosce nei tuoi messaggi compaiono nella pagina sotto **Per te**, con solo le parole che indicano il ruolo, come un titolo. Dire che qualcuno è il tuo commercialista o cliente non basta: serve anche qualcosa da parte tua, come i tuoi messaggi o le riunioni con quella persona. Non devi confermare niente. Hai trovato un errore? **Modifica** nella sua pagina lo corregge, oppure tocca **⋯** sulla riga in **Modifiche recenti**. La tua Machine impara dalle tue modifiche.

## Cosa sa su una persona

Le informazioni su una persona si trovano nella sua pagina, sotto **Informazioni note**; la sezione Apprendimento raccoglie quelle generali. Tocca **Aggiungi** per aggiungerne un’altra con parole tue. Ogni informazione ha un menu:

- **Modifica** la modifica direttamente.
- **Non riguarda questa persona** la trasforma di nuovo in un’informazione generale, sotto **Apprendimento**, **Fatti**.
- **Rimuovi** la elimina ovunque.

## Modifiche recenti

**Modifiche recenti**, nella sezione chiusa appena sopra la cronologia di una persona, organizzazione o progetto, mostra ciò che la tua Machine ha modificato o appreso: un ruolo, il luogo di lavoro, il legame tra due persone, un’informazione o un cambiamento di progetto. Ogni riga indica la data e la fonte; tocca la fonte per leggere il messaggio.

Se una riga non è corretta, il menu **⋯** ti permette di modificarla direttamente: **Modifica**, **Rimuovi**, **Non riguarda questa persona** oppure **Annulla** per ripristinare la posizione precedente di un progetto. Vengono mostrate tre righe; **Mostra altro** apre le altre.

Una persona aggiornata oggi dalla tua Machine è contrassegnata da un puntino nell’elenco Persone. In cima all’elenco, **4 persone aggiornate oggi** indica chi sono. Vedi [The Graph](graph.md).

## Un’attività su una persona

**Nuova attività** nel menu **⋯** di una persona, organizzazione o progetto crea un’attività che la riguarda.
