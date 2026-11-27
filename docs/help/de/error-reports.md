---
title: Fehlerberichte
area: security
summary: Wenn etwas schiefläuft, teilt deine Machine dem Team von The Machine mit, was nicht funktioniert hat und wo im Code der Fehler aufgetreten ist. Deine Nachrichten, Namen und Adressen werden nie gesendet.
covers: error-reports
code: error_feed.py, error_words.py, pacing.py, dashboard.html, sw.js
order: 4
translated: d474cfa6bcefd25a
---
## Was Fehlerberichte enthalten

Wenn in The Machine etwas schiefläuft, sendet deine Machine unserem Team eine kurze, anonyme Fehlermeldung. So können wir den Fehler beheben, bevor ihn jemand meldet. Fehlerberichte sind standardmäßig aktiviert und erfordern [The Machine Network](/network).

## Welche Daten gesendet werden

Nur diese Angaben, je nach Fehlertyp:

- der Fehlertyp, zum Beispiel `KeyError`;
- die Fehlermeldung, aus der alle spezifischen Angaben entfernt wurden: Zahlen, IDs, zitierter Text, E-Mail-Adressen, Links, Dateipfade, Schlüssel und alle Wörter, die Namen sein könnten;
- die Stelle im Code von The Machine, an der der Fehler aufgetreten ist, niemals ein Ordner auf deinem Computer;
- die App-Version, wie oft der Fehler aufgetreten ist und wann er zum ersten und letzten Mal aufgetreten ist.

Zum Beispiel: `IndexError`, `list index out of range`, bei `machine/faults.py:fault_event:246`, Version `05b17ee6ac79`, 1-mal.

## Was nie gesendet wird

Der Inhalt deiner Nachrichten, Aufgaben, Entwürfe oder Chats. Namen, E-Mail-Adressen, Telefonnummern, Links oder Passwörter. Um welches Konto oder welche Person es ging.

## Woher Fehler kommen

- Hintergrundaufgaben: neue Nachrichten prüfen, Aufgaben vorbereiten, Chats, Verbindungen und Synchronisierungen;
- das Dashboard, im Browser oder in der App, einschließlich der dort angezeigten Fehler;
- fehlgeschlagene oder abgelaufene Anfragen des Dashboards: welche Anfrage es war, niemals, was sie gesendet hat;
- fehlgeschlagene Jobs von Coding-Agenten: nur das verwendete Tool und die Art des Fehlers;
- der kurze Test deiner KI, wenn er fehlschlägt: der Fehler der KI, aus dem alle spezifischen Angaben entfernt wurden.

Eine Prüfung, die wegen des Nutzungslimits deines KI-Tarifs angehalten wurde, ist kein Fehler und wird nicht gesendet. Sie wartet, bis das Limit zurückgesetzt wird. Auch eine Prüfung, die fehlschlägt, weil deine KI abgemeldet ist, gilt nicht als Fehler: **Braucht dich** fordert dich auf, dich wieder anzumelden.

Ein selbst hinzugefügter Connector (eine eigene Datei in `connectors/`) sendet nur den Namen seines Dienstes und die Fehlerbezeichnung, zum Beispiel `notes` und `notes_http: HTTP unauthorized`, damit wir bei der Behebung helfen können. Aus dem Code wird nichts anderes gesendet. Die Verbindungskarte zeigt den vollständigen Fehler.

Wiederholungen desselben Fehlers werden gezählt, aber nicht erneut gesendet. Es wird höchstens alle 10 Minuten ein Fehlerbericht gesendet. Wir speichern die Berichte 30 Tage lang.

## Drosselung

Hintergrundaufgaben werden pausiert, wenn die Limits deines KI-Tarifs knapp werden, damit genug Spielraum für deine eigenen Chats bleibt (siehe [Dein KI-Modell](model.md)).

Wenn Fehlerberichte aktiviert sind, teilt deine Machine uns außerdem einmal täglich mit, wie oft das passiert ist: pro Pause die Stunde, das jeweilige Limit, die Dauer und die Anzahl der wartenden Jobs. Es werden keine Angaben zu den Jobs selbst gesendet.

## Fehlerberichte deaktivieren

Deaktiviere unter **Einstellungen** unter **Sicherheit** die Option **Fehlerberichte senden**. Danach werden keine weiteren Fehler erfasst oder gesendet und wartende Fehlerberichte werden gelöscht. Fehler werden weiterhin auf deiner Machine angezeigt. Dort kann dir auch eine Lösung angeboten werden.

Weitere Informationen findest du unter [Sicherheit und Datenschutz](security-and-privacy.md).
