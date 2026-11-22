---
title: App installieren und Benachrichtigungen einschalten
area: getting-started
summary: Installiere The Machine auf deinem Handy oder Computer und erhalte für jede Aufgabe eine Benachrichtigung. Telegram ist optional.
covers: phone-app
code: manifest.webmanifest, sw.js, dashboard.html
order: 3
translated: 3c10a121b1cfb06d
---
Installiere The Machine als App auf deinem Handy oder Computer, damit du innerhalb deiner [Arbeitszeiten](work-hours.md) für jede Aufgabe, jedes Ergebnis und jede Erinnerung eine Benachrichtigung erhältst. Lege unter [Benachrichtigungen](notifications.md) fest, was gesendet wird.

Die Aufgabe **Hol mehr aus The Machine heraus** oben in den Aufgaben enthält jeweils einen Eintrag für **Hol dir die App fürs Handy** (siehe [Die mobile App](mobile-app.md)), **Benachrichtigungen einschalten** und **Auf diesem Computer installieren**. Angezeigt wird nur, was auf dem jeweiligen Gerät noch fehlt. Über × kannst du einen Eintrag schließen. Dieselben Optionen findest du unter **Einstellungen**, **Allgemein**, **Dieses Gerät**.

In der Handy-App wird **Lass dich benachrichtigen, wenn dich etwas braucht.** angezeigt, solange Benachrichtigungen ausgeschaltet sind. Über **Einschalten** wird die Handy-Einstellung geöffnet oder eine Berechtigungsanfrage angezeigt. Über **×** wird der Hinweis 7 Tage lang ausgeblendet.

## Auf einem Computer (Chrome oder Edge)

1. Öffne dein Dashboard und klicke auf **Installieren** im entsprechenden Eintrag der Aufgabe, auf **App installieren** unter **Einstellungen**, **Allgemein** oder auf **Installieren** neben **Computer** unter **Einstellungen**, **Apps**.
2. The Machine wird in einem eigenen Fenster geöffnet. Heft sie an die Taskleiste oder ans Dock.
3. Klicke im entsprechenden Eintrag auf **Einschalten** und erlaube Benachrichtigungen. Eine Testbenachrichtigung erscheint sofort.

## Auf einem Mac (Safari)

1. Wähle in der Safari-Menüleiste „Ablage“ und dann „Zum Dock hinzufügen“.
2. Öffne The Machine über das Dock und klicke auf **Einschalten**.

## In Firefox

Firefox kann die App nicht installieren. Benachrichtigungen funktionieren im Tab: Klicke im entsprechenden Eintrag auf **Einschalten** oder auf die Glocke neben **Benachrichtigungen** unter **Einstellungen**.

## Auf einem iPhone oder iPad

1. Öffne dein Dashboard in Safari. Du brauchst iOS 16.4 oder neuer.
2. Tippe auf „Teilen“ und dann auf „Zum Home-Bildschirm“.
3. Öffne The Machine über den Home-Bildschirm und tippe auf **Einschalten**.

Benachrichtigungen funktionieren nur über die App auf dem Home-Bildschirm, nicht in einem Safari-Tab.

## Auf Android

1. Öffne dein Dashboard in Chrome, öffne das Menü und tippe auf „App installieren“.
2. Öffne die App über den Startbildschirm und tippe auf **Einschalten**.

## Einstellungen prüfen oder ändern

Unter **Einstellungen**, **Allgemein**, **Dieses Gerät** kannst du über die Glocke neben **Benachrichtigungen** die Benachrichtigungen nur für dieses Gerät ein- oder ausschalten. Über **Test senden** wird eine Testbenachrichtigung an dieses Gerät gesendet.

Blockiert? Klicke auf einem Computer auf das Symbol links neben der Adresszeile und erlaube Benachrichtigungen. Öffne auf einem iPhone die App „Einstellungen“ und tippe auf „Mitteilungen“ und dann auf „The Machine“.

## Schneller öffnen

Die App öffnet sofort deine zuletzt aufgerufenen Aufgaben und aktualisiert sie anschließend. Diese Kopie bleibt verschlüsselt und höchstens 7 Tage lang auf dem Gerät. Wenn du dich abmeldest, wird sie gelöscht.

## Ohne Internet und bei schlechtem WLAN

Im Flugzeug oder Zug funktioniert das Dashboard weiterhin. Oben wird eine Leiste mit dem Status **Offline** und dem Zeitpunkt der letzten Aktualisierung angezeigt. Deine Aufgaben, ihre Chats, der Kalender und die Listen in Graph lassen sich auf dem Gerät öffnen.

- **Zurückstellen**, **Nicht nötig**, **Als erledigt markieren**, **Wieder öffnen** und Chat-Nachrichten an The Machine werden mit der Option **Abbrechen** auf dem Gerät gespeichert. Sobald du wieder online bist, werden sie automatisch gesendet.
- Nachrichten an andere Personen werden nicht gespeichert. Sende sie erneut, wenn du wieder online bist.
- Was du in einen Chat eingibst, bleibt bis zum Senden auf dem Gerät gespeichert, auch wenn du die Seite neu lädst.
- Die App versucht es automatisch weiter. Über **Jetzt versuchen** kannst du es sofort erneut versuchen.
- Deine eigene Machine erreichst du über Tailscale. Auf einem Handy kann Tailscale im Hintergrund ausgeschaltet werden. Wenn deine Machine auf diesem Weg nicht erreichbar ist, steht in der Leiste **Tailscale ist möglicherweise auf diesem Gerät ausgeschaltet**. Auf einem Handy öffnet **Tailscale öffnen** Tailscale oder dessen Store-Seite, damit du es wieder einschalten kannst.
- Eine ausgelastete Machine braucht manchmal eine Weile, um zu antworten. Dann zeigt die App **Deine Machine antwortet langsam** an und behält die angezeigten Inhalte bei. Das bedeutet nicht, dass du offline bist.

## Weitere Geräte

Melde dich auf jedem Gerät auf dieselbe Weise an. Bei einer gehosteten Machine kannst du die Anmeldung mit einem Passkey pro Gerät beschleunigen: Wähle unter **Einstellungen** › **Konto** neben „Anmeldung“ die Option **Verwalten**.

Wie du Benachrichtigungen von deinem Android-Handy als Quelle ausliest, erfährst du unter [Android-Benachrichtigungen](android.md).
