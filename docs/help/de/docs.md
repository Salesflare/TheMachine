---
title: Microsoft OneDrive
area: connections
summary: Kommentare, Erwähnungen, nachverfolgte Änderungen und Freigaben deiner Word-Dateien in OneDrive und SharePoint. Neue Dokumente und Änderungen warten auf dein OK.
covers: connector:docs
code: connectors/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: b06d8ca4f35e5a38
---
## Was sie liest

**Microsoft OneDrive** liest deine Word-Dateien in OneDrive und SharePoint, sowohl auf einer gehosteten Machine als auch auf deinem eigenen Computer. Outlook muss dafür nicht verbunden sein. Informationen zu Google Docs findest du weiter unten. Sie bringt Folgendes ein:

- Dokumente, die jemand mit dir teilt.
- Kommentare und Antworten in deinen Dokumenten sowie Kommentare, in denen du erwähnt wirst.
- Nachverfolgte Änderungen in deinen Word-Dateien.

Der erste Abgleich reicht 7 Tage zurück. Jeder Eintrag ist mit Personen und Projekten in deinem [Graph](graph.md) verknüpft. Aus einem Kommentar, um den du dich kümmern musst, wird eine Aufgabe.

## Was sie kann

Wenn eine Aufgabe den Text eines Dokuments benötigt, liest deine Machine dieses Dokument, und zwar nur, während sie an der Aufgabe arbeitet.

Sie kann eine Antwort auf einen Kommentar entwerfen. Word bietet keine Möglichkeit, Antworten von außerhalb zu posten. Deshalb kopierst du den Entwurf in Word.

Sie nimmt niemals einen Vorschlag an, löst keinen Kommentar auf, teilt keine Datei und ändert kein Dokument ohne dein OK.

Wenn sie nur Aufgaben erledigen soll, deaktiviere **Liefert Signale** unter **Details**. Dann findet und liest sie nur die Dokumente, die für deine Aufgaben benötigt werden, und erstellt neue.

## Dokumente erstellen und bearbeiten

Deine Machine kann ein neues Dokument erstellen oder ein Dokument ändern, um das es in einer Aufgabe geht:

- Ein neues Dokument erstellt sie sofort, wenn die Aufgabe oder ein Skill danach fragt. Es ist privat und wird in deinem eigenen OneDrive oder Google Drive gespeichert. In der Aufgabe wird **Dokument öffnen** angezeigt. Das Dokument zu teilen oder seinen Link zu senden, wartet auf dein OK.
- Änderungen an einem bestehenden Dokument bereitet sie nur vor. Drücke **Änderungen prüfen**, um jeden Absatz vorher und nachher zu sehen, und anschließend **Speichern**. Eine Änderung, um die du im Chat der Aufgabe bittest, setzt sie sofort um.
- Sie schreibt nur in das Dokument, wie du es gesehen hast. Wenn jemand es inzwischen geändert hat, wird nichts geschrieben und die Aufgabe informiert dich darüber. Bitte um einen neuen Entwurf.
- In Talk liest sie die ganze Änderung laut vor und wartet auf ein eindeutiges Ja.
- Wenn Microsoft oder Google das Erstellen eines Dokuments ablehnt, erklärt die Aufgabe warum und zeigt **Prüfen und erstellen** an, damit du es noch einmal versuchen kannst.

Sie kann Text ersetzen sowie Text, Absätze und Überschriften hinzufügen. Tabellen, Bilder, nachverfolgte Änderungen und Felder bleiben unverändert.

Das Dokument einer Aufgabe für die Arbeit wird im Konto des Unternehmens gespeichert, niemals in einem persönlichen Konto. Auf deinem eigenen Computer kann auch ein Google-Konto mit Zugriff auf Drive neue Google Docs erstellen, wenn es für Gmail verbunden ist. Wenn kein passendes Konto vorhanden ist, sagt dir die Aufgabe, was du für die Arbeit verbinden musst: Microsoft OneDrive oder Google Docs, sofern deine Machine es verwenden kann.

Wenn das Dokument nicht der letzte Schritt ist, zum Beispiel bei einer Antwort mit einem Link darauf, bleibt die Aufgabe offen und erstellt einen Entwurf für diesen Schritt, der auf dein OK wartet.

Die Bearbeitungsfunktion ist beim Verbinden enthalten. Bei einer älteren Verbindung, die nur lesen kann, wird unter **Verbindungen** die Option **Bearbeiten erlauben** angezeigt. Drücke darauf und bestätige.

## Was sie anfragt

Microsoft bittet dich um ein einmaliges OK, damit deine Dateien gelesen und geändert werden können, einschließlich der Dateien, die mit dir geteilt wurden. Jede Änderung wartet weiterhin auf dein OK in der jeweiligen Aufgabe. Der Zugriff auf deine Mails und deinen Kalender ändert sich nicht.

Wenn du dieses OK später zurückziehst, zeigt Microsoft OneDrive unter **Verbindungen** die Meldung **Wartet auf dein OK, um Dokumente zu lesen** an.

## Verbindung herstellen

Auf einer gehosteten Machine oder auf deinem eigenen Computer, der mit deinem Konto gekoppelt ist:

- Öffne **Verbindungen**, dann **Dokumente und Dateien**, und wähle **Microsoft OneDrive** aus.
- Drücke **Mit Microsoft anmelden** und erlaube das Lesen und Bearbeiten deiner Dateien.

Wenn Microsoft das Lesen nicht erlaubt, wird die Verbindung nicht hinzugefügt. Wenn du **Bearbeiten erlauben** drückst und Microsoft das Bearbeiten nicht erlaubt, wird dir das mitgeteilt.

## Google Docs

Öffne auf einer gehosteten Machine **Verbindungen**, dann **Dokumente und Dateien**, und wähle **Google Docs** aus. Google bittet dich um Erlaubnis, die Dokumente anzusehen und zu bearbeiten, auf die du verweist, sowie neue Dokumente zu erstellen. Gmail muss nicht verbunden sein und dein Gmail-Zugriff ändert sich nicht.

Dann kann deine Machine:

- Ein Google-Dokument lesen, auf das in den Nachrichten einer Aufgabe verwiesen wird, und zwar nur, während sie an dieser Aufgabe arbeitet.
- Änderungen an diesem Dokument vorbereiten. Jede Änderung wartet wie oben beschrieben auf dein OK.
- Neue private Dokumente in deinem Google Drive erstellen.

Sie durchsucht dein Drive nicht. Kommentare, Freigaben und Vorschläge sieht sie nur in Dokumenten, die sie selbst erstellt hat. Für mehr Zugriff müsste sie auf dein ganzes Drive zugreifen können. Danach fragt sie aber nicht.

Auf deinem eigenen Computer kann deine Machine ein neues Google-Dokument in einem dort angemeldeten Gmail-Konto erstellen, das bereits Zugriff auf Drive hat. Sie liest keine anderen Google Docs und deren Kommentare. Unter **Dokumente und Dateien** wird das Konto als Google Docs angezeigt. Außerdem kann sie dort ein Dokument ändern, das sie für eine Aufgabe erstellt hat.

## Arbeit oder privat

Sie richtet sich wie bei Mails nach der Kennzeichnung Arbeit oder Privat der jeweiligen Verbindung. Dokumente für die Arbeit können gemäß deinen [Freigaberegeln](sharing-rules.md) in den Graph deines Teams gelangen. Private Dokumente gelangen niemals dorthin.

## Verbindung entfernen

Öffne **Verbindungen**, dann Microsoft OneDrive oder Google Docs, **Details** und **Trennen**. Die Verbindung liest dann nichts mehr. Was sie bereits eingebracht hat, bleibt erhalten. Auf einer gehosteten Machine öffnet **Trennen ↗** deine Einrichtungsseite, auf der die Anmeldung gespeichert ist.
