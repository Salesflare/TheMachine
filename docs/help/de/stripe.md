---
title: Stripe
area: connections
summary: Fehlgeschlagene Zahlungen, Rückbuchungen, Kündigungen und große neue Abos. Es liest nur.
covers: connector:stripe
code: connectors/stripe.py, shared_connectors.py
site: Sign in with Stripe, Connect, More sources, Share Stripe, Connect Stripe, Remove
---
## Was es liest

Ereignisse in deinem Stripe-Konto, die dich brauchen könnten: fehlgeschlagene Zahlungen, Rückbuchungen, Kündigungen und große neue Abos, mit dem Kunden, zu dem sie gehören. Die E-Mail eines Kunden verknüpft das Ereignis mit dieser Person und ihrer Organisation im [Graph](graph.md).

## Was es tun kann

Nichts in Stripe. Es schreibt nie, erstattet nichts und wiederholt keine Zahlung. Die Stripe-App von The Machine bittet Stripe nur um Leserechte, und Stripe zeigt sie dir, bevor du sie installierst.

## Verbinden

Mit Stripe anmelden, der einfache Weg:

1. Auf einer gehosteten Machine: Öffne deine Einrichtungsseite unter app.themachine.computer/setup, geh zu **Weitere Quellen** und öffne Stripe. Auf deinem eigenen Computer, gekoppelt mit deinem Konto: **Verbindungen**, **+ Hinzufügen**, Stripe.
2. Tippe auf **Mit Stripe anmelden**. Stripe fragt, welches Konto, und zeigt, was The Machine lesen darf.
3. Tippe auf **Installieren**. Du bist zurück auf deiner Einrichtungsseite, und Stripe ist verbunden.

Oder füge stattdessen einen eingeschränkten Schlüssel ein:

1. Erstelle in Stripe einen eingeschränkten Schlüssel mit Read für Events, Customers und Account und None für alles andere.
2. Deine Konto-ID (acct_...) findest du unter Settings, Business details.
3. Öffne Stripe wie oben (oder führe `assistant connect stripe` aus), öffne **Oder einen eingeschränkten Schlüssel einfügen**, füge die Konto-ID und den Schlüssel ein und tippe dann auf **Verbinden**.

## Einmal für dein Team verbinden

In einer Work Fleet verbindet ein Owner oder Admin Stripe einmal und teilt es mit dem Team:

1. Verbinde Stripe auf deiner eigenen Machine (siehe oben). Der Kasten **Geteilte Connectors** im Fleet-Tab hat auch **Stripe verbinden**.
2. Öffne im Fleet-Tab **Stripe teilen**. Alle sind angehakt. Nimm den Haken bei denen weg, die es nicht bekommen sollen. Tippe auf **Teilen**.

Die Machines der Teammitglieder lesen es auch, nur lesend. Unter Verbindungen steht, wer es geteilt hat, und nur die Admins der Fleet können es ändern oder stoppen. Deine Machine erneuert ihren Zugriff jede Stunde. Ist sie länger aus, pausiert ihr Stripe, bis sie wieder da ist. Niemand bekommt je deine Anmeldung selbst. Details: [Fleets](fleet.md).

Eine Stripe-Verbindung über einen anderen Dienst mit einem Schlüssel für viele Verbindungen kann nicht geteilt werden: Dieser Schlüssel öffnet mehr als Stripe. Verbinde Stripe stattdessen einzeln für das Team.

## Entfernen

- Im Dashboard: **Verbindungen**, Stripe öffnen, **Details**, dann **Trennen**. Was es schon reingebracht hat, bleibt.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** tippen.
- Mit einer Fleet geteilt: zuerst **Nicht mehr teilen** im Fleet-Tab.

## In Stripe widerrufen

- Mit Stripe angemeldet: Öffne in Stripe Settings, Installed apps und entferne The Machine.
- Eingeschränkter Schlüssel: Öffne in Stripe Developers, API keys und lösche oder erneuere den Schlüssel.
