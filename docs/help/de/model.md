---
title: Modell
area: settings
summary: Welches KI-Modell für dich antwortet, wie intensiv es nachdenkt und wie viel deines Kontingents es verbraucht hat.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: 249d2d7d6c368cfe
---
Unter **Einstellungen** > **Modell** siehst du, welches KI-Modell deine **Hintergrundarbeit** erledigt und womit du angemeldet bist, zum Beispiel mit ChatGPT.

Auf einer gehosteten Machine ist GPT-6.2 Sol das Hauptmodell, wenn du mit ChatGPT angemeldet bist: Es antwortet schneller als GPT-6.1 Sol und kostet gleich viel.

Bei einem privaten ChatGPT- oder Claude-Tarif können deine Chats standardmäßig zum Training verwendet werden. Mit **Training mit deinen Daten deaktivieren** öffnest du die entsprechende Einstellung beim Anbieter. **Erledigt** blendet die Zeile aus.

## Modell und Nachdenken in Chats

Unter **Chats** wählst du das Modell und die Nachdenk-Stufe für deine Aufgaben-Chats und die Hilfe aus. Du siehst nur die Modelle und Stufen, die bei deiner Anmeldung verfügbar sind.

Mehr Nachdenken hilft bei schwierigen Fragen, dauert aber länger und verbraucht mehr von deinem Kontingent. **Ultra-Nachdenken** holt bei besonders schwierigen Fragen Helferinnen hinzu und verbraucht am meisten. Bei einer neuen Machine ist **Wenig Nachdenken** voreingestellt: gute Ergebnisse bei deutlich geringerem Verbrauch deines Kontingents. Eine Änderung gilt ab der nächsten Nachricht.

Um die Einstellung nur für einen Chat zu ändern, tippst du unter dem Nachrichtenfeld auf das Modell oder die Nachdenk-Stufe. Wähle erneut **Einstellungen**, damit der Chat den Einstellungen folgt.

Prüfungen, dein Profil und vorbereitete Entwürfe verwenden weiterhin ihr eigenes Modell.

## Limits

Wenn dein Tarif Nutzungslimits hat, zum Beispiel die 5-Stunden- und Wochenlimits bei einem ChatGPT- oder Claude-Tarif, siehst du, wie viel du bereits verbraucht hast und wann die Limits zurückgesetzt werden. Das bloße Ansehen verbraucht nichts von deinem Kontingent.

## Platz für deine eigenen Chats

Hintergrundarbeit lässt Platz für deine eigenen Chats. Sie pausiert bei etwa 65 % des 5-Stunden-Limits. Neue Nachrichten werden bis etwa 90 % des Wochenlimits geprüft. Andere Arbeit nutzt pro Tag etwa ein Siebtel des Wochenlimits. Bei einer Anmeldung ohne Limits, zum Beispiel mit einem API-Schlüssel, wird nie pausiert.

Hintergrundarbeit läuft nie mit GPT-6 Astra. Stattdessen wird GPT-6.2 Sol verwendet oder GPT-6.1 Sol, wenn 6.2 nicht eingerichtet ist.

## Wenn ein Limit erreicht ist

Oben im Dashboard steht, welches Limit erreicht ist und wann es zurückgesetzt wird. Die Arbeit wartet und wird dann an der Stelle fortgesetzt, an der sie aufgehört hat. Es geht nichts verloren. Wenn dein ChatGPT-Tarif Resets umfasst, setzt **Ein Reset nutzen** die Limits zurück. Andernfalls öffnet **Resets in ChatGPT ansehen** die entsprechende Seite in ChatGPT.

## Mit einem Fallback

Wenn für deine Machine ein Fallback-Modell mit einem anderen Tarif oder Anbieter eingerichtet ist, übernimmt es, sobald ein Limit erreicht ist. Es muss dann nichts warten. Oben im Dashboard steht: „ChatGPT-Limit erreicht, Fallback wird verwendet.“ Wenn das Fallback nicht mehr funktioniert, wird wieder pausiert.

## Hauptmodell ändern

Das Hauptmodell wird vom Rest von The Machine verwendet. Auf einer gehosteten Machine änderst du es auf der Einrichtungsseite unter „Deine KI“. Auf deinem eigenen Computer findest du weitere Informationen unter [ChatGPT](chatgpt.md), [Mistral](mistral.md) und im [Leitfaden zu Modellen](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
