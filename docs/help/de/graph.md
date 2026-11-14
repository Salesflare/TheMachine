---
title: Der Graph
area: graph
summary: Die Menschen, Organisationen und Projekte in deinen Nachrichten, immer aktuell.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 850a4e2905f54511
---
Deine Machine erstellt anhand deiner Nachrichten, Besprechungen und Entscheidungen eine Übersicht darüber, mit wem du zu tun hast und was gerade läuft. Du musst nichts einrichten, und alles bleibt auf deiner Machine.

- [Personen](people.md): alle, mit denen du in Kontakt stehst, jeweils mit einer Zusammenfassung und einem Zeitstrahl.
- [Organisationen](organizations.md): die Unternehmen, bei denen sie arbeiten, mit ihren Personen und Projekten.
- [Projekte](projects.md): was gerade läuft, auf Boards mit Phasen, wie Deals in einem CRM.

## Heute aktualisiert

Eine unauffällige Zeile oben in jeder Liste zeigt, was deine Machine heute aktualisiert hat, zum Beispiel **Heute 4 Personen aktualisiert**. Tippe darauf, um zu sehen, wer und was sich geändert hat. Wenn du einen Namen auswählst, öffnet sich die entsprechende Seite mit geöffneten **Letzte Änderungen**. Ein kleiner Punkt markiert jede Zeile und Board-Kachel, die sie heute geändert hat. Gezählt werden nur Änderungen, die deine Machine selbst seit Mitternacht vorgenommen hat.

## Filtern und sortieren

Mit **Filtern** neben den Tabs kannst du die Liste eingrenzen. Jede Liste hat eigene Filter. Personen: Nähe, letzter Kontakt, Organisation, Inhaber, Tag und **Hat ein offenes Projekt**. Organisationen: Branche, Fachgebiet, Größe, Land, letzter Kontakt, Inhaber, Tag und **Hat ein offenes Projekt**. Projekte: Inhaber, Board, Phase, Tag, Organisation, Wert, voraussichtliches Abschlussdatum und **Keine Antwort seit 10+ Tagen**.

Die ausgewählten Filter erscheinen über der Liste, zusammen mit **Entfernen**. Bei Projekten verwenden Liste und Board denselben Filter. Auf dem Smartphone werden die Filter als Sheet geöffnet.

Über das Sortiermenü kannst du die Liste sortieren. Personen und Organisationen lassen sich nach Nähe, neuestem oder ältestem Kontakt und Name sortieren. Organisationen lassen sich außerdem nach Größe sortieren. Projekte lassen sich nach letzter Aktivität, Name, Phase, **Wert** und **Abschlussdatum** sortieren. Mit **CSV herunterladen** unter dem Sortiermenü speicherst du den aktuellen Tab als Tabelle.

## Felder und Tags

Klicke im Abschnitt **Felder** einer Person, Organisation oder eines Projekts auf einen Wert, um ihn zu ändern: Mit **Speichern** oder Enter übernimmst du die Änderung, mit **Abbrechen** oder Escape verwirfst du sie, und mit **Entfernen** leerst du das Feld.

Mit **Felder verwalten** (**Feld hinzufügen**, wenn es noch keine gibt) kannst du Felder für alle Einträge dieser Art hinzufügen oder entfernen. Mit **Neues Feld** fügst du ein Feld hinzu: Text, Zahl, Datum oder eine Auswahl aus einer Liste.

Mit **+ Tag** fügst du ein Tag hinzu, zum Beispiel VIP oder Partner. Mit **×** entfernst du es wieder. Tags werden in den Listen angezeigt und lassen sich über **Filtern** finden.

## Geburtstag

Der Geburtstag einer Person erscheint unter **Kontakt** zusammen mit der Quelle: aus ihren Google-Kontakten, aus einem Geburtstag in Google Kalender (die Geburtstags-Routine speichert ihn für enge Kontakte), aus einem Facebook-Import, aus deinen Notizen oder von dir. Mit **Bearbeiten** kannst du ihn festlegen oder korrigieren: Monat und Tag sowie das Jahr, wenn du es weißt. Dann wird auch das Alter angezeigt.

Dein Eintrag hat Vorrang vor allen anderen Quellen und bleibt erhalten. Mit **Entfernen** löschst du ihn. Ein Kontakt oder Import fügt ihn nicht wieder hinzu.

Wenn noch kein Geburtstag eingetragen ist, kannst du ihn unter **Felder** mit **Geburtstag hinzufügen** ergänzen. Die Geburtstags-Routine verwendet denselben Geburtstag, der auf der Seite angezeigt wird. Ein Geburtstag ist privat: Er wird auch bei einem geteilten Eintrag niemals mit deinem Team geteilt.

## Tabelle importieren

Mit **CSV importieren…** unter dem Sortiermenü bei Personen, Organisationen oder Projekten kannst du eine als CSV gespeicherte Tabelle hinzufügen.

1. Überprüfe die Spalten. Deine Machine erkennt anhand der Überschriften und Inhalte, welche Spalte welche ist. Du kannst die Zuordnung ändern. Wenn dein Modell ausgeführt werden kann, prüft es die Spalten ebenfalls und nennt kurz den Grund, wenn es unsicher ist. Es sieht nur die Überschriften, einige Werte pro Spalte und die Zellen, die sich anhand der Regeln nicht lesen ließen.
2. Überprüfe die Korrekturen. Unter **Prüfen** werden sie als Vorher und Nachher aufgelistet: zusätzliche Leerzeichen, Namen in Großbuchstaben, Telefonnummern im internationalen Format, Tippfehler in E-Mail-Adressen (gmial.com), Websites als Domain, Datumsangaben und Werte in beliebigem Format („€12k“ entspricht 12000), mehrere Tags in einer Zelle, eine anders geschriebene Phase und dieselbe Zeile zweimal. Deaktiviere eine Art von Korrektur oder eine Zeile, wenn du sie unverändert lassen möchtest.
3. Überprüfe die Vorschau. Jede Zeile ist neu, stimmt mit einem Eintrag in deinem Graph überein oder wird übersprungen. Der Grund wird jeweils angezeigt. Eine Person wird anhand der E-Mail-Adresse zugeordnet (wenn keine vorhanden ist, anhand von Name und Organisation), eine Organisation anhand der Website oder des Namens und ein Projekt anhand des Namens.
4. Mit **Importieren** fügst du neue Einträge hinzu und ergänzt die übereinstimmenden Einträge. Leere Zellen ändern nichts.

Mit **Rückgängig** direkt danach oder **Letzten Import rückgängig machen** unter dem Sortiermenü machst du den letzten Import rückgängig, solange die betroffenen Einträge seitdem nicht geändert wurden. Wenn dadurch eine spätere Korrektur überschrieben würde, wird stattdessen der Grund angezeigt. Die Datei bleibt auf deiner Machine.

## Inhaber

In einer Work Fleet hat jede Person, Organisation und jedes Projekt einen Inhaber. Du findest **Inhaber** unter „Bei dir“ auf der jeweiligen Seite. Standardmäßig bist du das, aber du kannst auch jemanden aus deiner Work Fleet auswählen. Über **Inhaber** unter **Filtern** kannst du nur deine Einträge anzeigen. Jede Änderung erscheint im Zeitstrahl.

## Team

Unter **Team** neben **Meine** siehst du, was deine Teammitglieder teilen. Die Tabs und das Sortiermenü sind dieselben. Mit **Filtern** kannst du nach der Person filtern, die den Eintrag geteilt hat, nach einer Organisation (bei Personen) oder nach dem Status (bei Projekten). Was du dort hinzufügst, gehört dir.

Die Arbeit mit Kunden wird mit der Machine jedes Teammitglieds geteilt, zusammen mit Inhaber, Feldern und Tags. Die geteilten Inhalte deiner Teammitglieder erscheinen auch auf deiner Machine. Bei jedem Thread steht **Team** oder **Nur du**. Weitere Informationen findest du unter [Team-Graph](team-graph.md).
