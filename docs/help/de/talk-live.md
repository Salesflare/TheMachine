---
title: Live sprechen
area: cards
summary: Ein gesprochenes Gespräch mit The Machine über eine Aufgabe, mit der Stimme von OpenAI. Sie arbeitet im Chat der Aufgabe und sendet einen Entwurf erst, wenn du Ja dazu sagst.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
translated: 60168384f08de74e
---
## Ein Gespräch starten

Tippe im Chat einer Aufgabe auf die Welle neben dem Mikrofon. Erlaube das Mikrofon, wenn dein Browser fragt. Wenn die Leiste **Live** zeigt, sprich wie bei einem Anruf. The Machine antwortet laut, und du kannst dazwischenreden, um sie zu unterbrechen.

Sie kennt diese Aufgabe: ihre Nachrichten, ihren Entwurf und ihren Chat. Sie kann auch deine anderen Aufgaben nachschlagen. Sag „als erledigt markieren“, „stell das bis morgen um 9 zurück“ oder „nicht nötig“, und sie macht das. Sag gleich danach „nein, nicht das“, um es zurückzunehmen. Zeiten richten sich nach der Zeitzone in deinen [Arbeitszeiten](work-hours.md).

Sie hört in der Sprache der App und in den Sprachen zu, die dein Browser nennt. Husten, Geräusche und andere Sprachen bekommen keine Antwort und bleiben aus dem Protokoll.

Die Leiste hat **Stummschalten** und **Ende**. Verabschiede dich, und das Gespräch endet von selbst. Ein Gespräch dauert bis zu 10 Minuten, in der letzten Minute mit Countdown. Starte es neu, um weiterzumachen.

## Alle Aufgaben durchsprechen

Tippe in der Seitenleiste (auf dem Handy im Menü) auf **Sprechen**. The Machine sagt, wie viele Aufgaben warten, und geht die unter **Für dich** nacheinander durch, die dringendste zuerst. Sie sagt dir, wenn eine mit **Wird vorbereitet…** bereit ist.

Sprechen hat eine eigene Seite: Oben steht die Aufgabe, um die es gerade geht, mit ihrem Entwurf und **Chat öffnen**.

Bitte sie, einen Entwurf vorzulesen, zu ändern, zurückzustellen, als erledigt zu markieren oder zur nächsten Aufgabe zu gehen. Was du über eine Aufgabe sagst, landet in ihrem Chat. Neue Aufgaben erwähnt sie in einer Pause. Sag „füge eine Aufgabe hinzu: …“, und sie legt eine an, ohne die aktuelle zu verlassen.

Frag nach einer Person, einer Organisation, einem Projekt, einem Termin oder einem Versprechen, und sie schlägt es nach und zeigt es. Sie kann Aufgaben auch verwerfen, umbenennen oder wieder öffnen, auch solche unter **Erledigt / verworfen**. Für alles andere gibt sie die Frage an den Chat einer neuen Aufgabe und sagt dir die Antwort.

Sie erinnert sich an eure früheren Gespräche. Frag „Was hatte ich zum Offsite entschieden?“, und sie sagt es dir, mit dem Zeitpunkt. Das kann nur **Sprechen** in der Seitenleiste.

Du kannst inzwischen auf eine andere Seite gehen: Die Leiste bleibt unten, und **Sprechen** in der Seitenleiste bringt dich zurück. Dieses Gespräch dauert höchstens 30 Minuten. Auf Computern und Android läuft es im Hintergrund weiter. Auf dem iPhone endet es, wenn die App den Bildschirm verlässt.

## Bitte um Dinge und sende mit einem Ja

Wenn du um etwas bittest, etwa „schreib eine Antwort, dass Donnerstag passt“, gibt The Machine es an den Chat der Aufgabe weiter, als hättest du es getippt. Der Chat folgt seinen üblichen Regeln.

Der Chat kann auch Dinge nachschlagen, etwa die Öffnungszeiten eines Geschäfts. Währenddessen zeigt er **Bin dran…**, und du kannst weiterreden. Wenn die Antwort da ist, sagt The Machine sie dir, und wo sie sie gefunden hat.

Willst du einen Entwurf senden, sag es. The Machine liest ihn vor (an wen er geht, den Betreff und den Text) und fragt, etwa „Diese Antwort per E-Mail an Sam senden?“. So klappt es auch mit dem Handy in der Tasche. Antworte mit einem klaren Ja, etwa „ja, senden“, und genau dieser Entwurf geht raus.

- Sie sendet genau den Entwurf, den sie vorgelesen hat. Ändert er sich, liest sie ihn neu vor und fragt erneut. Eine Frage, die du nicht innerhalb von 3 Minuten beantwortest, verfällt.
- Alles außer einem klaren Ja sendet nichts.
- Einen Entwurf, den du schon gesehen oder gehört hast, liest sie nicht noch einmal vor. Sie fragt nur, etwa „An Pat senden?“.
- Sag „sende alle, die bereit sind“, und sie nennt alle in einer Frage. Ein Ja sendet sie alle.
- Nach einem Ja zeigt Sprechen **Rückgängig** mit einem Countdown. Tippe darauf oder sag „rückgängig“ oder „warte“.
- Sobald er gesendet ist, sagt Sprechen „Gesendet.“, und die Aufgabe zeigt **An … gesendet** mit der Uhrzeit. Ging er nicht raus, sagt Sprechen, warum. Frag jederzeit „Ist er raus?“: Sprechen prüft nach und rät nie.

Du kannst auch auf **Freigeben** tippen.

Sag „mach es“, und The Machine fängt mit der Aufgabe an, wie bei **Ausführen**. Sag „Fehler melden“, und sie sendet einen Fehlerbericht, wie **Fehler melden** in der Hilfe.

## Eine Stimme wählen

Wähle in **Einstellungen**, **Allgemein**, unter **Spracheingabe** bei **Stimme**, wie The Machine klingt. Tippe auf Abspielen, um eine Probe zu hören. **Cedar** ist der Standard. Die Stimme Cove von ChatGPT gibt es für Live sprechen nicht.

## Ein Protokoll im Chat

Was ihr beide sagt, wird in den Chat der Aufgabe geschrieben, unter einer Zeile **Live gesprochen**. Du kannst es später nachlesen.

## Was du brauchst

Live sprechen nutzt die Echtzeitstimme von OpenAI, deshalb braucht deine Machine eines davon:

- Eine ChatGPT-Anmeldung: in den Tarifen enthalten, die es anbieten.
- Einen OpenAI-API-Schlüssel: OpenAI berechnet ihn pro Minute, und die Leiste sagt das. Wenn beides eingerichtet ist, nutzt deine Machine den Schlüssel.

**Einstellungen**, **Allgemein**, **Spracheingabe** zeigt, ob Live sprechen bereit ist. Ohne OpenAI erscheint die Welle nicht. Dein Audio geht von deinem Browser direkt an OpenAI.

## Wenn es nicht klappt

- **Das Mikrofon ist blockiert**: Erlaube das Mikrofon für diese Seite in den Einstellungen deines Browsers.
- **Live sprechen konnte nicht starten**: Prüfe die ChatGPT-Anmeldung oder den OpenAI-Schlüssel und versuch es noch mal.
- **Live sprechen hat die Verbindung verloren**: Starte es neu. Was bisher gesagt wurde, bleibt im Chat.
- Sie sagt, dass sie dich nicht versteht: Prüfe dein Mikrofon oder schreib im Chat.
