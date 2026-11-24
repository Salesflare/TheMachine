---
title: Andere KIs verbinden
area: connections
summary: Lass Claude, ChatGPT, Cursor, Codex oder GBrain deine Aufgaben und deinen Graph lesen. Mit „Lesen und Bearbeiten“ können sie Änderungen vornehmen, die du rückgängig machen kannst.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: cf0776c294917228
---
## Was eine andere KI tun kann

Claude, ChatGPT, Cursor, Codex, GBrain und andere KIs können sich mit deiner Machine verbinden. Sie können deine Aufgaben, Versprechen, Team-Briefings sowie die Personen und Unternehmen in deinem Graph lesen.

Mit **Lesen und Bearbeiten** können sie außerdem Aufgaben oder E-Mail-Entwürfe hinzufügen und deinen Graph aktualisieren: Fakten speichern, Details, Felder und Tags korrigieren oder einer Personen-Zusammenfassung einen Eintrag hinzufügen.

Jede Änderung wird unter **Aktivität** angezeigt und kann mit **Rückgängig** rückgängig gemacht werden. KIs können Datensätze nicht zusammenführen, löschen oder teilen. Was sie speichern, ist mit **AI:** und ihrem Namen gekennzeichnet. Deine Machine behandelt es als Behauptung der KI, niemals als deine Anweisung.

Ein Entwurf bleibt liegen, bis du ihn selbst liest und auf „Senden“ drückst. Eine verbundene KI sendet nichts und handelt nie in deinem Namen.

Ein Entwurf, in dem noch etwas ergänzt werden muss, der auf eine fehlende Datei verweist oder nur deine eigene Adresse als Empfänger enthält, wird zuerst zur Überarbeitung an die KI zurückgegeben. Fragt eine KI zweimal hintereinander nach derselben Aufgabe oder demselben Entwurf, bekommst du nur einen.

## Eine KI verbinden

Öffne **Einstellungen** und dann **Apps**. Unter **Die Apps von The Machine** findest du **In ChatGPT hinzufügen** und **In Claude hinzufügen**. Unter **Oder per Adresse hinzufügen** findest du die eine Adresse der offiziellen App für jede Machine, `https://mcp.themachine.computer/mcp`, und **Deine Adresse**, `https://<your name>.mcp.themachine.computer/mcp`. Beide haben eine Schaltfläche **Kopieren**.

Wenn deine Machine auf deinem eigenen Computer läuft, drücke zuerst unter **Adresse holen** auf **Einrichten**. Eine Seite in deinem Konto wird geöffnet. Prüfe, ob dort derselbe Code angezeigt wird, bestätige ihn und wähle einen Namen. Deine Machine wird automatisch gekoppelt, ohne Neustart. Das ist bei beiden Wegen nötig.

Danach richtet deine Machine ihre sichere Adresse automatisch ein. Das dauert ein paar Minuten.

Für Claude drückst du auf **In Claude hinzufügen** oder öffnest [The Machine im Claude-Verzeichnis](https://claude.ai/directory/the-machine) und drückst dann auf „Verbinden“. Bei Team- und Enterprise-Konten fügt ein Inhaber die App in den Organisationseinstellungen hinzu.

Wenn du stattdessen in Claude eine Adresse verwenden möchtest, öffne „Anpassen“ und dann „Connectors“, drücke auf „+ Hinzufügen“ und anschließend auf „Benutzerdefinierten Connector hinzufügen“. Nenne ihn The Machine, füge die Adresse ein, drücke auf „Weiter“ und dann auf „Hinzufügen“.

Für ChatGPT drückst du auf **In ChatGPT hinzufügen** oder öffnest [The Machine in ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4) und drückst dann auf „Plugin installieren“. Bei Business- und Enterprise-Konten muss ein Admin die App möglicherweise zuerst erlauben.

Die offizielle App verbindet sich mit einer gehosteten Machine und mit einer Machine auf deinem eigenen Computer, sobald diese ihre Adresse eingerichtet hat.

Für deine private Adresse oder eine Machine, die nicht im Network ist, kannst du stattdessen in ChatGPT einen benutzerdefinierten MCP-Server hinzufügen: Öffne chatgpt.com/plugins, drücke auf „+“ und dann auf „Benutzerdefinierten MCP-Server hinzufügen“. Nenne ihn The Machine, füge die Adresse ein und wähle OAuth. Bestätige den Hinweis und drücke auf „Als Plugin erstellen“. Dein Tarif oder Workspace muss benutzerdefinierte MCP-Server erlauben.

Bei der offiziellen App bittet dich die KI, dich mit deinem The Machine-Konto anzumelden. Wenn du mehrere Machines hast, wählst du die gewünschte aus und bestätigst sie auf der eigenen Seite deiner Machine. Mit der privaten Adresse verbindet sich die KI direkt mit deiner Machine.

KIs auf einem Gerät in deinem privaten Netzwerk (Tailscale), etwa Claude Code oder Cursor, können auch die Adresse deines Dashboards mit angehängtem `/mcp` verwenden. **Diese Machine trennen** findest du unten unter **Einstellungen** und **Konto**. Damit entfernst du eine Machine auf deinem eigenen Computer wieder aus deinem Konto.

Deine Machine zeigt an, welche KI die Anfrage stellt. Kann sie das nicht erkennen, zeigt sie, woher die Anfrage kommt. Verbinde sie nur, wenn du den Vorgang gerade selbst gestartet hast.

Wähle aus, was die KI tun darf: **Lesen** oder **Lesen und Bearbeiten**. Wenn du sowohl ein Work- als auch ein Personal-Konto hast, wählst du aus, worauf sie zugreifen darf. Lege dann fest, wie lange der Zugriff gelten soll: **1 Tag**, **7 Tage**, **30 Tage** oder **1 Jahr**. Drücke auf **Verbinden** oder auf **Abbrechen**, um die Anfrage abzulehnen.

## Offizielle App oder private Adresse

Die offizielle App ist der einfache Weg: eine Adresse für alle, und dein Konto findet deine Machine. Unsere Cloud leitet Anfragen weiter und speichert niemals, was darin steht.

Mit deiner privaten Adresse sind alle Daten Ende-zu-Ende bis zu deiner Machine verschlüsselt. Die Cloud leitet sie nur weiter und kann sie nicht lesen.

In beiden Fällen entscheidet deine Machine. Nur eine KI, die du auf ihrer Seite freigegeben hast, erhält Zugriff, und zwar mit den von dir ausgewählten Berechtigungen. In **Einstellungen** und **Apps** wird bei einer KI, die über die offizielle App verbunden ist, **Offizielle App** angezeigt.

## Was die KI sehen kann

Eine Verbindung hat nur Zugriff auf ihren jeweiligen Bereich. Work umfasst Aufgaben und Versprechen deiner Arbeitskonten, berufliche Kontakte, Unternehmen und Projekte sowie das Team-Briefing deiner Work Fleet. Personal umfasst alles andere. Nachrichtentexte bleiben auf deiner Machine, solange du **Nachrichten** nicht aktivierst. Ohne diese Option sieht eine KI bei den Quellen einer Aufgabe nur Absender, Betreff und Datum.

Datensätze von Teammitgliedern im Team Graph werden niemals an eine externe KI weitergegeben.

## Nachrichten

Mit **Nachrichten** kann eine KI deine E-Mails, Slack-, WhatsApp- und andere Chats durchsuchen und lesen. Die Funktion ist deaktiviert, bis du sie beim Verbinden oder später unter **Einstellungen** und **Apps** einschaltest. Die KI kann nur lesen. Sie kann nichts senden, löschen oder als gelesen markieren.

Die KI liest nur Nachrichten aus ihrem Bereich. Bestimmte Nachrichten werden nie weitergegeben: Einmalcodes und Anmeldelinks, Nachrichten in einem Board oder Projekt mit der Einstellung **Nur du**, von The Machine als sensibel eingestufte Unterhaltungen (Geschäfte, Personal, Rechtliches, Gesundheit, Geld), Unterhaltungen, die du privat gehalten hast, und gelöschte Nachrichten.

Jeder Lesezugriff wird unter **Aktivität** mit der Anzahl der Nachrichten und den jeweiligen Unterhaltungen angezeigt, aber niemals mit dem Nachrichtentext. Deine Machine übergibt den Text als Daten, damit die KI Anweisungen in einer Nachricht nicht befolgen sollte.

Solange „Nachrichten“ aktiviert ist, musst du Änderungen am Graph durch eine KI mit **Lesen und Bearbeiten** bestätigen. Drücke bei der Änderung unter **Aktivität** auf **Übernehmen** oder **Verwerfen**.

## In den Einstellungen

Öffne **Einstellungen** und dann **Apps**, um alle KIs zu sehen, die sich einmal verbunden haben. Dort findest du ihre Berechtigungen, ihren Bereich, das Ablaufdatum und die letzte Verwendung. **Nachrichten** kannst du dort ein- und ausschalten. Drücke auf **Ändern**, um die Berechtigungen, den Bereich oder die Gültigkeitsdauer anzupassen. Die Änderung gilt für den nächsten Aufruf. Unter **Aktivität** werden alle Aufrufe aufgeführt, auch abgelehnte. **Jetzt ausschalten** pausiert den Zugriff und beendet alle Anmeldungen. Der Verlauf bleibt erhalten. Mit **Entfernen** entfernst du die KI samt Verlauf.

Wenn du dich erneut bei derselben KI anmeldest, ersetzt die neue Freigabe die vorherige.

Eine KI, die sich nicht selbst anmelden kann, kann einen Schlüssel verwenden. Gib ihm unter **Schlüssel hinzufügen** einen Namen, wähle die Berechtigungen und die Gültigkeitsdauer aus und drücke auf **Schlüssel erstellen**. Kopiere den Schlüssel sofort, denn er wird nur einmal angezeigt. Die KI sendet ihn als `Authorization: Bearer <key>`.

## Sicherheit

Jeder Aufruf wird protokolliert, auch abgelehnte. Verbindungen, die abgelaufen oder ausgeschaltet sind, werden abgelehnt, bis du sie änderst. Deine Machine speichert von jeder Anmeldung nur einen Fingerabdruck. Eine Kopie der Daten reicht daher nicht aus, um Zugriff zu erhalten.
