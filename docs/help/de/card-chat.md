---
title: Aufgaben-Chat
area: cards
summary: Frag im Chat zu einer Aufgabe nach oder ändere ihren Entwurf. Der Chat gehört zu dieser Aufgabe.
covers: card-chat
code: dashboard.html, assistant.py, chat_files.py, corrections.py
order: 4
translated: 224f6163a84e80ca
---
## Öffnen

Tippe bei der Aufgabe auf **Chat** oder wähle sie in der Liste in der Seitenleiste aus. Wenn du auf den Titel tippst oder klickst, kannst du ihn bearbeiten.

## E-Mails im Chat

Jede E-Mail zeigt nur, was neu ist. Frühere zitierte Nachrichten sind unter **Frühere Nachrichten** eingeklappt. Über **Thread lesen** öffnest du die E-Mails vollständig.

## Was die KI gemacht hat

Während die KI deine Nachricht bearbeitet, wird der letzte Arbeitsschritt über den Tipp-Punkten angezeigt, zum Beispiel „Liest die E-Mail“. Das kennst du auch von der Aufgabe, während die KI sie vorbereitet. Wenn sie den Browser verwendet, wird außerdem ein kleines Bild der Seite angezeigt.

Jeder abgeschlossene Durchlauf erscheint als unauffällige Zeile, zum Beispiel „12 Dinge geprüft“. Öffne sie, um jede Art von Arbeitsschritt einmal mit der jeweiligen Anzahl zu sehen: „Browser auf example.com verwendet · 7“. Dabei wird die Website genannt, nicht die Adresse, ein Befehl oder eine Datei.

Wenn die KI angehalten hat, um dich etwas zu fragen, erscheint die Frage ebenfalls als unauffällige Zeile, zum Beispiel „Gefragt: Heute oder Montag senden?“. Deine Nachricht darunter zeigt nur deine Antwort.

## Was du fragen kannst

Bevor du etwas schreibst, schlägt der Chat möglicherweise bis zu drei Vorschläge zum Antippen vor, die auf dieser Aufgabe basieren, zum Beispiel „Stattdessen Dienstag um 10:00 Uhr vorschlagen“. Wenn du einen antippst, erscheint er im Nachrichtenfeld. Dort kannst du ihn senden oder ändern. Wenn nichts Passendes dabei ist, gibt es keine Vorschläge.

- Zum Thread, zu den Personen oder zum Hintergrund: „Was haben sie letztes Mal gefragt?“
- Zum Ändern des Entwurfs: „Mach ihn kürzer“ oder „Erwähne das neue Datum“.

Eine Frage wird beantwortet, der Entwurf bleibt unverändert. Zum Senden dienen weiterhin die Schaltflächen der Aufgabe. Der Chat verschickt einen Entwurf nie in derselben Antwort, in der er ihn erstellt hat. Eine Änderung, die du anforderst und die niemand anderen betrifft, etwa eine Bereinigung in einem Dokument, wird sofort umgesetzt, ohne zusätzliche Bestätigung. Alles, was über deinen Auftrag hinausgeht, wartet auf dein Okay. Eine Aufgabe mit mehreren Schritten bleibt offen, bis alle Schritte erledigt sind.

Am Computer sendet Enter oder Ctrl+Enter (Cmd+Enter auf dem Mac) die Nachricht. Mit Shift+Enter beginnst du eine neue Zeile. Auf dem Handy verwendest du die Schaltfläche zum Senden.

## Wenn etwas nicht stimmt

Sag es im Chat, zum Beispiel „Sie sind nicht der CEO“ oder „Sie haben das Unternehmen verlassen“. Die Machine korrigiert den Eintrag an der Quelle: eine Rolle, ein Unternehmen, einen Titel, die Phase eines Projekts, das Projekt der Aufgabe oder eine Regel, die sie gelernt hat. Im Chat wird angezeigt, was sich geändert hat, zum Beispiel „Korrigiert: Sams Rolle ist Head of Sales, laut E-Mail-Signatur“, mit **Rückgängig**. Damit wird der alte Wert wiederhergestellt, sofern er sich nicht inzwischen geändert hat.

Andere Entwürfe, die auf dem falschen Wert beruhen, werden einzeln neu erstellt. Im jeweiligen Chat steht **Entwurf nach einer Korrektur neu erstellen**. Entwürfe, die du bearbeitet oder freigegeben hast, sowie gerade versendete Entwürfe bleiben unverändert. In der Antwort steht, wie viele es jeweils sind.

Auf einer GBrain-Seite ändert sich nur der eigene Abschnitt von The Machine. Was du dort geschrieben hast, bleibt erhalten. Wenn The Machine nicht erkennen kann, woher etwas stammt, lernt sie stattdessen aus deiner Notiz.

## Modell und Nachdenken

Unter dem Nachrichtenfeld zeigt der Chat das Modell und die Nachdenkstufe an, zum Beispiel „GPT-6.2 Sol“ und „Wenig Nachdenken“. Tippe auf eines davon, um es nur für diesen Chat zu ändern. Neue Chats verwenden die Einstellungen unter **Einstellungen** und **Modell** (siehe [Modell](model.md)).

**Schnell** am Ende des Modellmenüs sorgt dafür, dass Aufgaben-Chats schneller antworten. Dafür kostet es etwa doppelt so viel (oder verbraucht doppelt so viel von deinem Tarif). Die Einstellung gilt für Nachrichten, die du sendest, und für **Ausführen** in allen deinen Aufgaben-Chats, aber nie für Hintergrundarbeit. Sie ist standardmäßig ausgeschaltet und für Modelle, die sie nicht unterstützen, ausgegraut.

## Antwort anhalten

Während eine Antwort geschrieben wird, wird die Schaltfläche zum Senden zu **Stoppen**. Damit wird die Antwort sofort beendet und der bisherige Text mit dem Status **Gestoppt** beibehalten. Schreib eine neue Nachricht, um fortzufahren, oder tippe auf **Erneut versuchen**.

## Dateien hinzufügen

Tippe auf die Büroklammer, füge einen Screenshot ein oder zieh Dateien in den Chat. Jede Datei wird über dem Nachrichtenfeld angezeigt. Mit × entfernst du sie wieder. Eine Nachricht kann nur aus Dateien bestehen.

- Bilder (PNG, JPEG, GIF, WebP) mit bis zu 5 MB werden als Bilder an das Modell übergeben.
- PDFs, Textdateien, Tabellen (CSV) und Office-Dateien mit bis zu 10 MB: The Machine liest sie und kann sie an einen Entwurf anhängen.
- Bis zu 5 Dateien pro Nachricht.

Dateien bleiben auf deiner Machine und sind wie deine Nachrichten verschlüsselt. Dateien, die du hinzufügst, aber nie sendest, werden nach einem Tag gelöscht. Auch eine neue Aufgabe kann Dateien enthalten. Füge sie über **Neue Aufgabe** hinzu (siehe [Selbst erstellen](cards.md#make-one-yourself)).
