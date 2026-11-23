---
title: Notion
area: connections
summary: Kommentare, Erwähnungen und dir zugewiesene Aufgaben in Notion. Antworten, neue Seiten, Änderungen und das Erledigen von Aufgaben warten auf deine Zustimmung.
covers: connector:notion
code: connectors/notion.py, doc_writes.py, notion_heads_up.py
site: Sign in with Notion, Connect, More sources, Remove
translated: 2e93c261cc09e401
---
## Was Notion liest

Die Seiten, auf die deine Notion-Verbindung zugreifen kann. Sie bringt Folgendes ein:

- Kommentare auf deinen Seiten, Antworten in Diskussionen, an denen du beteiligt bist, und Kommentare, in denen du erwähnt wirst. Ein Kommentar, der deine Aufmerksamkeit braucht, wird zu einer Aufgabe.
- Datenbankeinträge, die dir zugewiesen sind, einschließlich Fälligkeitsdatum und Status. Jeder Eintrag wird zu einer Aufgabe, und sein Fälligkeitsdatum erscheint im **Kalender**. Sobald der Eintrag in Notion erledigt ist, wird die Aufgabe automatisch geschlossen. **Rückgängig** öffnet sie wieder.
- Neue Seiten, die andere hinzufügen und die du sehen kannst.
- Einen unaufdringlichen Hinweis, wenn jemand eine Seite ändert, deren Änderung du angefragt hast. Es gibt keinen Signalton.

Die erste Synchronisierung reicht 7 Tage zurück. Personen werden über ihre E-Mail-Adresse mit deinem [Graph](graph.md) verknüpft. Wenn Notion keine E-Mail-Adresse teilt, wird stattdessen der vollständige Name verwendet, sofern genau eine Person in deinem Graph diesen Namen hat.

Wenn du Notion nur zum Erledigen von Aufgaben verwenden möchtest, deaktiviere **Liefert Signale** unter **Details**.

## Was Notion tun kann

Wenn eine Aufgabe oder ein Termin den Text einer Seite benötigt, liest deine Machine diese eine Seite, und zwar nur, während sie daran arbeitet. Bei einer Datei auf der Seite sieht sie nur den Namen. Seiten findet sie anhand ihres Titels, nicht anhand der Dateien darauf.

Für jede dieser Aktionen wartet Notion bei der jeweiligen Aufgabe auf deine Zustimmung:

- Auf einen Kommentar in der zugehörigen Diskussion antworten.
- Eine neue Seite erstellen. Sie bleibt privat, bis du sie teilst.
- Eine Seite bearbeiten. Wähle „**Änderungen prüfen**“, um jeden Absatz vorher und nachher zu sehen, und dann „**Speichern**“. Notion schreibt nur in die Seite, so wie du sie gesehen hast. Wenn in der Zwischenzeit jemand Änderungen vorgenommen hat, wird nichts geschrieben und die Aufgabe weist dich darauf hin.
- Eine dir zugewiesene Aufgabe als erledigt markieren. Dabei ändert sich nur ihr Status.

Notion löscht, teilt oder verschiebt niemals eine Seite.

## Notion verbinden

1. Öffne im Dashboard **Verbindungen** und **Dokumente und Dateien**, dann Notion. Oder öffne auf der Einrichtungsseite einer gehosteten Machine unter app.themachine.computer/setup **Weitere Quellen** und dann Notion. Auf deinem eigenen Computer musst du zuerst dein Konto damit verknüpfen.
2. Wähle „**Mit Notion anmelden**“, dann deinen Arbeitsbereich und die Seiten, auf die Notion zugreifen darf, und erteile den Zugriff.
3. Zurück in The Machine prüft sie sofort die Anmeldung und zeigt den Namen des Arbeitsbereichs an.

Für einen weiteren Arbeitsbereich kannst du Notion erneut hinzufügen.

## Stattdessen ein Token einfügen

Wähle unter **Oder füge ein Integrationstoken ein** die Option „**Token holen**“. Notion öffnet die Integrationsseite. Erstelle eine interne Integration und erlaube ihr, Inhalte und Kommentare zu lesen und einzufügen sowie Nutzerinformationen mit E-Mail-Adressen zu lesen. Kopiere das Token, füge es ein und wähle „**Verbinden**“.

Teile anschließend deine Seiten in Notion unter **Verbindungen** auf jeder Seite mit der Integration. Auf deinem eigenen Computer fragt `assistant connect notion` ebenfalls danach.

## Notion entfernen

- Öffne im Dashboard **Verbindungen**, wähle Notion und dann **Details**. Wähle anschließend „**Trennen**“. Bereits übernommene Inhalte bleiben erhalten.
- Auf einer gehosteten Machine kannst du Notion auch auf der Einrichtungsseite daneben über „**Entfernen**“ entfernen.

## Zugriff in Notion widerrufen

Wähle in Notion **Einstellungen** und dann **Verbindungen**, und trenne The Machine. Bei einem eingefügten Token: Lösche die Integration auf der Integrationsseite.
