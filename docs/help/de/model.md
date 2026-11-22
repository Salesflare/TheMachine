---
title: Modell
area: settings
summary: Welches KI-Modell für dich antwortet, wie intensiv es nachdenkt und wie viel deines Nutzungslimits es verbraucht hat.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: ee95ad4fa5323e3a
---
**Einstellungen** > **Modell** zeigt, welches KI-Modell deine **Hintergrundarbeit** erledigt und wie du angemeldet bist, zum Beispiel mit ChatGPT.

Auf einer gehosteten Machine ist GPT-6.2 Sol das Hauptmodell, wenn du mit ChatGPT angemeldet bist: Es antwortet schneller als GPT-6.1 Sol und kostet gleich viel.

Ein persönlicher ChatGPT- oder Claude-Tarif nutzt deine Chats möglicherweise standardmäßig zum Trainieren: **Training mit deinen Daten deaktivieren** öffnet die entsprechende Einstellung beim Anbieter, und **Erledigt** blendet den Hinweis aus.

## Modell und Nachdenken in Chats

Unter **Chats** wählst du das Modell und die Nachdenk-Stufe für deine Aufgaben-Chats und die Hilfe aus. Du siehst nur die Modelle und Stufen, die für deine Anmeldung verfügbar sind.

Mit mehr Nachdenken beantwortet das Modell schwierige Fragen besser, braucht aber länger und verbraucht mehr von deinem Tarif. **Ultra-Nachdenken** setzt bei besonders schwierigen Fragen zusätzliche Helfer ein und verbraucht am meisten. Eine neue Machine startet mit **Wenig Nachdenken**: gute Ergebnisse bei deutlich geringerem Verbrauch deines Tarifs. Änderungen gelten ab der nächsten Nachricht.

Wenn du die Einstellung nur für einen Chat ändern möchtest, tippe unter dem Eingabefeld auf das Modell oder die Nachdenk-Stufe. Wähle erneut die Einstellung aus, um wieder den Einstellungen zu folgen.

Prüfungen, dein Profil und vorab erstellte Entwürfe verwenden weiterhin ihr eigenes Modell.

## Limits

Wenn dein Tarif Nutzungslimits hat, etwa die 5-Stunden- und Wochenlimits eines ChatGPT- oder Claude-Tarifs, wird angezeigt, wie viel du verbraucht hast und wann die Limits zurückgesetzt werden. Das Anzeigen verbraucht nichts von deinem Tarif.

## Mehr Platz für deine eigenen Chats

Die Hintergrundarbeit lässt Platz für deine eigenen Chats. Sie pausiert bei etwa 65 % des 5-Stunden-Limits. Prüfungen neuer Nachrichten laufen bis etwa 90 % des Wochenlimits weiter. Andere Arbeit verbraucht täglich etwa ein Siebtel des Wochenlimits. Bei einer Anmeldung ohne Limits, etwa mit einem API-Schlüssel, wird nie pausiert.

Hintergrundarbeit läuft nie mit GPT-6 Astra. Bei einer ChatGPT-Anmeldung verwendet sie vorerst GPT-6.1 Sol, auch wenn GPT-6.2 Sol dein Hauptmodell ist: Bei dieser Anmeldung kann GPT-6.2 seine zwischengespeicherten Anweisungen noch nicht wiederverwenden und verbraucht daher mehr von deinem Tarif. Für deine Chats bleibt das ausgewählte Modell aktiv.

Vor einer Prüfung sortiert ein kleines Modell (GPT-6 Luna mit ChatGPT, Haiku mit Claude) Newsletter, Werbung und App-Mitteilungen aus, bei denen offensichtlich nichts zu tun ist. So verbrauchen Prüfungen weniger von deinem Tarif. Diese Nachrichten bleiben durchsuchbar. Nachrichten von Personen, Rechnungen, Sicherheitswarnungen und Anmeldecodes werden immer geprüft.

## Bevor ein Limit erreicht ist

Wenn für deinen ChatGPT-Tarif noch Resets verfügbar sind, wird unter Aufgaben eine kurze Meldung angezeigt, sobald die Hintergrundarbeit langsamer wird: bei etwa 65 % des 5-Stunden-Limits oder 90 % des Wochenlimits. Die Meldung zeigt an, wie viel du verbraucht hast und wie viele Resets noch verfügbar sind. Mit **Einen Reset nutzen** werden die Limits nach deiner Bestätigung zurückgesetzt. × blendet die Meldung aus, bis das betreffende Limit zurückgesetzt wird. Wenn keine Resets verfügbar sind, wird nichts Neues angezeigt.

Auf einer gehosteten Machine kann deine Machine Resets sehen und verwenden, sobald Codex auf deiner Machine mit demselben ChatGPT-Konto angemeldet ist. Bis dahin wird unter Aufgaben und in den Einstellungen **Resets aktivieren** angezeigt. Damit öffnest du den Codex-Schritt auf deiner Einrichtungsseite. Dort meldest du dich mit einem Code an, wie bei deiner ChatGPT-Anmeldung.

## Wenn ein Limit erreicht ist

Oben im Dashboard steht, welches Limit erreicht wurde und wann es zurückgesetzt wird. Die Arbeit wartet und wird dann an der Stelle fortgesetzt, an der sie unterbrochen wurde. Es geht nichts verloren. Wenn für deinen ChatGPT-Tarif Resets verfügbar sind, werden die Limits mit **Einen Reset nutzen** zurückgesetzt. Wenn Codex auf einer gehosteten Machine nicht angemeldet ist, öffnet **Resets aktivieren** stattdessen deine Einrichtungsseite. Andernfalls öffnet **Resets in ChatGPT ansehen** die entsprechende Seite in ChatGPT.

## Mit einem Ausweichmodell

Wenn für deine Machine ein Ausweichmodell mit einem anderen Tarif oder Anbieter eingerichtet ist, übernimmt es, sobald ein Limit erreicht ist. Die Arbeit wird dann nicht angehalten. Oben im Dashboard steht: „ChatGPT-Limit erreicht, Ausweichmodell wird verwendet.“ Wenn das Ausweichmodell nicht mehr funktioniert, wird die Arbeit wieder pausiert.

## Hauptmodell ändern

Das Hauptmodell wird für alle anderen Funktionen von The Machine verwendet. Auf einer gehosteten Machine änderst du es auf deiner Einrichtungsseite unter „Deine KI“. Wenn du deine eigene Machine verwendest, findest du weitere Infos unter [ChatGPT](chatgpt.md), [Mistral](mistral.md) und im [Modellleitfaden](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
