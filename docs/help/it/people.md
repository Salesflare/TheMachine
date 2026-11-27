---
title: Persone
area: graph
summary: Tutte le persone con cui sei in contatto: la loro pagina, il riepilogo e la cronologia, e come aggiungere, modificare, unire o eliminare una persona.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 315403ed8889dbac
---
Tutte le persone con cui sei in contatto, dalle più vicine in poi, in base ai tuoi messaggi e alle riunioni. Newsletter, ricevute e altre comunicazioni non aggiungono nessuno finché non rispondi. Le trovi in Mittenti nascosti, sotto l’elenco: **Mostra come persona** aggiunge una persona all’elenco. Campi, tag e importazioni funzionano allo stesso modo in tutti e tre gli elenchi, ognuno con i propri filtri: vedi [Il Graph](graph.md).

Una casella di posta condivisa (info@, servizio clienti, il nome di un negozio) è associata alla sua organizzazione, non a una persona, anche dopo che le scrivi.

## La pagina di una persona

Inizia con la foto, il nome, il ruolo, l’organizzazione e il luogo della persona, poi una riga che indica come siete in contatto ("Vi sentite ogni giorno · ultimo contatto ieri · prossima riunione mar 27 ott"). Il contatto recente è indicato con formule come "proprio ora", "3 ore fa", "ieri" o "3 giorni fa"; per i contatti più vecchi, viene mostrata la data. Passaci sopra con il puntatore per vedere la data esatta. Più sotto:

- **Contatto**: numeri di telefono e indirizzi email. Tocca uno di questi per chiamare o scrivere, oppure **Copia**. Qui trovi anche il **Compleanno**, con l’indicazione della fonte (contatti Google, Google Calendar, Facebook, le tue note o tu): vedi [Il Graph](graph.md#birthday).
- **Con te**: il rapporto che ha con te, se è un contatto di Lavoro o Personale e se fa parte della tua Fleet di famiglia o di lavoro, con **Vedi in Fleet**.
- **Anche su**: gli altri luoghi in cui parli con questa persona. **Slack** apre la persona in Slack o la tua chat più recente con lei.
- Le **Persone** e i **Progetti** di cui fa parte, gli **In sospeso tra voi** (promesse in entrambe le direzioni, con **Segna come fatto** e **Lascia perdere**) e la sua **Cronologia**.

Gli indirizzi e le chat di una persona vengono uniti automaticamente quando è chiaro che appartengono alla stessa persona, per esempio un’email di lavoro con il suo indirizzo personale in CC. Oppure quando una persona con cui chatti prenota una chiamata dal link che le hai inviato e l’azienda o il cognome corrispondono.

Se compare il messaggio **Impossibile caricare questa pagina.**, tocca **Riprova**. Se il messaggio continua a comparire, tocca **Qualcosa non va?** in fondo alla pagina.

## Riepilogo

In cima alla pagina di una persona trovi alcune brevi righe su decisioni, richieste, piani o promesse, con i nomi di tutte le persone coinvolte. The Machine lo riscrive quando ci sono novità, solo per le persone con cui sei davvero in contatto, e controlla ogni riga prima di mostrarla. Di solito una volta al giorno; entro poche ore se cambia qualcosa che riguarda quella persona, per esempio una nuova scadenza o una richiesta ritirata.

Le informazioni vaghe vengono omesse. Se non c’è nulla di specifico da dire, il riepilogo non viene mostrato. Ogni riga rimanda alla sua fonte: i messaggi dello stesso giorno sono raggruppati sotto un’unica data con il relativo conteggio e si aprono insieme.

**Modifica** il riepilogo per scriverlo a modo tuo. Quando ci sono novità, The Machine mostra un **Aggiornamento suggerito**, con le opzioni **Usalo** e **Tieni la mia**. Con **Lascia che lo scriva The Machine**, puoi affidarle di nuovo il riepilogo.

La preparazione per le riunioni usa il riepilogo, ma solo le righe relative all’ambito dell’attività, Lavoro o Personale. Rimane sulla tua Machine e il tuo team non può vederla.

## Cronologia

Ogni pagina di una persona o di un’organizzazione ha una cronologia, dalla più recente alla meno recente: email, riunioni e relativi riepiloghi di Zoom, conversazioni di Intercom (con **Apri in Intercom**), chat di WhatsApp, Telegram, Slack, LinkedIn e X, attività, promesse e aggiornamenti sui progetti. I filtri in alto mostrano una fonte alla volta. **Mostra altro** carica gli elementi meno recenti.

Le riunioni future sono in cima, nella sezione **In arrivo**, dalla più vicina alla più lontana. **Mostra tutti i prossimi** mostra le altre. In una riunione sono elencate le persone presenti, ciascuna una sola volta. Se sono disponibili note o una trascrizione, compaiono **Note** o **Trascrizione**: fai clic per leggerle.

Le tue cronologie sono personali: Graph del team mostra solo ciò che consentono le tue regole di condivisione. In una pagina, **Team** sopra la Cronologia aggiunge ciò che hanno condiviso le altre persone del team, indicando la fonte di ogni elemento; **Miei** mostra solo i tuoi.

## Lavoro e Personale

Le schede **Lavoro** e **Personale** elencano le persone in base al loro Tipo, indicato nella pagina. La scelta che hai fatto tu (**Modifica**) ha la precedenza. In caso contrario, le persone della tua famiglia e i tuoi amici, e chi considera te una persona di famiglia o un’amicizia (come una moglie o un padre), sono classificati come Personale, indipendentemente dall’indirizzo da cui scrivono. Il tuo team non può vedere i contatti Personali.

## Aggiungere una persona

Tocca **Nuova persona** in cima alla sezione Persone, oppure **+** nella barra in alto sul telefono. Inserisci un nome e, se li hai, un indirizzo email e un’organizzazione. Se nel tuo Graph c’è già una persona simile, il modulo la mostra per prima, così puoi aprire quella pagina. **Aggiungi** apre la nuova pagina.

La persona che aggiungi rimane nell’elenco anche se non ci sono ancora messaggi. Il primo messaggio verrà associato a lei.

## Modificare una persona

**Modifica**, in cima alla pagina, ti permette di cambiare nome, ruolo, organizzazione, luogo, LinkedIn, numeri di telefono e indirizzi email, il rapporto con te e la categoria Lavoro o Personale. Il campo **Note** serve per ricordare quello che vuoi; le note vengono conservate anche dopo un’unione. **Salva** conserva le modifiche, mentre **Annulla** le annulla.

Le modifiche che fai vengono conservate anche quando i dati vengono cercati di nuovo, e dopo **Unisci** e **Annulla**. Svuota un campo per usare di nuovo il valore trovato. Se svuoti il nome, viene ripristinato quello ricavato dai messaggi.

Per cambiare la foto, fai clic su di essa: scegli **Carica un’immagine**, seleziona una foto trovata per quella persona oppure **Rimuovi foto**. La foto rimane sulla tua Machine.

## Unire due persone

Quando due persone potrebbero essere la stessa, la loro pagina chiede se si tratta della stessa persona e la sezione Persone le mostra sotto **Stessa persona?**. **Unisci** le unisce, insieme a tutti i messaggi, le note, i ruoli e i progetti. **Non è la stessa** le mantiene separate definitivamente. La tua risposta rimane visibile per un po’ sulla coppia, che poi scompare dall’elenco. L’elenco scompare quando non ci sono più coppie da esaminare.

Una persona con un indirizzo che assomiglia soltanto a uno che conosci, per esempio acme-corp.example invece di acmecorp.example, non viene mai proposta come la stessa persona. Inoltre, solo tu puoi assegnarle un ruolo.

Un nome da solo non basta mai per associare due persone di domini diversi, perché chiunque può digitarlo. Due indirizzi di domini diversi vengono proposti solo se c’è un altro collegamento, come le stesse persone in comune o un progetto di piccole dimensioni. Se corrisponde solo il nome ("Sam" e "Sam Lee"), serve un’ulteriore corrispondenza: la stessa azienda, lo stesso numero di telefono o lo stesso profilo LinkedIn.

Una persona che usa il tuo nome con un indirizzo che non è tuo non viene mai proposta. Aggiungi gli altri tuoi indirizzi in Impostazioni, [I tuoi indirizzi](settings.md#your-addresses).

Se tra domini diversi corrisponde solo il nome (come "Sam" e "Sam Lee"), le persone vengono proposte solo se hanno lo stesso numero di telefono o lo stesso profilo LinkedIn.

Se corrisponde solo il nome tra una persona a cui hai scritto in chat e una riunione creata dalla chat, oppure se l’indirizzo appartiene a una persona che già conoscevi e solo la persona in chat dice che è suo, ti verrà chiesto di confermare. The Machine non apre mai un link per scoprirlo.

Un indirizzo condiviso, come info@ o una mailing list, non viene mai associato alle persone che lo usano per scrivere. Un contatto di lavoro esterno alla tua azienda e una chat personale che hanno in comune solo un nome non vengono associati automaticamente: vengono invece mostrati come una domanda.

**Unisci tutti** unisce tutte le coppie nell’elenco in una volta sola, tranne quelle che hai contrassegnato con **Non è la stessa**. Se tocchi **Annulla** subito dopo, le separa di nuovo tutte.

Per unire due persone manualmente, apri la pagina di una, poi tocca **⋯**, **Stessa persona di…** e scegli l’altra. Nella pagina della persona unita, sotto **Unita da**, trovi i motivi dell’unione e puoi toccare **Annulla** per separarle di nuovo.

## Eliminare definitivamente una persona

Nella sua pagina, apri il menu ⋯ e scegli **Elimina definitivamente…**, poi **Elimina**. La persona e le informazioni che la tua Machine ha su di lei vengono rimosse: la scheda, gli indirizzi, i dati cercati, i messaggi scambiati solo tra voi e le note che la riguardano.

Le attività che la coinvolgono rimangono, ma il suo nome viene rimosso. Non verrà aggiunta di nuovo, nemmeno tramite un’importazione o un’attività sui compleanni di Facebook che contiene il suo nome o indirizzo. L’operazione non si può annullare.

## Email non recapitata

Quando un’email inviata a una persona non viene recapitata, accanto al suo indirizzo compare **Non recapitata** con la data, e un suo altro indirizzo viene mostrato per primo. Le nuove bozze non verranno mai inviate a quell’indirizzo se ne è noto un altro. Se è l’unico indirizzo, la schermata di invio ti avvisa, ma puoi comunque inviare l’email.

Un’email viene considerata non recapitata quando il server di posta indica che l’indirizzo non esiste, oppure dopo 3 errori temporanei nell’arco di una settimana. L’indicazione scompare quando la persona scrive di nuovo da quell’indirizzo o quando un’email inviata lì viene recapitata.

## Ruolo e foto

Per le persone con un indirizzo aziendale, vengono cercati il ruolo, la foto, il profilo LinkedIn e la città, come descritto in [dati dell’organizzazione](organization-data.md). Su una Machine ospitata, la ricerca usa solo il nome e il dominio aziendale della persona. Per la foto, Gravatar riceve un hash dell’indirizzo di lavoro, mai l’indirizzo stesso. Puoi disattivare questa opzione in **Impostazioni**, nella sezione Sicurezza: **Cerca i contatti di lavoro**.

Questa opzione disattiva anche la consultazione del sito web prima della prima riunione e la ricerca sul web, se configurata (vedi [Preparati alle riunioni](calendar.md#ready-for-your-meetings)).

Quando la ricerca trova informazioni sulla persona, la sua pagina mostra anche la descrizione personale, da quando ricopre il ruolo attuale e i due ruoli precedenti. Anche la preparazione alle riunioni usa queste informazioni, ma la descrizione personale solo se la persona non ne ha una propria.

Le informazioni sui tuoi contatti si arricchiscono con ciò che è già disponibile: ruolo, telefono e fuso orario da Slack; descrizione personale e luogo da X; titolo e foto da LinkedIn; ruoli dai contatti Google e da Salesflare; e la foto di un contatto da Salesflare, se è salvata lì. Passa il puntatore sulla riga sotto il nome per vedere da dove provengono le informazioni.

Outlook aggiunge le foto dei colleghi della tua organizzazione e dei tuoi contatti Outlook, oltre ai ruoli e alle aziende dei tuoi contatti ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Le foto di WhatsApp e Telegram vengono aggiunte tramite la sincronizzazione di WhatsApp e la connessione alle chat di Telegram: fino a 50 al giorno per ciascun servizio, solo per le persone già nel tuo Graph. Non viene inviato loro nulla. Un’importazione dei compleanni di Facebook aggiunge la foto del profilo di una persona che non ha una foto, quando la salvi ([Routine](routines.md)). Tutto rimane sulla tua Machine.

Nel [Graph del team](team-graph.md) di una Fleet di lavoro, una piccola copia della foto di lavoro viene allegata alla scheda condivisa della persona. Non vengono condivise le foto di contatti Google, WhatsApp, Telegram o Facebook, né le foto che hai modificato o rimosso.

## Su di te

I tuoi indirizzi e numeri, compresi gli alias, appartengono sempre a te e non sono mai una persona nel tuo Graph. Se cerchi te o aggiungi una persona con uno dei tuoi indirizzi, si apre **Su di te**; durante un’importazione, la tua riga viene ignorata.

La sezione Su di te mostra i tuoi indirizzi e la relativa origine. Puoi modificarli in **Impostazioni**, nella sezione Account. Per inviare il tuo contatto a una persona del team o a un’amicizia, scegli **Condividi il mio contatto**. Vedi [Condividi un contatto](share-contact.md).

## Il rapporto che ha con te

I ruoli che la tua Machine rileva nei messaggi compaiono nella pagina della persona, sotto **Per te**, insieme alle sole parole che indicano il ruolo, per esempio un titolo. Dire di essere il tuo commercialista o un tuo cliente non basta: serve anche un riscontro da parte tua, per esempio nei tuoi messaggi o nelle riunioni con quella persona. Non devi confermare nulla. Se un’informazione è errata, puoi correggerla con **Modifica** nella pagina della persona o con **⋯** sulla relativa riga in **Modifiche recenti**. La Machine impara dalle tue modifiche.

## Cosa sa su una persona

Le informazioni su una persona si trovano nella sua pagina, sotto **Informazioni note**; Apprendimento raccoglie quelle generali. Con **Aggiungi** puoi inserire altre informazioni usando parole tue. Ogni informazione ha un menu:

- **Modifica** permette di modificarla direttamente.
- **Non riguarda** la persona la rende di nuovo un’informazione generale, sotto **Apprendimento**, **Fatti**.
- **Rimuovi** la elimina ovunque.

## Modifiche recenti

**Modifiche recenti**, chiuse appena sopra la cronologia di una persona, di un’organizzazione o di un progetto, elenca ciò che la tua Machine ha modificato o imparato: un ruolo, il luogo di lavoro, il rapporto tra due persone, un’informazione o un aggiornamento di progetto. Ogni riga mostra la data e la fonte. Tocca la fonte per leggere il messaggio.

Se una riga è errata, puoi correggerla direttamente dal menu **⋯**: scegli **Modifica**, **Rimuovi**, **Non riguarda** la persona oppure **Annulla** per ripristinare la posizione precedente di un progetto. Vengono mostrate tre righe; **Mostra altro** visualizza le altre.

Una persona aggiornata oggi dalla tua Machine è contrassegnata da un puntino nell’elenco Persone. In cima all’elenco, **4 persone aggiornate oggi** indica chi sono. Vedi [Il Graph](graph.md).

## Un’attività su una persona

**Nuova attività**, nel menu **⋯** di una persona, un’organizzazione o un progetto, crea un’attività che la riguarda.
