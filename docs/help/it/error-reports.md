---
title: Segnalazioni di errore
area: security
summary: Quando qualcosa smette di funzionare, la tua Machine comunica al team di The Machine cosa non ha funzionato e dove nel codice. Mai i tuoi messaggi, nomi o indirizzi.
covers: error-reports
code: error_feed.py, error_words.py, pacing.py, dashboard.html, sw.js
order: 4
translated: d474cfa6bcefd25a
---
## Che cosa sono

Quando qualcosa nella tua Machine smette di funzionare, la tua Machine invia al nostro team una breve segnalazione anonima sull’errore, così possiamo risolverlo prima che qualcuno lo segnali. L’invio è attivo per impostazione predefinita e richiede [The Machine Network](/network).

## Che cosa viene inviato

Solo questi dati, per ogni tipo di errore:

- il tipo di errore, per esempio `KeyError`;
- il messaggio, dopo aver rimosso ogni dato specifico: numeri, ID, testo tra virgolette, indirizzi email, link, percorsi dei file, chiavi e qualsiasi parola che potrebbe essere un nome;
- il punto del codice di The Machine in cui si è verificato, mai una cartella del tuo computer;
- la versione dell’app, quante volte si è verificato e quando è successo la prima e l’ultima volta.

Per esempio: `IndexError`, `list index out of range`, in `machine/faults.py:fault_event:246`, versione `05b17ee6ac79`, 1 volta.

## Che cosa non viene mai inviato

Il contenuto dei tuoi messaggi, delle attività, delle bozze o delle chat. Nomi, indirizzi email, numeri di telefono, link o password. L’account o la persona a cui si riferiva.

## Da dove arrivano gli errori

- attività in background: controlli dei nuovi messaggi, preparazione delle attività, chat, Connessioni e sincronizzazioni;
- la dashboard, nel browser o nell’app, compresi gli errori che ti mostra;
- richieste della dashboard non riuscite o scadute: quale richiesta, mai i dati inviati;
- attività dell’agente di programmazione non riuscite: solo lo strumento e il tipo di errore;
- il breve test della tua IA quando non riesce: l’errore della IA, dopo aver rimosso ogni dato specifico.

Un controllo interrotto perché hai raggiunto il limite di utilizzo del tuo piano IA non è un errore e non viene inviato: resta in attesa fino al ripristino del limite. Lo stesso vale se non riesce perché la tua IA non ha effettuato l’accesso: **Serve il tuo intervento** ti chiede di accedere di nuovo.

Un connettore che hai aggiunto tu, cioè un tuo file in `connectors/`, invia solo il nome del servizio e l’etichetta dell’errore, per esempio `notes` e `notes_http: HTTP unauthorized`, così possiamo aiutarti a risolverlo. Non invia altro dal suo codice. La scheda della connessione mostra l’errore completo.

Gli errori ripetuti vengono conteggiati, non inviati di nuovo. Viene inviata al massimo una serie di segnalazioni ogni 10 minuti. Le conserviamo per 30 giorni.

## Gestione dei limiti

Le attività in background vengono messe in pausa quando i limiti del tuo piano IA stanno per esaurirsi, per lasciare spazio alle tue chat (vedi [Il tuo modello di IA](model.md)).

Se le segnalazioni di errore sono attive, la tua Machine ci comunica anche una volta al giorno quanto spesso succede: per ogni pausa, l’ora, il limite raggiunto, la durata e il numero di attività in attesa. Non comunica nulla sul contenuto delle attività.

## Disattivare

In **Impostazioni**, **Sicurezza**, disattiva **Invia segnalazioni di errore**. Non viene registrato né inviato altro e le segnalazioni in attesa vengono eliminate. Gli errori continuano a essere visibili sulla tua Machine, che può proporti una soluzione.

Vedi [Sicurezza e privacy](security-and-privacy.md).
