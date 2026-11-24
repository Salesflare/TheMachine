---
title: Live sprechen
area: cards
summary: Ein gesprochenes Gespräch mit The Machine über eine Aufgabe, mit der Stimme von OpenAI. Es findet im Chat der Aufgabe statt und sendet einen Entwurf erst, wenn du zustimmst.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
translated: f5555cb693a23682
---
## Gespräch starten

Tippe im Chat einer Aufgabe auf die Welle neben dem Mikrofon und erlaube den Zugriff aufs Mikrofon, falls du dazu aufgefordert wirst. Wenn in der Leiste **Live** steht, sprich wie bei einem Telefonat. The Machine antwortet laut. Sprich einfach dazwischen, um sie zu unterbrechen.

The Machine kennt diese Aufgabe: ihre Nachrichten, ihren Entwurf und ihren Chat. Außerdem kann sie deine anderen Aufgaben nachschlagen. Sag „Markiere das als erledigt“, „Stelle es bis morgen um 9 Uhr zurück“ oder „Nicht nötig“, und sie führt es aus. Sag direkt danach „Nein, nicht das“, um es rückgängig zu machen. Die Uhrzeiten richten sich nach der Zeitzone deiner [Arbeitszeiten](work-hours.md).

The Machine hört auf die Sprache der App und auf die Sprachen, die in deinem Browser aufgeführt sind. Husten, Geräusche und andere Sprachen werden nicht beantwortet und erscheinen auch nicht im Transkript.

In der Leiste findest du **Stummschalten** und **Beenden**. Verabschiede dich, und das Gespräch endet von selbst. Ein Gespräch dauert bis zu 10 Minuten. In der letzten Minute läuft ein Countdown. Starte einfach ein neues Gespräch, um weiterzumachen.

## Alle deine Aufgaben durchgehen

Tippe in der Seitenleiste auf „**Sprechen**“ (auf dem Handy im Menü). The Machine sagt dir, wie viele Aufgaben anstehen, und geht die Aufgaben unter **Für dich** eine nach der anderen durch, in der Reihenfolge deiner Liste. Sie sagt dir Bescheid, wenn eine mit **Wird vorbereitet…** markierte Aufgabe bereit ist.

„**Sprechen**“ hat eine eigene Seite: Die aktuelle Aufgabe steht oben, mit ihrem Entwurf und **Chat öffnen**.

Bitte The Machine, einen Entwurf vorzulesen, zu ändern, eine Aufgabe zurückzustellen, sie als erledigt zu markieren oder zur nächsten zu wechseln. Was du zu einer Aufgabe sagst, landet in ihrem Chat. In Gesprächspausen weist The Machine auf neue Aufgaben hin. Sag „Füge eine Aufgabe hinzu, …“, um eine Aufgabe hinzuzufügen, ohne deine Stelle zu verlieren.

Frag nach einer Person, Organisation, einem Projekt, Meeting oder Versprechen. The Machine sucht danach und zeigt dir die Ergebnisse. Sie kann auch Aufgaben verwerfen, umbenennen oder wieder öffnen, auch solche unter **Erledigt / verworfen**. Bei anderen Fragen übergibt sie diese an den Chat einer neuen Aufgabe und sagt dir dort die Antwort.

The Machine erinnert sich an frühere Gespräche mit dir. Frag „Was hatte ich zum Offsite entschieden?“, und sie sagt es dir und wann du es gesagt hast. Das geht nur über „**Sprechen**“ in der Seitenleiste.

Du kannst währenddessen auch andere Seiten aufrufen: Die Leiste bleibt unten, und „**Sprechen**“ bringt dich zurück. Dieses Gespräch dauert bis zu 30 Minuten. Auf Computern und Android läuft es im Hintergrund weiter. Auf dem iPhone wird es beendet, sobald die App nicht mehr auf dem Bildschirm ist.

## Wünsche äußern und nach Zustimmung senden

Bitte The Machine um etwas, zum Beispiel „Schreib eine Antwort, dass Donnerstag passt“. Sie gibt es an den Chat der Aufgabe weiter, als hättest du es dort eingegeben. Für den Chat gelten die üblichen Regeln.

Der Chat kann auch Informationen nachschlagen, zum Beispiel die Öffnungszeiten eines Geschäfts. Dabei erscheint **Bin dran…**, und du kannst weiterreden. Sobald die Antwort bereit ist, nennt The Machine sie dir und sagt, woher sie stammt.

Um einen Entwurf zu senden, sag es einfach. The Machine liest ihn laut vor, einschließlich Empfänger, Betreff und Text, und fragt zum Beispiel: „Diese Antwort per E-Mail an Sam senden?“ Das funktioniert auch, wenn dein Handy in der Tasche steckt. Sag eindeutig Ja, zum Beispiel „Ja, senden“, und der Entwurf wird verschickt.

- The Machine sendet genau den Entwurf, den sie vorgelesen hat. Ändert sich der Entwurf, liest sie ihn erneut vor und fragt noch einmal. Eine Frage, auf die du nicht innerhalb von 3 Minuten antwortest, verfällt.
- Ohne eindeutiges Ja wird nichts gesendet.
- Einen Entwurf, den du bereits gesehen oder gehört hast, liest The Machine nicht noch einmal vor. Sie fragt nur, zum Beispiel: „An Pat senden?“
- Sag „Sende alle fertigen Entwürfe“, und The Machine nennt alle Empfänger in einer Frage. Ein Ja sendet alle Entwürfe.
- Nach deinem Ja zeigt „Sprechen“ **Rückgängig** mit einem Countdown an. Tippe darauf oder sag „Rückgängig“ oder „Warte“.
- Nach dem Senden sagt „Sprechen“ „Gesendet.“ Die Aufgabe zeigt **Gesendet an** mit dem Empfänger und dem Zeitpunkt. Falls etwas schiefgeht, sagt „Sprechen“ dir warum. Frag jederzeit „Wurde es gesendet?“. The Machine prüft es und rät nie.

Du kannst auch auf „**Freigeben**“ tippen.

Sag „Führe es aus“, um The Machine mit der Aufgabe zu starten, wie mit **Ausführen**. Sag „Melde einen Fehler“, um einen Fehlerbericht zu senden, wie mit **Fehler melden** in der Hilfe.

## Stimme auswählen

Wähle unter „**Einstellungen**“ > „**Allgemein**“ > „**Spracheingabe**“ eine **Stimme** aus und tippe auf Wiedergabe, um sie anzuhören. **Cedar** ist die Standardstimme. Die Cove-Stimme von ChatGPT ist nicht verfügbar.

## Ein Eintrag im Chat

Alles, was gesagt wird, erscheint im Chat der Aufgabe unter dem Eintrag **Live gesprochen**, damit du es später nachlesen kannst.

## Voraussetzungen

Für Live sprechen wird die Stimme von OpenAI verwendet. Deine Machine braucht daher eine der folgenden Möglichkeiten:

- Eine ChatGPT-Anmeldung: in den Tarifen enthalten, die sie anbieten.
- Einen OpenAI-API-Schlüssel: OpenAI berechnet die Nutzung pro Minute. In der Leiste wird darauf hingewiesen. Wenn beides vorhanden ist, verwendet deine Machine den Schlüssel.

Unter „**Einstellungen**“ > „**Allgemein**“ > „**Spracheingabe**“ siehst du, ob Live sprechen bereit ist. Ohne OpenAI wird die Welle nicht angezeigt. Deine Audiodaten werden direkt von deinem Browser an OpenAI übertragen.

## Wenn es nicht funktioniert

- **Das Mikrofon ist gesperrt**: Erlaube den Zugriff auf das Mikrofon für diese Website in den Browsereinstellungen.
- **Live sprechen konnte nicht gestartet werden**: Überprüfe deine ChatGPT-Anmeldung oder deinen OpenAI-Schlüssel und versuche es noch einmal.
- **Live sprechen hat die Verbindung verloren**: Starte erneut. Was gesagt wurde, bleibt im Chat.
- The Machine kann deine Worte nicht verstehen: Überprüfe dein Mikrofon oder schreibe im Chat.
