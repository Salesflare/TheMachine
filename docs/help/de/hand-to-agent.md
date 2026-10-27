---
title: An Claude Code oder Codex übergeben
area: cards
summary: Schick eine Programmieraufgabe an Claude Code oder Codex. Das Ergebnis kommt bei der Aufgabe zurück.
covers: hand-to-agent
code: agent_jobs.py, agent_remote.py, dashboard.html
site: Connect Codex, Add more any time
order: 5
---
## Eine Aufgabe übergeben

1. Öffne bei der Aufgabe **Mehr** und wähle **An Codex übergeben** oder **An Claude Code übergeben**. Das erscheint, sobald das Tool eingerichtet ist.
2. Prüfe die Zusammenfassung und was mitgeht, füge auf Wunsch eine Notiz hinzu und tippe auf **Übergeben**. **Ganzen Auftrag ansehen** zeigt das komplette Briefing.

Die Aufgabe zeigt dann, dass daran gearbeitet wird, und das Ergebnis, wenn es fertig ist, mit **Änderungen zeigen**. **Ändern** bittet um Änderungen. **Erneut übergeben** fängt von vorn an.

Ein Auftrag sendet nie etwas für dich.

## Einrichten

In **Einstellungen**, **Allgemein**, unter **Coding-Agents**:

- **Sitzung in Claude Code**: die Adresse einer Sitzung in Claude Code.
- **Cloud-Umgebung in Codex**: die ID ihrer Umgebung.
- **Läuft auf** und optional ein **Branch**.

Claude schickt sein Ergebnis über den Connector von The Machine zurück. Füge ihn einmal in claude.ai hinzu, unter Settings, Connectors, Add custom connector, mit der dort angezeigten Adresse. Für Codex auf einer gehosteten Machine tippst du zuerst auf deiner Einrichtungsseite unter **Jederzeit mehr hinzufügen** auf **Codex verbinden**. Es nutzt denselben ChatGPT-Tarif wie dein Modell, und OpenAI fragt nach einem weiteren Code, für Codex.

Auf einer gehosteten Machine erscheint Coding-Agents, sobald GitHub oder Codex verbunden ist. Es erscheint auch bei Setups, die Aufträge woanders ausführen. Mehr dazu im [Agents-Leitfaden](https://github.com/Salesflare/TheMachine/blob/main/docs/agents.md).
