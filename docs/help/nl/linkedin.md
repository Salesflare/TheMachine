---
title: LinkedIn
area: connections
summary: Je LinkedIn-berichten, gelezen in de eigen ingelogde browser van je Machine. Antwoordt pas nadat je het goedkeurt.
covers: connector:linkedin
code: connectors/linkedin.py, integrations/linkedin_inbox.py, linkedin_connections.py
site: Connect, More sources, Remove
---
## Wat het leest

Je LinkedIn-berichten. Het leest ze in een tabblad van de eigen browser van je Machine, ingelogd als jou, af en toe tijdens de uren dat je wakker bent. Het gebruikt geen API-sleutel en markeert niets als gelezen. Antwoorden in gesprekken die je hebt gearchiveerd en berichtverzoeken komen ook binnen; spam blijft buiten.

## Functies en bedrijven

Het houdt ook de functies en bedrijven van je LinkedIn-connecties bij op de mensen die al in je Graph staan, vanuit je lijst met connecties. Het opent hun profielen niet en voegt geen nieuwe mensen toe. Verandert iemands functie of bedrijf, dan staat dat in hun tijdlijn, zoals "Nu Head of Sales bij Acme, was Sales Lead bij Acme".

De functie komt uit hun kopregel, zoals "Head of Sales bij Acme" of "VP Sales and Strategy", nooit uit een slogan. Het vindt hen via hun profiellink, of via naam en bedrijf. Is er geen bedrijf om te vergelijken, dan volstaat een volledige naam die maar één persoon in je Graph heeft. Hun pagina toont ook sinds wanneer jullie verbonden zijn.

Het leest heel traag: één pagina tegelijk, minuten uit elkaar, een paar dozijn pagina's per dag, alleen overdag. Zo'n 3.000 connecties duren ongeveer vier dagen. Duwt LinkedIn terug, dan stopt het tot de volgende dag.

## Wat het kan versturen

Een antwoord op een bericht, of een nieuw bericht aan een profiel dat je noemt, en pas nadat je het goedkeurt op de to-do. Tot dan schrijft het alleen een concept.

LinkedIn biedt hier geen officiële manier voor. Lezen en af en toe een bericht dat je goedkeurde, geeft vrijwel nooit problemen; massaal of automatisch versturen kan tot een blokkering van het account leiden.

## Koppelen

Op een gehoste Machine:

1. Open je setuppagina op app.themachine.computer/setup en ga naar **Meer bronnen**.
2. Open LinkedIn, log in bij LinkedIn in de browser van je Machine als daarom gevraagd wordt, en druk dan op **Verbinden**.

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
