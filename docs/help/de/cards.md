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

- **Für dich**: alles, was auf dich wartet, das Dringendste zuerst. Jede Aufgabe zeigt **Vorbereitet** (die Arbeit ist getan, und **Ausführen** oder **Senden** erledigt sie) **Braucht dich** (zuerst deine Entscheidung oder eine Antwort) oder **Wird vorbereitet…** (deine Machine arbeitet daran).
- **Gerade erledigt**: ein letzter Schritt, den du bestätigt hast, etwa ein Formular absenden oder ein Issue anlegen, ist gelungen, während du weg warst. Er zeigt, was passiert ist, bis du auf **Verstanden** tippst, höchstens einen Tag, und dein Handy erfährt es auch. Danach steht er nur noch unter Erledigt.
- **Kommt später zurück**: zurückgestellt, und Aufgaben ohne Antwort auf **Noch nötig?** (unten).
- **Versprechen**: was du versprochen hast und was andere dir versprochen haben. Siehe [Versprechen](promises.md).
- **Erledigt / verworfen**: jede abgeschlossene Aufgabe, nach dem Zeitpunkt, an dem sie erledigt wurde, die neueste zuerst, 30 auf einmal beim Scrollen. Eine gerade gesendete Aufgabe steht oben, und jede sagt, wann, etwa „Erledigt vor 5 Minuten“. Aufgaben, die schon fertig aussehen, stehen dazwischen nach dem Zeitpunkt, ab dem sie so aussahen, markiert mit **Scheinbar erledigt**.

Nach dem Senden sagt ein kurzer Hinweis, wo die Aufgabe jetzt ist, etwa „Gesendet. Verschoben nach Erledigt.“ oder, wenn sie auf eine Antwort wartet, „Gesendet. Verschoben nach Später bis Mo.“ **Öffnen** bringt dich hin. Dass der E-Mail-Verlauf für ein paar Tage aus deinem Posteingang verschwindet, betrifft nur dein Postfach. Die Suche findet eine Aufgabe nach Titel oder Empfänger, auch in Später und Erledigt.

**Für dich** zeigt zuerst, was überfällig oder bis morgen fällig ist, dann Fragen aus deiner Fleet, dann der Rest. Darin jeweils neueste zuerst. Eine Aufgabe bleibt an ihrem Platz, während deine Machine sie vorbereitet und wenn sie fertig ist: Nur ihre Markierung ändert sich. Die anderen offenen Gruppen zeigen Überfälliges oder bis morgen Fälliges oben, den Rest neueste zuerst. Die Seitenleiste hat dieselbe Reihenfolge.

Eine Aufgabe mit **Scheinbar erledigt** sieht aus wie eine erledigte, mit dem, was zeigt, dass sie erledigt ist, etwa "PR #3451 gemergt". Sie ist noch nicht geschlossen: **Wieder öffnen** setzt sie wieder auf deine Liste, und deine Machine lernt daraus. Sie sind nie überfällig und zählen nicht als wartend auf dich. Eine Aufgabe mit einem Antwortentwurf scheint auch erledigt, wenn du in dieser Unterhaltung selbst geantwortet hast, etwa in Gmail oder Slack.

Eine Aufgabe, deren letzter Schritt noch bei jemand anderem offen ist, etwa ein Review, ein Merge oder eine Antwort, zeigt **Wartet auf:** diesen Schritt und bleibt offen. Sie wartet in **Wartet auf andere**, eingeklappt über Kommt später zurück, und zählt nicht als bereit für dich. Eine neue Nachricht dazu holt sie zurück. Das gilt auch, wenn du zurückgefragt hast: Sie kommt am Morgen vor ihrer Frist zurück, zur Frist, wenn sie später am Tag ist, oder am nächsten Morgen, wenn sie vorbei ist, und sagt, auf wen sie noch wartet.

Geht es bei einer Aufgabe um ein Ergebnis, das jemand anderes liefert, etwa einen unterschriebenen Vertrag oder eine Zahlung, zeigen ihre **Details** dieses Ergebnis als **Fertig, wenn**. Deinen Teil zu senden schließt sie nicht: Sie wartet in **Wartet auf andere**, bis eine Nachricht das Ergebnis zeigt, und schließt sich dann selbst, mit **Rückgängig**. Kommt bis zum Nachhaken nichts, kommt sie mit **Schreib eine kurze Erinnerung** in ihrem Chat zurück. Was als fertig zählt, änderst du, indem du es im Chat sagst.

Eine Aufgabe, die eine Woche niemand angefasst hat, fragt einmal: **Noch nötig?** **Nicht nötig** schließt sie, mit **Rückgängig**. **Behalten** behält sie, und sie fragt nie wieder. Öffnen, eine Chatnachricht, eine Änderung, Zurückstellen oder eine neue Nachricht dazu zählen als Anfassen. Kommt eine weitere Woche keine Antwort, wandert sie in Kommt später zurück, unter Noch nötig?, statt zu verschwinden. Dann zählen auch die Zahl am App-Symbol und die morgendliche Zusammenfassung sie nicht mehr mit. Anfassen holt sie zurück.

Wenn dich nichts braucht, macht deine Machine auf der leeren Liste ein Nickerchen. Während sie prüft, wird sie wach und sagt es. Ist eine Prüfung fehlgeschlagen oder spät dran, sagt ihre Zeile das, mit **Jetzt prüfen** darunter.

**Alle**, **Arbeit** und **Privat** über der Liste in der Seitenleiste zeigen alle Aufgaben oder nur eine Art. Deine Machine merkt sich die Wahl, sodass Handy und Computer dieselbe Liste zeigen. Wenn Arbeit oder Privat aktiv ist, steht das oben in der Liste, mit **Alle anzeigen** zum Zurückgehen.

Eine Aufgabe in einem Projekt zeigt den Projektnamen in der Zeile unter ihrem Titel; er öffnet das Projekt. **Projekt** unter **Details** ändert es oder entfernt es. Siehe [Aufgaben eines Projekts](projects.md#a-projects-to-dos).

**Bereich** unter **Details** verschiebt die Aufgabe in deinen anderen Bereich. Was sie lesen und wovon sie senden darf, zieht mit; die Nachrichten, aus denen sie kam, bleiben, wo sie sind. **Rückgängig** in der Meldung danach verschiebt sie zurück.

Braucht eine Aufgabe einen anderen Bereich, um weiterzukommen, und kamen ihre Nachrichten alle von dort, verschiebt sie sich von selbst und macht weiter. Sonst fragt sie mit einer Schaltfläche **Nach Arbeit verschieben**. Nichts wird verschoben, bevor du tippst; danach macht sie von selbst weiter. Eine Aufgabe, die du ohne Arbeit oder Privat angelegt hast, verschiebt sich von selbst, sobald sie weiß, wohin sie gehört.

Startest du eine Aufgabe, darf sie die Nachrichten, aus denen sie kam, immer lesen, auch im Postfach einer anderen Firma. Braucht sie andere Nachrichten aus einem anderen Bereich, fragt sie mit **Diese E-Mail für diese Aufgabe verwenden**; ein Tippen fügt sie hinzu und sie macht weiter. Mail für eine andere deiner Firmen landet gleich bei den Aufgaben dieser Firma. Eine Aufgabe aus deinem eigenen Leben, etwa Familie, die an deine Arbeitsadresse schreibt, ist von Anfang an Privat.

Die Antwort geht trotzdem von der Arbeitsadresse, an der sie ankam, und sie erscheint nie in einer Work Fleet oder im Team-Graph.

Ab zwei wartenden Aufgaben geht **Durchgehen** in der Überschrift von Für dich sie einzeln durch, in der Reihenfolge der Liste, jeden Entwurf vollständig, mit **Senden** oder **Ausführen**, **Änderungen anfragen**, **Zurückstellen** und **Überspringen**. Am Computer sendet Enter, was zu sehen ist, `S` stellt zurück, `→` überspringt und Esc hört auf. Unter dem Titel sagt die Überschrift auch, wie lange sie in deinem Tempo dauern, etwa "etwa 2 Min.".

Eine Aufgabe, die dich etwas fragt, zählt bei beidem nicht mit: Sie braucht deine Antwort, keinen Klick.

## Jetzt prüfen

Deine Machine liest jede Quelle alle paar Minuten, Tag und Nacht, und prüft das Neue auf Aufgaben, sobald 40 Nachrichten warten oder die älteste Nachricht von einer Person 15 Minuten gewartet hat. Newsletter, Benachrichtigungen und Belege kommen in die nächste Prüfung, innerhalb einer Stunde.

**Jetzt prüfen** liest sofort jede Quelle. Ist nichts offen, tippe auf die Zeile deiner Machine, um es zu sehen, mit **Details**, das Prüfungen unter Verbindungen öffnet. Sind Aufgaben offen, steht es auf einem Computer oben. Eine kurze Zeile dort erscheint nur, während eine Prüfung läuft oder wenn eine fehlgeschlagen oder spät dran ist. Du kannst auch im Chat fragen.

LinkedIn, X und Salesflare behalten ihr eigenes Tempo.

## Letzte Prüfung

Nach einer Prüfung, die neue Nachrichten gelesen hat, sagt eine Zeile über deinen Aufgaben, was sie aus allen Quellen gefunden hat, etwa „13 Nachrichten um 16:11 geprüft · nichts braucht dich“ oder „· 2 neue Aufgaben“. Wartet eine neue Aufgabe auf einen besseren Moment, etwa deine Morgenübersicht, steht dort, bis wann: „1 Aufgabe wartet bis morgen 08:30“.

Tippe auf die Zeile, um jeden E-Mail-Verlauf, Chat und jede Benachrichtigung mit dem Symbol ihrer Quelle zu sehen: wer geschrieben hat, den Betreff oder die ersten Worte und die neue Aufgabe oder warum nichts nötig war, etwa „Nur in Kopie, ein Teammitglied antwortet“ oder „Treffen steht schon für Donnerstag“. Ein Verlauf zeigt keinen Grund, wenn die Prüfung nur einen vagen hatte. Tippe auf einen Eintrag, um ihn zu lesen. Die Zeile bleibt 12 Stunden nach der Prüfung stehen.

Sie zählt nur E-Mails an dich. Deine eigenen Antworten werden für den Zusammenhang und Zusagen gelesen, sind aber keine neuen E-Mails. Die eigenen E-Mails deiner Machine an dich, etwa deine Morgenübersicht oder ein Hinweis auf eine Korrektur, werden nie gelesen oder aufgeführt. E-Mails zu Zahlungen, deiner Testphase oder einer Einladung werden wie gewohnt gelesen.

## Die Buttons

Eine Aufgabe zeigt ihren nächsten Schritt, etwa **Ausführen** oder **Prüfen und senden**, mit **Zurückstellen** daneben. Siehe [Ausführen](do-it.md) und [Zurückstellen](snooze.md).

**Änderungen anfragen** sagt, was anders sein soll: wie es gehen soll, oder, sobald ein Entwurf fertig ist, was darin anders sein soll. Ist die Zeile auf dem Handy voll, wandert **Zurückstellen** unter **…**. **Als erledigt markieren** (sie ist erledigt) gibt es auch: sichtbar bei einer fertigen ohne Entwurf, sonst oben unter **…**, auch bei einer, die deine Entscheidung braucht. Sie verschwindet sofort aus der Liste, mit **Rückgängig** in der Meldung. Wisch die Meldung weg oder zieh sie mit der Maus weg, um sie früher zu schließen. Die Änderung bleibt.

Soll sie anders erledigt werden, sag es in ihrem **Chat**.

Unter **…** (auf dem Handy öffnet sich das vom unteren Bildschirmrand):

- **Übergeben…**: Gib sie an ein Teammitglied, an [Claude Code oder Codex](hand-to-agent.md) (die du eingerichtet hast), oder [bitte jemanden um ein Review](ask-to-review.md).
- **Wiederholen…**: Sie [kommt in einem Rhythmus wieder](recurring.md).
- **Nicht nötig**: Sie verschwindet. Wähl auf Wunsch einen Grund: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Tippe auf den Titel oder auf **Name** unter **Details**, um sie umzubenennen. Dein Titel bleibt, auch wenn sich die Aufgabe ändert.

Eine geschlossene Aufgabe kommt mit **Wieder öffnen** zurück. Sie kommt auch von selbst zurück, wenn etwas Neues passiert, etwa eine neue Nachricht von der Person. Deine eigene Antwort holt sie nicht zurück.

Eine Aufgabe, die nur bis zu einem bestimmten Zeitpunkt zählte, etwa eine Bestätigung vor einem Meeting, schließt sich von selbst, sobald dieser Zeitpunkt vorbei ist. Sie wandert zu **Erledigt / verworfen** mit „Nicht mehr nötig“ und wann es war. **Rückgängig** holt sie einen Tag lang zurück.

Bevor eine Nachricht oder Übergabe an jemanden als bereit erscheint, prüft deine Machine deine letzten Chats mit den Beteiligten, auch Gruppenchats, und wartet, bis Slack sie gelesen hat. Zeigt eine spätere Nachricht, dass es schon erledigt ist, etwa weil die Person gefragt wurde und zugesagt hat, schließt sich die Aufgabe von selbst. **Rückgängig** holt sie einen Tag lang zurück.

Wenn eine neuere Nachricht den Plan ändert, etwa ein Fest an einem anderen Ort oder eine abgesagte Buchung, passt The Machine ihre Aufgaben selbst an. Eine, die noch zählt, folgt dem neuen Plan. Eine, bei der nichts mehr zu tun ist, wandert als "Nicht nötig" zu **Erledigt / verworfen**, ihr Chat sagt "Aktualisiert:" und warum, und **Rückgängig** holt sie einen Tag lang zurück.

Bei deinen ersten Aufgaben zeigt eine kurze Zeile unter den Buttons das Wichtigste: **Änderungen anfragen** und **Nicht nötig**, wenn eine Aufgabe nicht ganz passt, und bei deinem ersten fertigen Entwurf, dass nichts rausgeht, bevor du auf **Senden** tippst. Ein Tipp verschwindet für immer, sobald du seinen Button nutzt oder auf × tippst, auf all deinen Geräten.

An deinem ersten Tag begrüßt dich der Kopf von Aufgaben mit Namen und zeigt, wer am längsten auf deine Antwort wartet. Die Machine entwirft diese Antwort zuerst, damit sie bereitliegt, wenn du ankommst. Nichts geht raus, bevor du sie sendest. Die Zeile verschwindet nach deinem ersten Tag oder deiner ersten entschiedenen Aufgabe.

Jede Aufgabe beginnt mit ihrem Titel. Die Zeile darunter zeigt, um wen es geht, die Organisation, wenn es um eine geht (nie nur, weil jemand dort arbeitet), das Projekt, Arbeit oder Privat (unter **Alle**) und wann sie kam, dazu ihren Stand, wenn ihre Gruppe ihn nicht schon nennt. Tippe auf einen Namen, um seine Seite im Graph zu öffnen.

Manchmal sagt eine dezente Zeile unter dem Text, was nicht bekannt ist, etwa „Letzter Kontakt vor 12 Tagen per E-Mail; seitdem nichts.“ Sie erscheint nur, wenn der letzte Austausch alt oder noch unbeantwortet ist, und nennt nicht verbundene Kanäle, über die vielleicht eine Antwort kam, etwa WhatsApp. Deine Machine bereitet mit denselben Fakten vor, also sagt sie, was sie nicht weiß, statt zu raten.

Nennt die Zeile einen nicht verbundenen Kanal, öffnet Verbinden daneben diese Verbindung.

Ein Titel sagt, was zu tun ist. Er ändert sich nur, wenn sich das ändert, etwa bei einer neuen Bitte. Eine erledigte Aufgabe behält ihren Titel, darunter steht, wie sie ausging, etwa was rausging oder "Erledigt: Sam hat am Dienstag unterschrieben".

Über dem Entwurf nennt eine dezente Zeile die Nachricht, aus der sie stammt, mit dem Logo des Dienstes (Gmail, Slack, WhatsApp…). Tippe darauf, um den Verlauf zu lesen. Der Entwurf beginnt mit dem Logo, wohin er geht, so siehst du vor dem Lesen, ob es eine Slack-Antwort oder eine E-Mail ist. Ein Schritt ohne Entwurf, etwa eine Übergabe, zeigt das Logo auf seinem Button.

Folgt der Entwurf dem Hinweis von jemand anderem in einer anderen Nachricht, etwa dem Vorschlag einer Kollegin in Slack, sagt eine Zeile unter der Aufgabe das, etwa „Laut Sam in #ops“. Tippe darauf, um diese Nachricht hier zu lesen, mit In Slack oder Gmail öffnen darin. Ist diese Nachricht die Quelle der Aufgabe selbst, zeigt die Quellzeile sie schon, also gibt es keine zweite Zeile.

Ein Chat (Slack, WhatsApp, Telegram, Intercom…) liest sich als ein Gespräch, älteste zuerst, jede Nachricht einmal; die Nachricht, um die es in der Aufgabe geht, hat eine dünne Linie daneben.

**Details** zeigt ihren Namen, ihr Projekt und ihren Bereich (tippe auf eins, um es zu ändern), deine letzte Notiz und das Ergebnis eines Coding-Agenten. **Chat ›** am Ende dieser Zeile öffnet den Chat. Eine erledigte Aufgabe bleibt kurz: ihr Titel, eine Zeile und was rausging; die Nachricht, aus der sie stammt, steht unter ihren **Details**.

Eine „Wartet auf“-Aufgabe (jemand hat dir etwas versprochen) verlinkt deine eigene letzte Nachricht an die Person, die, auf die du eine Antwort erwartest: „E-Mail an Pat · Di“.

## Selbst eine erstellen

**Neue Aufgabe** (auf einem Computer unter **Suchen**) legt eine Aufgabe für alles an. Beim Erstellen wird nichts gesendet. Ohne Arbeit oder Privat landet sie dort, wo sie hingehört: nach den Personen und dem Thema, einer Firma oder einem Postfach, das sie nennt, oder der E-Mail, auf die sie sich bezieht. Wenn nichts darauf hinweist, landet sie dort, wo die meisten deiner Aufgaben sind. The Machine sucht diese E-Mail in deinem Postfach, auch ältere, die sie noch nicht geholt hat.

- **Fällig**: Gib einen Tag oder eine Uhrzeit ein, etwa „morgen“, „nächsten Fr“, „3. Nov“, „15:00“, „in 2 Stunden“ oder „morgen um 9 Uhr“. Englisch geht auch („in 2 hours“, „tomorrow 9“). Das Kalendersymbol hat Schnellauswahlen wie beim Zurückstellen und **Datum wählen**.
- **Nachricht**: Häng die Nachricht an, um die es geht: eine E-Mail, Slack, Teams, WhatsApp, Telegram oder jede andere Nachricht, die The Machine hat. Gesucht wird nach Text oder Absender. Jeder Treffer zeigt, woher er kommt, wer ihn geschickt hat und wann.
- **Dateien**: Tippe auf die Büroklammer im Feld, füge einen Screenshot ein oder zieh Dateien auf das Formular. Auf dem Handy kannst du auch ein Foto machen. Bis zu 5 Dateien, dieselben Arten und Größen wie im Chat (siehe [Dateien hinzufügen](card-chat.md#add-files)). × nimmt eine wieder weg.

Die Dateien bleiben bei der Aufgabe: Sie erscheinen auf ihr und in ihrem Chat, und The Machine liest sie, wenn sie daran arbeitet. Dateien allein reichen: The Machine liest den Text eines PDFs oder einer Textdatei und füllt die Aufgabe daraus aus.
