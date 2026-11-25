---
title: Live sprechen
area: cards
summary: Ein gesprochenes Gespräch mit The Machine über eine Aufgabe, mit der Stimme von OpenAI. Es findet im Chat der Aufgabe statt. Ein Entwurf wird erst gesendet, wenn du zustimmst.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
translated: da63957f0556ff4f
---
## Ein Gespräch beginnen

Tippe im Chat einer Aufgabe auf die Welle neben dem Mikrofon und erlaube den Zugriff auf das Mikrofon, falls du dazu aufgefordert wirst. Wenn in der Leiste **Live** steht, kannst du wie bei einem Anruf sprechen. The Machine antwortet laut. Sprich einfach dazwischen, um sie zu unterbrechen.

Sie kennt diese Aufgabe: ihre Nachrichten, ihren Entwurf und ihren Chat. Außerdem kann sie deine anderen Aufgaben nachschlagen. Sag „Markiere diese Aufgabe als erledigt“, „Stell sie bis morgen um 9 Uhr zurück“ oder „Nicht nötig“, und sie führt es aus. Sag direkt danach „Nein, nicht das“, um es rückgängig zu machen. Die Zeiten richten sich nach der Zeitzone deiner [Arbeitszeiten](work-hours.md).

Sie hört auf die Sprache der App und auf die Sprachen, die dein Browser aufführt. Husten, Geräusche und andere Sprachen bleiben unbeantwortet und erscheinen nicht im Transkript.

In der Leiste gibt es **Stummschalten** und **Beenden**. Sag „Tschüss“, und das Gespräch endet von selbst. Ein Gespräch dauert bis zu 10 Minuten. In der letzten Minute läuft ein Countdown. Starte erneut, um weiterzusprechen.

## Mit all deinen Aufgaben sprechen

Tippe in der Seitenleiste auf **Sprechen** (auf dem Handy im Menü). The Machine sagt dir, wie viele Aufgaben warten, und geht die Aufgaben unter **Für dich** der Reihe nach durch, wie sie in deiner Liste stehen. Bei einer Aufgabe mit dem Status **Wird vorbereitet…** sagt sie dir, sobald sie bereit ist.

Für das Gespräch gibt es eine eigene Seite: Die aktuelle Aufgabe steht oben, zusammen mit ihrem Entwurf und **Chat öffnen**.

Bitte sie, einen Entwurf vorzulesen oder zu ändern, eine Aufgabe zurückzustellen, als erledigt zu markieren oder zur nächsten Aufgabe zu wechseln. Was du über eine Aufgabe sagst, kommt in ihren Chat. In einer Pause weist sie dich auf neue Aufgaben hin. Sag „Füge eine Aufgabe hinzu …“, um eine hinzuzufügen, ohne den Überblick zu verlieren.

Frag nach einer Person, Organisation, einem Projekt, Meeting oder Versprechen. The Machine sucht danach und zeigt es dir. Sie kann auch Aufgaben verwerfen, umbenennen oder wieder öffnen, auch solche unter **Erledigt / verworfen**. Bei allen anderen Fragen gibt sie die Frage an den Chat einer neuen Aufgabe weiter und nennt dir die Antwort.

Sie erinnert sich an eure früheren Gespräche. Frag zum Beispiel „Was hatte ich zum Offsite entschieden?“, und sie sagt es dir und wann du es gesagt hast. Das funktioniert nur über **Sprechen** in der Seitenleiste.

In der Zwischenzeit kannst du andere Seiten öffnen: Die Leiste bleibt unten, und über **Sprechen** kommst du zurück. Dieses Gespräch dauert bis zu 30 Minuten. Auf Computern und Android läuft es im Hintergrund weiter. Auf dem iPhone wird es beendet, sobald die App nicht mehr auf dem Bildschirm ist.

## Etwas anfordern und mit Ja senden

Bitte um etwas, zum Beispiel „Schreib eine Antwort, dass Donnerstag passt“. The Machine gibt die Bitte an den Chat der Aufgabe weiter, als hättest du sie selbst eingegeben. Für den Chat gelten die üblichen Regeln.

Der Chat kann auch Dinge nachschlagen, zum Beispiel die Öffnungszeiten eines Geschäfts. Er zeigt dir, dass er gerade etwas nachsieht, und du kannst währenddessen weitersprechen. Sobald die Antwort bereit ist, sagt The Machine dir Bescheid und auch, wo sie die Information gefunden hat.

Sag Bescheid, wenn du einen Entwurf senden möchtest. The Machine liest ihn laut vor, also den Empfänger, den Betreff und den Text, und fragt zum Beispiel: „Diese Antwort per E-Mail an Sam senden?“ Das funktioniert auch, wenn dein Handy in der Tasche ist. Sag klar Ja, zum Beispiel „Ja, sende sie“, und der Entwurf wird gesendet.

- Sie sendet genau den Entwurf vor, den sie vorgelesen hat. Ändert sich der Entwurf, liest sie ihn erneut vor und fragt noch einmal. Eine Frage, die du nicht innerhalb von 3 Minuten beantwortest, läuft ab.
- Ohne ein klares Ja wird nichts gesendet.
- Einen Entwurf, den du bereits gesehen oder gehört hast, liest sie nicht noch einmal vor. Sie fragt nur, zum Beispiel: „An Pat senden?“
- Sag „Sende alle bereiten Entwürfe“, und sie nennt alle Empfänger in einer Frage. Ein Ja sendet sie alle.
- Nach deinem Ja zeigt Sprechen **Rückgängig** mit einem Countdown an. Tippe darauf oder sag „Rückgängig“ oder „Warte“.
- Nach dem Senden sagt Sprechen „Gesendet.“ und bei der Aufgabe steht **Gesendet an** die betreffende Person, zusammen mit der Uhrzeit. Falls das Senden fehlschlägt, sagt Sprechen warum. Frag jederzeit „Wurde es gesendet?“. The Machine prüft es, statt zu raten.

Du kannst auch auf **Freigeben** tippen.

Sag „Führ es aus“, um The Machine mit der Aufgabe zu starten, wie mit **Ausführen**. Sag „Fehler melden“, um einen Fehlerbericht zu senden, wie über **Fehler melden** in der Hilfe.

## Eine Stimme auswählen

Wähle unter **Einstellungen**, **Allgemein** und **Spracheingabe** eine **Stimme** aus und tippe auf Wiedergabe, um sie anzuhören. **Cedar** ist die Standardstimme. Die Cove-Stimme von ChatGPT ist nicht verfügbar.

## Ein Eintrag im Chat

Alles Gesagte erscheint im Chat der Aufgabe unter einer Zeile mit **Live gesprochen**, damit du es später nachlesen kannst.

## Voraussetzungen

Für Live sprechen wird die Stimme von OpenAI verwendet. Deine Machine braucht daher eine dieser Optionen:

- Eine Anmeldung bei ChatGPT: in den Tarifen enthalten, die diese Option anbieten.
- Einen OpenAI-API-Schlüssel: OpenAI berechnet die Nutzung pro Minute. In der Leiste wird darauf hingewiesen. Wenn du beides hast, verwendet deine Machine den Schlüssel.

Unter **Einstellungen**, **Allgemein** und **Spracheingabe** siehst du, ob Live sprechen bereit ist. Ohne OpenAI wird die Welle nicht angezeigt. Deine Audiodaten gehen direkt von deinem Browser an OpenAI.

## Wenn es nicht funktioniert

- **Das Mikrofon ist gesperrt**: Erlaube den Zugriff auf das Mikrofon für diese Website in den Einstellungen deines Browsers.
- **Live sprechen konnte nicht gestartet werden**: Prüfe deine Anmeldung bei ChatGPT oder deinen OpenAI-Schlüssel und versuche es noch einmal.
- **Live sprechen hat die Verbindung verloren**: Starte erneut. Alles Gesagte bleibt im Chat.
- Wenn die Meldung erscheint, dass deine Worte nicht verstanden werden: Prüfe dein Mikrofon oder schreibe im Chat.
