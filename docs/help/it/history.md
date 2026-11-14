---
title: Cronologia
area: connections
summary: Circa un anno di vecchie email, riunioni e messaggi WhatsApp, Slack e Teams, per cercare, leggere e conoscere le tue persone. Mai un'attività.
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
translated: 42069e80e6f85bdb
---
## Cosa tiene

Ogni account email, calendario, WhatsApp, Slack e Teams tiene circa un anno di vecchi messaggi e riunioni. La ricerca li trova, anche per significato, una conversazione li mostra e il [Calendario](calendar.md) mostra le riunioni passate.

La sua scheda dice fin dove arriva: **Cronologia: fino a** un mese, quando è arrivata.

## Cosa aggiunge al tuo Graph

Il tuo [Graph](graph.md) la conta: quanto sei vicino alle persone, quando vi siete sentiti l'ultima volta, chi conosce chi, e le persone e le organizzazioni stesse. Anche la Cronologia di una persona o di un'organizzazione la mostra, così il suo ultimo contatto è sempre lì. Le risposte della tua Fleet a "chi conosce qualcuno" la usano dagli account di lavoro, con le stesse [regole di condivisione](sharing-rules.md) delle email nuove.

## Cosa non fa mai

Non crea mai un'attività o una promessa, non conta mai come nuova, non avvia mai un controllo e non entra mai in un progetto. La cronologia personale resta personale, come le email personali. A parte la ricerca per significato, nessun modello di IA la legge.

## Quando funziona

Comincia quando il primo sguardo ai tuoi messaggi è finito, e per ogni connessione solo quando la sua prima settimana è arrivata, anche per una che aggiungi dopo. Procede piano in background e aspetta mentre è in corso un controllo o una sincronizzazione, quando un servizio chiede di rallentare o quando la tua Machine ha poco spazio. I messaggi nuovi vengono sempre prima.

Usa l'accesso che ogni connessione ha già. Non viene chiesto niente di nuovo.

## Fin dove

Circa un anno di default. Le Machine self-hosted possono impostare `history_days` nella configurazione (0 la spegne, fino a 730). Telegram e le altre fonti tengono quello che leggono oggi.

I messaggi di LinkedIn e X risalgono a 90 giorni e vengono letti molto lentamente: poche piccole letture all’ora, solo di giorno, e nessuna per un giorno se il sito fa resistenza, così il tuo account resta al sicuro (`social_history_days`, 0 la spegne).
