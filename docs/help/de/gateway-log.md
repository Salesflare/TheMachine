---
title: Machine-Log
area: connections
summary: Das eigene Log deiner Machine, damit sie eigene Probleme erkennt. Es liest nur.
covers: connector:gateway
code: onboarding.py
site: More sources, Remove
---
## Was es liest

Das Log deines OpenClaw Gateway: fehlgeschlagene Durchläufe, abgelehnte Übergaben, Telegram-Nachrichten, die nicht rausgingen, und Fehler von The Machine selbst. Eine Aufgabe sagt dir, wenn etwas repariert werden muss.

## Korrekturen, die eine Aktualisierung beiseitegelegt hat

Wenn The Machine sich aktualisiert und eine ihrer eigenen Korrekturen nicht mehr zur neuen Version passt, legt die Aktualisierung diese Korrektur beiseite und macht weiter, damit deine Machine nie auf einer alten Version bleibt. Eine Aufgabe, **Eine beiseitegelegte Korrektur neu machen**, nennt die Korrektur. Bitte darum, sie auf der neuen Version neu zu machen, oder schließ die Aufgabe.

## Was es tun kann

Nichts. Es liest nur das Log auf deiner eigenen Machine.

## Verbinden

- Auf einer gehosteten Machine steht es auf deiner Einrichtungsseite unter **Weitere Quellen**, als OpenClaw Gateway log. Eins pro Machine.
- Auf deinem eigenen Computer: Führe `assistant connect gateway` aus.

## Entfernen

- Im Dashboard: **Verbindungen**, öffnen, **Details**, dann **Trennen**.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** tippen.

Woanders gibt es nichts zu deinstallieren.
