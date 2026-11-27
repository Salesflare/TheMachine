---
title: Kalender
area: calendar
summary: Die Woche im Blick: Meetings, fällige Aufgaben, zurückgestellte Aufgaben und Versprechen.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 4b5bc600fefb624c
---
## Was angezeigt wird

Deine Tage ab heute mit:

- Meetings aus den Kalendern, die du verbunden hast,
- Aufgaben, die an dem Tag fällig sind, und zurückgestellten Aufgaben an dem Tag, an dem sie wieder anstehen,
- Rückfragen zu übergebenen Aufgaben,
- Versprechen mit einem Datum,
- [Reisen und Veranstaltungen](calendar.md#trips-and-events) aus Buchungs- und Ticket-E-Mails.

Ein Meeting in zwei Kalendern wird nur einmal angezeigt. Ein Kalender, den jemand mit dir geteilt hat, zeigt die Termine dieser Person blasser und mit ihrem Vornamen an. Daraus entstehen nie Aufgaben. Ganztägige und mehrtägige Termine werden an jedem betreffenden Tag als ganztägig angezeigt. In der Agenda steht eine Reise an jedem ihrer Tage ganz oben. In der Wochen- und Monatsansicht wird sie als durchgehender Balken über ihre Tage angezeigt, zum Beispiel „Reise nach Lissabon“.

Ein gemeinsamer Plan ist ein Versprechen, das mit „Mit“ und dem Namen der anderen Person gekennzeichnet ist. Ein Versprechen zu einem Meeting an diesem Tag mit derselben Person steht in der Zeile des Meetings.

**Überfällig** steht an erster Stelle. Bei einem Meeting mit einer offenen Aufgabe wird der Status angezeigt: **Vorbereitung bereit**, **Wird vorbereitet** oder **Aufgabe**. Eine Aufgabe, die erledigt zu sein scheint (du hast bereits geantwortet oder ein Durchlauf hat sie als erledigt erkannt), wird nicht als **Fällig** angezeigt.

## Agenda, Woche oder Monat

- **Agenda** listet jeden Tag einzeln auf. Scrolle nach unten zu späteren Tagen oder nach oben (oder tippe auf **Frühere Tage anzeigen**), um frühere Tage aufzurufen. Die Ansicht reicht bis eine Woche vor dem Tag zurück, an dem du deinen Kalender verbunden hast. Oben steht, ab welchem Tag sie angezeigt wird. Sobald dein [Verlauf](history.md) geladen ist, reicht sie etwa ein Jahr zurück.
- **Woche** zeigt eine Ansicht von Montag bis Sonntag. Auf dem Handy werden drei Tage angezeigt.
- **Monat** zeigt den ganzen Monat. Auf einem Computer werden bis zu drei Termine pro Tag angezeigt. Auf dem Handy siehst du Punkte. Tippe auf einen Tag, um alle Termine für diesen Tag aufzurufen.

Mit **Heute**, ‹ und › oben wechselst du zwischen Wochen oder Monaten. Die ausgewählte Ansicht wird auf diesem Gerät gespeichert.

In der Wochenansicht stehen Termine zur selben Zeit nebeneinander, bleiben aber lesbar. Die übrigen werden als **+N** angezeigt. Tippe darauf, um den Tag in der Agenda zu öffnen.

## Etwas öffnen

Klicke auf eine Zeile, um den Chat der Aufgabe, das Versprechen, die Reise oder Veranstaltung oder das Meeting zu öffnen. Bei einem Meeting, das du hier nicht ändern kannst, etwa einem Meeting einer anderen Person oder einem mit Gästen, werden die Details angezeigt: wann und wo es stattfindet und wer dabei ist. Personen, die dein Graph kennt, sowie die Organisationen und Projekte, zu denen das Meeting gehört, sind mit ihrer jeweiligen Seite verlinkt. **In Google Kalender öffnen** (oder **In Outlook öffnen**) darunter öffnet den Termin dort. Das Aufrufen nimmt keine Änderungen vor.

Ein für ein Meeting gebuchter Konferenzraum wird unter „Wo“ angezeigt, nie als Person oder in deinem Graph.

Ein Meeting-Link wird mit dem Dienst angezeigt, zu dem er gehört, etwa Zoom, Google Meet oder Teams, oder als **Videoanruf**. Öffne das Meeting, um teilzunehmen.

## Reisen und Veranstaltungen

Wenn eine Flug-, Hotel-, Ferienhaus-, Zug-, Bus-, Fähr-, Mietwagen-, Taxi- oder Flughafenparkplatzbuchung in deinen E-Mails eingeht, fügt deine Machine sie einer Reise hinzu. Buchungen für dieselbe Reise werden in einer Reise zusammengefasst, egal aus welchem deiner Postfächer sie stammen: die Zugfahrt zum Flughafen, die Flüge, das Auto, die Unterkunft und die Rückreise. Buchungen werden zusammengeführt, wenn sich ihre Tage überschneiden oder eine direkt an die andere anschließt.

Die Reise wird als durchgehender Balken über ihre Tage angezeigt. Öffne sie, um die einzelnen Buchungen chronologisch mit Uhrzeiten, Adresse, Buchungscode und Sitzplatz aufzurufen.

Tickets für ein Konzert, ein Spiel, ein Festival oder eine Konferenz ergeben jeweils eine Veranstaltung mit Veranstaltungsort, Buchungscode, Sitzplatz und Anzahl der Tickets. Eine weitere Bestellung für dieselbe Veranstaltung wird dort hinzugefügt. Eine Veranstaltung, die über dein Arbeitskonto gebucht wurde, ist „Arbeit“, andernfalls „Privat“. Tickets für etwas, das während einer Reise stattfindet, werden stattdessen der Reise hinzugefügt.

Bei einer bevorstehenden Reise zeigt deine Machine an, was noch fehlt, zum Beispiel **Für 2 Nächte ist keine Unterkunft gebucht** oder dass keine Fahrt vom Flughafen zum Hotel gebucht ist. Diese Zeilen sind blasser und mit **Keine Buchung** markiert. Bei einer Reise ohne Unterkunft werden keine Nächte erwähnt.

- In jeder Zeile steht, von wem die Buchung stammt, zum Beispiel **Von Example Tickets**. Öffne die Zeile, um die E-Mail aufzurufen.
- Wenn aus der E-Mail eine Aufgabe entstanden ist, zum Beispiel die Tickets zu bezahlen, wird sie über **Aufgabe öffnen** angezeigt.
- Änderungen an einer Buchung werden in der zugehörigen Zeile angezeigt. Stornierte Buchungen werden entfernt. Wenn alle Buchungen storniert sind, wird auch die Reise oder Veranstaltung entfernt.
- Buchungen für andere Personen, zum Beispiel der Flug eines Kollegen, den er dir weitergeleitet hat, erscheinen nicht bei deinen Reisen.

Die meisten Bestätigungen enthalten ihre Details in einem Format, das deine Machine ohne KI lesen kann. Bei Bestätigungen, die das nicht tun, etwa weitergeleiteten E-Mails oder von kleineren Buchungsseiten, liest dein [Modell](model.md) die E-Mail im Hintergrund, einige auf einmal, und wartet, wenn du dich deinem Nutzungslimit näherst. Buchungs-E-Mails aus dem Jahr deines [Verlaufs](history.md), das deine Machine speichert, werden im Hintergrund gelesen, sobald der Verlauf geladen ist.

## Meeting-Notizen und Transkript

Die Details eines Meetings bestehen aus zwei Teilen. **Notizen** ist die Zusammenfassung mit Entscheidungen und Aufgaben. Das **Transkript** enthält wortwörtlich, was gesagt wurde. Es ist anfangs eingeklappt und zeigt die Dauer an. Mit **Anzeigen** öffnest du es.

Wenn die Inhalte nicht geladen werden, wird es etwa eine halbe Minute lang automatisch erneut versucht. Danach tippe auf **Erneut versuchen**.

Für beide gibt es die Optionen **Notizen hinzufügen** oder **Transkript hinzufügen**, **Datei hochladen** für eine Markdown- oder Textdatei, **Bearbeiten** und **Entfernen** (zweimal tippen). Die Inhalte bleiben jeweils getrennt. Bei einem Meeting, das du ändern kannst, öffnet **Notizen** unter dem Formular die Notizen.

Wenn [Zoom](zoom.md), [Google Meet](google-meet.md) oder [Granola](granola.md) verbunden ist, erscheinen dessen Notizen unter „Notizen“ und das Transkript unter „Transkript“, gekennzeichnet mit **Von Zoom**, **Von Google Meet** oder **Von Granola**. Sie ersetzen nie Inhalte, die du hinzugefügt hast. Wenn beides vorhanden ist, wird beides angezeigt.

Notizen können auch im Kalendereintrag des Meetings selbst enthalten sein, nachdem das Meeting begonnen hat, oder per E-Mail von Zoom oder Gemini eingehen. Nach dem Meeting erstellt The Machine daraus nur dann Aufgaben, wenn es sich um eindeutige nächste Schritte handelt. Dieselben Notizen, die auf zwei Wegen eingehen, ergeben nur eine Aufgabe. Als Quelle wird das Meeting angegeben: „Quelle: Notizen aus“ dem Meeting.

Bei einem Meeting mit Transkript, aber ohne Notizen, gibt es die Option **Notizen erstellen**. The Machine erstellt anhand des Transkripts eine kurze Zusammenfassung mit Entscheidungen und Aufgaben samt den jeweils zuständigen Personen, und zwar in der Sprache des Meetings.

Es wird **Notizen werden geschrieben…** angezeigt. Der Vorgang läuft weiter, wenn du das Meeting schließt. Bei einem langen Meeting dauert es einige Minuten. Dafür wird dein eigenes Modell verwendet. Die Notizen sind mit **Von The Machine geschrieben** gekennzeichnet und ersetzen nie Notizen, die du hinzugefügt hast.

The Machine kann sie auch hinzufügen. Bitte sie in einem Chat zu einer Aufgabe darum, zum Beispiel: „Füge dieses Transkript zum heutigen Board-Meeting hinzu.“ Ein Transkript wird unter „Transkript“ abgelegt, eine Zusammenfassung unter „Notizen“. Bei einem Meeting mit solchen Inhalten wird im Kalender **Notizen** oder **Transkript** angezeigt.

The Machine liest beides, um die Nachfassnachrichten zum Meeting zu erstellen. Sie sind wie das Meeting entweder Arbeit oder privat und werden nur dann mit deinem Team geteilt, wenn das Meeting selbst im Team geteilt wird.

Ein Meeting lässt sich überall mit diesen Details öffnen: in einer Zeitleiste, in der Nachrichtensuche oder als Quelle einer Aufgabe. Über **Ursprüngliche Einladung** unten wird die Einladung so angezeigt, wie sie eingegangen ist.

## Termin hinzufügen oder ändern

Deinen eigenen Google-Kalender kannst du hier ändern. Outlook und andere Kalender sind schreibgeschützt. Mit **Neuer Termin** fügst du einen Termin hinzu (auf dem Handy über **+** in der oberen Leiste): Wähle den Kalender, einen Titel und die Uhrzeit aus. Klicke auf einen Termin ohne Gäste in diesem Kalender, um ihn zu ändern oder über **Löschen** zu entfernen (zweimal tippen).

**Ort** schlägt beim Tippen passende Orte vor: zuerst Orte, die du bereits verwendet hast, und deine Organisationen, danach Adressen von [OpenStreetMap](https://www.openstreetmap.org), einem kostenlosen Kartendienst. Nur die Wörter, die du eingibst, werden zur Suche gesendet. Wähle einen Vorschlag aus oder behalte deinen eigenen Text.

Mit **Einladen** fügst du Personen aus deinem Graph oder beliebige E-Mail-Adressen hinzu. Die Option gibt es nur in deinem eigenen Kalender. Über dem Button werden die eingeladenen Personen aufgelistet. Der Button zeigt auch ihre Anzahl an: **Hinzufügen und 2 einladen**. Google verschickt die Einladungen erst, wenn du darauf tippst. Ohne Gäste wird niemand eingeladen oder über Änderungen benachrichtigt.

Eine Aufgabe kann ebenfalls eine Änderung vorschlagen, zum Beispiel eine Abholung, die hinzugefügt werden soll. Es wird genau angezeigt, was geändert wird. Erst durch **Hinzufügen**, **Speichern** oder **Löschen** wird die Änderung vorgenommen.

Noch keine Meetings? Wenn du keinen Kalender verbunden hast, öffnet **Kalender verbinden** die Verbindungen. Dort kannst du [Google Calendar](google-calendar.md), [Outlook-Kalender](microsoft.md) oder [einen anderen Kalender](other-calendars.md) verbinden.

## Überschneidungen mit deinem anderen Kalender

Wenn sich ein Arbeitsmeeting mit einem Termin in deinem privaten Kalender überschneidet oder umgekehrt, erstellt The Machine eine Aufgabe zur jeweils neueren der beiden Veranstaltungen. Sie kann eine kurze Nachricht entwerfen, um den Termin zu verschieben, oder vorschlagen, ihn abzusagen. Nichts wird verschickt, bevor du es bestätigst.

Überschneidet sich ein Termin mit mehreren anderen, wird dafür nur eine Aufgabe erstellt. Solange sie offen ist, wird eine neue Überschneidung derselben Aufgabe hinzugefügt. Sobald sie erledigt oder verworfen ist, wird sie nur durch ein Meeting wieder geöffnet, das später erstellt oder geändert wurde.

Ganztägige, als verfügbar markierte und vorläufige Termine zählen nie. Jede Überschneidung wird nur einmal angezeigt. Auch Googles Arbeitsort, Fokuszeit und Abwesenheit zählen nicht. Ebenso wenig ein eigener Blocker, der andere Meetings umfasst, etwa ein Bürotag. Nur die Meetings innerhalb des Blockers können sich überschneiden. Ein Blocker ohne weitere Personen und ohne Meetings, etwa ein Flug, kann sich dagegen mit einem Termin überschneiden, an dem andere Personen teilnehmen.

Eine Arbeitsaufgabe weist nur auf einen Konflikt hin. Dein Team sieht deshalb nie den privaten Termin. Nur du siehst, womit er sich überschneidet: die ersten beiden Termine und danach die Anzahl der weiteren. Eine Aufgabe, an der du nichts unternommen hast, wird automatisch geschlossen, wenn sich ihr Termin mit einer anderen Aufgabe überschneidet oder sich herausstellt, dass es gar keine Überschneidung gab.

## Bereit für deine Meetings

Vor einem Meeting mit Personen außerhalb deines Unternehmens erstellt The Machine eine Aufgabe: **Vorbereiten auf** das Meeting. Sie enthält eine kurze Übersicht:

- **Wer:** wer die Personen sind, basierend auf deinem Graph, und, falls bekannt, Informationen zu ihrem Hintergrund.
- **Organisation:** was ihr Unternehmen tut, für wen und zu welchem Preis, sofern das für das Meeting relevant ist.
- **Bisher:** was ihr besprochen, gefragt und angeboten habt und wie der aktuelle Stand ist. Diese Nachrichten werden nach dem Meeting als Quellen der Aufgabe aufgeführt.
- **Früher vereinbart:**, **Seitdem geändert:** und **Noch offen:** die Ergebnisse früherer Meetings mit denselben Personen. Jede Zeile enthält das zugehörige Meeting oder die Nachricht.
- **Offene Versprechen:** was du oder die anderen noch erledigen müsst, basierend auf den Versprechen auf deiner Machine.
- **Offene Fragen:** was noch unbeantwortet ist.
- **Entscheiden oder mitbringen:** was zu klären oder mitzubringen ist und was für die anderen wahrscheinlich wichtig ist.

Die Übersicht erscheint morgens an einem Arbeitstag: am Tag des Meetings, wenn es nachmittags stattfindet, andernfalls am vorherigen Arbeitstag. Sie dient zum Lesen und wird als **Erledigt** markiert, sobald du sie gelesen hast. Ein Versprechen oder eine Frage, zu dem oder der etwas unternommen werden muss, erhält eine eigene Aufgabe.

Frag im Chat des Meetings danach oder füge dein Wissen hinzu. The Machine antwortet oder baut deine Notiz in die Übersicht ein, zum Beispiel unter **Entscheiden oder mitbringen**, und lernt daraus. Aus einer Übersicht wird nichts verschickt.

Frühere Meetings zählen, wenn an beiden eine Person von außerhalb teilnimmt, egal wie die Meetings hießen und welche Adresse die Person verwendet hat. The Machine liest die Notizen, die auf deiner Machine gespeichert sind: deine Notizen, die deiner Meeting-App oder die Notizen, die dir per E-Mail geschickt wurden. Andernfalls liest sie das Transkript oder die Notizen im Kalendereintrag. Neuere Notizen zählen stärker. Was später geklärt wurde, wird nicht mehr als offen angezeigt.

Auch Notizen und Nachrichten aus dem [Verlauf](history.md) zählen. So enthält eine Übersicht Informationen zu Meetings von vor deinem Einstieg.

Eine Arbeitsübersicht liest keine privaten Notizen und nichts von der Machine einer anderen Person. Ihr Inhalt bleibt bei dir: Bei einer Übergabe wird er nicht mitgeschickt und er kann nicht zur Überprüfung weitergegeben werden. Ohne Notizen werden diese Zeilen nicht angezeigt.

Die Übersicht verwendet, was sich bereits auf deiner Machine befindet. Bei einem ersten Meeting mit jemandem aus einem Unternehmen liest sie außerdem die Startseite der Unternehmenswebsite.

Wenn die Websuche auf deiner Machine eingerichtet ist, sucht sie auch kurz im Web nach dem Namen der Person und dem Unternehmen. Eine gehostete Machine wird ohne Websuche bereitgestellt. Auf deinem eigenen Computer kannst du sie in OpenClaw einrichten. Die Suchergebnisse werden mit einem Link angezeigt. Für die Suche werden nur der öffentliche Name der Person, der Unternehmensname und die Website verwendet, nie deine Nachrichten. Die Suchergebnisse werden 30 Tage lang wiederverwendet.

So kann auch für ein erstes Meeting, dem du zugesagt hast, eine Übersicht erstellt werden, bevor ihr ein Wort gewechselt habt: mit Informationen dazu, was das Unternehmen tut, was das für dich bedeutet und, falls bekannt, wer die Person ist. Wenn nur ein Vorname bekannt ist, werden Suchergebnisse nur dann übernommen, wenn sie eindeutig auf eine Person verweisen. Wenn **Arbeitskontakte nachschlagen** deaktiviert ist (Einstellungen, Sicherheit), wird nichts nachgeschlagen.

Für wiederkehrende Meetings wird nur dann eine Übersicht erstellt, wenn es seit dem letzten Meeting etwas Neues gab: eine Nachricht, Notizen oder ein Versprechen. Sie enthält die Neuigkeiten, nicht den Inhalt der letzten Übersicht. Sie wird erstellt, sobald das vorherige Meeting vorbei ist, höchstens für zwei wiederkehrende Meetings am Tag.

Für Meetings nur mit deinem Team gibt es nur dann eine Übersicht, wenn die Notizen zu früheren Meetings eine offene Entscheidung, einen noch ausstehenden Schritt oder Neuigkeiten zeigen. Diese müssen aus derselben Serie oder aus Meetings mit demselben Titel und mindestens einer gemeinsamen Person stammen, nie von einem anderen Meeting mit denselben Kollegen. Deine Kollegen werden nicht vorgestellt oder gesucht. Für ein normales Stand-up gibt es keine Übersicht.

Wenn es nichts Nützliches zu sagen gibt, wird keine Aufgabe erstellt. Für private oder abgelehnte Meetings wird keine erstellt. Wird ein Meeting verschoben, bleibt seine Aufgabe erhalten, nur der Zeitpunkt ändert sich. Eine verworfene Aufgabe wird nicht erneut angezeigt. Die Aufgabe eines abgesagten Meetings wird automatisch geschlossen.

Wenn eine Aktualisierung den Inhalt einer Übersicht ändert, werden offene Übersichten für noch bevorstehende Meetings einmal in der neuen Form erstellt. Titel, Quellen und Position in deiner Liste bleiben gleich. Eine Übersicht, die du geändert, zurückgestellt oder geschlossen hast, bleibt unverändert. Dasselbe gilt für Meetings, die in den nächsten Minuten beginnen.

Die Details des Meetings zeigen die zugehörige Aufgabe unter **Aufgabe** an. Tippe darauf, um zum Chat zu gelangen.
