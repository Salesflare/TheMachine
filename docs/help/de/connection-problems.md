---
title: Eine Verbindung braucht Hilfe
area: troubleshooting
summary: Eine Quelle zeigt Braucht deine Hilfe oder bringt nichts mehr rein. Was du versuchen kannst.
covers: 
code: onboarding.py, dashboard.html, assistant.py
order: 1
---
## Status prüfen

Öffne **Verbindungen**. Jede Quelle zeigt, wie es ihr geht:

- **Verbindet sich automatisch neu**: ein kurzer Aussetzer. Sie versucht es von selbst erneut.
- **Wartet auf die erste Synchronisierung**: gerade verbunden. Gib ihr ein paar Minuten.
- **Liest wieder um** 07:00: X und LinkedIn lesen nur tagsüber. Nichts zu tun.
- **Braucht deine Hilfe**: Öffne **Details**. Dort steht, was schiefging und was zu tun ist.
- **Handy getrennt**: Das Handy erreicht OpenClaw nicht. Öffne die OpenClaw-App darauf.

Eine Quelle, die immer wieder fehlschlägt und stundenlang nichts Neues bringt, länger als ihre übliche ruhige Zeit, gilt nicht als verbunden. Das verschwindet von selbst, sobald wieder Neues ankommt.

Die Zahl bei **Verbindungen** zählt nur Quellen, die deine Hilfe brauchen.

## Häufige Lösungen

- „Melde dich wieder bei Google an“ (oder Microsoft): eine Zeile pro Konto. Ein **Neu verbinden** holt alle seine Quellen zurück, etwa Gmail und Kalender.
- „needs you to sign in again“: Tippe auf **Neu verbinden** und melde dich an. Auf einer gehosteten Machine meldest du dich direkt dort an und kommst zurück zum Dashboard.
- Microsoft richtet den Zugriff noch ein: Es versucht es von selbst erneut.
- Slack: Prüfe deinen Maton-API-Schlüssel und die Slack-Verbindung in Maton.
- Android: Öffne die OpenClaw-App auf dem Handy und erlaube ihr den Zugriff auf Benachrichtigungen.

Auf deinem eigenen Computer prüft `assistant doctor` jede Quelle und zeigt für jedes Problem die Lösung.

Kommst du immer noch nicht weiter? Siehe [Support bekommen](get-support.md).
