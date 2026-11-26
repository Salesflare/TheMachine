---
title: Model
area: settings
summary: Welk AI-model antwoordt, hoeveel denkwerk het gebruikt en hoeveel van de limieten van je abonnement al zijn verbruikt.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: f34db396a7290252
---
**Instellingen**, **Model** laat zien welk AI-model je **Achtergrondwerk** doet en hoe je bent ingelogd, bijvoorbeeld met ChatGPT.

Op een gehoste Machine is het hoofdmodel met een ChatGPT-login GPT-6.2 Sol: het geeft sneller antwoord dan GPT-6.1 Sol voor dezelfde prijs.

Een persoonlijk ChatGPT- of Claude-abonnement kan standaard je chats gebruiken om te trainen. **Training met je gegevens uitschakelen** opent die instelling bij de aanbieder. Met **Gedaan** verberg je de regel.

## Model en denkwerk voor chats

Kies onder **Chats** het model en het denkwerkniveau voor je to-do-chats en Hulp. Je ziet alleen de modellen en niveaus die je login aanbiedt.

Meer denkwerk levert betere antwoorden op moeilijke vragen op, maar duurt langer en verbruikt meer van je abonnement. **Ultra denkwerk** schakelt hulp in voor de moeilijkste vragen en verbruikt het meest. Een nieuwe Machine begint op **Weinig denkwerk**: goede resultaten voor veel minder verbruik van je abonnement. Een wijziging geldt vanaf het volgende bericht.

Als je dit alleen voor één chat wilt wijzigen, tik je onder het berichtvak op het model of het denkwerkniveau. Kies opnieuw de optie Instellingen om de instelling te volgen.

Checks, je profiel en concepten die vooraf zijn voorbereid, gebruiken hun eigen model.

## Limieten

Heeft je abonnement gebruikslimieten, zoals de limieten van 5 uur en per week van een ChatGPT- of Claude-abonnement, dan zie je hoeveel ervan is verbruikt en wanneer ze worden gereset. Alleen kijken verbruikt niets van je abonnement.

## Ruimte voor je eigen chats

Achtergrondwerk laat ruimte over voor je eigen chats. Het pauzeert bij ongeveer 65% van de limiet van 5 uur. Checks van nieuwe berichten gaan door tot ongeveer 90% van de weeklimiet. Ander werk gebruikt ongeveer een zevende van de week per dag. Een login zonder limieten, zoals een API-sleutel, pauzeert nooit.

Achtergrondwerk draait nooit op GPT-6 Astra. Met een ChatGPT-login en een OpenClaw-versie ouder dan 2026.11.10 gebruikt het GPT-6.1 Sol, ook als je hoofdmodel GPT-6.2 Sol is. Daar hergebruikt 6.2 zijn gecachete instructies niet, waardoor het meer van je abonnement verbruikt. Vanaf OpenClaw 2026.11.10 gebruikt achtergrondwerk weer je hoofdmodel. Voor je chats blijft het model staan dat je hebt gekozen.

Voordat een check begint, filtert een klein model (GPT-6 Luna met ChatGPT, Haiku met Claude) nieuwsbrieven, aanbiedingen en appmeldingen eruit die duidelijk geen aandacht nodig hebben. Zo verbruiken checks minder van je abonnement. Je kunt ze nog steeds doorzoeken. Berichten van personen, rekeningen, beveiligingswaarschuwingen en inlogcodes worden altijd gecontroleerd.

## Voordat een limiet is bereikt

Heeft je ChatGPT-abonnement nog resets over, dan toont To-do's een korte melding zodra achtergrondwerk trager wordt: bij ongeveer 65% van de limiet van 5 uur of 90% van de weeklimiet. De melding geeft aan hoeveel is verbruikt en hoeveel resets je nog hebt. Met **Een reset gebruiken** begin je opnieuw, nadat je dit hebt bevestigd. Met × verberg je de melding totdat die limiet wordt gereset. Zonder resets verschijnt er niets nieuws.

Op een gehoste Machine kan je Machine resets zien en gebruiken zodra Codex op je Machine is ingelogd bij hetzelfde ChatGPT-account. Tot die tijd tonen To-do's en Instellingen **Resets inschakelen**. Hiermee open je de Codex-stap van je installatiepagina. Daar log je in met een code, net als bij je ChatGPT-login.

## Wanneer een limiet is bereikt

Bovenaan het dashboard staat welke limiet is bereikt en wanneer die wordt gereset. Het werk wacht en gaat daarna verder waar het was gebleven. Er gaat niets verloren. Heeft je ChatGPT-abonnement resets, dan begin je met **Een reset gebruiken** opnieuw. Is Codex op een gehoste Machine niet ingelogd, dan opent **Resets inschakelen** je installatiepagina. Anders opent **Resets bekijken in ChatGPT** de pagina van ChatGPT.

## Met een terugvalmodel

Heeft je Machine een terugvalmodel bij een ander abonnement of een andere aanbieder, dan neemt dat het over zodra een limiet is bereikt en hoeft er niets te wachten. Bovenaan het dashboard staat: "ChatGPT-limiet bereikt, je terugvalmodel wordt gebruikt." Als het terugvalmodel niet meer werkt, worden de taken weer gepauzeerd.

## Het hoofdmodel wijzigen

Het hoofdmodel is het model dat de rest van The Machine gebruikt. Wijzig het op een gehoste Machine op je installatiepagina, onder Your AI. Bekijk voor je eigen computer [ChatGPT](chatgpt.md), [Mistral](mistral.md) en de [handleiding voor modellen](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
