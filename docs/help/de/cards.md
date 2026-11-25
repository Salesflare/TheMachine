---
title: Aufgaben
area: cards
summary: Eine Aufgabe für alles, was dich braucht und auf dein Okay wartet. Was die einzelnen Teile einer Aufgabe bedeuten.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 43d9497d3a1c4a86
---
Deine Machine liest alles Neue und erstellt nur dann eine Aufgabe, wenn etwas dich braucht. Eine Aufgabe pro Anliegen, egal über wie viele Nachrichten es sich erstreckt.

## Wo Aufgaben stehen

Auf der Seite **Aufgaben** sind sie gruppiert:

- **Gerade erledigt**: Ganz oben siehst du den letzten Schritt, den du bestätigt hast, zum Beispiel ein Formular oder ein Problem, das erledigt wurde, während du nicht da warst. Er bleibt höchstens einen Tag lang stehen, bis du auf **Verstanden** tippst. Auch auf deinem Handy wirst du darüber informiert.
- **Für dich**: Alles, was auf dich wartet. Was bis morgen fällig ist, steht zuerst. Bei jeder Aufgabe steht **Vorbereitet** (ein Entwurf oder Ergebnis ist bereit und wird mit **Ausführen** oder **Senden** umgesetzt), **Braucht dich** (erst ist deine Entscheidung oder Antwort nötig; wenn die Arbeit ohne etwas, das nur du weißt, nicht weitergehen oder genutzt werden kann, zum Beispiel ohne einen Preis, eine Information oder eine Entscheidung, steht unter dem Titel, was fehlt), **Wird vorbereitet…** (deine Machine arbeitet daran) oder **Zum Lesen** (eine Zusammenfassung oder ein Briefing, bei dem nichts entschieden werden muss).
- **Älter**: Hier sind Aufgaben eingeklappt, zu denen es seit einer Woche nichts Neues gibt (siehe unten).
- **Wartet auf andere**: Hier sind Aufgaben eingeklappt, bei denen der nächste Schritt bei jemand anderem liegt (siehe unten).
- **Kommt später zurück**: Zurückgestellte Aufgaben, Nachrichten, die [später gesendet werden](send-later.md), und Aufgaben ohne Antwort auf **Noch nötig?** (siehe unten).
- **Versprechen**: Was du versprochen hast und was andere dir versprochen haben. Siehe [Versprechen](promises.md).
- **Erledigt / verworfen**: Alle erledigten Aufgaben, die neueste zuerst, mit dem Zeitpunkt, zu dem sie abgeschlossen wurden, zum Beispiel „Vor 5 Minuten erledigt“. Aufgaben, die offenbar schon erledigt sind, sind mit **Sieht erledigt aus** markiert.

Nach dem Senden steht in einer kurzen Meldung, wohin die Aufgabe verschoben wurde, zum Beispiel „Gesendet. Nach Erledigt verschoben.“ oder „Gesendet. Bis Mo. auf Später verschoben.“ Wenn eine Antwort nur verspricht, die Arbeit zu erledigen, zum Beispiel „Ich schicke es bis Dienstag“, bleibt die Aufgabe offen: „Gesendet. Offen gelassen.“ **Öffnen** führt dich zur Aufgabe. Über die Suche findest du Aufgaben nach Titel oder danach, an wen sie gegangen sind, auch unter Später und Erledigt.

Unter **Für dich** stehen zuerst überfällige Aufgaben und Aufgaben, die bis morgen fällig sind, danach Fragen aus deiner Fleet, dann Nachfassnachrichten zu einem Board und anschließend der Rest. Innerhalb jeder Gruppe stehen die neuesten zuerst. Eine Aufgabe behält ihren Platz, während deine Machine sie vorbereitet und wenn sie erledigt ist. Nur ihre Markierung ändert sich. In den anderen offenen Gruppen stehen überfällige Aufgaben und Aufgaben, die bis morgen fällig sind, zuerst, danach der Rest, neueste zuerst. Die Seitenleiste behält dieselbe Reihenfolge bei.

**Sieht erledigt aus** bedeutet, dass deine Machine erkennt, dass die Aufgabe erledigt ist, zum Beispiel „PR #3451 wurde zusammengeführt“, sie aber noch nicht geschlossen ist. Mit **Wieder öffnen** kommt sie zurück auf deine Liste, und deine Machine lernt daraus. Diese Aufgaben erscheinen nie als verspätet. Wenn eine Nachricht darauf hinweist, wird die Aufgabe nach einem Tag automatisch geschlossen. Dabei kannst du mit **Rückgängig** die Änderung zurücknehmen. Ansonsten wartet sie darauf, dass du **Als erledigt markieren** auswählst.

Eine Aufgabe, die du selbst bereits erledigt hast, zum Beispiel mit einer Antwort in Gmail oder Slack, wird ebenfalls automatisch geschlossen. Eine Antwort, in der steht, dass eine Datei angehängt ist, obwohl keine angehängt wurde, schließt die Aufgabe nicht.

Wenn eine Nachricht von einer Adresse kommt, die nur wie die einer Person aussieht, die du kennst, zum Beispiel sam@acme-corp.example statt sam@acmecorp.example, steht bei der Aufgabe deutlich: „Das ist nicht Sam Lee.“ Die Person wird unter ihrer tatsächlichen Adresse angezeigt, niemals unter dem Namen, den sie selbst verwendet hat. Deine Machine prüft solche Nachrichten bei der Person unter der Adresse, die du bereits hast, niemals bei der Person, die geschrieben hat.

Bei einer Aufgabe, die noch auf jemand anderen wartet, zum Beispiel auf eine Prüfung oder Antwort, steht der nächste Schritt unter **Wartet auf**. Sie bleibt eingeklappt unter **Wartet auf andere**, oberhalb von „Kommt später zurück“, bis eine neue Nachricht sie wieder hervorholt. Dasselbe gilt, wenn du eine Rückfrage gestellt hast: Die Aufgabe kommt am Morgen vor der Frist zurück, bei einer Frist später am selben Tag zum Zeitpunkt der Frist oder am nächsten Morgen, wenn die Frist bereits verstrichen ist. Dabei steht, auf wen sie noch wartet.

Wenn es bei einer Aufgabe um ein Ergebnis geht, das jemand anderes liefern muss, zum Beispiel einen unterschriebenen Vertrag, wird es unter **Details** als **Fertig, wenn** angezeigt. Wenn du deinen Teil sendest, wird die Aufgabe nicht geschlossen. Sie wartet unter **Wartet auf andere**, bis eine Nachricht das Ergebnis bestätigt. Dann wird sie automatisch geschlossen und du kannst die Änderung mit **Rückgängig** zurücknehmen. Wenn bis zum Zeitpunkt, an dem du nachhaken solltest, nichts eingeht, kommt sie mit **Schreib eine kurze Erinnerung** im Chat zurück. Schreib im Chat, was als erledigt gilt, um das zu ändern.

Bei einer Aufgabe, zu der es eine Woche lang nichts Neues gab, verschiebt sie sich von „Für dich“ nach **Älter**. So stehen nach ein paar Tagen Abwesenheit neue Aufgaben zuerst. Neu heißt: Es gab keine neue Nachricht dazu und du hast nichts daran gemacht, zum Beispiel eine Chatnachricht geschrieben, etwas bearbeitet oder sie zurückgestellt. Es zählt nicht, wenn du sie nur ansiehst.

Dringende Aufgaben, Aufgaben, die bald fällig sind, und Aufgaben, deren Versand ansteht, bleiben unter „Für dich“. **Alle verwerfen** markiert nach einmaliger Bestätigung alle Aufgaben unter „Älter“ als nicht nötig, so wie **Nicht nötig** es einzeln tut. Mit **Rückgängig** kannst du die Änderung zurücknehmen. Gibt es zu einer Aufgabe etwas Neues, kommt sie zurück zu „Für dich“.

Eine Aufgabe, die eine Woche lang niemand angefasst hat, fragt einmal: **Noch nötig?** Mit **Nicht nötig** wird sie geschlossen. Mit **Rückgängig** kannst du die Änderung zurücknehmen. **Behalten** lässt sie offen. Danach wird nicht erneut gefragt. Wenn du eine weitere Woche lang nicht antwortest, wird sie unter „Kommt später zurück“ eingeklappt. Sie wird dann nicht mehr auf dem App-Symbol und in der morgendlichen Zusammenfassung mitgezählt. Wenn du sie öffnest, im Chat schreibst, sie bearbeitest oder zurückstellst oder eine neue Nachricht eintrifft, kommt sie zurück.

Einmal pro Woche kann es für ein Projekt, zu dem es länger nichts gab und bei dem keine Aufgaben offen sind, eine Aufgabe mit einem konkreten nächsten Schritt geben. Höchstens drei pro Woche. Siehe [Projekte](projects.md).

Wenn nichts deine Aufmerksamkeit braucht, macht deine Machine ein Nickerchen und zeigt eine leere Liste. Während sie prüft, wacht sie auf und sagt Bescheid. Wenn eine Prüfung fehlgeschlagen ist oder sich verspätet, steht das in der Meldung. Darunter findest du **Jetzt prüfen**.

Mit **Alle**, **Arbeit** und **Privat** oben in der Seitenleiste kannst du alle Aufgaben oder nur eine Art anzeigen. Auf deinem Handy und Computer wird dieselbe Auswahl verwendet. Wenn „Arbeit“ oder „Privat“ ausgewählt ist, führt **Alle anzeigen** zurück zur Gesamtansicht. Eine Warnung zu deiner Machine selbst, zum Beispiel dass ein Teil immer wieder neu startet, ist weder Arbeit noch privat und erscheint nur unter „Alle“.

Mit der Zeile oben in der Liste kannst du auch direkt zur jeweils anderen Ansicht wechseln: Unter **Nur privat** tippst du auf **Arbeit** oder **Alle anzeigen**.

Die Zeile oben in der Liste nennt deine letzte morgendliche oder abendliche Zusammenfassung und was darin gezählt wurde, zum Beispiel **Zusammenfassung von gestern Abend** · 12 erledigt, 3 offen. Tippe darauf, um die Zusammenfassung noch einmal zu lesen. Mit **Kopieren** kannst du sie an beliebiger Stelle einfügen. Sobald du sie öffnest oder auf ihr **×** tippst, bleibt sie auf allen deinen Geräten verfügbar, bis die nächste Zusammenfassung kommt.

Wenn es keine aktuelle Zusammenfassung gibt, wird **Heute bisher** angezeigt: Was heute erledigt wurde und was noch offen ist, für Arbeit und privat oder nur für den ausgewählten Bereich.

Bei einer Aufgabe für ein Projekt steht der Projektname unter dem Titel. Tippe darauf, um das Projekt zu öffnen. Mit **Projekt** unter **Details** kannst du das Projekt ändern oder entfernen. Siehe [Aufgaben eines Projekts](projects.md#a-project-s-to-dos).

Mit **Bereich** unter **Details** verschiebst du eine Aufgabe in deinen anderen Bereich. Was sie lesen und senden darf, wird ebenfalls verschoben. Mit **Rückgängig** in der Meldung verschiebst du sie zurück.

Wenn eine Aufgabe deinen anderen Bereich braucht, um weiterzugehen, und alle Nachrichten, auf denen sie basiert, zu diesem Bereich gehören, wird sie automatisch dorthin verschoben und fortgesetzt. Andernfalls wird **Nach Arbeit verschieben** angezeigt. Erst wenn du darauf tippst, wird etwas verschoben. Eine Aufgabe, die du hinzugefügt hast, ohne „Arbeit“ oder „Privat“ auszuwählen, wird automatisch verschoben, sobald klar ist, wohin sie gehört. Bis dahin ist sie weder Arbeit noch privat und bleibt vertraulich.

Eine Aufgabe kann immer die Nachrichten lesen, aus denen sie entstanden ist. Wenn sie weitere Nachrichten aus deinem anderen Bereich braucht, fragt sie mit **Diese E-Mail für diese Aufgabe verwenden** nach. Ein Arbeits-Postfach, das du als privat markiert hast, zählt als privat. Nachrichten für ein anderes deiner Unternehmen gehören zu den Aufgaben dieses Unternehmens. Eine Aufgabe zu deinem eigenen Leben, zum Beispiel wenn deine Familie an deine Arbeitsadresse schreibt, ist von Anfang an privat.

Arbeit, die dich über ein privates Konto erreicht, zum Beispiel von einem Kunden auf WhatsApp, eine Bestellung in deinem privaten Postfach oder ein [Versprechen](promises.md) zu einer Arbeitssache, ist von Anfang an Arbeit.

Eine Aufgabe, die du selbst verschoben oder erstellt hast, bleibt immer dort, wo du sie abgelegt hast. „Arbeit“ oder „Privat“ legt fest, wo eine Aufgabe angezeigt und mit wem sie geteilt wird, niemals, wohin sie antwortet. Eine Antwort geht immer dorthin, wo das Gespräch stattfindet, auch nach einer Verschiebung, es sei denn, du wählst einen anderen Weg.

Eine solche private Aufgabe antwortet weiterhin von der Arbeitsadresse, an die ihre E-Mail gesendet wurde. Sie wird nie in einer Work Fleet oder im Team Graph angezeigt.

Wenn mindestens zwei Aufgaben auf dich warten, kannst du mit **Durchgehen** in der Kopfzeile von „Für dich“ jede Aufgabe der Reihe nach durchgehen. Der vollständige Entwurf wird jeweils angezeigt, mit **Senden** oder **Ausführen**, **Änderungen anfragen**, **Zurückstellen** und **Überspringen**. Auf einem Computer sendet Enter den angezeigten Inhalt, `S` stellt zurück, `→` überspringt und Esc bricht ab. In der Kopfzeile steht, wie lange es bei deinem Tempo dauert, zum Beispiel „etwa 2 Min.“.

Am Ende wird gezählt, was gesendet oder geschlossen wurde und was noch vorbereitet wird.

Aufgaben mit einer Frage an dich werden dabei ausgelassen: Sie brauchen deine Antwort, keinen Tipp.

## Jetzt prüfen

Deine Machine liest jede Quelle alle paar Minuten, Tag und Nacht. Sie prüft neue Nachrichten, sobald 40 davon warten oder die älteste Nachricht einer Person seit 15 Minuten wartet. Newsletter, Benachrichtigungen und Belege werden bei der nächsten Prüfung berücksichtigt, spätestens innerhalb einer Stunde.

Nachts, von 00:00 bis 06:30 Uhr, pausieren die Prüfungen. Neue Nachrichten werden weiterhin gelesen und gespeichert und um 06:30 Uhr gemeinsam geprüft, damit deine Aufgaben vor der morgendlichen Zusammenfassung bereit sind. Unter „Verbindungen“ steht bei den Prüfungen: „Über Nacht pausiert, wird um 06:30 Uhr nachgeholt“. Wenn du nachts in der App klickst, tippst oder scrollst, im Chat schreibst oder auf eine Aufgabe tippst, laufen die Prüfungen wie gewohnt weiter, bis du eine Stunde lang nicht mehr aktiv warst. **Jetzt prüfen** startet immer sofort eine Prüfung.

**Jetzt prüfen** liest sofort alle Quellen. Wenn keine Aufgaben offen sind, tippe auf die Zeile deiner Machine, um sie mit **Details** anzusehen. Dadurch öffnet sich „Prüfungen“ unter „Verbindungen“. Wenn Aufgaben offen sind, findest du die Zeile oben auf dem Computer. Eine kurze Meldung wird dort nur angezeigt, während eine Prüfung läuft oder wenn sie fehlgeschlagen ist oder sich verspätet. Du kannst auch im Chat danach fragen.

LinkedIn, X und Salesflare haben ihren eigenen Rhythmus.

## Letzte Prüfung

Nach einer Prüfung, bei der neue Nachrichten gelesen wurden, steht über deinen Aufgaben, was dabei gefunden wurde und aus welchen Quellen, zum Beispiel „13 Nachrichten um 16:11 geprüft · keine neue Aufgabe“ oder „· 2 neue Aufgaben“. Die Meldung bezieht sich nur auf diese Prüfung. Aufgaben, die bereits auf deiner Liste stehen, bleiben unverändert. Wenn eine neue Aufgabe auf einen passenden Zeitpunkt warten soll, zum Beispiel auf deine morgendliche Zusammenfassung, steht dort, bis wann: „1 Aufgabe bis morgen 08:30 zurückgehalten“.

Tippe auf die Meldung, um jeden E-Mail-Thread, Chat und jede Benachrichtigung mit dem Symbol der jeweiligen Quelle zu sehen: wer geschrieben hat, den Betreff oder die ersten Wörter und die neue Aufgabe oder den Grund, warum nichts nötig war, zum Beispiel „Nur in Cc, ein Teammitglied antwortet“ oder „Meeting für Donnerstag steht schon fest“. Bei einem Thread wird kein Grund angezeigt, wenn die Prüfung nur einen vagen Grund ergeben hat. Tippe auf einen Eintrag, um die Nachricht samt vorherigem Gespräch zu lesen.

Die ersten 10 Einträge werden angezeigt. Tippe darunter, um den Rest zu sehen. Eine Zahl nach einem Namen, zum Beispiel (3), gibt an, wie viele neue Nachrichten es in diesem Chat gibt. Eine Android-Benachrichtigung zu einer Nachricht, die bereits aufgelistet ist, wird nur einmal angezeigt. Die Meldung bleibt 12 Stunden nach der Prüfung sichtbar.

Gezählt werden nur E-Mails, die an dich gesendet wurden. Deine eigenen Antworten werden als Kontext und auf Versprechen hin gelesen, zählen aber nicht als neue E-Mail. Die E-Mails deiner Machine an dich, zum Beispiel deine morgendliche Zusammenfassung oder eine Benachrichtigung zu einer Fehlerbehebung, werden nie gelesen oder aufgelistet. E-Mails zu Abrechnung, Testphase oder Einladungen werden wie gewohnt gelesen.

## Die Schaltflächen

Bei einer Aufgabe steht der nächste Schritt, zum Beispiel **Ausführen** oder **Prüfen und senden**, daneben **Zurückstellen**. Siehe [Ausführen](do-it.md) und [Zurückstellen](snooze.md).

Unter **Änderungen anfragen** kannst du angeben, was geändert werden soll: wie etwas erledigt werden soll oder, sobald ein Entwurf bereit ist, was daran geändert werden soll. Wenn du deine Eingabe nicht abschickst, ist sie noch da, wenn du zurückkommst. **Abbrechen** verwirft sie.

**Als erledigt markieren** bedeutet, dass die Aufgabe erledigt ist. Auf einem Computer steht die Schaltfläche zwischen den anderen, wenn sie in eine Zeile passen. Auf einem Handy ist sie bei einer fertigen Aufgabe ohne Entwurf oder bei einer Aufgabe mit einer Frage an dich direkt sichtbar. Ansonsten findest du sie oben unter **…**. Die Aufgabe wird sofort aus der Liste entfernt. In der Meldung kannst du mit **Rückgängig** die Änderung zurücknehmen. Wische die Nachricht weg oder ziehe sie mit der Maus aus der Liste, um sie schneller zu schließen. Die Änderung bleibt bestehen.

Wenn du die Aufgabe anders erledigen lassen willst, schreib es in den **Chat**. In der Antwort steht nur, was sich geändert hat, zum Beispiel, dass die Aufgabe zurückgestellt wurde und bis wann. Wenn etwas nicht geändert werden konnte, zum Beispiel das Fälligkeitsdatum, wird das mitgeteilt.

Unter **…**:

- **Übergeben…**: Übergib die Aufgabe an ein Teammitglied, an [Claude Code oder Codex](hand-to-agent.md) oder [bitte jemanden um eine Prüfung](ask-to-review.md).
- **Wiederholen…**: Die Aufgabe [kommt regelmäßig wieder](recurring.md).
- **Nicht nötig**: Die Aufgabe verschwindet. Du kannst optional einen Grund auswählen: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Tippe auf den Titel oder unter **Details** auf **Name**, um die Aufgabe umzubenennen. Du kannst auch im Chat darum bitten, zum Beispiel: „Benenne sie in … um“. Dein Titel bleibt erhalten.

Mit **Wieder öffnen** holst du eine geschlossene Aufgabe zurück. Sie kommt auch automatisch wieder, wenn etwas Neues passiert, zum Beispiel eine neue Nachricht von der Person, nicht aber bei deiner eigenen Antwort. Dann wird angezeigt, wann sie zurückkam, und sie erscheint wie eine neue Aufgabe. Der Chat wird dort fortgesetzt, wo er aufgehört hat, auch nach Wochen.

Eine Rechnung, die du selbst noch bezahlen musst, wird unabhängig vom Land zu einer Aufgabe mit Betrag, Fälligkeitsdatum und den Zahlungsangaben auf der Rechnung. Automatisch bezahlte Rechnungen, zum Beispiel per Lastschrift oder gespeicherter Karte, werden nicht zu Aufgaben. Wenn eine spätere E-Mail bestätigt, dass die Rechnung bezahlt wurde, zum Beispiel eine Nachricht des Absenders über den Zahlungseingang, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du sie innerhalb eines Tages zurückholen.

Eine Aufgabe, die nur bis zu einem festgelegten Zeitpunkt wichtig war, zum Beispiel eine Bestätigung vor einem Meeting, wird danach automatisch geschlossen. Sie erscheint unter **Erledigt / verworfen** mit dem Hinweis „Nicht mehr nötig“. Mit **Rückgängig** kannst du sie innerhalb eines Tages zurückholen.

Bevor eine Nachricht oder Übergabe für jemand anderen als bereit angezeigt wird, prüft deine Machine deine letzten Chats mit den beteiligten Personen, auch Gruppenchats, und wartet, bis Slack sie gelesen hat. Wenn eine spätere Nachricht zeigt, dass die Aufgabe schon erledigt ist, zum Beispiel weil jemand darum gebeten wurde und zugestimmt hat, wird sie automatisch geschlossen. Mit **Rückgängig** kannst du sie innerhalb eines Tages zurückholen.

Wenn jemand nach dem Erstellen deines Entwurfs in derselben Unterhaltung geschrieben hat, hält **Senden** den Entwurf zurück: „Nicht gesendet: neue Nachricht im Thread“. Die Aufgabe zeigt die Nachricht mit **Lesen** und **Für diese Nachricht neu machen** an. Drücke noch einmal auf **Senden**, um den Entwurf unverändert zu senden.

Wenn eine neuere Nachricht den Plan ändert, zum Beispiel wenn eine Party an einen anderen Ort verlegt oder eine Buchung storniert wurde, aktualisiert The Machine ihre Aufgaben selbst. Eine weiterhin relevante Aufgabe folgt dem neuen Plan. Wenn nichts mehr zu tun ist, wird sie unter **Erledigt / verworfen** als „Nicht nötig“ abgelegt. Im Chat steht „Aktualisiert:“ mit dem Grund. Mit **Rückgängig** kannst du sie innerhalb eines Tages zurückholen.

Bei deinen ersten Aufgaben wird ein kurzer Tipp zu den wichtigsten Aktionen angezeigt: **Änderungen anfragen** und **Nicht nötig**. Außerdem erfährst du, dass nichts gesendet wird, bevor du auf **Senden** drückst. Ein Tipp wird dauerhaft ausgeblendet, sobald du seine Schaltfläche verwendest oder auf × drückst.

Am ersten Tag begrüßt dich deine Aufgabenliste oben und nennt die Person, die am längsten auf deine Antwort wartet. Dieser Antwortentwurf wird zuerst erstellt, damit er bereit ist, wenn du da bist.

Jede Aufgabe beginnt mit ihrem Titel. Darunter steht, um wen es geht, bei Aufgaben zu einer Organisation auch die Organisation (aber nicht allein deshalb, weil jemand dort arbeitet), das Projekt, „Arbeit“ oder „Privat“ und wann die Aufgabe eingegangen ist. Tippe auf einen Namen, um die Seite der Person im Graph zu öffnen.

Wenn der Graph ein Foto oder Logo hat, wird es neben dem Namen oder der Organisation angezeigt. Andernfalls erscheinen die Initialen. Bei einem Logo, das in dieser Größe nicht lesbar wäre, zum Beispiel weiß auf transparentem Hintergrund oder als breites Schriftlogo, werden ebenfalls die Initialen angezeigt.

Manchmal steht in einer unauffälligen Zeile, was nicht bekannt ist, zum Beispiel: „Letzter Kontakt vor 12 Tagen per E-Mail, seitdem nichts.“ Das wird angezeigt, wenn der letzte Kontakt schon länger her ist oder noch unbeantwortet ist. Dabei werden auch nicht verbundene Kanäle wie WhatsApp genannt. Deine Machine sagt, was sie nicht weiß, statt zu raten.

Wenn ein nicht verbundener Kanal genannt wird, öffnet **Verbinden** daneben die entsprechende Verbindung.

Der Titel beschreibt, was zu tun ist, und ändert sich nur, wenn sich das ändert. Eine erledigte Aufgabe behält ihren Titel. Darunter steht, wie sie erledigt wurde, zum Beispiel „Erledigt: Sam hat es am Dienstag unterschrieben“.

Über dem Entwurf steht in einer unauffälligen Zeile, aus welcher Nachricht er stammt, mit dem Logo des Dienstes. Tippe darauf, um den Thread zu lesen. Das Logo neben dem Entwurf zeigt, wohin er gesendet wird. So siehst du sofort, ob es sich um eine Slack-Antwort oder eine E-Mail handelt.

Wenn der Entwurf auf einer Eingabe von jemand anderem an anderer Stelle basiert, zum Beispiel auf einem Vorschlag eines Teammitglieds in Slack, steht das in einer Zeile, zum Beispiel „Basierend auf Sam in #ops“. Tippe darauf, um die Nachricht zu lesen. Sie wird nicht mehr angezeigt, wenn eine Aktualisierung den Entwurf ersetzt.

Ein Chat (Slack, WhatsApp, Telegram, Intercom …) wird als eine Unterhaltung angezeigt, älteste Nachricht zuerst: die Nachrichten vor der Nachricht, auf die sich die Aufgabe bezieht, und die Antworten danach. In WhatsApp, Telegram oder Signal stehen deine Nachrichten wie in der App rechts. Die Nachricht der Aufgabe ist mit „Diese Aufgabe“ markiert und wird geöffnet angezeigt. Mit **Frühere Nachrichten anzeigen** werden ältere Nachrichten eingeblendet. Bei einer E-Mail ist der Rest des Threads darüber und darunter eingeklappt.

Eine Nachricht wird auch aus der Suche, dem Graph, den Antworten von Ask oder der letzten Prüfung auf dieselbe Weise geöffnet und mit „Diese Nachricht“ oder „Neue Nachrichten“ markiert.

**In Gmail öffnen** öffnet die E-Mail in dem Gmail-Konto, an das sie gesendet wurde. Auf Android wird sie in der Gmail-App geöffnet, sofern du diese installiert hast.

Unter **Details** einer E-Mail stehen nur Informationen, die nicht schon in der Kopfzeile zu sehen sind, zum Beispiel vollständige Cc-Adressen, Bcc oder eine andere Antwortadresse. Gibt es nichts hinzuzufügen, wird auch nichts angezeigt.

Bei einer Antwort in einem Slack-Thread wird auch angezeigt, was vor dem Start des Threads geschrieben wurde. Über den Link der Aufgabe zur zugehörigen Nachricht kannst du diese ebenfalls hier öffnen. Unten findest du **In Slack öffnen**.

Unter **Details** stehen der Name, das Projekt und der Bereich der Aufgabe (tippe auf einen Eintrag, um ihn zu ändern), deine letzte Notiz und das Ergebnis eines Coding-Agenten. Über den Titel öffnest du den Chat. Eine erledigte Aufgabe bleibt kurz. Die Nachricht, aus der sie entstanden ist, steht unter **Details**.

Bei einer Aufgabe mit „Wartet auf“ führt der Link zu deiner letzten Nachricht an die Person, auf deren Antwort du wartest: „E-Mail an Pat · Di“.

## Selbst eine Aufgabe erstellen

Mit **Neue Aufgabe** (unter **Suchen** auf dem Computer, über **+** auf dem Handy oder mit `N`) kannst du eine Aufgabe zu jedem Thema erstellen. Beim Erstellen wird nichts gesendet. Wenn du weder **Arbeit** noch **Privat** auswählst, wird die Aufgabe dem passenden Bereich zugeordnet, je nachdem, um wen und was es geht. Außerdem findet sie die E-Mail, zu der sie gehört, auch ältere E-Mails.

Wenn du die Aufgabe schließt, bevor du sie hinzugefügt hast, bleiben dein Text und deine Auswahl für das nächste Mal erhalten, nicht aber Dateien. Mit **Verwerfen** in der Nachricht werden sie entfernt.

- **Fällig**: Gib einen Tag oder Zeitpunkt ein, zum Beispiel „morgen“, „nächsten Fr“, „3. Nov.“, „14 Uhr“ oder „in 2 Stunden“. Das geht auch in deiner Sprache. Das Kalendersymbol bietet Schnellauswahl und **Datum wählen**.
- **Wiederholt sich**: Die Aufgabe kommt regelmäßig wieder. Siehe [Wiederkehrende Aufgaben](recurring.md).
- **Person**: Verknüpfe bis zu 5 Personen oder Unternehmen, um die es geht.
- Nachrichtensymbol: Füge die Nachricht hinzu, auf die sich die Aufgabe bezieht. Das kann eine E-Mail, Slack-, Teams-, WhatsApp-, Telegram- oder jede andere Nachricht sein, auf die The Machine zugreifen kann. Suche nach Text oder Absender. Bei jedem Treffer siehst du, woher er stammt, wer ihn gesendet hat und wann.
- **Dateien**: Tippe auf die Büroklammer, füge einen Screenshot ein oder ziehe Dateien auf das Formular. Auf dem Handy kannst du mit der Kamera daneben ein Foto aufnehmen. Bis zu 5 Dateien, wie im Chat (siehe [Dateien hinzufügen](card-chat.md#add-files)). Mit × entfernst du eine Datei wieder.

Die Dateien bleiben bei der Aufgabe und werden von The Machine gelesen, wenn sie daran arbeitet. Auch Dateien allein genügen: The Machine erstellt die Aufgabe aus einer PDF- oder Textdatei. Ein Foto wird als kleines Bild angezeigt. Tippe darauf, um es in voller Größe anzusehen.
