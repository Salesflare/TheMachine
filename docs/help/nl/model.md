---
title: Model
area: settings
summary: Welk AI-model voor je antwoordt, hoeveel denkwerk het levert en hoeveel van de limieten van je abonnement het heeft gebruikt.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: d63ec55d8d0339e6
---
In **Instellingen** zie je bij **Model** welk AI-model je **Achtergrondwerk** uitvoert en hoe je bent ingelogd, bijvoorbeeld met ChatGPT.

Op een gehoste Machine met een ChatGPT-login is GPT-6.2 Sol het hoofdmodel: het geeft sneller antwoord dan GPT-6.1 Sol voor dezelfde prijs.

Een persoonlijk ChatGPT- of Claude-abonnement kan je chats standaard gebruiken om modellen te trainen. Met **Training met je gegevens uitschakelen** open je die instelling bij de aanbieder. Met **Gedaan** verberg je de melding.

## Model en denkwerk voor chats

Kies onder **Chats** het model en het niveau van denkwerk voor je to-do-chats en Hulp. Je ziet alleen de modellen en niveaus die beschikbaar zijn met je login.

Meer denkwerk levert betere antwoorden op moeilijke vragen op, maar duurt langer en gebruikt meer van je abonnement. **Ultra denkwerk** schakelt hulpmodellen in voor de moeilijkste vragen en gebruikt het meest. Een nieuwe Machine begint met **Weinig denkwerk**: goede resultaten voor veel minder van je abonnement. Een wijziging geldt vanaf je volgende bericht.

Wil je dit alleen voor één chat wijzigen? Tik dan onder het berichtvak op het model of het niveau van denkwerk. Kies opnieuw de optie uit Instellingen om de instelling daar te volgen.

Controles, je profiel en concepten die vooraf zijn opgesteld gebruiken hun eigen model.

## Limieten

Als je abonnement gebruikslimieten heeft, zoals de limieten van 5 uur en per week van een ChatGPT- of Claude-abonnement, zie je hoeveel ervan is gebruikt en wanneer elke limiet wordt gereset. Alleen kijken gebruikt niets van je abonnement.

## Ruimte voor je eigen chats

Achtergrondwerk laat ruimte over voor je eigen chats. Het wordt onderbroken bij ongeveer 65% van de limiet van 5 uur. Controles van nieuwe berichten gaan door tot ongeveer 90% van de wekelijkse limiet. Ander werk gebruikt ongeveer een zevende van de week per dag. Een login zonder limieten, zoals een API-sleutel, wordt nooit onderbroken.

Achtergrondwerk draait nooit op GPT-6 Astra. Met een ChatGPT-login gebruikt het voorlopig GPT-6.1 Sol, ook als GPT-6.2 Sol je hoofdmodel is. Bij die login kan 6.2 de gecachte instructies nog niet opnieuw gebruiken, dus verbruikt het meer van je abonnement. Je chats blijven het model gebruiken dat je hebt gekozen.

## Voordat een limiet is bereikt

Als je ChatGPT-abonnement nog resets heeft, verschijnt er bij To-do's een korte melding zodra achtergrondwerk wordt afgeremd: bij ongeveer 65% van de limiet van 5 uur of 90% van de wekelijkse limiet. Je ziet hoeveel er is gebruikt en hoeveel resets je nog hebt. Met **Een reset gebruiken** worden de limieten opnieuw ingesteld nadat je dit bevestigt. Met × verberg je de melding totdat die limiet wordt gereset. Als je geen resets meer hebt, verschijnt er niets nieuws.

## Wanneer een limiet is bereikt

Bovenaan het dashboard zie je welke limiet is bereikt en wanneer die wordt gereset. Het werk wacht en gaat daarna verder waar het was gebleven. Er gaat niets verloren. Als je ChatGPT-abonnement resets heeft, worden de limieten met **Een reset gebruiken** opnieuw ingesteld. Anders opent **Resets bekijken in ChatGPT** de pagina van ChatGPT.

## Met een reservemodel

Als je Machine een reservemodel heeft bij een ander abonnement of een andere aanbieder, neemt dat het over zodra een limiet is bereikt. Er hoeft dan niets te wachten. Bovenaan het dashboard staat: "ChatGPT-limiet bereikt, je reservemodel wordt gebruikt." Als het reservemodel niet meer werkt, worden de onderbrekingen hervat.

## Het hoofdmodel wijzigen

Het hoofdmodel wordt gebruikt voor de rest van The Machine. Wijzig het op een gehoste Machine op je instellingenpagina, onder Your AI. Bekijk op je eigen computer de handleidingen voor [ChatGPT](chatgpt.md), [Mistral](mistral.md) en [modellen](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
