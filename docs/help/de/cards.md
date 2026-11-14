---
title: Aufgaben
area: cards
summary: Eine Aufgabe pro Sache, die dich braucht, bereit für dein Ja. Was die einzelnen Teile einer Aufgabe bedeuten.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: e4ad156150993936
---
Deine Machine liest alles Neue und erstellt nur dann eine Aufgabe, wenn etwas dich braucht. Eine Aufgabe pro Thema, egal über wie viele Nachrichten es sich erstreckt.

## Wo Aufgaben zu finden sind

Auf der Seite **Aufgaben** sind sie gruppiert:

- **Für dich**: alles, was auf dich wartet, zuerst das Dringendste. Bei jeder Aufgabe steht **Vorbereitet** (die Arbeit ist erledigt und **Ausführen** oder **Senden** führt sie aus), **Braucht dich** (zuerst braucht es deine Entscheidung oder Antwort) oder **Wird vorbereitet…** (deine Machine arbeitet daran).
- **Gerade erledigt**: Ein letzter Schritt, den du bestätigt hast, zum Beispiel ein Formular oder ein Vorgang, wurde ausgeführt, während du nicht da warst. Er bleibt dort, bis du auf **Verstanden** tippst, höchstens einen Tag lang. Du bekommst auch eine Benachrichtigung auf deinem Smartphone.
- **Kommt später zurück**: zurückgestellte Aufgaben und Aufgaben, auf die du nicht mit **Noch nötig?** geantwortet hast (siehe unten).
- **Versprechen**: was du versprochen hast und was andere dir versprochen haben. Siehe [Versprechen](promises.md).
- **Erledigt / verworfen**: alle abgeschlossenen Aufgaben, die neuesten zuerst, mit dem Zeitpunkt des Abschlusses, zum Beispiel „Vor 5 Minuten erledigt“. Aufgaben, die offenbar schon erledigt sind, sind mit **Scheinbar erledigt** markiert.

Nach dem Senden steht kurz da, wo die Aufgabe gelandet ist, zum Beispiel „Gesendet. Nach Erledigt verschoben.“ oder „Gesendet. Bis Mo. nach Später verschoben.“ Mit **Öffnen** gelangst du zur Aufgabe. Über die Suche findest du Aufgaben anhand ihres Titels oder danach, an wen sie gingen, auch unter Später und Erledigt.

Unter **Für dich** stehen zuerst überfällige Aufgaben oder Aufgaben, die bis morgen fällig sind, danach Fragen von deiner Fleet und dann der Rest. Innerhalb jeder Gruppe stehen die neuesten zuerst. Eine Aufgabe behält ihren Platz, während deine Machine sie vorbereitet und wenn sie erledigt ist. Nur ihre Markierung ändert sich. In den anderen offenen Gruppen stehen überfällige Aufgaben oder Aufgaben, die bis morgen fällig sind, zuerst, danach die neuesten. Die Seitenleiste behält dieselbe Reihenfolge.

**Scheinbar erledigt** bedeutet, dass deine Machine sieht, dass die Aufgabe erledigt ist, zum Beispiel „PR #3451 zusammengeführt“, sie aber noch nicht geschlossen wurde. Mit **Wieder öffnen** kommt sie zurück auf deine Liste und deine Machine lernt daraus. Diese Aufgaben werden nie als verspätet angezeigt. Nach einem Tag wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Eine Aufgabe, die du schon selbst erledigt hast, zum Beispiel durch eine Antwort in Gmail oder Slack, wird ebenfalls automatisch geschlossen.

Eine Aufgabe, die noch auf jemand anderen wartet, zum Beispiel auf eine Prüfung oder eine Antwort, zeigt den wartenden Schritt unter **Wartet auf:** an. Sie bleibt unter **Wartet auf andere**, eingeklappt oberhalb von „Kommt später zurück“, bis eine neue Nachricht sie wieder hervorholt. Dasselbe gilt, wenn du eine Rückfrage gestellt hast: Die Aufgabe kommt am Morgen vor der Frist zurück, bei einer Frist im Laufe des heutigen Tages zum Zeitpunkt der Frist oder nach Ablauf der Frist am nächsten Morgen. Sie zeigt, auf wen sie noch wartet.

Wenn es bei einer Aufgabe um ein Ergebnis geht, das jemand anderes liefern muss, zum Beispiel einen unterschriebenen Vertrag, wird es unter **Details** bei **Fertig, wenn** angezeigt. Wenn du deinen Teil sendest, wird die Aufgabe nicht geschlossen. Sie wartet unter **Wartet auf andere**, bis eine Nachricht das Ergebnis bestätigt. Dann wird sie automatisch geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Wenn bis zum Zeitpunkt, an dem du nachhaken solltest, nichts kommt, erscheint die Aufgabe wieder mit **Schreib eine kurze Erinnerung** im zugehörigen Chat. Schreib im Chat, was als erledigt gilt, um das zu ändern.

Eine Aufgabe, die eine Woche lang niemand angerührt hat, fragt einmal: **Noch nötig?** Mit **Nicht nötig** wird sie geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Mit **Behalten** bleibt sie bestehen und fragt nie wieder nach. Wenn du eine weitere Woche lang nicht antwortest, wird sie unter „Kommt später zurück“ eingeklappt. Sie wird dann nicht mehr auf dem App-Symbol und in der morgendlichen Zusammenfassung mitgezählt. Wenn du sie öffnest, eine Chatnachricht schreibst, sie bearbeitest oder zurückstellst oder eine neue Nachricht eingeht, kommt sie wieder zurück.

Ein Projekt, bei dem es seit einer Weile ruhig ist und keine offenen Aufgaben mehr gibt, kann einmal pro Woche eine Aufgabe mit einem konkreten nächsten Schritt erhalten, höchstens drei pro Woche. Siehe [Projekte](projects.md).

Wenn dich nichts braucht, macht deine Machine ein Nickerchen und zeigt eine leere Liste. Während sie etwas prüft, wacht sie auf und sagt dir Bescheid. Wenn eine Prüfung fehlgeschlagen oder überfällig ist, steht das in ihrer Zeile. Darunter findest du **Jetzt prüfen**.

Mit **Alle**, **Arbeit** und **Privat** oben in der Seitenleiste werden alle Aufgaben oder nur Aufgaben einer bestimmten Art angezeigt. Auf deinem Smartphone und Computer gilt dieselbe Auswahl. Wenn „Arbeit“ oder „Privat“ ausgewählt ist, kommst du über **Alle anzeigen** zurück zur Gesamtansicht. Eine Meldung über deine Machine selbst, etwa dass ein Prozess immer wieder neu startet, gehört weder zu „Arbeit“ noch zu „Privat“ und erscheint nur unter „Alle“.

Über die Zeile oben in der Liste kannst du auch direkt zur jeweils anderen Ansicht wechseln: **Nur Privat · Arbeit · Alle anzeigen**.

In der Zeile oben in der Liste stehen der Name deiner letzten morgendlichen oder abendlichen Zusammenfassung und die Anzahl der darin erfassten Aufgaben, zum Beispiel **Zusammenfassung von gestern Abend** · 12 erledigt, 3 offen. Tippe darauf, um die Zusammenfassung erneut zu lesen. Mit **Kopieren** kannst du sie überall einfügen. Sobald du sie öffnest oder auf ihr **×** tippst, bleibt sie auf allen deinen Geräten verfügbar, bis die nächste Zusammenfassung kommt.

Wenn es keine aktuelle Zusammenfassung gibt, wird **Heute bisher** angezeigt: was heute erledigt wurde und was noch offen ist, für „Arbeit“ und „Privat“ oder nur für die Ansicht, die du ausgewählt hast.

Bei einer Aufgabe zu einem Projekt steht der Projektname unter dem Titel. Tippe darauf, um das Projekt zu öffnen. Unter **Details** kannst du bei **Projekt** das Projekt ändern oder die Aufgabe davon lösen. Siehe [Aufgaben eines Projekts](projects.md#a-projects-to-dos).

Unter **Details** kannst du mit **Bereich** eine Aufgabe in deinen anderen Bereich verschieben. Der Zugriff auf Nachrichten und die Möglichkeit, Nachrichten zu senden, werden dabei übernommen. Mit **Rückgängig** in der Meldung verschiebst du sie zurück.

Wenn eine Aufgabe deinen anderen Bereich braucht, um weiterzugehen, und alle Nachrichten, aus denen sie entstanden ist, dort liegen, wird sie automatisch dorthin verschoben und fortgesetzt. Andernfalls wird **Nach Arbeit verschieben** angezeigt und es wird nichts verschoben, bis du darauf tippst. Eine Aufgabe, die du hinzugefügt hast, ohne „Arbeit“ oder „Privat“ auszuwählen, wird automatisch dem passenden Bereich zugeordnet, sobald klar ist, wohin sie gehört. Bis dahin ist sie weder als „Arbeit“ noch als „Privat“ gekennzeichnet und bleibt privat.

Eine Aufgabe kann immer die Nachrichten lesen, aus denen sie entstanden ist. Wenn sie weitere Nachrichten aus deinem anderen Bereich braucht, fragt sie mit **Diese E-Mail für diese Aufgabe verwenden** nach. Ein Arbeits-Postfach, das du als „Privat“ gekennzeichnet hast, gilt als privat. E-Mails für ein anderes deiner Unternehmen gehören zu den Aufgaben dieses Unternehmens. Eine Aufgabe zu deinem Privatleben, etwa wenn deine Familie an deine Arbeitsadresse schreibt, ist von Anfang an privat.

Arbeit, die dich über ein privates Konto erreicht, zum Beispiel eine Nachricht von einem Kunden auf WhatsApp oder eine Bestellung in deinem privaten Postfach, gehört von Anfang an zu „Arbeit“. Eine Aufgabe, die du selbst verschoben oder zugeordnet hast, bleibt immer dort, wo du sie abgelegt hast. „Arbeit“ oder „Privat“ bestimmt, wo eine Aufgabe angezeigt und mit wem sie geteilt wird, aber nicht, von wo aus sie antwortet: Eine Antwort geht immer dorthin, wo die Unterhaltung stattfindet, auch nach dem Verschieben, es sei denn, du wählst einen anderen Weg.

Eine solche private Aufgabe antwortet weiterhin von der Arbeitsadresse, an die ihre E-Mail geschickt wurde. Sie wird nie in einer Work Fleet oder im Team Graph angezeigt.

Wenn mindestens zwei Aufgaben auf dich warten, kannst du mit **Durchgehen** in der Kopfzeile von „Für dich“ nacheinander durch sie gehen, in der Reihenfolge der Liste. Jede Aufgabe wird vollständig mit ihrem Entwurf angezeigt. Dazu gibt es **Senden** oder **Ausführen**, **Änderungen anfragen**, **Zurückstellen** und **Überspringen**. Auf einem Computer sendet Enter den angezeigten Inhalt, `S` stellt die Aufgabe zurück, `→` überspringt sie und Esc beendet den Vorgang. Unter dem Titel zeigt die Kopfzeile außerdem an, wie lange die Aufgaben dauern, wenn du sie in deinem eigenen Tempo erledigst, zum Beispiel „ca. 2 Min.“.

Eine Aufgabe, bei der dir eine Frage gestellt wird, ist von beidem ausgenommen: Sie braucht deine Antwort, keinen Tipp.

## Jetzt prüfen

Deine Machine liest jede Quelle tagsüber und nachts alle paar Minuten. Sie prüft neu eingegangene Nachrichten, sobald 40 Nachrichten vorliegen oder die älteste Nachricht einer Person seit 15 Minuten wartet. Newsletter, Benachrichtigungen und Belege werden innerhalb der nächsten Stunde bei der nächsten Prüfung berücksichtigt.

Nachts, von 00:00 bis 06:30, pausieren die Prüfungen. Neue Nachrichten werden weiterhin gelesen und gespeichert. Um 06:30 werden sie gemeinsam geprüft, damit deine Aufgaben vor der morgendlichen Zusammenfassung bereit sind. Unter „Verbindungen“ steht bei den Prüfungen „Nachts pausiert, wird um 06:30 nachgeholt“. Wenn du nachts die App öffnest, im Chat schreibst oder auf eine Aufgabe tippst, laufen die Prüfungen wieder wie gewohnt, bis du eine Stunde lang nicht aktiv warst. Mit **Jetzt prüfen** wird immer sofort geprüft.

Mit **Jetzt prüfen** werden alle Quellen sofort gelesen. Wenn keine Aufgabe offen ist, tippe auf die Zeile deiner Machine, um sie mit **Details** anzuzeigen. Dadurch werden die Prüfungen unter „Verbindungen“ geöffnet. Wenn Aufgaben offen sind, findest du die Zeile auf einem Computer ganz oben. Sie wird nur angezeigt, während eine Prüfung läuft oder wenn eine Prüfung fehlgeschlagen oder überfällig ist. Du kannst auch im Chat danach fragen.

LinkedIn, X und Salesflare haben ihren eigenen Rhythmus.

## Letzte Prüfung

Nach einer Prüfung, bei der neue Nachrichten gelesen wurden, steht über deinen Aufgaben, was gefunden wurde und aus welchen Quellen, zum Beispiel „13 Nachrichten um 16:11 geprüft · nichts braucht dich“ oder „· 2 neue Aufgaben“. Wenn eine neue Aufgabe auf einen besseren Zeitpunkt wartet, zum Beispiel auf deine morgendliche Zusammenfassung, steht dort, bis wann: „1 Aufgabe bis morgen 08:30 zurückgestellt“.

Tippe auf die Zeile, um alle E-Mail-Threads, Chats und Benachrichtigungen mit dem Symbol ihrer Quelle zu sehen. Angezeigt werden, wer geschrieben hat, der Betreff oder die ersten Wörter sowie die neue Aufgabe oder der Grund, warum nichts nötig war, zum Beispiel „Nur in CC, ein Teammitglied antwortet“ oder „Meeting für Donnerstag steht schon“. Wenn die Prüfung nur einen vagen Grund ergeben hat, wird bei einem Thread kein Grund angezeigt. Tippe auf einen Eintrag, um ihn zu lesen.

Die ersten 10 Einträge werden angezeigt. Tippe darunter, um den Rest zu sehen. Eine Zahl hinter einem Namen, zum Beispiel (3), zeigt, wie viele neue Nachrichten es in diesem Chat gibt. Eine Smartphone-Benachrichtigung zu einer Nachricht, die bereits aufgelistet ist, wird nur einmal angezeigt. Die Zeile bleibt nach der Prüfung 12 Stunden lang sichtbar.

Gezählt werden nur E-Mails, die an dich gerichtet sind. Deine eigenen Antworten werden für den Kontext und für Versprechen gelesen, zählen aber nicht als neue E-Mails. Die eigenen E-Mails von The Machine an dich, zum Beispiel deine morgendliche Zusammenfassung oder eine Benachrichtigung über eine Fehlerbehebung, werden nie gelesen oder aufgelistet. E-Mails zu Abrechnungen, deiner Testphase oder einer Einladung werden wie gewohnt gelesen.

## Die Schaltflächen

Bei einer Aufgabe steht der nächste Schritt, zum Beispiel **Ausführen** oder **Prüfen und senden**, daneben **Zurückstellen**. Siehe [Ausführen](do-it.md) und [Zurückstellen](snooze.md).

Mit **Änderungen anfragen** kannst du angeben, was geändert werden soll: wie die Aufgabe erledigt werden soll oder, sobald ein Entwurf bereit ist, was daran geändert werden soll. **Als erledigt markieren** bedeutet, dass die Aufgabe erledigt ist. Bei einer vorbereiteten Aufgabe ohne Entwurf ist die Schaltfläche direkt zu sehen. Andernfalls findest du sie oben unter **…**, auch bei einer Aufgabe, die deine Entscheidung braucht. Die Aufgabe verschwindet sofort aus der Liste. In der Meldung findest du **Rückgängig**. Wische die Meldung weg oder ziehe sie mit der Maus aus dem Fenster, um sie früher zu schließen. Die Änderung bleibt bestehen.

Wenn die Aufgabe anders erledigt werden soll, sag das im **Chat**.

Unter **…**:

- **Übergeben…**: Übergib die Aufgabe an ein Teammitglied, an [Claude Code oder Codex](hand-to-agent.md) oder [bitte jemanden um eine Prüfung](ask-to-review.md).
- **Wiederholen…**: Die Aufgabe [kommt regelmäßig wieder](recurring.md).
- **Nicht nötig**: Die Aufgabe wird entfernt. Du kannst optional einen Grund auswählen: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Tippe auf den Titel oder unter **Details** auf **Name**, um die Aufgabe umzubenennen. Dein Titel bleibt erhalten.

Mit **Wieder öffnen** holst du eine geschlossene Aufgabe zurück. Sie kommt auch automatisch zurück, wenn etwas Neues passiert, zum Beispiel eine neue Nachricht von der anderen Person, aber nicht nach deiner eigenen Antwort.

Eine Rechnung, die du selbst noch bezahlen musst, egal aus welchem Land, wird mit dem Betrag, dem Fälligkeitsdatum und den Zahlungsdetails auf der Rechnung zu einer Aufgabe. Rechnungen, die automatisch bezahlt werden, etwa per Lastschrift oder mit einer gespeicherten Karte, werden nicht zu Aufgaben. Wenn eine spätere E-Mail zeigt, dass die Rechnung bezahlt wurde, zum Beispiel eine Bestätigung des Absenders über den Zahlungseingang, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Eine Aufgabe, die nur bis zu einem bestimmten Zeitpunkt wichtig war, zum Beispiel eine Bestätigung vor einem Meeting, wird nach diesem Zeitpunkt automatisch geschlossen. Sie wird mit dem Vermerk „Nicht mehr nötig“ nach **Erledigt / verworfen** verschoben. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Bevor eine Nachricht oder Übergabe für jemanden als bereit angezeigt wird, prüft deine Machine deine letzten Chats mit den beteiligten Personen, auch Gruppenchats, und wartet darauf, dass Slack sie einliest. Wenn eine spätere Nachricht zeigt, dass die Aufgabe bereits erledigt ist, zum Beispiel weil jemand gefragt wurde und zugesagt hat, wird sie automatisch geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Wenn eine neuere Nachricht den Plan ändert, etwa weil eine Party an einen anderen Ort verlegt oder eine Buchung storniert wurde, aktualisiert The Machine ihre Aufgaben selbst. Eine Aufgabe, die weiterhin wichtig ist, wird an den neuen Plan angepasst. Wenn nichts mehr zu tun ist, wird sie mit dem Vermerk „Nicht nötig“ nach **Erledigt / verworfen** verschoben. Im Chat steht „Aktualisiert:“ mit einer Begründung. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Bei deinen ersten Aufgaben erscheint ein kurzer Tipp mit den wichtigsten Aktionen: **Änderungen anfragen** und **Nicht nötig**. Außerdem erfährst du, dass nichts gesendet wird, bevor du auf **Senden** drückst. Ein Tipp wird dauerhaft ausgeblendet, sobald du seine Schaltfläche verwendest oder auf × drückst.

Am ersten Tag begrüßt dich deine Aufgabenliste oben und nennt die Person, die am längsten auf deine Antwort wartet. Der Entwurf für diese Antwort wird zuerst erstellt, damit er bereit ist, wenn du kommst.

Jede Aufgabe beginnt mit ihrem Titel. In der Zeile darunter stehen, um wen es geht, gegebenenfalls die Organisation, das Projekt, „Arbeit“ oder „Privat“ und der Zeitpunkt, zu dem die Aufgabe einging. Die Organisation wird nur angezeigt, wenn es um sie geht, nicht einfach, weil jemand dort arbeitet. Tippe auf einen Namen, um die Seite dieser Person im Graph zu öffnen.

Bei einem Namen und einer Organisation wird das Foto oder Logo angezeigt, sofern der Graph eines hat. Andernfalls werden die Initialen angezeigt. Ein Logo, das in dieser Größe schwer zu erkennen wäre, etwa weiße Schrift auf transparentem Hintergrund oder ein breites Wortlogo, wird ebenfalls durch die Initialen ersetzt.

Manchmal zeigt eine unauffällige Zeile, was nicht bekannt ist, zum Beispiel „Letzter Kontakt vor 12 Tagen per E-Mail; seitdem nichts“. Sie erscheint, wenn der letzte Kontakt schon länger her ist oder unbeantwortet blieb. Außerdem nennt sie nicht verbundene Kanäle wie WhatsApp. Deine Machine sagt dir, was sie nicht weiß, statt zu raten.

Wenn ein nicht verbundener Kanal genannt wird, öffnet **Verbinden** daneben die entsprechende Verbindung.

Ein Titel sagt, was zu tun ist, und ändert sich nur, wenn sich das ändert. Eine erledigte Aufgabe behält ihren Titel. Darunter steht, wie sie abgeschlossen wurde, zum Beispiel „Erledigt: Sam hat es am Dienstag unterschrieben“.

Über dem Entwurf steht in einer unauffälligen Zeile, aus welcher Nachricht er stammt, samt Logo des jeweiligen Dienstes. Tippe darauf, um den Thread zu lesen. Das Logo über dem Entwurf zeigt, wohin er gesendet wird. So siehst du sofort, ob es eine Slack-Antwort oder eine E-Mail ist.

Wenn der Entwurf auf einer Eingabe an anderer Stelle basiert, zum Beispiel auf einem Vorschlag eines Teammitglieds in Slack, steht das in einer Zeile, etwa „Basierend auf Sam in #ops“. Tippe darauf, um die Nachricht zu lesen.

Ein Chat (Slack, WhatsApp, Telegram, Intercom …) wird als eine Unterhaltung angezeigt, beginnend mit den ältesten Nachrichten: erst die Nachrichten vor der Nachricht, auf die sich die Aufgabe bezieht, dann die Antworten darauf. In WhatsApp, Telegram oder Signal stehen deine Nachrichten wie in der App rechts. Die Nachricht zur Aufgabe ist mit „Diese Aufgabe“ markiert und wird direkt angezeigt. Mit **Frühere Nachrichten anzeigen** werden ältere Nachrichten eingeblendet. Bei einer E-Mail ist der restliche Thread darüber und darunter eingeklappt.

Unter **Details** einer E-Mail werden nur Angaben angezeigt, die nicht schon in der Kopfzeile stehen, zum Beispiel vollständige Cc-Adressen, Bcc oder eine abweichende Antwortadresse. Wenn es nichts hinzuzufügen gibt, werden keine Details angezeigt.

Bei einer Antwort in einem Slack-Thread wird auch angezeigt, was vor Beginn des Threads gesagt wurde. Über den Link einer Aufgabe zur zugehörigen Nachricht kannst du sie ebenfalls hier öffnen. Unten findest du **In Slack öffnen**.

Unter **Details** findest du den Namen, das Projekt und den Bereich (tippe auf einen Eintrag, um ihn zu ändern), deine letzte Notiz und das Ergebnis eines Coding-Agenten. Mit **Chat ›** öffnest du den Chat. Eine erledigte Aufgabe wird kompakt angezeigt. Die Nachricht, aus der sie entstanden ist, findest du unter **Details**.

Bei einer Aufgabe mit „Wartet auf“ führt ein Link zu deiner letzten Nachricht an die Person, auf deren Antwort du wartest: „E-Mail an Pat · Di“.

## Selbst eine Aufgabe erstellen

Mit **Neue Aufgabe** (auf einem Computer unter **Suchen**) kannst du eine Aufgabe für alles Mögliche erstellen. Beim Erstellen wird nichts gesendet. Wenn „Arbeit“ oder „Privat“ nicht ausgewählt ist, wird die Aufgabe dem passenden Bereich zugeordnet, je nachdem, um wen und was es geht. Außerdem findet sie die E-Mail, auf die sie sich bezieht, auch wenn sie schon älter ist.

- **Fällig**: Gib einen Tag oder eine Uhrzeit ein, zum Beispiel „morgen“, „nächsten Fr“, „3. Nov.“, „14 Uhr“ oder „in 2 Stunden“. Das geht auch in deiner Sprache. Über das Kalendersymbol findest du Schnellauswahlen und **Datum wählen**.
- **Nachricht**: Hänge die Nachricht an, um die es geht: eine E-Mail, Slack-, Teams-, WhatsApp-, Telegram- oder eine andere Nachricht, die The Machine hat. Suche nach Text oder Absender. Bei jedem Ergebnis wird angezeigt, woher es stammt, wer es gesendet hat und wann.
- **Dateien**: Tippe auf die Büroklammer, füge einen Screenshot ein oder ziehe Dateien auf das Formular. Auf einem Smartphone kannst du mit der Kamera daneben ein Foto aufnehmen. Bis zu 5 Dateien, wie im Chat (siehe [Dateien hinzufügen](card-chat.md#add-files)). Mit × entfernst du eine Datei.

Die Dateien bleiben bei der Aufgabe und The Machine liest sie, wenn sie daran arbeitet. Du kannst auch nur Dateien hinzufügen: The Machine erstellt die Aufgabe aus einer PDF- oder Textdatei. Ein Foto wird als kleines Bild angezeigt. Tippe darauf, um es in voller Größe zu sehen.
