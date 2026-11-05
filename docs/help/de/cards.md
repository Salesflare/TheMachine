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
- **Gerade erledigt**: ein letzter Schritt, den du bestätigt hast, etwa ein Formular absenden oder ein Issue anlegen, ist gelungen, während du weg warst. Er zeigt, was passiert ist, bis du auf **Verstanden** tippst, höchstens einen Tag, und dein Handy erfährt es auch. Danach steht er nur noch unter Erledigt.
- **Kommt später zurück**: zurückgestellt.
- **Versprechen**: was du versprochen hast und was andere dir versprochen haben. Siehe [Versprechen](promises.md).
- **Erledigt / verworfen**: jede abgeschlossene Aufgabe, die neueste zuerst, 30 auf einmal beim Scrollen. Aufgaben, die schon fertig aussehen, stehen oben, markiert mit **Scheinbar erledigt**.

In Bereit für dich, Braucht deine Entscheidung, Wird vorbereitet und Wartet auf andere steht eine Aufgabe, die überfällig ist oder bis morgen fällig ist, oben. Die übrigen kommen neueste zuerst, nach der Zeit, die jede Aufgabe zeigt. Die Seitenleiste hat dieselbe Reihenfolge.

Eine Aufgabe mit **Scheinbar erledigt** sieht aus wie eine erledigte, mit dem, was zeigt, dass sie erledigt ist, etwa "PR #3451 gemergt". Sie ist noch nicht geschlossen: **Wieder öffnen** setzt sie wieder auf deine Liste, und deine Machine lernt daraus. Sie sind nie überfällig und zählen nicht als wartend auf dich.

Eine Aufgabe, deren letzter Schritt noch bei jemand anderem offen ist, etwa ein Review, ein Merge oder eine Antwort, zeigt **Wartet auf:** diesen Schritt und bleibt offen. Sie wartet in **Wartet auf andere**, eingeklappt über Kommt später zurück, und zählt nicht als bereit für dich. Eine neue Nachricht dazu holt sie zurück.

**Alles erledigt** heißt, dass dich gerade nichts braucht. Die Zeile darunter sagt, wann deine Machine zuletzt nachgesehen hat.

**Alle**, **Arbeit** und **Privat** über der Liste in der Seitenleiste zeigen alle Aufgaben oder nur eine Art. Deine Machine merkt sich die Wahl, sodass Handy und Computer dieselbe Liste zeigen. Wenn Arbeit oder Privat aktiv ist, steht das oben in der Liste, mit **Alle anzeigen** zum Zurückgehen.

Eine Aufgabe in einem Projekt zeigt den Projektnamen in der Zeile unter ihrem Titel; er öffnet das Projekt. **Projekt** unter **Details** ändert es oder entfernt es. Siehe [Aufgaben eines Projekts](graph.md#a-projects-to-dos).

**Bereich** unter **Details** verschiebt die Aufgabe in deinen anderen Bereich, etwa eine private, die von deiner Arbeitsadresse aus rausgehen muss. Was sie lesen und wovon sie senden darf, zieht mit; die Nachrichten, aus denen sie kam, bleiben, wo sie sind. **Rückgängig** in der Meldung danach verschiebt sie zurück.

Braucht eine Aufgabe einen anderen Bereich, um weiterzukommen, fragt sie mit einer Schaltfläche **Nach Arbeit verschieben**. Nichts wird verschoben, bevor du tippst; danach macht sie von selbst weiter. Eine Aufgabe, die du ohne Arbeit oder Privat angelegt hast, verschiebt sich von selbst, sobald sie weiß, wohin sie gehört.

Startest du eine Aufgabe, darf sie die Nachrichten, aus denen sie kam, immer lesen, auch im Postfach einer anderen Firma. Braucht sie andere Nachrichten aus einem anderen Bereich, fragt sie mit **Diese E-Mail für diese Aufgabe verwenden**; ein Tippen fügt sie hinzu und sie macht weiter. Mail für eine andere deiner Firmen landet gleich bei den Aufgaben dieser Firma. Eine Aufgabe aus deinem eigenen Leben, etwa Familie, die an deine Arbeitsadresse schreibt, ist von Anfang an Privat.

## Die Buttons

Eine Aufgabe zeigt ihren nächsten Schritt, etwa **Ausführen** oder **Prüfen und senden**, mit **Zurückstellen** daneben. Siehe [Ausführen](do-it.md) und [Zurückstellen](snooze.md).

Noch nicht vorbereitet, hat sie **Anders angehen** (sag, wie es stattdessen gehen soll); fertig, **Änderungen anfragen** (sag, was im Entwurf anders sein soll). Ist die Zeile auf dem Handy voll, wandert **Zurückstellen** unter **…**. **Als erledigt markieren** (sie ist erledigt) gibt es auch: sichtbar ohne Entwurf, sonst oben unter **…**.

Soll sie anders erledigt werden, sag es in ihrem **Chat**.

Unter **…** (auf dem Handy öffnet sich das vom unteren Bildschirmrand):

- **Übergeben…**: Gib sie an ein Teammitglied, an [Claude Code oder Codex](hand-to-agent.md) (die du eingerichtet hast), oder [bitte jemanden um ein Review](ask-to-review.md).
- **Wiederholen…**: Sie [kommt in einem Rhythmus wieder](recurring.md).
- **Nicht nötig**: Sie verschwindet. Wähl auf Wunsch einen Grund: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Tippe auf den Titel oder auf **Name** unter **Details**, um sie umzubenennen. Dein Titel bleibt, auch wenn sich die Aufgabe ändert.

Eine geschlossene Aufgabe kommt mit **Wieder öffnen** zurück. Sie kommt auch von selbst zurück, wenn etwas Neues passiert, etwa eine neue Nachricht von der Person. Deine eigene Antwort holt sie nicht zurück.

Eine Aufgabe, die nur bis zu einem bestimmten Zeitpunkt zählte, etwa eine Bestätigung vor einem Meeting, schließt sich von selbst, sobald dieser Zeitpunkt vorbei ist. Sie wandert zu **Erledigt / verworfen** mit „Nicht mehr nötig“ und wann es war. **Rückgängig** holt sie einen Tag lang zurück.

Bei deinen ersten Aufgaben zeigt eine kurze Zeile unter den Buttons das Wichtigste: **Anders angehen** (oder **Änderungen anfragen**) und **Nicht nötig**, wenn eine Aufgabe nicht ganz passt, und bei deinem ersten fertigen Entwurf, dass nichts rausgeht, bevor du auf **Senden** tippst. Ein Tipp verschwindet für immer, sobald du seinen Button nutzt oder auf × tippst, auf all deinen Geräten.

An deinem ersten Tag begrüßt dich der Kopf von Aufgaben mit Namen und zeigt, wer am längsten auf deine Antwort wartet. Die Machine entwirft diese Antwort zuerst, damit sie bereitliegt, wenn du ankommst. Nichts geht raus, bevor du sie sendest. Die Zeile verschwindet nach deinem ersten Tag oder deiner ersten entschiedenen Aufgabe.

Jede Aufgabe beginnt mit ihrem Titel. Die Zeile darunter zeigt, um wen es geht, deren Organisation, das Projekt, Arbeit oder Privat (unter **Alle**) und wann sie kam, dazu ihren Stand, wenn ihre Gruppe ihn nicht schon nennt. Tippe auf einen Namen, um seine Seite im Graph zu öffnen.

Manchmal sagt eine dezente Zeile unter dem Text, was nicht bekannt ist, etwa „Letzter Kontakt vor 12 Tagen per E-Mail; seitdem nichts.“ Sie erscheint nur, wenn der letzte Austausch alt oder noch unbeantwortet ist, und nennt nicht verbundene Kanäle, über die vielleicht eine Antwort kam, etwa WhatsApp. Deine Machine bereitet mit denselben Fakten vor, also sagt sie, was sie nicht weiß, statt zu raten.

Ein Titel sagt, was zu tun ist. Er ändert sich nur, wenn sich das ändert, etwa bei einer neuen Bitte. Eine erledigte Aufgabe behält ihren Titel, darunter steht, wie sie ausging, etwa was rausging oder "Erledigt: Sam hat am Dienstag unterschrieben".

Über dem Entwurf nennt eine dezente Zeile die Nachricht, aus der sie stammt, mit dem Logo des Dienstes (Gmail, Slack, WhatsApp…). Tippe darauf, um den Verlauf zu lesen. Ein Chat (Slack, WhatsApp, Telegram, Intercom…) liest sich als ein Gespräch, älteste zuerst, jede Nachricht einmal; die Nachricht, um die es in der Aufgabe geht, hat eine dünne Linie daneben. Der Entwurf beginnt mit dem Logo, wohin er geht, so siehst du vor dem Lesen, ob es eine Slack-Antwort oder eine E-Mail ist. Ein Schritt ohne Entwurf, etwa eine Übergabe, zeigt das Logo auf seinem Button.

**Details** zeigt ihren Namen, ihr Projekt und ihren Bereich (tippe auf eins, um es zu ändern), deine letzte Notiz und das Ergebnis eines Coding-Agenten. **Chat ›** am Ende dieser Zeile öffnet den Chat. Eine erledigte Aufgabe bleibt kurz: ihr Titel, eine Zeile und was rausging; die Nachricht, aus der sie stammt, steht unter ihren **Details**.

Eine „Wartet auf“-Aufgabe (jemand hat dir etwas versprochen) verlinkt deine eigene letzte Nachricht an die Person, die, auf die du eine Antwort erwartest: „E-Mail an Pat · Di“.

## Selbst eine erstellen

**Neue Aufgabe** (auf einem Computer unter **Suchen**) legt eine Aufgabe für alles an. Beim Erstellen wird nichts gesendet. Ohne Arbeit oder Privat landet sie dort, wo sie hingehört: nach den Personen und dem Thema oder der E-Mail, auf die sie sich bezieht. The Machine sucht diese E-Mail in deinem Postfach, auch ältere, die sie noch nicht geholt hat.

- **Fällig**: Gib einen Tag oder eine Uhrzeit ein, etwa „morgen“, „nächsten Fr“, „3. Nov“, „15:00“, „in 2 Stunden“ oder „morgen um 9 Uhr“. Englisch geht auch („in 2 hours“, „tomorrow 9“). Das Kalendersymbol hat Schnellauswahlen wie beim Zurückstellen und **Datum wählen**.
- **E-Mail**: Häng die E-Mail an, um die es geht. Gesucht wird nur in deinen E-Mails, nach Betreff oder Absender.
- **Dateien**: Tippe auf die Büroklammer im Feld, füge einen Screenshot ein oder zieh Dateien auf das Formular. Auf dem Handy kannst du auch ein Foto machen. Bis zu 5 Dateien, dieselben Arten und Größen wie im Chat (siehe [Dateien hinzufügen](card-chat.md#add-files)). × nimmt eine wieder weg.

Die Dateien bleiben bei der Aufgabe: Sie erscheinen auf ihr und in ihrem Chat, und The Machine liest sie, wenn sie daran arbeitet.
