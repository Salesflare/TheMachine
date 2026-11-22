---
title: X
area: connections
summary: Deine Erwähnungen, Antworten und Direktnachrichten auf X, gelesen im eigenen Browser deiner Machine. Sendet erst nach deiner Freigabe.
covers: connector:x
code: connectors/x.py, integrations/x_inbox.py
site: Connect, More sources, Remove
translated: 5cbe43055458daf4
---
## Was es liest

Deine Erwähnungen, Antworten und Direktnachrichten auf X. Es liest sie im eigenen Browser deiner Machine, als du angemeldet. Es markiert nichts als gesehen und kann verschlüsselte X Chat-Nachrichten nicht lesen.

## Was es senden kann

Eine Antwort oder eine Direktnachricht, und nur, nachdem du sie bei der Aufgabe freigegeben hast.

Das läuft nicht über die offizielle API von X. Lesen und ab und zu eine Antwort, die du freigegeben hast, machen so gut wie nie Probleme; massenhaftes oder automatisches Senden kann zur Sperrung eines Kontos führen.

## Verbinden

Auf einer gehosteten Machine:

1. Öffne deine Einrichtungsseite unter app.themachine.computer/setup und geh zu **Weitere Quellen**.
2. Öffne X, gib deinen Handle ohne @ ein, melde dich bei X im Browser deiner Machine an, wenn es danach fragt, und tippe dann auf **Verbinden**.

Auf deinem eigenen Computer:

1. Öffne im Dashboard **Verbindungen**, dann **Chat**, und wähle X.
2. Wähle **Arbeit** mit der zugehörigen Firma oder **Privat**, gib deinen Handle ohne @ ein und tippe auf **Verbinden**.
3. Tippe auf **Bei X anmelden** und melde dich im Browser deiner Machine an. Sobald du drin bist, verbindet es sich von selbst.

Oder führe `assistant connect x` in einem Terminal aus.

Wenn X deine Machine abmeldet, siehe [Von einer Website abgemeldet](signed-out.md).

## Entfernen

- Im Dashboard: **Verbindungen**, X öffnen, **Details**, dann **Trennen**. Es hört auf zu lesen. Was es schon reingebracht hat, bleibt.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** tippen.

## Bei X abmelden

Öffne in X Einstellungen, Sicherheit und Kontozugriff, Apps und Sitzungen, Sitzungen, und melde die Sitzung des Browsers deiner Machine ab.
