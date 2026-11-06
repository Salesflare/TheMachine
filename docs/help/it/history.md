---
title: Cronologia
area: connections
summary: Circa un anno di vecchie email, riunioni e chat WhatsApp, da cercare e leggere. Mai un'attività.
covers: history
code: machine/app/history.py, machine/store/history.py
keywords: older messages, backfill, archive, past emails
---
## Cosa tiene

Ogni account email, calendario e WhatsApp tiene circa un anno di vecchi messaggi e riunioni. La ricerca li trova, una conversazione li mostra e il [Calendario](calendar.md) mostra le riunioni passate.

La sua scheda dice fin dove arriva: **Cronologia: fino a** un mese, quando è arrivata.

## Cosa non fa mai

La cronologia serve solo a ritrovare le cose. Non crea mai un'attività o una promessa, non entra mai in un controllo, non conta mai come nuova e non va mai nel tuo Graph o al tuo team. Nessun modello di IA la legge.

Attività e promesse arrivano ancora solo dai messaggi nuovi, come prima.

## Quando funziona

Comincia quando il primo sguardo ai tuoi messaggi è finito e procede piano in background. Aspetta mentre è in corso un controllo o una sincronizzazione, e quando la tua Machine ha poco spazio su disco o poca memoria. Dopo un riavvio riprende da dove era.

Usa l'accesso che ogni connessione ha già. Non viene chiesto niente di nuovo.

## Fin dove

Circa un anno di default. Le Machine self-hosted possono impostare `history_days` nella configurazione (0 la spegne, fino a 730). Telegram, Slack e le altre fonti tengono quello che leggono oggi.
