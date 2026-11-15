---
title: Modell
area: settings
summary: Welches KI-Modell für dich antwortet, wie lange es nachdenkt und wie viel deines Kontingents es verbraucht hat.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: 744a27a77ab747ac
---
**Einstellungen**, **Modell** zeigt dir, welches KI-Modell deine **Hintergrundarbeit** erledigt und wie du angemeldet bist, zum Beispiel über ChatGPT.

Bei einem persönlichen ChatGPT- oder Claude-Abo können deine Chats standardmäßig zum Trainieren verwendet werden: **Training mit deinen Daten deaktivieren** öffnet die entsprechende Einstellung beim Anbieter und **Erledigt** blendet die Zeile aus.

## Modell und Nachdenken in Chats

Unter **Chats** wählst du das Modell und die Nachdenk-Stufe für deine Aufgaben-Chats und die Hilfe aus. Du siehst nur die Modelle und Stufen, die dir mit deiner Anmeldung zur Verfügung stehen.

Mehr Nachdenken hilft bei schwierigen Fragen, dauert aber länger und verbraucht mehr von deinem Kontingent. **Ultra-Nachdenken** setzt bei den schwierigsten Fragen zusätzliche Helfer ein und verbraucht am meisten. Eine neue Machine startet mit **Wenig Nachdenken**: gute Ergebnisse bei deutlich geringerem Verbrauch deines Kontingents. Änderungen gelten ab der nächsten Nachricht.

Wenn du die Einstellung nur für einen Chat ändern möchtest, tippe unter dem Nachrichtenfeld auf das Modell oder die Nachdenk-Stufe. Wähle erneut **Einstellungen** aus, damit die Einstellungen gelten.

Checks, dein Profil und vorab vorbereitete Entwürfe verwenden weiterhin ihr eigenes Modell.

## Limits

Wenn dein Abo Nutzungslimits hat, zum Beispiel die 5-Stunden- und Wochenlimits eines ChatGPT- oder Claude-Abos, siehst du, wie viel davon verbraucht ist und wann die Limits zurückgesetzt werden. Die Anzeige verbraucht nichts von deinem Kontingent.

## Platz für deine eigenen Chats

Die Hintergrundarbeit lässt Platz für deine eigenen Chats. Sie pausiert bei etwa 65 % des 5-Stunden-Limits. Checks auf neue Nachrichten laufen bis etwa 90 % des Wochenlimits weiter. Andere Arbeit verbraucht pro Tag etwa ein Siebtel des Wochenlimits. Bei einer Anmeldung ohne Limits, zum Beispiel mit einem API-Schlüssel, wird nie pausiert.

Hintergrundarbeit läuft nie mit GPT-6 Astra. Stattdessen verwendet sie GPT-6.1 Sol.

## Wenn ein Limit erreicht ist

Oben im Dashboard steht, welches Limit erreicht wurde und wann es zurückgesetzt wird. Die Arbeit wartet und wird dann an der Stelle fortgesetzt, an der sie aufgehört hat. Es geht nichts verloren. Wenn dein ChatGPT-Abo Resets enthält, setzt **Ein Reset nutzen** die Limits zurück. Andernfalls öffnet **Resets in ChatGPT ansehen** die entsprechende Seite in ChatGPT.

## Mit einem Ausweichmodell

Wenn für deine Machine ein Ausweichmodell mit einem anderen Abo oder bei einem anderen Anbieter eingerichtet ist, übernimmt es, sobald ein Limit erreicht ist. Die Arbeit muss dann nicht warten. Oben im Dashboard steht „ChatGPT-Limit erreicht, Ausweichmodell wird verwendet.“ Wenn das Ausweichmodell nicht mehr funktioniert, wird die Arbeit wieder pausiert.

## Hauptmodell ändern

Das Hauptmodell wird für alles andere auf The Machine verwendet. Bei einer gehosteten Machine änderst du es auf deiner Einrichtungsseite unter „Deine KI“. Auf deinem eigenen Computer findest du weitere Infos unter [ChatGPT](chatgpt.md), [Mistral](mistral.md) und in der [Modellübersicht](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
