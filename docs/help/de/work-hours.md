---
title: Arbeitszeiten
area: settings
summary: Wann dich deine Machine erreichen darf, wann Zurückgestelltes wiederkommt und wann die morgendliche und abendliche Zusammenfassung erscheint.
code: dashboard.html, assistant.py
order: 3
keywords: quiet hours, weekend, evening, night, do not disturb, time zone
translated: 062ccef1310f228a
---
Wähle aus, wann dich deine Machine erreichen darf. Unter **Einstellungen**, **Benachrichtigungen** und **Arbeitszeiten**:

- **Arbeitstage**: Arbeitsaufgaben und zurückgestellte Arbeit warten bis zu einem Arbeitstag.
- **Nachrichten ab** und **Bis**: Außerhalb dieser Zeiten erreicht dich nichts: keine Benachrichtigung, keine Telegram-Nachricht und keine E-Mail.
- **Zurückgestelltes kommt um**: wann Zurückgestelltes nach einem Tag oder länger wiederkommt. Die morgendliche Zusammenfassung erscheint mindestens 5 Minuten später, damit es darin enthalten ist.
- **Morgendliche Zusammenfassung**: wann die morgendliche Zusammenfassung erscheint. Wenn du die Zeit für Zurückgestelltes nach hinten verschiebst, verschiebt sie sich ebenfalls.
- **Abendliche Zusammenfassung**: wann die abendliche Zusammenfassung erscheint. Sie ist zunächst auf 15 Minuten vor **Bis** eingestellt und verschiebt sich mit dieser Einstellung, bis du selbst eine Uhrzeit auswählst.
- **Zeitzone**: deine Zeitzone für alle oben genannten Einstellungen.

Drück auf **Speichern**. Standardmäßig sind Montag bis Freitag von 08:00 bis 23:00 Uhr eingestellt, Zurückgestelltes kommt um 08:00 Uhr, die morgendliche Zusammenfassung um 08:30 Uhr und die abendliche Zusammenfassung um 22:45 Uhr.

Was innerhalb dieser Zeiten und auf welche Weise gesendet wird, erfährst du unter [Benachrichtigungen](notifications.md).

Auf deinem eigenen Computer zeigt `assistant hours` die Einstellungen in einem Terminal an und ändert sie.
