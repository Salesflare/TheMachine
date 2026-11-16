---
title: Cronologia
area: connections
summary: Circa un anno di email, riunioni e messaggi meno recenti di WhatsApp, Slack e Teams, da cercare, leggere e usare per conoscere meglio le persone. Mai un’attività.
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
translated: 93575cd78b3085f7
---
## Cosa conserva

La tua Machine importa circa un anno di email, riunioni e messaggi meno recenti di WhatsApp, Slack e Teams. Puoi trovarli con la ricerca, anche per significato, visualizzarli nelle conversazioni e vedere le riunioni passate nel [Calendario](calendar.md).

In **Connessioni**, ogni connessione indica fino a che data risale la cronologia, per esempio **Cronologia: fino a** novembre 2025.

## Cosa aggiunge al tuo Graph

Il tuo [Graph](graph.md) ne tiene conto: quanto sei in contatto con le persone, quando ci hai parlato l’ultima volta, chi conosce chi e le persone e le organizzazioni stesse. Anche la timeline di una persona o di un’organizzazione la mostra, così l’ultimo contatto è sempre visibile. Le risposte di Fleet a domande come «chi conosce qualcuno» usano la cronologia degli account di lavoro, secondo le stesse [regole di condivisione](sharing-rules.md) delle nuove email.

## Cosa non fa mai

Non crea mai un’attività né una promessa, non conta mai come contenuto nuovo, non avvia mai un controllo e non aggiunge mai nulla a un progetto. La cronologia personale resta privata, come le email personali. Al di fuori della ricerca per significato, nessun modello di IA la legge.

## Quando viene importata

L’importazione inizia dopo il primo controllo dei messaggi e, per ogni connessione, solo quando è trascorsa la prima settimana. Vale anche per le connessioni che aggiungi in seguito. Avviene lentamente in background e si interrompe mentre è in corso un controllo o una sincronizzazione, quando un servizio chiede di rallentare o quando la tua Machine ha poco spazio. I nuovi messaggi hanno sempre la precedenza.

Una volta importata la cronologia di una casella, la tua Machine rilegge una volta le email che conserva per trovare i dettagli di prenotazioni e biglietti, così anche le prenotazioni meno recenti compaiono in [viaggi ed eventi](calendar.md#trips-and-events). La rilettura procede altrettanto lentamente e si interrompe per gli stessi motivi.

Usa le autorizzazioni già concesse a ogni connessione. Non devi approvare nulla di nuovo.

## Quanto indietro risale

Circa un anno. Sul tuo computer, puoi modificare il valore di `history_days` nel file delle impostazioni (0 disattiva la funzione, il massimo è 730). Telegram e le altre fonti non importano la cronologia meno recente.

I messaggi di LinkedIn e X risalgono a 90 giorni fa. Vengono letti molto lentamente: poche letture brevi all’ora, solo di giorno, e nessuna per un giorno se il sito oppone resistenza, così il tuo account resta al sicuro (`social_history_days`, 0 disattiva la funzione).
