---
title: Aufgaben
area: cards
summary: Eine Aufgabe für jedes Anliegen, bei dem du gefragt bist, bereit für dein Okay. Was die einzelnen Teile einer Aufgabe bedeuten.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: fcb9a016c9af8551
---
Deine Machine liest alles Neue und erstellt nur dann eine Aufgabe, wenn du gebraucht wirst. Eine Aufgabe pro Anliegen, unabhängig davon, über wie viele Nachrichten es sich erstreckt.

## Wo Aufgaben stehen

Auf der Seite **Aufgaben** sind sie gruppiert:

- **Gerade erledigt**: Ganz oben wird angezeigt, wenn ein letzter Schritt, den du bestätigt hast, zum Beispiel ein Formular oder ein Vorgang, während deiner Abwesenheit erledigt wurde. Er bleibt höchstens einen Tag lang dort, bis du auf **Verstanden** tippst. Auch dein Handy bekommt Bescheid.
- **Für dich**: Alles, worauf du reagieren musst. Was bis morgen fällig ist, steht zuerst. Bei jeder Aufgabe steht **Vorbereitet** (ein Entwurf oder Ergebnis ist bereit, und mit **Ausführen** oder **Senden** wird es umgesetzt), **Braucht dich** (zuerst ist deine Entscheidung oder Antwort nötig; wenn die Arbeit ohne etwas, das nur du liefern kannst, nicht weitergehen oder genutzt werden kann, etwa einen Preis, eine Angabe oder eine Entscheidung, steht unter dem Titel, worum es geht), **Wird vorbereitet…** (deine Machine arbeitet daran) oder **Zum Lesen** (eine Zusammenfassung oder ein Briefing, bei dem nichts entschieden werden muss).
- **Älter**: Eingeklappt. Aufgaben, bei denen es seit einer Woche nichts Neues gab (siehe unten).
- **Wartet auf andere**: Eingeklappt. Aufgaben, bei denen der nächste Schritt bei jemand anderem liegt (siehe unten).
- **Kommt später zurück**: Zurückgestellte Aufgaben, Nachrichten, die [später gesendet werden](send-later.md), und Aufgaben, auf die es keine Antwort auf **Noch nötig?** gab (siehe unten).
- **Versprechen**: Was du versprochen hast und was andere dir versprochen haben. Siehe [Versprechen](promises.md).
- **Erledigt / verworfen**: Alle abgeschlossenen Aufgaben, die neuesten zuerst, mit dem Zeitpunkt des Abschlusses, zum Beispiel „Vor 5 Minuten erledigt“. Aufgaben, die bereits erledigt zu sein scheinen, sind mit **Sieht erledigt aus** markiert.

Nach dem Senden steht kurz dabei, wohin die Aufgabe verschoben wurde, zum Beispiel „Gesendet. Nach Erledigt verschoben.“ oder „Gesendet. Bis Mo. nach Später verschoben.“ Wenn eine Antwort nur verspricht, die Arbeit zu erledigen, etwa „Ich schicke es bis Dienstag“, bleibt die Aufgabe offen: „Gesendet. Offen gelassen.“ Mit **Öffnen** gelangst du zur Aufgabe. Über die Suche findest du Aufgaben anhand ihres Titels oder der Person, an die sie gesendet wurden, auch unter Später und Erledigt.

Unter **Für dich** stehen überfällige oder bis morgen fällige Aufgaben zuerst, dann Fragen aus deiner Fleet, dann Nachfassnachrichten eines Boards und anschließend der Rest. Innerhalb jeder Gruppe stehen die neuesten zuerst. Eine Aufgabe behält ihren Platz, während deine Machine sie vorbereitet und wenn sie erledigt ist. Nur ihre Markierung ändert sich. In den anderen offenen Gruppen stehen überfällige oder bis morgen fällige Aufgaben zuerst, danach die übrigen, neueste zuerst. In der Seitenleiste bleibt die Reihenfolge gleich.

**Sieht erledigt aus** bedeutet, dass deine Machine erkennt, dass etwas erledigt ist, zum Beispiel „PR #3451 zusammengeführt“, die Aufgabe aber noch nicht geschlossen wurde. **Wieder öffnen** setzt sie wieder auf deine Liste, und deine Machine lernt daraus. Diese Aufgaben werden nie als verspätet angezeigt. Wenn eine Nachricht den Abschluss zeigt, wird die Aufgabe nach einem Tag automatisch geschlossen und **Rückgängig** angeboten. Andernfalls wartet sie darauf, dass du **Als erledigt markieren** auswählst.

Eine Aufgabe, die du bereits selbst erledigt hast, zum Beispiel durch eine Antwort in Gmail oder Slack, wird ebenfalls automatisch geschlossen. Eine Antwort, in der steht, dass eine Datei angehängt ist, obwohl keine angehängt wurde, schließt sie nicht.

Wenn eine Nachricht von einer Adresse kommt, die nur wie die Adresse einer Person aussieht, die du kennst, zum Beispiel sam@acme-corp.example statt sam@acmecorp.example, steht bei der Aufgabe klar: „Das ist nicht Sam Lee.“ Die Person wird mit ihrer tatsächlichen Adresse angezeigt, nie mit dem Namen, den sie angegeben hat. Deine Machine überprüft so eine Nachricht bei der Person unter der Adresse, die du bereits hast, niemals bei der Person, die sie geschrieben hat.

Bei einer Aufgabe, die noch auf jemand anderen wartet, zum Beispiel auf eine Prüfung oder Antwort, steht **Wartet auf:** und der nächste Schritt. Sie bleibt eingeklappt unter **Wartet auf andere**, oberhalb von Kommt später zurück, bis eine neue Nachricht sie wieder hervorholt. Dasselbe gilt, nachdem du eine Rückfrage gestellt hast: Die Aufgabe kommt am Morgen vor der Frist zurück, bei einer Frist später am selben Tag zum Zeitpunkt der Frist oder nach Ablauf der Frist am nächsten Morgen. Dabei steht, auf wen sie noch wartet.

Wenn es bei einer Aufgabe um ein Ergebnis geht, das jemand anderes liefern muss, etwa einen unterschriebenen Vertrag, steht es unter **Details** bei **Fertig, wenn**. Wenn du deinen Teil sendest, wird die Aufgabe nicht geschlossen. Sie bleibt unter **Wartet auf andere**, bis eine Nachricht das Ergebnis zeigt. Dann wird sie automatisch geschlossen und **Rückgängig** angeboten. Wenn bis zum Zeitpunkt, an dem du nachhaken solltest, nichts kommt, erscheint sie mit **Schreib eine kurze Erinnerung** in ihrem Chat. Schreib im Chat, was als erledigt gelten soll, um das zu ändern.

Wenn es eine Woche lang nichts Neues bei einer Aufgabe gab, wird sie von Für dich nach **Älter** verschoben. So stehen neue Aufgaben nach ein paar Tagen Abwesenheit oben. „Nichts Neues“ bedeutet, dass es weder eine neue Nachricht zur Aufgabe noch eine Aktion von dir gab, zum Beispiel eine Chatnachricht, eine Bearbeitung oder ein Zurückstellen. Es zählt nicht, wenn du sie nur ansiehst.

Dringende Aufgaben, bald fällige Aufgaben und Aufgaben mit einer ausstehenden Sendung bleiben unter Für dich. Mit **Alle verwerfen** werden alle Aufgaben unter Älter nach einer Bestätigung als nicht nötig markiert. Das entspricht **Nicht nötig**, wenn du die Aufgaben einzeln verwirfst. Dabei wird **Rückgängig** angeboten. Gibt es etwas Neues zu einer Aufgabe, kommt sie zurück zu Für dich.

Wenn eine Woche lang niemand eine Aufgabe angefasst hat, wird einmal gefragt: **Noch nötig?** Mit **Nicht nötig** wird sie geschlossen und **Rückgängig** angeboten. **Behalten** lässt sie bestehen, und die Frage wird nie wieder gestellt. Kommt eine weitere Woche lang keine Antwort, wird die Aufgabe unter Kommt später zurück eingeklappt. Sie wird dann nicht mehr auf dem App-Symbol oder in der morgendlichen Zusammenfassung mitgezählt. Wenn du sie öffnest, eine Chatnachricht sendest, sie bearbeitest oder zurückstellst oder eine neue Nachricht eintrifft, kommt sie wieder zurück.

Ein Projekt, zu dem es eine Woche lang nichts Neues gab und bei dem keine Aufgabe offen ist, kann einmal pro Woche eine Aufgabe mit einem konkreten nächsten Schritt bekommen. Höchstens drei pro Woche. Siehe [Projekte](projects.md).

Wenn nichts deine Aufmerksamkeit braucht, ruht deine Machine bei einer leeren Liste. Während sie prüft, wacht sie auf und meldet sich. Wenn eine Prüfung fehlgeschlagen ist oder sich verspätet, steht das in der Zeile, zusammen mit **Jetzt prüfen**.

Mit **Alle**, **Arbeit** und **Privat** oben in der Seitenleiste kannst du alle Aufgaben oder nur eine Art davon anzeigen. Auf deinem Handy und Computer gilt dieselbe Auswahl. Wenn Arbeit oder Privat ausgewählt ist, führt **Alle anzeigen** zurück zur Gesamtansicht. Eine Warnung zu deiner Machine selbst, etwa dass ein Teil immer wieder neu startet, gehört weder zu Arbeit noch zu Privat und wird nur unter Alle angezeigt.

Über die Zeile oben in der Liste kannst du auch direkt zur anderen Ansicht wechseln: Unter **Nur privat** tippst du auf **Arbeit** oder **Alle anzeigen**.

In der Zeile oben in der Liste stehen Name und Inhalt deiner letzten Zusammenfassung vom Morgen oder Abend, zum Beispiel **Zusammenfassung von gestern Abend** · 12 erledigt, 3 offen. Tippe darauf, um die Zusammenfassung erneut zu lesen. Mit **Kopieren** kannst du sie an beliebiger Stelle einfügen. Sobald du sie öffnest oder auf das **×** tippst, bleibt sie auf allen deinen Geräten sichtbar, bis die nächste Zusammenfassung erscheint.

Ohne aktuelle Zusammenfassung wird **Heute bisher** angezeigt: Was heute erledigt wurde und was noch offen ist, für Arbeit und Privat oder nur für den ausgewählten Bereich.

Bei einer Aufgabe zu einem Projekt steht der Projektname unter dem Titel. Tippe darauf, um das Projekt zu öffnen. Mit **Projekt** unter **Details** kannst du das Projekt ändern oder entfernen. Siehe [Aufgaben eines Projekts](projects.md#a-project-s-to-dos).

Mit **Bereich** unter **Details** verschiebst du eine Aufgabe in deinen anderen Bereich. Der Zugriff auf Nachrichten, die sie lesen und senden darf, ändert sich entsprechend. Mit **Rückgängig** in der Mitteilung verschiebst du sie zurück.

Wenn eine Aufgabe deinen anderen Bereich benötigt, um fortzufahren, und alle zugehörigen Nachrichten dort liegen, wird sie automatisch dorthin verschoben und fortgesetzt. Andernfalls wird **Nach Arbeit verschieben** angezeigt, und erst wenn du darauf tippst, wird etwas verschoben. Eine Aufgabe, die du hinzugefügt hast, ohne Arbeit oder Privat auszuwählen, wird automatisch dem passenden Bereich zugeordnet, sobald sie weiß, wohin sie gehört. Bis dahin ist sie weder Arbeit noch Privat zugeordnet und bleibt privat.

Eine Aufgabe kann immer die Nachrichten lesen, aus denen sie entstanden ist. Wenn sie weitere Nachrichten aus deinem anderen Bereich braucht, fragt sie mit **Diese E-Mail für diese Aufgabe verwenden** danach. Ein Arbeits-Postfach, das du als Privat gekennzeichnet hast, zählt als Privat. E-Mails für ein anderes deiner Unternehmen gehören zu den Aufgaben dieses Unternehmens. Eine Aufgabe zu deinem Privatleben, etwa wenn deine Familie an deine Arbeitsadresse schreibt, ist von Anfang an privat.

Arbeit, die dich über ein persönliches Konto erreicht, etwa eine Nachricht von einem Kunden in WhatsApp, eine Bestellung in deinem privaten Postfach oder ein [Versprechen](promises.md) zu einer Arbeitssache, gehört von Anfang an zu Arbeit.

Eine Aufgabe, die du selbst verschoben oder zugeordnet hast, bleibt immer dort, wo du sie abgelegt hast. Arbeit oder Privat bestimmt, wo eine Aufgabe angezeigt und mit wem sie geteilt wird, nicht, wohin sie antwortet. Eine Antwort geht immer dorthin, wo das Gespräch stattfindet, auch nach dem Verschieben, außer du wählst einen anderen Weg.

Eine solche private Aufgabe antwortet weiterhin von der Arbeitsadresse aus, an die die E-Mail gesendet wurde. Sie erscheint nie in einer Work Fleet oder im Team Graph.

Wenn mindestens zwei Aufgaben auf dich warten, gehst du mit **Durchgehen** in der Kopfzeile von Für dich eine nach der anderen durch, in der Reihenfolge der Liste. Jeder Entwurf wird vollständig angezeigt, mit **Senden** oder **Ausführen**, **Änderungen anfragen**, **Zurückstellen** und **Überspringen**. Auf einem Computer sendet die Eingabetaste, `S` stellt zurück, `→` überspringt und Esc bricht ab. In der Kopfzeile steht, wie lange es in deinem Tempo dauert, zum Beispiel „etwa 2 Min.“

Am Ende wird gezählt, was gesendet oder geschlossen wurde und was noch vorbereitet wird.

Eine Aufgabe, bei der du etwas beantworten sollst, wird bei beiden nicht mitgezählt. Sie braucht deine Antwort, nicht einen Tipp.

## Jetzt prüfen

Deine Machine liest jede Quelle alle paar Minuten, Tag und Nacht. Sie prüft neue Nachrichten, sobald 40 Nachrichten eingegangen sind oder die älteste Nachricht einer Person seit 15 Minuten wartet. Newsletter, Benachrichtigungen und Belege werden bei der nächsten Prüfung berücksichtigt, spätestens innerhalb einer Stunde.

Nachts, von 00:00 bis 06:30 Uhr, pausieren die Prüfungen. Neue Nachrichten werden weiterhin gelesen und gespeichert und um 06:30 Uhr gemeinsam geprüft, damit deine Aufgaben vor der morgendlichen Zusammenfassung bereit sind. Unter Verbindungen steht bei den Prüfungen: „Nachts pausiert, wird um 06:30 Uhr nachgeholt“. Wenn du nachts in der App klickst, schreibst oder scrollst, im Chat schreibst oder auf eine Aufgabe tippst, laufen die Prüfungen wie gewohnt weiter, bis du eine Stunde lang abwesend warst. **Jetzt prüfen** startet immer sofort eine Prüfung.

Mit **Jetzt prüfen** werden alle Quellen sofort gelesen. Wenn keine Aufgabe offen ist, tippe auf die Zeile deiner Machine, um sie mit **Details** anzuzeigen. Damit öffnest du die Prüfungen unter Verbindungen. Wenn Aufgaben offen sind, findest du sie auf einem Computer oben. Eine kurze Zeile wird dort nur angezeigt, während eine Prüfung läuft oder wenn sie fehlgeschlagen ist oder sich verspätet. Du kannst auch im Chat danach fragen.

LinkedIn, X und Salesflare haben ihren eigenen Rhythmus.

## Letzte Prüfung

Nach einer Prüfung, bei der neue Nachrichten gelesen wurden, steht über deinen Aufgaben eine Zeile mit den Ergebnissen aus allen gelesenen Quellen, zum Beispiel „13 Nachrichten um 16:11 geprüft · keine neue Aufgabe“ oder „· 2 neue Aufgaben“. Die Zeile bezieht sich nur auf diese Prüfung. Aufgaben, die bereits auf deiner Liste stehen, bleiben unverändert. Wenn eine neue Aufgabe bis zu einem günstigeren Zeitpunkt zurückgehalten wird, etwa bis zur morgendlichen Zusammenfassung, steht dabei, bis wann: „1 Aufgabe bis morgen 08:30 zurückgehalten“.

Tippe auf die Zeile, um jeden E-Mail-Thread, Chat und jede Benachrichtigung mit dem Symbol der jeweiligen Quelle zu sehen: wer geschrieben hat, den Betreff oder die ersten Wörter und die neue Aufgabe oder den Grund, warum keine nötig war. Zum Beispiel: „Nur in Cc, ein Teammitglied antwortet“ oder „Termin für Donnerstag steht bereits“. Wenn die Prüfung nur einen allgemeinen Grund ergeben hat, wird bei einem Thread kein Grund angezeigt. Tippe auf einen Eintrag, um ihn mit dem Gesprächsverlauf zu lesen.

Die ersten 10 werden angezeigt. Tippe darunter, um den Rest zu sehen. Eine Zahl nach einem Namen, zum Beispiel (3), gibt an, wie viele neue Nachrichten der Chat enthält. Eine Handy-Benachrichtigung zu einer bereits aufgeführten Nachricht wird nur einmal angezeigt. Die Zeile bleibt 12 Stunden nach der Prüfung sichtbar.

Gezählt werden nur E-Mails an dich. Deine eigenen Antworten werden als Kontext und auf Versprechen hin gelesen, zählen aber nicht als neue E-Mails. E-Mails von The Machine an dich, etwa deine morgendliche Zusammenfassung oder eine Benachrichtigung zu einer Korrektur, werden nie gelesen oder aufgeführt. E-Mails zu Abrechnungen, deiner Testphase oder einer Einladung werden wie gewohnt gelesen.

## Die Schaltflächen

Bei einer Aufgabe wird der nächste Schritt angezeigt, zum Beispiel **Ausführen** oder **Prüfen und senden**, daneben **Zurückstellen**. Siehe [Ausführen](do-it.md) und [Zurückstellen](snooze.md).

Mit **Änderungen anfragen** kannst du angeben, was geändert werden soll: wie etwas erledigt werden soll oder, sobald ein Entwurf bereit ist, was daran geändert werden soll. **Als erledigt markieren** bedeutet, dass die Aufgabe erledigt ist. Bei einer vorbereiteten Aufgabe ohne Entwurf oder bei einer Aufgabe, die dich etwas fragt, ist die Schaltfläche direkt sichtbar, sonst ganz oben unter **…**. Die Aufgabe wird sofort aus der Liste entfernt, und in der Mitteilung wird **Rückgängig** angeboten. Wische die Nachricht weg oder ziehe sie mit der Maus aus der Liste, um sie schneller zu schließen. Die Änderung bleibt bestehen.

Wenn du möchtest, dass es anders erledigt wird, schreib es in den **Chat** der Aufgabe. In der Antwort steht nur, was geändert wurde, zum Beispiel das Zurückstellen und bis wann. Wenn sich etwas nicht ändern ließ, etwa ein Fälligkeitsdatum, steht das ebenfalls dabei.

Unter **…**:

- **Übergeben…**: Übergib die Aufgabe an ein Teammitglied, an [Claude Code oder Codex](hand-to-agent.md) oder [bitte jemanden um eine Prüfung](ask-to-review.md).
- **Wiederholen…**: Die Aufgabe [kommt regelmäßig wieder](recurring.md).
- **Nicht nötig**: Die Aufgabe wird entfernt. Optional kannst du einen Grund auswählen: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Tippe auf den Titel oder unter **Details** auf **Name**, um die Aufgabe umzubenennen. Du kannst auch im Chat darum bitten, zum Beispiel „Benenne sie in … um“. Dein Titel bleibt bestehen.

Mit **Wieder öffnen** wird eine geschlossene Aufgabe wieder geöffnet. Sie kommt auch von selbst zurück, wenn etwas Neues passiert, etwa eine neue Nachricht von der anderen Person, aber nicht bei deiner eigenen Antwort. Dann wird angezeigt, wann sie zurückgekommen ist, und sie wird wie eine neue Aufgabe sortiert. Der Chat wird dort fortgesetzt, wo er aufgehört hat, auch nach Wochen.

Eine Rechnung, die du selbst noch bezahlen musst, wird unabhängig vom Land zu einer Aufgabe mit dem Betrag, dem Fälligkeitsdatum und den Zahlungsangaben auf der Rechnung. Automatisch bezahlte Rechnungen, etwa per Lastschrift oder mit einer hinterlegten Karte, werden nicht zu Aufgaben. Wenn eine spätere E-Mail zeigt, dass sie bezahlt wurde, zum Beispiel eine Bestätigung des Absenders über den Zahlungseingang, wird die Aufgabe automatisch geschlossen. **Rückgängig** holt sie einen Tag lang zurück.

Eine Aufgabe, die nur bis zu einem bestimmten Zeitpunkt wichtig war, etwa eine Bestätigung vor einem Meeting, wird danach automatisch geschlossen. Sie wird mit dem Vermerk „Nicht mehr nötig“ nach **Erledigt / verworfen** verschoben. Mit **Rückgängig** holst du sie einen Tag lang zurück.

Bevor eine Nachricht oder Übergabe für jemand anderen als bereit angezeigt wird, prüft deine Machine deine letzten Chats mit den beteiligten Personen, auch Gruppenchats, und wartet darauf, dass Slack sie gelesen hat. Wenn eine spätere Nachricht zeigt, dass die Aufgabe bereits erledigt ist, zum Beispiel weil jemand gefragt wurde und zugesagt hat, wird sie automatisch geschlossen. **Rückgängig** holt sie einen Tag lang zurück.

Wenn jemand anderes im selben Gespräch geschrieben hat, nachdem der Entwurf erstellt wurde, hält **Senden** den Entwurf zurück: „Nicht gesendet: neue Nachricht im Thread“. Bei der Aufgabe werden diese Nachricht sowie **Lesen** und **Für diese Nachricht neu machen** angezeigt. Tippe erneut auf **Senden**, um den Entwurf unverändert zu senden.

Wenn eine neuere Nachricht den Plan ändert, zum Beispiel wenn eine Feier an einen anderen Ort verlegt oder eine Buchung storniert wird, aktualisiert The Machine die Aufgaben selbst. Eine weiterhin relevante Aufgabe folgt dem neuen Plan. Wenn nichts mehr zu tun ist, wird sie mit dem Vermerk „Nicht nötig“ nach **Erledigt / verworfen** verschoben. Im Chat steht „Aktualisiert:“ mit dem Grund. Mit **Rückgängig** holst du sie einen Tag lang zurück.

Bei deinen ersten Aufgaben wird ein kurzer Tipp zu den wichtigsten Aktionen angezeigt: **Änderungen anfragen** und **Nicht nötig**. Außerdem erfährst du darin, dass erst dann etwas gesendet wird, wenn du auf **Senden** tippst. Der Tipp wird dauerhaft ausgeblendet, sobald du die Schaltfläche verwendest oder auf × tippst.

An deinem ersten Tag begrüßt dich deine Machine oben auf der Seite „Aufgaben“ und nennt die Person, die am längsten auf deine Antwort wartet. Dieser Antwortentwurf wird zuerst erstellt und ist bereit, wenn du kommst.

Jede Aufgabe beginnt mit ihrem Titel. Darunter steht, um wen es geht, die Organisation, falls eine dazugehört (nicht allein deshalb, weil jemand dort arbeitet), das Projekt, Arbeit oder Privat und wann die Aufgabe eingegangen ist. Tippe auf einen Namen, um die Seite der Person im Graph zu öffnen.

Bei Namen und Organisationen wird das Foto oder Logo angezeigt, sofern es im Graph vorhanden ist. Andernfalls erscheinen die Initialen. Wenn ein Logo in dieser Größe nicht lesbar wäre, zum Beispiel weiß auf transparentem Hintergrund oder als breites Wortzeichen, wird stattdessen ebenfalls die Initiale angezeigt.

Manchmal steht in einer unauffälligen Zeile, was nicht bekannt ist, zum Beispiel „Letzter Kontakt vor 12 Tagen per E-Mail, seitdem nichts.“ Sie wird angezeigt, wenn der letzte Kontakt schon lange zurückliegt oder unbeantwortet ist, und nennt nicht verbundene Kanäle, etwa WhatsApp. Deine Machine sagt, was sie nicht weiß, statt zu raten.

Wenn ein nicht verbundener Kanal genannt wird, öffnet **Verbinden** daneben diese Verbindung.

Der Titel sagt, was zu tun ist, und ändert sich nur, wenn sich das ändert. Eine erledigte Aufgabe behält ihren Titel. Darunter steht, wie sie abgeschlossen wurde, zum Beispiel „Erledigt: Sam hat am Dienstag unterschrieben“.

Über dem Entwurf steht in einer unauffälligen Zeile, aus welcher Nachricht er stammt, samt Logo des Dienstes. Tippe darauf, um den Thread zu lesen. Der Entwurf zeigt das Logo des Ziels. So siehst du sofort, ob es eine Slack-Antwort oder eine E-Mail ist.

Wenn der Entwurf auf einer Eingabe an anderer Stelle beruht, zum Beispiel einem Vorschlag eines Teammitglieds in Slack, steht das in einer Zeile, etwa „Basierend auf Sam in #ops“. Tippe darauf, um die Nachricht zu lesen. Sie wird ausgeblendet, sobald ein neuer Entwurf sie ersetzt.

Ein Chat (Slack, WhatsApp, Telegram, Intercom …) wird als ein Gespräch angezeigt, älteste Nachricht zuerst: die Nachrichten vor der Nachricht, um die es bei der Aufgabe geht, und die Antworten danach. In WhatsApp, Telegram oder Signal stehen deine Nachrichten wie in der App rechts. Die Nachricht der Aufgabe ist mit „Diese Aufgabe“ markiert und wird geöffnet angezeigt. Mit **Frühere Nachrichten anzeigen** werden ältere Nachrichten hinzugefügt. Bei einer E-Mail ist der restliche Thread ober- und unterhalb der Nachricht eingeklappt.

Eine Nachricht wird aus der Suche, dem Graph, den Antworten von Ask oder der letzten Prüfung auf dieselbe Weise geöffnet und mit „Diese Nachricht“ (oder „Neue Nachrichten“) markiert.

Mit **In Gmail öffnen** wird die E-Mail in dem Gmail-Konto geöffnet, in dem sie eingegangen ist. Auf Android wird sie in der Gmail-App geöffnet, sofern du diese installiert hast.

Unter **Details** einer E-Mail stehen nur Angaben, die nicht bereits in der Kopfzeile zu sehen sind, etwa vollständige Cc-Adressen, Bcc oder eine andere Antwortadresse. Gibt es nichts hinzuzufügen, wird nichts angezeigt.

Bei einer Antwort in einem Slack-Thread wird auch angezeigt, was vor Beginn des Threads gesagt wurde. Über den Link einer Aufgabe zu ihrer eigenen Nachricht kannst du sie ebenfalls hier öffnen. Unten wird **In Slack öffnen** angezeigt.

Unter **Details** stehen Name, Projekt und Bereich (tippe auf einen Eintrag, um ihn zu ändern), deine letzte Notiz und das Ergebnis eines Coding-Agenten. Über den Titel öffnest du den Chat. Eine erledigte Aufgabe bleibt kompakt. Die Nachricht, aus der sie entstanden ist, steht unter **Details**.

Eine Aufgabe mit „Wartet auf“ verlinkt deine letzte Nachricht an die andere Person, auf deren Antwort du wartest: „E-Mail an Pat · Di.“

## Selbst eine Aufgabe erstellen

Mit **Neue Aufgabe** (unter **Suchen** auf einem Computer, **+** auf einem Handy oder `N`) erstellst du eine Aufgabe für alles Mögliche. Beim Erstellen wird nichts gesendet. Wenn du nicht **Arbeit** oder **Privat** auswählst, wird die Aufgabe dem passenden Bereich zugeordnet, je nachdem, um wen und was es geht. Sie findet auch die E-Mail, auf die sie sich bezieht, selbst wenn sie älter ist.

- **Fällig**: Gib einen Tag oder eine Uhrzeit ein, zum Beispiel „morgen“, „nächsten Fr“, „3. Nov“, „14 Uhr“ oder „in 2 Stunden“, auch in deiner eigenen Sprache. Über das Kalendersymbol findest du eine Auswahl mit Schnellzugriff und **Datum wählen**.
- **Wiederholt sich**: Die Aufgabe kommt regelmäßig wieder. Siehe [Wiederkehrende Aufgaben](recurring.md).
- **Person**: Verknüpfe bis zu 5 Personen oder Unternehmen, um die es geht.
- Nachrichtensymbol: Hänge die Nachricht an, um die es geht: eine E-Mail, Slack-, Teams-, WhatsApp- oder Telegram-Nachricht oder eine andere Nachricht, die The Machine vorliegt. Suche nach Text oder Absender. Bei jedem Treffer steht, woher er stammt, wer ihn gesendet hat und wann.
- **Dateien**: Tippe auf die Büroklammer, füge einen Screenshot ein oder ziehe Dateien auf das Formular. Auf einem Handy kannst du mit der Kamera daneben ein Foto aufnehmen. Bis zu 5 Dateien, wie im Chat (siehe [Dateien hinzufügen](card-chat.md#add-files)). Mit × entfernst du eine Datei wieder.

Die Dateien bleiben bei der Aufgabe, und The Machine liest sie, wenn sie daran arbeitet. Dateien allein genügen: Aus einer PDF- oder Textdatei erstellt sie die Aufgabe. Ein Foto wird als kleines Bild angezeigt. Tippe darauf, um es in voller Größe zu sehen.
