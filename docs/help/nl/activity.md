---
title: Activiteit
area: settings
summary: Eén lijst met alles wat The Machine voor je heeft gedaan, nieuwste eerst: berichten, documenten, Fleet-antwoorden, inzichten, koppelingen en meer.
covers: settings:activity
code: activity_log.py, dashboard/settings-activity.js
order: 2
keywords: log, history, audit, what did it do, sent, refused, blocked
translated: ebb6a4cf0474a020
---
## Wat je hier ziet

Open **Instellingen** en **Activiteit**. Elke regel toont één ding dat The Machine heeft gedaan, nieuwste eerst, per dag:

- wat hij heeft gedaan en hoe het is afgelopen: verstuurd, geweigerd, mislukt of ongedaan gemaakt
- wanneer het gebeurde en welk account of welke app hij gebruikte, en [wat dit mogelijk maakte](activity.md#what-allowed-it)
- een link naar de bijbehorende to-do, als die er is
- bij een AI die je hebt gekoppeld, zoals ChatGPT of Claude: de naam met **(gekoppelde AI)**, zodat je die kunt onderscheiden van The Machine zelf

Je ziet hier berichten en antwoorden, wijzigingen in documenten en agenda's, stappen op internet, fixes die hij heeft gemerged, codeeragents, vragen en antwoorden in Fleet, inzichten die naar het team van The Machine zijn gestuurd, skills, Graph-imports, feiten die je chat hebt gevraagd te vergeten (met **Ongedaan maken**), toegevoegde of verwijderde koppelingen en elke inzage door ons team onder [Toegang voor support](get-support.md#support-access), ook geweigerde inzages.

## Wat dit mogelijk maakte

Bij elk bericht, elke wijziging in een document of agenda, elke stap op internet en elke gemergede fix staat wat die mogelijk maakte, zoals het op dat moment is vastgelegd:

- **Goedgekeurd in de to-do** of **Goedgekeurd in Telegram**: je tikte op **Versturen**, **Bevestigen** of **Mergen**
- **Goedgekeurd met je stem**: je zei ja in Talk
- **‘Doe het’ getikt**: je tikte op **Doe het** bij de to-do
- **Gevraagd in de chat**: je vroeg erom in een bericht. Het begin van je bericht staat tussen aanhalingstekens. Een citaat wordt alleen getoond zolang die woorden nog in je eigen bericht staan.
- **Opvolging, vanzelf verstuurd**, **Kleine fix, vanzelf gemerged**, **Nieuw privédocument, vanzelf gemaakt** of **Vooraf voorbereid, vanzelf**: een instelling van jou of een van de eigen regels van The Machine
- **Geen goedkeuring vastgelegd**: er is niets over vastgelegd. Dit komt ook in onze [foutrapporten](error-reports.md), zodat we kunnen achterhalen waar het vastleggen is misgegaan.

Bij Stappen op internet zie je ook de uitvoering van een to-do die op een pagina heeft geklikt of getypt, met wat die uitvoering mogelijk maakte. Werk dat na een snooze doorgaat, behoudt de reden die ervoor gold voordat het werd gesnoozed.

Bij oudere regels, van voordat dit werd vastgelegd, blijft de oude tekst staan, zoals **Na je OK**.

## Filteren

Kies bovenaan een soort in de lijst, zoals **Berichten** of **Fleet**. **Geweigerd of geblokkeerd** toont alleen wat niet is doorgegaan en waarom. Met **Meer tonen** laad je oudere regels.

## Andere plekken

De chat van een to-do vertelt nog steeds zijn eigen verhaal; vanuit Activiteit kun je die chat openen. In Fleet toont **Activiteit** dezelfde regels voor je Fleets en inzichten, met **Intrekken** bij een inzicht. Ga in Instellingen naar **Beveiliging** en open **Bekijk elke blik in Activiteit** om de inzages door ons team te bekijken.

Activiteit laat alleen zien wat er is gebeurd. Het verandert nooit wat The Machine mag doen.
