---
title: RSS-Feeds
area: connections
summary: Beiträge aus einem RSS- oder Atom-Feed, dem du folgst.
covers: connector:rss
code: connectors/rss.py
site: More sources
translated: efeb27dadc6163e9
---
## Was gelesen wird

Neue Beiträge aus einem RSS- oder Atom-Feed pro Verbindung. Füge für jeden Feed eine separate Verbindung hinzu.

Der Feed wird alle 30 Minuten gelesen, aber nie häufiger als alle 15 Minuten. Es werden nur öffentliche https://-Adressen gelesen.

## Was möglich ist

Nichts. Es wird nur der Feed gelesen.

## Verbindung herstellen

1. Öffne im Dashboard **Verbindungen** und dann **Andere**. Wähle RSS-Feed aus. Auf einer gehosteten Machine findest du die Einrichtung auch unter **Weitere Quellen**. Auf deinem eigenen Computer kannst du auch `assistant connect rss` ausführen.
2. Füge die Adresse des Feeds ein.

## Verbindung entfernen

Im Dashboard: Öffne **Verbindungen**, wähle den Feed und dann **Details** und **Trennen**. Anderswo muss nichts deinstalliert werden.
