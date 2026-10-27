---
title: Weekoverzicht
area: weekly
summary: Eén keer per week hoe je Machine het deed: to-do's, beloftes, personen en projecten, en wat hij opmerkte. Standaard uit.
covers: weekly-recap
code: assistant.py, config.example.json
order: 1
---
## Wat erin staat

- Je week met The Machine, en hoeveel to-do's de moeite waard waren, vergeleken met de week ervoor.
- To-do's: nieuw, gedaan, genegeerd en gesnoozed, en hoe snel je antwoordde.
- Beloftes: die van jou die nagekomen of nog open zijn, die van anderen die nagekomen zijn of nog wachten.
- Inzichten om te delen met het team van The Machine, als er op je wachten. Zie [Inzichten delen met het team](share-learnings.md).
- Personen en projecten, zoals wie stil is gevallen.
- Wat me opviel: concepten die verstuurd zijn zoals ze geschreven waren of na bewerking, to-do's die binnen enkele minuten genegeerd zijn, to-do's die meer dan eens gesnoozed zijn.
- Achter de schermen: wat hij bekeken heeft, en wat dat kostte.

## Wanneer en waar

Eén keer per week, standaard op vrijdag na 16:00 in je tijdzone. Het komt op [Telegram](telegram.md), of als melding met de titel "Je week" van de [telefoonapp](phone-app.md).

## Aanzetten

Het staat standaard uit, en het dashboard heeft er nog geen schakelaar voor, dus een gehoste Machine kan het vandaag niet aanzetten. Stel op je eigen computer `weekly_recap` in de config.json van je Machine in: `enabled` true, en eventueel `weekday` (1 tot 7, vrijdag is 5) en `at` ("16:00"). Zie de [configuratiegids](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).
