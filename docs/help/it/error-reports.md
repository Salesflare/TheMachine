---
title: Segnalazioni di errore
area: security
summary: Quando qualcosa non funziona, la tua Machine comunica al team di The Machine cosa è successo e in quale punto del codice. Mai i tuoi messaggi, nomi o indirizzi.
covers: error-reports
code: error_feed.py, error_words.py, pacing.py, dashboard.html, sw.js
order: 4
translated: e1d4d602255cde39
---
## Cos’è

Quando qualcosa nella tua Machine non funziona, la tua Machine invia al nostro team una breve segnalazione anonima dell’errore, così possiamo correggerlo prima che qualcuno ce lo segnali. L’invio è attivo per impostazione predefinita e richiede [The Machine Network](/network).

## Cosa viene inviato

Solo queste informazioni, per ogni tipo di errore:

- il tipo di errore, per esempio `KeyError`;
- il messaggio, dopo aver rimosso ogni dettaglio specifico: numeri, ID, testo tra virgolette, indirizzi email, link, percorsi dei file, chiavi e qualsiasi parola che potrebbe essere un nome;
- il punto del codice di The Machine in cui si è verificato, mai una cartella sul tuo computer;
- la versione dell’app, quante volte si è verificato e quando è successo la prima e l’ultima volta.

Per esempio: `IndexError`, `list index out of range`, in `machine/faults.py:fault_event:246`, versione `05b17ee6ac79`, 1 volta.

## Cosa non viene mai inviato

Il contenuto dei tuoi messaggi, delle tue attività, delle tue bozze o delle tue chat. Nomi, indirizzi email, numeri di telefono, link o password. L’account o la persona a cui si riferiva.

## Da dove arrivano gli errori

- attività in background: controllo dei nuovi messaggi, preparazione delle attività, chat, Connessioni e sincronizzazioni;
- la dashboard, nel browser o nell’app, compresi gli errori mostrati;
- le richieste della dashboard che non riescono o scadono: quale richiesta, mai cosa ha inviato;
- i lavori dell’agente di coding che non riescono: solo lo strumento e il tipo di errore;
- il breve test della tua IA quando non riesce: l’errore dell’IA, dopo aver rimosso ogni dettaglio specifico.

Un controllo interrotto perché hai raggiunto il limite di utilizzo del tuo piano IA non è un errore e non viene inviato: resta in attesa del ripristino del limite.

Un connettore che hai aggiunto tu (un tuo file in `connectors/`) invia solo il nome del servizio e l’etichetta dell’errore, per esempio `notes` e `notes_http: HTTP unauthorized`, così possiamo aiutarti a correggerlo. Nient’altro del suo codice. La scheda della connessione mostra l’errore completo.

Gli errori ripetuti vengono conteggiati, non inviati di nuovo. Viene inviato al massimo un gruppo di segnalazioni ogni 10 minuti. Le conserviamo per 30 giorni.

## Gestione dei limiti

Le attività in background si fermano quando i limiti del tuo piano IA stanno per esaurirsi, così resta spazio per le tue chat (vedi [Il tuo modello IA](model.md)).

Se le segnalazioni di errore sono attive, la tua Machine ci comunica anche una volta al giorno quanto spesso succede: per ogni pausa, l’ora, il limite raggiunto, la durata e quanti lavori sono rimasti in attesa. Non invia informazioni su cosa stavano facendo i lavori.

## Disattivare le segnalazioni

In **Impostazioni**, vai su **Sicurezza** e disattiva **Invia segnalazioni di errore**. Da quel momento non viene registrato né inviato altro e le segnalazioni in attesa vengono eliminate. Gli errori restano visibili sulla tua Machine, che può proporti una soluzione.

Vedi [Sicurezza e privacy](security-and-privacy.md).
