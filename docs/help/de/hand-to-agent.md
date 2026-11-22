---
title: An Claude Code oder Codex übergeben
area: cards
summary: Schick eine Programmieraufgabe an Claude Code oder Codex. Das Ergebnis kommt bei der Aufgabe zurück.
covers: hand-to-agent
code: agent_jobs.py, agent_remote.py, dashboard.html
site: Connect Codex, Add more any time, On your Machine, Other ways, On my computer
order: 5
translated: 333d553e80aea529
---
## Eine Aufgabe übergeben

1. Öffne bei der Aufgabe **…**, dann **Übergeben…**, und wähle **Codex** oder **Claude Code**. Nur die Tools, die du eingerichtet hast, erscheinen.
2. Prüfe die Zusammenfassung und was mitgeht, füge auf Wunsch eine Notiz hinzu und tippe auf **Übergeben**. **Ganzen Auftrag ansehen** zeigt das komplette Briefing.

Die Aufgabe zeigt dann, dass daran gearbeitet wird, und das Ergebnis, wenn es fertig ist, mit **Was es getan hat** und **Änderungen anzeigen**. **Änderungen anfragen** sagt dem Agenten, was er ändern soll. **Übergeben…** im **…** fängt von vorn an; **Ausblenden** legt das Ergebnis weg. Eine Aufgabe, die festhing und die du übergibst, zeigt **Läuft…** statt **Hängt fest**, solange der Auftrag läuft.

Ein Auftrag sendet nie etwas für dich. Lässt er dir einen Schritt zum Veröffentlichen oder Deployen übrig, führt **Ausführen** auf der Aufgabe diesen Schritt aus. Eine Antwort, die er geschrieben hat, bleibt ein Entwurf, den du selbst sendest.

## In der Codex-App

- **In Codex öffnen** öffnet den Thread des Auftrags in der Codex-App, sobald der Auftrag fertig ist.
- **Änderungen anfragen** geht in demselben Codex-Gespräch weiter, und die Aufgabe folgt ihm.
- Ein Auftrag stoppt nach 30 Minuten ohne Fortschritt oder nach insgesamt 6 Stunden. Ein Neustart stoppt ihn nicht.

## Einrichten

In **Einstellungen**, **Modell**, unter **Codex und Claude Code**:

- **Codex**: wo es läuft. Auf deiner Machine oder deinem Computer braucht es hier nichts weiter; **Ändern** öffnet deine Einrichtungsseite.
- **Codex Cloud**: die Umgebungs-ID aus Codex und optional ein **Branch** als Ausgangspunkt.
- **Claude Code**: der Link einer Sitzung in Claude Code.

Claude schickt sein Ergebnis über den Connector von The Machine zurück. Füge ihn einmal in claude.ai hinzu, unter Settings, Connectors, Add custom connector, mit der Adresse, die unter der Sitzung steht.

## Wo Codex läuft

Auf einer gehosteten Machine wählst du es auf deiner Einrichtungsseite, unter **Jederzeit mehr hinzufügen**, **Codex**:

- **Auf deiner Machine** (die Voreinstellung): Tippe auf **Codex verbinden** und gib den angezeigten Code bei OpenAI ein. Es nutzt denselben ChatGPT-Tarif wie dein Modell, und Aufträge laufen auf deiner Machine. Kein Terminal nötig.
- **Andere Wege**, **Auf meinem Computer**: Der Auftrag läuft auf deinem eigenen Computer, mit dem Codex, das dort angemeldet ist. Er wird verschlüsselt übertragen, nur für diesen Computer. Installiere The Machine auf diesem Computer, kopple ihn auf deiner Kontoseite, führe `codex login` aus und lass The Machine laufen. Das Ergebnis kommt bei der Aufgabe zurück. Ist der Computer aus, warten Aufträge.
- **Andere Wege**, **Codex Cloud**: Der Auftrag läuft in der Cloud von OpenAI. Tippe auf **Codex verbinden**. Es nutzt denselben ChatGPT-Tarif wie dein Modell, und OpenAI fragt nach einem weiteren Code, für Codex. Gib dann die Codex-Cloud-Umgebung in den Einstellungen ein.

Oder melde dich im Dashboard an: **Verbindungen**, **Projekte und Code**, **Codex**, **Code holen**. Eine selbst gehostete Machine führt dieselbe Anmeldung selbst aus.

Auf einer gehosteten Machine erscheint **Codex und Claude Code** in den Einstellungen, sobald GitHub oder Codex verbunden ist. Für Entwickler: der [Agents-Leitfaden](https://github.com/Salesflare/TheMachine/blob/main/docs/agents.md).
