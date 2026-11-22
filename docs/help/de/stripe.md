---
title: Stripe
area: connections
summary: Fehlgeschlagene Zahlungen, Zahlungsanfechtungen, Kündigungen und große neue Abos. Nur Lesezugriff.
covers: connector:stripe
code: connectors/stripe.py, shared_connectors.py
site: Sign in with Stripe, Connect, More sources, Share Stripe, Connect Stripe, Remove
translated: 6e7ca235dc502297
---
## Was sie liest

Ereignisse in deinem Stripe-Konto, die deine Aufmerksamkeit erfordern könnten: fehlgeschlagene Zahlungen, Zahlungsanfechtungen, Kündigungen und große neue Abos, jeweils mit dem zugehörigen Kunden. Die E-Mail-Adresse eines Kunden verknüpft das Ereignis mit der Person und ihrem Unternehmen im [Graph](graph.md).

## Was sie kann

In Stripe kann sie nichts tun. Sie erstattet nie Zahlungen, versucht Zahlungen nicht erneut und ändert nichts. Sie fordert nur Lesezugriff an. Stripe zeigt dir das, bevor du sie installierst.

## Verbinden

Melde dich ganz einfach mit Stripe an:

1. Im Dashboard: **Verbindungen**, **Kunden**, Stripe. Oder auf der Einrichtungsseite einer gehosteten Machine unter app.themachine.computer/setup: **Weitere Quellen**, Stripe. Auf deinem eigenen Computer musst du sie zuerst mit deinem Konto koppeln.
2. Klicke auf **Mit Stripe anmelden**. Stripe fragt, welches Konto du verbinden möchtest, und zeigt dir, was The Machine lesen darf.
3. Klicke auf **Installieren**. Du kehrst zur vorherigen Seite zurück und Stripe ist verbunden.

Auf deinem eigenen Computer kannst du stattdessen einen eingeschränkten Schlüssel einfügen:

1. Erstelle in Stripe einen eingeschränkten Schlüssel mit Leseberechtigung für **Ereignisse**, **Kunden** und **Konto** und ohne Berechtigungen für alles andere.
2. Deine Konto-ID (acct_...) findest du unter **Einstellungen**, **Unternehmensdaten**.
3. Öffne Stripe wie oben beschrieben (oder führe `assistant connect stripe` aus), öffne **Oder einen eingeschränkten Schlüssel einfügen**, füge die Konto-ID und den Schlüssel ein und klicke auf **Verbinden**.

Auf deinem eigenen Computer weist dich **Verbindungen** darauf hin, wenn **Mit Stripe anmelden** noch nicht verfügbar ist, und öffnet direkt dieses Formular.

## Einmal für dein Team verbinden

In einer Work Fleet verbindet ein Owner oder Admin Stripe einmal und teilt die Verbindung mit dem Team:

1. Verbinde Stripe mit deiner eigenen Machine (siehe oben). Im Feld **Geteilte Verbindungen** auf dem Fleet-Tab findest du auch **Stripe verbinden**.
2. Öffne auf dem Fleet-Tab **Stripe teilen**. Alle sind ausgewählt. Entferne die Auswahl für alle, die keinen Zugriff erhalten sollen. Klicke auf **Teilen**.

Die Machines deiner Teammitglieder können Stripe dann ebenfalls lesen. Unter **Verbindungen** siehst du, wer die Verbindung geteilt hat. Nur die Admins der Fleet können sie ändern oder beenden. Deine Machine erneuert den Zugriff für die anderen stündlich. Ist sie ausgeschaltet, wird der Stripe-Zugriff für sie pausiert. Niemand erhält deine Anmeldedaten. Weitere Informationen: [Fleet](fleet.md).

Wenn ein Teammitglied dasselbe Stripe-Konto selbst verbindet, wird es nur einmal gelesen. Die geteilte Verbindung bleibt ungenutzt.

Eine Stripe-Verbindung über einen Dienst, dessen einzelner Schlüssel auch andere Apps öffnet, kann nicht geteilt werden. Verbinde Stripe stattdessen direkt mit der Fleet.

## Verbindung entfernen

- Im Dashboard: **Verbindungen** öffnen, Stripe auswählen und auf **Details** und dann **Trennen** klicken. Was bereits importiert wurde, bleibt erhalten.
- Auf einer gehosteten Machine wird bei einer Stripe-Verbindung, für die du dich angemeldet hast, **Trennen ↗** angezeigt. Damit öffnest du deine Einrichtungsseite. Klicke dort daneben auf **Entfernen**.
- Wird die Verbindung mit einer Fleet geteilt, musst du zuerst auf dem Fleet-Tab auf **Nicht mehr teilen** klicken.

## Zugriff in Stripe widerrufen

- Wenn du dich mit Stripe angemeldet hast: Öffne in Stripe **Einstellungen**, **Installierte Apps** und entferne The Machine.
- Bei einem eingeschränkten Schlüssel: Öffne in Stripe **Entwickler**, **API-Schlüssel** und lösche oder erneuere den Schlüssel.
