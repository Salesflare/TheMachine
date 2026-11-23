---
title: Salesflare CRM
area: connections
summary: Accounts, contacten en deals, zodat hij weet wie belangrijk is. Hij leest ze met je API-sleutel.
covers: connector:salesflare
code: assistant.py, onboarding.py
site: More sources, Connect, Remove
translated: 8051c61777603a7e
---
## Wat hij leest

Je accounts, contacten en deals in Salesflare, plus de feed van elk account: e-mails van collega's waar je zelf niet bij stond en meetings met notities.

## Wat hij kan wijzigen

Niets. (Op je eigen computer kan de instelling `join_pipelines` ervoor zorgen dat hij je toevoegt aan accounts in geselecteerde pipelines. Standaard staat deze uit.)

## Koppelen

1. Open in Salesflare [Instellingen, API-sleutels](https://app.salesflare.com/#/settings/apikeys) en maak een sleutel aan.
2. Op een gehoste Machine: open je installatiepagina op app.themachine.computer/setup, ga naar **Meer bronnen**, open Salesflare CRM, plak de sleutel en klik op **Koppelen**.
3. In het dashboard: **Koppelingen**, **Klanten**, Salesflare CRM, plak de sleutel en klik op **Koppelen**. Op de kaart zie je vervolgens hoe ver de sync is.

## Syncgegevens

Onder **Koppelingen**, **Klanten** zie je bij Salesflare hoe ver de sync is: hoeveel accounts deze ronde zijn gecontroleerd, hoeveel er zijn overgeslagen omdat Salesflare te traag was en hoeveel accounts je API-sleutel niet kan openen (**geen toegang**). Als een ronde uren duurt, wordt aangegeven dat die mogelijk is vastgelopen.

De tegels tellen hoeveel accounts hij deze week heeft gelezen en hoeveel e-mails en meetings hij heeft opgehaald.

Een paar accounts zonder toegang hoef je niet op te lossen: de rest wordt gewoon opgehaald. Als je API-sleutel geen enkel account kan openen, staat op de kaart **Heeft je hulp nodig**. Gebruik dan de sleutel van een gebruiker die ze wel kan zien. Een nieuwe sleutel begint opnieuw en leest de afgelopen week weer in. Als Salesflare steeds een time-out geeft, maar elke nieuwe poging lukt, staat er dat Salesflare **soms traag** is.

Als Salesflare voor je team geen feedtoegang voor API-sleutels heeft ingeschakeld, staat dat op de kaart. Er worden dan geen e-mails of meetings opgehaald totdat de supportafdeling van Salesflare dit inschakelt. De koppeling controleert dit de eerste dag elke 10 minuten en daarna ongeveer elk uur. Zodra het werkt, gaat de sync vanzelf verder.

- **Stoppen**: er wordt niets nieuws opgehaald totdat je op **Starten** klikt. De sync gaat verder waar die was gebleven.
- **Sync herstarten**: begint opnieuw en leest de afgelopen week weer in. Er gaat niets verloren van wat al is opgehaald.
- **API-sleutels**: opent de pagina met API-sleutels van Salesflare, waar je een nieuwe sleutel kunt maken.

## Verwijderen

- In het dashboard: **Koppelingen**, open Salesflare, **Details** en klik vervolgens op **Ontkoppelen**. Wat al is opgehaald, blijft bewaard.
- Op een gehoste Machine kun je ook op **Verwijderen** naast de koppeling op je installatiepagina klikken.

## De sleutel intrekken in Salesflare

Verwijder de API-sleutel in Salesflare via Instellingen, API-sleutels.
