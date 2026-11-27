---
title: Aufgaben
area: cards
summary: Eine Aufgabe für alles, was dich braucht, bereit für dein Ja. Was die einzelnen Teile einer Aufgabe bedeuten.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: dfbc7ccc7313ecfe
---
Deine Machine liest alles Neue und erstellt nur dann eine Aufgabe, wenn etwas dich braucht. Eine Aufgabe pro Angelegenheit, egal über wie viele Nachrichten sie sich erstreckt.

## Wo Aufgaben stehen

Auf der Seite **Aufgaben** sind sie gruppiert:

- **Gerade erledigt**: Oben siehst du den letzten Schritt, den du bestätigt hast, etwa ein Formular oder ein Problem, das erledigt wurde, während du nicht da warst. Er bleibt höchstens einen Tag lang stehen, bis du auf **Verstanden** tippst. Auch dein Handy bekommt eine Meldung.
- **Für dich**: Alles, was auf dich wartet. Was bis morgen fällig ist, steht zuerst. Bei jeder Aufgabe steht **Vorbereitet** (ein Entwurf oder Ergebnis ist fertig, und **Ausführen** oder **Senden** setzt es um), **Braucht dich** (zuerst braucht es deine Entscheidung oder Antwort; wenn die Arbeit ohne etwas, das nur du hast, nicht weitergehen oder genutzt werden kann, etwa einen Preis, eine Information oder eine Entscheidung, steht darunter, was fehlt), **Wird vorbereitet…** (deine Machine arbeitet daran) oder **Zum Lesen** (eine Zusammenfassung oder ein Briefing, bei dem du nichts entscheiden musst).
- **Älter**: Eingeklappte Aufgaben, bei denen es seit einer Woche nichts Neues gibt (siehe unten).
- **Wartet auf andere**: Eingeklappte Aufgaben, bei denen der nächste Schritt bei jemand anderem liegt (siehe unten).
- **Kommt später zurück**: Zurückgestellte Aufgaben, Nachrichten, die [später gesendet werden](send-later.md), und Aufgaben ohne Antwort auf **Noch nötig?** (siehe unten).
- **Versprechen**: Was du versprochen hast und was andere dir versprochen haben. Mehr dazu unter [Versprechen](promises.md).
- **Erledigt / verworfen**: Alle abgeschlossenen Aufgaben, neueste zuerst, mit dem Zeitpunkt ihres Abschlusses, etwa „Erledigt vor 5 Minuten“. Aufgaben, die anscheinend bereits erledigt sind, sind mit **Sieht erledigt aus** markiert.

Nach dem Senden steht in einer kurzen Meldung, wohin die Aufgabe verschoben wurde, etwa „Gesendet. Nach Erledigt verschoben.“ oder „Gesendet. Bis Mo. nach Später verschoben.“ Eine Antwort, die nur verspricht, die Arbeit zu erledigen, etwa „Ich schicke es bis Dienstag“, lässt die Aufgabe offen: „Gesendet. Offen gelassen.“ Mit **Öffnen** gelangst du zur Aufgabe. Über die Suche findest du eine Aufgabe anhand ihres Titels oder der Person, an die sie ging, auch unter Später und Erledigt.

Unter **Für dich** stehen zuerst überfällige oder bis morgen fällige Aufgaben, dann Fragen aus deinem Fleet, dann Nachfassaktionen eines Boards und anschließend alle übrigen. Innerhalb jeder Gruppe stehen die neuesten zuerst. Eine Aufgabe behält ihren Platz, während deine Machine sie vorbereitet und wenn sie erledigt ist. Nur ihre Markierung ändert sich. In den anderen offenen Gruppen stehen überfällige oder bis morgen fällige Aufgaben zuerst, danach die neuesten. Die Seitenleiste behält dieselbe Reihenfolge bei.

**Sieht erledigt aus** bedeutet, dass deine Machine erkennt, dass etwas erledigt ist, etwa „PR #3451 zusammengeführt“, aber die Aufgabe noch nicht geschlossen wurde. Mit **Wieder öffnen** kommt sie zurück auf deine Liste, und deine Machine lernt daraus. Diese Aufgaben werden nie als verspätet angezeigt. Wenn eine Nachricht sie anzeigt, wird sie nach einem Tag automatisch geschlossen. Dabei kannst du **Rückgängig** wählen. Andernfalls wartet sie auf **Als erledigt markieren**.

Auch eine Aufgabe, die du bereits selbst erledigt hast, etwa mit einer Antwort in Gmail oder Slack, wird automatisch geschlossen. Eine Antwort, in der steht, dass eine Datei angehängt ist, obwohl keine dabei ist, schließt sie nicht.

Wenn eine Nachricht von einer Adresse kommt, die nur wie die einer bekannten Person aussieht, etwa sam@acme-corp.example statt sam@acmecorp.example, steht das deutlich bei der Aufgabe: „Das ist nicht Sam Lee.“ Die Person wird mit ihrer tatsächlichen Adresse angezeigt, nie mit dem Namen, den sie verwendet hat. Deine Machine prüft solche Nachrichten mit der Person unter der Adresse, die du bereits kennst, nie mit der Person, die geschrieben hat.

Eine Aufgabe, die noch auf jemand anderen wartet, etwa auf eine Prüfung oder Antwort, zeigt unter **Wartet auf:** den nächsten Schritt. Sie bleibt eingeklappt unter **Wartet auf andere**, oberhalb von Kommt später zurück, bis eine neue Nachricht sie wieder hervorholt. Das gilt auch, nachdem du eine Rückfrage gestellt hast: Die Aufgabe kommt am Morgen vor ihrer Frist zurück, bei einer Frist später am selben Tag erst zu diesem Zeitpunkt oder am nächsten Morgen, wenn die Frist bereits verstrichen ist. Sie zeigt dann, auf wen sie noch wartet.

Wenn es bei einer Aufgabe um ein Ergebnis geht, das jemand anderes liefern muss, etwa einen unterschriebenen Vertrag, wird es unter **Details** als **Fertig, wenn** angezeigt. Wenn du deinen Teil abschickst, ist die Aufgabe noch nicht abgeschlossen: Sie wartet unter **Wartet auf andere**, bis eine Nachricht das Ergebnis zeigt. Dann wird sie automatisch mit dem Ergebnis geschlossen. Dabei kannst du **Rückgängig** wählen. Wenn bis zum Zeitpunkt, an dem du nachhaken solltest, nichts eingetroffen ist, kommt sie mit **Schreib eine kurze Erinnerung** in ihrem Chat zurück. Um zu ändern, was als erledigt gilt, sag es im Chat.

Wenn das Ergebnis auf einer öffentlichen Webseite erscheinen soll, die in den Nachrichten genannt wird, etwa in einem Artikel, der dich aufführt, liest deine Machine die Seite, wenn es Zeit ist, nachzufragen. Wenn das Ergebnis dort steht und noch nicht angezeigt wurde, als die Aufgabe zu warten begann, wird die Aufgabe automatisch geschlossen und das Ergebnis angezeigt. Dabei kannst du **Rückgängig** wählen. Deine Machine liest die Seite nur, wie jede Besucherin und jeder Besucher, und sendet nichts.

Wenn das Ergebnis nicht auf der Seite steht und die Frist noch nicht erreicht ist, liest deine Machine die Seite am Morgen nach der Frist noch einmal. Andernfalls kommt die Aufgabe wie zuvor zurück, mit „Geprüft“ oder „Konnte nicht geöffnet werden“ und der Seite in ihrem Chat.

Eine Aufgabe, bei der es eine Woche lang nichts Neues gab, wird aus „Für dich“ nach **Älter** verschoben. So stehen nach ein paar Tagen Abwesenheit die neuen Aufgaben oben. Als nichts Neues zählen weder neue Nachrichten zur Aufgabe noch etwas, das du daran gemacht hast, etwa eine Chatnachricht, eine Änderung oder ein Zurückstellen. Sie nur anzusehen zählt nicht.

Dringende Aufgaben, bald fällige Aufgaben und Aufgaben, bei denen gerade etwas gesendet wird, bleiben unter „Für dich“. Mit **Alle verwerfen** kannst du nach einer Bestätigung alle Aufgaben unter „Älter“ als nicht nötig markieren. Das geht auch einzeln mit **Nicht nötig**. Dabei kannst du **Rückgängig** wählen. Gibt es bei einer Aufgabe etwas Neues, kommt sie zurück zu „Für dich“.

Eine Aufgabe, die eine Woche lang niemand angefasst hat, fragt einmal nach: **Noch nötig?** Mit **Nicht nötig** wird sie geschlossen. Dabei kannst du **Rückgängig** wählen. Mit **Behalten** bleibt sie bestehen und fragt nie wieder nach. Wenn eine weitere Woche lang keine Antwort kommt, wird sie unter „Kommt später zurück“ eingeklappt. Sie wird dann nicht mehr auf dem App-Symbol oder in der morgendlichen Zusammenfassung gezählt. Wenn du sie öffnest, eine Chatnachricht schreibst, sie bearbeitest, zurückstellst oder eine neue Nachricht eingeht, kommt sie zurück.

Einmal pro Woche kann es für ein Projekt, bei dem es ruhig geworden ist und keine Aufgaben offen sind, eine Aufgabe mit einem konkreten nächsten Schritt geben. Höchstens drei pro Woche. Mehr dazu unter [Projekte](projects.md).

Wenn nichts dich braucht, macht deine Machine ein Nickerchen und zeigt eine leere Liste. Während sie etwas prüft, wird sie aktiv und sagt dir Bescheid. Wenn eine Prüfung fehlgeschlagen oder verspätet ist, steht das in der Zeile. Darunter findest du **Jetzt prüfen**.

Mit **Alle**, **Arbeit** und **Privat** oben in der Seitenleiste kannst du alle Aufgaben oder nur eine Art anzeigen. Auf deinem Handy und Computer gilt dieselbe Auswahl. Wenn „Arbeit“ oder „Privat“ ausgewählt ist, führt **Alle anzeigen** zurück zur Gesamtansicht. Eine Meldung über deine Machine selbst, etwa dass ein Teil immer wieder neu startet, gehört weder zu Arbeit noch zu Privat und wird nur unter „Alle“ angezeigt.

Über die Zeile oben in der Liste kannst du auch direkt zur anderen Ansicht wechseln: Unter **Nur privat** tippst du auf **Arbeit** oder **Alle anzeigen**.

Die Zeile oben in der Liste nennt deine letzte morgendliche oder abendliche Zusammenfassung und was darin gezählt wurde, etwa **Zusammenfassung von gestern Abend** · 12 erledigt, 3 offen. Tippe darauf, um die Zusammenfassung noch einmal zu lesen. Mit **Kopieren** kannst du sie an anderer Stelle einfügen. Sobald du sie öffnest oder auf **×** tippst, ist sie auf all deinen Geräten verfügbar, bis die nächste Zusammenfassung erscheint.

Wenn es keine aktuelle Zusammenfassung gibt, wird **Heute bisher** angezeigt: was heute erledigt wurde und was noch offen ist, für Arbeit und Privat oder nur für den ausgewählten Bereich.

Bei einer Aufgabe zu einem Projekt steht der Projektname unter dem Titel. Tippe darauf, um das Projekt zu öffnen. Unter **Details** kannst du es mit **Projekt** ändern oder entfernen. Mehr dazu unter [Aufgaben eines Projekts](projects.md#a-project-s-to-dos).

Mit **Bereich** unter **Details** verschiebst du eine Aufgabe in deinen anderen Bereich. Was sie lesen und senden darf, wird ebenfalls verschoben. Mit **Rückgängig** in der Meldung verschiebst du sie zurück.

Wenn eine Aufgabe den anderen Bereich braucht, um weiterzugehen, und alle Nachrichten, aus denen sie hervorgegangen ist, dort liegen, wird sie automatisch dorthin verschoben und fortgesetzt. Andernfalls wird **Nach Arbeit verschieben** angezeigt. Es wird nichts verschoben, bis du darauf tippst. Eine Aufgabe, die du hinzugefügt hast, ohne Arbeit oder Privat auszuwählen, wird automatisch verschoben, sobald sie dem passenden Bereich zugeordnet werden kann. Bis dahin gehört sie weder zu Arbeit noch zu Privat und bleibt privat.

Eine Aufgabe kann immer die Nachrichten lesen, aus denen sie hervorgegangen ist. Wenn sie weitere Nachrichten aus deinem anderen Bereich braucht, fragt sie mit **Diese E-Mail für diese Aufgabe verwenden** nach. Ein Arbeits-Postfach, das du als privat markiert hast, gilt als privat. E-Mails für ein anderes Unternehmen von dir gehen zu den Aufgaben dieses Unternehmens. Eine Aufgabe über dein eigenes Leben, etwa wenn deine Familie an deine Arbeitsadresse schreibt, ist von Anfang an privat.

Arbeit, die dich über ein privates Konto erreicht, etwa eine Kundin oder ein Kunde auf WhatsApp, eine Bestellung in deinem privaten Postfach oder ein [Versprechen](promises.md) zu deiner Arbeit, gehört von Anfang an zu Arbeit.

Eine Aufgabe, die du selbst verschoben oder zugeordnet hast, bleibt immer dort, wo du sie abgelegt hast. Arbeit oder Privat bestimmt, wo eine Aufgabe angezeigt und mit wem sie geteilt wird, aber nicht, wohin sie antwortet: Eine Antwort geht immer dorthin, wo die Unterhaltung stattfindet, auch nach einer Verschiebung, es sei denn, du wählst einen anderen Weg.

Eine solche private Aufgabe antwortet weiterhin über die Arbeitsadresse, an die ihre E-Mail gesendet wurde, und wird nie in einem Work Fleet oder im Team Graph angezeigt.

Wenn mindestens zwei Aufgaben warten, kannst du mit **Durchgehen** in der Kopfzeile von „Für dich“ sie nacheinander in der Reihenfolge der Liste bearbeiten. Jeder Entwurf wird vollständig angezeigt, mit **Senden** oder **Ausführen**, **Änderungen anfragen**, **Zurückstellen** und **Überspringen**. Auf einem Computer sendet Enter, `S` stellt zurück, `→` überspringt und Esc beendet den Vorgang. In der Kopfzeile steht, wie lange es bei deinem Tempo dauert, etwa „ca. 2 Min.“.

Am Ende siehst du, was gesendet oder geschlossen wurde und was noch vorbereitet wird.

Aufgaben, bei denen du etwas beantworten musst, werden dabei ausgelassen: Sie brauchen deine Antwort und keinen Tipp.

## Jetzt prüfen

Deine Machine liest jede Quelle alle paar Minuten, Tag und Nacht. Sie prüft, was eingegangen ist, sobald 40 Nachrichten warten oder die älteste Nachricht einer Person 15 Minuten gewartet hat. Newsletter, Benachrichtigungen und Quittungen werden bei der nächsten Prüfung berücksichtigt, spätestens innerhalb einer Stunde.

Nachts, von 00:00 bis 06:30, pausieren die Prüfungen: Neue Nachrichten werden weiterhin gelesen und gespeichert und um 06:30 gemeinsam geprüft, damit deine Aufgaben vor der morgendlichen Zusammenfassung bereit sind. Unter „Verbindungen“ steht bei den Prüfungen „Nachts pausiert, holt um 06:30 auf“. Wenn du nachts in der App klickst, etwas eingibst oder scrollst, im Chat schreibst oder auf eine Aufgabe tippst, laufen die Prüfungen wie gewohnt weiter, bis du eine Stunde lang nicht mehr da warst. **Jetzt prüfen** startet immer sofort eine Prüfung.

**Jetzt prüfen** liest sofort alle Quellen. Wenn keine Aufgaben offen sind, tippe auf die Zeile deiner Machine, um sie mit **Details** zu sehen. Damit öffnest du die Prüfungen unter „Verbindungen“. Wenn Aufgaben offen sind, findest du sie auf einem Computer oben. Dort wird eine kurze Zeile nur angezeigt, während eine Prüfung läuft oder wenn eine fehlgeschlagen oder verspätet ist. Du kannst auch im Chat danach fragen.

LinkedIn, X und Salesflare haben ihren eigenen Takt.

## Letzte Prüfung

Nach einer Prüfung, bei der neue Nachrichten gelesen wurden, steht über deinen Aufgaben, was gefunden wurde, und zwar aus allen gelesenen Quellen. Zum Beispiel: „13 Nachrichten um 16:11 geprüft · keine neue Aufgabe“ oder „· 2 neue Aufgaben“. Die Meldung bezieht sich nur auf diese Prüfung. Aufgaben, die bereits auf deiner Liste stehen, bleiben unverändert. Wenn eine neue Aufgabe auf einen besseren Zeitpunkt wartet, etwa auf deine morgendliche Zusammenfassung, steht dabei, bis wann: „1 Aufgabe bis morgen 08:30 zurückgehalten“.

Tippe auf die Zeile, um jeden E-Mail-Thread, Chat und jede Benachrichtigung samt Symbol der Quelle zu sehen: wer geschrieben hat, den Betreff oder die ersten Wörter und die neue Aufgabe oder den Grund, warum nichts nötig war. Zum Beispiel: „Nur in Cc, eine Kollegin oder ein Kollege antwortet“ oder „Termin für Donnerstag steht schon“. Wenn die Prüfung nur einen vagen Grund ergeben hat, wird bei einem Thread kein Grund angezeigt. Tippe darauf, um die Nachricht und den Gesprächsverlauf zu lesen.

Die ersten 10 werden angezeigt. Tippe darunter, um den Rest zu sehen. Eine Zahl hinter einem Namen, etwa (3), gibt an, wie viele neue Nachrichten dieser Chat enthält. Eine Android-Benachrichtigung zu einer bereits aufgeführten Nachricht wird nur einmal angezeigt. Die Zeile bleibt nach der Prüfung 12 Stunden sichtbar.

Gezählt werden nur E-Mails an dich. Deine eigenen Antworten werden im Kontext und auf Versprechen hin gelesen, zählen aber nicht als neue E-Mails. E-Mails, die deine Machine selbst an dich sendet, etwa deine morgendliche Zusammenfassung oder ein Hinweis auf eine Fehlerbehebung, werden nie gelesen oder aufgeführt. E-Mails zu Abrechnungen, deinem Probezeitraum oder einer Einladung werden wie gewohnt gelesen.

## Die Schaltflächen

Bei einer Aufgabe wird der nächste Schritt angezeigt, etwa **Ausführen** oder **Prüfen und senden**, daneben steht **Zurückstellen**. Mehr dazu unter [Ausführen](do-it.md) und [Zurückstellen](snooze.md).

Mit **Änderungen anfragen** kannst du angeben, was geändert werden soll: wie etwas erledigt werden soll oder, sobald ein Entwurf fertig ist, was daran geändert werden soll. Wenn du den Text nur teilweise eingibst, bleibt er dort, bis du zurückkommst. Mit **Abbrechen** wird er verworfen.

**Als erledigt markieren** bedeutet, dass die Aufgabe erledigt ist. Auf einem Computer steht die Schaltfläche neben den anderen, wenn sie in eine Zeile passen. Auf einem Handy ist sie bei einer fertigen Aufgabe ohne Entwurf oder bei einer Frage sichtbar, andernfalls oben unter **…**. Die Aufgabe verschwindet sofort aus der Liste. In der Meldung kannst du **Rückgängig** wählen. Wische die Meldung weg oder ziehe sie mit der Maus aus der Liste, um sie schneller zu schließen. Die Änderung bleibt bestehen.

Wenn die Aufgabe auf eine andere Weise erledigt werden soll, sag es in ihrem **Chat**. In der Antwort steht nur, was geändert wurde, etwa eine Zurückstellung und bis wann. Wenn etwas nicht geändert werden konnte, etwa ein Fälligkeitsdatum, steht das ebenfalls dort.

Unter **…**:

- **Übergeben…**: Übergib die Aufgabe an ein Teammitglied, an [Claude Code oder Codex](hand-to-agent.md) oder [bitte jemanden um eine Prüfung](ask-to-review.md).
- **Wiederholen…**: Die Aufgabe [kommt regelmäßig zurück](recurring.md).
- **Nicht nötig**: Die Aufgabe wird entfernt. Du kannst optional einen Grund auswählen: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Tippe auf den Titel oder unter **Details** auf **Name**, um die Aufgabe umzubenennen. Du kannst auch im Chat danach fragen, etwa „Benenne sie in … um“. Dein Titel bleibt erhalten.

Mit **Wieder öffnen** holst du eine geschlossene Aufgabe zurück. Sie kommt auch von selbst wieder, wenn etwas Neues passiert, etwa eine neue Nachricht von der anderen Person, aber nicht bei deiner eigenen Antwort. Dann wird angezeigt, wann sie zurückkam, und sie wird wie eine neue Aufgabe sortiert. Der Chat läuft dort weiter, wo er aufgehört hat, auch nach mehreren Wochen.

Eine Rechnung, die du selbst noch bezahlen musst, wird unabhängig vom Land zu einer Aufgabe mit dem Betrag, dem Fälligkeitsdatum und den Zahlungsdaten, die auf der Rechnung stehen. Automatisch bezahlte Rechnungen, etwa per Lastschrift oder mit einer gespeicherten Karte, werden nicht als Aufgaben erfasst. Wenn eine spätere E-Mail zeigt, dass sie bezahlt wurde, etwa eine Bestätigung des Zahlungseingangs vom Absender, wird die Aufgabe automatisch geschlossen. Einen Tag lang kannst du **Rückgängig** wählen.

Eine Aufgabe, die nur bis zu einem bestimmten Zeitpunkt wichtig war, etwa eine Bestätigung vor einem Meeting, wird nach diesem Zeitpunkt automatisch geschlossen. Sie wird unter **Erledigt / verworfen** mit „Nicht mehr nötig“ abgelegt. Einen Tag lang kannst du **Rückgängig** wählen.

Bevor eine Nachricht oder Übergabe für jemanden als bereit angezeigt wird, prüft deine Machine deine letzten Chats mit den beteiligten Personen, einschließlich Gruppenchats, und wartet, bis Slack sie gelesen hat. Wenn eine spätere Nachricht zeigt, dass die Aufgabe bereits erledigt ist, etwa weil jemand gefragt wurde und Ja gesagt hat, wird sie automatisch geschlossen. Einen Tag lang kannst du **Rückgängig** wählen.

Wenn nach dem Erstellen deines Entwurfs jemand anderes in derselben Unterhaltung geschrieben hat, hält **Senden** den Entwurf zurück: „Nicht gesendet: neue Nachricht im Thread“. Bei der Aufgabe werden diese Nachricht sowie **Lesen** und **Für diese Nachricht neu machen** angezeigt. Tippe erneut auf **Senden**, um deinen Entwurf unverändert abzuschicken.

Wenn eine neuere Nachricht den Plan ändert, etwa eine Feier an einen anderen Ort verlegt oder eine Buchung storniert wird, aktualisiert The Machine die Aufgaben selbst. Eine weiterhin relevante Aufgabe folgt dem neuen Plan. Wenn nichts mehr zu tun ist, wird sie unter **Erledigt / verworfen** mit „Nicht nötig“ abgelegt. Im Chat steht „Aktualisiert:“ mit dem Grund. Einen Tag lang kannst du **Rückgängig** wählen.

Bei deinen ersten Aufgaben erscheint ein kurzer Tipp zu den wichtigsten Aktionen: **Änderungen anfragen** und **Nicht nötig**. Außerdem erfährst du, dass nichts gesendet wird, bevor du auf **Senden** tippst. Der Tipp verschwindet endgültig, sobald du die Schaltfläche verwendest oder auf × tippst.

An deinem ersten Tag begrüßt dich oben in „Aufgaben“ eine Nachricht. Sie nennt die Person, die am längsten auf deine Antwort wartet. Dieser Antwortentwurf wird zuerst vorbereitet und ist bereit, wenn du kommst.

Jede Aufgabe beginnt mit ihrem Titel. In der Zeile darunter stehen, um wen es geht, gegebenenfalls die Organisation (aber nicht allein deshalb, weil jemand dort arbeitet), das Projekt, Arbeit oder Privat und der Zeitpunkt des Eingangs. Tippe auf einen Namen, um die Seite der Person im Graph zu öffnen.

Bei Namen und Organisationen wird das Foto oder Logo angezeigt, wenn es im Graph vorhanden ist, andernfalls die Initialen. Wenn ein Logo in dieser Größe nicht lesbar wäre, etwa weiß auf durchsichtigem Hintergrund oder ein breites Wortlogo, wird stattdessen auch die Initiale angezeigt.

Manchmal steht in einer unauffälligen Zeile, was nicht bekannt ist, etwa „Letzter Kontakt vor 12 Tagen per E-Mail, seitdem nichts“. Das wird angezeigt, wenn der letzte Kontakt mit der Person lange zurückliegt oder unbeantwortet ist. Auch nicht verbundene Kanäle wie WhatsApp werden genannt. Deine Machine sagt, was sie nicht weiß, statt zu raten.

Wenn ein nicht verbundener Kanal genannt wird, öffnet „Verbinden“ daneben diese Verbindung.

Der Titel nennt die Aufgabe und ändert sich nur, wenn sich diese ändert. Eine erledigte Aufgabe behält ihren Titel. Darunter steht, wie sie abgeschlossen wurde, etwa „Erledigt: Sam hat es am Dienstag unterschrieben“.

Über dem Entwurf steht in einer blassen Zeile, aus welcher Nachricht er stammt, samt Logo des Dienstes. Tippe darauf, um den Thread zu lesen. Beim Entwurf wird das Logo des Ziels angezeigt. So erkennst du sofort, ob es eine Slack-Antwort oder eine E-Mail ist.

Wenn ein Entwurf auf einer Eingabe an anderer Stelle basiert, etwa einem Vorschlag eines Teammitglieds in Slack, steht das in einer Zeile, etwa „Basierend auf Sam in #ops“. Tippe darauf, um die Nachricht zu lesen. Sie verschwindet, wenn eine Aktualisierung den Entwurf ersetzt.

Ein Chat (Slack, WhatsApp, Telegram, Intercom…) wird als eine Unterhaltung angezeigt, mit den ältesten Nachrichten zuerst: den Nachrichten vor der Nachricht, um die es bei der Aufgabe geht, und den Antworten danach. In WhatsApp, Telegram oder Signal stehen deine Nachrichten wie in der App rechts. Die Nachricht zur Aufgabe ist mit „Diese Aufgabe“ markiert und wird geöffnet angezeigt. Mit **Frühere Nachrichten anzeigen** kommen ältere Nachrichten hinzu. Bei einer E-Mail wird der restliche Thread ober- und unterhalb der Nachricht eingeklappt angezeigt.

Eine Nachricht lässt sich auf dieselbe Weise über die Suche, den Graph, die Antworten von Ask oder die letzte Prüfung öffnen. Sie ist mit „Diese Nachricht“ oder „Neue Nachrichten“ markiert.

Mit **In Gmail öffnen** wird die E-Mail in dem Gmail-Konto geöffnet, an das sie gesendet wurde. Auf Android wird sie in der Gmail-App geöffnet, wenn du diese installiert hast.

Unter **Details** einer E-Mail stehen nur Angaben, die nicht bereits in ihrer Kopfzeile stehen, etwa vollständige Cc-Adressen, Bcc oder eine abweichende Antwortadresse. Gibt es nichts hinzuzufügen, werden keine Details angezeigt.

Bei einer Antwort in einem Slack-Thread wird auch angezeigt, was vor Beginn des Threads gesagt wurde. Auch über den Link einer Aufgabe zu ihrer eigenen Nachricht kannst du sie hier öffnen. Unten findest du **In Slack öffnen**.

Unter **Details** stehen Name, Projekt und Bereich (tippe darauf, um etwas zu ändern), deine letzte Notiz und das Ergebnis eines Coding-Agenten. Über den Titel öffnest du den Chat. Eine erledigte Aufgabe bleibt kompakt. Die Nachricht, aus der sie hervorgegangen ist, steht unter **Details**.

Bei einer Aufgabe mit „Wartet auf“ führt der Link zu deiner letzten Nachricht an die Person, auf deren Antwort du wartest: „E-Mail an Pat · Di“.

## Selbst eine Aufgabe erstellen

Mit **Neue Aufgabe** (unter **Suchen** auf einem Computer, **+** auf einem Handy oder `N`) kannst du eine Aufgabe für alles Mögliche erstellen. Beim Erstellen wird nichts gesendet. Wenn du weder **Arbeit** noch **Privat** auswählst, wird die Aufgabe dem passenden Bereich zugeordnet, je nachdem, um wen und was es geht. Sie findet auch die E-Mail, zu der sie gehört, selbst wenn diese älter ist.

Wenn du die Aufgabe schließt, bevor du sie hinzugefügt hast, bleiben dein Text und deine Auswahl beim nächsten Mal erhalten, Dateien jedoch nicht. Mit **Verwerfen** in der Meldung werden sie verworfen.

- **Fällig**: Gib einen Tag oder eine Uhrzeit ein, etwa „morgen“, „nächsten Fr“, „3. Nov.“, „14 Uhr“ oder „in 2 Stunden“, auch in deiner eigenen Sprache. Über das Kalendersymbol findest du Schnelloptionen und **Datum wählen**.
- **Wiederholt sich**: Die Aufgabe kommt regelmäßig zurück. Mehr dazu unter [Wiederkehrende Aufgaben](recurring.md).
- **Person**: Verknüpfe bis zu 5 Personen oder Unternehmen, um die es geht.
- Nachrichtensymbol: Hänge die Nachricht an, um die es geht: eine E-Mail, Slack-, Teams-, WhatsApp-, Telegram- oder eine andere Nachricht, auf die The Machine zugreifen kann. Suche nach Text oder Absender. Bei jedem Ergebnis werden Quelle, Absender und Zeitpunkt angezeigt.
- **Dateien**: Tippe auf die Büroklammer, füge einen Screenshot ein oder ziehe Dateien in das Formular. Auf einem Handy kannst du mit der Kamera daneben ein Foto aufnehmen. Bis zu 5 Dateien, wie im Chat (siehe [Dateien hinzufügen](card-chat.md#add-files)). Mit × entfernst du eine Datei wieder.

Die Dateien bleiben bei der Aufgabe, und The Machine liest sie, während sie daran arbeitet. Dateien allein reichen: Aus einer PDF- oder Textdatei erstellt sie die Aufgabe. Ein Foto wird als kleines Bild angezeigt. Tippe darauf, um es in voller Größe anzusehen.
