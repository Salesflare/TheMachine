---
title: Persone
area: graph
summary: Tutte le persone con cui sei in contatto: la loro pagina, il riepilogo e la cronologia, e come aggiungere, modificare, unire o eliminare una persona.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 84312952f04b8597
---
Tutte le persone con cui sei in contatto, dalle più vicine in poi, in base ai messaggi e alle riunioni. Newsletter, ricevute e altre comunicazioni non aggiungono nessuno finché non rispondi. Le trovi in Mittenti nascosti, sotto l’elenco: **Mostra come persona** aggiunge una persona. Campi, tag e importazioni funzionano allo stesso modo in tutti e tre gli elenchi, ognuno con i propri filtri: vedi [Il Graph](graph.md).

Una casella condivisa (info@, assistenza clienti, il nome di un negozio) viene associata alla sua organizzazione, non a una persona, anche se le scrivi.

## La pagina di una persona

Inizia con la foto, il nome, il ruolo, l’organizzazione e la località della persona, più una riga che riassume i vostri contatti ("Parlate ogni giorno · ultimo contatto ieri · prossima riunione mar 27 ott"). Il contatto recente è indicato con formule come "proprio ora", "3 ore fa", "ieri" o "3 giorni fa"; quello meno recente mostra una data. Passaci sopra con il puntatore per vedere la data esatta. Sotto trovi:

- **Contatto**: numeri di telefono e indirizzi email. Tocca un recapito per chiamare o scrivere, oppure **Copia** per copiarlo. Qui trovi anche il **Compleanno**, con l’indicazione della fonte (Contatti Google, Google Calendar, Facebook, le tue note o tu): vedi [Il Graph](graph.md#birthday).
- **Con te**: il ruolo che ha per te, se è un contatto di lavoro o personale, e la Fleet di famiglia o di lavoro a cui appartiene, con **Vedi in Fleet**.
- **Anche su**: gli altri luoghi in cui parli con la persona. **Slack** apre il suo profilo su Slack oppure la vostra chat più recente su Slack.
- Le **Persone** e i **Progetti** di cui fa parte, gli **In sospeso tra voi** (promesse reciproche, con **Segna come fatto** e **Lascia perdere**) e la **Cronologia**.

Gli indirizzi e le chat di una persona vengono associati automaticamente quando è chiaro che appartengono alla stessa persona, per esempio un indirizzo email di lavoro e un suo indirizzo in CC. Succede anche quando una persona con cui chatti prenota una chiamata dal link che le hai inviato e l’azienda o il cognome corrispondono.

Se compare il messaggio **Impossibile caricare questa pagina.**, tocca **Riprova**. Se continua a comparire, usa **Qualcosa non va?** in fondo alla pagina.

## Riepilogo

In cima alla pagina di una persona trovi poche righe su decisioni, domande, piani o promesse, con i nomi di tutte le persone coinvolte. The Machine le riscrive quando ci sono novità, solo per le persone con cui sei davvero in contatto, e verifica ogni riga prima di mostrarla. Di solito una volta al giorno; entro poche ore se cambia qualcosa che le riguarda, per esempio una nuova scadenza o una richiesta ritirata.

Le righe vaghe vengono omesse: se non c’è nulla di specifico da dire, non compare un riepilogo. Ogni riga rimanda alla fonte: i messaggi dello stesso giorno sono raggruppati sotto un’unica data con il numero di messaggi e si aprono insieme.

**Modifica** il riepilogo per esprimerti a modo tuo. Quando ci sono novità, The Machine mostra un **Aggiornamento suggerito**, con le opzioni **Usalo** e **Tieni la mia**. **Lascia che lo scriva The Machine** per affidarle di nuovo il riepilogo.

La preparazione delle riunioni usa questo riepilogo, ma solo le righe relative a quel to-do, di lavoro o personale. Resta sulla tua Machine; il tuo team non lo vede.

## Cronologia

Ogni pagina di persona e organizzazione ha una cronologia, in ordine dal più recente: email, riunioni e relativi riepiloghi Zoom, conversazioni Intercom (con **Apri in Intercom**), chat WhatsApp, Telegram, Slack, LinkedIn e X, attività, promesse e aggiornamenti sui progetti. I filtri in alto mostrano una fonte alla volta. **Mostra altro** carica gli elementi meno recenti.

Le riunioni future compaiono in alto, nella sezione **In arrivo**, dalla più vicina in poi; **Mostra tutti i prossimi** mostra anche le altre. Ogni riunione indica chi vi ha partecipato, una sola volta per persona. Quelle con appunti o trascrizioni riportano **Note** o **Trascrizione**: selezionale per leggerle.

Le tue cronologie sono private: il Graph del team mostra solo ciò che consentono le tue regole di condivisione. In una pagina, **Team** sopra la Cronologia aggiunge i contenuti condivisi dai colleghi, indicando chi li ha condivisi; **Miei** mostra solo i tuoi.

## Lavoro e personale

Le schede **Lavoro** e **Personale** elencano le persone in base al tipo indicato nella loro pagina. Fa fede la scelta che hai fatto tu (**Modifica**). Altrimenti, i membri della tua famiglia e i tuoi amici, oltre a familiari e amici per te (come una moglie o un padre), sono considerati contatti personali, qualunque sia l’indirizzo da cui scrivono. Il tuo team non vede i contatti personali.

## Aggiungere una persona

Seleziona **Nuova persona** in cima alla sezione Persone oppure **+** nella barra superiore sul telefono. Inserisci un nome e, se li conosci, un indirizzo email e un’organizzazione. Se nel tuo Graph c’è già una persona simile, il modulo la mostra per prima, così puoi aprire la sua pagina invece di crearne una nuova. **Aggiungi** apre la nuova pagina.

La persona che aggiungi resta anche se non ci sono ancora messaggi. Il primo messaggio verrà associato alla sua pagina.

## Modificare una persona

**Modifica**, in cima alla sua pagina, permette di cambiare nome, ruolo, organizzazione, località, profilo LinkedIn, numeri di telefono e indirizzi email, il suo ruolo per te e se è un contatto di lavoro o personale. Il campo **Note** serve per ricordare ciò che vuoi; le note restano anche dopo un’unione. **Salva** conserva le modifiche, mentre **Annulla** lascia tutto com’era.

Le tue modifiche restano anche quando i dettagli vengono cercati di nuovo, e dopo **Unisci** e **Annulla**. Svuota un campo per riutilizzare il valore trovato. Se svuoti il nome, viene ripristinato quello usato nei suoi messaggi.

Per cambiare la foto, selezionala: scegli **Carica un’immagine**, una foto trovata per la persona oppure **Rimuovi foto**. La foto resta sulla tua Machine.

## Unire due persone

Se due persone potrebbero essere la stessa, la loro pagina te lo chiede e la sezione Persone le elenca sotto **Stessa persona?**. **Unisci** le riunisce, includendo tutti i messaggi, le note, i ruoli e i progetti. **Non è la stessa** le mantiene separate definitivamente. La tua risposta resta visibile per qualche istante, poi la coppia scompare dall’elenco. L’elenco scompare quando non ci sono più casi da verificare.

Una persona con un indirizzo che somiglia solo a uno che conosci, per esempio acme-corp.example invece di acmecorp.example, non viene mai proposta come la stessa persona. Solo tu puoi assegnarle un ruolo.

Il solo nome non basta mai per associare persone con domini diversi, perché chiunque può scrivere un nome: due indirizzi con domini diversi vengono proposti solo se c’è un altro collegamento, come persone in comune o un progetto di piccole dimensioni. Per associare solo in base al nome («Sam» e «Sam Lee») serve un altro elemento, come la stessa azienda, lo stesso numero di telefono o lo stesso profilo LinkedIn.

Una persona che usa il tuo nome con un indirizzo che non è tuo non viene mai proposta. Aggiungi invece gli altri tuoi indirizzi in **Impostazioni**, alla voce [I tuoi indirizzi](settings.md#your-addresses).

Se tra domini diversi corrisponde solo il nome, come «Sam» e «Sam Lee», le persone vengono proposte solo se hanno lo stesso numero di telefono o lo stesso profilo LinkedIn.

Se corrisponde solo il nome di una riunione creata da una chat, oppure l’indirizzo appartiene a una persona che già conoscevi e solo la persona in chat dice che è suo, ti verrà chiesto di confermare. The Machine non apre mai un link per verificarlo.

Un indirizzo condiviso, come info@ o una mailing list, non viene mai associato alle persone che scrivono tramite quell’indirizzo. Un contatto di lavoro esterno alla tua azienda e una chat personale che hanno in comune solo il nome non vengono associati automaticamente: vengono elencati come caso da verificare.

**Unisci tutti** unisce in una volta tutte le coppie nell’elenco, tranne quelle che hai contrassegnato con **Non è la stessa**. Seleziona **Annulla** subito dopo per separarle di nuovo.

Per unire due persone manualmente, apri la pagina di una delle due, poi seleziona **⋯**, **Stessa persona di…** e scegli l’altra. Nella pagina della persona unita trovi il motivo alla voce **Unita da**, con **Annulla** per separarle di nuovo.

## Eliminare una persona definitivamente

Nella sua pagina, apri il menu ⋯ e seleziona **Elimina definitivamente…**, poi **Elimina**. La persona e le informazioni che la tua Machine conserva su di lei verranno rimosse: la scheda, gli indirizzi, i dettagli cercati, i messaggi solo tra voi e le note che la riguardano.

Le attività che la riguardano restano, ma senza il suo nome. La persona non verrà aggiunta di nuovo, nemmeno tramite un’importazione o un’attività per i compleanni di Facebook con il suo nome o indirizzo. L’operazione non si può annullare.

## Email non recapitate

Quando un’email inviata a una persona non viene recapitata, il suo indirizzo mostra **Non recapitata** con la data e, se è noto, compare prima un altro suo indirizzo. Se è noto un altro indirizzo, le nuove bozze non useranno mai quello non recapitato. Se è l’unico indirizzo, il pannello di invio ti avvisa, ma puoi comunque inviare l’email.

Un indirizzo viene contrassegnato come non recapitabile se il server di posta segnala che non esiste, oppure dopo 3 errori temporanei nell’arco di una settimana. L’indicazione scompare quando la persona scrive di nuovo da quell’indirizzo o quando un’email inviata lì viene recapitata.

## Ruolo e foto

Per le persone con un indirizzo aziendale, il ruolo, la foto, il profilo LinkedIn e la città vengono cercati come i [dettagli dell’organizzazione](organization-data.md). Su una Machine ospitata, la ricerca usa solo il nome e il dominio dell’azienda. Per la foto, Gravatar riceve un hash dell’indirizzo di lavoro, mai l’indirizzo stesso. Per disattivare la ricerca, vai in **Impostazioni**, nella sezione Sicurezza, e disattiva **Cerca i contatti di lavoro**.

Questa opzione disattiva anche la consultazione dei siti prima della prima riunione e la ricerca sul web (vedi [Preparati alle riunioni](calendar.md#ready-for-your-meetings)).

Se la ricerca trova informazioni, nella pagina della persona compaiono anche la biografia, da quando ricopre il ruolo attuale e i due ruoli precedenti. Le usa anche la preparazione delle riunioni, ma la biografia solo se la persona non ne ha una propria.

Le informazioni sui tuoi contatti si arricchiscono con quelle che hanno già condiviso: un ruolo, un numero di telefono e il fuso orario da Slack; una biografia e una località da X; un titolo e una foto da LinkedIn; i ruoli da Contatti Google e Salesflare; e la foto di un contatto da Salesflare, se è presente. Passa il puntatore sulla riga sotto il nome per vedere da dove provengono le informazioni.

Outlook aggiunge le foto dei colleghi della tua organizzazione e dei tuoi contatti Outlook, oltre ai ruoli e alle aziende dei tuoi contatti ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Le foto WhatsApp e Telegram vengono aggiunte tramite la sincronizzazione WhatsApp e la connessione alle chat Telegram: fino a 50 al giorno per ciascun servizio, solo per le persone già presenti nel tuo Graph. Non viene inviato loro nulla. Un’importazione dei compleanni di Facebook aggiunge la foto del profilo di una persona senza foto quando la salvi ([Routine](routines.md)). Tutto resta sulla tua Machine.

Nel [Graph del team](team-graph.md) di una Fleet di lavoro, una piccola copia della foto di lavoro accompagna la scheda condivisa della persona. Le foto da Contatti Google, WhatsApp, Telegram o Facebook, così come quelle che hai cambiato o rimosso, non vengono mai condivise.

## Su di te

I tuoi indirizzi e numeri, compresi gli alias, sono sempre tuoi e non vengono mai trattati come persone nel tuo Graph. Se cerchi te stesso o aggiungi una persona con uno dei tuoi indirizzi, si apre **Su di te**; un’importazione salta la riga che ti riguarda.

La sezione Su di te elenca i tuoi indirizzi e indica la provenienza di ciascuno. Per modificarli, vai in **Impostazioni**, nella sezione Account. Per inviare il tuo contatto a un collega o a un amico, seleziona **Condividi il mio contatto**. Vedi [Condividi un contatto](share-contact.md).

## Il suo ruolo per te

I ruoli che la tua Machine rileva nei messaggi compaiono nella pagina della persona, alla voce **Per te**, insieme alle parole che indicano il ruolo, come un titolo. Dire di essere il tuo commercialista o cliente non basta: serve anche qualcosa da parte tua, come i tuoi messaggi o le riunioni con quella persona. Non è necessario confermare nulla. Se un’informazione è sbagliata, correggila con **Modifica** nella sua pagina oppure con **⋯** sulla riga corrispondente in **Modifiche recenti**. La tua Machine impara dalle modifiche.

## Cosa sa di una persona

Le informazioni su una persona si trovano nella sua pagina, alla voce **Informazioni note**; quelle più generali restano in Apprendimento. **Aggiungi** per salvarne un’altra con parole tue. Ogni informazione ha un menu:

- **Modifica** la cambia direttamente.
- **Non riguarda** la persona la trasforma di nuovo in un’informazione generale, in **Apprendimento**, alla voce **Fatti**.
- **Rimuovi** la elimina ovunque.

## Modifiche recenti

**Modifiche recenti**, nella sezione ripiegata appena sopra la cronologia di una persona, un’organizzazione o un progetto, elenca ciò che la tua Machine ha cambiato o imparato: un ruolo, il luogo di lavoro, il rapporto tra due persone, un’informazione o un cambiamento di progetto. Ogni riga indica la data e la fonte; tocca la fonte per leggere il messaggio.

Se una riga è sbagliata, usa **⋯** per correggerla direttamente: **Modifica**, **Rimuovi**, **Non riguarda** la persona oppure **Annulla** per ripristinare la posizione precedente di un progetto. Vengono mostrate tre righe; **Mostra altro** visualizza le altre.

Una persona aggiornata oggi dalla tua Machine è contrassegnata da un puntino nell’elenco Persone. In cima all’elenco compare anche **4 persone aggiornate oggi**, con i loro nomi. Vedi [Il Graph](graph.md).

## Un’attività su una persona

**Nuova attività** nel menu **⋯** di una persona, un’organizzazione o un progetto crea un’attività che la riguarda.
