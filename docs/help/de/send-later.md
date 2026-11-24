---
title: Später senden
area: cards
summary: Bestätige eine Nachricht jetzt und leg fest, wann sie gesendet wird. Wenn die andere Person zuerst schreibt, wartet die Aufgabe wieder auf dich.
covers: send-later
code: machine/store/send_later.py, machine/app/send_later.py, dashboard/todos-send-later.js
order: 13
keywords: schedule, scheduled, send at a time, delay, tomorrow morning, unsend, take back
translated: 29860e4848acce2e
---
## Nachricht planen

Klicke im Fenster, in dem du eine Nachricht prüfst, neben **Jetzt senden** auf **Später senden**. Wähle **In 2 Stunden**, **Morgen**, **Montag** oder **Datum wählen** und dann **Uhrzeit speichern**. Die Nachricht wird genau so gesendet, wie du sie gesehen hast, und zwar zur ausgewählten Zeit in deiner Zeitzone.

Das funktioniert mit E-Mail, Slack, WhatsApp, Telegram, Signal, Teams und Intercom. Nicht mit LinkedIn und X, weil deine Machine unmittelbar vor dem Versand nicht nach neuen Nachrichten suchen kann. Auch Antworten in Dokumenten sind ausgeschlossen.

Die Option gibt es auch unter **Neue E-Mail**. Mehrere Nachrichten, die du gemeinsam prüfst, werden alle zum ausgewählten Zeitpunkt gesendet.

## Während die Nachricht wartet

Die Aufgabe steht unter **Kommt später zurück** und am entsprechenden Tag im [Kalender](calendar.md). Dort siehst du die Nachricht und den Versandzeitpunkt, zum Beispiel: „Wird gesendet: Do., 26. Nov., 09:30“. Mit **Jetzt senden** wird sie sofort gesendet, mit **Uhrzeit ändern** wählst du eine andere Zeit und mit **Abbrechen** wird sie wieder zu einem Entwurf. Im Chat wird dasselbe angezeigt.

Wenn du den Entwurf bearbeitest, die Aufgabe erledigst, verwirfst oder wieder aktivierst, wird die Nachricht nicht gesendet. Du musst sie erneut bestätigen.

## Wenn die andere Person zuerst schreibt

Wenn die Person vor dem Versand schreibt, sendet deine Machine die Nachricht nicht. Die Aufgabe kommt mit der neuen Nachricht zurück, zum Beispiel: „Nicht gesendet: Sam Lee hat zuerst geschrieben.“ Du erhältst dann dieselbe Benachrichtigung wie bei einer zurückgestellten Aufgabe. Bei E-Mails zählt jede Adresse, die deine Machine für die Person kennt, in jedem verbundenen Postfach. Auch eine Antwort von jemand anderem im Gespräch zählt.

Eine automatische Antwort, zum Beispiel eine Abwesenheitsnotiz, verhindert den Versand nicht. Auch eine eigene Nachricht verhindert ihn nicht.

Unmittelbar vor dem Versand liest deine Machine den Gesprächsverlauf noch einmal. Wenn das nicht möglich ist, steht in der Aufgabe: „Nach neuen Nachrichten konnte noch nicht gesucht werden.“ Deine Machine versucht es eine Stunde lang erneut. Danach fragt sie dich, statt die Nachricht zu senden.

Bei WhatsApp prüft deine Machine die Nachrichten, die dein eigenes verknüpftes WhatsApp bis dahin erhalten hat.

## Wenn The Machine ausgeschaltet ist

Wenn deine Machine zu diesem Zeitpunkt ausgeschaltet, im Ruhezustand oder abgemeldet ist, wird die Nachricht gesendet, sobald sie wieder online ist, höchstens eine Stunde verspätet. Danach kommt die Aufgabe mit dem Hinweis „Nicht gesendet: Die Nachricht war mehr als eine Stunde verspätet.“ zurück und du entscheidest.

Wenn du auf einen anderen Computer wechselst, musst du geplante Nachrichten dort erneut bestätigen. Siehe [Umzug](moving.md).

## Wer Nachrichten planen kann

Nur du kannst das im Dashboard oder in der App tun. Deine Machine, ihr Chat, eine verbundene KI und andere Machines können keine Nachrichten planen. Unter [Aktivität](activity.md) siehst du, wann eine Nachricht geplant, geändert, abgebrochen, gesendet oder nicht gesendet wurde.
