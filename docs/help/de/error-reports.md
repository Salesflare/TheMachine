---
title: Fehlerberichte
area: security
summary: Wenn etwas schiefläuft, teilt deine Machine dem Team von The Machine mit, was fehlgeschlagen ist und wo im Code. Niemals deine Nachrichten, Namen oder Adressen.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: fd3e1c2d68b93a35
---
## Was das ist

Wenn in The Machine etwas schiefläuft, sendet deine Machine unserem Team eine kurze, anonyme Meldung zum Fehler, damit wir ihn beheben können, bevor ihn jemand meldet. Fehlerberichte sind standardmäßig aktiviert und erfordern [The Machine Network](/network).

## Welche Daten gesendet werden

Nur diese Daten, je nach Fehlerart:

- die Fehlerart, zum Beispiel `KeyError`;
- die Fehlermeldung, aus der alle spezifischen Angaben entfernt wurden: Zahlen, IDs, zitierter Text, E-Mail-Adressen, Links, Dateipfade, Schlüssel und alle Wörter, die Namen sein könnten;
- die Stelle im Code von The Machine, an der der Fehler auftrat, niemals ein Ordner auf deinem Computer;
- die App-Version, wie oft der Fehler auftrat sowie den Zeitpunkt des ersten und letzten Auftretens.

Ein echtes Beispiel: `IndexError`, `list index out of range`, bei `assistant.py:fault_event:7899`, Version `05b17ee6ac79`, 1 Mal.

## Was niemals gesendet wird

Was in deinen Nachrichten, Aufgaben, Entwürfen oder Chats steht. Namen, E-Mail-Adressen, Telefonnummern, Links oder Passwörter. Um welches Konto oder welche Person es ging.

## Woher Fehler kommen

- Hintergrundaufgaben: neue Nachrichten prüfen, Aufgaben vorbereiten, Chat, Verbindungen und Synchronisierungen;
- das Dashboard in deinem Browser oder in der App, einschließlich der Fehler, die es dir angezeigt hat;
- Anfragen vom Dashboard, die fehlschlagen oder in einen Timeout laufen: welche Anfrage, niemals was sie gesendet hat;
- fehlgeschlagene Aufträge von Coding-Agenten: nur das Tool und die Art des Fehlers.

Wiederholungen desselben Fehlers werden gezählt, aber nicht erneut gesendet. Höchstens alle 10 Minuten wird ein Datenpaket gesendet. Wir speichern die Daten 30 Tage lang.

## Zeitliche Begrenzung

Hintergrundaufgaben werden angehalten, wenn die Limits deines KI-Tarifs knapp werden, damit genug Spielraum für deine eigenen Chats bleibt (siehe [Dein KI-Modell](model.md)).

Wenn Fehlerberichte aktiviert sind, teilt deine Machine uns außerdem einmal täglich mit, wie oft das passiert ist: pro Pause die Stunde, welches Limit, wie lange und wie viele Aufträge gewartet haben. Keine Angaben dazu, worum es bei den Aufträgen ging.

## Ausschalten

Deaktiviere unter **Einstellungen** > **Sicherheit** die Option **Fehlerberichte senden**. Es werden keine weiteren Daten erfasst oder gesendet, und ausstehende Daten werden gelöscht. Fehler werden weiterhin auf deiner Machine angezeigt. Sie kann dir eine Lösung anbieten.

Siehe [Sicherheit und Datenschutz](security-and-privacy.md).
