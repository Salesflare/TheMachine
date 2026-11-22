---
title: Aktivität
area: settings
summary: Eine Liste mit allem, was The Machine für dich getan hat, neueste Einträge zuerst: Nachrichten, Dokumente, Fleet-Antworten, Erkenntnisse, Verbindungen und mehr.
covers: settings:activity
code: activity_log.py, dashboard/settings-activity.js
order: 2
keywords: log, history, audit, what did it do, sent, refused, blocked
translated: ebb6a4cf0474a020
---
## Was angezeigt wird

Öffne **Einstellungen** und dann **Aktivität**. Jeder Eintrag steht für etwas, das The Machine getan hat. Die Einträge sind nach Tagen gruppiert und die neuesten stehen zuerst:

- was The Machine getan hat und wie es ausgegangen ist: gesendet, abgelehnt, fehlgeschlagen oder rückgängig gemacht
- wann es passiert ist, welches Konto oder welche App The Machine verwendet hat und [was die Aktion erlaubt hat](activity.md#what-allowed-it)
- einen Link zur zugehörigen Aufgabe, falls es eine gibt
- bei einer KI, die du verbunden hast, wie ChatGPT oder Claude: ihren Namen mit **(verbundene KI)**, damit du sie von The Machine selbst unterscheiden kannst

Aufgeführt werden Nachrichten und Antworten, Änderungen an Dokumenten und Kalendern, Schritte im Web, zusammengeführte Fixes, Coding-Agenten, Fleet-Fragen und -Antworten, Erkenntnisse, die an das Team von The Machine gesendet wurden, Skills, Graph-Importe, Fakten, die dein Chat auf deinen Wunsch vergessen hat (mit **Rückgängig**), hinzugefügte oder entfernte Verbindungen und jeder Zugriff unseres Teams unter [Supportzugriff](get-support.md#support-access), auch abgelehnte Zugriffe.

## Was die Aktion erlaubt hat

Bei jeder Nachricht, Änderung an einem Dokument oder Kalender, jedem Schritt im Web und jedem zusammengeführten Fix steht, was die Aktion im jeweiligen Moment ermöglicht hat:

- **In der Aufgabe freigegeben** oder **In Telegram freigegeben**: Du hast auf Senden, Bestätigen oder Zusammenführen getippt.
- **Per Sprache freigegeben**: Du hast in Talk Ja gesagt.
- **„Ausführen“ getippt**: Du hast bei der Aufgabe auf **Ausführen** getippt.
- **Im Chat gebeten**: Du hast in einer Nachricht darum gebeten. Der Anfang deiner Nachricht steht in Anführungszeichen. Ein Zitat wird nur angezeigt, solange diese Worte noch in deiner eigenen Nachricht stehen.
- **Nachfassen, von selbst gesendet**, **Kleiner Fix, von selbst gemergt**, **Neues privates Dokument, von selbst erstellt** oder **Vorbereitet, von selbst**: eine deiner Einstellungen oder eine eigene Regel von The Machine.
- **Keine Freigabe erfasst**: Für die Aktion wurde nichts erfasst. Sie wird auch unseren [Fehlerberichten](error-reports.md) hinzugefügt, damit wir den Ablauf finden können, bei dem etwas übersehen wurde.

Unter den Schritten im Web wird auch der Durchlauf einer Aufgabe aufgeführt, bei dem auf einer Seite geklickt oder Text eingegeben wurde. Dabei steht auch, was diesen Durchlauf erlaubt hat. Arbeiten, die nach dem Zurückstellen fortgesetzt werden, behalten die vorherige Freigabe.

Ältere Einträge aus der Zeit, bevor diese Informationen erfasst wurden, behalten ihre frühere Bezeichnung, zum Beispiel **Nach deinem OK**.

## Filtern

Wähle oben in der Liste eine Kategorie aus, zum Beispiel **Nachrichten** oder **Fleet**. **Abgelehnt oder blockiert** zeigt nur Aktionen, die nicht ausgeführt wurden, und den Grund dafür. Über **Mehr anzeigen** lädst du ältere Einträge.

## Weitere Orte

Der Chat einer Aufgabe zeigt weiterhin den zugehörigen Verlauf. **Aktivität** verlinkt dorthin. In Fleet zeigt **Aktivität** dieselben Einträge für deine Fleets und Erkenntnisse. Bei einer Erkenntnis kannst du **Zurückziehen** wählen. Unter **Einstellungen** und **Sicherheit** öffnet **Jeden Zugriff unter „Aktivität“ ansehen** die Einträge zu Zugriffen unseres Teams.

Aktivität zeigt nur, was passiert ist. Sie ändert nie, was The Machine tun darf.
