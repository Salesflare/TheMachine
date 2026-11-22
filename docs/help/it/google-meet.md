---
title: Google Meet
area: connections
summary: Trascrizioni e note Gemini delle riunioni Meet che organizzi. La tua Machine può solo leggerle.
covers: connector:google_meet
code: connectors/google_meet.py, onboarding.py
site: Sign in with Google
translated: cea7230915b5a536
---
## Cosa legge

Le trascrizioni e le note Gemini delle riunioni Google Meet che hai organizzato, una volta disponibili: quelle degli ultimi 7 giorni al momento della connessione, poi le nuove man mano che arrivano. Meet le conserva per 30 giorni.

Meet le crea solo se durante la riunione erano attive le trascrizioni o le note Gemini.

Ognuna viene aggiunta alla riunione corrispondente nel tuo Calendar: le note di Gemini sotto Note, la trascrizione sotto Trascrizione, contrassegnata come **Da Google Meet**. Quello che hai aggiunto tu resta.

## Cosa può fare

Non fa nulla in Meet, Docs o Drive. Può solo leggere e non attiva mai le trascrizioni.

## Quali autorizzazioni richiede

Un’autorizzazione specifica, separata da quella per la posta. Google chiede di consentire a The Machine di:

- Vedere le tue riunioni Google Meet, le relative trascrizioni e le note Gemini.
- Vedere i tuoi documenti Google Docs per leggere il documento con le note Gemini.

Non chiede mai accesso a Drive. Gli accessi a Gmail e Calendar restano invariati.

## Connetti

Non serve che Gmail sia connesso. Per connettere Google Meet:

- Machine ospitata: nella dashboard, apri **Connessioni**, **Riunioni**, seleziona **Google Meet** e premi **Accedi con Google**. Concedi le autorizzazioni indicate sopra e tornerai alla dashboard.
- Sul tuo computer, con il tuo account associato: segui gli stessi passaggi. La schermata di accesso si apre in una nuova scheda.

Senza l’autorizzazione per Meet, Google Meet non viene aggiunto. Non c’è nulla da incollare o rinnovare.

Se in seguito revochi l’autorizzazione, Google Meet in **Connessioni** ti chiederà di accedere di nuovo.

## Rimuovi

Nella dashboard: apri **Connessioni**, seleziona Google Meet, poi **Dettagli** e **Disconnetti**. I contenuti già importati restano.

## Revoca l’accesso da Google

Apri myaccount.google.com/permissions e rimuovi l’accesso di The Machine a Google Meet. Gmail e Calendar continueranno a funzionare.
