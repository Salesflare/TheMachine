---
title: LinkedIn
area: connections
summary: Je LinkedIn-berichten, gelezen in de browser van je Machine terwijl je daar bent ingelogd. Antwoorden worden pas verstuurd nadat je ze goedkeurt.
covers: connector:linkedin
code: connectors/linkedin.py, integrations/linkedin_inbox.py, linkedin_connections.py
site: Connect, More sources, Remove
translated: 850b91f79b9e23fc
---
## Wat hij leest

Je LinkedIn-berichten. Hij leest ze af en toe in de eigen browser van je Machine, terwijl je daar bent ingelogd, op momenten dat je wakker bent. Hij markeert niets als gelezen. Ook berichten in gearchiveerde gesprekken en berichtverzoeken komen binnen. Spam niet.

## Functies en bedrijven

Hij houdt ook de functies en bedrijven van je LinkedIn-connecties bij voor de mensen die al in je Graph staan, vanuit je lijst met Koppelingen. Hij opent hun profielen niet en voegt geen nieuwe mensen toe. Als iemands functie of bedrijf verandert, staat dat in de tijdlijn, bijvoorbeeld: "Nu Head of Sales bij Acme, was Sales Lead bij Acme".

De functie komt uit hun kopregel, bijvoorbeeld "Head of Sales bij Acme" of "VP Sales and Strategy", nooit uit een slogan. Hij vindt ze via hun profiellink, of op basis van naam en bedrijf. Als er geen bedrijf is om mee te vergelijken, is een volledige naam genoeg als die maar bij één persoon in je Graph hoort. Op hun pagina staat ook hoelang je al met ze verbonden bent.

Hij leest heel langzaam: één pagina tegelijk, met een paar minuten ertussen, een paar dozijn pagina's per dag en alleen overdag. Ongeveer 3.000 connecties kosten zo'n vier dagen. Als LinkedIn tegenwerkt, stopt hij tot de volgende dag.

## Wat hij kan versturen

Een antwoord op een bericht of een nieuw bericht aan een profiel dat je opgeeft, maar alleen nadat je het goedkeurt bij de to-do. Tot die tijd maakt hij alleen concepten.

LinkedIn biedt hiervoor geen officiële manier. Lezen en af en toe een bericht versturen dat je hebt goedgekeurd, levert waarschijnlijk geen problemen op. Bij massaal of automatisch versturen kan een account worden geblokkeerd.

## Koppelen

Op een gehoste Machine:

1. Open je instellingenpagina op app.themachine.computer/setup en ga naar **Meer bronnen**.
2. Open LinkedIn en log in bij LinkedIn in de browser van je Machine als daarom wordt gevraagd. Druk daarna op **Verbinden**.

Op je eigen computer:

1. Open in het dashboard **Koppelingen**, daarna **Chat**, en kies LinkedIn.
2. Kies **Werk** (met het bijbehorende bedrijf) of **Privé** en druk daarna op **Verbinden**.
3. Druk op **Inloggen bij LinkedIn** en log in in de browser van je Machine. Zodra je bent ingelogd, wordt de koppeling automatisch gemaakt.

Of voer `assistant connect linkedin` uit.

Een tweede LinkedIn-account krijgt een eigen browser. Als LinkedIn je Machine uitlogt, lees dan [Uitgelogd bij een website](signed-out.md).

## Als LinkedIn om een code vraagt

De eerste keer dat je Machine inlogt, stuurt LinkedIn vaak een code per e-mail. Typ die in het inlogvenster onder **Code** en druk op **Inloggen**. De pagina blijft open terwijl je de code invoert.

Als LinkedIn teruggaat naar het begin of er na twee minuten niets gebeurt, wacht dan een minuut en druk op **Opnieuw proberen**. Als LinkedIn een robotcontrole toont, voltooi die dan in de browser van je Machine.

## Verwijderen

- In het dashboard: open **Koppelingen**, open LinkedIn, kies **Details** en daarna **Ontkoppelen**. Hij stopt met lezen. Wat hij al heeft opgehaald, blijft staan.
- Op een gehoste Machine kun je LinkedIn ook verwijderen door op je instellingenpagina op **Verwijderen** ernaast te drukken.

## Uitloggen bij LinkedIn

Open in LinkedIn Instellingen, Aanmelden en beveiliging, Waar je bent aangemeld en log de sessie van de browser van je Machine uit.
