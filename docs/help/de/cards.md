---
title: Aufgaben
area: cards
summary: Eine Aufgabe pro Sache, die dich braucht, bereit für dein Okay. Was die einzelnen Teile einer Aufgabe bedeuten.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 51db64e67403d2ea
---
Deine Machine liest alles Neue und erstellt nur dann eine Aufgabe, wenn etwas deine Aufmerksamkeit braucht. Pro Thema gibt es eine Aufgabe, egal über wie viele Nachrichten es sich erstreckt.

## Wo Aufgaben stehen

Auf der Seite **Aufgaben** sind sie gruppiert:

- **Gerade erledigt**: Oben siehst du einen letzten Schritt, den du bestätigt hast, zum Beispiel ein Formular oder ein Problem, das erledigt wurde, während du nicht da warst. Er bleibt höchstens einen Tag hier, bis du auf **Verstanden** tippst. Du bekommst auch auf deinem Handy Bescheid.
- **Für dich**: Alles, was auf dich wartet, nach Dringlichkeit sortiert. Bei jeder Aufgabe steht **Vorbereitet** (ein Entwurf oder Ergebnis ist fertig, und mit **Ausführen** oder **Senden** wird es umgesetzt), **Braucht dich** (zuerst ist eine Entscheidung oder Antwort von dir nötig; wenn die Arbeit an etwas hängt, das nur du hast, zum Beispiel eine Information, eine Anmeldung oder eine Entscheidung, steht es unter dem Titel), **Wird vorbereitet…** (deine Machine arbeitet daran) oder **Zum Lesen** (eine Zusammenfassung oder ein Briefing, bei dem du nichts entscheiden musst).
- **Älter**: Eingeklappte Aufgaben, bei denen es seit einer Woche nichts Neues gibt (siehe unten).
- **Wartet auf andere**: Eingeklappte Aufgaben, bei denen der nächste Schritt bei jemand anderem liegt (siehe unten).
- **Kommt später zurück**: Zurückgestellte Aufgaben und Aufgaben ohne Antwort auf **Noch nötig?** (siehe unten).
- **Versprechen**: Was du versprochen hast und was andere dir versprochen haben. Siehe [Versprechen](promises.md).
- **Erledigt / verworfen**: Alle abgeschlossenen Aufgaben, neueste zuerst, mit dem Zeitpunkt ihres Abschlusses, zum Beispiel „Vor 5 Minuten erledigt“. Aufgaben, die bereits erledigt zu sein scheinen, sind mit **Sieht erledigt aus** markiert.

Nach dem Senden steht kurz, wohin die Aufgabe verschoben wurde, zum Beispiel „Gesendet. Nach Erledigt verschoben.“ oder „Gesendet. Bis Mo. nach Später verschoben.“ Eine Antwort, die nur die Arbeit verspricht, etwa „Ich schicke es bis Dienstag“, lässt die Aufgabe offen: „Gesendet. Offen gelassen.“ Mit **Öffnen** gelangst du zur Aufgabe. Über die Suche findest du Aufgaben anhand ihres Titels oder der Person, an die sie gegangen sind, auch unter Später und Erledigt.

Unter **Für dich** stehen zuerst überfällige Aufgaben und Aufgaben, die bis morgen fällig sind, dann Fragen aus deiner Fleet, dann Nachfassaufgaben eines Boards und danach der Rest. Innerhalb der Gruppen stehen die neuesten zuerst. Eine Aufgabe behält ihren Platz, während deine Machine sie vorbereitet und wenn sie erledigt ist. Nur ihre Markierung ändert sich. In den anderen offenen Gruppen stehen überfällige Aufgaben und Aufgaben, die bis morgen fällig sind, zuerst, danach der Rest, neueste zuerst. In der Seitenleiste bleibt die Reihenfolge gleich.

**Sieht erledigt aus** bedeutet, dass deine Machine erkennt, dass eine Aufgabe erledigt ist, zum Beispiel „PR #3451 ist zusammengeführt“, sie aber noch nicht geschlossen wurde. Mit **Wieder öffnen** kommt sie zurück auf deine Liste, und deine Machine lernt daraus. Diese Aufgaben werden nie als verspätet angezeigt. Wenn eine Nachricht darauf hinweist, wird die Aufgabe nach einem Tag automatisch mit **Rückgängig** geschlossen. Andernfalls wartet sie darauf, dass du **Als erledigt markieren** auswählst. Eine Aufgabe, die du schon selbst erledigt hast, etwa mit einer Antwort in Gmail oder Slack, wird ebenfalls automatisch geschlossen.

Wenn eine Nachricht von einer Adresse kommt, die nur einer Person ähnelt, die du kennst, zum Beispiel sam@acme-corp.example statt sam@acmecorp.example, steht bei der Aufgabe ganz deutlich: „Das ist nicht Sam Lee.“ Die Person wird mit ihrer eigenen Adresse angezeigt, nie mit dem Namen, den sie verwendet hat. Deine Machine überprüft solche Nachrichten bei der Person unter der Adresse, die du bereits kennst, nie bei der Person, die geschrieben hat.

Bei einer Aufgabe, die noch auf jemand anderen wartet, zum Beispiel auf eine Prüfung oder Antwort, steht **Wartet auf:** mit dem entsprechenden Schritt. Sie erscheint eingeklappt unter **Wartet auf andere**, oberhalb von Kommt später zurück, bis eine neue Nachricht sie wieder hervorholt. Das gilt auch, nachdem du eine Rückfrage gestellt hast: Die Aufgabe kommt am Morgen vor ihrer Frist zurück, bei einer Frist noch am selben Tag zum Zeitpunkt der Frist oder am nächsten Morgen, wenn die Frist bereits verstrichen ist. Außerdem steht dabei, auf wen sie noch wartet.

Wenn es bei einer Aufgabe um ein Ergebnis geht, das jemand anderes liefern muss, zum Beispiel einen unterschriebenen Vertrag, zeigt **Details** dieses Ergebnis unter **Fertig, wenn** an. Wenn du deinen Teil abschickst, wird die Aufgabe nicht geschlossen. Sie bleibt unter **Wartet auf andere**, bis eine Nachricht das Ergebnis zeigt. Dann wird sie automatisch mit **Rückgängig** geschlossen. Wenn bis zum Zeitpunkt fürs Nachfassen nichts kommt, erscheint die Aufgabe wieder mit **Schreib eine kurze Erinnerung** in ihrem Chat. Sag im Chat, was als erledigt gilt, um das zu ändern.

Aufgaben, bei denen es eine Woche lang nichts Neues gibt, werden von Für dich nach **Älter** verschoben. So stehen nach ein paar Tagen Abwesenheit neue Aufgaben zuerst. „Nichts Neues“ bedeutet, dass es keine neue Nachricht zur Aufgabe und nichts von dir dazu gab, zum Beispiel eine Chatnachricht, eine Änderung oder eine Zurückstellung. Sie nur anzusehen zählt nicht.

Dringende Aufgaben, bald fällige Aufgaben und Aufgaben, bei denen gerade etwas gesendet wird, bleiben unter Für dich. Mit **Alle verwerfen** markierst du alle Aufgaben unter Älter nach einmaliger Bestätigung als nicht nötig, genauso wie **Nicht nötig** einzelne Aufgaben markiert. **Rückgängig** macht das rückgängig. Sobald es bei einer Aufgabe etwas Neues gibt, kommt sie zurück zu Für dich.

Wenn sich eine Woche lang niemand um eine Aufgabe gekümmert hat, fragt sie einmal: **Noch nötig?** Mit **Nicht nötig** wird sie geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. **Behalten** lässt die Aufgabe offen, und sie fragt nie wieder nach. Wenn eine weitere Woche lang keine Antwort kommt, wird sie unter Kommt später zurück eingeklappt. Sie wird dann nicht mehr auf dem App-Symbol und in der morgendlichen Zusammenfassung mitgezählt. Wenn du sie öffnest, eine Chatnachricht schreibst, sie bearbeitest oder zurückstellst oder eine neue Nachricht dazu kommt, erscheint sie wieder.

Einmal pro Woche kann es für ein Projekt, bei dem nichts mehr passiert und keine Aufgaben offen sind, eine Aufgabe mit einem konkreten nächsten Schritt geben. Höchstens drei pro Woche. Siehe [Projekte](projects.md).

Wenn nichts deine Aufmerksamkeit braucht, macht deine Machine eine Pause und zeigt eine leere Liste. Während sie prüft, wird sie aktiv und zeigt das an. Wenn eine Prüfung fehlgeschlagen ist oder sich verspätet, steht es in der Zeile. Darunter erscheint **Jetzt prüfen**.

Mit **Alle**, **Arbeit** und **Privat** oben in der Seitenleiste kannst du alle Aufgaben oder nur eine Art anzeigen. Auf deinem Handy und Computer gilt dieselbe Auswahl. Wenn Arbeit oder Privat ausgewählt ist, führt **Alle anzeigen** zurück zur Gesamtansicht. Eine Meldung über deine Machine selbst, zum Beispiel über einen Teil, der immer wieder neu startet, gehört weder zu Arbeit noch zu Privat und erscheint nur unter Alle.

Mit der Zeile oben in der Liste wechselst du auch direkt zur anderen Ansicht: Unter **Nur privat** kannst du auf **Arbeit** oder **Alle anzeigen** tippen.

Die Zeile oben in der Liste zeigt deine letzte morgendliche oder abendliche Zusammenfassung und was darin gezählt wurde, zum Beispiel **Zusammenfassung von gestern Abend** · 12 erledigt, 3 offen. Tippe darauf, um die Zusammenfassung noch einmal zu lesen. Mit **Kopieren** kannst du sie überall einfügen. Sobald du sie öffnest oder auf ihr **×** tippst, ist sie auf allen deinen Geräten verfügbar, bis die nächste Zusammenfassung kommt.

Ohne eine aktuelle Zusammenfassung zeigt die Liste **Heute bisher**: was heute erledigt wurde und was noch offen ist, für Arbeit und Privat oder nur für den Bereich, nach dem du filterst.

Bei einer Aufgabe zu einem Projekt steht der Projektname unter dem Titel. Tippe darauf, um das Projekt zu öffnen. Unter **Details** kannst du es mit **Projekt** ändern oder entfernen. Siehe [Aufgaben eines Projekts](projects.md#a-project-s-to-dos).

Mit **Bereich** unter **Details** verschiebst du eine Aufgabe in deinen anderen Bereich. Der Zugriff auf Nachrichten und die Möglichkeit, Nachrichten zu senden, werden dabei ebenfalls verschoben. Mit **Rückgängig** in der Meldung verschiebst du sie zurück.

Wenn eine Aufgabe deinen anderen Bereich braucht, um weiterzugehen, und alle Nachrichten, auf denen sie beruht, dort sind, wird sie automatisch dorthin verschoben und fortgesetzt. Andernfalls wird **Nach Arbeit verschieben** angezeigt. Die Aufgabe wird erst verschoben, wenn du darauf tippst. Eine Aufgabe, die du selbst erstellt hast, ohne Arbeit oder Privat auszuwählen, wird automatisch verschoben, sobald klar ist, wohin sie gehört. Bis dahin gehört sie weder zu Arbeit noch zu Privat und bleibt privat.

Eine Aufgabe kann immer die Nachrichten lesen, auf denen sie beruht. Wenn sie weitere Nachrichten aus deinem anderen Bereich braucht, fragt sie mit **Diese E-Mail für diese Aufgabe verwenden** danach. Ein Arbeits-Postfach, das du als Privat gekennzeichnet hast, gilt als Privat. E-Mails für andere Unternehmen von dir gehören zu den Aufgaben des jeweiligen Unternehmens. Eine Aufgabe zu deinem Privatleben, zum Beispiel wenn deine Familie an deine Arbeitsadresse schreibt, ist von Anfang an privat.

Arbeit, die dich über ein privates Konto erreicht, zum Beispiel eine Nachricht von einem Kunden in WhatsApp oder eine Bestellung in deinem privaten Postfach, gilt von Anfang an als Arbeit. Eine Aufgabe, die du selbst verschoben oder zugeordnet hast, bleibt immer dort, wo du sie abgelegt hast. Arbeit oder Privat bestimmt, wo eine Aufgabe erscheint und mit wem sie geteilt wird, aber nicht, wo sie antwortet. Eine Antwort geht immer dorthin, wo das Gespräch stattfindet, auch nach einer Verschiebung, außer du wählst eine andere Möglichkeit.

Eine solche private Aufgabe antwortet weiterhin von der Arbeitsadresse, an die die E-Mail gesendet wurde. Sie erscheint nie in einer Work Fleet oder im Team Graph.

Wenn mindestens zwei Aufgaben auf dich warten, kannst du sie mit **Durchgehen** in der Kopfzeile von Für dich nacheinander in der Reihenfolge der Liste bearbeiten. Jeder Entwurf wird vollständig angezeigt, mit **Senden** oder **Ausführen**, **Änderungen anfragen**, **Zurückstellen** und **Überspringen**. Auf einem Computer sendet Enter den Inhalt auf dem Bildschirm, `S` stellt zurück, `→` überspringt und Esc beendet. In der Kopfzeile steht, wie lange es in deinem Tempo dauert, zum Beispiel „etwa 2 Min.“

Am Ende wird gezählt, was gesendet oder geschlossen wurde und was noch vorbereitet wird.

Eine Aufgabe, bei der dir eine Frage gestellt wird, ist in beidem nicht enthalten: Sie wartet auf deine Antwort, nicht auf einen Tipp.

## Jetzt prüfen

Deine Machine liest jede Quelle alle paar Minuten, Tag und Nacht. Sie prüft neue Nachrichten, sobald 40 Nachrichten eingegangen sind oder die älteste Nachricht einer Person seit 15 Minuten wartet. Newsletter, Benachrichtigungen und Belege werden bei der nächsten Prüfung innerhalb einer Stunde berücksichtigt.

Nachts, von 00:00 bis 06:30 Uhr, pausieren die Prüfungen. Neue Nachrichten werden weiterhin gelesen und gespeichert. Um 06:30 Uhr werden sie zusammen geprüft, damit deine Aufgaben vor der morgendlichen Zusammenfassung bereit sind. Unter Verbindungen steht bei den Prüfungen: „Nachts pausiert, wird um 06:30 Uhr nachgeholt“. Wenn du nachts in der App klickst, etwas eingibst oder scrollst, im Chat schreibst oder auf eine Aufgabe tippst, laufen die Prüfungen wie gewohnt, bis du eine Stunde lang nicht da warst. Mit **Jetzt prüfen** wird immer sofort geprüft.

**Jetzt prüfen** liest sofort alle Quellen. Wenn keine Aufgaben offen sind, tippe auf die Zeile deiner Machine, um sie mit **Details** anzusehen. Dadurch werden die Prüfungen unter Verbindungen geöffnet. Wenn Aufgaben offen sind, findest du die Zeile oben auf dem Computer. Sie erscheint nur kurz, während eine Prüfung läuft oder wenn eine fehlgeschlagen ist oder sich verspätet. Du kannst auch im Chat danach fragen.

LinkedIn, X und Salesflare folgen ihrem eigenen Rhythmus.

## Letzte Prüfung

Nach einer Prüfung, bei der neue Nachrichten gelesen wurden, steht oberhalb deiner Aufgaben, was in allen geprüften Quellen gefunden wurde, zum Beispiel „13 Nachrichten um 16:11 geprüft · keine neue Aufgabe“ oder „· 2 neue Aufgaben“. Die Angabe bezieht sich nur auf diese Prüfung. Aufgaben, die bereits auf deiner Liste stehen, bleiben unverändert. Wenn eine neue Aufgabe bis zu einem passenden Zeitpunkt warten soll, zum Beispiel bis zur morgendlichen Zusammenfassung, steht dabei, bis wann: „1 Aufgabe bis morgen 08:30 Uhr zurückgehalten“.

Tippe auf die Zeile, um die E-Mail-Unterhaltungen, Chats und Benachrichtigungen mit dem Symbol der jeweiligen Quelle zu sehen: wer geschrieben hat, den Betreff oder die ersten Wörter sowie die neue Aufgabe oder den Grund, warum nichts nötig war, zum Beispiel „Nur in Cc, ein Teammitglied antwortet“ oder „Termin für Donnerstag steht bereits“. Bei einer Unterhaltung wird kein Grund angezeigt, wenn die Prüfung nur einen vagen Grund ergeben hat. Tippe auf eine Unterhaltung, um sie zu lesen.

Die ersten 10 werden angezeigt. Tippe darunter, um den Rest zu sehen. Eine Zahl hinter einem Namen, zum Beispiel (3), gibt an, wie viele neue Nachrichten dieser Chat hat. Eine Handy-Benachrichtigung zu einer Nachricht, die bereits aufgelistet ist, wird nur einmal angezeigt. Die Zeile bleibt 12 Stunden nach der Prüfung sichtbar.

Es werden nur E-Mails an dich gezählt. Deine eigenen Antworten werden als Kontext und auf Versprechen hin gelesen, zählen aber nicht als neue E-Mails. E-Mails, die The Machine selbst an dich schickt, zum Beispiel deine morgendliche Zusammenfassung oder eine Meldung zu einer Fehlerbehebung, werden nie gelesen oder aufgelistet. E-Mails zu Abrechnungen, deiner Testphase oder einer Einladung werden wie gewohnt gelesen.

## Die Schaltflächen

Bei einer Aufgabe wird der nächste Schritt angezeigt, zum Beispiel **Ausführen** oder **Prüfen und senden**, daneben steht **Zurückstellen**. Siehe [Ausführen](do-it.md) und [Zurückstellen](snooze.md).

Mit **Änderungen anfragen** kannst du angeben, was geändert werden soll: wie die Aufgabe erledigt wird oder, sobald ein Entwurf bereit ist, was daran geändert werden soll. **Als erledigt markieren** bedeutet, dass die Aufgabe erledigt ist. Bei einer vorbereiteten Aufgabe ohne Entwurf oder einer Aufgabe, bei der dir eine Frage gestellt wird, ist die Schaltfläche direkt zu sehen. Sonst findest du sie oben unter **…**. Die Aufgabe wird sofort aus der Liste entfernt und die Meldung enthält **Rückgängig**. Wische die Meldung weg oder ziehe sie mit der Maus aus der Liste, um sie schneller zu schließen. Die Änderung bleibt bestehen.

Wenn die Aufgabe anders erledigt werden soll, sag es im **Chat**. In der Antwort steht nur, was geändert wurde, zum Beispiel eine Zurückstellung und bis wann. Wenn etwas nicht geändert werden konnte, etwa ein Fälligkeitsdatum, steht das ebenfalls dabei.

Unter **…**:

- **Übergeben…**: Gib die Aufgabe an ein Teammitglied, [Claude Code oder Codex](hand-to-agent.md) weiter oder [bitte jemanden um eine Prüfung](ask-to-review.md).
- **Wiederholen…**: Die Aufgabe [kommt regelmäßig wieder](recurring.md).
- **Nicht nötig**: Die Aufgabe wird entfernt. Du kannst optional einen Grund auswählen: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Tippe auf den Titel oder unter **Details** auf **Name**, um die Aufgabe umzubenennen. Du kannst auch im Chat darum bitten, zum Beispiel mit „Benenne sie in … um“. Dein Titel bleibt erhalten.

Mit **Wieder öffnen** holst du eine geschlossene Aufgabe zurück. Sie erscheint auch automatisch wieder, wenn etwas Neues passiert, zum Beispiel eine neue Nachricht von der anderen Person, aber nicht bei deiner eigenen Antwort. Dann steht dabei, wann sie wiederkam, und sie wird wie eine neue Aufgabe sortiert. Der Chat wird dort fortgesetzt, wo er aufgehört hat, auch nach Wochen.

Eine Rechnung, die du selbst noch bezahlen musst, wird unabhängig vom Land zu einer Aufgabe. Sie enthält den Betrag, das Fälligkeitsdatum und die Zahlungsangaben auf der Rechnung. Automatisch bezahlte Rechnungen, etwa per Lastschrift oder mit einer hinterlegten Karte, werden nicht als Aufgaben angelegt. Wenn eine spätere E-Mail zeigt, dass sie bezahlt wurde, zum Beispiel eine Bestätigung des Zahlungseingangs vom Absender, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Eine Aufgabe, die nur bis zu einem bestimmten Zeitpunkt wichtig war, etwa eine Bestätigung vor einem Termin, wird danach automatisch geschlossen. Sie wird mit dem Status „Nicht mehr nötig“ nach **Erledigt / verworfen** verschoben. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Bevor eine Nachricht oder Übergabe für jemanden als bereit angezeigt wird, prüft deine Machine die letzten Chats mit den beteiligten Personen, auch Gruppenchats, und wartet, bis Slack sie gelesen hat. Wenn eine spätere Nachricht zeigt, dass die Aufgabe bereits erledigt ist, zum Beispiel weil jemand gefragt wurde und zugestimmt hat, wird sie automatisch geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Wenn jemand anderes in derselben Unterhaltung geschrieben hat, nachdem der Entwurf erstellt wurde, wird er mit **Senden** zurückgehalten: „Nicht gesendet: neue Nachricht im Thread“. Bei der Aufgabe wird diese Nachricht mit **Lesen** und **Für diese Nachricht neu machen** angezeigt. Tippe noch einmal auf **Senden**, um den Entwurf unverändert zu senden.

Wenn eine neuere Nachricht den Plan ändert, zum Beispiel weil eine Feier an einen anderen Ort verlegt oder eine Buchung storniert wurde, aktualisiert The Machine die Aufgaben selbst. Eine weiterhin relevante Aufgabe folgt dem neuen Plan. Wenn nichts mehr zu tun ist, wird sie mit dem Status „Nicht nötig“ nach **Erledigt / verworfen** verschoben. Im Chat steht „Aktualisiert:“ mit dem Grund. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Bei deinen ersten Aufgaben erscheint ein kurzer Tipp zu den wichtigsten Aktionen: **Änderungen anfragen** und **Nicht nötig**. Außerdem erfährst du, dass nichts gesendet wird, bevor du auf **Senden** tippst. Der Tipp wird dauerhaft ausgeblendet, sobald du seine Schaltfläche verwendest oder auf × tippst.

Am ersten Tag begrüßt dich deine Machine oben auf der Seite Aufgaben und nennt die Person, die am längsten auf deine Antwort wartet. Dieser Antwortentwurf wird zuerst erstellt und ist bereit, wenn du da bist.

Jede Aufgabe beginnt mit ihrem Titel. In der Zeile darunter stehen, um wen es geht, die Organisation, wenn die Aufgabe damit zu tun hat, aber nicht allein deshalb, weil jemand dort arbeitet, das Projekt, Arbeit oder Privat und der Zeitpunkt, an dem die Aufgabe eingegangen ist. Tippe auf einen Namen, um die Seite der Person im Graph zu öffnen.

Wenn im Graph ein Foto oder Logo vorhanden ist, werden der Name und die Organisation damit angezeigt, andernfalls mit den Initialen. Ein Logo, das in dieser Größe schwer zu erkennen wäre, zum Beispiel weiße Schrift auf transparentem Hintergrund oder ein breites Wortlogo, wird ebenfalls durch die Initiale ersetzt.

Manchmal steht in einer unaufdringlichen Zeile, was nicht bekannt ist, etwa „Letzter Kontakt vor 12 Tagen per E-Mail; seitdem nichts.“ Sie wird angezeigt, wenn die letzte Nachricht der Person schon länger zurückliegt oder unbeantwortet ist. Außerdem werden nicht verbundene Kanäle wie WhatsApp genannt. Deine Machine sagt, was sie nicht weiß, statt zu raten.

Wenn ein nicht verbundener Kanal genannt wird, öffnet **Verbinden** daneben diese Verbindung.

Der Titel beschreibt, was zu tun ist, und ändert sich nur, wenn sich das ändert. Eine erledigte Aufgabe behält ihren Titel. Darunter steht, wie sie abgeschlossen wurde, zum Beispiel „Erledigt: Sam hat es am Dienstag unterschrieben“.

Über dem Entwurf steht in einer unauffälligen Zeile, aus welcher Nachricht er stammt, mit dem Logo des jeweiligen Dienstes. Tippe darauf, um die Unterhaltung zu lesen. Beim Entwurf wird das Logo des Ziels angezeigt. So erkennst du sofort, ob es sich um eine Slack-Antwort oder eine E-Mail handelt.

Wenn der Entwurf auf einer Eingabe von anderer Stelle beruht, zum Beispiel auf dem Vorschlag eines Teammitglieds in Slack, steht das in einer Zeile, etwa „Basiert auf Sam in #ops“. Tippe darauf, um die Nachricht zu lesen.

Ein Chat in Slack, WhatsApp, Telegram, Intercom und anderen Diensten wird als eine Unterhaltung angezeigt, von der ältesten Nachricht an: zuerst die Nachrichten vor der Nachricht, um die es in der Aufgabe geht, dann die Antworten darauf. In WhatsApp, Telegram oder Signal stehen deine Nachrichten wie in der App rechts. Die Nachricht zur Aufgabe ist mit „Diese Aufgabe“ markiert und wird direkt angezeigt. Mit **Frühere Nachrichten anzeigen** werden ältere Nachrichten eingeblendet. Bei einer E-Mail ist der Rest des Threads oberhalb und unterhalb der Nachricht eingeklappt.

Mit **In Gmail öffnen** wird die E-Mail in dem Gmail-Konto geöffnet, in dem sie eingegangen ist. Auf Android wird sie in der Gmail-App geöffnet, wenn du diese installiert hast.

Unter **Details** einer E-Mail stehen nur zusätzliche Angaben, die nicht in ihrer Kopfzeile erscheinen, etwa vollständige Cc-Adressen, Bcc oder eine andere Antwortadresse. Gibt es keine zusätzlichen Angaben, wird dieser Bereich nicht angezeigt.

Bei einer Antwort in einem Slack-Thread wird auch angezeigt, was vor dem Start des Threads gesagt wurde. Über den Link einer Aufgabe zu ihrer eigenen Nachricht kannst du sie ebenfalls hier öffnen. Unten steht **In Slack öffnen**.

Unter **Details** stehen der Name, das Projekt und der Bereich der Aufgabe. Tippe auf einen davon, um ihn zu ändern. Dort findest du auch deine letzte Notiz und das Ergebnis eines Coding-Agenten. Über den Titel öffnest du den Chat. Eine erledigte Aufgabe bleibt kompakt. Die Nachricht, aus der sie entstanden ist, findest du unter **Details**.

Bei einer Aufgabe mit „Wartet auf“ führt ein Link zu deiner letzten Nachricht an die Person, auf die du wartest: „E-Mail an Pat · Di“.

## Selbst eine Aufgabe erstellen

Mit **Neue Aufgabe** (auf einem Computer unter **Suchen**, auf einem Handy über **+** oder mit `N`) kannst du eine Aufgabe für alles Mögliche erstellen. Beim Erstellen wird nichts gesendet. Wenn du weder **Arbeit** noch **Privat** auswählst, wird die Aufgabe anhand der beteiligten Personen und des Themas dem passenden Bereich zugeordnet. Außerdem wird die E-Mail gefunden, auf die sich die Aufgabe bezieht, auch wenn sie schon älter ist.

- **Fällig**: Gib einen Tag oder eine Uhrzeit ein, zum Beispiel „morgen“, „nächsten Fr.“, „3. Nov.“, „14 Uhr“ oder „in 2 Stunden“. Das funktioniert auch in deiner eigenen Sprache. Über das Kalendersymbol findest du Schnelloptionen und **Datum wählen**.
- **Wiederholt sich**: Die Aufgabe kommt regelmäßig wieder. Siehe [Wiederkehrende Aufgaben](recurring.md).
- **Person**: Verknüpfe bis zu fünf Personen oder Unternehmen, um die es geht.
- Nachrichtensymbol: Hänge die Nachricht an, um die es geht. Das kann eine E-Mail, eine Nachricht aus Slack, Teams, WhatsApp, Telegram oder einem anderen Dienst sein, den The Machine unterstützt. Suche nach Text oder Absender. In jedem Ergebnis steht, woher die Nachricht kommt, wer sie gesendet hat und wann.
- **Dateien**: Tippe auf die Büroklammer, füge einen Screenshot ein oder ziehe Dateien in das Formular. Auf einem Handy kannst du mit der Kamera daneben ein Foto aufnehmen. Bis zu fünf Dateien, wie im Chat (siehe [Dateien hinzufügen](card-chat.md#add-files)). Mit × entfernst du eine Datei.

Die Dateien bleiben bei der Aufgabe und werden von The Machine gelesen, wenn sie daran arbeitet. Es reichen auch Dateien allein: Aus einer PDF- oder Textdatei erstellt The Machine die Aufgabe. Ein Foto wird als kleines Bild angezeigt. Tippe darauf, um es in voller Größe zu sehen.
