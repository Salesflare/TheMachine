---
title: Persone
area: graph
summary: Tutte le persone con cui sei in contatto: la loro pagina, il riepilogo e la cronologia, e come aggiungerle, modificarle, unirle o eliminarle.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 97ffaf9944299a8b
---
Tutte le persone con cui sei in contatto, dalle più vicine in poi, in base ai messaggi e alle riunioni. Newsletter, ricevute e altre email automatiche non aggiungono nessuno finché non rispondi. Le trovi in Mittenti nascosti, sotto l’elenco: **Mostra come persona** aggiunge una persona. Campi, tag e importazioni funzionano allo stesso modo in tutti e tre gli elenchi, ognuno con i propri filtri: vedi [The Graph](graph.md).

Una casella condivisa (info@, assistenza clienti, il nome di un negozio) è associata alla sua organizzazione, non a una persona, anche se le scrivi.

## Pagina di una persona

In alto trovi la foto, il nome, il ruolo, l’organizzazione e la località, oltre a una riga su come siete in contatto («Parlate ogni giorno · ultimo contatto ieri · prossima riunione mar 27 ott»). Il contatto recente è indicato con «adesso», «3 ore fa», «ieri» o «3 giorni fa», mentre quello meno recente mostra una data. Passaci sopra con il puntatore per vedere la data esatta. Più sotto trovi:

- **Contatto**: numeri di telefono e indirizzi email. Tocca un numero o un indirizzo per chiamare o scrivere, oppure **Copia**. Qui trovi anche il **Compleanno** e la sua fonte (Google Contacts, Google Calendar, Facebook o tu): vedi [The Graph](graph.md#birthday).
- **Con te**: che rapporto hai con questa persona, se è un contatto di lavoro o personale e la tua Family o Fleet, con **Vedi in Fleet**.
- **Anche su**: gli altri servizi in cui parli con questa persona. **Slack** apre il suo profilo in Slack o la tua chat più recente con lei.
- **Persone** e **Progetti** di cui fa parte, **In sospeso tra voi** (promesse in entrambe le direzioni, con **Segna come fatto** e **Lascia perdere**) e la sua **Cronologia**.

Gli indirizzi e le chat di una persona vengono collegati automaticamente quando è chiaro che appartengono alla stessa persona, per esempio un’email di lavoro con il suo indirizzo in copia.

Se compare il messaggio **Impossibile caricare la pagina.**, tocca **Riprova**. Se il messaggio continua a comparire, tocca **Qualcosa non va?** in fondo alla pagina.

## Riepilogo

In cima alla pagina di una persona trovi alcune brevi righe su decisioni, richieste, programmi o promesse, con il nome di tutte le persone coinvolte. The Machine lo riscrive quando ci sono novità, solo per le persone con cui sei davvero in contatto, e verifica ogni riga. Di solito una volta al giorno, ma entro poche ore se cambia qualcosa che la riguarda, per esempio una nuova scadenza o una richiesta ritirata.

Le informazioni vaghe vengono tralasciate: se non c’è niente di specifico da dire, il riepilogo non compare. Ogni riga rimanda alla sua fonte: i messaggi dello stesso giorno sono raggruppati sotto un’unica data, con il numero di messaggi, e si aprono insieme.

Tocca **Modifica** per riscriverlo a modo tuo. Quando ci sono novità, The Machine mostra un **Aggiornamento suggerito** con le opzioni **Usalo** e **Tieni la mia**. **Lascia che lo scriva The Machine** restituisce a The Machine il compito di scriverlo.

La preparazione delle riunioni usa questo riepilogo, ma solo le righe della categoria di quell’attività, Lavoro o Personale. Resta sulla tua Machine: il tuo team non la vede.

## Cronologia

Ogni pagina di una persona o di un’organizzazione ha una cronologia, dalla più recente alla meno recente: email, riunioni e relativi riepiloghi Zoom, conversazioni Intercom (con **Apri in Intercom**), chat WhatsApp, Telegram, Slack, LinkedIn e X, attività, promesse e cambiamenti ai progetti. I filtri in alto mostrano una fonte alla volta. **Mostra altro** carica gli elementi precedenti.

Le riunioni future compaiono in cima, sotto **In arrivo**, dalla più vicina alla più lontana. **Mostra tutti i prossimi** mostra le altre riunioni. Una riunione indica chi vi ha partecipato, una sola volta per persona. Se ha note o una trascrizione, trovi **Note** o **Trascrizione**: selezionala per leggerle.

Le tue cronologie sono private: il Graph del team mostra solo ciò che consentono le regole di condivisione. In una pagina, **Team** sopra la cronologia aggiunge ciò che hanno condiviso i tuoi colleghi, indicando la persona che ha condiviso ogni elemento; **Miei** mostra solo i tuoi.

## Lavoro e Personale

Le schede **Lavoro** e **Personale** elencano le persone in base al loro tipo, visibile sulla loro pagina. La tua scelta (**Modifica**) ha la precedenza. Altrimenti, la tua Family e i tuoi Friends, così come i familiari e gli amici per te (una moglie, un padre), sono considerati personali, indipendentemente dall’indirizzo da cui scrivono. Il tuo team non vede mai i contatti personali.

## Aggiungere una persona

Tocca **Nuova persona** in cima a Persone o **+** nella barra superiore da telefono. Inserisci un nome e, se li hai, un indirizzo email e un’organizzazione. Se nel tuo Graph c’è già una persona simile, il modulo la mostra per prima, così puoi aprire la scheda esistente. Tocca **Aggiungi** per aprire la nuova pagina.

La persona che aggiungi resta nell’elenco anche se non ci sono ancora messaggi. Il suo primo messaggio verrà associato alla sua scheda.

## Modificare una persona

Tocca **Modifica** in cima alla sua pagina per cambiare nome, ruolo, organizzazione, località, LinkedIn, numeri di telefono e indirizzi email, il rapporto che hai con lei e la categoria Lavoro o Personale. Il campo **Note** serve a ricordare quello che vuoi; le note restano anche dopo un’unione. Tocca **Salva** per salvare le modifiche o **Annulla** per lasciarle come sono.

Le modifiche restano anche quando i suoi dati vengono cercati di nuovo, e anche dopo **Unisci** e **Annulla**. Svuota un campo per usare di nuovo il valore trovato. Se svuoti il nome, verrà ripristinato quello presente nei messaggi.

Per cambiare la foto, selezionala: puoi **Carica un’immagine**, sceglierne una trovata per questa persona o **Rimuovi foto**. La foto resta sulla tua Machine.

## Unire due persone

Quando due persone potrebbero essere la stessa, sulla loro pagina ti viene chiesto se si tratta della stessa persona e in Persone compaiono sotto **Stessa persona?**. **Unisci** le associa e mantiene tutti i messaggi, le note, i ruoli e i progetti. **Non è la stessa** le tiene separate in modo definitivo. La tua risposta compare per qualche istante nella coppia, poi la coppia scompare dall’elenco. L’elenco scompare quando non ci sono più domande.

Una persona con un indirizzo che assomiglia soltanto a uno che conosci, come acme-corp.example rispetto ad acmecorp.example, non viene mai proposta come la stessa persona. Solo tu puoi assegnarle un ruolo.

Un indirizzo condiviso, come info@ o una mailing list, non viene mai associato alle persone che lo usano per scrivere. Un contatto di lavoro al di fuori della tua azienda e una chat personale con solo il nome in comune non vengono associati automaticamente: vengono mostrati come una domanda.

**Unisci tutti** unisce in un’unica volta tutte le coppie nell’elenco, tranne quelle che hai contrassegnato con **Non è la stessa**. Tocca **Annulla** subito dopo per separarle di nuovo tutte.

Per unire due persone manualmente, apri una delle loro pagine, poi tocca **⋯**, **Stessa persona di…** e scegli l’altra persona. Nella pagina della persona unita trovi i motivi dell’unione sotto **Unita da**, con l’opzione **Annulla** per separarle di nuovo.

## Eliminare definitivamente una persona

Nella sua pagina, apri il menu ⋯ e scegli **Elimina definitivamente…**, poi **Elimina**. La persona e tutte le informazioni che la tua Machine conosce su di lei vengono rimosse: la sua scheda, gli indirizzi, i dettagli trovati, i messaggi scambiati solo tra voi e le note che la riguardano.

Le attività che la coinvolgono restano, ma senza il suo nome. Non verrà aggiunta di nuovo, neanche tramite un’importazione o un’attività sui compleanni di Facebook che riporta il suo nome o indirizzo. L’operazione non si può annullare.

## Email respinta

Quando un’email inviata a una persona viene respinta, il suo indirizzo mostra **Respinto** con la data, e un altro suo indirizzo viene messo in cima. Se è noto un altro indirizzo, le nuove bozze non verranno mai inviate a quello respinto. Se è l’unico indirizzo, la schermata di invio ti avvisa, ma puoi comunque inviare l’email.

Un indirizzo viene considerato respinto se il server di posta segnala che non esiste oppure dopo 3 errori temporanei nell’arco di una settimana. Il contrassegno viene rimosso quando la persona ti scrive di nuovo da quell’indirizzo o quando un’email inviata a quell’indirizzo viene recapitata.

## Ruolo e foto

Per le persone con un indirizzo aziendale, vengono cercati il ruolo, la foto, il profilo LinkedIn e la città, come per i [dettagli dell’organizzazione](organization-data.md). Su una Machine ospitata, la ricerca usa solo il loro nome e il dominio dell’azienda. Per trovare una foto, Gravatar riceve un hash dell’indirizzo di lavoro, mai l’indirizzo stesso. Puoi disattivare questa funzione in **Impostazioni**, alla voce Sicurezza: **Cerca i contatti di lavoro**.

Quando le informazioni vengono trovate, nella pagina della persona compaiono anche la descrizione, da quando ricopre il ruolo attuale e i due ruoli precedenti. Anche la preparazione delle riunioni usa queste informazioni; la descrizione viene usata solo se la persona non ha una sua biografia.

Le Connessioni si arricchiscono con le informazioni che hanno già trovato: ruolo, telefono e fuso orario da Slack; biografia e località da X; titolo e foto da LinkedIn; ruoli da Google Contacts e Salesflare; e la foto del contatto da Salesflare, se il servizio la conserva. Passa il puntatore sopra la riga sotto il nome per vedere da dove proviene.

Outlook aggiunge le foto dei colleghi della tua organizzazione e dei tuoi contatti Outlook, oltre ai ruoli e alle aziende dei tuoi contatti ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Le foto di WhatsApp e Telegram vengono aggiunte tramite la sincronizzazione WhatsApp e la connessione alle chat Telegram: fino a 50 al giorno per ciascun servizio, solo per le persone già presenti nel tuo Graph. Non viene inviato loro nulla. Un’importazione dei compleanni di Facebook aggiunge la foto del profilo delle persone che non ne hanno una, quando la salvi ([Routine](routines.md)). Tutto resta sulla tua Machine.

Nel [Graph del team](team-graph.md) di una Fleet di lavoro, una piccola copia della foto di lavoro viene condivisa insieme alla scheda della persona. Le foto da Google Contacts, WhatsApp, Telegram o Facebook, e quelle che hai cambiato o rimosso, non vengono mai condivise.

## Su di te

I tuoi indirizzi e numeri, compresi gli alias, sono sempre tuoi e non vengono mai considerati persone nel tuo Graph. Se cerchi te stesso o aggiungi una persona con uno dei tuoi indirizzi, si apre **Su di te**; un’importazione ignora la riga con i tuoi dati.

La pagina Su di te elenca i tuoi indirizzi e indica da dove provengono. Puoi modificarli in **Impostazioni**, alla voce Account. Per inviare i tuoi recapiti a un collega o a un amico, scegli **Condividi il mio contatto**. Vedi [Condividere un contatto](share-contact.md).

## Che rapporto hai con questa persona

I ruoli che la tua Machine rileva nei messaggi compaiono nella sua pagina, sotto **Per te**, insieme alla frase in cui li ha trovati. Non devi aspettare che ti chieda conferma. Se un ruolo è sbagliato, correggilo con **Modifica** nella sua pagina o con **⋯** sulla riga corrispondente in **Modifiche recenti**. La tua Machine impara dalle modifiche.

## Cosa sa di una persona

Le informazioni che la riguardano si trovano nella sua pagina, sotto **Informazioni note**; Apprendimento conserva quelle generali. Tocca **Aggiungi** per aggiungere un’informazione con parole tue. Ogni informazione ha un menu:

- **Modifica** permette di modificarla direttamente.
- **Non riguarda** questa persona la trasforma di nuovo in un’informazione generale, sotto **Apprendimento**, **Fatti**.
- **Rimuovi** la elimina ovunque.

## Modifiche recenti

**Modifiche recenti**, che trovi chiuso appena sopra la cronologia di una persona, organizzazione o progetto, elenca ciò che la tua Machine ha modificato o appreso: un ruolo, il luogo di lavoro, il rapporto tra due persone, un’informazione o un cambiamento di progetto. Ogni riga riporta la data e la fonte; tocca la fonte per leggere il messaggio.

Se una riga è sbagliata, il menu **⋯** permette di correggerla direttamente: **Modifica**, **Rimuovi**, **Non riguarda** questa persona o **Annulla** per ripristinare la posizione precedente di un progetto. Vengono mostrate tre righe; tocca **Mostra altro** per vedere le altre.

Una persona di cui la tua Machine ha aggiornato le informazioni oggi è contrassegnata da un piccolo punto nell’elenco Persone, mentre in cima all’elenco compare **4 persone aggiornate oggi**. Vedi [The Graph](graph.md).

## Un’attività su una persona

Tocca **Nuova attività** nel menu **⋯** di una persona, un’organizzazione o un progetto per creare un’attività che la riguarda.
