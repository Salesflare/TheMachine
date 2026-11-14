---
title: Segnalazioni di errore
area: security
summary: Quando qualcosa si rompe, la tua Machine comunica al team di The Machine cosa non ha funzionato e in quale punto del codice. Non invia mai i tuoi messaggi, nomi o indirizzi.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: 03a8649f2f634b59
---
## Cos'è

Quando qualcosa in The Machine si rompe, la tua Machine invia al nostro team una breve segnalazione anonima sull'errore, così possiamo risolverlo prima che qualcuno lo segnali. È attiva per impostazione predefinita e richiede [The Machine Network](/network).

## Cosa viene inviato

Solo queste informazioni, per ogni tipo di errore:

- il tipo di errore, ad esempio `KeyError`;
- il messaggio, dopo aver rimosso ogni dato specifico: numeri, ID, testo tra virgolette, indirizzi email, link, percorsi dei file, chiavi e qualsiasi parola che potrebbe essere un nome;
- il punto del codice di The Machine in cui si è verificato, mai una cartella sul tuo computer;
- la versione dell'app, quante volte si è verificato e quando è successo la prima e l'ultima volta.

Ad esempio: `IndexError`, `list index out of range`, in `machine/faults.py:fault_event:246`, versione `05b17ee6ac79`, 1 volta.

## Cosa non viene mai inviato

Il contenuto dei tuoi messaggi, delle attività, delle bozze o delle chat. Nomi, indirizzi email, numeri di telefono, link o password. A quale account o persona si riferiva.

## Da dove arrivano gli errori

- attività in background: controllo dei nuovi messaggi, preparazione delle attività, chat, Connessioni e sincronizzazioni;
- la dashboard, nel browser o nell'app, inclusi gli errori che ti ha mostrato;
- richieste dalla dashboard non riuscite o scadute: quale richiesta, mai il contenuto inviato;
- attività degli agenti di programmazione non riuscite: solo lo strumento e il tipo di errore.

Le ripetizioni dello stesso errore vengono conteggiate, ma non inviate di nuovo. Viene inviata al massimo una raccolta ogni 10 minuti. Conserviamo le segnalazioni per 30 giorni.

## Intervalli

Il lavoro in background si mette in pausa quando i limiti del tuo piano AI stanno per esaurirsi, per lasciare spazio alle tue chat (vedi [Il tuo modello AI](model.md)).

Con le segnalazioni di errore attive, la tua Machine ci comunica una volta al giorno quanto spesso è successo: per ogni pausa, l'ora, il limite, la durata e quante attività sono rimaste in attesa. Non comunica di quali attività si trattava.

## Disattivare le segnalazioni

In **Impostazioni**, **Sicurezza**, disattiva **Invia segnalazioni di errore**. Non viene registrato né inviato altro e le segnalazioni in attesa vengono eliminate. Gli errori continuano a essere visibili sulla tua Machine, che può proporti una soluzione.

Vedi [Sicurezza e privacy](security-and-privacy.md).
