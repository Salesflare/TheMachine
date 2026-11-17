---
title: Kalender
area: calendar
summary: Die kommende Woche auf einen Blick: Besprechungen, fällige Aufgaben, zurückgestellte Aufgaben und Versprechen.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: c1941aa6ca09b134
---
## Was angezeigt wird

Deine Tage ab heute, mit:

- Besprechungen aus den Kalendern, die du verbunden hast,
- Aufgaben, die an diesem Tag fällig sind, und zurückgestellten Aufgaben an dem Tag, an dem sie wieder anstehen,
- Rückfragen zu Aufgaben, die du weitergegeben hast,
- Versprechen mit einem Datum,
- [Reisen und Veranstaltungen](calendar.md#trips-and-events) aus deinen Buchungs- und Ticket-E-Mails.

Eine Besprechung in zwei Kalendern wird nur einmal angezeigt. Ein Kalender, den jemand mit dir geteilt hat, zeigt die Termine der Person gedimmt und mit ihrem Vornamen an. Daraus entstehen keine Aufgaben. Ganztägige und mehrtägige Termine werden an jedem ihrer Tage als ganztägig angezeigt. In der Agenda steht eine Reise an jedem ihrer Tage ganz oben. In der Wochen- und Monatsansicht erstreckt sich ein Balken über alle Reisetage, zum Beispiel „Reise nach Lissabon“.

Ein gemeinsamer Plan zählt als ein Versprechen. Er ist mit „Mit“ und dem Namen der anderen Person gekennzeichnet. Ein Versprechen zu einer Besprechung an diesem Tag mit derselben Person erscheint in der Zeile der Besprechung.

**Überfällig** steht ganz oben. Bei einer Besprechung mit einer offenen Aufgabe wird der Status angezeigt: **Vorbereitung bereit**, **Wird vorbereitet** oder **Aufgabe**. Aufgaben, die erledigt zu sein scheinen, weil du bereits geantwortet hast oder ein Durchlauf sie als erledigt erkannt hat, werden nicht als **Fällig** angezeigt.

## Agenda, Woche oder Monat

- **Agenda** zeigt jeden Tag einzeln. Scrolle nach unten zu späteren Tagen oder nach oben zu früheren Tagen. Du kannst auch **Frühere Tage anzeigen** wählen. Die Ansicht reicht bis eine Woche vor dem Verbinden deines Kalenders zurück. Oben steht, ab welchem Tag sie beginnt. Sobald der [Verlauf](history.md) geladen ist, reicht sie etwa ein Jahr zurück.
- **Woche** zeigt eine Übersicht von Montag bis Sonntag. Auf dem Smartphone werden drei Tage angezeigt.
- **Monat** zeigt den ganzen Monat. Auf dem Computer werden bis zu drei Termine pro Tag angezeigt. Auf dem Smartphone erscheinen Punkte. Tippe auf einen Tag, um seine Termine zu sehen.

Mit **Heute**, ‹ und › oben wechselst du zwischen Wochen oder Monaten. Die ausgewählte Ansicht bleibt auf diesem Gerät gespeichert.

In der Wochenübersicht stehen Termine zur gleichen Zeit nebeneinander, aber bleiben lesbar. Weitere Termine werden als **+N** angezeigt. Tippe darauf, um den Tag in der Agenda zu öffnen.

## Etwas öffnen

Klicke auf eine Zeile, um den Chat zur Aufgabe, das Versprechen, die Reise oder Veranstaltung oder die Besprechung zu öffnen. Bei einer Besprechung, die du hier nicht ändern kannst, zum Beispiel der Besprechung einer anderen Person oder einer Besprechung mit Gästen, werden die Details angezeigt: wann und wo sie stattfindet und wer dabei ist. Personen, die dein Graph kennt, sowie die Organisationen und Projekte, zu denen die Besprechung gehört, sind mit ihren Seiten verlinkt. Über **In Google Kalender öffnen** (oder **In Outlook öffnen**) darunter öffnest du sie im jeweiligen Kalender. Durch das Ansehen wird nichts geändert.

Ein für eine Besprechung gebuchter Besprechungsraum wird unter „Wo“ angezeigt, aber nie als Person oder in deinem Graph.

Ein Besprechungslink wird mit dem Namen des Dienstes angezeigt, zum Beispiel Zoom, Google Meet oder Teams, oder als **Videoanruf**. Öffne die Besprechung, um teilzunehmen.

## Reisen und Veranstaltungen

Wenn die Bestätigung einer Flug-, Hotel-, Ferienhaus-, Zug-, Bus-, Fähr-, Mietwagen-, Taxi- oder Flughafenparkplatzbuchung in deinem Postfach eingeht, fügt deine Machine sie einer Reise hinzu. Buchungen für dieselbe Reise werden zu einer Reise zusammengefasst, auch wenn sie aus verschiedenen Postfächern stammen: die Zugfahrt zum Flughafen, die Flüge, das Auto, die Unterkunft und die Rückfahrt. Buchungen werden zusammengefasst, wenn sich ihre Tage überschneiden oder eine dort endet, wo die andere beginnt.

Die Reise wird als ein Balken über alle Reisetage angezeigt. Öffne ihn, um die einzelnen Buchungen in zeitlicher Reihenfolge mit Uhrzeit, Adresse, Buchungscode und Sitzplatz zu sehen.

Tickets für ein Konzert, ein Spiel, ein Festival oder eine Konferenz erstellen eine Veranstaltung. Für jede Veranstaltung gibt es einen Eintrag mit Veranstaltungsort, Buchungscode, Sitzplatz und Anzahl der Tickets. Eine zweite Bestellung für dieselbe Veranstaltung wird zum selben Eintrag hinzugefügt. Wurde ein Ticket über dein Arbeits-Postfach gebucht, ist die Veranstaltung als Arbeit gekennzeichnet, andernfalls als Privat. Tickets für etwas, das während einer Reise stattfindet, werden stattdessen der Reise hinzugefügt.

Bei einer bevorstehenden Reise weist deine Machine auf fehlende Buchungen hin, zum Beispiel **Keine Unterkunft für 2 Nächte gebucht** oder darauf, dass keine Fahrt vom Flughafen zum Hotel gebucht wurde. Diese Hinweise sind gedimmt und mit **Keine Buchung** gekennzeichnet. Bei einer Reise ohne Übernachtungen gibt es keine Hinweise zu Nächten.

- Jede Zeile nennt, von wem die Buchung stammt, zum Beispiel **Von Example Tickets**, und öffnet die zugehörige E-Mail.
- Wenn aus der E-Mail eine Aufgabe entstanden ist, etwa die Tickets zu bezahlen, wird sie über **Aufgabe öffnen** angezeigt.
- Bei einer geänderten Buchung wird die Zeile aktualisiert. Eine stornierte Buchung wird entfernt. Wenn alle Buchungen storniert sind, wird auch die Reise oder Veranstaltung entfernt.
- Eine Buchung für jemand anderen, zum Beispiel der Flug einer Kollegin, der an dich weitergeleitet wurde, erscheint nicht in deinen Reisen.

Die meisten Bestätigungen enthalten ihre Details in einem Format, das deine Machine ohne KI lesen kann. Bei Bestätigungen, die das nicht tun, zum Beispiel weitergeleiteten E-Mails oder von kleinen Buchungsseiten, liest dein [Modell](model.md) die E-Mails im Hintergrund, ein paar auf einmal. Wenn du dich deinem Nutzungslimit näherst, wartet es. Buchungs-E-Mails aus dem Jahr des [Verlaufs](history.md), den deine Machine speichert, werden im Hintergrund gelesen, sobald der Verlauf geladen ist.

## Notizen und Transkript zur Besprechung

Die Details einer Besprechung haben zwei Bereiche. **Notizen** enthalten die Zusammenfassung: Entscheidungen und Aufgaben. Das **Transkript** enthält wortwörtlich, was gesagt wurde. Es ist anfangs eingeklappt und zeigt an, wie lange es dauert. Über **Anzeigen** kannst du es öffnen.

Wenn die Inhalte nicht geladen werden, versucht es die App etwa eine halbe Minute lang automatisch erneut. Danach kannst du auf **Erneut versuchen** tippen.

Für Notizen und Transkript gibt es jeweils die Optionen **Notizen hinzufügen** oder **Transkript hinzufügen**, **Datei hochladen** für eine Markdown- oder Textdatei sowie **Bearbeiten** und **Entfernen** (zweimal tippen). Die Inhalte bleiben jeweils in ihrem Bereich. Bei einer Besprechung, die du ändern kannst, öffnet **Notizen** unter dem Formular die Notizen.

Wenn [Zoom](zoom.md), [Google Meet](google-meet.md) oder [Granola](granola.md) verbunden ist, werden die Notizen unter „Notizen“ und das Transkript unter „Transkript“ angezeigt. Sie sind mit **Von Zoom**, **Von Google Meet** oder **Von Granola** gekennzeichnet. Sie ersetzen nie Inhalte, die du selbst hinzugefügt hast. Wenn beides vorhanden ist, wird beides angezeigt.

Notizen können auch im Kalendereintrag der Besprechung selbst, nach Beginn der Besprechung hinzugefügt, oder per E-Mail von Zoom oder Gemini eingehen. Nach dem Ende der Besprechung erstellt The Machine daraus nur Aufgaben, die eindeutige nächste Schritte enthalten. Dieselben Notizen aus zwei Quellen führen zu einer Aufgabe, deren Quelle die Besprechung ist: „Quelle: Notizen aus“ der Besprechung.

Bei einer Besprechung mit Transkript, aber ohne Notizen, gibt es die Option **Notizen erstellen**. The Machine erstellt anhand des Transkripts eine kurze Zusammenfassung, Entscheidungen und Aufgaben mit den zuständigen Personen. Die Notizen werden in der Sprache der Besprechung verfasst.

Während die Notizen erstellt werden, wird **Notizen werden geschrieben…** angezeigt. Der Vorgang läuft weiter, wenn du die Besprechung schließt. Bei einer langen Besprechung dauert es mit deinem eigenen Modell ein paar Minuten. Die Notizen sind mit **Verfasst von The Machine** gekennzeichnet und ersetzen nie Notizen, die du selbst hinzugefügt hast.

The Machine kann auch selbst Notizen hinzufügen. Bitte sie in einer Aufgabe darum, zum Beispiel: „Füge dieses Transkript zur heutigen Board-Sitzung hinzu.“ Ein Transkript wird unter „Transkript“ eingefügt, eine Zusammenfassung unter „Notizen“. Bei einer Besprechung mit solchen Inhalten wird in der Agenda **Notizen** oder **Transkript** angezeigt.

The Machine liest beides, um Nachfassaufgaben für die Besprechung zu erstellen. Sie werden wie die Besprechung als Arbeit oder privat gekennzeichnet und nur dann mit deinem Team geteilt, wenn auch die Besprechung mit dem Team geteilt wird.

Die Besprechung lässt sich überall mit denselben Details öffnen: in einer Zeitleiste, in der Nachrichtensuche oder als Quelle einer Aufgabe. Über **Ursprüngliche Einladung** unten wird die Einladung so angezeigt, wie sie eingegangen ist.

## Einen Termin hinzufügen oder ändern

Deinen eigenen Google Kalender kannst du hier ändern. Outlook und andere Kalender lassen sich nur ansehen. Über **Neuer Termin** fügst du einen Termin hinzu (auf dem Smartphone über **+** in der oberen Leiste): Wähle den Kalender, einen Titel und die Uhrzeit aus. Klicke auf einen Termin in diesem Kalender, zu dem keine Gäste eingeladen sind, um ihn zu ändern oder über **Löschen** zu entfernen (zweimal tippen).

Unter **Wo** werden während der Eingabe Orte vorgeschlagen: zuerst Orte, die du bereits verwendet hast, und deine Organisationen, danach Adressen von [OpenStreetMap](https://www.openstreetmap.org), einer kostenlosen Karte. Nur die eingegebenen Wörter werden zur Suche gesendet. Wähle einen Vorschlag aus oder behalte deinen eigenen Text.

Über **Einladen** fügst du Personen aus deinem Graph oder eine beliebige E-Mail-Adresse hinzu. Die Option gibt es nur in deinem eigenen Kalender. Über dem Button werden die eingeladenen Personen aufgelistet. Der Button zeigt ihre Anzahl an: **Hinzufügen und 2 einladen**. Google verschickt die Einladungen erst, wenn du darauf tippst. Ohne Gäste wird niemand eingeladen und erhält keine Aktualisierung.

Eine Aufgabe kann auch eine Änderung vorschlagen, zum Beispiel einen Abholtermin, den du hinzufügen kannst. Es wird genau angezeigt, was geändert wird. Erst wenn du auf **Hinzufügen**, **Speichern** oder **Löschen** tippst, wird die Änderung vorgenommen.

Noch keine Besprechungen? Wenn du keinen Kalender verbunden hast, öffnet **Kalender verbinden** die Verbindungen. Dort kannst du [Google Kalender](google-calendar.md), [Outlook Kalender](microsoft.md) oder [einen anderen Kalender](other-calendars.md) verbinden.

## Konflikte mit deinem anderen Kalender

Wenn sich eine Arbeitsbesprechung mit etwas in deinem privaten Kalender überschneidet oder umgekehrt, erstellt The Machine eine Aufgabe zur späteren der beiden Veranstaltungen. Sie kann eine kurze Nachricht verfassen, um die Besprechung zu verschieben, oder anbieten, sie abzusagen. Erst nach deiner Bestätigung wird etwas verschickt.

Ganztägige, freie und vorläufige Termine werden nicht berücksichtigt. Jeder Konflikt wird nur einmal angezeigt. Eine Arbeitsaufgabe weist nur auf einen Konflikt hin, damit dein Team den privaten Termin nicht sieht. Nur du siehst, womit sich der Termin überschneidet.

## Gut vorbereitet in deine Besprechungen

Vor einer Besprechung mit Personen außerhalb deines Unternehmens erstellt The Machine eine Aufgabe: **Vorbereiten auf** die Besprechung. Sie enthält eine kurze Übersicht:

- **Wer:** Wer die Personen sind, laut deinem Graph.
- **Letzter Kontakt:** Dein letzter Austausch mit ihnen. Diese Nachricht wird nach der Besprechung als Quelle der Aufgabe angezeigt.
- **Offene Versprechen:** Was du oder die anderen Personen noch einlösen müssen.
- **Offene Fragen:** Was noch unbeantwortet ist.
- **Entscheiden oder mitbringen:** Was noch zu klären ist oder mitgebracht werden muss.

Die Aufgabe erscheint am Morgen eines Arbeitstags: am Tag der Besprechung, wenn sie nachmittags stattfindet, sonst am vorherigen Arbeitstag. Sie verwendet nur Informationen, die bereits auf deiner Machine vorhanden sind. Sie dient nur zum Lesen. Wenn du sie gelesen hast, markiere sie als **Erledigt**. Ein Versprechen oder eine Frage daraus, zu der etwas erledigt werden muss, erhält eine eigene Aufgabe.

Wenn es keinen hilfreichen Verlauf gibt, wird keine Aufgabe erstellt. Für wiederkehrende, interne und private Besprechungen sowie für abgesagte Besprechungen gibt es keine Aufgabe. Wird eine Besprechung verschoben, bleibt ihre Aufgabe erhalten und wird auf die neue Uhrzeit angepasst. Eine verworfene Aufgabe kommt nicht wieder. Die Aufgabe zu einer abgesagten Besprechung wird automatisch geschlossen.

Die Details der Besprechung zeigen die zugehörige Aufgabe unter **Aufgabe**. Tippe darauf, um den Chat zu öffnen.
