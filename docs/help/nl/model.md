---
title: Model
area: settings
summary: Welk AI-model je antwoorden geeft, hoeveel denkwerk het doet en hoeveel van de limieten van je abonnement het heeft verbruikt.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: c7a96914e4deb3d4
---
In **Instellingen** zie je bij **Model** welk AI-model je **Achtergrondwerk** uitvoert en hoe je bent aangemeld, bijvoorbeeld met ChatGPT.

Een persoonlijk abonnement op ChatGPT of Claude kan je chats standaard gebruiken om modellen te trainen. Met **Training met je gegevens uitschakelen** open je die instelling bij de aanbieder. Met **Gedaan** verberg je de melding.

## Model en denkwerk voor chats

Kies onder **Chats** het model en het niveau van het denkwerk voor je to-do-chats en Hulp. Je ziet alleen de modellen en niveaus die beschikbaar zijn met jouw aanmelding.

Meer denkwerk levert betere antwoorden op moeilijke vragen op, maar duurt langer en verbruikt meer van je abonnement. **Ultra denkwerk** schakelt hulpmodellen in voor de moeilijkste vragen en verbruikt het meest. Een nieuwe Machine begint met **Weinig denkwerk**: goede resultaten voor veel minder van je abonnement. Een wijziging geldt vanaf je volgende bericht.

Wil je dit voor één chat wijzigen? Tik dan op het model of het niveau van het denkwerk onder het berichtveld. Kies opnieuw de optie **Instellingen** om de instellingen te volgen.

Controles, je profiel en vooraf gemaakte concepten gebruiken hun eigen model.

## Limieten

Als je abonnement gebruikslimieten heeft, zoals de limieten van 5 uur en per week bij een ChatGPT- of Claude-abonnement, zie je hoeveel je hebt verbruikt en wanneer elke limiet wordt gereset. Alleen kijken verbruikt niets van je abonnement.

## Ruimte voor je eigen chats

Achtergrondwerk laat ruimte over voor je eigen chats. Het wordt gepauzeerd wanneer ongeveer 65% van de limiet van 5 uur is bereikt. Controles van nieuwe berichten gaan door tot ongeveer 90% van de weeklimiet. Ander werk verbruikt ongeveer een zevende van de weeklimiet per dag. Een aanmelding zonder limieten, zoals met een API-sleutel, wordt nooit gepauzeerd.

Achtergrondwerk gebruikt nooit GPT-6 Astra. In plaats daarvan gebruikt het GPT-6.2 Sol, of GPT-6.1 Sol als 6.2 niet is ingesteld.

## Wanneer een limiet is bereikt

Bovenaan het dashboard staat welke limiet is bereikt en wanneer die wordt gereset. Het werk wacht en gaat daarna verder waar het was gebleven. Er gaat niets verloren. Als je ChatGPT-abonnement resets heeft, kun je met **Een reset gebruiken** de limieten opnieuw laten beginnen. Anders opent **Resets bekijken in ChatGPT** de pagina van ChatGPT.

## Met een terugvalmodel

Als je Machine een terugvalmodel heeft bij een ander abonnement of een andere aanbieder, neemt dat het over zodra een limiet is bereikt. Er hoeft dan niets te wachten. Bovenaan het dashboard staat: "ChatGPT-limiet bereikt, je terugvalmodel wordt gebruikt." Als het terugvalmodel niet meer werkt, worden de pauzes hervat.

## Het hoofdmodel wijzigen

Het hoofdmodel wordt gebruikt voor de rest van The Machine. Wijzig het op een gehoste Machine op je installatiepagina, onder Your AI. Op je eigen computer vind je meer informatie bij [ChatGPT](chatgpt.md), [Mistral](mistral.md) en in de [handleiding voor modellen](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
