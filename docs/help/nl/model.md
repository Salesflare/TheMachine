---
title: Model
area: settings
summary: Welk AI-model je antwoorden geeft, hoeveel denkwerk het doet en hoeveel van de limieten van je abonnement het heeft gebruikt.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: 9a0777c555ab5637
---
Bij **Instellingen** > **Model** zie je welk AI-model je **Achtergrondwerk** uitvoert en hoe je bent ingelogd, bijvoorbeeld met ChatGPT.

Op een gehoste Machine met een ChatGPT-login is GPT-6.2 Sol het hoofdmodel: het geeft sneller antwoord dan GPT-6.1 Sol voor dezelfde prijs.

Een Claude-login verloopt ongeveer vier weken nadat je bent ingelogd. **Wacht op jou** laat dat drie dagen van tevoren weten. Na afloop krijg je één melding. Met **Opnieuw inloggen** los je dit in één stap op.

Een persoonlijk ChatGPT- of Claude-abonnement kan je chats standaard gebruiken om te trainen. Met **Training met je gegevens uitschakelen** open je die instelling bij de aanbieder. Met **Gedaan** verberg je de melding.

## Model en denkwerk voor chats

Kies onder **Chats** het model en het niveau van het denkwerk voor je to-do-chats en Hulp. Je ziet alleen de modellen en niveaus die bij je login beschikbaar zijn.

Meer denkwerk levert betere antwoorden op lastige vragen op, maar duurt langer en gebruikt meer van je abonnement. **Ultra denkwerk** schakelt hulpmodellen in voor de lastigste vragen en verbruikt het meest. Een nieuwe Machine begint met **Weinig denkwerk**: goede resultaten voor een veel kleiner deel van je abonnement. Een wijziging geldt vanaf je volgende bericht.

Je kunt dit ook voor één chat wijzigen door onder het berichtvak op het model of het niveau van het denkwerk te tikken. Kies opnieuw de optie Instellingen om de instellingen te volgen.

Controles, je profiel en vooraf gemaakte concepten gebruiken hun eigen model.

## Limieten

Heeft je abonnement gebruikslimieten, zoals de limieten van ChatGPT of Claude voor vijf uur en een week? Dan zie je hoeveel je hebt gebruikt en wanneer elke limiet wordt gereset. Alleen kijken gebruikt niets van je abonnement.

## Ruimte voor je eigen chats

Achtergrondwerk laat ruimte over voor je eigen chats. Het wordt onderbroken bij ongeveer 65% van de limiet voor vijf uur. Controles op nieuwe berichten gaan door tot ongeveer 90% van de weeklimiet. Ander werk gebruikt ongeveer een zevende van de week per dag. Een login zonder limieten, zoals een API-sleutel, wordt nooit onderbroken.

Achtergrondwerk wordt nooit uitgevoerd op GPT-6 Astra. Als je bent ingelogd met ChatGPT en OpenClaw ouder is dan 2026.11.10, gebruikt het GPT-6.1 Sol, ook als GPT-6.2 Sol je hoofdmodel is. GPT-6.2 hergebruikt daar de gecachte instructies niet, waardoor het meer van je abonnement verbruikt. Vanaf OpenClaw 2026.11.10 gebruikt achtergrondwerk weer je hoofdmodel. Je chats blijven het model gebruiken dat je hebt gekozen.

Voor een controle haalt een klein model (GPT-6 Luna met ChatGPT, Haiku met Claude) eerst nieuwsbrieven, aanbiedingen en appmeldingen eruit die duidelijk nergens voor nodig zijn. Zo verbruiken controles minder van je abonnement. Je kunt ze nog steeds doorzoeken. Berichten van mensen, rekeningen, beveiligingsmeldingen en inlogcodes worden altijd gecontroleerd.

## Voordat een limiet is bereikt

Als je ChatGPT-abonnement nog resets heeft, verschijnt bij To-do's een korte melding wanneer achtergrondwerk langzamer gaat: bij ongeveer 65% van de limiet voor vijf uur of 90% van de weeklimiet. Je ziet hoeveel je hebt gebruikt en hoeveel resets je nog hebt. Met **Een reset gebruiken** begin je opnieuw aan de limieten, nadat je dit hebt bevestigd. Met × verberg je de melding tot die limiet wordt gereset. Zonder resets verschijnt er geen melding.

Op een gehoste Machine kan je Machine resets zien en gebruiken zodra Codex op je Machine is ingelogd bij hetzelfde ChatGPT-account. Tot die tijd zie je bij To-do's en Instellingen **Resets inschakelen**. Hiermee open je de Codex-stap van je installatiepagina. Daar log je in met een code, net als bij je ChatGPT-login.

## Wanneer een limiet is bereikt

Bovenaan het dashboard staat welke limiet is bereikt en wanneer deze wordt gereset. Het werk wacht en gaat daarna verder waar het was gebleven. Er gaat niets verloren. Heeft je ChatGPT-abonnement resets, dan begint **Een reset gebruiken** opnieuw aan de limieten. Is Codex op een gehoste Machine niet ingelogd, dan opent **Resets inschakelen** je installatiepagina. Anders opent **Resets bekijken in ChatGPT** de pagina van ChatGPT.

## Met een terugvalmodel

Heeft je Machine een terugvalmodel bij een ander abonnement of een andere aanbieder, dan neemt dat het over zodra een limiet is bereikt. Er hoeft dan niets te wachten. Bovenaan het dashboard staat: "ChatGPT-limiet bereikt, je terugvalmodel wordt gebruikt." Als het terugvalmodel niet meer werkt, worden taken weer onderbroken.

## Het hoofdmodel wijzigen

Het hoofdmodel wordt voor de rest van The Machine gebruikt. Wijzig het op een gehoste Machine op je installatiepagina, onder Your AI. Bekijk op je eigen computer [ChatGPT](chatgpt.md), [Mistral](mistral.md) en de [handleiding voor modellen](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
