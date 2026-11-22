---
title: Andere KIs verbinden
area: connections
summary: Lass Claude, ChatGPT, Cursor, Codex oder GBrain deine Aufgaben und deinen Graph lesen. Mit Lesen und Bearbeiten können sie Änderungen vornehmen, die du rückgängig machen kannst.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: ac5a894df13907fd
---
## Was eine andere KI tun kann

Claude, ChatGPT, Cursor, Codex, GBrain und andere KIs können sich mit deiner Machine verbinden. Sie können deine Aufgaben, Versprechen, Team-Briefings sowie die Personen und Unternehmen in deinem Graph lesen.

Mit **Lesen und Bearbeiten** können sie auch eine Aufgabe oder einen E-Mail-Entwurf hinzufügen und deinen Graph aktualisieren: eine Information speichern, Details, Felder und Tags korrigieren oder eine Zeile zur Zusammenfassung einer Person hinzufügen.

Jede Änderung wird unter **Aktivität** angezeigt und lässt sich mit **Rückgängig** zurücknehmen. Sie führen niemals Datensätze zusammen, löschen sie oder teilen sie. Was sie speichern, wird mit **KI:** und ihrem Namen gekennzeichnet. Deine Machine behandelt es als ihre Behauptung, niemals als deine Anweisung.

Ein Entwurf bleibt liegen, bis du ihn selbst liest und auf „Senden“ drückst. Eine verbundene KI sendet niemals etwas und handelt nie in deinem Namen.

## Eine KI verbinden

Öffne **Einstellungen** und **Apps**. Unter **Die Apps von The Machine** findest du **In ChatGPT hinzufügen** und **In Claude hinzufügen**. Unter **Oder per Adresse hinzufügen** stehen die eine Adresse der offiziellen App für jede Machine, `https://mcp.themachine.computer/mcp`, und **Deine Adresse**, `https://<your name>.mcp.themachine.computer/mcp`, jeweils mit **Kopieren**.

Bei einer Machine auf deinem eigenen Computer drück zuerst unter **Adresse holen** auf **Einrichten**. Eine Seite in deinem Konto wird geöffnet: Prüfe, ob derselbe Code angezeigt wird, bestätige und wähle einen Namen. Deine Machine wird automatisch gekoppelt, ohne Neustart. Das ist bei beiden Methoden nötig.

Anschließend richtet deine Machine ihre sichere Adresse selbst ein. Das dauert ein paar Minuten.

Für Claude drück auf **In Claude hinzufügen** oder öffne [The Machine im Claude-Verzeichnis](https://claude.ai/directory/the-machine) und drück dann auf „Verbinden“. Bei Team und Enterprise fügt ein Inhaber die App in den Organisationseinstellungen hinzu.

Um stattdessen eine Adresse in Claude zu verwenden, öffne Customize, Connectors, drück auf + Add und dann auf Add custom connector. Nenne die Verbindung The Machine, füge die Adresse ein, drück auf Continue und dann auf Add.

Für ChatGPT drück auf **In ChatGPT hinzufügen** oder öffne [The Machine in ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4) und drück dann auf Install plugin. Bei Business und Enterprise muss ein Admin die App möglicherweise zuerst erlauben.

Die offizielle App verbindet sich mit einer gehosteten Machine und mit einer Machine auf deinem eigenen Computer, sobald diese ihre Adresse hat.

Für deine private Adresse oder eine Machine, die nicht im Network ist, füge stattdessen in ChatGPT einen benutzerdefinierten MCP-Server hinzu: Öffne chatgpt.com/plugins, drück auf + und dann auf Add custom MCP server. Nenne ihn The Machine, füge die Adresse ein und wähle OAuth. Bestätige den Warnhinweis und drück auf Create as a plugin. Dein Abo oder dein Workspace muss benutzerdefinierte MCP-Server erlauben.

Bei Verwendung der offiziellen App fordert dich die KI auf, dich mit deinem The Machine-Konto anzumelden. Wähle diese Machine aus, wenn du mehrere hast, und genehmige die Verbindung anschließend auf der eigenen Seite deiner Machine. Mit der privaten Adresse verbindet sich die KI direkt mit deiner Machine.

KIs auf einem Gerät in deinem privaten Netzwerk (Tailscale), etwa Claude Code oder Cursor, können auch die Adresse deines Dashboards gefolgt von `/mcp` verwenden. Mit **Diese Machine trennen** ganz unten unter **Einstellungen** und **Konto** entfernst du eine Machine auf deinem eigenen Computer wieder aus deinem Konto.

Deine Machine zeigt dir, welche KI anfragt. Kann sie das nicht feststellen, zeigt sie, woher die Anfrage kommt: Verbinde dich nur, wenn du das gerade selbst veranlasst hast.

Wähle aus, was die KI tun kann: **Lesen** oder **Lesen und Bearbeiten**. Wenn du Arbeits- und Privatkonten hast, wähle aus, was die KI sehen kann. Wähle dann aus, wie lange der Zugriff gelten soll: **1 Tag**, **7 Tage**, **30 Tage** oder **1 Jahr**. Drück auf **Verbinden** oder auf **Abbrechen**, um die KI ohne Zugriff abzuweisen.

## Offizielle App oder private Adresse

Die offizielle App ist der einfache Weg: eine Adresse für alle, und dein Konto findet deine Machine. Unsere Cloud leitet Anfragen weiter und speichert nichts.

Mit deiner privaten Adresse ist alles bis zu deiner Machine durchgehend verschlüsselt. Die Cloud leitet die Anfragen nur weiter und kann sie nicht lesen.

In beiden Fällen entscheidet deine Machine. Nur eine KI, die du auf ihrer Seite genehmigt hast, erhält Zugriff, und zwar mit den von dir gewählten Berechtigungen. Unter **Einstellungen** und **Apps** wird bei einer KI, die über die offizielle App verbunden ist, **Offizielle App** angezeigt.

## Was die KI sehen kann

Eine Verbindung sieht nur ihren jeweiligen Bereich. Arbeit umfasst die Aufgaben und Versprechen deiner Arbeitskonten, Personen, Unternehmen und Projekte aus dem Arbeitsbereich sowie das Team-Briefing deiner Work Fleet. Privat umfasst alles andere. Nachrichtentexte bleiben auf deiner Machine, sofern du **Nachrichten** nicht aktivierst: Ohne diese Option sieht eine KI bei den Quellen einer Aufgabe nur Absender, Betreff und Datum.

Team-Graph-Datensätze von Teammitgliedern werden niemals an eine externe KI weitergegeben.

## Nachrichten

Mit **Nachrichten** kann eine KI deine E-Mails, Slack-, WhatsApp- und andere Chats durchsuchen und lesen. Die Option ist zunächst deaktiviert. Du kannst sie beim Verbinden oder später unter **Einstellungen** und **Apps** aktivieren. Die KI kann nur lesen: Sie sendet und löscht nichts und markiert auch nichts.

Die KI liest nur Nachrichten in ihrem jeweiligen Bereich. Bestimmte Inhalte werden nie weitergegeben: Einmalcodes und Anmeldelinks, Nachrichten in einem **Nur du**-Board oder -Projekt, Threads, die The Machine als sensibel eingestuft hat (Geschäfte, Personal, Rechtliches, Gesundheit, Geld), Threads, die du privat gehalten hast, und gelöschte Nachrichten.

Jeder Lesezugriff wird unter **Aktivität** mit der Anzahl der Nachrichten und den betreffenden Threads angezeigt, niemals mit dem Nachrichtentext. Deine Machine übergibt den Text als Daten gekennzeichnet. Die KI sollte also keine Anweisungen befolgen, die in einer Nachricht stehen.

Solange **Nachrichten** aktiviert ist, musst du Änderungen am Graph durch eine KI mit **Lesen und Bearbeiten** bestätigen. Drück bei der Änderung unter **Aktivität** auf **Übernehmen** oder **Verwerfen**.

## In den Einstellungen

Öffne **Einstellungen** und **Apps**, um alle KIs zu sehen, die sich einmal verbunden haben, sowie deren Zugriff, Bereich, Ablaufdatum und letzte Nutzung. Mit **Nachrichten** kannst du den Zugriff auf Nachrichten direkt dort ein- und ausschalten. Drück auf **Ändern**, um den Zugriff, den Bereich oder die Dauer zu ändern. Der nächste Aufruf verwendet dann die neuen Einstellungen. Unter **Aktivität** werden alle Aufrufe angezeigt, auch abgewiesene. Mit **Jetzt ausschalten** pausierst du den Zugriff: Alle Anmeldungen werden beendet, der Verlauf bleibt erhalten. Mit **Entfernen** entfernst du die KI mitsamt ihrem Verlauf.

Wenn du dich erneut bei derselben KI anmeldest, ersetzt die neue Genehmigung die vorherige.

Eine KI, die sich nicht selbst anmelden kann, kann einen Schlüssel verwenden. Gib ihm unter **Schlüssel hinzufügen** einen Namen, wähle den Zugriff und die Dauer aus und drück auf **Schlüssel erstellen**. Kopiere den Schlüssel sofort: Er wird nur einmal angezeigt. Die KI sendet ihn als `Authorization: Bearer <key>`.

## Schütze deine Daten

Jeder Aufruf wird protokolliert, auch abgewiesene. Verbindungen, die abgelaufen oder ausgeschaltet sind, werden abgewiesen, bis du sie änderst. Deine Machine speichert von jeder Anmeldung nur einen Fingerabdruck. Eine Kopie dieser Daten reicht daher nicht aus, um etwas zu öffnen.
