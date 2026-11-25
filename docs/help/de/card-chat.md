---
title: Aufgaben-Chat
area: cards
summary: Stell Fragen zu einer Aufgabe oder ändere ihren Entwurf im Chat, der zu dieser Aufgabe gehört.
covers: card-chat
code: dashboard.html, assistant.py, chat_files.py, corrections.py
order: 4
translated: 18a428fbe38a70e7
---
## Öffnen

Tippe bei der Aufgabe auf **Chat** oder wähle sie in der Liste in der Seitenleiste aus. Wenn du auf den Titel tippst oder klickst, kannst du ihn bearbeiten.

## E-Mails im Chat

Jede E-Mail zeigt nur, was neu ist. Frühere Nachrichten, auf die sie sich bezieht, sind unter **Frühere Nachrichten** eingeklappt. Über **Thread lesen** kannst du die E-Mails vollständig öffnen.

## Was passiert ist

Während die KI arbeitet, wird über dem Nachrichtenfeld **Bin dran…** angezeigt. Im Chat siehst du animierte Tipp-Punkte. Wenn sie den Browser verwendet, wird außerdem ein kleines Bild der Seite angezeigt.

Was bei jedem Durchlauf passiert, wird in einer einzelnen, dezenten Zeile angezeigt, die mitzählt, zum Beispiel „12 Dinge überprüft“. Öffne die Zeile, um jede Art von Schritt einmal mit der Anzahl zu sehen: „Browser auf example.com verwendet · 7“. Dabei wird die Website genannt, niemals die Adresse, ein Befehl oder eine Datei.

Bei Claude Code werden die Schritte während der Arbeit nicht im Chat angezeigt. Stattdessen erscheint der letzte Schritt über den Tipp-Punkten, zum Beispiel „Liest die E-Mail“. Über dem Nachrichtenfeld wird nichts angezeigt.

Wenn die KI anhält, um dich etwas zu fragen, wird die Frage ebenfalls als dezente Zeile angezeigt, zum Beispiel „Gefragt: Heute oder Montag senden?“. Deine Nachricht darunter zeigt nur deine Antwort.

## Was du fragen kannst

Bevor du etwas schreibst, schlägt der Chat bis zu drei Optionen zum Antippen vor, die auf dieser Aufgabe basieren, zum Beispiel „Stattdessen Dienstag um 10:00 Uhr vorschlagen“. Wenn du eine antippst, wird sie ins Nachrichtenfeld eingefügt. Du kannst sie dann senden oder ändern. Wenn nichts Passendes dabei ist, werden keine Vorschläge angezeigt.

- Zum Thread, zu den Personen oder zum Hintergrund: „Was haben sie letztes Mal gefragt?“
- Um den Entwurf zu ändern: „Kürzer machen“ oder „Das neue Datum erwähnen“.

Auf eine Frage bekommst du eine Antwort, und der Entwurf bleibt unverändert. Zum Senden verwendest du weiterhin die Schaltflächen der Aufgabe. Der Chat sendet niemals einen Entwurf in derselben Antwort, in der er ihn erstellt hat. Eine gewünschte Änderung, die niemand anderen betrifft, zum Beispiel eine Bereinigung in einem Dokument, wird sofort vorgenommen, ohne zusätzliche Bestätigung. Alles, worum du nicht gebeten hast, wartet auf dein OK. Eine Aufgabe mit mehreren Schritten bleibt offen, bis alle Schritte erledigt sind.

Am Computer sendest du mit Enter oder Ctrl+Enter (Cmd+Enter auf dem Mac). Mit Shift+Enter beginnst du eine neue Zeile. Auf dem Handy verwendest du die Senden-Schaltfläche.

## Wenn etwas nicht stimmt

Sag es im Chat, zum Beispiel „Sie sind nicht der CEO“ oder „Sie haben das Unternehmen verlassen“. The Machine korrigiert den ursprünglichen Eintrag: eine Rolle, ein Unternehmen, einen Titel, die Phase eines Projekts, das Projekt der Aufgabe oder eine gelernte Regel. Im Chat wird angezeigt, was sich geändert hat, zum Beispiel „Korrigiert: Sams Rolle ist Head of Sales, laut E-Mail-Signatur“, zusammen mit **Rückgängig**. Mit „Rückgängig“ wird der alte Wert wiederhergestellt, sofern er sich nicht inzwischen geändert hat.

Andere Entwürfe, die auf dem falschen Wert basieren, werden einzeln neu erstellt. In ihrem Chat steht **Entwurf nach einer Korrektur neu erstellen**. Entwürfe, die du bearbeitet oder genehmigt hast, sowie Entwürfe, die gerade versendet werden, bleiben unverändert. In der Antwort steht, wie viele es jeweils sind.

Auf einer GBrain-Seite wird nur der eigene Abschnitt von The Machine geändert. Was du dort geschrieben hast, bleibt erhalten. Wenn nicht klar ist, woher etwas stammt, lernt die KI stattdessen aus deiner Notiz.

## Modell und Nachdenken

Unter dem Nachrichtenfeld zeigt der Chat sein Modell und die Nachdenk-Stufe an, zum Beispiel „GPT-6.2 Sol“ und „Wenig Nachdenken“. Tippe auf eines der beiden, um nur für diesen Chat ein anderes auszuwählen. Neue Chats verwenden die Einstellungen unter **Einstellungen**, **Modell** (siehe [Modell](model.md)).

Mit **Schnell** am Ende des Modellmenüs antworten Aufgaben-Chats schneller. Die Kosten sind dabei ungefähr doppelt so hoch, oder es wird doppelt so viel von deinem Tarif verbraucht. Das gilt für deine Nachrichten und für „Ausführen“ in allen Aufgaben-Chats, niemals für Hintergrundarbeit. Standardmäßig ist die Option deaktiviert. Für Modelle, die sie nicht unterstützen, ist sie ausgegraut.

## Antwort stoppen

Während eine Antwort geschrieben wird, wird aus der Senden-Schaltfläche **Stoppen**. Damit wird die Antwort sofort beendet und das bis dahin Geschriebene bleibt erhalten und wird als **Gestoppt** markiert. Schreib eine neue Nachricht, um fortzufahren, oder tippe auf **Erneut versuchen**.

## Dateien hinzufügen

Tippe auf die Büroklammer, füge einen Screenshot ein oder ziehe Dateien in den Chat. Jede Datei wird über dem Nachrichtenfeld angezeigt. Mit × kannst du sie wieder entfernen. Eine Nachricht kann auch nur aus Dateien bestehen.

- Bilder (PNG, JPEG, GIF, WebP) bis zu 5 MB werden dem Modell als Bilder übergeben.
- PDFs, Textdateien, Tabellen (CSV) und Office-Dateien bis zu 10 MB: The Machine liest sie und kann sie an einen Entwurf anhängen.
- Bis zu 5 Dateien pro Nachricht.

Dateien bleiben auf deiner Machine und sind wie deine Nachrichten verschlüsselt. Dateien, die du hinzufügst, aber nie sendest, werden nach einem Tag gelöscht. Auch eine neue Aufgabe kann Dateien enthalten, wenn du sie über **Neue Aufgabe** erstellst (siehe [Aufgabe selbst erstellen](cards.md#make-one-yourself)).
