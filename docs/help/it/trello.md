---
title: Trello
area: connections
summary: Modifiche alle schede, commenti e attività su una bacheca Trello. Legge soltanto.
covers: connector:trello
code: connectors/trello.py
site: Connect, More sources, Remove
---
## Cosa legge

Modifiche alle schede, commenti e attività su una bacheca Trello per connessione. Non segna mai una bacheca come vista.

## Cosa può fare

Niente in Trello. Legge soltanto.

## Collegala

1. Su trello.com/power-ups/admin, crea un Power-Up con un nome qualsiasi.
2. Apri la sua pagina della chiave API e copia la chiave API (non il secret).
3. Fai clic sul link Token accanto, consenti l'accesso in lettura e copia il token.
4. Su una Machine in hosting: apri la tua pagina di configurazione su app.themachine.computer/setup, vai su **Altre fonti** e apri Trello. Sul tuo computer: **Connessioni**, **+ Aggiungi**, Trello, oppure `assistant connect trello`.
5. Inserisci l'indirizzo della bacheca, la chiave API e il token, poi premi **Collegati**.

## Rimuovila

- Nella dashboard: **Connessioni**, apri la bacheca, **Dettagli**, poi **Disconnetti**. Quello che ha già portato resta.
- Su una Machine in hosting puoi anche premere **Rimuovi** accanto a essa nella tua pagina di configurazione.

## Revocala in Trello

Revoca il token nelle impostazioni del tuo account Trello, sotto Applicazioni, oppure elimina il Power-Up.
