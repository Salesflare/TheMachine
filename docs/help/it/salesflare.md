---
title: Salesflare CRM
area: connections
summary: Account, contatti e trattative, così sa chi conta. Legge con la tua chiave API.
covers: connector:salesflare
code: assistant.py, onboarding.py
site: More sources, Connect, Remove
---
## Cosa legge

I tuoi account, contatti e trattative in Salesflare, e i feed degli account: le email dei colleghi che non ti coinvolgono e le riunioni con note.

## Cosa può modificare

Niente, a meno che tu non imposti `join_pipelines` nel file di impostazioni della tua Machine. Allora ti aggiunge da sola agli account in quelle pipeline. Di default è vuoto.

## Collegalo

1. In Salesflare, apri [Settings, API keys](https://app.salesflare.com/#/settings/apikeys) e crea una chiave.
2. Su una Machine in hosting: apri la tua pagina di configurazione su app.themachine.computer/setup, vai su **Altre fonti**, apri Salesflare CRM, incolla la chiave e premi **Collegati**.
3. Sul tuo computer: esegui `assistant connect crm`, oppure **Connessioni**, **+ Aggiungi**, Salesflare CRM. Dopo **Collegati**, la tua Machine si riavvia e apre la scheda di Salesflare, che prima dice che sta cercando gli account con email e riunioni recenti, poi quanti ne ha letti.

## Dettagli della sincronizzazione

La sua scheda sotto **Connessioni**, **Altre fonti** mostra a che punto è: quanti account ha letto in questo giro e quanti ne ha saltati perché Salesflare rispondeva troppo lentamente. Un giro che dura da ore segnala che potrebbe essere bloccato.

- **Ferma**: non arriva nulla di nuovo finché non premi **Avvia**. Riprende da dove era.
- **Riavvia sincronizzazione**: abbandona il giro in corso, con i suoi errori, e rilegge subito l'ultima settimana. Non si perde nulla di quello che ha portato.
- **Chiavi API**: apre la pagina delle chiavi API di Salesflare, per creare una nuova chiave.

## Rimuovilo

- Nella dashboard: **Connessioni**, apri Salesflare, **Dettagli**, poi **Disconnetti**. Quello che ha già portato resta.
- Su una Machine in hosting puoi anche premere **Rimuovi** accanto a esso nella tua pagina di configurazione.

## Revocalo in Salesflare

Elimina la chiave API in Salesflare, sotto Settings, API keys.
