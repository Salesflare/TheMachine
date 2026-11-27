---
title: Versprechen
area: cards
summary: Was du zugesagt hast und was andere dir versprochen haben. Wird automatisch erfasst.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: b624394de7ff77b1
---
Behalte im Blick, was du versprochen hast und was andere dir versprochen haben. Deine Machine erkennt Versprechen in deinen Nachrichten automatisch.

## Wo du sie findest

Auf der Seite „Aufgaben“ unter **Versprechen**:

- Was du für wen tun wolltest: **Du hast versprochen**.
- Was andere tun wollten: **Dir versprochen**.

Jedes Versprechen hat ein Menü **⋯**:

- **Ausführen** bei deinen Versprechen: Daraus wird sofort eine Aufgabe, die deine Machine vorbereitet. **Erinnern** bei den Versprechen anderer: Deine Machine entwirft eine kurze Nachfrage an der Stelle, an der sie es versprochen haben. Du bleibst dabei in der Liste. Ein kurzer Hinweis sagt, dass die Nachricht unterwegs ist, mit **Aufgabe öffnen**. Beim Versprechen steht „jetzt eine Aufgabe“. Gesendet wird erst, wenn du die Nachricht abschickst. Ist es bereits eine Aufgabe, öffnet sich diese.
- **Als erledigt markieren**: Das Versprechen wurde eingehalten.
- **Findet nicht statt**: Es wird nicht passieren. Deine Machine verfolgt es nicht weiter und erstellt keine Aufgabe.

Ein offenes Versprechen wird um sein Datum herum automatisch auch zu einer Aufgabe: deine am Morgen davor, damit du einen Tag Zeit hast, die der anderen am Morgen danach, falls sie noch offen ist. Es erscheint an seinem Tag im [Kalender](calendar.md). Ist es jetzt eine Aufgabe, führt der Link dorthin. Mit **Als erledigt markieren** oder **Findet nicht statt** wird auch diese Aufgabe geschlossen. Erkennt deine Machine, dass es erledigt ist, werden beide geschlossen und ein Hinweis sagt Bescheid.

Eine Antwort, in der nur die Arbeit versprochen wird, etwa „Ich schicke die Dateien bis Dienstag“, schließt die Aufgabe nicht ab. Die Aufgabe bleibt mit diesem Datum offen und das Versprechen ist mit ihr verknüpft. Bei der Prüfung vor dem Senden wird darauf hingewiesen. Änderst du den Text vorher, entfallen das alte Versprechen und das Datum. Die Aufgabe bleibt offen, bis deine Machine erkennt, dass die Arbeit erledigt ist. Ein Versprechen in deiner gesendeten Nachricht wird dann mit ihr verknüpft.

Wurde es bereits eingehalten, etwa durch eine Antwort, die du gesendet hast, oder ein Meeting, in dem es erledigt wurde? Dann wird es automatisch geschlossen, ohne Aufgabe.

Wenn jemand auf ein eigenes Versprechen antwortet, bleibt es offen, bis aus der Antwort hervorgeht, dass es eingehalten wurde. Ein „Klar“ oder ein Teil der Antwort reicht nicht. Sollte eine Nachfrage noch gesendet werden, wird sie abgebrochen und die Aufgabe bleibt mit dem Hinweis „Sie haben wieder geschrieben“ offen. Eine Abwesenheitsnotiz ändert nichts.

Wird ein späteres neues Datum genannt, etwa „stattdessen nächste Woche“? Dasselbe Versprechen und auch die dazugehörige Aufgabe werden verschoben. Es wird keine zweite Aufgabe angelegt. Auf der Seite des Versprechens stehen das neue Datum und die neuere Nachricht.

Bei Versprechen ohne Datum wird ein **Nachfasstag** festgelegt: drei Tage, nachdem du es gemacht hast, oder eine Woche, nachdem die andere Person es gemacht hat. Ist es dann noch offen, wird es zu einer Aufgabe.

Bei Versprechen aus Slack wird der Name der Person angezeigt.

Ein Versprechen per E-Mail von jemandem, dem du noch nie geschrieben hast, wird ebenfalls erfasst und als **Absender nicht bestätigt** gekennzeichnet: Es beruht nur auf dem Wort der Person. Die Aufgabe beginnt mit „Nicht bestätigt: Du hast der Person noch nie geschrieben.“

## Rückerstattungen

Verspricht dir ein Geschäft, eine Fluggesellschaft, ein Vermieter oder ein Versicherer, Geld zurückzuzahlen, etwa für eine stornierte Bestellung oder einen genehmigten Antrag, erfasst deine Machine den Betrag, den Zahlungspflichtigen und das erwartete Datum. Das Versprechen erscheint unter **Dir versprochen**. Aber nur, wenn alle drei Angaben aus der Nachricht hervorgehen.

Kommt das Geld zuerst zurück, etwa laut einer E-Mail mit „Rückerstattung bearbeitet“, einer Mitteilung eines Zahlungsdienstes oder einer Benachrichtigung deiner Banking-App auf deinem Handy, wird das Versprechen automatisch geschlossen, ohne Aufgabe.

Ist das Geld bis zu diesem Datum nicht eingegangen? Dann wird eine einzelne, unaufdringliche Aufgabe erstellt: „Die Rückerstattung über 42 € bei … nachverfolgen“. Dazu wird eine kurze E-Mail an den Zahlungspflichtigen entworfen, in der die Bestell- oder Vorgangsnummer genannt wird. Gesendet wird erst, wenn du die Nachricht abschickst. Geht das Geld doch noch ein, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Die [wöchentliche Zusammenfassung](weekly-recap.md) zählt eingehaltene und offene Versprechen. Auf deinem eigenen Computer listet `assistant promises` sie in einem Terminal auf.
