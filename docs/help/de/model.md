---
title: Modell
area: settings
summary: Welches KI-Modell für dich antwortet, wie intensiv es nachdenkt und wie viel deines Tariflimits es verbraucht hat.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: b76f4f927bfd7be1
---
Unter **Einstellungen** > **Modell** siehst du, welches KI-Modell deine **Hintergrundarbeit** erledigt und wie du angemeldet bist, zum Beispiel über ChatGPT.

Auf einer gehosteten Machine ist GPT-6.2 Sol das Hauptmodell, wenn du dich mit ChatGPT anmeldest. Es antwortet schneller als GPT-6.1 Sol, und das zum gleichen Preis.

Auf einer gehosteten Machine gilt eine Claude-Anmeldung etwa ein Jahr. Mit `claude auth login` endet sie etwa vier Wochen nach deiner Anmeldung. Drei Tage vorher weist dich **Braucht dich** darauf hin und du erhältst eine E-Mail. Nach Ablauf bekommst du eine Benachrichtigung und, falls sie noch nicht rausgegangen ist, auch die E-Mail. Mit **Erneut anmelden** ist das in einem Schritt erledigt.

Bei einem persönlichen ChatGPT- oder Claude-Tarif können deine Chats standardmäßig zum Trainieren verwendet werden. **Training mit deinen Daten deaktivieren** öffnet die entsprechende Einstellung beim Anbieter, und **Erledigt** blendet den Hinweis aus.

## Modell und Nachdenken für Chats

Unter **Chats** wählst du das Modell und die Intensität des Nachdenkens für deine Aufgaben-Chats und die Hilfe aus. Du siehst nur die Modelle und Stufen, die für deine Anmeldung verfügbar sind.

Mit mehr Nachdenken beantwortet das Modell schwierige Fragen besser, braucht aber länger und verbraucht mehr von deinem Tarif. **Ultra-Nachdenken** zieht bei besonders schwierigen Fragen Helferinnen hinzu und verbraucht am meisten. Eine neue Machine startet mit **Wenig Nachdenken**: gute Ergebnisse bei deutlich geringerem Verbrauch deines Tarifs. Eine Änderung gilt ab der nächsten Nachricht.

Wenn du das nur für einen Chat ändern willst, tippe unter dem Nachrichtenfeld auf das Modell oder die Stufe des Nachdenkens. Wähle erneut die Einstellung aus, damit der Chat wieder den Einstellungen folgt.

Prüfungen, dein Profil und vorbereitete Entwürfe verwenden weiterhin ihr eigenes Modell.

## Limits

Wenn dein Tarif Nutzungslimits hat, zum Beispiel die 5-Stunden- und Wochenlimits eines ChatGPT- oder Claude-Tarifs, siehst du, wie viel du davon verbraucht hast und wann jedes Limit zurückgesetzt wird. Das Ansehen verbraucht nichts von deinem Tarif.

## Platz für deine eigenen Chats

Die Hintergrundarbeit lässt Platz für deine eigenen Chats. Sie pausiert bei etwa 65 % des 5-Stunden-Limits. Neue Nachrichten werden bis etwa 90 % des Wochenlimits geprüft. Andere Arbeiten verbrauchen pro Tag etwa ein Siebtel des Wochenlimits. Bei einer Anmeldung ohne Limits, zum Beispiel mit einem API-Schlüssel, wird nie pausiert.

Hintergrundarbeit läuft nie mit GPT-6 Astra. Wenn du mit ChatGPT angemeldet bist und eine OpenClaw-Version älter als 2026.11.10 verwendest, läuft sie mit GPT-6.1 Sol, auch wenn GPT-6.2 Sol dein Hauptmodell ist. GPT-6.2 nutzt dort seine zwischengespeicherten Anweisungen nicht erneut und verbraucht deshalb mehr von deinem Tarif. Ab OpenClaw 2026.11.10 verwendet die Hintergrundarbeit wieder dein Hauptmodell. Für deine Chats bleibt das ausgewählte Modell erhalten.

Vor einer Prüfung sortiert ein kleines Modell Newsletter, Werbung und App-Hinweise aus, bei denen eindeutig nichts zu tun ist. Mit ChatGPT ist das GPT-6 Luna, mit Claude Haiku. So verbrauchen Prüfungen weniger von deinem Tarif. Die Nachrichten bleiben durchsuchbar. Nachrichten von Personen, Rechnungen, Sicherheitswarnungen und Anmeldecodes werden immer geprüft.

## Bevor ein Limit erreicht ist

Wenn für deinen ChatGPT-Tarif noch Resets verfügbar sind, wird unter Aufgaben eine kurze Meldung angezeigt, sobald die Hintergrundarbeit langsamer wird: bei etwa 65 % des 5-Stunden-Limits oder 90 % des Wochenlimits. Darin steht, wie viel du verbraucht hast und wie viele Resets noch übrig sind. Mit **Einen Reset nutzen** werden die Limits nach deiner Bestätigung zurückgesetzt. × blendet die Meldung aus, bis das jeweilige Limit zurückgesetzt wird. Wenn keine Resets verfügbar sind, wird nichts angezeigt.

Auf einer gehosteten Machine erkennt und nutzt deine Machine Resets, sobald Codex auf deiner Machine bei demselben ChatGPT-Konto angemeldet ist. Bis dahin wird unter Aufgaben und in den Einstellungen **Resets aktivieren** angezeigt. Damit öffnest du den Codex-Schritt auf deiner Einrichtungsseite. Dort meldest du dich mit einem Code an, wie bei deiner ChatGPT-Anmeldung.

## Wenn ein Limit erreicht ist

Oben im Dashboard steht, welches Limit erreicht wurde und wann es zurückgesetzt wird. Die Arbeit wartet und wird dann an der Stelle fortgesetzt, an der sie pausiert wurde. Es geht nichts verloren. Wenn für deinen ChatGPT-Tarif Resets verfügbar sind, setzt **Einen Reset nutzen** die Limits zurück. Auf einer gehosteten Machine, auf der Codex nicht angemeldet ist, öffnet **Resets aktivieren** stattdessen deine Einrichtungsseite. In allen anderen Fällen öffnet **Resets in ChatGPT ansehen** die entsprechende ChatGPT-Seite.

## Mit einem Ausweichmodell

Wenn für deine Machine ein Ausweichmodell in einem anderen Tarif oder bei einem anderen Anbieter eingerichtet ist, übernimmt es, sobald ein Limit erreicht ist. Die Arbeit muss dann nicht warten. Oben im Dashboard steht „ChatGPT-Limit erreicht, Ausweichmodell wird verwendet.“ Wenn das Ausweichmodell nicht mehr funktioniert, wird die Arbeit wieder pausiert.

## Hauptmodell ändern

Das Hauptmodell wird für alles andere in The Machine verwendet. Auf einer gehosteten Machine kannst du es auf deiner Einrichtungsseite unter „Deine KI“ ändern. Auf deinem eigenen Computer findest du weitere Informationen unter [ChatGPT](chatgpt.md), [Mistral](mistral.md) und in der [Anleitung zu Modellen](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
