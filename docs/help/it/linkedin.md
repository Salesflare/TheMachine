---
title: LinkedIn
area: connections
summary: I tuoi messaggi LinkedIn, letti nel browser della tua Machine, con il tuo accesso. Risponde solo dopo la tua approvazione.
covers: connector:linkedin
code: connectors/linkedin.py, integrations/linkedin_inbox.py
site: Connect, More sources, Remove
---
## Cosa legge

I tuoi messaggi LinkedIn. Li legge in una scheda del browser della tua Machine, con il tuo accesso, di tanto in tanto durante le ore di veglia. Non usa chiavi API e non segna nulla come letto.

## Cosa può inviare

Una risposta a un messaggio, e solo dopo che l’hai approvata nell’attività. Fino ad allora prepara solo una bozza.

## Collegalo

Su una Machine in hosting:

1. Apri la tua pagina di configurazione su app.themachine.computer/setup e vai su **Altre fonti**.
2. Apri LinkedIn, accedi a LinkedIn nel browser della tua Machine quando te lo chiede, poi premi **Collegati**.

Sul tuo computer:

1. Accedi una volta a LinkedIn nel browser della tua Machine (Impostazioni, **Apri il browser della Machine ↗**).
2. Nella dashboard, apri **Connessioni**, poi **+ Aggiungi**, e scegli LinkedIn. Oppure esegui `assistant connect linkedin`.

Un secondo account LinkedIn ha un browser tutto suo. Se LinkedIn disconnette la tua Machine, vedi [Disconnesso da un sito](signed-out.md).

## Se LinkedIn chiede un codice

La prima volta che la tua Machine accede, LinkedIn spesso invia un codice per email. Scrivilo nella finestra di accesso sotto **Codice** e premi **Accedi**. La pagina resta ferma mentre scrivi.

Se LinkedIn torna all’inizio, o non succede niente per due minuti, LinkedIn ha interrotto l’accesso. Aspetta un minuto e premi **Riprova**. Se LinkedIn mostra un controllo anti-robot, completalo nel browser della tua Machine.

## Rimuovilo

- Nella dashboard: **Connessioni**, apri LinkedIn, **Dettagli**, poi **Disconnetti**. Smette di leggere. Quello che ha già portato dentro resta.
- Su una Machine in hosting puoi anche premere **Rimuovi** accanto a LinkedIn nella tua pagina di configurazione.

## Disconnettilo su LinkedIn

In LinkedIn, apri Impostazioni, Accesso e sicurezza, Dove hai effettuato l’accesso, e chiudi la sessione del browser della tua Machine.
