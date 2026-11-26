---
title: Microsoft OneDrive
area: connections
summary: Kommentare, Erwähnungen und nachverfolgte Änderungen in deinen Word-Dateien in OneDrive. Neue Dokumente und Änderungen warten auf dein OK.
covers: connector:docs
code: connectors/docs.py, google_files.py, google_links.py, machine/app/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: 057429e4c3b6408c
---
## Was gelesen wird

**Microsoft OneDrive** liest deine Word-Dateien in OneDrive, auf einer gehosteten Machine und auf deinem eigenen Computer. Outlook muss nicht verbunden sein. Informationen zu Google Docs findest du weiter unten. Die Integration liefert:

- Kommentare und Antworten zu deinen Word-Dateien sowie Kommentare darin, in denen du erwähnt wirst.
- Nachverfolgte Änderungen in deinen Word-Dateien.

Die erste Synchronisierung umfasst die letzten 7 Tage. Jeder Eintrag ist mit den Personen und Projekten in deinem [Graph](graph.md) verknüpft. Ein Kommentar, der deine Aufmerksamkeit braucht, wird zu einer Aufgabe.

## Dateien, die andere mit dir teilen

Microsoft zeigt diese Dateien ab November 2026 nicht mehr an. Geteilte Dateien und Erwähnungen in Dateien anderer Personen erreichen deine Machine dann nur noch als E-Mails von Microsoft. Verbinde auch [Outlook](microsoft.md) und lass diese E-Mails aktiviert. Eine Aufgabe daraus öffnet die E-Mail, und die Schaltfläche darin öffnet die Datei. Geteilte Dateien oder Erwähnungen ohne E-Mail werden nicht erkannt.

## Was die Integration kann

Wenn eine Aufgabe den Text eines Dokuments benötigt, liest deine Machine dieses Dokument nur, während sie an der Aufgabe arbeitet. Sie kann Word-, PDF- und Textdateien lesen.

Außerdem sucht sie nach Dateien aller Art in deinem eigenen OneDrive und gibt dir den Link dazu. Sie durchsucht keine SharePoint-Websites und keine Dateien, die mit dir geteilt wurden. Den Text eines eingescannten PDFs kann sie nicht lesen.

Sie kann einen Antwortentwurf für einen Kommentar erstellen. Word kann Antworten nicht von außerhalb posten. Deshalb kopierst du den Entwurf in Word.

Ohne dein OK nimmt sie keine Vorschläge an, löst keine Kommentare auf, teilt keine Dateien und ändert keine Dokumente.

Wenn du die Integration nur zum Erledigen von Aufgaben nutzen möchtest, deaktiviere unter „**Details**“ die Option „**Liefert Signale**“. Dann findet und liest sie nur die Dateien, die für deine Aufgaben benötigt werden, und erstellt neue Dateien.

## Dokumente erstellen und bearbeiten

Deine Machine kann ein neues Dokument erstellen oder ein Dokument ändern, um das es in einer Aufgabe geht:

- Ein neues Dokument erstellt sie sofort, wenn die Aufgabe oder ein Skill danach fragt. Es ist privat und wird in deinem eigenen OneDrive oder Google Drive gespeichert. In der Aufgabe erscheint „**Dokument öffnen**“. Das Dokument zu teilen oder seinen Link zu versenden, wartet auf dein OK.
- Eine Änderung an einem bestehenden Dokument bereitet sie nur vor. Wähle „**Änderungen prüfen**“, um jeden Absatz vorher und nachher zu sehen, und dann „**Speichern**“. Eine Änderung, die du im Chat der Aufgabe anforderst, führt sie sofort aus.
- Sie schreibt nur in das Dokument, so wie du es gesehen hast. Wenn jemand es in der Zwischenzeit geändert hat, wird nichts geschrieben und die Aufgabe weist dich darauf hin. Bitte um einen neuen Entwurf.
- In Talk liest sie die gesamte Änderung laut vor und wartet auf ein klares Ja.
- Wenn Microsoft oder Google das Erstellen eines neuen Dokuments ablehnt, erklärt die Aufgabe warum und zeigt „**Prüfen und erstellen**“ an, damit du es erneut versuchen kannst.

Sie kann Text ersetzen und Text, Absätze und Überschriften hinzufügen. In Google Docs kann sie außerdem Text formatieren: fett, kursiv, unterstrichen, mit Links, Überschriften, Aufzählungen und nummerierten Listen sowie einem Seitenumbruch. „**Änderungen prüfen**“ zeigt jede einzelne Änderung. Tabellen kann sie nicht erstellen. Bilder, nachverfolgte Änderungen und Felder bleiben unverändert.

Das Dokument einer geschäftlichen Aufgabe wird im Konto des jeweiligen Unternehmens gespeichert, niemals in einem privaten Konto. Auf deinem eigenen Computer kann auch ein Google-Konto neue Google Docs erstellen, wenn es für Gmail verbunden ist und Zugriff auf Drive hat. Wenn kein passendes Konto vorhanden ist, sagt dir die Aufgabe, was du für geschäftliche Aufgaben verbinden musst: Microsoft OneDrive oder Google Docs, sofern deine Machine es nutzen kann.

Wenn das Dokument nicht der letzte Schritt ist, zum Beispiel bei einer Antwort mit seinem Link, bleibt die Aufgabe offen und erstellt einen Entwurf für diesen Schritt, der auf dein OK wartet.

Die Bearbeitungsfunktion wird beim Verbinden aktiviert. Bei einer älteren Verbindung, die nur lesen kann, erscheint unter „**Verbindungen**“ die Option „**Bearbeiten erlauben**“. Wähle sie einmal aus und bestätige.

## Welche Berechtigungen abgefragt werden

Microsoft bittet dich um eine einmalige Zustimmung, deine Dateien zu lesen und zu ändern, auch Dateien, die mit dir geteilt wurden. Jede Änderung wartet weiterhin in der jeweiligen Aufgabe auf dein OK. Dein Zugriff auf E-Mails und Kalender ändert sich nicht.

Wenn du diese Zustimmung später widerrufst, zeigt Microsoft OneDrive unter „**Verbindungen**“ den Hinweis „**Wartet auf dein OK, um Dokumente zu lesen**“ an.

## Verbindung herstellen

Auf einer gehosteten Machine oder auf deinem eigenen Computer, wenn sie mit deinem Konto gekoppelt ist:

- Öffne „**Verbindungen**“, dann „**Dokumente und Dateien**“, und wähle „**Microsoft OneDrive**“.
- Wähle „**Mit Microsoft anmelden**“ und erlaube den Zugriff zum Lesen und Bearbeiten deiner Dateien.

Wenn Microsoft das Lesen nicht erlaubt, wird die Integration nicht hinzugefügt. Wenn du „**Bearbeiten erlauben**“ auswählst und Microsoft die Bearbeitung nicht erlaubt, wird dir das mitgeteilt.

## Google Docs

Öffne auf einer gehosteten Machine „**Verbindungen**“, dann „**Dokumente und Dateien**“, und wähle „**Google Docs**“. Google bittet dich, den Zugriff auf die Dokumente zu erlauben, auf die du verweist, sowie deren Bearbeitung und das Erstellen neuer Dokumente. Gmail muss nicht verbunden sein, und dein Gmail-Zugriff ändert sich nicht.

Danach kann deine Machine:

- Ein Google-Dokument lesen, das in Nachrichten einer Aufgabe verlinkt oder in den Chat der Aufgabe eingefügt wurde, aber nur, während sie an dieser Aufgabe arbeitet.
- Änderungen an diesem Dokument vorbereiten. Jede Änderung wartet wie oben beschrieben auf dein OK.
- Neue private Dokumente in deinem Google Drive erstellen.

Sie durchsucht dein Drive nicht. Kommentare, geteilte Dokumente und Vorschläge sieht sie nur in Dokumenten, die sie erstellt hat. Für mehr Zugriff müsste sie auf dein gesamtes Drive zugreifen können. Diesen Zugriff fragt sie nicht an.

## Google Sheets und Slides

Wenn unter „**Verbindungen**“ bei Google Docs die Option „**Zugriff auf Sheets und Slides erlauben**“ angezeigt wird, wähle sie aus und erlaube beides. Google bittet dich, deiner Machine Zugriff auf deine Sheets- und Slides-Dateien zu erlauben. Ändern kann sie diese Dateien nicht.

Danach liest deine Machine auch Google-Sheets- oder Slides-Dateien, die in Nachrichten einer Aufgabe verlinkt oder in den Chat der Aufgabe eingefügt wurden, aber nur, während sie an dieser Aufgabe arbeitet:

- Bei einem Sheet zuerst das verknüpfte Tabellenblatt oder die verknüpften Zellen, danach die anderen Tabellenblätter, bis zu 2.000 Zellen. Eine Formel wird als ihr Wert angezeigt. Ausgeblendete Tabellenblätter werden nur gelesen, wenn auf sie verwiesen oder danach gefragt wird.
- Bei Slides den Text und die Sprechernotizen, der Reihe nach. Bilder und Diagramme werden nicht gelesen.

### Sheets und Slides bearbeiten

Sobald deine Machine diese Dateien lesen kann, zeigt Google Docs möglicherweise auch „**Bearbeiten von Sheets und Slides erlauben**“ an. Wähle die Option aus und erlaube beides. Dann kann deine Machine ein verknüpftes Sheet oder eine Slides-Datei genauso ändern wie ein Dokument: Sie bereitet die Änderung nur vor, „**Änderungen prüfen**“ zeigt sie an, und geschrieben wird erst, wenn du „**Speichern**“ auswählst.

- In einem Sheet: neue Zellwerte in einem Tabellenblatt, Zeilen unter der letzten Zeile oder ein neues Tabellenblatt. Für jede Zelle wird vorher und nachher angezeigt. Werte werden als Text eingetragen. Eine Formel wird nur dann als Formel eingetragen, wenn die Aufgabe das verlangt.
- In Slides: Text auf einer Folie wird ersetzt und vorher und nachher angezeigt, oder es wird eine neue Folie mit Titel und Text erstellt.
- Sie schreibt nur in die Datei, so wie du sie gesehen hast. Wenn jemand die betreffenden Zellen oder Folien in der Zwischenzeit geändert hat, wird nichts geschrieben und die Aufgabe weist dich darauf hin.

Formatierungen, Diagramme, Bilder sowie Excel- und PowerPoint-Dateien bleiben unverändert.

Bei großen Dateien gib im Chat an, welches Tabellenblatt, welche Zellen oder welche Folien du meinst. Wenn eine Datei nur für eine andere Person freigegeben wurde, gelöscht wurde oder eine Excel- oder PowerPoint-Datei ist, weist dich die Aufgabe darauf hin. Ein Google-Drive-Link funktioniert genauso, wenn er zu einer Google-Docs-, Sheets- oder Slides-Datei führt.

## Google Docs auf deinem eigenen Computer

Auf deinem eigenen Computer kann deine Machine ein neues Google-Dokument in einem Gmail-Konto erstellen, das dort angemeldet ist und bereits Zugriff auf Drive hat. Sie liest keine deiner anderen Google-Dokumente oder deren Kommentare. Unter „**Dokumente und Dateien**“ erscheint Google Docs für dieses Konto. Sie kann dort auch ein Dokument ändern, das sie für eine Aufgabe erstellt hat.

Sie liest auch eine Google-Sheets- oder Slides-Datei, die in einer Aufgabe verlinkt oder in den Chat der Aufgabe eingefügt wurde, wenn das angemeldete Google-Konto bereits Zugriff auf Drive, Sheets oder Slides hat. Sie fragt Google niemals nach weiteren Berechtigungen und ändert diese Dateien dort nicht. Wenn Google den Zugriff ablehnt, aktiviere die Google-Sheets- oder Slides-API im eigenen Google-Projekt dieses Kontos.

## Geschäftlich oder privat

Wie bei E-Mails richtet sich die Integration nach der Kennzeichnung „Geschäftlich“ oder „Privat“ ihrer Verbindung. Geschäftliche Dokumente können gemäß deinen [Freigaberegeln](sharing-rules.md) den Graph deines Teams erreichen. Private Dokumente gelangen niemals dorthin.

## Verbindung entfernen

Öffne „**Verbindungen**“, dann Microsoft OneDrive oder Google Docs, „**Details**“ und „**Trennen**“. Die Integration hört dann auf zu lesen. Was sie bereits übernommen hat, bleibt erhalten. Auf einer gehosteten Machine öffnet „**Trennen ↗**“ deine Einrichtungsseite mit der Anmeldung.
