---
title: Model
area: settings
summary: Welk AI-model je antwoorden geeft, hoeveel denkwerk het doet en hoeveel van de limieten van je abonnement het heeft verbruikt.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: eee77413a4bdbf0b
---
**Instellingen**, **Model** laat zien welk AI-model je **Achtergrondwerk** uitvoert en hoe je bent ingelogd, bijvoorbeeld met ChatGPT.

## Model en denkwerk voor chats

Kies onder **Chats** het model en het denkwerkniveau voor je chats over to-do's en Help. Je ziet alleen de modellen en niveaus die beschikbaar zijn met de manier waarop je bent ingelogd.

Met meer denkwerk beantwoordt het model moeilijke vragen beter, maar het is langzamer en verbruikt meer van je abonnement. **Ultra denkwerk** schakelt hulp in voor de moeilijkste vragen en verbruikt het meest. Een nieuwe Machine begint met **Weinig denkwerk**: goede resultaten die veel minder van je abonnement verbruiken. Een wijziging geldt vanaf je volgende bericht.

Als je dit maar voor één chat wilt wijzigen, tik je onder het berichtvak op het model of het denkwerkniveau. Kies opnieuw **Instellingen** om de instelling uit Instellingen te gebruiken.

Checks, je profiel en concepten die vooraf zijn klaargezet, gebruiken hun eigen model.

## Limieten

Als je abonnement gebruikslimieten heeft, zoals de limieten van 5 uur en per week van een ChatGPT- of Claude-abonnement, zie je hoeveel je hebt verbruikt en wanneer elke limiet opnieuw wordt ingesteld. Alleen kijken verbruikt niets van je abonnement.

## Ruimte voor je eigen chats

Achtergrondwerk laat ruimte over voor je eigen chats. Het wordt gepauzeerd bij ongeveer 65% van de limiet van 5 uur. Checks van nieuwe berichten gaan door tot ongeveer 90% van de weeklimiet. Ander werk gebruikt ongeveer een zevende van de week per dag. Inloggen zonder limieten, bijvoorbeeld met een API-sleutel, leidt nooit tot pauzes.

Achtergrondwerk draait nooit op GPT-6 Astra. In plaats daarvan gebruikt het GPT-6.1 Sol.

## Wanneer een limiet is bereikt

Bovenaan het dashboard staat welke limiet is bereikt en wanneer die opnieuw wordt ingesteld. Het werk wacht en gaat daarna verder waar het was gebleven. Er gaat niets verloren. Als je ChatGPT-abonnement resets heeft, start **Een reset gebruiken** de limieten opnieuw. Anders opent **Resets bekijken in ChatGPT** de pagina van ChatGPT.

## Met een terugvalmodel

Als je Machine een terugvalmodel heeft bij een ander abonnement of een andere provider, neemt dat het over zodra een limiet is bereikt. Er hoeft dan niets te wachten. Bovenaan het dashboard staat: "ChatGPT-limiet bereikt, je terugvalmodel wordt gebruikt." Als het terugvalmodel niet meer werkt, worden de pauzes weer ingeschakeld.

## Het hoofdmodel wijzigen

Het hoofdmodel is het model dat de rest van The Machine gebruikt. Wijzig het op een gehoste Machine op je instelpagina, onder Je AI. Gebruik je je eigen computer, bekijk dan [ChatGPT](chatgpt.md), [Mistral](mistral.md) en de [handleiding voor modellen](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
