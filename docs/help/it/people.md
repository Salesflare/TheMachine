---
title: Persone
area: graph
summary: Tutte le persone con cui sei in contatto: la loro pagina, il riepilogo e la cronologia, e come aggiungere, modificare, unire o eliminare una persona.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 0eb2dcc70fba84c2
---
Tutte le persone con cui sei in contatto, dalle più vicine in poi, in base ai messaggi e alle riunioni. Newsletter, ricevute e altri invii non aggiungono nessuno finché non rispondi. Li trovi in Mittenti nascosti, sotto l’elenco: **Mostra come persona** aggiunge una persona. Campi, tag e importazioni funzionano allo stesso modo in tutti e tre gli elenchi, ma ognuno ha i propri filtri: vedi [The Graph](graph.md).

Una casella condivisa (info@, assistenza clienti, il nome di un negozio) è associata alla sua organizzazione, non a una persona, anche se le scrivi.

## La pagina di una persona

Inizia con la foto, il nome, il ruolo, l’organizzazione e il luogo della persona, poi una riga che spiega come siete in contatto ("Parlate ogni giorno · ultimo contatto ieri · prossima riunione mar 27 ott"). Il contatto recente è indicato con formule come "proprio ora", "3 ore fa", "ieri" o "3 giorni fa"; per i contatti meno recenti viene mostrata una data. Passaci sopra con il puntatore per vedere la data esatta. Sotto trovi:

- **Contatto**: i numeri di telefono e gli indirizzi email della persona. Tocca un numero per chiamare o un indirizzo per scrivere, oppure **Copia**. Qui trovi anche il **Compleanno** e la fonte (Google Contacts, Google Calendar, Facebook, le tue note o tu): vedi [The Graph](graph.md#birthday).
- **Con te**: il ruolo che ha per te, se è un contatto di Lavoro o Personale, e se fa parte della tua famiglia o del tuo Fleet, con **Vedi in Fleet**.
- **Anche su**: gli altri luoghi in cui parli con questa persona. **Slack** la apre su Slack oppure mostra la conversazione più recente che avete avuto lì.
- **Persone** e **Progetti** a cui partecipa, **In sospeso tra voi** (le promesse di entrambi, con **Segna come fatto** e **Lascia perdere**) e la sua **Cronologia**.

Gli indirizzi e le chat di una persona vengono collegati automaticamente quando è chiaro che appartengono alla stessa persona, per esempio quando un’email di lavoro è in copia conoscenza con il suo indirizzo personale.

Se una pagina mostra **Impossibile caricare questa pagina.**, tocca **Riprova**. Se il messaggio continua a comparire, usa **Qualcosa non va?** in fondo alla pagina.

## Riepilogo

In cima alla pagina di una persona trovi alcune brevi righe su decisioni, richieste, piani o promesse, con i nomi di tutte le persone coinvolte. The Machine le riscrive quando ci sono novità, solo per le persone con cui sei davvero in contatto, e controlla ogni riga prima di mostrarla. Di solito una volta al giorno; entro poche ore se cambia qualcosa che le riguarda, per esempio una nuova scadenza o una richiesta ritirata.

Le informazioni vaghe vengono escluse. Se non c’è nulla di specifico da dire, il riepilogo non viene mostrato. Ogni riga rimanda alla fonte: i messaggi dello stesso giorno sono raggruppati sotto un’unica data con il loro numero, e si aprono insieme.

Usa **Modifica** per riscriverlo a modo tuo. Quando ci sono novità, The Machine mostra un **Aggiornamento suggerito** con le opzioni **Usalo** e **Tieni la mia**. **Lascia che lo scriva The Machine** le restituisce il riepilogo.

La preparazione delle riunioni usa il riepilogo, ma solo le righe relative a quel tipo di attività (Lavoro o Personale). Resta sulla tua Machine e il tuo team non la vede.

## Cronologia

Ogni pagina di una persona o organizzazione ha una cronologia, dalla più recente in poi: email, riunioni e relativi riepiloghi Zoom, conversazioni Intercom (con **Apri in Intercom**), chat di WhatsApp, Telegram, Slack, LinkedIn e X, attività, promesse e cambiamenti di progetto. I filtri in alto mostrano una fonte alla volta. **Mostra altro** carica gli elementi meno recenti.

Le riunioni future sono in cima, sotto **In arrivo**, dalla più vicina in poi; **Mostra tutti i prossimi** mostra le altre. Per ogni riunione vengono indicate le persone che vi hanno partecipato, una sola volta ciascuna. Se ci sono note o una trascrizione, viene mostrato **Note** o **Trascrizione**: fai clic per leggerle.

Le tue cronologie sono solo tue: il Graph del team mostra solo ciò che consentono le tue regole di condivisione. In una pagina, **Team** sopra la Cronologia aggiunge ciò che hanno condiviso i colleghi e indica chi ha condiviso ogni elemento; **Miei** mostra solo i tuoi.

## Lavoro e Personale

Le schede **Lavoro** e **Personale** elencano le persone in base al loro tipo, indicato nella pagina. La scelta che fai tu (**Modifica**) ha la priorità. Altrimenti, i tuoi familiari e amici, e i familiari o gli amici per te (una moglie, un padre), sono considerati Personali, a prescindere dall’indirizzo da cui scrivono. Il tuo team non vede i contatti Personali.

## Aggiungere una persona

Usa **Nuova persona** in cima a Persone, oppure **+** nella barra superiore sul telefono. Inserisci un nome e, se li hai, un indirizzo email e un’organizzazione. Se nel tuo Graph c’è già una persona simile, il modulo la mostra per prima, così puoi aprire quella pagina. **Aggiungi** apre la nuova pagina.

La persona che aggiungi resta nell’elenco anche se non ci sono ancora messaggi. Il suo primo messaggio verrà associato al suo profilo.

## Modificare una persona

**Modifica**, in cima alla pagina, permette di cambiare nome, ruolo, organizzazione, luogo, profilo LinkedIn, numeri di telefono e indirizzi email, il suo ruolo per te e se è una persona di Lavoro o Personale. Il campo **Note** serve per annotare ciò che vuoi ricordare; le note restano anche dopo un’unione. **Salva** conserva le modifiche, mentre **Annulla** lascia tutto com’era.

Le modifiche restano anche quando i dati della persona vengono cercati di nuovo, e dopo **Unisci** e **Annulla**. Svuota un campo per usare di nuovo il valore trovato. Se svuoti il nome, viene ripristinato quello usato nei suoi messaggi.

Per cambiare la foto, fai clic su di essa: scegli **Carica un’immagine**, una foto trovata per quella persona oppure **Rimuovi foto**. La foto resta sulla tua Machine.

## Unire due persone

Se due profili potrebbero appartenere alla stessa persona, nella pagina compare la domanda e Persone li mostra sotto **Stessa persona?**. **Unisci** li fonde, includendo tutti i messaggi, le note, i ruoli e i progetti. **Non è la stessa** li mantiene separati. La tua risposta appare per un po’ sulla coppia, poi la coppia scompare dall’elenco. L’elenco scompare quando non ci sono più domande.

Una persona con un indirizzo che assomiglia soltanto a uno che conosci, per esempio acme-corp.example e acmecorp.example, non viene mai proposta come la stessa persona. Solo tu puoi assegnarle un ruolo.

Un nome da solo non basta mai per collegare due persone con domini diversi, perché chiunque può scrivere un nome: due indirizzi con domini diversi vengono proposti solo se c’è un altro collegamento, come le stesse persone o un progetto. Una persona che usa il tuo nome a un indirizzo che non è tuo non viene mai proposta. Aggiungi invece gli altri tuoi indirizzi in Impostazioni, [I tuoi indirizzi](settings.md#your-addresses).

Se corrisponde solo il nome di battesimo, ma i domini sono diversi, per esempio "Sam" e "Sam Lee", le persone vengono proposte solo se hanno lo stesso numero di telefono o profilo LinkedIn.

Un indirizzo condiviso, come info@ o una mailing list, non viene mai associato alle persone che lo usano per scrivere. Un contatto di lavoro esterno alla tua azienda e una chat personale che hanno in comune solo un nome non vengono uniti automaticamente: vengono mostrati come una domanda.

**Unisci tutti** unisce in una volta tutte le coppie nell’elenco, tranne quelle che hai contrassegnato con **Non è la stessa**. **Annulla** subito dopo le separa di nuovo tutte.

Per unire due persone manualmente, apri una delle loro pagine, poi **⋯**, **Stessa persona di…** e scegli l’altra persona. Nella pagina del profilo unito, la sezione **Unito da** spiega il motivo e offre l’opzione **Annulla** per separare di nuovo i profili.

## Eliminare definitivamente una persona

Nella sua pagina, apri il menu ⋯ e scegli **Elimina definitivamente…**, poi **Elimina**. La persona viene rimossa insieme a ciò che la tua Machine sa di lei: il suo profilo, gli indirizzi, i dettagli trovati, i messaggi scambiati solo tra voi e le note che la riguardano.

Le attività che la riguardano restano, ma senza il suo nome. Non verrà aggiunta di nuovo, nemmeno con un’importazione o un’attività dei compleanni di Facebook che riporti il suo nome o indirizzo. L’operazione non si può annullare.

## Email respinta

Quando un’email inviata a una persona viene respinta, accanto al suo indirizzo compare **Respinta** con la data, e viene mostrato per primo un suo altro indirizzo. Le nuove bozze non vengono mai inviate a quell’indirizzo se ne è noto un altro. Se è l’unico indirizzo, la schermata di invio ti avvisa, ma puoi comunque inviare l’email.

Un’email si considera respinta quando il server di posta segnala che l’indirizzo non esiste oppure dopo 3 errori temporanei nell’arco di una settimana. L’indicazione viene rimossa quando la persona scrive di nuovo da quell’indirizzo o quando un’email inviata lì viene consegnata.

## Ruolo e foto

Le persone con un indirizzo aziendale ricevono un ruolo, una foto, un profilo LinkedIn e una città, cercati come i [dati dell’organizzazione](organization-data.md). Su una Machine ospitata, la ricerca usa solo il nome e il dominio aziendale. Per la foto, Gravatar riceve l’hash dell’indirizzo di lavoro, mai l’indirizzo stesso. Puoi disattivare questa funzione in **Impostazioni**, nella sezione Sicurezza: **Cerca i contatti di lavoro**.

Quando trova queste informazioni, la pagina mostra anche il testo della sezione Informazioni, da quanto tempo la persona ricopre il ruolo attuale e i due ruoli precedenti. Anche la preparazione delle riunioni le legge, ma usa il testo della sezione Informazioni solo se la persona non ha una propria biografia.

Le tue connessioni completano i profili con le informazioni che hanno già letto: un ruolo, un numero di telefono e il fuso orario da Slack, una biografia e un luogo da X, un titolo e una foto da LinkedIn, i ruoli dai contatti Google e Salesflare e la foto di un contatto da Salesflare, se la conserva. Passa il puntatore sulla riga sotto il nome per vedere da dove proviene l’informazione.

Outlook aggiunge le foto dei colleghi della tua organizzazione e dei tuoi contatti Outlook, oltre ai ruoli e alle aziende dei tuoi contatti ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Le foto di WhatsApp e Telegram arrivano dalla sincronizzazione di WhatsApp e dalla connessione alle chat di Telegram: fino a 50 al giorno per ciascun servizio, solo per le persone già presenti nel tuo Graph. Non viene inviato loro nulla. L’importazione dei compleanni di Facebook aggiunge la foto del profilo di una persona che non ne ha una quando la salvi ([Routine](routines.md)). Tutto resta sulla tua Machine.

Nel [Graph del team](team-graph.md) di un Fleet di Lavoro, una copia ridotta della foto di lavoro viene inclusa nel profilo condiviso della persona. Le foto da Google Contacts, WhatsApp, Telegram o Facebook, così come quelle che hai modificato o rimosso, non vengono mai condivise.

## Su di te

I tuoi indirizzi e numeri, compresi gli alias, sono sempre tuoi e non vengono mai considerati come un’altra persona nel tuo Graph. Se cerchi te stesso o aggiungi una persona con uno dei tuoi indirizzi, si apre **Su di te**; durante un’importazione la tua riga viene ignorata.

La sezione Su di te mostra i tuoi indirizzi e la relativa fonte. Per modificarli, vai in **Impostazioni**, nella sezione Account. Per inviare i tuoi recapiti a un collega o a un amico, scegli **Condividi il mio contatto**. Vedi [Condividere un contatto](share-contact.md).

## Il suo ruolo per te

I ruoli che la tua Machine individua nei messaggi compaiono nella pagina della persona, sotto **Per te**, insieme alla frase da cui sono stati dedotti. Non devi aspettare che ti venga chiesto. C’è un errore? **Modifica** nella pagina della persona lo corregge, oppure puoi usare **⋯** sulla relativa riga in **Modifiche recenti**. La tua Machine impara dalle modifiche.

## Cosa sa di una persona

Le informazioni su una persona si trovano nella sua pagina, sotto **Informazioni note**; Apprendimento raccoglie quelle generali. Usa **Aggiungi** per aggiungerne un’altra con parole tue. Ogni informazione ha un menu:

- **Modifica** la cambia direttamente lì.
- **Non riguarda** quella persona: l’informazione torna a essere generale e passa sotto **Apprendimento**, **Fatti**.
- **Rimuovi** la elimina ovunque.

## Modifiche recenti

**Modifiche recenti**, nella sezione espandibile appena sopra la cronologia di una persona, organizzazione o progetto, mostra ciò che la tua Machine ha modificato o appreso: un ruolo, il luogo di lavoro, il rapporto tra due persone, un fatto o un cambiamento di progetto. Ogni riga mostra la data e la fonte; tocca la fonte per leggere il messaggio.

Se una riga è sbagliata, il menu **⋯** permette di correggerla direttamente: **Modifica**, **Rimuovi**, **Non riguarda** quella persona oppure **Annulla** per riportare un progetto alla posizione precedente. Vengono mostrate tre righe; **Mostra altro** mostra le altre.

Una persona aggiornata oggi dalla tua Machine è contrassegnata da un puntino nell’elenco Persone; in cima all’elenco, **4 persone aggiornate oggi** indica quali sono. Vedi [The Graph](graph.md).

## Un’attività su una persona

**Nuova attività** nel menu **⋯** di una persona, organizzazione o progetto crea un’attività che la riguarda.
