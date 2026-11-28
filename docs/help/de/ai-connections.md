---
title: Andere KIs verbinden
area: connections
summary: Lass Claude, ChatGPT, Cursor, Codex oder GBrain deine Aufgaben und deinen Graph lesen. Mit „Lesen und Bearbeiten“ können sie auch Änderungen vornehmen, die du rückgängig machen kannst.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: 3a7200b2a076c274
---
## Was andere KIs tun können

Claude, ChatGPT, Cursor, Codex, GBrain und andere KIs können sich mit deiner Machine verbinden. Sie können deine Aufgaben, Versprechen, Team-Briefings und die Personen und Unternehmen in deinem Graph lesen.

Mit „**Lesen und Bearbeiten**“ können sie auch eine Aufgabe oder einen E-Mail-Entwurf hinzufügen und deinen Graph aktualisieren: eine Tatsache speichern, Angaben, Felder und Tags korrigieren oder eine Zeile zur Zusammenfassung einer Person hinzufügen.

Jede Änderung erscheint unter „**Aktivität**“ und lässt sich mit „**Rückgängig**“ rückgängig machen. Sie führen niemals Datensätze zusammen, löschen oder teilen sie. Gespeicherte Angaben sind mit „**AI:**“ und ihrem Namen gekennzeichnet. Deine Machine behandelt sie als Behauptung der KI, niemals als deine Anweisung.

Ein Entwurf bleibt liegen, bis du ihn selbst gelesen und auf „Senden“ gedrückt hast. Eine verbundene KI sendet nichts und handelt niemals in deinem Namen.

## Was sie von dir lernt

Wenn ein Chat beginnt, erhält die KI ein kurzes Briefing: wer du bist, deine wichtigsten Regeln und was sich seit ihrem letzten Besuch geändert hat. Sie kann auch lesen, was unter „**Lernen**“ steht: deine Regeln, allgemeine Fakten und wie du in den einzelnen Kanälen schreibst. So schreibt sie wie du.

Mit „**Lesen und Bearbeiten**“ kann sie speichern, was ihr im Chat vereinbart. Eine Tatsache wird sofort gespeichert und lässt sich unter „**Aktivität**“ mit „**Rückgängig**“ rückgängig machen. Eine Regel beeinflusst die Arbeit deiner Machine und wartet deshalb unter „**Lernen**“, bis du auf „**Freigeben**“ oder „**Verwerfen**“ drückst. Sie ändert niemals, wie du schreibst.

Ein Entwurf, bei dem noch etwas fehlt, eine erwähnte Datei, auf die die KI keinen Zugriff hat, oder ein Entwurf, auf dem nur deine eigene Adresse steht, geht zuerst zurück an die KI, damit sie ihn korrigiert. Fragt eine KI zweimal hintereinander nach derselben Aufgabe oder demselben Entwurf, erhältst du nur einen davon.

## Eine KI verbinden

Öffne „**Einstellungen**“ und dann „**Apps**“. Unter „**Die Apps von The Machine**“ findest du „**In ChatGPT hinzufügen**“ und „**In Claude hinzufügen**“. Unter „**Oder per Adresse hinzufügen**“ findest du die offizielle App-Adresse für alle Machines, `https://mcp.themachine.computer/mcp`, und „**Deine Adresse**“, `https://<your name>.mcp.themachine.computer/mcp`. Für beide gibt es die Schaltfläche „**Kopieren**“.

Wenn deine Machine auf deinem eigenen Computer läuft, drücke zuerst unter „**Adresse holen**“ auf „**Einrichten**“. Eine Seite in deinem Konto wird geöffnet. Prüfe, ob dort derselbe Code angezeigt wird, bestätige ihn und wähle einen Namen. Deine Machine wird automatisch gekoppelt, ohne Neustart. Beides ist erforderlich.

Anschließend richtet deine Machine ihre sichere Adresse selbst ein. Das dauert ein paar Minuten.

Für Claude drückst du auf „**In Claude hinzufügen**“ oder öffnest [The Machine im Claude-Verzeichnis](https://claude.ai/directory/the-machine) und drückst dann auf „Verbinden“. Bei Team- und Enterprise-Konten fügt ein Inhaber die App in den Organisationseinstellungen hinzu.

Der Skill von The Machine teilt Claude mit, wann es deine Machine verwenden soll: zuerst das Briefing, dann deine Regeln und deinen Schreibstil, bevor Claude etwas entwirft. Drücke neben „**Claude-Skill**“ auf „**Herunterladen**“. Öffne dann in Claude „Customize“ und „Skills“ und lade den Skill hoch.

Wenn du stattdessen in Claude eine Adresse verwenden möchtest, öffne „Customize“ und „Connectors“, drücke auf „+ Add“ und dann auf „Add custom connector“. Nenne den Connector The Machine, füge die Adresse ein, drücke auf „Continue“ und dann auf „Add“.

Für ChatGPT drückst du auf „**In ChatGPT hinzufügen**“ oder öffnest [The Machine in ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4) und drückst dann auf „Install plugin“. Bei Business- und Enterprise-Konten muss ein Administrator die App möglicherweise zuerst zulassen.

Die offizielle App verbindet sich mit einer gehosteten Machine und mit einer Machine auf deinem eigenen Computer, sobald diese ihre Adresse eingerichtet hat.

Für deine private Adresse oder eine Machine, die nicht im Network ist, kannst du stattdessen in ChatGPT einen benutzerdefinierten MCP-Server hinzufügen: Öffne chatgpt.com/plugins, drücke auf „+“ und dann auf „Add custom MCP server“. Nenne ihn The Machine, füge die Adresse ein und wähle OAuth. Bestätige den Warnhinweis und drücke auf „Create as a plugin“. Dein Tarif oder Arbeitsbereich muss benutzerdefinierte MCP-Server erlauben.

Bei Verwendung der offiziellen App fordert die KI dich auf, dich mit deinem The Machine-Konto anzumelden. Wenn du mehrere Machines hast, wähle diese Machine aus und bestätige die Verbindung auf der eigenen Seite deiner Machine. Mit der privaten Adresse verbindet sich die KI direkt mit deiner Machine.

KIs auf einem Gerät in deinem privaten Netzwerk (Tailscale), zum Beispiel Claude Code oder Cursor, können auch die Adresse deines Dashboards gefolgt von `/mcp` verwenden. Mit „**Diese Machine trennen**“ ganz unten unter „**Einstellungen**“ und „**Konto**“ entfernst du eine Machine auf deinem eigenen Computer wieder aus deinem Konto.

Deine Machine zeigt dir, welche KI eine Verbindung anfragt. Wenn sie das nicht feststellen kann, zeigt sie dir, woher die Anfrage kommt. Verbinde sie nur, wenn du den Vorgang gerade selbst gestartet hast.

Wähle aus, was die KI tun darf: „**Lesen**“ oder „**Lesen und Bearbeiten**“. Wenn du ein Work- und ein Personal-Konto hast, wählst du aus, worauf sie zugreifen darf. Wähle dann aus, wie lange der Zugriff gelten soll: „**1 Tag**“, „**7 Tage**“, „**30 Tage**“ oder „**1 Jahr**“. Drücke auf „**Verbinden**“ oder auf „**Abbrechen**“, um die KI ohne Zugriff zurückzuschicken.

## Offizielle App oder private Adresse

Die offizielle App ist der einfache Weg: eine Adresse für alle, und dein Konto findet deine Machine. Unsere Cloud leitet Anfragen weiter und speichert niemals, was darin steht.

Mit deiner privaten Adresse ist alles bis zu deiner Machine durchgehend verschlüsselt. Die Cloud leitet die Anfragen nur weiter und kann sie nicht lesen.

In beiden Fällen entscheidet deine Machine. Nur eine KI, die du auf der Seite deiner Machine freigegeben hast, erhält Zugriff, und zwar nur auf das, was du ausgewählt hast. Unter „**Einstellungen**“ und „**Apps**“ ist bei einer KI, die über die offizielle App verbunden ist, „**Offizielle App**“ angegeben.

## Was sie sehen kann

Eine Verbindung sieht nur ihren jeweiligen Bereich. „Work“ umfasst Aufgaben und Versprechen deiner Work-Konten, Personen und Unternehmen aus dem Arbeitsbereich, Projekte und das Team-Briefing deiner Work Fleet. „Personal“ umfasst alles andere. Nachrichtentexte bleiben auf deiner Machine, solange du „**Nachrichten**“ nicht aktivierst. Ohne diese Option sieht eine KI bei den Quellen einer Aufgabe nur Absender, Betreff und Datum.

Datensätze von Teammitgliedern aus dem Team Graph werden niemals an externe KIs weitergegeben.

## Nachrichten

Mit „**Nachrichten**“ kann eine KI deine E-Mails, Slack-, WhatsApp- und andere Chats durchsuchen und lesen. Die Option ist zunächst ausgeschaltet. Du kannst sie auf der Seite aktivieren, auf der du die Verbindung einrichtest, oder später unter „**Einstellungen**“ und „**Apps**“. Die KI kann nur lesen. Sie sendet nichts, löscht nichts und markiert nichts.

Sie liest nur Nachrichten aus ihrem Bereich. Bestimmte Inhalte werden niemals weitergegeben: Einmalcodes und Anmeldelinks, Nachrichten auf einem Board oder in einem Projekt mit der Einstellung „**Nur du**“, Threads, die The Machine als sensibel einstuft (Geschäfte, Personal, Rechtliches, Gesundheit, Geld), Threads, die du privat gehalten hast, und gelöschte Nachrichten.

Jeder Lesezugriff erscheint unter „**Aktivität**“ mit der Anzahl der Nachrichten und den jeweiligen Threads, aber niemals mit dem Nachrichtentext. Deine Machine übergibt den Text als Daten an die KI. Die KI sollte daher keine Anweisungen befolgen, die in einer Nachricht stehen.

Solange „**Nachrichten**“ aktiviert ist, warten Änderungen am Graph durch eine KI mit „**Lesen und Bearbeiten**“ auf deine Bestätigung. Drücke bei der Änderung unter „**Aktivität**“ auf „**Übernehmen**“ oder „**Verwerfen**“.

## Termine

Mit „**Termine**“ kann eine KI wie ChatGPT selbstständig starten, wenn etwas passiert, zum Beispiel wenn eine neue Aufgabe hinzukommt, ein Briefing für ein morgiges Meeting ansteht oder ein Versprechen morgen fällig ist. Jeder Termin ist zunächst ausgeschaltet. Du kannst ihn unter „**Ändern**“ aktivieren. Die KI erhält dann den Titel und eine kurze Begründung. Sie bekommt keine Informationen, die sie nicht bereits lesen konnte, und niemals Informationen von vorher.

Die KI kann weiterhin nichts senden. Ihre Änderungen erscheinen unter „**Aktivität**“ und lassen sich mit „**Rückgängig**“ rückgängig machen. Wenn du einen Termin oder die KI ausschaltest, wird sie sofort gestoppt.

## In den Einstellungen

Öffne „**Einstellungen**“ und dann „**Apps**“, um alle verbundenen KIs samt Zugriff, Bereich, Ablaufdatum und letzter Verwendung zu sehen. Dort kannst du auch „**Nachrichten**“ ein- und ausschalten. Drücke auf „**Ändern**“, um den Zugriff, den Bereich oder die Laufzeit anzupassen. Die nächste Anfrage verwendet die neuen Einstellungen. Unter „**Aktivität**“ werden alle Anfragen aufgeführt, auch abgelehnte. Mit „**Jetzt ausschalten**“ pausierst du den Zugriff: Alle Anmeldungen werden beendet, der Verlauf bleibt erhalten. Mit „**Entfernen**“ löschst du die Verbindung mitsamt ihrem Verlauf.

Wenn du dich erneut bei derselben KI anmeldest, ersetzt die neue Freigabe die vorherige. Wenn du bei dieser KI bereits angemeldet bist, bleibt sie mit dem neuen Zugriff verbunden. Eine KI, die du verwendest, bleibt bis zum Ablaufdatum angemeldet. Eine KI, die du 90 Tage lang nicht verwendet hast, fordert dich zur erneuten Anmeldung auf.

Eine KI, die sich nicht selbst anmelden kann, kann einen Schlüssel verwenden. Gib unter „**Schlüssel hinzufügen**“ einen Namen ein, wähle den Zugriff und die Laufzeit und drücke auf „**Schlüssel erstellen**“. Kopiere den Schlüssel sofort, denn er wird nur einmal angezeigt. Die KI sendet ihn als `Authorization: Bearer <key>`.

## Sicher bleiben

Jede Anfrage wird protokolliert, auch abgelehnte. Anfragen von einer abgelaufenen oder ausgeschalteten Verbindung werden abgelehnt, bis du die Verbindung änderst. Deine Machine speichert nur einen Fingerabdruck für jede Anmeldung. Eine Kopie ihrer Daten reicht daher nicht aus, um etwas zu öffnen.
