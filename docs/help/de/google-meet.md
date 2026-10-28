---
title: Google Meet
area: connections
summary: Transkripte und Gemini-Notizen von Meet-Meetings, die du organisierst. Es liest nur.
covers: connector:google_meet
code: connectors/google_meet.py
site: Connect, More sources, Remove
---
## Was es liest

Transkripte und Gemini-Notizen von Google-Meet-Meetings, die du organisiert hast, sobald Meet sie erstellt hat: die letzten 7 Tage beim Verbinden, danach neue, sobald sie reinkommen. Meet bewahrt sie 30 Tage auf.

Meet erstellt sie nur, wenn Transkripte oder Gemini-Notizen während des Meetings eingeschaltet waren.

## Was es tun kann

Nichts in Meet oder Drive. Es liest nur und schaltet nie selbst Transkripte ein.

## Verbinden

1. Aktiviere in Google Cloud die Google Meet API und die Google Drive API.
2. Hol dir im OAuth Playground ein Zugriffstoken mit den zwei Nur-Lese-Scopes, die der Verbindungsbildschirm zeigt.
3. Auf einer gehosteten Machine: Öffne deine Einrichtungsseite unter app.themachine.computer/setup, geh zu **Weitere Quellen** und öffne Google Meet. Auf deinem eigenen Computer: **Verbindungen**, **+ Hinzufügen**, Google Meet, oder `assistant connect google_meet`.
4. Füge das Token ein und tippe auf **Verbinden**.

Das Token läuft nach etwa einer Stunde ab. Wenn Verbindungen sagt, dass es abgelehnt wurde, füge ein neues ein.

## Entfernen

- Im Dashboard: **Verbindungen**, Google Meet öffnen, **Details**, dann **Trennen**. Was es schon reingebracht hat, bleibt.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** tippen.

## Bei Google widerrufen

Öffne myaccount.google.com/permissions und entferne den Zugriff des OAuth Playground.
