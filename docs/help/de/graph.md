---
title: Der Graph
area: graph
summary: Die Personen, Organisationen und Projekte aus deinen Nachrichten, die sich automatisch aktualisieren.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: e437109f98725e65
---
Deine Machine erstellt anhand deiner Nachrichten, Meetings und Entscheidungen eine Übersicht darüber, mit wem du zu tun hast und was gerade läuft. Du musst nichts einrichten, und alles bleibt auf deiner Machine.

- [Personen](people.md): alle, mit denen du Kontakt hast, mit einer Zusammenfassung und einem Zeitstrahl für jede Person.
- [Organisationen](organizations.md): die Unternehmen, in denen sie arbeiten, mit ihren Personen und Projekten.
- [Projekte](projects.md): aktuelle Themen auf Boards mit Phasen, wie Deals in einem CRM.
- [Notizen](notes.md): eine gut lesbare Seite pro Thema, zum Beispiel eine Reise oder dein Zuhause.

## Heute aktualisiert

Eine unaufdringliche Zeile oben in jeder Liste zeigt, was deine Machine heute aktualisiert hat, zum Beispiel **Heute 4 Personen aktualisiert**. Tippe darauf, um zu sehen, wer und was sich geändert hat. Wenn du einen Namen auswählst, öffnet sich die zugehörige Seite mit **Letzte Änderungen**. Ein kleiner Punkt markiert jede Zeile und jede Board-Kachel, die sie heute geändert hat. Gezählt werden nur Änderungen deiner Machine seit Mitternacht.

## Filtern und sortieren

Mit **Filtern** neben den Tabs kannst du die Liste eingrenzen. Jede Liste hat eigene Filter. Personen: Nähe, letzter Kontakt, Organisation, Inhaber, Tag und **Hat ein offenes Projekt**. Organisationen: Branche, Spezialgebiet, Größe, Land, letzter Kontakt, Inhaber, Tag und **Hat ein offenes Projekt**. Projekte: Inhaber, Board, Phase, Tag, Organisation, Wert, voraussichtliches Abschlussdatum und **Keine Antwort seit 10+ Tagen**.

Die ausgewählten Filter werden über der Liste angezeigt, zusammen mit **Entfernen**. Bei Projekten verwenden Liste und Board denselben Filter. Auf dem Smartphone werden die Filter als Sheet geöffnet.

Über das Sortiermenü kannst du die Liste sortieren. Personen und Organisationen lassen sich nach Nähe, neuestem oder ältestem Kontakt und Namen sortieren. Organisationen zusätzlich nach Größe. Projekte lassen sich nach letzter Aktivität, Namen, Phase, **Wert** und **Abschlussdatum** sortieren. Mit **CSV herunterladen** unter dem Sortiermenü kannst du den geöffneten Tab als Tabelle speichern.

## Felder und Tags

Klicke unter Felder bei einer Person, Organisation oder einem Projekt auf einen Wert, um ihn zu ändern. Mit **Speichern** oder Enter übernimmst du die Änderung. Mit **Abbrechen** oder Escape verwirfst du sie. Mit **Entfernen** leerst du das Feld.

Mit **Felder verwalten** (oder **Feld hinzufügen**, wenn noch keine Felder vorhanden sind) kannst du Felder für alle Einträge dieses Typs hinzufügen oder entfernen. **New field** fügt ein Feld hinzu: Text, Zahl, Datum oder eine Auswahl aus einer Liste.

Mit **+ Tag** fügst du ein Tag hinzu, zum Beispiel VIP oder Partner. Mit **×** entfernst du es. Tags werden in den Listen angezeigt und lassen sich mit **Filtern** finden.

## Geburtstag

Der Geburtstag einer Person wird unter Kontakt angezeigt, zusammen mit der Quelle: ihr Google-Kontakt, ein Geburtstag in Google Calendar (die Routine Birthdays speichert ihn für einen engen Kontakt), ein Facebook-Import, deine Notizen oder du selbst. Mit **Bearbeiten** kannst du den Geburtstag festlegen oder korrigieren: Monat und Tag sowie das Jahr, falls du es weißt. Dann wird auch das Alter angezeigt.

Deine Angabe hat Vorrang vor allen Quellen und bleibt bestehen. Mit **Entfernen** löschst du sie. Ein Kontakt oder Import fügt sie nicht wieder hinzu.

Wenn kein Geburtstag eingetragen ist, kannst du ihn unter Felder mit **Geburtstag hinzufügen** hinzufügen. Die Routine Birthdays liest denselben Geburtstag aus, der auf der Seite angezeigt wird. Ein Geburtstag ist persönlich: Er wird niemals mit deinem Team geteilt, auch nicht bei einem geteilten Eintrag.

## Tabelle importieren

Mit **CSV importieren…** unter dem Sortiermenü bei Personen, Organisationen oder Projekten kannst du eine als CSV gespeicherte Tabelle hinzufügen.

1. Prüfe die Spalten. Deine Machine erkennt anhand der Überschriften und Inhalte, wofür die einzelnen Spalten gedacht sind. Du kannst die Zuordnung ändern. Wenn dein Modell ausgeführt werden kann, prüft es die Spalten ebenfalls und nennt kurz den Grund, wenn es unsicher ist. Es sieht nur die Überschriften, einige Werte pro Spalte und die Zellen, die sich anhand der Regeln nicht lesen ließen.
2. Prüfe die Korrekturen. Unter **Prüfen** werden sie vorher und nachher angezeigt: überflüssige Leerzeichen, Namen in Großbuchstaben, Telefonnummern im internationalen Format, Tippfehler in E-Mail-Adressen (gmial.com), Websites als Domain, Datumsangaben und Werte in beliebigen Formaten ("€12k" sind 12000), mehrere Tags in einer Zelle, anders geschriebene Phasen und doppelte Zeilen. Deaktiviere einen Typ oder eine Zeile, um sie unverändert zu lassen.
3. Prüfe die Vorschau. Jede Zeile ist neu, stimmt mit einem vorhandenen Eintrag in deinem Graph überein oder wird übersprungen. Der Grund wird jeweils angezeigt. Personen werden anhand der E-Mail-Adresse abgeglichen (andernfalls anhand von Name und Organisation), Organisationen anhand der Website oder des Namens und Projekte anhand des Namens.
4. Mit **Importieren** fügst du neue Einträge hinzu und ergänzt die passenden vorhandenen Einträge. Eine leere Zelle ändert nichts.

Mit **Rückgängig** direkt nach dem Import oder mit **Letzten Import rückgängig machen** unter dem Sortiermenü kannst du den letzten Import zurücknehmen, solange sich die betroffenen Einträge seitdem nicht geändert haben. Würde dadurch eine spätere Korrektur überschrieben, wird stattdessen der Grund angezeigt. Die Datei bleibt auf deiner Machine.

## Inhaber

In einer Work Fleet hat jede Person, Organisation und jedes Projekt einen Inhaber. Du findest **Inhaber** unter „Bei dir“ auf der jeweiligen Seite. Standardmäßig bist du das. Du kannst aber auch jemanden aus deiner Work Fleet auswählen. Mit **Inhaber** unter **Filtern** werden nur deine Einträge angezeigt. Jede Änderung erscheint im jeweiligen Zeitstrahl.

## Team

Unter **Team** neben Meine siehst du, was deine Teammitglieder teilen, mit denselben Tabs und demselben Sortiermenü. Mit **Filtern** kannst du die Einträge danach eingrenzen, wer sie geteilt hat, nach Organisation (bei Personen) oder nach Status (bei Projekten). Was du dort hinzufügst, gehört dir.

Kundenarbeit wird mit den Machines deiner Teammitglieder geteilt, zusammen mit Inhaber, Feldern und Tags. Ihre geteilten Einträge erscheinen auch auf deiner Machine. In jedem Thread wird **Team** oder **Nur du** angezeigt. Weitere Informationen findest du unter [Team-Graph](team-graph.md).
