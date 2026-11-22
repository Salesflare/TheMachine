---
title: Model
area: settings
summary: Welk AI-model je antwoorden geeft, hoeveel denkwerk het doet en hoeveel van je abonnementslimieten het heeft verbruikt.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: a6db52984a6fddeb
---
In **Instellingen** zie je onder **Model** welk AI-model je **Achtergrondwerk** doet en hoe je bent ingelogd, bijvoorbeeld met ChatGPT.

Op een gehoste Machine is het hoofdmodel GPT-6.2 Sol als je met ChatGPT bent ingelogd. Het geeft sneller antwoord dan GPT-6.1 Sol voor dezelfde prijs.

Een persoonlijk ChatGPT- of Claude-abonnement kan je chats standaard gebruiken om modellen te trainen. Met **Training met je gegevens uitschakelen** open je die instelling bij de aanbieder. Met **Gedaan** verberg je de regel.

## Model en denkwerk voor chats

Kies onder **Chats** het model en het niveau van het denkwerk voor je to-do-chats en Hulp. Je ziet alleen de modellen en niveaus die beschikbaar zijn voor je inlogmethode.

Meer denkwerk levert betere antwoorden op moeilijke vragen op, maar duurt langer en verbruikt meer van je abonnement. **Ultra denkwerk** schakelt hulp in voor de moeilijkste vragen en verbruikt het meest. Een nieuwe Machine begint met **Weinig denkwerk**. Dat levert goede resultaten op en verbruikt veel minder van je abonnement. Een wijziging geldt vanaf je volgende bericht.

Wil je dit voor één chat wijzigen? Tik dan onder het berichtveld op het model of het niveau van het denkwerk. Kies opnieuw **Instellingen** om de instelling te volgen.

Controles, je profiel en concepten die vooraf zijn voorbereid, gebruiken hun eigen model.

## Limieten

Als je abonnement gebruikslimieten heeft, zoals de limieten van 5 uur en per week voor een ChatGPT- of Claude-abonnement, zie je hoeveel je hebt verbruikt en wanneer de limieten worden gereset. Alleen de limieten bekijken verbruikt niets van je abonnement.

## Ruimte voor je eigen chats

Achtergrondwerk laat ruimte over voor je eigen chats. Het pauzeert wanneer je ongeveer 65% van de limiet van 5 uur hebt verbruikt. Controles op nieuwe berichten gaan door tot je ongeveer 90% van de wekelijkse limiet hebt verbruikt. Ander werk gebruikt ongeveer een zevende van de wekelijkse limiet per dag. Inloggen zonder limieten, bijvoorbeeld met een API-sleutel, leidt nooit tot pauzes.

Achtergrondwerk wordt nooit uitgevoerd op GPT-6 Astra. Als je met ChatGPT bent ingelogd, gebruikt het voorlopig GPT-6.1 Sol, ook als GPT-6.2 Sol je hoofdmodel is. GPT-6.2 hergebruikt de gecachte instructies voor die inlogmethode nog niet, waardoor het meer van je abonnement verbruikt. Je chats blijven het model gebruiken dat je hebt gekozen.

## Als een limiet is bereikt

Bovenaan het dashboard staat welke limiet is bereikt en wanneer die wordt gereset. Het werk wacht en gaat daarna verder waar het was gebleven. Er gaat niets verloren. Als je ChatGPT-abonnement resets heeft, kun je met **Een reset gebruiken** de limieten opnieuw laten beginnen. Anders opent **Resets bekijken in ChatGPT** de pagina van ChatGPT.

## Met een fallbackmodel

Als je Machine een fallbackmodel op een ander abonnement of bij een andere aanbieder heeft, neemt dat het over zodra een limiet is bereikt. Er hoeft dan niets te wachten. Bovenaan het dashboard staat: ‘ChatGPT-limiet bereikt, fallbackmodel wordt gebruikt.’ Als het fallbackmodel niet meer werkt, worden de pauzes weer ingeschakeld.

## Het hoofdmodel wijzigen

Het hoofdmodel wordt gebruikt voor de rest van The Machine. Wijzig het op een gehoste Machine op je instelpagina, onder Je AI. Gebruik je je eigen computer? Bekijk dan [ChatGPT](chatgpt.md), [Mistral](mistral.md) en de [handleiding voor modellen](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
