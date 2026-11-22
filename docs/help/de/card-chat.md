---
title: Aufgaben-Chat
area: cards
summary: Frag nach einer Aufgabe oder ändere ihren Entwurf im Chat, der zu dieser Aufgabe gehört.
covers: card-chat
code: dashboard.html, assistant.py, chat_files.py, corrections.py
order: 4
translated: 64a15c6ce46c6679
---
## Öffnen

Tippe auf einem Handy auf den Titel der Aufgabe. Am Computer klickst du auf **Im Chat ansehen ›** oder auf den Chat-Link der Aufgabe. Wenn du am Computer auf den Titel klickst, wird die Aufgabe umbenannt.

## E-Mails im Chat

Jede E-Mail zeigt nur, was neu ist. Frühere zitierte Nachrichten sind unter **Frühere Nachrichten** eingeklappt. Mit **Thread lesen** werden die E-Mails vollständig geöffnet.

## Was die KI getan hat

Während sie deine Nachricht bearbeitet, wird der letzte Schritt über den Tipp-Punkten angezeigt, etwa „Liest die E-Mail“. Das gilt auch für die Aufgabe während der Vorbereitung. Wenn sie den Browser verwendet, wird außerdem ein kleines Bild der Seite angezeigt.

Jeder abgeschlossene Durchlauf erscheint als unauffällige Zeile, etwa „12 Dinge überprüft“. Öffne sie, um jede Art von Schritt einmal mit der Anzahl zu sehen: „Browser auf example.com verwendet · 7“. Dabei wird die Website genannt, nie die Adresse, ein Befehl oder eine Datei.

Wenn sie angehalten hat, um dich etwas zu fragen, wird die Frage ebenfalls als unauffällige Zeile angezeigt, etwa „Gefragt: Heute oder Montag senden?“. Deine Nachricht darunter enthält nur deine Antwort.

## Was du fragen kannst

Bevor du etwas schreibst, schlägt der Chat möglicherweise bis zu drei Vorschläge für diese Aufgabe vor, etwa „Stattdessen Dienstag um 10:00 Uhr anbieten“. Wenn du auf einen Vorschlag tippst, wird er ins Nachrichtenfeld eingefügt und kann gesendet oder geändert werden. Wenn nichts Konkretes passt, werden keine Vorschläge angezeigt.

- Zum Thread, zu den Personen oder zum Hintergrund: „Was haben sie letztes Mal gefragt?“
- Um den Entwurf zu ändern: „Kürzer machen“ oder „Das neue Datum erwähnen“.

Auf eine Frage bekommst du eine Antwort, und der Entwurf bleibt unverändert. Gesendet wird weiterhin über die Schaltflächen der Aufgabe: Der Chat sendet nie einen Entwurf in derselben Antwort, in der er ihn geschrieben hat. Eine gewünschte Änderung, die niemand sonst betrifft, etwa das Bereinigen eines Dokuments, wird sofort vorgenommen, ohne zusätzliche Bestätigung. Alles, was über deine Bitte hinausgeht, wartet auf dein Okay. Eine Aufgabe mit mehreren Schritten bleibt offen, bis alle Schritte erledigt sind.

Am Computer sendet Enter oder Ctrl+Enter (Cmd+Enter auf einem Mac) die Nachricht. Mit Shift+Enter beginnst du eine neue Zeile. Auf einem Handy verwendest du die Senden-Schaltfläche.

## Wenn etwas nicht stimmt

Sag es im Chat, etwa „Sie sind nicht der CEO“ oder „Sie haben das Unternehmen verlassen“. The Machine korrigiert den Eintrag direkt an der Quelle: eine Rolle, ein Unternehmen, einen Titel, die Phase eines Projekts, das Projekt der Aufgabe oder eine gelernte Regel. Der Chat zeigt, was sich geändert hat, etwa „Korrigiert: Sams Rolle ist Head of Sales, laut E-Mail-Signatur“, mit **Rückgängig**. Damit wird der alte Wert wiederhergestellt, sofern er sich nicht inzwischen geändert hat.

Deine anderen Entwürfe, die auf dem falschen Wert basieren, werden nacheinander neu erstellt. In ihrem Chat steht **Entwurf nach Korrektur neu erstellen**. Entwürfe, die du bearbeitet oder freigegeben hast, und solche, die gerade versendet werden, bleiben unverändert. In der Antwort steht, wie viele es jeweils sind.

Auf einer GBrain-Seite wird nur der eigene Abschnitt von The Machine geändert. Was du dort geschrieben hast, bleibt erhalten. Wenn nicht klar ist, woher etwas stammt, lernt The Machine stattdessen aus deiner Notiz.

## Modell und Nachdenken

Unter dem Nachrichtenfeld zeigt der Chat sein Modell und die Nachdenk-Stufe an, etwa „GPT-6.2 Sol“ und „Wenig Nachdenken“. Tippe auf eines davon, um es nur für diesen Chat zu ändern. Neue Chats verwenden die Einstellungen aus **Einstellungen**, **Modell** (siehe [Modell](model.md)).

Mit **Schnell** am Ende des Modellmenüs antworten Aufgaben-Chats schneller. Die Kosten sind dabei etwa doppelt so hoch (oder es wird doppelt so viel von deinem Kontingent verbraucht). Das gilt für deine Nachrichten und **Ausführen** in all deinen Aufgaben-Chats, nie für Hintergrundarbeit. Die Option ist standardmäßig deaktiviert und für Modelle, die sie nicht unterstützen, ausgegraut.

## Antwort stoppen

Während eine Antwort geschrieben wird, wird aus der Senden-Schaltfläche **Stoppen**. Damit wird die Antwort sofort beendet, und der bisherige Text bleibt mit der Markierung **Gestoppt** erhalten. Schreib eine neue Nachricht, um fortzufahren, oder tippe auf **Erneut versuchen**.

## Dateien hinzufügen

Tippe auf die Büroklammer, füge einen Screenshot ein oder ziehe Dateien in den Chat. Jede Datei wird über dem Nachrichtenfeld angezeigt. Mit × entfernst du sie wieder. Eine Nachricht kann auch nur aus Dateien bestehen.

- Bilder (PNG, JPEG, GIF, WebP) mit bis zu 5 MB werden als Bilder an das Modell übermittelt.
- PDFs, Textdateien, Tabellen (CSV) und Office-Dateien mit bis zu 10 MB liest The Machine und kann sie an einen Entwurf anhängen.
- Bis zu 5 Dateien pro Nachricht.

Dateien bleiben auf deiner Machine und sind wie deine Nachrichten verschlüsselt. Dateien, die du hinzufügst, aber nie sendest, werden nach einem Tag entfernt. Eine neue Aufgabe kann ebenfalls Dateien enthalten, wenn du sie über **Neue Aufgabe** erstellst (siehe [Selbst erstellen](cards.md#make-one-yourself)).
