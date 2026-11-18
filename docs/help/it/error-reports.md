---
title: Segnalazioni di errore
area: security
summary: Quando qualcosa si rompe, la tua Machine comunica al team di The Machine che cosa non ha funzionato e dove nel codice. Mai i tuoi messaggi, nomi o indirizzi.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: 2253a0d695fe898c
---
## Che cosa sono

Quando qualcosa nella tua Machine si rompe, la tua Machine invia al nostro team una breve segnalazione anonima sull’errore, così possiamo risolverlo prima che qualcuno ce lo segnali. È attiva per impostazione predefinita e richiede [The Machine Network](/network).

## Che cosa viene inviato

Solo queste informazioni, per ogni tipo di errore:

- il tipo di errore, per esempio `KeyError`;
- il messaggio, senza dettagli specifici: numeri, ID, testo tra virgolette, indirizzi email, link, percorsi dei file, chiavi e qualsiasi parola che potrebbe essere un nome;
- il punto del codice di The Machine in cui si è verificato, mai una cartella del tuo computer;
- la versione dell’app, quante volte si è verificato e quando è successo la prima e l’ultima volta.

Per esempio: `IndexError`, `list index out of range`, in `machine/faults.py:fault_event:246`, versione `05b17ee6ac79`, 1 volta.

## Che cosa non viene mai inviato

Il contenuto dei tuoi messaggi, delle tue attività, bozze o chat. Nomi, indirizzi email, numeri di telefono, link o password. Quale account o persona riguardava.

## Da dove vengono gli errori

- attività in background: controlli dei nuovi messaggi, preparazione delle attività, chat, connessioni e sincronizzazioni;
- la dashboard, nel browser o nell’app, compresi gli errori che ti mostra;
- richieste della dashboard che non vanno a buon fine o scadono: quale richiesta, mai che cosa ha inviato;
- attività dell’agente di programmazione non riuscite: solo lo strumento e il tipo di errore;
- il breve test della tua IA quando non va a buon fine: l’errore dell’IA, senza dettagli specifici.

Un connettore che hai aggiunto tu (il tuo file in `connectors/`) invia solo il nome del servizio e l’etichetta dell’errore, per esempio `notes` e `notes_http: HTTP unauthorized`, così possiamo aiutarti a risolverlo. Nient’altro del suo codice. La scheda della connessione mostra l’errore completo.

Gli errori ripetuti vengono conteggiati, non inviati di nuovo. Viene inviata al massimo una raccolta ogni 10 minuti. Li conserviamo per 30 giorni.

## Gestione dei limiti

Le attività in background vengono sospese quando i limiti del tuo piano IA stanno per esaurirsi, così resta spazio per le tue chat ([Il tuo modello IA](model.md)).

Con le segnalazioni di errore attive, la tua Machine ci comunica anche una volta al giorno quanto spesso succede: per ogni pausa, l’ora, il limite raggiunto, la durata e quante attività sono rimaste in attesa. Niente informazioni sul contenuto delle attività.

## Disattivarle

In **Impostazioni**, **Sicurezza**, disattiva **Invia segnalazioni di errore**. Non vengono registrati né inviati altri dati e ciò che era in attesa viene eliminato. Gli errori continuano a essere visibili sulla tua Machine, che può proporti una soluzione.

Vedi [Sicurezza e privacy](security-and-privacy.md).
