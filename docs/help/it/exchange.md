---
title: Exchange Server
area: connections
summary: Riunioni da un Exchange Server gestito dalla tua azienda (dal 2013 al 2019 o Subscription Edition). Solo lettura.
covers: connector:exchange
code: ews_calendar.py, machine/sources/calendar_setup.py
order: 16
---
## Cosa legge

Le tue riunioni, con invitati, sale e note: la settimana passata e il mese successivo quando colleghi, poi ogni modifica. Compaiono in Calendario e nella preparazione delle riunioni.

È in sola lettura: non aggiunge, non sposta e non rimuove mai una riunione. La posta di Exchange Server non viene ancora letta.

## Microsoft 365 o Exchange Server?

Exchange Server gira nella tua azienda. Microsoft 365 (Exchange Online) è il cloud di Microsoft: per quello scegli invece **Calendario Outlook**. Se il tuo indirizzo risulta su Microsoft 365, il modulo te lo dice.

## Collegalo

1. Nella dashboard, apri **Connessioni**, poi **Calendario**, e scegli **Exchange Server**.
2. Inserisci il tuo indirizzo email di lavoro e la tua password di Windows.
3. Premi **Collegati**.

Il server viene trovato dal tuo indirizzo (Autodiscover). Non trovato? Apri **Impostazioni del server** e scrivi il server che il tuo team IT indica per Outlook, come `mail.example.com`. Accedi con un nome diverso dal tuo indirizzo? Scrivilo come `DOMAIN\name` in **Nome utente**.

Accede con NTLM o Basic, solo tramite https.

## Se si ferma

- **Il server del calendario ha rifiutato la password**: la tua password di Windows è cambiata. Ricollegalo.
- **Una casella Microsoft 365**: la tua casella è passata a Microsoft 365. Disconnetti questa e collega **Calendario Outlook**.
- **Il server del calendario non è raggiungibile**: riprova da solo. Alcuni server sono raggiungibili solo dalla rete aziendale o tramite VPN.

## Rimuovilo

**Connessioni**, apri il calendario, **Dettagli**, poi **Disconnetti**. Quello che ha già portato resta.
