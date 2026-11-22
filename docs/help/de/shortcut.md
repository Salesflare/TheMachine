---
title: Shortcut
area: connections
summary: Stories, deren Status sich ändert, mit Zuständigen und Fristen. Die Verbindung liest nur.
covers: connector:shortcut
code: connectors/shortcut.py
site: Sign in with Shortcut, Connect, More sources, Remove
translated: 68419e11fabc157c
---
## Was gelesen wird

Stories in deinem Shortcut-Workspace, deren Status sich ändert, mit den Zuständigen und Fristen.

## Was die Verbindung kann

In Shortcut kann sie nichts ändern. Sie liest nur.

## Shortcut verbinden

1. Im Dashboard: **Verbindungen**, **Projekte und Code**, Shortcut. Oder auf der Einrichtungsseite einer gehosteten Machine unter app.themachine.computer/setup: **Weitere Quellen**, Shortcut. Auf deinem eigenen Computer musst du ihn zuerst mit deinem Konto koppeln.
2. Klicke auf **Mit Shortcut anmelden** und erlaube den Lesezugriff. Shortcut wird nur um Lesezugriff gebeten.
3. Zurück in The Machine wird die Anmeldung sofort überprüft. The Machine zeigt dir, mit welchem Konto und in welchem Workspace die Verbindung besteht.

Nutzt du mehrere Shortcut-Workspaces? Wechsle zuerst in Shortcut zum gewünschten Workspace. Für einen weiteren Workspace musst du Shortcut erneut hinzufügen.

## Stattdessen einen Token einfügen

Klicke unter **Oder füge einen API-Token ein** auf **Token holen**. Shortcut öffnet die API-Tokens-Seite in einem neuen Tab. Erstelle einen Token, kopiere ihn, füge ihn ein und klicke auf **Verbinden**. Auf deinem eigenen Computer fragt `assistant connect shortcut` ebenfalls danach. Ein Token hat vollen Zugriff auf dein Konto, aber The Machine liest damit nur.

## Verbindung entfernen

- Im Dashboard: **Verbindungen**, öffne Shortcut, **Details** und dann **Trennen**. Was bereits übertragen wurde, bleibt erhalten.
- Auf einer gehosteten Machine kannst du Shortcut auch über **Entfernen** daneben auf der Einrichtungsseite entfernen.

## Zugriff in Shortcut widerrufen

Einen eingefügten Token löschst du auf der API-Tokens-Seite. Wenn du dich angemeldet hast, beendet **Trennen** hier alle Lesezugriffe.
