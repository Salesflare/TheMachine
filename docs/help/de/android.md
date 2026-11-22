---
title: Android-Benachrichtigungen
area: connections
summary: Benachrichtigungen auf deinem Android-Handy über die OpenClaw-App. Sie liest sie nur.
covers: connector:android
code: onboarding.py, android-notifications.mjs
site: Show a setup code, Approve, Remove
translated: 5b08b093662393a1
---
## Was gelesen wird

Benachrichtigungen auf deinem Android-Handy über die OpenClaw-App. Einmalcodes werden nicht erfasst, ebenso wenig Benachrichtigungen von WhatsApp, Telegram, Signal und Discord.

## Was damit möglich ist

Nichts auf deinem Handy. Sie liest nur Benachrichtigungen.

## Verbinden

Auf einer gehosteten Machine:

1. Installiere OpenClaw aus Google Play auf deinem Handy.
2. Öffne im Dashboard **Verbindungen**, dann **Andere**, wähle Android-Benachrichtigungen aus und tippe auf **Einrichtungscode zeigen**.
3. Füge in der OpenClaw-App ein Gateway hinzu und scanne den Code. Tippe dann im Dashboard auf **Freigeben**.
4. Erlaube den Zugriff auf Benachrichtigungen, wenn die App danach fragt. Aktiviere dann in den App-Einstellungen „Forward Notification Events“, damit Benachrichtigungen sofort ankommen und nicht nur bei der Überprüfung alle 10 Minuten.

Auf deinem eigenen Computer: Kopple das Handy in der OpenClaw-App und führe dann `assistant connect android` aus.

## Verbindung entfernen

- Im Dashboard: Öffne **Verbindungen**, wähle Android aus und tippe auf **Details** und dann auf **Trennen**.
- Auf einer gehosteten Machine kannst du auf deiner Einrichtungsseite auch daneben auf **Entfernen** tippen.

## Verbindung auf dem Handy entfernen

Deaktiviere in den Android-Einstellungen den Benachrichtigungszugriff für die OpenClaw-App oder entkopple das Handy in der OpenClaw-App.
