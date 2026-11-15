---
title: Kalender
area: calendar
summary: Die kommende Woche an einem Ort: Meetings, fällige Aufgaben, zurückgestellte Aufgaben und Versprechen.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py
order: 1
translated: 9da7909bce253806
---
## Was angezeigt wird

Deine Tage ab heute, mit:

- Meetings aus den Kalendern, die du verbunden hast,
- Aufgaben, die an dem jeweiligen Tag fällig sind, und zurückgestellte Aufgaben an dem Tag, an dem sie wieder anstehen,
- Rückfragen zu übergebener Arbeit,
- Versprechen mit einem Datum.

Ein Meeting, das in zwei Kalendern steht, wird nur einmal angezeigt. Ein Kalender, den jemand mit dir geteilt hat, zeigt die Termine dieser Person ausgegraut und mit ihrem Vornamen an. Daraus entstehen nie Aufgaben. Ganztägige und mehrtägige Termine werden an jedem Tag, den sie umfassen, als ganztägig angezeigt.

Ein gemeinsam gemachter Plan ist ein Versprechen, gekennzeichnet mit „Mit“ und dem Namen der anderen Person. Ein Versprechen zu einem Meeting an diesem Tag mit derselben Person steht in der Zeile des Meetings.

**Überfällig** steht ganz oben. Bei einem Meeting mit einer offenen Aufgabe wird diese angezeigt: **Vorbereitung bereit**, **Wird vorbereitet** oder **Aufgabe**. Eine Aufgabe, die erledigt zu sein scheint (du hast bereits geantwortet oder der Lauf hat ergeben, dass sie erledigt ist), wird nicht als **Fällig** angezeigt.

## Agenda, Woche oder Monat

- **Agenda** listet jeden Tag auf. Scrolle nach unten zu späteren Tagen oder nach oben (oder tippe auf **Frühere Tage anzeigen**), um frühere Tage zu sehen. Die Ansicht reicht bis eine Woche vor dem Verbinden deines Kalenders zurück. Oben steht eine Zeile mit dem Datum, ab dem die Ansicht beginnt. Sobald der [Verlauf](history.md) geladen ist, reicht sie etwa ein Jahr zurück.
- **Woche** zeigt ein Raster von Montag bis Sonntag. Auf dem Smartphone werden drei Tage angezeigt.
- **Monat** zeigt den ganzen Monat. Auf einem Computer werden bis zu drei Einträge pro Tag angezeigt. Auf dem Smartphone werden Punkte angezeigt. Tippe auf einen Tag, um die Einträge für diesen Tag aufzurufen.

Mit **Heute**, ‹ und › oben wechselst du zwischen den Wochen oder Monaten. Die von dir gewählte Ansicht wird auf diesem Gerät gespeichert.

Im Wochenraster stehen Termine zur selben Zeit nebeneinander, bleiben aber gut lesbar. Weitere Termine werden als **+N** angezeigt. Wenn du darauf tippst, öffnet sich dieser Tag in der Agenda.

## Etwas öffnen

Klicke auf eine Zeile, um den Chat zur Aufgabe, das Versprechen oder das Meeting zu öffnen. Bei einem Meeting, das du hier nicht ändern kannst, etwa weil es jemand anderem gehört oder Gäste hat, werden die Details angezeigt: wann, wo und wer. Personen, die dein Graph kennt, sowie die Organisationen und Projekte, zu denen das Meeting gehört, sind mit ihrer Seite verlinkt. Über **In Google Calendar öffnen** (oder **In Outlook öffnen**) darunter öffnest du den Termin dort. Das Anzeigen ändert nichts.

Ein für ein Meeting gebuchter Meetingraum wird unter „Wo“ angezeigt, aber nie als Person oder in deinem Graph.

Ein Meeting-Link wird mit dem zugehörigen Dienst angezeigt, zum Beispiel Zoom, Google Meet oder Teams, oder als **Videoanruf**. Öffne das Meeting, um teilzunehmen.

## Meetingnotizen und Transkript

Die Details eines Meetings bestehen aus zwei Teilen. **Notizen** ist die Zusammenfassung mit Entscheidungen und Aufgaben. Das **Transkript** enthält wortwörtlich, was gesagt wurde. Es ist zunächst eingeklappt und zeigt an, wie lang es ist. Mit **Anzeigen** öffnest du es.

Wenn die Inhalte nicht geladen werden, versucht es die App etwa eine halbe Minute lang automatisch erneut. Tippe danach auf **Erneut versuchen**.

Für jeden Teil gibt es ein eigenes **Notizen hinzufügen** oder **Transkript hinzufügen**, **Datei hochladen** für eine Markdown- oder Textdatei sowie **Bearbeiten** und **Entfernen** (zweimal tippen). Inhalte in einem Teil bleiben dort. Bei einem Meeting, das du ändern kannst, öffnest du sie über **Notizen** unter dem Formular.

Wenn [Zoom](zoom.md) oder [Google Meet](google-meet.md) verbunden ist, werden die Notizen unter „Notizen“ und das Transkript unter „Transkript“ angezeigt. Sie sind mit **Von Zoom** oder **Von Google Meet** gekennzeichnet. Sie ersetzen nie deine eigenen Inhalte: Wenn beides vorhanden ist, wird beides angezeigt.

Notizen können auch im Kalendereintrag des Meetings selbst stehen, nach Beginn des Meetings hinzugefügt oder per Mail von Zoom oder Gemini gesendet werden. Nach dem Meeting erstellt The Machine daraus nur dann Aufgaben, wenn die nächsten Schritte eindeutig sind. Werden dieselben Notizen auf zwei Wegen übermittelt, entsteht nur eine Aufgabe. Als Quelle wird das Meeting angegeben: „Quelle: Notizen aus“ dem Meeting.

Bei einem Meeting mit Transkript, aber ohne Notizen, gibt es **Notizen erstellen**. The Machine erstellt daraus anhand des Transkripts Notizen: eine kurze Zusammenfassung, Entscheidungen und Aufgaben mit den zuständigen Personen, in der Sprache des Meetings.

Dabei wird **Notizen werden geschrieben…** angezeigt. Der Vorgang läuft weiter, auch wenn du das Meeting schließt. Bei einem langen Meeting dauert es ein paar Minuten. Dafür wird dein eigenes Modell verwendet. Die Notizen sind mit **Geschrieben von The Machine** gekennzeichnet und ersetzen nie Notizen, die du selbst hinzugefügt hast.

The Machine kann sie auch hinzufügen. Bitte sie dazu in einer Aufgabe, zum Beispiel: „Füge dieses Transkript zum heutigen Board-Meeting hinzu.“ Ein Transkript kommt unter „Transkript“, eine Zusammenfassung unter „Notizen“. Bei einem Meeting mit Notizen oder Transkript steht im Kalender **Notizen** oder **Transkript**.

The Machine liest beides, um die Folgeaufgaben zum Meeting zu erstellen. Sie sind wie das Meeting entweder Arbeit oder privat und werden nur dann mit deinem Team geteilt, wenn auch das Meeting mit deinem Team geteilt wird.

Ein Meeting lässt sich überall mit denselben Details öffnen, egal, wo du es findest: auf einer Zeitleiste, in einer Nachrichtensuche oder als Quelle einer Aufgabe. Über **Ursprüngliche Einladung** unten wird die Einladung so angezeigt, wie sie eingegangen ist.

## Termin hinzufügen oder ändern

Deinen eigenen Google-Kalender kannst du hier ändern. Outlook und andere Kalender werden nur angezeigt. Mit **Neuer Termin** fügst du einen Termin hinzu (auf dem Smartphone über **+** in der oberen Leiste): Wähle den Kalender, einen Titel und die Uhrzeit aus. Klicke auf einen Termin ohne Gäste in diesem Kalender, um ihn zu ändern oder zu **Löschen** (zweimal tippen).

Unter **Wo** werden beim Tippen Orte vorgeschlagen: zuerst zuvor verwendete Orte und deine Organisationen, danach Adressen von [OpenStreetMap](https://www.openstreetmap.org), einem kostenlosen Kartendienst. Zur Suche werden nur die Wörter gesendet, die du eingibst. Wähle einen Vorschlag aus oder behalte deinen eigenen Text.

Über **Einladen** kannst du Personen aus deinem Graph oder eine beliebige E-Mail-Adresse hinzufügen. Diese Option gibt es nur in deinem eigenen Kalender. Über der Schaltfläche werden die eingeladenen Personen aufgelistet. Auf der Schaltfläche steht ihre Anzahl: **Hinzufügen und 2 einladen**. Google versendet die Einladungen, wenn du darauf tippst, nicht vorher. Ohne Gäste wird niemand eingeladen und niemand erhält eine Aktualisierung.

Eine Aufgabe kann auch eine Terminänderung vorschlagen, zum Beispiel einen Abholtermin. Es wird genau angezeigt, was sich ändert. Die Änderung wird erst vorgenommen, wenn du auf **Hinzufügen**, **Speichern** oder **Löschen** tippst.

Noch keine Meetings? Wenn du keinen Kalender verbunden hast, öffnet **Kalender verbinden** die Verbindungen. Verbinde dort [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) oder [einen anderen Kalender](other-calendars.md).

## Überschneidungen mit deinem anderen Kalender

Wenn sich ein Arbeitsmeeting mit einem Termin in deinem persönlichen Kalender überschneidet oder umgekehrt, erstellt The Machine eine Aufgabe zum neueren der beiden Termine. Sie kann einen kurzen Entwurf schreiben, um den Termin zu verschieben, oder anbieten, ihn abzusagen. Es wird nichts verschickt, bis du es bestätigst.

Ganztägige, freie und vorläufige Termine zählen nie. Jede Überschneidung wird nur einmal angezeigt. Eine Arbeitsaufgabe weist nur auf einen Konflikt hin, damit dein Team den privaten Termin nie sieht. Nur du siehst, womit sich der Termin überschneidet.

## Bereit für deine Meetings

Vor einem Meeting mit Personen von außerhalb deines Unternehmens erstellt The Machine eine Aufgabe: **Vorbereitung für** das Meeting. Sie enthält eine kurze Übersicht:

- **Wer:** Wer die Personen sind, laut deinem Graph.
- **Letzter Kontakt:** Dein letzter Austausch mit ihnen. Nach dem Meeting ist diese Nachricht die Quelle der Aufgabe.
- **Offene Versprechen:** Was du oder die anderen Personen noch schulden.
- **Offene Fragen:** Was noch unbeantwortet ist.
- **Entscheiden oder mitbringen:** Was zu klären oder mitzubringen ist.

Die Aufgabe erscheint am Morgen eines Arbeitstags: am Tag des Meetings, wenn es nachmittags stattfindet, andernfalls am vorherigen Arbeitstag. Sie verwendet nur Informationen, die bereits auf deiner Machine vorhanden sind. Sie dient nur zum Lesen. Tippe auf **Erledigt**, wenn du sie gelesen hast. Ein Versprechen oder eine Frage darin, für das oder die etwas zu tun ist, hat eine eigene Aufgabe.

Gibt es keinen nützlichen Verlauf, wird keine Aufgabe erstellt. Für wiederkehrende, interne, private und abgesagte Meetings wird keine erstellt. Wird ein Meeting verschoben, bleibt die Aufgabe erhalten und wird auf die neue Uhrzeit gesetzt. Eine verworfene Aufgabe erscheint nicht erneut. Die Aufgabe zu einem abgesagten Meeting wird automatisch geschlossen.

In den Details des Meetings wird die Aufgabe unter **Aufgabe** angezeigt. Von dort öffnest du ihren Chat mit einem Tippen.
