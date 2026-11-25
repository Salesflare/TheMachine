---
title: Persone
area: graph
summary: Tutte le persone con cui sei in contatto: la loro pagina, il riepilogo e la cronologia, e come aggiungere, modificare, unire o eliminare una persona.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 5e671ff84b143e74
---
Tutte le persone con cui sei in contatto, dalle più vicine in poi, in base ai tuoi messaggi e alle tue riunioni. Le newsletter, le ricevute e gli altri messaggi inviati in massa non aggiungono nessuno finché non rispondi. Li trovi in Mittenti nascosti, sotto l’elenco: **Mostra come persona** aggiunge una persona. Campi, tag e importazioni funzionano allo stesso modo in tutti e tre gli elenchi, ognuno con i propri filtri: vedi [Il Graph](graph.md).

Una casella condivisa (info@, assistenza clienti, il nome di un negozio) viene associata alla sua organizzazione, non a una persona, anche se le scrivi.

## La pagina di una persona

In cima trovi la foto, il nome, il titolo, l’organizzazione e il luogo, oltre a una riga che riassume come siete in contatto ("Parlate ogni giorno · ultimo contatto ieri · prossima riunione mar 27 ott"). Il contatto più recente è indicato come "adesso", "3 ore fa", "ieri" o "3 giorni fa"; per i contatti meno recenti viene mostrata una data. Passaci sopra con il puntatore per vedere la data esatta. Sotto trovi:

- **Contatto**: i suoi numeri di telefono e indirizzi email. Tocca un dato per chiamare o scrivere, oppure **Copia** per copiarlo. Qui trovi anche il suo **Compleanno**, con l’indicazione della fonte (Contatti Google, Google Calendar, Facebook, le tue note o tu): vedi [Il Graph](graph.md#birthday).
- **Con te**: che ruolo ha per te, se è un contatto di Lavoro o Personale e a quale Fleet di famiglia o Fleet appartiene, con **Vedi in Fleet**.
- **Anche su**: gli altri luoghi in cui parli con questa persona. **Slack** apre il suo profilo in Slack o la conversazione più recente che avete avuto lì.
- Le **Persone** e i **Progetti** di cui fa parte, le **In sospeso tra voi** (promesse reciproche, con **Segna come completata** e **Lascia perdere**) e la sua **Cronologia**.

Gli indirizzi e le chat della stessa persona vengono uniti automaticamente quando è chiaro che si tratta di una sola persona, per esempio se un’email di lavoro è in copia al suo indirizzo personale. Succede anche quando una persona con cui chatti prenota una chiamata dal link che le hai inviato lì e corrispondono il nome dell’azienda o il cognome.

Se la pagina mostra **Impossibile caricare la pagina.**, tocca **Riprova**. Se il messaggio continua a comparire, tocca **Qualcosa non va?** in fondo alla pagina.

## Riepilogo

In cima alla pagina di una persona trovi alcune righe brevi che riassumono decisioni, domande, piani o promesse, indicando tutte le persone coinvolte. The Machine le riscrive quando ci sono novità, solo per le persone con cui sei davvero in contatto, e verifica ogni riga prima di mostrarla. Di solito una volta al giorno; entro poche ore se cambia qualcosa che riguarda quella persona, per esempio una nuova scadenza o una richiesta ritirata.

Le informazioni vaghe vengono omesse: se non c’è niente di specifico da dire, il riepilogo non viene mostrato. Ogni riga rimanda alla fonte: i messaggi dello stesso giorno sono raccolti sotto un’unica data, con il numero di messaggi, e si aprono insieme.

Tocca **Modifica** per riscriverlo a modo tuo. Quando ci sono novità, The Machine mostra un **Aggiornamento suggerito**, con le opzioni **Usalo** e **Tieni la mia**. **Lascia che lo scriva The Machine** glielo restituisce.

Le preparazioni per le riunioni usano questo riepilogo, ma solo le righe relative a quella specifica attività (Lavoro o Personale). Rimane sulla tua Machine e il tuo team non può vederlo.

## Cronologia

Ogni pagina di una persona o di un’organizzazione ha una cronologia, dalla più recente: email, riunioni e relativi riepiloghi Zoom, conversazioni Intercom (con **Apri in Intercom**), chat WhatsApp, Telegram, Slack, LinkedIn e X, attività, promesse e aggiornamenti sui progetti. I filtri in alto mostrano una fonte alla volta. **Mostra altro** carica gli elementi meno recenti.

Le prossime riunioni vengono mostrate in cima, sotto **In arrivo**, dalla più vicina alla più lontana. **Mostra tutti i prossimi** mostra le altre. Per ogni riunione vengono indicate le persone presenti, ciascuna una sola volta. Se sono disponibili note o una trascrizione, trovi **Note** o **Trascrizione**: tocca per leggerle.

Le tue cronologie sono private: il Graph del team mostra solo ciò che consentono le tue regole di condivisione. Nella pagina, tocca **Team** sopra la Cronologia per vedere ciò che hanno condiviso i tuoi colleghi, con il nome di chi ha condiviso ogni elemento. **Miei** mostra solo i tuoi.

## Lavoro e Personale

Le schede **Lavoro** e **Personale** elencano le persone in base al loro tipo, indicato nella loro pagina. Fa fede la scelta che hai fatto tu con **Modifica**. Altrimenti, le persone della tua famiglia e i tuoi amici, così come chi è tuo parente o amico (una moglie, un padre), sono considerati Personale, a prescindere dall’indirizzo da cui scrivono. Il tuo team non vede mai i contatti Personali.

## Aggiungere una persona

Tocca **Nuova persona** in cima alla pagina Persone, oppure **+** nella barra in alto sul telefono. Inserisci un nome e, se li hai, un indirizzo email e un’organizzazione. Se nel tuo Graph c’è già una persona simile, il modulo la mostra per prima, così puoi aprire quella scheda. Tocca **Aggiungi** per aprire la nuova pagina.

La persona che aggiungi rimane anche se non ci sono ancora messaggi. Il primo messaggio verrà associato alla sua scheda.

## Modificare una persona

Tocca **Modifica** in cima alla sua pagina per cambiare nome, titolo, organizzazione, luogo, LinkedIn, numeri di telefono e indirizzi email, il suo ruolo per te e se è una persona di Lavoro o Personale. Nel campo **Note** puoi scrivere ciò che vuoi ricordare; le note vengono mantenute quando unisci le schede. Tocca **Salva** per salvare le modifiche o **Annulla** per annullarle.

Le modifiche rimangono anche quando i suoi dati vengono cercati di nuovo e dopo aver usato **Unisci** o **Annulla**. Svuota un campo per usare di nuovo il valore trovato. Se svuoti il nome, viene ripristinato quello presente nei suoi messaggi.

Per cambiare la foto, toccala: puoi **Carica un’immagine**, sceglierne una trovata per la persona oppure **Rimuovi foto**. La foto rimane sulla tua Machine.

## Unire due persone

Quando due schede potrebbero appartenere alla stessa persona, nella pagina ti viene chiesto se si tratta della stessa persona e nell’elenco Persone compaiono sotto **Stessa persona?**. **Unisci** le riunisce, conservando tutti i messaggi, le note, i ruoli e i progetti. **Non è la stessa** le mantiene separate in modo definitivo. La risposta resta visibile per un momento, poi la coppia scompare dall’elenco. L’elenco scompare quando non ci sono più persone da verificare.

Una persona con un indirizzo che assomiglia soltanto a uno che conosci, come acme-corp.example rispetto a acmecorp.example, non viene mai proposta come la stessa persona. Solo tu puoi assegnarle un ruolo.

Un nome da solo non basta mai per unire due persone con domini diversi, perché chiunque può inserirlo: due indirizzi di domini diversi vengono proposti solo se c’è un altro collegamento, come le stesse persone o un progetto. Non viene mai proposta una persona che usa il tuo nome con un indirizzo che non è tuo. Aggiungi invece gli altri tuoi indirizzi in **Impostazioni**, alla voce [I tuoi indirizzi](settings.md#your-addresses).

Se corrisponde solo il nome, come "Sam" e "Sam Lee", e i domini sono diversi, le persone vengono proposte solo se hanno lo stesso numero di telefono o profilo LinkedIn.

Se corrisponde solo il nome a una riunione creata da una chat, oppure l’indirizzo appartiene a una persona che già conoscevi e solo la persona nella chat dice che è suo, ti viene chiesto di confermare. The Machine non apre mai un link per verificarlo.

Un indirizzo condiviso, come info@ o quello di una mailing list, non viene mai associato alle persone che ci scrivono. Un contatto di lavoro esterno alla tua azienda e una chat personale che hanno in comune solo un nome non vengono uniti automaticamente: vengono mostrati come una domanda da verificare.

**Unisci tutti** unisce in una volta sola tutte le coppie nell’elenco, tranne quelle che hai contrassegnato con **Non è la stessa**. Tocca **Annulla** subito dopo per separarle di nuovo.

Per unire due persone manualmente, apri una delle due schede, poi tocca **⋯**, **Stessa persona di…** e scegli l’altra. Nella pagina della persona unita trovi i motivi sotto **Unita da**, con **Annulla** per separarle di nuovo.

## Eliminare definitivamente una persona

Nella sua pagina, apri il menu ⋯ e scegli **Elimina definitivamente…**, poi **Elimina**. La persona e tutte le informazioni che la tua Machine conosce su di lei vengono rimosse: la scheda, gli indirizzi, i dati trovati, i messaggi scambiati solo tra voi e le note che la riguardano.

Le attività che la riguardano rimangono, ma il suo nome viene rimosso. Non verrà aggiunta di nuovo, neanche tramite un’importazione o un’attività dei compleanni di Facebook con il suo nome o indirizzo. L’operazione non può essere annullata.

## Email respinta

Quando un’email inviata a una persona viene respinta, accanto al suo indirizzo compare **Respinta** con la data; se ha un altro indirizzo, questo viene mostrato per primo. Le nuove bozze non vengono mai inviate all’indirizzo respinto se ne è noto un altro. Se è l’unico, la schermata di invio ti avvisa, ma puoi comunque inviare l’email.

Un’email viene considerata respinta quando il server di posta segnala che l’indirizzo non esiste, oppure dopo 3 errori temporanei nell’arco di una settimana. L’avviso scompare quando la persona scrive di nuovo da quell’indirizzo o quando un’email inviata a quell’indirizzo viene recapitata.

## Titolo professionale e foto

Per le persone con un indirizzo aziendale vengono cercati il titolo professionale, la foto, il profilo LinkedIn e la città, come descritto in [Dati dell’organizzazione](organization-data.md). Su una Machine ospitata, la ricerca riceve solo il loro nome e il dominio aziendale. Per la foto, Gravatar riceve l’hash dell’indirizzo di lavoro, mai l’indirizzo stesso. Per disattivare la ricerca, vai in **Impostazioni**, nella sezione Sicurezza, e disattiva **Cerca i contatti di lavoro**.

Questa opzione disattiva anche la consultazione del sito web prima di una prima riunione e la ricerca sul web, se configurata (vedi [Preparazione alle riunioni](calendar.md#ready-for-your-meetings)).

Quando la ricerca trova queste informazioni, nella pagina compaiono anche la descrizione, da quando la persona ricopre il ruolo attuale e i due ruoli precedenti. Le preparazioni usano anche queste informazioni, ma la descrizione solo se la persona non ha una biografia propria.

Le tue connessioni si arricchiscono anche con le informazioni già disponibili: titolo, telefono e fuso orario da Slack; biografia e luogo da X; sommario e foto da LinkedIn; titoli professionali da Contatti Google e Salesflare; e la foto di un contatto da Salesflare, se è salvata lì. Passa il puntatore sulla riga sotto il nome per vedere da dove proviene l’informazione.

Outlook aggiunge le foto dei colleghi della tua organizzazione e dei tuoi contatti Outlook, oltre ai titoli professionali e alle aziende dei tuoi contatti ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Le foto di WhatsApp e Telegram vengono sincronizzate tramite la sincronizzazione di WhatsApp e la connessione alle chat di Telegram: fino a 50 al giorno per ciascuna app, solo per le persone già presenti nel tuo Graph. Non viene inviato loro nulla. Quando salvi un’importazione dei compleanni di Facebook, viene aggiunta la foto del profilo di una persona che non ne ha già una ([Routine](routines.md)). Tutto rimane sulla tua Machine.

Nel [Graph del team](team-graph.md) di una Fleet di lavoro, una piccola copia della foto professionale viene aggiunta alla scheda condivisa di una persona. Le foto da Contatti Google, WhatsApp, Telegram o Facebook, e quelle che hai modificato o rimosso, non vengono mai condivise.

## Su di te

I tuoi indirizzi e numeri, inclusi gli alias, appartengono sempre a te e non sono mai associati a una persona nel tuo Graph. Se cerchi te stesso o aggiungi una persona con uno dei tuoi indirizzi, si apre **Su di te**. Le importazioni ignorano la tua riga.

La sezione Su di te elenca i tuoi indirizzi e la relativa origine; puoi modificarli in **Impostazioni**, nella sezione Account. Per inviare i tuoi recapiti a un collega o a un amico, scegli **Condividi il mio contatto**. Vedi [Condividi un contatto](share-contact.md).

## Il suo ruolo per te

I ruoli che la tua Machine rileva nei tuoi messaggi compaiono nella sua pagina, sotto **Per te**, insieme alle parole che indicano il ruolo, come un titolo. Dire di essere il tuo commercialista o cliente non basta: serve anche un riscontro da parte tua, per esempio nei tuoi messaggi o nelle riunioni con quella persona. Non serve aspettare che tu confermi. Se un’informazione è sbagliata, correggila con **Modifica** nella sua pagina oppure con **⋯** sulla relativa riga in **Modifiche recenti**. La tua Machine impara dalle modifiche.

## Cosa sa di una persona

Le informazioni sulla persona si trovano nella sua pagina, sotto **Informazioni note**; in Apprendimento trovi quelle generali. Tocca **Aggiungi** per aggiungerne una con parole tue. Ogni informazione ha un menu:

- **Modifica** la modifica direttamente.
- **Non riguarda** la persona la trasforma di nuovo in un’informazione generale, in **Apprendimento**, sotto **Fatti**.
- **Rimuovi** la elimina ovunque.

## Modifiche recenti

La sezione **Modifiche recenti**, chiusa sopra la cronologia di una persona, organizzazione o progetto, elenca ciò che la tua Machine ha modificato o imparato: un ruolo, il luogo di lavoro di una persona, il legame tra due persone, un fatto o uno spostamento di progetto. Ogni riga mostra la data e la fonte. Tocca la fonte per leggere il messaggio.

Se un’informazione è sbagliata, tocca **⋯** sulla riga per correggerla direttamente: **Modifica**, **Rimuovi**, **Non riguarda** la persona oppure **Annulla** per ripristinare la posizione precedente di un progetto. Vengono mostrate tre righe; tocca **Mostra altro** per vedere le altre.

Nell’elenco Persone, accanto a chi è stato aggiornato oggi dalla tua Machine compare un puntino. In cima all’elenco trovi anche **4 persone aggiornate oggi**, con i loro nomi. Vedi [Il Graph](graph.md).

## Un’attività su una persona

Tocca **Nuova attività** nel menu **⋯** di una persona, un’organizzazione o un progetto per creare un’attività che la riguarda.
