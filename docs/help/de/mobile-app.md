---
title: Die mobile App
area: getting-started
summary: The Machine als App für iPhone und Android: Benachrichtigungen zu deinen Aufgaben und Teilen mit The Machine aus jeder App.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: 0d4d41134db91fcc
---
Die mobile App öffnet dein persönliches Dashboard, in dem du wie im Web angemeldet bist. Hol dir die App im [App Store](https://apps.apple.com/app/id6829875215) für iPhone und iPad oder bei [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) für Android.

Die Aufgabe **Hol mehr aus The Machine heraus** oben in **Aufgaben** schlägt dir die App vor. Im Browser eines Smartphones öffnet **Holen** den Store. Wenn dein Smartphone Desktop-Websites anzeigt, siehst du Links zu beiden Stores. Auf einem Computer wird ein QR-Code angezeigt, den du mit deinem Smartphone scannen kannst, sowie Links zu beiden Stores.

Auf jedem Smartphone öffnet [themachine.computer/app](https://themachine.computer/app) den passenden Store. Unter **Einstellungen** und **Apps** findest du oben Links zu beiden Stores oder auf einem Smartphone nur zum Store für dein Gerät. Auf einem Computer installiert **Computer** das Dashboard als App: Lies dazu [App installieren](phone-app.md).

## Verbinden

Bei einer gehosteten Machine meldet sich die App mit deinem Konto an. Bei einer selbst gehosteten Machine öffne auf einem Computer **Einstellungen** und **Apps**: Unter den Stores findest du unter **Nicht im Network?** einen Code. Installiere die App und scanne den Code mit der Kamera deines Smartphones oder gib die darunter angezeigte Adresse in der App ein. Die App fragt nach, bevor sie eine Verbindung herstellt. Die Anmeldung bei deiner Machine bleibt weiterhin erforderlich.

## Benachrichtigungen

Beim ersten Öffnen fragt die App, ob sie Benachrichtigungen senden darf. Tippe auf eine Benachrichtigung, um den passenden Inhalt zu öffnen: Eine Aufgabe wird in deiner Liste hervorgehoben, die Morgenübersicht öffnet den heutigen Tag im **Kalender**, das Team-Briefing öffnet **Aufgaben** und eine Frage in Fleet öffnet die zugehörige Aufgabe. Der Text einer Aufgabe wird nicht über Apple, Google oder den Dienst von The Machine übertragen. Darüber wird nur ein fester Text gesendet, zum Beispiel „Eine Aufgabe braucht dich“.

Die App fragt dann deine Machine nach dem Titel und dem nächsten Schritt der Aufgabe, zum Beispiel „Sam antworten“ und „An Sam senden: Dienstag, 10:00 Uhr passt“. Die Morgenübersicht zeigt, was ansteht, und die Uhrzeit deines ersten Meetings. Das Team-Briefing zeigt seine ersten Punkte und ein Fleet-Update, was passiert ist. Wenn die App deine Machine nicht erreicht, bleibt der feste Text stehen. Unter Android wird angezeigt, wie viele Aufgaben anstehen, zum Beispiel „2 Aufgaben brauchen dich“.

Eine Benachrichtigung enthält **Zurückstellen** (bis morgen) und **Als erledigt markieren** sowie **Ausführen**, wenn du eine Aufgabe noch nicht begonnen hast. Die Aktionen funktionieren, sobald du dein Smartphone entsperrt hast, ohne dass du die App öffnen musst. Zum Senden und für die letzten Schritte wird immer die App geöffnet. Pro Aufgabe gibt es eine Benachrichtigung: „Wird vorbereitet“ ändert sich zu „Bereit“. Sie verschwindet, sobald die Aufgabe erledigt oder zurückgestellt ist, egal ob hier oder anderswo.

Wenn ein von dir bestätigter Schritt ausgeführt wird, zeigt die Benachrichtigung **Erledigt** und was passiert ist. Sie bleibt sichtbar, bis du in **Aufgaben** auf **Verstanden** tippst. Auf dem iPhone kannst du damit bis zum nächsten Öffnen der App warten.

Wenn du **Text in Benachrichtigungen** unter **Einstellungen** und **Sicherheit** deaktivierst, wird weiterhin nur der feste Text angezeigt. Dasselbe gilt, wenn dein Sperrbildschirm den Inhalt von Benachrichtigungen ausblendet. Wenn nichts angezeigt werden kann, steht dort „Zum Öffnen tippen“. Wenn dein Smartphone deine Machine beim Eingang einer Benachrichtigung nicht erreicht, zeigt es die Details an, sobald es wieder online ist.

Für diese Benachrichtigungen gelten dieselben Regeln wie für Push-Benachrichtigungen im Web: deine Auswahl pro Art unter [Benachrichtigungen](notifications.md), deine [Arbeitszeiten](work-hours.md) und keine Benachrichtigungen, während du ein Dashboard verwendest.

Jedes Smartphone mit der App wird unter **Einstellungen** und **Benachrichtigungen** als **Telefon mit der App** angezeigt. Mit **Entfernen** werden die Benachrichtigungen dafür deaktiviert. Für Benachrichtigungen auf einer selbst gehosteten Machine ist The Machine Network erforderlich. Die App funktioniert auch ohne sie.

## Mit The Machine teilen

Tippe in einer beliebigen App auf **Teilen** und wähle The Machine aus. Es öffnet sich eine **Neue Aufgabe** mit dem geteilten Text, Link oder den geteilten Dateien. Prüfe sie, füge bei Bedarf ein Datum hinzu und füge sie hinzu. Es wird nichts hinzugefügt, bevor du das tust.

Auch eine einzelne Datei reicht, zum Beispiel eine Rechnung oder ein Brief. Deine Machine liest den Text einer PDF aus und füllt die Aufgabe aus: worum es geht, was als Nächstes zu tun ist und welches Datum dafür gilt. Die Datei wird direkt an deine Machine gesendet und bleibt dort.

Auch das auf Android als App installierte Dashboard kann Inhalte entgegennehmen: Wähle es wie gewohnt im Teilen-Menü aus.

Tarife und Abrechnung werden in der App nicht angezeigt. **Konto öffnen** unter **Einstellungen** bleibt verfügbar, damit du dein Konto löschen kannst.
