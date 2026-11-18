---
title: Segnalazioni di errore
area: security
summary: Quando si verifica un errore, la tua Machine comunica al team di The Machine cosa non ha funzionato e in quale punto del codice. Mai i tuoi messaggi, nomi o indirizzi.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: f67d18a44999cfce
---
## Che cos'è

Quando qualcosa non funziona nella tua Machine, la tua Machine invia al nostro team una breve nota anonima sull'errore, così possiamo risolverlo prima che qualcuno ce lo segnali. La funzione è attiva per impostazione predefinita e richiede [The Machine Network](/network).

## Cosa viene inviato

Solo queste informazioni, per ogni tipo di errore:

- il tipo di errore, ad esempio `KeyError`;
- il messaggio, dopo aver rimosso tutti i dettagli specifici: numeri, ID, testo tra virgolette, indirizzi email, link, percorsi dei file, chiavi e qualsiasi parola che potrebbe essere un nome;
- il punto del codice della Machine in cui si è verificato, mai una cartella del tuo computer;
- la versione dell'app, quante volte si è verificato e la prima e l'ultima volta.

Ad esempio: `IndexError`, `list index out of range`, in `machine/faults.py:fault_event:246`, versione `05b17ee6ac79`, 1 volta.

## Cosa non viene mai inviato

Il contenuto dei tuoi messaggi, delle attività, delle bozze o delle chat. Nomi, indirizzi email, numeri di telefono, link o password. L'account o la persona a cui si riferiva.

## Da dove arrivano gli errori

- attività in background: controlli dei nuovi messaggi, preparazione delle attività, chat, connessioni e sincronizzazioni;
- la dashboard, nel browser o nell'app, inclusi gli errori che ti mostra;
- richieste della dashboard non riuscite o scadute: quale richiesta, mai cosa ha inviato;
- processi degli agenti di programmazione non riusciti: solo lo strumento e il tipo di errore;
- il breve test della tua AI quando non va a buon fine: l'errore dell'AI, senza dettagli specifici.

Un connettore che hai aggiunto tu (un tuo file in `connectors/`) non invia mai i suoi errori. Li trovi nella scheda della connessione.

Gli errori ripetuti vengono conteggiati, ma non inviati di nuovo. Viene inviato al massimo un gruppo di segnalazioni ogni 10 minuti. Li conserviamo per 30 giorni.

## Limiti di invio

Le attività in background vengono messe in pausa quando i limiti del tuo piano AI stanno per esaurirsi, per lasciare spazio alle tue chat (vedi [Il tuo modello AI](model.md)).

Con le segnalazioni di errore attive, la tua Machine ci comunica anche una volta al giorno quante volte è successo: per ogni pausa, l'ora, quale limite, la durata e quanti processi sono rimasti in attesa. Non indica di quali processi si trattava.

## Disattivare

In **Impostazioni**, **Sicurezza**, disattiva **Invia segnalazioni di errore**. Non verrà registrato né inviato altro e i dati in attesa verranno eliminati. Gli errori continueranno a essere visibili sulla tua Machine, che può suggerirti una soluzione.

Vedi [Sicurezza e privacy](security-and-privacy.md).
