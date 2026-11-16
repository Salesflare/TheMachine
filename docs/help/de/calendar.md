---
title: Kalender
area: calendar
summary: Die kommende Woche an einem Ort: Besprechungen, fällige Aufgaben, zurückgestellte Aufgaben und Versprechen.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 93fe9794660b0ab2
---
## Was angezeigt wird

Deine Tage ab heute, mit:

- Besprechungen aus den Kalendern, die du verbunden hast,
- an diesem Tag fälligen Aufgaben und zurückgestellten Aufgaben an dem Tag, an dem sie wieder anstehen,
- Rückfragen zu Arbeit, die du weitergegeben hast,
- datierten Versprechen,
- [Reisen und Veranstaltungen](calendar.md#trips-and-events) aus Buchungs- und Ticket-Mails.

Eine Besprechung in zwei Kalendern wird nur einmal angezeigt. Ein Kalender, den jemand mit dir geteilt hat, zeigt die Termine der anderen Person ausgegraut und mit ihrem Vornamen an. Daraus werden nie Aufgaben erstellt. Ganztägige und mehrtägige Termine werden an jedem Tag, den sie abdecken, als ganztägig angezeigt. Eine Reise steht in der Agenda an jedem ihrer Tage ganz oben. In der Woche und im Monat erscheint sie als ein Balken über die betreffenden Tage, zum Beispiel „Reise nach Lissabon“.

Ein gemeinsam gemachtes Versprechen wird als ein Versprechen angezeigt, mit „Mit“ und dem Namen der anderen Person. Ein Versprechen zu einer Besprechung an diesem Tag mit derselben Person erscheint in der Zeile der Besprechung.

**Überfällig** steht ganz oben. Bei einer Besprechung mit einer offenen Aufgabe wird angezeigt, ob sie **Vorbereitung bereit**, **Wird vorbereitet** oder **Aufgabe** ist. Eine Aufgabe, die erledigt zu sein scheint, weil du bereits geantwortet hast oder ihr Durchlauf sie als erledigt erkannt hat, wird nicht als **Fällig** angezeigt.

## Agenda, Woche oder Monat

- **Agenda** listet die einzelnen Tage auf. Scrolle nach unten zu späteren Tagen oder nach oben beziehungsweise über **Frühere Tage anzeigen** zu früheren Tagen. Die Ansicht reicht bis eine Woche vor dem Verbinden deines Kalenders zurück. Oben steht, ab welchem Tag die Anzeige beginnt. Sobald der [Verlauf](history.md) geladen ist, reicht sie ungefähr ein Jahr zurück.
- **Woche** zeigt eine Rasteransicht von Montag bis Sonntag. Auf dem Smartphone werden drei Tage angezeigt.
- **Monat** zeigt den ganzen Monat. Auf einem Computer werden bis zu drei Einträge pro Tag angezeigt. Auf dem Smartphone werden Punkte angezeigt. Tippe auf einen Tag, um seine Einträge zu sehen.

Mit **Heute**, ‹ und › oben wechselst du zwischen den Wochen oder Monaten. Die ausgewählte Ansicht wird auf diesem Gerät gespeichert.

In der Wochenansicht stehen gleichzeitige Termine nebeneinander, damit sie lesbar bleiben. Die übrigen erscheinen als **+N**. Damit öffnest du diesen Tag in der Agenda.

## Etwas öffnen

Klicke auf eine Zeile, um den Chat zur Aufgabe, das Versprechen, die Reise oder Veranstaltung oder die Besprechung zu öffnen. Bei einer Besprechung, die du hier nicht ändern kannst, etwa weil sie jemand anderem gehört oder Gäste hat, werden die Details angezeigt: wann und wo sie stattfindet und wer dabei ist. Personen, die The Machine aus deinem Graph kennt, sowie die Organisationen und Projekte, zu denen die Besprechung gehört, sind mit ihrer jeweiligen Seite verlinkt. **In Google Calendar öffnen** oder **In Outlook öffnen** darunter öffnet die Besprechung im jeweiligen Kalender. Das Ansehen ändert nichts.

Ein für eine Besprechung gebuchter Raum wird unter „Wo“ angezeigt, aber nie als Person oder in deinem Graph.

Ein Besprechungslink wird mit dem jeweiligen Dienst angezeigt, zum Beispiel Zoom, Google Meet oder Teams, oder als **Videoanruf**. Öffne die Besprechung, um teilzunehmen.

## Reisen und Veranstaltungen

Wenn eine Flug-, Hotel-, Zug-, Bus-, Fähr- oder Mietwagenbuchung in deinen Mails eingeht, fügt deine Machine sie einer Reise hinzu. Buchungen für dieselbe Reise werden einer Reise zugeordnet: Hinreise, Hotel und Rückreise. Die Reise wird als ein Balken über ihre einzelnen Tage angezeigt. Öffne sie, um Buchungscode, Sitzplatz und Ticket jeder Buchung in zeitlicher Reihenfolge zu sehen.

Tickets für ein Konzert, ein Spiel, ein Festival oder eine Konferenz erstellen jeweils eine Veranstaltung mit Ort, Buchungscode, Sitzplatz und Anzahl der Tickets. Eine zweite Bestellung für dieselbe Veranstaltung wird derselben Veranstaltung hinzugefügt. Eine Veranstaltung, die über dein geschäftliches Postfach gebucht wurde, ist „Arbeit“, andernfalls „Privat“.

- Jede Zeile nennt, von wem die Buchung stammt, zum Beispiel **Von Example Tickets**, und öffnet die entsprechende Mail.
- Wenn aus der Mail eine Aufgabe erstellt wurde, etwa die Tickets zu bezahlen, wird sie über **Aufgabe öffnen** angezeigt.
- Bei einer geänderten Buchung wird die Zeile aktualisiert. Eine stornierte Buchung wird entfernt. Wenn alle Buchungen storniert sind, wird auch die Reise oder Veranstaltung entfernt.

Die Buchungsdetails werden ohne KI aus den Bestätigungsmails von Fluggesellschaften, Hotels, Buchungsseiten und Ticketanbietern gelesen. Eine Mail ohne solche Details erstellt nichts. Buchungsmails aus dem Jahr des [Verlaufs](history.md), den deine Machine speichert, werden im Hintergrund gelesen, sobald dieser Verlauf geladen ist.

## Besprechungsnotizen und Transkript

Die Details einer Besprechung bestehen aus zwei Teilen. **Notizen** sind die Zusammenfassung: Entscheidungen und Aufgaben. **Transkript** ist das wörtliche Protokoll des Gesagten. Es ist zunächst eingeklappt und zeigt an, wie lange es ist. Mit **Anzeigen** öffnest du es.

Wenn sie nicht geladen werden, versucht es die App etwa eine halbe Minute lang automatisch erneut. Danach tippe auf **Erneut versuchen**.

Für jeden Teil gibt es eigene Schaltflächen für **Notizen hinzufügen** oder **Transkript hinzufügen**, **Datei hochladen** für eine Markdown- oder Textdatei, **Bearbeiten** und **Entfernen** (zweimal tippen). Was du zu einem Teil hinzufügst, bleibt dort. Bei einer Besprechung, die du ändern kannst, öffnet **Notizen** unter dem Formular die Notizen.

Wenn [Zoom](zoom.md) oder [Google Meet](google-meet.md) verbunden ist, erscheinen die Notizen unter „Notizen“ und das Transkript unter „Transkript“. Sie sind mit **Von Zoom** oder **Von Google Meet** gekennzeichnet. Sie ersetzen nie deine eigenen Einträge. Wenn beide vorhanden sind, werden beide angezeigt.

Notizen können auch im Kalendereintrag der Besprechung selbst stehen, wenn sie nach Beginn hinzugefügt wurden, oder per Mail von Zoom oder Gemini eingehen. Nach Ende der Besprechung erstellt The Machine daraus nur dann Aufgaben, wenn klare nächste Schritte genannt werden. Gehen dieselben Notizen auf zwei Wegen ein, wird nur eine Aufgabe erstellt. Als Quelle ist die Besprechung angegeben: „Quelle: Notizen aus“ der Besprechung.

Bei einer Besprechung mit Transkript, aber ohne Notizen, wird **Notizen erstellen** angezeigt. The Machine erstellt anhand des Transkripts eine kurze Zusammenfassung, Entscheidungen und Aufgaben mit den jeweils verantwortlichen Personen, in der Sprache der Besprechung.

Die App zeigt **Notizen werden geschrieben…** an und arbeitet weiter, wenn du die Besprechung schließt. Bei einer langen Besprechung dauert es ein paar Minuten. Dafür wird dein eigenes Modell verwendet. Die Notizen sind mit „Von The Machine geschrieben“ gekennzeichnet und ersetzen nie deine eigenen Notizen.

The Machine kann Notizen auch selbst hinzufügen. Bitte sie in einer Aufgabe darum, zum Beispiel: „Füge das Transkript zur heutigen Vorstandssitzung hinzu.“ Ein Transkript wird unter „Transkript“, eine Zusammenfassung unter „Notizen“ hinzugefügt. Bei einer Besprechung mit Notizen oder Transkript wird im Kalender **Notizen** oder **Transkript** angezeigt.

The Machine liest beides, um die nächsten Schritte der Besprechung zu erkennen. Sie werden wie die Besprechung als „Arbeit“ oder „Privat“ eingestuft und nur dann mit deinem Team geteilt, wenn auch die Besprechung geteilt wird.

Eine Besprechung wird überall mit diesen Details geöffnet, egal, wo du sie findest: auf einer Zeitleiste, in einer Nachrichtensuche oder als Quelle einer Aufgabe. Über **Ursprüngliche Einladung** unten wird die Einladung so angezeigt, wie sie eingegangen ist.

## Termin hinzufügen oder ändern

Deinen eigenen Google-Kalender kannst du hier ändern. Outlook und andere Kalender lassen sich nur ansehen. Über **Neuer Termin** fügst du einen Termin hinzu. Auf dem Smartphone findest du die Schaltfläche unter **+** in der oberen Leiste. Wähle den Kalender, einen Titel und die Uhrzeit aus. Klicke auf einen Termin ohne Gäste in diesem Kalender, um ihn zu ändern oder über **Löschen** zu löschen (zweimal tippen).

**Wo** schlägt beim Tippen Orte vor: zuerst Orte, die du schon verwendet hast, und deine Organisationen, danach Adressen von [OpenStreetMap](https://www.openstreetmap.org), einer kostenlosen Karte. Zur Suche werden nur die Wörter gesendet, die du eingibst. Wähle einen Vorschlag aus oder gib eigenen Text ein.

Über **Einladen** fügst du Personen aus deinem Graph oder beliebige E-Mail-Adressen hinzu. Die Schaltfläche gibt es nur in deinem eigenen Kalender. Über ihr steht, wer eine Einladung bekommt. Die Schaltfläche nennt die Anzahl, zum Beispiel **Hinzufügen und 2 einladen**. Google verschickt die Einladungen erst, wenn du darauf tippst. Ohne Gäste wird niemand eingeladen und niemand erhält eine Aktualisierung.

Eine Aufgabe kann ebenfalls eine Änderung vorschlagen, zum Beispiel einen Abholtermin. Es wird genau angezeigt, was sich ändert. Erst wenn du auf **Hinzufügen**, **Speichern** oder **Löschen** tippst, wird die Änderung vorgenommen.

Noch keine Besprechungen? Wenn kein Kalender verbunden ist, öffnet **Kalender verbinden** die Verbindungen. Verbinde [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) oder [einen anderen Kalender](other-calendars.md).

## Überschneidungen mit deinem anderen Kalender

Wenn sich eine Besprechung bei der Arbeit mit etwas in deinem persönlichen Kalender überschneidet oder umgekehrt, erstellt The Machine eine Aufgabe zur neueren der beiden Veranstaltungen. Sie kann einen kurzen Entwurf für eine Nachricht zum Verschieben erstellen oder vorschlagen, die Einladung abzulehnen. Es wird nichts versendet, bevor du es bestätigst.

Ganztägige, als frei markierte und vorläufige Termine zählen nie. Jede Überschneidung wird nur einmal angezeigt. Eine Aufgabe für die Arbeit erwähnt nur, dass es einen Konflikt gibt. Dein Team sieht den persönlichen Termin also nie. Nur du siehst, womit er sich überschneidet.

## Bereit für deine Besprechungen

Vor einer Besprechung mit Personen außerhalb deines Unternehmens erstellt The Machine eine Aufgabe: **Vorbereitung für** die Besprechung. Sie enthält eine kurze Übersicht:

- **Wer:** Wer die Personen sind, laut deinem Graph.
- **Letzter Kontakt:** Euer letzter Austausch. Nach der Besprechung ist diese Nachricht die Quelle der Aufgabe.
- **Offene Versprechen:** Was du oder die anderen noch schuldig sind.
- **Offene Fragen:** Was noch unbeantwortet ist.
- **Entscheiden oder mitbringen:** Was noch geklärt werden muss oder mitzubringen ist.

Die Aufgabe erscheint am Morgen eines Werktags: am Tag der Besprechung, wenn sie am Nachmittag stattfindet, sonst am Werktag davor. Es werden nur Informationen verwendet, die bereits auf deiner Machine vorhanden sind. Die Aufgabe ist nur zum Lesen gedacht. Wenn du sie gelesen hast, markiere sie als **Erledigt**. Ein Versprechen oder eine Frage daraus, für das oder die etwas getan werden muss, erhält eine eigene Aufgabe.

Ohne nützlichen Verlauf wird keine Aufgabe erstellt. Für wiederkehrende, interne oder private Besprechungen sowie Besprechungen, die du abgelehnt hast, wird keine erstellt. Wird eine Besprechung verschoben, bleibt es bei derselben Aufgabe, die dann zur neuen Uhrzeit angezeigt wird. Eine verworfene Aufgabe erscheint nicht erneut. Wird die Besprechung abgesagt, wird die Aufgabe automatisch geschlossen.

Die Details der Besprechung zeigen die Aufgabe unter **Aufgabe**. Tippe darauf, um den zugehörigen Chat zu öffnen.
