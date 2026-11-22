---
title: Versprechen
area: cards
summary: Was du versprochen hast und was andere dir versprochen haben. Wird automatisch erfasst.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: 22b81ed3f7c4801f
---
Behalte im Blick, was du versprochen hast und was andere dir versprochen haben. Deine Machine erkennt Versprechen in deinen Nachrichten automatisch.

## Wo du sie findest

Auf der Aufgaben-Seite unter **Versprechen**:

- Was du tun wolltest und für wen: **Du hast versprochen**.
- Was andere tun wollten: **Dir versprochen**.

Jedes Versprechen hat ein Menü **⋯**:

- **Ausführen** bei deinen Versprechen: Es wird sofort zu einer Aufgabe, und deine Machine bereitet sie vor. **Erinnern** bei den Versprechen anderer: Deine Machine erstellt einen kurzen Entwurf für eine Nachfrage dort, wo die Person das Versprechen gegeben hat. Du bleibst dabei in der Liste. Ein kurzer Hinweis sagt, dass die Nachricht unterwegs ist, mit **Aufgabe öffnen**. Beim Versprechen steht dann „jetzt eine Aufgabe“. Gesendet wird nichts, bis du es abschickst. Ist es bereits eine Aufgabe, wird diese geöffnet.
- **Als erledigt markieren**: Das Versprechen wurde gehalten.
- **Findet nicht statt**: Das Versprechen wird nicht erfüllt. Deine Machine verfolgt es nicht mehr und erstellt keine Aufgabe.

Ein offenes Versprechen wird rund um sein Datum automatisch zu einer Aufgabe: deine Versprechen am Morgen davor, damit du einen Tag Zeit hast, und die anderer am Morgen danach, sofern sie noch offen sind. Es erscheint an diesem Tag auch im [Kalender](calendar.md). Wurde es bereits zu einer Aufgabe, führt der Link dorthin. **Als erledigt markieren** oder **Findet nicht statt** schließt auch diese Aufgabe. Erkennt deine Machine, dass das Versprechen erfüllt wurde, werden beide geschlossen und ein Hinweis sagt dir Bescheid.

Wurde das Versprechen bereits erfüllt, zum Beispiel durch eine Antwort von dir oder ein Treffen, das die Sache geklärt hat? Dann wird es automatisch geschlossen, ohne dass eine Aufgabe erstellt wird.

Wird später ein neues Datum genannt, zum Beispiel „stattdessen nächste Woche“? Dasselbe Versprechen und die zugehörige Aufgabe werden verschoben. Es wird keine zweite Aufgabe erstellt. Auf der Seite des Versprechens stehen das neue Datum und die neuere Nachricht.

Bei Versprechen ohne Datum wird ein Tag für die **Nachfrage** festgelegt: drei Tage nach deinem Versprechen, eine Woche nach dem Versprechen der anderen Person. Ist es bis dahin noch offen, wird es zu einer Aufgabe.

Bei Versprechen aus Slack wird der Name der Person angezeigt.

Auch ein Versprechen per E-Mail von jemandem, dem du noch nie geschrieben hast, wird erfasst und als **Absender nicht bestätigt** markiert: Es beruht nur auf dessen Aussage. Die Aufgabe beginnt mit „Nicht bestätigt: Du hast dieser Person noch nie geschrieben.“

## Rückerstattungen

Verspricht dir ein Geschäft, eine Fluggesellschaft, ein Vermieter oder ein Versicherer Geld zurück, zum Beispiel eine Rückerstattung für eine stornierte Bestellung oder einen bewilligten Versicherungsfall, erfasst deine Machine den Betrag, den Zahlungspflichtigen und das voraussichtliche Eingangsdatum. Das Versprechen erscheint unter **Dir versprochen**. Nur wenn aus der Nachricht alle drei Angaben hervorgehen.

Geht das Geld zuerst ein, zum Beispiel laut einer E-Mail mit dem Hinweis „Rückerstattung bearbeitet“, einer Benachrichtigung des Zahlungsdienstes oder einer Mitteilung deiner Banking-App auf dem Handy, wird das Versprechen automatisch geschlossen. Eine Aufgabe wird nicht erstellt.

Ist das Geld bis zu diesem Tag nicht eingegangen? Dann wird eine unaufdringliche Aufgabe erstellt: „Rückerstattung über 42 € von … nachverfolgen“, zusammen mit einem kurzen E-Mail-Entwurf, in dem die Bestell- oder Fallnummer genannt wird. Gesendet wird nichts, bis du es abschickst. Geht das Geld doch noch ein, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Die [Wochenrückblick](weekly-recap.md) zählt erfüllte und offene Versprechen. Auf deinem eigenen Computer listet `assistant promises` sie in einem Terminal auf.
