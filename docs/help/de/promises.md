---
title: Versprechen
area: cards
summary: Was du tun wolltest und was andere dir versprochen haben. Wird automatisch erfasst.
covers: promises
code: dashboard.html, assistant.py
order: 6
translated: 8e5ce7b371ab7fd0
---
Behalte im Blick, was du versprochen hast und was andere dir versprochen haben. Deine Machine erkennt Versprechen in deinen Nachrichten automatisch.

## Wo du sie findest

Unter **Versprechen** auf der Aufgaben-Seite:

- Was du tun wolltest und für wen: **Du hast versprochen**.
- Was andere tun wollten: **Dir versprochen**.

Jedes Versprechen hat ein Menü **⋯**:

- **Ausführen** bei deinen Versprechen: Es wird sofort zu einer Aufgabe und deine Machine bereitet sie vor. **Erinnern** bei den Versprechen anderer: Deine Machine erstellt einen kurzen Entwurf als Follow-up an der Stelle, an der die Person es versprochen hat. Du bleibst dabei auf der Liste. Eine kurze Notiz sagt, dass der Entwurf unterwegs ist, mit **Aufgabe öffnen**. Beim Versprechen steht dann „jetzt eine Aufgabe“. Nichts wird gesendet, bis du es sendest. Ist es bereits eine Aufgabe, öffnet sich diese.
- **Als erledigt markieren**: Das Versprechen wurde eingehalten.
- **Findet nicht statt**: Das Versprechen wird nicht eingelöst. Deine Machine verfolgt es dann nicht weiter und erstellt keine Aufgabe.

Ein offenes Versprechen wird um sein Datum herum automatisch zu einer Aufgabe: Deine Versprechen am Morgen davor, damit du einen Tag Zeit hast, sie zu erledigen. Die Versprechen anderer am Morgen danach, sofern sie noch offen sind. Außerdem erscheint es an diesem Tag im [Kalender](calendar.md). Ist es jetzt eine Aufgabe, führt der Link zu dieser Aufgabe. **Als erledigt markieren** oder **Findet nicht statt** schließt auch die Aufgabe. Erkennt deine Machine, dass das Versprechen eingehalten wurde, schließt sie beides und fügt eine entsprechende Zeile hinzu.

Wurde das Versprechen schon eingehalten, etwa durch eine Antwort von dir oder ein Treffen, das die Sache geklärt hat? Dann wird es automatisch geschlossen, ohne Aufgabe.

Wird später ein neues Datum genannt, etwa „stattdessen nächste Woche“? Das Versprechen wird verschoben, ebenso die dazugehörige Aufgabe. Es wird keine zweite Aufgabe erstellt. Auf der Seite des Versprechens stehen das neue Datum und die neuere Nachricht.

Ein Versprechen ohne Datum bekommt einen **Tag zum Nachfassen**: drei Tage, nachdem du es gemacht hast, oder eine Woche, nachdem die andere Person es gemacht hat. Ist es dann noch offen, wird es zu einer Aufgabe.

Bei Versprechen aus Slack wird der Name der Person angezeigt.

Ein Versprechen per E-Mail von jemandem, dem du noch nie geschrieben hast, wird ebenfalls erfasst und als **Absender nicht bestätigt** markiert: Es basiert allein auf der Aussage dieser Person. Die Aufgabe beginnt mit „Nicht bestätigt: Du hast dieser Person noch nie geschrieben.“

Der [Wochenrückblick](weekly-recap.md) zählt eingehaltene und offene Versprechen. Auf deinem eigenen Computer listet `assistant promises` sie in einem Terminal auf.
