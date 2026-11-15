---
title: Persone
area: graph
summary: Tutte le persone con cui sei in contatto: la loro pagina, il riepilogo e la cronologia, e come aggiungere, modificare, unire o eliminare una persona.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 907cec019dc70184
---
Tutte le persone con cui sei in contatto, dalle più vicine in poi, in base ai messaggi e alle riunioni. Le newsletter, le ricevute e le altre comunicazioni non aggiungono nessuno finché non rispondi. Le trovi in Mittenti nascosti, sotto l’elenco: **Mostra come persona** aggiunge una persona. Campi, tag e importazioni funzionano allo stesso modo in tutti e tre gli elenchi, ma ognuno ha i propri filtri: vedi [The Graph](graph.md).

Una casella condivisa (info@, assistenza clienti, il nome di un negozio) viene associata alla sua organizzazione, non a una persona, anche se le scrivi.

## La pagina di una persona

In alto trovi la foto, il nome, il ruolo, l’organizzazione e la località, oltre a una riga che riassume i vostri contatti ("Vi sentite ogni giorno · ultimo contatto ieri · prossima riunione mar 27 ott"). Il contatto più recente è indicato con formule come "proprio ora", "3 ore fa", "ieri" o "3 giorni fa"; per i contatti meno recenti, viene mostrata la data. Passaci sopra il puntatore per vedere la data esatta. Più in basso trovi:

- **Contatto**: numeri di telefono e indirizzi email. Tocca un numero o un indirizzo per chiamare o scrivere, oppure **Copia** per copiarlo. Qui trovi anche il **Compleanno**, con la fonte (Google contacts, Google Calendar, Facebook, le tue note o tu): vedi [The Graph](graph.md#birthday).
- **Con te**: che rapporto avete, se è un contatto di Lavoro o Personale e se fa parte della tua famiglia o del tuo Fleet, con **Vedi in Fleet**.
- **Anche su**: gli altri luoghi in cui vi sentite. **Slack** apre il suo profilo in Slack oppure la conversazione più recente che avete avuto su Slack.
- Le **Persone** e i **Progetti** di cui fa parte, le **In sospeso tra voi** (promesse in entrambe le direzioni, con **Segna come fatto** e **Lascia perdere**) e la sua **Cronologia**.

Gli indirizzi e le chat della stessa persona vengono collegati automaticamente quando è chiaro che appartengono alla stessa persona, per esempio un indirizzo email di lavoro con il suo indirizzo personale in CC.

Se la pagina mostra **Impossibile caricare questa pagina.**, tocca **Riprova**. Se il messaggio continua a comparire, usa **Qualcosa non va?** in fondo alla pagina.

## Riepilogo

In cima alla pagina di una persona trovi alcune brevi righe che riassumono decisioni, richieste, piani o promesse, indicando tutti i nomi. The Machine lo riscrive quando ci sono novità, solo per le persone con cui sei davvero in contatto, e verifica ogni riga prima di mostrarla. Di solito lo aggiorna una volta al giorno; quando cambia qualcosa che riguarda quella persona, come una nuova scadenza o una richiesta ritirata, lo aggiorna entro poche ore.

Le righe vaghe vengono omesse; se non c’è nulla di specifico da dire, il riepilogo non viene mostrato. Ogni riga rimanda alla fonte: i messaggi dello stesso giorno condividono una data che indica quanti sono e si aprono insieme.

**Modifica** il riepilogo per riscriverlo a modo tuo. Quando ci sono novità, The Machine mostra un **Aggiornamento suggerito**, con le opzioni **Usalo** e **Tieni la mia**. **Lascia che lo scriva The Machine** per affidarle di nuovo il riepilogo.

Le preparazioni per le riunioni usano il riepilogo, ma solo le righe relative all’attività di Lavoro o Personale. Rimane sulla tua Machine: il team non lo vede.

## Cronologia

Ogni pagina di una persona o organizzazione ha una cronologia, dalla più recente alla meno recente: email, riunioni e relativi riepiloghi Zoom, conversazioni Intercom (con **Apri in Intercom**), chat WhatsApp, Telegram, Slack, LinkedIn e X, attività, promesse e aggiornamenti sui progetti. I filtri in alto mostrano una fonte alla volta. **Mostra altro** carica gli elementi meno recenti.

Le riunioni future compaiono in cima, in **In arrivo**, dalla più vicina alla più lontana. **Mostra tutti i prossimi** mostra anche le altre. Per ogni riunione vengono indicati i partecipanti, una sola volta a testa. Se ci sono note o una trascrizione, trovi **Note** o **Trascrizione**: fai clic per leggerle.

Le tue cronologie sono private: il Graph del team mostra solo ciò che consentono le tue regole di condivisione. Nella pagina, **Team** sopra la cronologia aggiunge ciò che hanno condiviso i tuoi colleghi e indica chi ha condiviso ogni elemento; **Miei** mostra solo i tuoi.

## Lavoro e Personale

Le schede **Lavoro** e **Personale** elencano le persone in base al tipo indicato nella loro pagina. La tua scelta (**Modifica**) ha la precedenza. Altrimenti, la tua famiglia e i tuoi amici, e i tuoi familiari o amici (come una moglie o un padre), vengono considerati Personali, qualunque sia l’indirizzo da cui scrivono. Il tuo team non vede i contatti Personali.

## Aggiungere una persona

Tocca **Nuova persona** in cima a Persone, oppure **+** nella barra superiore sul telefono. Inserisci un nome e, se li hai, un indirizzo email e un’organizzazione. Se nel tuo Graph c’è già una persona simile, il modulo te la mostra per prima, così puoi aprire la sua pagina. **Aggiungi** crea la nuova pagina.

La persona che aggiungi rimane anche se non ci sono ancora messaggi. Il primo messaggio che ricevi da lei viene collegato al suo profilo.

## Modificare una persona

**Modifica**, in cima alla sua pagina, ti permette di cambiare nome, ruolo, organizzazione, località, LinkedIn, numeri di telefono e indirizzi email, il vostro rapporto e il tipo, Lavoro o Personale. Il campo **Note** serve a ricordare quello che vuoi; le note rimangono anche dopo un’unione. **Salva** applica le modifiche, mentre **Annulla** le annulla.

Le modifiche che fai rimangono anche quando i dettagli vengono cercati di nuovo, e dopo **Unisci** e **Annulla**. Svuota un campo per usare di nuovo il valore trovato automaticamente. Se svuoti il nome, viene ripristinato quello usato nei messaggi.

Per cambiare la foto, fai clic su di essa: puoi **Carica un’immagine**, sceglierne una trovata per la persona oppure **Rimuovi foto**. La foto rimane sulla tua Machine.

## Unire due persone

Quando due profili potrebbero appartenere alla stessa persona, la pagina te lo chiede e l’elenco Persone li mostra in **Stessa persona?**. **Unisci** li collega, insieme a tutti i messaggi, le note, i ruoli e i progetti. **Non è la stessa** li tiene separati definitivamente. La tua risposta viene mostrata per qualche istante nella coppia, che poi scompare dall’elenco. L’elenco scompare quando non ci sono più coppie da controllare.

Un indirizzo che somiglia a uno che conosci, come acme-corp.example rispetto ad acmecorp.example, non viene mai proposto come appartenente alla stessa persona. Solo tu puoi assegnare un ruolo a chi lo usa.

Il solo nome non basta mai per unire due persone di domini diversi, perché chiunque può inserirlo: due indirizzi con domini diversi vengono proposti solo se c’è un altro collegamento, come le stesse persone o un progetto. Un indirizzo che usa il tuo nome ma non è tuo non viene mai proposto. Aggiungi invece gli altri tuoi indirizzi in Impostazioni, [I tuoi indirizzi](settings.md#your-addresses).

Un indirizzo condiviso, come info@ o una lista di distribuzione, non viene mai collegato alle persone che lo usano per scrivere. Un contatto di lavoro esterno alla tua azienda e una chat personale che hanno in comune solo il nome non vengono collegati automaticamente: vengono mostrati come una domanda.

**Unisci tutti** unisce in una volta tutte le coppie nell’elenco, tranne quelle che hai contrassegnato con **Non è la stessa**. **Annulla** subito dopo le separa di nuovo.

Per unire due persone manualmente, apri una delle loro pagine, poi tocca **⋯**, **Stessa persona di…** e scegli l’altra persona. Nella pagina della persona unita trovi i motivi dell’unione in **Unita da**, con **Annulla** per separarle.

## Eliminare una persona definitivamente

Nella sua pagina, apri il menu ⋯ e scegli **Elimina definitivamente…**, poi **Elimina**. La persona e tutte le informazioni che la tua Machine conosce su di lei verranno rimosse: il suo profilo, gli indirizzi, i dettagli trovati automaticamente, i messaggi scambiati solo tra voi e le note che la riguardano.

Le attività che la coinvolgono rimangono, ma il suo nome viene rimosso. Non verrà aggiunta di nuovo, neanche tramite un’importazione o un’attività sui compleanni di Facebook con il suo nome o indirizzo. L’operazione non si può annullare.

## Email respinta

Quando un’email inviata a una persona viene respinta, il suo indirizzo mostra **Respinta** con la data e, se disponibile, viene messo in cima un altro suo indirizzo. Le nuove bozze non vengono mai inviate a quell’indirizzo se se ne conosce un altro. Se è l’unico indirizzo disponibile, la schermata di invio ti avvisa, ma puoi comunque inviare l’email.

Un’email viene considerata respinta se il server di posta segnala che l’indirizzo non esiste oppure dopo 3 errori temporanei nell’arco di una settimana. La segnalazione viene cancellata quando la persona scrive di nuovo da quell’indirizzo o quando un’email inviata a quell’indirizzo viene recapitata.

## Ruolo e foto

Le persone con un indirizzo aziendale hanno un ruolo, una foto, LinkedIn e una città, cercati come i [dettagli dell’organizzazione](organization-data.md). Su una Machine ospitata, la ricerca usa solo il nome e il dominio aziendale. Per la foto, Gravatar riceve l’hash dell’indirizzo di lavoro, mai l’indirizzo stesso. Puoi disattivare questa opzione in **Impostazioni**, nella sezione Sicurezza: **Cerca i contatti di lavoro**.

Se le informazioni vengono trovate, la pagina mostra anche la descrizione, da quando la persona ricopre il ruolo attuale e i due ruoli precedenti. Le preparazioni usano anche queste informazioni; la descrizione viene inclusa solo se la persona non ne ha una propria.

I tuoi contatti si arricchiscono anche delle informazioni che hanno già condiviso: ruolo, telefono e fuso orario da Slack; descrizione e località da X; titolo e foto da LinkedIn; ruoli da Google contacts e Salesflare; e la foto del contatto da Salesflare, se è stata salvata lì. Passa il puntatore sulla riga sotto il nome per vedere da dove provengono le informazioni.

Outlook aggiunge le foto dei colleghi della tua organizzazione e dei tuoi contatti Outlook, oltre ai ruoli e alle aziende dei tuoi contatti ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Le foto WhatsApp e Telegram vengono aggiunte tramite la sincronizzazione WhatsApp e la connessione alle chat Telegram: fino a 50 al giorno per ciascuna app, solo per le persone già presenti nel tuo Graph. Non viene inviato loro nulla. Un’importazione dei compleanni di Facebook aggiunge la foto del profilo delle persone senza foto quando la salvi ([Routine](routines.md)). Tutto rimane sulla tua Machine.

Nel [Team Graph](team-graph.md) di un Fleet di Lavoro, una copia ridotta della foto di lavoro accompagna il profilo condiviso della persona. Le foto da Google contacts, WhatsApp, Telegram o Facebook, così come quelle che hai modificato o rimosso, non vengono mai condivise.

## Su di te

I tuoi indirizzi e numeri, compresi gli alias, appartengono sempre a te e non sono mai una persona nel tuo Graph. Se cerchi te stesso o aggiungi una persona usando uno dei tuoi indirizzi, si apre **Su di te**. Le importazioni ignorano la tua riga.

La sezione Su di te mostra i tuoi indirizzi e la relativa fonte. Per modificarli, vai in **Impostazioni**, nella sezione Account. Per inviare il tuo contatto a un collega o a un amico, scegli **Condividi il mio contatto**. Vedi [Condividere un contatto](share-contact.md).

## Il suo rapporto con te

I ruoli che la tua Machine rileva nei messaggi vengono mostrati nella pagina della persona, sotto **Per te**, insieme alla frase da cui sono stati dedotti. Non serve aspettare che ti venga chiesto. Se un ruolo è sbagliato, correggilo con **Modifica** nella sua pagina oppure con **⋯** sulla relativa riga in **Modifiche recenti**. La tua Machine impara dalle modifiche.

## Cosa sa di una persona

Le informazioni su una persona si trovano nella sua pagina, sotto **Informazioni note**; Apprendimento conserva quelle generali. **Aggiungi** ti permette di inserire altre informazioni con parole tue. Ogni informazione ha un menu:

- **Modifica** la modifica direttamente.
- **Non riguarda** quella persona la riporta tra le informazioni generali, sotto **Apprendimento**, **Fatti**.
- **Rimuovi** la elimina ovunque.

## Modifiche recenti

**Modifiche recenti**, che puoi espandere sopra la cronologia di una persona, un’organizzazione o un progetto, elenca ciò che la tua Machine ha modificato o imparato: un ruolo, il luogo di lavoro di una persona, il rapporto tra due persone, un fatto o un cambiamento di progetto. Ogni riga mostra la data e la fonte; toccala per leggere il messaggio.

Se una riga è sbagliata, il menu **⋯** ti permette di correggerla direttamente: **Modifica**, **Rimuovi**, **Non riguarda** quella persona oppure **Annulla** per ripristinare la posizione precedente di un progetto. Vengono mostrate tre righe; **Mostra altro** mostra le altre.

Se la tua Machine ha aggiornato una persona oggi, nell’elenco Persone compare un piccolo punto e in cima all’elenco trovi **4 persone aggiornate oggi**, con i loro nomi. Vedi [The Graph](graph.md).

## Un’attività su una persona

**Nuova attività** nel menu **⋯** di una persona, un’organizzazione o un progetto crea un’attività che la riguarda.
