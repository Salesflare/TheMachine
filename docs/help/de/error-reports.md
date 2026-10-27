---
title: Fehlerberichte
area: security
summary: Wenn etwas kaputtgeht, sagt deine Machine dem Team von The Machine, was fehlgeschlagen ist und wo im Code. Nie deine Nachrichten, Namen oder Adressen.
covers: error-reports
code: error_feed.py, dashboard.html
order: 4
---
## Was es ist

Wenn in The Machine etwas kaputtgeht, sendet deine Machine dem Team eine kurze Signatur des Fehlers, damit wir ihn beheben können, bevor ihn jemand melden muss. Das ist standardmäßig an und braucht [The Machine Network](/network).

## Was gesendet wird

Nur das, für jede Art von Fehler:

- die Art des Fehlers, etwa `KeyError` oder `TypeError`;
- seine Meldung ohne alles Spezifische: Zahlen, IDs, zitierter Text, E-Mail-Adressen, Links, Dateipfade und alles, was wie ein Schlüssel aussieht. Jedes andere Wort, das ein Name sein könnte, wird auch entfernt;
- wo es im eigenen Code von The Machine passiert ist: Datei, Funktion und Zeile, nie ein Ordner auf deinem Computer;
- die App-Version, wie oft es passiert ist und wann zum ersten und zum letzten Mal.

Ein echtes Beispiel: `IndexError`, `list index out of range`, bei `assistant.py:fault_event:7899`, Version `05b17ee6ac79`, 1 Mal.

## Was nie gesendet wird

Was in deinen Nachrichten, Aufgaben, Entwürfen oder Chats steht. Namen, E-Mail-Adressen, Telefonnummern, Links, Tokens oder Passwörter. Um welches Konto oder welche Person es ging.

## Woher Fehler kommen

- der Dienst und seine Jobs: Prüfungen, Aufgaben vorbereiten, Chat, Verbindungen und Syncs;
- das Dashboard in deinem Browser;
- fehlgeschlagene Jobs von Claude Code und Codex: nur das Tool und die Art des Fehlers.

Derselbe Fehler zählt einmal, mit einer Anzahl. Höchstens ein Paket alle 10 Minuten. Das Team bewahrt sie 30 Tage auf.

## Ausschalten

Schalte in Einstellungen, Sicherheit **Fehlerberichte senden** aus. Dann wird nichts mehr erfasst oder gesendet, und was noch wartete, wird gelöscht. Fehler erscheinen weiterhin auf deiner eigenen Machine, die eine Lösung anbieten kann.

Siehe [Sicherheit und Datenschutz](security-and-privacy.md).
