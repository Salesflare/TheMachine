---
title: Kalender
area: calendar
summary: Die kommende Woche an einem Ort: Besprechungen, fällige Aufgaben, zurückgestellte Aufgaben und Versprechen.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: ae462ef9e7316cb6
---
## Was angezeigt wird

Deine Tage ab heute, mit:

- Besprechungen aus den Kalendern, die du verbunden hast,
- an diesem Tag fälligen Aufgaben und zurückgestellten Aufgaben an dem Tag, an dem sie wieder anstehen,
- Rückfragen zu übergebener Arbeit,
- Versprechen mit einem Datum,
- [Reisen und Veranstaltungen](calendar.md#trips-and-events) aus deinen Buchungs- und Ticketmails.

Eine Besprechung, die in zwei Kalendern steht, wird nur einmal angezeigt. Ein Kalender, den jemand mit dir geteilt hat, zeigt die Termine der Person dezent und mit ihrem Vornamen an. Daraus entstehen nie Aufgaben. Ganztägige und mehrtägige Termine werden an jedem betroffenen Tag als ganztägig angezeigt. Eine Reise erscheint in der Agenda an jedem ihrer Tage zuerst und in Woche und Monat als ein durchgehender Balken über alle Tage, zum Beispiel „Reise nach Lissabon“.

Ein gemeinsam gemachter Plan ist ein einzelnes Versprechen, gekennzeichnet mit „Mit“ und dem Namen der anderen Person. Ein Versprechen zu einer Besprechung an diesem Tag mit derselben Person steht in der Zeile der Besprechung.

**Überfällig** steht ganz oben. Bei einer Besprechung mit einer offenen Aufgabe wird angezeigt, ob sie **Vorbereitung bereit**, **Wird vorbereitet** oder **Aufgabe** ist. Eine Aufgabe, die erledigt aussieht (du hast bereits geantwortet oder ihr Durchlauf hat ergeben, dass sie erledigt ist), wird nicht als **Fällig** angezeigt.

## Agenda, Woche oder Monat

- **Agenda** zeigt jeden Tag einzeln. Scrolle nach unten zu späteren Tagen oder nach oben zu früheren Tagen. Mit **Frühere Tage anzeigen** kommst du ebenfalls zu früheren Tagen. Die Ansicht reicht bis eine Woche vor dem Tag zurück, an dem du deinen Kalender verbunden hast. Oben steht, ab welchem Tag sie beginnt. Sobald der [Verlauf](history.md) geladen ist, reicht sie etwa ein Jahr zurück.
- **Woche** zeigt eine Ansicht von Montag bis Sonntag. Auf dem Smartphone werden drei Tage angezeigt.
- **Monat** zeigt den ganzen Monat. Auf dem Computer werden bis zu drei Termine pro Tag angezeigt, auf dem Smartphone Punkte. Tippe auf einen Tag, um alle Termine zu sehen.

Mit **Heute**, ‹ und › oben wechselst du zwischen Wochen oder Monaten. Die ausgewählte Ansicht wird auf diesem Gerät gespeichert.

In der Wochenansicht stehen gleichzeitige Termine nebeneinander und bleiben lesbar. Weitere Termine werden als **+N** angezeigt. Tippe darauf, um den Tag in der Agenda zu öffnen.

## Etwas öffnen

Klicke auf eine Zeile, um den Chat der Aufgabe, das Versprechen, die Reise oder Veranstaltung oder die Besprechung zu öffnen. Bei einer Besprechung, die du hier nicht ändern kannst, etwa weil sie jemand anderem gehört oder Gäste hat, werden die Details angezeigt: wann und wo sie stattfindet und wer dabei ist. Personen, die The Machine aus dem Graph kennt, sowie Organisationen und Projekte, zu denen die Besprechung gehört, sind mit ihren jeweiligen Seiten verknüpft. Mit **In Google Calendar öffnen** (oder **In Outlook öffnen**) darunter öffnest du die Besprechung dort. Durch das Ansehen wird nichts geändert.

Ein Besprechungsraum, der für einen Termin gebucht wurde, wird unter „Wo“ angezeigt, aber nie als Person oder in deinem Graph.

Ein Besprechungslink wird mit dem jeweiligen Dienst angezeigt, zum Beispiel Zoom, Google Meet oder Teams, oder als **Videoanruf**. Öffne die Besprechung, um teilzunehmen.

## Reisen und Veranstaltungen

Wenn eine Flug-, Hotel-, Ferienhaus-, Zug-, Bus-, Fähr-, Mietwagen-, Taxi- oder Flughafenparkplatzbuchung in deinen Mails eingeht, fügt deine Machine sie einer Reise hinzu. Buchungen für dieselbe Reise werden zu einer Reise zusammengefasst, unabhängig davon, aus welchem deiner Postfächer sie stammen: die Zugfahrt zum Flughafen, die Flüge, das Auto, die Unterkunft und die Rückreise. Buchungen werden zusammengefasst, wenn sich ihre Tage überschneiden oder eine direkt an die andere anschließt.

Die Reise wird als ein durchgehender Balken über alle ihre Tage angezeigt. Öffne sie, um die einzelnen Buchungen in zeitlicher Reihenfolge mit Uhrzeiten, Adresse, Buchungscode und Sitzplatz zu sehen.

Tickets für ein Konzert, ein Spiel, ein Festival oder eine Konferenz ergeben jeweils eine Veranstaltung mit Ort, Buchungscode, Sitzplatz und Anzahl der Tickets. Eine weitere Bestellung für dieselbe Veranstaltung wird der bestehenden hinzugefügt. Wurde ein Ticket über dein Arbeitskonto gebucht, ist die Veranstaltung „Arbeit“, andernfalls „Privat“. Tickets für etwas, das während einer Reise stattfindet, werden stattdessen der Reise hinzugefügt.

Bei einer bevorstehenden Reise zeigt deine Machine an, was noch fehlt, zum Beispiel **Keine Unterkunft für 2 Nächte gebucht** oder dass keine Fahrt vom Flughafen zum Hotel gebucht ist. Diese Zeilen werden dezent angezeigt und mit **Keine Buchung** gekennzeichnet. Bei einer Reise ohne Unterkunft werden keine fehlenden Übernachtungen angezeigt.

- In jeder Zeile steht, von wem die Buchung stammt, zum Beispiel **Von Example Tickets**. Klicke darauf, um die Mail zu öffnen.
- Wenn aus der Mail eine Aufgabe entstanden ist, etwa die Tickets zu bezahlen, wird sie mit **Aufgabe öffnen** angezeigt.
- Eine geänderte Buchung aktualisiert ihre Zeile, eine stornierte Buchung wird entfernt. Wenn alle Buchungen storniert sind, wird auch die Reise oder Veranstaltung entfernt.
- Eine Buchung für jemand anderen, zum Beispiel den weitergeleiteten Flug eines Kollegen, wird nicht in deinen Reisen angezeigt.

Die meisten Bestätigungen enthalten ihre Details in einem Format, das deine Machine ohne KI lesen kann. Bei Bestätigungen, die das nicht tun, etwa weitergeleiteten Mails oder Mails von kleineren Buchungsseiten, liest dein [Modell](model.md) die Mail im Hintergrund. Es arbeitet einige Mails auf einmal ab und wartet, wenn du dich deinem Nutzungslimit näherst. Buchungsmails aus dem Jahr des [Verlaufs](history.md), den deine Machine speichert, werden im Hintergrund gelesen, sobald der Verlauf geladen ist.

## Notizen und Transkript zur Besprechung

Die Details einer Besprechung bestehen aus zwei Teilen. **Notizen** enthalten die Zusammenfassung: Entscheidungen und Aufgaben. **Transkript** enthält den Wortlaut der Besprechung. Es ist zunächst eingeklappt und zeigt die Dauer an. Mit **Anzeigen** wird es geöffnet.

Wenn die Inhalte nicht geladen werden, versucht es die App etwa eine halbe Minute lang automatisch erneut. Tippe danach auf **Erneut versuchen**.

Für beides gibt es **Notizen hinzufügen** oder **Transkript hinzufügen**, **Datei hochladen** für eine Markdown- oder Textdatei sowie **Bearbeiten** und **Entfernen** (zweimal tippen). Was du in einen Bereich einfügst, bleibt dort. Bei einer Besprechung, die du ändern kannst, öffnet **Notizen** unter dem Formular die Notizen.

Wenn [Zoom](zoom.md), [Google Meet](google-meet.md) oder [Granola](granola.md) verbunden ist, werden die Notizen unter „Notizen“ und das Transkript unter „Transkript“ angezeigt. Sie sind mit **Von Zoom**, **Von Google Meet** oder **Von Granola** gekennzeichnet. Sie ersetzen nie deine eigenen Inhalte: Wenn beides vorhanden ist, wird beides angezeigt.

Notizen können auch im Kalendereintrag der Besprechung selbst, nach deren Beginn, oder per Mail von Zoom oder Gemini eingehen. Nach der Besprechung erstellt The Machine daraus nur bei klaren nächsten Schritten Aufgaben. Kommen dieselben Notizen auf zwei Wegen an, entsteht eine einzige Aufgabe. Als Quelle wird die Besprechung angegeben: „Quelle: Notizen aus“ der Besprechung.

Bei einer Besprechung mit Transkript, aber ohne Notizen, wird **Notizen erstellen** angezeigt. The Machine erstellt anhand des Transkripts eine kurze Zusammenfassung mit Entscheidungen und Aufgaben samt zuständigen Personen, und zwar in der Sprache der Besprechung.

Die Anzeige **Notizen werden geschrieben…** erscheint. Der Vorgang läuft weiter, wenn du die Besprechung schließt. Bei einer langen Besprechung dauert es mit deinem eigenen Modell ein paar Minuten. Die Notizen sind mit **Von The Machine geschrieben** gekennzeichnet und ersetzen nie Notizen, die du selbst hinzugefügt hast.

The Machine kann Notizen auch für dich hinzufügen. Bitte sie in einer Aufgabe darum, zum Beispiel mit „Füge dieses Transkript zur heutigen Board-Besprechung hinzu“. Ein Transkript kommt unter „Transkript“, eine Zusammenfassung unter „Notizen“. Besprechungen mit solchen Inhalten sind im Kalender mit **Notizen** oder **Transkript** gekennzeichnet.

The Machine liest beides, um die nächsten Schritte aus der Besprechung zu finden. Sie werden wie die Besprechung als Arbeit oder privat gekennzeichnet und nur dann mit deinem Team geteilt, wenn die Besprechung ebenfalls geteilt wird.

Die Besprechung lässt sich überall mit denselben Details öffnen: in einer Zeitleiste, in einer Nachrichtensuche oder als Quelle einer Aufgabe. **Ursprüngliche Einladung** zeigt unten die Einladung, so wie sie eingegangen ist.

## Termin hinzufügen oder ändern

Deinen eigenen Google-Kalender kannst du hier ändern. Outlook und andere Kalender lassen sich nur ansehen. Mit **Neuer Termin** fügst du einen Termin hinzu (auf dem Smartphone über **+** in der oberen Leiste): Wähle den Kalender, einen Titel und die Uhrzeit aus. Klicke auf einen Termin ohne Gäste in diesem Kalender, um ihn zu ändern oder mit **Löschen** zu entfernen (zweimal tippen).

**Wo** schlägt beim Tippen Orte vor: zuerst Orte, die du bereits verwendet hast, und deine Organisationen, dann Adressen von [OpenStreetMap](https://www.openstreetmap.org), einem kostenlosen Kartendienst. Nur die Wörter, die du eintippst, werden zur Suche gesendet. Wähle einen Vorschlag aus oder behalte deinen eigenen Text.

Mit **Einladen** kannst du Personen aus deinem Graph oder beliebige E-Mail-Adressen hinzufügen. Diese Option gibt es nur in deinem eigenen Kalender. Über der Schaltfläche stehen die eingeladenen Personen, und die Schaltfläche zeigt ihre Anzahl an: **Hinzufügen und 2 einladen**. Google versendet die Einladungen erst, wenn du darauf tippst. Ohne Gäste wird niemand eingeladen oder über Änderungen benachrichtigt.

Eine Aufgabe kann ebenfalls eine Änderung vorschlagen, zum Beispiel einen Abholtermin. Es wird genau angezeigt, was sich ändert. Die Änderung wird erst übernommen, wenn du auf **Hinzufügen**, **Speichern** oder **Löschen** tippst.

Noch keine Besprechungen? Wenn du keinen Kalender verbunden hast, öffnet **Kalender verbinden** die Verbindungen. Verbinde [Google Kalender](google-calendar.md), [Outlook-Kalender](microsoft.md) oder [einen anderen Kalender](other-calendars.md).

## Überschneidungen mit deinem anderen Kalender

Wenn sich eine Besprechung bei der Arbeit mit einem Termin in deinem persönlichen Kalender überschneidet oder umgekehrt, erstellt The Machine eine Aufgabe zur jeweils neueren der beiden Veranstaltungen. Sie kann eine kurze Nachricht zum Verschieben entwerfen oder vorschlagen, die Einladung abzulehnen. Nichts wird versendet, bevor du es bestätigst.

Ganztägige, freie und vorläufige Termine werden nicht berücksichtigt. Jede Überschneidung wird nur einmal angezeigt. Eine Aufgabe für die Arbeit weist nur auf einen Konflikt hin, damit dein Team den persönlichen Termin nicht sieht. Nur du siehst, womit sich der Termin überschneidet.

## Bereit für deine Besprechungen

Vor einer Besprechung mit Personen außerhalb deines Unternehmens erstellt The Machine eine Aufgabe: **Vorbereiten auf** die Besprechung. Sie enthält eine kurze Übersicht:

- **Wer:** wer die Personen sind, basierend auf deinem Graph, und bei bekannten Informationen auch etwas zu ihrem Hintergrund.
- **Organisation:** was ihr Unternehmen macht und für die Besprechung relevant ist.
- **Bisher:** was ihr besprochen, gefragt und angeboten habt und wie der aktuelle Stand ist. Nach der Besprechung sind diese Nachrichten die Quellen der Aufgabe.
- **Offene Versprechen:** was du oder die anderen noch zu erledigen habt.
- **Offene Fragen:** was noch unbeantwortet ist.
- **Entscheiden oder mitbringen:** was noch geklärt oder mitgebracht werden muss und was den anderen wahrscheinlich wichtig ist.

Die Aufgabe erscheint morgens an einem Arbeitstag: am Tag der Besprechung, wenn sie nachmittags stattfindet, andernfalls am vorherigen Arbeitstag. Sie dient nur zum Lesen. Tippe auf **Erledigt**, wenn du sie gelesen hast. Ein Versprechen oder eine Frage, zu dem oder der etwas erledigt werden muss, erhält eine eigene Aufgabe.

Die Übersicht basiert auf Informationen, die bereits auf deiner Machine sind. Bei einer ersten Besprechung mit jemandem aus einem Unternehmen führt The Machine außerdem eine kurze Websuche zum Namen der Person und des Unternehmens durch. Neben den gefundenen Informationen wird ein Link angezeigt. An die Suche werden nur der öffentliche Name der Person, der Name des Unternehmens und dessen Website übermittelt, niemals deine Nachrichten. Suchergebnisse werden 30 Tage lang wiederverwendet. Wenn **Arbeitskontakte nachschlagen** deaktiviert ist (Einstellungen, Sicherheit), wird nicht gesucht.

Ohne nützliche Informationen aus der Vergangenheit wird keine Aufgabe erstellt. Für wiederkehrende, interne oder private Besprechungen sowie abgelehnte Einladungen wird keine Aufgabe erstellt. Wird eine Besprechung verschoben, bleibt ihre Aufgabe erhalten und wird zur neuen Uhrzeit angezeigt. Eine verworfene Aufgabe erscheint nicht erneut. Die Aufgabe zu einer abgesagten Besprechung wird automatisch geschlossen.

Die Aufgabe der Besprechung wird unter **Aufgabe** in den Details angezeigt. Tippe darauf, um direkt zum Chat zu gelangen.
