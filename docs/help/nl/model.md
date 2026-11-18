---
title: Model
area: settings
summary: Welk AI-model voor je antwoordt, hoeveel denkwerk het doet en hoeveel van de limieten van je abonnement het heeft gebruikt.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: 249d2d7d6c368cfe
---
**Instellingen**, **Model** laat zien welk AI-model je **Achtergrondwerk** uitvoert en hoe je bent aangemeld, bijvoorbeeld met ChatGPT.

Op een gehoste Machine met een ChatGPT-aanmelding is GPT-6.2 Sol het hoofdmodel: het antwoordt sneller dan GPT-6.1 Sol voor dezelfde prijs.

Een persoonlijk ChatGPT- of Claude-abonnement gebruikt je chats mogelijk standaard om te trainen. Met **Training met je gegevens uitschakelen** open je die instelling bij de aanbieder. **Gedaan** verbergt de regel.

## Model en denkwerk voor chats

Kies onder **Chats** het model en het denkwerkniveau voor je to-do-chats en Help. Je ziet alleen de modellen en niveaus die beschikbaar zijn met je aanmelding.

Met meer denkwerk beantwoordt het model moeilijke vragen beter, maar het antwoord duurt langer en gebruikt meer van je abonnement. **Ultra denkwerk** schakelt hulp in voor de moeilijkste vragen en gebruikt het meeste. Een nieuwe Machine begint met **Weinig denkwerk**: goede resultaten voor veel minder van je abonnement. Een wijziging geldt vanaf het volgende bericht.

Tik op het model of denkwerkniveau onder het berichtvak om dit voor één chat te wijzigen. Kies opnieuw **Instellingen** om de instelling te volgen.

Controles, je profiel en vooraf klaargezette concepten gebruiken hun eigen model.

## Limieten

Als je abonnement gebruikslimieten heeft, zoals de limieten van 5 uur en per week bij een ChatGPT- of Claude-abonnement, zie je hoeveel je hebt gebruikt en wanneer elke limiet wordt gereset. Alleen kijken verbruikt niets van je abonnement.

## Ruimte voor je eigen chats

Achtergrondwerk laat ruimte over voor je eigen chats. Het wordt gepauzeerd bij ongeveer 65% van de limiet van 5 uur. Controles van nieuwe berichten gaan door tot ongeveer 90% van de weeklimiet. Ander werk gebruikt ongeveer een zevende van de week per dag. Een aanmelding zonder limieten, zoals met een API-sleutel, wordt nooit gepauzeerd.

Achtergrondwerk draait nooit op GPT-6 Astra. In plaats daarvan gebruikt het GPT-6.2 Sol, of GPT-6.1 Sol als 6.2 niet is ingesteld.

## Als een limiet is bereikt

Bovenaan het dashboard staat welke limiet is bereikt en wanneer die wordt gereset. Het werk wacht en gaat daarna verder waar het gebleven was. Er gaat niets verloren. Als je ChatGPT-abonnement resets heeft, start **Een reset gebruiken** de limieten opnieuw. Anders opent **Resets bekijken in ChatGPT** de pagina van ChatGPT.

## Met een terugvalmodel

Als je Machine een terugvalmodel heeft bij een ander abonnement of een andere aanbieder, neemt dat het over zodra een limiet is bereikt en hoeft er niets te wachten. Bovenaan het dashboard staat: "ChatGPT-limiet bereikt, je terugvalmodel wordt gebruikt." Als het terugvalmodel niet meer werkt, worden de pauzes hervat.

## Het hoofdmodel wijzigen

Het hoofdmodel wordt gebruikt voor de rest van The Machine. Wijzig het op een gehoste Machine op je instellingenpagina, onder Je AI. Bekijk op je eigen computer de handleidingen voor [ChatGPT](chatgpt.md), [Mistral](mistral.md) en [modellen](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
