---
title: Der Graph
area: graph
summary: Die Personen, Organisationen und Projekte in deinen Nachrichten, die sich von selbst aktuell halten.
covers: tab:people
code: graph.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
---
Deine Machine baut eine Karte davon, mit wem du zu tun hast und was los ist, aus deinen Nachrichten, Meetings und Entscheidungen. Nichts einzurichten, und alles bleibt auf deiner Machine.

- [Personen](people.md): alle, mit denen du in Kontakt bist, jeweils mit Zusammenfassung und Verlauf.
- [Organisationen](organizations.md): die Firmen, in denen sie arbeiten, mit ihren Personen und Projekten.
- [Projekte](projects.md): was los ist, auf Boards mit Phasen, wie Deals in einem CRM.

## Filtern und sortieren

**Filtern**, neben den Tabs, grenzt die Liste ein. Jede Liste hat ihre eigenen Filter. Personen: Nähe, letzter Kontakt, Organisation, Inhaber, Tag und **Hat ein offenes Projekt**. Organisationen: Branche, Größe, Land, letzter Kontakt, Inhaber, Tag und **Hat ein offenes Projekt**. Projekte: Inhaber, Board, Phase, Tag, Organisation, Wert, erwartetes Abschlussdatum und **Keine Antwort seit 10+ Tagen**.

Die gewählten Filter stehen über der Liste, mit **Entfernen**. Bei Projekten teilen sich Liste und Board einen Filter. Auf dem Handy öffnen sie sich als Blatt.

Das Sortiermenü sortiert die Liste. Personen und Organisationen nach Nähe, neuestem oder ältestem Kontakt und Name, Organisationen auch nach Größe. Projekte auch nach **Wert** und **Abschlussdatum**. **CSV herunterladen** im Sortiermenü speichert den aktuellen Tab als Tabelle.

## Felder und Tags

Klick unter Felder bei einer Person, Organisation oder einem Projekt auf einen Wert, um ihn zu ändern: **Speichern** oder Enter behält ihn, **Abbrechen** oder Escape verwirft die Änderung, **Entfernen** leert ihn.

**Felder verwalten** fügt Felder für alle Einträge dieser Art hinzu oder entfernt sie. **Neues Feld** fügt eins hinzu: Text, Zahl, Datum oder eine Auswahl aus einer Liste.

**+ Tag** fügt einen Tag hinzu, etwa VIP oder Partner. **×** nimmt ihn wieder ab. Tags erscheinen in den Listen und **Filtern** findet sie.

## Geburtstag

Der Geburtstag einer Person steht unter Kontakt, mit seiner Herkunft: ihr Google-Kontakt, ein Geburtstag in Google Calendar (die Routine Geburtstage speichert ihn für einen engen Kontakt), ein Facebook-Import oder du. **Bearbeiten** setzt oder korrigiert ihn: Monat und Tag, und das Jahr, wenn du es kennst (dann steht auch das Alter dabei). Deiner gilt vor jeder Quelle und bleibt. **Entfernen** nimmt ihn weg; ein Kontakt oder ein Import bringt ihn nicht zurück.

Ohne Geburtstag fügt **Geburtstag hinzufügen** unter Felder ihn hinzu. Die Routine Geburtstage liest denselben Geburtstag, den die Seite zeigt. Ein Geburtstag ist persönlich: Er geht nie an dein Team, auch nicht bei einem geteilten Eintrag.

## Eine Tabelle importieren

**CSV importieren…** im Sortiermenü von Personen, Organisationen oder Projekten fügt eine als CSV gespeicherte Tabelle hinzu.

1. Prüf die Spalten. Deine Machine errät anhand der Überschriften und des Inhalts, welche was ist; du kannst jede ändern. Wenn dein Modell laufen kann, prüft es sie auch, mit einer kurzen Begründung, wo es unsicher ist. Es sieht nur die Überschriften, ein paar Werte pro Spalte und die Zellen, die die Regeln nicht lesen konnten.
2. Prüf die Korrekturen. **Prüfen** listet sie als Vorher und Nachher: zusätzliche Leerzeichen, Namen in Großbuchstaben, Telefonnummern im internationalen Format, Tippfehler in E-Mail-Adressen (gmial.com), Websites als ihre Domain, Daten und Werte in jedem Format („€12k“ ist 12000), mehrere Tags in einer Zelle, eine anders geschriebene Phase und dieselbe Zeile doppelt. Entferne das Häkchen bei einer Art oder Zeile, um sie zu lassen, wie sie ist.
3. Prüf die Vorschau. Jede Zeile ist neu, ein Treffer zu einem Eintrag in deinem Graph oder übersprungen, mit Grund. Eine Person passt über die E-Mail-Adresse (sonst Name und Organisation), eine Organisation über Website oder Name, ein Projekt über den Namen.
4. **Importieren** fügt die neuen hinzu und ergänzt die Treffer. Eine leere Zelle ändert nichts.

**Rückgängig** direkt danach, oder **Letzten Import rückgängig machen** im Sortiermenü, nimmt den letzten Import zurück, solange diese Einträge seitdem nicht geändert wurden. Würde es eine spätere Korrektur überschreiben, erklärt es stattdessen, warum. Die Datei bleibt auf deiner Machine.

## Inhaber

In einer Work Fleet hat jede Person, Organisation und jedes Projekt einen Inhaber: **Inhaber** unter Mit dir auf der jeweiligen Seite. Das bist du, außer du wählst jemanden aus deiner Work Fleet. **Inhaber** in Filtern zeigt nur deine. Jede Änderung erscheint im Verlauf.

## Team

**Team**, neben Meine, zeigt, was deine Teammitglieder teilen, mit denselben Tabs und demselben Sortiermenü. **Filtern** grenzt es ein nach der Person, die es geteilt hat, einer Organisation (Personen) oder einem Status (Projekte). Was du dort hinzufügst, gehört dir.

Kundenarbeit wird mit den Machines deiner Teammitglieder geteilt, mit Inhaber, Feldern und Tags, und ihre erscheint in deiner. Jeder Thread zeigt **Team** oder **Nur du**. Siehe [Team-Graph](team-graph.md).
