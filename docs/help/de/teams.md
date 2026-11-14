---
title: Microsoft Teams
area: connections
summary: Teams-Chats, Meeting-Chats und Meeting-Notizen für ein Arbeits- oder Schulkonto. Es liest nur.
covers: connector:teams
code: connectors/teams.py, ms_graph.py, onboarding.py
site: Connect Microsoft Teams
translated: 864f9e6e98309439
---
## Was es liest

Deine 1:1-, Gruppen- und Meeting-Chats in Teams: die letzten 7 Tage beim Verbinden, danach alle paar Minuten neue Nachrichten. Ältere Chats aus etwa einem Jahr, mit dem OK deines Admins auch Channel-Threads, kommen später nach und nach als [Verlauf](history.md) dazu, ohne etwas aufzuhalten.

Mit dem OK deines Admins liest es außerdem:

- Kanal-Threads in deinen Teams.
- Meeting-Transkripte von Meetings, die du organisiert hast.
- Copilots Meeting-Notizen und Aufgaben, wenn du eine Microsoft 365 Copilot-Lizenz hast.

Jedes Transkript und jede Notiz landet bei ihrem Meeting in deinem Kalender, markiert mit **Aus Teams**. Ohne sie bleibt der Meeting-Chat da.

Bots, Apps und Systemnachrichten bleiben außen vor.

## Was es tun kann

Nichts in Teams. Es liest nur. Zum Antworten öffne den Chat mit **In Teams öffnen**.

## Worum es fragt

Microsoft fragt, ob The Machine deine Chats und dein Profil lesen darf. Dafür braucht es keinen Admin.

Kanäle, Transkripte und Copilot-Notizen braucht einmal das OK des Admins deiner Organisation. Bis dahin zeigt die Teams-Karte, was es noch nicht lesen kann und warum.

Es funktioniert nur mit einem Microsoft-Arbeits- oder Schulkonto. Private Konten haben keine Teams-Chats, die es so lesen kann.

## Verbinden

Auf einer gehosteten Machine:

1. Öffne im Dashboard **Verbindungen**, **Chat** oder **Meetings** und wähle **Microsoft Teams** (unter Chat) oder **Teams-Meetings** (unter Meetings). Beide sind dieselbe Anmeldung.
2. Drücke **Mit Microsoft anmelden** und gib das OK. Danach bist du zurück im Dashboard.
3. Für Kanäle und Meeting-Notizen schick deinem Admin den Link, den die Anmeldeseite zeigt. Sobald er zugestimmt hat, verbinde Teams erneut.

Beim Einrichten hat auch die Einrichtungsseite **Connect Microsoft Teams**.

Auf deinem eigenen Computer, sobald er [mit deinem Konto gekoppelt](friends.md#a-machine-on-your-own-computer) ist: Öffne **Verbindungen**, dann **Chat** oder **Meetings**, wähle **Microsoft Teams** oder **Teams-Meetings** und drücke **Mit Microsoft anmelden**. Dort liest es deine Chats und Meeting-Chats. Kanäle und Besprechungsnotizen gibt es dort noch nicht.

## Entfernen

Im Dashboard: **Verbindungen**, Microsoft Teams öffnen, **Details**, dann **Trennen**. Was es schon hereingeholt hat, bleibt.

## Bei Microsoft widerrufen

Öffne myapps.microsoft.com und entferne The Machine. Ist Outlook mit derselben Adresse verbunden, wird es damit auch getrennt.
