---
title: Segnalazioni di errore
area: security
summary: Quando qualcosa si rompe, la tua Machine comunica al team di The Machine cosa non ha funzionato e dove nel codice. Mai i tuoi messaggi, nomi o indirizzi.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: fd3e1c2d68b93a35
---
## Cosa viene inviato

Quando qualcosa in The Machine si rompe, la tua Machine invia al nostro team una breve segnalazione anonima sull’errore, così possiamo risolverlo prima che qualcuno ce lo segnali. L’opzione è attiva per impostazione predefinita e richiede [The Machine Network](/network).

## Cosa viene inviato

Solo queste informazioni, per ogni tipo di errore:

- il tipo di errore, per esempio `KeyError`;
- il messaggio, dopo aver rimosso ogni dato specifico: numeri, ID, testo tra virgolette, indirizzi email, link, percorsi dei file, chiavi e qualsiasi parola che potrebbe essere un nome;
- il punto del codice di The Machine in cui si è verificato, mai una cartella sul tuo computer;
- la versione dell’app, quante volte si è verificato e quando è successo la prima e l’ultima volta.

Un esempio reale: `IndexError`, `list index out of range`, in `assistant.py:fault_event:7899`, versione `05b17ee6ac79`, 1 volta.

## Cosa non viene mai inviato

Il contenuto dei tuoi messaggi, delle tue attività, bozze o chat. Nomi, indirizzi email, numeri di telefono, link o password. L’account o la persona di cui si trattava.

## Da dove arrivano gli errori

- attività in background: controlli dei nuovi messaggi, preparazione delle attività, chat, connessioni e sincronizzazioni;
- la dashboard, nel browser o nell’app, compresi gli errori che ti mostra;
- richieste dalla dashboard che non vanno a buon fine o scadono: quale richiesta, mai cosa ha inviato;
- attività degli agenti di programmazione che non vanno a buon fine: solo lo strumento e il tipo di errore.

Gli errori ripetuti vengono conteggiati, non inviati di nuovo. Viene inviato al massimo un gruppo di segnalazioni ogni 10 minuti. Li conserviamo per 30 giorni.

## Gestione delle pause

Le attività in background si fermano quando i limiti del tuo piano AI stanno per esaurirsi, così resta spazio per le tue chat (vedi [Il tuo modello AI](model.md)).

Se le segnalazioni di errore sono attive, la tua Machine ci comunica anche una volta al giorno quanto spesso è successo: per ogni pausa, l’ora, quale limite, la durata e quanti job sono rimasti in attesa. Non ci dice di cosa si occupavano i job.

## Disattivare l’opzione

In **Impostazioni**, **Sicurezza**, disattiva **Invia segnalazioni di errore**. Non verrà più registrato né inviato nulla e i dati in attesa verranno eliminati. Gli errori continueranno a comparire sulla tua Machine, che può suggerirti una soluzione.

Vedi [Sicurezza e privacy](security-and-privacy.md).
