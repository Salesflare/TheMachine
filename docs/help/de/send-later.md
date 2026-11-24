---
title: Später senden
area: cards
summary: Wähle neben „Jetzt senden“ die Option „Später senden“, um eine E-Mail oder Nachricht zu planen. Du bestätigst sie jetzt und legst fest, wann sie gesendet wird. Wenn die andere Person zuerst schreibt, wartet die Nachricht wieder auf dich.
covers: send-later
code: machine/store/send_later.py, machine/app/send_later.py, dashboard/todos-send-later.js
order: 13
keywords: schedule, scheduled, schedule an email, send at a time, delay, tomorrow morning, unsend, take back
translated: 6fa6af155c337981
---
## Nachricht planen

Wähle im Fenster, in dem du eine Nachricht prüfst, neben **Jetzt senden** die Option **Später senden**. Wähle **In 2 Stunden**, **Morgen**, **Montag** oder **Datum wählen** und dann **Uhrzeit speichern**. Die Nachricht wird genau so gesendet, wie du sie gesehen hast, und zwar zur festgelegten Zeit in deiner Zeitzone.

Das funktioniert mit E-Mail, Slack, WhatsApp, Telegram, Signal, Teams und Intercom. Nicht mit LinkedIn und X, weil deine Machine dort nicht direkt vor dem Senden nach neuen Nachrichten suchen kann, und auch nicht mit einer Antwort in einem Dokument.

Auch unter **Neue E-Mail** findest du diese Option. Mehrere Nachrichten, die du zusammen prüfst, werden alle zum ausgewählten Zeitpunkt gesendet.

## Während die Nachricht wartet

Die Aufgabe findest du unter **Kommt später zurück** und am entsprechenden Tag im [Kalender](calendar.md), zusammen mit der Nachricht und dem Sendezeitpunkt: „Wird gesendet: Do., 26. Nov., 09:30“. Mit **Jetzt senden** wird die Nachricht sofort gesendet, mit **Uhrzeit ändern** wählst du einen anderen Zeitpunkt und mit **Abbrechen** wird sie wieder zum Entwurf. Im Chat wird dasselbe angezeigt.

Wenn du den Entwurf bearbeitest, die Aufgabe erledigst, sie verwirfst oder zurückholst, wird die Nachricht nicht gesendet. Du musst sie erneut bestätigen.

## Wenn die andere Person zuerst schreibt

Wenn die Person vor dem Sendezeitpunkt schreibt, sendet deine Machine die Nachricht nicht. Die Aufgabe kommt mit der Nachricht der Person zurück, zum Beispiel: „Nicht gesendet: Sam Lee hat zuerst geschrieben.“ Du erhältst dieselbe Benachrichtigung wie bei einer zurückgestellten Aufgabe. Bei einer E-Mail zählen alle Adressen, unter denen deine Machine die Person kennt, und alle verknüpften Postfächer. Auch eine Antwort von einer anderen Person im Gespräch zählt.

Eine automatische Antwort, zum Beispiel eine Abwesenheitsnotiz, verhindert das Senden nicht. Deine eigenen Nachrichten auch nicht.

Direkt vor dem Senden liest deine Machine den Gesprächsverlauf noch einmal. Wenn das nicht möglich ist, steht in der Aufgabe „Konnte noch nicht nach neuen Nachrichten suchen.“ Deine Machine versucht es eine Stunde lang erneut. Danach fragt sie dich, statt die Nachricht zu senden.

Bei WhatsApp prüft deine Machine die Nachrichten, die dein eigenes verknüpftes WhatsApp bisher empfangen hat.

## Wenn The Machine ausgeschaltet ist

Wenn deine Machine zu diesem Zeitpunkt ausgeschaltet, im Ruhezustand oder abgemeldet ist, wird die Nachricht gesendet, sobald sie wieder verfügbar ist, höchstens eine Stunde später. Danach kommt die Aufgabe mit dem Hinweis „Nicht gesendet: Die Nachricht war mehr als eine Stunde verspätet.“ zurück und du entscheidest, was passiert.

Wenn du zu einem anderen Computer wechselst, musst du geplante Nachrichten dort erneut bestätigen. Weitere Informationen findest du unter [Gerätewechsel](moving.md).

## Wer Nachrichten planen kann

Nur du, im Dashboard oder in der App. Deine Machine, ihr Chat, eine von dir verbundene KI und andere Machines können keine Nachrichten planen. Unter [Aktivität](activity.md) siehst du, wann eine Nachricht geplant, geändert, abgebrochen, gesendet oder nicht gesendet wurde.
