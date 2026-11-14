---
title: Proton Calendar und Kalenderlinks (ICS)
area: connections
summary: Meetings aus dem Freigabelink eines Kalenders: Proton Calendar, veröffentlichte Kalender, Schul- oder Sportkalender. Nur lesend.
covers: connector:proton_calendar, connector:ics
code: ics_feed.py, ical.py, machine/sources/calendar_setup.py
order: 15
translated: b3bcf33b5c027baf
---
## Was es liest

Die Termine im Kalender hinter dem Link, mit Serienterminen und Zeitzonen: die letzte Woche und der nächste Monat, danach jede Änderung. Sie erscheinen im Kalender und in der Meeting-Vorbereitung.

Ein Link kann nur gelesen werden, also ändert sich nie ein Meeting. Der Link wird höchstens alle 15 Minuten abgerufen. Laut Proton kann es ein paar Stunden dauern, bis Änderungen im Link ankommen.

## Proton Calendar verbinden

Proton Calendar hat keinen anderen Zugang für Apps, darum nutzt es einen Freigabelink.

1. Öffne Proton Calendar im Web, auf calendar.proton.me. In den Handy-Apps lassen sich keine Freigabelinks erstellen.
2. Geh zu "Einstellungen", "Alle Einstellungen", "Kalender", und wähle den Kalender.
3. Drücke unter "Share with anyone" auf "Create link" und wähle "Full view". Limited view zeigt nur, wann du beschäftigt bist.
4. Drücke "Copy link".
5. Öffne im Dashboard **Verbindungen**, dann **Kalender**, wähle **Proton Calendar**, füge den Link ein und drücke **Verbinden**.

## Einen anderen Kalenderlink verbinden

Wähle **Kalenderlink (ICS)** und füge den Link ein: eine https- oder webcal-Adresse, die auf .ics endet, etwa ein öffentlicher iCloud-Kalender, ein veröffentlichter Outlook-Kalender oder der Schulkalender deines Kindes.

## Halte den Link privat

Wer den Link hat, kann den Kalender lesen. The Machine bewahrt ihn wie ein Passwort auf: nie in einem Log oder auf dem Bildschirm. Zum Beenden lösch den Link dort, wo du ihn erstellt hast, und drücke hier **Trennen**.

## Wenn es stoppt

- **Der Kalenderlink funktioniert nicht mehr**: Der Link wurde gelöscht oder geändert. Erstelle einen neuen und verbinde neu.
- **Der Kalenderserver war nicht erreichbar**: Es versucht es selbst noch einmal.
