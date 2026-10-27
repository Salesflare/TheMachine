---
title: Modell
area: settings
summary: Welches KI-Modell für dich antwortet, wie gründlich es nachdenkt und wie viel der Limits deines Tarifs es schon verbraucht hat.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
---
In **Einstellungen** zeigt **Modell** das Modell, das Hintergrundarbeit nutzt (markiert mit **Hintergrundarbeit**), und wie du angemeldet bist, etwa mit ChatGPT.

## Modell und Nachdenken für Chats

Wähle unter **Chats** das Modell und die Nachdenkstufe für deine Aufgaben-Chats und die Hilfe. Die Liste hat nur die Modelle, die deine Anmeldung anbietet, etwa die von ChatGPT, wenn du dich mit ChatGPT angemeldet hast, und jedes Modell nur die Stufen, die es hat.

Mehr Nachdenken beantwortet schwierigere Fragen besser, ist aber langsamer und verbraucht mehr von deinem Tarif. **Ultra-Nachdenken** holt Helfer für die schwierigsten Fragen dazu: am langsamsten, und es verbraucht am meisten. Eine Änderung gilt ab der nächsten Nachricht.

Ein Chat kann etwas anderes nutzen: Tippe unter seinem Nachrichtenfeld auf das Modell oder die Nachdenkstufe. Diese Wahl gilt nur für diesen Chat. Wähle wieder dasselbe wie in den Einstellungen, um den Einstellungen zu folgen.

Reviews, dein Profil und vorab vorbereitete Entwürfe behalten ihr eigenes Modell.

## Limits

Wenn dein Tarif Nutzungslimits hat, siehst du, wie viel von jedem verbraucht ist und wann es zurückgesetzt wird, zum Beispiel das 5-Stunden-Limit und das Wochenlimit eines ChatGPT- oder Claude-Tarifs. Das Anzeigen verbraucht nie etwas von deinem Tarif.

## Platz für deine eigenen Chats

Hintergrundarbeit (Prüfungen, dein Profil, vorab vorbereitete Entwürfe) lässt Platz für deine eigenen Chats. Sie pausiert bei etwa 65 % des 5-Stunden-Limits. Prüfungen dessen, was reingekommen ist, laufen bis etwa 90 % des Wochenlimits; der Rest verteilt es auf etwa ein Siebtel pro Tag. Eine Anmeldung ohne Nutzungslimits, etwa ein API-Schlüssel, wird nie pausiert.

Hintergrundarbeit läuft nie auf GPT-6 Astra. Sie nutzt stattdessen GPT-6.1 Sol.

## Wenn ein Limit erreicht ist

Oben im Dashboard steht, welches Limit erreicht ist und wann es zurückgesetzt wird. Die Arbeit wartet und macht dann dort weiter, wo sie aufgehört hat. Nichts geht verloren. Manche ChatGPT-Tarife haben Resets: **Reset nutzen** setzt die Limits nach einer Bestätigung zurück. Sonst öffnet **Resets in ChatGPT ansehen** die Seite von ChatGPT selbst.

## Das Hauptmodell ändern

Das Hauptmodell nutzt der Rest von The Machine. Auf einer gehosteten Machine wählst du auf deiner Einrichtungsseite unter Dein Modell ein anderes. Auf deinem eigenen Computer änderst du es in OpenClaw. Siehe [ChatGPT](chatgpt.md) und den [Modell-Leitfaden](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
