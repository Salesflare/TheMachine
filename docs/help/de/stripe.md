---
title: Stripe
area: connections
summary: Fehlgeschlagene Zahlungen, Rückbuchungen, Kündigungen und große neue Abos. Es liest nur.
covers: connector:stripe
code: connectors/stripe.py
site: Connect, More sources, Remove
---
## Was es liest

Ereignisse in deinem Stripe-Konto, die dich brauchen könnten: fehlgeschlagene Zahlungen, Rückbuchungen, Kündigungen und große neue Abos, mit dem Kunden, zu dem sie gehören.

## Was es tun kann

Nichts in Stripe. Es schreibt nie, erstattet nichts und wiederholt keine Zahlung.

## Verbinden

1. Erstelle in Stripe einen eingeschränkten Schlüssel mit Read für Events, Customers und Account und None für alles andere.
2. Deine Konto-ID (acct_...) findest du unter Settings, Business details.
3. Auf einer gehosteten Machine: Öffne deine Einrichtungsseite unter app.themachine.computer/setup, geh zu **Weitere Quellen** und öffne Stripe. Auf deinem eigenen Computer: **Verbindungen**, **+ Hinzufügen**, Stripe, oder `assistant connect stripe`.
4. Füge die Konto-ID und den Schlüssel ein und tippe dann auf **Verbinden**.

## Entfernen

- Im Dashboard: **Verbindungen**, Stripe öffnen, **Details**, dann **Trennen**. Was es schon reingebracht hat, bleibt.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** tippen.

## In Stripe widerrufen

Öffne in Stripe Developers, API keys und lösche oder erneuere den eingeschränkten Schlüssel.
