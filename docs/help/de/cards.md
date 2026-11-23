---
title: Aufgaben
area: cards
summary: Eine Aufgabe für alles, was dich braucht, bereit für dein Okay. Was die einzelnen Teile einer Aufgabe bedeuten.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 88ccf5426e5a538f
---
Deine Machine liest alles Neue und erstellt nur dann eine Aufgabe, wenn etwas dich braucht. Eine Aufgabe pro Thema, egal über wie viele Nachrichten es sich erstreckt.

## Wo Aufgaben zu finden sind

Auf der Seite **Aufgaben** sind sie gruppiert:

- **Gerade erledigt**: Ganz oben siehst du den letzten Schritt, den du bestätigt hast, zum Beispiel ein Formular oder ein Problem, das erledigt wurde, während du nicht da warst. Er bleibt höchstens einen Tag lang sichtbar, bis du auf **Verstanden** tippst. Auch dein Handy wird darüber informiert.
- **Für dich**: Alles, worauf du reagieren musst, zuerst das Dringendste. Jede Aufgabe ist mit **Vorbereitet** gekennzeichnet (ein Entwurf oder Ergebnis ist fertig, und mit **Ausführen** oder **Senden** wird es umgesetzt), **Braucht dich** (zuerst ist eine Entscheidung oder Antwort von dir nötig; wenn die Arbeit an etwas hängt, das nur du liefern kannst, etwa eine Information, eine Anmeldung oder eine Entscheidung, steht unter dem Titel, was fehlt), **Wird vorbereitet…** (deine Machine arbeitet daran) oder **Zum Lesen** (eine Zusammenfassung oder ein Briefing, bei dem nichts entschieden werden muss).
- **Älter**: Eingeklappte Aufgaben, zu denen es seit einer Woche nichts Neues gibt (siehe unten).
- **Wartet auf andere**: Eingeklappte Aufgaben, bei denen der nächste Schritt bei jemand anderem liegt (siehe unten).
- **Kommt später zurück**: Zurückgestellte Aufgaben und Aufgaben ohne Antwort auf **Noch nötig?** (siehe unten).
- **Versprechen**: Was du versprochen hast und was andere dir versprochen haben. Mehr dazu unter [Versprechen](promises.md).
- **Erledigt / verworfen**: Alle abgeschlossenen Aufgaben, neueste zuerst, mit dem Zeitpunkt des Abschlusses, zum Beispiel „Vor 5 Minuten erledigt“. Aufgaben, die anscheinend schon erledigt sind, sind mit **Sieht erledigt aus** gekennzeichnet.

Nach dem Senden steht in einer kurzen Mitteilung, wohin die Aufgabe verschoben wurde, zum Beispiel „Gesendet. Nach Erledigt verschoben.“ oder „Gesendet. Bis Mo. nach Später verschoben.“ Wenn eine Antwort nur verspricht, die Arbeit zu erledigen, etwa „Ich schicke es bis Dienstag“, bleibt die Aufgabe offen: „Gesendet. Offen gelassen.“ Mit **Öffnen** kommst du zur Aufgabe. Über die Suche findest du Aufgaben nach Titel oder Empfänger, auch unter Später und Erledigt.

Unter **Für dich** stehen zuerst überfällige Aufgaben und Aufgaben, die bis morgen fällig sind, dann Fragen aus deiner Fleet, anschließend Nachfassnachrichten zu einem Board und danach alles Weitere. Innerhalb jeder Gruppe stehen die neuesten Aufgaben zuerst. Eine Aufgabe behält ihren Platz, während deine Machine sie vorbereitet und auch, wenn sie erledigt ist. Nur ihre Markierung ändert sich. In den anderen offenen Gruppen stehen zuerst überfällige Aufgaben und Aufgaben, die bis morgen fällig sind, danach die neuesten. In der Seitenleiste bleibt die Reihenfolge gleich.

**Sieht erledigt aus** bedeutet, dass deine Machine die Aufgabe für erledigt hält, etwa „PR #3451 zusammengeführt“, sie aber noch nicht geschlossen ist. Mit **Wieder öffnen** kommt sie zurück auf deine Liste, und deine Machine lernt daraus. Diese Aufgaben werden nie als verspätet angezeigt. Wenn sie in einer Nachricht auftauchen, werden sie nach einem Tag automatisch geschlossen und **Rückgängig** wird angezeigt. Ansonsten warten sie auf **Als erledigt markieren**. Eine Aufgabe, die du bereits selbst erledigt hast, zum Beispiel mit einer Antwort in Gmail oder Slack, wird ebenfalls automatisch geschlossen.

Wenn eine Nachricht von einer Adresse kommt, die nur wie die einer bekannten Person aussieht, etwa sam@acme-corp.example statt sam@acmecorp.example, steht bei der Aufgabe unmissverständlich: „Das ist nicht Sam Lee.“ Die Person wird mit ihrer tatsächlichen Adresse angezeigt, nie mit dem Namen, den sie verwendet hat. Deine Machine prüft solche Nachrichten mit der Person unter der Adresse, die du bereits kennst, nicht mit der schreibenden Person.

Bei einer Aufgabe, die noch auf jemand anderen wartet, etwa auf eine Prüfung oder Antwort, steht **Wartet auf:** und der jeweilige Schritt. Sie bleibt eingeklappt unter **Wartet auf andere**, oberhalb von Kommt später zurück, bis eine neue Nachricht sie wieder hervorholt. Das gilt auch, wenn du eine Rückfrage gestellt hast: Die Aufgabe kommt am Morgen vor dem Abgabetermin zurück, bei einem Termin noch heute zum Termin selbst oder am nächsten Morgen, wenn der Termin bereits verstrichen ist. Außerdem steht dabei, auf wen sie noch wartet.

Wenn es bei einer Aufgabe um ein Ergebnis geht, das jemand anderes liefern soll, etwa einen unterschriebenen Vertrag, wird es unter **Details** als **Fertig, wenn** angezeigt. Wenn du deinen Teil abschickst, wird die Aufgabe nicht geschlossen. Sie bleibt unter **Wartet auf andere**, bis eine Nachricht das Ergebnis bestätigt. Dann wird sie automatisch geschlossen und **Rückgängig** angezeigt. Wenn bis zum Zeitpunkt fürs Nachfassen nichts kommt, erscheint sie wieder mit **Schreib eine kurze Erinnerung** im Chat. Schreib im Chat, was als erledigt gilt, um das zu ändern.

Eine Aufgabe, zu der es eine Woche lang nichts Neues gibt, wird von Für dich nach **Älter** verschoben. So stehen nach ein paar Tagen Abwesenheit die neuen Aufgaben zuerst. Nichts Neues bedeutet: keine neue Nachricht dazu und nichts, was du damit gemacht hast, etwa eine Chatnachricht, eine Bearbeitung oder ein Zurückstellen. Sie nur anzusehen zählt nicht.

Dringende Aufgaben, bald fällige Aufgaben und Aufgaben, bei denen der Versand läuft, bleiben unter Für dich. Mit **Alle verwerfen** werden alle Aufgaben unter Älter nach einer Bestätigung als nicht nötig markiert. Das funktioniert wie **Nicht nötig**, mit dem du Aufgaben einzeln verwirfst. **Rückgängig** wird angezeigt. Gibt es bei einer Aufgabe etwas Neues, kommt sie zurück zu Für dich.

Wenn sich eine Woche lang niemand um eine Aufgabe gekümmert hat, wird einmal gefragt: **Noch nötig?** Mit **Nicht nötig** wird sie geschlossen, und **Rückgängig** wird angezeigt. Mit **Behalten** bleibt sie bestehen und es wird nie wieder danach gefragt. Wenn nach einer weiteren Woche noch keine Antwort da ist, wird sie unter Kommt später zurück eingeklappt. Sie wird dann nicht mehr auf dem App-Symbol oder in der morgendlichen Zusammenfassung mitgezählt. Wenn du sie öffnest, eine Chatnachricht schreibst, sie bearbeitest, zurückstellst oder eine neue Nachricht dazu kommt, erscheint sie wieder.

Ein Projekt, bei dem es ruhig geworden ist und keine Aufgaben mehr offen sind, kann einmal pro Woche eine Aufgabe mit einem konkreten nächsten Schritt erhalten, höchstens drei pro Woche. Mehr dazu unter [Projekte](projects.md).

Wenn nichts deine Aufmerksamkeit braucht, macht deine Machine ein Nickerchen und zeigt eine leere Liste. Während sie prüft, wird sie wach und sagt Bescheid. Wenn eine Prüfung fehlgeschlagen ist oder sich verspätet, steht das in der Zeile darunter. **Jetzt prüfen** wird angezeigt.

Mit **Alle**, **Arbeit** und **Privat** oben in der Seitenleiste kannst du alle Aufgaben oder nur eine Art davon anzeigen. Auf deinem Handy und Computer gilt dieselbe Auswahl. Wenn Arbeit oder Privat ausgewählt ist, führt **Alle anzeigen** zurück zur Gesamtansicht. Eine Meldung über deine Machine selbst, etwa wenn ein Prozess immer wieder neu startet, gehört weder zu Arbeit noch zu Privat und wird nur unter Alle angezeigt.

Über die Zeile oben in der Liste wechselst du direkt zur anderen Ansicht: Unter **Nur privat** tippst du auf **Arbeit** oder **Alle anzeigen**.

In der Zeile oben in der Liste stehen der Name deiner letzten morgendlichen oder abendlichen Zusammenfassung und die Anzahl der Aufgaben, zum Beispiel **Zusammenfassung von gestern Abend** · 12 erledigt, 3 offen. Tippe darauf, um die Zusammenfassung erneut zu lesen. Mit **Kopieren** kannst du sie überall einfügen. Sobald du sie öffnest oder auf ihr **×** tippst, ist sie auf all deinen Geräten verfügbar, bis die nächste Zusammenfassung kommt.

Wenn es keine aktuelle Zusammenfassung gibt, wird **Heute bisher** angezeigt: Was heute erledigt wurde und was noch offen ist, für Arbeit und Privat oder nur für die ausgewählte Ansicht.

Bei einer Aufgabe zu einem Projekt steht der Projektname unter dem Titel. Tippe darauf, um das Projekt zu öffnen. Unter **Details** kannst du mit **Projekt** das Projekt ändern oder entfernen. Mehr dazu unter [Aufgaben eines Projekts](projects.md#a-project-s-to-dos).

Mit **Bereich** unter **Details** verschiebst du eine Aufgabe in deinen anderen Bereich. Die Nachrichten, die sie lesen und senden darf, wechseln mit. Mit **Rückgängig** in der Mitteilung verschiebst du sie zurück.

Wenn eine Aufgabe in deinen anderen Bereich verschoben werden muss, damit es weitergehen kann, und alle zugehörigen Nachrichten bereits dort sind, wird sie automatisch dorthin verschoben und fortgesetzt. Andernfalls wird **Nach Arbeit verschieben** angezeigt. Verschoben wird erst, wenn du darauf tippst. Eine Aufgabe, die du ohne Auswahl von Arbeit oder Privat hinzugefügt hast, wird automatisch verschoben, sobald klar ist, wohin sie gehört. Bis dahin gehört sie weder zu Arbeit noch zu Privat und bleibt privat.

Eine Aufgabe kann immer die Nachrichten lesen, aus denen sie entstanden ist. Wenn sie weitere Nachrichten aus deinem anderen Bereich braucht, fragt sie mit **Diese E-Mail für diese Aufgabe verwenden** nach. Ein Arbeits-Postfach, das du als Privat gekennzeichnet hast, zählt als Privat. E-Mails für ein anderes deiner Unternehmen landen in den Aufgaben dieses Unternehmens. Eine Aufgabe zu deinem Privatleben, etwa wenn deine Familie an deine Arbeitsadresse schreibt, ist von Anfang an privat.

Arbeit, die dich über ein privates Konto erreicht, etwa eine Kundin auf WhatsApp oder eine Bestellung in deinem privaten Postfach, zählt von Anfang an als Arbeit. Eine Aufgabe, die du selbst verschoben oder zugeordnet hast, bleibt immer dort, wo du sie abgelegt hast. Arbeit oder Privat bestimmt, wo eine Aufgabe angezeigt und mit wem sie geteilt wird, aber nicht, wohin die Antwort geht: Sie wird immer dort gesendet, wo die Unterhaltung stattfindet, auch nach einem Wechsel, außer du wählst einen anderen Weg.

Eine solche private Aufgabe antwortet weiterhin von der Arbeitsadresse, an die die E-Mail gesendet wurde. Sie wird nie in einer Work Fleet oder im Team Graph angezeigt.

Wenn mindestens zwei Aufgaben auf dich warten, kannst du mit **Durchgehen** in der Kopfzeile von Für dich die Aufgaben nacheinander in Listenreihenfolge abarbeiten. Jeder Entwurf wird vollständig angezeigt, mit **Senden** oder **Ausführen**, **Änderungen anfragen**, **Zurückstellen** und **Überspringen**. Am Computer sendet Enter den angezeigten Inhalt, `S` stellt zurück, `→` überspringt und Esc bricht ab. In der Kopfzeile steht, wie lange es in deinem Tempo ungefähr dauert, etwa „ca. 2 Min.“

Am Ende wird gezählt, was gesendet oder geschlossen wurde und was noch vorbereitet wird.

Eine Aufgabe, die dir eine Frage stellt, ist bei beidem ausgenommen: Sie wartet auf deine Antwort, nicht auf einen Tipp.

## Jetzt prüfen

Deine Machine liest jede Quelle alle paar Minuten, Tag und Nacht. Sie prüft neue Nachrichten, sobald 40 Nachrichten eingegangen sind oder die älteste Nachricht einer Person seit 15 Minuten wartet. Newsletter, Benachrichtigungen und Belege werden innerhalb einer Stunde bei der nächsten Prüfung berücksichtigt.

Nachts, von 00:00 bis 06:30 Uhr, pausieren die Prüfungen. Neue Nachrichten werden weiterhin gelesen und gespeichert und um 06:30 Uhr gemeinsam geprüft, damit deine Aufgaben vor der morgendlichen Zusammenfassung bereit sind. Unter Verbindungen steht bei den Prüfungen: „Nachts pausiert, wird um 06:30 Uhr nachgeholt“. Wenn du nachts in der App klickst, tippst oder scrollst, im Chat schreibst oder eine Aufgabe öffnest, laufen die Prüfungen wie gewohnt, bis du eine Stunde lang nicht aktiv warst. Mit **Jetzt prüfen** wird immer sofort geprüft.

Mit **Jetzt prüfen** werden alle Quellen sofort gelesen. Wenn keine Aufgabe offen ist, tippe auf die Zeile deiner Machine, um sie zusammen mit **Details** zu sehen. Dadurch werden die Prüfungen unter Verbindungen geöffnet. Wenn Aufgaben offen sind, findest du die Zeile am Computer ganz oben. Eine kurze Meldung wird dort nur angezeigt, während eine Prüfung läuft oder wenn sie fehlgeschlagen ist oder sich verspätet. Du kannst auch im Chat danach fragen.

LinkedIn, X und Salesflare haben ihren eigenen Rhythmus.

## Letzte Prüfung

Nach einer Prüfung, bei der neue Nachrichten gelesen wurden, steht über deinen Aufgaben, was gefunden wurde. Die Meldung umfasst alle gelesenen Quellen, etwa „13 Nachrichten um 16:11 Uhr geprüft · keine neue Aufgabe“ oder „· 2 neue Aufgaben“. Sie bezieht sich nur auf diese Prüfung. Aufgaben, die bereits auf deiner Liste stehen, bleiben unverändert. Wenn eine neue Aufgabe auf einen passenden Zeitpunkt warten soll, etwa auf deine morgendliche Zusammenfassung, steht dabei, bis wann: „1 Aufgabe bis morgen 08:30 Uhr zurückgehalten“.

Tippe auf die Zeile, um alle E-Mail-Threads, Chats und Benachrichtigungen mit dem Symbol der jeweiligen Quelle zu sehen: wer geschrieben hat, den Betreff oder die ersten Wörter sowie die neue Aufgabe oder den Grund, warum nichts nötig war, etwa „Nur in Cc, ein Teammitglied antwortet“ oder „Termin für Donnerstag steht schon fest“. Bei einem Thread wird kein Grund angezeigt, wenn die Prüfung nur einen vagen Grund ergeben hat. Tippe auf einen Eintrag, um ihn zu lesen.

Die ersten 10 Einträge werden angezeigt. Tippe darunter, um die restlichen zu sehen. Eine Zahl hinter einem Namen, etwa (3), gibt an, wie viele neue Nachrichten dieser Chat enthält. Eine Handybenachrichtigung zu einer Nachricht, die bereits aufgelistet ist, wird nur einmal angezeigt. Die Zeile bleibt nach der Prüfung 12 Stunden lang sichtbar.

Es werden nur E-Mails gezählt, die an dich gesendet wurden. Deine eigenen Antworten werden als Kontext und auf Versprechen hin gelesen, zählen aber nicht als neue E-Mails. E-Mails, die The Machine selbst an dich sendet, etwa deine morgendliche Zusammenfassung oder eine Meldung zu einer Fehlerbehebung, werden nie gelesen oder aufgelistet. E-Mails zu einer Abrechnung, deiner Testphase oder einer Einladung werden wie gewohnt gelesen.

## Die Schaltflächen

Bei einer Aufgabe wird der nächste Schritt angezeigt, etwa **Ausführen** oder **Prüfen und senden**, daneben **Zurückstellen**. Mehr dazu unter [Ausführen](do-it.md) und [Zurückstellen](snooze.md).

Mit **Änderungen anfragen** kannst du angeben, was geändert werden soll: wie etwas erledigt werden soll oder, sobald ein Entwurf fertig ist, was daran geändert werden soll. Mit **Als erledigt markieren** gibst du an, dass die Aufgabe erledigt ist. Bei einer vorbereiteten Aufgabe ohne Entwurf ist die Option direkt sichtbar. Andernfalls findest du sie oben unter **…**, auch bei Aufgaben, die deine Entscheidung brauchen. Die Aufgabe verschwindet sofort aus der Liste. In der Mitteilung wird **Rückgängig** angezeigt. Wische die Nachricht weg oder ziehe sie mit der Maus aus der Liste, um sie schneller zu schließen. Die Änderung bleibt bestehen.

Wenn die Aufgabe anders erledigt werden soll, sag es im **Chat**. In der Antwort steht nur, was sich geändert hat, etwa eine Zurückstellung und bis wann. Wenn sich etwas nicht ändern ließ, etwa ein Fälligkeitsdatum, wird das ebenfalls gesagt.

Unter **…**:

- **Übergeben…**: Weise die Aufgabe einem Teammitglied, [Claude Code oder Codex](hand-to-agent.md) zu oder [bitte jemanden um eine Prüfung](ask-to-review.md).
- **Wiederholen…**: Die Aufgabe [kommt regelmäßig zurück](recurring.md).
- **Nicht nötig**: Die Aufgabe verschwindet. Du kannst angeben, warum: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Tippe auf den Titel oder unter **Details** auf **Name**, um die Aufgabe umzubenennen. Du kannst auch im Chat darum bitten, etwa mit „Benenne sie in … um“. Dein Titel bleibt erhalten.

Mit **Wieder öffnen** holst du eine geschlossene Aufgabe zurück. Sie erscheint auch automatisch wieder, wenn etwas Neues passiert, etwa eine neue Nachricht von der anderen Person, aber nicht bei deiner eigenen Antwort. Dann wird angezeigt, wann sie zurückgekommen ist, und sie wird wie eine neue Aufgabe sortiert. Der Chat wird dort fortgesetzt, wo er aufgehört hat, auch nach mehreren Wochen.

Eine Rechnung, die du selbst bezahlen musst, wird unabhängig vom Land zu einer Aufgabe. Sie enthält den Betrag, das Fälligkeitsdatum und die Zahlungsdetails auf der Rechnung. Automatisch bezahlte Rechnungen, etwa per Lastschrift oder gespeicherter Karte, werden nicht aufgenommen. Wenn eine spätere E-Mail die Zahlung bestätigt, etwa vom Absender, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** holst du sie für einen Tag zurück.

Eine Aufgabe, die nur bis zu einem bestimmten Zeitpunkt wichtig war, etwa eine Bestätigung vor einem Termin, wird nach diesem Zeitpunkt automatisch geschlossen. Sie wird unter **Erledigt / verworfen** als „Nicht mehr nötig“ abgelegt. Mit **Rückgängig** holst du sie für einen Tag zurück.

Bevor eine Nachricht oder Übergabe für jemand anderen als bereit angezeigt wird, prüft deine Machine deine letzten Chats mit den beteiligten Personen, auch Gruppenchats, und wartet, bis Slack sie gelesen hat. Wenn eine spätere Nachricht zeigt, dass die Aufgabe bereits erledigt ist, etwa weil jemand gefragt wurde und zugestimmt hat, wird sie automatisch geschlossen. Mit **Rückgängig** holst du sie für einen Tag zurück.

Wenn jemand anderes in derselben Unterhaltung geschrieben hat, nachdem dein Entwurf erstellt wurde, wird das Senden mit **Senden** angehalten: „Nicht gesendet: Neue Nachricht im Thread“. Bei der Aufgabe wird diese Nachricht mit **Lesen** und **Für diese Nachricht neu machen** angezeigt. Tippe erneut auf **Senden**, um deinen Entwurf unverändert abzuschicken.

Wenn eine neuere Nachricht den Plan ändert, etwa weil eine Feier an einen anderen Ort verlegt oder eine Buchung storniert wurde, aktualisiert The Machine die Aufgaben selbst. Eine Aufgabe, die weiterhin wichtig ist, folgt dem neuen Plan. Wenn nichts mehr zu tun ist, wird sie unter **Erledigt / verworfen** als „Nicht nötig“ abgelegt. Im Chat steht „Aktualisiert:“ mit einer Begründung. Mit **Rückgängig** holst du sie für einen Tag zurück.

Bei deinen ersten Aufgaben wird ein kurzer Tipp mit den wichtigsten Aktionen angezeigt: **Änderungen anfragen** und **Nicht nötig**. Außerdem erfährst du, dass nichts gesendet wird, bevor du auf **Senden** tippst. Ein Tipp verschwindet endgültig, sobald du die zugehörige Schaltfläche verwendest oder auf × tippst.

An deinem ersten Tag begrüßt dich die Kopfzeile von Aufgaben und nennt die Person, die am längsten auf deine Antwort wartet. Diese Antwort wird zuerst als Entwurf erstellt, damit sie bereit ist, wenn du kommst.

Jede Aufgabe beginnt mit ihrem Titel. In der Zeile darunter stehen die Person, um die es geht, die Organisation, wenn die Aufgabe eine betrifft, das Projekt, Arbeit oder Privat und der Zeitpunkt, zu dem die Aufgabe eingegangen ist. Die Organisation wird nicht allein deshalb genannt, weil jemand dort arbeitet. Tippe auf einen Namen, um die Seite der Person im Graph zu öffnen.

Bei einem Namen oder einer Organisation wird das Foto oder Logo angezeigt, wenn es im Graph hinterlegt ist. Andernfalls erscheinen die Initialen. Ein Logo, das in der kleinen Größe schwer zu lesen wäre, etwa weiße Schrift auf transparentem Hintergrund oder ein breites Wortzeichen, wird ebenfalls durch Initialen ersetzt.

Manchmal steht in einer unauffälligen Zeile, was nicht bekannt ist, etwa „Letzter Kontakt vor 12 Tagen per E-Mail, seitdem nichts“. Sie wird angezeigt, wenn der letzte Kontakt schon länger her oder unbeantwortet ist. Auch nicht verbundene Kanäle wie WhatsApp werden genannt. Deine Machine sagt, was sie nicht weiß, statt zu raten.

Wenn ein nicht verbundener Kanal genannt wird, öffnet **Verbinden** daneben die Verbindung.

Ein Titel beschreibt, was zu tun ist, und ändert sich nur, wenn sich die Aufgabe ändert. Eine erledigte Aufgabe behält ihren Titel. Darunter steht, wie sie erledigt wurde, etwa „Erledigt: Sam hat am Dienstag unterschrieben“.

Über dem Entwurf steht in einer unauffälligen Zeile, aus welcher Nachricht er stammt, samt Logo des Dienstes. Tippe darauf, um den Thread zu lesen. Am Logo im Entwurf siehst du, wohin er gesendet wird, etwa als Slack-Antwort oder E-Mail.

Wenn der Entwurf auf einem Beitrag an anderer Stelle beruht, etwa einem Vorschlag eines Teammitglieds in Slack, steht das in einer Zeile, etwa „Basierend auf Sams Nachricht in #ops“. Tippe darauf, um die Nachricht zu lesen.

Ein Chat in Slack, WhatsApp, Telegram, Intercom und anderen Diensten wird als eine Unterhaltung angezeigt, von der ältesten Nachricht an: zuerst die Nachrichten vor der Nachricht, um die es bei der Aufgabe geht, danach die Antworten. In WhatsApp, Telegram oder Signal stehen deine Nachrichten rechts, wie in der App. Die Nachricht zur Aufgabe ist mit „Diese Aufgabe“ markiert und wird geöffnet angezeigt. Mit **Frühere Nachrichten anzeigen** kommen ältere Nachrichten hinzu. Bei einer E-Mail ist der restliche Thread oberhalb und unterhalb davon eingeklappt.

Mit **In Gmail öffnen** wird die E-Mail in dem Gmail-Konto geöffnet, in dem sie eingegangen ist. Auf Android öffnet sie sich in der Gmail-App, sofern du diese installiert hast.

Unter **Details** einer E-Mail stehen nur Angaben, die nicht schon im Kopf der E-Mail enthalten sind, etwa vollständige Cc-Adressen, Bcc oder eine abweichende Antwortadresse. Gibt es nichts hinzuzufügen, wird nichts angezeigt.

Bei einer Antwort in einem Slack-Thread werden auch die Nachrichten vor Beginn des Threads angezeigt. Über den Link einer Aufgabe zu ihrer eigenen Nachricht kannst du sie ebenfalls hier öffnen. Unten findest du **In Slack öffnen**.

Unter **Details** stehen Name, Projekt und Bereich (tippe auf einen Eintrag, um ihn zu ändern), deine letzte Notiz und das Ergebnis eines Coding-Agenten. Über den Titel öffnest du den Chat. Eine erledigte Aufgabe bleibt kompakt. Die Nachricht, aus der sie entstanden ist, steht unter **Details**.

Bei einer Aufgabe mit „Wartet auf“ wird deine letzte Nachricht an die Person verlinkt und daneben steht, worauf du wartest: „E-Mail an Pat · Di“.

## Aufgabe selbst erstellen

Mit **Neue Aufgabe** (am Computer unter **Suchen**, auf dem Handy über **+** oder mit `N`) kannst du für alles eine Aufgabe erstellen. Beim Erstellen wird nichts gesendet. Wenn du weder **Arbeit** noch **Privat** auswählst, wird die Aufgabe dem passenden Bereich zugeordnet, je nachdem, um wen und was es geht. Außerdem wird die E-Mail gefunden, an die sie anknüpft, auch wenn sie schon älter ist.

- **Fällig**: Gib einen Tag oder eine Uhrzeit ein, etwa „morgen“, „nächsten Fr“, „3. Nov“, „14 Uhr“ oder „in 2 Stunden“, auch in deiner Sprache. Über das Kalendersymbol findest du Vorschläge und **Datum wählen**.
- **Wiederholt sich**: Die Aufgabe kommt regelmäßig zurück. Mehr dazu unter [Wiederkehrende Aufgaben](recurring.md).
- **Person**: Verknüpfe bis zu 5 Personen oder Unternehmen, um die es geht.
- Nachrichtensymbol: Hänge die Nachricht an, um die es geht: eine E-Mail, eine Nachricht aus Slack, Teams, WhatsApp, Telegram oder einem anderen Dienst, auf den The Machine zugreifen kann. Suche nach Text oder Absender. Bei jedem Treffer siehst du die Quelle, den Absender und den Zeitpunkt.
- **Dateien**: Tippe auf die Büroklammer, füge einen Screenshot ein oder ziehe Dateien auf das Formular. Auf einem Handy kannst du mit der Kamera daneben ein Foto aufnehmen. Wie im Chat sind bis zu 5 Dateien möglich (siehe [Dateien hinzufügen](card-chat.md#add-files)). Mit × entfernst du eine Datei.

Die Dateien bleiben bei der Aufgabe, und The Machine liest sie, wenn sie daran arbeitet. Auch Dateien allein reichen aus: Aus einer PDF- oder Textdatei erstellt sie eine Aufgabe. Ein Foto wird als kleines Bild angezeigt. Tippe darauf, um es in voller Größe anzusehen.
