---
title: Live sprechen
area: cards
summary: Ein gesprochenes Gespräch mit The Machine über eine Aufgabe, mit der Stimme von OpenAI. Sie arbeitet im Chat der Aufgabe und sendet einen Entwurf erst, wenn du Ja dazu sagst.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
---
## Ein Gespräch starten

Tippe im Chat einer Aufgabe auf die Welle neben dem Mikrofon. Erlaube das Mikrofon, wenn dein Browser fragt. Wenn die Leiste **Live** zeigt, sprich wie bei einem Anruf. The Machine antwortet laut, und du kannst dazwischenreden, um sie zu unterbrechen.

Sie kennt die Aufgabe, in der du bist: ihre Nachrichten, ihren Entwurf und ihren Chat. Sie kann auch deine anderen Aufgaben nachschlagen.

Die Leiste hat **Stummschalten** und **Ende**. Verabschiede dich oder sag, dass du fertig bist, und es endet von selbst. Ein Gespräch dauert bis zu 10 Minuten. Eine Minute vor dem Ende zeigt der Timer, wie viel Zeit übrig ist. Starte es neu, um weiterzumachen.

## Alle Aufgaben durchsprechen

Tippe in der Seitenleiste (auf dem Handy im Menü) auf **Sprechen**, um alles, was auf dich wartet, per Stimme durchzugehen. The Machine sagt, wie viele warten, und nimmt sie nacheinander durch: zuerst **Bereit**, dann **Zu entscheiden**. Sie sieht auch deine anderen Aufgaben, etwa die noch **Wird vorbereitet**, und sagt dir, wenn eine bereit ist.

Sprechen hat eine eigene Seite: ein Gespräch von Anfang bis Ende, oben die Aufgabe, um die es geht, mit ihrem Entwurf und **Chat öffnen**. Sie springt nicht von Chat zu Chat.

Bitte sie, einen Entwurf vorzulesen, zu ändern, zu verschieben, als erledigt zu markieren oder zum nächsten zu gehen. Senden funktioniert wie im Chat einer Aufgabe: ein Entwurf pro Frage, nach einem klaren Ja. Was du über eine Aufgabe sagst, landet im Chat dieser Aufgabe. Kommt eine neue Aufgabe herein, erwähnt sie sie in einer Pause. Sag „füge eine Aufgabe hinzu: …“, und sie legt eine neue an, ohne die aktuelle zu verlassen.

Sie erreicht auch den Rest von The Machine. Frag nach einer Person, einer Organisation, einem Projekt, einem Termin oder einem Versprechen, und sie schlägt es nach und zeigt es. Sie kann eine Aufgabe zurückstellen, als erledigt markieren, verwerfen, umbenennen oder wieder öffnen, auch eine unter **Erledigt / verworfen**. Für alles andere legt sie eine Aufgabe an, lässt deren Chat es erledigen und sagt dir die Antwort.

Du kannst inzwischen auf eine andere Seite gehen: Die Leiste bleibt unten, und **Sprechen** in der Seitenleiste bringt dich zurück. Dieses Gespräch dauert höchstens 30 Minuten. Auf Computern und Android läuft es im Hintergrund weiter. Auf dem iPhone endet es, wenn die App den Bildschirm verlässt.

## Bitte um Dinge und sende mit einem Ja

Wenn du um etwas bittest, etwa „schreib eine Antwort, dass Donnerstag passt“ oder „stell das bis Montag zurück“, gibt The Machine es an den Chat der Aufgabe weiter, als hättest du es getippt. Der Chat folgt seinen üblichen Regeln: Er kann den Entwurf ändern oder die Aufgabe zurückstellen.

Der Chat kann auch Dinge nachschlagen, etwa die Öffnungszeiten eines Geschäfts im Web. Währenddessen zeigt er **Bin dran…**, und du kannst weiterreden. Wenn die Antwort da ist, sagt The Machine sie dir, und wo sie sie gefunden hat. Fragst du inzwischen etwas anderes, kommt das danach dran.

Willst du einen Entwurf senden, sag es. The Machine fragt zuerst und nennt, an wen und wie, etwa „Diese Antwort per E-Mail an Lotte senden?“. Vorher liest sie den ganzen Entwurf vor: an wen er geht, den Betreff und den Text. So klappt es auch mit dem Handy in der Tasche. Antworte mit einem klaren Ja, in jeder Sprache, und genau dieser Entwurf geht raus.

- Sie sendet genau den Entwurf, den sie vorgelesen hat. Ändert er sich nach der Frage, liest sie ihn neu vor und fragt erneut. Eine Frage, die du nicht innerhalb von 3 Minuten beantwortest, verfällt.
- Ist deine Antwort kein klares Ja, geht nichts raus und sie fragt erneut. „Nein“ sendet nichts.
- Ein Ja sendet immer genau einen Entwurf. Für mehrere nimm die Follow-up-Prüfung.
- Der Chat zeigt ein paar Sekunden lang **Per Sprache freigegeben** mit **Rückgängig**, bevor er rausgeht.

Du kannst auch jederzeit auf **Freigeben** tippen.

## Eine Stimme wählen

Wähle in **Einstellungen**, **Allgemein**, unter **Spracheingabe** bei **Stimme**, wie The Machine klingt. Tippe auf Abspielen, um eine Probe zu hören. **Cedar** ist der Standard. Die Stimme Cove von ChatGPT gibt es für Live sprechen nicht.

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
