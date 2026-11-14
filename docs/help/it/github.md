---
title: GitHub
area: connections
summary: Esamina richieste di revisione, menzioni, assegnazioni e CI non riuscite. Crea issue solo dopo la tua conferma.
covers: connector:github
code: connectors/github.py, onboarding.py
site: Sign in with GitHub, More sources, Remove
translated: e97127e156e56f7d
---
## Cosa legge

Le notifiche di GitHub: richieste di revisione, menzioni, assegnazioni, risposte ed esecuzioni CI non riuscite. Non le segna mai come lette.

## Cosa può fare

La sola lettura non modifica nulla su GitHub. Quando un'attività include un passaggio GitHub, come la creazione di un issue, l'attività lo indica e il passaggio viene eseguito solo dopo che premi **Conferma** o quando lo hai richiesto esplicitamente nella chat. Gli screenshot vengono acquisiti tramite il browser della tua Machine. Se GitHub non è collegato, l'attività indica che userà il browser e mostra **Collega GitHub**.

## Collega GitHub

Su una Machine ospitata:

1. Apri **Connessioni**, poi **Progetti e codice**, e seleziona GitHub.
2. Seleziona **Lavoro** o **Personale** e premi **Accedi con GitHub**.
3. Premi **Apri GitHub ↗**, inserisci il codice mostrato e autorizza l'accesso. La connessione viene stabilita automaticamente.

La pagina di configurazione su app.themachine.computer/setup offre lo stesso accesso nella sezione **Altre fonti**.

Sul tuo computer:

1. Apri **Connessioni**, poi **Progetti e codice**, e seleziona GitHub.
2. Seleziona **Lavoro** con la tua azienda, oppure **Personale**, e premi **Collegati**.
3. Se richiesto, premi **Apri GitHub ↗**, inserisci il codice e autorizza l'accesso. La connessione viene stabilita automaticamente.

Oppure esegui `assistant connect github` e conferma il tuo accesso a GitHub.

## Rimuovi la connessione

- Apri **Connessioni**, poi GitHub, **Dettagli** e **Disconnetti**. La connessione smette di leggere le notifiche. I contenuti già importati restano.
- Su una Machine ospitata puoi anche premere **Rimuovi** accanto a GitHub nella pagina di configurazione.

## Disinstalla da GitHub

Su GitHub, apri **Impostazioni**, **Applicazioni**, **Applicazioni OAuth autorizzate** e revoca GitHub CLI. Sul tuo computer, anche `gh auth logout` disconnette l'account.
