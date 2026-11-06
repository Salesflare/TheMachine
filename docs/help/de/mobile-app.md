---
title: Die mobile App
area: getting-started
summary: The Machine als App auf iPhone und Android: Benachrichtigungen für deine Aufgaben und Teilen an The Machine aus jeder App.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
---
Die mobile App öffnet dein eigenes Dashboard, angemeldet wie im Web. Hol sie dir im [App Store](https://apps.apple.com/app/id6829875215) für iPhone und iPad oder bei [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) für Android.

Ab deinem ersten Besuch schlägt die kleine Aufgabe **Hol mehr aus The Machine heraus** oben in Aufgaben sie als Erstes vor. Im Browser auf dem Handy öffnet **Holen** ihren Store. Auf einem Computer zeigt sie einen QR-Code, der auf dem Handy den richtigen Store öffnet, mit Links zu beiden. In der App selbst erscheint sie nie.

## Verbinden

Auf einer gehosteten Machine meldet sich die App mit deinem Konto an. Auf einer selbst gehosteten öffnest du auf einem Computer **Einstellungen**, **Allgemein**: **Handy-App** zeigt einen Code. Installiere die App und scanne ihn dann mit der Kamera des Handys, oder tippe die Adresse darunter in die App ein. Die App fragt, bevor sie sich verbindet, und die eigene Anmeldung deiner Machine gilt weiterhin.

## Benachrichtigungen

Beim ersten Öffnen fragt die App, ob sie Benachrichtigungen senden darf. Tippe auf eine, um zu öffnen, worum es geht: Eine Aufgabe öffnet ihren Chat, der Morgen öffnet heute im **Kalender**, das Team-Briefing öffnet das Briefing dieser Fleet, und eine Frage aus der Fleet öffnet ihre Aufgabe. Kein Text einer Aufgabe geht über Apple, Google oder den Dienst von The Machine: Sie tragen nur eine feste Zeile, etwa „Eine Aufgabe braucht dich“.

Die App fragt dann deine eigene Machine nach dem Titel und dem nächsten Schritt der Aufgabe, etwa „Bereit: Sam antworten“ mit „An Sam senden: Dienstag 10:00 passt“. Der Morgen bekommt, was wartet, und die Uhrzeit deines ersten Termins, das Team-Briefing seine ersten Punkte. Erreicht sie deine Machine nicht, bleibt die feste Zeile. Auf Android steht da, wie viele warten, etwa „2 Aufgaben brauchen dich“.

Eine Benachrichtigung hat **Zurückstellen** (bis morgen) und **Als erledigt markieren**, und **Vorbereiten** bei einer Aufgabe, die noch nicht begonnen hat. Sie funktionieren, nachdem du das Handy entsperrt hast, ohne die App zu öffnen. Senden und letzte Schritte öffnen immer die App. Eine Benachrichtigung pro Aufgabe: Aus „Wird vorbereitet“ wird „Bereit“, und sie verschwindet, sobald die Aufgabe erledigt oder zurückgestellt ist, hier oder anderswo.

Ein letzter Schritt, den du bestätigt hast und der durchging, zeigt **Erledigt** mit dem, was passiert ist, bis du auf der Seite Aufgaben auf **Verstanden** tippst. Auf dem iPhone kann das warten, bis du die App das nächste Mal öffnest.

Ist **Text in Benachrichtigungen** unter **Einstellungen**, **Sicherheit** aus, bleibt es bei der festen Zeile. Blendet dein Handy sensible Inhalte von Benachrichtigungen auf dem Sperrbildschirm aus, steht dort nur die feste Zeile.

Es gelten dieselben Regeln wie für Push im Web: was du je Art unter [Benachrichtigungen](notifications.md) gewählt hast, deine [Arbeitszeiten](work-hours.md), und nichts, solange du ein Dashboard benutzt.

Jedes Handy mit der App steht unter **Einstellungen**, **Benachrichtigungen** als **Telefon mit der App**. **Entfernen** beendet seine Benachrichtigungen. Eine selbst gehostete Machine braucht dafür The Machine Network; die App funktioniert auch ohne Benachrichtigungen.

## An The Machine teilen

Tippe in einer beliebigen App auf Teilen und wähle The Machine. Eine **Neue Aufgabe** öffnet sich mit dem Text, dem Link oder den Dateien, die du geteilt hast. Prüf sie, füge auf Wunsch ein Datum hinzu, und füge sie hinzu. Vorher wird nichts hinzugefügt.

Eine Datei allein reicht, etwa eine Rechnung oder ein Brief. Deine Machine liest den Text eines PDFs und füllt die Aufgabe aus: was es ist, der nächste Schritt und sein Datum. Die Datei geht direkt an deine Machine und bleibt dort.

Auch das als App installierte Dashboard auf Android nimmt Geteiltes an: wähle es im Teilen-Menü genauso.

Tarife und Abrechnung zeigt die App nicht. **Konto öffnen** in **Einstellungen** bleibt, um dein Konto zu löschen.
