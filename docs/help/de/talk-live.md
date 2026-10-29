---
title: Live sprechen
area: cards
summary: Ein gesprochenes Gespräch mit The Machine über eine Aufgabe, mit der Stimme von OpenAI. Sie arbeitet im Chat der Aufgabe, sendet aber nie etwas.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
---
## Ein Gespräch starten

Tippe im Chat einer Aufgabe auf die Welle neben dem Mikrofon. Erlaube das Mikrofon, wenn dein Browser fragt. Wenn die Leiste **Live** zeigt, sprich wie bei einem Anruf. The Machine antwortet laut, und du kannst dazwischenreden, um sie zu unterbrechen.

Sie kennt die Aufgabe, in der du bist: ihre Nachrichten, ihren Entwurf und ihren Chat. Sie kann auch deine anderen Aufgaben nachschlagen.

Die Leiste hat **Stummschalten** und **Ende**. Ein Gespräch dauert bis zu 10 Minuten. Eine Minute vor dem Ende zeigt der Timer, wie viel Zeit übrig ist. Starte es neu, um weiterzumachen.

## Aus einem Gespräch wird nichts gesendet

Wenn du um etwas bittest, etwa „schreib eine Antwort, dass Donnerstag passt“ oder „stell das bis Montag zurück“, gibt The Machine es an den Chat der Aufgabe weiter, als hättest du es getippt. Der Chat folgt seinen üblichen Regeln: Er kann den Entwurf ändern oder die Aufgabe zurückstellen, aber ein Entwurf wartet auf dein **Freigeben**.

„Ja“ oder „schick es“ zu sagen bewirkt nichts. Nur dein Tippen auf **Freigeben** sendet.

## Ein Protokoll im Chat

Was ihr beide sagt, wird in den Chat der Aufgabe geschrieben, unter einer Zeile **Live gesprochen**. Du kannst es später nachlesen.

## Was du brauchst

Live sprechen nutzt die Echtzeitstimme von OpenAI, deshalb muss OpenAI in OpenClaw eingerichtet sein:

- Eine ChatGPT-Anmeldung: in deinem Tarif enthalten, wenn dein Tarif Zugang hat.
- Ein OpenAI-API-Schlüssel: OpenAI berechnet deinem Schlüssel jede Gesprächsminute, und die Leiste sagt das. Wenn beides eingerichtet ist, nutzt OpenClaw den Schlüssel.

**Einstellungen**, **Allgemein**, **Spracheingabe** zeigt, ob Live sprechen bereit ist. Ohne OpenAI erscheint die Welle nicht. Dein Audio geht von deinem Browser direkt an OpenAI. Dein Schlüssel erreicht den Browser nie.

## Wenn es nicht klappt

- **Das Mikrofon ist blockiert**: Erlaube das Mikrofon für diese Seite in den Einstellungen deines Browsers.
- **Live sprechen konnte nicht starten**: Prüfe OpenAI in OpenClaw und versuch es noch mal.
- **Live sprechen hat die Verbindung verloren**: Starte es neu. Was bisher gesagt wurde, bleibt im Chat.
