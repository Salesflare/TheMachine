---
title: GitHub
area: connections
summary: Richieste di revisione, menzioni, assegnazioni ed esecuzioni CI fallite. Legge soltanto.
covers: connector:github
code: connectors/github.py, onboarding.py
site: Sign in with GitHub, More sources, Remove
---
## Cosa legge

Le tue notifiche GitHub: richieste di revisione, menzioni, assegnazioni, risposte ed esecuzioni CI fallite. Non segna mai una notifica come letta.

## Cosa può fare

Niente su GitHub. Ogni chiamata che fa è una lettura.

## Collegalo

Su una Machine ospitata:

1. Apri la tua pagina di configurazione su app.themachine.computer/setup e vai su **Altre fonti**.
2. Apri GitHub e premi **Accedi con GitHub**.
3. Scrivi su GitHub il codice che ti mostra, dal telefono o dal computer.

Sul tuo computer:

1. Prima accedi alla GitHub CLI: `gh auth login`.
2. Nella dashboard, apri **Connessioni**, poi **+ Aggiungi**, e scegli GitHub. Oppure esegui `assistant connect github`.
3. Conferma il tuo login GitHub. The Machine controlla che corrisponda a ogni sincronizzazione.

## Rimuovilo

- Nella dashboard: **Connessioni**, apri GitHub, **Dettagli**, poi **Disconnetti**. Smette di leggere. Ciò che ha già portato dentro resta.
- Su una Machine ospitata puoi anche premere **Rimuovi** accanto a GitHub nella tua pagina di configurazione.

## Disinstallalo su GitHub

Revoca l'accesso della GitHub CLI in GitHub, in Settings, Applications, Authorized OAuth Apps. Sul tuo computer, anche `gh auth logout` disconnette la CLI.
