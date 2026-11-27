---
title: Modell
area: settings
summary: Welches KI-Modell für dich antwortet, wie intensiv es nachdenkt und wie viel deines Tarifs es verbraucht hat.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: 9a0777c555ab5637
---
Unter **Einstellungen** > **Modell** siehst du, welches KI-Modell deine **Hintergrundarbeit** erledigt und wie du angemeldet bist, zum Beispiel bei ChatGPT.

Auf einer gehosteten Machine ist GPT-6.2 Sol das Hauptmodell, wenn du mit ChatGPT angemeldet bist: Es antwortet schneller als GPT-6.1 Sol zum gleichen Preis.

Wenn du dich mit Claude anmeldest, läuft die Anmeldung nach etwa vier Wochen ab. **Braucht dich** weist dich drei Tage vorher darauf hin. Nach Ablauf erhältst du eine Benachrichtigung. Mit **Erneut anmelden** ist das in einem Schritt erledigt.

Bei einem persönlichen ChatGPT- oder Claude-Tarif kann es sein, dass deine Chats standardmäßig zum Trainieren verwendet werden: **Training mit deinen Daten deaktivieren** öffnet die entsprechende Einstellung beim Anbieter. Mit **Erledigt** blendest du den Hinweis aus.

## Modell und Nachdenken in Chats

Unter **Chats** wählst du das Modell und die Nachdenk-Stufe für deine Aufgaben-Chats und die Hilfe aus. Du siehst nur die Modelle und Stufen, die deine Anmeldung bietet.

Mehr Nachdenken hilft bei schwierigen Fragen, dauert aber länger und verbraucht mehr von deinem Tarif. **Ultra-Nachdenken** holt bei besonders schwierigen Fragen weitere Helferinnen dazu und verbraucht am meisten. Eine neue Machine startet mit **Wenig Nachdenken**: gute Ergebnisse bei deutlich geringerem Verbrauch deines Tarifs. Änderungen gelten ab der nächsten Nachricht.

Wenn du die Einstellung nur für einen Chat ändern möchtest, tippe unter dem Nachrichtenfeld auf das Modell oder die Nachdenk-Stufe. Wähle erneut die Option „Einstellungen“, damit der Chat wieder den Einstellungen folgt.

Prüfungen, dein Profil und vorab vorbereitete Entwürfe verwenden weiterhin ihr eigenes Modell.

## Limits

Wenn dein Tarif Nutzungslimits hat, etwa die 5-Stunden- und Wochenlimits eines ChatGPT- oder Claude-Tarifs, siehst du, wie viel du verbraucht hast und wann die Limits jeweils zurückgesetzt werden. Das Ansehen verbraucht nichts von deinem Tarif.

## Platz für deine eigenen Chats

Die Hintergrundarbeit lässt Platz für deine eigenen Chats. Bei etwa 65 % des 5-Stunden-Limits wird sie pausiert. Neue Nachrichten werden bis etwa 90 % des Wochenlimits weiter geprüft. Andere Arbeit nimmt täglich etwa ein Siebtel des Wochenlimits in Anspruch. Bei einer Anmeldung ohne Limits, etwa mit einem API-Schlüssel, wird nie pausiert.

Hintergrundarbeit läuft nie mit GPT-6 Astra. Wenn du mit ChatGPT angemeldet bist und OpenClaw älter als 2026.11.10 ist, verwendet sie GPT-6.1 Sol, auch wenn GPT-6.2 Sol dein Hauptmodell ist: GPT-6.2 verwendet dort seine zwischengespeicherten Anweisungen nicht erneut und verbraucht deshalb mehr von deinem Tarif. Ab OpenClaw 2026.11.10 verwendet die Hintergrundarbeit wieder dein Hauptmodell. Für deine Chats bleibt das ausgewählte Modell erhalten.

Vor einer Prüfung sortiert ein kleines Modell (GPT-6 Luna mit ChatGPT, Haiku mit Claude) Newsletter, Werbung und App-Hinweise aus, bei denen eindeutig nichts zu tun ist. So verbrauchen Prüfungen weniger von deinem Tarif. Die Nachrichten bleiben durchsuchbar. Nachrichten von Personen, Rechnungen, Sicherheitswarnungen und Anmeldecodes werden immer geprüft.

## Bevor ein Limit erreicht ist

Wenn für deinen ChatGPT-Tarif noch Resets verfügbar sind, wird unter Aufgaben eine kurze Meldung angezeigt, sobald die Hintergrundarbeit langsamer wird: bei etwa 65 % des 5-Stunden-Limits oder 90 % des Wochenlimits. Sie zeigt an, wie viel du verbraucht hast und wie viele Resets noch übrig sind. Mit **Einen Reset nutzen** setzt du die Limits nach deiner Bestätigung zurück. Über × blendest du die Meldung aus, bis das jeweilige Limit zurückgesetzt wird. Wenn keine Resets verfügbar sind, wird nichts Neues angezeigt.

Auf einer gehosteten Machine kann deine Machine Resets erkennen und verwenden, sobald Codex auf deiner Machine mit demselben ChatGPT-Konto angemeldet ist. Bis dahin wird unter Aufgaben und in den Einstellungen **Resets aktivieren** angezeigt. Damit öffnest du den Codex-Schritt auf deiner Einrichtungsseite. Dort meldest du dich mit einem Code an, wie bei deiner ChatGPT-Anmeldung.

## Wenn ein Limit erreicht ist

Oben im Dashboard siehst du, welches Limit erreicht wurde und wann es zurückgesetzt wird. Die Arbeit wartet und wird danach an der Stelle fortgesetzt, an der sie unterbrochen wurde. Es geht nichts verloren. Wenn dein ChatGPT-Tarif Resets umfasst, setzt **Einen Reset nutzen** die Limits zurück. Wenn du auf einer gehosteten Machine nicht bei Codex angemeldet bist, öffnet **Resets aktivieren** stattdessen deine Einrichtungsseite. Andernfalls öffnet **Resets in ChatGPT ansehen** die entsprechende Seite bei ChatGPT.

## Mit einem Ausweichmodell

Wenn für deine Machine ein Ausweichmodell in einem anderen Tarif oder bei einem anderen Anbieter eingerichtet ist, übernimmt es, sobald ein Limit erreicht ist. Es muss dann nichts warten. Oben im Dashboard steht: „ChatGPT-Limit erreicht, Ausweichmodell wird verwendet.“ Wenn das Ausweichmodell nicht mehr funktioniert, wird die Arbeit wieder pausiert.

## Hauptmodell ändern

Das Hauptmodell wird vom Rest von The Machine verwendet. Auf einer gehosteten Machine kannst du es auf deiner Einrichtungsseite unter „Deine KI“ ändern. Auf deinem eigenen Computer findest du weitere Informationen unter [ChatGPT](chatgpt.md), [Mistral](mistral.md) und im [Modellhandbuch](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
