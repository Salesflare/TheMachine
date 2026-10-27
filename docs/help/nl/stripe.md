---
title: Stripe
area: connections
summary: Mislukte betalingen, geschillen, opzeggingen en grote nieuwe abonnementen. Het leest alleen.
covers: connector:stripe
code: connectors/stripe.py, shared_connectors.py
site: Sign in with Stripe, Connect, More sources, Share Stripe, Connect Stripe, Remove
---
## Wat het leest

Gebeurtenissen op je Stripe-account die jou nodig kunnen hebben: mislukte betalingen, geschillen, opzeggingen en grote nieuwe abonnementen, met de klant bij wie ze horen. Het e-mailadres van een klant koppelt de gebeurtenis aan die persoon en diens organisatie in de [Graph](graph.md).

## Wat het kan doen

Niets in Stripe. Het schrijft nooit iets, betaalt nooit terug en probeert nooit een betaling opnieuw. De Stripe-app van The Machine vraagt Stripe alleen om leesrechten, en Stripe toont ze voor je hem installeert.

## Koppelen

Inloggen met Stripe, de makkelijke manier:

1. Op een gehoste Machine: open je setuppagina op app.themachine.computer/setup, ga naar **Meer bronnen** en open Stripe. Op je eigen computer, gekoppeld aan je account: **Koppelingen**, **+ Toevoegen**, Stripe.
2. Druk op **Inloggen met Stripe**. Stripe vraagt welk account, en toont wat The Machine mag lezen.
3. Druk op **Installeren**. Je bent terug op je setuppagina, en Stripe is gekoppeld.

Of plak in plaats daarvan een beperkte sleutel:

1. Maak in Stripe een beperkte sleutel aan met Read op Events, Customers en Account, en None op al de rest.
2. Zoek je account-ID (acct_...) onder Settings, Business details.
3. Open Stripe zoals hierboven (of voer `assistant connect stripe` uit), open **Of plak een beperkte sleutel**, plak het account-ID en de sleutel en druk op **Verbinden**.

## Eén keer koppelen voor je team

In een Werk-Fleet koppelt een eigenaar of beheerder Stripe één keer en deelt het met het team:

1. Koppel Stripe op je eigen Machine (zie hierboven). Het vak **Gedeelde connectors** in het tabblad Fleet heeft ook **Stripe koppelen**.
2. Open in het tabblad Fleet **Stripe delen**. Iedereen is aangevinkt; vink uit wie het niet mag krijgen. Druk op **Delen**.

De Machines van teamgenoten lezen het dan ook, alleen lezen. Onder Koppelingen staat wie het deelde, en alleen de beheerders van de Fleet kunnen het wijzigen of stoppen. Je Machine vernieuwt hun toegang elk uur, dus als hij langer uit staat, pauzeert hun Stripe tot hij terug is. Niemand krijgt ooit je login zelf. Details: [Fleets](fleet.md).

## Verwijderen

- In het dashboard: **Koppelingen**, open Stripe, **Details**, dan **Ontkoppelen**. Wat al binnengehaald is, blijft.
- Op een gehoste Machine kun je ook op **Verwijderen** ernaast drukken op je setuppagina.
- Gedeeld met een Fleet: eerst **Stoppen met delen** in het tabblad Fleet.

## Intrekken in Stripe

- Ingelogd met Stripe: open in Stripe Settings, Installed apps, en verwijder The Machine.
- Beperkte sleutel: open in Stripe Developers, API keys, en verwijder of vernieuw de sleutel.
