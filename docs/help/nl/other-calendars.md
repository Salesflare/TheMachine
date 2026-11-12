---
title: iCloud en andere agenda's (CalDAV)
area: connections
summary: Afspraken uit iCloud-agenda of elke CalDAV-agenda, zoals Fastmail, Nextcloud of Zoho. Alleen lezen.
covers: connector:icloud_calendar, connector:caldav
code: caldav_calendar.py, ical.py, machine/sources/calendar_setup.py
order: 14
---
## Wat het leest

Je afspraken, met hun gasten, zalen en notities: de afgelopen week en de volgende maand als je koppelt, daarna elke wijziging. Ze verschijnen in Agenda en in de voorbereiding van je afspraken, net als afspraken uit Google of Outlook. Elke agenda van het account wordt gelezen, of alleen die die je noemt.

Het leest alleen: het voegt nooit een afspraak toe, verplaatst er geen en verwijdert er geen.

## iCloud-agenda koppelen

1. Maak een app-specifiek wachtwoord aan op [appleid.apple.com](https://appleid.apple.com), onder **Inloggen en beveiliging**. Dat van iCloud Mail werkt ook.
2. Open in het dashboard **Koppelingen**, dan **+ Toevoegen**, en kies **iCloud-agenda**.
3. Vul je Apple ID en het app-specifieke wachtwoord in en druk op **Verbinden**.

## Een andere agenda koppelen

1. Open **Koppelingen**, dan **+ Toevoegen**, en kies **Andere agenda**.
2. Vul je e-mailadres en wachtwoord in. Veel providers willen hier een app-wachtwoord, dat je aanmaakt in je accountinstellingen.
3. Druk op **Verbinden**.

De server wordt gevonden voor Fastmail, Yahoo, Zoho en servers die zichzelf aankondigen. Die van jou niet gevonden? Open **Serverinstellingen** en typ het CalDAV-adres, zoals `nextcloud.example.com/remote.php/dav`. **Alleen deze agenda** leest één agenda op naam.

Agenda's van Google of Microsoft? Kies dan **Google Calendar** of **Outlook-agenda**.

## Als het stopt

- **De agendaserver weigerde het wachtwoord**: je hebt het gewijzigd, of het app-wachtwoord is verwijderd. Koppel opnieuw met een nieuw.
- **De agendaserver was niet bereikbaar**: hij probeert het zelf opnieuw. Blijft het mislukken, kijk dan het adres na in Serverinstellingen.

## Verwijderen

**Koppelingen**, open de agenda, **Details**, dan **Ontkoppelen**. Wat al binnen is, blijft. Verwijder het app-wachtwoord ook bij je provider.
