---
title: Google Meet
area: connections
summary: Trascrizioni e note di Gemini delle riunioni Meet che organizzi. Legge soltanto.
covers: connector:google_meet
code: connectors/google_meet.py, onboarding.py
site: Sign in with Google
---
## Cosa legge

Trascrizioni e note di Gemini delle riunioni Google Meet che hai organizzato, appena Meet le ha create: gli ultimi 7 giorni quando lo colleghi, poi quelle nuove man mano che arrivano. Meet le conserva per 30 giorni.

Meet le crea solo se trascrizioni o note di Gemini erano attive durante la riunione.

Ognuna viene abbinata alla riunione del tuo calendario alla stessa ora. Le note di Gemini compaiono in Note di quella riunione e la trascrizione in Trascrizione, segnate **Da Google Meet**, accanto a ciò che hai aggiunto lì; non lo sostituiscono mai.

## Cosa può fare

Niente in Meet, Docs o Drive. Legge soltanto e non attiva mai le trascrizioni da sola.

## Cosa chiede

Un OK a parte, separato dall’accesso alla posta. Google chiede di consentire a The Machine di:

- Vedere le tue riunioni Google Meet, con trascrizioni e note di Gemini.
- Vedere i tuoi Google Docs, per leggere il documento con le note di Gemini.

Non chiede mai il tuo Drive. L’accesso a Gmail e Calendar resta com’è.

## Collegalo

Non serve avere Gmail collegato. Per collegarlo:

- Machine in hosting: nella dashboard, apri **Connessioni**, **+ Aggiungi**, scegli **Google Meet** e premi **Accedi con Google**. Google chiede l’OK qui sopra, poi torni alla dashboard.
- Il tuo computer, abbinato al tuo account: gli stessi passaggi. L’accesso si apre in una nuova scheda.

Verifica che l’accesso possa leggere Meet. Senza quell’OK non viene aggiunto. L’accesso continua a funzionare: non c’è niente da incollare o rinnovare.

Se più avanti revochi l’OK, la scheda di Google Meet ti chiede di accedere di nuovo.

## Rimuovilo

Nella dashboard: **Connessioni**, apri Google Meet, **Dettagli**, poi **Disconnetti**. Quello che ha già portato resta.

## Revocalo in Google

Apri myaccount.google.com/permissions e rimuovi l’accesso di The Machine a Google Meet. Gmail e Calendar continuano a funzionare.
