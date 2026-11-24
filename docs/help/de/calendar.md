---
title: Kalender
area: calendar
summary: Die kommende Woche auf einen Blick: Termine, fällige Aufgaben, zurückgestellte Aufgaben und Versprechen.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 9f38e3718f3e8639
---
## Was angezeigt wird

Deine Tage ab heute mit:

- Terminen aus den Kalendern, die du verbunden hast,
- an diesem Tag fälligen Aufgaben und zurückgestellten Aufgaben an dem Tag, an dem sie wieder angezeigt werden,
- Nachfragen zu übergebener Arbeit,
- Versprechen mit einem Datum,
- [Reisen und Veranstaltungen](calendar.md#trips-and-events) aus deinen Buchungs- und Ticketmails.

Ein Termin in zwei Kalendern wird nur einmal angezeigt. Ein Kalender, den jemand mit dir geteilt hat, zeigt die Termine der Person dezent mit ihrem Vornamen an. Daraus entstehen nie Aufgaben. Ganztägige und mehrtägige Termine werden an jedem Tag, den sie umfassen, als ganztägig angezeigt. In der Agenda steht eine Reise an jedem ihrer Tage ganz oben. In Woche und Monat wird sie als ein Balken über ihre Tage angezeigt, zum Beispiel „Reise nach Lissabon“.

Ein gemeinsamer Plan ist ein Versprechen, gekennzeichnet mit „Mit“ und dem Namen der anderen Person. Ein Versprechen zu einem Termin an diesem Tag mit derselben Person steht in der Zeile des Termins.

**Überfällig** steht ganz oben. Bei einem Termin mit einer offenen Aufgabe wird deren Status angezeigt: **Vorbereitung bereit**, **Wird vorbereitet** oder **Aufgabe**. Eine Aufgabe, die offenbar erledigt ist (du hast bereits geantwortet oder ihr Durchlauf hat ergeben, dass sie erledigt ist), wird nicht als **Fällig** angezeigt.

## Agenda, Woche oder Monat

- **Agenda** zeigt jeden Tag einzeln an. Scrolle nach unten zu späteren Tagen oder nach oben (oder wähle **Frühere Tage anzeigen**) zu früheren Tagen. Die Agenda reicht bis eine Woche vor dem Verbinden deines Kalenders zurück. Oben steht, ab welchem Tag sie beginnt. Sobald der [Verlauf](history.md) geladen ist, reicht sie etwa ein Jahr zurück.
- **Woche** zeigt eine Ansicht von Montag bis Sonntag. Auf dem Handy werden drei Tage angezeigt.
- **Monat** zeigt den ganzen Monat. Auf einem Computer werden bis zu drei Einträge pro Tag angezeigt. Auf dem Handy siehst du Punkte. Tippe auf einen Tag, um seine Einträge anzusehen.

Mit **Heute**, ‹ und › oben wechselst du zwischen Wochen oder Monaten. Deine Auswahl wird auf diesem Gerät gespeichert.

In der Wochenansicht stehen Termine zur selben Uhrzeit nebeneinander, sodass jeder lesbar bleibt. Weitere Termine werden als **+N** angezeigt. Tippe darauf, um den Tag in der Agenda zu öffnen.

## Etwas öffnen

Klicke auf eine Zeile, um den Chat zur Aufgabe, das Versprechen, die Reise oder Veranstaltung oder den Termin zu öffnen. Bei einem Termin, den du hier nicht ändern kannst, etwa weil er jemand anderem gehört oder Gäste hat, werden die Details angezeigt: wann, wo und wer. Personen, die dein Graph kennt, sowie die Organisationen und Projekte des Termins sind mit ihren Seiten verlinkt. **In Google Kalender öffnen** (oder **In Outlook öffnen**) darunter öffnet den Termin dort. Das Ansehen ändert nichts.

Ein für einen Termin gebuchter Besprechungsraum wird unter dem Ort angezeigt, nie als Person oder in deinem Graph.

Ein Link zu einem Termin wird mit dem jeweiligen Dienst angezeigt, etwa Zoom, Google Meet oder Teams, oder als **Videoanruf**. Öffne den Termin, um teilzunehmen.

## Reisen und Veranstaltungen

Wenn eine Flug-, Hotel-, Ferienhaus-, Zug-, Bus-, Fähr-, Mietwagen-, Taxi- oder Flughafenparkplatzbuchung in deinen Mails eingeht, fügt deine Machine sie einer Reise hinzu. Buchungen für dieselbe Reise werden zu einer Reise zusammengefasst, egal in welchem deiner Postfächer sie eingehen: der Zug zum Flughafen, die Flüge, das Auto, die Unterkunft und die Rückreise. Buchungen werden zusammengefügt, wenn sich ihre Tage überschneiden oder eine direkt auf die andere folgt.

Die Reise wird als ein Balken über ihre Tage angezeigt. Öffne sie, um die einzelnen Buchungen in zeitlicher Reihenfolge mit Uhrzeit, Adresse, Buchungscode und Sitzplatz zu sehen.

Tickets für ein Konzert, ein Spiel, ein Festival oder eine Konferenz ergeben eine Veranstaltung mit Ort, Buchungscode, Sitzplatz und Anzahl der Tickets. Eine zweite Bestellung für dieselbe Veranstaltung wird derselben Veranstaltung hinzugefügt. Eine Veranstaltung, die über dein Arbeitskonto gebucht wurde, ist geschäftlich, andernfalls privat. Tickets für etwas, das während einer Reise stattfindet, werden stattdessen der Reise hinzugefügt.

Bei einer bevorstehenden Reise zeigt deine Machine, was noch fehlt, zum Beispiel **Keine Unterkunft für 2 Nächte gebucht** oder dass keine Fahrt vom Flughafen zum Hotel gebucht ist. Diese Zeilen sind dezent dargestellt und mit **Keine Buchung** gekennzeichnet. Bei einer Reise ganz ohne Unterkunft werden keine Angaben zu Übernachtungen angezeigt.

- In jeder Zeile steht, von wem die Buchung stammt, zum Beispiel **Von Example Tickets**. Klicke darauf, um die Mail zu öffnen.
- Wenn aus der Mail eine Aufgabe entstanden ist, etwa die Tickets zu bezahlen, wird sie über **Aufgabe öffnen** angezeigt.
- Bei einer geänderten Buchung wird die Zeile aktualisiert. Eine stornierte Buchung wird entfernt. Wenn alle Buchungen storniert sind, wird auch die Reise oder Veranstaltung entfernt.
- Eine Buchung für jemand anderen, etwa der Flug einer Kollegin, den sie dir weitergeleitet hat, wird nicht zu deinen Reisen hinzugefügt.

Die meisten Bestätigungen enthalten Details in einem Format, das deine Machine ohne KI lesen kann. Bei Bestätigungen, die das nicht tun, etwa weitergeleiteten Mails oder von kleinen Buchungsseiten, liest dein [Modell](model.md) die Mail im Hintergrund, ein paar auf einmal. Wenn du dich deinem Nutzungslimit näherst, wartet es. Buchungsmails aus dem Jahr des [Verlaufs](history.md), den deine Machine speichert, werden im Hintergrund gelesen, sobald der Verlauf geladen ist.

## Besprechungsnotizen und Transkript

Die Details eines Termins bestehen aus zwei Teilen. **Notizen** sind die Zusammenfassung: Entscheidungen und Aufgaben. Das **Transkript** enthält Wort für Wort, was gesagt wurde. Es ist zunächst eingeklappt und zeigt an, wie lange es ist. Mit **Anzeigen** wird es geöffnet.

Wenn die Inhalte nicht geladen werden, versucht es etwa eine halbe Minute lang automatisch erneut. Tippe danach auf **Erneut versuchen**.

Für beide gibt es eigene Optionen zum **Notizen hinzufügen** und **Transkript hinzufügen**, außerdem **Datei hochladen** für Markdown- oder Textdateien sowie **Bearbeiten** und **Entfernen** (zweimal tippen). Was du einem Teil hinzufügst, bleibt dort. Bei einem Termin, den du ändern kannst, öffnet **Notizen** unter dem Formular die Notizen.

Wenn [Zoom](zoom.md), [Google Meet](google-meet.md) oder [Granola](granola.md) verbunden ist, werden dessen Notizen unter „Notizen“ und das Transkript unter „Transkript“ angezeigt, gekennzeichnet mit **Von Zoom**, **Von Google Meet** oder **Von Granola**. Sie ersetzen nie etwas, das du hinzugefügt hast. Wenn beides vorhanden ist, wird beides angezeigt.

Notizen können auch im Kalendereintrag des Termins selbst stehen, nachdem er begonnen hat, oder per Mail von Zoom oder Gemini eingehen. Nach dem Termin erstellt The Machine daraus nur bei klaren nächsten Schritten Aufgaben. Wenn dieselben Notizen auf zwei Wegen eingehen, entsteht eine Aufgabe mit dem Termin als Quelle: „Quelle: Notizen aus“ dem Termin.

Bei einem Termin mit Transkript, aber ohne Notizen, gibt es die Option **Notizen erstellen**. The Machine erstellt anhand des Transkripts eine kurze Zusammenfassung, Entscheidungen und Aufgaben samt Zuständigkeiten in der Sprache des Termins.

Dabei wird **Notizen werden geschrieben…** angezeigt. Der Vorgang läuft weiter, wenn du den Termin schließt. Bei einem langen Transkript dauert es ein paar Minuten und verwendet dein eigenes Modell. Die Notizen sind mit **Von The Machine geschrieben** gekennzeichnet und ersetzen nie Notizen, die du hinzugefügt hast.

The Machine kann die Notizen auch hinzufügen. Bitte sie in einer Aufgabe darum, zum Beispiel „Füge dieses Transkript dem heutigen Team-Meeting hinzu“. Ein Transkript wird unter „Transkript“ und eine Zusammenfassung unter „Notizen“ abgelegt. Bei einem Termin mit solchen Inhalten wird im Kalender **Notizen** oder **Transkript** angezeigt.

The Machine liest beides, um Nachfassaufgaben für den Termin zu finden. Sie sind geschäftlich oder privat, je nachdem, wie der Termin eingestuft ist, und werden nur dann mit deinem Team geteilt, wenn auch der Termin geteilt wird.

Ein Termin wird überall mit diesen Details geöffnet, egal wo du ihn findest: in einer Timeline, in einer Nachrichtensuche oder als Quelle einer Aufgabe. Über **Ursprüngliche Einladung** unten wird die Einladung so angezeigt, wie sie eingegangen ist.

## Termin hinzufügen oder ändern

Deinen eigenen Google-Kalender kannst du hier ändern. Outlook und andere Kalender lassen sich nur ansehen. Über **Neuer Termin** wird ein Termin hinzugefügt (auf dem Handy findest du die Option unter **+** in der oberen Leiste): Wähle den Kalender, einen Titel und eine Uhrzeit aus. Klicke auf einen Termin ohne Gäste in diesem Kalender, um ihn zu ändern oder über **Löschen** zu entfernen (zweimal tippen).

**Ort** schlägt beim Tippen Orte vor: zuerst Orte, die du schon verwendet hast, und deine Organisationen, dann Adressen von [OpenStreetMap](https://www.openstreetmap.org), einem kostenlosen Kartendienst. Zur Suche werden nur die Wörter gesendet, die du eingibst. Wähle einen Vorschlag aus oder behalte deinen eigenen Text.

Mit **Einladen** kannst du Personen aus deinem Graph oder beliebige E-Mail-Adressen hinzufügen. Die Option gibt es nur in deinem eigenen Kalender. Die eingeladenen Personen werden über der Schaltfläche aufgelistet. Die Schaltfläche zeigt ihre Anzahl an: **Hinzufügen und 2 einladen**. Google versendet die Einladungen erst, wenn du darauf tippst. Ohne Gäste wird niemand eingeladen oder über Änderungen benachrichtigt.

Eine Aufgabe kann ebenfalls eine Änderung vorschlagen, etwa eine Abholung, die du hinzufügen kannst. Es wird genau angezeigt, was sich ändert. Erst wenn du **Hinzufügen**, **Speichern** oder **Löschen** auswählst, wird die Änderung vorgenommen.

Noch keine Termine? Wenn du keinen Kalender verbunden hast, öffnet **Kalender verbinden** die Verbindungen. Verbinde [Google Calendar](google-calendar.md), [Outlook-Kalender](microsoft.md) oder [einen anderen Kalender](other-calendars.md).

## Konflikte mit deinem anderen Kalender

Wenn sich ein geschäftlicher Termin mit etwas in deinem privaten Kalender überschneidet oder umgekehrt, erstellt The Machine eine Aufgabe zum neueren der beiden Einträge. The Machine kann einen kurzen Text verfassen, um den Termin zu verschieben, oder vorschlagen, ihn abzusagen. Nichts wird gesendet, bevor du es bestätigst.

Ganztägige, freie und vorläufige Termine zählen nie. Jeder Konflikt wird nur einmal angezeigt. Eine geschäftliche Aufgabe weist nur auf einen Konflikt hin, damit dein Team den privaten Termin nie sieht. Nur du siehst, womit sich der Termin überschneidet.

## Bereit für deine Termine

Vor einem Termin mit Personen außerhalb deines Unternehmens erstellt The Machine eine Aufgabe: **Vorbereiten auf** den Termin. Sie enthält ein kurzes Briefing:

- **Wer:** Wer die Personen sind, basierend auf deinem Graph, mit Informationen zu ihrem Hintergrund, sofern vorhanden.
- **Organisation:** Was ihr Unternehmen macht, das für den Termin wichtig ist.
- **Bisher:** Was ihr besprochen, gefragt und angeboten habt und wo es steht. Diese Nachrichten sind nach dem Termin die Quellen der Aufgabe.
- **Offene Versprechen:** Was du oder die anderen noch erledigen müsst, basierend auf den Versprechen auf deiner Machine.
- **Offene Fragen:** Was noch unbeantwortet ist.
- **Entscheiden oder mitbringen:** Was geklärt oder mitgebracht werden muss und was den anderen wahrscheinlich wichtig ist.

Das Briefing erscheint am Morgen eines Arbeitstags: am Tag des Termins, wenn er nachmittags stattfindet, sonst am vorherigen Arbeitstag. Es ist nur zum Lesen da: Tippe auf **Erledigt**, wenn du es gelesen hast. Ein Versprechen oder eine Frage darin, um die du dich kümmern musst, erhält eine eigene Aufgabe.

Das Briefing basiert auf den Informationen, die bereits auf deiner Machine stehen. Bei einem ersten Termin mit einer Person in einem Unternehmen führt The Machine außerdem eine kurze Websuche nach dem Namen der Person und des Unternehmens durch. Neben den gefundenen Informationen wird ein Link angezeigt. Bei der Suche werden nur der öffentliche Name der Person, der Unternehmensname und die Website verwendet, nie deine Nachrichten. Ein Suchergebnis wird 30 Tage lang wiederverwendet. Wenn **Arbeitskontakte nachschlagen** deaktiviert ist (Einstellungen, Sicherheit), wird nicht gesucht.

Wenn es keinen nützlichen Verlauf gibt, wird keine Aufgabe erstellt. Wiederkehrende, interne, private und abgesagte Termine erhalten keine. Wird ein Termin verschoben, bleibt die eine Aufgabe bestehen und zeigt die neue Uhrzeit. Eine verworfene Aufgabe wird nicht erneut angezeigt. Die Aufgabe zu einem abgesagten Termin wird automatisch geschlossen.

Wenn eine Aktualisierung den Inhalt eines Briefings ändert, werden offene Briefings für bevorstehende Termine einmal neu erstellt. Titel, Quellen und Position in deiner Liste bleiben gleich. Ein von dir geändertes, zurückgestelltes oder geschlossenes Briefing bleibt unverändert. Dasselbe gilt für ein Briefing zu einem Termin, der in den nächsten Minuten beginnt.

Die Details des Termins zeigen die zugehörige Aufgabe unter **Aufgabe**, sodass du sie mit einem Tippen im Chat öffnen kannst.
