---
title: Modell
area: settings
summary: Welches KI-Modell für dich antwortet, wie intensiv es nachdenkt und wie viel deines Tarifs es bereits verbraucht hat.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: eee77413a4bdbf0b
---
**Einstellungen**, **Modell** zeigt, welches KI-Modell deine **Hintergrundarbeit** erledigt und wie du angemeldet bist, zum Beispiel mit ChatGPT.

## Modell und Nachdenken in Chats

Unter **Chats** wählst du das Modell und die Nachdenk-Stufe für deine Aufgaben-Chats und die Hilfe aus. Du siehst nur die Modelle und Stufen, die dir mit deiner Anmeldung zur Verfügung stehen.

Mit mehr Nachdenken beantwortet das Modell schwierige Fragen besser, ist aber langsamer und verbraucht mehr von deinem Tarif. **Ultra-Nachdenken** bezieht bei besonders schwierigen Fragen Helfer ein und verbraucht am meisten. Eine neue Machine startet mit **Wenig Nachdenken**: gute Ergebnisse bei deutlich geringerem Verbrauch deines Tarifs. Eine Änderung gilt ab der nächsten Nachricht.

Um die Einstellung nur für einen Chat zu ändern, tippe unter dem Nachrichtenfeld auf das Modell oder die Nachdenk-Stufe. Wähle erneut **Einstellungen**, damit der Chat den Einstellungen folgt.

Prüfungen, dein Profil und im Voraus vorbereitete Entwürfe behalten ihr eigenes Modell.

## Limits

Wenn dein Tarif Nutzungslimits hat, zum Beispiel die 5-Stunden- und Wochenlimits eines ChatGPT- oder Claude-Tarifs, wird angezeigt, wie viel davon verbraucht ist und wann die Limits zurückgesetzt werden. Das Nachsehen verbraucht nichts von deinem Tarif.

## Platz für deine eigenen Chats

Hintergrundarbeit lässt Platz für deine eigenen Chats. Sie pausiert bei etwa 65 % des 5-Stunden-Limits. Prüfungen neuer Nachrichten laufen bis etwa 90 % des Wochenlimits weiter. Andere Arbeit verbraucht pro Tag etwa ein Siebtel des Wochenlimits. Eine Anmeldung ohne Limits, zum Beispiel mit einem API-Schlüssel, führt nie zu einer Pause.

Hintergrundarbeit läuft nie mit GPT-6 Astra. Stattdessen verwendet sie GPT-6.1 Sol.

## Wenn ein Limit erreicht ist

Oben auf dem Dashboard steht, welches Limit erreicht wurde und wann es zurückgesetzt wird. Die Arbeit wartet und wird dann an der Stelle fortgesetzt, an der sie aufgehört hat. Es geht nichts verloren. Wenn dein ChatGPT-Tarif Resets enthält, setzt **Ein Reset nutzen** die Limits zurück. Andernfalls öffnet **Resets in ChatGPT ansehen** die entsprechende Seite von ChatGPT.

## Mit einem Ausweichmodell

Wenn für deine Machine ein Ausweichmodell in einem anderen Tarif oder bei einem anderen Anbieter eingerichtet ist, übernimmt es, sobald ein Limit erreicht ist. Nichts muss warten. Oben auf dem Dashboard steht dann „ChatGPT-Limit erreicht, Ausweichmodell wird verwendet.“ Wenn das Ausweichmodell nicht mehr funktioniert, werden die Pausen wieder aktiviert.

## Hauptmodell ändern

Das Hauptmodell wird für alles andere auf The Machine verwendet. Bei einer gehosteten Machine kannst du es auf deiner Einrichtungsseite unter „Deine KI“ ändern. Auf deinem eigenen Computer findest du weitere Informationen unter [ChatGPT](chatgpt.md), [Mistral](mistral.md) und im [Leitfaden zu Modellen](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
