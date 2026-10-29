---
title: Slack
area: connections
summary: Die Channels und Direktnachrichten, in denen du bist. Sendet eine Direktnachricht erst, nachdem du sie freigegeben hast.
covers: connector:slack
code: assistant.py, slack_api.py, next_actions.py, onboarding.py
site: Sign in with Slack, Connect, More sources, Remove
---
## Was es liest

Die Unterhaltungen, in denen du Mitglied bist: Channels, private Channels, Direktnachrichten und Gruppennachrichten, die letzten 7 Tage beim Verbinden, danach alles Neue. Es tritt nie von selbst einem Channel bei und startet keine Unterhaltung.

## Was es senden kann

Eine Direktnachricht an eine Person, als du, und nur, nachdem du sie bei der Aufgabe freigegeben hast. Es postet nie in einem Channel.

## Verbinden

Mit Slack anmelden, der einfache Weg:

1. Im Dashboard: **Verbindungen**, **+ Hinzufügen**, Slack. Oder auf der Einrichtungsseite einer gehosteten Machine unter app.themachine.computer/setup: **Weitere Quellen**, Slack. Auf deinem eigenen Computer koppelst du ihn zuerst mit deinem Konto.
2. Tippe auf **Mit Slack anmelden**. Slack fragt, welcher Workspace, und zeigt, was The Machine lesen und senden darf.
3. Tippe auf **Allow**. Du bist wieder da, wo du angefangen hast, und Slack ist verbunden.

In manchen Workspaces dürfen nur Admins neue Apps freigeben. Slack fragt dann zuerst einen Admin; sobald er zustimmt, melde dich noch einmal an.

Oder nutze stattdessen Maton:

1. Melde dich bei maton.ai an, verbinde dort Slack und kopiere deinen Maton-API-Schlüssel unter Home.
2. Öffne Slack wie oben (oder führe `assistant connect slack` aus), öffne **Oder einen Maton-API-Schlüssel verwenden**, füge den Schlüssel ein und tippe auf **Verbinden**.

Slack schon über Maton verbunden? Es funktioniert weiter. Unter Verbindungen steht **Slack neu verbinden**: Tippe darauf und melde dich mit Slack an, um Maton nicht mehr zu nutzen. Was Slack schon geholt hat, bleibt.

## Entfernen

- Im Dashboard: **Verbindungen**, Slack öffnen, **Details**, dann **Trennen**. Was es schon reingebracht hat, bleibt.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** tippen.

## Bei Slack deinstallieren

- Mit Slack angemeldet: Öffne in Slack die Seite Manage apps deines Workspaces (oder Einstellungen, Apps), such The Machine und entferne die App. Ein Slack-Admin kann sie auch für den ganzen Workspace entfernen.
- Über Maton: Entferne die Slack-Verbindung in Maton und lösche den Maton-API-Schlüssel, den du angegeben hast.
