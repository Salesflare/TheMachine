---
title: Exchange Server
area: connections
summary: Afspraken uit een Exchange Server die je bedrijf zelf draait (2013 tot 2019 of Subscription Edition). Alleen lezen.
covers: connector:exchange
code: ews_calendar.py, machine/sources/calendar_setup.py
order: 16
---
## Wat het leest

Je afspraken, met hun gasten, zalen en notities: de afgelopen week en de volgende maand als je koppelt, daarna elke wijziging. Ze verschijnen in Agenda en in de voorbereiding van je afspraken.

Het leest alleen: het voegt nooit een afspraak toe, verplaatst er geen en verwijdert er geen. Mail uit Exchange Server wordt nog niet gelezen.

## Microsoft 365 of Exchange Server?

Exchange Server draait bij je bedrijf. Microsoft 365 (Exchange Online) is de cloud van Microsoft: kies daarvoor **Outlook-agenda**. Blijkt je adres op Microsoft 365 te staan, dan zegt het formulier dat.

## Koppelen

1. Open in het dashboard **Koppelingen**, dan **Agenda**, en kies **Exchange Server**.
2. Vul je werkadres en je Windows-wachtwoord in.
3. Druk op **Verbinden**.

De server wordt gevonden via je adres (Autodiscover). Niet gevonden? Open **Serverinstellingen** en typ de server die je IT-team opgeeft voor Outlook, zoals `mail.example.com`. Log je in met een andere naam dan je adres? Typ die als `DOMAIN\name` onder **Gebruikersnaam**.

Het logt in met NTLM of Basic, alleen via https.

## Als het stopt

- **De agendaserver weigerde het wachtwoord**: je Windows-wachtwoord is gewijzigd. Koppel opnieuw.
- **Een Microsoft 365-mailbox**: je mailbox is verhuisd naar Microsoft 365. Ontkoppel deze en koppel **Outlook-agenda**.
- **De agendaserver was niet bereikbaar**: hij probeert het zelf opnieuw. Sommige servers zijn alleen bereikbaar binnen het bedrijfsnetwerk of via VPN.

## Verwijderen

**Koppelingen**, open de agenda, **Details**, dan **Ontkoppelen**. Wat al binnen is, blijft.
