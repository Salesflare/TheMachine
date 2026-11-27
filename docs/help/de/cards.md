---
title: Aufgaben
area: cards
summary: Eine Aufgabe für jedes Anliegen, bei dem du gefragt bist, bereit für dein Ja. Was die einzelnen Teile einer Aufgabe bedeuten.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: b218e3423a2162c5
---
Deine Machine liest alles Neue und erstellt nur dann eine Aufgabe, wenn etwas deine Aufmerksamkeit braucht. Eine Aufgabe pro Anliegen, egal über wie viele Nachrichten es sich erstreckt.

## Wo Aufgaben zu finden sind

Auf der Seite **Aufgaben** sind sie gruppiert:

- **Gerade erledigt**: Oben wird angezeigt, wenn ein letzter Schritt, den du bestätigt hast, etwa ein Formular oder ein Problem, in deiner Abwesenheit ausgeführt wurde. Er bleibt höchstens einen Tag lang angezeigt, bis du auf **Verstanden** tippst. Du bekommst dazu auch eine Nachricht auf deinem Handy.
- **Für dich**: Alles, worauf du noch reagieren musst. Was bis morgen fällig ist, steht zuerst. Bei jeder Aufgabe steht **Vorbereitet** (ein Entwurf oder Ergebnis ist bereit. Mit **Ausführen** oder **Senden** wird es umgesetzt), **Braucht dich** (du musst zuerst eine Entscheidung treffen oder antworten; wenn die Arbeit ohne etwas, das nur du liefern kannst, nicht weitergehen oder genutzt werden kann, etwa einen Preis, eine Information oder eine Entscheidung, steht unter dem Titel, was fehlt), **Wird vorbereitet…** (deine Machine arbeitet daran) oder **Zum Lesen** (eine Zusammenfassung oder ein Briefing, bei dem nichts entschieden werden muss).
- **Älter**: Eingeklappte Aufgaben, bei denen es seit einer Woche nichts Neues gibt (siehe unten).
- **Wartet auf andere**: Eingeklappte Aufgaben, bei denen der nächste Schritt bei jemand anderem liegt (siehe unten).
- **Kommt später zurück**: Zurückgestellte Aufgaben, Nachrichten, die [später gesendet werden](send-later.md), und Aufgaben ohne Antwort auf **Noch nötig?** (siehe unten).
- **Versprechen**: Was du versprochen hast und was andere dir versprochen haben. Mehr dazu unter [Versprechen](promises.md).
- **Erledigt / verworfen**: Alle erledigten Aufgaben, neueste zuerst, mit dem Zeitpunkt, zu dem sie erledigt wurden, etwa „Vor 5 Minuten erledigt“. Aufgaben, die bereits erledigt zu sein scheinen, sind mit **Sieht erledigt aus** markiert.

Nachdem du etwas gesendet hast, steht in einer kurzen Notiz, wohin die Aufgabe verschoben wurde, etwa „Gesendet. Nach Erledigt verschoben.“ oder „Gesendet. Bis Mo. auf Später verschoben.“ Wenn eine Antwort nur verspricht, die Arbeit zu erledigen, etwa „Ich schicke es bis Dienstag“, bleibt die Aufgabe offen: „Gesendet. Offen gelassen.“ Mit **Öffnen** gelangst du zur Aufgabe. Über die Suche findest du Aufgaben anhand ihres Titels oder der Person, an die sie gingen, auch unter Später und Erledigt.

Unter **Für dich** stehen zuerst überfällige oder bis morgen fällige Aufgaben, dann Fragen aus deiner Fleet, danach Nachfassaktionen eines Boards und schließlich alles andere. Innerhalb jeder Gruppe stehen die neuesten zuerst. Eine Aufgabe behält ihren Platz, während deine Machine sie vorbereitet und wenn sie erledigt ist. Nur ihre Markierung ändert sich. In den anderen offenen Gruppen stehen überfällige oder bis morgen fällige Aufgaben zuerst, danach die neuesten. Die Seitenleiste behält dieselbe Reihenfolge bei.

**Sieht erledigt aus** bedeutet, dass deine Machine erkennt, dass etwas erledigt ist, etwa „PR #3451 zusammengeführt“, die Aufgabe aber noch nicht geschlossen wurde. Mit **Wieder öffnen** kommt sie zurück auf deine Liste. Deine Machine lernt daraus. Solche Aufgaben werden nie als überfällig angezeigt. Wenn sie in einer Nachricht auftauchen, werden sie nach einem Tag automatisch geschlossen. Dabei kannst du mit **Rückgängig** noch etwas ändern. Andernfalls warten sie auf **Als erledigt markieren**.

Eine Aufgabe wird auch automatisch geschlossen, wenn du sie bereits selbst erledigt hast, zum Beispiel durch eine Antwort in Gmail oder Slack. Eine Antwort, in der steht, dass eine Datei angehängt ist, obwohl keine angehängt wurde, schließt die Aufgabe nicht.

Wenn eine Nachricht von einer Adresse kommt, die nur wie die einer Person aussieht, die du kennst, etwa sam@acme-corp.example statt sam@acmecorp.example, wird bei der Aufgabe klar darauf hingewiesen: „Das ist nicht Sam Lee.“ Die Person wird mit ihrer eigenen Adresse angezeigt, niemals mit dem Namen, den sie verwendet hat. Deine Machine prüft solche Nachrichten mit der Person unter der Adresse, die du bereits hast, niemals mit der Person, die geschrieben hat.

Bei einer Aufgabe, die noch auf jemand anderen wartet, etwa auf eine Prüfung oder Antwort, steht der nächste Schritt unter **Wartet auf**. Sie bleibt eingeklappt unter **Wartet auf andere**, oberhalb von „Kommt später zurück“, bis eine neue Nachricht sie wieder hervorholt. Dasselbe gilt, wenn du eine Rückfrage gestellt hast: Die Aufgabe kommt am Morgen vor dem Abgabetermin zurück, am Abgabetermin, wenn dieser noch heute ist, oder am nächsten Morgen, sobald er verstrichen ist. Dabei steht, auf wen sie noch wartet.

Geht es bei einer Aufgabe um ein Ergebnis, das jemand anderes liefern soll, etwa einen unterschriebenen Vertrag, wird es unter **Details** bei **Fertig, wenn** angezeigt. Wenn du deinen Teil sendest, wird die Aufgabe nicht geschlossen: Sie bleibt unter **Wartet auf andere**, bis eine Nachricht das Ergebnis zeigt. Dann wird sie mit dem Ergebnis und **Rückgängig** automatisch geschlossen. Wenn bis zum Zeitpunkt, an dem du nachhaken solltest, nichts eingegangen ist, kommt sie mit **Schreib eine kurze Erinnerung** in ihrem Chat zurück. Um zu ändern, was als erledigt gilt, sag es im Chat.

Bevor die Aufgabe geschlossen wird, prüft deine Machine das Ergebnis anhand der Absprachen im Nachrichtenverlauf, etwa des Preises, Textes oder Links, den du gesendet hast. Sie wird nur geschlossen, wenn alles übereinstimmt, und zeigt an, was geprüft wurde. Wenn etwas abweicht, deine Zustimmung übersprungen wurde oder dein eigener Teil eines Tauschs noch offen ist, kommt die Aufgabe mit einem Hinweis darauf zurück.

Wenn das Ergebnis auf einer öffentlichen Webseite erscheinen soll, die in den Nachrichten genannt wird, etwa in einem Artikel, in dem du aufgeführt wirst, liest deine Machine die Seite, sobald es Zeit ist, nachzufragen. Wenn das Ergebnis dort zu sehen ist und noch nicht zu sehen war, als die Aufgabe zu warten begann, wird es vor dem Schließen auf dieselbe Weise geprüft. Deine Machine liest nur die Seite, wie jede andere Person auch, und sendet niemals etwas.

Wenn das Ergebnis nicht auf der Seite zu sehen ist und der Abgabetermin noch nicht erreicht ist, liest deine Machine die Seite am Morgen nach dem Abgabetermin noch einmal. Andernfalls kommt die Aufgabe wie zuvor zurück. In ihrem Chat steht dann „Geprüft“ oder „Konnte nicht geöffnet werden“ und die Seite.

Eine Aufgabe, bei der es eine Woche lang nichts Neues gab, wird von „Für dich“ nach **Älter** verschoben. So stehen nach ein paar Tagen Abwesenheit neue Aufgaben zuerst. Nichts Neues bedeutet, dass es keine neue Nachricht dazu gab und du nichts daran getan hast, etwa eine Chatnachricht geschrieben, etwas bearbeitet oder die Aufgabe zurückgestellt hast. Sie nur anzusehen zählt nicht.

Dringende Aufgaben, bald fällige Aufgaben und Aufgaben mit einer ausstehenden Nachricht bleiben unter „Für dich“. Mit **Alle verwerfen** kannst du alle Aufgaben unter „Älter“ nach einer Bestätigung als nicht nötig markieren. Das geht auch einzeln über **Nicht nötig**. Mit **Rückgängig** kannst du die Aktion rückgängig machen. Wenn es zu einer Aufgabe etwas Neues gibt, kommt sie zurück zu „Für dich“.

Wenn sich eine Woche lang niemand um eine Aufgabe gekümmert hat, wird einmal gefragt: **Noch nötig?** Mit **Nicht nötig** wird sie geschlossen. Mit **Rückgängig** kannst du die Aktion rückgängig machen. **Behalten** lässt die Aufgabe offen. Sie wird dann nicht noch einmal nachfragen. Gibt es eine weitere Woche lang keine Antwort, wird die Aufgabe unter „Kommt später zurück“ eingeklappt. Sie wird dann nicht mehr auf dem App-Symbol und in der morgendlichen Zusammenfassung mitgezählt. Wenn du die Aufgabe öffnest, eine Chatnachricht schreibst, sie bearbeitest, zurückstellst oder eine neue Nachricht dazu eingeht, kommt sie zurück.

Ein Projekt, bei dem es ruhig geworden ist und zu dem keine offenen Aufgaben gehören, kann einmal pro Woche eine Aufgabe mit einem konkreten nächsten Schritt erhalten, höchstens drei pro Woche. Mehr dazu unter [Projekte](projects.md).

Wenn nichts deine Aufmerksamkeit braucht, macht deine Machine ein Nickerchen und zeigt eine leere Liste. Während sie etwas prüft, wacht sie auf und informiert dich. Wenn eine Prüfung fehlgeschlagen ist oder sich verspätet, steht das in der Zeile. Darunter findest du **Jetzt prüfen**.

Mit **Alle**, **Arbeit** und **Privat** oben in der Seitenleiste kannst du alle Aufgaben oder nur eine Art anzeigen. Auf deinem Handy und Computer gilt dieselbe Auswahl. Wenn „Arbeit“ oder „Privat“ ausgewählt ist, führt **Alle anzeigen** zurück zur Gesamtansicht. Eine Meldung zu deiner Machine selbst, etwa dass ein Teil immer wieder neu startet, gehört weder zu „Arbeit“ noch zu „Privat“ und wird nur unter „Alle“ angezeigt.

Mit der Zeile oben in der Liste wechselst du direkt zur anderen Ansicht: Unter **Nur privat** kannst du auf **Arbeit** oder **Alle anzeigen** tippen.

Die Zeile oben in der Liste zeigt den Namen deiner letzten morgendlichen oder abendlichen Zusammenfassung und was darin gezählt wurde, etwa **Zusammenfassung von gestern Abend** · 12 erledigt, 3 offen. Tippe darauf, um die Zusammenfassung noch einmal zu lesen. Mit **Kopieren** kannst du sie an beliebiger Stelle einfügen. Sobald du sie öffnest oder auf **×** tippst, ist sie auf allen deinen Geräten verfügbar, bis die nächste Zusammenfassung kommt.

Gibt es keine aktuelle Zusammenfassung, wird **Heute bisher** angezeigt: Was heute erledigt wurde und was noch offen ist, für „Arbeit“ und „Privat“ oder nur für die Ansicht, nach der du filterst.

Bei einer Aufgabe zu einem Projekt steht der Projektname unter dem Titel. Tippe darauf, um das Projekt zu öffnen. Mit **Projekt** unter **Details** kannst du das Projekt ändern oder die Zuordnung entfernen. Mehr dazu unter [Aufgaben zu einem Projekt](projects.md#a-project-s-to-dos).

Mit **Bereich** unter **Details** verschiebst du eine Aufgabe in deinen anderen Bereich. Was die Aufgabe lesen und senden darf, ändert sich entsprechend. Mit **Rückgängig** in der Notiz verschiebst du sie zurück.

Wenn eine Aufgabe den Zugriff auf deinen anderen Bereich braucht, um weiterzumachen, und alle Nachrichten, auf denen sie beruht, dort liegen, wird sie automatisch dorthin verschoben und fortgesetzt. Andernfalls wird **Nach Arbeit verschieben** angezeigt und es wird erst etwas verschoben, wenn du darauf tippst. Eine Aufgabe, die du ohne Auswahl von „Arbeit“ oder „Privat“ hinzugefügt hast, wird automatisch dorthin verschoben, wo sie hingehört, sobald das klar ist. Bis dahin gehört sie weder zu „Arbeit“ noch zu „Privat“ und bleibt privat.

Eine Aufgabe kann immer die Nachrichten lesen, auf denen sie beruht. Wenn sie weitere Nachrichten aus deinem anderen Bereich braucht, fragt sie mit **Diese E-Mail für diese Aufgabe verwenden** danach. Ein Arbeits-Postfach, das du als privat gekennzeichnet hast, zählt als privat. E-Mails für eine andere deiner Firmen gehören zu den Aufgaben dieser Firma. Eine Aufgabe zu deinem Privatleben, etwa wenn deine Familie an deine Arbeitsadresse schreibt, ist von Anfang an privat.

Arbeit, die dich über ein privates Konto erreicht, etwa eine Nachricht von einem Kunden über WhatsApp, eine Bestellung in deinem privaten Postfach oder ein [Versprechen](promises.md) in Bezug auf die Arbeit, gehört von Anfang an zu „Arbeit“.

Eine Aufgabe, die du selbst verschoben oder zugeordnet hast, bleibt immer dort, wo du sie abgelegt hast. „Arbeit“ oder „Privat“ legt fest, wo eine Aufgabe angezeigt und mit wem sie geteilt wird, aber nicht, wohin die Antwort geht. Eine Antwort geht immer dorthin, wo die Unterhaltung stattfindet, auch nach dem Verschieben, es sei denn, du wählst einen anderen Weg.

Eine solche private Aufgabe antwortet weiterhin von der Arbeitsadresse aus, an die die E-Mail gesendet wurde, und erscheint nie in einer Work Fleet oder im Team Graph.

Wenn mindestens zwei Aufgaben warten, kannst du mit **Durchgehen** in der Kopfzeile von „Für dich“ die Aufgaben in der Listenreihenfolge nacheinander durchgehen. Jede wird vollständig mit ihrem Entwurf angezeigt. Du kannst **Senden** oder **Ausführen**, **Änderungen anfragen**, **Zurückstellen** oder **Überspringen**. Am Computer sendet Enter den angezeigten Inhalt, `S` stellt die Aufgabe zurück, `→` überspringt sie und Esc beendet den Vorgang. In der Kopfzeile steht, wie lange es bei deinem Tempo dauert, etwa „ca. 2 Min.“

Am Ende wird gezählt, was gesendet oder geschlossen wurde und was noch vorbereitet wird.

Aufgaben mit einer Frage an dich werden dabei ausgelassen: Sie brauchen deine Antwort, keinen Tippen.

## Jetzt prüfen

Deine Machine liest jede Quelle tags und nachts alle paar Minuten. Sie prüft die eingegangenen Nachrichten, sobald 40 Nachrichten warten oder die älteste Nachricht von einer Person seit 15 Minuten wartet. Newsletter, Benachrichtigungen und Belege werden bei der nächsten Prüfung innerhalb einer Stunde berücksichtigt.

Nachts, von 00:00 bis 06:30, werden Prüfungen angehalten. Neue Nachrichten werden weiterhin gelesen und gespeichert und um 06:30 gemeinsam geprüft, damit deine Aufgaben vor der morgendlichen Zusammenfassung bereitstehen. Unter „Verbindungen“ steht bei den Prüfungen „Nachts pausiert, Fortsetzung um 06:30“. Wenn du nachts in der App klickst, etwas eingibst oder scrollst, im Chat schreibst oder auf eine Aufgabe tippst, laufen die Prüfungen wie gewohnt weiter, bis du eine Stunde lang nichts machst. Mit **Jetzt prüfen** wird immer sofort geprüft.

Mit **Jetzt prüfen** werden alle Quellen sofort gelesen. Wenn keine Aufgaben offen sind, tippe auf die Zeile deiner Machine, um sie mit **Details** zu sehen. Dadurch werden die Prüfungen unter „Verbindungen“ geöffnet. Wenn Aufgaben offen sind, findest du die Zeile am Computer oben. Eine kurze Zeile wird nur angezeigt, während eine Prüfung läuft oder wenn sie fehlgeschlagen ist oder sich verspätet. Du kannst auch im Chat danach fragen.

LinkedIn, X und Salesflare haben ihren eigenen Rhythmus.

## Letzte Prüfung

Nach einer Prüfung, bei der neue Nachrichten gelesen wurden, steht über deinen Aufgaben, was in allen gelesenen Quellen gefunden wurde, etwa „13 Nachrichten um 16:11 geprüft · keine neue Aufgabe“ oder „· 2 neue Aufgaben“. Die Meldung bezieht sich nur auf diese Prüfung. Aufgaben, die bereits auf deiner Liste stehen, bleiben unverändert. Wenn eine neue Aufgabe auf einen besseren Zeitpunkt warten soll, etwa auf deine morgendliche Zusammenfassung, steht dabei, bis wann: „1 Aufgabe bis morgen 08:30 zurückgehalten“.

Tippe auf die Zeile, um die einzelnen E-Mail-Verläufe, Chats und Benachrichtigungen samt Symbol der jeweiligen Quelle zu sehen: wer geschrieben hat, den Betreff oder die ersten Wörter und die neue Aufgabe oder den Grund, warum nichts nötig war, etwa „Nur in Cc, ein Teammitglied antwortet“ oder „Besprechung bereits für Donnerstag angesetzt“. Wenn die Prüfung nur einen ungenauen Grund ergeben hat, wird bei einem Verlauf kein Grund angezeigt. Tippe auf einen Eintrag, um ihn mit dem dazugehörigen Gesprächsverlauf zu lesen.

Die ersten 10 Einträge werden angezeigt. Tippe darunter, um den Rest zu sehen. Eine Zahl hinter einem Namen, etwa (3), gibt an, wie viele neue Nachrichten dieser Chat enthält. Eine Android-Benachrichtigung zu einer Nachricht, die bereits aufgelistet ist, wird nur einmal angezeigt. Die Zeile bleibt nach der Prüfung 12 Stunden lang sichtbar.

Gezählt werden nur E-Mails, die an dich gesendet wurden. Deine eigenen Antworten werden als Kontext und auf Versprechen hin gelesen, zählen aber nicht als neue E-Mails. Die eigenen E-Mails von The Machine an dich, etwa deine morgendliche Zusammenfassung oder eine Meldung zu einer Fehlerbehebung, werden nie gelesen oder aufgelistet. E-Mails zu Rechnungen, deinem Testzeitraum oder einer Einladung werden wie gewohnt gelesen.

## Die Schaltflächen

Bei einer Aufgabe wird der nächste Schritt angezeigt, etwa **Ausführen** oder **Prüfen und senden**, daneben **Zurückstellen**. Mehr dazu unter [Ausführen](do-it.md) und [Zurückstellen](snooze.md).

Unter **Änderungen anfragen** steht, was geändert werden soll: wie etwas ausgeführt werden soll oder, sobald ein Entwurf bereit ist, was daran geändert werden soll. Wenn du mit der Eingabe beginnst, aber nicht fertig wirst, bleibt dein Text erhalten, bis du zurückkommst. Mit **Abbrechen** wird er verworfen.

Mit **Als erledigt markieren** wird die Aufgabe als erledigt markiert. Am Computer wird die Schaltfläche zusammen mit den anderen angezeigt, wenn sie in eine Zeile passen. Auf dem Handy ist sie bei einer vorbereiteten Aufgabe ohne Entwurf oder bei einer Aufgabe mit einer Frage an dich direkt zu sehen. Andernfalls findest du sie oben unter **…**. Die Aufgabe verschwindet sofort aus der Liste. In der Meldung kannst du mit **Rückgängig** die Aktion rückgängig machen. Wisch die Meldung weg oder zieh sie mit der Maus aus dem Fenster, um sie schneller zu schließen. Die Änderung bleibt bestehen.

Wenn die Aufgabe auf eine andere Weise erledigt werden soll, sag es in ihrem **Chat**. In der Antwort steht nur, was geändert wurde, etwa eine Zurückstellung und bis wann. Wenn sich etwas nicht ändern ließ, etwa ein Abgabetermin, wird das ebenfalls mitgeteilt.

Unter **…**:

- **Übergeben…**: Weise die Aufgabe einem Teammitglied zu, übergib sie an [Claude Code oder Codex](hand-to-agent.md) oder [bitte jemanden um eine Prüfung](ask-to-review.md).
- **Wiederholen…**: Die Aufgabe [kommt regelmäßig wieder](recurring.md).
- **Nicht nötig**: Die Aufgabe wird entfernt. Du kannst einen Grund auswählen: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Tippe auf den Titel oder unter **Details** auf **Name**, um die Aufgabe umzubenennen. Du kannst auch im Chat darum bitten, etwa mit „Benenne sie in … um“. Dein Titel bleibt erhalten.

Mit **Wieder öffnen** holst du eine geschlossene Aufgabe zurück. Sie kommt auch automatisch zurück, wenn etwas Neues passiert, etwa wenn die Person dir eine neue Nachricht schickt, aber nicht, wenn du selbst antwortest. Dann wird angezeigt, wann die Aufgabe zurückkam, und sie wird wie eine neue sortiert. Der Chat wird dort fortgesetzt, wo er aufgehört hat, auch nach mehreren Wochen.

Eine Rechnung, die du noch selbst bezahlen musst, wird unabhängig vom Land zu einer Aufgabe mit dem Betrag, dem Fälligkeitsdatum und den Zahlungsangaben auf der Rechnung. Automatisch bezahlte Rechnungen, etwa per Lastschrift oder gespeicherter Karte, werden nicht als Aufgabe angelegt. Wenn eine spätere E-Mail zeigt, dass sie bezahlt wurde, etwa eine Bestätigung des Zahlungseingangs vom Absender, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang zurückholen.

Eine Aufgabe, die nur bis zu einem bestimmten Zeitpunkt wichtig war, etwa eine Bestätigung vor einem Treffen, wird danach automatisch geschlossen. Sie wird unter **Erledigt / verworfen** als „Nicht mehr nötig“ angezeigt. Mit **Rückgängig** kannst du sie einen Tag lang zurückholen.

Bevor eine Nachricht oder Übergabe für eine andere Person als bereit angezeigt wird, prüft deine Machine deine letzten Chats mit den beteiligten Personen, einschließlich Gruppenchats, und wartet darauf, dass Slack sie gelesen hat. Wenn eine spätere Nachricht zeigt, dass die Aufgabe bereits erledigt ist, etwa weil die Person gefragt wurde und zugestimmt hat, wird sie automatisch geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang zurückholen.

Wenn nach dem Erstellen deines Entwurfs jemand anderes im selben Gespräch geschrieben hat, wird **Senden** angehalten: „Nicht gesendet: neue Nachricht im Verlauf“. Bei der Aufgabe wird diese Nachricht mit **Lesen** und **Für diese Nachricht neu machen** angezeigt. Tippe noch einmal auf **Senden**, um deinen Entwurf unverändert zu senden.

Wenn eine neuere Nachricht den Plan ändert, etwa weil eine Feier an einen anderen Ort verlegt oder eine Buchung storniert wurde, aktualisiert The Machine die Aufgaben selbst. Eine Aufgabe, die weiterhin wichtig ist, wird an den neuen Plan angepasst. Wenn nichts mehr zu tun ist, wird sie unter **Erledigt / verworfen** als „Nicht nötig“ angezeigt. Im Chat steht „Aktualisiert:“ mit dem Grund. Mit **Rückgängig** kannst du die Aufgabe einen Tag lang zurückholen.

Bei deinen ersten Aufgaben wird ein kurzer Tipp mit den wichtigsten Aktionen angezeigt: **Änderungen anfragen** und **Nicht nötig**. Außerdem wird darauf hingewiesen, dass nichts gesendet wird, bevor du auf **Senden** tippst. Ein Tipp wird dauerhaft ausgeblendet, sobald du seine Schaltfläche oder **×** verwendest.

Am ersten Tag begrüßt dich deine Aufgabenliste oben und nennt die Person, die am längsten auf deine Antwort wartet. Der Entwurf für diese Antwort wird zuerst erstellt, damit er bereit ist, wenn du ankommst.

Jede Aufgabe beginnt mit ihrem Titel. Darunter stehen, um wen es geht, gegebenenfalls die Organisation (nicht allein deshalb, weil jemand dort arbeitet), das Projekt, „Arbeit“ oder „Privat“ und der Eingangszeitpunkt. Tippe auf einen Namen, um die Seite der Person im Graph zu öffnen.

Bei einem Namen oder einer Organisation wird das Foto oder Logo angezeigt, sofern im Graph eines vorhanden ist. Andernfalls werden die Initialen angezeigt. Ein Logo, das in dieser Größe schwer lesbar wäre, etwa weiße Schrift auf transparentem Hintergrund oder ein breiter Schriftzug, wird ebenfalls durch Initialen ersetzt.

Manchmal steht in einer unauffälligen Zeile, was nicht bekannt ist, etwa „Letzter Kontakt vor 12 Tagen per E-Mail; seitdem nichts.“ Sie wird angezeigt, wenn der letzte Kontakt schon länger zurückliegt oder unbeantwortet ist. Auch nicht verbundene Kanäle wie WhatsApp werden genannt. Deine Machine sagt, was sie nicht weiß, statt zu raten.

Wenn ein nicht verbundener Kanal genannt wird, öffnet **Verbinden** daneben die entsprechende Verbindung.

Der Titel beschreibt, was zu tun ist, und ändert sich nur, wenn sich das ändert. Eine erledigte Aufgabe behält ihren Titel. Darunter steht, wie sie erledigt wurde, etwa „Erledigt: Sam hat es am Dienstag unterschrieben“.

Über dem Entwurf steht in einer blassen Zeile, aus welcher Nachricht er stammt, mit dem Logo des jeweiligen Dienstes. Tippe darauf, um den Nachrichtenverlauf zu lesen. Das Logo des Ziels neben dem Entwurf zeigt auf einen Blick, ob es eine Antwort in Slack oder eine E-Mail ist.

Wenn der Entwurf auf einer Eingabe an anderer Stelle beruht, etwa einem Vorschlag eines Teammitglieds in Slack, steht das in einer Zeile, etwa „Basierend auf Sam in #ops“. Tippe darauf, um die Nachricht zu lesen. Sie wird entfernt, sobald eine Aktualisierung diesen Entwurf ersetzt.

Ein Chat (Slack, WhatsApp, Telegram, Intercom …) wird als eine Unterhaltung von der ältesten zur neuesten Nachricht angezeigt: die Nachrichten vor der für die Aufgabe wichtigen Nachricht und die Antworten danach. In WhatsApp, Telegram oder Signal stehen deine Nachrichten wie in der App rechts. Die für die Aufgabe wichtige Nachricht ist mit „Diese Aufgabe“ markiert und wird direkt angezeigt. Mit **Frühere Nachrichten anzeigen** werden ältere Nachrichten eingeblendet. Bei einer E-Mail wird der Rest des Verlaufs ober- und unterhalb eingeklappt angezeigt.

Eine Nachricht wird auch in der Suche, im Graph, in Antworten von Ask oder bei der letzten Prüfung auf dieselbe Weise geöffnet und mit „Diese Nachricht“ (oder „Neue Nachrichten“) markiert.

Mit **In Gmail öffnen** wird die E-Mail in dem Gmail-Konto geöffnet, an das sie gesendet wurde. Auf Android wird sie in der Gmail-App geöffnet, sofern diese installiert ist.

Unter **Details** einer E-Mail werden nur Informationen angezeigt, die nicht bereits im Kopf der Nachricht stehen, etwa vollständige Cc-Adressen, Bcc oder eine abweichende Antwortadresse. Wenn es nichts hinzuzufügen gibt, wird nichts angezeigt.

Bei einer Antwort in einem Slack-Thread wird auch angezeigt, was vor Beginn des Threads gesagt wurde. Über den Link einer Aufgabe kannst du auch die zugehörige Nachricht hier öffnen. Unten findest du **In Slack öffnen**.

Unter **Details** stehen der Name, das Projekt und der Bereich der Aufgabe (tippe auf einen Eintrag, um ihn zu ändern), deine letzte Notiz und das Ergebnis eines Coding-Agenten. Über den Titel gelangst du zum Chat. Eine erledigte Aufgabe bleibt kurz. Die Nachricht, aus der sie entstanden ist, findest du unter **Details**.

Bei einer Aufgabe mit „Wartet auf“ führt ein Link zu deiner letzten Nachricht an die Person und zu der Nachricht, auf die du wartest: „E-Mail an Pat · Di.“

## Selbst eine Aufgabe erstellen

Mit **Neue Aufgabe** (am Computer unter **Suchen**, auf dem Handy über **+** oder mit `N`) kannst du eine Aufgabe für alles erstellen. Dabei wird nichts gesendet. Wenn du weder **Arbeit** noch **Privat** auswählst, wird die Aufgabe anhand der beteiligten Personen und des Anliegens dem passenden Bereich zugeordnet. Außerdem findet sie die E-Mail, zu der sie gehört, auch wenn diese schon älter ist.

Wenn du das Fenster vor dem Hinzufügen schließt, bleiben dein Text und deine Auswahl für das nächste Mal erhalten. Dateien werden nicht gespeichert. Mit **Verwerfen** in der Meldung werden sie entfernt.

- **Fällig**: Gib einen Tag oder eine Uhrzeit ein, etwa „morgen“, „nächsten Fr“, „3. Nov.“, „14 Uhr“ oder „in 2 Stunden“. Du kannst auch deine eigene Sprache verwenden. Über das Kalendersymbol findest du schnelle Vorschläge und **Datum wählen**.
- **Wiederholt sich**: Die Aufgabe kommt regelmäßig wieder. Mehr dazu unter [Wiederkehrende Aufgaben](recurring.md).
- **Person**: Verknüpfe bis zu 5 Personen oder Firmen, um die es geht.
- Nachrichtensymbol: Hänge die Nachricht an, um die es geht: eine E-Mail, Slack-, Teams-, WhatsApp-, Telegram- oder eine andere Nachricht, auf die deine Machine Zugriff hat. Suche nach Text oder Absender. Bei jedem Ergebnis steht, woher es stammt, wer es gesendet hat und wann.
- **Dateien**: Tippe auf die Büroklammer, füge einen Screenshot ein oder zieh Dateien auf das Formular. Auf dem Handy kannst du mit der Kamera daneben ein Foto aufnehmen. Es sind bis zu 5 Dateien möglich, wie im Chat (siehe [Dateien hinzufügen](card-chat.md#add-files)). Mit **×** entfernst du eine Datei.

Die Dateien bleiben bei der Aufgabe und werden von deiner Machine gelesen, wenn sie daran arbeitet. Es reichen auch Dateien allein: Deine Machine erstellt anhand einer PDF- oder Textdatei die Aufgabe. Ein Foto wird als kleines Bild angezeigt. Tippe darauf, um es in voller Größe zu sehen.
