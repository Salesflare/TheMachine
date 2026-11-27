---
title: Andere KIs verbinden
area: connections
summary: Lass Claude, ChatGPT, Cursor, Codex oder GBrain deine Aufgaben und deinen Graph lesen. Mit „Lesen und Bearbeiten“ können sie Änderungen vornehmen, die du rückgängig machen kannst.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: acdce4a5793f7c67
---
## Was eine andere KI tun kann

Claude, ChatGPT, Cursor, Codex, GBrain und andere KIs können sich mit deiner Machine verbinden. Sie können deine Aufgaben, Versprechen, Team-Briefings sowie die Personen und Unternehmen in deinem Graph lesen.

Mit **Lesen und Bearbeiten** können sie auch eine Aufgabe oder einen E-Mail-Entwurf hinzufügen und deinen Graph aktualisieren: Fakten speichern, Details, Felder und Tags korrigieren oder der Zusammenfassung einer Person eine Zeile hinzufügen.

Jede Änderung wird unter **Aktivität** angezeigt und kann mit **Rückgängig** rückgängig gemacht werden. Die KIs führen Datensätze nie zusammen, löschen sie nicht und geben sie nicht weiter. Gespeicherte Inhalte sind mit **AI:** und dem Namen der KI gekennzeichnet. Deine Machine behandelt sie als Aussage der KI, niemals als deine Anweisung.

Ein Entwurf bleibt liegen, bis du ihn liest und selbst auf **Senden** drückst. Eine verbundene KI sendet nichts und handelt nie in deinem Namen.

Ein Entwurf, in dem noch etwas ausgefüllt werden muss, der auf eine fehlende Datei verweist oder nur deine eigene Adresse enthält, wird zur Überarbeitung an die KI zurückgegeben. Fragt eine KI zweimal hintereinander nach derselben Aufgabe oder demselben Entwurf, erhältst du nur einen davon.

## Eine KI verbinden

Öffne **Einstellungen** und dann **Apps**. Unter **Die Apps von The Machine** findest du **In ChatGPT hinzufügen** und **In Claude hinzufügen**. Unter **Oder per Adresse hinzufügen** findest du die offizielle App-Adresse für jede Machine, `https://mcp.themachine.computer/mcp`, und **Deine Adresse**, `https://<your name>.mcp.themachine.computer/mcp`, jeweils mit **Kopieren**.

Wenn deine Machine auf deinem eigenen Computer läuft, drücke zuerst unter **Adresse holen** auf **Einrichten**. Eine Seite in deinem Konto wird geöffnet. Prüfe, ob dort derselbe Code angezeigt wird, bestätige ihn und wähle einen Namen. Deine Machine wird automatisch gekoppelt, ohne dass du sie neu starten musst. Das ist bei beiden Methoden nötig.

Danach richtet deine Machine ihre sichere Adresse selbst ein. Das dauert ein paar Minuten.

Für Claude drückst du auf **In Claude hinzufügen** oder öffnest [The Machine im Claude-Verzeichnis](https://claude.ai/directory/the-machine) und drückst dann auf **Verbinden**. Bei Team und Enterprise fügt ein Inhaber die App in den Organisationseinstellungen hinzu.

Wenn du stattdessen eine Adresse in Claude verwenden möchtest, öffne „Anpassen“ und dann „Connectors“, drücke auf „+ Hinzufügen“ und anschließend auf „Benutzerdefinierten Connector hinzufügen“. Nenne ihn The Machine, füge die Adresse ein, drücke auf „Weiter“ und dann auf „Hinzufügen“.

Für ChatGPT drückst du auf **In ChatGPT hinzufügen** oder öffnest [The Machine in ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4) und drückst dann auf „Plugin installieren“. Bei Business und Enterprise muss ein Administrator die App möglicherweise zuerst zulassen.

Die offizielle App verbindet sich mit einer gehosteten Machine und, sobald sie eine Adresse hat, auch mit einer Machine auf deinem eigenen Computer.

Für deine private Adresse oder eine Machine, die nicht im Network ist, kannst du stattdessen in ChatGPT einen benutzerdefinierten MCP-Server hinzufügen: Öffne chatgpt.com/plugins, drücke auf „+“ und dann auf „Benutzerdefinierten MCP-Server hinzufügen“. Nenne ihn The Machine, füge die Adresse ein und wähle OAuth. Bestätige die Warnung und drücke auf „Als Plugin erstellen“. Dein Tarif oder Workspace muss benutzerdefinierte MCP-Server zulassen.

Bei Verwendung der offiziellen App fordert dich die KI auf, dich mit deinem The Machine-Konto anzumelden. Wenn du mehrere Machines hast, wähle diese Machine aus und bestätige die Verbindung auf der Seite deiner Machine. Mit der privaten Adresse verbindet sich die KI direkt mit deiner Machine.

KIs auf einem Gerät in deinem privaten Netzwerk (Tailscale), etwa Claude Code oder Cursor, können auch die Adresse deines Dashboards gefolgt von `/mcp` verwenden. Mit **Diese Machine trennen** ganz unten unter **Einstellungen** und **Konto** entfernst du eine Machine auf deinem eigenen Computer wieder aus deinem Konto.

Deine Machine zeigt dir, welche KI anfragt. Kann sie das nicht erkennen, zeigt sie dir, woher die Anfrage kommt. Verbinde sie nur, wenn du die Verbindung gerade selbst gestartet hast.

Wähle aus, was die KI tun darf: **Lesen** oder **Lesen und Bearbeiten**. Wenn du Work- und Personal-Konten hast, wähle aus, was die KI sehen darf. Lege dann fest, wie lange der Zugriff gilt: **1 Tag**, **7 Tage**, **30 Tage** oder **1 Jahr**. Drücke auf **Verbinden** oder auf **Abbrechen**, um die Anfrage abzulehnen.

## Offizielle App oder private Adresse

Die offizielle App ist die einfache Lösung: eine Adresse für alle, und dein Konto findet deine Machine. Unsere Cloud leitet Anfragen weiter und speichert nie, was sie enthalten.

Mit deiner privaten Adresse ist alles durchgehend bis zu deiner Machine verschlüsselt. Die Cloud leitet die Anfragen nur weiter und kann sie nicht lesen.

In beiden Fällen entscheidet deine Machine. Zugriff erhält nur eine KI, die du auf der Seite deiner Machine genehmigt hast, und auch nur mit den Berechtigungen, die du ausgewählt hast. Unter **Einstellungen** und **Apps** wird bei einer KI, die über die offizielle App verbunden ist, **Offizielle App** angezeigt.

## Was die KI sehen kann

Eine Verbindung sieht nur ihren Bereich. Work umfasst Aufgaben und Versprechen deiner Arbeitskonten, Personen aus dem Arbeitsumfeld, Unternehmen, Projekte und das Team-Briefing deiner Work Fleet. Personal umfasst alles andere. Nachrichtentexte bleiben auf deiner Machine, solange du **Nachrichten** nicht aktivierst. Ohne diese Einstellung sieht eine KI bei den Quellen einer Aufgabe nur Absender, Betreff und Datum.

Datensätze aus dem Team Graph deiner Teammitglieder werden nie an eine externe KI weitergegeben.

## Nachrichten

Mit **Nachrichten** kann eine KI deine E-Mails, Slack-, WhatsApp- und andere Chats durchsuchen und lesen. Die Funktion ist ausgeschaltet, bis du sie auf der Verbindungsseite oder später unter **Einstellungen** und **Apps** aktivierst. Die KI kann nur lesen. Sie sendet nichts, löscht nichts und markiert nichts.

Die KI liest nur Nachrichten aus ihrem Bereich. Bestimmte Nachrichten werden nie weitergegeben: Einmalcodes und Anmeldelinks, Nachrichten auf einem Board oder in einem Projekt mit der Einstellung **Nur du**, Threads, die The Machine als sensibel eingestuft hat (Geschäfte, Personalwesen, Rechtliches, Gesundheit, Geld), Threads, die du privat gehalten hast, und gelöschte Nachrichten.

Jeder Lesezugriff wird in der **Aktivität** der KI angezeigt, einschließlich der Anzahl der Nachrichten und der betroffenen Threads, aber nie mit deren Text. Deine Machine übergibt den Text als Daten, damit die KI Anweisungen in einer Nachricht nicht befolgt.

Solange Nachrichten aktiviert sind, musst du Änderungen am Graph einer KI mit **Lesen und Bearbeiten** bestätigen. Drücke bei der Änderung unter **Aktivität** auf **Übernehmen** oder **Verwerfen**.

## In den Einstellungen

Öffne **Einstellungen** und **Apps**, um alle KIs zu sehen, die sich verbunden haben. Bei jeder KI werden ihre Berechtigungen, ihr Bereich, ihr Ablaufdatum und ihre letzte Nutzung angezeigt. Über **Nachrichten** kannst du die Funktion direkt dort ein- und ausschalten. Drücke auf **Ändern**, um ihre Berechtigungen, ihren Bereich oder die Dauer des Zugriffs zu ändern. Die nächste Anfrage verwendet dann die neuen Einstellungen. Unter **Aktivität** werden alle Anfragen aufgeführt, auch abgelehnte. Mit **Jetzt ausschalten** pausierst du den Zugriff: Alle Anmeldungen werden beendet, der Verlauf bleibt erhalten. Mit **Entfernen** entfernst du die KI samt Verlauf.

Wenn du dich erneut bei derselben KI anmeldest, ersetzt die neue Freigabe die vorherige. Wo du bei dieser KI bereits angemeldet bist, bleibt die Verbindung mit den neuen Berechtigungen bestehen. Eine KI, die du verwendest, bleibt bis zum Ablaufdatum angemeldet. Hast du eine KI 90 Tage lang nicht verwendet, musst du dich erneut anmelden.

Eine KI, die sich nicht selbst anmelden kann, kann einen Schlüssel verwenden. Gib unter **Schlüssel hinzufügen** einen Namen ein, wähle die Berechtigungen und die Dauer aus und drücke auf **Schlüssel erstellen**. Kopiere den Schlüssel sofort: Er wird nur einmal angezeigt. Die KI sendet ihn als `Authorization: Bearer <key>`.

## Sicher bleiben

Jede Anfrage wird protokolliert, auch abgelehnte. Anfragen von einer abgelaufenen oder ausgeschalteten Verbindung werden abgelehnt, bis du die Verbindung änderst. Deine Machine speichert von jeder Anmeldung nur einen Fingerabdruck. Eine Kopie dieser Daten allein ermöglicht keinen Zugriff.
