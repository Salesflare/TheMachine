---
title: Modell
area: settings
summary: Welches KI-Modell für dich antwortet, wie intensiv es nachdenkt und wie viel deiner Tariflimits es bereits genutzt hat.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: d63ec55d8d0339e6
---
**Einstellungen**, **Modell** zeigt, welches KI-Modell deine **Hintergrundarbeit** erledigt und wie du angemeldet bist, zum Beispiel bei ChatGPT.

Auf einer gehosteten Machine mit einer ChatGPT-Anmeldung ist GPT-6.2 Sol das Hauptmodell: Es antwortet schneller als GPT-6.1 Sol, zum selben Preis.

Bei einem persönlichen ChatGPT- oder Claude-Abo können deine Chats standardmäßig fürs Training verwendet werden. **Training mit deinen Daten deaktivieren** öffnet die entsprechende Einstellung beim Anbieter, und **Erledigt** blendet die Zeile aus.

## Modell und Nachdenken in Chats

Unter **Chats** wählst du das Modell und die Intensität des Nachdenkens für deine Aufgaben-Chats und die Hilfe aus. Du siehst nur die Modelle und Stufen, die bei deiner Anmeldung verfügbar sind.

Mehr Nachdenken verbessert die Antworten auf schwierige Fragen, dauert aber länger und verbraucht mehr von deinem Tarif. **Ultra-Nachdenken** holt bei den schwierigsten Fragen zusätzliche Helfer dazu und verbraucht am meisten. Eine neue Machine startet mit **Wenig Nachdenken**: gute Ergebnisse bei deutlich geringerem Verbrauch deines Tarifs. Änderungen gelten ab der nächsten Nachricht.

Um die Einstellung nur für einen Chat zu ändern, tippe unter dem Nachrichtenfeld auf das Modell oder die Stufe des Nachdenkens. Wähle erneut die Einstellung aus, damit der Chat den Einstellungen folgt.

Prüfungen, dein Profil und vorab erstellte Entwürfe behalten ihr eigenes Modell.

## Limits

Wenn dein Tarif Nutzungslimits hat, zum Beispiel die 5-Stunden- und Wochenlimits eines ChatGPT- oder Claude-Abos, wird angezeigt, wie viel du bereits verbraucht hast und wann die Limits zurückgesetzt werden. Das Anzeigen verbraucht nichts von deinem Tarif.

## Platz für deine eigenen Chats

Die Hintergrundarbeit lässt Platz für deine eigenen Chats. Sie pausiert bei etwa 65 % des 5-Stunden-Limits. Neue Nachrichten werden bis etwa 90 % des Wochenlimits überprüft. Andere Arbeiten beanspruchen pro Tag etwa ein Siebtel des Wochenlimits. Eine Anmeldung ohne Limits, zum Beispiel mit einem API-Schlüssel, pausiert nie.

Hintergrundarbeit läuft nie mit GPT-6 Astra. Bei einer ChatGPT-Anmeldung verwendet sie vorerst GPT-6.1 Sol, auch wenn dein Hauptmodell GPT-6.2 Sol ist: Bei dieser Anmeldung verwendet 6.2 seine zwischengespeicherten Anweisungen noch nicht wieder und verbraucht deshalb mehr von deinem Tarif. In deinen Chats bleibt das ausgewählte Modell aktiv.

## Bevor ein Limit erreicht ist

Wenn für dein ChatGPT-Abo noch Resets verfügbar sind, erscheint unter Aufgaben eine kurze Meldung, sobald die Hintergrundarbeit langsamer wird: bei etwa 65 % des 5-Stunden-Limits oder 90 % des Wochenlimits. Sie zeigt an, wie viel du verbraucht hast und wie viele Resets noch übrig sind. **Einen Reset nutzen** setzt die Limits zurück, nachdem du bestätigt hast. × blendet die Meldung aus, bis das jeweilige Limit zurückgesetzt wird. Wenn keine Resets verfügbar sind, erscheint keine Meldung.

## Wenn ein Limit erreicht ist

Oben im Dashboard steht, welches Limit erreicht wurde und wann es zurückgesetzt wird. Die Arbeit wartet und wird dann an der Stelle fortgesetzt, an der sie pausiert wurde. Es geht nichts verloren. Wenn für dein ChatGPT-Abo Resets verfügbar sind, setzt **Einen Reset nutzen** die Limits zurück. Andernfalls öffnet **Resets in ChatGPT ansehen** die entsprechende Seite in ChatGPT.

## Mit einem Ersatzmodell

Wenn für deine Machine ein Ersatzmodell mit einem anderen Abo oder bei einem anderen Anbieter eingerichtet ist, übernimmt es, sobald ein Limit erreicht ist. Die Arbeit muss dann nicht warten. Oben im Dashboard steht: „ChatGPT-Limit erreicht, dein Ersatzmodell wird verwendet.“ Wenn das Ersatzmodell nicht mehr funktioniert, wird die Arbeit wieder pausiert.

## Hauptmodell ändern

Das Hauptmodell wird vom Rest der The Machine verwendet. Auf einer gehosteten Machine kannst du es auf der Einrichtungsseite unter „Deine KI“ ändern. Auf deinem eigenen Computer findest du weitere Informationen unter [ChatGPT](chatgpt.md), [Mistral](mistral.md) und im [Modellleitfaden](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
