---
title: Persone
area: graph
summary: Tutte le persone con cui sei in contatto: la loro pagina, il riepilogo e la cronologia, e come aggiungere, modificare, unire o eliminare una persona.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 2fe1c104a74711c4
---
Tutte le persone con cui sei in contatto, dalle più vicine in poi, che compaiono nei tuoi messaggi e nelle tue riunioni. Newsletter, ricevute e altre email non aggiungono nessuno finché non rispondi. Le trovi sotto Mittenti nascosti, in fondo all’elenco: **Mostra come persona** aggiunge una persona. Campi, tag e importazione funzionano allo stesso modo in tutti e tre gli elenchi, ognuno con i propri filtri: vedi [The Graph](graph.md).

Una casella di posta condivisa (info@, assistenza clienti, il nome di un negozio) viene associata alla sua organizzazione, non a una persona, anche dopo che le hai scritto.

## La pagina di una persona

In alto trovi la foto, il nome, il titolo, l’organizzazione e il luogo, più una riga sul vostro rapporto ("Vi sentite ogni giorno · ultimo contatto ieri · prossima riunione mar 27 ott"). Il contatto più recente è indicato con formule come "proprio ora", "3 ore fa", "ieri" o "3 giorni fa"; per i contatti meno recenti viene mostrata una data. Passaci sopra con il cursore per vedere la data esatta. Più sotto trovi:

- **Contatto**: i numeri di telefono e gli indirizzi email. Tocca un numero o un indirizzo per chiamare o scrivere, oppure **Copia**. Qui trovi anche il **Compleanno**, con l’indicazione della fonte (Google Contacts, Google Calendar, Facebook o tu): vedi [The Graph](graph.md#birthday).
- **Con te**: il tipo di rapporto, Contatto di lavoro o Personale, e la tua Famiglia o Fleet, con **Vedi in Fleet**.
- **Anche su**: gli altri servizi in cui vi scrivete. **Slack** apre il profilo della persona in Slack o la chat più recente che avete su Slack.
- **Persone** e **Progetti** di cui fa parte, **In sospeso tra voi** (le promesse di entrambi, con **Segna come fatto** e **Lascia perdere**) e la sua **Cronologia**.

Gli indirizzi e le chat di una persona vengono associati automaticamente quando è chiaro che appartengono alla stessa persona, per esempio se un’email di lavoro include il suo indirizzo personale in CC.

Se la pagina mostra **Impossibile caricare la pagina.**, tocca **Riprova**. Se il messaggio continua a comparire, usa **Qualcosa non va?** in fondo alla pagina.

## Riepilogo

In cima alla pagina di una persona trovi alcune brevi righe su ciò che è stato deciso, chiesto, pianificato o promesso, con il nome di tutti i partecipanti. The Machine riscrive il riepilogo quando ci sono novità, solo per le persone con cui sei davvero in contatto, e verifica ogni riga. Di solito lo aggiorna una volta al giorno, ma entro poche ore se cambia qualcosa di importante, per esempio una nuova scadenza o una richiesta ritirata.

Le righe vaghe vengono escluse: se non c’è nulla di specifico da dire, il riepilogo non viene mostrato. Ogni riga rimanda alla fonte: i messaggi dello stesso giorno condividono una data e sono raggruppati. Tocca la data per aprirli.

Tocca **Modifica** per scrivere il riepilogo a modo tuo. Quando ci sono novità, The Machine mostra un **Aggiornamento suggerito** con le opzioni **Usalo** e **Tieni la mia**. **Lascia che lo scriva The Machine** rimette il riepilogo nelle sue mani.

La preparazione delle riunioni usa il riepilogo, ma solo le righe relative a quel lato dell’attività (Lavoro o Personale). Resta sulla tua Machine; il tuo team non la vede.

## Cronologia

Ogni pagina di una persona o di un’organizzazione ha una cronologia, dalla più recente alla meno recente: email, riunioni e relativi riepiloghi Zoom, conversazioni Intercom (con **Apri in Intercom**), chat WhatsApp, Telegram, Slack, LinkedIn e X, attività, promesse e modifiche ai progetti. I filtri in alto mostrano una fonte alla volta. **Mostra altro** carica gli elementi meno recenti.

Le riunioni future sono in cima, sotto **In arrivo**, dalla più vicina alla più lontana; **Mostra tutti i prossimi** mostra anche le altre. Una riunione indica chi vi ha partecipato, elencando ogni persona una sola volta. Se ha note o una trascrizione, trovi **Note** o **Trascrizione**: toccale per leggerle.

Le tue cronologie sono private: il Graph del team mostra solo ciò che consentono le tue regole di condivisione. In una pagina, **Team** sopra la Cronologia aggiunge i contenuti condivisi dai colleghi, indicando chi li ha condivisi; **Miei** mostra solo i tuoi.

## Lavoro e Personale

Le schede **Lavoro** e **Personale** mostrano le persone in base al loro Tipo, indicato nella pagina. La tua scelta (**Modifica**) ha la precedenza. In caso contrario, la tua Famiglia e i tuoi Amici, e i familiari o gli amici per cui sei una persona vicina (per esempio una moglie o un padre), sono considerati Personali, indipendentemente dall’indirizzo da cui scrivono. Il tuo team non vede i contatti Personali.

## Aggiungere una persona

Tocca **Nuova persona** in cima a Persone, oppure **+** nella barra in alto sul telefono. Inserisci un nome e, se li hai, un indirizzo email e un’organizzazione. Se nel tuo Graph c’è già una persona simile, il modulo te la mostra per prima, così puoi aprire quella pagina. Tocca **Aggiungi** per aprire la nuova pagina.

La persona che aggiungi resta nell’elenco anche se non ci sono ancora messaggi. Il primo messaggio verrà associato a lei.

## Modificare una persona

Tocca **Modifica** in cima alla pagina per cambiare il nome, il titolo, l’organizzazione, il luogo, LinkedIn, i numeri di telefono e gli indirizzi email, il tipo di rapporto e la categoria Lavoro o Personale. Il campo **Note** serve per annotare ciò che vuoi ricordare; le note restano anche dopo un’unione. Tocca **Salva** per confermare o **Annulla** per lasciare tutto com’era.

Le tue modifiche restano anche quando i dati vengono cercati di nuovo, e dopo aver usato **Unisci** o **Annulla**. Svuota un campo per usare di nuovo il valore trovato automaticamente. Se cancelli il nome, verrà ripristinato quello presente nei suoi messaggi.

Per cambiare la foto, toccala e scegli **Carica un’immagine**, una foto trovata per quella persona oppure **Rimuovi foto**. La foto resta sulla tua Machine.

## Unire due persone

Se due persone potrebbero essere la stessa, nella loro pagina ti viene chiesto se sono la stessa persona e in Persone compaiono sotto **Stessa persona?**. **Unisci** le combina, includendo tutti i messaggi, le note, i ruoli e i progetti. **Non è la stessa** le mantiene separate. La tua risposta viene mostrata per un momento sulla coppia, che poi scompare dall’elenco. L’elenco scompare quando non ci sono più coppie da valutare.

Un indirizzo condiviso, come info@ o una mailing list, non viene mai associato alle persone che lo usano. Un contatto di lavoro esterno alla tua azienda e una chat personale che hanno in comune solo il nome non vengono uniti automaticamente: vengono proposti come coppia da valutare.

**Unisci tutti** unisce in una volta tutte le coppie dell’elenco, tranne quelle che hai contrassegnato con **Non è la stessa**. Se tocchi subito **Annulla**, le separi di nuovo tutte.

Per unire due persone manualmente, apri la pagina di una di loro, poi tocca **⋯**, **Stessa persona di…** e scegli l’altra. Nella pagina della persona unita trovi il motivo sotto **Unita da**, con **Annulla** per separarle di nuovo.

## Eliminare una persona definitivamente

Nella sua pagina, apri il menu ⋯, scegli **Elimina definitivamente…** e poi **Elimina**. La persona e tutte le informazioni che la tua Machine conosce su di lei verranno eliminate: la scheda, gli indirizzi, i dati trovati, i messaggi scambiati solo tra voi e le note che la riguardano.

Le attività che la coinvolgono restano, ma il suo nome viene rimosso. Non verrà aggiunta di nuovo, nemmeno con un’importazione o un’attività dei compleanni di Facebook che riporta il suo nome o indirizzo. L’operazione non può essere annullata.

## Email respinte

Quando un’email inviata a una persona viene respinta, il suo indirizzo mostra la dicitura **Respinta** con la data, e un altro suo indirizzo viene messo in evidenza. Se si conosce un altro indirizzo, le nuove bozze non verranno mai inviate a quello respinto. Se è l’unico, la schermata di invio ti avvisa, ma puoi comunque inviare l’email.

Un indirizzo viene considerato respinto quando il server di posta dice che non esiste oppure dopo 3 errori temporanei nell’arco di una settimana. La segnalazione viene rimossa quando la persona scrive di nuovo da quell’indirizzo o quando un’email inviata a quell’indirizzo viene consegnata.

## Titolo professionale e foto

Alle persone con un indirizzo aziendale vengono aggiunti titolo professionale, foto, LinkedIn e città, cercati come descritto in [dati dell’organizzazione](organization-data.md). Su una Machine ospitata, la ricerca usa solo il loro nome e il dominio aziendale. Per le foto, Gravatar riceve un hash del loro indirizzo di lavoro, mai l’indirizzo stesso. Per disattivare questa funzione, vai su **Impostazioni**, nella sezione Sicurezza, e disattiva **Cerca i contatti di lavoro**.

Se la ricerca trova informazioni sulla persona, la pagina mostra anche la sua presentazione, da quando ricopre il ruolo attuale e i due ruoli precedenti. Le preparazioni le utilizzano a loro volta, ma mostrano la presentazione solo se la persona non ha una biografia propria.

Le tue Connessioni si arricchiscono anche con le informazioni già lette: titolo, telefono e fuso orario da Slack; biografia e luogo da X; presentazione e foto da LinkedIn; titoli professionali dai contatti Google e Salesflare; e la foto di un contatto da Salesflare, se Salesflare ne conserva una. Passa il cursore sulla riga sotto il nome per vedere da dove proviene l’informazione.

Outlook aggiunge le foto dei colleghi della tua organizzazione e dei tuoi contatti Outlook, oltre ai titoli professionali e alle aziende dei tuoi contatti ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Le foto di WhatsApp e Telegram arrivano dalla sincronizzazione di WhatsApp e dalla connessione alle tue chat Telegram: fino a 50 al giorno per ciascun servizio, solo per le persone già presenti nel tuo Graph. A loro non viene inviato nulla. Un’importazione dei compleanni di Facebook aggiunge la foto del profilo di una persona che non ne ha una quando la salvi ([Routine](routines.md)). Tutto resta sulla tua Machine.

Nel [Team Graph](team-graph.md) di una Fleet di lavoro, una piccola copia della foto professionale viene aggiunta alla scheda condivisa della persona. Le foto da Google Contacts, WhatsApp, Telegram o Facebook, così come quelle che hai modificato o rimosso, non vengono mai condivise.

## Informazioni su di te

I tuoi indirizzi e numeri, inclusi gli alias, appartengono sempre a te e non sono mai associati a una persona nel tuo Graph. Se cerchi te stesso o aggiungi una persona con uno dei tuoi indirizzi, si apre **Su di te**. Le importazioni ignorano la riga che ti riguarda.

La sezione Su di te elenca i tuoi indirizzi e indica la fonte di ciascuno; per modificarli, vai su **Impostazioni**, nella sezione Account. Per inviare il tuo contatto a un collega o a un amico, scegli **Condividi il mio contatto**. Vedi [Condividere un contatto](share-contact.md).

## Il tuo rapporto con loro

I ruoli che la tua Machine rileva nei tuoi messaggi compaiono nella pagina della persona, sotto **Per te**, insieme alla riga da cui sono stati ricavati. Non serve aspettare una tua conferma. Se un ruolo non è corretto, modificalo con **Modifica** nella pagina oppure con **⋯** sulla relativa riga in **Modifiche recenti**. La tua assistente impara dalle tue modifiche.

## Cosa sa di una persona

Le informazioni su una persona si trovano nella sua pagina, sotto **Informazioni note**; Apprendimento conserva quelle generali. Tocca **Aggiungi** per aggiungere un’informazione con parole tue. Ogni informazione ha un menu:

- **Modifica** la cambia direttamente.
- **Non riguarda** la persona la riporta tra le informazioni generali, sotto **Apprendimento**, **Fatti**.
- **Rimuovi** la elimina ovunque.

## Modifiche recenti

**Modifiche recenti**, nella sezione che puoi espandere appena sopra la cronologia di una persona, organizzazione o progetto, elenca ciò che la tua Machine ha modificato o appreso: un ruolo, il luogo di lavoro di una persona, il rapporto tra due persone, un fatto o un cambiamento di progetto. Ogni riga indica la data e la fonte; tocca la fonte per leggere il messaggio.

Se una riga non è corretta, usa **⋯** per modificarla direttamente: scegli **Modifica**, **Rimuovi**, **Non riguarda** la persona oppure **Annulla** per ripristinare la posizione precedente di un progetto. Vengono mostrate tre righe; tocca **Mostra altro** per vedere le altre.

Una persona aggiornata oggi dalla tua Machine è contrassegnata da un puntino nell’elenco Persone, e la dicitura **4 persone aggiornate oggi** in cima all’elenco ne mostra i nomi. Vedi [The Graph](graph.md).

## Un’attività su una persona

Tocca **Nuova attività** nel menu **⋯** di una persona, un’organizzazione o un progetto per creare un’attività che li riguarda.
