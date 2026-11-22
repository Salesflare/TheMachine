---
title: Exchange Server
area: connections
summary: Afspraken van een Exchange Server die je bedrijf zelf beheert (2013 tot en met 2019 of Subscription Edition). Alleen-lezen.
covers: connector:exchange
code: ews_calendar.py, machine/sources/calendar_setup.py
order: 16
translated: f2b98c9bd4f08dba
---
## Wat wordt gelezen

Je afspraken, met de gasten, ruimtes en notities: de afgelopen week en de komende maand wanneer je koppelt, en daarna elke wijziging. Ze verschijnen in **Agenda** en bij de voorbereiding van meetings.

De koppeling is alleen-lezen: er worden nooit afspraken toegevoegd, verplaatst of verwijderd. Mail uit Exchange Server wordt nog niet gelezen.

## Microsoft 365 of Exchange Server?

Exchange Server draait bij je bedrijf. Microsoft 365 (Exchange Online) is de cloud van Microsoft. Kies daarvoor **Outlook-agenda**.

Vul eerst je e-mailadres in. Als het om Microsoft 365 gaat, staat dat op het formulier en zie je **Inloggen met Microsoft** in plaats van het wachtwoordveld. Daarmee open je de inlogpagina van Outlook-agenda, zonder wachtwoord. Wordt het adres niet binnen een paar seconden gevonden, of beheert je bedrijf een eigen server? Dan blijft het wachtwoordformulier staan.

## Koppelen

1. Open in het dashboard **Koppelingen**, daarna **Agenda**, en kies **Exchange Server**.
2. Vul je zakelijke e-mailadres en Windows-wachtwoord in.
3. Klik op **Koppelen**.

De server wordt gevonden op basis van je e-mailadres (Autodiscover). Wordt de server niet gevonden? Open **Serverinstellingen** en vul de server in die je IT-afdeling voor Outlook opgeeft, bijvoorbeeld `mail.example.com`. Log je in met een andere naam dan je e-mailadres? Vul die dan in bij **Gebruikersnaam**, als `DOMAIN\name`.

Inloggen gebeurt via NTLM of Basic, alleen via https.

## Als de koppeling niet meer werkt

- **De agendaserver weigerde het wachtwoord**: je Windows-wachtwoord is gewijzigd. Koppel de agenda opnieuw.
- **Een Microsoft 365-mailbox**: je mailbox is verplaatst naar Microsoft 365. Ontkoppel deze agenda en koppel **Outlook-agenda**.
- **De agendaserver was niet bereikbaar**: er wordt automatisch opnieuw geprobeerd. Sommige servers zijn alleen bereikbaar via het bedrijfsnetwerk of VPN.

## De koppeling verwijderen

Open **Koppelingen**, open de agenda en kies **Details** en daarna **Ontkoppelen**. Wat al is binnengehaald, blijft staan.
