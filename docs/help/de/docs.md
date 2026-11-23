---
title: Microsoft OneDrive
area: connections
summary: Kommentare, Erwähnungen und nachverfolgte Änderungen in deinen Word-Dateien in OneDrive. Neue Dokumente und Änderungen warten auf dein OK.
covers: connector:docs
code: connectors/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: 41e5651f29782588
---
## Was gelesen wird

**Microsoft OneDrive** liest deine Word-Dateien in OneDrive, auf einer gehosteten Machine und auf deinem eigenen Computer. Outlook muss nicht verbunden sein. Informationen zu Google Docs findest du weiter unten. Folgendes wird importiert:

- Kommentare und Antworten auf deine Word-Dateien sowie Kommentare, in denen du erwähnt wirst.
- Nachverfolgte Änderungen in deinen Word-Dateien.

Die erste Synchronisierung reicht 7 Tage zurück. Jeder Eintrag ist mit den Personen und Projekten in deinem [Graph](graph.md) verknüpft. Ein Kommentar, der deine Aufmerksamkeit braucht, wird zu einer Aufgabe.

## Dateien, die andere mit dir teilen

Microsoft führt diese ab November 2026 nicht mehr auf. Geteilte Dateien und Erwähnungen in Dateien anderer erreichen deine Machine dann nur noch über E-Mails von Microsoft. Verbinde auch [Outlook](microsoft.md) und lass diese E-Mails aktiviert. Eine Aufgabe, die aus einer solchen E-Mail entsteht, öffnet die E-Mail. Über die Schaltfläche darin öffnest du die Datei. Geteilte Dateien und Erwähnungen ohne E-Mail werden nicht erkannt.

## Was möglich ist

Wenn eine Aufgabe den Text eines Dokuments benötigt, liest deine Machine dieses Dokument, aber nur, während sie an der Aufgabe arbeitet. Sie kann Word-, PDF- und Textdateien lesen.

Sie sucht auch nach Dateien aller Art in deinem eigenen OneDrive und stellt dir den Link dazu bereit. Sie durchsucht keine SharePoint-Websites und keine Dateien, die mit dir geteilt wurden. Den Text aus eingescannten PDFs kann sie nicht lesen.

Sie kann einen Antwortentwurf zu einem Kommentar schreiben. Da Word keine Möglichkeit bietet, Antworten von außerhalb zu posten, kopierst du den Entwurf in Word.

Sie nimmt niemals einen Vorschlag an, löst einen Kommentar auf, teilt eine Datei oder ändert ein Dokument ohne dein OK.

Wenn du sie nur zum Erledigen von Aufgaben verwenden möchtest, deaktiviere **Liefert Signale** unter **Details**. Dann findet und liest sie nur die Dateien, die für deine Aufgaben gebraucht werden, und erstellt neue Dateien.

## Dokumente erstellen und bearbeiten

Deine Machine kann ein neues Dokument schreiben oder ein Dokument ändern, um das es in einer Aufgabe geht:

- Ein neues Dokument erstellt sie sofort, wenn die Aufgabe oder ein Skill danach fragt. Es ist privat und wird in deinem eigenen OneDrive oder Google Drive gespeichert. In der Aufgabe wird **Dokument öffnen** angezeigt. Eine Freigabe oder das Senden des Links wartet auf dein OK.
- Änderungen an einem bestehenden Dokument bereitet sie nur vor. Wähle **Änderungen prüfen**, um jeden Absatz vorher und nachher zu sehen, und dann **Speichern**. Eine Änderung, um die du im Chat der Aufgabe bittest, nimmt sie sofort vor.
- Sie schreibt nur in das Dokument, so wie du es gesehen hast. Wenn es inzwischen jemand geändert hat, wird nichts geschrieben und die Aufgabe teilt dir das mit. Bitte um einen neuen Entwurf.
- In Talk liest sie die gesamte Änderung laut vor und wartet auf ein eindeutiges Ja.
- Wenn Microsoft oder Google ein neues Dokument nicht zulässt, erklärt die Aufgabe den Grund und zeigt **Prüfen und erstellen** an, damit du es erneut versuchen kannst.

Sie kann Text ersetzen und Text, Absätze und Überschriften hinzufügen. Tabellen, Bilder, nachverfolgte Änderungen und Felder bleiben unverändert.

Das Dokument einer geschäftlichen Aufgabe wird im Konto des Unternehmens gespeichert, niemals in einem privaten Konto. Auf deinem eigenen Computer kann ein Google-Konto, das für Gmail verbunden ist und Zugriff auf Drive hat, auch neue Google Docs erstellen. Wenn kein Konto dafür infrage kommt, sagt dir die Aufgabe, was du für geschäftliche Aufgaben verbinden musst: Microsoft OneDrive oder, sofern deine Machine es verwenden kann, Google Docs.

Wenn das Dokument nicht der letzte Schritt ist, zum Beispiel bei einer Antwort mit dem Link dazu, bleibt die Aufgabe offen und erstellt einen Entwurf für diesen Schritt, der auf dein OK wartet.

Die Bearbeitung wird beim Verbinden eingerichtet. Bei einer älteren Verbindung, die nur lesen kann, wird unter **Verbindungen** **Bearbeiten erlauben** angezeigt. Wähle die Option einmal aus und bestätige.

## Welche Berechtigungen angefragt werden

Microsoft bittet dich um ein OK, damit deine Machine deine Dateien lesen und ändern darf, auch Dateien, die mit dir geteilt wurden. Jede Änderung wartet weiterhin in der jeweiligen Aufgabe auf dein OK. Der Zugriff auf deine E-Mails und deinen Kalender ändert sich nicht.

Wenn du dieses OK später widerrufst, wird in **Verbindungen** bei Microsoft OneDrive **Wartet auf dein OK, um Dokumente zu lesen** angezeigt.

## Verbindung herstellen

Auf einer gehosteten Machine oder auf deinem eigenen Computer, der mit deinem Konto gekoppelt ist:

- Öffne **Verbindungen**, dann **Dokumente und Dateien**, und wähle **Microsoft OneDrive** aus.
- Wähle **Bei Microsoft anmelden** und erlaube das Lesen und Bearbeiten deiner Dateien.

Wenn Microsoft das Lesen nicht erlaubt, wird die Verbindung nicht hinzugefügt. Wenn du **Bearbeiten erlauben** auswählst und Microsoft die Bearbeitung nicht zulässt, wird dir das mitgeteilt.

## Google Docs

Öffne auf einer gehosteten Machine **Verbindungen**, dann **Dokumente und Dateien**, und wähle **Google Docs** aus. Google bittet dich darum, den Zugriff auf die Dokumente zu erlauben, auf die du verweist, und neue Dokumente erstellen und bearbeiten zu dürfen. Gmail muss nicht verbunden sein und der Zugriff auf dein Gmail-Konto ändert sich nicht.

Danach kann deine Machine:

- Ein Google-Dokument lesen, das in den Nachrichten einer Aufgabe verlinkt ist, aber nur, während sie an dieser Aufgabe arbeitet.
- Änderungen an diesem Dokument vorbereiten. Jede Änderung wartet wie oben beschrieben auf dein OK.
- Neue private Dokumente in deinem Google Drive erstellen.

Sie durchsucht dein Drive nicht. Kommentare, Freigaben und Vorschläge sieht sie nur in Dokumenten, die sie selbst erstellt hat. Für mehr Zugriff müsste sie dein gesamtes Drive nutzen können. Diesen Zugriff fragt sie nicht an.

Auf deinem eigenen Computer kann deine Machine ein neues Google-Dokument in einem dort angemeldeten Gmail-Konto erstellen, das bereits Zugriff auf Drive hat. Sie liest keine deiner anderen Google-Dokumente und auch nicht deren Kommentare. Unter **Dokumente und Dateien** wird dieses Konto als Google Docs angezeigt. Außerdem kann sie dort ein Dokument ändern, das sie für eine Aufgabe erstellt hat.

## Geschäftlich oder privat

Wie bei E-Mails richtet sie sich nach der Kennzeichnung „Geschäftlich“ oder „Privat“ der jeweiligen Verbindung. Geschäftliche Dokumente können gemäß deinen [Freigaberegeln](sharing-rules.md) im Graph deines Teams landen. Private Dokumente gelangen nie dorthin.

## Verbindung trennen

Öffne **Verbindungen**, dann Microsoft OneDrive oder Google Docs, **Details** und **Trennen**. Die Verbindung liest dann keine Dateien mehr. Was sie bereits importiert hat, bleibt erhalten. Auf einer gehosteten Machine öffnet **Trennen ↗** deine Einrichtungsseite, auf der die Anmeldung gespeichert ist.
