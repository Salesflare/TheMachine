---
title: Verlauf
area: connections
summary: Etwa ein Jahr ältere Mails, Meetings und WhatsApp-, Slack- und Teams-Nachrichten zum Suchen, Lesen und Kennen deiner Leute. Nie eine Aufgabe.
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
translated: 42069e80e6f85bdb
---
## Was er behält

Jedes E-Mail-Konto, jeder Kalender, WhatsApp, Slack und Teams behält etwa ein Jahr ältere Nachrichten und Meetings. Die Suche findet sie, auch nach Bedeutung, ein Verlauf zeigt sie, und der [Kalender](calendar.md) zeigt vergangene Meetings.

Die Karte sagt, wie weit er zurückreicht: **Verlauf: zurück bis** zu einem Monat, sobald er da ist.

## Was er deinem Graph gibt

Dein [Graph](graph.md) zählt ihn mit: wie nah du Leuten bist, wann ihr zuletzt Kontakt hattet, wer wen kennt, und die Personen und Organisationen selbst. Der Verlauf einer Person oder Organisation zeigt ihn auch, so ist ihr letzter Kontakt immer dort zu sehen. Die Antworten deiner Fleet auf „Wer kennt jemanden“ nutzen ihn aus Arbeitskonten, mit denselben [Teilregeln](sharing-rules.md) wie neue Mails.

## Was er nie tut

Er macht nie eine Aufgabe oder ein Versprechen, zählt nie als neu, startet nie eine Prüfung und kommt nie in ein Projekt. Privater Verlauf bleibt privat, wie private Mails. Außer für die Suche nach Bedeutung liest ihn kein KI-Modell.

## Wann er läuft

Er beginnt, wenn der erste Blick auf deine Nachrichten fertig ist, und für jede Verbindung erst, wenn ihre erste Woche da ist, auch bei einer, die du später hinzufügst. Er läuft langsam im Hintergrund und wartet, während eine Prüfung oder ein Abgleich läuft, wenn ein Dienst um weniger Tempo bittet oder wenn deine Machine wenig Speicherplatz hat. Neue Nachrichten gehen immer vor.

Er nutzt den Zugriff, den jede Verbindung schon hat. Nichts Neues wird gefragt.

## Wie weit zurück

Standardmäßig etwa ein Jahr. Selbst gehostete Machines können `history_days` in der Konfiguration setzen (0 schaltet ihn aus, bis 730). Telegram und andere Quellen behalten, was sie heute lesen.

LinkedIn- und X-Nachrichten reichen 90 Tage zurück und werden sehr langsam gelesen: ein paar kleine Abrufe pro Stunde, nur tagsüber, und einen Tag lang keine, wenn die Seite sich wehrt, damit dein Konto sicher bleibt (`social_history_days`, 0 schaltet es aus).
