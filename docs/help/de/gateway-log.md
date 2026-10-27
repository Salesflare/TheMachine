---
title: Server-Log
area: connections
summary: Das eigene Log deines Servers, damit The Machine eigene Probleme erkennt. Es liest nur.
covers: connector:gateway
code: onboarding.py
site: More sources, Remove
---
## Was es liest

Das Log deines OpenClaw Gateway: fehlgeschlagene Durchläufe, abgelehnte Übergaben, Telegram-Nachrichten, die nicht rausgingen, und Fehler von The Machine selbst. Eine Aufgabe sagt dir, wenn etwas repariert werden muss.

## Was es tun kann

Nichts. Es liest nur das Log auf deinem eigenen Server.

## Verbinden

- Auf einer gehosteten Machine steht es auf deiner Einrichtungsseite unter **Weitere Quellen**, als OpenClaw Gateway log. Eins pro Server.
- Auf deinem eigenen Computer: Führe `assistant connect gateway` aus.

## Entfernen

- Im Dashboard: **Verbindungen**, öffnen, **Details**, dann **Trennen**.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** tippen.

Woanders gibt es nichts zu deinstallieren.
