---
title: Spracheingabe
area: cards
summary: Sprechen statt tippen. Was du sagst, landet im Nachrichtenfeld, damit du es prüfen kannst. Nichts wird gesendet.
covers: voice-input
code: voice_input.py, voice_worker.py, dashboard.html
order: 7
keywords: voice, dictate, dictation, speak, talk, microphone, mic, speech, transcribe
---
## Sprechen statt tippen

Tippe in einem Nachrichtenfeld auf das Mikrofon: im Chat einer Aufgabe, bei **Neue Aufgabe**, in der **Hilfe** oder im Feld, mit dem du einen Entwurf änderst. Sprich und tippe dann auf das Häkchen. Oder halte das Mikrofon gedrückt, während du sprichst, und lass los, wenn du fertig bist.

Während sie zuhört, zeigt das Feld einen Timer. Tippe auf das Kreuz, um aufzuhören, ohne etwas zu behalten. Eine Aufnahme kann bis zu 2 Minuten lang sein; nach 2 Minuten stoppt sie von selbst und schreibt auf, was du gesagt hast.

Was du gesagt hast, landet im Feld, dort, wo dein Cursor war. Nichts wird gesendet: Lies es, ändere, was du willst, und sende es selbst.

## Beim ersten Mal

Wenn du zum ersten Mal auf das Mikrofon tippst, bereitet deine Machine die Sprache vor. Sie lädt das Sprachmodell einmal herunter, etwa 600 MB, und zeigt "Sprache wird vorbereitet…" mit dem Fortschritt. Das dauert ein paar Minuten. Deine Aufnahme wartet und wird aufgeschrieben, sobald alles bereit ist.

## Wohin deine Stimme geht

Standardmäßig wird deine Aufnahme auf deiner Machine selbst in Text umgewandelt. Sie verlässt sie nie und wird gelöscht, sobald der Text da ist. Die eigene Spracherkennung deines Browsers wird nicht genutzt, weil manche Browser deine Stimme dabei an ihren Hersteller schicken.

In den **Einstellungen**, unter **Allgemein**, **Spracheingabe**, kannst du wählen:

- **In Text umgewandelt**: **Auf dieser Machine** oder **Mit OpenAI**. OpenAI ist auf einem kleinen Server schneller, aber deine Aufnahme geht mit deinem eigenen Schlüssel an OpenAI. Dafür braucht es einen OpenAI-API-Schlüssel in OpenClaw. Eine ChatGPT-Anmeldung reicht nicht.
- **Genauigkeit**: **Genauer** funktioniert für die meisten Sprachen am besten und dauert auf einem kleinen Server etwa so lang, wie du gesprochen hast. **Schneller** geht flotter, hat aber mehr falsche Wörter.
- **Sprache**: **Erkennen** funktioniert für jede Sprache der App. Deine eigene zu wählen ist etwas schneller.

## Wenn es nicht klappt

- **Das Mikrofon ist blockiert**: Erlaube das Mikrofon für diese Seite in den Einstellungen deines Browsers. In der Handy-App findest du das bei den Berechtigungen der App.
- **Kein Mikrofon gefunden**: Schließ eins an und versuch es noch mal.
- **Deine Machine ist nicht erreichbar**: Deine Aufnahme bleibt erhalten. Tippe auf **Erneut versuchen**, wenn deine Machine wieder da ist.
- **Ich habe nichts verstanden**: Sprich etwas näher am Mikrofon, oder länger.
