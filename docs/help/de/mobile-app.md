---
title: Die mobile App
area: getting-started
summary: The Machine als App für iPhone und Android: Benachrichtigungen zu deinen Aufgaben und Teilen von Inhalten aus jeder App an The Machine.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: 927fa395fe97f565
---
Die mobile App öffnet dein eigenes Dashboard mit derselben Anmeldung wie im Web. Lade sie im [App Store](https://apps.apple.com/app/id6829875215) für iPhone und iPad oder bei [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) für Android.

Die Aufgabe **Hol mehr aus The Machine heraus** oben in den Aufgaben weist dich auf die App hin. Im Browser eines Handys öffnet **Laden** den Store. Wenn dein Handy Desktop-Websites anzeigt, siehst du Links zu beiden Stores. Auf einem Computer wird ein QR-Code angezeigt, den du mit deinem Handy scannen kannst, sowie Links zu beiden Stores.

Auf jedem Handy öffnet [themachine.computer/app](https://themachine.computer/app) den passenden Store. Unter **Einstellungen** > **Apps** findest du oben Links zu beiden Stores oder auf einem Handy nur den Link zum Store deines Handys. Auf einem Computer installierst du das Dashboard mit **Computer** als App. Mehr dazu: [App installieren](phone-app.md).

## Verbinden

Auf einer gehosteten Machine meldet sich die App mit deinem Konto an. Bei einer selbst gehosteten Machine öffnest du am Computer **Einstellungen** > **Apps**. Unter den Store-Links zeigt **Nicht im Network?** einen Code an. Installiere die App und scanne den Code mit der Kamera deines Handys oder gib die darunter angezeigte Adresse in der App ein. Bevor die App eine Verbindung herstellt, fragt sie dich um Erlaubnis. Die Anmeldung bei deiner Machine ist weiterhin erforderlich.

Wenn du dich unter **Verbindungen** mit einem Dienst anmeldest (Shortcut, Notion, Slack, Zoom und anderen), öffnet sich das Anmeldefenster auf deinem Handy. Anschließend kehrst du zur App zurück. Die neue Verbindung erscheint automatisch unter **Verbindungen**.

Wenn die App deine Machine nicht erreichen kann, sagt sie dir Bescheid und versucht es automatisch noch einmal. Auf einem Mac öffnet die App die Seite außerdem automatisch wieder, wenn ihr Fenster nach dem Ruhezustand leer ist. Eine Chat-Nachricht, die du gerade geschrieben hast, erscheint dann ebenfalls wieder. Auf einem Mac oder iPad mit Tastatur lädt Cmd+R die Seite erneut.

## Benachrichtigungen

Beim ersten Öffnen fragt die App, ob sie dir Benachrichtigungen senden darf. Tippe auf eine Benachrichtigung, um den zugehörigen Inhalt zu öffnen: Eine Aufgabe erscheint hervorgehoben in deiner Liste, die Morgenübersicht öffnet den heutigen Tag im **Kalender**, das Team-Briefing öffnet die Aufgaben und eine Frage aus einer Fleet öffnet die zugehörige Aufgabe. Der Text einer Aufgabe wird nicht über Apple, Google oder den Dienst von The Machine weitergeleitet. Diese übertragen nur einen festen Text, zum Beispiel „Eine Aufgabe braucht deine Aufmerksamkeit“.

Anschließend fragt die App deine Machine nach dem Titel und dem nächsten Schritt der Aufgabe, zum Beispiel „Sam antworten“ und „Antworte Sam: Dienstag, 10:00 Uhr passt“. Die Morgenübersicht zeigt an, was ansteht, sowie die Uhrzeit deines ersten Termins. Das Team-Briefing zeigt die ersten Punkte und eine Fleet-Aktualisierung zeigt, was passiert ist. Wenn die App deine Machine nicht erreichen kann, bleibt der feste Text stehen. Auf Android wird angezeigt, wie viele Aufgaben anstehen, zum Beispiel „2 Aufgaben brauchen deine Aufmerksamkeit“.

Eine Benachrichtigung enthält **Zurückstellen** (bis morgen) und **Erledigt markieren** sowie **Ausführen**, wenn du mit einer Aufgabe noch nicht begonnen hast. Die Aktionen funktionieren, sobald du dein Handy entsperrt hast, ohne dass du die App öffnen musst. Zum Senden und für die letzten Schritte musst du immer die App öffnen. Für jede Aufgabe gibt es nur eine Benachrichtigung: „Wird vorbereitet“ wird zu „Bereit“. Sobald die Aufgabe erledigt oder zurückgestellt ist, verschwindet die Benachrichtigung, egal ob du das hier oder an anderer Stelle getan hast.

Wenn ein von dir bestätigter Schritt ausgeführt wurde, zeigt die Benachrichtigung **Erledigt** und was passiert ist. Sie bleibt bestehen, bis du in den Aufgaben auf **Verstanden** tippst. Auf dem iPhone kannst du das auch erst tun, wenn du die App das nächste Mal öffnest.

Wenn du **Text in Benachrichtigungen** unter **Einstellungen** > **Sicherheit** deaktivierst, wird weiterhin der feste Text angezeigt. Dasselbe gilt, wenn dein Sperrbildschirm Benachrichtigungsinhalte ausblendet. Wenn keine weiteren Informationen angezeigt werden können, heißt es „Zum Öffnen tippen“. Kann dein Handy beim Eintreffen einer Benachrichtigung deine Machine nicht erreichen, werden die Details angezeigt, sobald es wieder online ist.

Es gelten dieselben Regeln wie für Push-Benachrichtigungen im Web: deine Auswahl pro Benachrichtigungstyp unter [Benachrichtigungen](notifications.md), deine [Arbeitszeiten](work-hours.md) und keine Benachrichtigungen, während du ein Dashboard verwendest.

Jedes Handy mit der App wird unter **Einstellungen** > **Benachrichtigungen** als **Handy mit der App** angezeigt. Mit **Entfernen** schaltest du die Benachrichtigungen für dieses Handy aus. Für Benachrichtigungen auf einer selbst gehosteten Machine ist The Machine Network erforderlich. Die App funktioniert auch ohne sie.

## Mit The Machine teilen

Tippe in einer beliebigen App auf „Teilen“ und wähle The Machine aus. Daraufhin öffnet sich eine **Neue Aufgabe** mit dem geteilten Text, Link oder den Dateien. Überprüfe den Inhalt, füge bei Bedarf ein Datum hinzu und erstelle die Aufgabe. Bis dahin wird nichts hinzugefügt.

Auch eine einzelne Datei, zum Beispiel eine Rechnung oder ein Brief, genügt. Deine Machine liest den Text einer PDF-Datei und füllt die Aufgabe aus: worum es geht, was als Nächstes zu tun ist und wann. Die Datei wird direkt an deine Machine gesendet und bleibt dort.

Das auf Android als App installierte Dashboard kann ebenfalls Inhalte empfangen. Wähle es wie gewohnt im Teilen-Menü aus.

Tarife und Abrechnung werden in der App nicht angezeigt. Unter **Einstellungen** bleibt **Konto öffnen** verfügbar, um dein Konto zu löschen.
