---
title: Support kontaktieren
area: troubleshooting
summary: Melde einen Fehler über dein Dashboard, schreib uns oder lass unser Team einen Tag lang einen Blick auf deine Machine werfen.
covers: support-bundle, support-access
code: support.py, cli.py, dashboard.html, fleet.py
site: Report a problem
order: 9
translated: 419a75e887b25e20
---
## Schreib uns

Schreib an support@themachine.computer. Eine echte Person antwortet.

Bei einer gehosteten Machine findest du im Footer des Dashboards **„Stimmt etwas nicht?“**. Damit öffnest du das Formular **Ein Problem melden** für dein Konto.

## Fehler melden

Öffne **Hilfe** und dann **Fehler melden**. Auch in einer Fehlermeldung gibt es die Schaltfläche **Fehler melden**.

1. Beschreib, was schiefgelaufen ist.
2. Füge bei Bedarf einen Screenshot hinzu: **Screenshot machen** nimmt einen Screenshot vom Dashboard auf. Oder wähle **Bild anhängen**.
3. Lass **Supportbericht mitschicken** aktiviert, wenn möglich. Der Bericht enthält Versionen, Prüfungen und aktuelle Fehler, aber keine Nachrichten, Schlüssel oder Adressen. Außerdem kann unser Team 24 Stunden lang die Logs und Einstellungen deiner Machine einsehen. Mehr dazu unter [Supportzugriff](get-support.md#support-access). Wenn du das Häkchen entfernst, werden nur dein Text und dein Screenshot gesendet.
4. Tippe auf **Senden**. Das Formular schließt sich sofort und der Supportbericht wird automatisch nachgesendet.

Wir kümmern uns darum. Eine selbst gehostete Machine kann einen Bericht senden, wenn sie mit dem Network verbunden ist. Andernfalls schreib uns.

Du kannst deiner Machine auch einfach im Chat sagen, dass etwas nicht stimmt. Sie öffnet dann **Fehler melden** und trägt deine Worte sowie eine kurze Zusammenfassung ein. Es wird nichts gesendet, bis du auf **Senden** tippst.

Sobald wir einen von dir gemeldeten Fehler behoben haben und deine Machine die Fehlerbehebung ausführt, benachrichtigen wir dich einmal: mit einem kurzen Hinweis auf deinem Dashboard und einer kurzen E-Mail. Eine selbst gehostete Machine erfährt davon, sobald sie mit dem Network verbunden ist.

Der Hinweis fragt, ob jetzt wirklich alles funktioniert. Tippe auf **Funktioniert jetzt** oder auf **Noch nicht richtig**, um zu beschreiben, was noch nicht stimmt. Bei Bedarf kannst du ein Bild hinzufügen. Deine Rückmeldung wird als neuer Bericht an uns gesendet und mit dem ersten verknüpft. **×** schließt den Hinweis ohne Antwort.

Ist deine Machine offline oder hast du mehrere Berichte hintereinander gesendet? Dein Bericht geht nicht verloren. Deine Machine speichert ihn und sendet ihn später automatisch. Bis dahin wird er unter **Wartet auf den Versand** angezeigt.

## Supportzugriff

Unser Team kann sich deine Machine ansehen, aber nur, wenn du das erlaubst. Wenn du einen Fehler meldest und **Supportbericht mitschicken** aktiviert ist, wird der Zugriff eingeschaltet, sobald du auf **Senden** tippst. Auf deinem eigenen Computer muss deine Machine dafür [mit deinem Konto gekoppelt](friends.md) sein.

- Nur-Lesezugriff: Logs, Einstellungen, Versionen, die Synchronisierung der einzelnen Verbindungen und aktuelle Fehler. Die Daten werden wie im Supportbericht bereinigt. Nachrichten, Schlüssel, Passwörter und die Identität deiner Kontakte bleiben immer privat.
- Der Zugriff endet nach 24 Stunden automatisch. Solange er aktiv ist, findest du ihn unter **Einstellungen** > **Sicherheit**. Mit **Ausschalten** beendest du ihn sofort.
- Jeder Zugriff wird mit Zeitangabe unter **Einstellungen** > **Aktivität** aufgeführt. Mehr dazu unter [Aktivität](activity.md).

## Auf deinem eigenen Computer

Führe `assistant support-bundle` aus. Damit wird eine Datei mit Versionen, den Prüfungen aus `assistant doctor`, aktuellen Logs und deinen Einstellungen gespeichert, aber ohne Schlüssel, Tokens, Passwörter oder Adressen. Sieh sie durch und sende sie dann an die Person, die dir hilft.

Wenn du einen Fehler in der Open-Source-App melden möchtest, erstelle ein Issue auf [GitHub](https://github.com/Salesflare/TheMachine/issues) und verwende dafür ausschließlich erfundene Daten.
