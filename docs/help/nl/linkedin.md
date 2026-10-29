---
title: LinkedIn
area: connections
summary: Je LinkedIn-berichten, gelezen in de eigen ingelogde browser van je Machine. Antwoordt pas nadat je het goedkeurt.
covers: connector:linkedin
code: connectors/linkedin.py, integrations/linkedin_inbox.py
site: Connect, More sources, Remove
---
## Wat het leest

Je LinkedIn-berichten. Het leest ze in een tabblad van de eigen browser van je Machine, ingelogd als jou, af en toe tijdens de uren dat je wakker bent. Het gebruikt geen API-sleutel en markeert niets als gelezen.

## Wat het kan versturen

Een antwoord op een bericht, en pas nadat je het goedkeurt op de to-do. Tot dan schrijft het alleen een concept.

## Koppelen

Op een gehoste Machine:

1. Open je setuppagina op app.themachine.computer/setup en ga naar **Meer bronnen**.
2. Open LinkedIn, log in bij LinkedIn in de browser van je server als daarom gevraagd wordt, en druk dan op **Verbinden**.

Op je eigen computer:

1. Log één keer in bij LinkedIn in de browser van je Machine (Instellingen, **De browser van je Machine openen ↗**).
2. Open in het dashboard **Koppelingen**, dan **+ Toevoegen**, en kies LinkedIn. Of voer `assistant connect linkedin` uit.

Een tweede LinkedIn-account krijgt een eigen browser. Logt LinkedIn je Machine uit, zie dan [Uitgelogd op een site](signed-out.md).

## Als LinkedIn om een code vraagt

De eerste keer dat je Machine inlogt, mailt LinkedIn vaak een code. Typ die in het inlogvenster bij **Code** en druk op **Inloggen**. De pagina blijft staan terwijl je typt.

Gaat LinkedIn terug naar het begin, of gebeurt er twee minuten niets, dan stopte LinkedIn het inloggen. Wacht een minuut en druk op **Opnieuw proberen**. Toont LinkedIn een robotcheck, maak die dan af in de browser van je Machine.

## Verwijderen

- In het dashboard: **Koppelingen**, open LinkedIn, **Details**, dan **Ontkoppelen**. Het stopt met lezen. Wat al binnengehaald is, blijft.
- Op een gehoste Machine kun je ook op **Verwijderen** ernaast drukken op je setuppagina.

## Uitloggen op LinkedIn

Open in LinkedIn Settings, Sign in and security, Where you're signed in, en log de sessie van de browser van je Machine uit.
