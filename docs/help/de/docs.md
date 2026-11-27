---
title: Microsoft OneDrive
area: connections
summary: Kommentare, Erwähnungen und nachverfolgte Änderungen in deinen Word-Dateien in OneDrive. Neue Dokumente und Änderungen warten auf dein OK.
covers: connector:docs
code: connectors/docs.py, google_files.py, google_links.py, machine/app/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: e931920c74158c98
---
## Was sie liest

**Microsoft OneDrive** liest deine Word-Dateien in OneDrive, auf einer gehosteten Machine und auf deinem eigenen Computer. Outlook muss nicht verbunden sein. Informationen zu Google Docs findest du weiter unten. Sie liefert:

- Kommentare und Antworten in deinen Word-Dateien sowie Kommentare, in denen du erwähnt wirst.
- Nachverfolgte Änderungen in deinen Word-Dateien.

Die erste Synchronisierung reicht 7 Tage zurück. Jedes Element verknüpft Personen und Projekte in deinem [Graph](graph.md). Ein Kommentar, der deine Aufmerksamkeit erfordert, wird zu einer Aufgabe.

## Dateien, die andere mit dir teilen

Microsoft listet diese ab November 2026 nicht mehr auf. Geteilte Dateien und Erwähnungen in Dateien anderer erreichen deine Machine dann nur noch als E-Mails von Microsoft. Verbinde auch [Outlook](microsoft.md) und lass diese E-Mails aktiviert. Eine Aufgabe aus einer solchen E-Mail öffnet die E-Mail, und über die Schaltfläche darin öffnest du die Datei. Geteilte Dateien und Erwähnungen ohne E-Mail werden nicht erkannt.

## Was sie kann

Wenn eine Aufgabe den Text eines Dokuments benötigt, liest deine Machine dieses Dokument, nur während sie an der Aufgabe arbeitet. Sie kann Word-, PDF- und Textdateien lesen.

Sie sucht auch nach Dateien aller Art in deinem eigenen OneDrive und gibt dir den Link dazu. SharePoint-Websites und Dateien, die mit dir geteilt wurden, durchsucht sie nicht. Den Text eines gescannten PDFs kann sie nicht lesen.

Sie kann eine Antwort auf einen Kommentar entwerfen. Word bietet keine Möglichkeit, Antworten von außerhalb zu posten. Deshalb kopierst du den Entwurf in Word.

Sie nimmt niemals ohne dein OK einen Vorschlag an, löst einen Kommentar auf, teilt eine Datei oder ändert ein Dokument.

Wenn du sie nur zum Erledigen von Aufgaben verwenden möchtest, deaktiviere **Liefert Signale** unter **Details**. Dann findet und liest sie nur die Dateien, die deine Aufgaben benötigen, und erstellt neue Dateien.

## Dokumente erstellen und bearbeiten

Deine Machine kann ein neues Dokument erstellen oder ein Dokument ändern, um das es in einer Aufgabe geht:

- Ein neues Dokument erstellt sie sofort, wenn die Aufgabe oder ein Skill danach fragt. Es ist privat und wird in deinem eigenen OneDrive oder Google Drive gespeichert. In der Aufgabe wird **Dokument öffnen** angezeigt. Das Dokument zu teilen oder den Link dazu zu senden, wartet auf dein OK.
- Eine Änderung an einem vorhandenen Dokument bereitet sie nur vor. Wähle **Änderungen prüfen**, um jeden Absatz vorher und nachher zu sehen, und dann **Speichern**. Eine Änderung, um die du im Chat der Aufgabe bittest, führt sie sofort aus.
- Sie schreibt nur in die Version des Dokuments, die du gesehen hast. Wenn jemand das Dokument inzwischen geändert hat, wird nichts geschrieben und die Aufgabe weist dich darauf hin. Bitte um einen neuen Entwurf.
- In Talk liest sie die gesamte Änderung laut vor und wartet auf ein eindeutiges Ja.
- Wenn Microsoft oder Google ein neues Dokument ablehnt, erklärt die Aufgabe warum und zeigt **Prüfen und erstellen** an, damit du es erneut versuchen kannst.

Sie kann Text ersetzen und Text, Absätze und Überschriften hinzufügen. In Google Docs kann sie außerdem formatieren: fett, kursiv, unterstrichen, Links, Überschriften, Aufzählungen und nummerierte Listen sowie einen Seitenumbruch. **Änderungen prüfen** zeigt jede Änderung an. Tabellen kann sie nicht erstellen. Bilder, nachverfolgte Änderungen und Felder bleiben unverändert.

Das Dokument einer Aufgabe aus Work wird im Konto des Unternehmens gespeichert, niemals in einem persönlichen Konto. Auf deinem eigenen Computer kann auch ein Google-Konto, das für Gmail verbunden ist und Zugriff auf Drive hat, neue Google Docs erstellen. Wenn kein Konto passt, steht in der Aufgabe, was du für Work verbinden musst: Microsoft OneDrive oder Google Docs, sofern deine Machine es verwenden kann.

Wenn das Dokument nicht der letzte Schritt ist, zum Beispiel bei einer Antwort mit dem Link dazu, bleibt die Aufgabe offen und sie entwirft diesen Schritt zur Freigabe.

Die Bearbeitungsfunktion ist verfügbar, sobald du eine Verbindung herstellst. Bei einer älteren Verbindung, die nur Lesezugriff hat, wird unter **Verbindungen** die Option **Bearbeiten erlauben** angezeigt. Wähle sie einmal aus und bestätige.

## Worum sie dich bittet

Microsoft bittet dich um ein OK, damit sie deine Dateien lesen und ändern kann, auch Dateien, die mit dir geteilt wurden. Jede Änderung wartet weiterhin auf dein OK in der jeweiligen Aufgabe. Der Zugriff auf deine E-Mails und deinen Kalender ändert sich nicht.

Wenn du dieses OK später widerrufst, zeigt Microsoft OneDrive unter **Verbindungen** die Meldung **Wartet auf dein OK, um Dokumente zu lesen** an.

## Verbindung herstellen

Auf einer gehosteten Machine oder auf deinem eigenen Computer, wenn er mit deinem Konto gekoppelt ist:

- Öffne **Verbindungen**, dann **Dokumente und Dateien** und wähle **Microsoft OneDrive** aus.
- Wähle **Mit Microsoft anmelden** und erlaube das Lesen und Bearbeiten deiner Dateien.

Wenn Microsoft das Lesen nicht erlaubt, wird die Verbindung nicht hinzugefügt. Wenn du **Bearbeiten erlauben** auswählst und Microsoft das Bearbeiten nicht erlaubt, weist Microsoft dich darauf hin.

## Google Docs

Öffne auf einer gehosteten Machine **Verbindungen**, dann **Dokumente und Dateien**, und wähle **Google Docs** aus. Google bittet dich, deiner Machine zu erlauben, die Dokumente zu sehen, auf die du verweist, sie zu bearbeiten und neue Dokumente zu erstellen. Gmail muss nicht verbunden sein, und dein Gmail-Zugriff ändert sich nicht.

Danach kann deine Machine:

- Ein Google-Dokument lesen, das in den Nachrichten einer Aufgabe verlinkt oder in ihren Chat eingefügt wurde, aber nur während sie an der Aufgabe arbeitet.
- Änderungen an diesem Dokument vorbereiten. Jede Änderung wartet wie oben beschrieben auf dein OK.
- Neue private Dokumente in deinem Google Drive erstellen.

Wenn im Bereich einer Aufgabe mehrere Google-Docs-Verbindungen vorhanden sind, liest und ändert sie eine Datei über eine Verbindung, mit der sie die Datei öffnen und möglicherweise ändern kann.

Sie durchsucht dein Drive nicht. Kommentare, geteilte Dateien und Vorschläge sieht sie nur in Dokumenten, die sie selbst erstellt hat. Für mehr Zugriff müsste sie dein gesamtes Drive nutzen. Darum bittet sie dich nicht.

## Google Sheets und Slides

Wenn unter **Verbindungen** bei Google Docs **Zugriff auf Sheets und Slides erlauben** angezeigt wird, wähle die Option aus und erlaube beides. Google bittet dich, deiner Machine zu erlauben, deine Sheets- und Slides-Dateien zu sehen. Ändern kann sie sie nicht.

Danach liest deine Machine auch ein Google-Sheet oder eine Slides-Datei, die in den Nachrichten einer Aufgabe verlinkt oder in ihren Chat eingefügt wurde, aber nur während sie an der Aufgabe arbeitet:

- In einem Sheet zuerst den verlinkten Tab oder die verlinkten Zellen, dann die anderen Tabs, bis zu 2.000 Zellen. Eine Formel wird als ihr Wert angezeigt. Ausgeblendete Tabs liest sie nur, wenn auf sie verwiesen oder danach gefragt wird.
- In Slides den Text und die Sprechernotizen der Reihe nach. Bilder und Diagramme liest sie nicht.

### Sheets und Slides bearbeiten

Sobald deine Machine sie lesen kann, wird bei Google Docs möglicherweise auch **Bearbeiten von Sheets und Slides erlauben** angezeigt. Wähle die Option aus und erlaube beides. Dann kann deine Machine ein Sheet oder eine Slides-Datei ändern, die in einer Aufgabe verlinkt oder in ihren Chat eingefügt wurde. Das funktioniert wie bei einem Dokument: Sie bereitet die Änderung nur vor, **Änderungen prüfen** zeigt sie an, und nichts wird geschrieben, bevor du **Speichern** auswählst.

- In einem Sheet: neue Zellwerte in einem Tab, Zeilen unter der letzten Zeile oder ein neuer Tab. Für jede Zelle werden vorher und nachher angezeigt. Werte werden als Text eingefügt. Eine Formel wird nur dann als Formel eingefügt, wenn die Aufgabe das vorgibt.
- In Slides: Text auf einer Folie ersetzen, mit vorher und nachher, oder eine neue Folie mit Titel und Text erstellen.
- Sie schreibt nur in die Version der Datei, die du gesehen hast. Wenn jemand die betreffenden Zellen oder Folien inzwischen geändert hat, wird nichts geschrieben und die Aufgabe weist dich darauf hin.

Formatierungen, Diagramme, Bilder sowie Excel- und PowerPoint-Dateien bleiben unverändert.

Bei einer großen Datei gib im Chat an, welchen Tab, welche Zellen oder welche Folien du meinst. Wenn eine Datei nur für jemand anderen zugänglich ist, gelöscht wurde oder eine Excel- oder PowerPoint-Datei ist, weist die Aufgabe dich darauf hin. Ein Google-Drive-Link funktioniert genauso, wenn er auf ein Google-Dokument, Sheet oder eine Slides-Datei verweist.

## Google Docs auf deinem eigenen Computer

Auf deinem eigenen Computer kann deine Machine ein neues Google-Dokument in einem dort angemeldeten Gmail-Konto erstellen, das bereits Zugriff auf Drive hat. Andere Google-Dokumente oder deren Kommentare liest sie nicht. Unter **Dokumente und Dateien** wird dieses Konto als Google Docs angezeigt. Außerdem kann sie dort ein Dokument ändern, das sie für eine Aufgabe erstellt hat.

Sie liest auch ein Google-Sheet oder eine Slides-Datei, die in einer Aufgabe verlinkt oder in ihren Chat eingefügt wurde, wenn das angemeldete Google-Konto bereits Zugriff auf Drive, Sheets oder Slides hat. Sie bittet Google niemals um weiteren Zugriff und ändert diese Dateien dort nicht. Wenn Google den Zugriff verweigert, aktiviere die Google Sheets- oder Slides-API im eigenen Google-Projekt dieses Kontos.

## Geschäftlich oder privat

Sie richtet sich wie bei E-Mails nach der Kennzeichnung „Geschäftlich“ oder „Privat“ ihrer Verbindung. Geschäftliche Dokumente können gemäß deinen [Freigaberegeln](sharing-rules.md) den Graph deines Teams erreichen. Private Dokumente tun das nie.

## Verbindung entfernen

Öffne **Verbindungen**, dann Microsoft OneDrive oder Google Docs, **Details** und **Trennen**. Die Verbindung liest dann keine Dateien mehr. Was sie bereits eingelesen hat, bleibt erhalten. Auf einer gehosteten Machine öffnet **Trennen ↗** deine Einrichtungsseite, auf der die Anmeldung gespeichert ist.
