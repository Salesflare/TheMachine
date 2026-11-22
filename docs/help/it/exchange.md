---
title: Exchange Server
area: connections
summary: Riunioni da un Exchange Server gestito dalla tua azienda (versioni dal 2013 al 2019 o Subscription Edition). Sola lettura.
covers: connector:exchange
code: ews_calendar.py, machine/sources/calendar_setup.py
order: 16
translated: f2b98c9bd4f08dba
---
## Cosa legge

Le tue riunioni, con ospiti, sale e note: quelle dell’ultima settimana e del mese successivo al collegamento, poi ogni modifica. Le trovi in **Calendario** e nella preparazione delle riunioni.

È in sola lettura: non aggiunge, sposta né rimuove riunioni. Non legge ancora le email di Exchange Server.

## Microsoft 365 o Exchange Server?

Exchange Server è gestito dalla tua azienda. Microsoft 365 (Exchange Online) è il servizio cloud di Microsoft: scegli **Calendario Outlook**.

Inserisci prima il tuo indirizzo. Se è su Microsoft 365, il modulo te lo segnala e mostra **Accedi con Microsoft** al posto del campo password. Si apre la schermata di accesso di Calendario Outlook, senza password. Se il server non viene rilevato entro pochi secondi o la tua azienda gestisce un server proprio, resta disponibile il modulo password.

## Collegalo

1. Nella dashboard, apri **Connessioni**, poi **Calendario** e scegli **Exchange Server**.
2. Inserisci il tuo indirizzo email di lavoro e la password di Windows.
3. Premi **Collega**.

Il server viene individuato dal tuo indirizzo (Autodiscover). Non viene trovato? Apri **Impostazioni del server** e inserisci il server che ti indica il team IT per Outlook, ad esempio `mail.example.com`. Se accedi con un nome diverso dal tuo indirizzo, inseriscilo in **Nome utente** come `DOMAIN\name`.

L’accesso avviene tramite NTLM o Basic, solo su https.

## Se smette di funzionare

- **Il server del calendario ha rifiutato la password**: la password di Windows è cambiata. Collegalo di nuovo.
- **Una casella Microsoft 365**: la tua casella è stata spostata su Microsoft 365. Disconnetti questa connessione e collega **Calendario Outlook**.
- **Il server del calendario non è raggiungibile**: il sistema riprova automaticamente. Alcuni server sono raggiungibili solo dalla rete aziendale o tramite VPN.

## Rimuovilo

Apri **Connessioni**, seleziona il calendario, poi **Dettagli** e **Disconnetti**. I dati già importati restano.
