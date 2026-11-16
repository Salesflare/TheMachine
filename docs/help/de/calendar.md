---
title: Kalender
area: calendar
summary: Die kommende Woche auf einen Blick: Meetings, fällige Aufgaben, zurückgestellte Aufgaben und Versprechen.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 970b39054ae39543
---
## Was angezeigt wird

Deine Tage ab heute mit:

- Meetings aus den Kalendern, die du verbunden hast,
- an dem jeweiligen Tag fälligen Aufgaben und zurückgestellten Aufgaben an dem Tag, an dem sie wieder anstehen,
- Nachfragen zu übergebenen Aufgaben,
- Versprechen mit einem Datum,
- [Reisen und Veranstaltungen](calendar.md#trips-and-events) aus Buchungs- und Ticketmails.

Ein Meeting, das in zwei Kalendern steht, wird nur einmal angezeigt. Ein Kalender, den jemand mit dir geteilt hat, zeigt die Termine der Person ausgegraut und mit ihrem Vornamen an. Daraus entstehen nie Aufgaben. Ganztägige und mehrtägige Termine werden an jedem Tag, den sie umfassen, als ganztägig angezeigt. Eine Reise steht in der Agenda an jedem ihrer Tage ganz oben. In der Wochen- und Monatsansicht wird sie als durchgehender Balken angezeigt, zum Beispiel „Reise nach Lissabon“.

Ein gemeinsam gemachter Plan ist ein Versprechen, das mit „Mit“ und dem Namen der anderen Person gekennzeichnet ist. Ein Versprechen zu einem Meeting an diesem Tag mit derselben Person wird in der Zeile des Meetings angezeigt.

**Überfällig** steht ganz oben. Bei einem Meeting mit einer offenen Aufgabe wird deren Status angezeigt: **Vorbereitung bereit**, **Wird vorbereitet** oder **Aufgabe**. Eine Aufgabe, die erledigt zu sein scheint, weil du bereits geantwortet hast oder ihr Durchlauf sie als erledigt erkannt hat, wird nicht als **Fällig** angezeigt.

## Agenda, Woche oder Monat

- **Agenda** zeigt die einzelnen Tage. Scrolle nach unten zu späteren Tagen oder nach oben beziehungsweise tippe auf **Frühere Tage anzeigen**, um frühere Tage zu sehen. Die Ansicht reicht bis eine Woche vor dem Verbinden deines Kalenders zurück. Oben steht, ab welchem Tag sie beginnt. Sobald der [Verlauf](history.md) geladen ist, reicht sie etwa ein Jahr zurück.
- **Woche** zeigt ein Raster von Montag bis Sonntag. Auf dem Smartphone werden drei Tage angezeigt.
- **Monat** zeigt den ganzen Monat. Auf dem Computer werden bis zu drei Einträge pro Tag angezeigt. Auf dem Smartphone siehst du Punkte. Tippe auf einen Tag, um alle Einträge dafür zu sehen.

Mit **Heute**, ‹ und › oben wechselst du zwischen Wochen oder Monaten. Die ausgewählte Ansicht wird auf diesem Gerät gespeichert.

Im Wochenraster stehen Termine zur selben Zeit nebeneinander und bleiben lesbar. Die übrigen werden als **+N** angezeigt. Tippe darauf, um den Tag in der Agenda zu öffnen.

## Etwas öffnen

Klicke auf eine Zeile, um den Chat zur Aufgabe, das Versprechen, die Reise oder Veranstaltung oder das Meeting zu öffnen. Bei einem Meeting, das du hier nicht ändern kannst, zum Beispiel einem Meeting einer anderen Person oder einem Meeting mit Gästen, werden die Details angezeigt: wann, wo und wer. Personen, die dein Graph kennt, sowie Organisationen und Projekte, zu denen das Meeting gehört, sind mit ihrer jeweiligen Seite verlinkt. Über **In Google Calendar öffnen** oder **In Outlook öffnen** öffnest du das Meeting dort. Beim Ansehen wird nichts geändert.

Ein für ein Meeting gebuchter Raum wird unter „Wo“ angezeigt, aber nie als Person oder in deinem Graph.

Ein Meeting-Link wird mit dem jeweiligen Dienst angezeigt, zum Beispiel Zoom, Google Meet oder Teams, oder als **Videoanruf**. Öffne das Meeting, um teilzunehmen.

## Reisen und Veranstaltungen

Wenn eine Flug-, Hotel-, Zug-, Bus-, Fähr- oder Mietwagenbuchung in deiner Mail eingeht, fügt deine Machine sie einer Reise hinzu. Buchungen für dieselbe Reise werden zu einer Reise zusammengefasst: Hinfahrt, Hotel und Rückfahrt. Die Reise wird an ihren Tagen als durchgehender Balken angezeigt. Öffne sie, um Buchungscode, Sitzplatz und Ticket für jede Buchung in zeitlicher Reihenfolge zu sehen.

Tickets für ein Konzert, ein Spiel, ein Festival oder eine Konferenz ergeben jeweils eine Veranstaltung. Sie enthält den Veranstaltungsort, den Buchungscode, den Sitzplatz und die Anzahl der Tickets. Eine zweite Bestellung für dieselbe Veranstaltung wird derselben hinzugefügt. Eine Veranstaltung, die über dein geschäftliches Postfach gebucht wurde, ist geschäftlich, sonst privat.

- In jeder Zeile steht, von wem die Buchung stammt, zum Beispiel **Von Example Tickets**. Ein Klick öffnet die entsprechende Mail.
- Wenn aus der Mail eine Aufgabe entstanden ist, zum Beispiel die Tickets zu bezahlen, wird sie über **Aufgabe öffnen** angezeigt.
- Bei einer geänderten Buchung wird die Zeile aktualisiert. Eine stornierte Buchung wird entfernt. Wenn alle Buchungen storniert sind, wird auch die Reise oder Veranstaltung entfernt.

Deine Machine liest die Details aus, die Fluggesellschaften, Hotels, Buchungsseiten und Ticketanbieter in ihre Bestätigungsmails aufnehmen, ganz ohne KI. Eine Mail ohne solche Details wird ignoriert. Buchungsmails aus dem Jahr des [Verlaufs](history.md), den deine Machine speichert, werden im Hintergrund gelesen, sobald dieser Verlauf geladen ist.

## Meetingnotizen und Transkript

Die Details eines Meetings bestehen aus zwei Teilen. **Notizen** ist die Zusammenfassung mit Entscheidungen und Aufgaben. **Transkript** enthält Wort für Wort, was gesagt wurde. Es ist anfangs eingeklappt und zeigt die Dauer an. Über **Anzeigen** öffnest du es.

Wenn die Inhalte nicht geladen werden, versucht es deine Machine etwa eine halbe Minute lang automatisch erneut. Danach tippe auf **Erneut versuchen**.

Für Notizen und Transkript gibt es jeweils **Notizen hinzufügen** oder **Transkript hinzufügen**, **Datei hochladen** für eine Markdown- oder Textdatei sowie **Bearbeiten** und **Entfernen**. Tippe zum Entfernen zweimal. Inhalte bleiben jeweils in dem Bereich, in den du sie eingefügt hast. Bei einem Meeting, das du ändern kannst, öffnet **Notizen** unter dem Formular die Notizen.

Wenn [Zoom](zoom.md), [Google Meet](google-meet.md) oder [Granola](granola.md) verbunden ist, werden die Notizen unter „Notizen“ und das Transkript unter „Transkript“ angezeigt. Sie sind mit **Von Zoom**, **Von Google Meet** oder **Von Granola** gekennzeichnet. Sie ersetzen nie deine eigenen Inhalte: Wenn beides vorhanden ist, wird beides angezeigt.

Notizen können auch im Kalendereintrag des Meetings selbst enthalten sein, wenn sie nach Beginn des Meetings hinzugefügt wurden, oder per Mail von Zoom oder Gemini eingehen. Nach dem Meeting erstellt The Machine daraus nur dann Aufgaben, wenn die nächsten Schritte eindeutig sind. Wenn dieselben Notizen auf zwei Wegen eingehen, entsteht nur eine Aufgabe. Als Quelle wird das Meeting angegeben: „Quelle: Notizen aus“ dem Meeting.

Bei einem Meeting mit Transkript, aber ohne Notizen, wird **Notizen erstellen** angezeigt. The Machine erstellt anhand des Transkripts Notizen mit einer kurzen Zusammenfassung, Entscheidungen und Aufgaben samt Zuständigkeiten, und zwar in der Sprache des Meetings.

Dabei wird **Notizen werden geschrieben…** angezeigt. Der Vorgang läuft weiter, wenn du das Meeting schließt. Bei längeren Meetings dauert es mit deinem eigenen Modell ein paar Minuten. Die Notizen sind mit **Von The Machine verfasst** gekennzeichnet und ersetzen nie Notizen, die du hinzugefügt hast.

The Machine kann die Notizen auch selbst hinzufügen. Bitte sie in einer Aufgabe darum, zum Beispiel mit „Füge das Transkript zum heutigen Board-Meeting hinzu“. Ein Transkript wird unter „Transkript“ eingefügt, eine Zusammenfassung unter „Notizen“. Im Kalender wird bei einem Meeting mit solchen Inhalten **Notizen** oder **Transkript** angezeigt.

The Machine liest beides aus, um die nächsten Schritte zum Meeting zu erkennen. Sie sind wie das Meeting geschäftlich oder privat und werden nur dann mit deinem Team geteilt, wenn auch das Meeting geteilt wird.

Ein Meeting wird überall mit denselben Details geöffnet, egal, wo du es findest: in einer Zeitleiste, in einer Nachrichtensuche oder als Quelle einer Aufgabe. Unter **Ursprüngliche Einladung** findest du unten die Einladung, wie sie eingegangen ist.

## Termin hinzufügen oder ändern

Deinen eigenen Google-Kalender kannst du hier ändern. Outlook und andere Kalender lassen sich nur ansehen. Über **Neuer Termin** fügst du einen Termin hinzu. Auf dem Smartphone findest du die Option unter **+** in der oberen Leiste. Wähle den Kalender, einen Titel und die Uhrzeit aus. Klicke auf einen Termin ohne Gäste in diesem Kalender, um ihn zu ändern oder über **Löschen** zu löschen. Tippe zum Löschen zweimal.

Unter **Wo** werden während der Eingabe Orte vorgeschlagen: zuerst Orte, die du bereits verwendet hast, und deine Organisationen, dann Adressen von [OpenStreetMap](https://www.openstreetmap.org), einer kostenlosen Karte. Zur Suche werden nur die Wörter gesendet, die du eingibst. Wähle einen Vorschlag aus oder lass deinen eigenen Text stehen.

Über **Einladen** kannst du Personen aus deinem Graph oder eine beliebige E-Mail-Adresse hinzufügen. Die Option gibt es nur in deinem eigenen Kalender. Über dem Button siehst du, wer eine Einladung erhält. Auf dem Button steht die Anzahl der Personen, zum Beispiel **2 hinzufügen und einladen**. Google verschickt die Einladungen erst, wenn du darauf tippst. Ohne Gäste wird niemand eingeladen und niemand über Änderungen benachrichtigt.

Eine Aufgabe kann ebenfalls eine Änderung vorschlagen, zum Beispiel einen Abholtermin. Es wird genau angezeigt, was geändert wird. Erst wenn du auf **Hinzufügen**, **Speichern** oder **Löschen** tippst, wird die Änderung vorgenommen.

Noch keine Meetings? Wenn du keinen Kalender verbunden hast, öffnet **Kalender verbinden** die Verbindungen. Verbinde dort [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) oder [einen anderen Kalender](other-calendars.md).

## Überschneidungen mit deinem anderen Kalender

Wenn sich ein geschäftliches Meeting mit einem Termin in deinem privaten Kalender überschneidet oder umgekehrt, erstellt The Machine eine Aufgabe zum neueren der beiden Termine. Sie kann einen kurzen Nachrichtentwurf vorschlagen, um den Termin zu verschieben, oder anbieten, ihn abzusagen. Nichts wird gesendet, bevor du es bestätigst.

Ganztägige, freie und vorläufige Termine zählen nicht. Jede Überschneidung wird nur einmal angezeigt. Eine geschäftliche Aufgabe erwähnt nur den Konflikt, damit dein Team den privaten Termin nicht sieht. Nur du siehst, mit welchem Termin er sich überschneidet.

## Bereit für deine Meetings

Vor einem Meeting mit Personen von außerhalb deines Unternehmens erstellt The Machine eine Aufgabe: **Vorbereitung auf** das Meeting. Sie enthält eine kurze Übersicht:

- **Wer:** Wer die Personen sind, aus deinem Graph.
- **Letzter Kontakt:** Dein letzter Austausch mit ihnen. Nach dem Meeting ist diese Nachricht die Quelle der Aufgabe.
- **Offene Versprechen:** Was du oder die anderen Personen noch zu erledigen haben.
- **Offene Fragen:** Was noch unbeantwortet ist.
- **Entscheiden oder mitbringen:** Was noch zu klären ist oder mitgebracht werden muss.

Die Aufgabe erscheint am Morgen eines Arbeitstags: am Tag des Meetings, wenn es nachmittags stattfindet, sonst am vorherigen Arbeitstag. Sie verwendet nur Informationen, die bereits auf deiner Machine sind. Sie dient nur zum Lesen. Tippe auf **Erledigt**, wenn du sie gelesen hast. Ein Versprechen oder eine Frage, zu der etwas erledigt werden muss, hat eine eigene Aufgabe.

Ohne nützlichen Verlauf wird keine Aufgabe erstellt. Für wiederkehrende, interne oder private Meetings sowie für abgesagte Meetings wird keine erstellt. Wird ein Meeting verschoben, bleibt die Aufgabe erhalten und wird auf die neue Uhrzeit gesetzt. Eine verworfene Aufgabe kommt nicht wieder. Die Aufgabe zu einem abgesagten Meeting wird automatisch geschlossen.

Die Details des Meetings zeigen die zugehörige Aufgabe unter **Aufgabe**. Tippe darauf, um direkt zu ihrem Chat zu gelangen.
