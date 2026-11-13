---
title: Slack
area: connections
summary: Die Channels und Direktnachrichten, in denen du bist. Sendet eine Direktnachricht erst, nachdem du sie freigegeben hast.
covers: connector:slack
code: assistant.py, next_actions.py, onboarding.py, slack_api.py
site: Connect, Remove
---
## Was es liest

Die Unterhaltungen, in denen du Mitglied bist: Channels, private Channels, Direktnachrichten und Gruppennachrichten, die letzten 7 Tage beim Verbinden, danach alles Neue. Es tritt nie von selbst einem Channel bei und startet keine Unterhaltung. Ein ruhiger Channel wird etwa einmal am Tag gelesen; braucht eine Aufgabe seine neuesten Nachrichten, liest The Machine ihn sofort.

Ältere Nachrichten aus etwa einem Jahr kommen später nach und nach als [Verlauf](history.md) dazu.

Personen erscheinen mit ihrem Namen und Apps mit ihrem, nie mit einer Slack-ID. Jemand, dessen Slack-Konto nicht mehr besteht, erscheint als ehemaliger Slack-Nutzer.

## Was es senden kann

Eine Direktnachricht an eine Person, als du, und nur, nachdem du sie bei der Aufgabe freigegeben hast. Eine Antwort auf die Slack-Nachricht, aus der eine Aufgabe kam, geht in den Thread dieser Nachricht, in der Direktnachricht oder im Channel; im Entwurf steht **Im Thread**. Es beginnt nie einen neuen Beitrag in einem Channel.

## Verbinden

1. **Verbindungen**, **Chat**, **Slack**, dann **Mit Slack anmelden**, und erlaube es in Slack. Auf deinem eigenen Computer verbindest du ihn zuerst mit deinem Konto auf themachine.computer.
2. Neue Nachrichten und Direktnachrichten kommen zuerst. Slack lässt Apps etwa ein Gespräch pro Minute lesen, ältere Nachrichten kommen deshalb im Lauf einiger Stunden dazu.

Oder einen Maton-API-Schlüssel verwenden: Melde dich bei maton.ai an, verbinde dort Slack und kopiere deinen Maton-API-Schlüssel unter Home. Öffne dann unter Slack **Oder einen Maton-API-Schlüssel verwenden** und füge ihn ein, oder führe auf deinem eigenen Computer `assistant connect slack` aus. Ein über Maton verbundenes Slack funktioniert weiter wie bisher.

## Entfernen

- Im Dashboard: **Verbindungen**, Slack öffnen, **Details**, dann **Trennen**. Was es schon reingebracht hat, bleibt.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** tippen.

## Bei Slack deinstallieren

Mit Slack angemeldet: Öffne in Slack die Seite Manage apps deines Workspace und entferne The Machine. Über Maton: Entferne die Slack-Verbindung in Maton und lösche den Maton-API-Schlüssel, den du angegeben hast. Ein Slack-Admin kann beide Apps auch unter Manage apps aus dem Workspace entfernen.
