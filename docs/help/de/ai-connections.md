---
title: Andere KIs verbinden
area: connections
summary: Lass Claude, ChatGPT, Cursor, Codex oder GBrain deine Aufgaben und deinen Graph über MCP lesen, jede mit eigenem Zugriff und Ablauf.
covers: ai-connections, settings:ai
code: ai_access.py, ai_app.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
---
## Was eine andere KI kann

Andere KIs können sich über MCP mit deiner Machine verbinden: Claude, ChatGPT, Cursor, Codex, GBrain und weitere. Sie können deine Aufgaben, Versprechen, Team-Briefings und die Personen und Firmen in deinem Graph lesen.

Höchstens fügen sie eine Aufgabe hinzu, oder eine Aufgabe mit einem E-Mail-Entwurf. Ein Entwurf wartet in deiner Machine, bis du ihn liest und selbst auf **Senden** drückst. Eine verbundene KI sendet nie etwas und handelt nie für dich. Do it und die Agents deiner Machine gehören nicht dazu.

## Eine verbinden

Füge in der anderen KI einen eigenen Connector oder MCP-Server mit der Adresse deiner Machine und `/mcp` hinzu. Bei einer gehosteten Machine ist das `https://<dein Name>.app.themachine.computer/mcp`. Bei einer Machine auf deinem eigenen Computer ist es die Adresse deines Dashboards, die nur Geräte in deinem Tailnet erreichen.

Die KI schickt dich zur Anmeldung zu deiner Machine. Deine Machine zeigt, welche KI es ist. Eine KI, die sie nicht erkennt, zeigt die Adresse, von der sie kommt: Verbinde nur, wenn du das gerade selbst gestartet hast.

Wähle, was sie darf, **Lesen** oder **Lesen und Entwürfe**. Mit Arbeits- und Privatkonten wählst du auch, was sie sehen darf. Dann wähle, wie lange: **1 Tag**, **7 Tage**, **30 Tage** oder **1 Jahr**. Drücke **Verbinden**, oder **Abbrechen**, um sie ohne etwas zurückzuschicken.

## Was sie sieht

Eine Verbindung sieht nur ihren Bereich. Arbeit umfasst Aufgaben und Versprechen deiner Arbeitskonten, Arbeitskontakte, Firmen, Projekte und das Team-Briefing deiner Work Fleet. Privat umfasst den Rest. Nachrichtentext bleibt auf deiner Machine: Eine KI sieht die Quellen einer Aufgabe nur mit Absender, Betreff und Datum.

Team-Graph-Daten deiner Teammitglieder gehen nie an eine KI von außen.

## In den Einstellungen

Öffne **Einstellungen**, **KIs**, um jede verbundene KI zu sehen, mit letzter Nutzung und Anzahl der Aufrufe. Ändere dort ihren Zugriff, ihren Bereich oder die Dauer. Der nächste Aufruf nutzt es. **Jetzt ausschalten** beendet alle ihre Anmeldungen auf einmal. **Aktivität** zeigt jeden Aufruf, auch abgelehnte. **Entfernen** nimmt sie weg.

Eine KI, die sich nicht selbst anmelden kann, kann einen Schlüssel nutzen. Gib ihm unter **Schlüssel hinzufügen** einen Namen, wähle Zugriff und Dauer und drücke **Schlüssel erstellen**. Kopiere den Schlüssel sofort: Er wird nur einmal gezeigt. Die KI sendet ihn als `Authorization: Bearer <key>`.

## Sicherheit

Jeder Aufruf wird festgehalten, abgelehnte auch. Eine abgelaufene oder ausgeschaltete Verbindung wird abgelehnt, bis du sie änderst. Die Anmeldung nutzt OAuth mit PKCE. Deine Machine speichert von jedem Token nur einen Fingerabdruck, eine Kopie ihrer Daten öffnet also nichts.
