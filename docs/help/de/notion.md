---
title: Notion
area: connections
summary: Kommentare, Erwähnungen und dir zugewiesene Aufgaben in Notion. Antworten, neue Seiten, Änderungen und das Erledigen von Aufgaben warten auf deine Zustimmung.
covers: connector:notion
code: connectors/notion.py, doc_writes.py, notion_heads_up.py
site: Sign in with Notion, Connect, More sources, Remove
translated: 8544baf8c60cc40b
---
## Was sie liest

Die Seiten, die deine Notion-Verbindung sehen kann. Sie bringt Folgendes ein:

- Kommentare auf deinen Seiten, Antworten in Diskussionen, an denen du teilnimmst, und Kommentare, in denen du erwähnt wirst. Wenn du etwas tun musst, wird daraus eine Aufgabe.
- Datenbankeinträge, die dir zugewiesen sind, samt Fälligkeitsdatum und Status. Aus jedem wird eine Aufgabe, und das Fälligkeitsdatum wird im **Kalender** angezeigt. Wenn der Eintrag in Notion erledigt ist, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** öffnest du sie wieder.
- Neue Seiten, die andere hinzufügen und die du sehen kannst.
- Einen stillen Hinweis, wenn jemand eine Seite ändert, die du ändern lassen wolltest. Es gibt nie einen Signalton.

Der erste Abgleich reicht 7 Tage zurück. Personen werden anhand ihrer E-Mail-Adresse mit deinem [Graph](graph.md) verknüpft. Wenn Notion keine E-Mail-Adresse teilt, erfolgt die Verknüpfung nur anhand des vollständigen Namens, wenn genau eine Person in deinem Graph diesen Namen hat.

Damit sie nur Dinge erledigt, deaktiviere **Liefert Signale** unter **Details**.

## Was sie tun kann

Wenn eine Aufgabe oder ein Termin den Text einer Seite benötigt, liest deine Machine diese Seite, und zwar nur, während sie daran arbeitet.

Jede dieser Aktionen wartet auf deine Zustimmung bei der jeweiligen Aufgabe:

- Auf einen Kommentar in der zugehörigen Diskussion antworten.
- Eine neue Seite erstellen. Sie ist privat, bis du sie teilst.
- Eine Seite bearbeiten. Drücke **Änderungen prüfen**, um jeden Absatz vorher und nachher anzusehen, und dann **Speichern**. Geschrieben wird nur in die Seite, wie du sie gesehen hast. Wenn jemand die Seite zwischenzeitlich geändert hat, wird nichts übernommen und die Aufgabe weist dich darauf hin.
- Eine dir zugewiesene Aufgabe als erledigt markieren. Dabei ändert sich nur ihr Status.

Sie löscht, teilt oder verschiebt niemals eine Seite.

## Verbindung herstellen

1. Im Dashboard: **Verbindungen**, **Dokumente und Dateien**, Notion. Oder auf der Einrichtungsseite einer gehosteten Machine unter app.themachine.computer/setup: **Weitere Quellen**, Notion. Auf deinem eigenen Computer musst du ihn zuerst mit deinem Konto koppeln.
2. Drücke **Mit Notion anmelden**, wähle deinen Workspace und die Seiten aus, die sie sehen darf, und erteile den Zugriff.
3. Zurück in The Machine prüft sie sofort die Anmeldung und zeigt den Namen des Workspaces an.

Für einen weiteren Workspace füge Notion erneut hinzu.

## Stattdessen ein Token einfügen

Drücke unter **Oder füge ein Integrationstoken ein** auf **Token holen**. Notion öffnet die Integrationsseite: Erstelle eine interne Integration, erlaube das Lesen und Einfügen von Inhalten und Kommentaren sowie das Lesen von Nutzerinformationen mit E-Mail-Adressen. Kopiere das Token, füge es ein und drücke **Verbinden**.

Teile die Seiten anschließend in Notion unter **Verbindungen** auf jeder Seite mit der Integration. Auf deinem eigenen Computer fragt auch `assistant connect notion` danach.

## Verbindung entfernen

- Im Dashboard: **Verbindungen**, öffne Notion und wähle **Details** und dann **Trennen**. Bereits importierte Inhalte bleiben erhalten.
- Auf einer gehosteten Machine kannst du sie auch über **Entfernen** neben Notion auf der Einrichtungsseite entfernen.

## Zugriff in Notion widerrufen

In Notion: **Einstellungen**, **Verbindungen** und dann The Machine trennen. Wenn du ein Token eingefügt hast, lösche die Integration auf der Integrationsseite.
