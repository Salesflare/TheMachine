---
title: Stripe
area: connections
summary: Mislukte betalingen, geschillen, annuleringen en grote nieuwe abonnementen. De koppeling kan alleen gegevens lezen.
covers: connector:stripe
code: connectors/stripe.py, shared_connectors.py
site: Sign in with Stripe, Connect, More sources, Share Stripe, Connect Stripe, Remove
translated: 85e6e07cca1a8e8d
---
## Wat de koppeling leest

Gebeurtenissen in je Stripe-account waarbij je mogelijk iets moet doen: mislukte betalingen, geschillen, annuleringen en grote nieuwe abonnementen, met de klant die erbij hoort. Het e-mailadres van een klant koppelt de gebeurtenis aan die persoon en diens organisatie in de [Graph](graph.md).

Bij een mislukte betaling staat waarvoor die was (een eerste betaling of een verlenging) en wanneer Stripe het opnieuw probeert. De reden waarom de kaart is geweigerd staat er niet bij. Stripe laat die informatie weg uit de gebeurtenis, dus open die in Stripe om de reden te bekijken.

## Wat de koppeling kan doen

Niets in Stripe. De koppeling voert nooit terugbetalingen uit, probeert geen betalingen opnieuw en verandert niets. Hij vraagt alleen leestoegang. Stripe laat dat zien voordat je de koppeling installeert.

## De koppeling instellen

Log op de eenvoudige manier in bij Stripe:

1. Ga in het dashboard naar **Koppelingen**, **Klanten** en Stripe. Of ga op de installatiepagina van een gehoste Machine op app.themachine.computer/setup naar **Meer bronnen** en Stripe. Koppel de Machine op je eigen computer eerst aan je account.
2. Klik op **Inloggen met Stripe**. Stripe vraagt welk account je wilt gebruiken en laat zien wat The Machine mag lezen.
3. Klik op **Installeren**. Je keert terug naar waar je begon en Stripe is gekoppeld.

Op je eigen computer kun je ook een beperkte sleutel plakken:

1. Maak in Stripe een beperkte sleutel aan met leestoegang voor Events, Customers en Account, en zonder toegang voor al het andere.
2. Zoek je account-ID (acct_...) onder Settings, Business details.
3. Open Stripe zoals hierboven (of voer `assistant connect stripe` uit), open **Of plak een beperkte sleutel**, plak de account-ID en de sleutel en klik op **Koppelen**.

Als Inloggen met Stripe nog niet beschikbaar is op je eigen computer, laat Koppelingen dat weten en opent het meteen dit formulier.

## Eén keer koppelen voor je team

In een Werk-Fleet koppelt een eigenaar of beheerder Stripe één keer en deelt die koppeling met het team:

1. Koppel Stripe op je eigen Machine (zie hierboven). In het vak **Gedeelde koppelingen** op het tabblad Fleet staat ook **Stripe koppelen**.
2. Open **Stripe delen** op het tabblad Fleet. Iedereen is geselecteerd. Haal het vinkje weg bij wie de koppeling niet mag gebruiken. Klik op **Delen**.

De Machines van je teamleden kunnen Stripe dan ook lezen. In Koppelingen zie je wie Stripe heeft gedeeld. Alleen beheerders van de Fleet kunnen de koppeling wijzigen of stopzetten. Je Machine vernieuwt elk uur hun toegang. Als die uitstaat, wordt hun toegang tot Stripe dus tijdelijk onderbroken. Niemand krijgt je inloggegevens. Meer informatie: [Fleets](fleet.md).

Als een teamlid hetzelfde Stripe-account ook zelf koppelt, wordt het maar één keer gelezen. De gedeelde koppeling wordt dan niet gebruikt.

Je kunt Stripe niet delen als het is gekoppeld via een dienst waarvan één sleutel ook toegang geeft tot andere apps. Koppel Stripe in plaats daarvan rechtstreeks voor het team.

## De koppeling verwijderen

- Ga in het dashboard naar **Koppelingen**, open Stripe en kies **Details** en vervolgens **Ontkoppelen**. Wat de koppeling al heeft opgehaald, blijft staan.
- Op een gehoste Machine staat bij Stripe waarvoor je bent ingelogd **Ontkoppelen ↗**. Daarmee open je je installatiepagina. Klik daar naast Stripe op **Verwijderen**.
- Gedeeld met een Fleet? Kies dan eerst **Stoppen met delen** op het tabblad Fleet.

## De toegang intrekken in Stripe

- Ingelogd met Stripe: open in Stripe Settings, Installed apps en verwijder The Machine.
- Beperkte sleutel: open in Stripe Developers, API keys en verwijder of vervang de sleutel.
