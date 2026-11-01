---
title: Google Calendar
area: connections
summary: Deine Meetings, damit du vorbereitet reingehst und nachfasst. Es ändert nichts, außer du tippst.
covers: connector:calendar
code: onboarding.py, google_api.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google
order: 11
---
## Was es liest

Deine Termine von 7 Tagen zurück bis 30 Tage voraus, mit allen Serienterminen. Sie erscheinen im Tab [Kalender](calendar.md) und helfen bei Aufgaben zu einem Meeting.

## Was es tun kann

Nichts von selbst. Es beantwortet nie eine Einladung und lädt nur Personen ein, die du selbst einträgst.

Wenn die Anmeldung in Kalender schreiben darf, kannst du einen Termin ohne Gäste hinzufügen, ändern oder löschen, in deinem eigenen Kalender oder einem geteilten, den du bearbeiten darfst. Jede Änderung ist dein Tippen: im [Kalender](calendar.md) oder bei einer Aufgabe, die sie anbietet. Eine Anmeldung über **Google verbinden** liest nur.

In deinem eigenen Kalender kannst du über das Formular im [Kalender](calendar.md) auch Personen einladen. Der Button sagt, wie viele eine Einladung bekommen, und Google verschickt die Einladungen bei diesem Tippen. Eine Aufgabe lädt nie jemanden ein.

## Verbinden

Auf einer gehosteten Machine wird es zusammen mit Gmail verbunden: Tippe auf deiner Einrichtungsseite unter **Mail und Kalender** auf **Google verbinden**.

Auf deinem eigenen Computer, sobald er [mit deinem Konto gekoppelt](friends.md#a-machine-on-your-own-computer) ist: Öffne **Verbindungen**, dann **+ Hinzufügen**, wähle Google Calendar und tippe auf **Mit Google anmelden**. Es wird zusammen mit Gmail verbunden.

Mit deiner eigenen App: Führe `assistant connect calendar` aus oder öffne dort **Eigene App nutzen**. Es fragt, welcher Kalender gelesen werden soll.

## Entfernen

- Auf einer gehosteten Machine: Tippe auf deiner Einrichtungsseite neben der Adresse auf **Trennen**. Das entfernt Gmail und Kalender für diese Adresse.
- Auf deinem eigenen Computer: **Verbindungen**, den Kalender öffnen, **Details**, dann **Trennen**.

## Bei Google deinstallieren

Öffne in deinem Google-Konto Sicherheit, dann Deine Verbindungen zu Drittanbieter-Apps und -Diensten, und entferne die App. Siehe [Gmail](gmail.md).
