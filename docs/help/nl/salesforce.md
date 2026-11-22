---
title: Salesforce
area: connections
summary: Deals, taken en activiteit uit Salesforce bij je mensen en projecten. Als je dat aanzet, kan The Machine daar contactgegevens bijwerken.
covers: connector:salesforce
code: connectors/salesforce.py, crm_sync.py, onboarding.py
site: Connect Salesforce, More sources, Remove, Sign in with Salesforce
translated: eee5e084bac6dbd1
---
## Wat The Machine leest

Nieuwe deals en deals die naar een andere fase gaan of waarvan het bedrag verandert. Je openstaande taken, gesprekken en andere taken die als Gedaan zijn gemarkeerd, met notities, plus meetings met een beschrijving. De gegevens van de afgelopen 7 dagen wanneer je koppelt, daarna elke 15 minuten nieuwe gegevens.

Elke deal wordt een project in je Graph. De contacten op die deal verschijnen bij de bijbehorende personen, als Salesforce-contact bij hun account.

## Wat The Machine kan wijzigen

Niets, totdat je **Contactgegevens bijwerken** aanzet. Je Salesforce-inloggegevens blijven op je Machine.

## Koppelen

Op een gehoste Machine:

1. Open je installatiepagina op app.themachine.computer/setup en ga naar **Meer bronnen**.
2. Open Salesforce en klik op **Salesforce koppelen**.
3. Log in bij Salesforce en geef The Machine (gemaakt door Salesflare) toestemming.

Of in het dashboard: **Koppelingen**, **Klanten**, kies Salesforce en klik op **Inloggen met Salesforce**. Koppel Salesforce op je eigen computer eerst aan je account.

Je Salesforce-gebruiker moet API-toegang hebben. Die is bij de meeste edities inbegrepen.

## Contactgegevens bijwerken

Als je Machine nieuwere gegevens heeft over een van je Salesforce-contacten, kan hij die gegevens daar bijwerken: functietitel, telefoonnummer en de LinkedIn-link als je organisatie een LinkedIn-veld voor contacten heeft.

1. Open Salesforce bij **Koppelingen** en klik op **Toon wat er zou veranderen**.
2. Controleer de lijst en klik op **Aanzetten** of **Niet nu**.

The Machine houdt zich aan deze regels:

- Alleen gegevens die de persoon zelf heeft opgegeven, bijvoorbeeld op diens LinkedIn- of Slack-profiel, of die je op de pagina van die persoon hebt ingevuld. Nooit een schatting.
- Alleen als de gegevens nieuwer zijn dan de laatste wijziging van het contact in Salesforce. Een wijziging in Salesforce gaat voor.
- Alleen velden waarvan de inhoud verschilt, en nooit een leeg veld. Het e-mailadres en het account worden nooit gewijzigd.
- Elke wijziging verschijnt als een regel met datum op de pagina van de persoon.

Klik op **Uitzetten** om te stoppen. Een koppeling die je Fleet deelt, leest alleen gegevens.

## Verwijderen

- In het dashboard: open Salesforce bij **Koppelingen**, klik op **Details** en daarna op **Ontkoppelen**. Gegevens die al zijn opgehaald, blijven staan.
- Op een gehoste Machine opent **Ontkoppelen ↗** je installatiepagina. Klik daar naast Salesforce op **Verwijderen**.

## Toegang intrekken in Salesforce

Open in Salesforce je persoonlijke instellingen en ga naar OAuth-gebruik van verbonden apps, of vraag het je beheerder, en trek de toegang van The Machine in. The Machine kan dan niets meer lezen of wijzigen.
