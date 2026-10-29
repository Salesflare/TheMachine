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

Während sie zuhört, zeigt das Feld einen Timer. Tippe auf das Kreuz, um aufzuhören, ohne etwas zu behalten. Eine Aufnahme kann bis zu 2 Minuten lang sein; nach 2 Minuten stoppt sie von selbst und schreibt auf, was du gesagt hast. Was sie bisher gehört hat, steht in der Leiste, während du sprichst, damit der Text kurz nach dem Stoppen da ist.

Was du gesagt hast, landet im Feld, dort, wo dein Cursor war. Nichts wird gesendet: Lies es, ändere, was du willst, und sende es selbst.

## Wohin deine Stimme geht

In **Einstellungen**, **Allgemein**, unter **Spracheingabe** sagt eine kurze Zeile, was gerade genutzt wird.

- **Automatisch** (Standard): Wenn OpenAI in OpenClaw eingerichtet ist, wandelt OpenAI deine Aufnahme in Text um. Das ist ein API-Schlüssel oder eine ChatGPT-Anmeldung, wenn dein Tarif Audio erlaubt. Ohne OpenAI wird sie auf deiner Machine selbst in Text umgewandelt und verlässt sie nie.
- **Auf dieser Machine**: immer auf deiner Machine, auch wenn OpenAI eingerichtet ist.
- **Mit OpenAI**: immer OpenAI.

Eine Aufnahme wird gelöscht, sobald der Text zurück ist.

## Vorbereitung

Um Sprache selbst in Text umzuwandeln, braucht deine Machine ein Sprachmodell mit 150 bis 500 MB. Sie lädt es im Hintergrund mit niedriger Priorität herunter, sobald sie eingerichtet ist, ihre erste Durchsicht fertig ist und es eine Weile ruhig war. Solange zeigen die Einstellungen **Wird vorbereitet (im Hintergrund)**. Wenn OpenAI genutzt wird, macht sie das nie.

Bis sie bereit ist, nutzt **Automatisch** die Spracherkennung deines Browsers, falls er eine hat, und sagt das unter dem Feld. Manche Browser schicken das an ihren Hersteller. Wenn **Auf dieser Machine** gewählt ist, wartet deine Aufnahme, und das Feld zeigt „Sprache wird vorbereitet…“ mit der verbleibenden Zeit.

## Einstellungen

- **In Text umgewandelt**: **Automatisch**, **Auf dieser Machine** oder **Mit OpenAI**.
- **Genauigkeit** (nur auf deiner Machine): **Genauer** funktioniert für die meisten Sprachen am besten. **Schneller** geht flotter, erkennt aber mehr Wörter falsch. Auf einem Standard-Server, der weniger Speicher hat, ist **Schneller** voreingestellt.
- **Sprache**: **Erkennen** funktioniert für jede Sprache der App. Deine eigene zu wählen ist etwas schneller.

Um stattdessen laut mit The Machine zu sprechen, sieh dir [Live sprechen](talk-live.md) an.

## Wenn es nicht klappt

- **Das Mikrofon ist blockiert**: Erlaube das Mikrofon für diese Seite in den Einstellungen deines Browsers. In der Handy-App findest du das bei den Berechtigungen der App.
- **Kein Mikrofon gefunden**: Schließ eins an und versuch es noch mal.
- **Deine Machine ist nicht erreichbar**: Deine Aufnahme bleibt erhalten und wird aufgeschrieben, sobald deine Machine wieder da ist. Für einen früheren Versuch tippe auf **Jetzt versuchen**.
- **Ich habe nichts verstanden**: Sprich etwas näher am Mikrofon, oder länger.
