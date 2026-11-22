---
title: Andere KIs verbinden
area: connections
summary: Lass Claude, ChatGPT, Cursor, Codex oder GBrain deine Aufgaben und deinen Graph lesen. Mit „Lesen und Bearbeiten“ können sie Änderungen vornehmen, die du rückgängig machen kannst.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: ac5a894df13907fd
---
## Was eine andere KI tun kann

Claude, ChatGPT, Cursor, Codex, GBrain und andere KIs können sich mit deiner Machine verbinden. Sie können deine Aufgaben, Versprechen, Team-Briefings sowie die Personen und Unternehmen in deinem Graph lesen.

Mit **Lesen und Bearbeiten** können sie auch eine Aufgabe oder einen E-Mail-Entwurf hinzufügen und deinen Graph aktualisieren: eine Tatsache speichern, Angaben, Felder und Tags korrigieren oder eine Zeile zur Zusammenfassung einer Person hinzufügen.

Jede Änderung erscheint unter **Aktivität** mit **Rückgängig**. Die KIs führen keine Datensätze zusammen, löschen oder teilen sie. Was sie speichern, ist mit **KI:** und ihrem Namen gekennzeichnet. Deine Machine behandelt es als deren Behauptung, niemals als deine Anweisung.

Ein Entwurf bleibt liegen, bis du ihn selbst liest und auf „Senden“ drückst. Eine verbundene KI sendet nie etwas und handelt nie in deinem Namen.

## Eine KI verbinden

Öffne **Einstellungen**, **Apps**. Unter **Die Apps von The Machine** findest du **In ChatGPT hinzufügen** und **In Claude hinzufügen**. Unter **Oder per Adresse hinzufügen** findest du die eine Adresse der offiziellen App für jede Machine, `https://mcp.themachine.computer/mcp`, sowie **Deine Adresse**, `https://<your name>.mcp.themachine.computer/mcp`, jeweils mit **Kopieren**.

Bei einer Machine auf deinem eigenen Computer drück zuerst unter **Adresse holen** auf **Einrichten**. Dann öffnet sich eine Seite in deinem Konto. Prüfe, ob dort derselbe Code angezeigt wird, bestätige und wähle einen Namen. Deine Machine wird automatisch gekoppelt, ohne Neustart. Beides ist nötig.

Deine Machine richtet dann automatisch ihre sichere Adresse ein. Das dauert ein paar Minuten.

Für Claude drück auf **In Claude hinzufügen** oder öffne [The Machine im Claude-Verzeichnis](https://claude.ai/directory/the-machine) und drück dann auf **Verbinden**. Bei Team und Enterprise fügt ein Inhaber die App in den Organisationseinstellungen hinzu.

Wenn du stattdessen eine Adresse in Claude verwenden möchtest, öffne „Anpassen“, „Konnektoren“, drück auf „+ Hinzufügen“ und dann auf „Benutzerdefinierten Connector hinzufügen“. Gib The Machine als Namen ein, füge die Adresse ein, drück auf „Weiter“ und dann auf „Hinzufügen“.

Für ChatGPT drück auf **In ChatGPT hinzufügen** oder öffne [The Machine in ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4) und drück dann auf „Plugin installieren“. Bei Business und Enterprise muss ein Admin die App möglicherweise zuerst freigeben.

Die offizielle App verbindet sich mit einer gehosteten Machine und, sobald sie ihre Adresse hat, auch mit einer Machine auf deinem eigenen Computer.

Für deine private Adresse oder eine Machine, die nicht im Network ist, kannst du stattdessen einen benutzerdefinierten MCP-Server in ChatGPT hinzufügen: Öffne chatgpt.com/plugins, drück auf „+“ und dann auf „Benutzerdefinierten MCP-Server hinzufügen“. Gib The Machine als Namen ein, füge die Adresse ein und wähle OAuth. Bestätige die Warnung und drück auf „Als Plugin erstellen“. Dein Abo oder Workspace muss benutzerdefinierte MCP-Server erlauben.

Bei der offiziellen App fordert die KI dich auf, dich mit deinem The Machine-Konto anzumelden. Wenn du mehrere Machines hast, wähl diese Machine aus und bestätige die Verbindung auf der eigenen Seite deiner Machine. Bei einer privaten Adresse verbindet sich die KI direkt mit deiner Machine.

KIs auf einem Gerät in deinem privaten Netzwerk (Tailscale), zum Beispiel Claude Code oder Cursor, können auch die Adresse deines Dashboards gefolgt von `/mcp` verwenden. **Diese Machine trennen** unten unter **Einstellungen**, **Konto** entfernt eine Machine auf deinem eigenen Computer wieder aus deinem Konto.

Deine Machine zeigt dir, welche KI die Verbindung anfragt. Wenn sie das nicht feststellen kann, zeigt sie dir, woher die Anfrage kommt. Verbinde sie nur, wenn du die Verbindung gerade selbst gestartet hast.

Wähl aus, was die KI tun darf: **Lesen** oder **Lesen und Bearbeiten**. Wenn du sowohl ein Work- als auch ein Personal-Konto hast, wähl aus, was sie sehen darf. Wähl dann aus, wie lange der Zugriff gelten soll: **1 Tag**, **7 Tage**, **30 Tage** oder **1 Jahr**. Drück auf **Verbinden** oder auf **Abbrechen**, um die Anfrage abzulehnen.

## Offizielle App oder private Adresse

Die offizielle App ist der einfache Weg: eine Adresse für alle, und dein Konto findet deine Machine. Unsere Cloud leitet Anfragen weiter und speichert nichts.

Bei deiner privaten Adresse ist alles bis zu deiner Machine durchgehend verschlüsselt. Die Cloud leitet nur weiter und kann die Inhalte nicht lesen.

So oder so entscheidet deine Machine. Nur eine KI, die du auf ihrer Seite freigegeben hast, erhält Zugriff, und zwar mit den von dir ausgewählten Berechtigungen. Unter **Einstellungen**, **Apps** wird bei einer KI, die über die offizielle App verbunden ist, **Offizielle App** angezeigt.

## Was sie sehen kann

Eine Verbindung sieht nur ihren jeweiligen Bereich. Work umfasst Aufgaben und Versprechen deiner Arbeitskonten, berufliche Kontakte, Unternehmen und Projekte sowie das Team-Briefing deiner Work Fleet. Personal umfasst alles andere. Nachrichtentexte bleiben auf deiner Machine, sofern du **Nachrichten** nicht aktivierst. Andernfalls sieht eine KI bei den Quellen einer Aufgabe nur Absender, Betreff und Datum.

Datensätze aus dem Team Graph deiner Teammitglieder werden niemals an eine externe KI weitergegeben.

## Nachrichten

Mit **Nachrichten** kann eine KI deine E-Mails, Slack-Nachrichten, WhatsApp-Nachrichten und andere Chats durchsuchen und lesen. Die Funktion ist ausgeschaltet, bis du sie auf der Seite aktivierst, auf der du die KI verbindest, oder später unter **Einstellungen**, **Apps**. Die KI kann nur lesen. Sie sendet und löscht nichts und markiert auch nichts.

Sie liest nur Nachrichten in ihrem Bereich. Bestimmte Nachrichten werden nie weitergegeben: Einmalcodes und Anmeldelinks, Nachrichten auf einem Board oder in einem Projekt mit **Nur du**, Threads, die The Machine als sensibel eingestuft hat (Geschäfte, Personal, Rechtliches, Gesundheit, Finanzen), Threads, die du privat gehalten hast, und gelöschte Nachrichten.

Jeder Lesezugriff erscheint unter **Aktivität** der KI mit der Anzahl der Nachrichten und den jeweiligen Threads, aber nie mit dem Nachrichtentext. Deine Machine übergibt den Text als Daten, damit die KI Anweisungen in einer Nachricht nicht befolgen sollte.

Solange Nachrichten aktiviert sind, musst du Änderungen am Graph durch eine KI mit **Lesen und Bearbeiten** erst freigeben. Drück bei der Änderung unter **Aktivität** auf **Übernehmen** oder **Verwerfen**.

## In den Einstellungen

Öffne **Einstellungen**, **Apps**, um jede KI zu sehen, die sich einmal verbunden hat, sowie ihre Berechtigungen, ihren Bereich, ihr Ablaufdatum und ihre letzte Nutzung. Dort kannst du **Nachrichten** auch ein- und ausschalten. Drück auf **Ändern**, um ihre Berechtigungen, ihren Bereich oder die Zugriffsdauer anzupassen. Die nächste Anfrage verwendet die neuen Einstellungen. Unter **Aktivität** werden alle Anfragen aufgeführt, auch abgelehnte. **Jetzt ausschalten** unterbricht den Zugriff: Alle Anmeldungen werden beendet, der Verlauf bleibt erhalten. **Entfernen** löscht die Verbindung samt Verlauf.

Wenn du dich erneut bei derselben KI anmeldest, ersetzt die neue Freigabe die vorherige.

Eine KI, die sich nicht selbst anmelden kann, kann einen Schlüssel verwenden. Gib unter **Schlüssel hinzufügen** einen Namen ein, wähl die Berechtigungen und die Zugriffsdauer aus und drück auf **Schlüssel erstellen**. Kopier den Schlüssel sofort, denn er wird nur einmal angezeigt. Die KI sendet ihn als `Authorization: Bearer <key>`.

## Sicher bleiben

Jede Anfrage wird protokolliert, auch abgelehnte. Anfragen werden abgelehnt, wenn eine Verbindung abgelaufen oder ausgeschaltet ist, bis du sie änderst. Deine Machine speichert von jeder Anmeldung nur einen Fingerabdruck. Eine Kopie dieser Daten reicht daher nicht aus, um Zugriff zu erhalten.
