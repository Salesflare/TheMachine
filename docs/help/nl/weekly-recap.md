---
title: Weekoverzicht
area: weekly
summary: Een wekelijks overzicht van hoe je Machine het deed: to-do's, beloftes, mensen en projecten, en wat hij heeft opgemerkt. Staat standaard aan.
covers: weekly-recap
code: assistant.py, machine/app/recap_settings.py, config.example.json
order: 1
translated: 223b143a6efd5692
---
## Wat erin staat

- Heeft je aandacht nodig: te late beloftes aan jou en je eigen beloftes die te laat zijn of waarvan de deadline in de komende twee weken valt.
- Volgende week: je meetings (met een link zodra de voorbereiding klaarstaat), to-do's met een naderende deadline en beloftes die anderen voor die week hebben gedaan.
- Wat er is veranderd: hoeveel to-do's de moeite waard waren vergeleken met de week ervoor, hoe vaak **Doe het** meteen de juiste keuze was, wat hij heeft aangepast aan je schrijfstijl en zijn filters, en hoeveel concepten ongewijzigd zijn verstuurd.
- Voor het team van The Machine: inzichten om te delen, als er iets voor je klaarstaat. Bekijk [Inzichten delen met het team](share-learnings.md).
- Mensen en projecten: projecten die aan kracht winnen of juist afkoelen, wie nieuw is en wie stil is geworden.
- Achter de schermen: hoeveel signalen hij deze week heeft gecontroleerd en hoeveel er nog wachten.
- Op [Telegram](telegram.md) volgen keuzes, elk in een eigen bericht: een drukke bron zonder resultaten (**Niet meer checken** of **Blijven checken**) en een to-do die meer dan eens is gesnoozed (**Niet nodig**, **Doe het** of **Houden**). Er verandert niets tot je tikt.

## Wanneer en waar

Standaard één keer per week, op vrijdag na 16:00 in je tijdzone. Je ontvangt het op [Telegram](telegram.md), of als melding met de titel "Je week" in de [telefoonapp](phone-app.md) en de dashboardapp. Je ontvangt het ook per e-mail als e-mail is ingeschakeld voor **Ochtendoverzicht** in Instellingen › Meldingen. Met [Voorzichtig](security-levels.md), of als **Tekst in meldingen** is uitgeschakeld, ontvang je het niet per e-mail.

## Uitzetten

Staat standaard aan. Zet het uit via Instellingen › Meldingen met de schakelaar **Weekoverzicht**. Als je het hebt uitgezet, blijft het uit. Op je eigen computer kun je ook `weekly_recap` instellen in config.json: `enabled` false met `chosen` true, en optioneel `weekday` (1 tot 7, vrijdag is 5) en `at` ("16:00"). Bekijk de [configuratiehandleiding](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).
