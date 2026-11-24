---
title: Kalender
area: calendar
summary: Die kommende Woche auf einen Blick: Meetings, fällige Aufgaben, zurückgestellte Aufgaben und Versprechen.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: f3f41306aad03084
---
## Was angezeigt wird

Deine Tage ab heute, mit:

- Meetings aus den Kalendern, die du verbunden hast,
- Aufgaben, die an dem Tag fällig sind, und zurückgestellten Aufgaben an dem Tag, an dem sie wieder anstehen,
- Rückmeldungen zu übergebenen Aufgaben,
- datierten Versprechen,
- [Reisen und Veranstaltungen](calendar.md#trips-and-events) aus Buchungs- und Ticketmails.

Ein Meeting, das in zwei Kalendern steht, wird nur einmal angezeigt. Ein Kalender, den jemand mit dir geteilt hat, zeigt die Termine der anderen Person ausgegraut und mit ihrem Vornamen an. Daraus werden nie Aufgaben erstellt. Ganztägige und mehrtägige Termine werden an jedem ihrer Tage als ganztägig angezeigt. Eine Reise wird in der Agenda an jedem ihrer Tage zuerst angezeigt. In der Wochen- und Monatsansicht erscheint sie als durchgehender Balken über alle Reisetage, zum Beispiel „Reise nach Lissabon“.

Ein gemeinsamer Plan zählt als ein Versprechen und ist mit „Mit“ und dem Namen der anderen Person gekennzeichnet. Ein Versprechen zu einem Meeting an diesem Tag mit derselben Person steht in der Zeile des Meetings.

**Überfällig** wird zuerst angezeigt. Bei einem Meeting mit einer offenen Aufgabe siehst du den Status: **Vorbereitung bereit**, **Wird vorbereitet** oder **Aufgabe**. Eine Aufgabe, die erledigt zu sein scheint, weil du bereits geantwortet hast oder ihr Lauf sie als erledigt erkannt hat, wird nicht als **Fällig** angezeigt.

## Agenda, Woche oder Monat

- **Agenda** listet jeden Tag einzeln auf. Scrolle nach unten zu späteren Tagen oder nach oben zu früheren Tagen. Du kannst auch **Frühere Tage anzeigen** auswählen. Die Ansicht reicht bis zu einer Woche vor dem Zeitpunkt zurück, an dem du deinen Kalender verbunden hast. Oben steht, ab welchem Tag sie beginnt. Sobald der [Verlauf](history.md) geladen ist, reicht sie ungefähr ein Jahr zurück.
- **Woche** zeigt eine Rasteransicht von Montag bis Sonntag. Auf dem Handy werden drei Tage angezeigt.
- **Monat** zeigt den ganzen Monat. Auf einem Computer werden bis zu drei Einträge pro Tag angezeigt. Auf dem Handy siehst du Punkte. Tippe auf einen Tag, um seine Einträge aufzurufen.

Mit **Heute**, ‹ und › oben wechselst du zwischen Wochen oder Monaten. Die ausgewählte Ansicht wird auf diesem Gerät gespeichert.

In der Wochenansicht stehen Termine zur selben Zeit nebeneinander, solange sie lesbar bleiben. Die übrigen werden als **+N** angezeigt. Tippe darauf, um den Tag in der Agenda zu öffnen.

## Etwas öffnen

Klicke auf eine Zeile, um den Chat zur Aufgabe, das Versprechen, die Reise oder Veranstaltung oder das Meeting zu öffnen. Bei einem Meeting, das du hier nicht ändern kannst, etwa weil es jemand anderem gehört oder Gäste hat, werden die Details angezeigt: wann, wo und wer. Personen, die dein Graph kennt, sowie Organisationen und Projekte, zu denen das Meeting gehört, verlinken auf ihre jeweilige Seite. Über **In Google Kalender öffnen** oder **In Outlook öffnen** darunter öffnest du den Termin dort. Das Anzeigen ändert nichts.

Ein für ein Meeting gebuchter Raum wird unter „Wo“ angezeigt, nie als Person oder in deinem Graph.

Ein Meeting-Link wird mit dem Namen des jeweiligen Dienstes angezeigt, zum Beispiel Zoom, Google Meet oder Teams, oder als **Videoanruf**. Öffne das Meeting, um teilzunehmen.

## Reisen und Veranstaltungen

Wenn eine Flug-, Hotel-, Ferienhaus-, Zug-, Bus-, Fähr-, Mietwagen-, Taxi- oder Flughafenparkplatzbuchung in deinem Postfach eingeht, fügt deine Machine sie einer Reise hinzu. Buchungen für dieselbe Reise landen auf einer Reise, unabhängig davon, aus welchem deiner Postfächer sie stammen: der Zug zum Flughafen, die Flüge, das Auto, die Unterkunft und die Rückreise. Buchungen werden zusammengefasst, wenn sich ihre Tage überschneiden oder eine direkt an das Ende der anderen anschließt.

Die Reise wird als durchgehender Balken über ihre Tage angezeigt. Öffne sie, um alle Buchungen in zeitlicher Reihenfolge mit Uhrzeiten, Adresse, Buchungscode und Sitzplatz zu sehen.

Tickets für ein Konzert, ein Spiel, ein Festival oder eine Konferenz ergeben eine Veranstaltung pro Event. Angezeigt werden der Veranstaltungsort, der Buchungscode, der Sitzplatz und die Anzahl der Tickets. Eine zweite Bestellung für dieselbe Veranstaltung wird derselben Veranstaltung hinzugefügt. Tickets, die über dein geschäftliches Postfach gebucht wurden, sind geschäftlich, alle anderen privat. Tickets für etwas, das während einer Reise stattfindet, werden stattdessen der Reise hinzugefügt.

Bei einer bevorstehenden Reise weist deine Machine darauf hin, was noch fehlt, zum Beispiel **Keine Unterkunft für 2 Nächte gebucht** oder dass nichts für die Fahrt vom Flughafen zum Hotel gebucht wurde. Diese Hinweise sind ausgegraut und mit **Keine Buchung** gekennzeichnet. Bei einer Reise ohne Unterkünfte gibt es keine Hinweise zu Übernachtungen.

- In jeder Zeile steht, von wem die Buchung stammt, zum Beispiel **Von Example Tickets**. Wenn du darauf klickst, öffnet sich die entsprechende Mail.
- Wenn aus der Mail eine Aufgabe erstellt wurde, etwa die Tickets zu bezahlen, wird sie über **Aufgabe öffnen** angezeigt.
- Änderungen an einer Buchung werden in ihrer Zeile übernommen. Stornierte Buchungen werden entfernt. Wenn alle Buchungen storniert sind, wird auch die Reise oder Veranstaltung entfernt.
- Buchungen für andere Personen, etwa der Flug einer Kollegin, der an dich weitergeleitet wurde, erscheinen nicht bei deinen Reisen.

Die meisten Bestätigungen enthalten Details in einem Format, das deine Machine ohne KI lesen kann. Bei Bestätigungen in anderen Formaten, etwa weitergeleiteten Mails oder von kleinen Buchungsseiten, liest dein [Modell](model.md) die Mail im Hintergrund. Es bearbeitet jeweils nur einige Mails und wartet, wenn du dich deinem Nutzungslimit näherst. Buchungsmails aus dem Jahr des [Verlaufs](history.md), das deine Machine speichert, werden im Hintergrund gelesen, sobald dieser Verlauf geladen ist.

## Meeting-Notizen und Transkript

Die Details zu einem Meeting bestehen aus zwei Teilen. **Notizen** ist die Zusammenfassung mit Entscheidungen und Aufgaben. Das **Transkript** enthält Wort für Wort, was gesagt wurde. Es ist zunächst eingeklappt und zeigt an, wie lange es ist. Über **Anzeigen** öffnest du es.

Wenn die Inhalte nicht geladen werden, versucht es die App etwa eine halbe Minute lang automatisch erneut. Tippe danach auf **Erneut versuchen**.

Für Notizen und Transkript gibt es jeweils die Optionen **Notizen hinzufügen** oder **Transkript hinzufügen**, **Datei hochladen** für eine Markdown- oder Textdatei, **Bearbeiten** und **Entfernen**. Zum Entfernen musst du zweimal tippen. Was du zu einem Teil hinzufügst, bleibt dort. Bei einem Meeting, das du ändern kannst, öffnet **Notizen** unter dem Formular die Notizen.

Wenn [Zoom](zoom.md), [Google Meet](google-meet.md) oder [Granola](granola.md) verbunden ist, werden die Notizen unter „Notizen“ und das Transkript unter „Transkript“ angezeigt. Sie sind mit **Von Zoom**, **Von Google Meet** oder **Von Granola** gekennzeichnet. Sie ersetzen nie Inhalte, die du hinzugefügt hast. Wenn beides vorhanden ist, wird beides angezeigt.

Notizen können auch im Kalendereintrag des Meetings selbst, nachdem es begonnen hat, oder per Mail von Zoom oder Gemini eingehen. Nach dem Meeting erstellt The Machine daraus nur bei klaren nächsten Schritten Aufgaben. Werden dieselben Notizen auf zwei Wegen übermittelt, wird nur eine Aufgabe erstellt. Als Quelle ist das Meeting angegeben: „Quelle: Notizen aus“ dem Meeting.

Für ein Meeting mit Transkript, aber ohne Notizen, gibt es **Notizen erstellen**. The Machine erstellt sie anhand des Transkripts: eine kurze Zusammenfassung, Entscheidungen und Aufgaben samt zuständiger Person, und zwar in der Sprache des Meetings.

Die App zeigt **Notizen werden geschrieben…** an und arbeitet weiter, wenn du das Meeting schließt. Bei einem langen Meeting dauert es ein paar Minuten. Dafür wird dein eigenes Modell verwendet. Die Notizen sind mit **Verfasst von The Machine** gekennzeichnet und ersetzen nie Notizen, die du hinzugefügt hast.

The Machine kann auch selbst Notizen hinzufügen. Bitte sie in einer Aufgabe darum, zum Beispiel: „Füge das Transkript zur heutigen Vorstandssitzung hinzu.“ Ein Transkript wird unter „Transkript“ abgelegt, eine Zusammenfassung unter „Notizen“. Im Kalender ist bei einem Meeting mit Notizen oder Transkript **Notizen** oder **Transkript** angegeben.

The Machine liest beides, um Nachfassnachrichten zum Meeting zu erstellen. Sie sind wie das Meeting geschäftlich oder privat und werden nur dann mit deinem Team geteilt, wenn auch das Meeting mit dem Team geteilt wird.

Ein Meeting lässt sich überall mit denselben Details öffnen: in einer Zeitleiste, in einer Nachrichtensuche oder als Quelle einer Aufgabe. Über **Ursprüngliche Einladung** unten wird die Einladung so angezeigt, wie sie eingegangen ist.

## Veranstaltung hinzufügen oder ändern

Deinen eigenen Google-Kalender kannst du hier ändern. Outlook und andere Kalender lassen sich nur anzeigen. Über **Neuer Termin** fügst du einen Termin hinzu. Auf dem Handy findest du die Option unter **+** in der oberen Leiste. Wähle einen Kalender, einen Titel und eine Uhrzeit aus. Klicke auf einen Termin ohne Gäste in diesem Kalender, um ihn zu ändern oder über **Löschen** zu entfernen. Zum Löschen musst du zweimal tippen.

Unter „Wo“ werden während der Eingabe Orte vorgeschlagen: zuerst Orte, die du bereits verwendet hast, und deine Organisationen, dann Adressen von [OpenStreetMap](https://www.openstreetmap.org), einer kostenlosen Karte. Zur Suche werden nur die Wörter gesendet, die du eingibst. Wähle einen Vorschlag aus oder behalte deinen eigenen Text.

Über **Einladen** fügst du Personen aus deinem Graph oder eine beliebige E-Mail-Adresse hinzu. Diese Option gibt es nur für deinen eigenen Kalender. Wer eine Einladung erhält, wird über der Schaltfläche aufgelistet. Die Schaltfläche zeigt die Anzahl an: **Hinzufügen und 2 einladen**. Google verschickt die Einladungen erst, wenn du darauf tippst. Ohne Gäste wird niemand eingeladen oder über Änderungen informiert.

Eine Aufgabe kann ebenfalls eine Änderung vorschlagen, zum Beispiel eine Abholung, die hinzugefügt werden soll. Dabei wird genau angezeigt, was sich ändert. Erst wenn du **Hinzufügen**, **Speichern** oder **Löschen** auswählst, wird die Änderung vorgenommen.

Noch keine Meetings? Wenn kein Kalender verbunden ist, öffnet **Kalender verbinden** die Verbindungen. Verbinde dort [Google Calendar](google-calendar.md), [Outlook-Kalender](microsoft.md) oder [einen anderen Kalender](other-calendars.md).

## Überschneidungen mit deinem anderen Kalender

Wenn sich ein Arbeitsmeeting mit etwas in deinem privaten Kalender überschneidet oder umgekehrt, erstellt The Machine eine Aufgabe zur neueren der beiden Veranstaltungen. Sie kann eine kurze Nachricht zum Verschieben entwerfen oder vorschlagen, abzusagen. Nichts wird verschickt, bevor du es bestätigst.

Ganztägige, als frei markierte und vorläufige Termine werden nie berücksichtigt. Jede Überschneidung wird nur einmal angezeigt. Bei einer geschäftlichen Aufgabe steht nur, dass es einen Konflikt gibt. Dein Team sieht den privaten Termin also nie. Nur du siehst, womit er sich überschneidet.

## Gut vorbereitet auf deine Meetings

Vor einem Meeting mit Personen von außerhalb deines Unternehmens erstellt The Machine eine Aufgabe: **Vorbereitung für** das Meeting. Sie enthält eine kurze Übersicht:

- **Wer:** Wer die Personen sind, basierend auf deinem Graph, und, falls bekannt, Informationen zu ihrem Hintergrund.
- **Organisation:** Was ihr Unternehmen macht, für wen und zu welchem Preis, sofern das für das Meeting wichtig ist.
- **Bisher:** Was ihr besprochen, gefragt und angeboten habt und wo die Dinge stehen. Diese Nachrichten werden nach dem Meeting als Quellen der Aufgabe angezeigt.
- **Früher vereinbart:**, **Seitdem geändert:** und **Noch offen:** Was bei früheren Meetings mit denselben Personen herauskam. Zu jeder Zeile gehört das Meeting oder die Nachricht, aus der sie stammt.
- **Offene Versprechen:** Was du oder die anderen noch schulden, basierend auf den Versprechen auf deiner Machine.
- **Offene Fragen:** Was noch unbeantwortet ist.
- **Entscheiden oder mitbringen:** Was zu klären oder mitzubringen ist und was den anderen wahrscheinlich wichtig ist.

Die Übersicht erscheint am Morgen eines Arbeitstags: am Tag des Meetings, wenn es nachmittags stattfindet, andernfalls am vorherigen Arbeitstag. Sie ist nur zum Lesen gedacht. Wenn du sie gelesen hast, markiere sie als **Erledigt**. Ein Versprechen oder eine Frage darin, zu dem oder der noch etwas getan werden muss, erhält eine eigene Aufgabe.

Frühere Meetings werden berücksichtigt, wenn bei beiden eine Person von außerhalb dabei ist, unabhängig davon, wie das Meeting hieß und welche Adresse diese Person verwendet hat. The Machine liest die Notizen, die auf deiner Machine gespeichert sind: deine eigenen, die deiner Meeting-App oder Notizen, die dir per Mail geschickt wurden. Falls es keine Notizen gibt, liest sie das Transkript oder die Notizen im Kalendereintrag. Die neuesten Informationen zählen am meisten. Was später geklärt wurde, wird nicht mehr als offen angezeigt.

Auch Notizen und Nachrichten aus dem [Verlauf](history.md) werden berücksichtigt. So enthält die Übersicht auch Informationen zu Meetings von vor deinem Start.

Eine geschäftliche Übersicht greift nicht auf private Notizen oder Inhalte von der Machine einer anderen Person zu. Der Text bleibt bei dir: Bei einer Übergabe wird er nicht mitübergeben und kann nicht zur Überprüfung weitergegeben werden. Wenn es keine Notizen gibt, werden diese Zeilen nicht angezeigt.

Die Übersicht nutzt die Informationen, die bereits auf deiner Machine gespeichert sind. Bei einem ersten Meeting mit einer Person aus einem Unternehmen wird außerdem die Startseite der Unternehmenswebsite gelesen.

Wenn die Websuche auf deiner Machine eingerichtet ist, sucht The Machine außerdem kurz im Web nach dem Namen der Person und ihrem Unternehmen. Eine gehostete Machine enthält die Websuche nicht. Auf deinem eigenen Computer kannst du sie in OpenClaw einrichten. Die Suchergebnisse enthalten einen Link. An die Suche werden nur der öffentliche Name, der Unternehmensname und die Website übermittelt, nie deine Nachrichten. Die Suchergebnisse werden 30 Tage lang wiederverwendet.

So kann es für ein Meeting, das du zum ersten Mal zugesagt hast, schon vor eurem ersten Gespräch eine Übersicht geben: Was das Unternehmen macht, was das für dich bedeutet und, falls bekannt, wer die Person ist. Wenn nur der Vorname bekannt ist, werden Suchergebnisse nur übernommen, wenn sie eindeutig auf eine Person hinweisen. Wenn **Arbeitskontakte nachschlagen** deaktiviert ist (Einstellungen, Sicherheit), wird nichts nachgeschlagen.

Für wiederkehrende Meetings wird nur dann eine Übersicht erstellt, wenn seit dem letzten Mal etwas passiert ist: eine Nachricht, Notizen oder ein Versprechen. Die Übersicht fasst die neuen Informationen zusammen, nicht den Inhalt der letzten Übersicht. Sie erscheint, sobald die vorherige Zeitspanne vorbei ist. Pro Tag wird sie für höchstens zwei wiederkehrende Meetings erstellt.

Wenn es nichts Nützliches zu sagen gibt, wird keine Aufgabe erstellt. Für interne, private und abgesagte Meetings gibt es keine. Wird ein Meeting verschoben, bleibt die zugehörige Aufgabe bestehen und wird auf die neue Uhrzeit gesetzt. Eine verworfene Aufgabe wird nicht erneut angezeigt. Die Aufgabe zu einem abgesagten Meeting wird automatisch geschlossen.

Wenn eine Aktualisierung den Inhalt einer Übersicht verändert, werden offene Übersichten für bevorstehende Meetings einmal in der neuen Form verfasst. Titel, Quellen und Position in deiner Liste bleiben gleich. Eine von dir geänderte, zurückgestellte oder geschlossene Übersicht bleibt unverändert. Dasselbe gilt für eine Übersicht zu einem Meeting, das in den nächsten Minuten beginnt.

Die Details des Meetings zeigen die zugehörige Aufgabe unter **Aufgabe**. Tippe darauf, um direkt zu ihrem Chat zu gelangen.
