---
title: Kalender
area: calendar
summary: Die kommende Woche auf einen Blick: Meetings, fällige Aufgaben, zurückgestellte Aufgaben und Versprechen.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 7f9f9d9e9a502b7d
---
## Was angezeigt wird

Deine Tage ab heute, mit:

- Meetings aus den Kalendern, die du verbunden hast,
- an diesem Tag fälligen Aufgaben und zurückgestellten Aufgaben an dem Tag, an dem sie wieder anstehen,
- Nachfassnachrichten zu übergebenen Aufgaben,
- Versprechen mit einem Datum,
- [Reisen und Events](calendar.md#trips-and-events) aus Buchungs- und Ticketmails.

Ein Meeting in zwei Kalendern wird nur einmal angezeigt. Ein Kalender, den jemand mit dir geteilt hat, zeigt die Termine dieser Person ausgegraut und mit ihrem Vornamen an. Daraus entstehen nie Aufgaben. Ganztägige und mehrtägige Termine werden an jedem ihrer Tage als ganztägig angezeigt. Eine Reise steht in der Agenda an jedem ihrer Tage ganz oben und wird in der Wochen- und Monatsansicht als durchgehender Balken über diese Tage angezeigt, etwa „Reise nach Lissabon“.

Ein gemeinsam gemachtes Versprechen zählt als ein Versprechen und ist mit „Mit“ und dem Namen der anderen Person gekennzeichnet. Ein Versprechen zu einem Meeting an diesem Tag mit derselben Person steht in der Zeile dieses Meetings.

**Überfällig** steht ganz oben. Bei einem Meeting mit einer offenen Aufgabe wird deren Status angezeigt: **Vorbereitung bereit**, **Wird vorbereitet** oder **Aufgabe**. Eine Aufgabe, die offenbar erledigt ist, weil du schon geantwortet hast oder ihr Durchlauf sie als erledigt erkannt hat, wird nicht als **Fällig** angezeigt.

## Agenda, Woche oder Monat

- **Agenda** zeigt die einzelnen Tage. Scrolle nach unten zu späteren Tagen oder nach oben beziehungsweise tippe auf **Frühere Tage anzeigen**, um frühere Tage aufzurufen. Die Ansicht reicht bis eine Woche vor dem Verbinden deines Kalenders zurück. Oben steht, ab welchem Tag sie angezeigt wird. Sobald der [Verlauf](history.md) geladen ist, reicht sie etwa ein Jahr zurück.
- **Woche** zeigt eine Ansicht von Montag bis Sonntag. Auf dem Handy werden drei Tage angezeigt.
- **Monat** zeigt den ganzen Monat. Auf einem Computer werden bis zu drei Einträge pro Tag angezeigt. Auf dem Handy erscheinen Punkte. Tippe darauf, um die Termine des Tages aufzurufen.

Mit **Heute**, ‹ und › oben wechselst du zwischen Wochen oder Monaten. Die ausgewählte Ansicht wird auf diesem Gerät gespeichert.

In der Wochenansicht stehen Termine zur selben Zeit nebeneinander, ohne dass sie schwer lesbar werden. Weitere Termine werden als **+N** angezeigt. Tippe darauf, um den Tag in der Agenda zu öffnen.

## Etwas öffnen

Klicke auf eine Zeile, um den Chat zur Aufgabe, das Versprechen, die Reise oder das Event beziehungsweise das Meeting zu öffnen. Bei einem Meeting, das du hier nicht ändern kannst, etwa einem Meeting einer anderen Person oder einem Meeting mit Gästen, werden Details angezeigt: wann und wo es stattfindet und wer teilnimmt. Personen, die dein Graph kennt, sowie die Organisationen und Projekte, zu denen das Meeting gehört, führen zu ihrer jeweiligen Seite. Über **In Google Kalender öffnen** oder **In Outlook öffnen** kannst du den Termin dort aufrufen. Wenn du ihn nur ansiehst, wird nichts geändert.

Ein zu einem Meeting gebuchter Besprechungsraum wird unter „Wo“ angezeigt, aber nie als Person oder in deinem Graph.

Ein Meeting-Link wird mit dem jeweiligen Dienst angezeigt, etwa Zoom, Google Meet oder Teams, oder als **Videoanruf**. Öffne das Meeting, um teilzunehmen.

## Reisen und Events

Wenn eine Flug-, Hotel-, Ferienwohnung-, Zug-, Bus-, Fähr-, Mietwagen-, Taxi- oder Flughafenparkplatzbuchung in deinen Mails eingeht, fügt deine Machine sie einer Reise hinzu. Buchungen für dieselbe Reise werden in einer Reise zusammengefasst, auch wenn sie aus verschiedenen Postfächern stammen: die Zugfahrt zum Flughafen, die Flüge, das Auto, die Unterkunft und die Rückreise. Buchungen werden zusammengefasst, wenn sich ihre Tage überschneiden oder eine direkt an die andere anschließt.

Die Reise wird als ein durchgehender Balken über ihre Tage angezeigt. Öffne sie, um alle Buchungen in zeitlicher Reihenfolge mit Uhrzeiten, Adresse, Buchungscode und Sitzplatz aufzurufen.

Tickets für ein Konzert, ein Spiel, ein Festival oder eine Konferenz ergeben ein Event pro Veranstaltung. Angezeigt werden der Veranstaltungsort, der Buchungscode, der Sitzplatz und die Anzahl der Tickets. Eine weitere Bestellung für dasselbe Event wird dort ergänzt. Ein Event, das über dein Arbeitskonto gebucht wurde, ist „Arbeit“, andernfalls „Privat“. Tickets für etwas, das während einer Reise stattfindet, werden stattdessen der Reise hinzugefügt.

Bei einer bevorstehenden Reise weist deine Machine auf fehlende Buchungen hin, etwa **Für 2 Nächte ist keine Unterkunft gebucht** oder darauf, dass nichts für die Fahrt vom Flughafen zum Hotel gebucht wurde. Diese Zeilen sind ausgegraut und mit **Keine Buchung** gekennzeichnet. Bei einer Reise ganz ohne Unterkunft wird nichts zu Nächten angezeigt.

- In jeder Zeile steht, woher die Buchung stammt, etwa **Von Example Tickets**. Tippe darauf, um die Mail zu öffnen.
- Wenn aus der Mail eine Aufgabe entstanden ist, etwa die Tickets zu bezahlen, wird sie über **Aufgabe öffnen** angezeigt.
- Wird eine Buchung geändert, wird ihre Zeile aktualisiert. Wird sie storniert, wird sie entfernt. Wenn alle Buchungen storniert wurden, wird auch die Reise oder das Event entfernt.
- Eine Buchung für jemand anderen, etwa der an dich weitergeleitete Flug einer Kollegin, wird nicht zu deinen Reisen hinzugefügt.

Die meisten Bestätigungen enthalten ihre Details in einem Format, das deine Machine ohne KI auslesen kann. Bei Bestätigungen, die das nicht tun, etwa weitergeleiteten Mails oder von kleinen Buchungsseiten, liest dein [Modell](model.md) die Mail im Hintergrund aus, einige auf einmal. Wenn du dich deinem Nutzungslimit näherst, wartet es. Buchungsmails aus dem Jahr des [Verlaufs](history.md), das deine Machine speichert, werden im Hintergrund ausgelesen, sobald der Verlauf geladen ist.

## Meeting-Notizen und Transkript

Die Details eines Meetings bestehen aus zwei Teilen. **Notizen** ist die Zusammenfassung mit Entscheidungen und Aufgaben. **Transkript** enthält Wort für Wort, was gesagt wurde. Es ist zunächst eingeklappt und zeigt an, wie lange es ist. Mit **Anzeigen** wird es geöffnet.

Wenn die Inhalte nicht geladen werden, versucht es das etwa eine halbe Minute lang automatisch erneut. Tippe danach auf **Erneut versuchen**.

Für beide gibt es eigene Optionen: **Notizen hinzufügen** oder **Transkript hinzufügen**, **Datei hochladen** für eine Markdown- oder Textdatei, **Bearbeiten** und **Entfernen**. Tippe zum Entfernen zweimal. Was du zu einem Teil hinzufügst, bleibt dort. Bei einem Meeting, das du ändern kannst, öffnet **Notizen** unter dem Formular die Notizen.

Wenn [Zoom](zoom.md), [Google Meet](google-meet.md) oder [Granola](granola.md) verbunden ist, werden dessen Notizen unter „Notizen“ und das Transkript unter „Transkript“ angezeigt. Sie sind mit **Von Zoom**, **Von Google Meet** oder **Von Granola** gekennzeichnet. Sie ersetzen nie Inhalte, die du hinzugefügt hast. Sind beide vorhanden, werden beide angezeigt.

Notizen können auch im Kalendereintrag des Meetings selbst stehen, nachdem das Meeting begonnen hat, oder per Mail von Zoom oder Gemini eingehen. Nach dem Meeting erstellt The Machine daraus nur Aufgaben für klare nächste Schritte. Wenn dieselben Notizen auf zwei Wegen eingehen, entsteht nur eine Aufgabe. Als Quelle wird das Meeting angegeben: „Quelle: Notizen aus“ dem Meeting.

Bei einem Meeting mit Transkript, aber ohne Notizen, gibt es die Option **Notizen erstellen**. The Machine erstellt aus dem Transkript eine kurze Zusammenfassung, Entscheidungen und Aufgaben mit Angaben dazu, wer sie übernimmt. Die Notizen sind in der Sprache des Meetings.

Die Anzeige **Notizen werden geschrieben…** bleibt sichtbar, und der Vorgang läuft weiter, wenn du das Meeting schließt. Bei einem langen Meeting kann es mit deinem eigenen Modell einige Minuten dauern. Die Notizen sind mit **Von The Machine geschrieben** gekennzeichnet und ersetzen nie Notizen, die du hinzugefügt hast.

The Machine kann die Notizen auch selbst hinzufügen. Bitte im Chat einer Aufgabe darum, etwa mit „Füge dieses Transkript zum heutigen Teammeeting hinzu“. Ein Transkript kommt unter „Transkript“, eine Zusammenfassung unter „Notizen“. Bei einem Meeting mit Notizen oder Transkript wird im Kalender **Notizen** oder **Transkript** angezeigt.

The Machine liest beides aus, um Nachfassaufgaben zum Meeting zu erstellen. Sie sind wie das Meeting als Arbeit oder privat gekennzeichnet und werden nur dann mit deinem Team geteilt, wenn auch das Meeting geteilt wird.

Ein Meeting lässt sich überall mit denselben Details öffnen, etwa in einer Timeline, in der Nachrichtensuche oder als Quelle einer Aufgabe. Unten zeigt **Ursprüngliche Einladung** die Einladung so an, wie sie eingegangen ist.

## Event hinzufügen oder ändern

Deinen eigenen Google-Kalender kannst du hier ändern. Outlook und andere Kalender lassen sich nur ansehen. Über **Neuer Termin** fügst du einen Termin hinzu. Auf dem Handy findest du die Option unter **+** in der oberen Leiste. Wähle den Kalender, einen Titel und die Uhrzeit aus. Klicke auf einen Termin in diesem Kalender, zu dem keine Gäste eingeladen sind, um ihn zu ändern oder zu **Löschen**. Tippe zum Löschen zweimal.

Unter **Wo** werden während der Eingabe Orte vorgeschlagen: zuerst Orte, die du schon verwendet hast, und deine Organisationen, danach Adressen von [OpenStreetMap](https://www.openstreetmap.org), einem kostenlosen Kartendienst. Zur Suche werden nur die Wörter gesendet, die du eingibst. Wähle einen Vorschlag aus oder behalte deinen eigenen Text.

Über **Einladen** kannst du Personen aus deinem Graph oder beliebige E-Mail-Adressen hinzufügen. Die Option gibt es nur in deinem eigenen Kalender. Über der Schaltfläche stehen die Personen, die eine Einladung erhalten. Auf der Schaltfläche steht ihre Anzahl: **Hinzufügen und 2 einladen**. Google sendet die Einladungen erst, wenn du darauf tippst. Ohne Gäste wird niemand eingeladen und niemand erhält eine Aktualisierung.

Eine Aufgabe kann ebenfalls eine Änderung vorschlagen, etwa einen Abholtermin. Dabei wird genau angezeigt, was geändert wird. Die Änderung wird nur vorgenommen, wenn du auf **Hinzufügen**, **Speichern** oder **Löschen** tippst.

Noch keine Meetings? Wenn du keinen Kalender verbunden hast, öffnet **Kalender verbinden** die Verbindungen. Verbinde dort [Google Calendar](google-calendar.md), [Outlook-Kalender](microsoft.md) oder [einen anderen Kalender](other-calendars.md).

## Überschneidungen mit deinem anderen Kalender

Wenn sich ein Arbeitsmeeting mit etwas in deinem privaten Kalender überschneidet oder umgekehrt, erstellt The Machine eine Aufgabe zum neueren der beiden Termine. Sie kann eine kurze Nachricht entwerfen, um den Termin zu verschieben, oder anbieten, ihn abzusagen. Nichts wird gesendet, bevor du es bestätigst.

Überschneidet sich ein Event mit mehreren Terminen, wird eine Aufgabe zu diesem Event erstellt. Solange sie offen ist, werden neue Überschneidungen hinzugefügt. Sobald die Aufgabe erledigt oder verworfen wurde, wird sie nur durch ein später erstelltes oder geändertes Meeting wieder aufgenommen.

Ganztägige, freie und vorläufige Termine zählen nie. Jede Überschneidung wird nur einmal angezeigt. Auch Googles Arbeitsort, Fokuszeit und Abwesenheit zählen nicht. Ein eigener Block mit mehreren darin liegenden Meetings zählt ebenfalls nicht, etwa ein Bürotag. Nur die Meetings darin können sich überschneiden. Ein Block ohne andere Personen und ohne Meetings darin, etwa ein Flug, kann sich weiterhin mit einem Event überschneiden, an dem andere teilnehmen.

Eine Aufgabe für die Arbeit weist nur auf einen Konflikt hin. Dein Team sieht den privaten Termin also nie. Nur du siehst, womit er sich überschneidet: zuerst die ersten beiden Termine, dann die Anzahl weiterer. Eine Aufgabe, an der du nichts gemacht hast, wird automatisch geschlossen, wenn sich der Termin mit einer anderen Aufgabe überschneidet oder sich herausstellt, dass es gar keine Überschneidung gab.

## Für deine Meetings vorbereitet

Vor einem Meeting mit Personen von außerhalb deines Unternehmens erstellt The Machine eine Aufgabe: **Vorbereiten auf** das Meeting. Sie enthält ein kurzes Briefing:

- **Wer:** wer die Personen sind, laut deinem Graph, und, wenn bekannt, etwas zu ihrem Hintergrund.
- **Organisation:** was ihr Unternehmen tut, für wen und zu welchem Preis, sofern das für das Meeting wichtig ist.
- **Bisher:** was ihr besprochen, gefragt und angeboten habt und wo die Dinge stehen. Nach dem Meeting werden diese Nachrichten als Quellen der Aufgabe angezeigt.
- **Früher vereinbart:**, **Seitdem geändert:** und **Noch offen:** was bei früheren Meetings mit denselben Personen besprochen wurde. Jede Zeile zeigt das Meeting oder die Nachricht, aus der sie stammt.
- **Offene Versprechen:** was du oder die anderen noch erledigen müssen, basierend auf den Versprechen auf deiner Machine.
- **Offene Fragen:** was noch unbeantwortet ist.
- **Entscheiden oder mitbringen:** was noch geklärt oder mitgebracht werden muss und was den anderen vermutlich wichtig ist.

Das Briefing erscheint am Morgen eines Arbeitstags: am Tag des Meetings, wenn es nachmittags stattfindet, andernfalls am vorherigen Arbeitstag. Es ist zum Lesen gedacht und wird als **Erledigt** markiert, wenn du es gelesen hast. Ein Versprechen oder eine Frage darin, um die du dich kümmern musst, erhält eine eigene Aufgabe.

Frag im Chat zum Meeting danach oder ergänze, was du weißt. The Machine antwortet oder arbeitet deine Notiz ins Briefing ein, etwa unter **Entscheiden oder mitbringen**, und lernt daraus. Aus einem Briefing wird nichts gesendet.

Frühere Meetings zählen, wenn dieselbe Person von außerhalb bei beiden dabei war, egal wie die Meetings hießen oder welche E-Mail-Adresse die Person verwendet hat. The Machine liest die Notizen auf deiner Machine aus: deine eigenen, die deiner Meeting-App oder die Notizen, die dir per Mail geschickt wurden. Wenn keine davon vorhanden sind, nutzt sie das Transkript oder die Notizen im Kalendereintrag. Neuere Notizen zählen stärker. Ein Punkt, der später geklärt wurde, wird nicht mehr als offen angezeigt.

Auch Notizen und Nachrichten aus dem [Verlauf](history.md) zählen. So kann das Briefing auch Meetings berücksichtigen, die vor deinem Start stattgefunden haben.

Ein Arbeitsbriefing enthält keine privaten Notizen und nichts von der Machine einer anderen Person. Der Inhalt bleibt bei dir: Bei einer Übergabe wird er nicht mitgeschickt und kann auch nicht zur Prüfung weitergegeben werden. Wenn keine Notizen vorhanden sind, werden diese Zeilen nicht angezeigt.

Das Briefing nutzt, was bereits auf deiner Machine ist. Bei einem ersten Meeting mit jemandem aus einem Unternehmen wird auch die Startseite der Unternehmenswebsite ausgelesen.

Außerdem wird kurz im Web nach dem Namen und dem Unternehmen der Person gesucht. Auf einer gehosteten Machine läuft die Suche über dein eigenes ChatGPT- oder Claude-Konto und verbraucht einen kleinen Teil deines Kontingents. Auf deinem eigenen Computer wird der Suchanbieter verwendet, den du in OpenClaw eingerichtet hast, oder dein Konto, sobald du das aktivierst (`meeting_prep_signin_search` in `config.json`). Ein von dir eingerichteter Anbieter hat immer Vorrang.

An die Suche werden nur der öffentliche Name, der Unternehmensname und die Website der Person übermittelt, niemals deine Nachrichten. Die Ergebnisse werden mit einem Link angezeigt und 30 Tage lang wiederverwendet. Bei ChatGPT benennt das Modell den Link, der nicht überprüft wird. Öffne ihn, bevor du dich auf die Angaben verlässt. Im Chat der Aufgabe wird **Hat im Web gesucht** angezeigt.

So kann es schon vor eurem ersten Gespräch ein Briefing geben, wenn du einem ersten Meeting zugesagt hast: mit Informationen zum Unternehmen, dazu, was es für dich bedeutet, und, wenn bekannt, zur Person. Wenn nur ein Vorname bekannt ist, werden Suchergebnisse nur übernommen, wenn sie eindeutig auf eine Person verweisen. Wenn **Arbeitskontakte nachschlagen** in den Einstellungen unter „Sicherheit“ deaktiviert ist, werden keine Kontakte nachgeschlagen und keine Suche durchgeführt.

Bei einem wiederkehrenden Meeting wird nur dann ein Briefing erstellt, wenn es seit dem letzten Termin etwas Neues gab: eine Nachricht, Notizen oder ein Versprechen. Es beschreibt die Neuigkeiten, nicht den Inhalt des letzten Briefings. Das neue Briefing erscheint, sobald der vorherige Termin vorbei ist. Pro Tag werden höchstens zwei wiederkehrende Meetings berücksichtigt.

Für ein Meeting nur mit deinem eigenen Team gibt es nur dann ein Briefing, wenn frühere Notizen derselben Serie oder mit demselben Titel, in denen mindestens eine Person vorkommt, noch einen Punkt für dich enthalten: einen eigenen offenen Schritt, eine an dich gerichtete Frage, eine noch zu treffende Entscheidung oder ein von dir gegebenes Versprechen. Offene Aufgaben, für die nur Kolleginnen oder Kollegen zuständig sind, reichen nicht aus. Deine Kolleginnen und Kollegen werden nicht nachgeschlagen. Wenn möglich, erscheint das Briefing am Morgen des Meetings.

Wenn es nichts Hilfreiches zu sagen gibt, wird keine Aufgabe erstellt. Für private und abgesagte Meetings gibt es keine Briefings. Wird ein Meeting verschoben, bleibt seine Aufgabe erhalten und wird auf die neue Uhrzeit aktualisiert. Eine verworfene Aufgabe wird nicht erneut erstellt. Die Aufgabe zu einem abgesagten Meeting wird automatisch geschlossen.

Wenn eine Aktualisierung den Inhalt eines Briefings verändert, werden offene Briefings für bevorstehende Meetings einmal neu geschrieben. Titel, Quellen und Position in deiner Liste bleiben gleich. Ein Briefing, das du geändert, zurückgestellt oder geschlossen hast, bleibt unverändert. Dasselbe gilt für Meetings, die in den nächsten Minuten beginnen.

Die Details des Meetings zeigen die zugehörige Aufgabe unter **Aufgabe**. Tippe darauf, um direkt zum Chat zu gelangen.
