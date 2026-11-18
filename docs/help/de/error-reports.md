---
title: Fehlerberichte
area: security
summary: Wenn etwas schiefläuft, teilt deine Machine dem Team von The Machine mit, was fehlgeschlagen ist und wo im Code. Niemals deine Nachrichten, Namen oder Adressen.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: 2253a0d695fe898c
---
## Was das ist

Wenn etwas in The Machine schiefläuft, sendet deine Machine unserem Team eine kurze, anonyme Meldung zum Fehler. So können wir ihn beheben, bevor ihn jemand meldet. Die Funktion ist standardmäßig aktiviert und benötigt [The Machine Network](/network).

## Was übermittelt wird

Nur diese Angaben, je nach Fehlertyp:

- die Art des Fehlers, zum Beispiel `KeyError`;
- die Fehlermeldung, nachdem alles Spezifische entfernt wurde: Zahlen, IDs, zitierter Text, E-Mail-Adressen, Links, Dateipfade, Schlüssel und alle Wörter, die Namen sein könnten;
- die Stelle im eigenen Code von The Machine, niemals ein Ordner auf deinem Computer;
- die App-Version, wie oft der Fehler aufgetreten ist sowie Zeitpunkt des ersten und letzten Auftretens.

Zum Beispiel: `IndexError`, `list index out of range`, bei `machine/faults.py:fault_event:246`, Version `05b17ee6ac79`, 1 Mal.

## Was niemals übermittelt wird

Der Inhalt deiner Nachrichten, Aufgaben, Entwürfe oder Chats. Namen, E-Mail-Adressen, Telefonnummern, Links oder Passwörter. Um welches Konto oder welche Person es ging.

## Woher Fehler kommen

- Hintergrundaufgaben: neue Nachrichten prüfen, Aufgaben vorbereiten, Chats, Verbindungen und Synchronisierungen;
- das Dashboard in deinem Browser oder in der App, einschließlich Fehlern, die dort angezeigt wurden;
- fehlgeschlagene oder abgelaufene Anfragen des Dashboards: um welche Anfrage es ging, niemals was sie gesendet hat;
- fehlgeschlagene Jobs von Coding-Agenten: nur das Tool und die Art des Fehlers;
- der kurze Test deiner KI, wenn er fehlschlägt: der Fehler der KI, nachdem alles Spezifische entfernt wurde.

Ein Connector, den du selbst hinzugefügt hast, also eine eigene Datei in `connectors/`, übermittelt nur den Namen des Dienstes und die Fehlerbezeichnung, zum Beispiel `notes` und `notes_http: HTTP unauthorized`, damit wir bei der Behebung helfen können. Nichts anderes aus dem Code. Die Verbindungskarte zeigt den vollständigen Fehler.

Wiederholungen desselben Fehlers werden gezählt, aber nicht erneut gesendet. Höchstens alle 10 Minuten wird ein Paket gesendet. Wir speichern die Berichte 30 Tage lang.

## Drosselung

Wenn die Limits deines KI-Tarifs knapp werden, wartet die Hintergrundarbeit, damit genug Kapazität für deine Chats bleibt (siehe [Dein KI-Modell](model.md)).

Wenn Fehlerberichte aktiviert sind, teilt uns deine Machine außerdem einmal täglich mit, wie oft das passiert ist: pro Pause die Stunde, das betreffende Limit, die Dauer und wie viele Jobs warten mussten. Nicht, worum es in den Jobs ging.

## Funktion ausschalten

Deaktiviere unter **Einstellungen** und **Sicherheit** die Option **Fehlerberichte senden**. Danach werden keine weiteren Fehler erfasst oder gesendet, und wartende Berichte werden gelöscht. Fehler werden weiterhin auf deiner Machine angezeigt. Sie kann dir auch eine Lösung vorschlagen.

Weitere Informationen findest du unter [Sicherheit und Datenschutz](security-and-privacy.md).
