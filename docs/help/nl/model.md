---
title: Model
area: settings
summary: Welk AI-model voor je antwoordt, hoeveel denkwerk het doet en hoeveel van de limieten van je abonnement al is verbruikt.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: b76f4f927bfd7be1
---
**Instellingen**, **Model** laat zien welk AI-model je **Achtergrondwerk** uitvoert en hoe je bent ingelogd, bijvoorbeeld met ChatGPT.

Op een gehoste Machine is GPT-6.2 Sol het hoofdmodel als je bent ingelogd met ChatGPT. Het geeft sneller antwoord dan GPT-6.1 Sol voor dezelfde prijs.

Op een gehoste Machine blijft een Claude-login ongeveer een jaar geldig. Met `claude auth login` verloopt die ongeveer vier weken nadat je bent ingelogd. Drie dagen van tevoren meldt **Wacht op jou** dit en ontvang je één e-mail. Zodra de login is verlopen, ontvang je één melding en alsnog die e-mail als die nog niet was verstuurd. Met **Opnieuw inloggen** los je dit in één stap op.

Een persoonlijk ChatGPT- of Claude-abonnement kan je chats standaard gebruiken om modellen te trainen. Met **Training met je gegevens uitschakelen** open je de betreffende instelling bij de aanbieder. Met **Gedaan** verberg je de melding.

## Model en denkwerk voor chats

Kies onder **Chats** het model en niveau van denkwerk voor je to-do-chats en Hulp. Je ziet alleen de modellen en niveaus die beschikbaar zijn met je login.

Met meer denkwerk beantwoordt het model moeilijke vragen beter, maar het is trager en verbruikt meer van je abonnement. **Ultra denkwerk** schakelt hulpen in voor de moeilijkste vragen en verbruikt het meest. Een nieuwe Machine begint met **Weinig denkwerk**: goede resultaten voor veel minder van je abonnement. Een wijziging geldt vanaf je volgende bericht.

Tik op het model of niveau van denkwerk onder het berichtvak om dit voor één chat te wijzigen. Kies opnieuw de optie Instellingen om de instellingen te volgen.

Checks, je profiel en concepten die vooraf zijn klaargezet, gebruiken hun eigen model.

## Limieten

Als je abonnement gebruikslimieten heeft, zoals de limieten van 5 uur en per week bij een ChatGPT- of Claude-abonnement, zie je hoeveel je hebt verbruikt en wanneer elke limiet wordt gereset. Alleen kijken verbruikt niets van je abonnement.

## Ruimte voor je eigen chats

Achtergrondwerk laat ruimte over voor je eigen chats. Het wordt gepauzeerd bij ongeveer 65% van de limiet van 5 uur. Checks van nieuwe berichten gaan door tot ongeveer 90% van de weeklimiet. Ander werk gebruikt ongeveer een zevende van de week per dag. Een login zonder limieten, zoals een API-sleutel, wordt nooit gepauzeerd.

Achtergrondwerk draait nooit op GPT-6 Astra. Als je bent ingelogd met ChatGPT en OpenClaw ouder is dan 2026.11.10, gebruikt het GPT-6.1 Sol, ook als GPT-6.2 Sol je hoofdmodel is. GPT-6.2 hergebruikt daar de gecachete instructies niet, waardoor het meer van je abonnement verbruikt. Vanaf OpenClaw 2026.11.10 gebruikt achtergrondwerk weer je hoofdmodel. Je chats blijven het model gebruiken dat je hebt gekozen.

Voordat een check begint, filtert een klein model (GPT-6 Luna met ChatGPT, Haiku met Claude) nieuwsbrieven, promoties en meldingen van apps eruit die duidelijk geen aandacht nodig hebben. Zo verbruiken checks minder van je abonnement. Je kunt deze berichten nog steeds doorzoeken. Berichten van mensen, facturen, beveiligingsmeldingen en inlogcodes worden altijd gecontroleerd.

## Voordat een limiet is bereikt

Als je ChatGPT-abonnement nog resets heeft, toont To-do's een korte melding zodra achtergrondwerk trager wordt: bij ongeveer 65% van de limiet van 5 uur of 90% van de weeklimiet. Je ziet hoeveel je hebt verbruikt en hoeveel resets je nog hebt. Met **Een reset gebruiken** begin je opnieuw, nadat je dit hebt bevestigd. Met × verberg je de melding totdat die limiet wordt gereset. Zonder resets verschijnt er niets nieuws.

Op een gehoste Machine kan je Machine resets zien en gebruiken zodra Codex op je Machine is ingelogd met hetzelfde ChatGPT-account. Tot die tijd tonen To-do's en Instellingen **Resets inschakelen**. Hiermee open je de Codex-stap van je installatiepagina. Daar log je in met een code, net als bij je ChatGPT-login.

## Wanneer een limiet is bereikt

Bovenaan het dashboard staat welke limiet is bereikt en wanneer die wordt gereset. Het werk wacht en gaat daarna verder waar het was gebleven. Er gaat niets verloren. Als je ChatGPT-abonnement resets heeft, begint **Een reset gebruiken** de limieten opnieuw. Op een gehoste Machine waarop Codex niet is ingelogd, opent **Resets inschakelen** in plaats daarvan je installatiepagina. Anders opent **Resets bekijken in ChatGPT** de pagina van ChatGPT.

## Met een terugvalmodel

Als je Machine een terugvalmodel heeft bij een ander abonnement of een andere aanbieder, neemt dat het over zodra een limiet is bereikt. Er hoeft dan niets te wachten. Bovenaan het dashboard staat: "ChatGPT-limiet bereikt, je terugvalmodel wordt gebruikt." Als het terugvalmodel niet meer werkt, worden de pauzes weer ingeschakeld.

## Het hoofdmodel wijzigen

Het hoofdmodel is het model dat de rest van The Machine gebruikt. Wijzig het op een gehoste Machine op je installatiepagina, onder Je AI. Lees op je eigen computer [ChatGPT](chatgpt.md), [Mistral](mistral.md) en de [handleiding voor modellen](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
