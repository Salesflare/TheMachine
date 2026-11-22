---
title: Persone
area: graph
summary: Tutte le persone con cui sei in contatto: la loro pagina, il riepilogo e la cronologia, e come aggiungere, modificare, unire o eliminare una persona.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 5e808343918f7f47
---
Tutte le persone con cui sei in contatto, a partire da quelle più vicine, dai tuoi messaggi e dalle riunioni. Newsletter, ricevute e altre comunicazioni non aggiungono nessuno finché non rispondi. Si trovano in Mittenti nascosti, sotto l’elenco: Mostra come persona aggiunge una persona all’elenco. Campi, tag e importazione funzionano allo stesso modo in tutti e tre gli elenchi, e ognuno ha i propri filtri: vedi [Il Graph](graph.md).

Una casella condivisa (info@, assistenza clienti, il nome del negozio) viene associata alla sua organizzazione, non a una persona, anche dopo che le scrivi.

## La pagina di una persona

Inizia con foto, nome, titolo, organizzazione e località, e una riga che spiega come siete in contatto ("Parlate ogni giorno · ultimo contatto ieri · prossima riunione mar 27 ott"). Il contatto più recente è indicato con formule come "proprio ora", "3 ore fa", "ieri" o "3 giorni fa"; per i contatti meno recenti viene mostrata una data. Passaci sopra con il puntatore per vedere la data esatta. Sotto trovi:

- **Contatto**: numeri di telefono e indirizzi email. Tocca un elemento per chiamare o scrivere, oppure **Copia**. Qui trovi anche il **Compleanno**, con l’indicazione della fonte (Contatti Google, Google Calendar, Facebook, le tue note o tu): vedi [Il Graph](graph.md#birthday).
- **Con te**: il ruolo che ha per te, se è un contatto di lavoro o personale, e se fa parte della tua famiglia o di Fleet, con **Vedi in Fleet**.
- **Anche su**: gli altri luoghi in cui parli con questa persona. **Slack** apre la persona in Slack o la tua chat più recente con lei.
- **Persone** e **Progetti** di cui fa parte, **In sospeso tra voi** (promesse da entrambe le parti, con **Segna come fatto** e **Lascia perdere**) e la sua **Cronologia**.

Gli indirizzi e le chat di una persona vengono uniti automaticamente quando è chiaro che appartengono alla stessa persona, per esempio un indirizzo email di lavoro con il suo indirizzo personale in copia.

Se compare il messaggio **Impossibile caricare questa pagina.**, tocca **Riprova**. Se continua a comparire, usa **Qualcosa non va?** in fondo alla pagina.

## Riepilogo

Poche righe all’inizio della pagina di una persona: decisioni, richieste, piani o promesse, con i nomi di tutte le persone coinvolte. The Machine lo riscrive quando ci sono novità, solo per le persone con cui sei davvero in contatto, e verifica ogni riga prima di mostrarla. Di solito una volta al giorno; entro poche ore se cambia qualcosa che riguarda quella persona, per esempio una nuova scadenza o una richiesta ritirata.

Le righe vaghe non vengono incluse; se non c’è nulla di specifico da dire, il riepilogo non viene mostrato. Ogni riga rimanda alla fonte: i messaggi dello stesso giorno sono raggruppati sotto un’unica data con il relativo conteggio e si aprono insieme.

**Modifica** il riepilogo per esprimerti a modo tuo. Quando ci sono novità, The Machine mostra un **Aggiornamento suggerito**, con **Usalo** e **Tieni la mia**. **Lascia che lo scriva The Machine** restituisce a The Machine il compito di scriverlo.

La preparazione delle riunioni lo usa, ma solo con le righe pertinenti a quell’attività (Lavoro o Personale). Resta sulla tua Machine; il tuo team non può vederlo.

## Cronologia

Ogni pagina di una persona o di un’organizzazione ha una cronologia, dalla più recente alla meno recente: email, riunioni e relativi riepiloghi Zoom, conversazioni Intercom (con **Apri in Intercom**), chat WhatsApp, Telegram, Slack, LinkedIn e X, attività, promesse e aggiornamenti sui progetti. I filtri in alto mostrano una fonte alla volta. **Mostra altro** carica gli elementi meno recenti.

Le riunioni future sono in cima, sotto **In arrivo**, dalla più vicina alla più lontana; **Mostra tutti i prossimi** mostra le altre. Per ogni riunione sono indicate le persone presenti, una sola volta ciascuna. Se ci sono note o una trascrizione, compare **Note** o **Trascrizione**; fai clic per leggerle.

Le tue cronologie sono private: il Graph del team mostra solo ciò che consentono le tue regole di condivisione. In una pagina, **Team** sopra la Cronologia aggiunge i contenuti condivisi dai colleghi, indicando per ciascuno chi l’ha condiviso; **Miei** mostra solo i tuoi.

## Lavoro e Personale

Le schede **Lavoro** e **Personale** elencano le persone in base al loro tipo, indicato sulla pagina. La scelta che fai tu (**Modifica**) ha la precedenza. Altrimenti, la tua famiglia e i tuoi amici, e le persone che sono tue familiari o amiche (una moglie, un padre), sono di tipo Personale, indipendentemente dall’indirizzo da cui scrivono. Il tuo team non vede mai i contatti personali.

## Aggiungere una persona

Usa **Nuova persona** in cima a Persone, oppure **+** nella barra superiore sul telefono. Inserisci un nome e, se li hai, un indirizzo email e un’organizzazione. Se nel tuo Graph c’è già una persona simile, il modulo la mostra per prima, così puoi aprire quella pagina. **Aggiungi** apre la nuova pagina.

La persona che aggiungi resta nell’elenco anche se non ci sono ancora messaggi. Il suo primo messaggio verrà associato alla sua pagina.

## Modificare una persona

**Modifica**, in cima alla sua pagina, permette di cambiare nome, titolo, organizzazione, località, LinkedIn, numeri di telefono e indirizzi email, il ruolo che ha per te e se è un contatto di lavoro o personale. Il campo **Note** serve a ricordare ciò che vuoi; le note restano anche dopo l’unione. **Salva** applica le modifiche, **Annulla** le annulla.

Le modifiche restano anche quando i dettagli vengono cercati di nuovo, e dopo **Unisci** e **Annulla**. Svuota un campo per usare di nuovo il valore trovato. Se svuoti il nome, viene ripristinato quello presente nei suoi messaggi.

Per cambiare la foto, fai clic su di essa: **Carica un’immagine**, scegline una trovata per quella persona oppure **Rimuovi foto**. La foto resta sulla tua Machine.

## Unire due persone

Quando due persone potrebbero essere la stessa, la loro pagina chiede se si tratta della stessa persona e Persone le mostra sotto **Stessa persona?**. **Unisci** le unisce, includendo tutti i messaggi, le note, i ruoli e i progetti. **Non è la stessa** le tiene separate definitivamente. La tua risposta viene mostrata per un po’ sulla coppia, che poi scompare dall’elenco. L’elenco scompare quando non ci sono più coppie da verificare.

Una persona con un indirizzo che assomiglia soltanto a uno che conosci, come acme-corp.example e acmecorp.example, non viene mai proposta come la stessa persona. Inoltre, solo tu puoi assegnarle un ruolo.

Il solo nome non basta mai per associare due persone con domini diversi, perché chiunque può inserirlo: due indirizzi con domini diversi vengono proposti solo se c’è un altro collegamento, come le stesse persone o un progetto. Una persona che usa il tuo nome a un indirizzo che non è tuo non viene mai proposta. Aggiungi invece gli altri tuoi indirizzi in Impostazioni, [I tuoi indirizzi](settings.md#your-addresses).

Se tra domini diversi corrisponde solo il nome, come "Sam" e "Sam Lee", le persone vengono proposte solo se hanno lo stesso numero di telefono o profilo LinkedIn.

Un indirizzo condiviso, come info@ o una mailing list, non viene mai associato alle persone che scrivono tramite quell’indirizzo. Un contatto di lavoro esterno alla tua azienda e una chat personale che hanno in comune solo un nome non vengono associati automaticamente: sono elencati come coppia da verificare.

**Unisci tutti** unisce in una sola volta tutte le coppie dell’elenco, tranne quelle che hai contrassegnato con **Non è la stessa**. Puoi usare **Annulla** subito dopo per separarle di nuovo.

Per unire due persone manualmente, aprine una, poi scegli **⋯**, **Stessa persona di…** e seleziona l’altra. La pagina della persona unita indica il motivo sotto **Unito da**, con **Annulla** per separarle di nuovo.

## Eliminare una persona definitivamente

Nella sua pagina, apri il menu ⋯ e scegli **Elimina definitivamente…**, poi **Elimina**. La persona e tutte le informazioni che la tua Machine conosce su di lei vengono rimosse: la sua scheda, gli indirizzi, i dettagli trovati, i messaggi scambiati solo tra voi e le note che la riguardano.

Le attività che la riguardano restano, ma il suo nome viene rimosso. Non verrà aggiunta di nuovo, neanche tramite un’importazione o un’attività di compleanno Facebook con il suo nome o indirizzo. L’operazione non si può annullare.

## Email non recapitata

Quando un’email inviata a qualcuno non viene recapitata, il suo indirizzo mostra **Respinto** con la data, e un suo altro indirizzo viene messo in cima. Le nuove bozze non vengono mai inviate a quell’indirizzo se ne è noto un altro. Se è l’unico, la schermata di invio ti avvisa, ma puoi comunque inviare.

Un mancato recapito viene registrato quando il server di posta segnala che l’indirizzo non esiste oppure dopo 3 errori temporanei nell’arco di una settimana. Lo stato viene rimosso quando la persona scrive di nuovo da quell’indirizzo o quando un’email inviata a quell’indirizzo viene recapitata.

## Titolo professionale e foto

Per le persone con un indirizzo aziendale vengono cercati titolo professionale, foto, LinkedIn e città, come per i [dati dell’organizzazione](organization-data.md). Su una Machine ospitata, la ricerca usa solo il loro nome e il dominio aziendale. Per trovare una foto, Gravatar riceve un hash dell’indirizzo di lavoro, mai l’indirizzo stesso. Per disattivare questa funzione, vai in **Impostazioni**, alla voce Sicurezza, e disattiva **Cerca i contatti di lavoro**.

Questa opzione disattiva anche la breve ricerca sul web prima di una prima riunione (vedi [Preparati alle riunioni](calendar.md#ready-for-your-meetings)).

Quando la ricerca trova queste informazioni, la pagina mostra anche il testo Informazioni, da quando la persona ricopre il ruolo attuale e i due ruoli precedenti. Le preparazioni delle riunioni includono anche queste informazioni, ma usano il testo Informazioni solo se la persona non ha una biografia propria.

Le tue connessioni aggiungono altri dettagli con ciò che hanno già letto: titolo, telefono e fuso orario da Slack; biografia e località da X; descrizione e foto da LinkedIn; titoli professionali da Contatti Google e Salesflare; e la foto di un contatto da Salesflare, se il servizio ne conserva una. Passa il puntatore sulla riga sotto il nome per vedere da dove proviene l’informazione.

Outlook aggiunge le foto dei colleghi della tua organizzazione e dei tuoi contatti Outlook, oltre ai titoli professionali e alle aziende dei tuoi contatti ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Le foto di WhatsApp e Telegram vengono sincronizzate tramite la sincronizzazione di WhatsApp e la connessione alle chat Telegram: fino a 50 al giorno per ciascun servizio, solo per le persone già presenti nel tuo Graph. Non viene inviato loro nulla. L’importazione dei compleanni Facebook aggiunge, quando la salvi, la foto del profilo di una persona che non ne ha una ([Routine](routines.md)). Tutto resta sulla tua Machine.

Nel [Graph del team](team-graph.md) di una Fleet di lavoro, una piccola copia della foto professionale viene inclusa nella scheda condivisa della persona. Le foto da Contatti Google, WhatsApp, Telegram o Facebook, e quelle che hai cambiato o rimosso, non vengono mai condivise.

## Su di te

I tuoi indirizzi e numeri, compresi gli alias, appartengono sempre a te e mai a qualcuno nel tuo Graph. Se cerchi il tuo nome o aggiungi una persona con uno dei tuoi indirizzi, si apre **Su di te**; durante un’importazione, la tua riga viene ignorata.

La pagina Su di te elenca i tuoi indirizzi e la relativa fonte; puoi modificarli in **Impostazioni**, alla voce Account. Per inviare il tuo contatto a un collega o a un amico, scegli **Condividi il mio contatto**. Vedi [Condividi un contatto](share-contact.md).

## Il suo ruolo per te

I ruoli che la tua Machine rileva nei messaggi compaiono sulla pagina della persona, sotto **Per te**, con solo le parole che indicano il ruolo, come un titolo. Non basta che qualcuno dica di essere il tuo commercialista o cliente: deve risultare anche da parte tua, per esempio dai tuoi messaggi o dalle riunioni con quella persona. Non serve che tu lo confermi. Se è sbagliato, **Modifica** nella pagina della persona lo corregge; puoi anche usare **⋯** sulla relativa riga in **Modifiche recenti**. La tua Machine impara dalle tue modifiche.

## Cosa sa di una persona

Le informazioni su una persona si trovano sulla sua pagina, sotto **Cosa si sa su** e il suo nome; in Apprendimento trovi quelle generali. **Aggiungi** salva un’altra informazione con parole tue. Ogni informazione ha un menu:

- **Modifica** la cambia direttamente.
- **Non riguarda** quella persona la rende di nuovo un’informazione generale, in **Apprendimento**, **Fatti**.
- **Rimuovi** la elimina ovunque.

## Modifiche recenti

**Modifiche recenti**, nella sezione espandibile subito sopra la cronologia di una persona, organizzazione o progetto, elenca ciò che la tua Machine ha modificato o imparato: un ruolo, il luogo di lavoro, il rapporto tra due persone, un’informazione o un cambiamento di progetto. Ogni riga riporta la data e la fonte; tocca la fonte per leggere il messaggio.

Se una riga è sbagliata, il menu **⋯** ti permette di correggerla subito: **Modifica**, **Rimuovi**, **Non riguarda** quella persona oppure **Annulla** per ripristinare la posizione precedente di un progetto. Vengono mostrate tre righe; **Mostra altro** mostra le altre.

Una persona aggiornata oggi dalla tua Machine ha un puntino accanto al nome nell’elenco Persone, e in cima all’elenco compare **4 persone aggiornate oggi** con i loro nomi. Vedi [Il Graph](graph.md).

## Un’attività su una persona

**Nuova attività** nel menu **⋯** di una persona, organizzazione o progetto crea un’attività che la riguarda.
