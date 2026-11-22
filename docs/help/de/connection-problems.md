---
title: Eine Verbindung braucht deine Hilfe
area: troubleshooting
summary: Eine Quelle zeigt „Braucht deine Hilfe“ an oder liefert nichts mehr. Das kannst du tun.
covers:
code: onboarding.py, dashboard.html, assistant.py
order: 1
translated: c07a7f214b1e4deb
---
## Status prüfen

Öffne **Verbindungen**. Bei jeder Quelle siehst du ihren Status:

- **Verbindet sich automatisch neu**: eine kurze Unterbrechung. Die Quelle versucht es von selbst erneut.
- **Wartet auf die erste Synchronisierung**: gerade verbunden. Warte ein paar Minuten.
- **Liest wieder um** 07:00: X und LinkedIn lesen nur tagsüber. Du musst nichts tun.
- **Braucht deine Hilfe**: Öffne **Details**. Dort erfährst du, was schiefgelaufen ist und was du tun kannst.
- **Handy getrennt**: Dein Android-Handy erreicht deine Machine nicht. Öffne darauf die OpenClaw-App.

Eine Quelle, die länger als gewöhnlich nichts liefert, zeigt **Wartet auf eine neue Synchronisierung** an. Der Status wird automatisch aufgehoben, sobald eine Synchronisierung klappt.

Die Zahl bei **Verbindungen** zählt nur Quellen, die deine Hilfe brauchen.

## Häufige Lösungen

- „Melde dich noch einmal bei Google an“ (oder Microsoft): Mit **Neu verbinden** werden alle Quellen dieses Kontos wiederhergestellt, zum Beispiel Gmail und Kalender.
- „braucht eine neue Anmeldung von dir“: Drücke **Neu verbinden** und melde dich an.
- Microsoft richtet den Zugriff noch ein: Es versucht es automatisch erneut.
- Slack: Drücke **Neu verbinden**. Mit einem Maton-Schlüssel verbunden? Prüfe den Schlüssel und die Slack-Verbindung in Maton.
- Android: Öffne die OpenClaw-App auf dem Handy und erlaube ihr den Zugriff auf Benachrichtigungen.

Auf deinem eigenen Computer prüft `assistant doctor` jede Quelle und erklärt, wie du jedes Problem behebst.

Hakt es immer noch? Siehe [Support kontaktieren](get-support.md).
