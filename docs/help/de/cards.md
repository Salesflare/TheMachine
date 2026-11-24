---
title: Aufgaben
area: cards
summary: Eine Aufgabe pro Sache, die dich braucht und auf dein Ja wartet. Was die einzelnen Teile einer Aufgabe bedeuten.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: f77d6b07f6f94ce5
---
Deine Machine liest alles Neue und erstellt nur dann eine Aufgabe, wenn etwas dich braucht. Pro Thema eine Aufgabe, egal über wie viele Nachrichten es sich erstreckt.

## Wo Aufgaben zu finden sind

Auf der Seite **Aufgaben** sind sie gruppiert:

- **Gerade erledigt**: Ganz oben siehst du einen letzten Schritt, den du bestätigt hast, etwa ein Formular oder ein Problem. Er wurde abgeschlossen, während du weg warst. Er bleibt höchstens einen Tag lang dort, bis du auf **Verstanden** tippst. Auch auf deinem Handy wird er angezeigt.
- **Für dich**: Alles, was auf dich wartet. Was bis morgen fällig ist, steht zuerst. Bei jeder Aufgabe steht **Vorbereitet** (ein Entwurf oder Ergebnis ist fertig, und mit **Ausführen** oder **Senden** wird es umgesetzt), **Braucht dich** (zuerst ist deine Entscheidung oder Antwort nötig; wenn die Arbeit ohne etwas, das nur du weißt, nicht weitergehen oder verwendet werden kann, etwa ohne Preis, Fakt oder Auswahl, steht unter dem Titel, was fehlt), **Wird vorbereitet…** (deine Machine arbeitet daran) oder **Zum Lesen** (eine Zusammenfassung oder ein Briefing, bei dem nichts entschieden werden muss).
- **Älter**: Eingeklappte Aufgaben, zu denen es seit einer Woche nichts Neues gibt (siehe unten).
- **Wartet auf andere**: Eingeklappte Aufgaben, bei denen jemand anderes am Zug ist (siehe unten).
- **Kommt später zurück**: Zurückgestellte Aufgaben, Nachrichten, die [später gesendet werden](send-later.md), und Aufgaben ohne Antwort auf **Noch nötig?** (siehe unten).
- **Versprechen**: Was du versprochen hast und was andere dir versprochen haben. Mehr dazu unter [Versprechen](promises.md).
- **Erledigt / verworfen**: Alle abgeschlossenen Aufgaben, die neuesten zuerst, mit dem Zeitpunkt ihres Abschlusses, zum Beispiel „Vor 5 Minuten erledigt“. Aufgaben, die offenbar schon erledigt sind, sind mit **Sieht erledigt aus** markiert.

Nach dem Senden steht kurz, wohin die Aufgabe verschoben wurde, zum Beispiel „Gesendet. Nach Erledigt verschoben.“ oder „Gesendet. Bis Mo. nach Später verschoben.“ Eine Antwort, die nur verspricht, etwas zu erledigen, etwa „Ich schicke es bis Dienstag“, lässt die Aufgabe offen: „Gesendet. Offen gelassen.“ Mit **Öffnen** gelangst du zur Aufgabe. Über die Suche findest du Aufgaben anhand ihres Titels oder danach, an wen sie gingen. Auch in Später und Erledigt wird gesucht.

Unter **Für dich** stehen zuerst überfällige oder bis morgen fällige Aufgaben, dann Fragen aus deinem Fleet, dann Nachfassnachrichten aus einem Board und schließlich der Rest. Innerhalb jeder Gruppe stehen die neuesten zuerst. Eine Aufgabe behält ihren Platz, während deine Machine sie vorbereitet und nachdem sie erledigt ist. Nur ihre Markierung ändert sich. In den anderen offenen Gruppen stehen überfällige oder bis morgen fällige Aufgaben zuerst, der Rest ist nach Aktualität sortiert. In der Seitenleiste bleibt die Reihenfolge gleich.

**Sieht erledigt aus** bedeutet, dass deine Machine erkennt, dass etwas erledigt ist, zum Beispiel „PR #3451 zusammengeführt“, die Aufgabe aber noch nicht geschlossen wurde. Mit **Wieder öffnen** kommt sie zurück auf deine Liste, und deine Machine lernt daraus. Diese Aufgaben werden nie als verspätet angezeigt. Wenn eine Nachricht den Abschluss zeigt, wird die Aufgabe nach einem Tag automatisch geschlossen. Du kannst das mit **Rückgängig** rückgängig machen. Andernfalls wartet die Aufgabe auf **Als erledigt markieren**.

Eine Aufgabe, die du selbst schon erledigt hast, etwa mit einer Antwort in Gmail oder Slack, wird ebenfalls automatisch geschlossen. Eine Antwort, die behauptet, eine Datei sei angehängt, obwohl keine dabei ist, schließt die Aufgabe nicht.

Wenn eine Nachricht von einer Adresse kommt, die nur wie die einer Person aussieht, die du kennst, etwa sam@acme-corp.example statt sam@acmecorp.example, steht das deutlich bei der Aufgabe: „Das ist nicht Sam Lee.“ Die Person wird mit ihrer tatsächlichen Adresse angezeigt, nie mit dem Namen, den sie verwendet hat. Deine Machine prüft solche Nachrichten bei der Person unter der Adresse, die du bereits hast, niemals bei der schreibenden Person.

Bei einer Aufgabe, die noch auf jemand anderen wartet, etwa auf eine Prüfung oder Antwort, steht **Wartet auf:** und der ausstehende Schritt. Sie bleibt eingeklappt unter **Wartet auf andere**, oberhalb von Kommt später zurück, bis eine neue Nachricht sie wieder hervorholt. Das gilt auch, wenn du eine Rückfrage gestellt hast: Die Aufgabe kommt am Morgen vor dem Abgabetermin zurück, am Abgabetermin, wenn er noch heute ist, oder am nächsten Morgen, wenn er schon verstrichen ist. Dabei steht, auf wen sie noch wartet.

Wenn es bei einer Aufgabe um ein Ergebnis geht, das jemand anderes liefern soll, etwa einen unterschriebenen Vertrag, wird es unter **Details** bei **Fertig, wenn** angezeigt. Wenn du deinen Teil sendest, wird die Aufgabe nicht geschlossen. Sie bleibt unter **Wartet auf andere**, bis eine Nachricht das Ergebnis zeigt. Dann wird sie automatisch geschlossen. Du kannst das mit **Rückgängig** rückgängig machen. Wenn bis zum Zeitpunkt, an dem du nachhaken solltest, nichts eingetroffen ist, kommt die Aufgabe mit **Schreib eine kurze Erinnerung** in ihrem Chat zurück. Schreib im Chat, was als erledigt gilt, um das zu ändern.

Eine Aufgabe, zu der es eine Woche lang nichts Neues gibt, wird von Für dich nach **Älter** verschoben. So stehen nach ein paar Tagen Abwesenheit die neuen Aufgaben zuerst. Als neu gilt eine Nachricht zur Aufgabe oder etwas, das du damit gemacht hast, etwa eine Chatnachricht, eine Bearbeitung oder ein Zurückstellen. Nur die Aufgabe anzusehen zählt nicht.

Dringende Aufgaben, bald fällige Aufgaben und Aufgaben mit einer ausstehenden Sendung bleiben unter Für dich. Mit **Alle verwerfen** kannst du nach einer Bestätigung alle Aufgaben unter Älter als nicht nötig markieren. Das entspricht **Nicht nötig** für einzelne Aufgaben. Du kannst es mit **Rückgängig** rückgängig machen. Gibt es etwas Neues zu einer Aufgabe, kommt sie zurück zu Für dich.

Bei einer Aufgabe, die eine Woche lang niemand angefasst hat, erscheint einmal die Frage **Noch nötig?** Mit **Nicht nötig** wird sie geschlossen. Du kannst es mit **Rückgängig** rückgängig machen. **Behalten** lässt sie offen, und die Frage wird nie wieder gestellt. Gibt es eine weitere Woche lang keine Antwort, wird die Aufgabe unter Kommt später zurück eingeklappt. Sie wird dann nicht mehr auf dem App-Symbol und in der morgendlichen Zusammenfassung mitgezählt. Wenn du sie öffnest, eine Chatnachricht schreibst, sie bearbeitest, zurückstellst oder eine neue Nachricht eintrifft, kommt sie wieder zurück.

Ein Projekt, zu dem es ruhiger geworden ist und bei dem keine Aufgabe offen ist, kann einmal pro Woche eine Aufgabe mit einem konkreten nächsten Schritt bekommen, höchstens drei pro Woche. Mehr dazu unter [Projekte](projects.md).

Wenn dich nichts braucht, macht deine Machine ein Nickerchen und zeigt eine leere Liste. Während sie etwas prüft, wird sie wach und sagt Bescheid. Wenn eine Prüfung fehlgeschlagen oder verspätet ist, steht das in der Zeile. Darunter findest du **Jetzt prüfen**.

Mit **Alle**, **Arbeit** und **Privat** oben in der Seitenleiste kannst du alle Aufgaben oder nur eine Kategorie anzeigen. Auf deinem Handy und Computer gilt dieselbe Auswahl. Wenn Arbeit oder Privat ausgewählt ist, führt **Alle anzeigen** zurück zur Gesamtansicht. Ein Hinweis zu deiner Machine selbst, etwa dass ein Teil immer wieder neu startet, gehört weder zu Arbeit noch zu Privat und wird nur unter Alle angezeigt.

Mit der Zeile oben in der Liste kannst du auch direkt zur anderen Ansicht wechseln: Unter **Nur privat** tippst du auf **Arbeit** oder **Alle anzeigen**.

Die Zeile oben in der Liste nennt deine letzte morgendliche oder abendliche Zusammenfassung und was darin gezählt wurde, zum Beispiel **Zusammenfassung von gestern Abend** · 12 erledigt, 3 offen. Tippe darauf, um die Zusammenfassung noch einmal zu lesen. Mit **Kopieren** kannst du sie an beliebiger Stelle einfügen. Sobald du sie öffnest oder auf ihr **×** tippst, ist sie auf all deinen Geräten verfügbar, bis die nächste Zusammenfassung kommt.

Ohne aktuelle Zusammenfassung wird **Heute bisher** angezeigt: Was heute erledigt wurde und was noch offen ist, für Arbeit und Privat oder nur für die ausgewählte Kategorie.

Bei einer Aufgabe zu einem Projekt steht der Projektname unter dem Titel. Tippe darauf, um das Projekt zu öffnen. Unter **Details** kannst du mit **Projekt** das Projekt ändern oder entfernen. Mehr dazu unter [Aufgaben eines Projekts](projects.md#a-project-s-to-dos).

Mit **Bereich** unter **Details** verschiebst du eine Aufgabe in deinen anderen Bereich. Was sie lesen und senden darf, wird mitverschoben. Mit **Rückgängig** in der Bestätigung verschiebst du sie zurück.

Wenn eine Aufgabe deinen anderen Bereich braucht, um weiterzugehen, und alle Nachrichten, auf denen sie beruht, dort sind, wird sie automatisch dorthin verschoben und fortgesetzt. Andernfalls wird **Nach Arbeit verschieben** angezeigt, und erst wenn du darauf tippst, wird etwas verschoben. Eine Aufgabe, die du hinzugefügt hast, ohne Arbeit oder Privat auszuwählen, wird automatisch verschoben, sobald klar ist, wohin sie gehört. Bis dahin ist sie weder Arbeit noch Privat zugeordnet und bleibt privat.

Eine Aufgabe kann immer die Nachrichten lesen, aus denen sie entstanden ist. Wenn sie weitere Nachrichten aus deinem anderen Bereich braucht, fragt sie mit **Diese E-Mail für diese Aufgabe verwenden** danach. Ein Arbeits-Postfach, das du als Privat gekennzeichnet hast, zählt als Privat. E-Mails für eine andere deiner Firmen gehen an die Aufgaben dieser Firma. Bei einer Aufgabe zu deinem Privatleben, etwa wenn deine Familie an deine Arbeitsadresse schreibt, gilt sie von Anfang an als privat.

Arbeit, die dich über ein privates Konto erreicht, etwa von einem Kunden auf WhatsApp, eine Bestellung in deinem privaten Postfach oder ein [Versprechen](promises.md) zu einer Arbeitssache, gilt von Anfang an als Arbeit.

Eine Aufgabe, die du selbst verschoben oder zugeordnet hast, bleibt immer dort, wo du sie abgelegt hast. Arbeit oder Privat bestimmt, wo eine Aufgabe angezeigt und mit wem sie geteilt wird, aber nie, wohin sie antwortet. Eine Antwort geht immer dorthin, wo das Gespräch stattfindet, auch nach einer Verschiebung, sofern du keinen anderen Weg auswählst.

Eine solche private Aufgabe antwortet weiterhin von der Arbeitsadresse aus, an die ihre E-Mail geschickt wurde. Sie erscheint nie in einem Work Fleet oder im Team Graph.

Wenn mindestens zwei Aufgaben auf dich warten, kannst du mit **Durchgehen** in der Kopfzeile von Für dich nacheinander durch sie gehen, in der Reihenfolge der Liste. Jede Aufgabe wird vollständig mit ihrem Entwurf angezeigt. Zur Auswahl stehen **Senden** oder **Ausführen**, **Änderungen anfragen**, **Zurückstellen** und **Überspringen**. Auf einem Computer sendet Enter den Inhalt auf dem Bildschirm, `S` stellt zurück, `→` überspringt, und Esc beendet den Ablauf. In der Kopfzeile steht, wie lange es in deinem Tempo dauert, zum Beispiel „etwa 2 Min.“

Am Ende wird gezählt, was gesendet oder geschlossen wurde und was noch vorbereitet wird.

Eine Aufgabe, die dir eine Frage stellt, wird dabei ausgelassen: Sie braucht deine Antwort, nicht einen Fingertipp.

## Jetzt prüfen

Deine Machine liest jede Quelle alle paar Minuten, tagsüber und nachts. Sie prüft neu eingegangene Nachrichten, sobald 40 davon warten oder die älteste Nachricht einer Person seit 15 Minuten wartet. Newsletter, Benachrichtigungen und Belege werden bei der nächsten Prüfung berücksichtigt, spätestens innerhalb einer Stunde.

Nachts, von 00:00 bis 06:30, pausieren die Prüfungen. Neue Nachrichten werden weiterhin gelesen und gespeichert und um 06:30 gemeinsam geprüft, damit deine Aufgaben vor der morgendlichen Zusammenfassung bereit sind. Unter Verbindungen steht bei Prüfungen: „Nachts pausiert, holt um 06:30 auf“. Wenn du nachts in der App klickst, tippst oder scrollst, im Chat schreibst oder eine Aufgabe antippst, laufen die Prüfungen wie gewohnt weiter, bis du eine Stunde lang weg warst. Mit **Jetzt prüfen** wird immer sofort geprüft.

Mit **Jetzt prüfen** werden alle Quellen sofort gelesen. Wenn keine Aufgabe offen ist, tippe auf die Zeile deiner Machine, um sie mit **Details** zu sehen. Dadurch werden die Prüfungen unter Verbindungen geöffnet. Wenn Aufgaben offen sind, steht die Zeile auf dem Computer ganz oben. Eine kurze Zeile wird dort nur angezeigt, während eine Prüfung läuft oder wenn sie fehlgeschlagen oder verspätet ist. Du kannst auch im Chat danach fragen.

LinkedIn, X und Salesflare haben ihren eigenen Rhythmus.

## Letzte Prüfung

Nach einer Prüfung, bei der neue Nachrichten gelesen wurden, steht über deinen Aufgaben, was gefunden wurde und aus welchen Quellen, zum Beispiel „13 Nachrichten um 16:11 geprüft · keine neue Aufgabe“ oder „· 2 neue Aufgaben“. Die Meldung bezieht sich nur auf diese Prüfung. Aufgaben, die bereits auf deiner Liste stehen, bleiben unverändert. Wenn eine neue Aufgabe bis zu einem besseren Zeitpunkt, etwa deiner morgendlichen Zusammenfassung, zurückgehalten wird, steht dabei, bis wann: „1 Aufgabe bis morgen 08:30 zurückgehalten“.

Tippe auf die Zeile, um die einzelnen E-Mail-Threads, Chats und Benachrichtigungen mit dem Symbol der jeweiligen Quelle zu sehen: wer geschrieben hat, den Betreff oder die ersten Wörter und die neue Aufgabe oder den Grund, warum keine nötig war, etwa „Nur in Cc, ein Teammitglied antwortet“ oder „Termin für Donnerstag steht schon“. Wenn bei einer Nachricht nur ein vager Grund für die Prüfung angegeben wurde, wird kein Grund angezeigt. Tippe auf eine Nachricht, um sie zusammen mit dem Gesprächsverlauf zu lesen.

Die ersten 10 werden angezeigt. Tippe darunter, um den Rest zu sehen. Eine Zahl hinter einem Namen, etwa (3), gibt an, wie viele neue Nachrichten dieser Chat enthält. Eine Handybenachrichtigung zu einer Nachricht, die bereits in der Liste steht, wird nur einmal angezeigt. Die Zeile bleibt 12 Stunden nach der Prüfung sichtbar.

Gezählt werden nur E-Mails an dich. Deine eigenen Antworten werden als Kontext und für Versprechen gelesen, zählen aber nicht als neue E-Mails. Die eigenen E-Mails von The Machine an dich, etwa deine morgendliche Zusammenfassung oder ein Hinweis zu einer Korrektur, werden nie gelesen oder aufgelistet. E-Mails zur Abrechnung, deiner Testphase oder einer Einladung werden wie gewohnt gelesen.

## Die Schaltflächen

Bei einer Aufgabe wird der nächste Schritt angezeigt, etwa **Ausführen** oder **Prüfen und senden**, daneben **Zurückstellen**. Mehr dazu unter [Ausführen](do-it.md) und [Zurückstellen](snooze.md).

Mit **Änderungen anfragen** kannst du angeben, was geändert werden soll: wie die Aufgabe erledigt werden soll oder, sobald ein Entwurf fertig ist, was daran geändert werden soll. Wenn du den Text nur teilweise eingibst, ist er noch da, wenn du zurückkommst. Mit **Abbrechen** wird er verworfen.

**Als erledigt markieren** bedeutet, dass die Aufgabe erledigt ist. Die Schaltfläche wird bei einer bereiten Aufgabe ohne Entwurf oder bei einer Aufgabe, die dir eine Frage stellt, direkt angezeigt. Sonst findest du sie oben unter **…**. Die Aufgabe wird sofort aus der Liste entfernt. In der Nachricht kannst du das mit **Rückgängig** rückgängig machen. Wische die Nachricht weg oder ziehe sie mit der Maus aus der Liste, um sie schneller zu schließen. Die Änderung bleibt bestehen.

Wenn die Aufgabe auf andere Weise erledigt werden soll, sag es im **Chat**. In der Antwort steht nur, was geändert wurde, zum Beispiel eine Zurückstellung und bis wann. Wenn etwas nicht geändert werden konnte, etwa ein Fälligkeitsdatum, steht das ebenfalls dort.

Unter **…**:

- **Übergeben…**: Weise die Aufgabe einem Teammitglied oder [Claude Code oder Codex](hand-to-agent.md) zu, oder [bitte jemanden um eine Prüfung](ask-to-review.md).
- **Wiederholen…**: Die Aufgabe [kommt in einem bestimmten Rhythmus zurück](recurring.md).
- **Nicht nötig**: Die Aufgabe wird entfernt. Optional kannst du einen Grund auswählen: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Tippe auf den Titel oder unter **Details** auf **Name**, um die Aufgabe umzubenennen. Du kannst auch im Chat darum bitten, zum Beispiel mit „Benenne sie in … um“. Dein Titel bleibt erhalten.

Mit **Wieder öffnen** holst du eine geschlossene Aufgabe zurück. Sie kommt auch von selbst zurück, wenn etwas Neues passiert, etwa eine neue Nachricht von der betreffenden Person, aber nicht bei deiner eigenen Antwort. Dann wird angezeigt, wann sie zurückkam, und sie wird wie eine neue Aufgabe sortiert. Der Chat wird dort fortgesetzt, wo er aufgehört hat, auch nach mehreren Wochen.

Eine Rechnung, die du selbst noch bezahlen musst, wird unabhängig vom Land zu einer Aufgabe mit dem Betrag, dem Fälligkeitsdatum und den Zahlungsangaben auf der Rechnung. Rechnungen, die automatisch bezahlt werden, etwa per Lastschrift oder gespeicherter Karte, werden nicht hinzugefügt. Wenn eine spätere E-Mail zeigt, dass die Rechnung bezahlt wurde, zum Beispiel eine Bestätigung des Zahlungseingangs vom Absender, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du sie innerhalb eines Tages zurückholen.

Eine Aufgabe, die nur bis zu einem bestimmten Zeitpunkt wichtig war, etwa eine Bestätigung vor einem Meeting, wird nach diesem Zeitpunkt automatisch geschlossen. Sie wird unter **Erledigt / verworfen** als „Nicht mehr nötig“ angezeigt. Mit **Rückgängig** kannst du sie innerhalb eines Tages zurückholen.

Bevor eine Nachricht oder Übergabe für jemanden als bereit angezeigt wird, prüft deine Machine deine letzten Chats mit den beteiligten Personen, einschließlich Gruppenchats, und wartet darauf, dass Slack sie gelesen hat. Wenn eine spätere Nachricht zeigt, dass die Sache bereits erledigt ist, etwa weil die Person gefragt wurde und zugestimmt hat, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du sie innerhalb eines Tages zurückholen.

Wenn jemand anderes nach der Erstellung deines Entwurfs in derselben Unterhaltung geschrieben hat, wird der Entwurf beim Senden zurückgehalten: „Nicht gesendet: neue Nachricht im Thread“. Bei der Aufgabe wird diese Nachricht mit **Lesen** und **Für diese Nachricht neu machen** angezeigt. Drücke noch einmal auf **Senden**, um deinen Entwurf unverändert zu senden.

Wenn eine neuere Nachricht den Plan ändert, etwa wenn eine Feier an einen anderen Ort verlegt oder eine Buchung storniert wird, aktualisiert The Machine ihre Aufgaben selbst. Eine weiterhin relevante Aufgabe folgt dem neuen Plan. Wenn nichts mehr zu tun ist, wird sie unter **Erledigt / verworfen** als „Nicht nötig“ angezeigt. Im Chat steht „Aktualisiert:“ mit dem Grund. Mit **Rückgängig** kannst du sie innerhalb eines Tages zurückholen.

Bei deinen ersten Aufgaben wird ein kurzer Tipp mit den wichtigsten Aktionen angezeigt: **Änderungen anfragen** und **Nicht nötig**. Außerdem erfährst du, dass erst etwas gesendet wird, wenn du auf **Senden** drückst. Der Tipp verschwindet endgültig, sobald du die Schaltfläche verwendest oder auf × drückst.

An deinem ersten Tag begrüßt dich The Machine oben unter Aufgaben und nennt die Person, die schon am längsten auf deine Antwort wartet. Diese Antwort wird zuerst vorbereitet, damit sie bei deiner Ankunft bereit ist.

Jede Aufgabe beginnt mit ihrem Titel. In der Zeile darunter stehen, um wen es geht, die Organisation, wenn es um eine Organisation geht, der Name des Projekts, Arbeit oder Privat und der Eingangszeitpunkt. Die Organisation wird nicht allein deshalb genannt, weil dort jemand arbeitet. Tippe auf einen Namen, um die Seite der Person im Graph zu öffnen.

Bei einem Namen oder einer Organisation wird das Foto oder Logo angezeigt, falls es im Graph vorhanden ist. Andernfalls werden die Initialen angezeigt. Ein Logo, das in dieser Größe nicht lesbar wäre, etwa weiße Schrift auf transparentem Hintergrund oder ein breites Wortzeichen, wird ebenfalls durch die Initialen ersetzt.

Manchmal steht in einer unaufdringlichen Zeile, was nicht bekannt ist, etwa „Letzter Kontakt vor 12 Tagen per E-Mail, seitdem nichts“. Sie wird angezeigt, wenn die letzte Nachricht an die Person schon länger zurückliegt oder unbeantwortet ist. Außerdem werden nicht verbundene Kanäle genannt, etwa WhatsApp. Deine Machine sagt, was sie nicht weiß, statt zu raten.

Wenn ein nicht verbundener Kanal genannt wird, öffnet **Verbinden** daneben die entsprechende Verbindung.

Der Titel nennt die nötige Aufgabe und ändert sich nur, wenn sich diese ändert. Eine erledigte Aufgabe behält ihren Titel. Darunter steht, wie sie abgeschlossen wurde, etwa „Erledigt: Sam hat am Dienstag unterschrieben“.

Über dem Entwurf steht in einer blasseren Zeile, aus welcher Nachricht er stammt, samt Logo des jeweiligen Dienstes. Tippe darauf, um den Thread zu lesen. Der Entwurf zeigt das Logo des Dienstes, an den er gesendet wird. So siehst du sofort, ob es eine Slack-Antwort oder eine E-Mail ist.

Wenn ein Entwurf auf einer Eingabe an anderer Stelle beruht, etwa einem Vorschlag eines Teammitglieds in Slack, steht das in einer Zeile, zum Beispiel „Basierend auf Sam in #ops“. Tippe darauf, um die Nachricht zu lesen. Der Hinweis verschwindet, wenn eine Aktualisierung den Entwurf ersetzt.

Ein Chat, etwa in Slack, WhatsApp, Telegram oder Intercom, wird als eine Unterhaltung angezeigt, von der ältesten Nachricht an: zuerst die Nachrichten vor der Nachricht, um die es bei der Aufgabe geht, dann die Antworten darauf. In WhatsApp, Telegram oder Signal stehen deine Nachrichten wie in der App rechts. Die Nachricht zur Aufgabe ist mit „Diese Aufgabe“ markiert und wird in der Ansicht geöffnet. Mit **Frühere Nachrichten anzeigen** kommen ältere Nachrichten dazu. Bei einer E-Mail werden die übrigen Nachrichten des Threads oberhalb und unterhalb eingeklappt angezeigt.

Eine Nachricht wird in der Suche, im Graph, in den Antworten von Ask oder bei der letzten Prüfung genauso geöffnet. Sie ist mit „Diese Nachricht“ oder „Neue Nachrichten“ markiert.

Mit **In Gmail öffnen** wird die E-Mail in dem Gmail-Konto geöffnet, in dem sie eingegangen ist. Auf Android wird sie in der Gmail-App geöffnet, sofern sie installiert ist.

Unter **Details** einer E-Mail stehen nur Angaben, die nicht schon in der Kopfzeile enthalten sind, etwa vollständige Cc-Adressen, Bcc oder eine abweichende Antwortadresse. Gibt es nichts hinzuzufügen, werden keine Details angezeigt.

Bei einer Antwort in einem Slack-Thread wird auch angezeigt, was vor dem Thread gesagt wurde. Über den Link einer Aufgabe zur zugehörigen Nachricht kannst du sie ebenfalls hier öffnen. Unten findest du **In Slack öffnen**.

Unter **Details** stehen Name, Projekt und Bereich. Tippe auf einen Eintrag, um ihn zu ändern. Außerdem siehst du deine letzte Notiz und das Ergebnis eines Coding-Agenten. Über den Titel wird der Chat geöffnet. Eine erledigte Aufgabe bleibt kurz. Die Nachricht, aus der sie entstanden ist, steht unter **Details**.

Bei einer Aufgabe mit „Wartet auf“ ist deine letzte Nachricht an die Person verlinkt, auf deren Antwort du wartest: „E-Mail an Pat · Di“.

## Aufgabe selbst erstellen

Mit **Neue Aufgabe** kannst du alles als Aufgabe hinzufügen. Auf einem Computer findest du die Option unter **Suchen**, auf einem Handy über **+** oder mit `N`. Beim Erstellen wird nichts gesendet. Wenn du weder **Arbeit** noch **Privat** auswählst, landet die Aufgabe abhängig davon, um wen oder was es geht, im passenden Bereich. Die passende E-Mail, auf die sich die Aufgabe bezieht, wird ebenfalls gefunden, auch wenn sie schon älter ist.

Wenn du die Aufgabe vor dem Hinzufügen schließt, bleiben dein Text und deine Auswahl für das nächste Mal erhalten, Dateien jedoch nicht. Mit **Verwerfen** in der Nachricht werden sie gelöscht.

- **Fällig**: Gib einen Tag oder eine Uhrzeit ein, etwa „morgen“, „nächsten Fr“, „3 Nov“, „14 Uhr“ oder „in 2 Stunden“. Du kannst auch deine eigene Sprache verwenden. Über das Kalendersymbol findest du Schnelloptionen und **Datum wählen**.
- **Wiederholt sich**: Die Aufgabe kommt in einem bestimmten Rhythmus zurück. Mehr dazu unter [Wiederkehrende Aufgaben](recurring.md).
- **Person**: Verknüpfe die Personen oder Firmen, um die es geht, bis zu 5.
- Nachrichtensymbol: Hänge die betreffende Nachricht an, etwa eine E-Mail, Slack-, Teams-, WhatsApp-, Telegram- oder andere Nachricht, auf die The Machine zugreifen kann. Suche nach Text oder Absender. Bei jedem Treffer siehst du, woher er stammt, wer ihn gesendet hat und wann.
- **Dateien**: Tippe auf die Büroklammer, füge einen Screenshot ein oder ziehe Dateien auf das Formular. Auf einem Handy kannst du mit der Kamera daneben ein Foto machen. Wie im Chat sind bis zu 5 Dateien möglich. Mehr dazu unter [Dateien hinzufügen](card-chat.md#add-files). Mit × entfernst du eine Datei.

Die Dateien bleiben bei der Aufgabe, und The Machine liest sie, wenn sie daran arbeitet. Dateien allein reichen: Aus einer PDF- oder Textdatei erstellt The Machine die Aufgabe. Ein Foto wird als kleines Bild angezeigt. Tippe darauf, um es in voller Größe zu sehen.
