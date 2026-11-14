---
title: Proton Calendar en agendalinks (ICS)
area: connections
summary: Afspraken uit de deellink van een agenda: Proton Calendar, gepubliceerde agenda's, school- of sportagenda's. Alleen lezen.
covers: connector:proton_calendar, connector:ics
code: ics_feed.py, ical.py, machine/sources/calendar_setup.py
order: 15
translated: b3bcf33b5c027baf
---
## Wat het leest

De afspraken in de agenda achter de link, met terugkerende afspraken en tijdzones: de afgelopen week en de volgende maand, daarna elke wijziging. Ze verschijnen in Agenda en in de voorbereiding van je afspraken.

Een link kan alleen gelezen worden, dus er verandert nooit een afspraak. De link wordt hoogstens om de 15 minuten bekeken. Volgens Proton kan het een paar uur duren voor wijzigingen in een link zitten.

## Proton Calendar koppelen

Proton Calendar heeft geen andere toegang voor apps, dus het gebruikt een deellink.

1. Open Proton Calendar op het web, op calendar.proton.me. In de apps op je telefoon kun je geen deellinks maken.
2. Ga naar "Instellingen", "Alle instellingen", "Agenda's", en kies de agenda.
3. Druk onder "Share with anyone" op "Create link" en kies "Full view". Limited view toont alleen wanneer je bezet bent.
4. Druk op "Copy link".
5. Open in het dashboard **Koppelingen**, dan **Agenda**, kies **Proton Calendar**, plak de link en druk op **Verbinden**.

## Een andere agendalink koppelen

Kies **Agendalink (ICS)** en plak de link: een https- of webcal-adres dat eindigt op .ics, zoals een openbare iCloud-agenda, een gepubliceerde Outlook-agenda of de schoolagenda van je kind.

## Hou de link privé

Iedereen met de link kan de agenda lezen. The Machine bewaart hem als een wachtwoord: nooit in een log of op het scherm. Wil je stoppen? Verwijder de link waar je hem maakte, en druk hier op **Ontkoppelen**.

## Als het stopt

- **De agendalink werkt niet meer**: de link is verwijderd of gewijzigd. Maak een nieuwe en koppel opnieuw.
- **De agendaserver was niet bereikbaar**: hij probeert het zelf opnieuw.
