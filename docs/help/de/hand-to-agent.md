---
title: Aufgabe an Claude Code oder Codex übergeben
area: cards
summary: Übergib eine Programmieraufgabe an Claude Code oder Codex. Das Ergebnis erscheint wieder in der Aufgabe.
covers: hand-to-agent
code: agent_jobs.py, agent_remote.py, dashboard.html
site: Connect Codex, Add more any time, On your Machine, Other ways, On my computer
order: 5
translated: 22e1b9b950988a58
---
## Aufgabe übergeben

1. Öffne bei der Aufgabe **…**, dann **Übergeben…** und wähle **Codex** oder **Claude Code**. Angezeigt werden nur die Tools, die du eingerichtet hast.
2. Prüfe die Zusammenfassung und was das Tool erhält, füge bei Bedarf eine Notiz hinzu und wähle **Übergeben**. Unter **Ganzen Auftrag ansehen** findest du die vollständige Aufgabenbeschreibung.

Während der Auftrag läuft, wird bei der Aufgabe der Status angezeigt. Anschließend siehst du das Ergebnis sowie **Was es getan hat** und **Änderungen anzeigen**. Über **Änderungen anfragen** kannst du angeben, was geändert werden soll. Mit **Übergeben…** unter **…** startest du den Auftrag neu. **Ausblenden** blendet das Ergebnis aus. Bei einer festhängenden Aufgabe, die du übergibst, wird während des Auftrags **Läuft…** statt **Hängt fest** angezeigt.

Ein Auftrag sendet niemals etwas für dich. Wenn du bei einem Schritt zum Veröffentlichen oder Bereitstellen selbst aktiv werden musst, führt **Ausführen** auf der Aufgabe diesen Schritt aus. Eine vom Auftrag verfasste Antwort bleibt ein Entwurf, den du selbst sendest.

## In der Codex-App

- **In Codex öffnen** öffnet nach Abschluss des Auftrags den zugehörigen Thread in der Codex-App.
- **Änderungen anfragen** setzt die Unterhaltung in derselben Codex-Konversation fort. Die Aufgabe folgt dieser Unterhaltung.
- Ein Auftrag endet, wenn 30 Minuten lang kein Fortschritt erfolgt oder nach insgesamt 6 Stunden. Ein Neustart hält ihn nicht an.

## Einrichten

Unter **Einstellungen** bei **Modell**, im Bereich **Codex und Claude Code**:

- **Codex**: Wähle aus, wo der Auftrag ausgeführt wird. Auf deiner Machine oder deinem Computer musst du hier nichts weiter einrichten. Mit **Ändern** öffnest du deine Einrichtungsseite.
- **Codex Cloud**: Gib die Umgebungs-ID von Codex und optional einen **Branch** an, von dem aus gestartet werden soll.
- **Claude Code**: Gib den Link zu einer Claude Code-Sitzung an.

Claude sendet das Ergebnis über den Connector von The Machine zurück. Füge ihn einmalig in claude.ai unter „Einstellungen“ > „Connectors“ > „Benutzerdefinierten Connector hinzufügen“ hinzu. Verwende dafür die Adresse, die unter der Sitzung angezeigt wird.

## Wo Codex läuft

Wähle auf einer gehosteten Machine die gewünschte Option auf deiner Einrichtungsseite unter **Jederzeit mehr hinzufügen** > **Codex**:

- **Auf deiner Machine** (Standard): Wähle **Codex verbinden** und gib den Code ein, den Codex bei OpenAI anzeigt. Codex nutzt denselben ChatGPT-Tarif wie dein Modell, und die Aufträge laufen auf deiner Machine. Ein Terminal ist nicht nötig. Wenn du mit demselben ChatGPT-Konto angemeldet bist, kann deine Machine außerdem sehen, wann dein Nutzungslimit zurückgesetzt wird, und dieses Wissen nutzen.
- **Andere Möglichkeiten** > **Auf meinem Computer**: Der Auftrag läuft auf deinem Computer und verwendet das dort angemeldete Codex. Die Verbindung ist verschlüsselt und gilt nur für diesen Computer. Installiere dort The Machine, verknüpfe sie auf deiner Kontoseite, führe `codex login` aus und lass The Machine laufen. Das Ergebnis erscheint wieder in der Aufgabe. Wenn der Computer ausgeschaltet ist, warten die Aufträge.
- **Andere Möglichkeiten** > **Codex Cloud**: Der Auftrag läuft in der Cloud von OpenAI. Wähle **Codex verbinden**. Codex nutzt denselben ChatGPT-Tarif wie dein Modell. OpenAI fragt dann nach einem weiteren Code für Codex. Gib anschließend in den Einstellungen die Codex-Cloud-Umgebung an.

Du kannst dich auch über dein Dashboard anmelden: **Verbindungen** > **Projekte und Code** > **Codex** > **Code holen**. Eine selbst gehostete Machine führt dieselbe Anmeldung selbst durch.

Auf einer gehosteten Machine wird **Codex und Claude Code** in den Einstellungen angezeigt, sobald GitHub oder Codex verbunden ist. Für Entwickler: der [Leitfaden zu Agents](https://github.com/Salesflare/TheMachine/blob/main/docs/agents.md).
