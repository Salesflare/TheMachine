---
title: Aufgaben
area: cards
summary: Eine Aufgabe pro Sache, die dich braucht, bereit für dein Okay. Was die einzelnen Teile einer Aufgabe bedeuten.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 4209ed807e753101
---
Deine Machine liest alles Neue und erstellt nur dann eine Aufgabe, wenn etwas dich braucht. Eine Aufgabe pro Angelegenheit, egal über wie viele Nachrichten sie sich erstreckt.

## Wo Aufgaben zu finden sind

Auf der Seite **Aufgaben** sind sie gruppiert:

- **Gerade erledigt**: Ganz oben siehst du einen letzten Schritt, den du bestätigt hast, etwa ein Formular oder ein Ticket, das während deiner Abwesenheit bearbeitet wurde. Er bleibt höchstens einen Tag lang dort, bis du auf **Verstanden** tippst. Auch dein Handy bekommt Bescheid.
- **Für dich**: Alles, worauf du reagieren musst, zuerst das Dringendste. Bei jeder Aufgabe steht **Vorbereitet** (ein Entwurf oder Ergebnis ist bereit, und mit **Ausführen** oder **Senden** wird es umgesetzt), **Braucht dich** (du musst zuerst entscheiden oder antworten; wenn die Arbeit an etwas hängt, das nur du liefern kannst, etwa eine Information, eine Anmeldung oder eine Entscheidung, steht unter dem Titel, worum es geht), **Wird vorbereitet…** (deine Machine arbeitet daran) oder **Zum Lesen** (eine Zusammenfassung oder ein Briefing, bei dem du nichts entscheiden musst).
- **Älter**: Eingeklappte Aufgaben, zu denen es seit einer Woche nichts Neues gibt (siehe unten).
- **Wartet auf andere**: Eingeklappte Aufgaben, bei denen jemand anderes als Nächstes dran ist (siehe unten).
- **Kommt später zurück**: Zurückgestellte Aufgaben und Aufgaben ohne Antwort auf **Noch nötig?** (siehe unten).
- **Versprechen**: Was du versprochen hast und was andere dir versprochen haben. Siehe [Versprechen](promises.md).
- **Erledigt / verworfen**: Alle abgeschlossenen Aufgaben, die neueste zuerst, mit dem Zeitpunkt des Abschlusses, etwa „Vor 5 Minuten erledigt“. Aufgaben, die anscheinend schon erledigt sind, sind mit **Sieht erledigt aus** gekennzeichnet.

Nachdem du etwas gesendet hast, steht in einer kurzen Meldung, wohin die Aufgabe verschoben wurde, etwa „Gesendet. Nach Erledigt verschoben.“ oder „Gesendet. Bis Mo. auf Später verschoben.“ Wenn eine Antwort nur verspricht, die Arbeit zu erledigen, etwa „Ich schicke es bis Dienstag“, bleibt die Aufgabe offen: „Gesendet. Offen gelassen.“ Über **Öffnen** gelangst du zur Aufgabe. Über die Suche findest du Aufgaben anhand ihres Titels oder der Person, an die sie gingen, auch unter Später und Erledigt.

Unter **Für dich** stehen zuerst überfällige Aufgaben oder Aufgaben, die bis morgen fällig sind, dann Fragen aus deinem Fleet, anschließend Nachfassaktionen eines Boards und danach alles Übrige. Innerhalb jeder Gruppe stehen die neuesten Aufgaben zuerst. Eine Aufgabe behält ihren Platz, während deine Machine sie vorbereitet und wenn sie erledigt ist. Nur ihre Markierung ändert sich. In den anderen offenen Gruppen stehen zuerst überfällige oder bis morgen fällige Aufgaben, danach die neuesten. Die Seitenleiste verwendet dieselbe Reihenfolge.

**Sieht erledigt aus** bedeutet, dass deine Machine davon ausgeht, dass eine Aufgabe erledigt ist, etwa „PR #3451 zusammengeführt“, sie aber noch nicht geschlossen wurde. **Wieder öffnen** setzt sie zurück auf deine Liste, und deine Machine lernt daraus. Diese Aufgaben werden nie als verspätet angezeigt. Wenn eine Nachricht sie anzeigt, schließt sie sich nach einem Tag von selbst, mit **Rückgängig**. Andernfalls wartet sie darauf, dass du **Als erledigt markieren** auswählst. Eine Aufgabe, die du selbst bereits erledigt hast, etwa durch eine Antwort in Gmail oder Slack, wird ebenfalls automatisch geschlossen.

Wenn eine Nachricht von einer Adresse kommt, die nur wie die einer bekannten Person aussieht, etwa sam@acme-corp.example statt sam@acmecorp.example, steht bei der Aufgabe ganz klar: „Das ist nicht Sam Lee.“ Die Person wird mit ihrer eigenen Adresse angezeigt, niemals mit dem Namen, den sie verwendet hat. Deine Machine prüft solche Nachrichten bei der Person unter der Adresse, die du bereits kennst, niemals bei der schreibenden Person.

Bei einer Aufgabe, die noch auf jemand anderen wartet, etwa auf eine Prüfung oder Antwort, steht **Wartet auf:** gefolgt von diesem Schritt. Sie bleibt eingeklappt unter **Wartet auf andere**, oberhalb von Kommt später zurück, bis eine neue Nachricht sie wieder anzeigt. Das gilt auch, wenn du eine Rückfrage gestellt hast: Die Aufgabe kommt am Morgen vor der Frist zurück, bei einer Frist später am selben Tag zum Fristzeitpunkt oder am nächsten Morgen, wenn die Frist bereits verstrichen ist. Außerdem steht dabei, auf wen sie noch wartet.

Wenn es bei einer Aufgabe um ein Ergebnis geht, das jemand anderes liefern muss, etwa einen unterschriebenen Vertrag, wird es unter **Details** als **Fertig, wenn** angezeigt. Wenn du deinen Teil sendest, wird die Aufgabe nicht geschlossen. Sie bleibt unter **Wartet auf andere**, bis eine Nachricht das Ergebnis bestätigt, und schließt sich dann von selbst, mit **Rückgängig**. Wenn bis zum Zeitpunkt, an dem du nachhaken solltest, nichts eintrifft, kommt sie mit **Schreib eine kurze Erinnerung** im Chat zurück. Sag im Chat, was als erledigt gilt, wenn du das ändern möchtest.

Eine Aufgabe, zu der es eine Woche lang nichts Neues gibt, wird von Für dich nach **Älter** verschoben. So stehen Aufgaben, die erst seit ein paar Tagen da sind, nach deiner Abwesenheit weiter oben. Nichts Neues bedeutet: keine neue Nachricht dazu und keine Aktion von dir, etwa eine Chatnachricht, eine Bearbeitung oder ein Zurückstellen. Nur die Aufgabe anzusehen zählt nicht.

Dringende Aufgaben, bald fällige Aufgaben und Aufgaben, bei denen etwas gesendet wird, bleiben unter Für dich. Mit **Alle verwerfen** markierst du nach einmaliger Bestätigung alle nicht benötigten Aufgaben unter Älter als **Nicht nötig**. Das geht auch einzeln, jeweils mit **Rückgängig**. Gibt es etwas Neues zu einer Aufgabe, kommt sie zurück zu Für dich.

Wenn eine Aufgabe eine Woche lang niemanden beschäftigt hat, wird einmal gefragt: **Noch nötig?** Mit **Nicht nötig** schließt du sie, mit **Rückgängig**. Mit **Behalten** bleibt sie bestehen und wird nie wieder nachgefragt. Gibt es eine weitere Woche lang keine Antwort, wird sie unter Kommt später zurück eingeklappt und nicht mehr auf dem App-Symbol oder in der morgendlichen Zusammenfassung gezählt. Wenn du sie öffnest, eine Chatnachricht schreibst, sie bearbeitest, zurückstellst oder eine neue Nachricht eintrifft, kommt sie zurück.

Ein Projekt, zu dem es nichts Neues gibt und für das keine Aufgaben offen sind, kann einmal pro Woche eine Aufgabe mit einem konkreten nächsten Schritt bekommen, höchstens drei pro Woche. Siehe [Projekte](projects.md).

Wenn dich nichts braucht, macht deine Machine ein Nickerchen und lässt die Liste leer. Während sie etwas prüft, wacht sie auf und sagt Bescheid. Wenn eine Prüfung fehlgeschlagen oder verspätet ist, steht das in der Zeile, mit **Jetzt prüfen** darunter.

Mit **Alle**, **Arbeit** und **Privat** oben in der Seitenleiste kannst du alle Aufgaben oder nur eine Art anzeigen. Auf deinem Handy und Computer gilt dieselbe Auswahl. Wenn Arbeit oder Privat ausgewählt ist, führt **Alle anzeigen** zurück zur Gesamtansicht. Eine Meldung zu deiner Machine selbst, etwa dass ein Teil immer wieder neu startet, gehört weder zu Arbeit noch zu Privat und wird nur unter Alle angezeigt.

Mit der Zeile oben in der Liste kannst du auch direkt zur anderen Ansicht wechseln: Unter **Nur privat** tippst du auf **Arbeit** oder **Alle anzeigen**.

Die Zeile oben in der Liste nennt deine letzte morgendliche oder abendliche Zusammenfassung und was darin gezählt wurde, etwa **Zusammenfassung von gestern Abend** · 12 erledigt, 3 offen. Tippe darauf, um die Zusammenfassung noch einmal zu lesen. Mit **Kopieren** kannst du sie irgendwo einfügen. Sobald du sie öffnest oder auf **×** tippst, ist sie auf all deinen Geräten verfügbar, bis die nächste Zusammenfassung erscheint.

Wenn es keine aktuelle Zusammenfassung gibt, wird **Heute bisher** angezeigt: Was heute erledigt wurde und was noch offen ist, für Arbeit und Privat oder nur für die ausgewählte Ansicht.

Bei einer Aufgabe zu einem Projekt steht der Projektname unter dem Titel. Tippe darauf, um das Projekt zu öffnen. Unter **Details** kannst du mit **Projekt** das Projekt ändern oder entfernen. Siehe [Aufgaben eines Projekts](projects.md#a-project-s-to-dos).

Mit **Bereich** unter **Details** verschiebst du eine Aufgabe in deinen anderen Bereich. Welche Nachrichten sie lesen und senden darf, ändert sich entsprechend. Über **Rückgängig** in der Meldung verschiebst du sie zurück.

Wenn eine Aufgabe deinen anderen Bereich braucht, um fortzufahren, und alle Nachrichten, auf denen sie beruht, dort liegen, wird sie automatisch dorthin verschoben und fortgesetzt. Andernfalls wird **Nach Arbeit verschieben** angezeigt, und nichts wird verschoben, bis du darauf tippst. Eine Aufgabe, die du ohne Auswahl von Arbeit oder Privat hinzugefügt hast, wird automatisch dem passenden Bereich zugeordnet, sobald klar ist, wohin sie gehört. Bis dahin gehört sie weder zu Arbeit noch zu Privat und bleibt privat.

Eine Aufgabe kann immer die Nachrichten lesen, aus denen sie entstanden ist. Wenn sie weitere Nachrichten aus deinem anderen Bereich braucht, fragt sie mit **Diese E-Mail für diese Aufgabe verwenden** danach. Ein Arbeits-Postfach, das du als Privat gekennzeichnet hast, zählt als Privat. E-Mails für ein anderes Unternehmen von dir gehören zu den Aufgaben dieses Unternehmens. Eine Aufgabe zu deinem Privatleben, etwa wenn deine Familie an deine Arbeitsadresse schreibt, ist von Anfang an privat.

Arbeit, die dich über ein privates Konto erreicht, etwa von einem Kunden über WhatsApp, eine Bestellung in deinem privaten Postfach oder ein [Versprechen](promises.md) zu einer Arbeitssache, gehört von Anfang an zu Arbeit.

Eine Aufgabe, die du selbst verschoben oder zugeordnet hast, bleibt immer dort, wo du sie abgelegt hast. Arbeit oder Privat entscheidet, wo eine Aufgabe angezeigt und mit wem sie geteilt wird, aber nicht, wohin sie antwortet: Eine Antwort geht immer dorthin, wo das Gespräch stattfindet, auch nach dem Verschieben, außer du wählst einen anderen Weg.

Eine solche private Aufgabe antwortet weiterhin von der Arbeitsadresse, an die die E-Mail gesendet wurde, und wird nie in einem Work Fleet oder dem Team Graph angezeigt.

Wenn mindestens zwei Aufgaben warten, führt **Durchgehen** in der Kopfzeile von Für dich sie nacheinander in der Reihenfolge der Liste durch. Jeder Entwurf wird vollständig angezeigt, mit **Senden** oder **Ausführen**, **Änderungen anfragen**, **Zurückstellen** und **Überspringen**. Auf einem Computer sendet Enter den angezeigten Inhalt, `S` stellt zurück, `→` überspringt und Esc beendet den Vorgang. In der Kopfzeile steht, wie lange es in deinem Tempo ungefähr dauert, etwa „ca. 2 Min.“

Am Ende wird gezählt, was gesendet oder geschlossen wurde und was noch vorbereitet wird.

Aufgaben, bei denen dir eine Frage gestellt wird, sind davon ausgenommen: Sie brauchen deine Antwort und keinen Tipp.

## Jetzt prüfen

Deine Machine liest jede Quelle alle paar Minuten, Tag und Nacht. Sie prüft neue Inhalte, sobald 40 Nachrichten warten oder die älteste Nachricht einer Person seit 15 Minuten wartet. Newsletter, Benachrichtigungen und Belege kommen innerhalb einer Stunde bei der nächsten Prüfung dazu.

Nachts, von 00:00 bis 06:30 Uhr, pausieren die Prüfungen. Neue Nachrichten werden trotzdem gelesen und gespeichert und um 06:30 Uhr gemeinsam geprüft, damit deine Aufgaben vor der morgendlichen Zusammenfassung bereit sind. Unter Verbindungen steht bei Prüfungen: „Nachts pausiert, holt um 06:30 Uhr auf“. Wenn du nachts in der App klickst, tippst oder scrollst, im Chat schreibst oder auf eine Aufgabe tippst, laufen die Prüfungen wie gewohnt weiter, bis du eine Stunde lang abwesend warst. **Jetzt prüfen** startet immer sofort eine Prüfung.

**Jetzt prüfen** liest alle Quellen sofort. Wenn keine Aufgaben offen sind, tippe auf die Zeile deiner Machine, um sie mit **Details** zu sehen. Dadurch werden Prüfungen unter Verbindungen geöffnet. Wenn Aufgaben offen sind, findest du die Zeile oben auf einem Computer. Eine kurze Zeile wird dort nur angezeigt, während eine Prüfung läuft oder wenn sie fehlgeschlagen oder verspätet ist. Du kannst auch im Chat danach fragen.

LinkedIn, X und Salesflare haben ihren eigenen Rhythmus.

## Letzte Prüfung

Nach einer Prüfung, bei der neue Nachrichten gelesen wurden, steht über deinen Aufgaben, was gefunden wurde, aus allen gelesenen Quellen. Zum Beispiel: „13 Nachrichten um 16:11 geprüft · keine neue Aufgabe“ oder „· 2 neue Aufgaben“. Die Meldung bezieht sich nur auf diese Prüfung. Aufgaben, die bereits auf deiner Liste stehen, bleiben unverändert. Wenn eine neue Aufgabe bis zu einem passenden Zeitpunkt zurückgehalten wird, etwa bis zur morgendlichen Zusammenfassung, steht dabei, bis wann: „1 Aufgabe bis morgen 08:30 Uhr zurückgehalten“.

Tippe auf die Zeile, um alle E-Mail-Unterhaltungen, Chats und Benachrichtigungen mit dem Symbol der jeweiligen Quelle zu sehen: wer geschrieben hat, den Betreff oder die ersten Wörter sowie die neue Aufgabe oder den Grund, warum nichts nötig war, etwa „Nur in Cc, eine Teamkollegin antwortet“ oder „Besprechung bereits für Donnerstag angesetzt“. Wenn die Prüfung nur einen ungenauen Grund ergeben hat, wird bei einer Unterhaltung kein Grund angezeigt. Tippe darauf, um die Nachricht und den Gesprächsverlauf zu lesen.

Die ersten 10 werden angezeigt. Tippe darunter, um den Rest zu sehen. Eine Zahl hinter einem Namen, etwa (3), gibt an, wie viele neue Nachrichten dieser Chat enthält. Eine Handybenachrichtigung zu einer Nachricht, die bereits in der Liste steht, wird nur einmal angezeigt. Die Zeile bleibt 12 Stunden nach der Prüfung sichtbar.

Gezählt werden nur E-Mails an dich. Deine eigenen Antworten werden als Kontext und auf Versprechen hin gelesen, zählen aber nicht als neue E-Mails. E-Mails von The Machine an dich, etwa deine morgendliche Zusammenfassung oder eine Mitteilung über eine Fehlerbehebung, werden nie gelesen oder aufgelistet. E-Mails zu Rechnungen, deiner Testphase oder einer Einladung werden wie gewohnt gelesen.

## Die Schaltflächen

Bei einer Aufgabe wird der nächste Schritt angezeigt, etwa **Ausführen** oder **Prüfen und senden**, daneben **Zurückstellen**. Siehe [Ausführen](do-it.md) und [Zurückstellen](snooze.md).

Mit **Änderungen anfragen** gibst du an, was geändert werden soll: wie die Aufgabe ausgeführt wird oder, sobald ein Entwurf bereit ist, was daran geändert werden soll. **Als erledigt markieren** bedeutet, dass die Aufgabe erledigt ist. Bei einer vorbereiteten Aufgabe ohne Entwurf oder einer Aufgabe mit einer Frage steht die Schaltfläche direkt in der Ansicht, sonst oben unter **…**. Die Aufgabe verschwindet sofort aus der Liste. In der Meldung gibt es **Rückgängig**. Wische die Meldung weg oder ziehe sie mit der Maus aus der Ansicht, um sie sofort zu schließen. Die Änderung bleibt bestehen.

Wenn die Aufgabe anders erledigt werden soll, sag es im **Chat**. In der Antwort wird nur genannt, was geändert wurde, etwa eine Zurückstellung und bis wann. Wenn etwas nicht geändert werden konnte, etwa ein Fälligkeitsdatum, steht das ebenfalls dabei.

Unter **…**:

- **Übergeben…**: Übergib die Aufgabe an eine Teamkollegin oder einen Teamkollegen, an [Claude Code oder Codex](hand-to-agent.md) oder [bitte jemanden um eine Prüfung](ask-to-review.md).
- **Wiederholen…**: Die Aufgabe [kommt regelmäßig wieder](recurring.md).
- **Nicht nötig**: Die Aufgabe wird entfernt. Optional kannst du einen Grund auswählen: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Tippe auf den Titel oder unter **Details** auf **Name**, um die Aufgabe umzubenennen. Du kannst auch im Chat darum bitten, etwa mit „Benenne sie in … um“. Dein Titel bleibt erhalten.

Mit **Wieder öffnen** holst du eine geschlossene Aufgabe zurück. Sie kommt auch von selbst zurück, wenn etwas Neues passiert, etwa eine neue Nachricht von der anderen Person, aber nicht bei deiner eigenen Antwort. Dann wird angezeigt, wann sie zurückkam, und sie wird wie eine neue Aufgabe eingeordnet. Der Chat läuft dort weiter, wo er aufgehört hat, auch nach mehreren Wochen.

Eine Rechnung, die du selbst noch bezahlen musst, wird unabhängig vom Land zu einer Aufgabe. Sie enthält den Betrag, das Fälligkeitsdatum und die Zahlungsdetails aus der Rechnung. Automatisch bezahlte Rechnungen, etwa per Lastschrift oder gespeicherter Karte, werden nicht aufgenommen. Wenn eine spätere E-Mail die Zahlung bestätigt, etwa eine Nachricht des Absenders über den Zahlungseingang, schließt sich die Aufgabe von selbst. Mit **Rückgängig** holst du sie innerhalb eines Tages zurück.

Eine Aufgabe, die nur bis zu einem bestimmten Zeitpunkt wichtig war, etwa eine Bestätigung vor einem Meeting, wird danach automatisch geschlossen. Sie wird mit dem Status „Nicht mehr nötig“ nach **Erledigt / verworfen** verschoben. Mit **Rückgängig** holst du sie innerhalb eines Tages zurück.

Bevor eine Nachricht oder Übergabe für jemand anderen als bereit angezeigt wird, prüft deine Machine deine letzten Chats mit den beteiligten Personen, auch Gruppenchats, und wartet darauf, dass Slack sie gelesen hat. Wenn eine spätere Nachricht zeigt, dass die Aufgabe bereits erledigt ist, etwa weil jemand darum gebeten und eine Zusage erhalten hat, schließt sie sich von selbst. Mit **Rückgängig** holst du sie innerhalb eines Tages zurück.

Wenn nach dem Erstellen deines Entwurfs jemand anderes in derselben Unterhaltung geschrieben hat, hält **Senden** den Entwurf zurück: „Nicht gesendet: neue Nachricht im Thread“. Die Aufgabe zeigt diese Nachricht mit **Lesen** und **Für diese Nachricht neu machen** an. Drücke erneut auf **Senden**, um deinen Entwurf unverändert abzuschicken.

Wenn eine neuere Nachricht den Plan ändert, etwa eine Feier an einen anderen Ort verlegt oder eine Buchung storniert wird, aktualisiert The Machine ihre Aufgaben selbst. Eine weiterhin relevante Aufgabe folgt dem neuen Plan. Wenn nichts mehr zu tun ist, wird sie mit dem Status „Nicht nötig“ nach **Erledigt / verworfen** verschoben. Im Chat steht „Aktualisiert:“ mit einer Begründung. Mit **Rückgängig** holst du sie innerhalb eines Tages zurück.

Bei deinen ersten Aufgaben wird in einem kurzen Tipp erklärt, wie **Änderungen anfragen** und **Nicht nötig** funktionieren und dass nichts gesendet wird, bevor du auf **Senden** drückst. Ein Tipp wird dauerhaft ausgeblendet, sobald du seine Schaltfläche verwendest oder auf × drückst.

An deinem ersten Tag begrüßt dich oben in Aufgaben eine Nachricht und nennt die Person, die am längsten auf deine Antwort wartet. Diese Antwort wird zuerst entworfen, damit sie bereit ist, wenn du kommst.

Jede Aufgabe beginnt mit ihrem Titel. Die Zeile darunter nennt, worum es geht, die Organisation, wenn es um eine geht, das Projekt, Arbeit oder Privat und den Zeitpunkt, zu dem die Aufgabe eingegangen ist. Eine Organisation wird nicht nur deshalb genannt, weil jemand dort arbeitet. Tippe auf einen Namen, um die Seite der Person im Graph zu öffnen.

Bei Namen und Organisationen wird ein Foto oder Logo angezeigt, wenn es im Graph vorhanden ist, andernfalls die Initialen. Ein Logo, das in dieser Größe schwer lesbar wäre, etwa weiße Schrift auf transparentem Hintergrund oder ein breites Wortlogo, wird ebenfalls durch die Initiale ersetzt.

Manchmal steht in einer unaufdringlichen Zeile, was nicht bekannt ist, etwa „Letzter Kontakt vor 12 Tagen per E-Mail, seitdem nichts.“ Sie wird angezeigt, wenn der letzte Austausch mit der Person lange zurückliegt oder unbeantwortet ist, und nennt nicht verbundene Kanäle wie WhatsApp. Deine Machine sagt, was sie nicht weiß, statt zu raten.

Wenn ein nicht verbundener Kanal genannt wird, öffnet **Verbinden** daneben die entsprechende Verbindung.

Der Titel sagt, was zu tun ist, und ändert sich nur, wenn sich das ändert. Eine erledigte Aufgabe behält ihren Titel. Darunter steht, wie sie abgeschlossen wurde, etwa „Erledigt: Sam hat es am Dienstag unterschrieben“.

Über dem Entwurf steht in einer blassen Zeile, aus welcher Nachricht er stammt, zusammen mit dem Logo des jeweiligen Dienstes. Tippe darauf, um den Thread zu lesen. Der Entwurf zeigt das Logo des Zielorts. So erkennst du sofort, ob es sich um eine Slack-Antwort oder eine E-Mail handelt.

Wenn der Entwurf auf einer Eingabe an anderer Stelle beruht, etwa einem Vorschlag eines Teammitglieds in Slack, steht es in einer Zeile, zum Beispiel „Basiert auf Sam in #ops“. Tippe darauf, um die Nachricht zu lesen.

Ein Chat (Slack, WhatsApp, Telegram, Intercom …) wird als eine Unterhaltung angezeigt, vom ältesten zum neuesten Beitrag: zuerst die Nachrichten vor der Nachricht, auf die sich die Aufgabe bezieht, dann die Antworten darauf. In WhatsApp, Telegram oder Signal stehen deine Nachrichten wie in der App rechts. Die Nachricht der Aufgabe ist mit „Diese Aufgabe“ markiert und wird in der Ansicht geöffnet. Mit **Frühere Nachrichten anzeigen** werden ältere Nachrichten ergänzt. Bei einer E-Mail wird der übrige Thread darüber und darunter eingeklappt angezeigt.

Eine Nachricht wird in der Suche, im Graph, in den Antworten von Ask oder bei der letzten Prüfung auf dieselbe Weise geöffnet und als „Diese Nachricht“ (oder „Neue Nachrichten“) markiert.

**In Gmail öffnen** öffnet die E-Mail in dem Gmail-Konto, an das sie gesendet wurde. Auf Android wird sie in der Gmail-App geöffnet, sofern diese installiert ist.

Unter **Details** einer E-Mail werden nur Angaben angezeigt, die nicht bereits in der Kopfzeile stehen, etwa vollständige Cc-Adressen, Bcc oder eine andere Antwortadresse. Gibt es nichts hinzuzufügen, wird nichts angezeigt.

Bei einer Antwort in einem Slack-Thread wird auch angezeigt, was vor Beginn des Threads gesagt wurde. Über den Link einer Aufgabe wird auch die zugehörige Nachricht hier geöffnet. Unten findest du **In Slack öffnen**.

Unter **Details** stehen der Name, das Projekt und der Bereich der Aufgabe (tippe darauf, um etwas zu ändern), deine letzte Notiz und das Ergebnis eines Coding-Agenten. Über den Titel öffnest du den Chat. Eine erledigte Aufgabe bleibt kompakt. Die Nachricht, aus der sie entstanden ist, findest du unter **Details**.

Eine Aufgabe mit dem Hinweis „Wartet auf“ verlinkt auf deine letzte Nachricht an die Person und auf die Nachricht, auf die du wartest: „E-Mail an Pat · Di“.

## Selbst eine Aufgabe erstellen

Mit **Neue Aufgabe** (unter **Suchen** auf einem Computer, über **+** auf einem Handy oder mit `N`) kannst du eine Aufgabe für alles erstellen. Beim Erstellen wird nichts gesendet. Wenn du weder **Arbeit** noch **Privat** auswählst, wird sie anhand der beteiligten Personen und des Themas dem passenden Bereich zugeordnet. Außerdem findet sie die E-Mail, auf die sie sich bezieht, auch wenn sie schon älter ist.

- **Fällig**: Gib einen Tag oder eine Uhrzeit ein, etwa „morgen“, „nächsten Fr“, „3. Nov.“, „14 Uhr“ oder „in 2 Stunden“. Das geht auch in deiner eigenen Sprache. Über das Kalendersymbol findest du schnelle Auswahlmöglichkeiten und **Datum wählen**.
- **Wiederholt sich**: Die Aufgabe kommt regelmäßig wieder. Siehe [Wiederkehrende Aufgaben](recurring.md).
- **Person**: Verknüpfe bis zu fünf Personen oder Unternehmen, um die es geht.
- Nachrichtensymbol: Hänge die Nachricht an, um die es geht: eine E-Mail, Slack-, Teams-, WhatsApp- oder Telegram-Nachricht oder eine andere Nachricht, auf die The Machine zugreifen kann. Suche nach Text oder Absender. Bei jedem Treffer siehst du, aus welcher Quelle er stammt, wer ihn gesendet hat und wann.
- **Dateien**: Tippe auf die Büroklammer, füge einen Screenshot ein oder ziehe Dateien auf das Formular. Auf einem Handy kannst du mit der Kamera daneben ein Foto aufnehmen. Bis zu fünf Dateien, wie im Chat (siehe [Dateien hinzufügen](card-chat.md#add-files)). Mit × entfernst du eine Datei.

Die Dateien bleiben bei der Aufgabe, und The Machine liest sie, wenn sie daran arbeitet. Dateien allein reichen aus: Deine Machine erstellt die Aufgabe aus einer PDF- oder Textdatei. Ein Foto wird als kleines Bild angezeigt. Tippe darauf, um es in voller Größe anzusehen.
