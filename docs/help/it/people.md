---
title: Persone
area: graph
summary: Tutte le persone con cui sei in contatto: la loro pagina, il riepilogo e la cronologia, e come aggiungere, modificare, unire o eliminare una persona.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 97ffaf9944299a8b
---
Tutte le persone con cui sei in contatto, dalla più vicina in poi, in base ai tuoi messaggi e alle tue riunioni. Newsletter, ricevute e altre email non aggiungono nessuno finché non rispondi. Le trovi sotto Mittenti nascosti, in fondo all’elenco: **Mostra come persona** aggiunge una persona. Campi, tag e importazione funzionano allo stesso modo in tutti e tre gli elenchi, ma ogni elenco ha i propri filtri: vedi [The Graph](graph.md).

Una casella condivisa (info@, assistenza clienti, il nome di un negozio) viene associata all’organizzazione, non a una persona, anche dopo che le hai scritto.

## La pagina di una persona

La pagina inizia con foto, nome, ruolo, organizzazione e luogo della persona, e una riga che riassume i vostri contatti ("Parlate ogni giorno · ultimo contatto ieri · prossima riunione mar 27 ott"). Il contatto più recente è indicato con espressioni come "proprio ora", "3 ore fa", "ieri" o "3 giorni fa"; i contatti più vecchi mostrano una data. Passaci sopra con il mouse per vedere la data esatta. Sotto trovi:

- **Contatto**: numeri di telefono e indirizzi email. Tocca un numero o un indirizzo per chiamare o scrivere, oppure **Copia**. Qui trovi anche il **Compleanno** e la sua origine (Google Contacts, Google Calendar, Facebook o tu): vedi [The Graph](graph.md#birthday).
- **Con te**: che rapporto hai con questa persona, se è un contatto di Lavoro o Personale, e la tua famiglia o Fleet, con **Vedi in Fleet**.
- **Anche su**: gli altri servizi su cui parli con questa persona. **Slack** la apre in Slack oppure apre la conversazione più recente che hai avuto con lei su Slack.
- **Persone** e **Progetti** di cui fa parte, **In sospeso tra voi** (promesse in entrambe le direzioni, con **Segna come fatto** e **Lascia perdere**) e la sua **Cronologia**.

Gli indirizzi e le chat di una persona vengono collegati automaticamente quando è chiaro che appartengono alla stessa persona, per esempio un’email di lavoro con il suo indirizzo personale in CC.

Se una pagina mostra **Impossibile caricare questa pagina.**, tocca **Riprova**. Se il messaggio continua a comparire, usa **Qualcosa non va?** in fondo alla pagina.

## Riepilogo

Poche righe in cima alla pagina di una persona che riportano decisioni, richieste, piani o promesse, indicando tutti i nomi. The Machine lo riscrive quando ci sono novità, solo per le persone con cui sei davvero in contatto, e verifica ogni riga. Di solito una volta al giorno; entro poche ore se cambia qualcosa che riguarda quella persona, per esempio una nuova scadenza o una richiesta ritirata.

Le righe vaghe vengono tralasciate: se non c’è niente di specifico da dire, il riepilogo non viene mostrato. Ogni riga rimanda alla sua origine: i messaggi dello stesso giorno sono raggruppati sotto un’unica data con il relativo conteggio e si aprono insieme.

**Modifica** il riepilogo per esprimerti a modo tuo. Quando ci sono novità, The Machine mostra un **Aggiornamento suggerito** con le opzioni **Usalo** e **Tieni la mia**. **Lascia che lo scriva The Machine** per affidarle di nuovo il riepilogo.

La preparazione delle riunioni lo usa, ma solo con le righe pertinenti a quell’attività, di Lavoro o Personale. Resta sulla tua Machine: il tuo team non la vede.

## Cronologia

Ogni pagina di una persona o organizzazione ha una cronologia, con gli elementi più recenti in cima: email, riunioni e relativi riepiloghi di Zoom, conversazioni di Intercom (con **Apri in Intercom**), chat di WhatsApp, Telegram, Slack, LinkedIn e X, attività, promesse e aggiornamenti sui progetti. I filtri in alto mostrano una fonte alla volta. **Mostra altro** carica gli elementi meno recenti.

Le riunioni future sono in cima, sotto **In arrivo**, dalla più vicina in poi; **Mostra tutti i prossimi** mostra le altre. Una riunione indica chi vi ha partecipato, contando ogni persona una sola volta. Se include note o una trascrizione, trovi **Note** o **Trascrizione**: selezionale per leggerle.

Le tue cronologie sono tue: il Graph del team mostra solo ciò che le tue regole di condivisione consentono. In una pagina, **Team** sopra la Cronologia aggiunge ciò che hanno condiviso i tuoi colleghi, indicando chi ha condiviso ogni elemento; **Miei** mostra solo i tuoi.

## Lavoro e Personale

Le schede **Lavoro** e **Personale** elencano le persone in base al loro Tipo, indicato nella rispettiva pagina. La scelta che fai tu (**Modifica**) ha la precedenza. Altrimenti, le persone della tua famiglia e i tuoi amici, oltre ai familiari o amici per cui sei tu un familiare o un amico (per esempio, una moglie o un padre), sono Personali, qualunque indirizzo usino per scriverti. Il tuo team non vede mai i contatti Personali.

## Aggiungere una persona

Tocca **Nuova persona** in cima a Persone, oppure **+** nella barra superiore sul telefono. Inserisci un nome e, se li hai, un indirizzo email e un’organizzazione. Se nel tuo Graph c’è già una persona simile, il modulo la mostra per prima, così puoi aprire la pagina esistente. **Aggiungi** apre la nuova pagina.

La persona che aggiungi resta nell’elenco anche se non ci sono ancora messaggi. Il suo primo messaggio verrà associato alla pagina.

## Modificare una persona

**Modifica**, in cima alla pagina, ti permette di cambiare nome, ruolo, organizzazione, luogo, LinkedIn, numeri di telefono e indirizzi email, il vostro rapporto e la categoria Lavoro o Personale. Il campo **Note** serve a ricordare ciò che vuoi; le note restano anche dopo un’unione. **Salva** conserva le modifiche, mentre **Annulla** le annulla.

Le modifiche restano anche quando i dettagli vengono cercati di nuovo e dopo **Unisci** e **Annulla**. Svuota un campo per riutilizzare il valore trovato. Se svuoti il nome, verrà ripristinato quello presente nei suoi messaggi.

Per cambiare la foto, selezionala e scegli **Carica un’immagine**, una foto trovata per quella persona oppure **Rimuovi foto**. La foto resta sulla tua Machine.

## Unire due persone

Quando due persone potrebbero essere la stessa, la loro pagina ti chiede se si tratta della stessa persona e Persone le mostra sotto **Stessa persona?**. **Unisci** le combina, includendo tutti i messaggi, le note, i ruoli e i progetti. **Non è la stessa** le mantiene separate definitivamente. La tua risposta appare per un momento sulla coppia, che poi scompare dall’elenco. L’elenco scompare quando non ci sono più coppie da esaminare.

Una persona con un indirizzo che somiglia soltanto a uno che conosci, come acme-corp.example rispetto ad acmecorp.example, non viene mai proposta come la stessa persona. Solo tu puoi assegnarle un ruolo.

Un indirizzo condiviso, come info@ o una mailing list, non viene mai unito alle persone che scrivono tramite quell’indirizzo. Un contatto di lavoro esterno alla tua azienda e una chat personale che hanno in comune solo il nome non vengono uniti automaticamente: vengono elencati come una coppia da esaminare.

**Unisci tutti** unisce in una volta tutte le coppie dell’elenco, tranne quelle contrassegnate con **Non è la stessa**. Usando **Annulla** subito dopo, le separi di nuovo tutte.

Per unire due persone manualmente, apri una delle loro pagine, poi seleziona **⋯**, **Stessa persona di…** e scegli l’altra. La pagina di una persona unita mostra il motivo sotto **Unita da**, con l’opzione **Annulla** per separarle di nuovo.

## Eliminare una persona definitivamente

Nella sua pagina, apri il menu ⋯ e seleziona **Elimina definitivamente…**, poi **Elimina**. La persona e tutte le informazioni che la tua Machine conosce su di lei vengono rimosse: la scheda, gli indirizzi, i dettagli trovati, i messaggi scambiati solo tra voi e le note che la riguardano.

Le attività che la coinvolgono restano, ma il suo nome viene rimosso. Non verrà aggiunta di nuovo, nemmeno tramite un’importazione o un’attività sui compleanni di Facebook che riporta il suo nome o indirizzo. L’operazione non si può annullare.

## Email non consegnata

Quando un’email inviata a una persona non viene consegnata, accanto al suo indirizzo appare **Non consegnata** con la data, e un suo eventuale altro indirizzo compare per primo. Se è noto un altro indirizzo, le nuove bozze non verranno mai inviate a quello non valido. Se è l’unico indirizzo, il riepilogo dell’invio ti avvisa, ma puoi comunque inviare l’email.

Un mancato recapito viene registrato quando il server di posta segnala che l’indirizzo non esiste oppure dopo 3 errori temporanei nell’arco di una settimana. L’avviso viene rimosso quando la persona scrive di nuovo da quell’indirizzo o quando un’email gli viene consegnata.

## Ruolo e foto

Alle persone con un indirizzo aziendale vengono associati un ruolo, una foto, LinkedIn e la città, cercati come descritto in [dettagli dell’organizzazione](organization-data.md). Su una Machine ospitata, la ricerca usa solo il loro nome e il dominio aziendale. Per la foto, Gravatar riceve un hash dell’indirizzo di lavoro, mai l’indirizzo stesso. Puoi disattivare questa funzione in **Impostazioni**, nella sezione Sicurezza: **Cerca i contatti di lavoro**.

Quando trova queste informazioni, la pagina mostra anche il testo Informazioni, da quando la persona ricopre il ruolo attuale e i due ruoli precedenti. Anche la preparazione delle riunioni usa questi dati; il testo Informazioni viene usato solo se la persona non ha una propria biografia.

Le tue Connessioni si arricchiscono anche con le informazioni già lette: un ruolo, un numero di telefono e il fuso orario da Slack; una biografia e un luogo da X; un titolo e una foto da LinkedIn; ruoli da Google Contacts e Salesflare; e la foto del contatto da Salesflare, se il servizio ne conserva una. Passa il mouse sulla riga sotto il nome per vedere da dove proviene l’informazione.

Outlook aggiunge le foto dei colleghi della tua organizzazione e dei tuoi contatti di Outlook, oltre ai ruoli e alle aziende dei tuoi contatti ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Le foto di WhatsApp e Telegram vengono sincronizzate tramite la sincronizzazione di WhatsApp e la connessione alle chat di Telegram: fino a 50 al giorno per ciascun servizio, solo per le persone già presenti nel tuo Graph. Non viene inviato loro nulla. Un’importazione dei compleanni di Facebook aggiunge la foto del profilo di una persona che non ne ha una, quando la salvi ([Routine](routines.md)). Tutto resta sulla tua Machine.

Nel [Team Graph](team-graph.md) di una Fleet di Lavoro, una piccola copia della foto di lavoro viene inclusa nella scheda condivisa della persona. Le foto da Google Contacts, WhatsApp, Telegram o Facebook, così come quelle che hai modificato o rimosso, non vengono mai condivise.

## Su di te

I tuoi indirizzi e numeri, inclusi gli alias, sono sempre tuoi e non sono mai una persona nel tuo Graph. Se cerchi te stesso o aggiungi una persona con uno dei tuoi indirizzi, si apre **Su di te**; un’importazione ignora la tua riga.

La pagina Su di te elenca i tuoi indirizzi e la loro origine. Puoi modificarli in **Impostazioni**, nella sezione Account. Per inviare i tuoi dati di contatto a un collega o a un amico, seleziona **Condividi il mio contatto**. Vedi [Condividere un contatto](share-contact.md).

## Che rapporto hai con una persona

I ruoli che la tua Machine riconosce nei tuoi messaggi appaiono nella pagina della persona, sotto **Per te**, insieme alla riga in cui li ha riconosciuti. Non aspetta una tua conferma. Se qualcosa non è corretto, puoi correggerlo con **Modifica** nella pagina oppure con **⋯** sulla relativa riga in **Modifiche recenti**. Impara dalle tue modifiche.

## Cosa sa di una persona

Le informazioni sulla persona sono nella sua pagina, sotto **Informazioni note**; la sezione Apprendimento conserva quelle generali. **Aggiungi** permette di aggiungerne un’altra con parole tue. Ogni informazione ha un menu:

- **Modifica** la cambia direttamente.
- **Non riguarda** la persona la rende di nuovo un’informazione generale, sotto **Apprendimento**, **Fatti**.
- **Rimuovi** la elimina ovunque.

## Modifiche recenti

La sezione **Modifiche recenti**, chiusa appena sopra la cronologia di una persona, organizzazione o progetto, elenca ciò che la tua Machine ha modificato o appreso: un ruolo, il luogo di lavoro, il rapporto tra due persone, un’informazione o uno spostamento di progetto. Ogni riga mostra la data e la fonte; tocca la fonte per leggere il messaggio.

Se una riga non è corretta, il menu **⋯** permette di sistemarla direttamente: **Modifica**, **Rimuovi**, **Non riguarda** la persona oppure **Annulla** per riportare un progetto dov’era. Vengono mostrate tre righe; **Mostra altro** mostra le altre.

Una persona aggiornata oggi dalla tua Machine è contrassegnata da un piccolo punto nell’elenco Persone. In cima all’elenco, **4 persone aggiornate oggi** indica chi è stato aggiornato. Vedi [The Graph](graph.md).

## Un’attività su una persona

**Nuova attività** nel menu **⋯** di una persona, organizzazione o progetto crea un’attività che la riguarda.
