---
title: LinkedIn
area: connections
summary: Je LinkedIn-berichten, gelezen in de eigen browser van je Machine, die met jouw account is ingelogd. Antwoorden worden pas verstuurd nadat je ze hebt goedgekeurd.
covers: connector:linkedin
code: connectors/linkedin.py, integrations/linkedin_inbox.py, linkedin_connections.py
site: Connect, More sources, Remove
translated: bc67fbc21c77a97a
---
## Wat hij leest

Je LinkedIn-berichten. Hij leest ze af en toe overdag in de eigen browser van je Machine, die met jouw account is ingelogd. Hij markeert niets als gelezen. Antwoorden in gesprekken die je hebt gearchiveerd en berichtverzoeken komen ook binnen. Spam niet.

## Functies en bedrijven

Hij houdt ook de functies en bedrijven van je LinkedIn-connecties bij die al in je Graph staan, op basis van je lijst met connecties. Hij opent hun profielen niet en voegt geen nieuwe mensen toe. Als iemands functie of bedrijf verandert, zie je dat op hun tijdlijn, bijvoorbeeld: "Nu Head of Sales bij Acme, was Sales Lead bij Acme".

De functie komt uit hun kopregel, zoals "Head of Sales at Acme" of "VP Sales and Strategy", nooit uit een slogan. Hij vindt ze aan de hand van hun profiellink, of op basis van naam en bedrijf. Als er geen bedrijf is om mee te vergelijken, is een volledige naam die maar één persoon in je Graph heeft genoeg. Op hun pagina zie je ook hoelang jullie al verbonden zijn.

Hij leest heel langzaam: één pagina tegelijk, met minuten ertussen, een paar dozijn pagina's per dag en alleen overdag. Voor ongeveer 3.000 connecties heeft hij zo'n vier dagen nodig. Als LinkedIn tegenwerkt, stopt hij tot de volgende dag.

## Wat hij kan versturen

Een antwoord op een bericht of een nieuw bericht aan een profiel dat je opgeeft, en alleen nadat je het hebt goedgekeurd bij de to-do. Tot die tijd maakt hij alleen concepten.

LinkedIn biedt hiervoor geen officiële manier. Lezen en af en toe een bericht versturen dat je hebt goedgekeurd, levert zeer waarschijnlijk geen problemen op. Door grote aantallen berichten te versturen of automatisch berichten te versturen, kan een account worden geblokkeerd.

## Koppelen

1. Open in het dashboard **Koppelingen**, ga naar **Chat** en kies LinkedIn.
2. Kies **Werk** (met het bijbehorende bedrijf) of **Privé** en druk op **Koppelen**.
3. Druk op **Inloggen bij LinkedIn** en log in in de browser van je Machine. Zodra je bent ingelogd, wordt de koppeling automatisch gemaakt.

Op een gehoste Machine werkt je installatiepagina op app.themachine.computer/setup ook: ga naar **Meer bronnen**, open LinkedIn, log in wanneer daarom wordt gevraagd en druk op **Koppelen**. Op je eigen computer doet `assistant connect linkedin` hetzelfde in een terminal.

Voor een tweede LinkedIn-account wordt een eigen browser gebruikt. Als LinkedIn je Machine uitlogt, lees dan [Uitgelogd bij een site](signed-out.md).

## Als LinkedIn om een code vraagt

LinkedIn stuurt vaak een code per e-mail wanneer je Machine voor het eerst inlogt. Typ de code in het inlogvenster onder **Code** en druk op **Inloggen**. De pagina blijft staan terwijl je typt.

Als LinkedIn teruggaat naar het begin of er na twee minuten niets gebeurt, wacht dan een minuut en druk op **Opnieuw proberen**. Als LinkedIn een robotcontrole toont, voer die dan uit in de browser van je Machine.

## Verwijderen

- In het dashboard: open **Koppelingen**, kies LinkedIn en ga naar **Details**. Druk daarna op **Ontkoppelen**. Hij stopt met lezen. Wat hij al heeft binnengehaald, blijft staan.
- Op een gehoste Machine kun je ook op je installatiepagina naast LinkedIn op **Verwijderen** drukken.

## Uitloggen via LinkedIn

Open in LinkedIn Settings, Sign in and security en Where you're signed in. Log de sessie van de browser van je Machine uit.
