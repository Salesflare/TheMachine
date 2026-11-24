---
title: Persone
area: graph
summary: Tutte le persone con cui sei in contatto: la loro pagina, il riepilogo e la cronologia, e come aggiungere, modificare, unire o eliminare una persona.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: b23d3ebdc4f162f2
---
Tutte le persone con cui sei in contatto, dalle più vicine in poi, in base ai messaggi e alle riunioni. Newsletter, ricevute e altre comunicazioni non aggiungono nessuno finché non rispondi. Si trovano in Mittenti nascosti, sotto l’elenco: **Mostra come persona** aggiunge una persona all’elenco. Campi, tag e importazioni funzionano allo stesso modo in tutti e tre gli elenchi, ognuno con i propri filtri: vedi [Il Graph](graph.md).

Una casella di posta condivisa (info@, assistenza clienti, il nome di un negozio) viene associata alla sua organizzazione, non a una persona, anche dopo che le scrivi.

## La pagina di una persona

Inizia con la foto, il nome, il titolo, l’organizzazione e il luogo della persona, più una riga che descrive il vostro rapporto ("Parlate ogni giorno · ultimo contatto ieri · prossima riunione mar 27 ott"). Il contatto più recente è indicato come "proprio ora", "3 ore fa", "ieri" o "3 giorni fa", mentre per i contatti più vecchi è indicata la data. Passaci sopra con il cursore per vedere la data esatta. Sotto trovi:

- **Contatto**: numeri di telefono e indirizzi email. Tocca un numero per chiamare o un indirizzo per scrivere, oppure **Copia**. Qui trovi anche il **Compleanno**, con l’indicazione della fonte (Contatti Google, Google Calendar, Facebook, le tue note o tu): vedi [Il Graph](graph.md#birthday).
- **Con te**: che ruolo ha per te, se è un contatto di Lavoro o Personale e se fa parte della tua Fleet di famiglia o di lavoro, con **Vedi in Fleet**.
- **Anche su**: gli altri servizi su cui parli con questa persona. **Slack** apre la persona in Slack o la conversazione più recente che avete avuto su Slack.
- Le **Persone** e i **Progetti** di cui fa parte, gli **In sospeso tra voi** (promesse da entrambe le parti, con **Segna come fatto** e **Lascia perdere**) e la **Cronologia**.

Gli indirizzi e le chat di una persona vengono associati automaticamente quando è chiaro che appartengono alla stessa persona, per esempio un’email di lavoro con il suo indirizzo personale in CC. Lo stesso vale quando qualcuno con cui chatti prenota una chiamata tramite il link che gli hai inviato e l’azienda o il cognome corrispondono.

Se la pagina mostra **Impossibile caricare questa pagina.**, tocca **Riprova**. Se il messaggio continua a comparire, tocca **Qualcosa non va?** in fondo alla pagina.

## Riepilogo

Poche righe all’inizio della pagina di una persona, che riassumono decisioni, domande, piani e promesse e indicano i nomi di tutte le persone coinvolte. The Machine lo riscrive quando ci sono novità, solo per le persone con cui sei davvero in contatto, e prima controlla ogni riga. Di solito una volta al giorno; entro poche ore se cambia qualcosa che riguarda quella persona, come una nuova scadenza o una richiesta ritirata.

Le informazioni vaghe vengono escluse: se non c’è niente di specifico da dire, il riepilogo non viene mostrato. Ogni riga rimanda alla fonte. I messaggi dello stesso giorno condividono una data e mostrano il numero di messaggi; toccali per aprirli tutti.

Tocca **Modifica** per riscriverlo a modo tuo. Quando ci sono novità, The Machine mostra un **Aggiornamento suggerito**, con le opzioni **Usalo** e **Tieni la mia**. **Lascia che lo scriva The Machine** ripristina il riepilogo scritto da The Machine.

La preparazione delle riunioni usa il riepilogo, ma solo le righe pertinenti al contesto dell’attività, Lavoro o Personale. Resta sulla tua Machine: il team non può vederlo.

## Cronologia

Ogni pagina di una persona o organizzazione ha una cronologia, dalla più recente alla meno recente: email, riunioni e relativi riepiloghi Zoom, conversazioni Intercom (con **Apri in Intercom**), chat WhatsApp, Telegram, Slack, LinkedIn e X, attività, promesse e cambiamenti ai progetti. I filtri in alto mostrano una fonte alla volta. **Mostra altro** carica gli elementi più vecchi.

Le riunioni future compaiono in alto, sotto **In arrivo**, dalla più vicina alla più lontana. **Mostra tutti i prossimi** mostra le altre. Per ogni riunione sono indicate le persone presenti, ciascuna una sola volta. Quelle con note o trascrizione sono contrassegnate con **Note** o **Trascrizione**. Toccale per leggerle.

Le tue cronologie sono private: il Graph del team mostra solo ciò che consentono le tue regole di condivisione. Nella pagina, tocca **Team** sopra la Cronologia per aggiungere i contenuti condivisi dai compagni di team. Per ogni elemento è indicato chi l’ha condiviso. **Miei** mostra solo i tuoi.

## Lavoro e Personale

Le schede **Lavoro** e **Personale** elencano le persone in base al Tipo indicato nella loro pagina. Se hai scelto tu il Tipo (**Modifica**), la tua scelta ha la precedenza. Altrimenti, i membri della tua famiglia e i tuoi amici, così come i familiari e gli amici per te (per esempio una moglie o un padre), sono considerati Personali, indipendentemente dall’indirizzo da cui scrivono. Il team non vede mai i contatti Personali.

## Aggiungere una persona

Tocca **Nuova persona** in cima alla sezione Persone o **+** nella barra superiore sul telefono. Inserisci un nome e, se li hai, un indirizzo email e un’organizzazione. Se nel tuo Graph c’è già una persona simile, il modulo la mostra per prima, così puoi aprire quella pagina. Tocca **Aggiungi** per aprire la nuova pagina.

La persona che aggiungi rimane nel Graph anche se non ci sono ancora messaggi. Il suo primo messaggio verrà associato alla sua pagina.

## Modificare una persona

Tocca **Modifica** in cima alla pagina per cambiare nome, titolo, organizzazione, luogo, LinkedIn, numeri di telefono, indirizzi email, il ruolo della persona per te e se è un contatto di Lavoro o Personale. Il campo **Note** serve a ricordare quello che vuoi. Le note restano anche dopo un’unione. Tocca **Salva** per conservare le modifiche o **Annulla** per annullarle.

Le modifiche restano anche quando i dettagli della persona vengono cercati di nuovo, e dopo aver usato **Unisci** e **Annulla**. Svuota un campo per usare di nuovo il valore trovato. Se svuoti il nome, viene ripristinato quello presente nei messaggi.

Per cambiare la foto, toccala: scegli **Carica un’immagine**, seleziona una foto trovata per la persona oppure tocca **Rimuovi foto**. La foto resta sulla tua Machine.

## Unire due persone

Se due persone potrebbero essere la stessa, la pagina te lo chiede e la sezione Persone le mostra sotto **Stessa persona?**. Tocca **Unisci** per unire tutte le informazioni, inclusi messaggi, note, ruoli e progetti. Tocca **Non è la stessa** per tenerle separate. La tua risposta viene mostrata per un momento sulla coppia, poi la coppia scompare dall’elenco. L’elenco scompare quando non ci sono più coppie da controllare.

Una persona con un indirizzo che somiglia soltanto a uno che conosci, per esempio acme-corp.example invece di acmecorp.example, non viene mai proposta come la stessa persona. Solo tu puoi assegnarle un ruolo.

Un nome da solo non basta mai per associare due persone che usano domini diversi, perché chiunque può scriverlo. Due indirizzi con domini diversi vengono proposti solo se c’è un altro collegamento, per esempio se hanno persone o un progetto in comune. Una persona che usa il tuo nome ma un indirizzo che non è tuo non viene mai proposta. Aggiungi invece gli altri tuoi indirizzi in **Impostazioni**, alla voce [I tuoi indirizzi](settings.md#your-addresses).

Se corrisponde solo il nome, come "Sam" e "Sam Lee", ma i domini sono diversi, le persone vengono proposte solo se hanno lo stesso numero di telefono o profilo LinkedIn.

Se corrisponde solo il nome a quello di una riunione creata da una chat, oppure l’indirizzo appartiene a una persona che conoscevi già e solo la persona in chat dice che è suo, ti viene chiesto di confermare. The Machine non apre mai un link per verificarlo.

Un indirizzo condiviso, come info@ o quello di una mailing list, non viene mai associato alle persone che scrivono tramite quell’indirizzo. Un contatto di lavoro esterno alla tua azienda e una chat personale con solo il nome in comune non vengono associati automaticamente: vengono mostrati come una domanda.

**Unisci tutti** unisce tutte le coppie dell’elenco in una volta, tranne quelle contrassegnate con **Non è la stessa**. Tocca **Annulla** subito dopo per separarle di nuovo.

Per unire due persone, apri la pagina di una delle due, poi tocca **⋯**, **Stessa persona di…** e scegli l’altra. Nella pagina della persona unita, la sezione **Unita da** spiega il motivo. Tocca **Annulla** per separarle di nuovo.

## Eliminare definitivamente una persona

Nella pagina della persona, apri il menu ⋯ e scegli **Elimina definitivamente…**, poi **Elimina**. La persona e tutte le informazioni che la tua Machine conosce su di lei vengono rimosse: la sua scheda, gli indirizzi, i dettagli trovati, i messaggi scambiati solo tra voi due e le note che la riguardano.

Le attività che la riguardano restano, ma il suo nome viene rimosso. La persona non verrà aggiunta di nuovo, neanche tramite un’importazione o un’attività sui compleanni di Facebook che riporti il suo nome o indirizzo. L’operazione non può essere annullata.

## Email non recapitate

Quando un’email inviata a una persona non viene recapitata, il suo indirizzo viene contrassegnato con **Non recapitata** e la data. Se è noto un altro suo indirizzo, questo viene mostrato per primo. Le nuove bozze non verranno mai inviate all’indirizzo non recapitato se ne è noto un altro. Se è l’unico indirizzo, il foglio di invio ti avvisa, ma puoi comunque inviare l’email.

Un’email viene considerata non recapitata quando il server di posta indica che l’indirizzo non esiste oppure dopo 3 errori temporanei nell’arco di una settimana. L’avviso scompare quando la persona scrive di nuovo da quell’indirizzo o quando un’email inviata a quell’indirizzo viene recapitata.

## Titolo professionale e foto

Per chi ha un indirizzo aziendale, vengono cercati titolo professionale, foto, profilo LinkedIn e città, come per i [dettagli dell’organizzazione](organization-data.md). Su una Machine ospitata, la ricerca usa solo il nome e il dominio aziendale. Per cercare una foto, Gravatar riceve un hash dell’indirizzo di lavoro, mai l’indirizzo stesso. Puoi disattivare la ricerca in **Impostazioni**, nella sezione Sicurezza, con **Cerca i contatti di lavoro**.

Questa impostazione disattiva anche la consultazione del sito web prima della prima riunione e la ricerca sul web, se è configurato un provider di ricerca (vedi [Preparati alle riunioni](calendar.md#ready-for-your-meetings)).

Quando la ricerca trova informazioni sulla persona, la pagina mostra anche la sua descrizione, da quando ricopre il ruolo attuale e i due ruoli precedenti. Anche la preparazione delle riunioni usa queste informazioni. La descrizione viene usata solo se la persona non ha una biografia.

Le tue Connessioni si arricchiscono anche con le informazioni che hai già consultato: titolo, telefono e fuso orario da Slack; biografia e luogo da X; titolo e foto da LinkedIn; titoli professionali da Contatti Google e Salesflare; foto di un contatto da Salesflare, se è salvata lì. Passa il cursore sulla riga sotto il nome per vedere da dove provengono le informazioni.

Outlook aggiunge le foto dei colleghi della tua organizzazione e dei tuoi contatti Outlook, oltre ai titoli professionali e alle aziende dei tuoi contatti ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Le foto di WhatsApp e Telegram vengono sincronizzate tramite la sincronizzazione WhatsApp e la connessione alle chat Telegram: fino a 50 al giorno per ciascun servizio, solo per le persone già presenti nel tuo Graph. Non viene inviato loro nulla. Quando salvi un’importazione dei compleanni di Facebook, viene aggiunta la foto del profilo di chi non ne ha una ([Routine](routines.md)). Tutto resta sulla tua Machine.

Nel [Graph del team](team-graph.md) di una Fleet di lavoro, una copia ridotta della foto di lavoro viene associata alla scheda condivisa della persona. Le foto da Contatti Google, WhatsApp, Telegram o Facebook, e quelle che hai cambiato o rimosso, non vengono mai condivise.

## Su di te

I tuoi indirizzi e numeri, inclusi gli alias, appartengono sempre a te e non sono mai persone nel tuo Graph. Se cerchi te o aggiungi una persona con uno dei tuoi indirizzi, si apre **Su di te**. Le importazioni ignorano la tua riga.

La sezione Su di te elenca i tuoi indirizzi e indica da dove proviene ciascuno. Modificali in **Impostazioni**, alla voce Account. Per condividere il tuo contatto con un compagno di team o un amico, tocca **Condividi il mio contatto**. Vedi [Condividi un contatto](share-contact.md).

## Che ruolo ha per te

I ruoli che la tua Machine riconosce nei messaggi compaiono nella pagina della persona, sotto **Per te**, insieme alle parole che li indicano, come un titolo. Dire che qualcuno è il tuo commercialista o cliente non basta: serve anche qualcosa dalla tua parte, come messaggi o riunioni con quella persona. Non serve che tu lo confermi. Se un’informazione è sbagliata, correggila con **Modifica** nella pagina della persona o con **⋯** sulla riga corrispondente in **Modifiche recenti**. La tua Machine impara dalle modifiche.

## Cosa sa di una persona

I fatti relativi alla persona sono nella sua pagina, sotto **Informazioni note**. La sezione Apprendimento raccoglie quelli generali. Tocca **Aggiungi** per aggiungerne uno con parole tue. Ogni fatto ha un menu:

- **Modifica** lo cambia direttamente.
- **Non riguarda** la persona: il fatto torna a essere generale, in **Apprendimento**, sotto **Fatti**.
- **Rimuovi** lo elimina ovunque.

## Modifiche recenti

La sezione **Modifiche recenti**, chiusa per impostazione predefinita sopra la cronologia di una persona, organizzazione o progetto, elenca ciò che la tua Machine ha modificato o imparato: un ruolo, il luogo di lavoro, il rapporto tra due persone, un fatto o uno spostamento di progetto. Ogni riga indica la data e la fonte. Tocca la fonte per leggere il messaggio.

Se una riga è sbagliata, tocca **⋯** per correggerla direttamente: **Modifica**, **Rimuovi**, **Non riguarda** la persona oppure **Annulla** per riportare un progetto alla posizione precedente. Vengono mostrate tre righe; tocca **Mostra altro** per vedere le altre.

Una persona aggiornata oggi dalla tua Machine ha un piccolo punto accanto al nome nell’elenco Persone. In cima all’elenco, **4 persone aggiornate oggi** mostra i loro nomi. Vedi [Il Graph](graph.md).

## Un’attività su una persona

Tocca **Nuova attività** nel menu **⋯** di una persona, organizzazione o progetto per creare un’attività che la riguarda.
