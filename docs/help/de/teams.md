---
title: Microsoft Teams
area: connections
summary: Teams-Chats, Meeting-Chats und Meeting-Notizen für ein Geschäfts- oder Schulkonto. Antworten werden erst nach deiner Freigabe gesendet.
covers: connector:teams
code: connectors/teams.py, teams_send.py, ms_graph.py, onboarding.py
site: Connect Microsoft Teams
translated: 9ca0bb08466b4d58
---
## Was gelesen wird

Deine 1:1-, Gruppen- und Meeting-Chats in Teams: die letzten 7 Tage beim Verbinden, danach alle paar Minuten neue Nachrichten. Etwa ein Jahr ältere Chats und mit Zustimmung deiner Admins auch Kanal-Threads werden später nach und nach als [Verlauf](history.md) geladen, ohne etwas aufzuhalten.

Mit Zustimmung deiner Admins werden außerdem gelesen:

- Kanal-Threads in deinen Teams.
- Transkripte von Meetings, die du organisiert hast.
- Meeting-Notizen und Aufgaben von Copilot, wenn du eine Microsoft 365 Copilot-Lizenz hast.

Jedes Transkript und jeder Notizensatz wird dem zugehörigen Meeting in deinem Kalender hinzugefügt und mit **Aus Teams** gekennzeichnet. Auch ohne diese Inhalte bleibt der Meeting-Chat verfügbar.

Bots, Apps und Systemnachrichten werden ausgelassen.

## Was es kann

In dem 1:1-, Gruppen- oder Meeting-Chat antworten, aus dem eine Aufgabe stammt. The Machine entwirft die Antwort. Sie wird erst gesendet, nachdem du sie geprüft und **Jetzt senden** gedrückt hast. Sie wird in deinem Namen und in diesem Chat gesendet. The Machine beginnt nie einen neuen Chat.

In Kanälen werden keine Beiträge veröffentlicht. Um in einem Kanal-Thread zu antworten, öffne ihn über **In Teams öffnen**.

## Welche Berechtigungen nötig sind

Microsoft bittet darum, The Machine das Lesen deiner Chats und deines Profils sowie das Senden von Chatnachrichten in deinem Namen zu erlauben. Dafür ist keine Adminfreigabe nötig.

Wenn du Teams verbunden hast, bevor The Machine Nachrichten senden konnte, steht auf der Teams-Karte **Stelle die Verbindung wieder her, um Antworten zu senden.** Drücke **Neu verbinden** und erteile die Zustimmung erneut. Bis dahin bleibt der Entwurf für dich bereit, damit du ihn in Teams senden kannst.

Für Kanäle, Transkripte und Copilot-Notizen müssen die Admins deiner Organisation einmalig ihre Zustimmung geben. Bis dahin steht auf der Teams-Karte, was noch nicht gelesen werden kann und warum.

Das funktioniert nur mit einem Microsoft-Geschäfts- oder Schulkonto. Bei persönlichen Konten gibt es keine Teams-Chats, die auf diese Weise gelesen werden können.

## Verbindung herstellen

Auf einer gehosteten Machine:

1. Öffne im Dashboard **Verbindungen** und dann **Chat** für **Microsoft Teams** oder **Meetings** für **Teams-Meetings**. Für beide wird dieselbe Anmeldung verwendet.
2. Drücke **Mit Microsoft anmelden** und erteile deine Zustimmung. Danach kehrst du zum Dashboard zurück.
3. Für Kanäle und Meeting-Notizen sende deinen Admins den Link, der auf der Anmeldeseite angezeigt wird. Sobald sie zugestimmt haben, verbinde Teams erneut.

Während der Einrichtung findest du auf der Einrichtungsseite auch **Microsoft Teams verbinden**.

Auf deinem eigenen Computer, sobald er [mit deinem Konto gekoppelt ist](friends.md#a-machine-on-your-own-computer): Öffne **Verbindungen** und dann **Chat** oder **Meetings**. Wähle **Microsoft Teams** oder **Teams-Meetings** und drücke **Mit Microsoft anmelden**. Dort liest The Machine deine Chats und Meeting-Chats. Kanäle und Meeting-Notizen sind dort noch nicht verfügbar.

## Verbindung trennen

Im Dashboard: Öffne unter **Verbindungen** Microsoft Teams und wähle **Details** und dann **Trennen**. Bereits übertragene Inhalte bleiben erhalten.

## Berechtigung in Microsoft widerrufen

Öffne myapps.microsoft.com und entferne The Machine. Wenn Outlook mit derselben Adresse verbunden ist, wird die Verbindung dort ebenfalls getrennt.
