---
title: Activiteit
area: settings
summary: Eén lijst van alles wat The Machine voor je deed, nieuwste eerst: berichten, documenten, Fleet-antwoorden, inzichten, koppelingen en meer.
covers: settings:activity
code: activity_log.py, dashboard/settings-activity.js
order: 2
keywords: log, history, audit, what did it do, sent, refused, blocked
---
## Wat je ziet

Open **Instellingen**, **Activiteit**. Elke regel is iets wat The Machine deed, nieuwste eerst, per dag:

- wat hij deed, en hoe het afliep: verstuurd, geweigerd, mislukt of ongedaan gemaakt
- wanneer, het account of de app die hij gebruikte, en [wat het toeliet](activity.md#what-allowed-it)
- een link naar de to-do, als die er is
- bij een AI die je koppelde, zoals ChatGPT of Claude: de naam met **(gekoppelde AI)**, zodat je ze onderscheidt van The Machine zelf

Je ziet berichten en antwoorden, wijzigingen in documenten en de agenda, stappen op het web, oplossingen die hij samenvoegde, codeeragents, Fleet-vragen en -antwoorden, inzichten verstuurd naar het team van The Machine, skills, Graph-imports, feiten die je in de chat liet vergeten (met **Ongedaan maken**), toegevoegde of verwijderde koppelingen, en elke blik van ons team via [Toegang voor support](get-support.md#support-access), ook geweigerde.

## Wat het toeliet

Elk bericht, elke wijziging in een document of de agenda, elke stap op het web en elke samengevoegde fix zegt wat hem liet gaan, zoals het gebeurde:

- **Goedgekeurd in de to-do** of **Goedgekeurd in Telegram**: je tik op Versturen, Bevestigen of Samenvoegen
- **Goedgekeurd met je stem**: je ja in Talk
- **‘Doe het’ getikt**: je Doe het op de to-do
- **Gevraagd in de chat**: je vroeg het in woorden, met het begin van je bericht tussen aanhalingstekens. Een citaat staat er alleen zolang die woorden nog in je eigen bericht staan.
- **Opvolging, vanzelf verstuurd**, **Kleine fix, vanzelf gemerged**, **Nieuw privédocument, vanzelf gemaakt** of **Vooraf voorbereid, vanzelf**: een instelling van jou of een eigen regel van The Machine
- **Geen goedkeuring vastgelegd**: er werd niets vastgelegd. Het gaat ook naar onze [foutmeldingen](error-reports.md), zodat we het pad vinden dat het miste.

Stappen op het web toont ook een run van een to-do die op een pagina klikte of typte, met wat die run toeliet.

Oudere regels, van voor dit werd vastgelegd, houden hun oude woorden, zoals **Na je OK**.

## Filteren

Kies bovenaan een soort, zoals **Berichten** of **Fleet**. **Geweigerd of geblokkeerd** toont alleen wat niet ging, en waarom. **Meer tonen** laadt oudere regels.

## Andere plekken

De chat van een to-do vertelt nog steeds zijn eigen verhaal; Activiteit linkt ernaar. Fleet, **Activiteit** toont dezelfde regels voor je Fleets en inzichten, met **Intrekken** voor een inzicht. In Instellingen, **Beveiliging** opent **Bekijk elke blik in Activiteit** wat ons team bekeek.

Activiteit toont alleen wat er gebeurde. Het verandert nooit wat The Machine mag.
