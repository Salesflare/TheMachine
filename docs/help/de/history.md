---
title: Verlauf
area: connections
summary: Etwa ein Jahr ältere Mails, Meetings und WhatsApp-Chats zum Suchen und Lesen. Nie eine Aufgabe.
covers: history
code: machine/app/history.py, machine/store/history.py
keywords: older messages, backfill, archive, past emails
---
## Was er behält

Jedes E-Mail-Konto, jeder Kalender und WhatsApp behält etwa ein Jahr ältere Nachrichten und Meetings. Die Suche findet sie, ein Verlauf zeigt sie, und der [Kalender](calendar.md) zeigt vergangene Meetings.

Die Karte sagt, wie weit er zurückreicht: **Verlauf: zurück bis** zu einem Monat, sobald er da ist.

## Was er nie tut

Der Verlauf ist nur zum Nachschlagen da. Er macht nie eine Aufgabe oder ein Versprechen, kommt nie in eine Prüfung, zählt nie als neu und geht nie in deinen Graph oder an dein Team. Kein KI-Modell liest ihn.

Aufgaben und Versprechen kommen weiter nur aus neuen Nachrichten, wie bisher.

## Wann er läuft

Er beginnt, wenn der erste Blick auf deine Nachrichten fertig ist, und läuft langsam im Hintergrund. Er wartet, während eine Prüfung oder ein Abgleich läuft und wenn deine Machine wenig Speicherplatz oder Arbeitsspeicher hat. Nach einem Neustart macht er dort weiter, wo er war.

Er nutzt den Zugriff, den jede Verbindung schon hat. Nichts Neues wird gefragt.

## Wie weit zurück

Standardmäßig etwa ein Jahr. Selbst gehostete Machines können `history_days` in der Konfiguration setzen (0 schaltet ihn aus, bis 730). Telegram, Slack und andere Quellen behalten, was sie heute lesen.
