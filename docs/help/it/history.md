---
title: Cronologia
area: connections
summary: Circa un anno di vecchie email, riunioni e messaggi di WhatsApp, Slack e Teams, da cercare e leggere per conoscere le persone. Mai un’attività.
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
translated: 2b5e84c61892c8e4
---
## Cosa conserva

La tua Machine importa circa un anno di vecchie email, riunioni e messaggi di WhatsApp, Slack e Teams. Puoi trovarli con la ricerca, anche per significato, e nelle conversazioni. Il [Calendario](calendar.md) mostra le riunioni passate.

In **Connessioni** puoi vedere fino a che punto risale la cronologia di ogni connessione, per esempio **Cronologia: fino a** novembre 2025.

## Cosa aggiunge al tuo Graph

Il tuo [Graph](graph.md) ne tiene conto: quanto sei in contatto con le persone, quando avete parlato l’ultima volta, chi conosce chi e le persone e organizzazioni stesse. Anche la cronologia di una persona o di un’organizzazione lo mostra, così l’ultimo contatto è sempre visibile. Le risposte di Fleet di lavoro su «chi conosce qualcuno» usano questi dati degli account di lavoro, con le stesse [regole di condivisione](sharing-rules.md) delle nuove email.

## Cosa non fa mai

Non crea mai un’attività né una promessa, non conta mai come novità, non avvia mai un controllo e non aggiunge mai elementi a un progetto. La cronologia personale resta privata, come le email personali.

A parte la ricerca per significato, il tuo modello di IA la legge solo in tre casi:

- nei risultati di una ricerca, per esempio per rispondere a una tua domanda o gestire un’attività in corso
- nelle email con dettagli di prenotazione, per [viaggi ed eventi](calendar.md#trips-and-events)
- nel [briefing per le riunioni](calendar.md#ready-for-your-meetings): note delle riunioni precedenti e alcuni vecchi messaggi delle persone che incontrerai

## Quando viene eseguita

Inizia dopo la prima analisi dei tuoi messaggi e, per ogni connessione, solo dopo la prima settimana. Vale anche per le connessioni che aggiungi in seguito. Viene eseguita lentamente in background e si interrompe mentre è in corso un controllo o una sincronizzazione, se un servizio le chiede di rallentare o se la tua Machine ha poco spazio. I nuovi messaggi hanno sempre la precedenza.

Una volta importata la cronologia di una casella di posta, la tua Machine rilegge una volta le email che conserva per cercare dettagli di prenotazioni e biglietti, così anche le prenotazioni meno recenti compaiono in [viaggi ed eventi](calendar.md#trips-and-events). La lettura procede altrettanto lentamente e si interrompe per gli stessi motivi.

Usa gli accessi già concessi a ogni connessione. Non devi approvare nulla di nuovo.

## Quanto indietro risale

Circa un anno. Sul tuo computer puoi modificarlo nel file delle impostazioni con `history_days` (0 lo disattiva, fino a 730). Telegram e le altre fonti non importano la cronologia più vecchia.

I messaggi di LinkedIn e X risalgono a 90 giorni fa e vengono letti molto lentamente: poche richieste di lettura all’ora, solo di giorno. Se il sito limita l’accesso, la lettura si interrompe per un giorno, così il tuo account resta al sicuro (`social_history_days`, 0 la disattiva).
