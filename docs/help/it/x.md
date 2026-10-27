---
title: X
area: connections
summary: Le tue menzioni, risposte e messaggi diretti su X, letti nel browser della tua Machine. Invia solo dopo la tua approvazione.
covers: connector:x
code: connectors/x.py, integrations/x_inbox.py
site: Connect, More sources, Remove
---
## Cosa legge

Le tue menzioni, risposte e messaggi diretti su X. Li legge nel browser della tua Machine, con il tuo accesso. Non usa l'API per sviluppatori di X, non segna nulla come visto e non può leggere X Chat cifrata.

## Cosa può inviare

Una risposta o un messaggio diretto, e solo dopo che l'hai approvato sull'attività.

## Collegalo

Su una Machine in hosting:

1. Apri la tua pagina di configurazione su app.themachine.computer/setup e vai su **Altre fonti**.
2. Apri X, scrivi il tuo nome utente senza la @, accedi a X nel browser del tuo server quando te lo chiede, poi premi **Collegati**.

Sul tuo computer:

1. Accedi a X una volta nel browser della tua Machine (Impostazioni, **Apri il browser della Machine ↗**).
2. Nella dashboard, apri **Connessioni**, poi **+ Aggiungi**, e scegli X. Oppure esegui `assistant connect x`.
3. Scrivi il tuo nome utente, e quello con cui il browser di solito ha l'accesso.

Se X disconnette la tua Machine, vedi [Disconnesso da un sito](signed-out.md).

## Rimuovilo

- Nella dashboard: **Connessioni**, apri X, **Dettagli**, poi **Disconnetti**. Smette di leggere. Quello che ha già portato resta.
- Su una Machine in hosting puoi anche premere **Rimuovi** accanto a esso nella tua pagina di configurazione.

## Esci da X

In X, apri Impostazioni, Sicurezza e accesso all'account, App e sessioni, Sessioni, ed esci dalla sessione del browser della tua Machine.
