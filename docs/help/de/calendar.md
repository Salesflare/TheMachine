---
title: Kalender
area: calendar
summary: Die kommende Woche auf einen Blick: Termine, fällige Aufgaben, zurückgestellte Aufgaben und Versprechen.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 479aa9c3fadda8bd
---
## Was angezeigt wird

Deine Tage ab heute, mit:

- Terminen aus den Kalendern, die du verbunden hast,
- an diesem Tag fälligen Aufgaben und zurückgestellten Aufgaben an dem Tag, an dem sie wieder anstehen,
- Nachfassnachrichten zu übergebenen Aufgaben,
- Versprechen mit Datum,
- [Reisen und Veranstaltungen](calendar.md#trips-and-events) aus Buchungs- und Ticketmails.

Ein Termin in zwei Kalendern wird nur einmal angezeigt. Ein Kalender, den jemand mit dir geteilt hat, zeigt die Termine der Person ausgegraut und mit ihrem Vornamen an. Daraus entstehen nie Aufgaben. Ganztägige und mehrtägige Termine werden an jedem betroffenen Tag als ganztägig angezeigt. Eine Reise steht in der Agenda an jedem ihrer Tage zuerst und wird in Woche und Monat als ein Balken über diese Tage angezeigt, zum Beispiel „Reise nach Lissabon“.

Ein gemeinsam gemachter Plan ist ein Versprechen, gekennzeichnet mit „Mit“ und dem Namen der anderen Person. Ein Versprechen zu einem Termin an diesem Tag mit derselben Person wird in der Zeile des Termins angezeigt.

**Überfällig** steht an erster Stelle. Bei einem Termin mit einer offenen Aufgabe wird angezeigt, ob sie **Vorbereitung bereit**, **Wird vorbereitet** oder **Aufgabe** ist. Eine Aufgabe, die erledigt zu sein scheint, weil du bereits geantwortet hast oder ihr Durchlauf ergeben hat, dass sie erledigt ist, wird nicht als **Fällig** angezeigt.

## Agenda, Woche oder Monat

- **Agenda** listet jeden Tag auf. Scrolle nach unten zu späteren Tagen oder nach oben beziehungsweise tippe auf **Frühere Tage anzeigen**, um frühere Tage zu sehen. Die Ansicht reicht bis eine Woche vor dem Verbinden deines Kalenders zurück. Oben steht, ab welchem Tag sie beginnt. Sobald der [Verlauf](history.md) geladen ist, reicht sie etwa ein Jahr zurück.
- **Woche** zeigt eine Übersicht von Montag bis Sonntag. Auf dem Handy werden drei Tage angezeigt.
- **Monat** zeigt den ganzen Monat. Auf einem Computer werden bis zu drei Einträge pro Tag angezeigt, auf dem Handy Punkte. Tippe auf einen Tag, um seine Einträge zu sehen.

Mit **Heute**, ‹ und › oben wechselst du zwischen Wochen oder Monaten. Die ausgewählte Ansicht wird auf diesem Gerät gespeichert.

In der Wochenansicht stehen Termine zur selben Zeit nebeneinander und bleiben dabei lesbar. Die übrigen werden als **+N** angezeigt. Tippe darauf, um den Tag in der Agenda zu öffnen.

## Etwas öffnen

Klicke auf eine Zeile, um den Chat der Aufgabe, das Versprechen, die Reise oder Veranstaltung oder den Termin zu öffnen. Bei einem Termin, den du hier nicht ändern kannst, etwa dem einer anderen Person oder einem Termin mit Gästen, werden die Details angezeigt: wann, wo und mit wem. Personen, die dein Graph kennt, sowie Organisationen und Projekte, zu denen der Termin gehört, führen zu ihrer jeweiligen Seite. **„In Google Kalender öffnen“** (oder **„In Outlook öffnen“**) darunter öffnet den Termin dort. Beim Ansehen wird nichts geändert.

Ein zu einem Termin gebuchter Besprechungsraum wird unter „Wo“ angezeigt, nie als Person oder in deinem Graph.

Ein Meeting-Link wird mit dem jeweiligen Dienst angezeigt, zum Beispiel Zoom, Google Meet oder Teams, oder als **Videoanruf**. Öffne den Termin, um teilzunehmen.

## Reisen und Veranstaltungen

Wenn eine Flug-, Hotel-, Ferienwohnungs-, Zug-, Bus-, Fähr-, Mietwagen-, Taxi- oder Flughafenparkplatzbuchung in deinem Postfach eingeht, fügt deine Machine sie einer Reise hinzu. Buchungen für dieselbe Reise werden in einer Reise zusammengefasst, aus allen deinen Postfächern: der Zug zum Flughafen, Flüge, Mietwagen, Unterkunft und Rückfahrt. Buchungen werden zusammengefasst, wenn sich ihre Tage überschneiden oder eine dort endet, wo die nächste beginnt.

Die Reise wird als ein Balken über ihre Tage angezeigt. Öffne sie, um alle Buchungen in zeitlicher Reihenfolge mit Uhrzeiten, Adresse, Buchungscode und Sitzplatz zu sehen.

Tickets für ein Konzert, ein Spiel, ein Festival oder eine Konferenz ergeben eine Veranstaltung pro Event. Angezeigt werden Ort, Buchungscode, Sitzplatz und Ticketanzahl. Eine weitere Buchung für dasselbe Event wird derselben Veranstaltung hinzugefügt. Eine Veranstaltung, die über dein geschäftliches Postfach gebucht wurde, ist geschäftlich, andernfalls privat. Tickets für etwas, das während einer Reise stattfindet, werden stattdessen der Reise hinzugefügt.

Bei einer bevorstehenden Reise zeigt deine Machine an, was noch fehlt, zum Beispiel **Keine Unterkunft für 2 Nächte gebucht** oder dass für die Fahrt vom Flughafen zum Hotel nichts gebucht ist. Diese Zeilen sind ausgegraut und mit **Keine Buchung** gekennzeichnet. Bei einer Reise ganz ohne Unterkunft werden keine Angaben zu Übernachtungen angezeigt.

- In jeder Zeile steht, woher die Buchung stammt, zum Beispiel **Von Example Tickets**. Öffne die Zeile, um die Mail anzusehen.
- Wenn aus der Mail eine Aufgabe entstanden ist, etwa die Tickets zu bezahlen, wird sie über **Aufgabe öffnen** angezeigt.
- Bei einer geänderten Buchung wird die Zeile aktualisiert, eine stornierte Buchung wird entfernt. Wenn alle Buchungen storniert sind, wird auch die Reise oder Veranstaltung entfernt.
- Buchungen für andere Personen, etwa der Flug einer Kollegin, den sie an dich weitergeleitet hat, werden nicht zu deinen Reisen hinzugefügt.

Die Details der meisten Bestätigungen liegen in einem Format vor, das deine Machine ohne KI auslesen kann. Bei Buchungen, bei denen das nicht möglich ist, etwa weitergeleiteten Mails oder kleinen Buchungsseiten, liest dein [Modell](model.md) die Mail im Hintergrund, einige auf einmal. Wenn du dich deinem Nutzungslimit näherst, wartet es. Buchungsmails aus dem Jahr des [Verlaufs](history.md), das deine Machine aufbewahrt, werden im Hintergrund gelesen, sobald der Verlauf geladen ist.

## Besprechungsnotizen und Transkript

Die Details eines Termins bestehen aus zwei Teilen. **Notizen** ist die Zusammenfassung mit Entscheidungen und Aufgaben. **Transkript** ist der Wortlaut des Gesprächs. Es ist zunächst eingeklappt und zeigt an, wie lange es ist. **Anzeigen** klappt es auf.

Wenn die Inhalte nicht geladen werden, versucht es etwa eine halbe Minute lang automatisch erneut. Danach tippst du auf **Erneut versuchen**.

Für beide gibt es jeweils **Notizen hinzufügen** oder **Transkript hinzufügen**, **Datei hochladen** für eine Markdown- oder Textdatei sowie **Bearbeiten** und **Entfernen** (zweimal tippen). Die Inhalte bleiben jeweils getrennt. Bei einem Termin, den du ändern kannst, öffnet **Notizen** unter dem Formular die Notizen.

Wenn [Zoom](zoom.md), [Google Meet](google-meet.md) oder [Granola](granola.md) verbunden ist, werden die Notizen unter „Notizen“ und das Transkript unter „Transkript“ angezeigt. Sie sind mit **Von Zoom**, **Von Google Meet** oder **Von Granola** gekennzeichnet. Sie ersetzen nie Inhalte, die du hinzugefügt hast. Wenn beides vorhanden ist, wird beides angezeigt.

Notizen können auch im Kalendereintrag des Termins selbst stehen, wenn sie nach Beginn hinzugefügt wurden, oder per Mail von Zoom oder Gemini eingehen. Nach dem Termin erstellt The Machine daraus nur dann Aufgaben, wenn sich daraus klare nächste Schritte ergeben. Wenn dieselben Notizen auf zwei Wegen eingehen, entsteht nur eine Aufgabe. Als Quelle wird der Termin angegeben: „Quelle: Notizen aus“ dem Termin.

Bei einem Termin mit Transkript, aber ohne Notizen, wird **Notizen erstellen** angezeigt. The Machine erstellt sie anhand des Transkripts: eine kurze Zusammenfassung, Entscheidungen und Aufgaben mit den jeweils zuständigen Personen, in der Sprache des Termins.

**Notizen werden geschrieben…** wird angezeigt, und der Vorgang läuft weiter, wenn du den Termin schließt. Bei einem langen Termin dauert es ein paar Minuten und es wird dein eigenes Modell verwendet. Die Notizen sind mit **Von The Machine geschrieben** gekennzeichnet und ersetzen nie Notizen, die du selbst hinzugefügt hast.

The Machine kann die Notizen auch selbst hinzufügen. Bitte sie in einem Chat zu einer Aufgabe darum, zum Beispiel: „Füge das Transkript zur heutigen Vorstandssitzung hinzu.“ Ein Transkript wird unter „Transkript“, eine Zusammenfassung unter „Notizen“ abgelegt. Bei einem Termin mit Notizen oder Transkript wird im Kalender **Notizen** beziehungsweise **Transkript** angezeigt.

The Machine liest beides aus, um Nachfassaufgaben zum Termin zu erstellen. Sie sind wie der Termin geschäftlich oder privat und werden nur dann mit deinem Team geteilt, wenn auch der Termin geteilt wird.

Ein Termin lässt sich überall mit denselben Details öffnen: in einer Zeitleiste, über die Nachrichtensuche oder als Quelle einer Aufgabe. Unter **Ursprüngliche Einladung** findest du unten die Einladung, wie sie eingegangen ist.

## Termin hinzufügen oder ändern

Dein eigener Google-Kalender lässt sich von hier aus ändern. Outlook und andere Kalender werden nur angezeigt. Mit **Neuer Termin** fügst du einen Termin hinzu (auf dem Handy über **+** in der oberen Leiste): Wähle den Kalender, einen Titel und die Uhrzeit aus. Klicke auf einen Termin ohne Gäste in diesem Kalender, um ihn zu ändern oder **Löschen** (zweimal tippen).

**Wo** schlägt während der Eingabe Orte vor: zuerst Orte, die du schon verwendet hast, und deine Organisationen, danach Adressen von [OpenStreetMap](https://www.openstreetmap.org), einem kostenlosen Kartendienst. Zur Suche werden nur die Wörter gesendet, die du eingibst. Wähle einen Vorschlag aus oder behalte deinen eigenen Text.

Mit **Einladen** fügst du Personen aus deinem Graph oder beliebige E-Mail-Adressen hinzu. Diese Option gibt es nur in deinem eigenen Kalender. Über der Schaltfläche steht, wer eine Einladung erhält. Die Schaltfläche zeigt die Anzahl an: **Hinzufügen und 2 einladen**. Google versendet die Einladungen erst, wenn du darauf tippst. Ohne Gäste wird niemand eingeladen oder benachrichtigt.

Eine Aufgabe kann ebenfalls eine Änderung vorschlagen, zum Beispiel eine Abholung, die du hinzufügen kannst. Es wird genau angezeigt, was sich ändert. Erst wenn du auf **Hinzufügen**, **Speichern** oder **Löschen** tippst, wird die Änderung vorgenommen.

Noch keine Termine? Wenn du keinen Kalender verbunden hast, öffnet **Kalender verbinden** die Verbindungen. Verbinde [Google Calendar](google-calendar.md), [Outlook-Kalender](microsoft.md) oder [einen anderen Kalender](other-calendars.md).

## Überschneidungen mit deinem anderen Kalender

Wenn sich ein geschäftlicher Termin mit etwas in deinem privaten Kalender überschneidet oder umgekehrt, erstellt The Machine eine Aufgabe zum späteren der beiden Termine. Sie kann eine kurze Nachricht zum Verschieben entwerfen oder vorschlagen, den Termin abzusagen. Nichts wird versendet, bevor du es bestätigst.

Überschneidet sich ein Termin mit mehreren anderen, wird eine Aufgabe zu diesem Termin erstellt. Solange sie offen ist, wird jede neue Überschneidung hinzugefügt. Sobald sie erledigt oder verworfen ist, wird sie nur durch einen später erstellten oder geänderten Termin erneut ausgelöst.

Ganztägige, freie und vorläufige Termine zählen nie. Jede Überschneidung wird nur einmal erfasst. Auch Arbeitsorte, Fokuszeiten und Abwesenheiten in Google zählen nicht. Ebenso wenig zählen eigene Zeitblöcke mit anderen Terminen, etwa ein Bürotageintrag. Nur die darin enthaltenen Termine können sich überschneiden. Ein Zeitblock ohne andere Personen und ohne darin enthaltene Termine, etwa ein Flug, kann sich weiterhin mit einem Termin mit anderen Personen überschneiden.

Eine geschäftliche Aufgabe sagt nur, dass es einen Konflikt gibt. Dein Team sieht den privaten Termin also nie. Nur du siehst, womit er sich überschneidet: zuerst die ersten beiden und danach die Anzahl weiterer. Eine Aufgabe, mit der du nichts gemacht hast, wird automatisch geschlossen, wenn ihre Überschneidung zu einer anderen Aufgabe gehört oder sich herausstellt, dass es gar keine Überschneidung gab.

## Vorbereitet für deine Termine

Vor einem Termin mit Personen außerhalb deines Unternehmens erstellt The Machine eine Aufgabe: **Vorbereiten auf** den Termin. Sie enthält ein kurzes Briefing:

- **Wer:** Wer die Personen sind, laut deinem Graph, und wenn bekannt, Informationen zu ihrem Hintergrund.
- **Organisation:** Was ihr Unternehmen tut, für wen und zu welchem Preis, sofern das für den Termin relevant ist.
- **Bisher:** Was ihr besprochen, gefragt und angeboten habt und wie der aktuelle Stand ist. Nach dem Termin werden diese Nachrichten als Quellen der Aufgabe aufgeführt.
- **Früher vereinbart:**, **Seitdem geändert:** und **Noch offen:** Ergebnisse früherer Termine mit denselben Personen. Jede Zeile verweist auf den Termin oder die Nachricht, aus der sie stammt.
- **Offene Versprechen:** Was du oder die anderen noch schuldig seid, basierend auf den Versprechen auf deiner Machine.
- **Offene Fragen:** Was noch unbeantwortet ist.
- **Entscheiden oder mitbringen:** Was geklärt oder mitgebracht werden sollte und was den anderen wahrscheinlich wichtig ist.

Das Briefing erscheint am Morgen eines Arbeitstags: am Tag des Termins, wenn er nachmittags stattfindet, andernfalls am vorherigen Arbeitstag. Es ist zum Lesen gedacht: Tippe auf **Erledigt**, sobald du es gelesen hast. Für Versprechen oder Fragen darin, die erledigt werden müssen, gibt es jeweils eine eigene Aufgabe.

Frag im Chat des Termins danach oder ergänze dein Wissen: The Machine beantwortet deine Fragen oder arbeitet deine Notiz in das Briefing ein, zum Beispiel unter **Entscheiden oder mitbringen**, und lernt daraus. Aus einem Briefing wird nichts versendet.

Frühere Termine werden berücksichtigt, wenn bei beiden eine Person von außerhalb dabei war, unabhängig davon, wie der Termin hieß oder welche Adresse sie verwendet hat. The Machine liest die Notizen, die auf deiner Machine verfügbar sind: deine eigenen, die deiner Meeting-App oder die Notizen, die dir per Mail geschickt wurden. Andernfalls liest sie das Transkript oder die Notizen aus dem Kalendereintrag. Neuere Notizen zählen stärker. Was später geklärt wurde, wird nicht mehr als offen angezeigt.

Notizen und Nachrichten aus dem [Verlauf](history.md) zählen ebenfalls. So kennt das Briefing auch Termine, die vor deinem Start stattgefunden haben.

Ein geschäftliches Briefing liest keine privaten Notizen und nichts von der Machine einer anderen Person. Der Inhalt bleibt bei dir: Bei einer Übergabe wird er nicht mitgegeben und er kann nicht zur Prüfung weitergegeben werden. Wenn es keine Notizen gibt, werden diese Zeilen nicht angezeigt.

Das Briefing verwendet, was bereits auf deiner Machine vorhanden ist. Bei einem ersten Termin mit einer Person aus einem Unternehmen wird auch die Startseite der Unternehmenswebsite gelesen.

Wenn die Websuche auf deiner Machine eingerichtet ist, wird außerdem kurz nach dem Namen der Person und ihrem Unternehmen im Web gesucht. Eine gehostete Machine wird ohne Websuche geliefert. Auf deinem eigenen Computer kannst du sie in OpenClaw einrichten. Die Suchergebnisse werden mit einem Link angezeigt. An die Suche werden nur der öffentliche Name, der Unternehmensname und die Website übermittelt, niemals deine Nachrichten. Die Ergebnisse werden 30 Tage lang wiederverwendet.

So kann für einen ersten Termin, den du zugesagt hast, schon vor eurem ersten Gespräch ein Briefing erstellt werden: mit Informationen dazu, was das Unternehmen tut, was das für dich bedeutet und, falls bekannt, wer die Person ist. Wenn nur ein Vorname bekannt ist, werden Suchergebnisse nur dann gespeichert, wenn sie eindeutig auf eine Person hinweisen. Wenn **Arbeitskontakte nachschlagen** ausgeschaltet ist (Einstellungen, Sicherheit), wird nichts nachgeschlagen.

Für einen wiederkehrenden Termin wird nur dann ein Briefing erstellt, wenn es seit dem letzten Termin etwas Neues gibt: eine Nachricht, Notizen oder ein Versprechen. Es zeigt, was neu ist, nicht den Inhalt des letzten Briefings. Es erscheint nach dem vorherigen Termin und höchstens für zwei wiederkehrende Termine pro Tag.

Wenn es nichts Nützliches zu sagen gibt, wird keine Aufgabe erstellt. Für interne, private und abgesagte Termine wird keine erstellt. Wird ein Termin verschoben, bleibt die zugehörige Aufgabe bestehen und wird zur neuen Uhrzeit angezeigt. Eine verworfene Aufgabe kommt nicht wieder. Die Aufgabe zu einem abgesagten Termin wird automatisch geschlossen.

Wenn eine Aktualisierung den Inhalt eines Briefings ändert, werden offene Briefings für noch bevorstehende Termine einmal in der neuen Form erstellt. Titel, Quellen und Position in deiner Liste bleiben gleich. Ein von dir geändertes, zurückgestelltes oder geschlossenes Briefing bleibt unverändert. Das gilt auch für Briefings zu Terminen, die in den nächsten Minuten beginnen.

In den Termindetails wird die Aufgabe unter **Aufgabe** angezeigt. Tippe darauf, um sie im Chat zu öffnen.
