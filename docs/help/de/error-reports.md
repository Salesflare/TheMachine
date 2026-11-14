---
title: Fehlerberichte
area: security
summary: Wenn etwas schiefläuft, teilt deine Machine dem Team von The Machine mit, was fehlgeschlagen ist und wo im Code. Niemals deine Nachrichten, Namen oder Adressen.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: 03a8649f2f634b59
---
## Was das ist

Wenn etwas in The Machine schiefläuft, schickt deine Machine unserem Team eine kurze, anonyme Meldung zum Fehler. So können wir ihn beheben, bevor ihn jemand meldet. Die Funktion ist standardmäßig aktiviert und erfordert [The Machine Network](/network).

## Was gesendet wird

Nur Folgendes, je Fehlerart:

- die Art des Fehlers, zum Beispiel `KeyError`;
- die Fehlermeldung, aus der alles Spezifische entfernt wurde: Zahlen, IDs, zitierter Text, E-Mail-Adressen, Links, Dateipfade, Schlüssel und jedes Wort, das ein Name sein könnte;
- wo der Fehler im Code von The Machine aufgetreten ist, niemals in einem Ordner auf deinem Computer;
- die App-Version, wie oft der Fehler aufgetreten ist und wann zum ersten und letzten Mal.

Zum Beispiel: `IndexError`, `list index out of range`, bei `machine/faults.py:fault_event:246`, Version `05b17ee6ac79`, 1 Mal.

## Was niemals gesendet wird

Der Inhalt deiner Nachrichten, Aufgaben, Entwürfe oder Chats. Namen, E-Mail-Adressen, Telefonnummern, Links oder Passwörter. Um welches Konto oder welche Person es ging.

## Woher Fehler kommen

- Hintergrundprozesse: neue Nachrichten prüfen, Aufgaben vorbereiten, Chats, Verbindungen und Synchronisierungen;
- das Dashboard in deinem Browser oder in der App, einschließlich der Fehler, die dir angezeigt wurden;
- fehlgeschlagene oder abgelaufene Anfragen vom Dashboard: welche Anfrage, niemals was sie gesendet hat;
- fehlgeschlagene Jobs von Coding-Agenten: nur das Tool und die Art des Fehlers.

Wiederholungen desselben Fehlers werden gezählt, aber nicht erneut gesendet. Höchstens alle 10 Minuten wird ein Paket gesendet. Wir bewahren die Berichte 30 Tage lang auf.

## Pausen

Hintergrundprozesse werden angehalten, wenn die Limits deines KI-Plans knapp werden. So bleibt genug Platz für deine eigenen Chats (siehe [Dein KI-Modell](model.md)).

Wenn Fehlerberichte aktiviert sind, teilt uns deine Machine außerdem einmal täglich mit, wie oft das passiert ist: pro Pause die Stunde, welches Limit erreicht wurde, wie lange die Pause dauerte und wie viele Jobs gewartet haben. Nichts darüber, worum es bei den Jobs ging.

## Deaktivieren

Deaktiviere unter **Einstellungen** > **Sicherheit** die Option **Fehlerberichte senden**. Danach werden keine weiteren Fehler erfasst oder gesendet, und bereits wartende Berichte werden gelöscht. Fehler werden weiterhin auf deiner Machine angezeigt. Sie kann dir eine Lösung vorschlagen.

Weitere Informationen findest du unter [Sicherheit und Datenschutz](security-and-privacy.md).
