---
title: Android-Benachrichtigungen
area: connections
summary: Die Benachrichtigungen auf deinem Android-Handy, über die OpenClaw-App. Sie liest nur.
covers: connector:android
code: onboarding.py, android-notifications.mjs
site: Show a setup code, Approve, Remove
translated: 344d64dafc75a0a9
---
## Was sie liest

Die Benachrichtigungen, die auf deinem Android-Handy ankommen, über die OpenClaw-App. Einmalcodes bleiben außen vor, ebenso Benachrichtigungen von WhatsApp, Telegram, Signal und Discord.

## Was sie tun kann

Nichts auf deinem Handy. Sie liest nur Benachrichtigungen.

## Verbinden

Auf einer gehosteten Machine:

1. Installiere OpenClaw aus Google Play auf deinem Handy.
2. Öffne im Dashboard **Verbindungen**, dann **Andere**, wähle Android-Handy und tippe auf **Einrichtungscode zeigen**.
3. Füge in der OpenClaw-App ein Gateway hinzu und scanne den Code. Tippe dann im Dashboard auf **Freigeben**.
4. Erlaube den Zugriff auf Benachrichtigungen, wenn die App danach fragt. Schalte dann in den Einstellungen der App Forward Notification Events ein, damit Benachrichtigungen sofort ankommen, nicht nur bei der Prüfung alle 10 Minuten.

Auf deinem eigenen Computer koppelst du das Handy in der OpenClaw-App und führst dann `assistant connect android` aus.

## Entfernen

- Im Dashboard: **Verbindungen**, Android öffnen, **Details**, dann **Trennen**.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** tippen.

## Auf dem Handy entfernen

Schalte in den Android-Einstellungen den Zugriff auf Benachrichtigungen für die OpenClaw-App aus, oder entkopple das Handy in der OpenClaw-App.
