---
title: Google Meet
area: connections
summary: Trascrizioni e note di Gemini delle riunioni Meet che organizzi. Legge soltanto.
covers: connector:google_meet
code: connectors/google_meet.py
site: Connect, More sources, Remove
---
## Cosa legge

Trascrizioni e note di Gemini delle riunioni Google Meet che hai organizzato, appena Meet le ha create: gli ultimi 7 giorni quando lo colleghi, poi quelle nuove man mano che arrivano. Meet le conserva per 30 giorni.

Meet le crea solo se trascrizioni o note di Gemini erano attive durante la riunione.

## Cosa può fare

Niente in Meet o Drive. Legge soltanto e non attiva mai le trascrizioni da solo.

## Collegalo

1. In Google Cloud, attiva l'API di Google Meet e l'API di Google Drive.
2. Nell'OAuth Playground, ottieni un token di accesso con i due scope di sola lettura mostrati nella schermata di collegamento.
3. Su una Machine in hosting: apri la tua pagina di configurazione su app.themachine.computer/setup, vai su **Altre fonti** e apri Google Meet. Sul tuo computer: **Connessioni**, **+ Aggiungi**, Google Meet, oppure `assistant connect google_meet`.
4. Incolla il token e premi **Collegati**.

Il token scade dopo circa un'ora. Quando Connessioni dice che è stato rifiutato, incollane uno nuovo.

## Rimuovilo

- Nella dashboard: **Connessioni**, apri Google Meet, **Dettagli**, poi **Disconnetti**. Ciò che ha già importato resta.
- Su una Machine in hosting puoi anche premere **Rimuovi** accanto a Google Meet nella tua pagina di configurazione.

## Revocalo in Google

Apri myaccount.google.com/permissions e rimuovi l'accesso dell'OAuth Playground.
