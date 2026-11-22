---
title: The Graph
area: graph
summary: Die Personen, Organisationen und Projekte in deinen Nachrichten, automatisch auf dem neuesten Stand.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 181ff5fa2a9d8f47
---
Deine Machine erstellt anhand deiner Nachrichten, Besprechungen und Entscheidungen eine Übersicht darüber, mit wem du zu tun hast und was gerade läuft. Du musst nichts einrichten, und alles bleibt auf deiner Machine.

- [Personen](people.md): alle, mit denen du Kontakt hast, jeweils mit einer Zusammenfassung und einem Zeitstrahl.
- [Organisationen](organizations.md): die Unternehmen, für die sie arbeiten, mit den zugehörigen Personen und Projekten.
- [Projekte](projects.md): was gerade läuft, auf Boards mit Phasen, wie Deals in einem CRM.

Deine eigenen Änderungen werden sofort angezeigt. Neue Personen, neue Nachrichten in ihren Zeitachsen und nachgeschlagene Details erscheinen innerhalb von 30 Minuten.

## Heute aktualisiert

Oben in jeder Liste steht dezent, was deine Machine heute aktualisiert hat, zum Beispiel **Heute 4 Personen aktualisiert**. Tippe darauf, um zu sehen, wer und was sich geändert hat. Wenn du einen Namen auswählst, öffnet sich die zugehörige Seite mit geöffneten **Letzte Änderungen**. Ein kleiner Punkt kennzeichnet jede Zeile und jede Board-Kachel, die heute geändert wurde. Gezählt werden nur Änderungen, die deine Machine selbst seit Mitternacht vorgenommen hat.

## Filtern und sortieren

Mit **Filtern** neben den Tabs schränkst du die Liste ein. Jede Liste hat eigene Filter. Personen: Nähe, letzter Kontakt, Organisation, Inhaber, Tag und **Hat ein offenes Projekt**. Organisationen: Branche, Spezialgebiet, Größe, Land, letzter Kontakt, Inhaber, Tag und **Hat ein offenes Projekt**. Projekte: Inhaber, Board, Phase, Tag, Organisation, Wert, erwartetes Abschlussdatum und **Keine Antwort seit 10+ Tagen**.

Die ausgewählten Filter erscheinen über der Liste neben **Entfernen**. Bei Projekten verwenden Liste und Board denselben Filter. Auf dem Handy öffnen sich die Filter in einem Fenster.

Über das Sortiermenü kannst du die Liste sortieren. Personen und Organisationen lassen sich nach Nähe, neuestem oder ältestem Kontakt und Namen sortieren. Organisationen außerdem nach Größe. Projekte lassen sich nach letzter Aktivität, Name, Phase, **Wert** und **Abschlussdatum** sortieren. Mit **CSV herunterladen** unter dem Sortiermenü speicherst du den aktuellen Tab als Tabelle.

## Felder und Tags

Unter „Felder“ kannst du den Wert bei einer Person, Organisation oder einem Projekt anklicken, um ihn zu ändern: Mit **Speichern** oder Enter übernimmst du ihn, mit **Abbrechen** oder Escape verwirfst du die Änderung und mit **Entfernen** leerst du das Feld.

Mit **Felder verwalten** oder, wenn noch keine Felder vorhanden sind, **Feld hinzufügen** kannst du Felder für alle Einträge dieser Art hinzufügen oder entfernen. Über **Neues Feld** fügst du ein Text-, Zahlen- oder Datumsfeld oder ein Auswahlfeld hinzu.

Mit **+ Tag** fügst du einen Tag hinzu, zum Beispiel VIP oder Partner. Über **×** entfernst du ihn wieder. Tags erscheinen in den Listen. Auf dem Handy werden die Tags einer Person auf ihrer Seite angezeigt. Mit **Filtern** kannst du nach Tags suchen.

## Geburtstag

Der Geburtstag einer Person steht unter „Kontakt“, zusammen mit der Angabe, woher er stammt: aus dem Google-Kontakt, einem Geburtstag in Google Kalender (die Routine „Geburtstage“ speichert ihn für enge Kontakte), einem Facebook-Import, deinen Notizen oder von dir. Mit **Bearbeiten** kannst du ihn festlegen oder korrigieren: Monat und Tag sowie, falls bekannt, das Jahr. Dann wird auch das Alter angezeigt.

Deine Angabe hat Vorrang vor allen anderen Quellen und bleibt bestehen. Mit **Entfernen** löschst du sie. Ein Kontakt oder Import trägt sie nicht erneut ein.

Wenn noch kein Geburtstag eingetragen ist, kannst du ihn über **Geburtstag hinzufügen** unter „Felder“ ergänzen. Die Routine „Geburtstage“ verwendet denselben Geburtstag, der auf der Seite angezeigt wird. Ein Geburtstag ist persönlich und wird nie mit deinem Team geteilt, auch nicht bei einem gemeinsam genutzten Eintrag.

## Tabelle importieren

Mit **CSV importieren…** unter dem Sortiermenü bei Personen, Organisationen oder Projekten kannst du eine als CSV gespeicherte Tabelle hinzufügen.

1. Überprüfe die Spalten. Deine Machine ordnet sie anhand der Überschriften und Inhalte zu. Du kannst die Zuordnung ändern. Wenn dein Modell ausgeführt werden kann, prüft es die Spalten ebenfalls und nennt kurz den Grund, wenn es unsicher ist. Es sieht nur die Überschriften, einige Werte pro Spalte und die Zellen, die sich mit den Regeln nicht auslesen ließen.
2. Überprüfe die Korrekturen. Unter **Prüfen** werden sie vorher und nachher angezeigt: zusätzliche Leerzeichen, Namen in Großbuchstaben, Telefonnummern im internationalen Format, Tippfehler in E-Mail-Adressen (gmial.com), Websites als Domain, Datumsangaben und Werte in beliebigem Format ("€12k" entspricht 12000), mehrere Tags in einer Zelle, abweichend geschriebene Phasen und doppelte Zeilen. Deaktiviere eine Art oder Zeile, wenn sie unverändert bleiben soll.
3. Überprüfe die Vorschau. Jede Zeile ist entweder neu, stimmt mit einem Eintrag in deinem Graph überein oder wird übersprungen. Der Grund wird jeweils angezeigt. Personen werden anhand der E-Mail-Adresse zugeordnet, andernfalls anhand des Namens und der Organisation. Organisationen werden anhand der Website oder des Namens zugeordnet, Projekte anhand des Namens.
4. Mit **Importieren** fügst du neue Einträge hinzu und ergänzt die passenden bestehenden Einträge. Leere Zellen ändern nichts.

Mit **Rückgängig** direkt nach dem Import oder **Letzten Import rückgängig machen** unter dem Sortiermenü kannst du den letzten Import rückgängig machen, solange die betreffenden Einträge seitdem nicht geändert wurden. Wenn dadurch eine spätere Korrektur überschrieben würde, wird stattdessen der Grund angezeigt. Die Datei bleibt auf deiner Machine.

## Inhaber

In einer Work Fleet hat jede Person, Organisation und jedes Projekt einen Inhaber. Du findest ihn unter „Bei dir“ auf der jeweiligen Seite bei **Inhaber**. Standardmäßig bist du der Inhaber, du kannst aber auch jemanden aus deiner Work Fleet auswählen. Mit **Inhaber** unter „Filtern“ werden nur deine Einträge angezeigt. Jede Änderung erscheint in der jeweiligen Zeitachse.

## Team

Unter **Team** neben „Meine“ siehst du, was deine Teammitglieder teilen. Dort gibt es dieselben Tabs und dasselbe Sortiermenü. Mit **Filtern** kannst du nach der Person filtern, die den Eintrag geteilt hat, nach einer Organisation (Personen) oder nach dem Status (Projekte). Was du dort hinzufügst, gehört dir.

Kundenarbeit wird mit den Machines deiner Teammitglieder geteilt, einschließlich Inhaber, Feldern und Tags. Ihre Kundenarbeit wird auch auf deiner Machine angezeigt. In jedem Thread steht **Team** oder **Nur du**. Weitere Informationen findest du unter [Team Graph](team-graph.md).
