---
title: Fehlerberichte
area: security
summary: Wenn etwas nicht funktioniert, teilt deine Machine dem Team von The Machine mit, was fehlgeschlagen ist und wo im Code. Niemals deine Nachrichten, Namen oder Adressen.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: 4dc53a854d15f1a3
---
## Was gesendet wird

Wenn in The Machine etwas nicht funktioniert, sendet deine Machine unserem Team eine kurze, anonyme Fehlermeldung. So können wir den Fehler beheben, bevor ihn jemand meldet. Die Funktion ist standardmäßig aktiviert und erfordert [The Machine Network](/network).

## Welche Daten gesendet werden

Nur diese Daten, je nach Fehlertyp:

- der Fehlertyp, zum Beispiel `KeyError`;
- die Fehlermeldung ohne konkrete Angaben: Zahlen, IDs, zitierte Texte, E-Mail-Adressen, Links, Dateipfade, Schlüssel und alle Wörter, die Namen sein könnten;
- die Stelle im Code von The Machine, an der der Fehler aufgetreten ist, niemals ein Ordner auf deinem Computer;
- die App-Version, wie oft der Fehler aufgetreten ist sowie wann er zum ersten und letzten Mal aufgetreten ist.

Zum Beispiel: `IndexError`, `list index out of range`, bei `machine/faults.py:fault_event:246`, Version `05b17ee6ac79`, 1 Mal.

## Welche Daten niemals gesendet werden

Der Inhalt deiner Nachrichten, Aufgaben, Entwürfe oder Chats. Namen, E-Mail-Adressen, Telefonnummern, Links oder Passwörter. Um welches Konto oder welche Person es ging.

## Woher die Fehler kommen

- Hintergrundaufgaben: neue Nachrichten prüfen, Aufgaben vorbereiten, Chats, Verbindungen und Synchronisierungen;
- das Dashboard in deinem Browser oder in der App, einschließlich angezeigter Fehler;
- fehlgeschlagene oder abgelaufene Anfragen des Dashboards: welche Anfrage es war, niemals was sie gesendet hat;
- fehlgeschlagene Jobs von Coding-Agenten: nur das Tool und die Art des Fehlers;
- der kurze Test deiner KI, wenn er fehlschlägt: der Fehler der KI, ohne konkrete Angaben.

Wiederholungen desselben Fehlers werden gezählt und nicht erneut gesendet. Höchstens alle 10 Minuten wird ein Paket gesendet. Wir speichern die Daten 30 Tage lang.

## Pausen

Wenn die Limits deines KI-Tarifs knapp werden, pausieren Hintergrundaufgaben, damit genug Kapazität für deine Chats bleibt (siehe [Dein KI-Modell](model.md)).

Wenn Fehlerberichte aktiviert sind, teilt deine Machine uns außerdem einmal täglich mit, wie oft das passiert ist: für jede Pause die Stunde, das betreffende Limit, die Dauer und wie viele Aufgaben gewartet haben. Keine Angaben dazu, um welche Aufgaben es ging.

## Funktion ausschalten

Deaktiviere unter **Einstellungen** und **Sicherheit** die Option **Fehlerberichte senden**. Danach wird nichts Weiteres erfasst oder gesendet, und bereits wartende Daten werden gelöscht. Fehler werden weiterhin auf deiner eigenen Machine angezeigt, wo dir eine Lösung angeboten werden kann.

Weitere Informationen findest du unter [Sicherheit und Datenschutz](security-and-privacy.md).
