---
title: Microsoft OneDrive
area: connections
summary: Kommentare, Erwähnungen und nachverfolgte Änderungen in deinen Word-Dateien in OneDrive. Neue Dokumente und Änderungen warten auf dein OK.
covers: connector:docs
code: connectors/docs.py, google_files.py, google_links.py, machine/app/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: c8fca3cf0299e327
---
## Was gelesen wird

**Microsoft OneDrive** liest deine Word-Dateien in OneDrive, auf einer gehosteten Machine und auf deinem eigenen Computer. Outlook muss dafür nicht verbunden sein. Informationen zu Google Docs findest du weiter unten. Die Verbindung liefert:

- Kommentare und Antworten zu deinen Word-Dateien sowie Kommentare darin, in denen du erwähnt wirst.
- Nachverfolgte Änderungen in deinen Word-Dateien.

Beim ersten Sync werden die letzten 7 Tage berücksichtigt. Jeder Eintrag ist mit den Personen und Projekten in deinem [Graph](graph.md) verknüpft. Aus einem Kommentar, der deine Aufmerksamkeit braucht, wird eine Aufgabe.

## Dateien, die andere für dich freigeben

Microsoft führt diese Dateien ab November 2026 nicht mehr auf. Freigaben und Erwähnungen in Dateien anderer Personen erreichen deine Machine dann nur noch über die E-Mails von Microsoft. Verbinde auch [Outlook](microsoft.md) und lass diese E-Mails aktiviert. Eine Aufgabe aus so einer E-Mail öffnet die E-Mail, und über die Schaltfläche darin öffnest du die Datei. Freigaben oder Erwähnungen ohne E-Mail werden nicht erkannt.

## Was die Verbindung kann

Wenn eine Aufgabe den Text eines Dokuments benötigt, liest deine Machine dieses Dokument, aber nur, während sie an der Aufgabe arbeitet. Sie kann Word-, PDF- und Textdateien lesen.

Sie sucht auch nach Dateien aller Art in deinem eigenen OneDrive und stellt dir den Link dazu bereit. SharePoint-Websites und Dateien, die andere für dich freigegeben haben, durchsucht sie nicht. Den Text in einem eingescannten PDF kann sie nicht lesen.

Sie kann einen Antwortentwurf zu einem Kommentar schreiben. Da Word keine Möglichkeit bietet, Antworten von außerhalb zu posten, kopierst du den Entwurf in Word.

Sie nimmt niemals einen Vorschlag an, löst einen Kommentar auf, gibt eine Datei frei oder ändert ein Dokument ohne dein OK.

Wenn du die Verbindung nur zum Erledigen von Aufgaben verwenden möchtest, deaktiviere **Liefert Signale** unter **Details**. Dann findet und liest sie nur die Dateien, die deine Aufgaben benötigen, und erstellt neue Dateien.

## Dokumente erstellen und bearbeiten

Deine Machine kann ein neues Dokument schreiben oder ein Dokument ändern, um das es in einer Aufgabe geht:

- Ein neues Dokument erstellt sie sofort, wenn die Aufgabe oder ein Skill danach fragt. Es ist privat und liegt in deinem eigenen OneDrive oder Google Drive. In der Aufgabe wird **Dokument öffnen** angezeigt. Das Dokument freizugeben oder seinen Link zu verschicken, wartet auf dein OK.
- Änderungen an einem vorhandenen Dokument bereitet sie nur vor. Drücke **Änderungen prüfen**, um jeden Absatz vorher und nachher zu sehen, und dann **Speichern**. Änderungen, die du im Chat der Aufgabe anforderst, setzt sie sofort um.
- Sie schreibt nur in das Dokument, dessen Inhalt du gesehen hast. Wenn es inzwischen jemand geändert hat, wird nichts geschrieben und die Aufgabe weist dich darauf hin. Bitte um einen neuen Entwurf.
- In Talk liest sie die gesamte Änderung vor und wartet auf ein eindeutiges Ja.
- Wenn Microsoft oder Google das Erstellen eines neuen Dokuments ablehnt, erklärt die Aufgabe den Grund und zeigt **Prüfen und erstellen** an, damit du es noch einmal versuchen kannst.

Sie kann Text ersetzen und Text, Absätze und Überschriften hinzufügen. In Google Docs kann sie außerdem formatieren: fett, kursiv, unterstrichen, Links, Überschriften, Aufzählungen und nummerierte Listen sowie Seitenumbrüche. **Änderungen prüfen** zeigt jede einzelne Änderung. Tabellen kann sie nicht erstellen. Bilder, nachverfolgte Änderungen und Felder bleiben unverändert.

Das Dokument einer Work-Aufgabe wird im Konto des jeweiligen Unternehmens gespeichert, niemals in einem persönlichen Konto. Auf deinem eigenen Computer kann auch ein Google-Konto, das für Gmail verbunden ist und Zugriff auf Drive hat, neue Google Docs erstellen. Wenn kein Konto passt, erklärt die Aufgabe, was du für Work verbinden musst: Microsoft OneDrive oder Google Docs, sofern deine Machine es verwenden kann.

Wenn das Dokument nicht der letzte Schritt ist, zum Beispiel bei einer Antwort mit dem Link darauf, bleibt die Aufgabe offen und erstellt einen Entwurf für diesen Schritt, der auf dein OK wartet.

Die Bearbeitungsfunktion ist Teil der Verbindung. Bei einer älteren Verbindung mit reinem Lesezugriff wird unter **Verbindungen** die Option **Bearbeiten erlauben** angezeigt. Drücke einmal darauf und bestätige.

## Welche Berechtigungen angefragt werden

Microsoft bittet dich um ein OK, damit die Verbindung deine Dateien lesen und ändern kann, auch Dateien, die für dich freigegeben wurden. Jede Änderung wartet weiterhin auf dein OK in der jeweiligen Aufgabe. Der Zugriff auf deine E-Mails und deinen Kalender ändert sich nicht.

Wenn du dieses OK später widerrufst, zeigt Microsoft OneDrive unter **Verbindungen** den Hinweis **Wartet auf dein OK, um Dokumente zu lesen** an.

## Verbindung herstellen

Auf einer gehosteten Machine oder auf deinem eigenen Computer, der mit deinem Konto gekoppelt ist:

- Öffne **Verbindungen**, dann **Dokumente und Dateien**, und wähle **Microsoft OneDrive** aus.
- Drücke **Mit Microsoft anmelden** und erlaube den Lese- und Bearbeitungszugriff auf deine Dateien.

Wenn Microsoft den Lesezugriff nicht erlaubt, wird die Verbindung nicht hinzugefügt. Wenn du **Bearbeiten erlauben** drückst und Microsoft den Bearbeitungszugriff nicht erlaubt, weist Microsoft dich darauf hin.

## Google Docs

Öffne auf einer gehosteten Machine **Verbindungen**, dann **Dokumente und Dateien**, und wähle **Google Docs** aus. Google bittet dich darum, den Zugriff auf die Dokumente zu erlauben, auf die du verweist, damit die Verbindung sie sehen, bearbeiten und neue erstellen kann. Gmail muss nicht verbunden sein, und dein Gmail-Zugriff ändert sich nicht.

Danach kann deine Machine:

- Ein Google-Dokument lesen, das in den Nachrichten einer Aufgabe verlinkt oder in den Chat der Aufgabe eingefügt wurde, aber nur, während sie an dieser Aufgabe arbeitet.
- Änderungen an diesem Dokument vorbereiten. Jede Änderung wartet wie oben beschrieben auf dein OK.
- Neue private Dokumente in deinem Google Drive erstellen.

Sie durchsucht dein Drive nicht. Kommentare, Freigaben und Vorschläge sieht sie nur in Dokumenten, die sie selbst erstellt hat. Für den Zugriff auf mehr müsste sie dein gesamtes Drive verwenden. Danach fragt sie nicht.

## Google Sheets und Slides

Wenn unter **Verbindungen** bei Google Docs die Option **Zugriff auf Sheets und Slides erlauben** angezeigt wird, drücke darauf und erlaube den Zugriff auf beide. Google bittet dich darum, deiner Machine Zugriff auf deine Sheets- und Slides-Dateien zu geben. Ändern kann sie diese nicht.

Danach liest deine Machine auch eine Google-Sheets- oder Slides-Datei, die in den Nachrichten einer Aufgabe verlinkt oder in ihren Chat eingefügt wurde, aber nur, während sie an dieser Aufgabe arbeitet:

- In einem Sheet liest sie zuerst den verlinkten Tabellenreiter oder die verknüpften Zellen, dann die anderen Reiter, bis zu 2.000 Zellen. Eine Formel wird als ihr Wert angezeigt. Ausgeblendete Reiter liest sie nur, wenn auf sie verwiesen oder danach gefragt wird.
- In Slides liest sie den Text und die Sprechernotizen der Reihe nach. Bilder und Diagramme liest sie nicht.

Bei einer großen Datei kannst du im Chat angeben, welchen Reiter, welche Zellen oder welche Folien du meinst. Wenn eine Datei für jemand anderen privat ist, gelöscht wurde oder eine Excel- oder PowerPoint-Datei ist, weist dich die Aufgabe darauf hin. Ein Google-Drive-Link funktioniert genauso, wenn er auf ein Google-Dokument, ein Sheet oder eine Slides-Datei verweist.

## Google Docs auf deinem eigenen Computer

Auf deinem eigenen Computer kann deine Machine ein neues Google-Dokument in einem Gmail-Konto erstellen, bei dem du angemeldet bist und das bereits Zugriff auf Drive hat. Andere Google-Dokumente und ihre Kommentare liest sie nicht. Unter **Dokumente und Dateien** wird es als Google Docs für dieses Konto angezeigt. Sie kann auch ein Dokument ändern, das sie dort für eine Aufgabe erstellt hat.

Sie liest außerdem eine Google-Sheets- oder Slides-Datei, die in einer Aufgabe verlinkt oder in deren Chat eingefügt wurde, wenn die angemeldete Google-Verbindung bereits Zugriff auf Drive, Sheets oder Slides hat. Bei Google fragt sie niemals nach weiteren Berechtigungen. Wenn Google den Zugriff verweigert, aktiviere die Google-Sheets- oder Slides-API im eigenen Google-Projekt dieser Anmeldung.

## Arbeit oder privat

Wie bei E-Mails richtet sie sich nach der Kennzeichnung „Arbeit“ oder „Privat“ der Verbindung. Arbeitsdokumente können gemäß deinen [Freigaberegeln](sharing-rules.md) in den Graph deines Teams gelangen. Private Dokumente gelangen niemals dorthin.

## Verbindung entfernen

Öffne **Verbindungen**, dann Microsoft OneDrive oder Google Docs, **Details** und **Trennen**. Die Verbindung liest dann keine Daten mehr. Was sie bereits importiert hat, bleibt erhalten. Auf einer gehosteten Machine öffnet **Trennen ↗** deine Einrichtungsseite, auf der die Anmeldung gespeichert ist.
