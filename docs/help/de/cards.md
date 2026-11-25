---
title: Aufgaben
area: cards
summary: Eine Aufgabe pro Sache, bei der du gefragt bist, bereit für dein Ja. Was die einzelnen Teile einer Aufgabe bedeuten.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 91b111b2d6f2a97b
---
Deine Machine liest alles Neue und erstellt nur dann eine Aufgabe, wenn du gefragt bist. Eine Aufgabe pro Thema, egal über wie viele Nachrichten es geht.

## Wo Aufgaben stehen

Auf der Seite **Aufgaben** sind sie gruppiert:

- **Gerade erledigt**: Ganz oben siehst du den letzten Schritt, den du bestätigt hast, zum Beispiel ein Formular oder ein Problem, das erledigt wurde, während du weg warst. Er bleibt höchstens einen Tag lang dort, bis du auf **Verstanden** tippst. Auch auf deinem Handy wirst du darüber informiert.
- **Für dich**: Alles, was auf dich wartet. Was bis morgen fällig ist, kommt zuerst. Bei jeder Aufgabe steht **Vorbereitet** (ein Entwurf oder Ergebnis ist fertig, und mit **Ausführen** oder **Senden** wird es umgesetzt), **Braucht dich** (zuerst braucht es deine Entscheidung oder Antwort; wenn die Arbeit ohne etwas, das nur du hast, nicht weitergehen oder genutzt werden kann, etwa einen Preis, eine Information oder eine Entscheidung, steht unter dem Titel, was fehlt), **Wird vorbereitet…** (deine Machine arbeitet daran) oder **Zum Lesen** (eine Zusammenfassung oder ein Briefing, bei dem du nichts entscheiden musst).
- **Älter**: Aufgaben ohne neue Aktivität seit einer Woche sind eingeklappt (siehe unten).
- **Wartet auf andere**: Aufgaben, bei denen der nächste Schritt bei jemand anderem liegt, sind eingeklappt (siehe unten).
- **Kommt später zurück**: Zurückgestellte Aufgaben, Nachrichten, die [später gesendet werden](send-later.md), und Aufgaben, auf die es keine Antwort auf **Noch nötig?** gibt (siehe unten).
- **Versprechen**: Was du versprochen hast und was andere dir versprochen haben. Siehe [Versprechen](promises.md).
- **Erledigt / verworfen**: Alle abgeschlossenen Aufgaben, die neuesten zuerst, mit dem Zeitpunkt des Abschlusses, etwa „Vor 5 Minuten erledigt“. Aufgaben, die schon erledigt zu sein scheinen, sind mit **Sieht erledigt aus** markiert.

Nach dem Senden steht in einer kurzen Mitteilung, wohin die Aufgabe verschoben wurde, zum Beispiel „Gesendet. Nach Erledigt verschoben.“ oder „Gesendet. Bis Mo. auf Später verschoben.“ Eine Antwort, die nur verspricht, etwas zu erledigen, etwa „Ich schicke es bis Dienstag“, lässt die Aufgabe offen: „Gesendet. Offen gelassen.“ Mit **Öffnen** gelangst du zur Aufgabe. Über die Suche findest du Aufgaben nach Titel oder Empfänger, auch unter Später und Erledigt.

Unter **Für dich** stehen zuerst überfällige oder bis morgen fällige Aufgaben, dann Fragen aus deiner Fleet, dann Nachfassaufgaben eines Boards und schließlich alle übrigen. Innerhalb der Gruppen stehen die neuesten zuerst. Eine Aufgabe behält ihren Platz, während deine Machine sie vorbereitet und auch nach ihrer Erledigung. Nur ihre Markierung ändert sich. In den anderen offenen Gruppen stehen überfällige oder bis morgen fällige Aufgaben zuerst, danach die neuesten. Die Seitenleiste zeigt dieselbe Reihenfolge.

**Sieht erledigt aus** bedeutet, dass deine Machine erkennt, dass etwas erledigt ist, zum Beispiel „PR #3451 zusammengeführt“, die Aufgabe aber noch nicht geschlossen wurde. Mit **Wieder öffnen** kommt sie zurück in deine Liste, und deine Machine lernt daraus. Diese Aufgaben werden nie als verspätet angezeigt. Wenn eine Nachricht sie zeigt, schließt sie sich nach einem Tag von selbst. Mit **Rückgängig** kannst du das rückgängig machen. Andernfalls wartet sie darauf, dass du **Als erledigt markieren** auswählst.

Eine Aufgabe wird auch automatisch geschlossen, wenn du sie bereits selbst erledigt hast, zum Beispiel mit einer Antwort in Gmail oder Slack. Eine Antwort, die behauptet, eine Datei sei angehängt, obwohl keine angehängt ist, schließt die Aufgabe nicht.

Wenn eine Nachricht von einer Adresse kommt, die nur wie die einer Person aussieht, die du kennst, zum Beispiel sam@acme-corp.example statt sam@acmecorp.example, steht das klar in der Aufgabe: „Das ist nicht Sam Lee.“ Die Person wird mit ihrer tatsächlichen Adresse angezeigt, nie mit dem Namen, den sie angegeben hat. Deine Machine prüft solche Nachrichten bei der Person unter der Adresse, die du bereits gespeichert hast, nie bei der Person, die geschrieben hat.

Bei einer Aufgabe, die noch auf jemand anderen wartet, etwa auf eine Prüfung oder Antwort, steht **Wartet auf:** und der betreffende Schritt. Sie bleibt eingeklappt unter **Wartet auf andere**, oberhalb von Kommt später zurück, bis eine neue Nachricht sie wieder hervorholt. Dasselbe gilt, nachdem du eine Rückfrage gestellt hast: Die Aufgabe kommt am Morgen vor der Frist zurück, zum Zeitpunkt der Frist, wenn diese noch heute ist, oder am nächsten Morgen, wenn sie bereits verstrichen ist. Außerdem steht dabei, auf wen sie noch wartet.

Geht es bei einer Aufgabe um ein Ergebnis, das jemand anderes liefern muss, etwa einen unterschriebenen Vertrag, zeigt **Details** es unter **Fertig, wenn** an. Wenn du deinen Teil abschickst, wird die Aufgabe nicht geschlossen. Sie bleibt unter **Wartet auf andere**, bis eine Nachricht das Ergebnis zeigt. Dann wird sie automatisch geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Wenn bis zum Zeitpunkt, an dem du nachhaken solltest, nichts eingeht, kommt sie mit **Schreib eine kurze Erinnerung** in ihrem Chat zurück. Sag im Chat, was als erledigt gilt, um das zu ändern.

Eine Aufgabe ohne Neuigkeiten seit einer Woche wird von Für dich nach **Älter** verschoben, damit nach ein paar Tagen Abwesenheit neue Aufgaben zuerst kommen. Keine Neuigkeiten bedeutet, dass es keine neue Nachricht und keine Aktivität von dir dazu gab, etwa eine Chatnachricht, eine Bearbeitung oder ein Zurückstellen. Sie einfach nur anzusehen zählt nicht.

Dringende Aufgaben, bald fällige Aufgaben und Aufgaben mit einer ausstehenden Sendung bleiben unter Für dich. Mit **Alle verwerfen** kannst du nach einmaligem Bestätigen alle Aufgaben unter Älter als nicht nötig markieren. Dasselbe passiert mit **Nicht nötig**, wenn du es für einzelne Aufgaben auswählst. Mit **Rückgängig** kannst du das rückgängig machen. Neue Aktivitäten holen eine Aufgabe zurück nach Für dich.

Wenn eine Woche lang niemand eine Aufgabe bearbeitet hat, fragt sie einmal: **Noch nötig?** Mit **Nicht nötig** wird sie geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Mit **Behalten** bleibt sie bestehen und fragt nie wieder nach. Kommt eine weitere Woche lang keine Antwort, wird sie unter Kommt später zurück eingeklappt. Dann wird sie nicht mehr auf dem App-Symbol und in der morgendlichen Zusammenfassung mitgezählt. Wenn du sie öffnest, eine Chatnachricht schreibst, sie bearbeitest oder zurückstellst oder eine neue Nachricht eingeht, kommt sie zurück.

Einmal pro Woche kann ein Projekt, in dem nichts mehr offen ist und zu dem es keine Neuigkeiten gibt, eine Aufgabe mit einem konkreten nächsten Schritt erhalten. Höchstens drei pro Woche. Siehe [Projekte](projects.md).

Wenn du nichts erledigen musst, macht deine Machine ein Nickerchen und zeigt eine leere Liste. Während einer Prüfung wacht sie auf und zeigt das an. Wenn eine Prüfung fehlgeschlagen ist oder sich verspätet, steht das in der Zeile, darunter **Jetzt prüfen**.

Mit **Alle**, **Arbeit** und **Privat** oben in der Seitenleiste kannst du alle Aufgaben oder nur eine Art anzeigen. Auf deinem Handy und Computer gilt dieselbe Auswahl. Wenn Arbeit oder Privat ausgewählt ist, kommst du mit **Alle anzeigen** zurück zur Gesamtansicht. Eine Warnung zu deiner Machine selbst, etwa wenn ein Teil immer wieder neu startet, ist weder Arbeit noch Privat und wird nur unter Alle angezeigt.

Über die Zeile oben in der Liste kannst du auch direkt zur anderen Ansicht wechseln: Unter **Nur privat** tippst du auf **Arbeit** oder **Alle anzeigen**.

Die Zeile oben in der Liste nennt deine letzte morgendliche oder abendliche Zusammenfassung und ihren Inhalt, zum Beispiel **Zusammenfassung von gestern Abend** · 12 erledigt, 3 offen. Tippe darauf, um die Zusammenfassung noch einmal zu lesen und sie mit **Kopieren** an beliebiger Stelle einzufügen. Sobald du sie öffnest oder auf ihr **×** tippst, bleibt sie auf allen deinen Geräten sichtbar, bis die nächste Zusammenfassung kommt.

Wenn es keine aktuelle Zusammenfassung gibt, wird **Heute bisher** angezeigt: Was heute erledigt wurde und was noch offen ist, für Arbeit und Privat oder nur für den Bereich, nach dem du filterst.

Bei einer Aufgabe zu einem Projekt steht der Projektname unter dem Titel. Tippe darauf, um das Projekt zu öffnen. Unter **Details** kannst du mit **Projekt** das Projekt ändern oder entfernen. Siehe [Aufgaben eines Projekts](projects.md#a-project-s-to-dos).

Mit **Bereich** unter **Details** kannst du eine Aufgabe in deinen anderen Bereich verschieben. Der Zugriff auf Nachrichten, die sie lesen und senden darf, wird mitverschoben. Mit **Rückgängig** in der Mitteilung verschiebst du sie zurück.

Wenn eine Aufgabe deinen anderen Bereich braucht, um weiterzugehen, und alle Nachrichten, aus denen sie stammt, dort liegen, wird sie automatisch dorthin verschoben und fortgesetzt. Andernfalls wird **Nach Arbeit verschieben** angezeigt. Erst wenn du darauf tippst, wird etwas verschoben. Eine Aufgabe, die du hinzugefügt hast, ohne Arbeit oder Privat auszuwählen, wird automatisch in den passenden Bereich verschoben, sobald klar ist, wohin sie gehört. Bis dahin ist sie weder Arbeit noch Privat zugeordnet und bleibt privat.

Eine Aufgabe kann immer die Nachrichten lesen, aus denen sie stammt. Wenn sie weitere Nachrichten aus deinem anderen Bereich braucht, fragt sie mit **Diese E-Mail für diese Aufgabe verwenden** danach. Ein Arbeits-Postfach, das du als Privat markiert hast, zählt als Privat. E-Mails zu einem anderen deiner Unternehmen gehören zu den Aufgaben dieses Unternehmens. Eine Aufgabe zu deinem Privatleben, etwa wenn deine Familie an deine Arbeitsadresse schreibt, ist von Anfang an Privat.

Arbeit, die dich über ein privates Konto erreicht, etwa eine Nachricht von einem Kunden auf WhatsApp, eine Bestellung in deinem privaten Postfach oder ein [Versprechen](promises.md) zu einer Arbeitssache, zählt von Anfang an als Arbeit.

Eine Aufgabe, die du selbst verschoben oder zugeordnet hast, bleibt immer dort. Arbeit oder Privat legt fest, wo eine Aufgabe angezeigt und mit wem sie geteilt wird, aber nicht, wohin sie antwortet: Eine Antwort geht immer dorthin, wo das Gespräch stattfindet, auch nach einer Verschiebung, sofern du keinen anderen Weg auswählst.

Eine solche private Aufgabe antwortet weiterhin von der Arbeitsadresse, an die ihre E-Mail geschickt wurde. Sie wird nie in einer Work Fleet oder im Team Graph angezeigt.

Wenn mindestens zwei Aufgaben auf dich warten, führt **Durchgehen** in der Kopfzeile von Für dich sie nacheinander durch, in der Reihenfolge der Liste. Jeder Entwurf wird vollständig angezeigt, mit **Senden** oder **Ausführen**, **Änderungen anfragen**, **Zurückstellen** und **Überspringen**. Am Computer sendet die Eingabetaste, `S` stellt zurück, `→` überspringt und Esc beendet den Ablauf. In der Kopfzeile steht, wie lange du in deinem Tempo ungefähr brauchst, zum Beispiel „etwa 2 Min.“.

Am Ende siehst du, was gesendet oder geschlossen wurde und was noch vorbereitet wird.

Aufgaben, bei denen du eine Frage beantworten sollst, sind dabei nicht enthalten. Sie brauchen deine Antwort, nicht einen Tipp.

## Jetzt prüfen

Deine Machine liest jede Quelle alle paar Minuten, Tag und Nacht. Sie prüft eingegangene Nachrichten, sobald 40 Nachrichten warten oder die älteste Nachricht einer Person seit 15 Minuten wartet. Newsletter, Benachrichtigungen und Belege werden bei der nächsten Prüfung innerhalb einer Stunde berücksichtigt.

Nachts, von 00:00 bis 06:30, pausieren die Prüfungen. Neue Nachrichten werden weiterhin gelesen und gespeichert, aber erst um 06:30 gemeinsam geprüft. So sind deine Aufgaben vor der morgendlichen Zusammenfassung bereit. Unter Verbindungen steht bei den Prüfungen: „Nachts pausiert, Fortsetzung um 06:30“. Wenn du nachts in der App klickst, tippst oder scrollst, im Chat schreibst oder auf eine Aufgabe tippst, laufen die Prüfungen wie gewohnt weiter, bis du eine Stunde lang abwesend warst. Mit **Jetzt prüfen** wird immer sofort geprüft.

Mit **Jetzt prüfen** werden alle Quellen sofort gelesen. Wenn keine Aufgabe offen ist, tippe auf die Zeile deiner Machine, um sie mit **Details** zu sehen. Damit öffnest du die Prüfungen unter Verbindungen. Wenn Aufgaben offen sind, findest du sie am Computer oben. Eine kurze Zeile wird dort nur angezeigt, während eine Prüfung läuft oder wenn sie fehlgeschlagen ist oder sich verspätet. Du kannst auch im Chat danach fragen.

LinkedIn, X und Salesflare haben ihren eigenen Rhythmus.

## Letzte Prüfung

Nach einer Prüfung, bei der neue Nachrichten gelesen wurden, steht über deinen Aufgaben, was dabei gefunden wurde und aus welchen Quellen die Nachrichten stammen. Zum Beispiel: „13 Nachrichten um 16:11 geprüft · keine neue Aufgabe“ oder „· 2 neue Aufgaben“. Die Zeile bezieht sich nur auf diese Prüfung. Aufgaben, die bereits in deiner Liste stehen, bleiben unverändert. Wenn eine neue Aufgabe bis zu einem passenden Zeitpunkt zurückgehalten wird, etwa bis zur morgendlichen Zusammenfassung, steht dabei, bis wann: „1 Aufgabe bis morgen 08:30 zurückgehalten“.

Tippe auf die Zeile, um die E-Mail-Threads, Chats und Benachrichtigungen einzeln anzusehen, jeweils mit dem Symbol der Quelle. Du siehst, wer geschrieben hat, den Betreff oder die ersten Wörter und die neue Aufgabe oder den Grund, warum keine nötig war, zum Beispiel „Nur in Cc, ein Teammitglied antwortet“ oder „Termin für Donnerstag steht bereits“. Bei einem Thread wird kein Grund angezeigt, wenn die Prüfung nur einen ungenauen Grund ergeben hat. Tippe auf einen Eintrag, um ihn mit dem Gesprächsverlauf zu lesen.

Die ersten 10 Einträge werden angezeigt. Tippe darunter, um den Rest zu sehen. Eine Zahl nach einem Namen, etwa (3), gibt an, wie viele neue Nachrichten dieser Chat hat. Eine Handy-Benachrichtigung zu einer Nachricht, die bereits aufgelistet ist, wird nur einmal angezeigt. Die Zeile bleibt 12 Stunden nach der Prüfung sichtbar.

Gezählt werden nur E-Mails an dich. Deine eigenen Antworten werden als Kontext und auf Versprechen hin gelesen, zählen aber nicht als neue E-Mails. E-Mails deiner Machine an dich, etwa die morgendliche Zusammenfassung oder eine Benachrichtigung über eine Fehlerbehebung, werden nie gelesen oder aufgelistet. E-Mails zu deiner Abrechnung, deinem Testzeitraum oder einer Einladung werden wie gewohnt gelesen.

## Die Schaltflächen

Bei einer Aufgabe wird der nächste Schritt angezeigt, zum Beispiel **Ausführen** oder **Prüfen und senden**, daneben **Zurückstellen**. Siehe [Ausführen](do-it.md) und [Zurückstellen](snooze.md).

Mit **Änderungen anfragen** kannst du angeben, was geändert werden soll: wie etwas erledigt werden soll oder, sobald ein Entwurf bereit ist, was darin geändert werden soll. Wenn du deine Eingabe nicht abschickst, bleibt sie erhalten, bis du zurückkommst. Mit **Abbrechen** wird sie verworfen.

Mit **Als erledigt markieren** gibst du an, dass die Aufgabe erledigt ist. Am Computer steht die Schaltfläche bei den anderen, wenn sie in eine Zeile passen. Auf dem Handy ist sie bei einer bereiten Aufgabe ohne Entwurf oder einer Aufgabe mit einer Frage direkt zu sehen. Sonst findest du sie oben unter **…**. Die Aufgabe verschwindet sofort aus der Liste. In der Mitteilung kannst du mit **Rückgängig** die Änderung rückgängig machen. Wische die Mitteilung weg oder ziehe sie mit der Maus weg, um sie schneller zu schließen. Die Änderung bleibt bestehen.

Wenn die Aufgabe anders erledigt werden soll, sag das in ihrem **Chat**. Die Antwort nennt nur, was sich geändert hat, etwa eine Zurückstellung und bis wann. Wenn etwas nicht geändert werden konnte, etwa ein Fälligkeitsdatum, steht das ebenfalls dabei.

Unter **…**:

- **Übergeben…**: Übergib die Aufgabe an ein Teammitglied, an [Claude Code oder Codex](hand-to-agent.md) oder [bitte jemanden um eine Prüfung](ask-to-review.md).
- **Wiederholen…**: Die Aufgabe [kommt regelmäßig zurück](recurring.md).
- **Nicht nötig**: Die Aufgabe wird ausgeblendet. Du kannst optional einen Grund auswählen: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Tippe auf den Titel oder unter **Details** auf **Name**, um die Aufgabe umzubenennen. Du kannst auch in ihrem Chat darum bitten, zum Beispiel: „Benenne sie in … um.“ Dein Titel bleibt erhalten.

Mit **Wieder öffnen** holst du eine geschlossene Aufgabe zurück. Sie kommt auch von selbst zurück, wenn etwas Neues passiert, zum Beispiel eine neue Nachricht von der betreffenden Person, aber nicht bei deiner eigenen Antwort. Dann wird angezeigt, wann sie zurückgekommen ist, und sie wird wie eine neue Aufgabe einsortiert. Der Chat läuft dort weiter, wo er aufgehört hat, auch nach mehreren Wochen.

Eine Rechnung, die du selbst bezahlen musst, wird unabhängig vom Land zu einer Aufgabe mit Betrag, Fälligkeitsdatum und Zahlungsangaben aus der Rechnung. Rechnungen, die automatisch bezahlt werden, etwa per Lastschrift oder mit einer hinterlegten Karte, werden nicht zu Aufgaben. Wenn eine spätere E-Mail zeigt, dass die Rechnung bezahlt wurde, zum Beispiel eine Bestätigung des Zahlungseingangs vom Absender, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du sie innerhalb eines Tages zurückholen.

Eine Aufgabe, die nur bis zu einem bestimmten Zeitpunkt wichtig war, etwa eine Bestätigung vor einem Meeting, wird danach automatisch geschlossen. Sie wird unter **Erledigt / verworfen** mit dem Hinweis „Nicht mehr nötig“ abgelegt. Mit **Rückgängig** kannst du sie innerhalb eines Tages zurückholen.

Bevor eine Nachricht oder Übergabe für jemanden als bereit angezeigt wird, prüft deine Machine deine letzten Chats mit den beteiligten Personen, einschließlich Gruppenchats, und wartet darauf, dass Slack sie gelesen hat. Wenn eine spätere Nachricht zeigt, dass die Aufgabe bereits erledigt ist, etwa weil die Person gefragt wurde und zugesagt hat, wird sie automatisch geschlossen. Mit **Rückgängig** kannst du sie innerhalb eines Tages zurückholen.

Wenn jemand im selben Gespräch schreibt, nachdem dein Entwurf erstellt wurde, hält **Senden** den Entwurf zurück: „Nicht gesendet: Neue Nachricht im Thread“. Die Aufgabe zeigt diese Nachricht mit **Lesen** und **Für diese Nachricht neu machen** an. Tippe noch einmal auf **Senden**, um deinen Entwurf unverändert zu senden.

Wenn eine neuere Nachricht den Plan ändert, etwa weil eine Party an einen anderen Ort verlegt oder eine Buchung storniert wurde, aktualisiert The Machine ihre Aufgaben selbst. Eine weiterhin wichtige Aufgabe folgt dem neuen Plan. Wenn nichts mehr zu tun ist, wird sie unter **Erledigt / verworfen** mit „Nicht nötig“ abgelegt. Im Chat steht „Aktualisiert:“ mit der Begründung. Mit **Rückgängig** kannst du sie innerhalb eines Tages zurückholen.

Bei deinen ersten Aufgaben wird ein kurzer Tipp mit den wichtigsten Aktionen angezeigt: **Änderungen anfragen** und **Nicht nötig**. Außerdem wird erklärt, dass nichts gesendet wird, bevor du auf **Senden** tippst. Ein Tipp verschwindet endgültig, sobald du seine Schaltfläche verwendest oder auf × tippst.

An deinem ersten Tag begrüßt dich deine Aufgabenliste oben und nennt die Person, die am längsten auf deine Antwort wartet. Dieser Antwortentwurf wird zuerst erstellt, damit er bereit ist, wenn du kommst.

Jede Aufgabe beginnt mit ihrem Titel. Die Zeile darunter nennt, um wen es geht, bei einem Unternehmen auch dessen Namen (aber nicht einfach deshalb, weil jemand dort arbeitet), das Projekt, Arbeit oder Privat und den Zeitpunkt, zu dem die Aufgabe eingegangen ist. Tippe auf einen Namen, um die Seite der Person im Graph zu öffnen.

Wenn im Graph ein Foto oder Logo vorhanden ist, wird es neben dem Namen oder Unternehmen angezeigt, andernfalls die Initialen. Ein Logo, das in dieser Größe unleserlich wäre, etwa weiße Schrift auf transparentem Hintergrund oder ein breiter Schriftzug, wird ebenfalls durch die Initiale ersetzt.

Manchmal steht in einer dezenten Zeile, was nicht bekannt ist, zum Beispiel: „Letzter Kontakt vor 12 Tagen per E-Mail, seitdem nichts.“ Sie wird angezeigt, wenn der letzte Kontakt schon länger zurückliegt oder unbeantwortet ist. Außerdem werden nicht verbundene Kanäle wie WhatsApp genannt. Deine Machine sagt, was sie nicht weiß, statt zu raten.

Wenn ein nicht verbundener Kanal genannt wird, öffnet **Verbinden** daneben die Verbindung.

Der Titel beschreibt, was zu tun ist, und ändert sich nur, wenn sich die Aufgabe ändert. Eine erledigte Aufgabe behält ihren Titel. Darunter steht, wie sie abgeschlossen wurde, zum Beispiel: „Erledigt: Sam hat es am Dienstag unterschrieben“.

Über dem Entwurf steht in einer dezenten Zeile, aus welcher Nachricht er stammt, zusammen mit dem Logo des Dienstes. Tippe darauf, um den Thread zu lesen. Am Logo über dem Entwurf erkennst du, wohin er geht, zum Beispiel als Slack-Antwort oder E-Mail.

Wenn der Entwurf auf einer Eingabe von anderer Stelle beruht, etwa einem Vorschlag eines Teammitglieds in Slack, steht das in einer Zeile, zum Beispiel „Basierend auf Sam in #ops“. Tippe darauf, um die Nachricht zu lesen. Die Zeile verschwindet, wenn ein Update den Entwurf ersetzt.

Ein Chat (Slack, WhatsApp, Telegram, Intercom …) wird als ein Gespräch angezeigt, älteste Nachrichten zuerst: die Nachrichten vor der Nachricht, um die es in der Aufgabe geht, und die Antworten danach. In WhatsApp, Telegram oder Signal stehen deine Nachrichten wie in der App rechts. Die Nachricht der Aufgabe ist mit „Diese Aufgabe“ markiert und wird direkt angezeigt. Mit **Frühere Nachrichten anzeigen** werden ältere Nachrichten eingeblendet. Bei einer E-Mail ist der restliche Thread ober- und unterhalb der Nachricht eingeklappt.

Eine Nachricht wird auch über die Suche, den Graph, die Antworten von Ask oder die letzte Prüfung auf dieselbe Weise geöffnet und mit „Diese Nachricht“ (oder „Neue Nachrichten“) markiert.

Mit **In Gmail öffnen** wird die E-Mail in dem Gmail-Konto geöffnet, an das sie gesendet wurde. Auf Android wird sie in der Gmail-App geöffnet, wenn du diese installiert hast.

Unter **Details** einer E-Mail stehen nur Angaben, die nicht schon in der Kopfzeile zu sehen sind, etwa vollständige Cc-Adressen, Bcc oder eine abweichende Antwortadresse. Gibt es nichts hinzuzufügen, werden keine Details angezeigt.

Bei einer Antwort in einem Slack-Thread wird auch angezeigt, was vor dem Start des Threads gesagt wurde. Über den Link einer Aufgabe zur ursprünglichen Nachricht kannst du sie hier ebenfalls öffnen. Unten steht dann **In Slack öffnen**.

Unter **Details** stehen der Name, das Projekt und der Bereich der Aufgabe (tippe auf einen davon, um ihn zu ändern), deine letzte Notiz und das Ergebnis eines Coding-Agenten. Über den Titel wird der Chat geöffnet. Eine erledigte Aufgabe bleibt kurz. Die Nachricht, aus der sie entstanden ist, steht unter **Details**.

Bei einer Aufgabe mit „Wartet auf“ führt der Link zu deiner letzten Nachricht an die Person, auf deren Antwort du wartest: „E-Mail an Pat · Di“.

## Selbst eine Aufgabe erstellen

Mit **Neue Aufgabe** (am Computer unter **Suchen**, auf dem Handy über **+** oder mit `N`) kannst du eine Aufgabe für alles Mögliche erstellen. Beim Erstellen wird nichts gesendet. Wenn du weder **Arbeit** noch **Privat** auswählst, wird sie dem passenden Bereich zugeordnet, je nachdem, um wen und was es geht. Außerdem findet die Aufgabe die E-Mail, an die sie anknüpft, auch wenn sie schon älter ist.

Wenn du das Fenster schließt, bevor du die Aufgabe hinzufügst, bleiben dein Text und deine Auswahl beim nächsten Mal erhalten, Dateien jedoch nicht. Mit **Verwerfen** in der Mitteilung werden sie gelöscht.

- **Fällig**: Gib einen Tag oder eine Uhrzeit ein, zum Beispiel „morgen“, „nächsten Fr“, „3. Nov“, „14 Uhr“ oder „in 2 Stunden“, auch in deiner eigenen Sprache. Über das Kalendersymbol findest du Schnelloptionen und **Datum wählen**.
- **Wiederholt sich**: Die Aufgabe kommt regelmäßig zurück. Siehe [Wiederkehrende Aufgaben](recurring.md).
- **Person**: Verknüpfe bis zu 5 Personen oder Unternehmen, um die es geht.
- Nachrichtensymbol: Hänge die Nachricht an, um die es geht, etwa eine E-Mail, Slack-, Teams-, WhatsApp-, Telegram- oder eine andere Nachricht, auf die The Machine zugreifen kann. Suche nach Text oder Absender. Bei jedem Ergebnis siehst du, woher es stammt, wer es gesendet hat und wann.
- **Dateien**: Tippe auf die Büroklammer, füge einen Screenshot ein oder ziehe Dateien auf das Formular. Auf dem Handy kannst du mit der Kamera daneben ein Foto aufnehmen. Wie im Chat sind bis zu 5 Dateien möglich (siehe [Dateien hinzufügen](card-chat.md#add-files)). Mit × entfernst du eine Datei wieder.

Die Dateien bleiben bei der Aufgabe, und The Machine liest sie, wenn sie daran arbeitet. Du kannst auch nur Dateien hinzufügen: The Machine erstellt die Aufgabe aus einer PDF- oder Textdatei. Ein Foto wird als kleines Bild angezeigt. Tippe darauf, um es in voller Größe anzusehen.
