---
title: Eine Verbindung braucht Hilfe
area: troubleshooting
summary: Eine Quelle zeigt Braucht deine Hilfe oder bringt nichts mehr rein. Was du versuchen kannst.
covers: 
code: onboarding.py, dashboard.html
order: 1
---
## Status prüfen

Öffne **Verbindungen**. Jede Quelle zeigt, wie es ihr geht:

- **Verbindet sich automatisch neu**: ein kurzer Aussetzer. Sie versucht es von selbst erneut.
- **Wartet auf die erste Synchronisierung**: gerade verbunden. Gib ihr ein paar Minuten.
- **Liest wieder um** 07:00: X und LinkedIn lesen nur tagsüber. Nichts zu tun.
- **Braucht deine Hilfe**: Öffne **Details**. Dort steht, was schiefging und was zu tun ist.

Die Zahl bei **Verbindungen** zählt nur Quellen, die deine Hilfe brauchen.

## Häufige Lösungen

- „needs you to sign in again“: Tippe auf **Neu verbinden** und melde dich an. Auf einer gehosteten Machine verbindest du Google und Microsoft über deine Einrichtungsseite neu.
- Microsoft richtet den Zugriff noch ein: Es versucht es von selbst erneut.
- Slack: Prüfe deinen Maton-API-Schlüssel und die Slack-Verbindung in Maton.
- Android: Öffne die OpenClaw-App auf dem Handy und erlaube ihr den Zugriff auf Benachrichtigungen.

Auf deinem eigenen Computer prüft `assistant doctor` jede Quelle und zeigt für jedes Problem die Lösung.

Kommst du immer noch nicht weiter? Siehe [Support bekommen](get-support.md).
