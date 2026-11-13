---
title: Exchange Server
area: connections
summary: Meetings aus einem Exchange Server, den deine Firma betreibt (2013 bis 2019 oder Subscription Edition). Nur lesend.
covers: connector:exchange
code: ews_calendar.py, machine/sources/calendar_setup.py
order: 16
---
## Was es liest

Deine Meetings, mit Gästen, Räumen und Notizen: beim Verbinden die letzte Woche und der nächste Monat, danach jede Änderung. Sie erscheinen im Kalender und in der Meeting-Vorbereitung.

Es liest nur: Es fügt nie ein Meeting hinzu, verschiebt keins und entfernt keins. Mail aus Exchange Server wird noch nicht gelesen.

## Microsoft 365 oder Exchange Server?

Exchange Server läuft bei deiner Firma. Microsoft 365 (Exchange Online) ist die Cloud von Microsoft: Wähle dafür **Outlook-Kalender**. Liegt deine Adresse auf Microsoft 365, sagt das Formular es dir.

## Verbinden

1. Öffne im Dashboard **Verbindungen**, dann **Kalender**, und wähle **Exchange Server**.
2. Gib deine Arbeitsadresse und dein Windows-Passwort ein.
3. Drücke **Verbinden**.

Der Server wird über deine Adresse gefunden (Autodiscover). Nicht gefunden? Öffne **Servereinstellungen** und gib den Server ein, den dein IT-Team für Outlook nennt, etwa `mail.example.com`. Meldest du dich mit einem anderen Namen als deiner Adresse an? Gib ihn als `DOMAIN\name` unter **Benutzername** ein.

Es meldet sich mit NTLM oder Basic an, nur über https.

## Wenn es stoppt

- **Der Kalenderserver hat das Passwort abgelehnt**: Dein Windows-Passwort hat sich geändert. Verbinde neu.
- **Ein Microsoft-365-Postfach**: Dein Postfach ist zu Microsoft 365 umgezogen. Trenne dieses und verbinde **Outlook-Kalender**.
- **Der Kalenderserver war nicht erreichbar**: Es versucht es selbst noch einmal. Manche Server sind nur im Firmennetz oder per VPN erreichbar.

## Entfernen

**Verbindungen**, den Kalender öffnen, **Details**, dann **Trennen**. Was schon da ist, bleibt.
