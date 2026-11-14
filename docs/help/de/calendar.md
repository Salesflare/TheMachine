---
title: Kalender
area: calendar
summary: Die kommende Woche auf einen Blick: Termine, fällige Aufgaben, zurückgestellte Aufgaben und Versprechen.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py
order: 1
translated: 7187a83e373922b3
---
## Was angezeigt wird

Deine Tage ab heute mit:

- Terminen aus den Kalendern, die du verbunden hast,
- Aufgaben, die an diesem Tag fällig sind, und zurückgestellten Aufgaben an dem Tag, an dem sie wieder anstehen,
- Rückfragen zu übergebener Arbeit,
- Versprechen mit einem Datum.

Ein Termin in zwei Kalendern wird nur einmal angezeigt. Ein Kalender, den jemand mit dir geteilt hat, zeigt die Termine der Person abgeblendet und mit ihrem Vornamen an. Daraus entstehen nie Aufgaben. Ganztägige und mehrtägige Termine werden an jedem betroffenen Tag als ganztägig angezeigt.

Ein gemeinsam erstellter Plan ist ein Versprechen. Es ist mit „Mit“ und dem Namen der anderen Person gekennzeichnet. Ein Versprechen zu einem Termin an diesem Tag mit derselben Person wird in der Zeile des Termins angezeigt.

**Überfällig** wird zuerst angezeigt. Bei einem Termin mit einer offenen Aufgabe wird deren Status angezeigt: **Vorbereitung bereit**, **Wird vorbereitet** oder **Aufgabe**. Eine Aufgabe, die erledigt scheint (du hast bereits geantwortet oder ihr Durchlauf hat ergeben, dass sie erledigt ist), wird nicht als **Fällig** angezeigt.

## Agenda, Woche oder Monat

- **Agenda** listet jeden Tag auf. Scrolle nach unten zu späteren Tagen oder nach oben (oder wähle **Frühere Tage anzeigen**) zu früheren Tagen. Die Agenda reicht bis eine Woche vor dem Verbinden deines Kalenders zurück. Oben steht, ab welchem Tag sie angezeigt wird. Sobald der [Verlauf](history.md) geladen ist, reicht sie etwa ein Jahr zurück.
- **Woche** zeigt eine Ansicht von Montag bis Sonntag. Auf dem Smartphone werden drei Tage angezeigt.
- **Monat** zeigt den ganzen Monat. Auf dem Computer werden bis zu drei Einträge pro Tag angezeigt. Auf dem Smartphone siehst du Punkte. Tippe auf einen Tag, um die Einträge dafür aufzulisten.

Mit **Heute**, ‹ und › oben wechselst du zwischen Wochen oder Monaten. Die ausgewählte Ansicht wird auf diesem Gerät gespeichert.

In der Wochenansicht stehen Termine zur selben Zeit nebeneinander und bleiben dabei gut lesbar. Weitere Termine werden als **+N** angezeigt. Tippe darauf, um den Tag in der Agenda zu öffnen.

## Etwas öffnen

Klicke auf eine Zeile, um den Chat zur Aufgabe, das Versprechen oder den Termin zu öffnen. Bei einem Termin, den du hier nicht ändern kannst, etwa einem Termin von jemand anderem oder einem mit Gästen, werden die Details angezeigt: wann, wo und wer. Personen, die dein Graph kennt, sowie die Organisationen und Projekte des Termins führen zu ihren jeweiligen Seiten. **In Google Kalender öffnen** (oder **In Outlook öffnen**) darunter öffnet den Termin dort. Das Ansehen ändert nichts.

Ein für einen Termin gebuchter Besprechungsraum wird unter „Wo“ angezeigt, nie als Person oder in deinem Graph.

Ein Meeting-Link wird mit dem Namen des Dienstes angezeigt, zum Beispiel Zoom, Google Meet oder Teams, oder als **Videoanruf**. Öffne den Termin, um teilzunehmen.

## Notizen und Transkript zum Termin

Die Details eines Termins haben zwei Bereiche. **Notizen** enthalten die Zusammenfassung: Entscheidungen und Aufgaben. **Transkript** enthält wortwörtlich, was gesagt wurde. Das Transkript ist zunächst eingeklappt und zeigt seine Dauer an. Mit **Anzeigen** öffnest du es.

Wenn die Inhalte nicht geladen werden, versucht es die App etwa eine halbe Minute lang automatisch erneut. Tippe danach auf **Erneut versuchen**.

Für jeden Bereich gibt es eigene Optionen: **Notizen hinzufügen** oder **Transkript hinzufügen**, **Datei hochladen** für eine Markdown- oder Textdatei, **Bearbeiten** und **Entfernen** (zweimal tippen). Inhalte bleiben in dem Bereich, in dem du sie hinzugefügt hast. Bei einem Termin, den du ändern kannst, öffnet **Notizen** unter dem Formular die Notizen.

Wenn [Zoom](zoom.md) oder [Google Meet](google-meet.md) verbunden ist, werden die Notizen unter „Notizen“ und das Transkript unter „Transkript“ angezeigt. Sie sind mit **Von Zoom** oder **Von Google Meet** gekennzeichnet. Bereits hinzugefügte Inhalte werden dadurch nie ersetzt. Wenn beides vorhanden ist, wird beides angezeigt.

Notizen können auch im Kalendereintrag des Termins selbst, nach Beginn des Termins, oder per Mail von Zoom oder Gemini eingehen. Nach dem Termin erstellt The Machine daraus nur dann Aufgaben, wenn es klare nächste Schritte gibt. Kommen dieselben Notizen auf zwei Wegen an, entsteht eine einzige Aufgabe, deren Quelle der Termin ist: **Notizen vom** Termin.

Für einen Termin mit Transkript, aber ohne Notizen, gibt es die Option **Notizen erstellen**. The Machine erstellt sie anhand des Transkripts: eine kurze Zusammenfassung, Entscheidungen und Aufgaben mit den jeweils zuständigen Personen, und zwar in der Sprache des Termins.

Die Anzeige **Notizen werden geschrieben…** bleibt auch dann aktiv, wenn du den Termin schließt. Bei einem langen Termin dauert es ein paar Minuten. Dafür wird dein eigenes Modell verwendet. Die Notizen sind mit **Von The Machine verfasst** gekennzeichnet und ersetzen nie Notizen, die du hinzugefügt hast.

The Machine kann die Notizen auch hinzufügen. Bitte sie in einer Aufgabe darum, zum Beispiel: „Füge das Transkript zur heutigen Vorstandssitzung hinzu.“ Ein Transkript kommt unter „Transkript“, eine Zusammenfassung unter „Notizen“. Bei einem Termin mit solchen Inhalten wird im Kalender **Notizen** oder **Transkript** angezeigt.

The Machine liest beides, um die nächsten Schritte des Termins zu ermitteln. Sie werden wie der Termin als Arbeit oder Privat gekennzeichnet und nur dann mit deinem Team geteilt, wenn auch der Termin mit deinem Team geteilt wird.

Die Details eines Termins werden überall gleich angezeigt, wo du ihn öffnest: in einer Zeitleiste, in einer Nachrichtensuche oder als Quelle einer Aufgabe. Unter **Ursprüngliche Einladung** am unteren Rand siehst du die Einladung so, wie sie eingegangen ist.

## Termin hinzufügen oder ändern

Deinen eigenen Google Kalender kannst du hier ändern. Outlook und andere Kalender lassen sich hier nur ansehen. Mit **Neuer Termin** fügst du einen Termin hinzu (auf dem Smartphone findest du die Option unter **+** in der oberen Leiste): Wähle den Kalender, einen Titel und die Uhrzeit. Klicke auf einen Termin in diesem Kalender, zu dem keine Gäste eingeladen sind, um ihn zu ändern oder **Löschen**, um ihn zu löschen (zweimal tippen).

**Wo** schlägt dir beim Tippen Orte vor: zuerst zuvor verwendete Orte und deine Organisationen, dann Adressen von [OpenStreetMap](https://www.openstreetmap.org), einer kostenlosen Karte. Zur Suche werden nur die Wörter gesendet, die du eingibst. Wähle einen Vorschlag aus oder lass deinen eigenen Text stehen.

Mit **Einladen** fügst du Personen aus deinem Graph oder eine beliebige E-Mail-Adresse hinzu. Diese Option gibt es nur in deinem eigenen Kalender. Über der Schaltfläche steht, wer eine Einladung erhält. Auf der Schaltfläche steht auch die Anzahl der Eingeladenen: **Hinzufügen und 2 einladen**. Google versendet die Einladungen erst, wenn du auf die Schaltfläche tippst. Ohne Gäste wird niemand eingeladen und niemand erhält eine Aktualisierung.

Eine Aufgabe kann auch eine Änderung vorschlagen, zum Beispiel einen Abholtermin, den du hinzufügen kannst. Sie zeigt genau, was geändert wird. Erst wenn du auf **Hinzufügen**, **Speichern** oder **Löschen** tippst, wird die Änderung vorgenommen.

Noch keine Termine? Wenn du keinen Kalender verbunden hast, öffnet **Kalender verbinden** die Verbindungen. Dort kannst du [Google Kalender](google-calendar.md), [Outlook-Kalender](microsoft.md) oder [einen anderen Kalender](other-calendars.md) verbinden.

## Überschneidungen mit deinem anderen Kalender

Wenn sich ein geschäftlicher Termin mit etwas in deinem privaten Kalender überschneidet oder umgekehrt, erstellt The Machine eine Aufgabe zum neueren der beiden Termine. Sie kann einen kurzen Textentwurf zum Verschieben erstellen oder vorschlagen, den Termin abzusagen. Es wird nichts gesendet, bis du es bestätigst.

Ganztägige, als frei markierte und vorläufige Termine werden nie berücksichtigt. Jede Überschneidung wird nur einmal angezeigt. Eine Aufgabe für die Arbeit weist nur auf den Konflikt hin, damit dein Team den privaten Termin nicht sieht. Nur du siehst, womit er sich überschneidet.

## Gut vorbereitet auf deine Termine

Vor einem Termin mit Personen außerhalb deines Unternehmens erstellt The Machine eine Aufgabe: **Vorbereitung für** den Termin. Sie enthält eine kurze Zusammenfassung:

- **Wer:** Wer die Personen sind, basierend auf deinem Graph.
- **Letzter Kontakt:** Dein letzter Austausch mit ihnen. Nach dem Termin ist diese Nachricht die Quelle der Aufgabe.
- **Offene Versprechen:** Was du oder die anderen Personen noch erledigen müssen.
- **Offene Fragen:** Was noch unbeantwortet ist.
- **Entscheiden oder mitbringen:** Was noch zu klären ist oder mitgebracht werden soll.

Die Aufgabe erscheint morgens an einem Arbeitstag: am Tag des Termins, wenn er nachmittags stattfindet, andernfalls am vorherigen Arbeitstag. Sie nutzt nur Informationen, die bereits auf deiner Machine vorhanden sind. Sie ist nur zum Lesen gedacht. Wenn du sie gelesen hast, markiere sie als **Erledigt**. Ein Versprechen oder eine Frage darin, für die etwas getan werden muss, hat eine eigene Aufgabe.

Gibt es keinen nützlichen Verlauf, wird keine Aufgabe erstellt. Bei wiederkehrenden, internen oder privaten Terminen sowie bei abgesagten Terminen wird keine erstellt. Wird ein Termin verschoben, bleibt die eine Aufgabe bestehen und erscheint zur neuen Uhrzeit. Eine verworfene Aufgabe erscheint nicht wieder. Die Aufgabe zu einem abgesagten Termin wird automatisch geschlossen.

In den Termindetails findest du die Aufgabe unter **Aufgabe**. Tippe darauf, um ihren Chat zu öffnen.
