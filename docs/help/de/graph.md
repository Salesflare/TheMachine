---
title: The Graph
area: graph
summary: Die Personen, Unternehmen und Projekte in deinen Nachrichten, die sich selbst aktuell halten.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 850a4e2905f54511
---
Deine Machine erstellt aus deinen Nachrichten, Besprechungen und Entscheidungen eine Übersicht darüber, mit wem du zu tun hast und was gerade läuft. Du musst nichts einrichten, und alles bleibt auf deiner Machine.

- [Personen](people.md): alle, mit denen du in Kontakt bist, jeweils mit einer Zusammenfassung und einem Zeitstrahl.
- [Unternehmen](organizations.md): die Unternehmen, bei denen sie arbeiten, mit den dazugehörigen Personen und Projekten.
- [Projekte](projects.md): was gerade läuft, auf Boards mit Phasen, ähnlich wie Deals in einem CRM.

## Heute aktualisiert

Oben in jeder Liste steht unauffällig, was deine Machine heute aktualisiert hat, zum Beispiel **Heute 4 Personen aktualisiert**. Tippe darauf, um zu sehen, wer und was sich geändert hat. Wenn du einen Namen öffnest, ist **Letzte Änderungen** geöffnet. Ein kleiner Punkt markiert jede Zeile und jede Kachel auf einem Board, die heute geändert wurde. Gezählt werden nur Änderungen, die deine Machine selbst seit Mitternacht vorgenommen hat.

## Filtern und sortieren

Mit **Filtern** neben den Tabs grenzt du die Liste ein. Für jede Liste gibt es eigene Filter. Personen: Nähe, letzter Kontakt, Unternehmen, Inhaber, Tag und **Hat ein offenes Projekt**. Unternehmen: Branche, Spezialgebiet, Größe, Land, letzter Kontakt, Inhaber, Tag und **Hat ein offenes Projekt**. Projekte: Inhaber, Board, Phase, Tag, Unternehmen, Wert, voraussichtliches Abschlussdatum und **Keine Antwort seit 10+ Tagen**.

Die ausgewählten Filter erscheinen über der Liste neben **Entfernen**. Bei Projekten gilt ein Filter sowohl für die Liste als auch für das Board. Auf dem Smartphone öffnen sich die Filter in einem Fenster.

Im Sortiermenü kannst du die Liste sortieren. Personen und Unternehmen lassen sich nach Nähe, neuestem oder ältestem Kontakt und Name sortieren. Unternehmen lassen sich außerdem nach Größe sortieren. Projekte lassen sich nach letzter Aktivität, Name, Phase, **Wert** und **Abschlussdatum** sortieren. Mit **CSV herunterladen** unter dem Sortiermenü speicherst du den geöffneten Tab als Tabelle.

## Felder und Tags

Unter „Felder“ kannst du bei einer Person, einem Unternehmen oder einem Projekt auf einen Wert klicken, um ihn zu ändern. Mit **Speichern** oder Enter übernimmst du die Änderung, mit **Abbrechen** oder Escape verwirfst du sie und mit **Entfernen** leerst du das Feld.

Mit **Felder verwalten** oder, wenn noch keine Felder vorhanden sind, **Feld hinzufügen** kannst du Felder für alle Einträge dieser Art hinzufügen oder entfernen. Mit **Neues Feld** fügst du ein Text-, Zahlen- oder Datumsfeld hinzu oder ein Feld mit Auswahlmöglichkeiten.

Mit **+ Tag** fügst du einen Tag hinzu, zum Beispiel VIP oder Partner. Mit **×** entfernst du ihn. Tags werden in den Listen angezeigt und lassen sich mit **Filtern** finden.

## Geburtstag

Der Geburtstag einer Person wird unter „Kontakt“ angezeigt, zusammen mit der Quelle: ihr Google-Kontakt, ein Geburtstag in Google Calendar (die Routine „Geburtstage“ speichert ihn für enge Kontakte), ein Facebook-Import, deine Notizen oder du selbst. Mit **Bearbeiten** kannst du ihn eintragen oder korrigieren: Monat und Tag sowie, wenn du ihn kennst, das Jahr. Dann wird auch das Alter angezeigt.

Deine Angaben haben Vorrang vor allen anderen Quellen und bleiben erhalten. Mit **Entfernen** löschst du den Geburtstag. Ein Kontakt oder Import fügt ihn nicht wieder hinzu.

Wenn noch kein Geburtstag eingetragen ist, kannst du ihn unter „Felder“ mit **Geburtstag hinzufügen** hinzufügen. Die Routine „Geburtstage“ liest denselben Geburtstag aus, der auf der Seite angezeigt wird. Ein Geburtstag ist privat: Er wird nie mit deinem Team geteilt, auch nicht bei einem gemeinsam genutzten Eintrag.

## Tabelle importieren

Mit **CSV importieren…** unter dem Sortiermenü für Personen, Unternehmen oder Projekte kannst du eine als CSV gespeicherte Tabelle hinzufügen.

1. Prüfe die Spalten. Deine Machine ermittelt anhand der Überschriften und Inhalte, welche Spalte welche ist. Du kannst die Zuordnung ändern. Wenn dein Modell ausgeführt werden kann, prüft es die Spalten ebenfalls und gibt kurz an, wenn es sich nicht sicher ist. Es sieht nur die Überschriften, einige Werte pro Spalte und die Zellen, die sich anhand der Regeln nicht lesen ließen.
2. Prüfe die Korrekturen. Unter **Prüfen** werden sie vorher und nachher angezeigt: überflüssige Leerzeichen, Namen in Großbuchstaben, Telefonnummern im internationalen Format, Tippfehler in E-Mail-Adressen (gmial.com), Websites nur mit ihrer Domain, Datumsangaben und Werte in beliebigem Format („€12k“ wird zu 12000), mehrere Tags in einer Zelle, eine anders geschriebene Phase und dieselbe Zeile zweimal. Deaktiviere eine Korrekturart oder einzelne Zeilen, wenn sie unverändert bleiben sollen.
3. Prüfe die Vorschau. Für jede Zeile wird angezeigt, ob sie neu ist, einem bereits vorhandenen Eintrag in deinem Graph entspricht oder übersprungen wird, und warum. Eine Person wird anhand der E-Mail-Adresse zugeordnet (andernfalls anhand von Name und Unternehmen), ein Unternehmen anhand der Website oder des Namens und ein Projekt anhand des Namens.
4. Mit **Importieren** fügst du neue Einträge hinzu und ergänzt passende vorhandene Einträge. Leere Zellen ändern nichts.

Mit **Rückgängig** direkt nach dem Import oder mit **Letzten Import rückgängig machen** unter dem Sortiermenü machst du den letzten Import rückgängig, solange die betroffenen Einträge seitdem nicht geändert wurden. Würde dadurch eine spätere Korrektur überschrieben, wird stattdessen der Grund angezeigt. Die Datei bleibt auf deiner Machine.

## Inhaber

In einer Work Fleet hat jede Person, jedes Unternehmen und jedes Projekt einen Inhaber. Du findest **Inhaber** auf der jeweiligen Seite unter „Bei dir“. Standardmäßig bist das du, aber du kannst auch eine Person aus deiner Work Fleet auswählen. Mit **Inhaber** unter **Filtern** werden nur deine Einträge angezeigt. Jede Änderung erscheint im Zeitstrahl.

## Team

Unter **Team** neben „Meine“ siehst du, was deine Teammitglieder teilen, mit denselben Tabs und demselben Sortiermenü. Mit **Filtern** grenzt du die Einträge danach ein, wer sie geteilt hat, zu welchem Unternehmen sie gehören (bei Personen) oder welchen Status sie haben (bei Projekten). Was du dort hinzufügst, gehört dir.

Kundenarbeit wird mit den Machines deiner Teammitglieder geteilt, einschließlich Inhaber, Feldern und Tags. Ihre Kundenarbeit wird auch auf deiner Machine angezeigt. In jedem Thread steht **Team** oder **Nur du**. Weitere Infos findest du unter [Team Graph](team-graph.md).
