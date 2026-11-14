---
title: Versprechen
area: cards
summary: Was du versprochen hast und was andere dir versprochen haben. Wird automatisch nachverfolgt.
covers: promises
code: dashboard.html, assistant.py
order: 6
translated: dbac0241c54b0ec6
---
Behalte im Blick, was du versprochen hast und was andere dir versprochen haben. Deine Machine erkennt Versprechen in deinen Nachrichten automatisch.

## Wo du sie findest

Auf der Seite „Aufgaben“ unter **Versprechen**:

- Was du tun wolltest und für wen: **Du hast versprochen**.
- Was andere tun wollten: **Dir versprochen**.

Jedes Versprechen hat ein Menü **⋯**:

- **Ausführen** bei deinen Versprechen: Daraus wird sofort eine Aufgabe, die deine Machine vorbereitet. **Erinnern** bei den Versprechen anderer: Deine Machine entwirft eine kurze Nachfrage dort, wo die Person es versprochen hat. Du bleibst dabei in der Liste. Eine kurze Notiz sagt, dass die Nachricht unterwegs ist, und enthält **Aufgabe öffnen**. Beim Versprechen steht dann „jetzt eine Aufgabe“. Gesendet wird nichts, bis du es selbst abschickst. Ist es bereits eine Aufgabe, öffnet sich diese.
- **Als erledigt markieren**: Das Versprechen wurde eingehalten.
- **Findet nicht statt**: Das Versprechen wird nicht eingehalten. Deine Machine verfolgt es nicht weiter und erstellt keine Aufgabe.

Ein offenes Versprechen wird automatisch zu einer Aufgabe, sobald es fällig ist. Bei deinen Versprechen passiert das am Morgen davor, damit du einen Tag Zeit hast. Außerdem erscheint es am entsprechenden Tag im [Kalender](calendar.md). Versprechen, die jetzt Aufgaben sind, sind mit diesen verknüpft. Wenn du **Als erledigt markieren** oder **Findet nicht statt** auswählst, wird auch die jeweilige Aufgabe geschlossen. Erkennt deine Machine, dass das Versprechen eingehalten wurde, schließt sie beides und vermerkt es.

Wurde das Versprechen bereits eingehalten, zum Beispiel durch eine Antwort von dir oder ein entsprechendes Meeting? Dann wird es automatisch geschlossen, ohne eine Aufgabe zu erstellen.

Wird später ein neuer Termin genannt, zum Beispiel „doch erst nächste Woche“? Dann wird das bestehende Versprechen samt Aufgabe verschoben, ohne ein zweites anzulegen. Auf der Seite des Versprechens siehst du den neuen Termin und die neuere Nachricht.

Für Versprechen ohne Termin wird ein Tag zum **Nachfassen** festgelegt: drei Tage, nachdem du das Versprechen abgegeben hast, oder eine Woche, nachdem es jemand anderes abgegeben hat. Ist es bis dahin noch offen, wird es zu einer Aufgabe.

Bei Versprechen aus Slack wird der Name der Person angezeigt.

Versprechen per E-Mail von Personen, denen du noch nie geschrieben hast, werden ebenfalls erfasst und als **Absender nicht bestätigt** markiert: Sie beruhen nur auf der Aussage der Person. Die Aufgabe beginnt mit „Nicht bestätigt: Du hast der Person noch nie geschrieben.“

Die [Wochenübersicht](weekly-recap.md) zählt eingehaltene und offene Versprechen. Auf deinem eigenen Computer listet `assistant promises` sie in einem Terminal auf.
