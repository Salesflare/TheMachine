---
title: Aufgaben
area: cards
summary: Eine Aufgabe pro Sache, die dich braucht, bereit für dein Okay. Was die einzelnen Teile einer Aufgabe bedeuten.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: c54b334f5764bdf9
---
Deine Machine liest alles Neue und erstellt nur dann eine Aufgabe, wenn etwas dich braucht. Eine Aufgabe pro Anliegen, egal über wie viele Nachrichten es sich erstreckt.

## Wo Aufgaben zu finden sind

Auf der Seite **Aufgaben** sind sie gruppiert:

- **Gerade erledigt**: Ganz oben findest du einen letzten Schritt, den du bestätigt hast, zum Beispiel ein Formular oder ein Issue, der durchgegangen ist, während du weg warst. Er bleibt, bis du auf **Verstanden** tippst, höchstens einen Tag, und auch dein Handy erfährt davon.
- **Für dich**: Alles, worauf du reagieren musst, nach Dringlichkeit sortiert. Bei jeder Aufgabe steht **Vorbereitet** (die Arbeit ist erledigt, und mit **Ausführen** oder **Senden** wird sie abgeschlossen), **Braucht dich** (zuerst braucht es deine Entscheidung oder Antwort), **Wird vorbereitet…** (deine Machine arbeitet daran) oder **Zum Lesen** (eine Zusammenfassung oder ein Briefing, bei dem nichts entschieden werden muss).
- **Wartet auf andere**: Aufgaben, bei denen der nächste Schritt bei jemand anderem liegt, sind eingeklappt (siehe unten).
- **Kommt später zurück**: Zurückgestellte Aufgaben und solche, auf die niemand mit **Noch nötig?** geantwortet hat (siehe unten).
- **Versprechen**: Was du versprochen hast und was andere dir versprochen haben. Mehr dazu unter [Versprechen](promises.md).
- **Erledigt / verworfen**: Alle abgeschlossenen Aufgaben, die neuesten zuerst. Dabei steht, wann sie abgeschlossen wurden, zum Beispiel „Erledigt vor 5 Minuten“. Aufgaben, die offenbar schon erledigt sind, sind mit **Sieht erledigt aus** markiert.

Nach dem Senden steht in einer kurzen Meldung, wohin die Aufgabe verschoben wurde, zum Beispiel „Gesendet. Nach ‚Erledigt‘ verschoben.“ oder „Gesendet. Bis Mo. nach ‚Später‘ verschoben.“ Eine Antwort, die die Arbeit nur verspricht, etwa „Ich schicke es bis Dienstag“, lässt die Aufgabe offen: „Gesendet. Bleibt offen.“ Mit **Öffnen** gelangst du zur Aufgabe. Über die Suche findest du Aufgaben nach Titel oder Empfänger, auch unter Später und Erledigt.

Unter **Für dich** stehen zuerst Aufgaben, die überfällig sind oder bis morgen fällig werden, dann Fragen aus deiner Fleet, anschließend Nachfassaktionen zu einem Board und danach der Rest. Innerhalb jeder Gruppe stehen die neuesten zuerst. Eine Aufgabe behält ihren Platz, während deine Machine sie vorbereitet und wenn sie erledigt ist. Nur ihre Markierung ändert sich. In den anderen offenen Gruppen stehen überfällige oder bis morgen fällige Aufgaben zuerst, der Rest ist nach Aktualität sortiert. Die Seitenleiste behält dieselbe Reihenfolge bei.

**Sieht erledigt aus** bedeutet, dass deine Machine sieht, dass die Aufgabe erledigt ist, zum Beispiel „PR #3451 zusammengeführt“, sie aber noch nicht geschlossen wurde. Mit **Wieder öffnen** kommt sie zurück auf deine Liste, und deine Machine lernt daraus. Diese Aufgaben werden nie als verspätet angezeigt. Nach einem Tag wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Eine Aufgabe, die du bereits selbst erledigt hast, zum Beispiel mit einer Antwort in Gmail oder Slack, wird ebenfalls automatisch geschlossen.

Wenn eine Nachricht von einer Adresse kommt, die nur so aussieht, als gehöre sie jemandem, den du kennst, zum Beispiel sam@acme-corp.example statt sam@acmecorp.example, steht in der Aufgabe ausdrücklich: „Das ist nicht Sam Lee.“ Die Person wird unter ihrer tatsächlichen Adresse angezeigt, nie unter dem Namen, den sie verwendet hat. Deine Machine prüft solche Nachrichten bei der Person unter der Adresse, die du bereits gespeichert hast, nie bei der Person, die geschrieben hat.

Bei einer Aufgabe, die noch auf jemand anderen wartet, zum Beispiel auf eine Prüfung oder Antwort, steht **Wartet auf:** und der entsprechende Schritt. Sie bleibt eingeklappt unter **Wartet auf andere**, oberhalb von Kommt später zurück, bis eine neue Nachricht sie wieder hervorholt. Das gilt auch, nachdem du eine Rückfrage gestellt hast: Die Aufgabe kommt am Morgen vor dem Termin zurück, am Termin selbst, wenn er noch heute ist, oder am nächsten Morgen, wenn er bereits verstrichen ist. Dabei steht, auf wen sie noch wartet.

Wenn es bei einer Aufgabe um ein Ergebnis geht, das jemand anderes liefern soll, zum Beispiel einen unterschriebenen Vertrag, steht es unter **Details** bei **Fertig, wenn**. Das Senden deines Teils schließt die Aufgabe nicht ab: Sie bleibt unter **Wartet auf andere**, bis eine Nachricht das Ergebnis bestätigt. Dann wird sie automatisch geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Wenn bis zum Zeitpunkt, an dem du nachfassen solltest, nichts eingeht, kommt die Aufgabe mit **Schreib eine kurze Erinnerung** im Chat zurück. Sag im Chat, was als erledigt gilt, um das zu ändern.

Hat eine Woche lang niemand eine Aufgabe angerührt, fragt sie einmal: **Noch nötig?** Mit **Nicht nötig** wird sie geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. **Behalten** lässt sie offen, und es wird nicht noch einmal gefragt. Wenn eine weitere Woche lang keine Antwort kommt, wird die Aufgabe unter Kommt später zurück eingeklappt. Sie wird dann nicht mehr auf dem App-Symbol oder in der morgendlichen Zusammenfassung mitgezählt. Wenn du sie öffnest, im Chat schreibst, sie bearbeitest oder zurückstellst oder eine neue Nachricht eingeht, kommt sie wieder zurück.

Einmal pro Woche kann es für ein ruhiges Projekt ohne offene Aufgaben eine Aufgabe mit einem konkreten nächsten Schritt geben, höchstens drei pro Woche. Mehr dazu unter [Projekte](projects.md).

Wenn nichts deine Aufmerksamkeit braucht, macht deine Machine ein Nickerchen und zeigt eine leere Liste. Während sie prüft, wird sie aktiv und zeigt das an. Wenn eine Prüfung fehlgeschlagen ist oder verspätet läuft, steht das in der Zeile, darunter findest du **Jetzt prüfen**.

Mit **Alle**, **Arbeit** und **Privat** oben in der Seitenleiste kannst du alle Aufgaben oder nur eine Art anzeigen. Auf deinem Handy und Computer wird dieselbe Auswahl angezeigt. Wenn Arbeit oder Privat ausgewählt ist, führt **Alle anzeigen** zurück zur Gesamtansicht. Eine Meldung über deine Machine selbst, zum Beispiel, wenn ein Teil immer wieder neu startet, gehört weder zu Arbeit noch zu Privat und wird nur unter Alle angezeigt.

Die Zeile oben in der Liste wechselt außerdem direkt zur anderen Ansicht: Unter **Nur privat** kannst du auf **Arbeit** oder **Alle anzeigen** tippen.

In der Zeile oben in der Liste steht der Name deiner letzten morgendlichen oder abendlichen Zusammenfassung und was sie erfasst hat, zum Beispiel **Zusammenfassung von gestern Abend** · 12 erledigt, 3 offen. Tippe darauf, um die Zusammenfassung erneut zu lesen. Mit **Kopieren** kannst du sie an beliebiger Stelle einfügen. Sobald du sie öffnest oder auf das **×** tippst, verschwindet sie auf all deinen Geräten bis zur nächsten Zusammenfassung.

Wenn es keine aktuelle Zusammenfassung gibt, steht dort **Heute bisher**: Was heute erledigt wurde und was noch offen ist, für Arbeit und Privat oder nur für den ausgewählten Bereich.

Bei einer Aufgabe zu einem Projekt steht der Projektname unter dem Titel. Tippe darauf, um das Projekt zu öffnen. Unter **Details** kannst du mit **Projekt** das Projekt ändern oder die Aufgabe daraus entfernen. Siehe [Aufgaben eines Projekts](projects.md#a-project-s-to-dos).

Mit **Bereich** unter **Details** verschiebst du eine Aufgabe in deinen anderen Bereich. Was sie lesen darf und von wo sie senden darf, wandert mit. Mit **Rückgängig** in der Meldung kannst du sie zurückverschieben.

Wenn eine Aufgabe deinen anderen Bereich braucht, um weiterzumachen, und alle Nachrichten, auf denen sie basiert, dort sind, wird sie automatisch dorthin verschoben und fortgesetzt. Andernfalls wird **Nach Arbeit verschieben** angezeigt. Nichts wird verschoben, bis du darauf tippst. Eine Aufgabe, die du hinzugefügt hast, ohne Arbeit oder Privat auszuwählen, wird automatisch verschoben, sobald klar ist, wohin sie gehört. Bis dahin ist sie weder als Arbeit noch als Privat gekennzeichnet und bleibt privat.

Eine Aufgabe kann immer die Nachrichten lesen, auf denen sie basiert. Wenn sie weitere Nachrichten aus deinem anderen Bereich braucht, fragt sie mit **Diese E-Mail für diese Aufgabe verwenden** danach. Ein Arbeits-Postfach, das du als Privat gekennzeichnet hast, zählt als Privat. E-Mails für ein anderes deiner Unternehmen gehören zu den Aufgaben dieses Unternehmens. Eine Aufgabe zu deinem Privatleben, zum Beispiel wenn deine Familie an deine Arbeitsadresse schreibt, ist von Anfang an privat.

Arbeit, die dich über ein privates Konto erreicht, zum Beispiel eine Kundin oder ein Kunde auf WhatsApp oder eine Bestellung in deinem privaten Postfach, zählt von Anfang an als Arbeit. Eine Aufgabe, die du selbst verschoben oder zugeordnet hast, bleibt immer dort, wo du sie abgelegt hast. Arbeit oder Privat bestimmt, wo eine Aufgabe angezeigt wird und mit wem sie geteilt wird, aber nicht, wohin sie antwortet: Eine Antwort geht immer dorthin, wo die Unterhaltung stattfindet, auch nach dem Verschieben, sofern du keine andere Möglichkeit auswählst.

Eine solche private Aufgabe antwortet trotzdem über die geschäftliche Adresse, an die ihre E-Mail gesendet wurde, und erscheint nie in einer Work Fleet oder im Team Graph.

Wenn mindestens zwei Aufgaben anstehen, kannst du mit **Durchgehen** in der Kopfzeile von Für dich nacheinander alle Aufgaben in der Reihenfolge der Liste durchgehen. Dabei wird jeder Entwurf vollständig angezeigt, zusammen mit **Senden** oder **Ausführen**, **Änderungen anfragen**, **Zurückstellen** und **Überspringen**. Am Computer sendet Enter den angezeigten Inhalt, `S` stellt zurück, `→` überspringt und Esc beendet den Ablauf. Unter dem Titel steht in der Kopfzeile außerdem, wie lange das in deinem eigenen Tempo dauert, zum Beispiel „etwa 2 Min.“.

Eine Aufgabe, die dir eine Frage stellt, wird dabei ausgelassen: Sie braucht deine Antwort, nicht nur ein Tippen.

## Jetzt prüfen

Deine Machine liest jede Quelle alle paar Minuten, Tag und Nacht. Sie prüft neu eingegangene Nachrichten, sobald 40 Nachrichten vorliegen oder die älteste Nachricht einer Person 15 Minuten gewartet hat. Newsletter, Benachrichtigungen und Belege werden bei der nächsten Prüfung innerhalb einer Stunde berücksichtigt.

Nachts, von 00:00 bis 06:30, pausieren die Prüfungen: Neue Nachrichten werden weiterhin gelesen und gespeichert. Um 06:30 werden sie gemeinsam geprüft, damit deine Aufgaben vor der morgendlichen Zusammenfassung bereit sind. Unter Verbindungen steht bei den Prüfungen: „Nachts pausiert, wird um 06:30 nachgeholt“. Wenn du nachts in der App klickst, schreibst oder scrollst, im Chat schreibst oder auf eine Aufgabe tippst, laufen die Prüfungen wie gewohnt weiter, bis du eine Stunde lang nicht aktiv warst. Mit **Jetzt prüfen** wird immer sofort geprüft.

Mit **Jetzt prüfen** werden alle Quellen sofort gelesen. Wenn keine Aufgaben offen sind, tippe auf die Zeile deiner Machine, um die Schaltfläche zu sehen, zusammen mit **Details**, das „Prüfungen“ unter Verbindungen öffnet. Wenn Aufgaben offen sind, steht sie am Computer ganz oben. Eine kurze Meldung wird nur angezeigt, solange eine Prüfung läuft oder wenn eine fehlgeschlagen oder verspätet ist. Du kannst auch im Chat danach fragen.

LinkedIn, X und Salesflare haben ihren eigenen Rhythmus.

## Letzte Prüfung

Nach einer Prüfung, bei der neue Nachrichten gelesen wurden, steht über deinen Aufgaben, was in allen gelesenen Quellen gefunden wurde, zum Beispiel „13 Nachrichten um 16:11 geprüft · nichts braucht dich“ oder „· 2 neue Aufgaben“. Wenn eine neue Aufgabe auf einen passenden Zeitpunkt wartet, etwa auf deine morgendliche Zusammenfassung, wird angezeigt, bis wann: „1 Aufgabe bis morgen 08:30 zurückgehalten“.

Tippe auf die Zeile, um die einzelnen E-Mail-Threads, Chats und Benachrichtigungen mit dem Symbol der jeweiligen Quelle zu sehen: Wer geschrieben hat, der Betreff oder die ersten Wörter und die neue Aufgabe oder der Grund, warum nichts nötig war, zum Beispiel „Nur in Cc, ein Teammitglied antwortet“ oder „Besprechung bereits für Donnerstag angesetzt“. Wenn die Prüfung nur einen vagen Grund ergeben hat, wird für den Thread kein Grund angezeigt. Tippe auf einen Eintrag, um ihn zu lesen.

Die ersten 10 Einträge werden angezeigt. Tippe darunter, um den Rest zu sehen. Eine Zahl nach einem Namen, zum Beispiel (3), gibt an, wie viele neue Nachrichten dieser Chat enthält. Eine Handybenachrichtigung zu einer Nachricht, die bereits aufgelistet ist, wird nur einmal angezeigt. Die Zeile bleibt 12 Stunden nach der Prüfung sichtbar.

Gezählt werden nur E-Mails, die an dich gesendet wurden. Deine eigenen Antworten werden berücksichtigt, um den Kontext und Versprechen zu verstehen, zählen aber nicht als neue E-Mails. E-Mails, die The Machine selbst an dich sendet, zum Beispiel deine morgendliche Zusammenfassung oder eine Benachrichtigung zu einer Fehlerbehebung, werden nie gelesen oder aufgelistet. E-Mails zu Abrechnungen, deiner Testphase oder einer Einladung werden wie gewohnt gelesen.

## Die Schaltflächen

Bei einer Aufgabe wird der nächste Schritt angezeigt, zum Beispiel **Ausführen** oder **Prüfen und senden**, daneben **Zurückstellen**. Siehe [Ausführen](do-it.md) und [Zurückstellen](snooze.md).

Mit **Änderungen anfragen** kannst du angeben, was geändert werden soll: wie die Aufgabe ausgeführt wird oder, sobald ein Entwurf bereit ist, was daran geändert werden soll. **Als erledigt markieren** bedeutet, dass die Aufgabe erledigt ist. Bei einer vorbereiteten Aufgabe ohne Entwurf ist die Option direkt zu sehen, andernfalls findest du sie oben unter **…**. Sie ist auch bei Aufgaben verfügbar, für die du noch eine Entscheidung treffen musst. Die Aufgabe verschwindet sofort aus der Liste. In der Meldung findest du **Rückgängig**. Wische die Meldung weg oder ziehe sie mit der Maus aus der Ansicht, um sie früher zu schließen. Die Änderung bleibt bestehen.

Wenn die Aufgabe anders erledigt werden soll, sag es im **Chat** dazu.

Unter **…**:

- **Übergeben…**: Weise die Aufgabe einem Teammitglied, [Claude Code oder Codex](hand-to-agent.md) zu oder [bitte jemanden um eine Prüfung](ask-to-review.md).
- **Wiederholen…**: Die Aufgabe [kommt regelmäßig wieder](recurring.md).
- **Nicht nötig**: Die Aufgabe wird entfernt. Optional kannst du einen Grund auswählen: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Tippe auf den Titel oder unter **Details** auf **Name**, um die Aufgabe umzubenennen. Du kannst auch im Chat darum bitten, zum Beispiel: „Benenne sie in … um.“ Dein Titel bleibt erhalten.

Mit **Wieder öffnen** holst du eine geschlossene Aufgabe zurück. Sie kommt auch automatisch zurück, wenn etwas Neues passiert, zum Beispiel eine neue Nachricht von der anderen Person, aber nicht bei deiner eigenen Antwort. Dann wird angezeigt, wann sie zurückgekommen ist, und sie wird wie eine neue Aufgabe sortiert. Der Chat wird dort fortgesetzt, wo er aufgehört hat, auch nach Wochen.

Eine Rechnung, die du selbst noch bezahlen musst, wird unabhängig vom Land zu einer Aufgabe mit dem Betrag, dem Fälligkeitsdatum und den Zahlungsangaben aus der Rechnung. Automatisch bezahlte Rechnungen, zum Beispiel per Lastschrift oder mit einer hinterlegten Karte, werden nicht zu Aufgaben. Wenn eine spätere E-Mail zeigt, dass sie bezahlt wurde, etwa eine Bestätigung des Absenders über den Zahlungseingang, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du sie innerhalb eines Tages zurückholen.

Eine Aufgabe, die nur bis zu einem bestimmten Zeitpunkt wichtig war, zum Beispiel eine Bestätigung vor einer Besprechung, wird nach diesem Zeitpunkt automatisch geschlossen. Sie wird unter **Erledigt / verworfen** als „Nicht mehr nötig“ angezeigt. Mit **Rückgängig** kannst du sie innerhalb eines Tages zurückholen.

Bevor eine Nachricht oder Übergabe für jemanden als bereit angezeigt wird, prüft deine Machine deine letzten Chats mit den beteiligten Personen, auch Gruppenchats, und wartet darauf, dass Slack sie gelesen hat. Wenn eine spätere Nachricht zeigt, dass die Aufgabe bereits erledigt ist, zum Beispiel weil jemand gefragt wurde und Ja gesagt hat, wird sie automatisch geschlossen. Mit **Rückgängig** kannst du sie innerhalb eines Tages zurückholen.

Wenn eine neuere Nachricht den Plan ändert, zum Beispiel wenn eine Party an einen anderen Ort verlegt oder eine Buchung storniert wird, aktualisiert The Machine die Aufgaben selbst. Eine weiterhin relevante Aufgabe folgt dem neuen Plan. Wenn nichts mehr zu tun ist, wird sie unter **Erledigt / verworfen** als „Nicht nötig“ angezeigt. Im Chat steht „Aktualisiert:“ mit dem Grund. Mit **Rückgängig** kannst du sie innerhalb eines Tages zurückholen.

Bei deinen ersten Aufgaben wird ein kurzer Tipp mit den wichtigsten Aktionen angezeigt: **Änderungen anfragen** und **Nicht nötig**. Außerdem erfährst du, dass nichts gesendet wird, bevor du auf **Senden** tippst. Ein Tipp verschwindet dauerhaft, sobald du seine Schaltfläche verwendest oder auf × tippst.

An deinem ersten Tag begrüßt dich deine Aufgabenliste oben und nennt die Person, die am längsten auf deine Antwort wartet. Für diese Person wird zuerst ein Entwurf erstellt, damit er bereit ist, wenn du kommst.

Jede Aufgabe beginnt mit ihrem Titel. In der Zeile darunter stehen, um wen es geht, gegebenenfalls die Organisation (nicht allein deshalb, weil jemand dort arbeitet), das Projekt, Arbeit oder Privat und der Eingangszeitpunkt. Tippe auf einen Namen, um die Seite der Person im Graph zu öffnen.

Wenn es im Graph ein Foto oder Logo gibt, wird es neben dem Namen oder der Organisation angezeigt, ansonsten die Initialen. Ein Logo, das in dieser Größe schwer zu erkennen wäre, zum Beispiel weiße Schrift auf transparentem Hintergrund oder ein breites Wortlogo, wird ebenfalls durch die Initiale ersetzt.

Manchmal steht in einer unauffälligen Zeile, was nicht bekannt ist, zum Beispiel „Letzter Kontakt vor 12 Tagen per E-Mail, seitdem nichts“. Sie wird angezeigt, wenn der letzte Kontakt schon länger zurückliegt oder unbeantwortet ist, und nennt nicht verbundene Kanäle wie WhatsApp. Deine Machine sagt, was sie nicht weiß, statt etwas zu erraten.

Wenn ein nicht verbundener Kanal genannt wird, öffnet **Verbinden** daneben diese Verbindung.

Der Titel beschreibt, was zu tun ist, und ändert sich nur, wenn sich die Aufgabe ändert. Eine erledigte Aufgabe behält ihren Titel. Darunter steht, wie sie abgeschlossen wurde, zum Beispiel „Erledigt: Sam hat es am Dienstag unterschrieben“.

Über dem Entwurf steht in einer unauffälligen Zeile, aus welcher Nachricht er stammt, mit dem Logo des jeweiligen Dienstes. Tippe darauf, um den Thread zu lesen. Das Logo des Ziels zeigt dir beim Entwurf sofort, ob es eine Slack-Antwort oder eine E-Mail ist.

Wenn sich der Entwurf auf die Eingabe einer anderen Person an anderer Stelle stützt, zum Beispiel auf den Vorschlag eines Teammitglieds in Slack, steht das in einer Zeile, etwa „Basiert auf Sam in #ops“. Tippe darauf, um die Nachricht zu lesen.

Ein Chat (Slack, WhatsApp, Telegram, Intercom…) wird als eine Unterhaltung angezeigt, von den ältesten Nachrichten bis zu den neuesten: die Nachrichten vor der Nachricht, auf die sich die Aufgabe bezieht, und die Antworten danach. In WhatsApp, Telegram oder Signal stehen deine Nachrichten rechts, wie in der App. Die Nachricht der Aufgabe ist mit „Diese Aufgabe“ markiert und wird direkt angezeigt. Mit **Frühere Nachrichten anzeigen** werden ältere Nachrichten hinzugefügt. Bei einer E-Mail ist der Rest des Threads ober- und unterhalb eingeklappt.

Mit **In Gmail öffnen** öffnest du die E-Mail in dem Gmail-Konto, an das sie gesendet wurde. Auf Android wird sie in der Gmail-App geöffnet, falls du sie installiert hast.

Unter **Details** einer E-Mail werden nur Angaben angezeigt, die nicht in ihrer Kopfzeile stehen, zum Beispiel vollständige Cc-Adressen, Bcc oder eine andere Antwortadresse. Gibt es nichts hinzuzufügen, wird nichts angezeigt.

Bei einer Antwort in einem Slack-Thread wird auch angezeigt, was vor dem Start des Threads gesagt wurde. Über den Link einer Aufgabe zur zugehörigen Nachricht kannst du sie ebenfalls hier öffnen. Unten findest du **In Slack öffnen**.

Unter **Details** stehen der Name, das Projekt und der Bereich der Aufgabe (tippe auf einen Eintrag, um ihn zu ändern), deine letzte Notiz und das Ergebnis eines Coding-Agenten. Über den Titel öffnest du den Chat. Eine erledigte Aufgabe bleibt kompakt. Die Nachricht, auf der sie basiert, findest du unter **Details**.

Bei einer Aufgabe mit dem Status „Wartet auf“ führt ein Link zu deiner letzten Nachricht an die Person, auf deren Antwort du wartest, zum Beispiel: „E-Mail an Pat · Di.“

## Selbst eine Aufgabe erstellen

Mit **Neue Aufgabe** (unter **Suchen** am Computer, über **+** auf dem Handy oder mit `N`) kannst du eine Aufgabe zu beliebigen Themen erstellen. Beim Erstellen wird nichts gesendet. Wenn du weder **Arbeit** noch **Privat** auswählst, wird die Aufgabe dem passenden Bereich zugeordnet, je nachdem, um wen und was es geht. Außerdem findet sie die E-Mail, an die sie anknüpft, auch wenn sie älter ist.

- **Fällig**: Gib einen Tag oder eine Uhrzeit ein, zum Beispiel „morgen“, „nächsten Fr“, „3. Nov.“, „14 Uhr“ oder „in 2 Stunden“, auch in deiner eigenen Sprache. Über das Kalendersymbol findest du Schnelloptionen und **Datum wählen**.
- **Wiederholt sich**: Die Aufgabe kommt regelmäßig wieder. Siehe [Wiederkehrende Aufgaben](recurring.md).
- **Person**: Verknüpfe bis zu 5 Personen oder Unternehmen, um die es geht.
- Nachrichtensymbol: Hänge die Nachricht an, um die es geht: eine E-Mail, eine Nachricht aus Slack, Teams, WhatsApp, Telegram oder einem anderen Dienst, den The Machine kennt. Suche nach Text oder Absender. Bei jedem Ergebnis wird angezeigt, woher es stammt, wer es gesendet hat und wann.
- **Dateien**: Tippe auf die Büroklammer, füge einen Screenshot ein oder ziehe Dateien auf das Formular. Auf dem Handy kannst du mit der Kamera daneben ein Foto aufnehmen. Bis zu 5 Dateien, wie im Chat (siehe [Dateien hinzufügen](card-chat.md#add-files)). Mit × entfernst du eine Datei.

Die Dateien bleiben bei der Aufgabe, und The Machine liest sie, wenn sie daran arbeitet. Dateien allein reichen aus: The Machine erstellt die Aufgabe aus einer PDF- oder Textdatei. Ein Foto wird als kleines Bild angezeigt. Tippe darauf, um es in voller Größe zu sehen.
