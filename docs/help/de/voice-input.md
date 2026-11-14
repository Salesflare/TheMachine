---
title: Spracheingabe
area: cards
summary: Sprich statt zu tippen. Deine Worte erscheinen im Nachrichtenfeld, wo du sie prüfen kannst. Gesendet wird nichts.
covers: voice-input
code: voice_input.py, voice_worker.py, dashboard.html
order: 7
keywords: voice, dictate, dictation, speak, talk, microphone, mic, speech, transcribe
translated: f311b21bb4996eb4
---
## Sprich statt zu tippen

Tippe auf das Mikrofon in einem Nachrichtenfeld: im Chat einer Aufgabe, bei **Neue Aufgabe**, **Hilfe** oder im Feld zum Bearbeiten eines Entwurfs. Sprich und tippe dann auf das Häkchen. Oder halte das Mikrofon gedrückt, während du sprichst, und lass los, wenn du fertig bist.

Während die Spracheingabe läuft, zeigt das Feld einen Timer und den bisher erkannten Text. Tippe auf das Kreuz, um abzubrechen, ohne etwas zu übernehmen. Eine Aufnahme endet nach 2 Minuten automatisch.

Der Text erscheint im Feld an der Stelle, an der dein Cursor stand. Es wird nichts gesendet: Lies den Text, ändere, was du möchtest, und sende ihn selbst.

## Wohin deine Sprache geht

Wähle die gewünschte Option unter **Einstellungen**, **Allgemein** und **Spracheingabe**. Eine kurze Zeile dort zeigt, welche Option gerade verwendet wird.

- **Automatisch** (Standardeinstellung): OpenAI wandelt die Aufnahme in Text um, wenn deine Machine OpenAI nutzt (mit einem OpenAI-Schlüssel oder einem ChatGPT-Tarif, der Audio unterstützt). Andernfalls übernimmt deine Machine die Umwandlung selbst, und die Aufnahme verlässt sie nie.
- **Auf dieser Machine**: Die Umwandlung erfolgt immer auf deiner Machine, auch wenn OpenAI eingerichtet ist.
- **Mit OpenAI**: Die Umwandlung erfolgt immer mit OpenAI.

Eine Aufnahme wird gelöscht, sobald der Text vorliegt.

## Vorbereitung

Damit deine Machine Sprache selbst in Text umwandeln kann, lädt sie zuerst im Hintergrund ein Sprachmodell herunter (150 bis 500 MB), wenn gerade wenig los ist. In der Zwischenzeit steht in den Einstellungen **Wird im Hintergrund vorbereitet**. Wenn OpenAI verwendet wird, wird dieser Schritt übersprungen.

Bis dahin verwendet **Automatisch** die integrierte Spracherkennung deines Browsers, sofern vorhanden. Das wird unter dem Feld angezeigt. Manche Browser senden die Aufnahme an den jeweiligen Anbieter. Wenn **Auf dieser Machine** ausgewählt ist, wartet deine Aufnahme. Im Feld steht dann „Spracheingabe wird vorbereitet …“ und die verbleibende Zeit.

## Einstellungen

- **In Text umgewandelt**: **Automatisch**, **Auf dieser Machine** oder **Mit OpenAI**.
- **Genauigkeit** (nur auf deiner Machine): **Genauer** funktioniert für die meisten Sprachen am besten. **Schneller** ist zwar schneller, macht aber mehr Fehler. Auf einer Standard-Machine ist diese Option standardmäßig ausgewählt.
- **Sprache**: **Erkennen** funktioniert mit jeder App-Sprache. Wenn du deine Sprache auswählst, geht es etwas schneller.

Wenn du stattdessen laut mit The Machine sprechen möchtest, sieh dir [Live sprechen](talk-live.md) an.

## Wenn es nicht funktioniert

- **Das Mikrofon ist gesperrt**: Erlaube den Zugriff auf das Mikrofon für diese Website in den Browsereinstellungen. In der App auf deinem Smartphone findest du die Einstellung unter den App-Berechtigungen.
- **Kein Mikrofon gefunden**: Schließe ein Mikrofon an und versuche es noch einmal.
- **Deine Machine ist nicht erreichbar**: Deine Aufnahme wird behalten und transkribiert, sobald deine Machine wieder erreichbar ist. Wenn du es früher versuchen möchtest, tippe auf **Jetzt versuchen**.
- **Es wurde nichts erkannt**: Sprich näher am Mikrofon oder etwas länger.
