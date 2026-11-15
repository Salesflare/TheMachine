---
title: Model
area: settings
summary: Welk AI-model je antwoorden geeft, hoeveel denkwerk het doet en hoeveel van de limieten van je abonnement het heeft gebruikt.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: 744a27a77ab747ac
---
**Instellingen**, **Model** toont welk AI-model je **Achtergrondwerk** uitvoert en hoe je bent aangemeld, bijvoorbeeld met ChatGPT.

Een persoonlijk ChatGPT- of Claude-abonnement kan je chats standaard gebruiken om te trainen. **Training met je gegevens uitschakelen** opent die instelling bij de aanbieder en **Gedaan** verbergt de regel.

## Model en denkwerk voor chats

Kies onder **Chats** het model en het niveau van denkwerk voor je to-do-chats en Help. Je ziet alleen de modellen en niveaus die beschikbaar zijn met je aanmelding.

Meer denkwerk geeft betere antwoorden op lastige vragen, maar is trager en gebruikt meer van je abonnement. **Ultra denkwerk** schakelt helpers in voor de lastigste vragen en gebruikt het meest. Een nieuwe Machine begint met **Weinig denkwerk**: goede resultaten die veel minder van je abonnement gebruiken. Een wijziging geldt vanaf het volgende bericht.

Tik op het model of niveau van denkwerk onder het berichtvak om dit voor één chat te wijzigen. Kies opnieuw de optie voor Instellingen om de instellingen te volgen.

Controles, je profiel en vooraf gemaakte concepten gebruiken elk hun eigen model.

## Limieten

Als je abonnement gebruikslimieten heeft, zoals de limieten van 5 uur en per week bij een ChatGPT- of Claude-abonnement, zie je hoeveel je hebt gebruikt en wanneer elke limiet wordt gereset. Alleen kijken gebruikt niets van je abonnement.

## Ruimte voor je eigen chats

Achtergrondwerk laat ruimte over voor je eigen chats. Het wordt gepauzeerd bij ongeveer 65% van de limiet van 5 uur. Controles van nieuwe berichten gaan door tot ongeveer 90% van de weeklimiet. Ander werk gebruikt ongeveer een zevende van de weeklimiet per dag. Een aanmelding zonder limieten, zoals met een API-sleutel, wordt nooit gepauzeerd.

Achtergrondwerk draait nooit op GPT-6 Astra. In plaats daarvan gebruikt het GPT-6.1 Sol.

## Wanneer een limiet is bereikt

Bovenaan het dashboard staat welke limiet is bereikt en wanneer die wordt gereset. Werk wacht en gaat daarna verder waar het was gebleven. Er gaat niets verloren. Als je ChatGPT-abonnement resets heeft, begint **Een reset gebruiken** opnieuw met de limieten. Anders opent **Resets bekijken in ChatGPT** de pagina van ChatGPT.

## Met een fallback

Als je Machine een fallbackmodel heeft bij een ander abonnement of een andere aanbieder, neemt dat het over zodra een limiet is bereikt. Er hoeft dan niets te wachten. Bovenaan het dashboard staat: "ChatGPT-limiet bereikt, fallback wordt gebruikt." Als de fallback niet meer werkt, worden de pauzes weer ingeschakeld.

## Het hoofdmodel wijzigen

Het hoofdmodel wordt voor de rest van The Machine gebruikt. Wijzig het op een gehoste Machine op je instellingenpagina, onder Je AI. Bekijk op je eigen computer [ChatGPT](chatgpt.md), [Mistral](mistral.md) en de [gids voor modellen](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
