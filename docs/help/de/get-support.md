---
title: Support bekommen
area: troubleshooting
summary: Melde einen Fehler aus deinem Dashboard, schreib uns oder lass unser Team einen Tag lang auf deine Machine schauen.
covers: support-bundle, support-access
code: support.py, cli.py, dashboard.html, fleet.py
site: Report a problem
order: 9
---
## Schreib uns

Schick eine E-Mail an support@themachine.computer. Ein Mensch antwortet.

Auf einer gehosteten Machine steht in der Fußzeile des Dashboards „Stimmt etwas nicht?“. Das öffnet das Formular **Problem melden** deines Kontos.

## Einen Fehler melden

Öffne **Hilfe**, dann **Fehler melden**. Auch eine Fehlermeldung hat einen Button **Fehler melden**.

1. Sag, was schiefging.
2. Füge einen Screenshot hinzu, wenn es hilft: **Screenshot machen** vom Dashboard oder **Bild anhängen**.
3. Lass **Supportbericht mitschicken** an, außer du möchtest das nicht. Das schickt Versionen, Prüfungen und letzte Fehler mit, ohne Nachrichten, Schlüssel oder Adressen, und unser Team darf 24 Stunden lang die Logs und Einstellungen deiner Machine lesen. Siehe [Support-Zugriff](get-support.md#support-access). Ohne Haken gehen nur dein Text und dein Screenshot.
4. Tippe auf **Senden**. Das Formular schließt sich sofort. Deine Machine fügt den Supportbericht selbst hinzu; eine langsame Prüfung hält deinen Bericht nie auf.

Ab da kümmern wir uns. Eine selbst gehostete Machine kann einen Bericht senden, wenn sie im Network ist. Sonst schreib uns.

Wenn wir einen Bug beheben, den du gemeldet hast, und deine Machine die Korrektur hat, sagen wir es dir einmal: eine kurze Zeile in deinem Dashboard (**Verstanden** schließt sie) und eine kurze E-Mail. Eine selbst gehostete Machine erfährt es, wenn sie im Network ist.

Wenn ein Bericht nicht sofort rausgehen kann (du bist offline oder hast in kurzer Zeit viele gesendet), geht er nicht verloren. Deine Machine behält ihn, sagt, wann er rausgeht, und sendet ihn von selbst. Berichte, die noch warten, stehen unter **Wartet auf den Versand**.

## Support-Zugriff

Unser Team kann für dich auf deine Machine schauen, aber erst, wenn du es erlaubst. Wenn du einen Fehler mit **Supportbericht mitschicken** meldest, startet er, sobald du auf **Senden** tippst. Auf deinem eigenen Computer muss deine Machine dafür [mit deinem Konto gekoppelt](friends.md) sein.

- Nur lesend: Logs, Einstellungen, Versionen, wie jede Verbindung synchronisiert, und letzte Fehler, bereinigt wie der Supportbericht. Nie deine Nachrichten, Schlüssel, Passwörter oder wer deine Kontakte sind.
- Es endet von selbst nach 24 Stunden. Solange es an ist, zeigt **Einstellungen**, **Sicherheit** es an: **Ausschalten** beendet es sofort.
- Jeder Blick wird dort aufgelistet, mit Zeitpunkt.

## Von deinem eigenen Computer

Führe `assistant support-bundle` aus. Es speichert eine Datei mit Versionen, den Prüfungen aus `assistant doctor`, letzten Logs und deinen Einstellungen, ohne Schlüssel, Tokens, Passwörter oder Adressen. Sieh sie durch und schick sie dann an die Person, die dir hilft.

Für einen Fehler in der Open-Source-App öffne ein Issue auf [GitHub](https://github.com/Salesflare/TheMachine/issues), nur mit ausgedachten Daten.
