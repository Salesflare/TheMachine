---
title: Kalender
area: calendar
summary: Die kommende Woche auf einen Blick: Meetings, fällige und zurückgestellte Aufgaben sowie Versprechen.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py
order: 1
translated: d85b3eff63ea503d
---
## Was angezeigt wird

Deine Tage ab heute mit:

- Meetings aus den Kalendern, die du verbunden hast,
- Aufgaben, die an diesem Tag fällig sind, und zurückgestellte Aufgaben an dem Tag, an dem sie wieder anstehen,
- Rückmeldungen zu Aufgaben, die du abgegeben hast,
- Versprechen mit einem Datum,
- [Notizen](notes.md) mit Datum, zum Beispiel zu einer Reise.

Ein Meeting in zwei Kalendern wird nur einmal angezeigt. Ein Kalender, den jemand mit dir geteilt hat, zeigt die Termine dieser Person gedimmt und mit ihrem Vornamen an. Daraus wird nie eine Aufgabe erstellt. Ganztägige und mehrtägige Termine werden an jedem Tag, den sie umfassen, als ganztägig angezeigt. Eine Reise steht in der Agenda an jedem ihrer Tage ganz oben. In der Wochen- und Monatsansicht wird sie als durchgehender Balken über diese Tage angezeigt, zum Beispiel „Lisbon-Reise“.

Ein gemeinsamer Plan ist ein Versprechen, das mit „Mit“ und dem Namen der anderen Person gekennzeichnet ist. Ein Versprechen zu einem Meeting an diesem Tag mit derselben Person erscheint in der Zeile des Meetings.

**Überfällig** steht ganz oben. Bei einem Meeting mit einer offenen Aufgabe wird **Vorbereitung bereit**, **Wird vorbereitet** oder **Aufgabe** angezeigt. Eine Aufgabe, die erledigt scheint, weil du schon geantwortet hast oder ihr Durchlauf sie als erledigt erkannt hat, wird nicht als **Fällig** angezeigt.

## Agenda, Woche oder Monat

- **Agenda** listet jeden Tag auf. Scrolle nach unten zu späteren Tagen oder nach oben beziehungsweise tippe auf **Frühere Tage anzeigen**, um frühere Tage zu sehen. Die Ansicht reicht bis zu einer Woche vor dem Tag zurück, an dem du deinen Kalender verbunden hast. Oben steht eine Zeile, ab welchem Tag sie beginnt. Sobald der [Verlauf](history.md) geladen ist, reicht sie etwa ein Jahr zurück.
- **Woche** zeigt eine Übersicht von Montag bis Sonntag. Auf dem Smartphone werden drei Tage angezeigt.
- **Monat** zeigt den ganzen Monat. Auf einem Computer werden bis zu drei Einträge pro Tag angezeigt. Auf dem Smartphone erscheinen Punkte. Tippe darauf, um die Einträge des Tages aufzulisten.

Mit **Heute**, ‹ und › oben kannst du durch die Wochen oder Monate wechseln. Die ausgewählte Ansicht wird auf diesem Gerät gespeichert.

In der Wochenübersicht werden Termine zur selben Zeit nebeneinander angezeigt, sodass jeder lesbar bleibt. Weitere Termine werden als **+N** angezeigt. Tippe darauf, um den Tag in der Agenda zu öffnen.

## Etwas öffnen

Klicke auf eine Zeile, um den Chat zur Aufgabe, das Versprechen, die Notiz oder das Meeting zu öffnen. Bei einem Meeting, das du hier nicht ändern kannst, etwa dem einer anderen Person oder einem mit Gästen, werden die Details angezeigt: wann und wo es stattfindet und wer dabei ist. Ein Kontakt, den dein Graph kennt, sowie die Organisationen und Projekte des Meetings sind mit ihren Seiten verlinkt. Über **In Google Calendar öffnen** oder **In Outlook öffnen** darunter kannst du den Termin dort öffnen. Das Öffnen ändert nichts.

Ein Meetingraum, der für ein Meeting gebucht wurde, wird unter dem Ort angezeigt, niemals als Person oder in deinem Graph.

Ein Meeting-Link wird mit dem jeweiligen Dienst angezeigt, zum Beispiel Zoom, Google Meet oder Teams, oder als **Videoanruf**. Öffne das Meeting, um teilzunehmen.

## Meeting-Notizen und Transkript

Die Details eines Meetings haben zwei Bereiche. **Notizen** enthält die Zusammenfassung: Entscheidungen und Aufgaben. **Transkript** enthält wortwörtlich, was gesagt wurde. Es ist zunächst eingeklappt und zeigt die Dauer an. Über **Anzeigen** kannst du es öffnen.

Wenn die Inhalte nicht geladen werden, versucht The Machine es etwa eine halbe Minute lang automatisch erneut. Tippe danach auf **Erneut versuchen**.

Für beide Bereiche gibt es eigene Optionen zum **Notizen hinzufügen** oder **Transkript hinzufügen**, zum **Datei hochladen** für eine Markdown- oder Textdatei sowie zum **Bearbeiten** und **Entfernen** (zweimal tippen). Was du in einen Bereich einfügst, bleibt dort. Bei einem Meeting, das du ändern kannst, öffnet **Notizen** unter dem Formular die Notizen.

Wenn [Zoom](zoom.md) oder [Google Meet](google-meet.md) verbunden ist, werden die Notizen des Dienstes unter „Notizen“ und das Transkript unter „Transkript“ angezeigt. Sie sind mit **Von Zoom** oder **Von Google Meet** gekennzeichnet. Sie ersetzen nie Inhalte, die du hinzugefügt hast. Sind beide vorhanden, werden beide angezeigt.

Notizen können auch im Kalendereintrag des Meetings selbst hinzugefügt werden, nachdem es begonnen hat, oder per E-Mail von Zoom oder Gemini eingehen. Nach dem Meeting erstellt The Machine daraus nur dann Aufgaben, wenn es klare nächste Schritte gibt. Gehen dieselben Notizen auf zwei Wegen ein, wird nur eine Aufgabe erstellt, deren Quelle das Meeting ist: „Quelle: Notizen aus“ dem Meeting.

Bei einem Meeting mit Transkript, aber ohne Notizen, gibt es die Option **Notizen erstellen**. The Machine erstellt daraus Notizen: eine kurze Zusammenfassung, Entscheidungen und Aufgaben mit den jeweils zuständigen Personen, und zwar in der Sprache des Meetings.

The Machine zeigt **Notizen werden geschrieben…** an und arbeitet weiter, wenn du das Meeting schließt. Bei einem langen Meeting dauert es ein paar Minuten. Dafür wird dein eigenes Modell verwendet. Die Notizen sind mit **Verfasst von The Machine** gekennzeichnet und ersetzen nie Notizen, die du hinzugefügt hast.

The Machine kann sie auch hinzufügen. Bitte sie in einer Aufgabe darum, zum Beispiel mit „Füge dieses Transkript zum heutigen Board-Meeting hinzu“. Ein Transkript kommt unter „Transkript“, eine Zusammenfassung unter „Notizen“. Bei einem Meeting mit solchen Inhalten wird im Kalender **Notizen** oder **Transkript** angezeigt.

The Machine liest beides, um die nächsten Schritte für das Meeting zu erkennen. Sie werden wie das Meeting als Arbeit oder privat eingestuft und nur dann mit deinem Team geteilt, wenn das Meeting ebenfalls mit dem Team geteilt wird.

Ein Meeting lässt sich überall mit denselben Details öffnen: in einer Zeitleiste, in einer Nachrichtensuche oder als Quelle einer Aufgabe. Unter **Ursprüngliche Einladung** findest du unten die Einladung, so wie sie eingegangen ist.

## Termin hinzufügen oder ändern

Deinen eigenen Google-Kalender kannst du hier ändern. Outlook und andere Kalender werden nur angezeigt. Über **Neuer Termin** kannst du einen Termin hinzufügen. Auf dem Smartphone findest du die Option unter **+** in der oberen Leiste. Wähle den Kalender, einen Titel und die Uhrzeit aus. Klicke auf einen Termin ohne Gäste in diesem Kalender, um ihn zu ändern oder **Löschen** auszuwählen (zweimal tippen).

Unter **Wo** werden während der Eingabe Orte vorgeschlagen: zuerst Orte, die du schon verwendet hast, und deine Organisationen, danach Adressen von [OpenStreetMap](https://www.openstreetmap.org), einer kostenlosen Karte. Nur die Wörter, die du eingibst, werden zur Suche gesendet. Wähle einen Vorschlag aus oder behalte deinen eigenen Text.

Über **Einladen** kannst du Personen aus deinem Graph oder eine beliebige E-Mail-Adresse hinzufügen. Die Option gibt es nur in deinem eigenen Kalender. Über der Schaltfläche werden die eingeladenen Personen aufgelistet. Die Schaltfläche zeigt ihre Anzahl an: **Hinzufügen und 2 einladen**. Google versendet die Einladungen erst, wenn du darauf tippst. Ohne Gäste wird niemand eingeladen und niemand erhält eine Aktualisierung.

Eine Aufgabe kann auch eine Änderung vorschlagen, zum Beispiel einen Abholtermin, den du hinzufügen kannst. Es wird genau angezeigt, was sich ändert. Erst wenn du auf **Hinzufügen**, **Speichern** oder **Löschen** tippst, wird die Änderung vorgenommen.

Noch keine Meetings? Wenn du keinen Kalender verbunden hast, öffnet **Kalender verbinden** die Verbindungen. Verbinde [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) oder [einen anderen Kalender](other-calendars.md).

## Überschneidungen mit deinem anderen Kalender

Wenn sich ein Arbeitsmeeting mit einem Termin in deinem persönlichen Kalender überschneidet oder umgekehrt, erstellt The Machine eine Aufgabe zum neueren der beiden Termine. Sie kann einen kurzen Entwurf für eine Nachricht erstellen, mit der du um eine Verschiebung bittest, oder anbieten, den Termin abzusagen. Nichts wird versendet, bevor du es freigibst.

Ganztägige, freie und unverbindliche Termine zählen nie. Jede Überschneidung wird nur einmal angezeigt. Eine Arbeitsaufgabe weist nur auf einen Konflikt hin, damit dein Team den persönlichen Termin nie sieht. Nur du siehst, womit er sich überschneidet.

## Bereit für deine Meetings

Vor einem Meeting mit Personen außerhalb deines Unternehmens erstellt The Machine eine Aufgabe: **Vorbereitung für** das Meeting. Sie enthält eine kurze Übersicht:

- **Wer:** Wer die Personen sind, basierend auf deinem Graph.
- **Letzter Kontakt:** Dein letzter Austausch mit ihnen. Nach dem Meeting ist diese Nachricht die Quelle der Aufgabe.
- **Offene Versprechen:** Was du oder die anderen noch erledigen müssen.
- **Offene Fragen:** Was noch unbeantwortet ist.
- **Entscheiden oder mitbringen:** Was noch zu klären ist oder du mitbringen solltest.

Die Aufgabe erscheint am Morgen eines Arbeitstags: am Tag des Meetings, wenn es nachmittags stattfindet, andernfalls am vorherigen Arbeitstag. Dafür werden nur Informationen verwendet, die bereits auf deiner Machine sind. Die Aufgabe ist nur zum Lesen gedacht. Wenn du sie gelesen hast, markiere sie als **Erledigt**. Ein Versprechen oder eine Frage darin, um das oder die du dich kümmern musst, erhält eine eigene Aufgabe.

Gibt es keinen nützlichen Verlauf, wird keine Aufgabe erstellt. Für wiederkehrende, interne oder private Meetings und für abgesagte Meetings wird keine erstellt. Wird ein Meeting verschoben, bleibt es bei der einen Aufgabe, nun zum neuen Zeitpunkt. Eine verworfene Aufgabe erscheint nicht erneut. Die Aufgabe eines abgesagten Meetings wird automatisch geschlossen.

Die Details des Meetings zeigen die zugehörige Aufgabe unter **Aufgabe**. Tippe darauf, um direkt zu ihrem Chat zu gelangen.
