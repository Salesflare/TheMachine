---
title: Proton Calendar e link di calendario (ICS)
area: connections
summary: Riunioni dal link di condivisione di un calendario: Proton Calendar, calendari pubblicati, scolastici o sportivi. Solo lettura.
covers: connector:proton_calendar, connector:ics
code: ics_feed.py, ical.py, machine/sources/calendar_setup.py
order: 15
---
## Cosa legge

Gli eventi del calendario dietro il link, con eventi ricorrenti e fusi orari: la settimana passata e il mese successivo, poi ogni modifica. Compaiono in Calendario e nella preparazione delle riunioni.

Un link si può solo leggere, quindi non cambia mai una riunione. Il link viene controllato al massimo ogni 15 minuti. Secondo Proton le modifiche possono impiegare qualche ora per arrivare a un link.

## Collega Proton Calendar

Proton Calendar non ha altri accessi per le app, quindi usa un link di condivisione.

1. Apri Proton Calendar sul web, su calendar.proton.me. Nelle sue app per telefono non si possono creare link di condivisione.
2. Vai su "Impostazioni", "Tutte le impostazioni", "Calendari", e scegli il calendario.
3. In "Share with anyone", premi "Create link" e scegli "Full view". Limited view mostra solo quando sei occupato.
4. Premi "Copy link".
5. Nella dashboard, apri **Connessioni**, poi **+ Aggiungi**, scegli **Proton Calendar**, incolla il link e premi **Collegati**.

## Collega qualsiasi altro link di calendario

Scegli **Link del calendario (ICS)** e incolla il link: un indirizzo https o webcal che finisce in .ics, come un calendario pubblico di iCloud, un calendario pubblicato di Outlook o il calendario della scuola di tuo figlio.

## Tieni privato il link

Chiunque abbia il link può leggere il calendario. The Machine lo custodisce come una password: mai in un log o sullo schermo. Per fermarlo, elimina il link dove l’hai creato, poi premi qui **Disconnetti**.

## Se si ferma

- **Il link del calendario non funziona più**: il link è stato eliminato o cambiato. Creane uno nuovo e ricollegalo.
- **Il server del calendario non è raggiungibile**: riprova da solo.
