---
title: Slack
area: connections
summary: Die Channels und Direktnachrichten, in denen du bist. Sendet eine Direktnachricht erst, nachdem du sie freigegeben hast.
covers: connector:slack
code: assistant.py, next_actions.py, onboarding.py
site: Connect, More sources, Remove
---
## Was es liest

Die Unterhaltungen, in denen du Mitglied bist: Channels, private Channels, Direktnachrichten und Gruppennachrichten, die letzten 7 Tage beim Verbinden, danach alles Neue. Es tritt nie von selbst einem Channel bei und startet keine Unterhaltung.

Personen erscheinen mit ihrem Namen und Apps mit ihrem, nie mit einer Slack-ID. Jemand, dessen Slack-Konto nicht mehr besteht, erscheint als ehemaliger Slack-Nutzer.

## Was es senden kann

Eine Direktnachricht an eine Person, als du, und nur, nachdem du sie bei der Aufgabe freigegeben hast. Es postet nie in einem Channel.

## Verbinden

Slack wird über Maton gelesen, das die Slack-Anmeldung hält.

1. Melde dich bei maton.ai an, verbinde dort Slack und kopiere deinen Maton-API-Schlüssel unter Home.
2. Auf einer gehosteten Machine: Öffne deine Einrichtungsseite unter app.themachine.computer/setup, geh zu **Weitere Quellen**, öffne Slack, füge den Schlüssel ein und tippe auf **Verbinden**.
3. Auf deinem eigenen Computer: Führe `assistant connect slack` aus, oder **Verbindungen**, **+ Hinzufügen**, Slack.

## Entfernen

- Im Dashboard: **Verbindungen**, Slack öffnen, **Details**, dann **Trennen**. Was es schon reingebracht hat, bleibt.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** tippen.

## Bei Slack deinstallieren

Entferne die Slack-Verbindung in Maton und lösche den Maton-API-Schlüssel, den du angegeben hast. Ein Slack-Admin kann die App auch unter Manage apps aus dem Workspace entfernen.
