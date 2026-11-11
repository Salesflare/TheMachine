---
title: LinkedIn
area: connections
summary: I tuoi messaggi LinkedIn, letti nel browser della tua Machine, con il tuo accesso. Risponde solo dopo la tua approvazione.
covers: connector:linkedin
code: connectors/linkedin.py, integrations/linkedin_inbox.py, linkedin_connections.py
site: Connect, More sources, Remove
---
## Cosa legge

I tuoi messaggi LinkedIn. Li legge in una scheda del browser della tua Machine, con il tuo accesso, di tanto in tanto durante le ore di veglia. Non usa chiavi API e non segna nulla come letto.

## Ruoli e aziende

Tiene anche aggiornati i ruoli e le aziende dei tuoi collegamenti LinkedIn sulle persone già nel tuo Graph, dalla tua lista di collegamenti. Non apre i loro profili e non aggiunge persone nuove. Quando il ruolo o l’azienda di qualcuno cambia, la sua cronologia lo dice, come "Ora Head of Sales presso Acme, prima Sales Lead presso Acme".

Il ruolo viene dal loro sommario, come "Head of Sales presso Acme" o "VP Sales and Strategy", mai da uno slogan. Li trova dal link del profilo, o da nome e azienda. Senza un’azienda da confrontare, basta un nome completo che ha una sola persona nel tuo Graph. La loro pagina mostra anche da quando siete collegati.

Legge molto lentamente: una pagina alla volta, a minuti di distanza, qualche decina di pagine al giorno, solo di giorno. Circa 3.000 collegamenti richiedono quattro giorni. Se LinkedIn frena, si ferma fino al giorno dopo.

## Cosa può inviare

Una risposta a un messaggio, o un nuovo messaggio a un profilo che indichi, e solo dopo che l’hai approvato nell’attività. Fino ad allora prepara solo una bozza.

LinkedIn non offre un modo ufficiale per farlo. Leggere e inviare ogni tanto un messaggio che hai approvato difficilmente crea problemi; inviare in massa o in automatico può far bloccare un account.

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
