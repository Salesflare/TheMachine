---
title: Arbeitszeiten
area: settings
summary: Wann deine Machine dir Nachrichten schicken darf, wann Zurückgestelltes zurückkommt und wann die morgendliche Zusammenfassung kommt.
code: dashboard.html, assistant.py
order: 3
keywords: quiet hours, weekend, evening, night, do not disturb, time zone
---
In **Einstellungen**, **Benachrichtigungen**, unter **Arbeitszeiten**:

- **Arbeitstage**: Arbeitsaufgaben und zurückgestellte Arbeit warten auf einen Arbeitstag.
- **Nachrichten ab** und **Bis**: Außerhalb dieser Zeiten wird dir nichts geschickt, weder Push noch Telegram noch E-Mail.
- **Zurückgestelltes kommt um**: wann etwas zurückkommt, das um einen Tag oder länger zurückgestellt wurde. Die morgendliche Zusammenfassung kommt mindestens 5 Minuten später, damit es darin steht.
- **Morgendliche Zusammenfassung**: wann die morgendliche Zusammenfassung kommt. Kommt Zurückgestelltes später, rückt sie mit.
- **Abendliche Zusammenfassung**: wann die Übersicht am Abend kommt. Sie steht auf 15 Minuten vor **Bis** und folgt dieser Zeit, bis du eine eigene Uhrzeit wählst.
- **Zeitzone**: deine, für alles oben Genannte.

Tippe auf **Speichern**. Standardmäßig gilt Montag bis Freitag, 08:00 bis 23:00, Zurückgestelltes um 08:00, die morgendliche Zusammenfassung um 08:30 und die abendliche um 22:45.

Was in diesen Zeiten rausgeht, und wie, steht unter [Benachrichtigungen](notifications.md).

Auf deinem eigenen Computer zeigt und ändert `assistant hours` sie ebenfalls.
