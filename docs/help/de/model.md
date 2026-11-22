---
title: Modell
area: settings
summary: Welches KI-Modell für dich antwortet, wie intensiv es nachdenkt und wie viel deiner Tariflimits es bereits ausgeschöpft hat.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: a6db52984a6fddeb
---
**Einstellungen**, **Modell** zeigt, welches KI-Modell deine **Hintergrundarbeit** erledigt und wie du angemeldet bist, zum Beispiel bei ChatGPT.

Auf einer gehosteten Machine mit einer Anmeldung bei ChatGPT ist GPT-6.2 Sol das Hauptmodell. Es antwortet schneller als GPT-6.1 Sol, zum gleichen Preis.

Bei einem persönlichen ChatGPT- oder Claude-Tarif können deine Chats standardmäßig zum Trainieren verwendet werden. **Training mit deinen Daten deaktivieren** öffnet die entsprechende Einstellung beim Anbieter, und **Erledigt** blendet den Hinweis aus.

## Modell und Nachdenken in Chats

Unter **Chats** kannst du das Modell und die Nachdenk-Stufe für deine Aufgaben-Chats und die Hilfe auswählen. Du siehst nur die Modelle und Stufen, die deine Anmeldung unterstützt.

Mit mehr Nachdenken werden schwierige Fragen besser beantwortet. Es dauert aber länger und verbraucht mehr von deinem Tarif. **Ultra-Nachdenken** setzt bei besonders schwierigen Fragen zusätzliche Helfer ein und verbraucht am meisten. Bei einer neuen Machine ist **Wenig Nachdenken** eingestellt. Damit bekommst du gute Ergebnisse und verbrauchst deutlich weniger von deinem Tarif. Eine Änderung gilt ab der nächsten Nachricht.

Wenn du die Einstellung nur für einen Chat ändern möchtest, tippe unter dem Nachrichtenfeld auf das Modell oder die Nachdenk-Stufe. Wähle dort erneut **Einstellungen**, damit der Chat den Einstellungen folgt.

Prüfungen, dein Profil und vorab vorbereitete Entwürfe verwenden weiterhin ihr eigenes Modell.

## Limits

Wenn dein Tarif Nutzungslimits hat, zum Beispiel die 5-Stunden- und Wochenlimits eines ChatGPT- oder Claude-Tarifs, wird angezeigt, wie viel du bereits verbraucht hast und wann die Limits zurückgesetzt werden. Beim Ansehen wird dein Tarif nicht belastet.

## Platz für deine eigenen Chats

Hintergrundarbeit lässt Platz für deine eigenen Chats. Sie wird bei etwa 65 % des 5-Stunden-Limits pausiert. Prüfungen neuer Nachrichten laufen bis etwa 90 % des Wochenlimits weiter. Andere Arbeit nutzt pro Tag etwa ein Siebtel des Wochenlimits. Eine Anmeldung ohne Limits, zum Beispiel mit einem API-Schlüssel, wird nie pausiert.

Hintergrundarbeit läuft nie mit GPT-6 Astra. Bei einer Anmeldung bei ChatGPT wird vorerst GPT-6.1 Sol verwendet, auch wenn dein Hauptmodell GPT-6.2 Sol ist. Bei dieser Anmeldung kann 6.2 die zwischengespeicherten Anweisungen noch nicht wiederverwenden und verbraucht daher mehr von deinem Tarif. Deine Chats behalten das von dir ausgewählte Modell.

## Bevor ein Limit erreicht ist

Wenn dein ChatGPT-Tarif noch Resets übrig hat, zeigt die Seite Aufgaben eine kurze Zeile, sobald die Hintergrundarbeit langsamer wird: bei etwa 65 % des 5-Stunden-Limits oder 90 % des Wochenlimits. Dort steht, wie viel verbraucht ist und wie viele Resets noch übrig sind. **Einen Reset nutzen** setzt die Limits nach deiner Bestätigung zurück. × blendet die Zeile aus, bis dieses Limit zurückgesetzt wird. Ohne Resets wird nichts Neues angezeigt.

## Wenn ein Limit erreicht ist

Oben im Dashboard steht, welches Limit erreicht wurde und wann es zurückgesetzt wird. Die Arbeit wartet und wird dann an der Stelle fortgesetzt, an der sie unterbrochen wurde. Es geht nichts verloren. Wenn dein ChatGPT-Tarif Resets hat, setzt **Einen Reset nutzen** die Limits zurück. Andernfalls öffnet **Resets in ChatGPT ansehen** die entsprechende Seite in ChatGPT.

## Mit einem Ersatzmodell

Wenn für deine Machine ein Ersatzmodell in einem anderen Tarif oder bei einem anderen Anbieter eingerichtet ist, übernimmt es, sobald ein Limit erreicht ist. Es muss nichts warten. Oben im Dashboard steht dann: „ChatGPT-Limit erreicht, dein Ersatzmodell übernimmt.“ Wenn das Ersatzmodell nicht mehr funktioniert, gibt es wieder Pausen.

## Hauptmodell ändern

Das Hauptmodell wird für alles andere in The Machine verwendet. Ändere es bei einer gehosteten Machine auf deiner Einrichtungsseite unter „Deine KI“. Auf deinem eigenen Computer findest du weitere Informationen unter [ChatGPT](chatgpt.md), [Mistral](mistral.md) und im [Modell-Leitfaden](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
