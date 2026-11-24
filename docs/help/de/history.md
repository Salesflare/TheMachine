---
title: Verlauf
area: connections
summary: Etwa ein Jahr ältere E-Mails, Termine sowie WhatsApp-, Slack- und Teams-Nachrichten zum Suchen, Lesen und um deine Kontakte besser kennenzulernen. Nie als Aufgabe.
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
translated: 2b5e84c61892c8e4
---
## Was gespeichert wird

Deine Machine importiert etwa ein Jahr ältere E-Mails, Termine sowie WhatsApp-, Slack- und Teams-Nachrichten. Die Suche findet sie auch nach ihrer Bedeutung, Unterhaltungen zeigen sie an und der [Kalender](calendar.md) zeigt vergangene Termine.

Unter **Verbindungen** steht für jede Verbindung, wie weit sie zurückreicht, zum Beispiel **Verlauf: zurück bis** November 2025.

## Was deinem Graph hinzugefügt wird

Dein [Graph](graph.md) erfasst, wie eng du mit anderen verbunden bist, wann du zuletzt mit ihnen gesprochen hast, wer wen kennt und welche Personen und Organisationen es gibt. Auch in der Chronik einer Person oder Organisation ist der Verlauf zu sehen, damit der letzte Kontakt immer dort steht. Die Antworten deiner Fleet auf die Frage „Wer kennt wen?“ berücksichtigen Verläufe aus Arbeitskonten. Dabei gelten dieselben [Freigaberegeln](sharing-rules.md) wie für neue E-Mails.

## Was niemals passiert

Aus dem Verlauf entsteht nie eine Aufgabe oder ein Versprechen. Er wird nie als neu gezählt, löst nie eine Prüfung aus und wird keinem Projekt hinzugefügt. Persönlicher Verlauf bleibt persönlich, genau wie private E-Mails.

Abgesehen von der Suche nach Bedeutung liest dein KI-Modell den Verlauf nur an drei Stellen:

- in Suchergebnissen, zum Beispiel bei einer Frage von dir oder einer Aufgabe, an der gerade gearbeitet wird
- in E-Mails mit Buchungsdetails, für [Reisen und Veranstaltungen](calendar.md#trips-and-events)
- in einem [Meeting-Briefing](calendar.md#ready-for-your-meetings): Notizen früherer Meetings und einige ältere Nachrichten von den Personen, die du triffst

## Wann der Verlauf geladen wird

Der Vorgang beginnt nach dem ersten Durchsehen deiner Nachrichten. Bei jeder Verbindung startet er erst, wenn die erste Woche verarbeitet wurde. Das gilt auch für Verbindungen, die du später hinzufügst. Der Verlauf wird langsam im Hintergrund geladen. Der Vorgang pausiert, während eine Prüfung oder Synchronisierung läuft, wenn ein Dienst darum bittet, langsamer zu machen, oder wenn auf deiner Machine wenig Speicherplatz frei ist. Neue Nachrichten haben immer Vorrang.

Sobald der Verlauf eines Postfachs geladen ist, liest deine Machine die gespeicherten E-Mails noch einmal, um Buchungs- und Ticketdetails zu finden. So erscheinen auch ältere Buchungen unter [Reisen und Veranstaltungen](calendar.md#trips-and-events). Dabei geht sie genauso langsam vor und pausiert aus denselben Gründen.

Dabei werden nur die Zugriffsrechte genutzt, die für die jeweilige Verbindung bereits gelten. Du musst nichts Neues genehmigen.

## Wie weit der Verlauf zurückreicht

Etwa ein Jahr. Auf deinem eigenen Computer kannst du das mit `history_days` in der Einstellungsdatei ändern (0 deaktiviert den Verlauf, der Höchstwert ist 730). Telegram und andere Quellen laden keine älteren Verläufe.

Nachrichten von LinkedIn und X reichen 90 Tage zurück und werden sehr langsam eingelesen: nur wenige kleine Abrufe pro Stunde und nur tagsüber. Wenn die Website sich dagegen wehrt, gibt es einen Tag lang keine Abrufe. So bleibt dein Konto geschützt (`social_history_days`, 0 deaktiviert den Verlauf).
