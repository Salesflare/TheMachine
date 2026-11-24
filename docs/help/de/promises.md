---
title: Versprechen
area: cards
summary: Was du versprochen hast und was andere dir versprochen haben. Wird automatisch erfasst.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: 0bc6594bbd8f4c0b
---
Behalte im Blick, was du versprochen hast und was andere dir versprochen haben. Deine Machine erkennt Versprechen in deinen Nachrichten automatisch.

## Wo du sie findest

Unter **Versprechen** auf der Aufgabenseite:

- Was du tun wolltest und für wen: **Du hast versprochen**.
- Was andere tun wollten: **Dir versprochen**.

Jedes Versprechen hat ein **⋯**-Menü:

- **Ausführen** bei deinen Versprechen: Daraus wird sofort eine Aufgabe, die deine Machine vorbereitet. **Erinnern** bei den Versprechen anderer: Deine Machine entwirft eine kurze Nachfassnachricht an der Stelle, an der die Person das Versprechen abgegeben hat. Du bleibst dabei in der Liste. Ein kurzer Hinweis sagt, dass die Nachricht unterwegs ist, und enthält **Aufgabe öffnen**. Beim Versprechen steht dann „jetzt eine Aufgabe“. Gesendet wird erst, wenn du die Nachricht abschickst. Wenn es bereits eine Aufgabe ist, wird diese geöffnet.
- **Als erledigt markieren**: Das Versprechen wurde eingehalten.
- **Findet nicht statt**: Es wird nicht passieren. Deine Machine verfolgt das Versprechen nicht weiter und erstellt keine Aufgabe.

Ein offenes Versprechen wird rund um das zugehörige Datum automatisch zu einer Aufgabe: deines am Morgen davor, damit du einen Tag Zeit hast, ihres am Morgen danach, falls es noch offen ist. Es wird an diesem Tag auch im [Kalender](calendar.md) angezeigt. Wenn es jetzt eine Aufgabe ist, führt der Link dorthin. Mit **Als erledigt markieren** oder **Findet nicht statt** wird auch diese Aufgabe geschlossen. Wenn deine Machine erkennt, dass es erledigt ist, werden beide geschlossen und ein Hinweis dazu angezeigt.

Eine Antwort, in der nur versprochen wird, die Aufgabe zu erledigen, zum Beispiel „Ich schicke die Dateien bis Dienstag“, schließt die Aufgabe nicht ab. Die Aufgabe bleibt mit diesem Datum offen und das Versprechen ist damit verknüpft. Bei der Versandprüfung steht ein entsprechender Hinweis, bevor du die Nachricht abschickst.

Wurde das Versprechen bereits eingehalten, etwa durch eine Antwort von dir oder ein entsprechendes Meeting? Dann wird es automatisch geschlossen und keine Aufgabe erstellt.

Wenn jemand auf ein eigenes Versprechen antwortet, bleibt es offen, bis aus der Antwort hervorgeht, dass es eingehalten wurde. Ein „Klar“ oder die Erledigung eines Teils reicht nicht. Falls eine Nachfassnachricht zum Senden bereitstand, wird sie abgebrochen und die Aufgabe bleibt mit dem Hinweis „Sie haben wieder geschrieben“ offen. Eine Abwesenheitsnotiz ändert nichts.

Wird später ein neues Datum genannt, etwa „stattdessen nächste Woche“? Dann wird dasselbe Versprechen verschoben, ebenso die zugehörige Aufgabe. Es wird keine zweite Aufgabe erstellt. Auf der Seite des Versprechens stehen das neue Datum und die neuere Nachricht.

Bei einem Versprechen ohne Datum wird ein Tag zum **Nachfassen** festgelegt: drei Tage nach deinem Versprechen, eine Woche nach dem Versprechen der anderen Person. Ist es dann noch offen, wird es zu einer Aufgabe.

Bei Versprechen aus Slack wird der Name der Person angezeigt.

Auch ein Versprechen per E-Mail von jemandem, dem du noch nie geschrieben hast, wird erfasst. Es ist mit **Absender nicht bestätigt** gekennzeichnet: Es beruht nur auf dem Wort dieser Person. Die Aufgabe beginnt mit „Nicht bestätigt: Du hast der Person noch nie geschrieben.“

## Rückerstattungen

Wenn ein Geschäft, eine Fluggesellschaft, ein Vermieter oder ein Versicherer dir Geld zurückverspricht, etwa eine Rückerstattung für eine stornierte Bestellung oder eine genehmigte Forderung, erfasst deine Machine den Betrag, den Zahlungspflichtigen und das Datum, an dem das Geld eingehen soll. Das Versprechen erscheint unter **Dir versprochen**. Nur wenn in der Nachricht alle drei Angaben eindeutig sind.

Wenn das Geld zuerst zurückkommt, etwa durch eine E-Mail mit dem Hinweis „Rückerstattung bearbeitet“, eine Mitteilung eines Zahlungsdienstes oder eine Benachrichtigung deiner Bank-App auf deinem Handy, wird das Versprechen automatisch geschlossen und keine Aufgabe erstellt.

Ist das Geld bis zu diesem Datum nicht eingegangen? Dann wird unauffällig eine Aufgabe erstellt: „Den Betrag von 42 € von … nachverfolgen“. Dazu gehört eine kurze E-Mail an die betreffende Stelle, in der die Bestell- oder Vorgangsnummer genannt wird. Gesendet wird erst, wenn du die Nachricht abschickst. Geht das Geld doch noch ein, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** wird sie für einen Tag wiederhergestellt.

Die [Wochenübersicht](weekly-recap.md) zählt eingehaltene und offene Versprechen. Auf deinem eigenen Computer listet `assistant promises` sie in einem Terminal auf.
