---
title: Modell
area: settings
summary: Welches KI-Modell für dich antwortet, wie intensiv es nachdenkt und wie viel deines Kontingents es verbraucht hat.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: c7a96914e4deb3d4
---
Unter **Einstellungen** > **Modell** siehst du, welches KI-Modell deine **Hintergrundarbeit** erledigt und wie du angemeldet bist, zum Beispiel über ChatGPT.

Bei persönlichen ChatGPT- oder Claude-Tarifen können deine Chats standardmäßig zum Training verwendet werden: **Training mit deinen Daten deaktivieren** öffnet die entsprechende Einstellung beim Anbieter, und **Erledigt** blendet die Zeile aus.

## Modell und Nachdenken in Chats

Unter **Chats** wählst du das Modell und die Nachdenk-Stufe für deine Aufgaben-Chats und die Hilfe aus. Du siehst nur die Modelle und Stufen, die deine Anmeldung unterstützt.

Mit mehr Nachdenken werden schwierige Fragen besser beantwortet. Es dauert aber länger und verbraucht mehr von deinem Kontingent. **Ultra-Nachdenken** holt sich bei besonders schwierigen Fragen Unterstützung und verbraucht am meisten. Eine neue Machine startet mit **Wenig Nachdenken**. Das liefert gute Ergebnisse und verbraucht deutlich weniger von deinem Kontingent. Änderungen gelten ab der nächsten Nachricht.

Wenn du die Einstellung nur für einen Chat ändern möchtest, tippe unter dem Nachrichtenfeld auf das Modell oder die Nachdenk-Stufe. Wähle erneut **Einstellungen**, damit der Chat wieder den Einstellungen folgt.

Prüfungen, dein Profil und vorab erstellte Entwürfe verwenden weiterhin ihr eigenes Modell.

## Limits

Wenn dein Tarif Nutzungslimits hat, zum Beispiel die 5-Stunden- und Wochenlimits eines ChatGPT- oder Claude-Tarifs, siehst du, wie viel du davon verbraucht hast und wann sie zurückgesetzt werden. Das Ansehen verbraucht nichts von deinem Kontingent.

## Platz für deine eigenen Chats

Hintergrundarbeit lässt Platz für deine eigenen Chats. Sie wird bei etwa 65 % des 5-Stunden-Limits pausiert. Neue Nachrichten werden bis zu etwa 90 % des Wochenlimits geprüft. Andere Arbeit verbraucht pro Tag etwa ein Siebtel des Wochenlimits. Bei einer Anmeldung ohne Limits, zum Beispiel mit einem API-Schlüssel, wird nie pausiert.

Hintergrundarbeit läuft nie mit GPT-6 Astra. Stattdessen verwendet sie GPT-6.2 Sol oder, wenn 6.2 nicht eingerichtet ist, GPT-6.1 Sol.

## Wenn ein Limit erreicht ist

Oben im Dashboard steht, welches Limit erreicht wurde und wann es zurückgesetzt wird. Die Arbeit wartet und wird anschließend dort fortgesetzt, wo sie aufgehört hat. Es geht nichts verloren. Wenn dein ChatGPT-Tarif Resets hat, setzt **Ein Reset nutzen** die Limits zurück. Andernfalls öffnet **Resets in ChatGPT ansehen** die entsprechende Seite in ChatGPT.

## Mit einem Fallback

Wenn deine Machine ein Fallback-Modell in einem anderen Tarif oder bei einem anderen Anbieter hat, übernimmt es, sobald ein Limit erreicht ist. Es muss nichts warten. Oben im Dashboard steht dann „ChatGPT-Limit erreicht, Fallback wird verwendet.“ Wenn das Fallback nicht mehr funktioniert, wird wieder pausiert.

## Hauptmodell ändern

Das Hauptmodell wird vom Rest von The Machine verwendet. Bei einer gehosteten Machine änderst du es auf deiner Einrichtungsseite unter Deine KI. Auf deinem eigenen Computer findest du weitere Informationen unter [ChatGPT](chatgpt.md), [Mistral](mistral.md) und in der [Modellübersicht](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
