---
title: iCloud e altri calendari (CalDAV)
area: connections
summary: Riunioni dal Calendario iCloud o da qualsiasi calendario CalDAV, come Fastmail, Nextcloud o Zoho. Solo lettura.
covers: connector:icloud_calendar, connector:caldav
code: caldav_calendar.py, ical.py, machine/sources/calendar_setup.py
order: 14
---
## Cosa legge

Le tue riunioni, con invitati, sale e note: la settimana passata e il mese successivo quando colleghi, poi ogni modifica. Compaiono in Calendario e nella preparazione delle riunioni, come le riunioni di Google o Outlook. Viene letto ogni calendario dell’account, o solo quello che indichi.

È in sola lettura: non aggiunge, non sposta e non rimuove mai una riunione.

## Collega il Calendario iCloud

1. Crea una password specifica per l’app su [appleid.apple.com](https://appleid.apple.com), in **Accesso e sicurezza**. Va bene anche quella creata per iCloud Mail.
2. Nella dashboard, apri **Connessioni**, poi **Calendario**, e scegli **Calendario iCloud**.
3. Inserisci il tuo Apple ID e la password specifica per l’app, poi premi **Collegati**.

## Collega un altro calendario

1. Apri **Connessioni**, poi **Calendario**, e scegli **Altro calendario**.
2. Inserisci il tuo indirizzo email e la password. Molti provider qui chiedono una password per le app, da creare nelle impostazioni dell’account.
3. Premi **Collegati**.

Il server viene trovato per Fastmail, Yahoo, Zoho e i server che lo annunciano. Il tuo non viene trovato? Apri **Impostazioni del server** e scrivi il suo indirizzo CalDAV, come `nextcloud.example.com/remote.php/dav`. **Solo questo calendario** legge un solo calendario per nome.

Calendari di Google o Microsoft? Scegli invece **Google Calendar** o **Calendario Outlook**.

## Se si ferma

- **Il server del calendario ha rifiutato la password**: l’hai cambiata, o la password per le app è stata rimossa. Ricollegalo con una nuova.
- **Il server del calendario non è raggiungibile**: riprova da solo. Se continua a non riuscire, controlla l’indirizzo in Impostazioni del server.

## Rimuovilo

**Connessioni**, apri il calendario, **Dettagli**, poi **Disconnetti**. Quello che ha già portato resta. Rimuovi anche la password per le app presso il tuo provider.
