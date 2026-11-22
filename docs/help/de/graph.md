---
title: The Graph
area: graph
summary: Die Menschen, Organisationen und Projekte in deinen Nachrichten, die sich selbst auf dem neuesten Stand halten.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 9052c679e45207f7
---
Deine Machine erstellt anhand deiner Nachrichten, Besprechungen und Entscheidungen eine Übersicht darüber, mit wem du zu tun hast und was gerade läuft. Du musst nichts einrichten, und alles bleibt auf deiner Machine.

- [Personen](people.md): alle, mit denen du Kontakt hast, jeweils mit einer Zusammenfassung und einem Verlauf.
- [Organisationen](organizations.md): die Unternehmen, für die sie arbeiten, mit den jeweiligen Personen und Projekten.
- [Projekte](projects.md): was gerade läuft, auf Boards mit Phasen, ähnlich wie Deals in einem CRM.

## Heute aktualisiert

Eine unaufdringliche Zeile oben in jeder Liste zeigt, was deine Machine heute aktualisiert hat, zum Beispiel **4 Personen heute aktualisiert**. Tippe darauf, um zu sehen, was sich geändert hat und bei wem. Wenn du einen Namen anklickst, öffnet sich die jeweilige Seite mit geöffneten **Letzte Änderungen**. Ein kleiner Punkt markiert jede Zeile und jede Board-Kachel, die heute geändert wurde. Gezählt werden nur Änderungen, die deine Machine selbst seit Mitternacht vorgenommen hat.

## Filtern und sortieren

Mit **Filtern** neben den Tabs kannst du die Liste eingrenzen. Jede Liste hat eigene Filter. Personen: Nähe, letzter Kontakt, Organisation, Inhaber, Tag und **Hat ein offenes Projekt**. Organisationen: Branche, Fachgebiet, Größe, Land, letzter Kontakt, Inhaber, Tag und **Hat ein offenes Projekt**. Projekte: Inhaber, Board, Phase, Tag, Organisation, Wert, voraussichtliches Abschlussdatum und **Keine Antwort seit 10+ Tagen**.

Die ausgewählten Filter werden über der Liste angezeigt, zusammen mit **Entfernen**. Bei Projekten gilt ein Filter für Liste und Board. Auf dem Handy werden die Filter in einem Sheet geöffnet.

Über das Sortiermenü kannst du die Liste sortieren. Personen und Organisationen lassen sich nach Nähe, neuestem oder ältestem Kontakt und Name sortieren. Organisationen außerdem nach Größe. Projekte lassen sich nach letzter Aktivität, Name, Phase, **Wert** und **Abschlussdatum** sortieren. Mit **CSV herunterladen** unter dem Sortiermenü kannst du den geöffneten Tab als Tabelle speichern.

## Felder und Tags

Unter „Felder“ kannst du den Wert einer Person, Organisation oder eines Projekts anklicken, um ihn zu ändern: Mit **Speichern** oder Enter wird die Änderung übernommen, mit **Abbrechen** oder Escape verworfen und mit **Entfernen** wird das Feld geleert.

Mit **Felder verwalten** (oder **Feld hinzufügen**, wenn es noch keine gibt) kannst du Felder für alle Einträge dieser Art hinzufügen oder entfernen. Über **Neues Feld** kannst du ein Text-, Zahlen- oder Datumsfeld oder eine Auswahl aus einer Liste hinzufügen.

Mit **+ Tag** fügst du einen Tag hinzu, zum Beispiel VIP oder Partner. Mit **×** entfernst du ihn. Tags erscheinen in den Listen. Auf dem Handy siehst du die Tags einer Person auf ihrer Seite. Über **Filtern** kannst du nach Tags suchen.

## Geburtstag

Der Geburtstag einer Person wird unter „Kontakt“ angezeigt, zusammen mit der Quelle: der Google-Kontakt, ein Geburtstag in Google Kalender (die Routine „Geburtstage“ speichert ihn für enge Kontakte), ein Facebook-Import, deine Notizen oder du selbst. Mit **Bearbeiten** kannst du den Geburtstag festlegen oder korrigieren: Monat und Tag sowie das Jahr, falls du es weißt. Dann wird auch das Alter angezeigt.

Deine Angabe hat Vorrang vor allen anderen Quellen und bleibt erhalten. Mit **Entfernen** löschst du sie. Ein Kontakt oder Import fügt sie nicht wieder hinzu.

Wenn noch kein Geburtstag eingetragen ist, kannst du ihn unter „Felder“ mit **Geburtstag hinzufügen** ergänzen. Die Routine „Geburtstage“ liest denselben Geburtstag aus, der auf der Seite angezeigt wird. Ein Geburtstag ist persönlich: Er wird nie mit deinem Team geteilt, auch nicht bei einem gemeinsam genutzten Eintrag.

## Tabelle importieren

Mit **CSV importieren…** unter dem Sortiermenü bei Personen, Organisationen oder Projekten kannst du eine als CSV gespeicherte Tabelle hinzufügen.

1. Prüfe die Spalten. Deine Machine erkennt anhand der Überschriften und Inhalte, wofür die Spalten gedacht sind. Du kannst die Zuordnung ändern. Wenn dein Modell ausgeführt werden kann, prüft es die Spalten ebenfalls und nennt kurz den Grund, wenn es sich nicht sicher ist. Es sieht nur die Überschriften, einige Werte pro Spalte und die Zellen, die sich mit den Regeln nicht lesen ließen.
2. Prüfe die Korrekturen. **Prüfen** zeigt sie im Vorher-Nachher-Vergleich: überzählige Leerzeichen, Namen in Großbuchstaben, Telefonnummern im internationalen Format, Tippfehler in E-Mail-Adressen (gmial.com), Websites als Domain, Datumsangaben und Werte in beliebigem Format („€12k“ entspricht 12000), mehrere Tags in einer Zelle, eine anders geschriebene Phase und doppelte Zeilen. Deaktiviere eine Art von Korrektur oder eine Zeile, wenn sie unverändert bleiben soll.
3. Prüfe die Vorschau. Jede Zeile wird als neu, als Übereinstimmung mit einem vorhandenen Eintrag in deinem Graph oder als übersprungen angezeigt, jeweils mit einer Begründung. Personen werden anhand der E-Mail-Adresse abgeglichen (sonst anhand von Name und Organisation), Organisationen anhand der Website oder des Namens und Projekte anhand des Namens.
4. Mit **Importieren** fügst du neue Einträge hinzu und ergänzt die übereinstimmenden. Leere Zellen ändern nichts.

Mit **Rückgängig** direkt nach dem Import oder **Letzten Import rückgängig machen** unter dem Sortiermenü kannst du den letzten Import rückgängig machen, solange die betroffenen Einträge seither nicht geändert wurden. Würde dadurch eine spätere Korrektur überschrieben, wird stattdessen der Grund angezeigt. Die Datei bleibt auf deiner Machine.

## Inhaber

In einer Work Fleet hat jede Person, Organisation und jedes Projekt einen Inhaber. Du findest **Inhaber** unter „Mit dir“ auf der jeweiligen Seite. Standardmäßig bist du der Inhaber, sofern du nicht jemanden aus deiner Work Fleet auswählst. Mit **Inhaber** unter „Filtern“ werden nur deine Einträge angezeigt. Jede Änderung erscheint im jeweiligen Verlauf.

## Team

Unter **Team** neben „Meine“ siehst du, was deine Teammitglieder teilen, mit denselben Tabs und demselben Sortiermenü. Mit **Filtern** kannst du nach der Person filtern, die etwas geteilt hat, nach einer Organisation (bei Personen) oder nach dem Status (bei Projekten). Was du dort hinzufügst, gehört dir.

Kundenarbeit wird mit den Machines deiner Teammitglieder geteilt, einschließlich Inhaber, Feldern und Tags. Die Einträge deiner Teammitglieder werden auch in deiner Machine angezeigt. In jedem Thread steht **Team** oder **Nur du**. Mehr dazu unter [Team Graph](team-graph.md).
