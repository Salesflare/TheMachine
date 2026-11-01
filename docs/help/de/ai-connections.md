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

Öffne **Einstellungen**, **KIs**. Es gibt zwei Wege. Zuerst kommt **Offizielle App**: **In Claude hinzufügen** und eine Adresse für jede Machine, `https://mcp.themachine.computer/mcp`, mit **Kopieren**. Darunter steht deine **Private Adresse (Ende-zu-Ende)**, `https://<dein Name>.mcp.themachine.computer/mcp`.

Bei einer Machine auf deinem eigenen Computer tippst du zuerst auf **Adresse holen**. Eine Seite in deinem Konto öffnet sich: Prüfe, ob sie denselben Code zeigt, bestätige und wähle einen Namen. Deine Machine verbindet sich selbst, ohne Neustart. Beide Wege brauchen das.

Danach holt sie sich ein eigenes Zertifikat für die Adresse. Das dauert ein paar Minuten und braucht das Paket `cryptography` für Python.

Für Claude tippe auf **In Claude hinzufügen** oder öffne [The Machine im Verzeichnis von Claude](https://claude.ai/directory/the-machine) und tippe auf Connect. Bei Team und Enterprise fügt ein Owner ihn in Organization settings hinzu.

Um in Claude stattdessen eine Adresse zu nutzen, öffne Customize, Connectors, tippe auf + Add und dann auf Add custom connector. Nenne ihn The Machine, füge die Adresse ein, tippe auf Continue und dann auf Add.

Öffne in ChatGPT chatgpt.com/plugins, tippe auf + und dann auf Add custom MCP server. Nenne ihn The Machine, füge die Adresse ein und wähle OAuth. Bestätige die Warnung und tippe auf Create as a plugin. Dein Tarif oder Workspace muss eigene MCP-Server erlauben.

Mit der offiziellen App bittet dich die KI, dich mit deinem The Machine-Konto anzumelden. Wähle diese Machine, wenn du mehrere hast, und gib die KI dann auf der eigenen Seite deiner Machine frei. Mit der privaten Adresse kommt die KI direkt zu deiner Machine.

KIs auf einem Gerät in deinem Tailnet, etwa Claude Code oder Cursor, können auch die Adresse deines Dashboards mit `/mcp` nutzen. **Trennen** nimmt eine Machine auf deinem eigenen Computer wieder aus deinem Konto.

Deine Machine zeigt, welche KI es ist. Eine KI, die sie nicht erkennt, zeigt die Adresse, von der sie kommt: Verbinde nur, wenn du das gerade selbst gestartet hast.

Wähle, was sie darf, **Lesen** oder **Lesen und Bearbeiten**. Mit Arbeits- und Privatkonten wählst du auch, was sie sehen darf. Dann wähle, wie lange: **1 Tag**, **7 Tage**, **30 Tage** oder **1 Jahr**. Drücke **Verbinden**, oder **Abbrechen**, um sie ohne etwas zurückzuschicken.

## Offizielle App oder private Adresse

Die offizielle App ist der einfache Weg: eine Adresse für alle, und dein Konto findet deine Machine. Die Cloud leitet die Anfragen unterwegs weiter, speichert aber nichts.

Mit deiner privaten Adresse ist alles bis zu deiner Machine verschlüsselt. Die Cloud reicht es nur weiter und kann es nicht lesen.

So oder so entscheidet deine Machine. Nur eine KI, die du auf ihrer Seite freigegeben hast, kommt hinein, mit dem Zugriff, den du gewählt hast. In **Einstellungen**, **KIs** zeigt eine KI, die über die offizielle App kam, **Offizielle App**.

## Was sie sieht

Eine Verbindung sieht nur ihren Bereich. Arbeit umfasst Aufgaben und Versprechen deiner Arbeitskonten, Arbeitskontakte, Firmen, Projekte und das Team-Briefing deiner Work Fleet. Privat umfasst den Rest. Nachrichtentext bleibt auf deiner Machine, außer du schaltest **Nachrichten** ein: Ohne das sieht eine KI die Quellen einer Aufgabe nur mit Absender, Betreff und Datum.

Team-Graph-Daten deiner Teammitglieder gehen nie an eine KI von außen.

## Nachrichten

Mit **Nachrichten** kann eine KI deine E-Mails, Slack, WhatsApp und andere Chats durchsuchen und lesen. Es ist aus, bis du es einschaltest, auf der Seite, auf der du sie verbindest, oder später in **Einstellungen**, **KIs**. Sie liest nur: Sie sendet, löscht oder markiert nie etwas.

Sie liest nur Nachrichten in ihrem Bereich. Manche gehen nie hinaus: Einmalcodes und Anmeldelinks, Nachrichten eines Boards oder Projekts **Nur du**, Verläufe, die The Machine als heikel eingestuft hat (Deals, Personal, Recht, Gesundheit, Geld), Verläufe, die du privat gehalten hast, und gelöschte Nachrichten.

Jedes Lesen steht in ihrer **Aktivität**, mit der Zahl der Nachrichten und den Verläufen, nie mit dem Text. Deine Machine gibt den Text als Daten markiert weiter, damit die KI keinen Anweisungen in einer Nachricht folgt.

Solange Nachrichten an ist, warten die Graph-Änderungen einer KI mit **Lesen und Bearbeiten** auf dein OK. Tippe bei der Änderung in **Aktivität** auf **Übernehmen** oder **Verwerfen**.

## In den Einstellungen

Öffne **Einstellungen**, **KIs**, um jede verbundene KI zu sehen, mit letzter Nutzung und Anzahl der Aufrufe. Ändere dort ihren Zugriff, ihren Bereich oder die Dauer. Der nächste Aufruf nutzt es. **Jetzt ausschalten** beendet alle ihre Anmeldungen auf einmal. **Aktivität** zeigt jeden Aufruf, auch abgelehnte. **Entfernen** nimmt sie weg.

Eine KI, die sich nicht selbst anmelden kann, kann einen Schlüssel nutzen. Gib ihm unter **Schlüssel hinzufügen** einen Namen, wähle Zugriff und Dauer und drücke **Schlüssel erstellen**. Kopiere den Schlüssel sofort: Er wird nur einmal gezeigt. Die KI sendet ihn als `Authorization: Bearer <key>`.

## Sicherheit

Jeder Aufruf wird festgehalten, abgelehnte auch. Eine abgelaufene oder ausgeschaltete Verbindung wird abgelehnt, bis du sie änderst. Die Anmeldung nutzt OAuth mit PKCE. Deine Machine speichert von jedem Token nur einen Fingerabdruck, eine Kopie ihrer Daten öffnet also nichts.
