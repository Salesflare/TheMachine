---
title: Versprechen
area: cards
summary: Was du zugesagt hast und was andere dir versprochen haben. Automatisch erfasst.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: ba0e2190e1b8b791
---
Behalte im Blick, was du versprochen hast und was andere dir versprochen haben. Deine Machine erkennt Versprechen in deinen Nachrichten automatisch.

## Wo du sie findest

Auf der Aufgaben-Seite unter **Versprechen**:

- Was du zugesagt hast und für wen: **Du hast versprochen**.
- Was andere zugesagt haben: **Dir versprochen**.

Jeder Eintrag hat ein Menü **⋯**:

- **Ausführen** bei deinen Versprechen: Daraus wird sofort eine Aufgabe, die deine Machine vorbereitet. **Erinnern** bei den Versprechen anderer: Deine Machine entwirft eine kurze Nachfrage dort, wo die Person das Versprechen gemacht hat. Du bleibst dabei in der Liste. Ein kurzer Hinweis sagt, dass die Nachricht unterwegs ist, mit **Aufgabe öffnen**. Beim Versprechen steht „jetzt eine Aufgabe“. Nichts wird gesendet, bevor du es abschickst. Ist es bereits eine Aufgabe, wird diese geöffnet.
- **Erledigt markieren**: Das Versprechen wurde eingehalten.
- **Findet nicht statt**: Das Versprechen wird nicht eingehalten. Deine Machine verfolgt es nicht weiter und erstellt keine Aufgabe.

Ein offenes Versprechen wird um sein Datum herum automatisch zu einer Aufgabe: deine am Morgen davor, damit du einen Tag Zeit hast, und das Versprechen einer anderen Person am Morgen danach, falls es noch offen ist. Am entsprechenden Tag erscheint es auch im [Kalender](calendar.md). Ist es jetzt eine Aufgabe, führt der Link dorthin. Wenn du **Erledigt markieren** oder **Findet nicht statt** auswählst, wird auch die Aufgabe geschlossen. Erkennt deine Machine, dass das Versprechen eingehalten wurde, werden beide geschlossen und ein Hinweis sagt dir Bescheid.

Eine Antwort, in der nur versprochen wird, die Aufgabe zu erledigen, etwa „Ich schicke die Dateien bis Dienstag“, schließt sie nicht ab. Die Aufgabe bleibt mit diesem Datum offen und das Versprechen ist mit ihr verknüpft. Bei der Versandprüfung wird darauf hingewiesen, bevor du die Nachricht sendest.

Wurde das Versprechen bereits eingehalten, etwa durch eine Antwort, die du gesendet hast, oder ein Meeting, in dem es erledigt wurde? Dann wird es automatisch geschlossen, ohne eine Aufgabe zu erstellen.

Wenn jemand auf ein eigenes Versprechen antwortet, bleibt es offen, bis aus der Antwort hervorgeht, dass es eingehalten wurde. Ein „Klar“, eine automatische Antwort oder die Erledigung eines Teils reicht nicht. War eine Nachfrage zum Senden vorgemerkt, wird sie abgebrochen. Die Aufgabe bleibt offen und es erscheint der Hinweis „Die Person hat wieder geschrieben“.

Wird später ein neues Datum genannt, etwa „stattdessen nächste Woche“? Dann wird dasselbe Versprechen samt Aufgabe verschoben, ohne dass ein zweites erstellt wird. Auf der Seite dazu stehen das neue Datum und die neuere Nachricht.

Bei einem Versprechen ohne Datum wird ein **Nachfasstag** festgelegt: drei Tage, nachdem du es gemacht hast, oder eine Woche, nachdem es die andere Person gemacht hat. Ist es dann noch offen, wird es zu einer Aufgabe.

Bei Versprechen aus Slack wird der Name der Person angezeigt.

Auch ein Versprechen per E-Mail von jemandem, dem du noch nie geschrieben hast, wird erfasst. Es ist als **Absender nicht bestätigt** gekennzeichnet: Das Versprechen beruht nur auf dessen Aussage. Die Aufgabe beginnt mit „Nicht bestätigt: Du hast der Person noch nie geschrieben.“

## Rückerstattungen

Wenn ein Geschäft, eine Fluggesellschaft, ein Vermieter oder eine Versicherung dir eine Rückerstattung verspricht, etwa für eine stornierte Bestellung oder einen genehmigten Antrag, erfasst deine Machine den Betrag, wer zahlt und wann das Geld eingehen soll. Der Eintrag erscheint unter **Dir versprochen**. Das passiert nur, wenn aus der Nachricht alle drei Angaben hervorgehen.

Geht das Geld zuerst ein, etwa laut einer E-Mail mit „Rückerstattung bearbeitet“, einer Benachrichtigung eines Zahlungsdienstes oder einer Mitteilung deiner Banking-App auf deinem Handy, wird der Eintrag automatisch geschlossen, ohne eine Aufgabe zu erstellen.

Ist das Geld bis zu diesem Tag nicht eingegangen? Dann erscheint eine einzelne, unaufdringliche Aufgabe: „Der Rückerstattung über 42 € von … nachgehen“, zusammen mit einer kurzen E-Mail an die zuständige Stelle, in der die Bestell- oder Fallnummer genannt wird. Nichts wird gesendet, bevor du es abschickst. Geht das Geld doch noch ein, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Der [Wochenrückblick](weekly-recap.md) zählt die eingehaltenen und offenen Versprechen. Auf deinem eigenen Computer listet `assistant promises` sie in einem Terminal auf.
