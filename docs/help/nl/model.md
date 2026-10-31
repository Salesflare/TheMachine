---
title: Model
area: settings
summary: Welk AI-model voor je antwoordt, hoe hard het nadenkt, en hoeveel van de limieten van je abonnement het al gebruikt heeft.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
---
In **Instellingen** toont **Model** het model dat achtergrondwerk gebruikt (gemarkeerd als **Achtergrondwerk**) en hoe je bent ingelogd, bijvoorbeeld met ChatGPT.

## Model en denkwerk voor chats

Kies onder **Chats** het model en het denkniveau dat je to-do-chats en Help gebruiken. De lijst heeft alleen de modellen die je login aanbiedt, zoals die van ChatGPT als je met ChatGPT inlogde, en elk model alleen de niveaus die het heeft.

Meer denkwerk beantwoordt moeilijkere vragen beter, maar is trager en gebruikt meer van je abonnement. **Ultra denkwerk** haalt helpers erbij voor de moeilijkste vragen: het traagst, en het gebruikt het meest. Een wijziging geldt vanaf het volgende bericht. Een nieuwe Machine start met **Weinig denkwerk** als het model dat heeft: goede resultaten voor veel minder van je abonnement.

Eén chat kan iets anders gebruiken: tik onder het berichtvak op het model of het denkniveau. Die keuze geldt alleen voor die chat. Kies weer hetzelfde als in Instellingen om Instellingen te volgen.

Reviews, je profiel en vooraf voorbereide concepten houden hun eigen model.

## Limieten

Heeft je abonnement gebruikslimieten, dan zie je hoeveel van elke limiet gebruikt is en wanneer die weer vrijkomt, bijvoorbeeld de 5-uurslimiet en de weeklimiet van een abonnement op ChatGPT of Claude. Dit lezen gebruikt nooit iets van je abonnement.

## Ruimte voor je eigen chats

Werk op de achtergrond (reviews, je profiel, concepten die vooraf klaargezet worden) laat ruimte voor je eigen chats. Het pauzeert bij ongeveer 65% van de 5-uurslimiet. Reviews van wat binnenkwam gaan door tot ongeveer 90% van de weeklimiet; de rest verdeelt die over ongeveer een zevende per dag. Een login zonder gebruikslimieten, zoals een API-sleutel, wordt nooit gepauzeerd.

Werk op de achtergrond draait nooit op GPT-6 Astra. Het gebruikt in plaats daarvan GPT-6.1 Sol.

## Als een limiet bereikt is

Bovenaan het dashboard staat welke limiet bereikt is en wanneer die weer vrijkomt. Het werk wacht en gaat daarna verder waar het gebleven was. Er gaat niets verloren. Sommige ChatGPT-abonnementen hebben resets: **Een reset gebruiken** zet de limieten opnieuw op nul, na een bevestiging. Anders opent **Resets bekijken in ChatGPT** de eigen pagina van ChatGPT.

## Met een reservemodel

Heeft je Machine een reservemodel op een ander abonnement of bij een andere aanbieder, zoals een API-sleutel, dan neemt dat het over als een limiet bereikt is. Zolang het reservemodel werkt, pauzeert of wacht er niets voor je limieten, en bovenaan het dashboard staat "ChatGPT-limiet bereikt, je reservemodel neemt het over." Werkt het niet meer, dan komen de pauzes terug.

## Het hoofdmodel wijzigen

Het hoofdmodel is wat de rest van The Machine gebruikt. Kies op een gehoste Machine een ander model op je setuppagina, onder Je model. Wijzig het op je eigen computer in OpenClaw. Zie [ChatGPT](chatgpt.md) en de [gids over modellen](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
