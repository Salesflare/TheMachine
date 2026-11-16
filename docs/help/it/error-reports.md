---
title: Segnalazioni di errore
area: security
summary: Quando qualcosa si rompe, la tua Machine comunica al team di The Machine cosa non ha funzionato e in quale punto del codice. Mai i tuoi messaggi, nomi o indirizzi.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: 4dc53a854d15f1a3
---
## Che cosa sono

Quando qualcosa in The Machine si rompe, la tua Machine invia al nostro team una breve nota anonima sull’errore, così possiamo risolverlo prima che qualcuno ce lo segnali. La funzione è attiva per impostazione predefinita e richiede [The Machine Network](/network).

## Quali dati vengono inviati

Solo questi, per ogni tipo di errore:

- il tipo di errore, ad esempio `KeyError`;
- il messaggio, dopo aver rimosso ogni dettaglio specifico: numeri, ID, testo tra virgolette, indirizzi email, link, percorsi dei file, chiavi e qualsiasi parola che potrebbe essere un nome;
- il punto del codice di The Machine in cui si è verificato, mai una cartella sul tuo computer;
- la versione dell’app, quante volte è successo e quando è successo la prima e l’ultima volta.

Ad esempio: `IndexError`, `list index out of range`, alle `machine/faults.py:fault_event:246`, versione `05b17ee6ac79`, 1 volta.

## Cosa non viene mai inviato

Il contenuto dei tuoi messaggi, delle attività, delle bozze o delle chat. Nomi, indirizzi email, numeri di telefono, link o password. L’account o la persona a cui si riferiva.

## Da dove arrivano gli errori

- attività in background: controlli dei nuovi messaggi, preparazione delle attività, chat, Connessioni e sincronizzazioni;
- la dashboard, nel browser o nell’app, inclusi gli errori che ti mostra;
- richieste dalla dashboard che non vanno a buon fine o scadono: quale richiesta, mai cosa ha inviato;
- attività degli agenti di programmazione che non vanno a buon fine: solo lo strumento e il tipo di errore;
- il breve test della tua IA quando non va a buon fine: l’errore dell’IA, dopo aver rimosso ogni dettaglio specifico.

Gli errori ripetuti vengono conteggiati, ma non inviati di nuovo. Al massimo viene inviato un gruppo di segnalazioni ogni 10 minuti. Le conserviamo per 30 giorni.

## Frequenza

Il lavoro in background si mette in pausa quando i limiti del tuo piano IA si avvicinano, per lasciare spazio alle tue chat (vedi [Il tuo modello IA](model.md)).

Con le segnalazioni di errore attive, la tua Machine ci comunica anche una volta al giorno quanto spesso è successo: per ogni pausa, l’ora, il limite raggiunto, la durata e quanti processi erano in attesa. Non comunica cosa riguardava il lavoro in attesa.

## Disattivare le segnalazioni

In **Impostazioni**, **Sicurezza**, disattiva **Invia segnalazioni di errore**. Non viene registrato né inviato altro e i dati in attesa vengono eliminati. Gli errori continuano a essere visibili sulla tua Machine, che può proporti una soluzione.

Vedi [Sicurezza e privacy](security-and-privacy.md).
