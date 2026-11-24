---
title: Kalender
area: calendar
summary: Die kommende Woche an einem Ort: Besprechungen, fällige und zurückgestellte Aufgaben sowie Versprechen.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: d6f800709c378338
---
## Was angezeigt wird

Deine Tage ab heute mit:

- Besprechungen aus den Kalendern, die du verbunden hast,
- an diesem Tag fälligen Aufgaben und zurückgestellten Aufgaben an dem Tag, an dem sie wieder anstehen,
- Nachfassnachrichten zu übergebenen Aufgaben,
- Versprechen mit Datum,
- [Reisen und Veranstaltungen](calendar.md#trips-and-events) aus Buchungs- und Ticketmails.

Eine Besprechung, die in zwei Kalendern steht, wird nur einmal angezeigt. Ein Kalender, den jemand mit dir geteilt hat, zeigt die Termine dieser Person ausgegraut und mit ihrem Vornamen an. Daraus entstehen keine Aufgaben. Ganztägige und mehrtägige Termine werden an jedem ihrer Tage als ganztägig angezeigt. In der Agenda steht eine Reise an jedem ihrer Tage ganz oben. In der Wochen- und Monatsansicht erstreckt sich ein Balken über alle Reisetage, zum Beispiel „Reise nach Lissabon“.

Ein gemeinsamer Plan ist ein Versprechen, das mit „Mit“ und dem Namen der anderen Person gekennzeichnet ist. Ein Versprechen über eine Besprechung an diesem Tag mit derselben Person steht in der Zeile der Besprechung.

**Überfällig** steht an erster Stelle. Bei einer Besprechung mit einer offenen Aufgabe wird angezeigt, ob die **Vorbereitung bereit**, **Wird vorbereitet** oder **Aufgabe** ist. Eine Aufgabe, die erledigt zu sein scheint (du hast bereits geantwortet oder ihr Durchlauf hat ergeben, dass sie erledigt ist), wird nicht als **Fällig** angezeigt.

## Agenda, Woche oder Monat

- **Agenda** zeigt jeden Tag einzeln an. Scrolle nach unten zu späteren Tagen oder nach oben zu früheren Tagen. Du kannst auch **Frühere Tage anzeigen** auswählen. Die Ansicht reicht bis zu einer Woche vor dem Verbinden deines Kalenders zurück. Oben steht, ab welchem Tag sie beginnt. Sobald der [Verlauf](history.md) geladen ist, reicht sie etwa ein Jahr zurück.
- **Woche** zeigt eine Übersicht von Montag bis Sonntag. Auf dem Handy werden drei Tage angezeigt.
- **Monat** zeigt den ganzen Monat. Auf einem Computer werden bis zu drei Einträge pro Tag angezeigt. Auf dem Handy siehst du Punkte. Tippe auf einen Tag, um seine Einträge anzuzeigen.

Mit **Heute**, ‹ und › oben wechselst du zwischen Wochen oder Monaten. Die ausgewählte Ansicht wird auf diesem Gerät gespeichert.

In der Wochenübersicht stehen Termine zur selben Zeit nebeneinander, sodass jeder lesbar bleibt. Weitere Termine werden als **+N** angezeigt. Tippe darauf, um den Tag in der Agenda zu öffnen.

## Etwas öffnen

Klicke auf eine Zeile, um den Chat zur Aufgabe, das Versprechen, die Reise oder Veranstaltung oder die Besprechung zu öffnen. Bei einer Besprechung, die du hier nicht ändern kannst, zum Beispiel weil sie jemand anderem gehört oder Gäste hat, werden die Details angezeigt: wann und wo sie stattfindet und wer dabei ist. Personen, die dein Graph kennt, sowie die Organisationen und Projekte der Besprechung sind mit ihren jeweiligen Seiten verknüpft. Über **In Google Kalender öffnen** (oder **In Outlook öffnen**) darunter öffnest du den Termin dort. Das Öffnen nimmt keine Änderungen vor.

Ein Besprechungsraum, der für einen Termin gebucht wurde, wird unter „Wo“ angezeigt, niemals als Person oder in deinem Graph.

Ein Besprechungslink wird mit dem jeweiligen Dienst angezeigt, zum Beispiel Zoom, Google Meet oder Teams, oder als **Videoanruf**. Öffne die Besprechung, um teilzunehmen.

## Reisen und Veranstaltungen

Wenn eine Flug-, Hotel-, Ferienwohnungs-, Zug-, Bus-, Fähr-, Mietwagen-, Taxi- oder Flughafenparkplatzbuchung in deinen Mails eingeht, fügt deine Machine sie einer Reise hinzu. Buchungen für eine Reise werden einer gemeinsamen Reise zugeordnet, unabhängig davon, in welchem deiner Postfächer sie eingehen: die Zugfahrt zum Flughafen, die Flüge, das Auto, die Unterkunft und die Rückfahrt. Buchungen werden zusammengefasst, wenn sich ihre Tage überschneiden oder eine direkt an die andere anschließt.

Die Reise wird als ein Balken über alle Reisetage angezeigt. Öffne sie, um die einzelnen Buchungen in chronologischer Reihenfolge mit Uhrzeit, Adresse, Buchungscode und Sitzplatz zu sehen.

Tickets für ein Konzert, ein Spiel, ein Festival oder eine Konferenz erstellen jeweils eine eigene Veranstaltung mit Veranstaltungsort, Buchungscode, Sitzplatz und Anzahl der Tickets. Eine zweite Bestellung für dieselbe Veranstaltung wird derselben Veranstaltung hinzugefügt. Eine Veranstaltung, die über dein geschäftliches Postfach gebucht wurde, ist geschäftlich, andernfalls privat. Tickets für etwas, das während einer Reise stattfindet, werden stattdessen der Reise hinzugefügt.

Bei einer bevorstehenden Reise weist deine Machine auf fehlende Buchungen hin, zum Beispiel mit **Für 2 Nächte keine Unterkunft gebucht** oder wenn keine Fahrt vom Flughafen zum Hotel gebucht ist. Diese Zeilen sind ausgegraut und mit **Keine Buchung** gekennzeichnet. Bei einer Reise ohne gebuchte Unterkünfte gibt es keinen Hinweis zu Übernachtungen.

- Jede Zeile zeigt, von wem die Buchung stammt, zum Beispiel **Von Example Tickets**, und öffnet die entsprechende Mail.
- Wenn aus der Mail eine Aufgabe entstanden ist, zum Beispiel die Tickets zu bezahlen, wird sie über **Aufgabe öffnen** angezeigt.
- Eine geänderte Buchung aktualisiert die entsprechende Zeile. Eine stornierte Buchung wird entfernt. Wenn alle Buchungen storniert sind, wird auch die Reise oder Veranstaltung entfernt.
- Buchungen für andere Personen, zum Beispiel der Flug eines Kollegen, den man dir weitergeleitet hat, werden nicht zu deinen Reisen hinzugefügt.

Die meisten Bestätigungen enthalten ihre Details in einem Format, das deine Machine ohne KI lesen kann. Bei Bestätigungen, die das nicht tun, etwa weitergeleiteten Mails oder Mails von kleinen Buchungsseiten, liest dein [Modell](model.md) die Mail im Hintergrund. Dabei verarbeitet es einige Mails auf einmal und wartet, wenn du dich deinem Nutzungslimit näherst. Buchungsmails aus dem Jahr [Verlauf](history.md), das deine Machine speichert, werden im Hintergrund gelesen, sobald der Verlauf geladen ist.

## Besprechungsnotizen und Transkript

Die Details einer Besprechung bestehen aus zwei Teilen. **Notizen** enthalten die Zusammenfassung: Entscheidungen und Aufgaben. Das **Transkript** enthält Wort für Wort, was gesagt wurde. Es ist zunächst eingeklappt und zeigt an, wie lange es ist. Über **Anzeigen** kannst du es öffnen.

Wenn die Inhalte nicht geladen werden, versucht es die App etwa eine halbe Minute lang automatisch erneut. Danach tippe auf **Erneut versuchen**.

Für Notizen und Transkript gibt es jeweils **Notizen hinzufügen** oder **Transkript hinzufügen**, **Datei hochladen** für eine Markdown- oder Textdatei sowie **Bearbeiten** und **Entfernen** (zweimal tippen). Was du in den jeweiligen Bereich einfügst, bleibt dort. Bei einer Besprechung, die du ändern kannst, öffnet **Notizen** unter dem Formular die Notizen.

Wenn [Zoom](zoom.md), [Google Meet](google-meet.md) oder [Granola](granola.md) verbunden ist, werden die Notizen unter „Notizen“ und das Transkript unter „Transkript“ angezeigt. Sie sind mit **Von Zoom**, **Von Google Meet** oder **Von Granola** gekennzeichnet. Sie ersetzen niemals Inhalte, die du hinzugefügt hast. Wenn beides vorhanden ist, wird beides angezeigt.

Notizen können auch im Kalendereintrag der Besprechung selbst enthalten sein, nachdem die Besprechung begonnen hat, oder per Mail von Zoom oder Gemini eingehen. Nach Ende der Besprechung erstellt The Machine daraus nur dann Aufgaben, wenn die nächsten Schritte eindeutig sind. Wenn dieselben Notizen auf zwei Wegen eingehen, wird nur eine Aufgabe erstellt. Als Quelle ist die Besprechung angegeben: „Quelle: Notizen aus“ der Besprechung.

Bei einer Besprechung mit Transkript, aber ohne Notizen, gibt es **Notizen erstellen**. The Machine erstellt aus dem Transkript eine kurze Zusammenfassung, die Entscheidungen und die Aufgaben mit den jeweils zuständigen Personen, und zwar in der Sprache der Besprechung.

Dabei wird **Notizen werden geschrieben…** angezeigt. Die Erstellung läuft weiter, wenn du die Besprechung schließt. Bei einer langen Besprechung dauert es ein paar Minuten. Dafür wird dein eigenes Modell verwendet. Die Notizen sind mit **Von The Machine verfasst** gekennzeichnet und ersetzen niemals Notizen, die du hinzugefügt hast.

The Machine kann Notizen auch hinzufügen. Bitte sie zum Beispiel in einer Aufgabe darum: „Füge dieses Transkript zur heutigen Teambesprechung hinzu.“ Ein Transkript wird unter „Transkript“ eingefügt, eine Zusammenfassung unter „Notizen“. Bei einer Besprechung mit Notizen oder Transkript wird im Kalender **Notizen** oder **Transkript** angezeigt.

The Machine liest beides, um Nachfassnachrichten zur Besprechung zu erstellen. Sie sind wie die Besprechung geschäftlich oder privat und werden nur dann mit deinem Team geteilt, wenn auch die Besprechung geteilt wird.

Eine Besprechung lässt sich überall mit denselben Details öffnen: auf einer Zeitleiste, in einer Nachrichtensuche oder als Quelle einer Aufgabe. Über **Ursprüngliche Einladung** unten wird die Einladung so angezeigt, wie sie eingegangen ist.

## Termin hinzufügen oder ändern

Deinen eigenen Google-Kalender kannst du hier ändern. Outlook und andere Kalender lassen sich nur anzeigen. Über **Neuer Termin** fügst du einen Termin hinzu (auf dem Handy findest du die Option unter **+** in der oberen Leiste). Wähle den Kalender, einen Titel und die Uhrzeit aus. Klicke auf einen Termin ohne Gäste in diesem Kalender, um ihn zu ändern oder über **Löschen** zu entfernen (zweimal tippen).

**Wo** schlägt während der Eingabe Orte vor: zuerst Orte, die du bereits verwendet hast, und deine Organisationen, danach Adressen von [OpenStreetMap](https://www.openstreetmap.org), einem kostenlosen Kartendienst. Nur die von dir eingegebenen Wörter werden zur Suche gesendet. Wähle einen Vorschlag aus oder behalte deinen eigenen Text.

Über **Einladen** kannst du Personen aus deinem Graph oder beliebige E-Mail-Adressen hinzufügen. Die Option gibt es nur in deinem eigenen Kalender. Über der Schaltfläche wird angezeigt, wer eine Einladung erhält. Die Schaltfläche zeigt auch die Anzahl an: **Hinzufügen und 2 einladen**. Google versendet die Einladungen erst, wenn du darauf tippst. Ohne Gäste wird niemand eingeladen und niemand erhält eine Aktualisierung.

Eine Aufgabe kann ebenfalls eine Änderung vorschlagen, zum Beispiel eine Abholung, die du hinzufügen kannst. Es wird genau angezeigt, was sich ändert. Erst wenn du **Hinzufügen**, **Speichern** oder **Löschen** auswählst, wird die Änderung vorgenommen.

Noch keine Besprechungen? Wenn du noch keinen Kalender verbunden hast, öffnet **Kalender verbinden** die Verbindungen. Verbinde [Google Calendar](google-calendar.md), [Outlook-Kalender](microsoft.md) oder [einen anderen Kalender](other-calendars.md).

## Überschneidungen mit deinem anderen Kalender

Wenn sich eine geschäftliche Besprechung mit einem Termin in deinem privaten Kalender überschneidet oder umgekehrt, erstellt The Machine eine Aufgabe zur neueren der beiden Veranstaltungen. The Machine kann einen kurzen Entwurf verfassen, um den Termin zu verschieben, oder vorschlagen, ihn abzusagen. Nichts wird verschickt, bevor du es bestätigst.

Ganztägige, freie und vorläufige Termine zählen nicht. Jede Überschneidung wird nur einmal berücksichtigt. Eine geschäftliche Aufgabe weist nur auf einen Konflikt hin, damit dein Team den privaten Termin nicht sieht. Nur du siehst, womit sich der Termin überschneidet.

## Bereit für deine Besprechungen

Vor einer Besprechung mit Personen außerhalb deines Unternehmens erstellt The Machine eine Aufgabe: **Vorbereiten auf** die Besprechung. Sie enthält ein kurzes Briefing:

- **Wer:** wer die Personen sind, basierend auf den Informationen in deinem Graph, einschließlich Angaben zu ihrem Hintergrund, sofern bekannt.
- **Organisation:** was ihr Unternehmen macht, für wen und zu welchem Preis, sofern das für die Besprechung relevant ist.
- **Bisher:** was besprochen, gefragt und angeboten wurde und wie der aktuelle Stand ist. Nach der Besprechung sind diese Nachrichten die Quellen der Aufgabe.
- **Früher vereinbart:**, **Seitdem geändert:** und **Noch offen:** was bei früheren Besprechungen mit denselben Personen herausgekommen ist. Bei jeder Zeile ist die Besprechung oder Nachricht als Quelle angegeben.
- **Offene Versprechen:** was du oder die anderen noch schulden, basierend auf den Versprechen in deiner Machine.
- **Offene Fragen:** was noch unbeantwortet ist.
- **Entscheiden oder mitbringen:** was geklärt oder mitgebracht werden muss und was die anderen wahrscheinlich wichtig finden.

Das Briefing erscheint am Morgen eines Arbeitstags: am Tag der Besprechung, wenn sie am Nachmittag stattfindet, andernfalls am vorherigen Arbeitstag. Es ist nur zum Lesen gedacht. Markiere es als **Erledigt**, wenn du es gelesen hast. Ein Versprechen oder eine Frage, für die etwas erledigt werden muss, erhält eine eigene Aufgabe.

Frühere Besprechungen werden berücksichtigt, wenn eine Person von außerhalb an beiden Besprechungen teilnimmt, unabhängig davon, wie die Besprechungen genannt wurden und welche Adresse die Person verwendet hat. Das Briefing berücksichtigt die Notizen, die deine Machine hat: deine Notizen, die deiner Besprechungs-App oder die Notizen, die dir per Mail geschickt wurden. Andernfalls verwendet es das Transkript oder die Notizen im Kalendereintrag. Die neuesten Informationen zählen am meisten. Ein Punkt, der später geklärt wurde, wird nicht mehr als offen angezeigt.

Notizen und Nachrichten aus dem [Verlauf](history.md) werden ebenfalls berücksichtigt. So kann das Briefing auch Besprechungen einbeziehen, die vor deinem Einstieg stattgefunden haben.

Ein geschäftliches Briefing berücksichtigt keine privaten Notizen und keine Inhalte von der Machine einer anderen Person. Der Text bleibt bei dir: Bei einer Übergabe wird er nicht mitgegeben und er kann nicht zur Überprüfung weitergegeben werden. Wenn es keine Notizen gibt, werden diese Zeilen nicht angezeigt.

Das Briefing verwendet die Informationen, die bereits in deiner Machine gespeichert sind. Bei einer ersten Besprechung mit einer Person aus einem Unternehmen wird auch die Startseite der Unternehmenswebsite gelesen.

Wenn in OpenClaw ein Websuchanbieter eingerichtet ist (bei einer gehosteten Machine ist standardmäßig keiner eingerichtet), führt The Machine außerdem eine kurze Websuche nach dem Namen und Unternehmen der Person durch. Die Suchergebnisse werden mit einem Link angezeigt. Für die Suche werden nur der öffentliche Name der Person, der Unternehmensname und die Website verwendet, niemals deine Nachrichten. Die Suchergebnisse werden 30 Tage lang wiederverwendet.

So kann eine Besprechung, der du zum ersten Mal zugesagt hast, schon vor eurem ersten Gespräch ein Briefing erhalten: was das Unternehmen macht, was das für dich bedeutet und, sofern bekannt, wer die Person ist. Wenn nur ein Vorname bekannt ist, werden Suchergebnisse nur übernommen, wenn sie eindeutig auf eine Person verweisen. Wenn **Arbeitskontakte nachschlagen** deaktiviert ist (Einstellungen, Sicherheit), wird nichts nachgeschlagen.

Für eine wiederkehrende Besprechung wird nur dann ein Briefing erstellt, wenn seit dem letzten Termin etwas passiert ist: eine Nachricht, Notizen oder ein Versprechen. Das Briefing nennt die neuen Informationen, nicht die des letzten Briefings. Es wird erst erstellt, wenn der vorherige Termin vorbei ist, und höchstens für zwei wiederkehrende Besprechungen pro Tag.

Wenn es nichts Sinnvolles zu sagen gibt, wird keine Aufgabe erstellt. Für interne, private und abgesagte Besprechungen gibt es keine Aufgabe. Wird eine Besprechung verschoben, bleibt ihre Aufgabe bestehen und wird auf die neue Uhrzeit gesetzt. Eine verworfene Aufgabe erscheint nicht erneut. Die Aufgabe einer abgesagten Besprechung wird automatisch geschlossen.

Wenn eine Aktualisierung den Inhalt eines Briefings ändert, werden offene Briefings für noch bevorstehende Besprechungen einmal neu erstellt. Titel, Quellen und Position in deiner Liste bleiben erhalten. Ein Briefing, das du geändert, zurückgestellt oder geschlossen hast, bleibt unverändert. Das gilt auch für Besprechungen, die in den nächsten Minuten beginnen.

Die Details der Besprechung zeigen die dazugehörige Aufgabe unter **Aufgabe**, sodass du sie mit einem Tippen im Chat öffnen kannst.
