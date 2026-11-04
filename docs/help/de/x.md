---
title: X
area: connections
summary: Deine Erwähnungen, Antworten und Direktnachrichten auf X, gelesen im eigenen Browser deiner Machine. Sendet erst nach deiner Freigabe.
covers: connector:x
code: connectors/x.py, integrations/x_inbox.py
site: Connect, More sources, Remove
---
## Was es liest

Deine Erwähnungen, Antworten und Direktnachrichten auf X. Es liest sie im eigenen Browser deiner Machine, mit dir angemeldet. Es nutzt nicht die Entwickler-API von X, markiert nichts als gesehen und kann verschlüsselte X Chat-Nachrichten nicht lesen.

## Was es senden kann

Eine Antwort oder eine Direktnachricht, und nur, nachdem du sie bei der Aufgabe freigegeben hast.

## Verbinden

Auf einer gehosteten Machine:

1. Öffne deine Einrichtungsseite unter app.themachine.computer/setup und geh zu **Weitere Quellen**.
2. Öffne X, gib deinen Handle ohne @ ein, melde dich bei X im Browser deiner Machine an, wenn es danach fragt, und tippe dann auf **Verbinden**.

Auf deinem eigenen Computer:

1. Öffne im Dashboard **Verbindungen**, dann **+ Hinzufügen**, und wähle X.
2. Wähle **Arbeit** mit ihrer Firma oder **Privat**, gib deinen Handle ohne @ ein und tippe auf **Verbinden**.
3. Tippe auf **Bei X anmelden** und melde dich im Browser deiner Machine an. Sobald du drin bist, verbindet es sich von selbst.

Oder führe `assistant connect x` aus und gib deinen Handle ein und den Handle, mit dem der Browser normalerweise angemeldet ist.

Wenn X deine Machine abmeldet, siehe [Von einer Website abgemeldet](signed-out.md).

## Entfernen

- Im Dashboard: **Verbindungen**, X öffnen, **Details**, dann **Trennen**. Es hört auf zu lesen. Was es schon reingebracht hat, bleibt.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** tippen.

## Bei X abmelden

Öffne in X Einstellungen, Sicherheit und Kontozugriff, Apps und Sitzungen, Sitzungen, und melde die Sitzung des Browsers deiner Machine ab.
