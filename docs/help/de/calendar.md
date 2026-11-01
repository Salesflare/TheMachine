---
title: Kalender
area: calendar
summary: Die kommende Woche an einem Ort: Meetings, fällige Aufgaben, zurückgestellte Aufgaben und Versprechen.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py
order: 1
---
## Was er zeigt

Deine Tage ab heute, mit:

- Meetings aus den Kalendern, die du verbunden hast,
- Aufgaben, die an dem Tag fällig sind, und zurückgestellten Aufgaben an dem Tag, an dem sie zurückkommen,
- Nachfragen zu Arbeit, die du übergeben hast,
- Versprechen mit einem Datum.

Ein Meeting, das in zwei Kalendern steht, erscheint nur einmal. Ein Kalender, den jemand mit dir geteilt hat, zeigt die Termine dieser Person gedämpft, mit ihrem Vornamen. Daraus wird nie eine Aufgabe. Ganztägige und mehrtägige Termine erscheinen als ganztägig, an jedem Tag, den sie abdecken.

Ein gemeinsam gemachter Plan ist ein Versprechen, markiert mit „Mit“ und dem Namen der Person. Ein Versprechen zu einem Meeting am selben Tag mit derselben Person steht in der Zeile dieses Meetings.

**Überfällig** kommt zuerst. Ein Meeting mit einer offenen Aufgabe zeigt sie an: **Vorbereitung bereit**, **Wird vorbereitet** oder **Aufgabe**.

## Agenda, Woche oder Monat

- **Agenda** listet jeden Tag auf. Scroll nach unten für spätere Tage, nach oben (oder **Frühere Tage anzeigen**) für frühere.
- **Woche** zeigt ein Raster, Montag bis Sonntag. Auf dem Handy zeigt sie drei Tage.
- **Monat** zeigt den ganzen Monat. Ein Computer zeigt bis zu drei Einträge pro Tag; ein Handy zeigt Punkte, und ein Tippen listet diesen Tag auf.

**Heute**, ‹ und › oben blättern durch die Wochen oder Monate. Die gewählte Ansicht wird auf diesem Gerät gespeichert.

Im Wochenraster stehen Termine zur selben Zeit nebeneinander, solange jeder lesbar bleibt. Der Rest erscheint als **+N** und öffnet diesen Tag in der Agenda.

## Etwas öffnen

Klick auf eine Zeile, um den Chat der Aufgabe, das Versprechen oder das Meeting in seinem eigenen Kalender zu öffnen. Bei einem Meeting sind Personen, die dein Graph kennt, und die Organisationen und Projekte, um die es geht, Links zu ihrer Seite. Ansehen ändert nichts.

Ein gebuchter Besprechungsraum steht beim Ort, nie als Person oder in deinem Graph.

## Besprechungsnotizen und Transkript

Die Details eines Termins haben zwei Teile. **Notizen** ist die Zusammenfassung: Entscheidungen und Aufgaben. **Transkript** ist, was gesagt wurde, Wort für Wort. Es ist zuerst eingeklappt, mit seiner Länge; **Anzeigen** öffnet es.

Wenn sie nicht laden (etwa während deine Machine neu startet), versucht es die Besprechung etwa eine halbe Minute lang selbst erneut, und noch einmal, wenn du zum Fenster zurückkommst. Danach steht es dort, mit **Erneut versuchen**.

Jeder Teil hat sein eigenes **Notizen hinzufügen** oder **Transkript hinzufügen**, **Datei hochladen** für eine Markdown- oder Textdatei, **Bearbeiten** und **Entfernen** (zweimal tippen). Was in einem Teil steht, bleibt dort. Bei einem Termin, den du ändern kannst, öffnet **Notizen** unter seinem Formular sie.

Ist [Zoom](zoom.md) oder [Google Meet](google-meet.md) verbunden, stehen seine Notizen in Notizen und sein Transkript in Transkript, markiert mit **Von Zoom** oder **Von Google Meet**. Sie ersetzen nie, was du hinzugefügt hast: Gibt es beides, siehst du beides.

Ein Termin mit Transkript und ohne Notizen hat **Notizen erstellen**. The Machine schreibt sie dann aus dem Transkript: eine kurze Zusammenfassung, Entscheidungen und nächste Schritte mit dem, der sie übernimmt, in der Sprache des Termins.

The Machine zeigt **Notizen werden geschrieben…** und macht weiter, wenn du den Termin schließt; ein langer dauert ein paar Minuten. Sie nutzt dein eigenes Modell und wartet, wenn du dein Nutzungslimit erreichst. Bei den Notizen steht **Von The Machine geschrieben**. Sie ersetzen nie Notizen, die du hinzugefügt hast, und die Nachfassungen kommen daraus wie aus denen von Zoom.

The Machine kann sie auch hinzufügen. Frag sie bei einer Aufgabe, etwa "füge dieses Transkript zur heutigen Vorstandssitzung hinzu". Ein Transkript kommt in Transkript, eine Zusammenfassung in Notizen. Ein Termin damit zeigt **Notizen** oder **Transkript** im Kalender.

The Machine liest beides für die nächsten Schritte nach dem Termin. Sie sind Arbeit oder Privat wie der Termin und gehen nur an dein Team, wenn der Termin es tut.

Ein Termin öffnet sich überall mit diesen Details: in einem Verlauf, in einer Nachrichtensuche oder als Quelle einer Aufgabe. **Ursprüngliche Einladung** unten zeigt die Einladung, wie sie ankam.

## Termin hinzufügen oder ändern

Wenn sich ein Kalender von hier aus ändern lässt, fügt **Neuer Termin** einen hinzu (auf dem Handy unter **+** in der oberen Leiste): Wähle den Kalender, einen Titel und die Uhrzeit. Klick auf einen Termin ohne Gäste in diesem Kalender, um ihn zu ändern, oder **Löschen** (zweimal tippen).

**Wo** schlägt beim Tippen Orte vor: zuerst solche, die du schon benutzt hast, und deine Organisationen, dann Adressen aus [OpenStreetMap](https://www.openstreetmap.org) über Photon, eine kostenlose Kartensuche. Deine Machine fragt dort nur mit den Wörtern an, die du getippt hast. Wähle einen Ort oder behalte deinen eigenen Text.

**Einladen** fügt Personen aus deinem Graph hinzu, oder eine beliebige E-Mail-Adresse. Das gibt es nur in deinem eigenen Kalender. Wer eine Einladung bekommt, steht über dem Button, und der Button sagt, wie viele: **Hinzufügen und 2 einladen**. Google verschickt die Einladungen, wenn du darauf tippst, nicht vorher. Ohne Gäste wird niemand eingeladen oder benachrichtigt.

Auch eine Aufgabe kann eine Änderung vorschlagen, etwa eine Abholung, die eingetragen werden soll. Sie zeigt genau, was sich ändert, und erst dein **Hinzufügen**, **Speichern** oder **Löschen** führt es aus.

Noch keine Meetings? Ohne Kalender öffnet **Kalender verbinden** die Verbindungen: Verbinde [Google Calendar](google-calendar.md) oder [Outlook-Kalender](microsoft.md).
