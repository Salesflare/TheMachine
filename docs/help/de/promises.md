---
title: Versprechen
area: cards
summary: Was du versprochen hast und was andere dir versprochen haben. Wird automatisch erfasst.
covers: promises
code: dashboard.html, assistant.py
order: 6
translated: dbac0241c54b0ec6
---
Behalte im Blick, was du versprochen hast und was andere dir versprochen haben. Deine Machine erkennt Versprechen in deinen Nachrichten automatisch.

## Wo du sie findest

Auf der Aufgaben-Seite unter **Versprechen**:

- Was du tun wolltest und für wen: **Du hast versprochen**.
- Was andere tun wollten: **Dir versprochen**.

Jedes Versprechen hat ein Menü mit **⋯**:

- **Ausführen** bei deinen Versprechen: Daraus wird sofort eine Aufgabe, und deine Machine bereitet sie vor. **Erinnern** bei den Versprechen anderer: Deine Machine erstellt einen kurzen Entwurf für eine Nachfrage dort, wo das Versprechen gemacht wurde, während du in der Liste bleibst. Eine kurze Notiz sagt, dass sie unterwegs ist, mit **Aufgabe öffnen**. Beim Versprechen steht „jetzt eine Aufgabe“. Gesendet wird erst, wenn du es abschickst. Ist es bereits eine Aufgabe, wird diese geöffnet.
- **Als erledigt markieren**: Das Versprechen wurde eingehalten.
- **Findet nicht statt**: Das Versprechen wird nicht eingehalten. Deine Machine verfolgt es nicht weiter und erstellt keine Aufgabe.

Ein offenes Versprechen wird automatisch zu einer Aufgabe, wenn es fällig ist. Bei deinen Versprechen passiert das am Morgen davor, damit du einen Tag Zeit hast. Außerdem wird es an diesem Tag im [Kalender](calendar.md) angezeigt. Ein Versprechen, das jetzt eine Aufgabe ist, ist mit ihr verknüpft. Wenn du **Als erledigt markieren** oder **Findet nicht statt** auswählst, wird auch die Aufgabe geschlossen. Erkennt deine Machine, dass das Versprechen eingehalten wurde, werden beide geschlossen und eine entsprechende Zeile wird angezeigt.

Wurde das Versprechen bereits eingehalten, zum Beispiel durch eine Antwort von dir oder ein Meeting, in dem es besprochen wurde? Dann wird es automatisch geschlossen, ohne dass eine Aufgabe erstellt wird.

Wurde später ein neues Datum genannt, etwa „stattdessen nächste Woche“? Dasselbe Versprechen wird verschoben, ebenso die zugehörige Aufgabe. Es wird keine zweite erstellt. Auf der Versprechensseite stehen das neue Datum und die neuere Nachricht.

Für ein Versprechen ohne Datum wird ein Tag für die **Nachfrage** festgelegt: drei Tage, nachdem du es gemacht hast, oder eine Woche, nachdem es die andere Person gemacht hat. Ist es bis dahin noch offen, wird es zu einer Aufgabe.

Bei Versprechen aus Slack wird der Name der Person angezeigt.

Ein Versprechen per E-Mail von jemandem, dem du noch nie geschrieben hast, wird ebenfalls erfasst und als **Absender nicht bestätigt** markiert: Es beruht nur auf dem Wort der Person. Die Aufgabe beginnt mit „Nicht bestätigt: Du hast der Person noch nie geschrieben.“

Die [Wochenübersicht](weekly-recap.md) zählt eingehaltene und offene Versprechen. Auf deinem eigenen Computer listet `assistant promises` sie in einem Terminal auf.
