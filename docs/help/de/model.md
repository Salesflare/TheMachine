---
title: Modell
area: settings
summary: Welches KI-Modell für dich antwortet, wie intensiv es nachdenkt und wie viel deines Nutzungslimits es verbraucht hat.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: f34db396a7290252
---
**Einstellungen**, **Modell** zeigt, welches KI-Modell deine **Hintergrundarbeit** erledigt und wie du angemeldet bist, zum Beispiel bei ChatGPT.

Auf einer gehosteten Machine ist das Hauptmodell bei einer ChatGPT-Anmeldung GPT-6.2 Sol: Es antwortet schneller als GPT-6.1 Sol, zum selben Preis.

Bei einem persönlichen ChatGPT- oder Claude-Abo können deine Chats standardmäßig zum Trainieren verwendet werden: **Training mit deinen Daten deaktivieren** öffnet die entsprechende Einstellung beim Anbieter, und **Erledigt** blendet den Hinweis aus.

## Modell und Nachdenken für Chats

Unter **Chats** kannst du das Modell und die Nachdenk-Stufe für deine Aufgaben-Chats und die Hilfe auswählen. Du siehst nur die Modelle und Stufen, die mit deiner Anmeldung verfügbar sind.

Mit mehr Nachdenken beantwortet das Modell schwierige Fragen besser, braucht aber länger und verbraucht mehr von deinem Abo. **Ultra-Nachdenken** zieht Helfer bei den schwierigsten Fragen hinzu und verbraucht am meisten. Eine neue Machine startet mit **Wenig Nachdenken**: gute Ergebnisse bei deutlich geringerem Verbrauch deines Abos. Änderungen gelten ab der nächsten Nachricht.

Um das Modell oder die Nachdenk-Stufe nur für einen Chat zu ändern, tippe unter dem Nachrichtenfeld auf das Modell oder die Nachdenk-Stufe. Wähle erneut die Option „Einstellungen“, damit die Einstellung aus den Einstellungen gilt.

Prüfungen, dein Profil und vorbereitete Entwürfe verwenden weiterhin ihr eigenes Modell.

## Limits

Wenn dein Abo Nutzungslimits hat, etwa die 5-Stunden- und Wochenlimits eines ChatGPT- oder Claude-Abos, wird angezeigt, wie viel du verbraucht hast und wann die Limits zurückgesetzt werden. Das Ansehen verbraucht nichts von deinem Abo.

## Platz für deine eigenen Chats

Die Hintergrundarbeit lässt Platz für deine eigenen Chats. Sie wird bei etwa 65 % des 5-Stunden-Limits pausiert. Prüfungen neuer Nachrichten laufen bis etwa 90 % des Wochenlimits weiter. Andere Arbeit verbraucht pro Tag etwa ein Siebtel des Wochenlimits. Bei einer Anmeldung ohne Limits, etwa mit einem API-Schlüssel, wird nie pausiert.

Hintergrundarbeit läuft nie mit GPT-6 Astra. Bei einer ChatGPT-Anmeldung und einer OpenClaw-Version vor 2026.11.10 verwendet sie GPT-6.1 Sol, auch wenn dein Hauptmodell GPT-6.2 Sol ist: GPT-6.2 verwendet dort seine zwischengespeicherten Anweisungen nicht erneut und verbraucht deshalb mehr von deinem Abo. Ab OpenClaw 2026.11.10 verwendet die Hintergrundarbeit wieder dein Hauptmodell. Für deine Chats bleibt das ausgewählte Modell erhalten.

Vor einer Prüfung sortiert ein kleines Modell (GPT-6 Luna mit ChatGPT, Haiku mit Claude) Newsletter, Werbung und App-Benachrichtigungen aus, bei denen eindeutig nichts zu tun ist. So verbrauchen Prüfungen weniger von deinem Abo. Die Nachrichten bleiben durchsuchbar. Nachrichten von einer Person, eine Rechnung, eine Sicherheitswarnung oder ein Anmeldecode werden immer geprüft.

## Bevor ein Limit erreicht ist

Wenn du bei deinem ChatGPT-Abo noch Resets hast, wird unter Aufgaben eine kurze Meldung angezeigt, sobald die Hintergrundarbeit langsamer wird: bei etwa 65 % des 5-Stunden-Limits oder 90 % des Wochenlimits. Sie zeigt an, wie viel du verbraucht hast und wie viele Resets noch übrig sind. **Einen Reset nutzen** setzt die Limits nach deiner Bestätigung zurück. × blendet die Meldung aus, bis das jeweilige Limit zurückgesetzt wird. Ohne Resets wird nichts angezeigt.

Auf einer gehosteten Machine kann deine Machine Resets sehen und nutzen, sobald Codex auf deiner Machine beim selben ChatGPT-Konto angemeldet ist. Bis dahin wird unter Aufgaben und in den Einstellungen **Resets aktivieren** angezeigt. Damit öffnest du den Codex-Schritt deiner Einrichtungsseite. Dort meldest du dich mit einem Code an, wie bei deiner ChatGPT-Anmeldung.

## Wenn ein Limit erreicht ist

Oben im Dashboard steht, welches Limit erreicht wurde und wann es zurückgesetzt wird. Die Arbeit wartet und wird anschließend an der Stelle fortgesetzt, an der sie pausiert wurde. Es geht nichts verloren. Wenn dein ChatGPT-Abo Resets hat, setzt **Einen Reset nutzen** die Limits zurück. Auf einer gehosteten Machine ohne angemeldetes Codex öffnet **Resets aktivieren** stattdessen deine Einrichtungsseite. Andernfalls öffnet **Resets in ChatGPT ansehen** die entsprechende Seite in ChatGPT.

## Mit einem Ausweichmodell

Wenn deine Machine ein Ausweichmodell in einem anderen Abo oder bei einem anderen Anbieter hat, übernimmt es, sobald ein Limit erreicht ist. Die Arbeit muss dann nicht warten. Oben im Dashboard steht „ChatGPT-Limit erreicht, Ausweichmodell wird verwendet.“ Wenn das Ausweichmodell nicht mehr funktioniert, wird die Arbeit wieder pausiert.

## Hauptmodell ändern

Das Hauptmodell wird für alles andere in The Machine verwendet. Auf einer gehosteten Machine kannst du es auf deiner Einrichtungsseite unter „Deine KI“ ändern. Wenn du The Machine auf deinem eigenen Computer verwendest, findest du weitere Infos unter [ChatGPT](chatgpt.md), [Mistral](mistral.md) und in der [Modellübersicht](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
