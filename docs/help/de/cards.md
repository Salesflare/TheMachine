---
title: Aufgaben
area: cards
summary: Eine Aufgabe für jedes Anliegen, das dich braucht, bereit für dein Ja. Was die einzelnen Teile einer Aufgabe bedeuten.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: baa6b797e040a271
---
Deine Machine liest alles Neue und erstellt nur dann eine Aufgabe, wenn etwas dich braucht. Eine Aufgabe pro Anliegen, egal über wie viele Nachrichten es sich erstreckt.

## Wo Aufgaben zu finden sind

Auf der Seite **Aufgaben** sind sie gruppiert:

- **Gerade erledigt**: Ganz oben wird ein letzter Schritt angezeigt, den du bestätigt hast. Zum Beispiel wurde ein Formular abgeschickt oder ein Problem gelöst, während du nicht da warst. Die Aufgabe bleibt dort, bis du auf **Verstanden** tippst, höchstens einen Tag lang. Du bekommst auch eine Benachrichtigung auf dein Smartphone.
- **Für dich**: Alles, worauf du reagieren musst, nach Dringlichkeit sortiert. Bei jeder Aufgabe steht **Vorbereitet** (die Arbeit ist erledigt und mit **Ausführen** oder **Senden** wird sie abgeschlossen), **Braucht dich** (zuerst ist deine Entscheidung oder Antwort nötig), **Wird vorbereitet…** (deine Machine arbeitet daran) oder **Zum Lesen** (eine Zusammenfassung oder ein Briefing, zu dem du nichts entscheiden musst).
- **Wartet auf andere**: Zugeklappte Aufgaben, bei denen der nächste Schritt bei jemand anderem liegt (siehe unten).
- **Kommt später zurück**: Zurückgestellte Aufgaben und Aufgaben, auf die du nicht mit **Noch nötig?** geantwortet hast (siehe unten).
- **Versprechen**: Was du versprochen hast und was andere dir versprochen haben. Siehe [Versprechen](promises.md).
- **Erledigt / verworfen**: Alle abgeschlossenen Aufgaben, neueste zuerst, mit dem Zeitpunkt des Abschlusses, zum Beispiel „Vor 5 Minuten erledigt“. Aufgaben, die schon abgeschlossen zu sein scheinen, sind als **Scheinbar erledigt** markiert.

Nachdem du etwas gesendet hast, steht in einer kurzen Mitteilung, wohin die Aufgabe verschoben wurde, zum Beispiel „Gesendet. Zu Erledigt verschoben.“ oder „Gesendet. Bis Mo. zu Später verschoben.“ Mit **Öffnen** gelangst du zur Aufgabe. Über die Suche findest du Aufgaben anhand des Titels oder der Person, an die sie gegangen sind, auch unter Später und Erledigt.

Unter **Für dich** stehen zuerst Aufgaben, die überfällig sind oder bis morgen fällig werden, dann Fragen aus deiner Fleet, anschließend Nachfassaktionen eines Boards und danach alle übrigen Aufgaben. Innerhalb jeder Gruppe stehen die neuesten zuerst. Eine Aufgabe behält ihren Platz, während deine Machine sie vorbereitet und wenn sie erledigt ist. Nur ihre Markierung ändert sich. In den anderen geöffneten Gruppen stehen überfällige oder bis morgen fällige Aufgaben zuerst, danach die neuesten. Die Seitenleiste behält dieselbe Reihenfolge bei.

**Scheinbar erledigt** bedeutet, dass deine Machine sieht, dass eine Aufgabe abgeschlossen ist, zum Beispiel „PR #3451 wurde zusammengeführt“, sie aber noch nicht geschlossen wurde. Mit **Wieder öffnen** kommt sie zurück auf deine Liste, und deine Machine lernt daraus. Diese Aufgaben werden nie als überfällig angezeigt. Nach einem Tag wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Eine Aufgabe, die du selbst schon erledigt hast, zum Beispiel durch eine Antwort in Gmail oder Slack, wird ebenfalls automatisch geschlossen.

Wenn eine Nachricht von einer Adresse kommt, die nur wie die Adresse einer Person aussieht, die du kennst, zum Beispiel sam@acme-corp.example statt sam@acmecorp.example, steht es ausdrücklich in der Aufgabe: „Das ist nicht Sam Lee.“ Die Person wird mit ihrer tatsächlichen Adresse angezeigt, nie mit dem Namen, den sie verwendet hat. Deine Machine überprüft solche Nachrichten bei der Person unter der Adresse, die du bereits hast, nie bei der absendenden Person.

Bei einer Aufgabe, die noch auf jemand anderen wartet, zum Beispiel auf eine Prüfung oder Antwort, steht **Wartet auf:** und der nächste Schritt. Die Aufgabe bleibt zugeklappt unter **Wartet auf andere**, oberhalb von „Kommt später zurück“, bis eine neue Nachricht sie wieder hervorholt. Das gilt auch, nachdem du eine Rückfrage gestellt hast: Die Aufgabe kommt am Morgen vor der Frist zurück, bei einer Frist noch am selben Tag zum Zeitpunkt der Frist oder am nächsten Morgen, wenn die Frist bereits verstrichen ist. Außerdem steht dabei, auf wen sie noch wartet.

Wenn es bei einer Aufgabe um ein Ergebnis geht, das jemand anderes liefern muss, zum Beispiel einen unterschriebenen Vertrag, wird es unter **Details** als **Fertig, wenn** angezeigt. Wenn du deinen Teil abschickst, wird die Aufgabe nicht geschlossen. Sie bleibt unter **Wartet auf andere**, bis eine Nachricht das Ergebnis bestätigt. Dann wird sie automatisch geschlossen und du kannst das mit **Rückgängig** rückgängig machen. Wenn bis zu dem Zeitpunkt, an dem du nachhaken solltest, nichts kommt, erscheint die Aufgabe wieder mit **Schreib eine kurze Erinnerung** in ihrem Chat. Sag im Chat, was als erledigt zählt, um das zu ändern.

Wenn eine Aufgabe eine Woche lang niemand angerührt hat, wird einmal gefragt: **Noch nötig?** Mit **Nicht nötig** wird sie geschlossen. Du kannst das mit **Rückgängig** rückgängig machen. Mit **Behalten** bleibt die Aufgabe bestehen und es wird nie wieder nachgefragt. Wenn du eine weitere Woche nicht antwortest, wird sie unter „Kommt später zurück“ zugeklappt und nicht mehr auf dem App-Symbol oder in der morgendlichen Zusammenfassung mitgezählt. Wenn du sie öffnest, eine Chatnachricht schreibst, sie bearbeitest oder zurückstellst oder eine neue Nachricht eingeht, kommt sie wieder zurück.

Einmal pro Woche kann für ein Projekt, bei dem nichts mehr offen ist und das zur Ruhe gekommen ist, eine Aufgabe mit einem konkreten nächsten Schritt erstellt werden. Höchstens drei pro Woche. Siehe [Projekte](projects.md).

Wenn dich nichts braucht, macht deine Machine ein Nickerchen und die Liste bleibt leer. Während einer Prüfung wird sie aktiv und zeigt an, dass sie prüft. Wenn eine Prüfung fehlgeschlagen ist oder sich verspätet, steht das in der Zeile. Darunter wird **Jetzt prüfen** angezeigt.

Mit **Alle**, **Arbeit** und **Privat** oben in der Seitenleiste kannst du alle Aufgaben oder nur eine der beiden Arten anzeigen. Auf Smartphone und Computer gilt dieselbe Auswahl. Wenn „Arbeit“ oder „Privat“ ausgewählt ist, führt **Alle anzeigen** zurück zur vollständigen Liste. Eine Benachrichtigung über deine Machine selbst, zum Beispiel über einen Teil, der immer wieder neu startet, gehört weder zu Arbeit noch zu Privat und wird nur unter „Alle“ angezeigt.

Die Zeile oben in der Liste wechselt auch direkt zur anderen Ansicht: Unter **Nur privat** kannst du auf **Arbeit** oder **Alle anzeigen** tippen.

In der Zeile oben in der Liste stehen der Name deiner letzten morgendlichen oder abendlichen Zusammenfassung und die Zahl der darin enthaltenen Aufgaben, zum Beispiel **Zusammenfassung von gestern Abend** · 12 erledigt, 3 offen. Tippe darauf, um die Zusammenfassung erneut zu lesen. Mit **Kopieren** kannst du sie an beliebiger Stelle einfügen. Sobald du sie öffnest oder auf das **×** tippst, wird sie auf allen deinen Geräten angezeigt, bis die nächste Zusammenfassung kommt.

Wenn es keine aktuelle Zusammenfassung gibt, wird **Heute bisher** angezeigt: Was heute erledigt wurde und was noch offen ist, für Arbeit und Privat oder nur für den ausgewählten Bereich.

Bei einer Aufgabe zu einem Projekt steht der Projektname unter dem Titel. Tippe darauf, um das Projekt zu öffnen. Unter **Details** kannst du mit **Projekt** das Projekt ändern oder entfernen. Siehe [Aufgaben eines Projekts](projects.md#a-project-s-to-dos).

Mit **Bereich** unter **Details** verschiebst du eine Aufgabe in deinen anderen Bereich. Was die Aufgabe lesen und senden darf, wird mitverschoben. Mit **Rückgängig** in der Mitteilung kannst du sie zurückverschieben.

Wenn eine Aufgabe deinen anderen Bereich braucht, um fortzufahren, und alle zugehörigen Nachrichten dort sind, wird sie automatisch dorthin verschoben und fortgesetzt. Andernfalls wird **Nach Arbeit verschieben** angezeigt und erst nach deinem Tippen wird etwas verschoben. Eine Aufgabe, die du ohne Auswahl von Arbeit oder Privat hinzugefügt hast, wird automatisch dem passenden Bereich zugeordnet, sobald deine Machine herausfindet, wo sie hingehört. Bis dahin gehört sie weder zu Arbeit noch zu Privat und bleibt privat.

Eine Aufgabe kann immer die Nachrichten lesen, aus denen sie entstanden ist. Wenn sie weitere Nachrichten aus deinem anderen Bereich braucht, fragt sie mit **Diese E-Mail für diese Aufgabe verwenden** danach. Ein Arbeits-Postfach, das du als Privat markiert hast, zählt als Privat. E-Mails für ein anderes deiner Unternehmen gehören zu den Aufgaben dieses Unternehmens. Eine Aufgabe zu deinem Privatleben, zum Beispiel eine Nachricht deiner Familie an deine Arbeitsadresse, ist von Anfang an privat.

Arbeit, die dich über ein privates Konto erreicht, zum Beispiel eine Nachricht eines Kunden auf WhatsApp oder eine Bestellung in deinem privaten Postfach, gehört von Anfang an zu Arbeit. Eine Aufgabe, die du selbst verschoben oder zugeordnet hast, bleibt immer dort, wo du sie abgelegt hast. Arbeit oder Privat bestimmt, wo eine Aufgabe angezeigt und mit wem sie geteilt wird, aber nie, wohin sie antwortet: Eine Antwort geht immer dorthin, wo die Unterhaltung stattfindet, auch nach dem Verschieben, es sei denn, du wählst einen anderen Weg.

Eine solche private Aufgabe antwortet weiterhin von der Arbeitsadresse, an die die E-Mail gesendet wurde, und wird nie in einer Work-Fleet oder im Team-Graph angezeigt.

Wenn mindestens zwei Aufgaben auf dich warten, kannst du mit **Durchgehen** in der Kopfzeile von „Für dich“ die Aufgaben der Reihe nach einzeln durchgehen. Die Reihenfolge entspricht der Liste. Jeder Entwurf wird vollständig angezeigt, mit **Senden** oder **Ausführen**, **Änderungen anfragen**, **Zurückstellen** und **Überspringen**. Am Computer sendet Enter den angezeigten Inhalt, `S` stellt zurück, `→` überspringt und Esc beendet. Unter dem Titel steht in der Kopfzeile auch, wie lange du in deinem eigenen Tempo dafür brauchst, zum Beispiel „etwa 2 Min.“

Eine Aufgabe, bei der dir eine Frage gestellt wird, wird bei beidem ausgelassen: Dafür braucht es deine Antwort, keinen Tipp.

## Jetzt prüfen

Deine Machine liest jede Quelle alle paar Minuten, Tag und Nacht. Sie prüft, was eingegangen ist, sobald 40 Nachrichten vorliegen oder die älteste Nachricht einer Person seit 15 Minuten wartet. Newsletter, Benachrichtigungen und Belege werden bei der nächsten Prüfung innerhalb einer Stunde berücksichtigt.

Nachts, von 00:00 bis 06:30 Uhr, werden Prüfungen pausiert. Neue Nachrichten werden weiterhin gelesen und gespeichert. Um 06:30 Uhr werden sie gemeinsam geprüft, damit deine Aufgaben vor der morgendlichen Zusammenfassung bereit sind. Unter „Verbindungen“ steht bei Prüfungen: „Nachts pausiert, wird um 06:30 Uhr nachgeholt.“ Wenn du nachts in der App klickst, etwas eingibst oder scrollst, im Chat schreibst oder auf eine Aufgabe tippst, laufen die Prüfungen wie gewohnt weiter, bis du eine Stunde lang nicht mehr aktiv warst. Mit **Jetzt prüfen** wird immer sofort geprüft.

Mit **Jetzt prüfen** werden alle Quellen sofort gelesen. Wenn nichts offen ist, tippe auf die Zeile deiner Machine, um sie mit **Details** anzuzeigen. Damit öffnest du „Prüfungen“ unter „Verbindungen“. Wenn Aufgaben offen sind, steht die Zeile am Computer ganz oben. Sie wird nur kurz angezeigt, solange eine Prüfung läuft oder wenn eine fehlgeschlagen ist oder sich verspätet. Du kannst auch im Chat danach fragen.

LinkedIn, X und Salesflare haben ihren eigenen Rhythmus.

## Letzte Prüfung

Nach einer Prüfung, bei der neue Nachrichten gelesen wurden, steht oberhalb deiner Aufgaben, was in allen gelesenen Quellen gefunden wurde, zum Beispiel „13 Nachrichten um 16:11 geprüft · nichts braucht dich“ oder „· 2 neue Aufgaben“. Wenn eine neue Aufgabe bis zu einem günstigeren Zeitpunkt zurückgestellt wird, zum Beispiel bis zur morgendlichen Zusammenfassung, steht dort auch bis wann: „1 Aufgabe bis morgen 08:30 zurückgestellt“.

Tippe auf die Zeile, um jeden E-Mail-Thread, Chat und jede Benachrichtigung mit dem Symbol der jeweiligen Quelle zu sehen: Wer geschrieben hat, den Betreff oder die ersten Wörter sowie die neue Aufgabe oder den Grund, warum nichts weiter nötig war, zum Beispiel „Nur in Cc, ein Teammitglied antwortet“ oder „Termin für Donnerstag steht schon“. Wenn die Prüfung nur einen vagen Grund ergeben hat, wird bei einem Thread kein Grund angezeigt. Tippe auf einen Eintrag, um ihn zu lesen.

Die ersten 10 Einträge werden angezeigt. Wenn du darunter tippst, erscheinen die übrigen. Eine Zahl hinter einem Namen, zum Beispiel (3), gibt an, wie viele neue Nachrichten der Chat enthält. Eine Smartphone-Benachrichtigung zu einer Nachricht, die schon in der Liste steht, wird nur einmal angezeigt. Die Zeile bleibt 12 Stunden nach der Prüfung sichtbar.

Gezählt werden nur E-Mails an dich. Deine eigenen Antworten werden als Kontext und für Versprechen gelesen, gelten aber nicht als neue E-Mails. E-Mails von The Machine an dich, zum Beispiel deine morgendliche Zusammenfassung oder eine Benachrichtigung über eine Fehlerbehebung, werden nie gelesen oder aufgelistet. E-Mails zu Abrechnungen, deiner Testphase oder einer Einladung werden wie gewohnt gelesen.

## Die Schaltflächen

Bei einer Aufgabe wird der nächste Schritt angezeigt, zum Beispiel **Ausführen** oder **Prüfen und senden**, daneben steht **Zurückstellen**. Siehe [Ausführen](do-it.md) und [Zurückstellen](snooze.md).

Mit **Änderungen anfragen** kannst du angeben, was geändert werden soll: wie die Aufgabe erledigt werden soll oder, sobald ein Entwurf bereit ist, was daran geändert werden soll. **Als erledigt markieren** bedeutet, dass die Aufgabe erledigt ist. Bei einer vorbereiteten Aufgabe ohne Entwurf wird die Schaltfläche direkt angezeigt, ansonsten oben unter **…**, auch bei Aufgaben, die deine Entscheidung brauchen. Die Aufgabe wird sofort aus der Liste entfernt. In der Mitteilung kannst du das mit **Rückgängig** rückgängig machen. Wische die Mitteilung weg oder ziehe sie mit der Maus aus dem Fenster, um sie schneller zu schließen. Die Änderung bleibt bestehen.

Wenn die Aufgabe anders erledigt werden soll, sag es im **Chat**.

Unter **…**:

- **Übergeben…**: Übergib die Aufgabe einem Teammitglied, [Claude Code oder Codex](hand-to-agent.md) oder [bitte jemanden um eine Prüfung](ask-to-review.md).
- **Wiederholen…**: Die Aufgabe [kommt regelmäßig wieder](recurring.md).
- **Nicht nötig**: Die Aufgabe wird entfernt. Du kannst optional den Grund auswählen: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Tippe auf den Titel oder unter **Details** auf **Name**, um die Aufgabe umzubenennen. Dein Titel bleibt erhalten.

Mit **Wieder öffnen** holst du eine geschlossene Aufgabe zurück. Sie kommt auch automatisch zurück, wenn etwas Neues passiert, zum Beispiel wenn die Person dir eine neue Nachricht schickt, aber nicht, wenn du selbst antwortest.

Eine Rechnung, die du selbst noch bezahlen musst, wird unabhängig vom Land zu einer Aufgabe mit dem Betrag, dem Fälligkeitsdatum und den Zahlungsangaben auf der Rechnung. Automatisch bezahlte Rechnungen, zum Beispiel per Lastschrift oder mit einer gespeicherten Karte, werden nicht zu Aufgaben. Wenn eine spätere E-Mail zeigt, dass die Rechnung bezahlt wurde, zum Beispiel eine Bestätigung des Zahlungseingangs vom Absender, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Eine Aufgabe, die nur bis zu einem bestimmten Zeitpunkt wichtig ist, zum Beispiel eine Bestätigung vor einem Termin, wird danach automatisch geschlossen. Sie wird unter **Erledigt / verworfen** als „Nicht mehr nötig“ abgelegt. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Bevor eine Nachricht oder Übergabe für jemanden als bereit angezeigt wird, prüft deine Machine deine letzten Chats mit den beteiligten Personen, auch Gruppenchats, und wartet, bis Slack sie gelesen hat. Wenn eine spätere Nachricht zeigt, dass die Aufgabe schon erledigt ist, zum Beispiel weil jemand gefragt wurde und zugesagt hat, wird sie automatisch geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Wenn eine neuere Nachricht den Plan ändert, zum Beispiel wenn eine Party an einen anderen Ort verlegt oder eine Buchung storniert wurde, aktualisiert The Machine ihre Aufgaben selbst. Eine Aufgabe, die noch wichtig ist, folgt dem neuen Plan. Wenn nichts mehr zu tun ist, wird sie unter **Erledigt / verworfen** als „Nicht nötig“ abgelegt. Im Chat steht „Aktualisiert:“ mit dem Grund. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Bei deinen ersten Aufgaben erscheint ein kurzer Tipp zu den wichtigsten Aktionen: **Änderungen anfragen** und **Nicht nötig**. Außerdem wird darauf hingewiesen, dass nichts gesendet wird, bevor du auf **Senden** tippst. Ein Tipp verschwindet dauerhaft, sobald du die entsprechende Schaltfläche verwendest oder auf × tippst.

An deinem ersten Tag begrüßt dich deine Machine oben in „Aufgaben“ und nennt die Person, die am längsten auf deine Antwort wartet. Der Entwurf für diese Antwort wird zuerst erstellt und ist bereit, wenn du da bist.

Jede Aufgabe beginnt mit ihrem Titel. In der Zeile darunter stehen die Person, um die es geht, die Organisation, falls die Aufgabe eine betrifft (nicht allein deshalb, weil jemand dort arbeitet), das Projekt, Arbeit oder Privat und der Eingangszeitpunkt. Tippe auf einen Namen, um die entsprechende Seite im Graph zu öffnen.

Bei Namen und Organisationen wird das Foto oder Logo angezeigt, sofern es im Graph vorhanden ist. Andernfalls werden die Initialen angezeigt. Wenn ein Logo in dieser Größe nicht lesbar wäre, zum Beispiel weiße Schrift auf transparentem Hintergrund oder ein breites Wortlogo, wird auch die Initiale angezeigt.

Manchmal steht in einer unauffälligen Zeile, was nicht bekannt ist, zum Beispiel „Letzter Kontakt vor 12 Tagen per E-Mail, danach nichts.“ Das wird angezeigt, wenn der letzte Kontakt schon lange zurückliegt oder noch unbeantwortet ist. Auch nicht verbundene Kanäle wie WhatsApp werden genannt. Deine Machine sagt, was sie nicht weiß, statt zu raten.

Wenn ein nicht verbundener Kanal genannt wird, öffnet **Verbinden** daneben die entsprechende Verbindung.

Der Titel beschreibt, was zu tun ist, und ändert sich nur, wenn sich das ändert. Eine erledigte Aufgabe behält ihren Titel. Darunter steht, wie sie abgeschlossen wurde, zum Beispiel „Erledigt: Sam hat es am Dienstag unterschrieben“.

Über dem Entwurf steht in einer blassen Zeile die Nachricht, aus der die Aufgabe entstanden ist, mit dem Logo des jeweiligen Dienstes. Tippe darauf, um den Thread zu lesen. Beim Entwurf wird das Logo des Ziels angezeigt. So siehst du sofort, ob es eine Slack-Antwort oder eine E-Mail ist.

Wenn der Entwurf auf einer Eingabe an anderer Stelle beruht, zum Beispiel auf dem Vorschlag eines Teammitglieds in Slack, steht das in einer Zeile, zum Beispiel „Basierend auf Sam in #ops“. Tippe darauf, um die Nachricht zu lesen.

Ein Chat (Slack, WhatsApp, Telegram, Intercom…) wird als eine Unterhaltung angezeigt, älteste Nachricht zuerst: mit den Nachrichten vor der Nachricht, um die es in der Aufgabe geht, und den Antworten danach. In WhatsApp, Telegram oder Signal stehen deine Nachrichten rechts, wie in der App. Die Nachricht zur Aufgabe ist als „Diese Aufgabe“ markiert und wird in der Ansicht geöffnet. Mit **Frühere Nachrichten anzeigen** werden ältere Nachrichten eingeblendet. Bei einer E-Mail wird der übrige Thread ober- und unterhalb der Nachricht zugeklappt angezeigt.

Mit **In Gmail öffnen** öffnest du die E-Mail im Gmail-Konto, in dem sie eingegangen ist. Auf Android wird sie in der Gmail-App geöffnet, wenn diese installiert ist.

Unter **Details** einer E-Mail stehen nur Angaben, die nicht bereits in ihrem Header zu sehen sind, zum Beispiel vollständige Cc-Adressen, Bcc oder eine andere Antwortadresse. Wenn es nichts hinzuzufügen gibt, wird nichts angezeigt.

Bei einer Antwort in einem Slack-Thread wird auch angezeigt, was vor Beginn des Threads gesagt wurde. Über den Link einer Aufgabe zur zugehörigen Nachricht kannst du sie hier ebenfalls öffnen. Unten steht **In Slack öffnen**.

Unter **Details** stehen Name, Projekt und Bereich (tippe auf einen Eintrag, um ihn zu ändern), deine letzte Notiz und das Ergebnis eines Coding-Agenten. Über den Titel öffnest du den Chat. Eine erledigte Aufgabe bleibt kompakt. Die Nachricht, aus der sie entstanden ist, findest du unter **Details**.

Bei einer Aufgabe mit „Wartet auf“ ist deine letzte Nachricht an die Person verlinkt, auf deren Antwort du wartest: „E-Mail an Pat · Di“.

## Selbst eine Aufgabe erstellen

Mit **Neue Aufgabe** (am Computer unter **Suchen**, auf dem Smartphone über **+** oder mit `N`) kannst du eine Aufgabe zu einem beliebigen Thema hinzufügen. Beim Erstellen wird nichts gesendet. Wenn du weder **Arbeit** noch **Privat** auswählst, wird die Aufgabe anhand der beteiligten Personen und des Themas dem passenden Bereich zugeordnet. Außerdem findet die Funktion die E-Mail, auf die sich die Aufgabe bezieht, auch wenn sie schon älter ist.

- **Fällig**: Gib einen Tag oder eine Uhrzeit ein, zum Beispiel „morgen“, „nächsten Fr“, „3. Nov.“, „14 Uhr“ oder „in 2 Stunden“. Das geht auch in deiner Sprache. Über das Kalendersymbol kannst du einen schnellen Vorschlag oder **Datum wählen** auswählen.
- **Wiederholt sich**: Die Aufgabe kommt regelmäßig wieder. Siehe [Wiederkehrende Aufgaben](recurring.md).
- **Person**: Verknüpfe bis zu 5 Personen oder Unternehmen, um die es geht.
- Nachrichtensymbol: Hänge die Nachricht an, um die es geht. Das kann eine E-Mail, Slack-, Teams-, WhatsApp-, Telegram- oder eine andere Nachricht sein, auf die The Machine zugreifen kann. Suche nach Text oder Absender. Bei jedem Ergebnis werden Quelle, Absender und Zeitpunkt angezeigt.
- **Dateien**: Tippe auf die Büroklammer, füge einen Screenshot ein oder ziehe Dateien auf das Formular. Auf einem Smartphone kannst du mit der Kamera daneben ein Foto aufnehmen. Bis zu 5 Dateien, wie im Chat (siehe [Dateien hinzufügen](card-chat.md#add-files)). Mit × kannst du eine Datei wieder entfernen.

Die Dateien bleiben bei der Aufgabe und The Machine liest sie, während sie daran arbeitet. Dateien allein reichen aus: Aus einer PDF- oder Textdatei erstellt sie die Aufgabe. Ein Foto wird als kleines Bild angezeigt. Tippe darauf, um es in voller Größe anzusehen.
