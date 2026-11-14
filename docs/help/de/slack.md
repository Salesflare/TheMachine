---
title: Slack
area: connections
summary: Die Channels und Direktnachrichten, in denen du bist. Sendet eine Direktnachricht erst, nachdem du sie freigegeben hast.
covers: connector:slack
code: assistant.py, next_actions.py, onboarding.py, slack_api.py
site: Connect, Remove
translated: 23f9e98f4680d23c
---
## Was gelesen wird

Unterhaltungen, bei denen du Mitglied bist: Channels, private Channels, Direktnachrichten und Gruppennachrichten. Beim Verbinden werden die letzten 7 Tage geladen, danach alle neuen Nachrichten. The Machine tritt niemals selbst einem Channel bei und öffnet auch keine Unterhaltung. Ein ruhiger Channel wird etwa einmal täglich gelesen. Wenn eine Aufgabe die neuesten Nachrichten daraus braucht, liest The Machine den Channel sofort.

Ältere Nachrichten aus etwa einem Jahr werden später nach und nach als [Verlauf](history.md) geladen.

Personen werden mit ihrem Namen angezeigt und Apps mit ihrem Namen, nie mit einer Slack-ID. Wenn ein Slack-Konto nicht mehr existiert, wird die Person als ehemalige Slack-Nutzerin oder ehemaliger Slack-Nutzer angezeigt.

## Was gesendet werden kann

Eine Direktnachricht an eine Person, in deinem Namen und erst, nachdem du sie bei der Aufgabe freigegeben hast. Eine Antwort auf die Slack-Nachricht, aus der eine Aufgabe stammt, wird im Thread dieser Nachricht gesendet, in der Direktnachricht oder im Channel. Im Entwurf steht **Im Thread**. The Machine startet niemals einen neuen Beitrag in einem Channel.

## Was gespeichert wird

Alles, was The Machine liest, bleibt auf deiner Machine, bis du es oder die Machine löschst. Der Hosting-Dienst speichert keine Kopie deiner Nachrichten und keine Slack-Anmeldedaten. Außerdem wird kein KI-Modell mit deinen Slack-Daten trainiert. The Machine nutzt KI, die Fehler machen kann. Deshalb siehst du jede Nachricht, bevor sie gesendet wird.

## Verbinden

1. **Verbindungen**, **Chat**, **Slack**, dann **Mit Slack anmelden** und den Zugriff in Slack erlauben. Wenn du deinen eigenen Computer verwendest, verknüpfe deine Machine zuerst unter themachine.computer mit deinem Konto.
2. Zuerst werden neue Nachrichten und Direktnachrichten geladen. Slack erlaubt Apps, etwa eine Unterhaltung pro Minute zu lesen. Deshalb werden ältere Nachrichten nach und nach über einige Stunden geladen.

Oder verwende einen Maton-API-Schlüssel: Melde dich bei maton.ai an, verbinde dort Slack und kopiere deinen Maton-API-Schlüssel unter Home. Öffne dann unter Slack **Oder einen Maton-API-Schlüssel verwenden** und füge ihn ein, oder führe `assistant connect slack` auf deinem eigenen Computer aus. Eine über Maton verbundene Slack-Verbindung funktioniert unverändert weiter.

## Entfernen

- Im Dashboard: **Verbindungen** öffnen, Slack auswählen, **Details** und dann **Trennen**. Bereits importierte Daten bleiben erhalten.
- Bei einer gehosteten Machine kannst du auf der Einrichtungsseite auch daneben auf **Entfernen** klicken.

## In Slack deinstallieren

Wenn du dich mit Slack angemeldet hast: Öffne in Slack die Seite Apps verwalten deines Workspaces und entferne The Machine. Sie hört sofort auf zu lesen und fordert dich auf, dich erneut anzumelden. Bereits importierte Daten bleiben erhalten. Wenn du Maton verwendest: Entferne die Slack-Verbindung in Maton und lösche den Maton-API-Schlüssel, den du angegeben hast. Ein Slack-Admin kann auch eine der beiden Apps im Workspace unter Apps verwalten entfernen.
