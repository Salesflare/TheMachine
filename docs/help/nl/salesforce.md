---
title: Salesforce
area: connections
summary: Deals, taken en activiteit uit Salesforce bij je mensen en projecten. Als je het aanzet, houdt het contactgegevens daar actueel.
covers: connector:salesforce
code: connectors/salesforce.py, crm_sync.py, onboarding.py
site: Connect Salesforce, More sources, Remove, Sign in with Salesforce
---
## Wat het leest

Nieuwe deals, en deals die naar een andere fase gaan of een ander bedrag krijgen. Je open taken, gesprekken en andere taken die als gedaan zijn gelogd met notities, en afspraken met een beschrijving. De laatste 7 dagen als je koppelt, daarna elke 15 minuten de nieuwe.

Elke deal wordt een project in je Graph, en de contacten erop verschijnen bij hun mensen, als Salesforce-contact bij hun account.

## Wat het kan wijzigen

Niets, tot je **Contactgegevens bijwerken** aanzet. Je Salesforce-login blijft op je Machine.

## Koppelen

Op een gehoste Machine:

1. Open je setuppagina op app.themachine.computer/setup en ga naar **Meer bronnen**.
2. Open Salesforce en druk op **Salesforce koppelen**.
3. Log in bij Salesforce en sta The Machine toe (gemaakt door Salesflare).

Of in het dashboard: **Koppelingen**, **+ Toevoegen**, kies Salesforce en druk op **Inloggen met Salesforce**.

Je Salesforce-gebruiker heeft API-toegang nodig, wat de meeste edities hebben.

## Contactgegevens bijwerken

Als je Machine nieuwere gegevens kent van een van je Salesforce-contacten, kan het dat contact daar bijwerken: functie, telefoon, en de LinkedIn-link als je org een LinkedIn-veld op contacten heeft.

1. Open in **Koppelingen** Salesforce en druk op **Toon wat er zou veranderen**.
2. Bekijk de lijst en druk dan op **Aanzetten** of **Niet nu**.

Waar het zich aan houdt:

- Alleen gegevens in de eigen woorden van de persoon, zoals hun LinkedIn- of Slack-profiel, of die je zelf op hun pagina zette. Nooit een gok.
- Alleen als het gegeven nieuwer is dan de laatste wijziging van het contact in Salesforce. Een wijziging daar wint.
- Alleen velden die verschillen, en nooit een lege waarde. Het verandert nooit het e-mailadres of het account.
- Elke wijziging is een gedateerde regel op de pagina van de persoon.

Druk op **Uitzetten** om te stoppen. Een koppeling die je Fleet deelt, leest alleen.

## Verwijderen

- In het dashboard: **Koppelingen**, open Salesforce, **Details**, dan **Ontkoppelen**. Wat het al binnenhaalde, blijft.
- Op een gehoste Machine kun je ook op **Verwijderen** ernaast drukken op je setuppagina.

## Intrekken in Salesforce

Open in Salesforce je persoonlijke instellingen, dan Connected Apps OAuth Usage, of vraag het je admin, en trek The Machine in. Het kan dan niets meer lezen of wijzigen.
