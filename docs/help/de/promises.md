---
title: Versprechen
area: cards
summary: Was du zugesagt hast und was andere dir versprochen haben. Wird automatisch erfasst.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: 176831c86d0a382a
---
Behalte im Blick, was du versprochen hast und was andere dir versprochen haben. Deine Machine erkennt Versprechen in deinen Nachrichten automatisch.

## Wo du sie findest

Unter **Versprechen** auf der Aufgabenseite:

- Was du zugesagt hast und für wen: **Du hast versprochen**.
- Was andere zugesagt haben: **Dir versprochen**.

Zu jedem Eintrag gibt es ein Menü **⋯**:

- **Ausführen** bei deinen Versprechen: Daraus wird sofort eine Aufgabe, die deine Machine vorbereitet. **Erinnern** bei den Versprechen anderer: Deine Machine entwirft eine kurze Nachfassnachricht an der Stelle, an der das Versprechen gemacht wurde. Du bleibst dabei in der Liste. Ein kurzer Hinweis sagt, dass die Nachricht unterwegs ist, und enthält **Aufgabe öffnen**. Beim Versprechen steht dann „jetzt eine Aufgabe“. Gesendet wird erst, wenn du die Nachricht sendest. Ist es bereits eine Aufgabe, öffnet sich diese.
- **Als erledigt markieren**: Das Versprechen wurde eingehalten.
- **Findet nicht statt**: Das Versprechen wird nicht eingehalten. Deine Machine erfasst es nicht weiter und erstellt keine Aufgabe.

Ein offenes Versprechen wird zum angegebenen Datum auch automatisch zu einer Aufgabe: bei deinen Versprechen am Morgen davor, damit du einen Tag Zeit hast, und bei den Versprechen anderer am Morgen danach, falls es noch offen ist. Es erscheint an diesem Tag auch im [Kalender](calendar.md). Ist es bereits eine Aufgabe, führt der Link direkt dorthin. **Als erledigt markieren** oder **Findet nicht statt** schließt dann auch die Aufgabe. Wenn deine Machine erkennt, dass sie erledigt ist, werden beide geschlossen und ein Hinweis dazu angezeigt.

Eine Antwort, in der nur die Arbeit zugesagt wird, wie „Ich schicke die Dateien bis Dienstag“, erledigt die Aufgabe nicht. Die Aufgabe bleibt mit diesem Datum offen und das Versprechen ist mit ihr verknüpft. In der Prüfung vor dem Senden wird darauf hingewiesen.

Wurde das Versprechen bereits eingehalten, etwa durch eine gesendete Antwort oder ein entsprechendes Meeting? Dann wird es automatisch geschlossen, ohne dass eine Aufgabe erstellt wird.

Wird später ein neues Datum genannt, etwa „doch erst nächste Woche“? Dasselbe Versprechen wird verschoben, ebenso die zugehörige Aufgabe. Es wird keine zweite erstellt. Auf der Seite des Versprechens stehen das neue Datum und die neuere Nachricht.

Bei Versprechen ohne Datum wird ein Nachfasstermin festgelegt: drei Tage, nachdem du das Versprechen gegeben hast, oder eine Woche, nachdem andere es gegeben haben. Ist es bis dahin noch offen, wird es zu einer Aufgabe.

Bei Versprechen aus Slack wird der Name der Person angezeigt.

Ein Versprechen per E-Mail von jemandem, dem du noch nie geschrieben hast, wird ebenfalls erfasst und mit **Absender nicht bestätigt** gekennzeichnet: Es basiert nur auf der Aussage dieser Person. Die Aufgabe beginnt mit „Nicht bestätigt: Du hast dieser Person noch nie geschrieben.“

## Rückerstattungen

Wenn ein Geschäft, eine Fluggesellschaft, ein Vermieter oder ein Versicherer dir Geld zurückverspricht, etwa eine Rückerstattung für eine stornierte Bestellung oder einen genehmigten Versicherungsfall, erfasst deine Machine den Betrag, wer ihn zahlt und bis wann er eingehen soll. Das Versprechen erscheint unter **Dir versprochen**. Aber nur, wenn die Nachricht alle drei Angaben eindeutig enthält.

Geht das Geld zuerst ein, etwa durch eine E-Mail mit dem Hinweis „Rückerstattung bearbeitet“, eine Benachrichtigung eines Zahlungsdienstes oder eine Mitteilung deiner Banking-App auf dem Handy, wird das Versprechen automatisch geschlossen, ohne dass eine Aufgabe erstellt wird.

Ist das Geld bis zu diesem Tag nicht eingegangen? Dann erscheint unauffällig eine Aufgabe: „Der Rückerstattung über 42 € von … nachgehen“. Dazu wird eine kurze E-Mail an den Absender entworfen, in der die Bestell- oder Fallnummer genannt wird. Gesendet wird erst, wenn du die Nachricht sendest. Geht das Geld doch noch ein, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Die [Wochenrückblick](weekly-recap.md) zählt eingehaltene und offene Versprechen. Auf deinem eigenen Computer listet `assistant promises` sie in einem Terminal auf.
