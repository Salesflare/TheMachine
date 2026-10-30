---
title: Docs: Word, OneDrive und SharePoint
area: connections
summary: Kommentare, Erwähnungen, nachverfolgte Änderungen und Freigaben in deinen Word-Dateien in OneDrive und SharePoint. Google Docs kommen später.
covers: connector:docs
code: connectors/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
---
## Was es liest

Docs liest Word-Dateien in OneDrive und SharePoint, mit der Microsoft-Anmeldung, die du für diese Adresse schon hast. Das geht auf einer gehosteten Machine und auf deinem eigenen Computer, der mit deinem Konto gekoppelt ist. Google Docs kommen später: Die Google-Anmeldung von The Machine kann noch keine Dokumente lesen. Es bringt rein:

- Dokumente, die jemand mit dir teilt.
- Kommentare und Antworten in Dokumenten, die dir gehören, und Kommentare, die dich erwähnen.
- Nachverfolgte Änderungen in Word-Dateien, die dir gehören.

Die erste Synchronisierung schaut 30 Tage zurück. Daraus wird jeweils ein Termin, verknüpft mit den Personen und Projekten in deinem [Graph](graph.md). Wenn ein Kommentar dich braucht, wird daraus eine Aufgabe.

## Was es tun kann

Wenn eine Aufgabe den Text eines Dokuments braucht, liest deine Machine genau dieses Dokument, und nur, solange sie an dieser Aufgabe arbeitet.

Es kann eine Antwort auf einen Kommentar entwerfen. Word-Dateien bieten keinen Weg, von außerhalb von Word zu antworten. Die Antwort bleibt also ein Entwurf, den du in Word kopierst.

Es nimmt keine Vorschläge an, löst keine Kommentare auf, teilt keine Dateien und ändert kein Dokument ohne dein OK.

## Dokumente erstellen und bearbeiten

Deine Machine kann ein neues Word-Dokument schreiben oder ein Dokument ändern, um das es in einer deiner Aufgaben geht. Sie schreibt nie von selbst:

- Sie bereitet die Änderung in der Aufgabe vor. Ein neues Dokument siehst du ganz, eine Bearbeitung als jeden Absatz vorher und nachher.
- Tippe auf **Prüfen und erstellen** oder **Änderungen prüfen**, lies alles und dann **Erstellen** oder **Speichern**.
- Sie schreibt einmal, und nur in das Dokument, wie du es gesehen hast. Hat jemand es inzwischen geändert, wird nichts geschrieben und die Aufgabe sagt es dir. Bitte dann um einen neuen Entwurf.
- In Talk liest sie die ganze Änderung vor und wartet auf ein klares Ja.

Sie ersetzt Text, fügt Text hinzu und fügt Absätze und Überschriften ein. Tabellen, Bilder, nachverfolgte Änderungen und Felder lässt sie in Ruhe. Ein neues Dokument landet in deinem OneDrive und bleibt privat, bis du es teilst.

Zum Einschalten tippst du auf der Docs-Karte unter **Verbindungen** auf **Bearbeiten erlauben**. Microsoft fragt, ob sie deine Dateien ändern darf, getrennt vom Lesen. Eine neue Anmeldung behält das bei.

## Worum es fragt

Das Lesen von Dokumenten braucht ein eigenes OK, getrennt von deiner Mail-Anmeldung: Microsoft bittet dich, das Lesen deiner Dateien zu erlauben, auch der Dateien, die in OneDrive und SharePoint mit dir geteilt sind. Dein Zugriff auf Mail und Kalender bleibt, wie er ist.

Wird dieses OK später zurückgenommen, zeigt die Docs-Karte **Wartet auf dein OK, um Dokumente zu lesen**.

## Verbinden

Verbinde zuerst Outlook für die Adresse. Dann:

- Gehostete Machine: Öffne im Dashboard **Verbindungen**, **+ Hinzufügen**, wähle **Dokumente** und tippe auf **Mit Microsoft anmelden**. Microsoft bittet dich, das Lesen deiner Dateien zu erlauben, dann kommst du zurück zum Dashboard.
- Dein eigener Computer, gekoppelt mit deinem Konto: Öffne **Verbindungen**, **+ Hinzufügen**, wähle **Dokumente** und tippe auf **Mit Microsoft anmelden**.

Es prüft, ob die Anmeldung Dokumente lesen darf. Ohne dieses OK wird es nicht hinzugefügt.

## Arbeit oder privat

Docs folgt der Kennzeichnung Arbeit oder privat seiner Verbindung, wie bei Mail. Arbeitsdokumente können nach deinen [Freigaberegeln](sharing-rules.md) in den Graph deines Teams gelangen. Private nie.

## Entfernen

Im Dashboard: **Verbindungen**, Docs öffnen, **Details**, dann **Trennen**. Es hört auf zu lesen. Was es schon reingebracht hat, bleibt.
