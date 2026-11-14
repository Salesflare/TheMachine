---
title: Weekoverzicht
area: weekly
summary: Eén keer per week hoe je Machine het deed: to-do's, beloftes, personen en projecten, en wat hij opmerkte. Standaard aan.
covers: weekly-recap
code: assistant.py, machine/app/recap_settings.py, config.example.json
order: 1
translated: 936df3d624aba2d7
---
## Wat erin staat

- Je week met The Machine, en hoeveel to-do's de moeite waard waren, vergeleken met de week ervoor.
- To-do's: nieuw, gedaan, genegeerd en gesnoozed, en hoe snel je antwoordde.
- Beloftes: die van jou die nagekomen of nog open zijn, die van anderen die nagekomen zijn of nog wachten.
- Inzichten om te delen met het team van The Machine, als er op je wachten. Zie [Inzichten delen met het team](share-learnings.md).
- Personen en projecten, zoals wie stil is gevallen.
- Wat me opviel: concepten die verstuurd zijn zoals ze geschreven waren of na bewerking, to-do's die binnen enkele minuten genegeerd zijn, to-do's die meer dan eens gesnoozed zijn.
- Achter de schermen: hoeveel signalen hij deze week gecheckt heeft, en hoeveel er nog wachten.
- Keuzes, elk in een eigen bericht na het overzicht: een drukke bron zonder resultaat (**Niet meer checken** of **Blijven checken**) en een to-do die meer dan eens gesnoozed is (**Niet nodig**, **Doe het** of **Houden**). Er verandert niets tot je tikt.

## Wanneer en waar

Eén keer per week, standaard op vrijdag na 16:00 in je tijdzone. Het komt op [Telegram](telegram.md), of als melding met de titel "Je week" van de [telefoonapp](phone-app.md) en de dashboard-app. Het komt ook per e-mail als e-mail aanstaat voor **Ochtendoverzicht** in Instellingen › Meldingen. Met [Voorzichtig](security-levels.md) komt het niet per e-mail.

## Uitzetten

Het staat standaard aan. Zet het uit in Instellingen › Meldingen met de schakelaar **Weekoverzicht**. Zette je het uit, dan blijft het uit. Op je eigen computer kun je ook `weekly_recap` in de config.json instellen: `enabled` false met `chosen` true, en eventueel `weekday` (1 tot 7, vrijdag is 5) en `at` ("16:00"). Zie de [configuratiegids](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).
