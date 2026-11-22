---
title: Die mobile App
area: getting-started
summary: The Machine als App auf iPhone und Android: Benachrichtigungen zu deinen Aufgaben und Teilen von Inhalten aus jeder App mit The Machine.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: 672364a90f92ef8f
---
Die mobile App öffnet dein persönliches Dashboard. Du bist dort wie im Web angemeldet. Hol sie dir im [App Store](https://apps.apple.com/app/id6829875215) für iPhone und iPad oder bei [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) für Android.

Die Aufgabe **Hol mehr aus The Machine heraus** oben in den Aufgaben empfiehlt dir die App. Im Browser deines Handys öffnet **Laden** den Store. Wenn dein Handy Desktop-Websites anzeigt, siehst du Links zu beiden Stores. Auf einem Computer wird ein QR-Code angezeigt, den du mit deinem Handy scannen kannst, sowie Links zu beiden Stores.

Auf jedem Handy öffnet [themachine.computer/app](https://themachine.computer/app) den passenden Store. Unter **Einstellungen**, **Apps** findest du oben Links zu beiden Stores oder auf einem Handy nur den Link zum Store deines Handys. Auf einem Computer installierst du mit **Computer** das Dashboard als App. Weitere Informationen findest du unter [App installieren](phone-app.md).

## Verbinden

Bei einer gehosteten Machine meldest du dich in der App mit deinem Konto an. Bei einer selbst gehosteten Machine öffnest du auf einem Computer **Einstellungen**, **Apps**. Unter den Store-Links findest du unter **Nicht im Network?** einen Code. Installiere die App und scanne den Code mit der Kamera deines Handys oder gib die darunter angezeigte Adresse in der App ein. Bevor die App eine Verbindung herstellt, fragt sie dich um Erlaubnis. Die Anmeldung bei deiner Machine ist weiterhin erforderlich.

Wenn du dich bei einem Dienst unter **Verbindungen** (Shortcut, Notion, Slack, Zoom und andere) **Mit ... anmelden** möchtest, öffnet sich die Anmeldemaske deines Handys. Danach kehrst du zur App zurück. Die neue Verbindung wird automatisch unter **Verbindungen** angezeigt.

Wenn die App deine Machine nicht erreichen kann, sagt sie dir Bescheid und versucht es automatisch erneut. Auf einem Mac oder iPad mit Tastatur lädt Cmd+R die Seite erneut.

## Benachrichtigungen

Beim ersten Öffnen fragt die App, ob sie Benachrichtigungen senden darf. Tippe auf eine Benachrichtigung, um den zugehörigen Inhalt zu öffnen: Eine Aufgabe wird hervorgehoben in deiner Liste angezeigt, die morgendliche Zusammenfassung öffnet den heutigen Tag im **Kalender**, das Team-Briefing öffnet die Aufgaben und eine Frage aus Fleet öffnet die zugehörige Aufgabe. Der Text einer Aufgabe wird nicht über Apple, Google oder den Dienst von The Machine übertragen. Diese Dienste übermitteln nur einen festen Text, zum Beispiel „Eine Aufgabe braucht dich“.

Anschließend fragt die App deine Machine nach dem Titel und dem nächsten Schritt der Aufgabe, zum Beispiel „Sam antworten“ und „Sam schreiben: Dienstag um 10:00 Uhr passt“. Die morgendliche Zusammenfassung zeigt, was ansteht, und die Uhrzeit deines ersten Meetings, das Team-Briefing seine ersten Punkte und ein Fleet-Update, was passiert ist. Wenn die App deine Machine nicht erreichen kann, bleibt der feste Text stehen. Auf Android wird angezeigt, wie viele Aufgaben anstehen, zum Beispiel „2 Aufgaben brauchen dich“.

Eine Benachrichtigung enthält **Zurückstellen** (bis morgen) und **Als erledigt markieren** sowie **Ausführen** für eine noch nicht begonnene Aufgabe. Diese Aktionen funktionieren, nachdem du dein Handy entsperrt hast, auch ohne die App zu öffnen. Zum Senden und für letzte Schritte wird immer die App geöffnet. Pro Aufgabe gibt es eine Benachrichtigung: „Wird vorbereitet“ wird zu „Bereit“. Die Benachrichtigung verschwindet, sobald die Aufgabe erledigt oder zurückgestellt wurde, egal ob hier oder anderswo.

Wenn ein von dir bestätigter Schritt ausgeführt wurde, zeigt die Benachrichtigung **Erledigt** und was passiert ist. Sie bleibt so lange stehen, bis du unter Aufgaben auf **Verstanden** tippst. Auf dem iPhone kann das bis zum nächsten Öffnen der App warten.

Wenn **Text in Benachrichtigungen** unter **Einstellungen**, **Sicherheit** deaktiviert ist, bleibt der feste Text stehen. Dasselbe gilt, wenn dein Sperrbildschirm den Inhalt von Benachrichtigungen ausblendet. Wenn eine Benachrichtigung nichts anzeigen kann, steht dort „Zum Öffnen tippen“. Kann dein Handy deine Machine beim Eingang einer Benachrichtigung nicht erreichen, werden die Details angezeigt, sobald es wieder online ist.

Für sie gelten dieselben Regeln wie für Push-Benachrichtigungen im Web: deine Einstellungen pro Benachrichtigungstyp unter [Benachrichtigungen](notifications.md), deine [Arbeitszeiten](work-hours.md) und keine Benachrichtigungen, während du ein Dashboard verwendest.

Jedes Handy mit der App wird unter **Einstellungen**, **Benachrichtigungen** als **Handy mit der App** angezeigt. Mit **Entfernen** werden die Benachrichtigungen für dieses Handy ausgeschaltet. Für Benachrichtigungen auf einer selbst gehosteten Machine ist The Machine Network erforderlich. Die App funktioniert auch ohne sie.

## Mit The Machine teilen

Tippe in einer beliebigen App auf „Teilen“ und wähle The Machine aus. Daraufhin öffnet sich **Neue Aufgabe** mit dem Text, Link oder den Dateien, die du geteilt hast. Überprüfe den Inhalt, füge bei Bedarf ein Datum hinzu und speichere die Aufgabe. Bis dahin wird nichts hinzugefügt.

Auch eine einzelne Datei reicht, zum Beispiel eine Rechnung oder ein Brief. Deine Machine liest den Text einer PDF-Datei und ergänzt die Aufgabe um den Inhalt, den nächsten Schritt und das Datum. Die Datei wird direkt an deine Machine gesendet und bleibt dort.

Das Dashboard, das auf Android als App installiert ist, kann ebenfalls Inhalte empfangen: Wähle es wie gewohnt im Teilen-Menü aus.

Tarife und Abrechnung werden in der App nicht angezeigt. **Konto öffnen** findest du weiterhin unter **Einstellungen**, um dein Konto zu löschen.
