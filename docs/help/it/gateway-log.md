---
title: Stato della Machine
area: connections
summary: Il registro della tua Machine stessa, per aiutarla a rilevare i problemi. È di sola lettura.
covers: connector:gateway
code: onboarding.py
site: More sources, Remove
translated: 7d66ff6a6a5d5b1d
---
## Cosa legge

Il registro della tua Machine stessa: esecuzioni non riuscite, passaggi rifiutati, messaggi Telegram non inviati ed errori di The Machine stessa. Un’attività ti avvisa quando c’è qualcosa da correggere. Sul tuo computer, include **Completa l’installazione dell’ultimo aggiornamento**: una parte dell’aggiornamento richiede un breve riavvio notturno, ma per alcune notti non è stato possibile. Chiedi nella chat dell’attività e The Machine completa l’aggiornamento. L’attività si chiude da sola una volta installata quella parte.

## Correzioni messe da parte da un aggiornamento

Quando la Machine si aggiorna e una delle sue correzioni non è più compatibile con la nuova versione, l’aggiornamento la mette da parte e prosegue, così la tua Machine non rimane mai con una versione obsoleta. Un’attività, **Rifai una correzione messa da parte dall’aggiornamento**, indica quale correzione.

Con **Rifai**, la tua Machine crea di nuovo la correzione nella nuova versione, come per qualsiasi correzione della Machine: vedi la modifica e tocchi **Unisci correzione**. Una volta integrata, la vecchia copia viene eliminata. Oppure chiudi l’attività.

## I tuoi file conservati da un aggiornamento

Quando una nuova versione include un file con lo stesso nome di uno che hai aggiunto tu, l’aggiornamento rinomina il tuo invece di sovrascriverlo e prosegue. Un’attività indica quanti file sono stati conservati e mostra per ciascuno il nome precedente e quello nuovo. Chiudila dopo averli controllati.

## Cosa può fare

Niente. Legge soltanto il registro della tua Machine.

## Collegarla

- Su una Machine ospitata, la trovi nella pagina di configurazione, sotto **Altre fonti**, come Salute della tua Machine. Una per Machine.
- Sul tuo computer: **Connessioni**, **Altro**, Salute della tua Machine. Oppure esegui `assistant connect gateway`.

## Rimuoverla

- Nella dashboard: **Connessioni**, aprila, **Dettagli**, poi **Disconnetti**.
- Su una Machine ospitata, puoi anche premere **Rimuovi** accanto alla Machine nella pagina di configurazione.

Non c’è altro da disinstallare.
