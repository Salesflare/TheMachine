---
title: Android-Benachrichtigungen
area: connections
summary: Die Benachrichtigungen auf deinem Android-Handy, über die OpenClaw-App. Sie liest nur.
covers: connector:android
code: onboarding.py, android-notifications.mjs
site: Show a setup code, Approve, More sources, Remove
---
## Was sie liest

Die Benachrichtigungen, die auf deinem Android-Handy ankommen, über die OpenClaw-App. Einmalcodes bleiben außen vor, ebenso Benachrichtigungen von WhatsApp, Telegram, Signal und Discord.

## Was sie tun kann

Nichts auf deinem Handy. Sie liest nur Benachrichtigungen.

## Verbinden

Auf einer gehosteten Machine:

1. Installiere die OpenClaw-App auf deinem Handy.
2. Öffne im Dashboard **Verbindungen**, dann **+ Hinzufügen**, wähle Android-Handy und tippe auf **Einrichtungscode zeigen**.
3. Scanne ihn in der OpenClaw-App und tippe dann auf **Freigeben**, um die Kopplung zu bestätigen.
4. Schalte in der OpenClaw-App Forward Notification Events ein und erlaube den Zugriff auf Benachrichtigungen, wenn Android danach fragt.

Auf deinem eigenen Computer koppelst du das Handy mit deinem OpenClaw Gateway und führst dann `assistant connect android` aus.

## Entfernen

- Im Dashboard: **Verbindungen**, Android öffnen, **Details**, dann **Trennen**.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** tippen.

## Auf dem Handy entfernen

Schalte in den Android-Einstellungen den Zugriff auf Benachrichtigungen für die OpenClaw-App aus, oder entkopple das Handy in der OpenClaw-App.
