---
title: Aufgaben-Chat
area: cards
summary: Stell Fragen zu einer Aufgabe oder ändere ihren Entwurf im Chat, der zu dieser Aufgabe gehört.
covers: card-chat
code: dashboard.html, assistant.py, chat_files.py, corrections.py
order: 4
translated: 340b9cfc0e3a424d
---
## Öffnen

Tippe auf dem Handy auf den Titel der Aufgabe. Am Computer klickst du auf **Im Chat ansehen ›** oder auf den Chat-Link der Aufgabe. Wenn du am Computer auf den Titel klickst, benennst du die Aufgabe um.

## E-Mails im Chat

Jede E-Mail zeigt nur, was neu ist. Frühere zitierte Nachrichten sind unter **Frühere Nachrichten** eingeklappt. Über **Thread lesen** öffnest du die vollständigen E-Mails.

## Was ausgeführt wurde

Jeder Durchlauf erscheint als unauffällige Zeile, zum Beispiel „12 Dinge geprüft“. Öffne sie, um jede Art von Schritt einmal zu sehen, mit der jeweiligen Anzahl: „Browser auf example.com verwendet · 7“. Dabei wird die Website genannt, niemals die Adresse, ein Befehl oder eine Datei.

Wenn die Machine angehalten hat, um dich etwas zu fragen, erscheint die Frage ebenfalls als unauffällige Zeile, zum Beispiel „Gefragt: Heute oder am Montag senden?“. Deine Nachricht darunter zeigt nur deine Antwort.

## Was du fragen kannst

Bevor du etwas schreibst, schlägt der Chat möglicherweise bis zu drei Formulierungen vor, die auf dieser Aufgabe basieren, zum Beispiel „Stattdessen Dienstag um 10:00 Uhr anbieten“. Wenn du auf eine davon tippst, erscheint sie im Nachrichtenfeld. Du kannst sie dann senden oder ändern. Wenn nichts Bestimmtes passt, werden keine Vorschläge angezeigt.

- Zum Thread, zu den Personen oder zum Hintergrund: „Was haben sie letztes Mal gefragt?“
- Um den Entwurf zu ändern: „Kürzer machen“ oder „Das neue Datum erwähnen“.

Auf eine Frage erhältst du eine Antwort, und der Entwurf bleibt unverändert. Zum Senden verwendest du die Buttons der Aufgabe. Der Chat sendet niemals einen Entwurf in derselben Antwort, in der er ihn erstellt hat. Eine Änderung, die sonst niemanden erreicht, etwa eine Bereinigung in einem Dokument, wird sofort umgesetzt, ohne dass du noch einmal auf Bestätigen klicken musst. Alles, was über deine Bitte hinausgeht, wartet auf dein OK. Eine Aufgabe mit mehreren Schritten bleibt offen, bis alle Schritte erledigt sind.

Am Computer sendet Enter oder Ctrl+Enter (Cmd+Enter auf dem Mac) deine Nachricht. Mit Shift+Enter beginnst du eine neue Zeile. Auf dem Handy verwendest du den Senden-Button.

## Wenn etwas nicht stimmt

Sag es im Chat, zum Beispiel „Sie ist nicht die CEO“ oder „Sie arbeitet nicht mehr für das Unternehmen“. Die Machine korrigiert den Fehler direkt an der Quelle: eine Rolle, ein Unternehmen, einen Titel, die Phase eines Projekts, das Projekt der Aufgabe oder eine Regel, die sie gelernt hat. Im Chat wird angezeigt, was geändert wurde, zum Beispiel „Korrigiert: Sams Rolle ist Head of Sales, laut E-Mail-Signatur“, mit **Rückgängig**. Damit wird der alte Wert wiederhergestellt, sofern er sich nicht inzwischen geändert hat.

Andere Entwürfe, die auf dem falschen Wert beruhen, werden nacheinander neu erstellt. In ihrem Chat steht **Entwurf wird nach einer Korrektur neu erstellt**. Entwürfe, die du bearbeitet oder freigegeben hast, und solche, die gerade versendet werden, bleiben unverändert. In der Antwort steht, wie viele es jeweils sind.

Auf einer GBrain-Seite ändert sich nur der eigene Abschnitt der Machine. Was du dort geschrieben hast, bleibt erhalten. Wenn sie nicht erkennen kann, woher etwas stammt, lernt sie stattdessen aus deiner Notiz.

## Modell und Nachdenken

Unter dem Nachrichtenfeld zeigt der Chat sein Modell und die Nachdenkstufe an, zum Beispiel „GPT-6.2 Sol“ und „Wenig Nachdenken“. Tippe auf eines davon, um es nur für diesen Chat zu ändern. Für neue Chats gelten die Einstellungen unter **Einstellungen** und **Modell** (siehe [Modell](model.md)).

Mit **Schnell** am Ende des Modellmenüs antworten Aufgaben-Chats schneller. Das kostet ungefähr doppelt so viel oder verbraucht doppelt so viel von deinem Kontingent. Die Option gilt für Nachrichten, die du sendest, und für Ausführen in all deinen Aufgaben-Chats, niemals für Hintergrundarbeit. Sie ist standardmäßig deaktiviert und für Modelle, die sie nicht unterstützen, ausgegraut.

## Antwort anhalten

Während eine Antwort geschrieben wird, wird aus dem Senden-Button **Stoppen**. Damit wird die Antwort sofort beendet und das bis dahin Geschriebene bleibt erhalten und wird als **Gestoppt** markiert. Schreib eine neue Nachricht, um fortzufahren, oder tippe auf **Erneut versuchen**.

## Dateien hinzufügen

Tippe auf die Büroklammer, füge einen Screenshot ein oder zieh Dateien in den Chat. Jede Datei wird über dem Nachrichtenfeld angezeigt. Mit × entfernst du sie wieder. Eine Nachricht kann auch nur aus Dateien bestehen.

- Bilder (PNG, JPEG, GIF, WebP) mit bis zu 5 MB werden als Bilder an das Modell gesendet.
- PDFs, Textdateien, Tabellen (CSV) und Office-Dateien mit bis zu 10 MB: Die Machine liest sie und kann sie an einen Entwurf anhängen.
- Bis zu 5 Dateien pro Nachricht.

Dateien bleiben auf deiner Machine und sind wie deine Nachrichten verschlüsselt. Dateien, die du hinzufügst, aber nie sendest, werden nach einem Tag entfernt. Auch eine neue Aufgabe kann Dateien enthalten, wenn du sie über **Neue Aufgabe** erstellst (siehe [Selbst erstellen](cards.md#make-one-yourself)).
