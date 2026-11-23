---
title: Aufgaben
area: cards
summary: Eine Aufgabe pro Sache, die dich braucht, bereit für dein Okay. Was die einzelnen Teile einer Aufgabe bedeuten.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: e0fd02e557e6daee
---
Deine Machine liest alles Neue und erstellt nur dann eine Aufgabe, wenn etwas dich braucht. Eine Aufgabe pro Angelegenheit, egal über wie viele Nachrichten sie sich erstreckt.

## Wo Aufgaben zu finden sind

Auf der Seite **Aufgaben** sind sie gruppiert:

- **Gerade erledigt**: Ganz oben siehst du den letzten Schritt, den du bestätigt hast, zum Beispiel ein Formular oder einen Vorgang. Er wurde erledigt, während du nicht da warst. Er bleibt höchstens einen Tag lang dort, bis du auf **Verstanden** tippst. Auch dein Handy wird darüber benachrichtigt.
- **Für dich**: Alles, was auf dich wartet, nach Dringlichkeit sortiert. Bei jeder Aufgabe steht **Vorbereitet** (ein Entwurf oder Ergebnis ist bereit, und mit **Ausführen** oder **Senden** wird es umgesetzt), **Braucht dich** (erst ist deine Entscheidung oder Antwort nötig; wenn die Arbeit an etwas hängt, das nur du hast, etwa an einer Information, einer Anmeldung oder einer Entscheidung, steht unter dem Titel, worum es geht), **Wird vorbereitet…** (deine Machine arbeitet daran) oder **Zum Lesen** (eine Zusammenfassung oder ein Briefing, bei dem nichts zu entscheiden ist).
- **Älter**: Eingeklappte Aufgaben, zu denen es seit einer Woche nichts Neues gibt (siehe unten).
- **Wartet auf andere**: Eingeklappte Aufgaben, bei denen der nächste Schritt bei jemand anderem liegt (siehe unten).
- **Kommt später zurück**: Zurückgestellte Aufgaben und Aufgaben ohne Antwort auf **Noch nötig?** (siehe unten).
- **Versprechen**: Was du versprochen hast und was andere dir versprochen haben. Siehe [Versprechen](promises.md).
- **Erledigt / verworfen**: Alle abgeschlossenen Aufgaben, beginnend mit den neuesten, samt Abschlusszeit, zum Beispiel „Vor 5 Minuten erledigt“. Aufgaben, die schon erledigt zu sein scheinen, sind mit **Sieht erledigt aus** markiert.

Nach dem Senden steht in einer kurzen Meldung, wohin die Aufgabe verschoben wurde, zum Beispiel „Gesendet. Nach Erledigt verschoben.“ oder „Gesendet. Bis Mo. nach Später verschoben.“ Wenn eine Antwort nur verspricht, die Arbeit zu erledigen, etwa „Ich schicke es bis Dienstag“, bleibt die Aufgabe offen: „Gesendet. Offen gelassen.“ Über **Öffnen** gelangst du zur Aufgabe. Über die Suche findest du Aufgaben anhand ihres Titels oder der Person, an die sie gingen, auch unter Später und Erledigt.

Unter **Für dich** stehen zuerst überfällige oder bis morgen fällige Aufgaben, dann Fragen aus deiner Fleet, danach Nachfassnachrichten eines Boards und schließlich der Rest. Innerhalb jeder Gruppe stehen die neuesten zuerst. Eine Aufgabe behält ihren Platz, während deine Machine sie vorbereitet und wenn sie erledigt ist. Nur ihre Markierung ändert sich. In den anderen offenen Gruppen stehen überfällige oder bis morgen fällige Aufgaben zuerst, der Rest ist nach Aktualität sortiert. Die Seitenleiste behält dieselbe Reihenfolge.

**Sieht erledigt aus** bedeutet, dass deine Machine erkennt, dass etwas erledigt ist, zum Beispiel „PR #3451 zusammengeführt“, die Aufgabe aber noch nicht geschlossen wurde. Mit **Wieder öffnen** kommt sie zurück auf deine Liste, und deine Machine lernt daraus. Diese Aufgaben werden nie als überfällig angezeigt. Wenn eine Nachricht sie anzeigt, wird sie nach einem Tag automatisch geschlossen. Du kannst das mit **Rückgängig** rückgängig machen. Andernfalls wartet sie darauf, dass du **Als erledigt markieren** auswählst. Eine Aufgabe, die du selbst bereits erledigt hast, zum Beispiel mit einer Antwort in Gmail oder Slack, wird ebenfalls automatisch geschlossen.

Wenn eine Nachricht von einer Adresse kommt, die nur wie die Adresse einer Person aussieht, die du kennst, zum Beispiel sam@acme-corp.example statt sam@acmecorp.example, steht bei der Aufgabe klar: „Das ist nicht Sam Lee.“ Die Person wird mit ihrer eigenen Adresse angezeigt, nie mit dem Namen, den sie verwendet hat. Deine Machine überprüft solche Nachrichten bei der Person unter der Adresse, die du bereits kennst, nie bei der schreibenden Person.

Bei einer Aufgabe, die noch auf jemand anderen wartet, etwa auf eine Prüfung oder Antwort, steht **Wartet auf:** mit dem nächsten Schritt. Sie bleibt eingeklappt unter **Wartet auf andere**, oberhalb von „Kommt später zurück“, bis eine neue Nachricht sie wieder hervorholt. Dasselbe gilt, nachdem du eine Rückfrage gestellt hast: Die Aufgabe kommt am Morgen vor dem Abgabetermin zurück, am Abgabetermin selbst, wenn dieser später am selben Tag liegt, oder am nächsten Morgen, wenn der Termin bereits verstrichen ist. Außerdem steht dabei, auf wen sie noch wartet.

Wenn es bei einer Aufgabe um ein Ergebnis geht, das jemand anderes liefern muss, zum Beispiel einen unterschriebenen Vertrag, wird es unter **Details** bei **Fertig, wenn** angezeigt. Wenn du deinen Teil abschickst, wird die Aufgabe nicht geschlossen. Sie bleibt unter **Wartet auf andere**, bis eine Nachricht das Ergebnis bestätigt. Dann wird sie automatisch geschlossen. Du kannst das mit **Rückgängig** rückgängig machen. Wenn bis zum Zeitpunkt, an dem du nachhaken solltest, nichts eingetroffen ist, erscheint die Aufgabe wieder mit **Schreib eine kurze Erinnerung** in ihrem Chat. Sag im Chat, was als erledigt gilt, um das zu ändern.

Eine Aufgabe, zu der es eine Woche lang nichts Neues gab, wandert von „Für dich“ nach **Älter**, damit nach einigen Tagen Abwesenheit die neuen Aufgaben zuerst kommen. Als neu zählt eine neue Nachricht zur Aufgabe oder eine Aktion von dir, etwa eine Chatnachricht, eine Änderung oder das Zurückstellen. Sie nur anzusehen zählt nicht.

Dringende Aufgaben, bald fällige Aufgaben und Aufgaben mit einer ausstehenden Nachricht bleiben unter „Für dich“. Mit **Alle verwerfen** markierst du alle nicht nötigen Aufgaben unter „Älter“ nach einmaliger Bestätigung als **Nicht nötig**. Einzeln geht das ebenfalls mit **Nicht nötig**. In beiden Fällen kannst du es mit **Rückgängig** rückgängig machen. Gibt es etwas Neues zu einer Aufgabe, kommt sie zurück zu „Für dich“.

Wenn eine Aufgabe seit einer Woche niemand bearbeitet hat, fragt sie einmal: **Noch nötig?** Mit **Nicht nötig** wird sie geschlossen. Du kannst das mit **Rückgängig** rückgängig machen. Mit **Behalten** bleibt sie bestehen und wird nie wieder danach fragen. Wenn eine weitere Woche lang keine Antwort kommt, wird sie unter „Kommt später zurück“ eingeklappt, und sie wird nicht mehr auf dem App-Symbol oder in der morgendlichen Zusammenfassung mitgezählt. Wenn du sie öffnest, eine Chatnachricht schreibst, sie änderst oder zurückstellst oder eine neue Nachricht eintrifft, kommt sie zurück.

Einmal pro Woche kann für ein still gewordenes Projekt ohne offene Aufgaben eine Aufgabe mit einem konkreten nächsten Schritt erstellt werden, höchstens drei pro Woche. Siehe [Projekte](projects.md).

Wenn dich nichts braucht, macht deine Machine ein Nickerchen und deine Liste bleibt leer. Während sie prüft, wacht sie auf und sagt Bescheid. Wenn eine Prüfung fehlgeschlagen ist oder sich verspätet, steht das in der Zeile, mit **Jetzt prüfen** darunter.

Mit **Alle**, **Arbeit** und **Privat** oben in der Seitenleiste zeigst du alle Aufgaben oder nur eine Kategorie an. Auf deinem Handy und Computer gilt dieselbe Auswahl. Wenn „Arbeit“ oder „Privat“ ausgewählt ist, führt **Alle anzeigen** zurück zur Gesamtansicht. Eine Warnung zu deiner Machine selbst, etwa dass ein Teil immer wieder neu startet, gehört weder zu „Arbeit“ noch zu „Privat“ und wird nur unter „Alle“ angezeigt.

Über die Zeile oben in der Liste wechselst du direkt zur anderen Ansicht: Unter **Nur privat** tippst du auf **Arbeit** oder **Alle anzeigen**.

In der Zeile oben in der Liste stehen deine letzte morgendliche oder abendliche Zusammenfassung und die Zahl der darin erfassten Aufgaben, zum Beispiel **Zusammenfassung von gestern Abend** · 12 erledigt, 3 offen. Tippe darauf, um die Zusammenfassung erneut zu lesen. Mit **Kopieren** kannst du sie an beliebiger Stelle einfügen. Sobald du sie öffnest oder auf **×** tippst, bleibt sie auf allen deinen Geräten sichtbar, bis die nächste Zusammenfassung kommt.

Wenn es keine aktuelle Zusammenfassung gibt, wird **Heute bisher** angezeigt: was heute erledigt wurde und was noch offen ist, für „Arbeit“ und „Privat“ oder nur für die ausgewählte Ansicht.

Bei einer Aufgabe zu einem Projekt steht der Projektname unter dem Titel. Tippe darauf, um das Projekt zu öffnen. Unter **Details** kannst du das **Projekt** ändern oder entfernen. Siehe [Aufgaben eines Projekts](projects.md#a-project-s-to-dos).

Mit **Bereich** unter **Details** verschiebst du eine Aufgabe in deinen anderen Bereich. Der Zugriff darauf, was sie lesen und senden darf, wird mitverschoben. Über **Rückgängig** in der Meldung kannst du sie zurückverschieben.

Wenn eine Aufgabe den anderen Bereich braucht, um weiterzugehen, und alle Nachrichten, auf denen sie basiert, dort liegen, wird sie automatisch dorthin verschoben und fortgesetzt. Andernfalls wird **Nach Arbeit verschieben** angezeigt. Erst wenn du darauf tippst, wird etwas verschoben. Eine Aufgabe, die du hinzugefügt hast, ohne „Arbeit“ oder „Privat“ auszuwählen, wird automatisch verschoben, sobald klar ist, wohin sie gehört. Bis dahin gehört sie weder zu „Arbeit“ noch zu „Privat“ und bleibt privat.

Eine Aufgabe kann immer die Nachrichten lesen, aus denen sie entstanden ist. Wenn sie andere Nachrichten aus deinem anderen Bereich braucht, fragt sie mit **Diese E-Mail für diese Aufgabe verwenden** danach. Ein Arbeits-Postfach, das du als privat markiert hast, zählt als privat. E-Mails für ein anderes deiner Unternehmen gehören zu den Aufgaben dieses Unternehmens. Eine Aufgabe zu deinem Privatleben, etwa wenn deine Familie an deine Arbeitsadresse schreibt, ist von Anfang an privat.

Arbeit, die dich über ein privates Konto erreicht, zum Beispiel eine Nachricht eines Kunden auf WhatsApp oder eine Bestellung in deinem privaten Postfach, gehört von Anfang an zu „Arbeit“. Eine Aufgabe, die du selbst verschoben oder zugeordnet hast, bleibt immer dort, wo du sie abgelegt hast. „Arbeit“ oder „Privat“ bestimmt, wo eine Aufgabe angezeigt wird und mit wem sie geteilt wird, aber nie, wohin sie antwortet: Eine Antwort geht immer dorthin, wo die Unterhaltung stattfindet, auch nach dem Verschieben, sofern du keine andere Möglichkeit auswählst.

Eine solche private Aufgabe antwortet weiterhin von der Arbeitsadresse aus, an die ihre E-Mail geschickt wurde. Sie wird nie in einer Work Fleet oder im Team Graph angezeigt.

Wenn mindestens zwei Aufgaben warten, führt dich **Durchgehen** in der Kopfzeile von „Für dich“ eine nach der anderen durch die Liste. Bei jeder wird der vollständige Entwurf angezeigt, mit **Senden** oder **Ausführen**, **Änderungen anfragen**, **Zurückstellen** und **Überspringen**. Am Computer sendet Enter, `S` stellt zurück, `→` überspringt und Esc bricht ab. In der Kopfzeile steht, wie lange es in deinem Tempo dauert, zum Beispiel „etwa 2 Min.“.

Am Ende wird gezählt, was gesendet oder geschlossen wurde und was noch vorbereitet wird.

Aufgaben mit einer Frage an dich sind davon ausgenommen: Sie brauchen deine Antwort, keinen Tipp.

## Jetzt prüfen

Deine Machine liest jede Quelle alle paar Minuten, Tag und Nacht. Sie prüft neue Nachrichten, sobald 40 eingegangen sind oder die älteste Nachricht einer Person seit 15 Minuten wartet. Newsletter, Benachrichtigungen und Belege werden bei der nächsten Prüfung berücksichtigt, spätestens innerhalb einer Stunde.

Nachts, von 00:00 bis 06:30 Uhr, pausieren die Prüfungen. Neue Nachrichten werden weiterhin gelesen und gespeichert und um 06:30 Uhr gemeinsam geprüft, damit deine Aufgaben vor der morgendlichen Zusammenfassung bereit sind. Unter „Verbindungen“ steht bei „Prüfungen“: „Nachts pausiert, Aufholen um 06:30“. Wenn du nachts in der App klickst, etwas eingibst oder scrollst, im Chat schreibst oder auf eine Aufgabe tippst, laufen die Prüfungen wie gewohnt weiter, bis du eine Stunde lang nicht mehr da warst. Mit **Jetzt prüfen** wird immer sofort geprüft.

Mit **Jetzt prüfen** werden alle Quellen sofort gelesen. Wenn nichts offen ist, tippe auf die Zeile deiner Machine, um sie mit **Details** aufzurufen. Damit öffnest du „Prüfungen“ unter „Verbindungen“. Wenn Aufgaben offen sind, findest du die Zeile oben am Computer. Eine kurze Meldung wird dort nur angezeigt, solange eine Prüfung läuft oder wenn sie fehlgeschlagen ist oder sich verspätet. Du kannst auch im Chat danach fragen.

LinkedIn, X und Salesflare haben ihren eigenen Rhythmus.

## Letzte Prüfung

Nach einer Prüfung, bei der neue Nachrichten gelesen wurden, steht über deinen Aufgaben, was dabei gefunden wurde, aus allen gelesenen Quellen, zum Beispiel „13 Nachrichten um 16:11 geprüft · keine neue Aufgabe“ oder „· 2 neue Aufgaben“. Die Meldung bezieht sich nur auf diese Prüfung. Aufgaben, die schon auf deiner Liste stehen, bleiben unverändert. Wenn eine neue Aufgabe bis zu einem passenden Zeitpunkt zurückgehalten wird, zum Beispiel bis zur morgendlichen Zusammenfassung, steht dort bis wann: „1 Aufgabe bis morgen 08:30 zurückgehalten“.

Tippe auf die Zeile, um jeden E-Mail-Thread, Chat und jede Benachrichtigung mit dem Symbol der jeweiligen Quelle zu sehen: wer geschrieben hat, der Betreff oder die ersten Wörter sowie die neue Aufgabe oder der Grund, warum nichts nötig war, etwa „Nur in cc, ein Teammitglied antwortet“ oder „Termin für Donnerstag steht bereits“. Wenn die Prüfung nur einen vagen Grund ergeben hat, wird für einen Thread kein Grund angezeigt. Tippe auf einen Eintrag, um ihn samt dem Gesprächsverlauf zu lesen.

Die ersten 10 Einträge werden angezeigt. Wenn du darunter tippst, erscheinen die übrigen. Eine Zahl hinter einem Namen, etwa (3), gibt an, wie viele neue Nachrichten dieser Chat enthält. Eine Handybenachrichtigung zu einer bereits aufgelisteten Nachricht wird nur einmal angezeigt. Die Zeile ist nach der Prüfung 12 Stunden lang sichtbar.

Gezählt werden nur E-Mails an dich. Deine eigenen Antworten werden berücksichtigt, um den Kontext und Versprechen zu verstehen, zählen aber nicht als neue E-Mails. E-Mails von The Machine an dich, etwa deine morgendliche Zusammenfassung oder eine Mitteilung über eine Fehlerbehebung, werden nie gelesen oder aufgelistet. E-Mails zu Abrechnungen, deiner Testphase oder einer Einladung werden wie gewohnt gelesen.

## Die Schaltflächen

Bei einer Aufgabe wird der nächste Schritt angezeigt, zum Beispiel **Ausführen** oder **Prüfen und senden**, daneben **Zurückstellen**. Siehe [Ausführen](do-it.md) und [Zurückstellen](snooze.md).

Mit **Änderungen anfragen** gibst du an, was geändert werden soll: wie die Aufgabe erledigt wird oder, sobald ein Entwurf bereit ist, was daran geändert werden soll. Mit **Als erledigt markieren** gibst du an, dass die Aufgabe erledigt ist. Bei einer vorbereiteten Aufgabe ohne Entwurf oder bei einer Aufgabe mit einer Frage an dich ist die Schaltfläche direkt zu sehen, sonst findest du sie oben unter **…**. Die Aufgabe verschwindet sofort aus der Liste, und in der Meldung wird **Rückgängig** angezeigt. Wische die Meldung weg oder ziehe sie mit der Maus aus dem Fenster, um sie früher zu schließen. Die Änderung bleibt bestehen.

Wenn die Aufgabe anders erledigt werden soll, sag es im **Chat**. In der Antwort steht nur, was sich geändert hat, etwa eine Zurückstellung und bis wann. Wenn etwas nicht geändert werden konnte, zum Beispiel ein Fälligkeitsdatum, steht das ebenfalls dort.

Unter **…**:

- **Übergeben…**: Übergib die Aufgabe an ein Teammitglied, [Claude Code oder Codex](hand-to-agent.md) oder [bitte jemanden um eine Prüfung](ask-to-review.md).
- **Wiederholen…**: Die Aufgabe [kommt regelmäßig wieder](recurring.md).
- **Nicht nötig**: Die Aufgabe wird entfernt. Optional kannst du einen Grund auswählen: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Tippe auf den Titel oder unter **Details** auf **Name**, um die Aufgabe umzubenennen. Du kannst auch im Chat danach fragen, zum Beispiel „Benenne sie in … um“. Dein Titel bleibt erhalten.

Mit **Wieder öffnen** holst du eine geschlossene Aufgabe zurück. Sie kommt auch von selbst zurück, wenn etwas Neues passiert, etwa eine neue Nachricht von der anderen Person, aber nicht bei deiner eigenen Antwort. Dann wird angezeigt, wann sie zurückkam, und sie wird wie eine neue Aufgabe sortiert. Im Chat geht es dort weiter, wo es aufgehört hat, auch nach mehreren Wochen.

Eine Rechnung, die du selbst noch bezahlen musst, egal aus welchem Land, wird zu einer Aufgabe mit Betrag, Fälligkeitsdatum und Zahlungsangaben aus der Rechnung. Automatisch bezahlte Rechnungen, etwa per Lastschrift oder hinterlegter Karte, werden nicht aufgenommen. Wenn eine spätere E-Mail zeigt, dass sie bezahlt wurde, zum Beispiel eine Bestätigung des Zahlungseingangs vom Absender, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du sie innerhalb eines Tages wiederherstellen.

Eine Aufgabe, die nur bis zu einem bestimmten Zeitpunkt relevant ist, etwa eine Bestätigung vor einem Meeting, wird nach diesem Zeitpunkt automatisch geschlossen. Sie wird unter **Erledigt / verworfen** als „Nicht mehr nötig“ abgelegt. Mit **Rückgängig** kannst du sie innerhalb eines Tages wiederherstellen.

Bevor eine Nachricht oder Übergabe für jemand anderen als bereit angezeigt wird, prüft deine Machine deine letzten Chats mit den betreffenden Personen, auch Gruppenchats, und wartet, bis Slack sie gelesen hat. Wenn eine spätere Nachricht zeigt, dass die Aufgabe bereits erledigt ist, etwa weil jemand gefragt wurde und zugesagt hat, wird sie automatisch geschlossen. Mit **Rückgängig** kannst du sie innerhalb eines Tages wiederherstellen.

Wenn jemand nach dem Erstellen deines Entwurfs in derselben Unterhaltung geschrieben hat, hält **Senden** den Entwurf zurück: „Nicht gesendet: neue Nachricht im Thread“. Bei der Aufgabe wird diese Nachricht mit **Lesen** und **Für diese Nachricht neu machen** angezeigt. Tippe erneut auf **Senden**, um den Entwurf unverändert zu senden.

Wenn eine neuere Nachricht den Plan ändert, etwa weil eine Feier an einen anderen Ort verlegt oder eine Buchung storniert wurde, aktualisiert The Machine ihre Aufgaben selbst. Eine Aufgabe, die weiterhin relevant ist, folgt dem neuen Plan. Wenn nichts mehr zu tun ist, wird sie unter **Erledigt / verworfen** als „Nicht nötig“ abgelegt. Im Chat steht „Aktualisiert:“ mit einer Begründung. Mit **Rückgängig** kannst du sie innerhalb eines Tages wiederherstellen.

Bei deinen ersten Aufgaben wird ein kurzer Tipp mit den wichtigsten Aktionen angezeigt: **Änderungen anfragen** und **Nicht nötig**. Außerdem wird darauf hingewiesen, dass nichts gesendet wird, bis du auf **Senden** tippst. Ein Tipp wird dauerhaft ausgeblendet, sobald du die zugehörige Schaltfläche verwendest oder auf × tippst.

Am ersten Tag begrüßt dich oben in „Aufgaben“ eine Nachricht. Sie nennt die Person, die am längsten auf deine Antwort wartet. Diese Antwort wird zuerst entworfen und ist bereit, wenn du da bist.

Jede Aufgabe beginnt mit ihrem Titel. In der Zeile darunter steht, um wen es geht, bei Bedarf die Organisation (nicht einfach nur, weil jemand dort arbeitet), das Projekt, „Arbeit“ oder „Privat“ und wann die Aufgabe eingegangen ist. Tippe auf einen Namen, um die Seite der Person im Graph zu öffnen.

Wenn es im Graph ein Foto oder Logo gibt, wird es neben dem Namen oder der Organisation angezeigt, sonst die Initialen. Ein Logo, das in dieser Größe schwer zu lesen wäre, etwa weiße Schrift auf transparentem Hintergrund oder ein breites Wortlogo, wird ebenfalls durch die Initialen ersetzt.

Manchmal steht in einer unauffälligen Zeile, was nicht bekannt ist, zum Beispiel: „Letzter Kontakt vor 12 Tagen per E-Mail, seitdem nichts.“ Sie wird angezeigt, wenn der letzte Austausch schon länger her ist oder eine Antwort aussteht. Außerdem nennt sie nicht verbundene Kanäle wie WhatsApp. Deine Machine sagt, was sie nicht weiß, statt zu raten.

Wenn ein nicht verbundener Kanal genannt wird, öffnet **Verbinden** daneben die Verbindung.

Der Titel sagt, was zu tun ist, und wird nur geändert, wenn sich das ändert. Eine erledigte Aufgabe behält ihren Titel. Darunter steht, wie sie abgeschlossen wurde, zum Beispiel „Erledigt: Sam hat am Dienstag unterschrieben“.

Über dem Entwurf steht in einer dezenten Zeile, aus welcher Nachricht er stammt, samt Logo des jeweiligen Dienstes. Tippe darauf, um den Thread zu lesen. Am Logo beim Entwurf erkennst du, wohin er geht, also zum Beispiel, ob es eine Slack-Antwort oder eine E-Mail ist.

Wenn der Entwurf auf einer Eingabe an anderer Stelle basiert, etwa einem Vorschlag eines Teammitglieds in Slack, steht das in einer Zeile, zum Beispiel „Basierend auf Sam in #ops“. Tippe darauf, um die Nachricht zu lesen.

Ein Chat (Slack, WhatsApp, Telegram, Intercom …) wird als eine Unterhaltung angezeigt, in chronologischer Reihenfolge: zuerst die Nachrichten vor der Nachricht, um die es bei der Aufgabe geht, danach die Antworten. In WhatsApp, Telegram oder Signal stehen deine Nachrichten wie in der App rechts. Die Nachricht zur Aufgabe ist mit „Diese Aufgabe“ markiert und wird direkt angezeigt. Mit **Frühere Nachrichten anzeigen** werden ältere Nachrichten hinzugefügt. Bei einer E-Mail wird der restliche Thread darüber und darunter eingeklappt angezeigt.

Eine Nachricht lässt sich genauso über die Suche, den Graph, die Antworten von Ask oder die letzte Prüfung öffnen. Sie ist mit „Diese Nachricht“ (oder „Neue Nachrichten“) markiert.

Mit **In Gmail öffnen** wird die E-Mail in dem Gmail-Konto geöffnet, an das sie geschickt wurde. Auf Android wird sie in der Gmail App geöffnet, wenn du sie installiert hast.

Unter **Details** einer E-Mail stehen nur zusätzliche Angaben, die nicht in der Kopfzeile enthalten sind, etwa vollständige Cc-Adressen, Bcc oder eine andere Antwortadresse. Gibt es nichts hinzuzufügen, wird nichts angezeigt.

Bei einer Antwort in einem Slack-Thread wird auch angezeigt, was vor Beginn des Threads gesagt wurde. Über den Link einer Aufgabe zur zugehörigen Nachricht kannst du sie ebenfalls hier öffnen. Unten steht **In Slack öffnen**.

Unter **Details** stehen der Name, das Projekt und der Bereich (tippe darauf, um sie zu ändern), deine letzte Notiz und das Ergebnis eines Coding-Agenten. Über den Titel öffnest du den Chat. Eine erledigte Aufgabe bleibt kompakt. Die zugehörige Nachricht findest du unter **Details**.

Bei einer Aufgabe mit „Wartet auf“ ist deine letzte Nachricht an die Person verlinkt, auf deren Antwort du wartest: „E-Mail an Pat · Di“.

## Selbst eine Aufgabe erstellen

Mit **Neue Aufgabe** (unter **Suchen** am Computer, über **+** auf dem Handy oder mit `N`) erstellst du eine Aufgabe zu beliebigen Themen. Beim Erstellen wird nichts gesendet. Wenn du nicht **Arbeit** oder **Privat** auswählst, wird die Aufgabe anhand der Personen und des Themas dem passenden Bereich zugeordnet. Außerdem findet sie die zugehörige E-Mail, auch wenn sie schon älter ist.

- **Fällig**: Gib einen Tag oder eine Uhrzeit ein, zum Beispiel „morgen“, „nächsten Fr“, „3. Nov.“, „14 Uhr“ oder „in 2 Stunden“, auch in deiner eigenen Sprache. Über das Kalendersymbol findest du schnelle Auswahlmöglichkeiten und **Datum wählen**.
- **Wiederholt sich**: Die Aufgabe kommt regelmäßig wieder. Siehe [Wiederkehrende Aufgaben](recurring.md).
- **Person**: Verknüpfe bis zu 5 Personen oder Unternehmen, um die es geht.
- Nachrichtensymbol: Hänge die betreffende Nachricht an: eine E-Mail, Slack-, Teams-, WhatsApp- oder Telegram-Nachricht oder eine andere Nachricht, die The Machine vorliegt. Suche anhand des Textes oder Absenders. Bei jedem Treffer werden Quelle, Absender und Zeitpunkt angezeigt.
- **Dateien**: Tippe auf die Büroklammer, füge einen Screenshot ein oder ziehe Dateien auf das Formular. Auf dem Handy kannst du mit der Kamera daneben ein Foto aufnehmen. Bis zu 5 Dateien, wie im Chat (siehe [Dateien hinzufügen](card-chat.md#add-files)). Mit × entfernst du eine Datei wieder.

Die Dateien bleiben bei der Aufgabe, und The Machine liest sie, wenn sie daran arbeitet. Dateien allein reichen aus: Sie erstellt die Aufgabe aus einer PDF- oder Textdatei. Ein Foto wird als kleines Bild angezeigt. Tippe darauf, um es in voller Größe zu sehen.
