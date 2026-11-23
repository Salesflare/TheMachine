---
title: Notion
area: connections
summary: Reacties, vermeldingen en taken die aan jou zijn toegewezen in Notion. Antwoorden, nieuwe pagina's, wijzigingen en taken als gedaan markeren wachten op je akkoord.
covers: connector:notion
code: connectors/notion.py, doc_writes.py, notion_heads_up.py
site: Sign in with Notion, Connect, More sources, Remove
translated: 2e93c261cc09e401
---
## Wat het leest

De pagina's die je Notion-koppeling kan zien. Deze brengt het volgende binnen:

- Reacties op je pagina's, antwoorden in discussies waaraan je deelneemt en reacties waarin je wordt vermeld. Een reactie waarvoor je iets moet doen, wordt een to-do.
- Database-items die aan jou zijn toegewezen, met hun deadline en status. Elk item wordt een to-do en de deadline staat in **Agenda**. Zodra het item in Notion is afgerond, wordt de to-do automatisch gesloten. Met **Ongedaan maken** open je die opnieuw.
- Nieuwe pagina's die iemand anders toevoegt en die jij kunt zien.
- Een stille melding wanneer iemand een pagina wijzigt waarvan je had gevraagd om die te laten aanpassen. Die maakt nooit geluid.

De eerste synchronisatie kijkt 7 dagen terug. Mensen worden op basis van hun e-mailadres aan je [Graph](graph.md) gekoppeld. Als Notion geen e-mailadres deelt, gebeurt dat alleen op basis van een volledige naam die precies één persoon in je Graph heeft.

Wil je deze koppeling alleen gebruiken om dingen te doen, schakel dan **Brengt signalen binnen** uit onder **Details**.

## Wat het kan doen

Als een to-do of meeting de tekst van een pagina nodig heeft, leest je Machine die pagina alleen terwijl hij eraan werkt. Van een bestand op die pagina ziet hij alleen de naam. Hij zoekt pagina's op basis van de titel, niet op basis van de bestanden erop.

Voor elk van deze acties vraagt hij eerst je akkoord via de bijbehorende to-do:

- Reageren op een opmerking in de bijbehorende discussie.
- Een nieuwe pagina maken. Die is privé totdat je hem deelt.
- Een pagina wijzigen. Druk op **Wijzigingen nakijken** om elke alinea voor en na de wijziging te zien en druk daarna op **Opslaan**. Hij schrijft alleen naar de pagina zoals jij die zag. Heeft iemand de pagina intussen gewijzigd, dan wordt er niets opgeslagen en staat dat in de to-do.
- Een taak die aan jou is toegewezen als gedaan markeren. Alleen de status verandert.

Hij verwijdert, deelt of verplaatst nooit een pagina.

## Koppelen

1. In het dashboard: **Koppelingen**, **Documenten en bestanden**, Notion. Of op de installatiepagina van een gehoste Machine op app.themachine.computer/setup: **Meer bronnen**, Notion. Op je eigen computer koppel je eerst je account.
2. Druk op **Inloggen met Notion**, kies je workspace en de pagina's die hij mag zien en geef toegang.
3. Terug in The Machine controleert hij de login meteen en toont hij de naam van de workspace.

Als je een andere workspace wilt gebruiken, voeg je Notion opnieuw toe.

## Plak liever een token

Druk onder **Of plak een integratietoken** op **Je token ophalen**. Notion opent de integratiepagina. Maak een interne integratie aan en geef toestemming om content en reacties te lezen en toe te voegen, en gebruikersinformatie met e-mailadressen te lezen. Kopieer de token, plak hem en druk op **Koppelen**.

Deel daarna je pagina's met de integratie in Notion, onder **Koppelingen** op elke pagina. Op je eigen computer vraagt `assistant connect notion` er ook om.

## Verwijderen

- In het dashboard: **Koppelingen**, open Notion, **Details** en daarna **Ontkoppelen**. Wat de koppeling al heeft binnengebracht, blijft staan.
- Op een gehoste Machine kun je ook op **Verwijderen** drukken naast de koppeling op je installatiepagina.

## Toegang intrekken in Notion

Ga in Notion naar **Instellingen**, **Koppelingen** en ontkoppel The Machine. Heb je een token geplakt, verwijder dan de integratie op de integratiepagina.
