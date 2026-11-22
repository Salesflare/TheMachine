---
title: Versprechen
area: cards
summary: Was du versprochen hast und was andere dir versprochen haben. Wird automatisch erfasst.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: 176831c86d0a382a
---
Erfasse, was du versprochen hast und was andere dir versprochen haben. Deine Machine erkennt Versprechen in deinen Nachrichten automatisch.

## Wo du sie findest

Auf der Seite „Aufgaben“ unter **Versprechen**:

- Was du tun wolltest und für wen: **Du hast versprochen**.
- Was andere tun wollten: **Dir versprochen**.

Bei jedem Versprechen gibt es ein Menü **⋯**:

- Bei deinen Versprechen: **Ausführen**. Dadurch wird sofort eine Aufgabe daraus, und deine Machine bereitet sie vor. Bei den Versprechen anderer: **Erinnern**. Deine Machine erstellt dort, wo das Versprechen abgegeben wurde, einen kurzen Nachfassentwurf, während du in der Liste bleibst. Eine kurze Meldung sagt, dass der Entwurf unterwegs ist, und bietet **Aufgabe öffnen** an. Beim Versprechen steht dann „jetzt eine Aufgabe“. Nichts wird gesendet, bis du es selbst sendest. Ist daraus bereits eine Aufgabe geworden, wird diese geöffnet.
- **Als erledigt markieren**: Das Versprechen wurde eingehalten.
- **Findet nicht statt**: Es wird nicht passieren. Deine Machine verfolgt es nicht weiter und erstellt keine Aufgabe.

Ein offenes Versprechen wird rund um sein Datum automatisch auch zu einer Aufgabe: bei deinen am Morgen davor, damit du einen Tag Zeit hast, es zu erledigen, bei den Versprechen anderer am Morgen danach, falls es noch offen ist. Am entsprechenden Tag erscheint es auch im [Kalender](calendar.md). Ist daraus jetzt eine Aufgabe geworden, führt der Link zu ihr. **Als erledigt markieren** oder **Findet nicht statt** schließt auch diese Aufgabe. Wenn deine Machine erkennt, dass sie erledigt ist, werden beide geschlossen und ein entsprechender Hinweis angezeigt.

Eine Antwort, in der nur versprochen wird, die Aufgabe zu erledigen, etwa „Ich schicke die Dateien bis Dienstag“, schließt die Aufgabe nicht ab. Die Aufgabe bleibt mit diesem Datum offen, und das Versprechen ist mit ihr verknüpft. In der Prüfung vor dem Senden wird darauf hingewiesen.

Wurde das Versprechen bereits eingehalten, etwa durch eine von dir gesendete Antwort oder ein entsprechendes Meeting? Dann wird es automatisch geschlossen, ohne eine Aufgabe zu erstellen.

Wird später ein neues Datum genannt, etwa „stattdessen nächste Woche“? Dann wird dasselbe Versprechen samt Aufgabe verschoben, ohne eine zweite anzulegen. Auf der zugehörigen Seite stehen das neue Datum und die neuere Nachricht.

Ein Versprechen ohne Datum bekommt einen Tag fürs Nachfassen: drei Tage nachdem du es abgegeben hast, eine Woche nachdem andere es abgegeben haben. Ist es bis dahin noch offen, wird daraus eine Aufgabe.

Bei Versprechen aus Slack wird der Name der Person angezeigt.

Ein Versprechen per E-Mail von jemandem, dem du noch nie geschrieben hast, wird ebenfalls erfasst und als **Absender nicht bestätigt** markiert: Es gibt nur das Wort dieser Person. Die Aufgabe beginnt mit „Nicht bestätigt: Du hast dieser Person noch nie geschrieben.“

## Rückerstattungen

Wenn ein Geschäft, eine Fluggesellschaft, ein Vermieter oder eine Versicherung verspricht, dir Geld zurückzuzahlen, etwa eine Rückerstattung für eine stornierte Bestellung oder eine bewilligte Forderung, erfasst deine Machine den Betrag, wer zahlt und wann das Geld eingehen soll. Das Versprechen erscheint unter **Dir versprochen**. Allerdings nur, wenn alle drei Angaben aus der Nachricht hervorgehen.

Kommt das Geld zuerst zurück, etwa laut einer E-Mail mit „Rückerstattung bearbeitet“, einer Mitteilung des Zahlungsdienstes oder einer Benachrichtigung deiner Banking-App auf dem Handy, wird das Versprechen automatisch geschlossen, ohne eine Aufgabe zu erstellen.

Ist das Geld bis zu diesem Tag nicht eingegangen? Dann wird unauffällig eine Aufgabe erstellt: „Bei … wegen der Rückerstattung von €42 nachhaken“, mit einer kurzen E-Mail an die betreffende Stelle, in der die Bestell- oder Fallnummer genannt wird. Nichts wird gesendet, bis du es selbst sendest. Geht das Geld doch noch ein, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du sie für einen Tag wiederherstellen.

Der [Wochenrückblick](weekly-recap.md) zählt die eingehaltenen und offenen Versprechen. Auf deinem eigenen Computer listet `assistant promises` sie im Terminal auf.
