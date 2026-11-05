---
title: GitHub
area: connections
summary: Richieste di revisione, menzioni, assegnazioni ed esecuzioni CI fallite. Apre issue solo quando confermi.
covers: connector:github
code: connectors/github.py, onboarding.py
site: Sign in with GitHub, More sources, Remove
---
## Cosa legge

Le tue notifiche GitHub: richieste di revisione, menzioni, assegnazioni, risposte ed esecuzioni CI fallite. Non segna mai una notifica come letta.

## Cosa può fare

Leggere non cambia nulla su GitHub. Quando un’attività finisce con un passo su GitHub, come aprire una issue, quel passo usa lo stesso accesso gh appena tocchi **Conferma**, e l’attività lo dice prima. Gli screenshot passano comunque dal browser della tua Machine, perché lo strumento di GitHub non può aggiungere immagini. Senza GitHub collegato, l’attività dice che userà il browser, con **Collega GitHub**.

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
