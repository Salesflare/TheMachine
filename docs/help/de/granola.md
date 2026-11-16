---
title: Granola
area: connections
summary: Notizen und Transkripte deiner Meetings in Granola. The Machine liest sie nur.
covers: connector:granola
code: connectors/granola.py, meeting_notes.py, onboarding.py
site: Connect, More sources, Remove
translated: fb6244142af7800d
---
## Was gelesen wird

Notizen und Transkripte von Meetings, an denen du teilgenommen hast: beim Verbinden die der letzten 7 Tage, danach neue, sobald sie dazukommen. Notizen, an denen Granola noch arbeitet, werden erst übernommen, wenn sie fertig sind.

Jeder Eintrag wird dem Meeting in deinem Kalender zugeordnet, das Granola benennt. Gibt es keines, wird er dem Meeting zur gleichen Zeit zugeordnet. Granolas Notizen erscheinen unter „Notizen“, das Transkript unter „Transkript“, jeweils mit der Markierung **Von Granola**. Was du selbst hinzugefügt hast, bleibt erhalten.

Nach dem Meeting liest The Machine daraus, was versprochen, beschlossen oder noch offen ist, zum Beispiel: „Ich schicke die Präsentation“. Aufgaben erstellt sie nur für klare nächste Schritte. Personen im Meeting werden anhand ihrer E-Mail-Adresse mit deinem [Graph](graph.md) verknüpft.

## Was damit gemacht werden kann

In Granola kann The Machine nichts tun. Sie liest nur und ändert, teilt oder löscht keine Notizen.

## Was benötigt wird

Ein persönlicher API-Schlüssel von Granola. API-Schlüssel gibt es in Granolas Business- und Enterprise-Tarifen. Der Schlüssel kann deine eigenen Notizen und die mit dir geteilten lesen, so wie du sie in Granola siehst.

## Granola verbinden

1. Öffne Granolas Desktop-App und gehe zu **Einstellungen**, Connectors, API keys. Erstelle einen Schlüssel mit dem Zugriff Personal notes und kopiere ihn.
2. Öffne im Dashboard **Verbindungen**, **Meetings**, Granola. Auf der Einrichtungsseite einer gehosteten Machine unter app.themachine.computer/setup findest du Granola unter **Weitere Quellen**. Auf deinem eigenen Computer fragt auch `assistant connect granola` danach.
3. Füge den Schlüssel ein, wähle **Arbeit** oder **Privat** und klicke auf **Verbinden**.

Der Schlüssel wird sofort überprüft. Wenn Granola ihn später ablehnt, wirst du bei Granola unter **Verbindungen** aufgefordert, einen neuen Schlüssel einzugeben.

## Granola trennen

- Öffne im Dashboard **Verbindungen**, dann Granola und **Details**, und klicke auf **Trennen**. Bereits übernommene Inhalte bleiben erhalten.
- Auf einer gehosteten Machine kannst du auch auf der Einrichtungsseite daneben auf **Entfernen** klicken.

## Schlüssel in Granola widerrufen

Öffne Granolas Desktop-App und gehe zu **Einstellungen**, Connectors, API keys. Lösche dann den Schlüssel.
