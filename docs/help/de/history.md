---
title: Verlauf
area: connections
summary: Etwa ein Jahr ältere E-Mails, Meetings sowie WhatsApp-, Slack- und Teams-Nachrichten zum Durchsuchen, Lesen und um deine Kontakte besser kennenzulernen. Nie eine Aufgabe.
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
translated: 93575cd78b3085f7
---
## Was gespeichert wird

Deine Machine übernimmt etwa ein Jahr ältere E-Mails, Meetings sowie WhatsApp-, Slack- und Teams-Nachrichten. Über die Suche findest du sie, auch nach ihrer Bedeutung. In Threads werden sie ebenfalls angezeigt, und im [Kalender](calendar.md) siehst du vergangene Meetings.

Unter **Verbindungen** siehst du bei jeder Verbindung, wie weit sie zurückreicht, zum Beispiel **Verlauf: zurück bis** November 2025.

## Was deinem Graph hinzugefügt wird

Dein [Graph](graph.md) berücksichtigt diese Informationen: wie eng du mit anderen verbunden bist, wann du zuletzt mit ihnen gesprochen hast, wer wen kennt und die Personen und Organisationen selbst. Auch in der Timeline einer Person oder Organisation sind die Informationen zu sehen, damit der letzte Kontakt immer angezeigt wird. Die Antworten deiner Fleet auf die Frage „Wer kennt jemanden?“ berücksichtigen diese Informationen aus Arbeitskonten. Dabei gelten dieselben [Freigaberegeln](sharing-rules.md) wie für neue E-Mails.

## Was niemals passiert

Daraus entsteht nie eine Aufgabe oder ein Versprechen. Die Nachrichten gelten nie als neu, lösen nie eine Prüfung aus und werden nie einem Projekt hinzugefügt. Persönlicher Verlauf bleibt privat, genau wie persönliche E-Mails. Abgesehen von der Suche nach Bedeutung liest kein KI-Modell diese Nachrichten.

## Wann der Import läuft

Er beginnt nach dem ersten Blick auf deine Nachrichten. Bei jeder Verbindung startet er erst, wenn ihre erste Woche abgeschlossen ist. Das gilt auch für Verbindungen, die du später hinzufügst. Der Import läuft langsam im Hintergrund und pausiert, während eine Prüfung oder Synchronisierung läuft, wenn ein Dienst darum bittet, langsamer zu machen, oder wenn deiner Machine der Speicherplatz ausgeht. Neue Nachrichten haben immer Vorrang.

Sobald der Verlauf eines Postfachs importiert ist, liest deine Machine die gespeicherten E-Mails noch einmal, um Buchungs- und Ticketdetails zu finden. So werden auch ältere Buchungen unter [Reisen und Veranstaltungen](calendar.md#trips-and-events) angezeigt. Der Import läuft genauso langsam und pausiert aus denselben Gründen.

Dabei werden die Zugriffsrechte verwendet, die jede Verbindung bereits hat. Du musst nichts Neues genehmigen.

## Wie weit der Verlauf zurückreicht

Etwa ein Jahr. Auf deinem eigenen Computer kannst du den Zeitraum mit `history_days` in der Einstellungsdatei ändern (0 deaktiviert den Import, maximal sind 730 Tage). Telegram und andere Quellen importieren keinen älteren Verlauf.

Bei LinkedIn und X reichen Nachrichten 90 Tage zurück. Sie werden sehr langsam gelesen: nur tagsüber, ein paar kleine Lesevorgänge pro Stunde. Wenn die Website sich dagegen wehrt, wird einen Tag lang nichts gelesen, damit dein Konto sicher bleibt (`social_history_days`, 0 deaktiviert den Import).
