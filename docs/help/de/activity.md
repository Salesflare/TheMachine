---
title: Aktivität
area: settings
summary: Eine Liste von allem, was The Machine für dich getan hat, das Neueste zuerst: Nachrichten, Dokumente, Fleet-Antworten, Erkenntnisse, Verbindungen und mehr.
covers: settings:activity
code: activity_log.py, dashboard/settings-activity.js
order: 2
keywords: log, history, audit, what did it do, sent, refused, blocked
---
## Was sie zeigt

Öffne **Einstellungen**, **Aktivität**. Jede Zeile ist eine Sache, die The Machine getan hat, das Neueste zuerst, nach Tag:

- was sie getan hat und wie es ausging: gesendet, abgelehnt, fehlgeschlagen oder rückgängig gemacht
- wann, welches Konto oder welche App sie genutzt hat und [was es erlaubte](activity.md#what-allowed-it)
- ein Link zu ihrer Aufgabe, wenn es eine gibt
- bei einer KI, die du verbunden hast, etwa ChatGPT oder Claude: ihr Name mit **(verbundene KI)**, damit du sie von The Machine selbst unterscheidest

Sie zeigt Nachrichten und Antworten, Änderungen an Dokumenten und im Kalender, Schritte im Web, Korrekturen, die sie zusammengeführt hat, Coding-Agents, Fleet-Fragen und -Antworten, Erkenntnisse an das Team von The Machine, Skills, Graph-Importe, Fakten, die du im Chat vergessen ließest (mit **Rückgängig**), hinzugefügte oder entfernte Verbindungen und jeden Blick unseres Teams über den [Support-Zugriff](get-support.md#support-access), abgelehnte eingeschlossen.

## Was es erlaubte

Jede Nachricht, jede Änderung an Dokumenten oder Kalender, jeder Schritt im Web und jeder gemergte Fix sagt, was ihn erlaubte, so wie es geschah:

- **In der Aufgabe freigegeben** oder **In Telegram freigegeben**: dein Tippen auf Senden, Bestätigen oder Mergen
- **Per Sprache freigegeben**: dein Ja in Talk
- **„Ausführen“ getippt**: dein Ausführen in der Aufgabe
- **Im Chat gebeten**: du hast in Worten darum gebeten, mit dem Anfang deiner Nachricht in Anführungszeichen. Ein Zitat erscheint nur, solange diese Worte noch in deiner eigenen Nachricht stehen.
- **Nachfassen, von selbst gesendet**, **Kleiner Fix, von selbst gemergt**, **Neues privates Dokument, von selbst erstellt** oder **Vorbereitet, von selbst**: eine deiner Einstellungen oder eine eigene Regel von The Machine
- **Keine Freigabe erfasst**: dafür wurde nichts erfasst. Es geht auch in unsere [Fehlerberichte](error-reports.md), damit wir den Weg finden, der es verpasst hat.

Schritte im Web listet auch einen Lauf einer Aufgabe, der auf einer Seite geklickt oder getippt hat, mit dem, was diesen Lauf erlaubte.

Ältere Zeilen, von bevor dies erfasst wurde, behalten ihre alten Worte, wie **Nach deinem OK**.

## Filtern

Wähle oben eine Art, etwa **Nachrichten** oder **Fleet**. **Abgelehnt oder blockiert** zeigt nur, was nicht ging, und warum. **Mehr anzeigen** lädt ältere Zeilen.

## Andere Stellen

Der Chat einer Aufgabe erzählt weiter seine eigene Geschichte; Aktivität verlinkt dorthin. Fleet, **Aktivität** zeigt dieselben Zeilen für deine Fleets und Erkenntnisse, mit **Zurückziehen** für eine Erkenntnis. In Einstellungen, **Sicherheit** öffnet **Jeden Blick in Aktivität ansehen** die Blicke unseres Teams.

Aktivität zeigt nur, was passiert ist. Sie ändert nie, was The Machine darf.
