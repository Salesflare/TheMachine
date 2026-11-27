---
title: Die mobile App
area: getting-started
summary: The Machine als App für iPhone und Android: Benachrichtigungen zu deinen Aufgaben und Inhalte aus jeder App mit The Machine teilen.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: aaf34f864dadf180
---
Die mobile App öffnet dein persönliches Dashboard, mit derselben Anmeldung wie im Web. Lade sie für iPhone und iPad im [App Store](https://apps.apple.com/app/id6829875215) oder für Android bei [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) herunter.

Die Aufgabe **Hol mehr aus The Machine heraus** oben unter Aufgaben empfiehlt die App. Im Browser deines Handys öffnet **Laden** den Store. Wenn dein Handy Desktop-Websites anzeigt, siehst du Links zu beiden Stores. Auf einem Computer wird ein QR-Code angezeigt, den du mit deinem Handy scannen kannst, sowie Links zu beiden Stores.

Auf jedem Handy öffnet [themachine.computer/app](https://themachine.computer/app) den passenden Store. Unter **Einstellungen**, **Apps** findest du oben Links zu beiden Stores oder auf einem Handy nur den Link zum Store deines Handys. Auf einem Computer findest du dort auch die Desktop-App für Windows, Mac und Linux: siehe [Die Desktop-App](desktop-app.md).

## Verbinden

Auf einer gehosteten Machine meldest du dich in der App mit deinem Konto an. Bei einer selbst gehosteten Machine öffne auf einem Computer **Einstellungen**, **Apps**. Unter den Stores findest du **Nicht im Network?** mit einem Code. Installiere die App und scanne den Code mit der Kamera deines Handys oder gib die darunter angezeigte Adresse in der App ein. Die App fragt nach, bevor sie die Verbindung herstellt. Die Anmeldung bei deiner Machine ist weiterhin erforderlich.

Über **Anmelden mit** einem Dienst unter **Verbindungen** (Shortcut, Notion, Slack, Zoom und andere) öffnet sich das Anmeldefenster deines Handys. Danach bist du wieder in der App. Die neue Verbindung erscheint automatisch unter **Verbindungen**.

Wenn die App deine Machine nicht erreichen kann, weist sie dich darauf hin und versucht es automatisch erneut. Auf einem Mac öffnet die App die Seite außerdem automatisch wieder, wenn ihr Fenster nach dem Ruhezustand leer ist. Auch eine Chat-Nachricht, die du gerade geschrieben hast, wird wieder angezeigt. Auf einem Mac oder einem iPad mit Tastatur lädt Cmd+R die Seite neu.

## Benachrichtigungen

Beim ersten Öffnen fragt die App, ob sie Benachrichtigungen senden darf. Tippe auf eine Benachrichtigung, um den entsprechenden Inhalt zu öffnen: Eine Aufgabe wird hervorgehoben in deiner Liste angezeigt, die Morgenübersicht öffnet den heutigen Tag im **Kalender**, das Team-Briefing öffnet Aufgaben und eine Fleet-Frage öffnet die zugehörige Aufgabe. Der Text einer Aufgabe wird nicht über Apple, Google oder den Dienst von The Machine weitergegeben. Diese übertragen nur einen festen Text, zum Beispiel „Eine Aufgabe wartet auf dich“.

Anschließend fragt die App deine eigene Machine nach dem Titel und dem nächsten Schritt der Aufgabe, zum Beispiel „Sam antworten“ und „Sam schreiben: Dienstag um 10:00 Uhr passt“. Die Morgenübersicht zeigt, was ansteht, und die Uhrzeit deines ersten Meetings. Das Team-Briefing zeigt seine ersten Punkte und ein Fleet-Update, was passiert ist. Wenn die App deine Machine nicht erreichen kann, bleibt der feste Text stehen. Auf Android wird angezeigt, wie viele Aufgaben anstehen, zum Beispiel „2 Aufgaben warten auf dich“.

Eine Benachrichtigung bietet **Zurückstellen** (bis morgen), **Als erledigt markieren** und **Ausführen**, wenn du noch nicht mit einer Aufgabe begonnen hast. Diese Aktionen funktionieren, sobald du dein Handy entsperrt hast, auch ohne die App zu öffnen. Zum Senden und für die letzten Schritte musst du immer die App öffnen. Für jede Aufgabe gibt es nur eine Benachrichtigung: „Wird vorbereitet“ wird zu „Bereit“. Sobald die Aufgabe erledigt oder zurückgestellt ist, verschwindet die Benachrichtigung, egal ob du das hier oder anderswo machst.

Wenn ein von dir bestätigter Schritt ausgeführt wurde, zeigt die Benachrichtigung **Erledigt** und was passiert ist. Sie bleibt stehen, bis du unter Aufgaben auf **Verstanden** tippst. Auf dem iPhone kannst du das auch beim nächsten Öffnen der App erledigen.

Wenn **Text in Benachrichtigungen** unter **Einstellungen**, **Sicherheit** deaktiviert ist, bleibt der feste Text stehen. Das gilt auch, wenn dein Sperrbildschirm den Inhalt von Benachrichtigungen ausblendet. Wenn eine Benachrichtigung nichts anzeigen darf, steht dort „Zum Öffnen tippen“. Kann dein Handy deine Machine beim Eingang einer Benachrichtigung nicht erreichen, werden die Details angezeigt, sobald die Verbindung wiederhergestellt ist.

Für Benachrichtigungen gelten dieselben Regeln wie für Push-Benachrichtigungen im Web: deine Auswahl für die jeweilige Art unter [Benachrichtigungen](notifications.md), deine [Arbeitszeiten](work-hours.md) und keine Benachrichtigungen, während du ein Dashboard verwendest.

Jedes Handy mit der App wird unter **Einstellungen**, **Benachrichtigungen** als **Handy mit der App** angezeigt. Mit **Entfernen** schaltest du die Benachrichtigungen für dieses Handy aus. Eine selbst gehostete Machine benötigt dafür The Machine Network. Die App funktioniert auch ohne Benachrichtigungen.

## Mit The Machine teilen

Tippe in einer beliebigen App auf „Teilen“ und wähle The Machine aus. Es öffnet sich **Neue Aufgabe** mit dem Text, Link oder den Dateien, die du geteilt hast. Prüfe die Angaben, füge bei Bedarf ein Datum hinzu und speichere die Aufgabe. Sie wird erst dann hinzugefügt.

Auch eine einzelne Datei genügt, zum Beispiel eine Rechnung oder ein Brief. Deine Machine liest den Text einer PDF-Datei und füllt die Aufgabe aus: worum es geht, was als Nächstes zu tun ist und das Datum. Die Datei wird direkt an deine Machine gesendet und bleibt dort.

Das auf Android als App installierte Dashboard kann ebenfalls Inhalte empfangen: Wähle es wie gewohnt im Teilen-Menü aus.

Tarife und Abrechnung werden in der App nicht angezeigt. **Konto öffnen** findest du weiterhin unter **Einstellungen**, um dein Konto zu löschen.
