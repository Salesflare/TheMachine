---
title: Microsoft OneDrive: Word-Dateien in OneDrive und SharePoint
area: connections
summary: Kommentare, Erwähnungen, nachverfolgte Änderungen und Freigaben in deinen Word-Dateien in OneDrive und SharePoint, dazu neue private Dokumente und Änderungen, die du freigibst. Google Docs kommen später.
covers: connector:docs
code: connectors/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
---
## Was es liest

Die Verbindung **Microsoft OneDrive** liest Word-Dateien in OneDrive und SharePoint. Du meldest dich dafür mit Microsoft an, mit oder ohne verbundenes Outlook. Das geht auf einer gehosteten Machine und auf deinem eigenen Computer, der mit deinem Konto gekoppelt ist. Google Docs kommen später: Die Google-Anmeldung von The Machine kann noch keine Dokumente lesen. Es bringt rein:

- Dokumente, die jemand mit dir teilt.
- Kommentare und Antworten in Dokumenten, die dir gehören, und Kommentare, die dich erwähnen.
- Nachverfolgte Änderungen in Word-Dateien, die dir gehören.

Die erste Synchronisierung schaut 30 Tage zurück. Daraus wird jeweils ein Termin, verknüpft mit den Personen und Projekten in deinem [Graph](graph.md). Wenn ein Kommentar dich braucht, wird daraus eine Aufgabe.

## Was es tun kann

Wenn eine Aufgabe den Text eines Dokuments braucht, liest deine Machine genau dieses Dokument, und nur, solange sie an dieser Aufgabe arbeitet.

Es kann eine Antwort auf einen Kommentar entwerfen. Word-Dateien bieten keinen Weg, von außerhalb von Word zu antworten. Die Antwort bleibt also ein Entwurf, den du in Word kopierst.

Es nimmt keine Vorschläge an, löst keine Kommentare auf, teilt keine Dateien und ändert kein Dokument ohne dein OK.

## Dokumente erstellen und bearbeiten

Deine Machine kann ein neues Dokument schreiben oder ein Dokument ändern, um das es in einer deiner Aufgaben geht:

- Ein neues Dokument erstellt sie sofort, wenn die Aufgabe oder ein Skill eines verlangt: ein privates Dokument in deinem eigenen Google Drive oder OneDrive, mit niemandem geteilt. Die Aufgabe zeigt es mit **Dokument öffnen**. Das Teilen, oder den Link an jemanden schicken, wartet auf dein OK.
- Eine Änderung an einem bestehenden Dokument bereitet sie nur vor, jeden Absatz vorher und nachher. Tippe auf **Änderungen prüfen**, lies alles und dann **Speichern**.
- Sie schreibt eine Änderung einmal, und nur in das Dokument, wie du es gesehen hast. Hat jemand es inzwischen geändert, wird nichts geschrieben und die Aufgabe sagt es dir. Bitte dann um einen neuen Entwurf.
- In Talk liest sie die ganze Änderung vor und wartet auf ein klares Ja.
- Lehnt Google oder Microsoft ein neues Dokument ab, sagt die Aufgabe, was abgelehnt wurde, und zeigt **Prüfen und erstellen**, um es noch einmal zu versuchen.

Sie ersetzt Text, fügt Text hinzu und fügt Absätze und Überschriften ein. Tabellen, Bilder, nachverfolgte Änderungen und Felder lässt sie in Ruhe. Ein neues Dokument landet in deinem Google Drive oder OneDrive und bleibt privat, bis du es teilst.

Ein neues Dokument kommt in ein Konto aus dem Bereich der Aufgabe: das Dokument einer Arbeitsaufgabe in das Konto dieser Firma, wenn möglich das Konto des Gesprächs, nie in ein privates. Auf deinem eigenen Computer kann auch ein Google-Konto, das für Gmail angemeldet ist und schon Zugriff auf Drive hat, ein neues Google-Dokument bekommen. Passt kein Konto, sagt die Aufgabe **Verbinde Google Docs oder Microsoft OneDrive für Arbeit**.

Ist das Dokument nicht das Ende der Aufgabe, etwa wenn noch eine Antwort mit dem Link fehlt, bleibt die Aufgabe offen und bereitet diesen nächsten Schritt für dein OK vor.

Das Verbinden von Microsoft OneDrive erlaubt das schon: Es gibt keinen eigenen Schritt. Eine ältere Microsoft-OneDrive-Verbindung, die nur liest, zeigt auf ihrer Karte unter **Verbindungen** **Bearbeiten erlauben**. Tippe einmal darauf und stimme zu.

## Worum es fragt

Microsoft OneDrive fragt Microsoft nach einem OK, getrennt von deiner Mail-Anmeldung: deine Dateien zu lesen und zu ändern, auch die, die in OneDrive und SharePoint mit dir geteilt sind. Jede Änderung wartet trotzdem auf dein OK in ihrer Aufgabe. Dein Zugriff auf Mail und Kalender bleibt, wie er ist. Ohne Outlook gilt die Anmeldung nur für deine Dateien, nie für Mail oder Kalender.

Wird dieses OK später zurückgenommen, zeigt die Microsoft-OneDrive-Karte **Wartet auf dein OK, um Dokumente zu lesen**.

## Verbinden

Du brauchst dafür kein verbundenes Outlook.

- Gehostete Machine: Öffne im Dashboard **Verbindungen**, **+ Hinzufügen**, wähle **Microsoft OneDrive** und tippe auf **Mit Microsoft anmelden**. Microsoft bittet dich, das Lesen und Bearbeiten deiner Dateien zu erlauben, dann kommst du zurück zum Dashboard.
- Dein eigener Computer, gekoppelt mit deinem Konto: Öffne **Verbindungen**, **+ Hinzufügen**, wähle **Microsoft OneDrive** und tippe auf **Mit Microsoft anmelden**.

Es prüft, ob die Anmeldung Dokumente lesen darf. Ohne dieses OK wird es nicht hinzugefügt. Tippst du auf **Bearbeiten erlauben** und Microsoft erlaubt keine Änderungen, sagt es das, statt Verbunden zu zeigen.

## Arbeit oder privat

Microsoft OneDrive folgt der Kennzeichnung Arbeit oder privat seiner Verbindung, wie bei Mail. Arbeitsdokumente können nach deinen [Freigaberegeln](sharing-rules.md) in den Graph deines Teams gelangen. Private nie.

## Entfernen

Im Dashboard: **Verbindungen**, Microsoft OneDrive öffnen, **Details**, dann **Trennen**. Es hört auf zu lesen. Was es schon reingebracht hat, bleibt.
