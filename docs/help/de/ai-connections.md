---
title: Andere KI-Systeme verbinden
area: connections
summary: Lass Claude, ChatGPT, Cursor, Codex oder GBrain deine Aufgaben und deinen Graph lesen. Mit „Lesen und Bearbeiten“ können sie Änderungen vornehmen, die du rückgängig machen kannst.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: 7681c632f712e93c
---
## Was andere KI-Systeme tun können

Claude, ChatGPT, Cursor, Codex, GBrain und andere KI-Systeme können sich mit deiner Machine verbinden. Sie können deine Aufgaben, Versprechen, Team-Briefings sowie die Personen und Unternehmen in deinem Graph lesen.

Mit **Lesen und Bearbeiten** können sie auch eine Aufgabe oder einen E-Mail-Entwurf hinzufügen und deinen Graph aktualisieren: eine Erkenntnis speichern, Details, Felder und Tags korrigieren oder eine Zeile zur Zusammenfassung einer Person hinzufügen.

Jede Änderung wird unter **Aktivität** angezeigt und kann mit **Rückgängig** rückgängig gemacht werden. Die KI-Systeme führen niemals Datensätze zusammen, löschen oder teilen sie. Gespeicherte Inhalte sind mit **KI:** und dem Namen der KI gekennzeichnet. Deine Machine behandelt diese Inhalte als Aussagen der KI, niemals als deine Anweisung.

Ein Entwurf bleibt liegen, bis du ihn selbst liest und auf „Senden“ drückst. Eine verbundene KI sendet nichts und handelt nie in deinem Namen.

## Was sie von dir lernt

Wenn ein Chat beginnt, erhält die KI eine kurze Zusammenfassung: wer du bist, deine wichtigsten Regeln und was sich seit dem letzten Besuch geändert hat. Außerdem kann sie lesen, was unter **Lernen** steht: deine Regeln, allgemeine Fakten und wie du in den einzelnen Kanälen schreibst. So schreibt sie wie du.

Mit **Lesen und Bearbeiten** kann die KI speichern, was ihr im Chat festlegt. Eine Tatsache wird sofort gespeichert und kann unter **Aktivität** mit **Rückgängig** rückgängig gemacht werden. Eine Regel steuert die Arbeit deiner Machine und bleibt deshalb unter **Lernen**, bis du auf **Freigeben** oder **Verwerfen** drückst. Sie ändert niemals, wie du schreibst.

Ein Entwurf, in dem noch etwas fehlt, der eine nicht vorhandene Datei erwähnt oder nur deine eigene Adresse enthält, geht zuerst zurück an die KI, damit sie ihn korrigiert. Wenn eine KI zweimal hintereinander dieselbe Aufgabe oder denselben Entwurf anfordert, bekommst du nur einen davon.

## Eine KI verbinden

Öffne **Einstellungen** und dann **Apps**. Unter **Die Apps von The Machine** findest du **In ChatGPT hinzufügen** und **In Claude hinzufügen**. Unter **Oder per Adresse hinzufügen** findest du die eine Adresse der offiziellen App für jede Machine, `https://mcp.themachine.computer/mcp`, und **Deine Adresse**, `https://<your name>.mcp.themachine.computer/mcp`, jeweils mit **Kopieren**.

Bei einer Machine auf deinem eigenen Computer drückst du zuerst unter **Adresse holen** auf **Einrichten**. Eine Seite in deinem Konto wird geöffnet. Prüfe, ob dort derselbe Code angezeigt wird, bestätige und wähle einen Namen. Deine Machine wird automatisch gekoppelt, ohne Neustart. Beides ist erforderlich.

Deine Machine richtet dann selbstständig ihre sichere Adresse ein. Das dauert einige Minuten.

Für Claude drückst du auf **In Claude hinzufügen** oder öffnest [The Machine im Claude-Verzeichnis](https://claude.ai/directory/the-machine) und drückst dann auf „Verbinden“. Bei Team- und Enterprise-Konten fügt ein Inhaber sie in den Organisationseinstellungen hinzu.

Der Skill von The Machine erklärt Claude, wann es deine Machine verwenden soll: zuerst die Zusammenfassung, dann deine Regeln und deinen Schreibstil, bevor Claude etwas entwirft. Drücke neben **Claude-Skill** auf **Herunterladen**. Öffne dann in Claude „Anpassen“ und „Skills“ und lade den Skill hoch.

Du kannst stattdessen auch eine Adresse in Claude verwenden. Öffne dazu „Anpassen“ und „Connectors“, drücke auf „+ Hinzufügen“ und dann auf „Benutzerdefinierten Connector hinzufügen“. Nenne ihn The Machine, füge die Adresse ein, drücke auf „Weiter“ und dann auf „Hinzufügen“.

Für ChatGPT drückst du auf **In ChatGPT hinzufügen** oder öffnest [The Machine in ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4) und drückst dann auf „Plugin installieren“. Bei Business- und Enterprise-Konten muss ein Administrator die App möglicherweise zuerst erlauben.

Die offizielle App verbindet sich mit einer gehosteten Machine und auch mit einer Machine auf deinem eigenen Computer, sobald diese ihre Adresse eingerichtet hat.

Für deine private Adresse oder eine Machine, die nicht im Network ist, kannst du stattdessen in ChatGPT einen benutzerdefinierten MCP-Server hinzufügen: Öffne chatgpt.com/plugins, drücke auf „+“ und dann auf „Benutzerdefinierten MCP-Server hinzufügen“. Nenne ihn The Machine, füge die Adresse ein und wähle OAuth. Bestätige die Warnung und drücke auf „Als Plugin erstellen“. Dein Tarif oder Workspace muss benutzerdefinierte MCP-Server zulassen.

Bei der offiziellen App fordert die KI dich auf, dich mit deinem Konto bei The Machine anzumelden. Wenn du mehr als eine Machine hast, wähle diese Machine aus und bestätige sie dann auf der eigenen Seite deiner Machine. Mit der privaten Adresse verbindet sich die KI direkt mit deiner Machine.

KI-Systeme auf einem Gerät in deinem privaten Netzwerk (Tailscale), etwa Claude Code oder Cursor, können auch die Adresse deines Dashboards verwenden, gefolgt von `/mcp`. Mit **Diese Machine trennen** am Ende von **Einstellungen** und **Konto** entfernst du eine Machine auf deinem eigenen Computer wieder aus deinem Konto.

Deine Machine zeigt dir, welche KI anfragt. Wenn sie das nicht erkennen kann, zeigt sie dir, woher die Anfrage kommt. Verbinde sie nur, wenn du gerade selbst damit begonnen hast.

Wähle aus, was die KI tun darf: **Lesen** oder **Lesen und Bearbeiten**. Wenn du sowohl ein Work- als auch ein Personal-Konto hast, wähle aus, worauf sie zugreifen darf. Lege dann fest, wie lange der Zugriff gelten soll: **1 Tag**, **7 Tage**, **30 Tage** oder **1 Jahr**. Drücke auf **Verbinden** oder auf **Abbrechen**, um die Anfrage abzulehnen.

## Offizielle App oder private Adresse

Die offizielle App ist der einfache Weg: eine Adresse für alle, und dein Konto findet deine Machine. Unsere Cloud leitet Anfragen weiter und speichert niemals deren Inhalt.

Mit deiner privaten Adresse ist alles durchgehend bis zu deiner Machine verschlüsselt. Die Cloud leitet die Inhalte nur weiter und kann sie nicht lesen.

In beiden Fällen entscheidet deine Machine. Nur eine KI, die du auf ihrer Seite freigegeben hast, erhält Zugriff, und zwar mit den von dir gewählten Berechtigungen. Unter **Einstellungen** und **Apps** wird bei einer KI, die über die offizielle App verbunden ist, **Offizielle App** angezeigt.

## Was die KI sehen kann

Eine Verbindung sieht nur ihren jeweiligen Bereich. „Work“ umfasst Aufgaben und Versprechen deiner Arbeitskonten, Kontakte, Unternehmen und Projekte aus dem Arbeitsbereich sowie das Team-Briefing deines Work Fleet. „Personal“ umfasst alles andere. Nachrichtentexte bleiben auf deiner Machine, sofern du **Nachrichten** nicht aktivierst. Ohne diese Option sieht eine KI bei den Quellen einer Aufgabe nur Absender, Betreff und Datum.

Datensätze deiner Teammitglieder im Team Graph werden niemals an externe KI-Systeme weitergegeben.

## Nachrichten

Mit **Nachrichten** kann eine KI deine E-Mails, Slack-, WhatsApp- und andere Chats durchsuchen und lesen. Die Funktion ist zunächst ausgeschaltet. Du kannst sie beim Verbinden oder später unter **Einstellungen** und **Apps** einschalten. Die KI kann nur lesen: Sie sendet und löscht nichts und markiert auch nichts.

Sie liest nur Nachrichten aus ihrem jeweiligen Bereich. Manche Nachrichten werden niemals weitergegeben: Einmalcodes und Anmeldelinks, Nachrichten aus einem Board oder Projekt mit der Einstellung **Nur du**, Unterhaltungen, die The Machine als sensibel eingestuft hat (Geschäfte, Personal, Rechtliches, Gesundheit, Geld), Unterhaltungen, die du privat gehalten hast, und gelöschte Nachrichten.

Jeder Lesezugriff wird unter **Aktivität** angezeigt, mit der Anzahl der Nachrichten und den jeweiligen Unterhaltungen, aber niemals mit dem Nachrichtentext. Deine Machine übergibt den Text als Daten gekennzeichnet, damit die KI Anweisungen in Nachrichten nicht befolgt.

Solange „Nachrichten“ eingeschaltet ist, müssen Änderungen am Graph, die eine KI mit **Lesen und Bearbeiten** vornimmt, von dir bestätigt werden. Drücke bei der Änderung unter **Aktivität** auf **Übernehmen** oder **Verwerfen**.

## In den Einstellungen

Öffne **Einstellungen** und dann **Apps**, um alle KI-Systeme zu sehen, die sich verbunden haben. Jedes wird einmal mit seinen Berechtigungen, seinem Bereich, Ablaufdatum und letzter Nutzung angezeigt. Dort kannst du **Nachrichten** ein- und ausschalten. Drücke auf **Ändern**, um die Berechtigungen, den Bereich oder die Dauer zu ändern. Die Änderung gilt beim nächsten Zugriff. Unter **Aktivität** werden alle Zugriffe aufgeführt, auch abgelehnte. **Jetzt ausschalten** setzt den Zugriff aus: Alle Anmeldungen werden beendet, der Verlauf bleibt erhalten. Mit **Entfernen** entfernst du die Verbindung samt Verlauf.

Wenn du dich erneut bei derselben KI anmeldest, ersetzt die neue Freigabe die vorherige. Wo du bei dieser KI bereits angemeldet bist, bleibt die Verbindung mit den neuen Berechtigungen bestehen. Eine KI, die du verwendest, bleibt bis zum Ablaufdatum angemeldet. Wenn du eine KI 90 Tage lang nicht verwendest, musst du dich erneut anmelden.

Eine KI, die sich nicht selbst anmelden kann, kann einen Schlüssel verwenden. Gib unter **Schlüssel hinzufügen** einen Namen ein, wähle die Berechtigungen und die Dauer aus und drücke auf **Schlüssel erstellen**. Kopiere den Schlüssel sofort: Er wird nur einmal angezeigt. Die KI sendet ihn als `Authorization: Bearer <key>`.

## Sicherheit

Jeder Zugriff wird protokolliert, auch abgelehnte Zugriffe. Eine abgelaufene oder ausgeschaltete Verbindung wird abgelehnt, bis du sie änderst. Deine Machine speichert nur einen Fingerabdruck für jede Anmeldung. Eine Kopie ihrer Daten reicht also nicht aus, um etwas zu öffnen.
