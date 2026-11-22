---
title: Support kontaktieren
area: troubleshooting
summary: Melde einen Fehler aus deinem Dashboard, schreib uns oder lass unser Team einen Tag lang auf deine Machine schauen.
covers: support-bundle, support-access
code: support.py, cli.py, dashboard.html, fleet.py
site: Report a problem
order: 9
translated: 419a75e887b25e20
---
## Schreib uns

Schick eine E-Mail an support@themachine.computer. Ein Mensch antwortet.

Auf einer gehosteten Machine steht in der Fußzeile des Dashboards „Stimmt etwas nicht?“. Das öffnet das Formular **Ein Problem melden** deines Kontos.

## Einen Fehler melden

Öffne **Hilfe**, dann **Fehler melden**. Auch eine Fehlermeldung hat einen Button **Fehler melden**.

1. Sag, was schiefging.
2. Füge einen Screenshot hinzu, wenn es hilft: **Screenshot machen** vom Dashboard oder **Bild anhängen**.
3. Lass **Supportbericht mitschicken** möglichst an. Das schickt Versionen, Prüfungen und letzte Fehler mit, ohne Nachrichten, Schlüssel oder Adressen, und unser Team darf 24 Stunden lang die Logs und Einstellungen deiner Machine lesen. Siehe [Support-Zugriff](get-support.md#support-access). Ohne Haken gehen nur dein Text und dein Screenshot.
4. Tippe auf **Senden**. Das Formular schließt sich sofort, und der Supportbericht folgt von selbst.

Ab da kümmern wir uns. Eine selbst gehostete Machine kann einen Bericht senden, wenn sie im Network ist. Sonst schreib uns.

Oder sag deiner Machine einfach im Chat, dass etwas nicht stimmt. Sie öffnet **Fehler melden** für dich, schon ausgefüllt mit deinen Worten und einer kurzen Zusammenfassung. Nichts geht raus, bis du auf **Senden** tippst.

Wenn wir einen Bug beheben, den du gemeldet hast, und deine Machine die Korrektur hat, sagen wir es dir einmal: eine kurze Zeile in deinem Dashboard und eine kurze E-Mail. Eine selbst gehostete Machine erfährt es, wenn sie im Network ist.

Die Zeile fragt, ob es jetzt wirklich funktioniert. Tippe auf **Funktioniert jetzt**, oder auf **Noch nicht richtig**, um zu sagen, was noch nicht stimmt, gern mit einem Bild. Das kommt als neue Meldung bei uns an, verknüpft mit der ersten. **×** schließt die Zeile ohne Antwort.

Offline oder viele Berichte kurz hintereinander gesendet? Dein Bericht geht nicht verloren. Deine Machine behält ihn und sendet ihn später von selbst. Bis dahin steht er unter **Wartet auf den Versand**.

## Support-Zugriff

Unser Team kann für dich auf deine Machine schauen, aber erst, wenn du es erlaubst. Wenn du einen Fehler mit **Supportbericht mitschicken** meldest, startet er, sobald du auf **Senden** tippst. Auf deinem eigenen Computer muss deine Machine dafür [mit deinem Konto gekoppelt](friends.md) sein.

- Nur lesend: Logs, Einstellungen, Versionen, wie jede Verbindung synchronisiert, und letzte Fehler, bereinigt wie der Supportbericht. Nie deine Nachrichten, Schlüssel, Passwörter oder wer deine Kontakte sind.
- Er endet von selbst nach 24 Stunden. Solange er aktiv ist, zeigt **Einstellungen**, **Sicherheit** ihn an: **Ausschalten** beendet ihn sofort.
- Jeder Blick steht in Einstellungen, **Aktivität**, mit Zeitpunkt. Siehe [Aktivität](activity.md).

## Von deinem eigenen Computer

Führe `assistant support-bundle` aus. Es speichert eine Datei mit Versionen, den Prüfungen aus `assistant doctor`, letzten Logs und deinen Einstellungen, ohne Schlüssel, Tokens, Passwörter oder Adressen. Sieh sie durch und schick sie dann an die Person, die dir hilft.

Für einen Fehler in der Open-Source-App öffne ein Issue auf [GitHub](https://github.com/Salesflare/TheMachine/issues), nur mit ausgedachten Daten.
