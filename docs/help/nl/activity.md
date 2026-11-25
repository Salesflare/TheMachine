---
title: Activiteit
area: settings
summary: Eén lijst met alles wat The Machine voor je heeft gedaan, nieuwste eerst: berichten, documenten, antwoorden in Fleet, inzichten, koppelingen en meer.
covers: settings:activity
code: activity_log.py, dashboard/settings-activity.js
order: 2
keywords: log, history, audit, what did it do, sent, refused, blocked
translated: 1ebeba09417a11e9
---
## Wat je ziet

Open **Instellingen** en dan **Activiteit**. Elke regel toont één ding dat The Machine heeft gedaan, per dag, nieuwste eerst:

- wat hij heeft gedaan en hoe het is afgelopen: verstuurd, geweigerd, mislukt of ongedaan gemaakt; bij een bericht dat [later wordt verstuurd](send-later.md) ook wanneer het is ingepland, gewijzigd of geannuleerd
- wanneer het gebeurde, welk account of welke app hij gebruikte en [wat het toestond](activity.md#what-allowed-it)
- een link naar de bijbehorende to-do, als die er is
- bij een AI die je hebt gekoppeld, zoals ChatGPT of Claude: de naam met **(verbonden AI)**, zodat je die kunt onderscheiden van The Machine zelf

Je ziet er berichten en antwoorden, wijzigingen in documenten en afspraken, stappen op het web, fixes die hij heeft gemerged, codeeragents, vragen en antwoorden in Fleet, inzichten die naar het team van The Machine zijn verstuurd, skills, Graph-imports, feiten die je je chat hebt gevraagd te vergeten (met **Ongedaan maken**), toegevoegde of verwijderde koppelingen en elke keer dat ons team heeft meegekeken onder [Toegang door support](get-support.md#support-access), ook als dat is geweigerd.

## Wat het toestond

Bij elk bericht, elke wijziging in een document of afspraak, elke stap op het web en elke gemergede fix staat wat ervoor zorgde dat het kon, zoals dat op dat moment gebeurde:

- **Goedgekeurd in de to-do** of **Goedgekeurd in Telegram**: je tik op **Versturen**, **Bevestigen** of **Samenvoegen**
- **Goedgekeurd met je stem**: je ja in Talk
- **‘Doe het’ getikt**: je tik op **Doe het** bij de to-do
- **Gevraagd in de chat**: je hebt er in woorden om gevraagd, met het begin van je bericht tussen aanhalingstekens. De quote wordt alleen getoond zolang die woorden nog in je eigen bericht staan.
- **Opvolging, vanzelf verstuurd**, **Kleine fix, vanzelf gemerged**, **Nieuw privédocument, vanzelf gemaakt** of **Vooraf voorbereid, vanzelf**: een instelling van jou of een van de eigen regels van The Machine
- **Geen goedkeuring vastgelegd**: er is niets over vastgelegd. Het komt ook in onze [foutrapporten](error-reports.md), zodat we kunnen achterhalen waar het misging.

Bij Webstappen zie je ook uitvoeringen van een to-do die op een pagina klikten of tekst invoerden, met wat die uitvoering toestond. Werk dat na een snooze doorgaat, behoudt wat het vóór de snooze toestond.

Oudere regels, van voordat dit werd vastgelegd, houden hun oude tekst, zoals **Na je OK**.

## Filteren

Kies bovenaan een soort in de lijst, zoals **Berichten** of **Fleet**. **Geweigerd of geblokkeerd** toont alleen wat niet is doorgegaan, en waarom. Met **Meer tonen** laad je oudere regels.

## Andere plekken

De chat van een to-do vertelt nog steeds zijn eigen verhaal. Activiteit bevat een link ernaartoe. In Fleet toont **Activiteit** dezelfde regels voor je Fleets en inzichten, met **Intrekken** bij een inzicht. Ga in Instellingen naar **Beveiliging** en kies **Bekijk elke blik in Activiteit** om te zien wanneer ons team heeft meegekeken.

Activiteit toont alleen wat er is gebeurd. Het verandert nooit wat The Machine mag doen.
