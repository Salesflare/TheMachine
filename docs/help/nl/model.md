---
title: Model
area: settings
summary: Welk AI-model je antwoorden geeft, hoe grondig het nadenkt en hoeveel van de limieten van je abonnement het heeft verbruikt.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: ee95ad4fa5323e3a
---
**Instellingen**, **Model** toont welk AI-model je **Achtergrondwerk** uitvoert en hoe je bent aangemeld, bijvoorbeeld met ChatGPT.

Op een gehoste Machine is het hoofdmodel bij een ChatGPT-aanmelding GPT-6.2 Sol: het geeft sneller antwoord dan GPT-6.1 Sol voor dezelfde prijs.

Een persoonlijk ChatGPT- of Claude-abonnement kan standaard je chats gebruiken om te trainen. Met **Training met je gegevens uitschakelen** open je die instelling bij de aanbieder. **Gedaan** verbergt de regel.

## Model en denkwerk voor chats

Kies onder **Chats** het model en het denkwerkniveau voor je to-do-chats en Hulp. Je ziet alleen de modellen en niveaus die beschikbaar zijn met je aanmelding.

Meer denkwerk levert betere antwoorden op moeilijke vragen op, maar duurt langer en verbruikt meer van je abonnement. **Ultra denkwerk** schakelt helpers in voor de moeilijkste vragen en verbruikt het meest. Een nieuwe Machine begint met **Weinig denkwerk**: goede resultaten voor veel minder van je abonnement. Een wijziging geldt vanaf je volgende bericht.

Wil je dit alleen voor één chat wijzigen, tik dan onder het berichtvak op het model of denkwerkniveau. Kies opnieuw de optie Instellingen om de instellingen te volgen.

Controles, je profiel en concepten die vooraf zijn klaargezet, gebruiken hun eigen model.

## Limieten

Als je abonnement gebruikslimieten heeft, zoals de limieten van 5 uur en per week bij een ChatGPT- of Claude-abonnement, zie je hoeveel ervan is verbruikt en wanneer ze worden gereset. Alleen bekijken telt nooit mee voor je limieten.

## Ruimte voor je eigen chats

Achtergrondwerk laat ruimte over voor je eigen chats. Het pauzeert bij ongeveer 65% van de 5-uurslimiet. Controles van nieuwe berichten gaan door tot ongeveer 90% van de wekelijkse limiet. Ander werk gebruikt per dag ongeveer een zevende van de wekelijkse limiet. Een aanmelding zonder limieten, zoals een API-sleutel, pauzeert nooit.

Achtergrondwerk draait nooit op GPT-6 Astra. Met een ChatGPT-aanmelding gebruikt het voorlopig GPT-6.1 Sol, ook als je hoofdmodel GPT-6.2 Sol is. Op die aanmelding gebruikt 6.2 de gecachte instructies nog niet opnieuw, waardoor het meer van je abonnement verbruikt. Je chats blijven het model gebruiken dat je hebt gekozen.

Voor een controle filtert een klein model (GPT-6 Luna met ChatGPT, Haiku met Claude) nieuwsbrieven, reclame en appmeldingen eruit die duidelijk geen aandacht nodig hebben. Zo verbruiken controles minder van je abonnement. De berichten blijven doorzoekbaar. Berichten van mensen, facturen, beveiligingsmeldingen en aanmeldcodes worden altijd gecontroleerd.

## Voordat een limiet is bereikt

Als je ChatGPT-abonnement nog resets heeft, verschijnt er bij To-do's een korte melding zodra achtergrondwerk wordt afgeremd: bij ongeveer 65% van de 5-uurslimiet of 90% van de wekelijkse limiet. De melding laat zien hoeveel is verbruikt en hoeveel resets je nog hebt. Met **Een reset gebruiken** zet je de limieten terug op nul, nadat je dit hebt bevestigd. Met × verberg je de melding tot die limiet wordt gereset. Zonder resets verschijnt er niets nieuws.

Op een gehoste Machine ziet en gebruikt je Machine resets zodra Codex op je Machine is aangemeld bij hetzelfde ChatGPT-account. Tot die tijd tonen To-do's en Instellingen **Resets inschakelen**. Daarmee open je de Codex-stap op je instelpagina, waar je je aanmeldt met een code, net als bij je ChatGPT-aanmelding.

## Wanneer een limiet is bereikt

Bovenaan het dashboard staat welke limiet is bereikt en wanneer die wordt gereset. Het werk wacht en gaat daarna verder waar het was gebleven. Er gaat niets verloren. Als je ChatGPT-abonnement resets heeft, zet **Een reset gebruiken** de limieten terug op nul. Op een gehoste Machine zonder aangemelde Codex opent **Resets inschakelen** in plaats daarvan je instelpagina. Anders opent **Resets bekijken in ChatGPT** de pagina van ChatGPT.

## Met een uitwijkmodel

Als je Machine een uitwijkmodel heeft bij een ander abonnement of een andere aanbieder, neemt dat het over zodra een limiet is bereikt. Er hoeft dan niets te wachten. Bovenaan het dashboard staat: "ChatGPT-limiet bereikt, je uitwijkmodel wordt gebruikt." Als het uitwijkmodel niet meer werkt, worden de pauzes weer ingeschakeld.

## Het hoofdmodel wijzigen

Het hoofdmodel wordt gebruikt door de rest van The Machine. Wijzig het op een gehoste Machine op je instelpagina, onder Your AI. Bekijk op je eigen computer [ChatGPT](chatgpt.md), [Mistral](mistral.md) en de [handleiding voor modellen](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
