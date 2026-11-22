---
title: Notion
area: connections
summary: Reacties, vermeldingen en aan jou toegewezen taken in Notion. Antwoorden, nieuwe pagina’s, bewerkingen en taken als voltooid markeren worden pas uitgevoerd nadat je akkoord geeft.
covers: connector:notion
code: connectors/notion.py, doc_writes.py, notion_heads_up.py
site: Sign in with Notion, Connect, More sources, Remove
translated: 8544baf8c60cc40b
---
## Wat hij leest

De pagina’s die je Notion-koppeling kan zien. Hij haalt het volgende binnen:

- Reacties op je pagina’s, antwoorden in discussies waaraan je deelneemt en reacties waarin je wordt genoemd. Een reactie waarvoor actie van jou nodig is, wordt een to-do.
- Database-items die aan jou zijn toegewezen, met hun deadline en status. Elk item wordt een to-do en de deadline staat in **Agenda**. Als het item in Notion is voltooid, wordt de to-do automatisch afgesloten. Met **Ongedaan maken** open je hem weer.
- Nieuwe pagina’s die iemand anders toevoegt en die jij kunt zien.
- Een stille melding wanneer iemand een pagina wijzigt die je hebt laten aanpassen. Hij geeft nooit een geluidssignaal.

De eerste synchronisatie gaat 7 dagen terug. Mensen worden aan je [Graph](graph.md) gekoppeld op basis van hun e-mailadres. Als Notion geen e-mailadres deelt, gebeurt dat alleen op basis van een volledige naam die precies één persoon in je Graph heeft.

Wil je Notion alleen gebruiken om acties uit te voeren, schakel dan **Brengt signalen binnen** uit onder **Details**.

## Wat hij kan doen

Als een to-do of meeting tekst van een pagina nodig heeft, leest je Machine die pagina alleen terwijl hij eraan werkt.

Voor elk van deze acties vraagt je Machine eerst om akkoord via de bijbehorende to-do:

- Een reactie plaatsen in de betreffende discussie.
- Een nieuwe pagina maken. Die is privé totdat je hem deelt.
- Een pagina bewerken. Druk op **Wijzigingen nakijken** om elke alinea vóór en na de wijziging te bekijken en druk daarna op **Opslaan**. Je Machine schrijft alleen naar de pagina zoals jij die hebt gezien. Als iemand de pagina ondertussen heeft gewijzigd, wordt er niets opgeslagen en staat dat in de to-do.
- Een aan jou toegewezen taak als voltooid markeren. Alleen de status verandert.

Hij verwijdert, deelt of verplaatst nooit een pagina.

## Koppelen

1. Ga in het dashboard naar **Koppelingen**, **Documenten en bestanden**, Notion. Of ga op de installatiepagina van een gehoste Machine op app.themachine.computer/setup naar **Meer bronnen**, Notion. Koppel The Machine op je eigen computer eerst aan je account.
2. Druk op **Inloggen met Notion**, kies je werkruimte en de pagina’s die hij mag zien en geef toegang.
3. Terug in The Machine controleert hij meteen de login en toont hij de naam van de werkruimte.

Voeg Notion opnieuw toe voor een andere werkruimte.

## Plak een token

Druk onder **Of plak een integratietoken** op **Je token ophalen**. Notion opent de pagina met integraties. Maak een interne integratie, geef toestemming om inhoud en reacties te lezen en toe te voegen, en om gebruikersinformatie met e-mailadressen te lezen. Kopieer het token, plak het en druk op **Koppelen**.

Deel daarna in Notion je pagina’s met de integratie, onder **Koppelingen** op elke pagina. Op je eigen computer vraagt `assistant connect notion` er ook om.

## Loskoppelen

- Ga in het dashboard naar **Koppelingen**, open Notion, kies **Details** en druk op **Ontkoppelen**. Wat al is binnengehaald, blijft staan.
- Op een gehoste Machine kun je ook op je installatiepagina op **Verwijderen** ernaast drukken.

## Toegang intrekken in Notion

Ga in Notion naar **Instellingen**, **Koppelingen** en koppel The Machine los. Heb je een token geplakt? Verwijder dan de integratie op de pagina met integraties.
