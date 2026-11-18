---
title: Fehlerberichte
area: security
summary: Wenn etwas schiefläuft, teilt deine Machine dem Team von The Machine mit, was fehlgeschlagen ist und an welcher Stelle im Code. Niemals deine Nachrichten, Namen oder Adressen.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: f67d18a44999cfce
---
## Was das ist

Wenn auf deiner Machine etwas schiefläuft, sendet sie unserem Team eine kurze, anonyme Meldung zum Fehler. So können wir ihn beheben, bevor ihn jemand meldet. Die Funktion ist standardmäßig aktiviert und benötigt [The Machine Network](/network).

## Welche Daten gesendet werden

Nur diese Angaben, je nach Fehlerart:

- die Fehlerart, zum Beispiel `KeyError`;
- die Fehlermeldung, aus der alle spezifischen Angaben entfernt wurden: Zahlen, IDs, zitierter Text, E-Mail-Adressen, Links, Dateipfade, Schlüssel und alle Wörter, die Namen sein könnten;
- die Stelle im Code von The Machine, an der der Fehler aufgetreten ist, niemals ein Ordner auf deinem Computer;
- die App-Version, wie oft der Fehler aufgetreten ist sowie wann er zum ersten und letzten Mal auftrat.

Zum Beispiel: `IndexError`, `list index out of range`, bei `machine/faults.py:fault_event:246`, Version `05b17ee6ac79`, 1-mal.

## Was niemals gesendet wird

Die Inhalte deiner Nachrichten, Aufgaben, Entwürfe oder Chats. Namen, E-Mail-Adressen, Telefonnummern, Links oder Passwörter. Um welches Konto oder welche Person es ging.

## Woher Fehler kommen

- Hintergrundaufgaben: neue Nachrichten prüfen, Aufgaben vorbereiten, Chats, Verbindungen und Synchronisierungen;
- das Dashboard in deinem Browser oder in der App, einschließlich der dort angezeigten Fehler;
- fehlgeschlagene oder abgelaufene Anfragen vom Dashboard: um welche Anfrage es ging, niemals aber, was sie gesendet hat;
- fehlgeschlagene Aufträge von Coding-Agenten: nur das Tool und die Art des Fehlers;
- der kurze Test deiner KI, wenn er fehlschlägt: der Fehler der KI, ohne spezifische Angaben.

Ein Connector, den du selbst hinzugefügt hast (deine eigene Datei in `connectors/`), sendet niemals Fehler. Die Karte der Verbindung zeigt sie an.

Wiederholungen desselben Fehlers werden gezählt, aber nicht erneut gesendet. Höchstens alle 10 Minuten wird ein Fehlerpaket gesendet. Wir speichern die Berichte 30 Tage lang.

## Taktung

Hintergrundaufgaben warten, wenn die Limits deines KI-Plans knapp werden, damit genug Kapazität für deine Chats bleibt (siehe [Dein KI-Modell](model.md)).

Wenn Fehlerberichte aktiviert sind, meldet uns deine Machine außerdem einmal täglich, wie oft das vorkam: für jede Pause die Stunde, welches Limit erreicht wurde, wie lange sie dauerte und wie viele Aufträge gewartet haben. Es wird nichts darüber mitgeteilt, worum es bei den Aufträgen ging.

## Deaktivieren

Deaktiviere unter **Einstellungen** > **Sicherheit** die Option **Fehlerberichte senden**. Es werden keine weiteren Daten erfasst oder gesendet, und alles, was noch ausstand, wird gelöscht. Fehler werden weiterhin auf deiner Machine angezeigt. Sie kann dir eine Lösung vorschlagen.

Weitere Informationen findest du unter [Sicherheit und Datenschutz](security-and-privacy.md).
