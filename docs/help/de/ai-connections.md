---
title: Andere KIs verbinden
area: connections
summary: Lass Claude, ChatGPT, Cursor, Codex oder GBrain deine Aufgaben und deinen Graph lesen. Mit „Lesen und Bearbeiten“ können sie Änderungen vornehmen, die du rückgängig machen kannst.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: a8637260c99df309
---
## Was eine andere KI tun kann

Claude, ChatGPT, Cursor, Codex, GBrain und andere KIs können sich mit deiner Machine verbinden. Sie können deine Aufgaben, Versprechen, Team-Briefings und die Personen und Unternehmen in deinem Graph lesen.

Mit **Lesen und Bearbeiten** können sie auch Aufgaben oder E-Mail-Entwürfe hinzufügen und deinen Graph aktualisieren: Fakten speichern, Details, Felder und Tags korrigieren oder einer Personenübersicht eine Zeile hinzufügen.

Jede Änderung erscheint unter **Aktivität** mit **Rückgängig**. Die KIs führen niemals Datensätze zusammen, löschen sie oder geben sie weiter. Was sie speichern, ist mit **KI:** und ihrem Namen gekennzeichnet. Deine Machine behandelt es als Behauptung der KI, niemals als deine Anweisung.

Ein Entwurf bleibt liegen, bis du ihn selbst liest und auf **Senden** drückst. Eine verbundene KI sendet nichts und handelt nie in deinem Namen.

## Eine KI verbinden

Öffne **Einstellungen** und **Apps**. Unter **Die Apps von The Machine** findest du **In ChatGPT hinzufügen** und **In Claude hinzufügen**. Unter **Oder per Adresse hinzufügen** stehen die offizielle App-Adresse, die für jede Machine gleich ist, `https://mcp.themachine.computer/mcp`, und **Deine Adresse**, `https://<your name>.mcp.themachine.computer/mcp`. Beide haben eine Schaltfläche **Kopieren**.

Wenn deine Machine auf deinem eigenen Computer läuft, drücke zuerst unter **Adresse holen** auf **Einrichten**. Es öffnet sich eine Seite in deinem Konto: Prüfe, ob dort derselbe Code angezeigt wird, bestätige ihn und wähle einen Namen. Deine Machine wird automatisch gekoppelt, ohne Neustart. Das ist bei beiden Methoden nötig.

Anschließend richtet deine Machine ihre sichere Adresse selbst ein. Das dauert ein paar Minuten.

Für Claude drückst du auf **In Claude hinzufügen** oder öffnest [The Machine im Claude-Verzeichnis](https://claude.ai/directory/the-machine) und drückst dann auf **Verbinden**. Bei Team und Enterprise fügt ein Inhaber die App in den Organisationseinstellungen hinzu.

Wenn du stattdessen eine Adresse in Claude verwenden möchtest, öffne **Anpassen** und **Connectors**, drücke auf **+ Hinzufügen** und dann auf **Benutzerdefinierten Connector hinzufügen**. Gib als Namen The Machine ein, füge die Adresse ein, drücke auf **Weiter** und dann auf **Hinzufügen**.

Für ChatGPT drückst du auf **In ChatGPT hinzufügen** oder öffnest [The Machine in ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4) und drückst dann auf **Plugin installieren**. Bei Business und Enterprise muss ein Administrator die App möglicherweise zuerst freigeben.

Die offizielle App verbindet sich mit einer gehosteten Machine und mit einer Machine auf deinem eigenen Computer, sobald diese eine Adresse hat.

Für deine private Adresse oder eine Machine, die nicht im Network ist, fügst du stattdessen in ChatGPT einen benutzerdefinierten MCP-Server hinzu: Öffne chatgpt.com/plugins, drücke auf **+** und dann auf **Benutzerdefinierten MCP-Server hinzufügen**. Gib als Namen The Machine ein, füge die Adresse ein und wähle OAuth. Bestätige die Warnung und drücke auf **Als Plugin erstellen**. Dein Tarif oder Arbeitsbereich muss benutzerdefinierte MCP-Server zulassen.

Bei Verwendung der offiziellen App fordert dich die KI auf, dich mit deinem The Machine-Konto anzumelden. Wenn du mehrere Machines hast, wähle diese Machine aus und bestätige die Verbindung auf der eigenen Seite deiner Machine. Bei Verwendung der privaten Adresse verbindet sich die KI direkt mit deiner Machine.

KIs auf einem Gerät in deinem privaten Netzwerk (Tailscale), zum Beispiel Claude Code oder Cursor, können auch die Adresse deines Dashboards gefolgt von `/mcp` verwenden. Mit **Diese Machine trennen** unten unter **Einstellungen** und **Konto** entfernst du eine Machine auf deinem eigenen Computer wieder aus deinem Konto.

Deine Machine zeigt dir, welche KI eine Verbindung anfragt. Kann sie die KI nicht erkennen, zeigt sie, woher die Anfrage kommt. Verbinde sie nur, wenn du die Anfrage gerade selbst gestartet hast.

Wähle aus, was die KI darf: **Lesen** oder **Lesen und Bearbeiten**. Wenn du sowohl ein Work- als auch ein Personal-Konto hast, wählst du aus, worauf sie zugreifen darf. Wähle dann den Zeitraum: **1 Tag**, **7 Tage**, **30 Tage** oder **1 Jahr**. Drücke auf **Verbinden** oder auf **Abbrechen**, um die Anfrage abzulehnen, ohne etwas freizugeben.

## Offizielle App oder private Adresse

Die offizielle App ist der einfache Weg: eine Adresse für alle, und dein Konto findet deine Machine. Unsere Cloud leitet Anfragen weiter und speichert niemals deren Inhalt.

Bei deiner privaten Adresse ist alles durchgehend bis zu deiner Machine verschlüsselt. Die Cloud leitet die Anfragen nur weiter und kann sie nicht lesen.

In beiden Fällen entscheidet deine Machine. Nur eine KI, die du auf ihrer Seite genehmigt hast, erhält Zugriff, und zwar mit den von dir gewählten Berechtigungen. Unter **Einstellungen** und **Apps** wird bei einer KI, die über die offizielle App verbunden ist, **Offizielle App** angezeigt.

## Was die KI sehen kann

Eine Verbindung hat nur Zugriff auf ihren jeweiligen Bereich. Work umfasst Aufgaben und Versprechen deiner Arbeitskonten, Personen, Unternehmen und Projekte aus dem Arbeitsbereich sowie das Team-Briefing deiner Work Fleet. Personal umfasst alles andere. Nachrichtentexte bleiben auf deiner Machine, solange du **Nachrichten** nicht aktivierst. Ohne diese Option sieht eine KI bei den Quellen einer Aufgabe nur Absender, Betreff und Datum.

Datensätze von Teammitgliedern im Team Graph werden niemals an eine externe KI weitergegeben.

## Nachrichten

Mit **Nachrichten** kann eine KI deine E-Mails, Slack-Nachrichten, WhatsApp-Nachrichten und andere Chats durchsuchen und lesen. Die Option ist zunächst deaktiviert. Du kannst sie beim Verbinden oder später unter **Einstellungen** und **Apps** aktivieren. Die KI kann nur lesen: Sie sendet und löscht nichts und markiert auch nichts.

Sie liest nur Nachrichten aus ihrem jeweiligen Bereich. Bestimmte Nachrichten werden nie weitergegeben: Einmalcodes und Anmeldelinks, Nachrichten aus einem Board oder Projekt mit der Einstellung **Nur du**, Threads, die The Machine als vertraulich eingestuft hat (Geschäfte, Personal, Rechtliches, Gesundheit, Geld), Threads, die du privat gehalten hast, und gelöschte Nachrichten.

Jeder Lesezugriff wird unter **Aktivität** mit der Anzahl der Nachrichten und den betroffenen Threads angezeigt, niemals mit dem Nachrichtentext. Deine Machine übergibt den Text als Daten gekennzeichnet, damit die KI Anweisungen in Nachrichten nicht befolgen sollte.

Solange **Nachrichten** aktiviert ist, warten Änderungen am Graph durch eine KI mit **Lesen und Bearbeiten** auf deine Bestätigung. Drücke bei der Änderung unter **Aktivität** auf **Übernehmen** oder **Verwerfen**.

## In den Einstellungen

Öffne **Einstellungen** und **Apps**, um jede verbundene KI mit ihren Berechtigungen, ihrem Bereich, ihrem Ablaufdatum und ihrer letzten Nutzung zu sehen. **Nachrichten** kannst du direkt dort ein- und ausschalten. Drücke auf **Ändern**, um Berechtigungen, Bereich oder Gültigkeitsdauer anzupassen. Die Änderung gilt ab der nächsten Anfrage. Unter **Aktivität** werden alle Anfragen aufgeführt, auch abgelehnte. Mit **Jetzt ausschalten** pausierst du den Zugriff: Alle Anmeldungen werden beendet, der Verlauf bleibt erhalten. **Entfernen** löscht den Zugriff und den zugehörigen Verlauf.

Wenn du dich erneut bei derselben KI anmeldest, ersetzt die neue Genehmigung die vorherige.

Eine KI, die sich nicht selbst anmelden kann, kann einen Schlüssel verwenden. Gib unter **Schlüssel hinzufügen** einen Namen ein, wähle die Berechtigungen und Gültigkeitsdauer und drücke auf **Schlüssel erstellen**. Kopiere den Schlüssel sofort, denn er wird nur einmal angezeigt. Die KI sendet ihn als `Authorization: Bearer <key>`.

## Sicherheit

Jede Anfrage wird protokolliert, auch abgelehnte. Eine abgelaufene oder deaktivierte Verbindung wird abgelehnt, bis du sie änderst. Deine Machine speichert von jeder Anmeldung nur einen Fingerabdruck. Eine Kopie der Daten reicht daher nicht aus, um Zugriff zu erhalten.
