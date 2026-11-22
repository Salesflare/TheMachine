---
title: Stripe
area: connections
summary: Mislukte betalingen, geschillen, annuleringen en grote nieuwe abonnementen. De koppeling kan alleen gegevens lezen.
covers: connector:stripe
code: connectors/stripe.py, shared_connectors.py
site: Sign in with Stripe, Connect, More sources, Share Stripe, Connect Stripe, Remove
translated: 6e7ca235dc502297
---
## Wat hij leest

Gebeurtenissen in je Stripe-account waarbij je mogelijk iets moet doen: mislukte betalingen, geschillen, annuleringen en grote nieuwe abonnementen, met de bijbehorende klant. Het e-mailadres van een klant koppelt de gebeurtenis aan die persoon en diens organisatie in de [Graph](graph.md).

## Wat hij kan doen

Niets in Stripe. Hij betaalt nooit terug, probeert betalingen nooit opnieuw en verandert niets. Hij vraagt alleen leestoegang aan. Stripe laat dat zien voordat je de koppeling installeert.

## Koppelen

Inloggen met Stripe is het makkelijkst:

1. In het dashboard: **Koppelingen**, **Klanten**, Stripe. Of op de installatiepagina van een gehoste Machine op app.themachine.computer/setup: **Meer bronnen**, Stripe. Op je eigen computer moet je de Machine eerst aan je account koppelen.
2. Druk op **Inloggen met Stripe**. Stripe vraagt welk account je wilt gebruiken en laat zien wat The Machine mag lezen.
3. Druk op **Installeren**. Je keert terug naar waar je was en Stripe is gekoppeld.

Op je eigen computer kun je ook een beperkte sleutel plakken:

1. Maak in Stripe een beperkte sleutel aan met leesrechten voor Events, Customers en Account, en geen rechten voor al het andere.
2. Zoek je account-ID (acct_...) onder Instellingen, Bedrijfsgegevens.
3. Open Stripe zoals hierboven (of voer `assistant connect stripe` uit), open **Of plak een beperkte sleutel**, plak de account-ID en de sleutel en druk op **Koppelen**.

Als Inloggen met Stripe op je eigen computer nog niet beschikbaar is, laat Koppelingen dat weten en opent het formulier meteen.

## Eén keer koppelen voor je team

In een Werk-Fleet koppelt een eigenaar of beheerder Stripe één keer en deelt de koppeling met het team:

1. Koppel Stripe op je eigen Machine (zie hierboven). In het vak **Gedeelde koppelingen** op het tabblad Fleet staat ook **Stripe koppelen**.
2. Open op het tabblad Fleet **Stripe delen**. Iedereen is geselecteerd. Haal het vinkje weg bij wie de koppeling niet moet krijgen. Druk op **Delen**.

De Machines van je teamgenoten kunnen Stripe dan ook lezen. Koppelingen laat zien wie de koppeling heeft gedeeld. Alleen de beheerders van de Fleet kunnen de koppeling wijzigen of stopzetten. Je Machine vernieuwt hun toegang elk uur. Zolang hij uitstaat, wordt hun toegang tot Stripe onderbroken. Niemand krijgt je login zelf. Meer informatie: [Fleets](fleet.md).

Als een teamgenoot hetzelfde Stripe-account ook zelf koppelt, leest de Machine de gegevens maar één keer. De gedeelde koppeling blijft dan ongebruikt.

Een Stripe-koppeling via een dienst waarvan één sleutel ook andere apps opent, kun je niet delen. Koppel Stripe rechtstreeks voor het team.

## De koppeling verwijderen

- In het dashboard: **Koppelingen**, open Stripe, **Details** en dan **Ontkoppelen**. Gegevens die al zijn opgehaald, blijven staan.
- Op een gehoste Machine staat bij Stripe waarbij je bent ingelogd **Ontkoppelen ↗**. Daarmee open je je installatiepagina. Druk daar naast Stripe op **Verwijderen**.
- Gedeeld met een Fleet? Druk dan eerst op **Stoppen met delen** op het tabblad Fleet.

## De toegang intrekken in Stripe

- Ingelogd met Stripe: open in Stripe Instellingen, Geïnstalleerde apps en verwijder The Machine.
- Beperkte sleutel: open in Stripe Developers, API-sleutels en verwijder de sleutel of maak een nieuwe.
