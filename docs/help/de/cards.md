---
title: Aufgaben
area: cards
summary: Eine Aufgabe für jede Sache, die dich braucht, bereit für dein Ja. Was die Teile einer Aufgabe bedeuten.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
---
Deine Machine liest alles Neue und erstellt nur dann eine Aufgabe, wenn etwas dich braucht. Eine Aufgabe pro Angelegenheit, egal über wie viele Nachrichten sie geht.

## Wo Aufgaben stehen

Die Seite **Aufgaben** gruppiert sie:

- **Bereit für dich**: vorbereitet und wartet auf deine Freigabe.
- **Braucht deine Entscheidung**: etwas, das nur du entscheiden kannst.
- **Wird vorbereitet**: Deine Machine arbeitet daran. Eine Aufgabe, zu der du gerade **Ausführen** gesagt hast, bleibt an ihrem Platz, während sie vorbereitet wird, und wandert dann zu **Bereit für dich**.
- **Kommt später zurück**: zurückgestellt.
- **Versprechen**: was du versprochen hast und was andere dir versprochen haben. Siehe [Versprechen](promises.md).
- **Scheinbar erledigt**: Aufgaben, die schon fertig aussehen. Eingeklappt, direkt über **Erledigt / verworfen**.
- **Erledigt / verworfen**: jede abgeschlossene Aufgabe, die neueste zuerst, 30 auf einmal beim Scrollen.

Unter **Scheinbar erledigt** ist jede Aufgabe eine Zeile: ihr Titel und was zeigt, dass sie erledigt ist, etwa "PR #3451 gemergt". **Erledigt** schließt eine, **Alle als erledigt markieren** schließt alle (mit **Rückgängig**), und **Nicht erledigt** macht sie wieder zu einer normalen Aufgabe, damit deine Machine daraus lernt. Tipp auf eine Zeile, um die ganze Aufgabe zu sehen. Sie sind nie überfällig und zählen nicht als wartend auf dich. Nichts wird ohne dich geschlossen.

Eine Aufgabe, deren letzter Schritt noch bei jemand anderem offen ist, etwa ein Review, ein Merge oder eine Antwort, zeigt **Wartet auf:** diesen Schritt und bleibt offen. Sie wartet in **Wartet auf andere**, eingeklappt über Kommt später zurück, und zählt nicht als bereit für dich. Eine neue Nachricht dazu holt sie zurück.

**Alles erledigt** heißt, dass dich gerade nichts braucht. Die Zeile darunter sagt, wann deine Machine zuletzt nachgesehen hat.

**Alle**, **Arbeit** und **Privat** über der Liste in der Seitenleiste zeigen alle Aufgaben oder nur eine Art. Deine Machine merkt sich die Wahl, sodass Handy und Computer dieselbe Liste zeigen. Wenn Arbeit oder Privat aktiv ist, steht das oben in der Liste, mit **Alle anzeigen** zum Zurückgehen.

Eine Aufgabe in einem Projekt zeigt den Projektnamen in der Zeile unter ihrem Titel; er öffnet das Projekt. **Projekt ändern** unter **Mehr** ändert es (bei einer erledigten Aufgabe unter **Details**). Siehe [Aufgaben eines Projekts](graph.md#a-projects-to-dos).

## Die Buttons

Eine neue Aufgabe hat **Ausführen**, **Als erledigt markieren**, **Zurückstellen**, **Anders ausführen** und **Nicht nötig**. Nur ein paar sind gleichzeitig zu sehen. Der Rest steht unter **Mehr**, zusammen mit **Umbenennen**.

- **Ausführen**: Deine Machine bereitet sie vor. Siehe [Ausführen](do-it.md).
- **Als erledigt markieren**: Sie ist erledigt.
- **Zurückstellen**: Hol sie später zurück. Siehe [Zurückstellen](snooze.md).
- **Anders ausführen**: Sag in ein paar Worten, was du stattdessen möchtest. Bei einer vorbereiteten Aufgabe heißt das **Änderungen anfragen**: Sag, was im Entwurf anders sein soll, und sie macht ihn neu. **Prüfen und senden** bleibt daneben.
- **Nicht nötig**: Sie verschwindet. Wähl auf Wunsch einen Grund: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Eine geschlossene Aufgabe kommt mit **Wieder öffnen** zurück. Sie kommt auch von selbst zurück, wenn etwas Neues passiert, etwa eine neue Nachricht von der Person. Deine eigene Antwort holt sie nicht zurück.

Eine Aufgabe, die nur bis zu einem bestimmten Zeitpunkt zählte, etwa eine Bestätigung vor einem Meeting, schließt sich von selbst, sobald dieser Zeitpunkt vorbei ist. Sie wandert zu den erledigten mit „Nicht mehr nötig“ und wann es war. **Rückgängig** holt sie einen Tag lang zurück.

Bei deinen ersten Aufgaben zeigt eine kurze Zeile unter den Buttons das Wichtigste: **Anders ausführen** (oder **Änderungen anfragen**) und **Nicht nötig**, wenn eine Aufgabe nicht ganz passt, und bei deinem ersten fertigen Entwurf, dass nichts rausgeht, bevor du auf **Senden** tippst. Ein Tipp verschwindet für immer, sobald du seinen Button nutzt oder auf × tippst, auf all deinen Geräten.

Jede Aufgabe beginnt mit ihrem Titel. Die Zeile darunter zeigt, um wen es geht, deren Organisation, das Projekt, Arbeit oder Privat (unter **Alle**) und wann sie kam, dazu ihren Stand, wenn ihre Gruppe ihn nicht schon nennt. Tippe auf einen Namen, um seine Seite im Graph zu öffnen.

Manchmal sagt eine dezente Zeile unter dem Text, was nicht bekannt ist, etwa „Letzter Kontakt vor 12 Tagen per E-Mail; seitdem nichts.“ Sie erscheint nur, wenn der letzte Austausch alt oder noch unbeantwortet ist, und nennt nicht verbundene Kanäle, über die vielleicht eine Antwort kam, etwa WhatsApp. Deine Machine bereitet mit denselben Fakten vor, also sagt sie, was sie nicht weiß, statt zu raten.

Ein Titel sagt, was zu tun ist. Er ändert sich nur, wenn sich das ändert, etwa bei einer neuen Bitte. Eine erledigte Aufgabe behält ihren Titel, darunter steht, wie sie ausging, etwa was rausging oder "Erledigt: Sam hat am Dienstag unterschrieben".

**Details** zeigt die Nachricht, aus der sie stammt (tippe darauf, um den Verlauf zu lesen), deine letzte Notiz und das Ergebnis eines Coding-Agenten. **Chat ›** am Ende dieser Zeile öffnet den Chat. Eine erledigte Aufgabe bleibt kurz: ihr Titel, eine Zeile und was rausging.

Eine „Wartet auf“-Aufgabe (jemand hat dir etwas versprochen) verlinkt deine eigene letzte Nachricht an die Person, die, auf die du eine Antwort erwartest: „E-Mail an Pat · Di“.

## Selbst eine erstellen

**Neue Aufgabe** (auf einem Computer unter **Suchen**) legt eine Aufgabe für alles an. Beim Erstellen wird nichts gesendet.

- **Fällig**: Gib einen Tag oder eine Uhrzeit ein, etwa „morgen“, „nächsten Fr“, „3. Nov“, „15:00“, „in 2 Stunden“ oder „morgen um 9 Uhr“. Englisch geht auch („in 2 hours“, „tomorrow 9“). Das Kalendersymbol hat Schnellauswahlen wie beim Zurückstellen und **Datum wählen**.
- **E-Mail**: Häng die E-Mail an, um die es geht. Gesucht wird nur in deinen E-Mails, nach Betreff oder Absender.
- **Dateien**: Tippe auf die Büroklammer im Feld, füge einen Screenshot ein oder zieh Dateien auf das Formular. Auf dem Handy kannst du auch ein Foto machen. Bis zu 5 Dateien, dieselben Arten und Größen wie im Chat (siehe [Dateien hinzufügen](card-chat.md#add-files)). × nimmt eine wieder weg.

Die Dateien bleiben bei der Aufgabe: Sie erscheinen auf ihr und in ihrem Chat, und The Machine liest sie, wenn sie daran arbeitet.
