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
3. Lass **Supportbericht mitschicken** an, außer du möchtest das nicht: Versionen, Prüfungen und letzte Fehler, ohne Nachrichten, Schlüssel oder Adressen.
4. Tippe auf **Prüfen**. Es zeigt alles, was rausgeht, genau so, wie es rausgeht.
5. Tippe auf **Senden**. Vorher wird nichts gesendet.

Wir antworten per E-Mail. Eine selbst gehostete Machine kann einen Bericht senden, wenn sie im Network ist. Sonst schreib uns.

Wenn ein Bericht nicht sofort rausgehen kann (du bist offline oder hast in kurzer Zeit viele gesendet), geht er nicht verloren. Deine Machine behält ihn, sagt, wann er rausgeht, und sendet ihn von selbst. Berichte, die noch warten, stehen unter **Wartet auf den Versand**.

## Support-Zugriff

Unser Team kann für dich auf deine Machine schauen, aber erst, wenn du es erlaubst. Tippe in **Einstellungen**, **Sicherheit**, **Support-Zugriff** auf **Für 24 Stunden erlauben**. Auf deinem eigenen Computer muss deine Machine dafür [mit deinem Konto gekoppelt](friends.md) sein.

- Nur lesend: Logs, Einstellungen, Versionen, wie jede Verbindung synchronisiert, und letzte Fehler, bereinigt wie der Supportbericht. Nie deine Nachrichten, Schlüssel, Passwörter oder wer deine Kontakte sind.
- Es endet von selbst nach 24 Stunden. **Ausschalten** beendet es sofort.
- Jeder Blick wird darunter aufgelistet, mit Zeitpunkt.

## Von deinem eigenen Computer

Führe `assistant support-bundle` aus. Es speichert eine Datei mit Versionen, den Prüfungen aus `assistant doctor`, letzten Logs und deinen Einstellungen, ohne Schlüssel, Tokens, Passwörter oder Adressen. Sieh sie durch und schick sie dann an die Person, die dir hilft.

Für einen Fehler in der Open-Source-App öffne ein Issue auf [GitHub](https://github.com/Salesflare/TheMachine/issues), nur mit ausgedachten Daten.
