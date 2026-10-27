---
title: Trello
area: connections
summary: Kartenänderungen, Kommentare und Aktivität auf einem Trello-Board. Es liest nur.
covers: connector:trello
code: connectors/trello.py
site: Connect, More sources, Remove
---
## Was es liest

Kartenänderungen, Kommentare und Aktivität auf einem Trello-Board pro Verbindung. Es markiert ein Board nie als angesehen.

## Was es tun kann

Nichts in Trello. Es liest nur.

## Verbinden

1. Erstelle unter trello.com/power-ups/admin ein Power-Up mit beliebigem Namen.
2. Öffne seine Seite für den API-Schlüssel und kopiere den API-Schlüssel (nicht das Secret).
3. Klick auf den Token-Link daneben, erlaube Lesezugriff und kopiere das Token.
4. Auf einer gehosteten Machine: Öffne deine Einrichtungsseite unter app.themachine.computer/setup, geh zu **Weitere Quellen** und öffne Trello. Auf deinem eigenen Computer: **Verbindungen**, **+ Hinzufügen**, Trello, oder `assistant connect trello`.
5. Gib die Adresse des Boards, den API-Schlüssel und das Token an und tippe dann auf **Verbinden**.

## Entfernen

- Im Dashboard: **Verbindungen**, das Board öffnen, **Details**, dann **Trennen**. Was es schon reingebracht hat, bleibt.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** tippen.

## In Trello widerrufen

Widerrufe das Token in den Einstellungen deines Trello-Kontos unter Applications, oder lösche das Power-Up.
