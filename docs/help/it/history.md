---
title: Cronologia
area: connections
summary: Circa un anno di vecchie email, riunioni e messaggi di WhatsApp, Slack e Teams da cercare e leggere, per conoscere meglio le persone. Non crea mai attività.
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
translated: c10fe5fb8d7b2d8b
---
## Cosa conserva

La tua Machine importa circa un anno di vecchie email, riunioni e messaggi di WhatsApp, Slack e Teams. Puoi trovarli con la ricerca, anche per significato. Le conversazioni li mostrano e il [Calendario](calendar.md) mostra le riunioni passate.

In **Connessioni**, ogni connessione indica fino a che data arriva, per esempio **Cronologia: fino a** novembre 2025.

## Cosa aggiunge al tuo Graph

Il tuo [Graph](graph.md) usa questi dati per calcolare quanto sei in contatto con le persone, quando avete parlato l'ultima volta e chi conosce chi, oltre a raccogliere informazioni sulle persone e sulle organizzazioni. Anche la cronologia di una persona o di un'organizzazione li mostra, così l'ultimo contatto è sempre visibile. Le risposte di Fleet a «chi conosce qualcuno» usano questi dati dagli account di lavoro, seguendo le stesse [regole di condivisione](sharing-rules.md) delle nuove email.

## Cosa non fa mai

Non crea mai un'attività o una promessa, non considera mai questi dati come nuovi, non avvia mai un controllo e non li aggiunge mai a un progetto. La cronologia personale resta privata, come le email personali. A parte la ricerca per significato, nessun modello di AI la legge.

## Quando viene eseguita

Inizia dopo il primo controllo dei messaggi e, per ogni connessione, solo dopo aver completato la prima settimana. Lo stesso vale per le connessioni aggiunte in seguito. Funziona lentamente in background e si mette in pausa mentre è in corso un controllo o una sincronizzazione, quando un servizio chiede di rallentare o quando la tua Machine ha poco spazio. I nuovi messaggi hanno sempre la precedenza.

Quando la cronologia di una casella di posta è stata importata, la tua Machine rilegge una volta le email conservate per cercare dettagli di prenotazioni e biglietti. In questo modo, anche le prenotazioni più vecchie compaiono in [Viaggi ed eventi](notes.md). La lettura procede altrettanto lentamente e si mette in pausa per gli stessi motivi.

Usa gli accessi già concessi a ogni connessione. Non devi approvare nulla di nuovo.

## Fino a che data

Circa un anno. Sul tuo computer, puoi modificare questo periodo con `history_days` nel file delle impostazioni (0 lo disattiva, il massimo è 730). Telegram e le altre fonti non importano la cronologia più vecchia.

I messaggi di LinkedIn e X risalgono a 90 giorni fa. La lettura è molto lenta: poche letture brevi all'ora, solo di giorno. Se il sito oppone resistenza, la lettura si interrompe per un giorno, così il tuo account resta al sicuro (`social_history_days`, 0 lo disattiva).
