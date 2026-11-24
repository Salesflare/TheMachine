---
title: Aufgaben
area: cards
summary: Eine Aufgabe pro Sache, die dich braucht, bereit für dein Ja. Was die einzelnen Teile einer Aufgabe bedeuten.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 32c3a3e62b74548f
---
Deine Machine liest alles Neue und erstellt nur dann eine Aufgabe, wenn etwas dich braucht. Eine Aufgabe pro Angelegenheit, egal über wie viele Nachrichten sie sich erstreckt.

## Wo Aufgaben zu finden sind

Auf der Seite **Aufgaben** sind sie gruppiert:

- **Gerade erledigt**: Ganz oben ist ein letzter Schritt, den du bestätigt hast, zum Beispiel ein Formular oder ein Vorgang, während deiner Abwesenheit durchgelaufen. Er bleibt dort, bis du auf **Verstanden** tippst, höchstens einen Tag lang. Auch dein Handy wird darüber informiert.
- **Für dich**: Alles, was auf dich wartet, zuerst das, was bis morgen fällig ist. Bei jeder Aufgabe steht **Vorbereitet** (ein Entwurf oder Ergebnis ist bereit, und mit **Ausführen** oder **Senden** wird es umgesetzt), **Braucht dich** (zuerst braucht es deine Entscheidung oder Antwort; wenn die Arbeit ohne etwas, das nur du hast, nicht weitergehen oder verwendet werden kann, zum Beispiel einen Preis, eine Information oder eine Entscheidung, steht unter dem Titel, was fehlt), **Wird vorbereitet…** (deine Machine arbeitet daran) oder **Zum Lesen** (eine Zusammenfassung oder ein Briefing, bei dem du nichts entscheiden musst).
- **Älter**: Zugeklappt. Aufgaben, bei denen es seit einer Woche nichts Neues gibt (siehe unten).
- **Wartet auf andere**: Zugeklappt. Aufgaben, bei denen der nächste Schritt bei jemand anderem liegt (siehe unten).
- **Kommt später zurück**: Zurückgestellte Aufgaben und Aufgaben ohne Antwort auf **Noch nötig?** (siehe unten).
- **Versprechen**: Was du versprochen hast und was andere dir versprochen haben. Mehr dazu unter [Versprechen](promises.md).
- **Erledigt / verworfen**: Alle abgeschlossenen Aufgaben, die neuesten zuerst, mit dem Zeitpunkt des Abschlusses, zum Beispiel „Vor 5 Minuten erledigt“. Aufgaben, die offenbar schon erledigt sind, sind mit **Sieht erledigt aus** markiert.

Nach dem Senden erscheint eine kurze Notiz dazu, wohin die Aufgabe verschoben wurde, zum Beispiel „Gesendet. Zu Erledigt verschoben.“ oder „Gesendet. Bis Mo. auf Später verschoben.“ Eine Antwort, die nur verspricht, die Arbeit zu erledigen, zum Beispiel „Ich schicke es bis Dienstag“, lässt die Aufgabe offen: „Gesendet. Offen gelassen.“ Mit **Öffnen** gelangst du zur Aufgabe. Über die Suche findest du Aufgaben nach Titel oder Empfänger, auch unter Später und Erledigt.

Unter **Für dich** stehen zuerst überfällige oder bis morgen fällige Aufgaben, danach Fragen aus deiner Fleet, dann Nachfassnachrichten eines Boards und schließlich alle übrigen. Innerhalb jeder Gruppe stehen die neuesten zuerst. Eine Aufgabe behält ihren Platz, während deine Machine sie vorbereitet und auch, wenn sie erledigt ist. Nur ihre Markierung ändert sich. In den anderen offenen Gruppen stehen überfällige oder bis morgen fällige Aufgaben zuerst, danach die übrigen, neueste zuerst. Die Seitenleiste behält dieselbe Reihenfolge bei.

**Sieht erledigt aus** bedeutet, dass deine Machine erkennt, dass etwas erledigt ist, zum Beispiel „PR #3451 zusammengeführt“, aber noch nicht geschlossen wurde. Mit **Wieder öffnen** kommt die Aufgabe zurück auf deine Liste, und deine Machine lernt daraus. Diese Aufgaben werden nie als verspätet angezeigt. Wenn eine Nachricht das Erledigte zeigt, schließt sich die Aufgabe nach einem Tag automatisch. Du kannst das mit **Rückgängig** rückgängig machen. Andernfalls wartet sie darauf, dass du **Erledigt markieren** auswählst.

Eine Aufgabe schließt sich auch automatisch, wenn du sie bereits selbst erledigt hast, zum Beispiel mit einer Antwort in Gmail oder Slack. Eine Antwort, die behauptet, eine Datei sei angehängt, obwohl keine angehängt ist, schließt sie nicht.

Wenn eine Nachricht von einer Adresse kommt, die nur einer Person ähnelt, die du kennst, zum Beispiel sam@acme-corp.example statt sam@acmecorp.example, steht bei der Aufgabe ganz klar: „Das ist nicht Sam Lee.“ Die Person wird mit ihrer eigenen Adresse angezeigt, nicht mit dem Namen, den sie verwendet hat. Deine Machine überprüft solche Nachrichten bei der Person unter der Adresse, die du bereits kennst, und nie bei der Person, die geschrieben hat.

Bei einer Aufgabe, die noch auf jemand anderen wartet, zum Beispiel auf eine Prüfung oder Antwort, steht **Wartet auf:** und der betreffende Schritt. Sie erscheint zugeklappt unter **Wartet auf andere**, oberhalb von Kommt später zurück, bis eine neue Nachricht sie wieder hervorholt. Das Gleiche gilt, wenn du eine Rückfrage gestellt hast: Die Aufgabe kommt am Morgen vor der Frist zurück, bei einer Frist später am selben Tag zur Frist oder am nächsten Morgen, wenn die Frist bereits verstrichen ist. Außerdem steht dabei, auf wen sie noch wartet.

Wenn es bei einer Aufgabe um ein Ergebnis geht, das jemand anderes liefert, zum Beispiel einen unterschriebenen Vertrag, wird es unter **Details** bei **Fertig, wenn** angezeigt. Wenn du deinen Teil abschickst, wird die Aufgabe nicht geschlossen. Sie bleibt unter **Wartet auf andere**, bis eine Nachricht das Ergebnis zeigt, und schließt sich dann automatisch. Du kannst das mit **Rückgängig** rückgängig machen. Wenn bis zum Zeitpunkt, an dem du nachhaken solltest, nichts eintrifft, kommt die Aufgabe mit **Schreib eine kurze Erinnerung** in ihrem Chat zurück. Schreib im Chat, was als erledigt gilt, um das zu ändern.

Wenn es bei einer Aufgabe eine Woche lang nichts Neues gibt, wandert sie von Für dich zu **Älter**. So stehen nach ein paar Tagen Abwesenheit die neuen Aufgaben zuerst. Nichts Neues bedeutet, dass es keine neue Nachricht dazu gab und du nichts daran gemacht hast, zum Beispiel eine Chatnachricht geschrieben, etwas bearbeitet oder die Aufgabe zurückgestellt hast. Nur sie anzusehen zählt nicht.

Dringende Aufgaben, bald fällige Aufgaben und Aufgaben, bei denen etwas auf dem Weg ist, bleiben unter Für dich. Mit **Alle verwerfen** markierst du nach einer Bestätigung alle Aufgaben unter Älter als nicht nötig. Das geht auch einzeln mit **Nicht nötig**. Mit **Rückgängig** kannst du das rückgängig machen. Sobald es zu einer Aufgabe etwas Neues gibt, kommt sie zurück zu Für dich.

Wenn eine Aufgabe eine Woche lang niemand angefasst hat, fragt sie einmal: **Noch nötig?** Mit **Nicht nötig** wird sie geschlossen. Du kannst das mit **Rückgängig** rückgängig machen. Mit **Behalten** bleibt sie bestehen, und die Frage wird nie wieder gestellt. Wenn du eine weitere Woche lang nicht antwortest, wird sie unter Kommt später zurück eingeklappt, und sie wird nicht mehr auf dem App-Symbol oder in der morgendlichen Zusammenfassung mitgezählt. Wenn du sie öffnest, eine Chatnachricht schreibst, sie bearbeitest oder zurückstellst oder eine neue Nachricht eintrifft, kommt sie zurück.

Einmal pro Woche kann es für ein Projekt, bei dem es ruhig geworden ist und keine offenen Aufgaben mehr gibt, eine Aufgabe mit einem konkreten nächsten Schritt geben, höchstens drei pro Woche. Mehr dazu unter [Projekte](projects.md).

Wenn dich nichts braucht, macht deine Machine ein Nickerchen und zeigt eine leere Liste. Während sie prüft, wacht sie auf und sagt Bescheid. Wenn eine Prüfung fehlgeschlagen ist oder sich verzögert, steht das in der Zeile. Darunter findest du **Jetzt prüfen**.

Mit **Alle**, **Arbeit** und **Privat** oben in der Seitenleiste zeigst du alle Aufgaben oder nur eine Art davon an. Auf deinem Handy und Computer gilt dieselbe Auswahl. Wenn Arbeit oder Privat ausgewählt ist, bringt dich **Alle anzeigen** zurück zur Gesamtansicht. Eine Meldung zu deiner Machine selbst, zum Beispiel dass ein Teil ständig neu startet, gehört weder zu Arbeit noch zu Privat und erscheint nur unter Alle.

Über die Zeile oben in der Liste kannst du auch direkt zur jeweils anderen Ansicht wechseln: Unter **Nur privat** tippst du auf **Arbeit** oder **Alle anzeigen**.

In der Zeile oben in der Liste stehen der Name deiner letzten morgendlichen oder abendlichen Zusammenfassung und die darin gezählten Aufgaben, zum Beispiel **Zusammenfassung von gestern Abend** · 12 erledigt, 3 offen. Tippe darauf, um die Zusammenfassung noch einmal zu lesen. Mit **Kopieren** kannst du sie überall einfügen. Sobald du sie öffnest oder auf ihr **×** tippst, bleibt sie auf all deinen Geräten sichtbar, bis die nächste Zusammenfassung erscheint.

Ohne aktuelle Zusammenfassung wird **Heute bisher** angezeigt: was heute erledigt wurde und was noch offen ist, für Arbeit und Privat oder nur für die Ansicht, nach der du gefiltert hast.

Bei einer Aufgabe in einem Projekt wird der Projektname unter dem Titel angezeigt. Tippe darauf, um das Projekt zu öffnen. Unter **Details** kannst du mit **Projekt** das Projekt ändern oder entfernen. Mehr dazu unter [Aufgaben eines Projekts](projects.md#a-project-s-to-dos).

Mit **Bereich** unter **Details** verschiebst du eine Aufgabe in deinen anderen Bereich. Welche Nachrichten sie lesen und von wo sie senden darf, ändert sich mit. Mit **Rückgängig** in der Notiz kannst du sie zurückverschieben.

Wenn eine Aufgabe deinen anderen Bereich braucht, um weiterzugehen, und alle Nachrichten, auf denen sie basiert, dort liegen, wird sie automatisch dorthin verschoben und fortgesetzt. Andernfalls wird **Nach Arbeit verschieben** angezeigt. Erst wenn du darauf tippst, wird etwas verschoben. Eine Aufgabe, die du ohne Auswahl von Arbeit oder Privat hinzugefügt hast, wird automatisch dem passenden Bereich zugeordnet, sobald klar ist, wohin sie gehört. Bis dahin gehört sie weder zu Arbeit noch zu Privat und bleibt privat.

Eine Aufgabe kann immer die Nachrichten lesen, auf denen sie basiert. Wenn sie weitere Nachrichten aus deinem anderen Bereich braucht, fragt sie mit **Diese E-Mail für diese Aufgabe verwenden** danach. Ein Arbeits-Postfach, das du als Privat gekennzeichnet hast, gilt als privat. E-Mails für ein anderes deiner Unternehmen gehören zu den Aufgaben dieses Unternehmens. Bei einer Aufgabe zu deinem Privatleben, zum Beispiel wenn deine Familie an deine Arbeitsadresse schreibt, ist der Bereich von Anfang an Privat.

Arbeit, die dich über ein privates Konto erreicht, zum Beispiel eine Kundin oder ein Kunde auf WhatsApp, eine Bestellung in deinem privaten Postfach oder ein [Versprechen](promises.md) zu deiner Arbeit, gehört von Anfang an zu Arbeit.

Eine Aufgabe, die du selbst verschoben oder zugeordnet hast, bleibt immer dort, wo du sie abgelegt hast. Arbeit oder Privat bestimmt, wo eine Aufgabe erscheint und mit wem sie geteilt wird, aber nie, wohin sie antwortet. Eine Antwort geht immer dorthin, wo das Gespräch stattfindet, auch nach einer Verschiebung, sofern du keinen anderen Weg auswählst.

Eine solche private Aufgabe antwortet weiterhin von der Arbeitsadresse, an die ihre E-Mail gesendet wurde. Sie erscheint nie in einer Work Fleet oder im Team Graph.

Wenn mindestens zwei Aufgaben auf dich warten, führt dich **Durchgehen** in der Kopfzeile von Für dich nacheinander durch die Aufgaben in Listenreihenfolge, jeweils mit dem vollständigen Entwurf und den Optionen **Senden** oder **Ausführen**, **Änderungen anfragen**, **Zurückstellen** und **Überspringen**. Am Computer sendet die Eingabetaste, `S` stellt zurück, `→` überspringt und Esc beendet den Vorgang. In der Kopfzeile steht, wie lange es bei deinem Tempo dauert, zum Beispiel „etwa 2 Min.“

Am Ende wird gezählt, was gesendet oder geschlossen wurde und was noch vorbereitet wird.

Aufgaben, bei denen du eine Frage beantworten sollst, werden dabei ausgelassen. Sie brauchen deine Antwort, nicht einen Tipp.

## Jetzt prüfen

Deine Machine liest jede Quelle alle paar Minuten, Tag und Nacht. Sie prüft neue Nachrichten, sobald 40 Nachrichten warten oder die älteste Nachricht einer Person seit 15 Minuten wartet. Newsletter, Benachrichtigungen und Belege werden bei der nächsten Prüfung berücksichtigt, spätestens innerhalb einer Stunde.

Nachts, von 00:00 bis 06:30, pausieren die Prüfungen. Neue Nachrichten werden weiterhin gelesen und gespeichert. Um 06:30 werden sie gemeinsam geprüft, damit deine Aufgaben vor der morgendlichen Zusammenfassung bereit sind. Unter Verbindungen steht bei Prüfungen „Nachts pausiert, Nachholen um 06:30“. Wenn du nachts in der App klickst, schreibst oder scrollst, im Chat schreibst oder auf eine Aufgabe tippst, laufen die Prüfungen wie üblich weiter, bis du eine Stunde lang nicht aktiv warst. Mit **Jetzt prüfen** wird immer sofort geprüft.

Mit **Jetzt prüfen** werden alle Quellen sofort gelesen. Wenn keine Aufgabe offen ist, tippe auf die Zeile deiner Machine, um sie mit **Details** zu sehen. Damit werden die Prüfungen unter Verbindungen geöffnet. Wenn Aufgaben offen sind, findest du die Option am Computer ganz oben. Eine kurze Zeile wird dort nur angezeigt, während eine Prüfung läuft oder wenn sie fehlgeschlagen ist oder sich verzögert. Du kannst auch im Chat danach fragen.

LinkedIn, X und Salesflare halten ihren eigenen Rhythmus ein.

## Letzte Prüfung

Nach einer Prüfung, bei der neue Nachrichten gelesen wurden, steht über deinen Aufgaben, was gefunden wurde und aus welchen Quellen, zum Beispiel „13 Nachrichten um 16:11 geprüft · keine neue Aufgabe“ oder „· 2 neue Aufgaben“. Die Zeile bezieht sich nur auf diese Prüfung. Aufgaben, die bereits auf deiner Liste stehen, bleiben unverändert. Wenn eine neue Aufgabe bis zu einem günstigeren Zeitpunkt zurückgehalten wird, etwa bis zur morgendlichen Zusammenfassung, steht dort bis wann: „1 Aufgabe bis morgen 08:30 zurückgehalten“.

Tippe auf die Zeile, um jeden E-Mail-Thread, Chat und jede Benachrichtigung mit dem Symbol der jeweiligen Quelle zu sehen. Angezeigt werden, wer geschrieben hat, der Betreff oder die ersten Wörter und die neue Aufgabe oder der Grund, warum nichts nötig war, zum Beispiel „Nur in CC, ein Teammitglied antwortet“ oder „Termin für Donnerstag steht bereits“. Ein Thread zeigt keinen Grund an, wenn die Prüfung nur einen ungenauen Grund ergeben hat. Tippe darauf, um die Nachricht und den Gesprächsverlauf zu lesen.

Die ersten 10 werden angezeigt. Wenn du darunter tippst, erscheinen die übrigen. Eine Zahl hinter einem Namen, zum Beispiel (3), zeigt, wie viele neue Nachrichten dieser Chat enthält. Eine Handy-Benachrichtigung zu einer Nachricht, die bereits aufgelistet ist, wird nur einmal angezeigt. Die Zeile bleibt nach der Prüfung 12 Stunden lang sichtbar.

Gezählt werden nur E-Mails an dich. Deine eigenen Antworten werden als Kontext und auf Versprechen hin gelesen, zählen aber nicht als neue E-Mails. E-Mails von The Machine an dich, zum Beispiel deine morgendliche Zusammenfassung oder eine Meldung zur Fehlerbehebung, werden nie gelesen oder aufgelistet. E-Mails zu Abrechnung, Testphase oder Einladungen werden wie üblich gelesen.

## Die Schaltflächen

Bei einer Aufgabe wird der nächste Schritt angezeigt, zum Beispiel **Ausführen** oder **Prüfen und senden**, daneben steht **Zurückstellen**. Mehr dazu unter [Ausführen](do-it.md) und [Zurückstellen](snooze.md).

Mit **Änderungen anfragen** kannst du sagen, was geändert werden soll: wie etwas erledigt werden soll oder, sobald ein Entwurf bereit ist, was daran geändert werden soll. **Erledigt markieren** bedeutet, dass die Aufgabe erledigt ist. Die Option ist bei einer bereiten Aufgabe ohne Entwurf oder bei einer Aufgabe mit einer Frage direkt sichtbar, andernfalls findest du sie oben unter **…**. Die Aufgabe wird sofort aus der Liste entfernt. In der Meldung kannst du sie mit **Rückgängig** zurückholen. Wische die Meldung weg oder ziehe sie mit der Maus aus der Ansicht, um sie schneller zu schließen. Die Änderung bleibt bestehen.

Wenn du die Aufgabe auf andere Weise erledigen lassen möchtest, sag es in ihrem **Chat**. In der Antwort steht nur, was geändert wurde, zum Beispiel die Zurückstellung und bis wann. Wenn sich etwas nicht ändern ließ, zum Beispiel ein Fälligkeitsdatum, steht das ebenfalls dort.

Unter **…**:

- **Übergeben…**: Übergib die Aufgabe an ein Teammitglied, [Claude Code oder Codex](hand-to-agent.md), oder [bitte jemanden um eine Prüfung](ask-to-review.md).
- **Wiederholen…**: Die Aufgabe [kommt regelmäßig zurück](recurring.md).
- **Nicht nötig**: Die Aufgabe wird entfernt. Optional kannst du einen Grund auswählen: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Tippe auf den Titel oder unter **Details** auf **Name**, um die Aufgabe umzubenennen. Du kannst auch in ihrem Chat darum bitten, zum Beispiel mit „Benenne sie in … um“. Dein Titel bleibt bestehen.

Mit **Wieder öffnen** holst du eine geschlossene Aufgabe zurück. Sie kommt auch von selbst zurück, wenn etwas Neues passiert, zum Beispiel eine neue Nachricht von der anderen Person, aber nicht bei deiner eigenen Antwort. Dann wird angezeigt, wann sie zurückgekommen ist, und sie wird wie eine neue Aufgabe sortiert. Der Chat wird dort fortgesetzt, wo er aufgehört hat, auch nach Wochen.

Eine Rechnung, die du selbst noch bezahlen musst, wird unabhängig vom Land zu einer Aufgabe mit dem Betrag, Fälligkeitsdatum und den Zahlungsangaben auf der Rechnung. Automatisch bezahlte Rechnungen, zum Beispiel per Lastschrift oder mit einer hinterlegten Karte, werden nicht aufgenommen. Wenn eine spätere E-Mail zeigt, dass die Rechnung bezahlt wurde, etwa weil der Absender den Zahlungseingang bestätigt, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du sie innerhalb eines Tages zurückholen.

Eine Aufgabe, die nur bis zu einem bestimmten Zeitpunkt wichtig war, zum Beispiel eine Bestätigung vor einem Termin, wird nach diesem Zeitpunkt automatisch geschlossen. Sie wandert mit dem Hinweis „Nicht mehr nötig“ zu **Erledigt / verworfen**. Mit **Rückgängig** kannst du sie innerhalb eines Tages zurückholen.

Bevor eine Nachricht oder Übergabe für jemanden als bereit angezeigt wird, prüft deine Machine deine letzten Chats mit den beteiligten Personen, auch Gruppenchats, und wartet darauf, dass Slack sie gelesen hat. Wenn eine spätere Nachricht zeigt, dass etwas schon erledigt ist, zum Beispiel weil die Person gefragt wurde und zugesagt hat, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du sie innerhalb eines Tages zurückholen.

Wenn jemand anderes in derselben Unterhaltung geschrieben hat, nachdem der Entwurf erstellt wurde, hält **Senden** den Entwurf zurück: „Nicht gesendet: neue Nachricht im Thread“. Bei der Aufgabe wird diese Nachricht mit **Lesen** und **Für diese Nachricht neu machen** angezeigt. Tippe erneut auf **Senden**, um den Entwurf unverändert abzuschicken.

Wenn eine neuere Nachricht den Plan ändert, zum Beispiel wenn eine Feier an einen anderen Ort verlegt oder eine Buchung storniert wurde, aktualisiert The Machine ihre Aufgaben selbst. Eine weiterhin relevante Aufgabe folgt dem neuen Plan. Wenn nichts mehr zu tun ist, wandert die Aufgabe mit dem Hinweis „Nicht nötig“ zu **Erledigt / verworfen**. Im Chat steht „Aktualisiert:“ mit der Begründung. Mit **Rückgängig** kannst du sie innerhalb eines Tages zurückholen.

Bei deinen ersten Aufgaben wird ein kurzer Tipp mit den wichtigsten Aktionen angezeigt: **Änderungen anfragen** und **Nicht nötig**. Außerdem wird erklärt, dass nichts gesendet wird, bevor du auf **Senden** tippst. Ein Tipp wird dauerhaft ausgeblendet, sobald du seine Schaltfläche verwendest oder auf × tippst.

An deinem ersten Tag begrüßt dich oben in Aufgaben eine Nachricht. Sie nennt die Person, die am längsten auf deine Antwort wartet. Diese Antwort wird zuerst entworfen, damit sie bereit ist, wenn du ankommst.

Jede Aufgabe beginnt mit ihrem Titel. In der Zeile darunter steht, um wen es geht, bei einem Unternehmen auch die Organisation, sofern die Aufgabe tatsächlich damit zu tun hat, das Projekt, Arbeit oder Privat und wann sie eingegangen ist. Tippe auf einen Namen, um die Seite der Person im Graph zu öffnen.

Bei einem Namen oder Unternehmen wird das Foto oder Logo angezeigt, falls es im Graph vorhanden ist, andernfalls die Initialen. Wenn ein Logo in dieser Größe nicht lesbar wäre, zum Beispiel weiße Schrift auf durchsichtigem Hintergrund oder ein breites Wortlogo, wird stattdessen ebenfalls die Initiale angezeigt.

Manchmal steht in einer dezenten Zeile, was unbekannt ist, zum Beispiel „Letzter Kontakt vor 12 Tagen per E-Mail, seitdem nichts.“ Sie erscheint, wenn der letzte Kontakt mit der Person lange her oder unbeantwortet ist. Außerdem werden nicht verbundene Kanäle genannt, zum Beispiel WhatsApp. Deine Machine sagt, was sie nicht weiß, statt zu raten.

Wenn ein nicht verbundener Kanal genannt wird, öffnet **Verbinden** daneben die betreffende Verbindung.

Der Titel sagt, was zu tun ist, und ändert sich nur, wenn sich das ändert. Eine erledigte Aufgabe behält ihren Titel. Darunter steht, wie sie abgeschlossen wurde, zum Beispiel „Erledigt: Sam hat es am Dienstag unterschrieben“.

Über dem Entwurf steht in einer blasseren Zeile, aus welcher Nachricht er stammt, zusammen mit dem Logo des Dienstes. Tippe darauf, um den Thread zu lesen. Im Entwurf wird das Logo des Ziels angezeigt. So siehst du sofort, ob es sich um eine Slack-Antwort oder eine E-Mail handelt.

Wenn der Entwurf auf einer Eingabe an anderer Stelle beruht, zum Beispiel einem Vorschlag eines Teammitglieds in Slack, steht das in einer Zeile, etwa „Basierend auf Sam in #ops“. Tippe darauf, um die Nachricht zu lesen. Die Zeile verschwindet, sobald eine Aktualisierung den Entwurf ersetzt.

Ein Chat (Slack, WhatsApp, Telegram, Intercom …) wird als eine Unterhaltung angezeigt, mit den ältesten Nachrichten zuerst: die Nachrichten vor der Nachricht, um die es bei der Aufgabe geht, und die Antworten danach. In WhatsApp, Telegram oder Signal stehen deine Nachrichten rechts, wie in der App. Die Nachricht, auf die sich die Aufgabe bezieht, ist mit „Diese Aufgabe“ markiert und wird beim Öffnen angezeigt. Mit **Frühere Nachrichten anzeigen** werden ältere Nachrichten eingeblendet. Bei einer E-Mail ist der übrige Thread oberhalb und unterhalb der Nachricht eingeklappt.

Eine Nachricht wird in der Suche, im Graph, in den Antworten von Ask oder bei der letzten Prüfung auf dieselbe Weise geöffnet. Sie ist mit „Diese Nachricht“ oder „Neue Nachrichten“ markiert.

Mit **In Gmail öffnen** öffnest du die E-Mail im Gmail-Konto, an das sie gesendet wurde. Auf Android wird sie in der Gmail App geöffnet, falls du die App hast.

Unter **Details** einer E-Mail stehen nur Angaben, die nicht bereits in der Kopfzeile zu sehen sind, zum Beispiel vollständige Cc-Adressen, Bcc oder eine andere Antwortadresse. Wenn es nichts hinzuzufügen gibt, wird dort nichts angezeigt.

Bei einer Antwort in einem Slack-Thread wird auch angezeigt, was vor Beginn des Threads gesagt wurde. Der Link einer Aufgabe zu ihrer eigenen Nachricht öffnet sie ebenfalls hier. Unten findest du **In Slack öffnen**.

Unter **Details** stehen Name, Projekt und Bereich der Aufgabe (tippe auf einen Eintrag, um ihn zu ändern), deine letzte Notiz und das Ergebnis eines Coding-Agenten. Wenn du auf den Titel tippst, öffnet sich der Chat. Eine erledigte Aufgabe bleibt kompakt. Die Nachricht, auf der sie basiert, findest du unter **Details**.

Bei einer Aufgabe mit „Wartet auf“ führt ein Link zu deiner letzten Nachricht an die Person, auf die du wartest, zum Beispiel „E-Mail an Pat · Di“.

## Eigene Aufgaben erstellen

Mit **Neue Aufgabe** (am Computer unter **Suchen**, auf dem Handy unter **+** oder mit `N`) erstellst du eine Aufgabe für beliebige Dinge. Beim Erstellen wird nichts gesendet. Wenn du nicht **Arbeit** oder **Privat** auswählst, wird die Aufgabe anhand der beteiligten Personen und ihres Themas dem passenden Bereich zugeordnet. Außerdem findet sie die E-Mail, zu der sie gehört, auch wenn diese schon älter ist.

- **Fällig**: Gib einen Tag oder eine Uhrzeit ein, zum Beispiel „morgen“, „nächsten Fr.“, „3. Nov.“, „14 Uhr“ oder „in 2 Stunden“. Du kannst die Angaben auch in deiner eigenen Sprache eingeben. Über das Kalendersymbol findest du Vorschläge und **Datum wählen**.
- **Wiederholt sich**: Die Aufgabe kommt regelmäßig zurück. Mehr dazu unter [Wiederkehrende Aufgaben](recurring.md).
- **Person**: Verknüpfe bis zu 5 Personen oder Unternehmen, um die es geht.
- Nachrichtensymbol: Hänge die Nachricht an, um die es geht: eine E-Mail, eine Nachricht in Slack, Teams, WhatsApp, Telegram oder einen anderen Dienst, auf den The Machine zugreifen kann. Suche nach Text oder Absender. Bei jedem Ergebnis wird angezeigt, woher es stammt, wer es gesendet hat und wann.
- **Dateien**: Tippe auf die Büroklammer, füge einen Screenshot ein oder ziehe Dateien auf das Formular. Auf dem Handy kannst du mit der danebenliegenden Kamera ein Foto aufnehmen. Es sind bis zu 5 Dateien möglich, wie im Chat (siehe [Dateien hinzufügen](card-chat.md#add-files)). Mit × entfernst du eine Datei.

Die Dateien bleiben bei der Aufgabe, und The Machine liest sie, wenn sie daran arbeitet. Dateien allein genügen: Sie füllt die Aufgabe anhand einer PDF- oder Textdatei aus. Ein Foto wird als kleines Bild angezeigt. Tippe darauf, um es in voller Größe zu sehen.
