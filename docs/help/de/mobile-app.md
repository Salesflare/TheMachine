---
title: Die mobile App
area: getting-started
summary: The Machine als App für iPhone und Android: Benachrichtigungen zu deinen Aufgaben und Teilen von Inhalten aus jeder App an The Machine.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: f622bdc266f69965
---
Die mobile App öffnet dein persönliches Dashboard, mit derselben Anmeldung wie im Web. Hol sie dir im [App Store](https://apps.apple.com/app/id6829875215) für iPhone und iPad oder bei [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) für Android.

Die Aufgabe **Hol mehr aus The Machine heraus** oben in der Aufgabenliste schlägt dir die App vor. Im Browser deines Telefons öffnet **Holen** den Store. Wenn dein Telefon Desktop-Websites anzeigt, werden beide Store-Links angezeigt. Auf einem Computer wird ein QR-Code angezeigt, den du mit deinem Telefon scannen kannst, sowie Links zu beiden Stores.

Auf jedem Telefon öffnet [themachine.computer/app](https://themachine.computer/app) den passenden Store. Unter **Einstellungen** > **Apps** findest du oben Links zu beiden Stores oder auf einem Telefon nur zum Store deines Telefons. Auf einem Computer installierst du mit **Computer** das Dashboard als App. Weitere Informationen findest du unter [App installieren](phone-app.md).

## Verbinden

Auf einer gehosteten Machine meldet sich die App mit deinem Konto an. Bei einer selbst gehosteten Machine öffne auf einem Computer **Einstellungen** > **Apps**. Unter den Stores findest du unter **Nicht im Network?** einen Code. Installiere die App und scanne den Code mit der Kamera deines Telefons oder gib die darunter angezeigte Adresse in der App ein. Die App fragt dich, bevor sie eine Verbindung herstellt. Die Anmeldung bei deiner Machine ist weiterhin erforderlich.

Wenn du unter **Verbindungen** bei einem Dienst (Shortcut, Notion, Slack, Zoom und anderen) **Anmelden mit** auswählst, öffnet sich das Anmeldefenster deines Telefons. Sobald du dich angemeldet hast, kehrst du zur App zurück und die neue Verbindung erscheint automatisch unter **Verbindungen**.

## Benachrichtigungen

Beim ersten Öffnen fragt die App, ob sie Benachrichtigungen senden darf. Tippe auf eine Benachrichtigung, um den entsprechenden Inhalt zu öffnen: Eine Aufgabe wird hervorgehoben in deiner Liste angezeigt, die Morgenübersicht öffnet den heutigen Tag im **Kalender**, das Teambriefing öffnet die Aufgaben und eine Fleet-Frage öffnet die zugehörige Aufgabe. Der Text einer Aufgabe wird weder über Apple noch über Google oder den Dienst von The Machine übertragen. Diese Dienste übermitteln nur einen festen Text, zum Beispiel „Eine Aufgabe wartet auf dich“.

Anschließend fragt die App deine Machine nach dem Titel und dem nächsten Schritt der Aufgabe, zum Beispiel „Sam antworten“ mit „Sam schreiben: Dienstag um 10:00 Uhr passt“. Die Morgenübersicht zeigt, was ansteht, und die Uhrzeit deines ersten Meetings. Das Teambriefing zeigt seine ersten Punkte und ein Fleet-Update, was passiert ist. Wenn die App deine Machine nicht erreicht, bleibt der feste Text stehen. Auf Android wird angezeigt, wie viele Aufgaben warten, zum Beispiel „2 Aufgaben warten auf dich“.

Eine Benachrichtigung enthält **Zurückstellen** (bis morgen) und **Als erledigt markieren** sowie **Ausführen** für eine Aufgabe, mit der du noch nicht begonnen hast. Diese Optionen funktionieren, sobald du dein Telefon entsperrt hast, ohne dass du die App öffnen musst. Zum Senden und für die letzten Schritte wird immer die App geöffnet. Pro Aufgabe gibt es eine Benachrichtigung: „Wird vorbereitet“ wird zu „Bereit“. Sie verschwindet, sobald die Aufgabe erledigt oder zurückgestellt ist, egal ob hier oder anderswo.

Wenn ein von dir bestätigter Schritt ausgeführt wurde, zeigt die Benachrichtigung **Erledigt** und was passiert ist, bis du unter Aufgaben auf **Verstanden** tippst. Auf dem iPhone kannst du damit warten, bis du die App das nächste Mal öffnest.

Wenn **Text in Benachrichtigungen** unter **Einstellungen** > **Sicherheit** deaktiviert ist, wird weiterhin der feste Text angezeigt. Dasselbe gilt, wenn dein Sperrbildschirm Benachrichtigungsinhalte ausblendet. Wenn nichts angezeigt werden kann, steht dort „Zum Öffnen tippen“. Wenn dein Telefon beim Eingang einer Benachrichtigung deine Machine nicht erreicht, werden die Details angezeigt, sobald es wieder online ist.

Es gelten dieselben Regeln wie für Push-Benachrichtigungen im Web: deine Auswahl für die einzelnen Arten unter [Benachrichtigungen](notifications.md), deine [Arbeitszeiten](work-hours.md) und keine Benachrichtigungen, während du ein Dashboard verwendest.

Jedes Telefon mit der App wird unter **Einstellungen** > **Benachrichtigungen** als **Telefon mit der App** angezeigt. Mit **Entfernen** werden die Benachrichtigungen für dieses Telefon deaktiviert. Für Benachrichtigungen auf einer selbst gehosteten Machine ist The Machine Network erforderlich. Die App funktioniert auch ohne sie.

## An The Machine teilen

Tippe in einer beliebigen App auf „Teilen“ und wähle The Machine aus. Es öffnet sich eine **Neue Aufgabe** mit dem Text, Link oder den Dateien, die du geteilt hast. Überprüfe sie, füge bei Bedarf ein Datum hinzu und erstelle sie. Bis dahin wird nichts hinzugefügt.

Es reicht, nur eine Datei zu teilen, zum Beispiel eine Rechnung oder einen Brief. Deine Machine liest den Text in einer PDF-Datei und füllt die Aufgabe aus: worum es geht, was als Nächstes zu tun ist und welches Datum gilt. Die Datei wird direkt an deine Machine gesendet und bleibt dort.

Auch das auf Android als App installierte Dashboard kann geteilte Inhalte empfangen. Wähle es wie gewohnt im Teilen-Menü aus.

Tarife und Abrechnungsinformationen werden in der App nicht angezeigt. **Konto öffnen** unter **Einstellungen** bleibt verfügbar, um dein Konto zu löschen.
