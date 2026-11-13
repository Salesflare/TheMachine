---
title: iCloud und andere Kalender (CalDAV)
area: connections
summary: Meetings aus dem iCloud-Kalender oder jedem CalDAV-Kalender, etwa Fastmail, Nextcloud oder Zoho. Nur lesend.
covers: connector:icloud_calendar, connector:caldav
code: caldav_calendar.py, ical.py, machine/sources/calendar_setup.py
order: 14
---
## Was es liest

Deine Meetings, mit Gästen, Räumen und Notizen: beim Verbinden die letzte Woche und der nächste Monat, danach jede Änderung. Sie erscheinen im Kalender und in der Meeting-Vorbereitung, wie Meetings aus Google oder Outlook. Jeder Kalender des Kontos wird gelesen, oder nur der, den du nennst.

Es liest nur: Es fügt nie ein Meeting hinzu, verschiebt keins und entfernt keins.

## iCloud-Kalender verbinden

1. Erstelle ein App-spezifisches Passwort auf [appleid.apple.com](https://appleid.apple.com), unter **Anmeldung und Sicherheit**. Das für iCloud Mail geht auch.
2. Öffne im Dashboard **Verbindungen**, dann **Kalender**, und wähle **iCloud-Kalender**.
3. Gib deine Apple ID und das App-spezifische Passwort ein und drücke **Verbinden**.

## Einen anderen Kalender verbinden

1. Öffne **Verbindungen**, dann **Kalender**, und wähle **Anderer Kalender**.
2. Gib deine E-Mail-Adresse und dein Passwort ein. Viele Anbieter wollen hier ein App-Passwort, das du in deinen Kontoeinstellungen erstellst.
3. Drücke **Verbinden**.

Der Server wird für Fastmail, Yahoo, Zoho und Server gefunden, die sich selbst bekannt machen. Deiner nicht gefunden? Öffne **Servereinstellungen** und gib seine CalDAV-Adresse ein, etwa `nextcloud.example.com/remote.php/dav`. **Nur dieser Kalender** liest einen Kalender über seinen Namen.

Kalender von Google oder Microsoft? Wähle dann **Google Calendar** oder **Outlook-Kalender**.

## Wenn es stoppt

- **Der Kalenderserver hat das Passwort abgelehnt**: Du hast es geändert, oder das App-Passwort wurde entfernt. Verbinde neu mit einem neuen.
- **Der Kalenderserver war nicht erreichbar**: Es versucht es selbst noch einmal. Klappt es weiter nicht, prüfe die Adresse in den Servereinstellungen.

## Entfernen

**Verbindungen**, den Kalender öffnen, **Details**, dann **Trennen**. Was schon da ist, bleibt. Entferne das App-Passwort auch bei deinem Anbieter.
