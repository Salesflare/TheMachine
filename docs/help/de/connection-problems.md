---
title: Eine Verbindung braucht deine Hilfe
area: troubleshooting
summary: Eine Quelle zeigt „Braucht deine Hilfe“ an oder liefert nichts mehr. Das kannst du tun.
covers:
code: onboarding.py, dashboard.html, assistant.py
order: 1
translated: cc4b227abd053022
---
## Status prüfen

Öffne **Verbindungen**. Bei jeder Quelle wird ihr Status angezeigt:

- **Verbindet sich automatisch neu**: eine kurze Unterbrechung. Die Quelle versucht es von selbst erneut.
- **Wartet auf die erste Synchronisierung**: gerade verbunden. Warte ein paar Minuten.
- **Liest wieder ab** 07:00: X und LinkedIn lesen nur tagsüber. Du musst nichts tun.
- **Noch nicht eingerichtet**: Hier hat sich noch niemand angemeldet. Drücke **Verbinden**. Innerhalb einer Minute geht es los.
- **Braucht deine Hilfe**: Öffne **Details**. Dort steht, was schiefgelaufen ist und was du tun kannst.
- **Handy getrennt**: Dein Android-Handy erreicht deine Machine nicht. Öffne darauf die OpenClaw-App.

Eine Quelle, die länger als üblich nichts liefert, zeigt **Wartet auf eine neue Synchronisierung** an. Der Hinweis verschwindet von selbst, sobald die Synchronisierung wieder klappt.

Die Zahl bei **Verbindungen** zählt nur Quellen, die deine Hilfe brauchen.

## Häufige Lösungen

- „Melde dich wieder bei Google an“ (oder Microsoft): Mit einmal **Neu verbinden** werden alle Quellen dieses Kontos wiederhergestellt, zum Beispiel Gmail und Kalender.
- „Du musst dich erneut anmelden“: Drücke **Neu verbinden** und melde dich an.
- „Ein Programm, das auf diesem Computer fehlt, wird benötigt“: Führe den Befehl auf der zugehörigen Karte in einem Terminal auf diesem Computer aus. Dort steht, was du installieren musst, oder es wird ein verschobenes Programm gefunden.
- Microsoft richtet den Zugriff noch ein: Es wird von selbst erneut versucht.
- Slack: Drücke **Neu verbinden**. Mit einem Maton-Schlüssel verbunden? Überprüfe den Schlüssel und die Slack-Verbindung in Maton.
- Android: Öffne die OpenClaw-App auf dem Handy und erlaube ihr den Zugriff auf Benachrichtigungen.

Auf deinem eigenen Computer prüft `assistant doctor` jede Quelle und erklärt, wie du die einzelnen Probleme behebst.

Kommst du nicht weiter? Sieh dir [Support kontaktieren](get-support.md) an.
