---
title: Andere KIs verbinden
area: connections
summary: Lass Claude, ChatGPT, Cursor, Codex oder GBrain deine Aufgaben und deinen Graph über MCP lesen, jede mit eigenem Zugriff und Ablauf.
covers: ai-connections, settings:ai
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
---
## Was eine andere KI kann

Andere KIs können sich über MCP mit deiner Machine verbinden: Claude, ChatGPT, Cursor, Codex, GBrain und weitere. Sie können deine Aufgaben, Versprechen, Team-Briefings und die Personen und Firmen in deinem Graph lesen.

Mit **Lesen und Bearbeiten** können sie auch eine Aufgabe hinzufügen, oder eine Aufgabe mit einem E-Mail-Entwurf, und deinen Graph ändern: einen Fakt zu einer Person oder Firma speichern, Details, Felder und Tags korrigieren oder eine Zeile zur Zusammenfassung einer Person hinzufügen.

Jede Änderung steht unter **Aktivität** mit **Rückgängig**. Sie führen nie Einträge zusammen, löschen oder teilen sie nie. Was sie speichern, zeigt **KI:** und ihren Namen, in ihrem Bereich. Du kannst es ändern oder entfernen, und The Machine kann eine Zeile der Zusammenfassung später überarbeiten. Deine Machine behandelt es als ihre Aussage, nie als deine Anweisung.

Ein Entwurf wartet in deiner Machine, bis du ihn liest und selbst auf **Senden** drückst. Eine verbundene KI sendet nie etwas und handelt nie für dich. Do it und die Agents deiner Machine gehören nicht dazu.

## Eine verbinden

Öffne **Einstellungen**, **KIs**. Oben steht die Adresse deiner Machine für KIs, `https://<dein Name>.mcp.themachine.computer/mcp`, mit **Kopieren**. Bei einer Machine auf deinem eigenen Computer tippst du zuerst auf **Adresse holen**. Eine Seite in deinem Konto öffnet sich: Prüfe, ob sie denselben Code zeigt, bestätige und wähle einen Namen. Deine Machine verbindet sich selbst, ohne Neustart.

Danach holt sie sich ein eigenes Zertifikat für die Adresse. Das dauert ein paar Minuten und braucht das Paket `cryptography` für Python.

Öffne in ChatGPT chatgpt.com/plugins, tippe auf + und dann auf Add custom MCP server. Nenne ihn The Machine, füge die Adresse ein und wähle OAuth. Bestätige die Warnung und tippe auf Create as a plugin. Dein Tarif oder Workspace muss eigene MCP-Server erlauben.

Öffne in Claude Customize, Connectors, tippe auf + Add und dann auf Add custom connector. Nenne ihn The Machine, füge die Adresse ein, tippe auf Continue und dann auf Add. Bei Team und Enterprise fügt ein Owner ihn in Organization settings hinzu.

KIs auf einem Gerät in deinem Tailnet, etwa Claude Code oder Cursor, können auch die Adresse deines Dashboards mit `/mcp` nutzen. **Trennen** nimmt eine Machine auf deinem eigenen Computer wieder aus deinem Konto.

Die KI schickt dich zur Anmeldung zu deiner Machine. Deine Machine zeigt, welche KI es ist. Eine KI, die sie nicht erkennt, zeigt die Adresse, von der sie kommt: Verbinde nur, wenn du das gerade selbst gestartet hast.

Wähle, was sie darf, **Lesen** oder **Lesen und Bearbeiten**. Mit Arbeits- und Privatkonten wählst du auch, was sie sehen darf. Dann wähle, wie lange: **1 Tag**, **7 Tage**, **30 Tage** oder **1 Jahr**. Drücke **Verbinden**, oder **Abbrechen**, um sie ohne etwas zurückzuschicken.

## Was sie sieht

Eine Verbindung sieht nur ihren Bereich. Arbeit umfasst Aufgaben und Versprechen deiner Arbeitskonten, Arbeitskontakte, Firmen, Projekte und das Team-Briefing deiner Work Fleet. Privat umfasst den Rest. Nachrichtentext bleibt auf deiner Machine: Eine KI sieht die Quellen einer Aufgabe nur mit Absender, Betreff und Datum.

Team-Graph-Daten deiner Teammitglieder gehen nie an eine KI von außen.

## In den Einstellungen

Öffne **Einstellungen**, **KIs**, um jede verbundene KI zu sehen, mit letzter Nutzung und Anzahl der Aufrufe. Ändere dort ihren Zugriff, ihren Bereich oder die Dauer. Der nächste Aufruf nutzt es. **Jetzt ausschalten** beendet alle ihre Anmeldungen auf einmal. **Aktivität** zeigt jeden Aufruf, auch abgelehnte. **Entfernen** nimmt sie weg.

Eine KI, die sich nicht selbst anmelden kann, kann einen Schlüssel nutzen. Gib ihm unter **Schlüssel hinzufügen** einen Namen, wähle Zugriff und Dauer und drücke **Schlüssel erstellen**. Kopiere den Schlüssel sofort: Er wird nur einmal gezeigt. Die KI sendet ihn als `Authorization: Bearer <key>`.

## Sicherheit

Jeder Aufruf wird festgehalten, abgelehnte auch. Eine abgelaufene oder ausgeschaltete Verbindung wird abgelehnt, bis du sie änderst. Die Anmeldung nutzt OAuth mit PKCE. Deine Machine speichert von jedem Token nur einen Fingerabdruck, eine Kopie ihrer Daten öffnet also nichts.
