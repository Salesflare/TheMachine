---
title: Salesflare CRM
area: connections
summary: Accounts, contacten en deals, zodat hij weet wie belangrijk is. Het leest met je API-sleutel.
covers: connector:salesflare
code: assistant.py, onboarding.py
site: More sources, Connect, Remove
---
## Wat het leest

Je accounts, contacten en deals in Salesflare, en de feeds van de accounts: e-mails van collega's waar jij niet bij betrokken bent, en afspraken met notities.

## Wat het kan wijzigen

Niets, tenzij je `join_pipelines` instelt in het instellingenbestand van je Machine. Dan voegt hij je zelf toe aan accounts in die pipelines. Standaard is het leeg.

## Koppelen

1. Open in Salesflare [Settings, API keys](https://app.salesflare.com/#/settings/apikeys) en maak een sleutel aan.
2. Op een gehoste Machine: open je setuppagina op app.themachine.computer/setup, ga naar **Meer bronnen**, open Salesflare CRM, plak de sleutel en druk op **Verbinden**.
3. Op je eigen computer: voer `assistant connect crm` uit, of **Koppelingen**, **+ Toevoegen**, Salesflare CRM. Na **Verbinden** herstart je Machine en opent hij de Salesflare-kaart. Die zegt eerst dat hij de accounts met recente e-mails en afspraken zoekt, en daarna hoeveel hij er gelezen heeft.

## Details van de sync

De kaart onder **Koppelingen**, **Andere bronnen** toont hoe ver hij is: hoeveel accounts hij in deze ronde gelezen heeft, en hoeveel hij overgeslagen heeft omdat Salesflare te traag antwoordde. Een ronde die uren duurt, meldt dat ze misschien vastzit.

- **Stoppen**: er komt niets nieuws binnen tot je op **Begin** drukt. Hij gaat verder waar hij was.
- **Sync herstarten**: laat de huidige ronde vallen, met de fouten, en leest nu de afgelopen week opnieuw. Er gaat niets verloren van wat hij binnengehaald heeft.
- **API-sleutels**: opent de pagina met API-sleutels van Salesflare, om een nieuwe sleutel te maken.

## Verwijderen

- In het dashboard: **Koppelingen**, open Salesflare, **Details**, dan **Ontkoppelen**. Wat al binnengehaald is, blijft.
- Op een gehoste Machine kun je ook op **Verwijderen** ernaast drukken op je setuppagina.

## Intrekken in Salesflare

Verwijder de API-sleutel in Salesflare, onder Settings, API keys.
