---
title: Verlauf
area: connections
summary: Etwa ein Jahr ältere E-Mails, Meetings sowie Nachrichten aus WhatsApp, Slack und Teams, die du durchsuchen und lesen kannst und die dir helfen, deine Kontakte besser zu kennen. Daraus wird nie eine Aufgabe.
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
translated: c10fe5fb8d7b2d8b
---
## Was gespeichert wird

Deine Machine importiert etwa ein Jahr ältere E-Mails, Meetings sowie Nachrichten aus WhatsApp, Slack und Teams. Über die Suche findest du sie, auch nach ihrer Bedeutung. In Threads sind sie ebenfalls zu sehen, und im [Kalender](calendar.md) findest du vergangene Meetings.

Unter **Verbindungen** siehst du für jede Verbindung, wie weit sie zurückreicht, zum Beispiel **Verlauf: zurück bis** November 2025.

## Was zum Graph hinzugefügt wird

Dein [Graph](graph.md) berücksichtigt diese Daten: wie nah du anderen Menschen stehst, wann ihr zuletzt gesprochen habt, wer wen kennt und wer die Menschen und Organisationen sind. Auch die Zeitleiste einer Person oder Organisation zeigt sie an. So ist der letzte Kontakt immer zu sehen. Die Antworten von Fleet auf die Frage „Wer kennt wen?“ nutzen diese Daten aus Arbeitskonten. Dabei gelten dieselben [Freigaberegeln](sharing-rules.md) wie für neue E-Mails.

## Was nie passiert

Daraus wird nie eine Aufgabe oder ein Versprechen. Die Daten zählen nie als neu, lösen nie eine Prüfung aus und werden nie einem Projekt hinzugefügt. Persönlicher Verlauf bleibt persönlich, genau wie persönliche E-Mails. Abgesehen von der Suche nach Bedeutung liest kein KI-Modell diese Daten.

## Wann der Import läuft

Der Import beginnt nach dem ersten Durchsehen deiner Nachrichten. Für jede Verbindung startet er erst, wenn ihre erste Woche abgelaufen ist. Das gilt auch für Verbindungen, die du später hinzufügst. Er läuft langsam im Hintergrund und wird pausiert, während eine Prüfung oder Synchronisierung läuft, wenn ein Dienst darum bittet, langsamer zu machen, oder wenn auf deiner Machine wenig Speicherplatz verfügbar ist. Neue Nachrichten haben immer Vorrang.

Sobald der Verlauf eines Postfachs importiert ist, liest deine Machine die gespeicherten E-Mails noch einmal, um Buchungs- und Ticketdetails zu finden. So werden auch ältere Buchungen unter [Reisen und Veranstaltungen](notes.md) angezeigt. Dieser Vorgang läuft genauso langsam und wird aus denselben Gründen pausiert.

Dabei wird der Zugriff genutzt, den die jeweilige Verbindung bereits hat. Du musst nichts Neues genehmigen.

## Wie weit zurück

Etwa ein Jahr. Auf deinem eigenen Computer kannst du das mit `history_days` in der Einstellungsdatei ändern (0 schaltet den Import aus, maximal sind 730 Tage). Telegram und andere Quellen importieren keinen älteren Verlauf.

Nachrichten von LinkedIn und X reichen 90 Tage zurück. Sie werden sehr langsam gelesen: ein paar kleine Abrufe pro Stunde, nur tagsüber. Wenn die Website sich dagegen wehrt, gibt es einen Tag lang keine Abrufe. So bleibt dein Konto sicher (`social_history_days`, 0 schaltet den Import aus).
