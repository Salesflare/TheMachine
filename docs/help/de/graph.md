---
title: Der Graph
area: graph
summary: Die Personen, Organisationen und Projekte in deinen Nachrichten, die sich von selbst aktuell halten.
covers: tab:people
code: graph.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, enrichment.py, dashboard.html
order: 1
---
Deine Machine baut eine Karte davon, mit wem du zu tun hast und was los ist, aus deinen Nachrichten, Meetings und Entscheidungen. Nichts einzurichten, und alles bleibt auf deiner Machine.

## Personen

Alle, mit denen du in Kontakt bist, die engsten zuerst. Die Seite einer Person beginnt mit Foto, Name, Position, Organisation und Ort und einer Zeile dazu, wie ihr in Kontakt seid („Täglicher Austausch · zuletzt Fr, 23. Okt · nächstes Meeting Di, 27. Okt“). Darunter:

- **Kontakt**: Telefonnummern und E-Mail-Adressen. Tippe auf eine, um anzurufen oder zu schreiben, oder **Kopieren**.
- **Mit dir**: was die Person für dich ist, Kontakt aus Arbeit oder Privat, und deine Familie oder Fleet, mit **In Fleet ansehen**.
- **Auch auf**: die anderen Orte, an denen ihr miteinander sprecht. **Slack** öffnet die Person in Slack, oder deinen neuesten Slack-Thread mit ihr.
- **Personen** und **Projekte**, zu denen sie gehört, **Offen zwischen euch** (Versprechen in beide Richtungen, mit **Erledigt** und **Entfernen**) und ihr **Verlauf**.

Adressen und Chats einer Person werden von selbst zusammengeführt, wenn klar ist, dass es eine Person ist, etwa eine Arbeitsadresse mit der privaten Adresse in CC.

Die Tabs **Arbeit** und **Privat** listen nur diese Kontakte. **CSV herunterladen** im Sortiermenü speichert den aktuellen Tab als Tabelle, auch für Organisationen und Projekte.

### Verlauf

Jede Seite einer Person und Organisation hat einen, das Neueste zuerst: E-Mails, Meetings und ihre Zoom-Zusammenfassungen, Intercom-Unterhaltungen (offen oder geschlossen, mit **In Intercom öffnen**), Chats auf WhatsApp, Slack, LinkedIn und X, Aufgaben, Versprechen und Projektbewegungen. Die Chips oben zeigen jeweils eine Quelle. **Mehr anzeigen** lädt ältere Einträge.

Anstehende Meetings stehen getrennt oben unter **Demnächst**, das nächste zuerst. **Alle anstehenden zeigen** zeigt den Rest. Ein Meeting, das in mehreren deiner Kalender steht, erscheint nur einmal.

Der Verlauf einer Organisation enthält die Nachrichten ihrer Personen und die Intercom-Unterhaltungen von ihrer Domain. Deine Verläufe gehören dir: Der Graph des Teams zeigt nur, was deine Freigaberegeln erlauben.

Wenn eine Seite **Die Seite konnte nicht geladen werden.** zeigt, tippe auf **Erneut versuchen**. Bleibt es dabei, nutze **Stimmt etwas nicht?** unten auf der Seite.

## Filtern und sortieren

**Filtern**, neben den Tabs bei Personen, Organisationen und Projekten, grenzt die Liste ein nach Owner, Tag, Board, Phase, Organisation, Wert und erwartetem Abschlussdatum. Personen und Organisationen passen über ihre offenen Projekte.

Die gewählten Filter stehen über der Liste, mit **Entfernen**. Das Sortiermenü sortiert auch nach **Wert** und **Abschlussdatum**. Deine Machine filtert selbst, damit lange Listen schnell bleiben. Auf dem Handy öffnen sich die Filter als Blatt.

## Team

**Team**, neben Meine, zeigt, was deine Teammitglieder teilen. Es hat dieselben Tabs, dasselbe Sortiermenü und **Neue Person** oder **Neue Organisation** wie Meine. Was du hinzufügst, gehört dir. **Filtern** grenzt es ein nach der Person, die es geteilt hat, einer Organisation (Personen) oder einem Status (Projekte).

## Inhaber

In einer Work Fleet hat jede Person, Organisation und jedes Projekt einen Inhaber: **Inhaber** unter Mit dir auf der jeweiligen Seite. Das bist du, außer du wählst jemanden aus deiner Work Fleet. **Meine**, neben Filtern und auf einem Board, zeigt nur deine. Eine Board-Karte zeigt den Namen ihres Inhabers. Jede Änderung erscheint im Verlauf. Ein Eintrag, der mit deinem Team geteilt wird, nimmt seinen Inhaber mit, nach denselben Freigaberegeln wie der Rest.

## Felder und Tags

Klick unter Felder bei einer Person, Organisation oder einem Projekt auf einen Wert, um ihn zu ändern: **Speichern** oder Enter behält ihn, **Abbrechen** oder Escape verwirft die Änderung, **Entfernen** leert ihn. **Felder verwalten** fügt Felder hinzu oder entfernt sie: **Neues Feld** fügt eins für alle Einträge dieser Art hinzu: Text, Zahl, Datum oder eine Auswahl aus einer Liste. **Entfernen** nimmt ein Feld bei allen weg.

**+ Tag** fügt einen Tag hinzu, etwa VIP oder Partner. **×** nimmt ihn wieder ab. Tags erscheinen in den Listen und **Filtern** findet sie. Ein Eintrag, der mit deinem Team geteilt wird, nimmt seine Felder und Tags mit.

## Eine Tabelle importieren

**CSV importieren…** im Sortiermenü von Personen, Organisationen oder Projekten fügt eine als CSV gespeicherte Tabelle hinzu. Deine Machine errät anhand der Überschriften und des Inhalts, welche Spalte was ist. Du kannst jede Zuordnung ändern.

Wenn dein Modell laufen kann, prüft es die Spalten auch, in jeder Sprache und egal wie die Überschriften geschrieben sind, mit einer kurzen Begründung, wo es unsicher ist. Es sieht nur die Überschriften, ein paar Werte pro Spalte und die Zellen, die die Regeln nicht lesen konnten, auf deiner Machine wie bei einer Prüfung. Ohne Modell bleibt es bei der Zuordnung anhand der Überschriften.

**Prüfen**, neben den vorgeschlagenen Korrekturen, listet einfache Korrekturen als Vorher und Nachher: zusätzliche Leerzeichen, Namen in Großbuchstaben, Telefonnummern im internationalen Format, Tippfehler in E-Mail-Adressen (gmial.com), Websites als ihre Domain, Daten und Werte in jedem Format („€12k“ ist 12000), mehrere Tags in einer Zelle, eine Phase, die anders geschrieben ist als im Board, und dieselbe Zeile doppelt.

Entferne das Häkchen bei einer Art oder einer einzelnen Zeile, um sie zu lassen, wie sie ist. Nur was angehakt ist, wird korrigiert.

Die Vorschau zeigt jede Zeile als neu, als Treffer zu einem Eintrag, der schon in deinem Graph ist, oder als übersprungen, mit Grund. Ein Treffer ist dieselbe E-Mail-Adresse bei einer Person (sonst derselbe Name bei derselben Organisation), dieselbe Website oder derselbe Name bei einer Organisation und derselbe Name bei einem Projekt.

**Importieren** fügt die neuen hinzu und ergänzt die Treffer. Eine leere Zelle ändert nichts. **Rückgängig** direkt danach, oder **Letzten Import rückgängig machen** im Sortiermenü, nimmt den letzten Import zurück, solange diese Einträge seitdem nicht geändert wurden. Spätere Korrekturen bleiben erhalten: Würde Rückgängig eine überschreiben, erklärt es stattdessen, warum. Die Datei bleibt auf deiner Machine.

## Eine Organisation, mehrere Websites

**⋯**, **Gleiche Organisation wie…** auf der Seite einer Organisation macht sie zu einem Teil einer anderen, mit ihren Personen, Projekten und Notizen. **Website hinzufügen…** fügt eine weitere ihrer Websites hinzu, etwa ihre .io neben ihrer .com: Personen mit einer Adresse dort gehören dann dazu, und ihre Details werden für jede Website nachgeschlagen.

Sie stehen unter **Websites**, jede mit **Abtrennen**, um es rückgängig zu machen. Spätere Änderungen an der zusammengelegten Organisation bleiben erhalten. Organisationen, die wie Doppelte aussehen, erscheinen unter **Gleiche Organisation?**: **Zusammenführen** oder **Nicht dieselbe**.

## Eine Person oder Organisation hinzufügen

**Neue Person** oben bei Personen, **Neue Organisation** oben bei Organisationen, oder auf dem Handy **+** in der oberen Leiste. Gib einen Namen an, bei einer Person auch E-Mail-Adresse und Organisation, wenn du sie hast, bei einer Organisation ihre Website. Wenn schon ein ähnlicher Eintrag in deinem Graph ist, zeigt das Formular ihn zuerst, damit du stattdessen diesen öffnen kannst. **Hinzufügen** öffnet die neue Seite.

Wen du hinzufügst, der bleibt, auch ohne Nachrichten. Die erste Nachricht wird dann zugeordnet. Eine Organisation, die du hinzugefügt hast, lässt sich über ihr Menü **⋯** löschen, solange niemand darin ist.

## Über dich

Deine eigenen Adressen und Nummern, auch Aliasse, sind immer du, nie jemand in deinem Graph. Wenn du nach dir selbst suchst oder eine Person mit einer deiner Adressen hinzufügst, öffnet sich **Über dich**, und ein Import überspringt deine eigene Zeile.

Über dich listet deine Adressen mit ihrer Herkunft auf. Ändern kannst du sie in **Einstellungen** unter Konto. Eine Person, die früher aus deiner eigenen Adresse entstanden ist, wandert von selbst zu Über dich, mit einem Backup auf deiner Machine.

Um deine eigene Karte an ein Teammitglied oder einen Freund zu schicken, wähle **Meinen Kontakt teilen**. Siehe [Einen Kontakt teilen](share-contact.md).

## Bild

Klick auf das Bild auf der Seite einer Person oder Organisation, um es zu ändern: **Bild hochladen**, eins der gefundenen auswählen oder **Bild entfernen**. Es bleibt auf deiner Machine.

## Notizen

**Bearbeiten** auf der Seite einer Person oder Organisation hat ein Feld **Notizen** für alles, was du dir merken willst. Notizen erscheinen auf der Seite und bleiben beim Zusammenführen erhalten.

## Jemanden bearbeiten

**Bearbeiten** oben auf der Seite ändert Name, Position, Organisation, Ort, Telefonnummern, LinkedIn und E-Mail-Adressen, was die Person für dich ist, und Arbeit oder Privat. **Speichern** behält es, **Abbrechen** lässt es, wie es war.

Deine Änderungen bleiben, auch wenn die Details neu nachgeschlagen werden oder eine Prüfung etwas anderes liest, und auch bei **Zusammenführen** und **Rückgängig**. Leere ein Feld, um wieder den nachgeschlagenen Wert zu nutzen. Ein leerer Name holt den Namen aus den Nachrichten zurück.

## Gleiche Person?

Wenn zwei Personen eine sein könnten, fragt ihre Seite, ob es dieselbe Person ist, und Personen listet sie unter **Gleiche Person?**. **Zusammenführen** verbindet sie, mit allen Nachrichten, Notizen, Rollen und Projekten. **Nicht dieselbe** hält sie dauerhaft getrennt.

**Alle zusammenführen** führt jedes Paar in der Liste auf einmal zusammen, außer denen, die du mit **Nicht dieselbe** markiert hast. **Rückgängig** direkt danach trennt sie alle wieder.

Die Seite einer zusammengeführten Person zeigt unter **Zusammengeführt aus**, warum. **Rückgängig** trennt sie wieder.

Um zwei Personen selbst zusammenzuführen, öffne eine davon, dann **⋯**, **Gleiche Person wie…** und wähle die andere.

## Position und Foto

Personen mit einer Firmenadresse bekommen Position, Foto, LinkedIn und Stadt. Das wird nachgeschlagen wie [Organisationsdetails](organization-data.md). Auf einer gehosteten Machine werden nur ihr Name und die Domain der Firma gesendet. Ausschalten kannst du das in **Einstellungen** unter Sicherheit: **Arbeitskontakte nachschlagen**.

Deine Verbindungen ergänzen mehr, während sie laufen, mit dem, was sie ohnehin lesen, ohne zusätzliche Anfragen: Position, Telefon und Zeitzone aus Slack, Bio, Ort und Website aus X, Headline und Foto aus LinkedIn und Positionen aus Google-Kontakten und Salesflare. Was jemand über sich selbst sagt, hat Vorrang. Fahr mit der Maus über die Zeile unter dem Namen, um zu sehen, woher es kommt. Alles bleibt auf deiner Machine.

WhatsApp-Bilder kommen über deine dauerhaft laufende WhatsApp-Synchronisierung, wenn sie das erlaubt: bis zu 50 am Tag, nur für Personen, die schon in deinem Graph sind. An die Personen wird nichts gesendet.

## Jemanden endgültig löschen

Öffne auf der Seite das Menü ⋯ und wähle **Endgültig löschen…**, dann **Löschen**. Das entfernt die Person und was deine Machine über sie weiß: ihren Eintrag, Adressen, nachgeschlagene Details, die Nachrichten nur zwischen euch beiden und Notizen über sie. Aufgaben, an denen sie beteiligt ist, bleiben, ohne ihren Namen. Sie wird nicht wieder hinzugefügt. Das lässt sich nicht rückgängig machen.

## Wer ist wer

Rollen, die deine Machine in deinen Nachrichten gelesen hat und die auf dein Wort warten. **✓ Stimmt** bestätigt eine. **Bearbeiten** öffnet die Seite der Person im Bearbeitungsmodus. Sie lernt aus deinen Änderungen. Das erscheint nur, wenn Rollen warten.

## In einer Work Fleet

Kundenarbeit wird mit den Machines deiner Teammitglieder geteilt, und ihre erscheint in deiner. Jeder Thread zeigt **Team** oder **Nur du**. Siehe [Team-Graph](team-graph.md).

## Organisationen

Firmen, aus den Adressen und Namen in deinen Nachrichten. Siehe [Organisationsdetails](organization-data.md).

Die Seite einer Organisation ist aufgebaut wie die einer Person: Logo, Name und was sie macht, eine Zeile dazu, wie ihr in Kontakt seid, dann **Kontakt** (Website und LinkedIn), **Mit dir** (was sie für dich ist), die Personen dort und ihr **Verlauf**.

Ihre **Projekte** listen die offenen zuerst, jedes mit seiner Phase. Ihre Bewegungen erscheinen im Verlauf. **Bearbeiten** oben ändert ihre Details und was sie für dich ist. **Die Fleet fragen, wer sie kennt** findet über deine Fleet einen Zugang.

Mails von Tools zum E-Mail-Warm-up bleiben außen vor, unter „Als Warm-up ausgeblendet“, mit **Rückgängig** pro Domain.

## Projekte

Benannt von deiner Machine, danach, worum es in deinen Nachrichten geht. Signale, die dazuzugehören scheinen, erscheinen als „wahrscheinlich Teil davon“. Wenn du ein Projekt in den Namen eines anderen Projekts umbenennst, werden die beiden zusammengeführt.

Oder führe sie von Hand, wie Deals in einem CRM:

- **Neues Projekt**: oben auf einem Board, **+ Hinzufügen** unter einer Phase, **Neues Projekt** oben in der Liste, **+** in der oberen Leiste auf dem Handy oder von der Seite einer Person oder Organisation aus. Gib ihm einen Namen, ein Board und eine Phase, eine Organisation (such in deinem Graph oder **Hinzufügen** einer neuen), einen Wert, ein erwartetes Abschlussdatum, Personen und Notizen. Projekte mit ähnlichem Namen, die schon in deinem Graph sind, erscheinen zuerst.
- **Bearbeiten** auf der Seite eines Projekts, oder **Bearbeiten** im **⋯** einer Karte auf dem Board (oder drück E auf einer Karte). Das ändert alles oben Genannte.
- **Gewonnen** oder **Verloren**, mit Grund. Gewonnen verschiebt es in die letzte Phase des Boards, Verloren nach Stalled or declined. **Wieder öffnen** macht das rückgängig.
- **Archivieren** nimmt es vom Board und aus den Listen. Eine neue Nachricht dazu holt es zurück. **Löschen** entfernt es endgültig. Seine Nachrichten und Personen bleiben.
- Verschieb eine Karte per Ziehen, oder auf dem Handy mit **⋯**, **Verschieben nach**. Deine Verschiebung gilt, bis eine neuere Nachricht sie verschiebt.
- **Phasen**, oben auf einem Board, zeigt nur die Phasen, die du auswählst, pro Board. **Entfernen** zeigt wieder alle.

### Aufgaben eines Projekts

Eine Aufgabe kann zu einem Projekt gehören. Deine Machine wählt es, wenn ihr Thread oder die Personen, um die es geht, zu genau einem offenen Projekt gehören, und die Aufgabe zeigt es als Chip. Tippe auf **▾** auf dem Chip oder auf **Einem Projekt zuordnen** im Befehlsmenü (Ctrl K), um es zu ändern oder zu entfernen. Deine Wahl bleibt.

Die Seite eines Projekts listet seine Aufgaben unter **Aufgaben**, die offenen zuerst, und seine Karte auf dem Board sagt, wie viele offen sind. Eine Aufgabe mit einem geteilten Projekt zu verknüpfen teilt nichts weiter: Dein Team sieht weiterhin nur, was aus geteilten Nachrichten kam.

### Die Organisation eines Projekts

Jedes Projekt kann mit einer Organisation verknüpft sein. Seine Seite, seine Zeile und seine Karte auf dem Board zeigen sie und verlinken dorthin.

Wenn niemand eine gewählt hat, setzt deine Machine sie anhand der Personen im Projekt und seiner Nachrichten, ohne deine Kolleginnen und Kollegen. Das macht sie nur, wenn eindeutig eine Organisation die Gegenseite ist: Private E-Mail wie Gmail zählt nie, und ein Projekt mit mehreren Firmen bleibt ohne. Das Projektformular sagt dann „Aus seinen Personen“.

Deine Wahl in **Bearbeiten** bleibt immer, auch wenn du sie entfernst. **Gleiche Organisation wie…** nimmt die Projekte einer Organisation mit, und **Abtrennen** verschiebt sie zurück.

### Boards

Projekte einer Art in Phasen, etwa eine Pipeline für Evaluierungen. **⋯** auf einem Board: **Board bearbeiten** (Name, Phasen, welche Projekte dazugehören), **Auf diesem Board öffnen** und **Neues Board**. Prüfungen fügen weiter passende Projekte hinzu und setzen sie in eine Phase. Wenn sie unsicher sind, zeigt das Board „2 Projekte könnten hierher gehören“: **Hinzufügen** oder **Auslassen**.

Hake ein paar an, oder **Alle auswählen**, um sie auf einmal zu bearbeiten, und **Rückgängig** direkt danach, wenn du es dir anders überlegst. Ein Projekt, das mehrere Gegenüber bündelt, wird beim Hinzufügen zu einem Projekt pro Gegenüber.

**Pipeline**, oben auf einem Board, rechnet den Wert der offenen Projekte pro Phase zusammen, und was pro Monat laut Abschlussdatum abgeschlossen werden soll. Gewonnene, verlorene und festgefahrene Projekte sind nicht offen. Was du diesen Monat gewonnen hast, steht getrennt. Werte sind in Euro, außer deine Machine ist auf eine andere Währung eingestellt. **Meine** zählt nur deine.

Ein neues Board, oder ein vorgeschlagenes Board, das du speicherst, durchsucht einmal deinen ganzen Verlauf. Es findet passende Projekte und Organisationen, legt ein Projekt pro Organisation an und setzt jedes in eine Phase. Die Kopfzeile sagt „Durchsuche deinen Verlauf…“, solange es arbeitet, und dann, wie viele es hinzugefügt hat und wie viele auf deine Prüfung warten. Ein Board mit Nur du behält, was es findet, für dich.

## Eine Aufgabe zu jemandem

**Neue Aufgabe** im Menü **⋯** einer Person, Organisation oder eines Projekts startet eine Aufgabe dazu.

## Was sie über jemanden weiß

Unter Bekannt über hat jeder Fakt ein Menü:

- **Vergessen** löscht ihn überall.
- Nicht über die Person nimmt ihn nur von dieser Seite.
