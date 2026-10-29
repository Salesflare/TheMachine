---
title: An Claude Code oder Codex übergeben
area: cards
summary: Schick eine Programmieraufgabe an Claude Code oder Codex. Das Ergebnis kommt bei der Aufgabe zurück.
covers: hand-to-agent
code: agent_jobs.py, agent_remote.py, dashboard.html
site: Connect Codex, Add more any time, On your Machine, Other ways, On my computer
order: 5
---
## Eine Aufgabe übergeben

1. Öffne bei der Aufgabe **Mehr** und wähle **An Codex übergeben** oder **An Claude Code übergeben**. Das erscheint, sobald das Tool eingerichtet ist.
2. Prüfe die Zusammenfassung und was mitgeht, füge auf Wunsch eine Notiz hinzu und tippe auf **Übergeben**. **Ganzen Auftrag ansehen** zeigt das komplette Briefing.

Die Aufgabe zeigt dann, dass daran gearbeitet wird, und das Ergebnis, wenn es fertig ist, mit **Änderungen zeigen**. **Ändern** bittet um Änderungen. **Erneut übergeben** fängt von vorn an.

Ein Auftrag sendet nie etwas für dich.

## In der Codex-App

- **In Codex öffnen** öffnet den Thread des Jobs in der Codex-App. Solange Codex hier daran arbeitet, kann die App ihn noch nicht öffnen. Er öffnet sich, sobald es fertig ist.
- **Ändern** bei einem Thread, der in der Codex-App offen ist, geht in genau diesem Gespräch dort weiter, und die Aufgabe folgt ihm.
- Ein Job stoppt nur, wenn Codex 30 Minuten lang nichts tut, oder nach insgesamt 6 Stunden. Ein Neustart von The Machine stoppt ihn nicht.

## Einrichten

In **Einstellungen**, **Modell**, unter **Codex und Claude Code**:

- **Codex**: wo es läuft. Auf deiner Machine oder deinem Computer braucht es hier nichts weiter; **Ändern** öffnet deine Einrichtungsseite.
- **Codex Cloud**: die ID ihrer Umgebung, aus Codex, und optional ein **Branch** als Ausgangspunkt.
- **Claude Code**: der Link einer Sitzung in Claude Code.

Claude schickt sein Ergebnis über den Connector von The Machine zurück. Füge ihn einmal in claude.ai hinzu, unter Settings, Connectors, Add custom connector, mit der Adresse, die unter der Sitzung steht.

## Wo Codex läuft

Auf einer gehosteten Machine wählst du es auf deiner Einrichtungsseite, unter **Jederzeit mehr hinzufügen**, **Codex**:

- **Auf deiner Machine** (die Voreinstellung): Tippe auf **Codex verbinden** und gib den angezeigten Code bei OpenAI ein. Es nutzt denselben ChatGPT-Tarif wie dein Modell, und Aufträge laufen auf deiner Machine. Kein Terminal nötig.
- **Andere Wege**, **Auf meinem Computer**: Der Auftrag läuft auf deinem eigenen Computer, mit dem Codex, das dort angemeldet ist. Nichts von Codex liegt auf deinem Server, und der Auftrag ist nur für diesen Computer verschlüsselt: Das Network gibt ihn weiter, kann ihn aber nicht lesen. Installiere The Machine auf diesem Computer, kopple ihn auf deiner Kontoseite und führe dort `codex login` aus. Lass The Machine darauf laufen. Der Auftrag erscheint als Thread in der Codex-App auf diesem Computer, und das Ergebnis kommt bei der Aufgabe zurück. Ist der Computer aus, warten Aufträge, bis er wieder da ist.
- **Andere Wege**, **Codex Cloud**: Der Auftrag läuft in der Cloud von OpenAI. Tippe auf **Codex verbinden**. Es nutzt denselben ChatGPT-Tarif wie dein Modell, und OpenAI fragt nach einem weiteren Code, für Codex. Gib dann die Cloud-Umgebung in Codex in den Einstellungen ein.

Oder melde dich im Dashboard an: **Verbindungen**, **+ Hinzufügen**, **Codex**, **Code holen**. Eine selbst gehostete Machine führt dieselbe Anmeldung selbst aus.

Auf einer gehosteten Machine erscheint Codex und Claude Code, sobald GitHub oder Codex verbunden ist. Es erscheint auch bei Setups, die Aufträge woanders ausführen. Mehr dazu im [Agents-Leitfaden](https://github.com/Salesflare/TheMachine/blob/main/docs/agents.md).
