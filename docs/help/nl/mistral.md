---
title: Mistral
area: connections
summary: Laat je Machine draaien op de modellen van Mistral, met een API-sleutel van Mistral. Le Chat Pro bevat API-tegoed.
covers: mistral
code: docs/models.md, dashboard/settings-models.js
site: Other AI services, Save key, Keys, Remove
translated: 5d782f28fb69efef
---
## Waarvoor het dient

Mistral is een Europese AI-aanbieder. Met een API-sleutel van Mistral leest en schrijft je Machine concepten met de modellen van Mistral. The Machine heeft geen eigen AI: de verzoeken gaan rechtstreeks naar Mistral, onder jouw account en hun voorwaarden.

## Een sleutel maken

Mistral heeft geen login voor andere apps, dus het werkt met een API-sleutel. Open in de [Mistral-console](https://console.mistral.ai/) API keys en maak er een. Le Chat Pro bevat elke maand API-tegoed; daarna rekent Mistral per gebruik af.

## Koppelen

Open op een gehoste Machine je setuppagina, ga naar Je AI en open **Andere AI-diensten**. Kies Mistral als provider, plak de sleutel en druk op **Sleutel opslaan**. Je Machine probeert de sleutel eerst met één piepklein verzoek. Klopt de sleutel niet, dan zie je dat meteen, en wordt er niets bewaard.

Mistral Large wordt het hoofdmodel. Mistral Small staat er ook, als goedkopere keuze voor chats of als terugvaloptie.

Op je eigen computer: zie de [modellengids](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).

## Gebruik

**Instellingen**, **Model** zegt "Gebruikt je Mistral-API-sleutel". Een API-sleutel heeft geen gebruikslimieten, dus achtergrondwerk pauzeert er nooit voor. Zie [Model](model.md).

## Verwijderen

Druk op je setuppagina, onder Je AI, op **Verwijderen** naast Mistral in **Sleutels**. De sleutel verdwijnt van je Machine, en als Mistral je hoofdmodel was, neemt een ander verbonden model het over. Om de sleutel zelf te schrappen, verwijder je hem in de Mistral-console.
