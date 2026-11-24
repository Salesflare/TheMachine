---
title: Microsoft OneDrive
area: connections
summary: Kommentare, Erwähnungen und nachverfolgte Änderungen in deinen Word-Dateien in OneDrive. Neue Dokumente und Änderungen warten auf dein OK.
covers: connector:docs
code: connectors/docs.py, google_files.py, google_links.py, machine/app/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: d79388a1c8811d5f
---
## Was sie liest

**Microsoft OneDrive** liest deine Word-Dateien in OneDrive, auf einer gehosteten Machine und auf deinem eigenen Computer. Outlook muss nicht verbunden sein. Informationen zu Google Docs findest du weiter unten. Sie liefert:

- Kommentare und Antworten zu deinen Word-Dateien sowie Kommentare, in denen du erwähnt wirst.
- Nachverfolgte Änderungen in deinen Word-Dateien.

Beim ersten Abgleich werden die letzten 7 Tage berücksichtigt. Jeder Eintrag ist mit den Personen und Projekten in deinem [Graph](graph.md) verknüpft. Ein Kommentar, der deine Aufmerksamkeit braucht, wird zu einer Aufgabe.

## Dateien, die andere mit dir teilen

Microsoft zeigt diese ab November 2026 nicht mehr an. Geteilte Dateien und Erwähnungen in den Dateien anderer erreichen deine Machine dann nur noch über E-Mails von Microsoft. Verbinde auch [Outlook](microsoft.md) und lass diese E-Mails aktiviert. Eine Aufgabe aus einer solchen E-Mail öffnet die E-Mail, und die Schaltfläche darin öffnet die Datei. Geteilte Dateien oder Erwähnungen ohne E-Mail werden nicht erkannt.

## Was sie kann

Wenn eine Aufgabe den Text eines Dokuments benötigt, liest deine Machine dieses Dokument, aber nur, während sie an der Aufgabe arbeitet. Sie kann Word-, PDF- und Textdateien lesen.

Sie sucht außerdem in deiner eigenen OneDrive nach Dateien aller Art und gibt dir den Link dazu. Sie durchsucht keine SharePoint-Websites und keine Dateien, die mit dir geteilt wurden. Den Text eines eingescannten PDFs kann sie nicht lesen.

Sie kann einen Antwortentwurf zu einem Kommentar erstellen. Word bietet keine Möglichkeit, Antworten von außerhalb zu veröffentlichen. Deshalb kopierst du den Entwurf in Word.

Sie nimmt niemals einen Vorschlag an, löst keinen Kommentar auf, teilt keine Datei und ändert kein Dokument ohne dein OK.

Wenn du sie nur zum Erledigen von Aufgaben nutzen möchtest, deaktiviere **Liefert Signale** unter **Details**. Dann sucht und liest sie nur die Dateien, die für deine Aufgaben benötigt werden, und erstellt neue Dateien.

## Dokumente erstellen und bearbeiten

Deine Machine kann ein neues Dokument schreiben oder ein Dokument ändern, um das es in einer Aufgabe geht:

- Ein neues Dokument erstellt sie sofort, wenn die Aufgabe oder ein Skill danach fragt. Es ist privat und wird in deiner eigenen OneDrive oder Google Drive gespeichert. In der Aufgabe wird **Dokument öffnen** angezeigt. Das Dokument zu teilen oder den Link zu senden, wartet auf dein OK.
- Eine Änderung an einem vorhandenen Dokument bereitet sie nur vor. Drücke **Änderungen prüfen**, um jeden Absatz vorher und nachher zu sehen, und dann **Speichern**. Eine Änderung, die du im Chat der Aufgabe anforderst, setzt sie sofort um.
- Sie schreibt nur in das Dokument, das du gesehen hast. Wenn jemand es inzwischen geändert hat, wird nichts geschrieben und die Aufgabe weist dich darauf hin. Bitte um einen neuen Entwurf.
- In Talk liest sie die gesamte Änderung vor und wartet auf ein klares Ja.
- Wenn Microsoft oder Google das Erstellen eines neuen Dokuments ablehnt, erklärt die Aufgabe warum und zeigt **Prüfen und erstellen** an, damit du es erneut versuchen kannst.

Sie kann Text ersetzen und Text, Absätze und Überschriften hinzufügen. Tabellen, Bilder, nachverfolgte Änderungen und Felder bleiben unverändert.

Das Dokument einer Work-Aufgabe wird im Konto des Unternehmens gespeichert, niemals in einem persönlichen Konto. Auf deinem eigenen Computer kann ein Google-Konto, das für Gmail verbunden ist und Zugriff auf Drive hat, auch neue Google Docs erstellen. Wenn kein Konto passt, steht in der Aufgabe, was du für Work verbinden musst: Microsoft OneDrive oder Google Docs, sofern deine Machine es verwenden kann.

Wenn das Dokument nicht der letzte Schritt ist, zum Beispiel bei einer Antwort mit dem Dokumentlink, bleibt die Aufgabe offen und erstellt einen Entwurf für diesen Schritt, der auf dein OK wartet.

Die Bearbeitung ist verfügbar, sobald du die Verbindung herstellst. Bei einer älteren Verbindung, die nur Lesen erlaubt, wird unter **Verbindungen** die Option **Bearbeiten erlauben** angezeigt. Drücke sie einmal und bestätige.

## Welche Berechtigungen sie braucht

Microsoft bittet dich um ein einziges OK, um deine Dateien zu lesen und zu ändern, einschließlich der Dateien, die mit dir geteilt wurden. Jede Änderung wartet weiterhin in der jeweiligen Aufgabe auf dein OK. Der Zugriff auf deine E-Mails und deinen Kalender ändert sich nicht.

Wenn du diese Zustimmung später widerrufst, zeigt Microsoft OneDrive unter **Verbindungen** den Hinweis **Wartet auf dein OK, um Dokumente zu lesen** an.

## Verbindung herstellen

Auf einer gehosteten Machine oder auf deinem eigenen Computer, wenn er mit deinem Konto gekoppelt ist:

- Öffne **Verbindungen**, dann **Dokumente und Dateien**, und wähle **Microsoft OneDrive** aus.
- Drücke **Mit Microsoft anmelden** und erlaube das Lesen und Bearbeiten deiner Dateien.

Wenn Microsoft das Lesen nicht erlaubt, wird die Verbindung nicht hinzugefügt. Wenn du **Bearbeiten erlauben** drückst und Microsoft die Bearbeitung nicht erlaubt, weist Microsoft dich darauf hin.

## Google Docs

Öffne auf einer gehosteten Machine **Verbindungen**, dann **Dokumente und Dateien**, und wähle **Google Docs** aus. Google bittet dich, den Zugriff auf die von dir angegebenen Dokumente zu erlauben, damit sie angesehen und bearbeitet sowie neue erstellt werden können. Gmail muss nicht verbunden sein, und dein Gmail-Zugriff ändert sich nicht.

Danach kann deine Machine:

- Ein Google Doc lesen, das in den Nachrichten einer Aufgabe verlinkt oder in ihren Chat eingefügt wurde, aber nur, während sie an dieser Aufgabe arbeitet.
- Änderungen an diesem Dokument vorbereiten. Jede Änderung wartet wie oben beschrieben auf dein OK.
- Neue private Dokumente in deiner Google Drive erstellen.

Sie durchsucht deine Drive nicht. Kommentare, geteilte Dateien und Vorschläge sieht sie nur in Dokumenten, die sie selbst erstellt hat. Für mehr Zugriff müsste sie auf deine gesamte Drive zugreifen können. Darum bittet sie dich nicht.

## Google Sheets und Slides

Wenn unter **Verbindungen** bei Google Docs **Zugriff auf Sheets und Slides erlauben** angezeigt wird, drücke darauf und erlaube den Zugriff auf beides. Google bittet dich, deiner Machine den Zugriff auf deine Sheets- und Slides-Dateien zu erlauben. Ändern kann sie diese nicht.

Danach liest deine Machine auch Google Sheets- oder Slides-Dateien, die in den Nachrichten einer Aufgabe verlinkt oder in ihren Chat eingefügt wurden, aber nur, während sie an dieser Aufgabe arbeitet:

- Bei Sheets liest sie zuerst den verlinkten Tab oder die verlinkten Zellen und dann die übrigen Tabs, bis zu 2.000 Zellen. Eine Formel wird als ihr Wert angezeigt. Ausgeblendete Tabs liest sie nur, wenn sie verlinkt oder ausdrücklich angefordert wurden.
- Bei Slides liest sie den Text und die Sprechernotizen der Reihe nach. Bilder und Diagramme werden nicht gelesen.

Bei großen Dateien gib im Chat an, welchen Tab, welche Zellen oder welche Folien du meinst. Wenn eine Datei für jemand anderen privat ist, gelöscht wurde oder eine Excel- oder PowerPoint-Datei ist, weist die Aufgabe dich darauf hin. Ein Google-Drive-Link funktioniert genauso, wenn er zu einer Google-Docs-, Sheets- oder Slides-Datei führt.

## Google Docs auf deinem eigenen Computer

Auf deinem eigenen Computer kann deine Machine ein neues Google Doc in einem Gmail-Konto erstellen, bei dem du dort angemeldet bist und das bereits Zugriff auf Drive hat. Sie liest deine anderen Google Docs und deren Kommentare nicht. Unter **Dokumente und Dateien** wird das Konto als Google Docs angezeigt. Sie kann dort auch ein Dokument ändern, das sie für eine Aufgabe erstellt hat.

Sie liest außerdem Google-Sheets- oder Slides-Dateien, die in einer Aufgabe verlinkt oder in ihren Chat eingefügt wurden, wenn die Google-Anmeldung bereits Zugriff auf Drive, Sheets oder Slides hat. Sie bittet Google niemals um weitere Berechtigungen. Wenn Google den Zugriff verweigert, aktiviere die Google Sheets API oder Slides API im eigenen Google-Projekt dieser Anmeldung.

## Arbeit oder privat

Wie bei E-Mails richtet sie sich nach der Kennzeichnung Work oder Personal der jeweiligen Verbindung. Work-Dokumente können gemäß deinen [Freigaberegeln](sharing-rules.md) den Graph deines Teams erreichen. Persönliche Dokumente erreichen ihn nie.

## Verbindung entfernen

Öffne **Verbindungen**, dann Microsoft OneDrive oder Google Docs, **Details** und **Trennen**. Danach liest sie keine Dateien mehr. Was sie bereits übernommen hat, bleibt erhalten. Auf einer gehosteten Machine öffnet **Trennen ↗** deine Einrichtungsseite, auf der die Anmeldung gespeichert ist.
