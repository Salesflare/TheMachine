---
title: Fehlerberichte
area: security
summary: Wenn etwas schiefläuft, teilt deine Machine dem Team von The Machine mit, was fehlgeschlagen ist und wo im Code. Niemals deine Nachrichten, Namen oder Adressen.
covers: error-reports
code: error_feed.py, error_words.py, pacing.py, dashboard.html, sw.js
order: 4
translated: e1d4d602255cde39
---
## Was das ist

Wenn in The Machine etwas schiefläuft, sendet deine Machine unserem Team eine kurze, anonyme Nachricht zum Fehler. So können wir ihn beheben, bevor ihn jemand meldet. Die Funktion ist standardmäßig aktiviert und benötigt [The Machine Network](/network).

## Was gesendet wird

Nur Folgendes, je nach Fehlertyp:

- der Fehlertyp, zum Beispiel `KeyError`;
- die Fehlermeldung, nachdem alles Spezifische entfernt wurde: Zahlen, IDs, zitierter Text, E-Mail-Adressen, Links, Dateipfade, Schlüssel und alle Wörter, die ein Name sein könnten;
- die Stelle in The Machines eigenem Code, an der der Fehler aufgetreten ist, niemals ein Ordner auf deinem Computer;
- die App-Version, wie oft der Fehler aufgetreten ist und wann zum ersten und letzten Mal.

Zum Beispiel: `IndexError`, `list index out of range`, bei `machine/faults.py:fault_event:246`, Version `05b17ee6ac79`, 1 Mal.

## Was niemals gesendet wird

Der Inhalt deiner Nachrichten, Aufgaben, Entwürfe oder Chats. Namen, E-Mail-Adressen, Telefonnummern, Links oder Passwörter. Um welches Konto oder welche Person es ging.

## Woher Fehler kommen

- Hintergrundaufgaben: neue Nachrichten prüfen, Aufgaben vorbereiten, Chats, Verbindungen und Synchronisierungen;
- das Dashboard in deinem Browser oder in der App, einschließlich angezeigter Fehler;
- fehlgeschlagene oder abgelaufene Anfragen des Dashboards: welche Anfrage, niemals was sie gesendet hat;
- fehlgeschlagene Aufträge von Coding-Agenten: nur das Tool und die Art des Fehlers;
- der kurze Test deiner KI, wenn er fehlschlägt: der Fehler der KI, nachdem alles Spezifische entfernt wurde.

Eine Prüfung, die wegen des Nutzungslimits deines KI-Tarifs angehalten wurde, ist kein Fehler und wird nicht gesendet. Sie wartet, bis das Limit zurückgesetzt wird.

Ein Connector, den du selbst hinzugefügt hast (deine eigene Datei in `connectors/`), sendet nur den Namen des Dienstes und die Fehlerbezeichnung, zum Beispiel `notes` und `notes_http: HTTP unauthorized`, damit wir bei der Fehlerbehebung helfen können. Sonst nichts aus seinem Code. Die Verbindungskarte zeigt den vollständigen Fehler.

Wiederholungen desselben Fehlers werden gezählt, aber nicht erneut gesendet. Höchstens alle 10 Minuten wird ein Paket gesendet. Wir speichern die Berichte 30 Tage lang.

## Drosselung

Hintergrundaufgaben werden pausiert, wenn die Limits deines KI-Tarifs knapp werden. So bleibt genug Platz für deine eigenen Chats (siehe [Dein KI-Modell](model.md)).

Wenn Fehlerberichte aktiviert sind, teilt uns deine Machine außerdem einmal täglich mit, wie oft das passiert ist: für jede Pause die Stunde, das betreffende Limit, die Dauer und wie viele Aufträge gewartet haben. Nicht, worum es bei den Aufträgen ging.

## Deaktivieren

Deaktiviere unter **Einstellungen** > **Sicherheit** die Option **Fehlerberichte senden**. Es werden keine weiteren Daten erfasst oder gesendet und wartende Berichte werden gelöscht. Fehler werden weiterhin auf deiner Machine angezeigt. Sie kann dir auch eine Lösung vorschlagen.

Weitere Informationen findest du unter [Sicherheit und Datenschutz](security-and-privacy.md).
