---
title: X
area: connections
summary: Deine Erwähnungen, Antworten und Direktnachrichten auf X werden im Browser deiner Machine gelesen. Gesendet wird nur nach deiner Freigabe.
covers: connector:x
code: connectors/x.py, integrations/x_inbox.py
site: Connect, More sources, Remove
translated: 5cbe43055458daf4
---
## Was gelesen wird

Deine Erwähnungen, Antworten und Direktnachrichten auf X, im Browser deiner Machine und mit deinem Konto angemeldet. Sie markiert nichts als gelesen und kann keine verschlüsselten X Chats lesen.

## Was gesendet werden kann

Eine Antwort oder eine Direktnachricht, und zwar nur, nachdem du sie in der Aufgabe freigegeben hast.

Das läuft nicht über die offizielle API von X. Lesen und eine gelegentliche, von dir freigegebene Antwort führen sehr wahrscheinlich zu keinen Problemen. Massenhaftes oder automatisiertes Senden kann dazu führen, dass dein Konto gesperrt wird.

## Verbinden

Auf einer gehosteten Machine:

1. Öffne deine Setup-Seite unter app.themachine.computer/setup und gehe zu **Weitere Quellen**.
2. Öffne X, gib deinen Handle ohne @ ein und melde dich auf Nachfrage im Browser deiner Machine bei X an. Drücke dann **Verbinden**.

Auf deinem eigenen Computer:

1. Öffne im Dashboard **Verbindungen**, dann **Chat**, und wähle X aus.
2. Wähle **Arbeit** mit dem zugehörigen Unternehmen oder **Privat**, gib deinen Handle ohne @ ein und drücke **Verbinden**.
3. Drücke **Bei X anmelden** und melde dich im Browser deiner Machine an. Sobald du angemeldet bist, wird die Verbindung automatisch hergestellt.

Oder führe `assistant connect x` in einem Terminal aus.

Wenn X deine Machine abmeldet, lies den Artikel [Von einer Website abgemeldet](signed-out.md).

## Verbindung trennen

- Im Dashboard: Öffne **Verbindungen**, wähle X aus und gehe zu **Details**. Drücke dann **Trennen**. Das Lesen wird beendet. Bereits übernommene Inhalte bleiben erhalten.
- Auf einer gehosteten Machine kannst du auf deiner Setup-Seite auch daneben auf **Entfernen** drücken.

## Auf X abmelden

Öffne in X **Einstellungen**, **Sicherheit und Kontozugriff**, **Apps und Sitzungen**, **Sitzungen** und melde die Sitzung des Browsers deiner Machine ab.
