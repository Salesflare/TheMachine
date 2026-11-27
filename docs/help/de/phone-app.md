---
title: App installieren und Benachrichtigungen einschalten
area: getting-started
summary: Installiere The Machine auf deinem Handy oder Computer und erhalte für jede Aufgabe eine Benachrichtigung. Telegram ist optional.
covers: phone-app
code: manifest.webmanifest, sw.js, dashboard.html
order: 3
translated: c1ead6181c38a6d8
---
Installiere The Machine als App auf deinem Handy oder Computer, um innerhalb deiner [Arbeitszeiten](work-hours.md) eine Benachrichtigung für jede Aufgabe, jedes Ergebnis und jede Erinnerung zu erhalten. Lege unter [Benachrichtigungen](notifications.md) fest, was gesendet wird.

Die Aufgabe **Hol mehr aus The Machine heraus** oben unter „Aufgaben“ enthält für jede Option eine Zeile: **Hol dir die App fürs Handy** (siehe [Die mobile App](mobile-app.md)), **Desktop-App herunterladen** (siehe [Die Desktop-App](desktop-app.md)), **Benachrichtigungen einschalten** und **Auf diesem Computer installieren**. Angezeigt wird nur, was auf dem jeweiligen Gerät noch fehlt. Über das × in einer Zeile kannst du sie schließen. Dieselben Optionen findest du unter **Einstellungen**, **Allgemein**, **Dieses Gerät**.

**Auf diesem Computer installieren** wird nur auf einem Computer ohne Desktop-App angezeigt, zum Beispiel auf einem Chromebook.

In der Handy-App wird bei ausgeschalteten Benachrichtigungen **Lass dich benachrichtigen, wenn etwas deine Aufmerksamkeit braucht.** angezeigt. **Einschalten** fragt die Berechtigung am Handy ab oder öffnet die Einstellungen. Mit **×** blendest du den Hinweis 7 Tage lang aus.

## Auf einem Computer (Chrome oder Edge)

1. Öffne dein Dashboard und klicke unter „Einstellungen“ → „Allgemein“ → „Dieses Gerät“ auf **App installieren**. Auf einem Chromebook kannst du stattdessen in der entsprechenden Aufgabe auf **Installieren** klicken.
2. The Machine öffnet sich in einem eigenen Fenster. Heft sie an die Taskleiste oder das Dock an.
3. Klicke in der Zeile auf **Einschalten** und erlaube Benachrichtigungen. Sofort wird eine Testbenachrichtigung angezeigt.

## Auf einem Mac (Safari)

1. Wähle in der Menüleiste von Safari „Ablage“ und dann „Zum Dock hinzufügen“.
2. Öffne The Machine über das Dock und klicke auf **Einschalten**.

## In Firefox

Firefox kann die App nicht installieren. Benachrichtigungen funktionieren im Tab: Klicke in der Zeile auf **Einschalten** oder in den Einstellungen auf die Glocke neben **Benachrichtigungen**.

## Auf einem iPhone oder iPad

1. Öffne dein Dashboard in Safari. Dafür brauchst du iOS 16.4 oder neuer.
2. Tippe auf „Teilen“ und dann auf „Zum Home-Bildschirm“.
3. Öffne The Machine über den Home-Bildschirm und tippe auf **Einschalten**.

Benachrichtigungen funktionieren nur in der App auf dem Home-Bildschirm, nicht in einem Safari-Tab.

## Auf Android

1. Öffne dein Dashboard in Chrome, öffne das Menü und tippe auf **App installieren**.
2. Öffne die App über den Startbildschirm und tippe auf **Einschalten**.

## Prüfen oder ändern

Unter **Einstellungen**, **Allgemein**, **Dieses Gerät** kannst du über die Glocke neben **Benachrichtigungen** die Benachrichtigungen nur für dieses Gerät ein- oder ausschalten. Mit **Test senden** schickst du eine Testbenachrichtigung an dieses Gerät.

Keine Benachrichtigungen? Klicke am Computer links neben der Adresszeile auf das Symbol und erlaube Benachrichtigungen. Öffne auf einem iPhone die App „Einstellungen“ und wähle „Mitteilungen“ und dann The Machine.

## Schnell öffnen

Die App zeigt sofort deine zuletzt verwendeten Aufgaben und aktualisiert sie anschließend. Diese Kopie bleibt höchstens 7 Tage lang verschlüsselt auf dem Gerät und wird gelöscht, wenn du dich abmeldest.

## Ohne Internet oder bei schlechtem WLAN

Im Flugzeug oder Zug funktioniert das Dashboard weiterhin. Oben wird eine Leiste mit dem Status **Offline** und dem Zeitpunkt der letzten Aktualisierung angezeigt. Deine Aufgaben, die zugehörigen Chats, der Kalender und die Graph-Listen lassen sich vom Gerät aus öffnen.

- **Zurückstellen**, **Nicht nötig**, **Als erledigt markieren**, **Wieder öffnen** und Chatnachrichten an The Machine werden mit **Abbrechen** auf dem Gerät vorgemerkt. Sobald du wieder online bist, werden sie automatisch gesendet.
- Nachrichten an andere Personen werden nicht vorgemerkt. Sende sie erneut, wenn du wieder online bist.
- Was du in einen Chat eingibst, bleibt auf dem Gerät, bis du es sendest, auch nach einem Neuladen.
- Die App versucht es automatisch immer wieder. Mit **Jetzt versuchen** startest du einen neuen Versuch.
- Auf deine eigene Machine greifst du über Tailscale zu. Auf einem Handy kann Tailscale im Hintergrund ausgeschaltet werden. Wenn deine Machine auf diesem Weg nicht erreichbar ist, steht in der Leiste **Tailscale ist auf diesem Gerät möglicherweise ausgeschaltet**. Auf einem Handy öffnet **Tailscale öffnen** die App oder ihre Store-Seite, damit du Tailscale wieder einschalten kannst.
- Eine ausgelastete Machine braucht manchmal länger für eine Antwort. Dann zeigt die App **Deine Machine antwortet langsam** an und behält die angezeigten Inhalte bei. Das bedeutet nicht, dass du offline bist.

## Weitere Geräte

Melde dich auf jedem Gerät auf dieselbe Weise an. Bei einer gehosteten Machine kannst du dich schneller anmelden, wenn du pro Gerät einen Passkey verwendest: Gehe in **Einstellungen** › **Konto** und klicke neben „Anmeldung“ auf **Verwalten**.

Wie du Benachrichtigungen von deinem Android-Handy als Quelle einliest, erfährst du unter [Android-Benachrichtigungen](android.md).
