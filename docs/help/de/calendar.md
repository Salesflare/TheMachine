---
title: Kalender
area: calendar
summary: Die kommende Woche an einem Ort: Meetings, fällige Aufgaben, zurückgestellte Aufgaben und Versprechen.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 9b7475608bb04e5c
---
## Was angezeigt wird

Deine Tage ab heute mit:

- Meetings aus den Kalendern, die du verbunden hast,
- Aufgaben, die an diesem Tag fällig sind, und zurückgestellten Aufgaben an dem Tag, an dem sie wieder anstehen,
- Nachfragen zu übergebener Arbeit,
- Versprechen mit einem Datum,
- [Reisen und Veranstaltungen](calendar.md#trips-and-events) aus Buchungs- und Ticketmails.

Ein Meeting, das in zwei Kalendern steht, wird nur einmal angezeigt. Ein Kalender, den jemand mit dir geteilt hat, zeigt die Termine der Person ausgegraut und mit ihrem Vornamen an. Daraus entstehen nie Aufgaben. Ganztägige und mehrtägige Termine werden an jedem betreffenden Tag als ganztägig angezeigt. In der Agenda steht eine Reise an jedem ihrer Tage ganz oben. In Woche und Monat wird sie als durchgehender Balken über ihre Tage angezeigt, zum Beispiel „Reise nach Lissabon“.

Ein gemeinsamer Plan ist ein Versprechen, das mit „Mit“ und dem Namen der anderen Person gekennzeichnet ist. Ein Versprechen zu einem Meeting an diesem Tag mit derselben Person steht in der Zeile des Meetings.

**Überfällig** steht ganz oben. Bei einem Meeting mit einer offenen Aufgabe wird deren Status angezeigt: **Vorbereitung bereit**, **Wird vorbereitet** oder **Aufgabe**. Eine Aufgabe, die erledigt aussieht, weil du bereits geantwortet hast oder ihre Ausführung sie als erledigt erkannt hat, wird nicht als **Fällig** angezeigt.

## Agenda, Woche oder Monat

- **Agenda** listet die einzelnen Tage auf. Scrolle nach unten zu späteren Tagen oder nach oben beziehungsweise über **Frühere Tage anzeigen** zu früheren Tagen. Die Ansicht reicht bis eine Woche vor dem Verbinden deines Kalenders zurück. Oben steht, ab welchem Tag sie beginnt. Sobald dein [Verlauf](history.md) geladen ist, reicht sie etwa ein Jahr zurück.
- **Woche** zeigt eine Übersicht von Montag bis Sonntag. Auf dem Handy werden drei Tage angezeigt.
- **Monat** zeigt den ganzen Monat. Auf dem Computer werden pro Tag bis zu drei Einträge angezeigt. Auf dem Handy siehst du Punkte. Tippe auf einen Tag, um seine Einträge aufzurufen.

Mit **Heute**, ‹ und › oben wechselst du zwischen Wochen oder Monaten. Die ausgewählte Ansicht wird auf diesem Gerät gespeichert.

In der Wochenübersicht stehen Termine zur selben Zeit nebeneinander, bleiben aber lesbar. Die übrigen werden als **+N** angezeigt. Tippe darauf, um den Tag in der Agenda zu öffnen.

## Etwas öffnen

Klicke auf eine Zeile, um den Chat zur Aufgabe, das Versprechen, die Reise oder Veranstaltung oder das Meeting zu öffnen. Bei einem Meeting, das du hier nicht ändern kannst, etwa dem Termin einer anderen Person oder einem Meeting mit Gästen, werden die Details angezeigt: wann, wo und wer. Personen, die dein Graph kennt, sowie die Organisationen und Projekte, zu denen das Meeting gehört, sind mit ihren Seiten verlinkt. Über **In Google Calendar öffnen** (oder **In Outlook öffnen**) darunter öffnest du den Termin dort. Beim Ansehen wird nichts geändert.

Ein für ein Meeting gebuchter Besprechungsraum wird unter „Wo“ angezeigt, nie als Person oder in deinem Graph.

Ein Meeting-Link wird mit dem jeweiligen Dienst angezeigt, zum Beispiel Zoom, Google Meet oder Teams, oder als **Videoanruf**. Öffne das Meeting, um teilzunehmen.

## Reisen und Veranstaltungen

Wenn eine Flug-, Hotel-, Ferienhaus-, Zug-, Bus-, Fähr-, Mietwagen-, Taxi- oder Flughafenparkplatzbuchung in deinen Mails eingeht, fügt deine Machine sie einer Reise hinzu. Buchungen für dieselbe Reise werden einer Reise zugeordnet, unabhängig davon, aus welchem deiner Postfächer sie stammen: die Fahrt zum Flughafen, Flüge, Mietwagen, Unterkunft und Rückreise. Buchungen werden zusammengeführt, wenn sich ihre Tage überschneiden oder eine dort endet, wo die nächste beginnt.

Die Reise wird über ihre Tage als ein Balken angezeigt. Öffne ihn, um alle Buchungen in zeitlicher Reihenfolge mit Uhrzeiten, Adresse, Buchungscode und Sitzplatz zu sehen.

Tickets für ein Konzert, ein Spiel, ein Festival oder eine Konferenz ergeben jeweils eine Veranstaltung mit Ort, Buchungscode, Sitzplatz und Anzahl der Tickets. Eine weitere Bestellung für dieselbe Veranstaltung wird hinzugefügt. Eine Veranstaltung, die über dein geschäftliches Postfach gebucht wurde, ist „Arbeit“, andernfalls „Privat“. Tickets für etwas, das während einer Reise stattfindet, werden stattdessen der Reise hinzugefügt.

Bei einer bevorstehenden Reise weist deine Machine auf fehlende Buchungen hin, zum Beispiel **Für 2 Nächte keine Unterkunft gebucht** oder auf eine fehlende Fahrt vom Flughafen zum Hotel. Diese Zeilen werden ausgegraut und mit **Keine Buchung** gekennzeichnet. Bei einer Reise ganz ohne Unterkunft gibt es keinen Hinweis zu Nächten.

- In jeder Zeile steht, woher die Buchung stammt, zum Beispiel **Von Example Tickets**. Öffne die Zeile, um die Mail aufzurufen.
- Wenn aus der Mail eine Aufgabe entstanden ist, zum Beispiel die Tickets zu bezahlen, wird sie über **Aufgabe öffnen** angezeigt.
- Eine geänderte Buchung aktualisiert ihre Zeile. Eine stornierte Buchung wird entfernt. Wenn alle Buchungen storniert sind, wird auch die Reise oder Veranstaltung entfernt.
- Eine Buchung für jemand anderen, zum Beispiel der Flug einer Kollegin, der an dich weitergeleitet wurde, erscheint nicht bei deinen Reisen.

Die meisten Bestätigungen enthalten ihre Details in einem Format, das deine Machine ohne KI auslesen kann. Bei Bestätigungen, die das nicht tun, zum Beispiel weitergeleiteten Mails oder von einer kleinen Buchungsseite, liest dein [Modell](model.md) die Mail im Hintergrund. Es verarbeitet jeweils einige Mails und wartet, wenn du dich deinem Nutzungslimit näherst. Buchungsmails aus dem Jahr deines [Verlaufs](history.md), das deine Machine speichert, werden im Hintergrund gelesen, sobald der Verlauf geladen ist.

## Meeting-Notizen und Transkript

Die Details eines Meetings bestehen aus zwei Teilen. **Notizen** sind die Zusammenfassung mit Entscheidungen und Aufgaben. Das **Transkript** enthält Wort für Wort, was gesagt wurde. Es ist zunächst eingeklappt und zeigt an, wie lange es ist. Über **Anzeigen** öffnest du es.

Wenn die Inhalte nicht geladen werden, versucht es etwa eine halbe Minute lang automatisch erneut. Tippe danach auf **Erneut versuchen**.

Für Notizen und Transkript gibt es jeweils **Notizen hinzufügen** oder **Transkript hinzufügen**, **Datei hochladen** für eine Markdown- oder Textdatei, **Bearbeiten** und **Entfernen** (zweimal tippen). Was du zu einem Teil hinzufügst, bleibt dort. Bei einem Meeting, das du ändern kannst, öffnet **Notizen** unter dem Formular die Notizen.

Wenn [Zoom](zoom.md), [Google Meet](google-meet.md) oder [Granola](granola.md) verbunden ist, werden die Notizen unter „Notizen“ und das Transkript unter „Transkript“ angezeigt. Sie sind mit **Von Zoom**, **Von Google Meet** oder **Von Granola** gekennzeichnet. Sie ersetzen nie Inhalte, die du hinzugefügt hast. Wenn beides vorhanden ist, wird beides angezeigt.

Notizen können auch im Kalendereintrag des Meetings selbst enthalten sein, nachdem es begonnen hat, oder per Mail von Zoom oder Gemini eingehen. Nach dem Meeting erstellt The Machine daraus nur dann Aufgaben, wenn sich daraus klare nächste Schritte ergeben. Wenn dieselben Notizen auf zwei Wegen eingehen, entsteht nur eine Aufgabe. Als Quelle steht das Meeting dort mit dem Hinweis „Quelle: Notizen von“ dem Meeting.

Bei einem Meeting mit Transkript, aber ohne Notizen, gibt es **Notizen erstellen**. The Machine erstellt sie aus dem Transkript: eine kurze Zusammenfassung, Entscheidungen und Aufgaben mit den jeweils zuständigen Personen, und zwar in der Sprache des Meetings.

Die Anzeige **Notizen werden geschrieben…** erscheint. Der Vorgang läuft weiter, wenn du das Meeting schließt. Bei einem langen Meeting dauert es mit deinem eigenen Modell einige Minuten. Die Notizen sind mit **Von The Machine geschrieben** gekennzeichnet und ersetzen nie Notizen, die du hinzugefügt hast.

The Machine kann die Notizen auch hinzufügen. Bitte sie in einer Aufgabe darum, zum Beispiel mit „Füge das Transkript zum heutigen Board-Meeting hinzu“. Ein Transkript wird unter „Transkript“ und eine Zusammenfassung unter „Notizen“ abgelegt. Bei einem Meeting mit Notizen oder Transkript wird im Kalender **Notizen** oder **Transkript** angezeigt.

The Machine liest beides aus, um Nachfassaufgaben zum Meeting zu erstellen. Sie sind wie das Meeting „Arbeit“ oder „Privat“ und werden nur dann mit deinem Team geteilt, wenn auch das Meeting geteilt wird.

Ein Meeting wird überall mit denselben Details geöffnet, egal wo du es findest: auf einer Zeitleiste, in einer Nachrichtensuche oder als Quelle einer Aufgabe. Über **Ursprüngliche Einladung** unten wird die Einladung so angezeigt, wie sie eingegangen ist.

## Termin hinzufügen oder ändern

Du kannst deinen eigenen Google-Kalender hier ändern. Outlook und andere Kalender werden nur angezeigt. Über **Neuer Termin** fügst du einen Termin hinzu (auf dem Handy über **+** in der oberen Leiste): Wähle den Kalender, einen Titel und die Uhrzeit aus. Klicke auf einen Termin ohne Gäste in diesem Kalender, um ihn zu ändern oder über **Löschen** zu entfernen (zweimal tippen).

Unter **Wo** werden während der Eingabe Orte vorgeschlagen: zuerst bereits verwendete Orte und deine Organisationen, danach Adressen von [OpenStreetMap](https://www.openstreetmap.org), einer kostenlosen Karte. Zum Nachschlagen werden nur die Wörter gesendet, die du eingibst. Wähle einen Vorschlag aus oder behalte deinen eigenen Text.

Über **Einladen** fügst du Personen aus deinem Graph oder eine beliebige E-Mail-Adresse hinzu. Diese Option gibt es nur für deinen eigenen Kalender. Über dem Button stehen die eingeladenen Personen. Auf dem Button wird ihre Anzahl angezeigt, zum Beispiel **Hinzufügen und 2 einladen**. Google verschickt die Einladungen erst, wenn du darauf tippst. Ohne Gäste wird niemand eingeladen und niemand erhält eine Aktualisierung.

Auch eine Aufgabe kann eine Änderung vorschlagen, zum Beispiel einen Abholtermin. Es wird genau angezeigt, was sich ändert. Die Änderung wird nur übernommen, wenn du auf **Hinzufügen**, **Speichern** oder **Löschen** tippst.

Noch keine Meetings? Wenn du keinen Kalender verbunden hast, öffnet **Kalender verbinden** die Verbindungen. Verbinde [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) oder [einen anderen Kalender](other-calendars.md).

## Überschneidungen mit deinem anderen Kalender

Wenn sich ein geschäftliches Meeting mit einem Termin in deinem persönlichen Kalender überschneidet oder umgekehrt, erstellt The Machine eine Aufgabe zum neueren der beiden Termine. Sie kann einen kurzen Text verfassen, um den Termin zu verschieben, oder vorschlagen, ihn abzusagen. Nichts wird verschickt, bevor du es bestätigst.

Überschneidet sich ein Termin mit mehreren anderen, gibt es dafür eine Aufgabe. Solange sie offen ist, werden weitere Überschneidungen hinzugefügt. Sobald sie erledigt oder verworfen wurde, wird sie nur dann wieder erstellt, wenn später ein Meeting neu erstellt oder geändert wird.

Ganztägige, freie und vorläufige Termine werden nie berücksichtigt. Jede Überschneidung wird nur einmal angezeigt. Auch der Arbeitsort, die Fokuszeit und die Abwesenheitsnotiz von Google werden nicht berücksichtigt. Dasselbe gilt für einen von dir erstellten Block mit anderen Meetings, zum Beispiel einen Bürotag. Nur die darin enthaltenen Meetings können sich überschneiden. Ein Block ohne andere Personen und Meetings, zum Beispiel ein Flug, kann sich dagegen mit einem Termin überschneiden, an dem andere Personen beteiligt sind.

Eine geschäftliche Aufgabe weist nur auf einen Konflikt hin, damit dein Team den persönlichen Termin nie sieht. Nur du siehst, womit sich der Termin überschneidet: zuerst die beiden ersten, dann die Anzahl der weiteren Termine. Eine Aufgabe, mit der du nichts gemacht hast, wird automatisch geschlossen, wenn der Konflikt zu einer anderen Aufgabe gehört oder sich herausstellt, dass es gar keinen gab.

## Für deine Meetings vorbereitet

Vor einem Meeting mit Personen außerhalb deines Unternehmens erstellt The Machine eine Aufgabe: **Vorbereitung für** das Meeting. Sie enthält eine kurze Übersicht:

- **Wer:** wer die Personen sind, basierend auf deinem Graph, sowie Informationen zu ihrem Hintergrund, sofern bekannt.
- **Organisation:** was ihr Unternehmen macht, für wen und zu welchem Preis, sofern das für das Meeting wichtig ist.
- **Bisher:** was besprochen, gefragt und angeboten wurde und wo die Dinge stehen. Diese Nachrichten werden nach dem Meeting als Quellen der Aufgabe angezeigt.
- **Früher vereinbart:**, **Seitdem geändert:** und **Noch offen:** was aus früheren Meetings mit denselben Personen hervorging. Bei jedem Punkt ist das Meeting oder die Nachricht als Quelle angegeben.
- **Offene Versprechen:** was du oder die anderen noch zu tun haben, basierend auf den Versprechen auf deiner Machine.
- **Offene Fragen:** was noch unbeantwortet ist.
- **Entscheiden oder mitbringen:** was geklärt oder mitgebracht werden sollte und was den anderen vermutlich wichtig ist.

Die Aufgabe erscheint am Morgen eines Werktags: am Tag des Meetings selbst, wenn es am Nachmittag stattfindet, andernfalls am Werktag davor. Sie dient nur zum Lesen. Sobald du sie gelesen hast, markierst du sie als **Erledigt**. Ein Versprechen oder eine Frage darin, aus dem oder der sich eine Aufgabe ergibt, bekommt eine eigene Aufgabe.

Frühere Meetings werden berücksichtigt, wenn an beiden eine externe Person teilgenommen hat, unabhängig davon, wie das Meeting hieß und welche Adresse die Person verwendet hat. Die Übersicht basiert auf den Notizen, die deine Machine hat: deine eigenen, die aus deiner Meeting-App oder die, die dir per Mail geschickt wurden. Wenn es keine gibt, verwendet sie das Transkript oder die Notizen im Kalendereintrag. Neuere Inhalte werden stärker gewichtet. Ein Punkt, der später geklärt wurde, wird nicht mehr als offen angezeigt.

Auch Notizen und Nachrichten aus dem [Verlauf](history.md) werden berücksichtigt. So enthält die Übersicht auch Meetings von vor deinem Einstieg.

Eine geschäftliche Übersicht liest keine persönlichen Notizen und nichts von der Machine einer anderen Person. Der Text bleibt bei dir: Bei einer Übergabe wird er nicht mitgenommen und kann nicht zur Prüfung weitergeleitet werden. Wenn keine Notizen vorhanden sind, fehlen diese Zeilen.

Die Übersicht verwendet, was bereits auf deiner Machine ist. Bei einem ersten Meeting mit einer Person aus einem Unternehmen wird außerdem die Startseite der Unternehmenswebsite gelesen.

Wenn die Websuche auf deiner Machine eingerichtet ist, wird außerdem kurz nach dem Namen der Person und ihrem Unternehmen gesucht. Eine gehostete Machine hat diese Funktion nicht. Auf deinem eigenen Computer kannst du sie in OpenClaw einrichten. Die Suchergebnisse werden mit einem Link angezeigt. Für die Suche werden nur der öffentliche Name der Person, der Firmenname und die Website verwendet, nie deine Nachrichten. Suchergebnisse werden 30 Tage lang wiederverwendet.

So kann es für ein erstes Meeting, das du zugesagt hast, schon vor dem ersten Gespräch eine Übersicht geben: was das Unternehmen macht, was das für dich bedeutet und, sofern bekannt, wer die Person ist. Wenn nur ein Vorname bekannt ist, werden Suchergebnisse nur dann übernommen, wenn sie eindeutig auf eine Person verweisen. Wenn **Arbeitskontakte nachschlagen** deaktiviert ist (Einstellungen, Sicherheit), wird nichts nachgeschlagen.

Für ein wiederkehrendes Meeting wird nur dann eine neue Übersicht erstellt, wenn es seit dem letzten Mal etwas Neues gibt: eine Nachricht, Notizen oder ein Versprechen. Sie nennt die Neuigkeiten, nicht den Inhalt der letzten Übersicht. Sie erscheint nach Ende des vorherigen Meetings, höchstens für zwei wiederkehrende Meetings am Tag.

Wenn es nichts Nützliches zu sagen gibt, wird keine Aufgabe erstellt. Für interne, private und abgesagte Meetings gibt es keine. Wird ein Meeting verschoben, bleibt die Aufgabe erhalten und zeigt die neue Uhrzeit. Eine verworfene Aufgabe erscheint nicht erneut. Die Aufgabe für ein abgesagtes Meeting wird automatisch geschlossen.

Wenn eine Aktualisierung den Inhalt einer Übersicht ändert, werden offene Übersichten für noch bevorstehende Meetings einmal in der neuen Form erstellt. Titel, Quellen und Position in deiner Liste bleiben gleich. Eine von dir geänderte, zurückgestellte oder geschlossene Übersicht bleibt unverändert. Dasselbe gilt für eine Übersicht zu einem Meeting, das in den nächsten Minuten beginnt.

Die Details des Meetings zeigen die zugehörige Aufgabe unter **Aufgabe**, einen Fingertipp vom Chat entfernt.
