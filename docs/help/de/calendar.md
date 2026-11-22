---
title: Kalender
area: calendar
summary: Die kommende Woche auf einen Blick: Termine, fällige Aufgaben, zurückgestellte Aufgaben und Versprechen.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 24033419578a8c8f
---
## Was angezeigt wird

Deine Tage ab heute mit:

- Terminen aus den Kalendern, die du verbunden hast,
- Aufgaben, die an diesem Tag fällig sind, und zurückgestellten Aufgaben an dem Tag, an dem sie wieder anstehen,
- Nachfragen zu Arbeit, die du übergeben hast,
- Versprechen mit einem Datum,
- [Reisen und Veranstaltungen](calendar.md#trips-and-events) aus Buchungs- und Ticketmails.

Ein Termin in zwei Kalendern wird nur einmal angezeigt. Ein Kalender, den jemand mit dir geteilt hat, zeigt die Termine der Person ausgegraut und mit ihrem Vornamen an. Daraus entstehen nie Aufgaben. Ganztägige und mehrtägige Termine werden an jedem Tag, den sie umfassen, als ganztägig angezeigt. In der Agenda steht eine Reise an jedem ihrer Tage ganz oben. In der Wochen- und Monatsansicht wird sie als ein Balken über die betreffenden Tage angezeigt, zum Beispiel „Reise nach Lissabon“.

Ein gemeinsam erstellter Plan ist ein Versprechen, gekennzeichnet mit „Mit“ und dem Namen der anderen Person. Ein Versprechen zu einem Termin an diesem Tag mit derselben Person steht in der Zeile des Termins.

**Überfällig** steht ganz oben. Bei einem Termin mit einer offenen Aufgabe wird **Vorbereitung bereit**, **Wird vorbereitet** oder **Aufgabe** angezeigt. Eine Aufgabe, die erledigt zu sein scheint, weil du schon geantwortet hast oder der Durchlauf ergeben hat, dass sie erledigt ist, wird nicht als **Fällig** angezeigt.

## Agenda, Woche oder Monat

- **Agenda** zeigt die einzelnen Tage. Scrolle nach unten zu späteren Tagen oder nach oben beziehungsweise tippe auf **Frühere Tage anzeigen**, um frühere Tage aufzurufen. Die Ansicht reicht bis eine Woche vor dem Verbinden deines Kalenders zurück. Oben steht eine Zeile mit dem Startdatum. Sobald dein [Verlauf](history.md) geladen ist, reicht sie ungefähr ein Jahr zurück.
- **Woche** zeigt eine Übersicht von Montag bis Sonntag. Auf dem Handy werden drei Tage angezeigt.
- **Monat** zeigt den ganzen Monat. Auf dem Computer werden pro Tag bis zu drei Einträge angezeigt. Auf dem Handy erscheinen Punkte. Tippe auf einen Tag, um die Einträge dafür aufzurufen.

Mit **Heute**, ‹ und › oben wechselst du zwischen Wochen oder Monaten. Die ausgewählte Ansicht wird auf diesem Gerät gespeichert.

In der Wochenübersicht stehen Termine zur selben Uhrzeit nebeneinander, ohne dass sie unleserlich werden. Weitere Termine werden als **+N** angezeigt. Tippe darauf, um den Tag in der Agenda zu öffnen.

## Eintrag öffnen

Klicke auf eine Zeile, um den Chat zur Aufgabe, das Versprechen, die Reise oder Veranstaltung oder den Termin zu öffnen. Bei einem Termin, den du hier nicht ändern kannst, zum Beispiel einem Termin einer anderen Person oder einem Termin mit Gästen, werden die Details angezeigt: wann, wo und wer. Personen, die dein Graph kennt, sowie Organisationen und Projekte, die im Termin vorkommen, sind mit ihren Seiten verknüpft. Über **In Google Calendar öffnen** (oder **In Outlook öffnen**) darunter kannst du den Termin dort öffnen. Durch das Öffnen wird nichts geändert.

Ein für einen Termin gebuchter Besprechungsraum wird unter „Wo“ angezeigt, aber nie als Person oder in deinem Graph.

Ein Terminlink wird mit dem jeweiligen Dienst angezeigt, zum Beispiel Zoom, Google Meet oder Teams, oder als **Videoanruf**. Öffne den Termin, um teilzunehmen.

## Reisen und Veranstaltungen

Wenn eine Flug-, Hotel-, Ferienwohnungs-, Zug-, Bus-, Fähr-, Mietwagen-, Taxi- oder Flughafenparkplatzbuchung in deinem Postfach eingeht, fügt deine Machine sie einer Reise hinzu. Buchungen für dieselbe Reise werden zu einer Reise zusammengefasst, egal aus welchem deiner Postfächer sie stammen: der Zug zum Flughafen, die Flüge, das Auto, die Unterkunft und die Rückfahrt. Buchungen werden zusammengeführt, wenn sich ihre Tage überschneiden oder eine direkt an die andere anschließt.

Die Reise wird als ein Balken über ihre Tage angezeigt. Öffne sie, um alle Buchungen in zeitlicher Reihenfolge mit Uhrzeit, Adresse, Buchungscode und Sitzplatz zu sehen.

Tickets für ein Konzert, ein Spiel, ein Festival oder eine Konferenz werden jeweils zu einer Veranstaltung zusammengefasst. Angezeigt werden der Veranstaltungsort, der Buchungscode, der Sitzplatz und die Anzahl der Tickets. Eine zweite Bestellung für dieselbe Veranstaltung wird derselben Veranstaltung hinzugefügt. Eine Veranstaltung, die über dein geschäftliches Postfach gebucht wurde, ist „Arbeit“, andernfalls „Privat“. Tickets für etwas, das während einer Reise stattfindet, werden stattdessen der Reise hinzugefügt.

Bei einer bevorstehenden Reise zeigt deine Machine an, was noch fehlt, zum Beispiel **Für 2 Nächte keine Unterkunft gebucht** oder dass keine Fahrt vom Flughafen zum Hotel gebucht wurde. Diese Zeilen sind ausgegraut und mit **Keine Buchung** gekennzeichnet. Bei einer Reise ohne Unterkunft wird nichts zu Übernachtungen angezeigt.

- In jeder Zeile steht, von wem die Buchung stammt, zum Beispiel **Von Example Tickets**. Klicke darauf, um die Mail zu öffnen.
- Wenn aus der Mail eine Aufgabe entstanden ist, zum Beispiel die Tickets zu bezahlen, wird sie über **Aufgabe öffnen** angezeigt.
- Bei einer geänderten Buchung wird die Zeile aktualisiert. Eine stornierte Buchung wird entfernt. Wenn alle Buchungen storniert sind, wird auch die Reise oder Veranstaltung entfernt.
- Eine Buchung für jemand anderen, zum Beispiel der Flug einer Kollegin, der an dich weitergeleitet wurde, erscheint nicht bei deinen Reisen.

Die meisten Buchungsbestätigungen enthalten Details in einem Format, das deine Machine ohne KI auslesen kann. Bei anderen, zum Beispiel weitergeleiteten Mails oder Buchungen über eine kleine Buchungsseite, liest dein [Modell](model.md) die Mail im Hintergrund aus, einige auf einmal. Wenn du dich deinem Nutzungslimit näherst, wartet es. Buchungsmails aus dem Jahr deines [Verlaufs](history.md), das deine Machine speichert, werden im Hintergrund ausgelesen, sobald dieser Verlauf geladen ist.

## Notizen und Transkript zum Termin

Die Details eines Termins bestehen aus zwei Teilen. **Notizen** enthalten die Zusammenfassung: Entscheidungen und Aufgaben. Das **Transkript** enthält Wort für Wort, was gesagt wurde. Es ist zunächst eingeklappt und zeigt an, wie lange es dauert. Über **Anzeigen** kannst du es öffnen.

Wenn die Inhalte nicht geladen werden, wird es etwa eine halbe Minute lang automatisch erneut versucht. Tippe danach auf **Erneut versuchen**.

Für Notizen und Transkript gibt es jeweils **Notizen hinzufügen** oder **Transkript hinzufügen**, **Datei hochladen** für eine Markdown- oder Textdatei sowie **Bearbeiten** und **Entfernen** (zweimal tippen). Inhalte bleiben jeweils in ihrem Bereich. Bei einem Termin, den du ändern kannst, öffnet **Notizen** unter dem Formular die Notizen.

Wenn [Zoom](zoom.md), [Google Meet](google-meet.md) oder [Granola](granola.md) verbunden ist, werden die Notizen unter „Notizen“ und das Transkript unter „Transkript“ angezeigt. Sie sind mit **Von Zoom**, **Von Google Meet** oder **Von Granola** gekennzeichnet. Sie ersetzen nie Inhalte, die du hinzugefügt hast. Wenn beides vorhanden ist, wird beides angezeigt.

Notizen können auch im Kalendereintrag des Termins selbst, nach Beginn des Termins, oder per Mail von Zoom oder Gemini eingehen. Nach dem Ende des Termins erstellt The Machine daraus nur dann Aufgaben, wenn die nächsten Schritte eindeutig sind. Wenn dieselben Notizen auf zwei Wegen eingehen, entsteht nur eine Aufgabe. Als Quelle ist der Termin angegeben: „Quelle: Notizen aus“ dem Termin.

Bei einem Termin mit Transkript, aber ohne Notizen, wird **Notizen erstellen** angezeigt. The Machine erstellt sie anhand des Transkripts: eine kurze Zusammenfassung, Entscheidungen und Aufgaben mit den jeweils zuständigen Personen, und zwar in der Sprache des Termins.

Dabei wird **Notizen werden geschrieben…** angezeigt. The Machine arbeitet weiter, auch wenn du den Termin schließt. Bei einem langen Transkript dauert es mit deinem eigenen Modell ein paar Minuten. Die Notizen sind mit **Von The Machine geschrieben** gekennzeichnet und ersetzen nie Notizen, die du hinzugefügt hast.

The Machine kann Notizen auch hinzufügen. Bitte sie bei einer Aufgabe darum, zum Beispiel „Füge dieses Transkript zum heutigen Board-Meeting hinzu“. Ein Transkript wird unter „Transkript“ abgelegt, eine Zusammenfassung unter „Notizen“. Bei einem Termin mit Notizen oder Transkript wird im Kalender **Notizen** beziehungsweise **Transkript** angezeigt.

The Machine liest beides aus, um die nächsten Schritte zum Termin zu erfassen. Sie sind wie der Termin als „Arbeit“ oder „Privat“ gekennzeichnet und werden nur dann mit deinem Team geteilt, wenn auch der Termin geteilt wird.

Die Termindetails werden überall angezeigt, wo du den Termin findest: in einer Zeitleiste, in einer Nachrichtensuche oder als Quelle einer Aufgabe. Über **Ursprüngliche Einladung** unten wird die Einladung so angezeigt, wie sie eingegangen ist.

## Termin hinzufügen oder ändern

Deinen eigenen Google-Kalender kannst du hier ändern. Outlook und andere Kalender sind schreibgeschützt. Über **Neuer Termin** fügst du einen Termin hinzu (auf dem Handy unter **+** in der oberen Leiste). Wähle den Kalender, einen Titel und die Uhrzeit aus. Klicke auf einen Termin ohne Gäste in diesem Kalender, um ihn zu ändern oder über **Löschen** zu entfernen (zweimal tippen).

Unter **Wo** werden beim Tippen Orte vorgeschlagen: zuerst Orte, die du schon verwendet hast, und deine Organisationen, danach Adressen aus [OpenStreetMap](https://www.openstreetmap.org), einer kostenlosen Karte. Zur Suche werden nur die Wörter gesendet, die du eingibst. Wähle einen Vorschlag aus oder behalte deinen eigenen Text.

Über **Einladen** kannst du Personen aus deinem Graph oder eine beliebige E-Mail-Adresse hinzufügen. Diese Option gibt es nur in deinem eigenen Kalender. Über der Schaltfläche steht, wer eine Einladung erhält. Die Schaltfläche zeigt die Anzahl an: **Hinzufügen und 2 einladen**. Google versendet die Einladungen erst, wenn du darauf tippst. Ohne Gäste wird niemand eingeladen und niemand erhält eine Aktualisierung.

Eine Aufgabe kann ebenfalls eine Änderung vorschlagen, zum Beispiel einen Abholtermin, den du hinzufügen kannst. Es wird genau angezeigt, was geändert wird. Die Änderung wird nur durch **Hinzufügen**, **Speichern** oder **Löschen** vorgenommen.

Noch keine Termine? Wenn du keinen Kalender verbunden hast, öffnet **Kalender verbinden** die Verbindungen. Verbinde [Google Calendar](google-calendar.md), [Outlook-Kalender](microsoft.md) oder [einen anderen Kalender](other-calendars.md).

## Überschneidungen mit deinem anderen Kalender

Wenn sich ein geschäftlicher Termin mit etwas in deinem privaten Kalender überschneidet oder umgekehrt, erstellt The Machine eine Aufgabe zum neueren der beiden Termine. Sie kann einen kurzen Entwurf vorschlagen, um den Termin zu verschieben, oder anbieten, ihn abzusagen. Nichts wird versendet, bevor du es bestätigst.

Ganztägige, freie und vorläufige Termine werden nie berücksichtigt. Jede Überschneidung wird nur einmal angezeigt. Bei einer geschäftlichen Aufgabe wird nur angegeben, dass ein Konflikt vorliegt. Dein Team sieht den privaten Termin also nie. Nur du siehst, womit er sich überschneidet.

## Bereit für deine Termine

Vor einem Termin mit Personen von außerhalb deines Unternehmens erstellt The Machine eine Aufgabe: **Vorbereiten:** und der Name des Termins. Sie enthält eine kurze Übersicht:

- **Wer:** Wer die Personen sind, basierend auf deinem Graph, mit Informationen zu ihrem Hintergrund, sofern diese bekannt sind.
- **Organisation:** Was ihr Unternehmen macht und für den Termin wichtig ist.
- **Bisher:** Was ihr besprochen, angefragt und angeboten habt und wie der aktuelle Stand ist. Nach dem Termin sind diese Nachrichten die Quellen der Aufgabe.
- **Offene Versprechen:** Was du oder die anderen noch erledigen müsst.
- **Offene Fragen:** Was noch unbeantwortet ist.
- **Entscheiden oder mitbringen:** Was zu klären oder mitzubringen ist und was die anderen wahrscheinlich interessiert.

Die Aufgabe wird am Morgen eines Werktags erstellt: am Tag des Termins, wenn er nachmittags stattfindet, andernfalls am vorherigen Werktag. Sie dient nur zum Lesen. Markiere sie mit **Erledigt**, sobald du sie gelesen hast. Ein darin genanntes Versprechen oder eine Frage, zu der etwas getan werden muss, erhält eine eigene Aufgabe.

Die Übersicht basiert auf Informationen, die bereits auf deiner Machine vorhanden sind. Bei einem ersten Termin mit jemandem aus einem Unternehmen führt sie außerdem eine kurze Websuche nach dem Namen der Person und des Unternehmens durch und zeigt neben den Suchergebnissen einen Link an. Bei der Suche werden nur der öffentliche Name, der Unternehmensname und die Website der Person verwendet, nie deine Nachrichten. Suchergebnisse werden 30 Tage lang wiederverwendet. Wenn **Arbeitskontakte nachschlagen** deaktiviert ist (Einstellungen, Sicherheit), findet keine Suche statt.

Wenn kein nützlicher Verlauf vorhanden ist, wird keine Aufgabe erstellt. Für wiederkehrende, interne oder private Termine sowie für abgesagte Termine wird keine erstellt. Wird ein Termin verschoben, bleibt die Aufgabe erhalten und wird zur neuen Uhrzeit angezeigt. Eine verworfene Aufgabe wird nicht erneut angezeigt. Die Aufgabe zu einem abgesagten Termin wird automatisch geschlossen.

Wenn eine Aktualisierung den Inhalt einer Übersicht ändert, werden bestehende Übersichten für bevorstehende Termine einmal neu erstellt. Titel, Quellen und Position in deiner Liste bleiben gleich. Eine Übersicht, die du geändert, zurückgestellt oder geschlossen hast, bleibt unverändert. Das gilt auch für eine Übersicht zu einem Termin, der in den nächsten Minuten beginnt.

Die Aufgabe zum Termin wird in den Termindetails unter **Aufgabe** angezeigt. Tippe darauf, um direkt zu ihrem Chat zu gelangen.
