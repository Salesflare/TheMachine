---
title: X
area: connections
summary: Deine Erwähnungen, Antworten und Direktnachrichten auf X, gelesen im eigenen Browser deiner Machine. Gesendet wird erst, wenn du zustimmst.
covers: connector:x
code: connectors/x.py, integrations/x_inbox.py
site: Connect, More sources, Remove
translated: e8997ab6eb32523f
---
## Was sie liest

Deine Erwähnungen, Antworten und Direktnachrichten auf X, in deiner Machine im eigenen Browser und als du angemeldet. Sie markiert nichts als gelesen und kann verschlüsselte X-Chats nicht lesen.

## Was sie senden kann

Eine Antwort oder eine Direktnachricht, und erst nachdem du sie bei der Aufgabe freigegeben hast.

X stellt Konten nach und nach auf eine neue Web-App um. Wenn dein Konto schon umgestellt wurde, können Antworten noch nicht über deine Machine gesendet werden. Eine von dir freigegebene Antwort wird daher nicht veröffentlicht, und die Machine weist dich darauf hin. Direktnachrichten werden weiterhin gesendet.

Das läuft nicht über die offizielle API von X. Lesen und gelegentliche, von dir freigegebene Antworten führen sehr wahrscheinlich zu keinen Problemen. Massenhaftes oder automatisiertes Senden kann dazu führen, dass ein Konto gesperrt wird.

## Verbinden

Auf einer gehosteten Machine:

1. Öffne deine Einrichtungsseite unter app.themachine.computer/setup und gehe zu **Weitere Quellen**.
2. Öffne X, gib deinen Handle ohne @ ein, melde dich bei X im Browser deiner Machine an, wenn du dazu aufgefordert wirst, und klicke dann auf **Verbinden**.

Auf deinem eigenen Computer:

1. Öffne im Dashboard **Verbindungen**, dann **Chat**, und wähle X aus.
2. Wähle **Arbeit** und das zugehörige Unternehmen oder **Privat**, gib deinen Handle ohne @ ein und klicke auf **Verbinden**.
3. Klicke auf **Bei X anmelden** und melde dich im Browser deiner Machine an. Sobald du angemeldet bist, wird die Verbindung automatisch hergestellt.

Oder führe `assistant connect x` in einem Terminal aus.

Wenn X deine Machine abmeldet, lies den Artikel [Von einer Website abgemeldet](signed-out.md).

## Entfernen

- Im Dashboard: Öffne **Verbindungen**, wähle X aus und gehe zu **Details**. Klicke dann auf **Trennen**. X wird dann nicht mehr gelesen. Bereits importierte Inhalte bleiben erhalten.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** klicken.

## Auf X abmelden

Öffne auf X **Einstellungen** > **Sicherheit und Kontozugriff** > **Apps und Sitzungen** > **Sitzungen** und melde die Sitzung im Browser deiner Machine ab.
