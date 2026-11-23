---
title: Stripe
area: connections
summary: Fehlgeschlagene Zahlungen, Streitfälle, Kündigungen und große neue Abos. Die Verbindung liest nur Daten.
covers: connector:stripe
code: connectors/stripe.py, shared_connectors.py
site: Sign in with Stripe, Connect, More sources, Share Stripe, Connect Stripe, Remove
translated: 85e6e07cca1a8e8d
---
## Was gelesen wird

Ereignisse in deinem Stripe-Konto, die deine Aufmerksamkeit erfordern könnten: fehlgeschlagene Zahlungen, Streitfälle, Kündigungen und große neue Abos, jeweils mit dem zugehörigen Kunden. Die E-Mail-Adresse eines Kunden verknüpft das Ereignis mit dieser Person und ihrer Organisation im [Graph](graph.md).

Bei einer fehlgeschlagenen Zahlung steht dabei, wofür sie gedacht war (eine erste Zahlung oder eine Verlängerung) und wann Stripe es erneut versucht. Warum die Karte abgelehnt wurde, steht dort nicht. Stripe zeigt diesen Grund im Ereignis nicht an. Öffne es in Stripe, um den Grund zu sehen.

## Was die Verbindung kann

In Stripe kann sie nichts ändern. Sie veranlasst weder Rückerstattungen noch erneute Zahlungsversuche und ändert auch sonst nichts. Sie benötigt nur Lesezugriff. Stripe zeigt dir das vor der Installation an.

## Verbindung herstellen

Melde dich einfach mit Stripe an:

1. Im Dashboard: **Verbindungen**, **Kunden**, Stripe. Oder auf der Einrichtungsseite einer gehosteten Machine unter app.themachine.computer/setup: **Weitere Quellen**, Stripe. Auf deinem eigenen Computer musst du sie zuerst mit deinem Konto koppeln.
2. Klicke auf **Mit Stripe anmelden**. Stripe fragt, welches Konto du verwenden möchtest, und zeigt dir, welche Daten The Machine lesen darf.
3. Klicke auf **Installieren**. Du kehrst zur vorherigen Seite zurück und Stripe ist verbunden.

Auf deinem eigenen Computer kannst du stattdessen einen eingeschränkten Schlüssel einfügen:

1. Erstelle in Stripe einen eingeschränkten Schlüssel mit Leseberechtigung für Ereignisse, Kunden und Konto sowie ohne Berechtigungen für alles andere.
2. Deine Konto-ID (acct_...) findest du unter Einstellungen, Unternehmensdetails.
3. Öffne Stripe wie oben (oder führe `assistant connect stripe` aus), öffne **Oder einen eingeschränkten Schlüssel einfügen**, füge die Konto-ID und den Schlüssel ein und klicke auf **Verbinden**.

Auf deinem eigenen Computer weist dich „Verbindungen“ darauf hin, wenn „Mit Stripe anmelden“ noch nicht verfügbar ist, und öffnet direkt dieses Formular.

## Einmal für dein Team verbinden

In einer Work Fleet verbindet ein Inhaber oder Admin Stripe einmal und teilt die Verbindung mit dem Team:

1. Verbinde Stripe auf deiner Machine (siehe oben). Im Feld **Geteilte Verbindungen** auf dem Fleet-Tab findest du ebenfalls **Stripe verbinden**.
2. Öffne im Fleet-Tab **Stripe teilen**. Alle sind ausgewählt. Entferne die Auswahl bei allen, die keinen Zugriff erhalten sollen. Klicke auf **Teilen**.

Die Machines deiner Teammitglieder können Stripe dann ebenfalls auslesen. Unter „Verbindungen“ siehst du, wer die Verbindung geteilt hat. Nur Admins der Fleet können sie ändern oder beenden. Deine Machine erneuert den Zugriff für die Teammitglieder stündlich. Ist sie ausgeschaltet, wird ihr Stripe-Zugriff pausiert. Niemand erhält deine Anmeldedaten. Weitere Details: [Fleets](fleet.md).

Wenn ein Teammitglied dasselbe Stripe-Konto selbst verbindet, wird es nur einmal ausgelesen. Die geteilte Verbindung bleibt dann ungenutzt.

Eine Stripe-Verbindung über einen Dienst, dessen Schlüssel auch andere Apps öffnet, kann nicht geteilt werden. Verbinde Stripe stattdessen direkt mit der Fleet.

## Verbindung entfernen

- Im Dashboard: **Verbindungen** öffnen, Stripe auswählen, **Details** und dann **Trennen**. Bereits importierte Daten bleiben erhalten.
- Auf einer gehosteten Machine wird für Stripe, bei dem du angemeldet bist, **Trennen ↗** angezeigt. Damit öffnest du deine Einrichtungsseite. Klicke dort daneben auf **Entfernen**.
- Wenn die Verbindung mit einer Fleet geteilt wird, klicke zuerst im Fleet-Tab auf **Nicht mehr teilen**.

## Zugriff in Stripe widerrufen

- Wenn du dich mit Stripe angemeldet hast: Öffne in Stripe Einstellungen und dann Installierte Apps. Entferne dort The Machine.
- Bei einem eingeschränkten Schlüssel: Öffne in Stripe Entwickler und dann API-Schlüssel. Lösche oder erneuere den Schlüssel.
