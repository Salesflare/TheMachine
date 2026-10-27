---
title: Stripe
area: connections
summary: Mislukte betalingen, geschillen, opzeggingen en grote nieuwe abonnementen. Het leest alleen.
covers: connector:stripe
code: connectors/stripe.py
site: Connect, More sources, Remove
---
## Wat het leest

Gebeurtenissen op je Stripe-account die jou nodig kunnen hebben: mislukte betalingen, geschillen, opzeggingen en grote nieuwe abonnementen, met de klant bij wie ze horen.

## Wat het kan doen

Niets in Stripe. Het schrijft nooit iets, betaalt nooit terug en probeert nooit een betaling opnieuw.

## Koppelen

1. Maak in Stripe een beperkte sleutel aan met Read op Events, Customers en Account, en None op al de rest.
2. Zoek je account-ID (acct_...) onder Settings, Business details.
3. Op een gehoste Machine: open je setuppagina op app.themachine.computer/setup, ga naar **Meer bronnen** en open Stripe. Op je eigen computer: **Koppelingen**, **+ Toevoegen**, Stripe, of `assistant connect stripe`.
4. Plak het account-ID en de sleutel en druk op **Verbinden**.

## Verwijderen

- In het dashboard: **Koppelingen**, open Stripe, **Details**, dan **Ontkoppelen**. Wat al binnengehaald is, blijft.
- Op een gehoste Machine kun je ook op **Verwijderen** ernaast drukken op je setuppagina.

## Intrekken in Stripe

Open in Stripe Developers, API keys, en verwijder of vernieuw de beperkte sleutel.
