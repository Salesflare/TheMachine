---
title: Linear
area: connections
summary: Deine Linear-Issues, Erwähnungen, Kommentare, Reviews und Fälligkeitstermine. Kommentare, Status- und Zuweisungsänderungen sowie neue Issues warten auf dein OK.
covers: connector:linear
code: connectors/linear.py, linear_writes.py
site: Sign in with Linear, Connect, More sources, Remove
translated: 1e16b6abdf4fefad
---
## Was gelesen wird

Dein Linear-Posteingang und die dir zugewiesenen Issues. Folgendes wird übernommen:

- Dir zugewiesene Issues: neue Issues sowie Issues, deren Status, Fälligkeitstermin oder Titel geändert wurde. Wenn ein Issue in Linear erledigt oder abgebrochen ist, wird die zugehörige Aufgabe automatisch geschlossen. Mit **Rückgängig** öffnest du sie wieder.
- Erwähnungen von dir sowie Kommentare und Antworten zu Issues, denen du folgst.
- Review-Anfragen und Issues, die der Triage hinzugefügt wurden.
- Erinnerungen an Fälligkeitstermine.

Etwas wird nur dann zu einer Aufgabe, wenn es deine Aufmerksamkeit erfordert. Das wird anhand des Inhalts entschieden. Deine eigenen Änderungen werden nie übernommen. Der erste Abgleich reicht 7 Tage zurück. Personen werden über die E-Mail-Adresse, die Linear für sie anzeigt, mit deinem [Graph](graph.md) verknüpft.

Wenn du die Verbindung nur zum Erledigen von Aufgaben nutzen möchtest, deaktiviere unter **Details** die Option **Liefert Signale**.

## Was die Verbindung kann

Jede dieser Aktionen wartet bei der zugehörigen Aufgabe auf dein OK:

- Einen Kommentar zu einem Issue schreiben, auf das sich die Aufgabe bezieht, oder in einem Kommentar-Thread antworten. Der Beitrag erscheint unter deinem Namen.
- Den Status des Issues in einen Status des zugehörigen Teams ändern.
- Das Issue einer Person aus dem Team oder dir zuweisen.
- Ein neues Issue in einem deiner Teams erstellen.

Issues werden nie gelöscht, archiviert oder in ein anderes Team verschoben.

## Verbindung herstellen

1. Im Dashboard: **Verbindungen**, **+ Hinzufügen**, Linear. Oder auf der Einrichtungsseite einer gehosteten Machine unter app.themachine.computer/setup: **Weitere Quellen**, Linear. Auf deinem eigenen Computer koppelst du deine Machine zuerst mit deinem Konto.
2. Klicke auf **Mit Linear anmelden**, wähle deinen Workspace aus und erlaube den Zugriff.
3. Zurück in The Machine wird die Anmeldung sofort überprüft und der Name des Workspace angezeigt.

Für einen weiteren Workspace fügst du Linear erneut hinzu. Wähle wie bei jeder Verbindung **Arbeit** oder **Privat**.

## Stattdessen einen API-Schlüssel einfügen

Klicke unter **Oder füge einen API-Schlüssel ein** auf **Token holen**. Linear öffnet **Einstellungen** und **Sicherheit und Zugriff**. Erstelle einen persönlichen API-Schlüssel, kopiere ihn, füge ihn ein und klicke auf **Verbinden**. Auf deinem eigenen Computer wirst du ebenfalls danach gefragt: `assistant connect linear`.

## Verbindung entfernen

- Im Dashboard: **Verbindungen** öffnen, Linear auswählen, **Details** und dann **Trennen**. Bereits übernommene Inhalte bleiben erhalten.
- Auf einer gehosteten Machine kannst du auch auf der Einrichtungsseite neben der Verbindung auf **Entfernen** klicken.

## Zugriff in Linear widerrufen

Gehe in Linear zu **Einstellungen** und **Sicherheit und Zugriff** und widerrufe dort unter den autorisierten Anwendungen den Zugriff von The Machine. Wenn du einen Schlüssel eingefügt hast, widerrufe ihn auf derselben Seite.
