---
title: Linear
area: connections
summary: Je Linear-issues, vermeldingen, opmerkingen, reviews en deadlines. Opmerkingen, statuswijzigingen, wijzigingen van toegewezen personen en nieuwe issues wachten op je akkoord.
covers: connector:linear
code: connectors/linear.py, linear_writes.py
site: Sign in with Linear, Connect, More sources, Remove
translated: 1e16b6abdf4fefad
---
## Wat er wordt gelezen

Je eigen Linear-inbox en de issues die aan jou zijn toegewezen. Deze koppeling haalt binnen:

- Issues die aan jou zijn toegewezen: nieuwe issues en issues waarvan de status, deadline of titel is gewijzigd. Als een issue in Linear is afgerond of geannuleerd, wordt de bijbehorende to-do automatisch gesloten. **Ongedaan maken** opent die weer.
- Vermeldingen van jou, en opmerkingen en reacties op issues die je volgt.
- Verzoeken om reviews en issues die aan triage zijn toegevoegd.
- Herinneringen aan deadlines.

Elk item wordt alleen een to-do als er iets mee moet gebeuren, op basis van de inhoud. Je eigen wijzigingen worden nooit binnengehaald. De eerste synchronisatie gaat 7 dagen terug. Personen worden in je [Graph](graph.md) gekoppeld op basis van het e-mailadres dat Linear bij hen toont.

Wil je deze koppeling alleen gebruiken om acties uit te voeren, schakel dan **Brengt signalen binnen** uit onder **Details**.

## Wat je ermee kunt doen

Voor elk van deze acties op een to-do wordt eerst je goedkeuring gevraagd:

- Een opmerking plaatsen bij het issue waar de to-do over gaat, of reageren in de thread van een opmerking. De opmerking wordt namens jou geplaatst.
- De status van dat issue wijzigen in een van de statussen van het team.
- Het issue toewijzen aan iemand in het team of aan jou.
- Een nieuw issue aanmaken in een van je teams.

De koppeling verwijdert of archiveert nooit een issue en verplaatst het nooit naar een ander team.

## Koppelen

1. In het dashboard: **Koppelingen**, **+ Toevoegen**, Linear. Of op de installatiepagina van een gehoste Machine via app.themachine.computer/setup: **Meer bronnen**, Linear. Koppel de Machine op je eigen computer eerst aan je account.
2. Druk op **Inloggen met Linear**, kies je workspace en geef toegang.
3. Terug in The Machine controleert hij meteen of je bent ingelogd en toont hij de naam van de workspace.

Voeg Linear opnieuw toe voor een andere workspace. Kies **Werk** of **Privé**, net als bij elke andere koppeling.

## Een API-sleutel plakken

Druk onder **Of plak een API-sleutel** op **Je token ophalen**. Linear opent **Settings**, **Security & access**. Maak een persoonlijke API-sleutel aan, kopieer en plak die en druk op **Koppelen**. Op je eigen computer vraagt `assistant connect linear` er ook om.

## De koppeling verwijderen

- In het dashboard: **Koppelingen**, open Linear en kies **Details** en vervolgens **Ontkoppelen**. Wat al is binnengehaald, blijft staan.
- Op een gehoste Machine kun je ook op de installatiepagina naast de koppeling op **Verwijderen** drukken.

## Toegang intrekken in Linear

Ga in Linear naar **Settings**, **Security & access** en trek de toegang van The Machine in onder authorized applications. Als je een API-sleutel hebt geplakt, trek je de sleutel op dezelfde pagina in.
