---
title: Model
area: settings
summary: Welk AI-model voor je antwoordt, hoeveel denkwerk het doet en hoeveel van de limieten van je abonnement het heeft gebruikt.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: ee95ad4fa5323e3a
---
**Instellingen**, **Model** laat zien welk AI-model je **Achtergrondwerk** uitvoert en hoe je bent ingelogd, bijvoorbeeld met ChatGPT.

Op een gehoste Machine met een ChatGPT-login is GPT-6.2 Sol het hoofdmodel: het antwoordt sneller dan GPT-6.1 Sol voor dezelfde prijs.

Een persoonlijk ChatGPT- of Claude-abonnement gebruikt je chats mogelijk standaard om te trainen. Met **Training met je gegevens uitschakelen** open je die instelling bij de aanbieder. **Gedaan** verbergt de regel.

## Model en denkwerk voor chats

Kies onder **Chats** het model en het denkwerkniveau voor je to-do-chats en Help. Je ziet alleen de modellen en niveaus die beschikbaar zijn met je login.

Met meer denkwerk beantwoordt het model moeilijke vragen beter, maar het antwoord duurt langer en gebruikt meer van je abonnement. **Ultra denkwerk** schakelt hulp in voor de moeilijkste vragen en gebruikt het meeste. Een nieuwe Machine begint met **Weinig denkwerk**: goede resultaten voor veel minder van je abonnement. Een wijziging geldt vanaf het volgende bericht.

Tik op het model of denkwerkniveau onder het berichtvak om dit voor één chat te wijzigen. Kies opnieuw wat in Instellingen staat om Instellingen weer te volgen.

Controles, je profiel en vooraf klaargezette concepten gebruiken hun eigen model.

## Limieten

Als je abonnement gebruikslimieten heeft, zoals de limieten van 5 uur en per week bij een ChatGPT- of Claude-abonnement, zie je hoeveel je hebt gebruikt en wanneer elke limiet wordt gereset. Alleen kijken verbruikt niets van je abonnement.

## Ruimte voor je eigen chats

Achtergrondwerk laat ruimte over voor je eigen chats. Het wordt gepauzeerd bij ongeveer 65% van de limiet van 5 uur. Controles van nieuwe berichten gaan door tot ongeveer 90% van de weeklimiet. Ander werk gebruikt ongeveer een zevende van de week per dag. Een login zonder limieten, zoals met een API-sleutel, wordt nooit gepauzeerd.

Achtergrondwerk draait nooit op GPT-6 Astra. Ben je met ChatGPT ingelogd, dan gebruikt het voorlopig GPT-6.1 Sol, ook als je hoofdmodel GPT-6.2 Sol is: met die login hergebruikt 6.2 zijn gecachte instructies nog niet en verbruikt het dus meer van je abonnement. Je chats houden het model dat je hebt gekozen.

Vóór een controle zet een klein model (GPT-6 Luna met ChatGPT, Haiku met Claude) nieuwsbrieven, promoties en appmeldingen die duidelijk niets nodig hebben opzij, zodat controles minder van je abonnement verbruiken. Ze blijven doorzoekbaar. Een bericht van een persoon, een factuur, een beveiligingsmelding of een inlogcode wordt altijd gecontroleerd.

## Voor een limiet is bereikt

Heeft je ChatGPT-abonnement nog resets, dan toont To-do's een korte regel zodra het achtergrondwerk vertraagt: bij ongeveer 65% van de limiet van 5 uur of 90% van de weeklimiet. Daarin staat hoeveel er verbruikt is en hoeveel resets je nog hebt. **Een reset gebruiken** start de limieten opnieuw, nadat je dat bevestigt. Met × verberg je de regel tot die limiet wordt gereset. Zonder resets verschijnt er niets nieuws.

Op een gehoste Machine ziet en gebruikt je Machine resets zodra Codex op je Machine is ingelogd op hetzelfde ChatGPT-account. Tot dan tonen To-do's en Instellingen **Resets inschakelen**. Dat opent de Codex-stap op je installatiepagina, waar je inlogt met een code, zoals bij je ChatGPT-login.

## Als een limiet is bereikt

Bovenaan het dashboard staat welke limiet is bereikt en wanneer die wordt gereset. Het werk wacht en gaat daarna verder waar het gebleven was. Er gaat niets verloren. Als je ChatGPT-abonnement resets heeft, start **Een reset gebruiken** de limieten opnieuw. Op een gehoste Machine zonder ingelogde Codex opent **Resets inschakelen** in plaats daarvan je installatiepagina. Anders opent **Resets bekijken in ChatGPT** de pagina van ChatGPT.

## Met een terugvalmodel

Als je Machine een terugvalmodel heeft bij een ander abonnement of een andere aanbieder, neemt dat het over zodra een limiet is bereikt en hoeft er niets te wachten. Bovenaan het dashboard staat: "ChatGPT-limiet bereikt, je terugvalmodel wordt gebruikt." Als het terugvalmodel niet meer werkt, worden de pauzes hervat.

## Het hoofdmodel wijzigen

Het hoofdmodel wordt gebruikt voor de rest van The Machine. Wijzig het op een gehoste Machine op je installatiepagina, onder Je AI. Bekijk op je eigen computer de handleidingen voor [ChatGPT](chatgpt.md), [Mistral](mistral.md) en [modellen](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
