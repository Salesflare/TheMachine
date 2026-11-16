---
title: Aufgaben
area: cards
summary: Eine Aufgabe pro Sache, bei der du gefragt bist, bereit für dein Ja. Was die einzelnen Teile einer Aufgabe bedeuten.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 6cbbad37c4dfaf07
---
Deine Machine liest alles Neue und erstellt nur dann eine Aufgabe, wenn etwas dich braucht. Eine Aufgabe pro Anliegen, egal über wie viele Nachrichten es sich erstreckt.

## Wo Aufgaben stehen

Auf der Seite **Aufgaben** sind sie gruppiert:

- **Gerade erledigt**: Ganz oben siehst du einen letzten Schritt, den du bestätigt hast, zum Beispiel ein Formular oder ein Vorgang, der erledigt wurde, während du weg warst. Er bleibt höchstens einen Tag lang dort, bis du auf **Verstanden** tippst. Dein Smartphone wird ebenfalls benachrichtigt.
- **Für dich**: Alles, was auf dich wartet, nach Dringlichkeit sortiert. Bei jeder Aufgabe steht **Vorbereitet** (die Arbeit ist erledigt, mit **Ausführen** oder **Senden** wird sie abgeschlossen), **Braucht dich** (du musst erst entscheiden oder antworten), **Wird vorbereitet…** (deine Machine arbeitet daran) oder **Zum Lesen** (eine Zusammenfassung oder ein Briefing, bei dem du nichts entscheiden musst).
- **Wartet auf andere**: Aufgaben, bei denen der nächste Schritt bei jemand anderem liegt, sind eingeklappt (siehe unten).
- **Kommt später zurück**: Zurückgestellte Aufgaben und Aufgaben, auf die du nicht mit **Noch nötig?** geantwortet hast (siehe unten).
- **Versprechen**: Was du versprochen hast und was andere dir versprochen haben. Siehe [Versprechen](promises.md).
- **Erledigt / verworfen**: Jede abgeschlossene Aufgabe, neueste zuerst, mit dem Zeitpunkt, zu dem sie erledigt wurde, zum Beispiel „Vor 5 Minuten erledigt“. Aufgaben, die scheinbar schon erledigt sind, sind mit **Scheinbar erledigt** markiert.

Nachdem du etwas gesendet hast, steht in einer kurzen Nachricht, wohin die Aufgabe verschoben wurde, zum Beispiel „Gesendet. Nach Erledigt verschoben.“ oder „Gesendet. Bis Mo. auf Später verschoben.“ Mit **Öffnen** kommst du zur Aufgabe. Über die Suche findest du Aufgaben anhand ihres Titels oder der Person, an die sie gesendet wurden, auch unter Später und Erledigt.

Unter **Für dich** stehen zuerst überfällige Aufgaben oder Aufgaben, die bis morgen fällig sind, dann Fragen von deiner Fleet, danach die nächsten Schritte eines Boards und schließlich alle übrigen. Innerhalb jeder Gruppe stehen die neuesten zuerst. Eine Aufgabe behält ihren Platz, während deine Machine sie vorbereitet und wenn sie erledigt ist. Nur ihre Markierung ändert sich. In den anderen offenen Gruppen stehen überfällige Aufgaben oder Aufgaben, die bis morgen fällig sind, zuerst, der Rest ist nach Aktualität sortiert. Die Seitenleiste behält dieselbe Reihenfolge bei.

**Scheinbar erledigt** bedeutet, dass deine Machine sieht, dass etwas erledigt ist, zum Beispiel „PR #3451 zusammengeführt“, die Aufgabe aber noch nicht geschlossen wurde. Mit **Wieder öffnen** kommt sie zurück auf deine Liste, und deine Machine lernt daraus. Diese Aufgaben werden nie als verspätet angezeigt. Nach einem Tag schließt sich die Aufgabe von selbst. Mit **Rückgängig** kannst du das rückgängig machen. Eine Aufgabe, die du selbst schon erledigt hast, zum Beispiel mit einer Antwort in Gmail oder Slack, schließt sich ebenfalls von selbst.

Wenn eine Nachricht von einer Adresse kommt, die nur einer Person ähnelt, die du kennst, zum Beispiel sam@acme-corp.example statt sam@acmecorp.example, steht das ausdrücklich bei der Aufgabe: „Das ist nicht Sam Lee.“ Die Person wird mit ihrer eigenen Adresse angezeigt, nie mit dem Namen, den sie verwendet hat. Deine Machine prüft solche Nachrichten bei der Person unter der Adresse, die du bereits hast, niemals bei der Person, die geschrieben hat.

Bei einer Aufgabe, die noch auf jemand anderen wartet, zum Beispiel auf eine Prüfung oder Antwort, steht **Wartet auf:** und der nächste Schritt. Sie bleibt eingeklappt unter **Wartet auf andere**, oberhalb von „Kommt später zurück“, bis eine neue Nachricht sie wieder hervorholt. Das gilt auch, nachdem du eine Rückfrage gestellt hast: Die Aufgabe kommt am Morgen vor der Frist zurück, bei einer später am selben Tag liegenden Frist zum Zeitpunkt der Frist oder nach Ablauf der Frist am nächsten Morgen. Außerdem steht dort, auf wen sie noch wartet.

Geht es bei einer Aufgabe um ein Ergebnis, das jemand anderes liefern muss, zum Beispiel einen unterschriebenen Vertrag, zeigt **Details** es unter **Fertig, wenn** an. Wenn du deinen Teil sendest, wird die Aufgabe nicht geschlossen. Sie wartet unter **Wartet auf andere**, bis eine Nachricht das Ergebnis bestätigt. Dann schließt sie sich von selbst. Mit **Rückgängig** kannst du das rückgängig machen. Wenn bis zu dem Zeitpunkt, an dem du nachfassen solltest, nichts eingegangen ist, kommt die Aufgabe mit **Schreib eine kurze Erinnerung** im Chat zurück. Schreib im Chat, was als erledigt gilt, um das zu ändern.

Wenn sich eine Woche lang niemand um eine Aufgabe gekümmert hat, fragt sie einmal: **Noch nötig?** Mit **Nicht nötig** wird sie geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Mit **Behalten** bleibt sie bestehen und fragt nie wieder nach. Wenn du eine weitere Woche nicht antwortest, wird die Aufgabe unter „Kommt später zurück“ eingeklappt. Sie wird dann nicht mehr auf dem App-Symbol oder in der morgendlichen Zusammenfassung mitgezählt. Wenn du sie öffnest, eine Chatnachricht schreibst, sie bearbeitest oder zurückstellst oder eine neue Nachricht eintrifft, kommt sie wieder zurück.

Einmal pro Woche kann es für ein Projekt, zu dem es nichts Neues gab und bei dem keine Aufgaben offen sind, eine Aufgabe mit einem konkreten nächsten Schritt geben. Höchstens drei pro Woche. Siehe [Projekte](projects.md).

Wenn dich nichts braucht, macht deine Machine ein Nickerchen und zeigt eine leere Liste. Während sie prüft, wird sie aktiv und sagt dir Bescheid. Wenn eine Prüfung fehlgeschlagen ist oder sich verspätet, steht das in der Zeile, darunter findest du **Jetzt prüfen**.

Mit **Alle**, **Arbeit** und **Privat** oben in der Seitenleiste kannst du alle Aufgaben oder nur eine der beiden Arten anzeigen. Auf deinem Smartphone und Computer gilt dieselbe Auswahl. Wenn „Arbeit“ oder „Privat“ ausgewählt ist, führt **Alle anzeigen** zurück zur Gesamtansicht. Eine Meldung über deine Machine selbst, zum Beispiel, dass ein Teil immer wieder neu startet, gehört weder zu Arbeit noch zu Privat und erscheint nur unter „Alle“.

Über die Zeile oben in der Liste kannst du auch direkt zur anderen Ansicht wechseln: Unter **Nur privat** tippst du auf **Arbeit** oder **Alle anzeigen**.

In der obersten Zeile der Liste stehen der Name deiner letzten morgendlichen oder abendlichen Zusammenfassung und die Anzahl der Aufgaben, die darin enthalten sind, zum Beispiel **Zusammenfassung von gestern Abend** · 12 erledigt, 3 offen. Tippe darauf, um die Zusammenfassung noch einmal zu lesen. Mit **Kopieren** kannst du sie überall einfügen. Sobald du sie öffnest oder auf **×** tippst, ist sie auf all deinen Geräten verfügbar, bis die nächste Zusammenfassung erscheint.

Wenn es keine aktuelle Zusammenfassung gibt, wird **Heute bisher** angezeigt: Was heute erledigt wurde und was noch offen ist, für Arbeit und Privat oder nur für die Ansicht, die du ausgewählt hast.

Bei einer Aufgabe zu einem Projekt steht der Projektname unter dem Titel. Tippe darauf, um das Projekt zu öffnen. Mit **Projekt** unter **Details** kannst du das Projekt ändern oder entfernen. Siehe [Aufgaben eines Projekts](projects.md#a-project-s-to-dos).

Mit **Bereich** unter **Details** kannst du eine Aufgabe in deinen anderen Bereich verschieben. Der Zugriff auf Nachrichten, die die Aufgabe lesen und senden darf, wird dabei mitverschoben. Mit **Rückgängig** in der Nachricht verschiebst du sie zurück.

Wenn eine Aufgabe deinen anderen Bereich braucht, um weiterzumachen, und alle zugehörigen Nachrichten dort sind, wird sie von selbst dorthin verschoben und fortgesetzt. Andernfalls wird **Nach Arbeit verschieben** angezeigt, und erst wenn du darauf tippst, wird etwas verschoben. Eine Aufgabe, die du hinzugefügt hast, ohne „Arbeit“ oder „Privat“ auszuwählen, wird automatisch dem passenden Bereich zugeordnet, sobald klar ist, wohin sie gehört. Bis dahin gehört sie weder zu Arbeit noch zu Privat und bleibt privat.

Eine Aufgabe kann immer die Nachrichten lesen, aus denen sie entstanden ist. Wenn sie weitere Nachrichten aus deinem anderen Bereich braucht, fragt sie mit **Diese E-Mail für diese Aufgabe verwenden** danach. Ein Arbeits-Postfach, das du als Privat gekennzeichnet hast, gilt als privat. E-Mails für ein anderes deiner Unternehmen gehören zu den Aufgaben dieses Unternehmens. Eine Aufgabe zu deinem eigenen Leben, zum Beispiel wenn deine Familie an deine Arbeitsadresse schreibt, gehört von Anfang an zu Privat.

Arbeit, die dich über ein persönliches Konto erreicht, zum Beispiel von einem Kunden über WhatsApp oder eine Bestellung in deinem privaten Postfach, gehört von Anfang an zu Arbeit. Eine Aufgabe, die du selbst verschoben oder zugeordnet hast, bleibt immer dort, wo du sie abgelegt hast. „Arbeit“ oder „Privat“ entscheidet, wo eine Aufgabe angezeigt und mit wem sie geteilt wird, aber nie, wo sie antwortet. Eine Antwort geht immer dorthin, wo die Unterhaltung stattfindet, auch nach einem Verschieben, sofern du keinen anderen Weg auswählst.

Eine solche private Aufgabe antwortet weiterhin über die Arbeitsadresse, an die die E-Mail gesendet wurde. Sie erscheint nie in einer Fleet für Arbeit oder im Team-Graph.

Wenn mindestens zwei Aufgaben auf dich warten, kannst du mit **Durchgehen** in der Kopfzeile von „Für dich“ nacheinander durchgehen, in der Reihenfolge der Liste. Jede Aufgabe wird mit ihrem vollständigen Entwurf angezeigt, dazu **Senden** oder **Ausführen**, **Änderungen anfragen**, **Zurückstellen** und **Überspringen**. Am Computer sendet Enter den angezeigten Inhalt, `S` stellt zurück, `→` überspringt und Esc beendet. Unter dem Titel steht in der Kopfzeile auch, wie lange es in deinem eigenen Tempo dauert, zum Beispiel „etwa 2 Min.“

Eine Aufgabe, die dir eine Frage stellt, wird dabei ausgelassen: Sie braucht deine Antwort, nicht einen Tipp.

## Jetzt prüfen

Deine Machine liest jede Quelle alle paar Minuten, Tag und Nacht. Sie prüft neue Inhalte, sobald 40 Nachrichten vorliegen oder die älteste Nachricht einer Person seit 15 Minuten wartet. Newsletter, Benachrichtigungen und Belege werden bei der nächsten Prüfung berücksichtigt, spätestens innerhalb einer Stunde.

Nachts, von 00:00 bis 06:30 Uhr, pausieren die Prüfungen. Neue Nachrichten werden weiterhin gelesen und gespeichert. Um 06:30 Uhr werden sie gemeinsam geprüft, sodass deine Aufgaben vor der morgendlichen Zusammenfassung bereitstehen. Unter Verbindungen steht bei den Prüfungen: „Nachts pausiert, wird um 06:30 Uhr nachgeholt“. Wenn du nachts in der App klickst, tippst oder scrollst, im Chat schreibst oder auf eine Aufgabe tippst, laufen die Prüfungen wie gewohnt weiter, bis du eine Stunde lang inaktiv warst. Mit **Jetzt prüfen** wird immer sofort geprüft.

Mit **Jetzt prüfen** werden alle Quellen sofort gelesen. Wenn keine Aufgaben offen sind, tippe auf die Zeile deiner Machine, um sie mit **Details** anzuzeigen. Damit öffnest du „Prüfungen“ unter Verbindungen. Bei offenen Aufgaben findest du sie am Computer ganz oben. Eine kurze Zeile wird dort nur angezeigt, während eine Prüfung läuft oder wenn sie fehlgeschlagen ist oder sich verspätet. Du kannst auch im Chat danach fragen.

LinkedIn, X und Salesflare haben ihren eigenen Rhythmus.

## Letzte Prüfung

Nach einer Prüfung, bei der neue Nachrichten gelesen wurden, steht über deinen Aufgaben eine Zeile mit den Ergebnissen aus allen gelesenen Quellen, zum Beispiel „13 Nachrichten um 16:11 geprüft · nichts braucht dich“ oder „· 2 neue Aufgaben“. Wenn eine neue Aufgabe bis zu einem günstigeren Zeitpunkt zurückgehalten wird, zum Beispiel bis zur morgendlichen Zusammenfassung, steht dort, bis wann: „1 Aufgabe bis morgen 08:30 Uhr zurückgehalten“.

Tippe auf die Zeile, um die einzelnen E-Mail-Threads, Chats und Benachrichtigungen mit dem Symbol des jeweiligen Dienstes zu sehen: wer geschrieben hat, den Betreff oder die ersten Wörter und die neue Aufgabe oder den Grund, warum keine Aufgabe nötig war, zum Beispiel „Nur in Cc, eine Teamkollegin antwortet“ oder „Termin für Donnerstag steht schon“. Wenn die Prüfung nur einen vagen Grund ergeben hat, wird für einen Thread kein Grund angezeigt. Tippe darauf, um ihn zu lesen.

Die ersten 10 werden angezeigt. Tippe darunter, um die übrigen zu sehen. Eine Zahl nach einem Namen, zum Beispiel (3), gibt an, wie viele neue Nachrichten dieser Chat enthält. Eine Smartphone-Benachrichtigung zu einer bereits aufgelisteten Nachricht wird nur einmal angezeigt. Die Zeile bleibt nach der Prüfung 12 Stunden lang sichtbar.

Gezählt werden nur E-Mails an dich. Deine eigenen Antworten werden zur Einordnung und für Versprechen gelesen, zählen aber nicht als neue E-Mails. Eigene E-Mails von The Machine an dich, zum Beispiel deine morgendliche Zusammenfassung oder eine Benachrichtigung über eine Korrektur, werden nie gelesen oder aufgelistet. E-Mails zu deiner Abrechnung, Testphase oder Einladung werden wie gewohnt gelesen.

## Die Schaltflächen

Bei einer Aufgabe wird der nächste Schritt angezeigt, zum Beispiel **Ausführen** oder **Prüfen und senden**, daneben **Zurückstellen**. Siehe [Ausführen](do-it.md) und [Zurückstellen](snooze.md).

Mit **Änderungen anfragen** kannst du angeben, was geändert werden soll: wie etwas erledigt werden soll oder, sobald ein Entwurf bereit ist, was daran geändert werden soll. **Als erledigt markieren** bedeutet, dass die Aufgabe erledigt ist. Bei einer vorbereiteten Aufgabe ohne Entwurf ist die Schaltfläche direkt sichtbar. Andernfalls findest du sie oben unter **…**, auch bei Aufgaben, die deine Entscheidung brauchen. Die Aufgabe verschwindet sofort aus der Liste. In der Nachricht findest du **Rückgängig**. Wische die Nachricht weg oder zieh sie mit der Maus aus der Liste, um sie schneller zu schließen. Die Änderung bleibt bestehen.

Wenn du möchtest, dass es anders erledigt wird, sag es im **Chat** der Aufgabe.

Unter **…**:

- **Übergeben…**: Gib die Aufgabe an eine Teamkollegin oder einen Teamkollegen, an [Claude Code oder Codex](hand-to-agent.md) weiter oder [bitte jemanden um eine Prüfung](ask-to-review.md).
- **Wiederholen…**: Die Aufgabe [kommt regelmäßig wieder](recurring.md).
- **Nicht nötig**: Die Aufgabe wird entfernt. Optional kannst du einen Grund auswählen: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Tippe auf den Titel oder unter **Details** auf **Name**, um die Aufgabe umzubenennen. Dein Titel bleibt bestehen.

Mit **Wieder öffnen** holst du eine geschlossene Aufgabe zurück. Sie kommt auch von selbst zurück, wenn etwas Neues passiert, zum Beispiel eine neue Nachricht von der anderen Person, aber nicht bei deiner eigenen Antwort.

Eine Rechnung, die du selbst noch bezahlen musst, egal aus welchem Land, wird zu einer Aufgabe mit dem Betrag, dem Fälligkeitsdatum und den Zahlungsangaben aus der Rechnung. Automatisch bezahlte Rechnungen, zum Beispiel per Lastschrift oder mit einer hinterlegten Karte, werden nicht zu Aufgaben. Wenn eine spätere E-Mail zeigt, dass die Rechnung bezahlt wurde, zum Beispiel eine Bestätigung des Absenders über den Zahlungseingang, wird die Aufgabe von selbst geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Eine Aufgabe, die nur bis zu einem bestimmten Zeitpunkt wichtig war, zum Beispiel eine Bestätigung vor einem Termin, wird danach von selbst geschlossen. Sie wird unter **Erledigt / verworfen** mit dem Vermerk „Nicht mehr nötig“ abgelegt. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Bevor eine Nachricht oder Übergabe für jemanden als bereit angezeigt wird, prüft deine Machine deine aktuellen Chats mit den beteiligten Personen, auch Gruppenchats, und wartet darauf, dass Slack sie einliest. Wenn eine spätere Nachricht zeigt, dass es bereits erledigt ist, zum Beispiel weil die Person gefragt wurde und zugesagt hat, wird die Aufgabe von selbst geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Wenn eine neuere Nachricht den Plan ändert, zum Beispiel weil eine Feier an einen anderen Ort verlegt oder eine Buchung storniert wurde, aktualisiert The Machine ihre Aufgaben selbst. Eine weiterhin relevante Aufgabe folgt dem neuen Plan. Wenn nichts mehr zu tun ist, wird sie unter **Erledigt / verworfen** mit dem Vermerk „Nicht nötig“ abgelegt. Im Chat steht „Aktualisiert:“ mit einer Begründung. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Bei deinen ersten Aufgaben wird ein kurzer Tipp zu den wichtigsten Aktionen angezeigt: **Änderungen anfragen** und **Nicht nötig**. Außerdem erfährst du, dass nichts gesendet wird, bevor du **Senden** drückst. Der Tipp verschwindet dauerhaft, sobald du die entsprechende Schaltfläche verwendest oder auf × drückst.

An deinem ersten Tag begrüßt dich oben in „Aufgaben“ eine Nachricht. Sie nennt die Person, die am längsten auf deine Antwort wartet. Diese Antwort wird zuerst vorbereitet, damit sie bereit ist, wenn du kommst.

Jede Aufgabe beginnt mit ihrem Titel. Die Zeile darunter nennt die beteiligte Person, die Organisation, falls es um eine geht (nicht nur, weil jemand dort arbeitet), das Projekt, Arbeit oder Privat und den Zeitpunkt, zu dem die Aufgabe eingegangen ist. Tippe auf einen Namen, um die Seite der Person im Graph zu öffnen.

Bei Namen und Organisationen wird ein Foto oder Logo angezeigt, wenn im Graph eines vorhanden ist, andernfalls die Initialen. Ein Logo, das in dieser Größe schwer zu erkennen wäre, zum Beispiel weiße Schrift auf transparentem Hintergrund oder ein breites Wortlogo, wird ebenfalls durch die Initiale ersetzt.

Manchmal steht in einer unaufdringlichen Zeile, was nicht bekannt ist, zum Beispiel: „Letzter Kontakt vor 12 Tagen per E-Mail, seitdem nichts.“ Das wird angezeigt, wenn der letzte Austausch mit der Person schon länger her oder unbeantwortet ist. Außerdem werden nicht verbundene Kanäle wie WhatsApp genannt. Deine Machine sagt, was sie nicht weiß, statt zu raten.

Wenn ein nicht verbundener Kanal genannt wird, öffnet **Verbinden** daneben die entsprechende Verbindung.

Der Titel nennt die Aufgabe und ändert sich nur, wenn sich die Aufgabe ändert. Eine erledigte Aufgabe behält ihren Titel. Darunter steht, wie sie abgeschlossen wurde, zum Beispiel „Erledigt: Sam hat es am Dienstag unterschrieben“.

Über dem Entwurf steht in einer dezenten Zeile, aus welcher Nachricht er stammt, mit dem Logo des jeweiligen Dienstes. Tippe darauf, um den Thread zu lesen. Im Entwurf wird das Logo des Dienstes angezeigt, an den er geht. So siehst du sofort, ob es eine Slack-Antwort oder eine E-Mail ist.

Wenn der Entwurf auf einer Eingabe an anderer Stelle beruht, zum Beispiel auf dem Vorschlag einer Teamkollegin in Slack, steht das in einer Zeile, etwa „Basierend auf Sams Nachricht in #ops“. Tippe darauf, um die Nachricht zu lesen.

Ein Chat (Slack, WhatsApp, Telegram, Intercom …) wird als eine Unterhaltung angezeigt, beginnend mit der ältesten Nachricht: zuerst die Nachrichten vor der Nachricht, um die es bei der Aufgabe geht, dann die Antworten danach. In WhatsApp, Telegram oder Signal stehen deine Nachrichten wie in der App rechts. Die Nachricht zur Aufgabe ist mit „Diese Aufgabe“ markiert und wird geöffnet angezeigt. Mit **Frühere Nachrichten anzeigen** werden ältere Nachrichten hinzugefügt. Bei einer E-Mail ist der übrige Thread oberhalb und unterhalb der Nachricht eingeklappt.

Unter **Details** einer E-Mail werden nur Angaben angezeigt, die nicht schon in ihrer Kopfzeile stehen, zum Beispiel vollständige Cc-Adressen, Bcc oder eine abweichende Antwortadresse. Gibt es nichts hinzuzufügen, wird nichts angezeigt.

Bei einer Antwort in einem Slack-Thread wird auch angezeigt, was vor dem Start des Threads gesagt wurde. Über den Link einer Aufgabe zur zugehörigen Nachricht kannst du sie ebenfalls hier öffnen. Unten findest du **In Slack öffnen**.

Unter **Details** findest du den Namen, das Projekt und den Bereich (tippe darauf, um sie zu ändern), deine letzte Notiz und das Ergebnis eines Coding-Agenten. Über den Titel öffnest du den Chat. Eine erledigte Aufgabe bleibt kompakt. Die Nachricht, aus der sie entstanden ist, findest du unter **Details**.

Bei einer Aufgabe mit dem Vermerk „Wartet auf“ wird deine letzte Nachricht an die betreffende Person verlinkt, auf die du wartest: „E-Mail an Pat · Di“.

## Selbst eine Aufgabe erstellen

Mit **Neue Aufgabe** (am Computer unter **Suchen**, auf dem Smartphone über **+** oder mit `N`) kannst du eine Aufgabe für alles Mögliche erstellen. Beim Erstellen wird nichts gesendet. Wenn du weder **Arbeit** noch **Privat** auswählst, kommt die Aufgabe in den passenden Bereich, je nachdem, um wen oder was es geht. Die passende E-Mail, zu der die Aufgabe gehört, wird ebenfalls gefunden, auch wenn sie schon älter ist.

- **Fällig**: Gib einen Tag oder eine Uhrzeit ein, zum Beispiel „morgen“, „nächsten Fr“, „3. Nov.“, „14 Uhr“ oder „in 2 Stunden“. Das geht auch in deiner Sprache. Über das Kalendersymbol findest du Schnelloptionen und **Datum wählen**.
- **Wiederholt sich**: Die Aufgabe kommt regelmäßig wieder. Siehe [Wiederkehrende Aufgaben](recurring.md).
- **Person**: Verknüpfe bis zu 5 Personen oder Unternehmen, um die es bei der Aufgabe geht.
- Nachrichtensymbol: Hänge die betreffende Nachricht an, zum Beispiel eine E-Mail, Slack-, Teams-, WhatsApp- oder Telegram-Nachricht oder eine andere Nachricht, auf die The Machine Zugriff hat. Suche nach Text oder Absender. Bei jedem Treffer wird angezeigt, woher er stammt, wer ihn gesendet hat und wann.
- **Dateien**: Tippe auf die Büroklammer, füge einen Screenshot ein oder zieh Dateien auf das Formular. Auf dem Smartphone kannst du mit der Kamera daneben ein Foto aufnehmen. Wie im Chat kannst du bis zu 5 Dateien hinzufügen (siehe [Dateien hinzufügen](card-chat.md#add-files)). Mit × entfernst du eine Datei.

Die Dateien bleiben bei der Aufgabe. The Machine liest sie, wenn sie daran arbeitet. Auch Dateien allein reichen aus: Sie erstellt die Aufgabe aus einer PDF- oder Textdatei. Ein Foto wird als kleines Bild angezeigt. Tippe darauf, um es in voller Größe zu sehen.
