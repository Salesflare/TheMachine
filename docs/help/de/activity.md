---
title: Aktivität
area: settings
summary: Eine chronologische Liste aller Aktionen, die The Machine für dich ausgeführt hat: Nachrichten, Dokumente, Fleet-Antworten, Erkenntnisse, Verbindungen und mehr.
covers: settings:activity
code: activity_log.py, dashboard/settings-activity.js
order: 2
keywords: log, history, audit, what did it do, sent, refused, blocked
translated: 1ebeba09417a11e9
---
## Was angezeigt wird

Öffne **Einstellungen** und dann **Aktivität**. Jeder Eintrag zeigt eine Aktion von The Machine, nach Tag sortiert und die neueste zuerst:

- was sie getan hat und wie es endete: gesendet, abgelehnt, fehlgeschlagen oder rückgängig gemacht; bei einer Nachricht, die [später gesendet wird](send-later.md), auch, wann sie geplant, geändert oder abgebrochen wurde
- wann es passiert ist, welches Konto oder welche App sie verwendet hat und [was die Aktion erlaubt hat](activity.md#what-allowed-it)
- einen Link zur zugehörigen Aufgabe, falls vorhanden
- bei einer von dir verbundenen KI wie ChatGPT oder Claude: ihren Namen mit **(verbundene KI)**, damit du sie von The Machine selbst unterscheiden kannst

Die Liste enthält Nachrichten und Antworten, Änderungen an Dokumenten und Kalendern, Schritte im Web, zusammengeführte Fixes, Coding-Agenten, Fragen und Antworten in Fleets, an das The Machine-Team gesendete Erkenntnisse, Skills, Graph-Importe, Fakten, die du deinen Chat bitten kannst zu vergessen (mit **Rückgängig**), hinzugefügte oder entfernte Verbindungen sowie jeden Zugriff unseres Teams unter [Supportzugriff](get-support.md#support-access), einschließlich abgelehnter Zugriffe.

## Was die Aktion erlaubt hat

Bei jeder Nachricht, Änderung an einem Dokument oder Kalender, jedem Schritt im Web und jedem zusammengeführten Fix steht, was die Aktion im jeweiligen Moment erlaubt hat:

- **In der Aufgabe freigegeben** oder **In Telegram freigegeben**: Du hast auf **Senden**, **Bestätigen** oder **Zusammenführen** getippt.
- **Per Sprache freigegeben**: Du hast in Talk zugestimmt.
- **„Ausführen“ getippt**: Du hast bei der Aufgabe auf **„Ausführen“** getippt.
- **Im Chat gebeten**: Du hast in Worten darum gebeten. Der Anfang deiner Nachricht steht in Anführungszeichen. Das Zitat wird nur angezeigt, solange diese Worte noch in deiner Nachricht stehen.
- **Nachfassen, von selbst gesendet**, **Kleiner Fix, von selbst gemergt**, **Neues privates Dokument, von selbst erstellt** oder **Vorbereitet, von selbst**: Eine deiner Einstellungen oder eine eigene Regel von The Machine hat die Aktion erlaubt.
- **Keine Freigabe erfasst**: Für die Aktion wurde keine Freigabe erfasst. Sie erscheint auch in unseren [Fehlerberichten](error-reports.md), damit wir herausfinden können, warum sie nicht erfasst wurde.

Unter „Schritte im Web“ siehst du außerdem Aufgabenläufe, bei denen auf einer Seite geklickt oder Text eingegeben wurde, samt der jeweiligen Freigabe. Arbeit, die nach dem Zurückstellen fortgesetzt wird, behält die vorherige Freigabe.

Ältere Einträge, die erfasst wurden, bevor diese Aufzeichnung eingeführt wurde, behalten ihre frühere Bezeichnung, etwa **Nach deinem OK**.

## Filtern

Wähle oben in der Liste eine Art aus, zum Beispiel **Nachrichten** oder **Fleet**. **Abgelehnt oder blockiert** zeigt nur Aktionen, die nicht ausgeführt wurden, und den Grund dafür. Über **Mehr anzeigen** lädst du ältere Einträge.

## Weitere Orte

Im Chat einer Aufgabe wird der Verlauf weiterhin angezeigt. In der Aktivität findest du einen Link dazu. Unter **Aktivität** in Fleet siehst du dieselben Einträge für deine Fleets und Erkenntnisse. Bei einer Erkenntnis kannst du **Zurückziehen** auswählen. Unter **Sicherheit** in den Einstellungen öffnet **Jeden Zugriff unter „Aktivität“ ansehen** die Zugriffe unseres Teams.

Die Aktivität zeigt nur, was passiert ist. Sie ändert nie, was The Machine tun darf.
