---
title: Aufgaben
area: cards
summary: Eine Aufgabe für alles, was dich braucht, bereit für dein Ja. Hier erfährst du, was die einzelnen Teile einer Aufgabe bedeuten.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 81b65d513aa5941b
---
Deine Machine liest alles Neue und erstellt nur dann eine Aufgabe, wenn etwas dich braucht. Eine Aufgabe pro Anliegen, egal über wie viele Nachrichten es sich erstreckt.

## Wo Aufgaben zu finden sind

Auf der Seite **Aufgaben** sind sie gruppiert:

- **Gerade erledigt**: Ganz oben siehst du den letzten Schritt, den du bestätigt hast, etwa ein Formular oder ein Problem, das während deiner Abwesenheit bearbeitet wurde. Er bleibt höchstens einen Tag sichtbar, bis du auf **Verstanden** tippst. Dein Smartphone erhält ebenfalls eine Benachrichtigung.
- **Für dich**: Alles, worauf du reagieren musst, zuerst das Dringendste. Jede Aufgabe ist mit **Vorbereitet** gekennzeichnet (die Arbeit ist erledigt, und mit **Ausführen** oder **Senden** wird sie ausgeführt), **Braucht dich** (zuerst braucht es deine Entscheidung oder Antwort), **Wird vorbereitet…** (deine Machine arbeitet daran) oder **Zum Lesen** (eine Zusammenfassung oder ein Briefing, bei dem du nichts entscheiden musst).
- **Wartet auf andere**: Eingeklappte Aufgaben, bei denen der nächste Schritt bei jemand anderem liegt (siehe unten).
- **Kommt später zurück**: Zurückgestellte Aufgaben und Aufgaben ohne Antwort auf **Noch nötig?** (siehe unten).
- **Versprechen**: Was du anderen versprochen hast und was andere dir versprochen haben. Weitere Informationen findest du unter [Versprechen](promises.md).
- **Erledigt / verworfen**: Alle abgeschlossenen Aufgaben, neueste zuerst, mit dem Zeitpunkt des Abschlusses, zum Beispiel „Vor 5 Minuten erledigt“. Aufgaben, die anscheinend schon erledigt sind, sind mit **Scheinbar erledigt** gekennzeichnet.

Nachdem du etwas gesendet hast, zeigt eine kurze Meldung, wohin die Aufgabe verschoben wurde, zum Beispiel „Gesendet. Nach Erledigt verschoben.“ oder „Gesendet. Bis Mo. nach Später verschoben.“ Mit **Öffnen** gelangst du zur Aufgabe. Über die Suche findest du Aufgaben nach Titel oder Empfänger, auch unter Später und Erledigt.

Unter **Für dich** stehen zuerst überfällige Aufgaben oder Aufgaben mit Fälligkeit bis morgen, dann Fragen aus deiner Fleet, danach Folgeaufgaben aus einem Board und anschließend der Rest. Innerhalb jeder Gruppe stehen die neuesten zuerst. Eine Aufgabe behält ihren Platz, während deine Machine sie vorbereitet und auch nach dem Erledigen. Nur ihre Kennzeichnung ändert sich. In den anderen offenen Gruppen stehen überfällige Aufgaben oder Aufgaben mit Fälligkeit bis morgen zuerst, der Rest nach Aktualität. Die Seitenleiste behält dieselbe Reihenfolge bei.

**Scheinbar erledigt** bedeutet, dass deine Machine erkennt, dass etwas erledigt ist, zum Beispiel „PR #3451 wurde zusammengeführt“, die Aufgabe aber noch nicht geschlossen ist. Mit **Wieder öffnen** kommt sie zurück in deine Liste, und deine Machine lernt daraus. Solche Aufgaben werden nie als überfällig angezeigt. Nach einem Tag wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Eine Aufgabe, die du bereits selbst erledigt hast, etwa durch eine Antwort in Gmail oder Slack, wird ebenfalls automatisch geschlossen.

Wenn eine Nachricht von einer Adresse kommt, die nur wie die Adresse einer bekannten Person aussieht, etwa sam@acme-corp.example statt sam@acmecorp.example, weist die Aufgabe deutlich darauf hin: „Das ist nicht Sam Lee.“ Die Person wird mit ihrer tatsächlichen Adresse angezeigt, niemals mit dem Namen, den sie verwendet hat. Deine Machine überprüft solche Nachrichten bei der Person unter der Adresse, die du bereits hast, niemals bei der schreibenden Person.

Bei einer Aufgabe, bei der noch jemand anderes am Zug ist, etwa mit einer Prüfung oder Antwort, steht **Wartet auf:** und der entsprechende Schritt. Sie wird eingeklappt unter **Wartet auf andere** angezeigt, oberhalb von Kommt später zurück, bis eine neue Nachricht sie wieder hervorholt. Dasselbe gilt, wenn du eine Rückfrage gestellt hast: Die Aufgabe kommt am Morgen vor dem Fälligkeitstermin zurück, am Fälligkeitstag, wenn dieser noch heute ist, oder am nächsten Morgen, wenn der Termin bereits verstrichen ist. Sie zeigt dann, auf wen sie noch wartet.

Wenn es bei einer Aufgabe um ein Ergebnis geht, das jemand anderes liefern muss, etwa einen unterschriebenen Vertrag, wird es unter **Details** als **Fertig, wenn** angezeigt. Wenn du deinen Teil abschickst, wird die Aufgabe nicht geschlossen. Sie bleibt unter **Wartet auf andere**, bis eine Nachricht das Ergebnis bestätigt. Dann wird sie automatisch geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Wenn bis zum Zeitpunkt, an dem du nachhaken solltest, nichts eingegangen ist, kommt sie mit **Schreib eine kurze Erinnerung** in ihrem Chat zurück. Schreib im Chat, was als erledigt gilt, um das zu ändern.

Wenn eine Aufgabe eine Woche lang unbeachtet bleibt, fragt sie einmal: **Noch nötig?** Mit **Nicht nötig** wird sie geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Mit **Behalten** bleibt sie bestehen, und es wird nicht noch einmal nachgefragt. Wenn eine weitere Woche lang keine Antwort kommt, wird die Aufgabe unter Kommt später zurück eingeklappt. Die Zahl auf dem App-Symbol und in der morgendlichen Zusammenfassung zählt sie dann nicht mehr mit. Wenn du sie öffnest, eine Chatnachricht schreibst, sie bearbeitest oder zurückstellst oder eine neue Nachricht eingeht, kommt sie zurück.

Ein Projekt, bei dem es eine Woche lang ruhig war und keine Aufgaben offen sind, kann einmal pro Woche eine Aufgabe mit einem konkreten nächsten Schritt erhalten, höchstens drei pro Woche. Weitere Informationen findest du unter [Projekte](projects.md).

Wenn nichts deine Aufmerksamkeit braucht, wartet deine Machine mit einer leeren Liste. Während sie etwas überprüft, wird sie aktiv und zeigt das an. Wenn eine Überprüfung fehlgeschlagen ist oder sich verspätet, steht das in der Zeile. Darunter findest du **Jetzt prüfen**.

Mit **Alle**, **Arbeit** und **Privat** oben in der Seitenleiste kannst du alle Aufgaben oder nur eine Kategorie anzeigen. Auf Smartphone und Computer gilt dieselbe Auswahl. Wenn Arbeit oder Privat ausgewählt ist, bringt dich **Alle anzeigen** zurück zur Gesamtansicht. Eine Meldung über deine Machine selbst, etwa dass ein Teil immer wieder neu startet, gehört weder zu Arbeit noch zu Privat und wird nur unter Alle angezeigt.

Die Zeile oben in der Liste wechselt ebenfalls direkt zur anderen Ansicht: Unter **Nur privat** kannst du auf **Arbeit** oder **Alle anzeigen** tippen.

In der Zeile oben in der Liste stehen der Name deiner letzten morgendlichen oder abendlichen Zusammenfassung und die Anzahl der darin erfassten Aufgaben, zum Beispiel **Zusammenfassung von gestern Abend** · 12 erledigt, 3 offen. Tippe darauf, um die Zusammenfassung noch einmal zu lesen. Mit **Kopieren** kannst du sie an anderer Stelle einfügen. Sobald du sie öffnest oder auf ihr **×** tippst, wird sie auf all deinen Geräten angezeigt, bis die nächste Zusammenfassung kommt.

Wenn es keine aktuelle Zusammenfassung gibt, wird **Heute bisher** angezeigt: was heute erledigt wurde und was noch offen ist, für Arbeit und Privat oder nur für die ausgewählte Kategorie.

Bei einer Aufgabe zu einem Projekt wird der Projektname unter dem Titel angezeigt. Tippe darauf, um das Projekt zu öffnen. Unter **Details** kannst du mit **Projekt** das Projekt ändern oder entfernen. Weitere Informationen findest du unter [Aufgaben eines Projekts](projects.md#a-project-s-to-dos).

Mit **Bereich** unter **Details** verschiebst du eine Aufgabe in den anderen Bereich. Was sie lesen und senden darf, wird mitverschoben. Mit **Rückgängig** in der Meldung kannst du sie zurückverschieben.

Wenn eine Aufgabe den anderen Bereich braucht, um fortgesetzt zu werden, und alle zugehörigen Nachrichten bereits dort sind, wird sie automatisch dorthin verschoben und fortgesetzt. Andernfalls wird **Nach Arbeit verschieben** angezeigt, und erst wenn du darauf tippst, wird etwas verschoben. Eine Aufgabe, die du hinzugefügt hast, ohne Arbeit oder Privat auszuwählen, wird automatisch dem passenden Bereich zugewiesen, sobald klar ist, wo sie hingehört. Bis dahin gehört sie weder zu Arbeit noch zu Privat und bleibt privat.

Eine Aufgabe kann die Nachrichten, aus denen sie entstanden ist, immer lesen. Wenn sie weitere Nachrichten aus deinem anderen Bereich braucht, fragt sie mit **Diese E-Mail für diese Aufgabe verwenden** danach. Ein Arbeits-Postfach, das du als Privat gekennzeichnet hast, zählt als Privat. E-Mails für ein anderes deiner Unternehmen werden den Aufgaben dieses Unternehmens zugeordnet. Eine Aufgabe zu deinem Privatleben, etwa wenn deine Familie an deine Arbeitsadresse schreibt, gehört von Anfang an zu Privat.

Arbeit, die dich über ein privates Konto erreicht, etwa eine Nachricht von einem Kunden auf WhatsApp oder eine Bestellung in deinem privaten Postfach, gehört von Anfang an zu Arbeit. Eine Aufgabe, die du selbst verschoben oder zugeordnet hast, bleibt immer dort, wo du sie abgelegt hast. Arbeit oder Privat bestimmt, wo eine Aufgabe angezeigt und mit wem sie geteilt wird, nicht aber, wohin sie antwortet: Eine Antwort geht immer dorthin, wo das Gespräch stattfindet, auch nach einem Verschieben, es sei denn, du wählst eine andere Möglichkeit.

Eine solche Aufgabe unter Privat antwortet trotzdem über die Arbeitsadresse, an die ihre E-Mail gesendet wurde. Sie wird niemals in einer Work Fleet oder im Team Graph angezeigt.

Wenn mindestens zwei Aufgaben auf dich warten, kannst du sie mit **Durchgehen** in der Kopfzeile von Für dich nacheinander in der Reihenfolge der Liste bearbeiten. Jeder Entwurf wird vollständig angezeigt, zusammen mit **Senden** oder **Ausführen**, **Änderungen anfragen**, **Zurückstellen** und **Überspringen**. Am Computer sendet die Eingabetaste den angezeigten Inhalt, `S` stellt zurück, `→` überspringt und Esc bricht ab. Unter dem Titel zeigt die Kopfzeile außerdem an, wie lange es in deinem eigenen Tempo dauert, zum Beispiel „etwa 2 Min.“.

Eine Aufgabe, die dir eine Frage stellt, wird in beiden Fällen ausgelassen: Sie wartet auf deine Antwort, nicht auf einen Tipp.

## Jetzt prüfen

Deine Machine liest jede Quelle alle paar Minuten, Tag und Nacht. Sie prüft neue Nachrichten, sobald 40 Nachrichten eingegangen sind oder die älteste Nachricht einer Person seit 15 Minuten wartet. Newsletter, Benachrichtigungen und Belege werden innerhalb einer Stunde bei der nächsten Überprüfung berücksichtigt.

Nachts, von 00:00 bis 06:30 Uhr, pausieren die Überprüfungen. Neue Nachrichten werden weiterhin gelesen und gespeichert. Um 06:30 Uhr werden sie gemeinsam überprüft, damit deine Aufgaben vor der morgendlichen Zusammenfassung bereit sind. Unter Verbindungen steht bei den Überprüfungen „Für die Nacht pausiert, Fortsetzung um 06:30“. Wenn du nachts die App öffnest, im Chat schreibst oder auf eine Aufgabe tippst, laufen die Überprüfungen wieder wie gewohnt, bis du eine Stunde lang abwesend bist. Mit **Jetzt prüfen** wird immer sofort geprüft.

Mit **Jetzt prüfen** werden alle Quellen sofort gelesen. Wenn keine Aufgaben offen sind, tippe auf die Zeile deiner Machine, um sie zusammen mit **Details** anzuzeigen. Damit öffnest du die Überprüfungen unter Verbindungen. Wenn Aufgaben offen sind, findest du die Zeile am Computer oben. Dort wird kurz etwas angezeigt, solange eine Überprüfung läuft oder eine fehlgeschlagen ist oder sich verspätet. Du kannst auch im Chat danach fragen.

LinkedIn, X und Salesflare haben ihren eigenen Rhythmus.

## Letzte Überprüfung

Nach einer Überprüfung, bei der neue Nachrichten gelesen wurden, steht über deinen Aufgaben, was gefunden wurde und aus welchen Quellen, zum Beispiel „13 Nachrichten um 16:11 geprüft · nichts braucht dich“ oder „· 2 neue Aufgaben“. Wenn eine neue Aufgabe auf einen passenderen Zeitpunkt wartet, etwa auf deine morgendliche Zusammenfassung, steht dort bis wann: „1 Aufgabe bis morgen 08:30 zurückgestellt“.

Tippe auf die Zeile, um alle E-Mail-Unterhaltungen, Chats und Benachrichtigungen zu sehen, mit dem Symbol der jeweiligen Quelle: wer geschrieben hat, den Betreff oder die ersten Wörter sowie die neue Aufgabe oder den Grund, warum nichts nötig war. Zum Beispiel „Nur in cc, eine Teamkollegin antwortet“ oder „Termin für Donnerstag steht bereits“. Wenn die Überprüfung nur einen vagen Grund ergeben hat, wird kein Grund angezeigt. Tippe auf einen Eintrag, um ihn zu lesen.

Die ersten 10 Einträge werden angezeigt. Tippe darunter, um den Rest zu sehen. Eine Zahl nach einem Namen, etwa (3), gibt an, wie viele neue Nachrichten der Chat enthält. Eine Smartphone-Benachrichtigung über eine Nachricht, die bereits in der Liste steht, wird nur einmal angezeigt. Die Zeile bleibt 12 Stunden nach der Überprüfung sichtbar.

Gezählt werden nur E-Mails an dich. Deine eigenen Antworten werden als Kontext und für Versprechen gelesen, zählen aber nicht als neue E-Mails. E-Mails von The Machine an dich, etwa deine morgendliche Zusammenfassung oder ein Hinweis zu einer Fehlerbehebung, werden niemals gelesen oder aufgelistet. E-Mails zu Abrechnung, Testversion oder Einladung werden wie gewohnt gelesen.

## Die Schaltflächen

Eine Aufgabe zeigt ihren nächsten Schritt an, zum Beispiel **Ausführen** oder **Prüfen und senden**, daneben steht **Zurückstellen**. Weitere Informationen findest du unter [Ausführen](do-it.md) und [Zurückstellen](snooze.md).

Mit **Änderungen anfragen** kannst du angeben, was geändert werden soll: wie etwas erledigt werden soll oder, sobald ein Entwurf bereit ist, was daran geändert werden soll. **Als erledigt markieren** bedeutet, dass die Aufgabe erledigt ist. Bei einer vorbereiteten Aufgabe ohne Entwurf ist die Schaltfläche direkt sichtbar, andernfalls findest du sie oben unter **…**, auch bei Aufgaben, die deine Entscheidung brauchen. Die Aufgabe wird sofort aus der Liste entfernt. In der Meldung steht **Rückgängig**. Wische die Meldung weg oder ziehe sie am Computer mit der Maus aus der Ansicht, um sie schneller zu schließen. Die Änderung bleibt bestehen.

Wenn die Aufgabe anders erledigt werden soll, sag es im **Chat** dazu.

Unter **…**:

- **Übergeben…**: Übergib die Aufgabe an ein Teammitglied, an [Claude Code oder Codex](hand-to-agent.md) oder [bitte jemanden um eine Prüfung](ask-to-review.md).
- **Wiederholen…**: Die Aufgabe [kommt regelmäßig zurück](recurring.md).
- **Nicht nötig**: Die Aufgabe wird entfernt. Du kannst optional einen Grund auswählen: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Tippe auf den Titel oder unter **Details** auf **Name**, um die Aufgabe umzubenennen. Dein Titel bleibt erhalten.

Mit **Wieder öffnen** holst du eine geschlossene Aufgabe zurück. Sie kommt auch automatisch zurück, wenn etwas Neues passiert, etwa eine neue Nachricht von der Person, aber nicht bei deiner eigenen Antwort.

Eine Rechnung, die du selbst bezahlen musst, wird unabhängig vom Land zu einer Aufgabe mit Betrag, Fälligkeitsdatum und den Zahlungsdetails auf der Rechnung. Automatisch bezahlte Rechnungen, etwa per Lastschrift oder mit einer gespeicherten Karte, werden nicht als Aufgabe angelegt. Wenn eine spätere E-Mail bestätigt, dass die Rechnung bezahlt wurde, etwa eine Nachricht des Absenders über den Zahlungseingang, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang zurückholen.

Eine Aufgabe, die nur bis zu einem bestimmten Zeitpunkt wichtig war, etwa eine Bestätigung vor einem Meeting, wird nach diesem Zeitpunkt automatisch geschlossen. Sie wird unter **Erledigt / verworfen** als „Nicht mehr nötig“ angezeigt. Mit **Rückgängig** kannst du sie einen Tag lang zurückholen.

Bevor eine Nachricht oder Übergabe an jemanden als bereit angezeigt wird, prüft deine Machine deine letzten Chats mit den beteiligten Personen, auch Gruppenchats, und wartet darauf, dass Slack sie gelesen hat. Wenn eine spätere Nachricht zeigt, dass die Aufgabe bereits erledigt ist, etwa weil die Person gefragt wurde und zugesagt hat, wird sie automatisch geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang zurückholen.

Wenn eine neuere Nachricht den Plan ändert, etwa weil eine Feier an einen anderen Ort verlegt oder eine Buchung storniert wurde, aktualisiert The Machine ihre Aufgaben selbst. Eine Aufgabe, die weiterhin wichtig ist, folgt dem neuen Plan. Wenn nichts mehr zu tun ist, wird sie unter **Erledigt / verworfen** als „Nicht nötig“ angezeigt. In ihrem Chat steht „Aktualisiert:“ mit einer Begründung. Mit **Rückgängig** kannst du sie einen Tag lang zurückholen.

Bei deinen ersten Aufgaben wird ein kurzer Tipp zu den wichtigsten Aktionen angezeigt: **Änderungen anfragen** und **Nicht nötig**. Außerdem erfährst du, dass nichts versendet wird, bevor du auf **Senden** tippst. Ein Tipp verschwindet endgültig, sobald du die zugehörige Schaltfläche verwendest oder auf × tippst.

Am ersten Tag begrüßt dich deine Aufgabenliste oben und nennt die Person, die am längsten auf deine Antwort wartet. Der Entwurf für diese Antwort wird zuerst erstellt, damit er bereit ist, wenn du kommst.

Jede Aufgabe beginnt mit ihrem Titel. In der Zeile darunter steht, um wen es geht, die Organisation, wenn es um eine Organisation geht, aber nicht nur, weil jemand dort arbeitet, das Projekt, Arbeit oder Privat und wann die Aufgabe eingegangen ist. Tippe auf einen Namen, um die Personenseite im Graph zu öffnen.

Bei Namen und Organisationen wird das Foto oder Logo angezeigt, falls im Graph vorhanden, ansonsten die Initialen. Wenn ein Logo in dieser Größe nicht gut lesbar wäre, etwa weiße Schrift auf transparentem Hintergrund oder ein breites Wortlogo, wird stattdessen ebenfalls die Initiale angezeigt.

Manchmal steht in einer unauffälligen Zeile, was nicht bekannt ist, etwa „Letzter Kontakt vor 12 Tagen per E-Mail, seither nichts“. Das wird angezeigt, wenn der letzte Kontakt schon länger zurückliegt oder unbeantwortet ist. Außerdem werden nicht verbundene Kanäle wie WhatsApp genannt. Deine Machine sagt, was sie nicht weiß, statt zu raten.

Wenn ein nicht verbundener Kanal genannt wird, öffnet **Verbinden** daneben die entsprechende Verbindung.

Der Titel beschreibt, was zu tun ist, und ändert sich nur, wenn sich die Aufgabe ändert. Eine erledigte Aufgabe behält ihren Titel. Darunter steht, wie sie erledigt wurde, etwa „Erledigt: Sam hat es am Dienstag unterschrieben“.

Über dem Entwurf steht in einer dezenten Zeile die Nachricht, aus der die Aufgabe entstanden ist, mit dem Logo des jeweiligen Dienstes. Tippe darauf, um die Unterhaltung zu lesen. Beim Entwurf wird das Logo des Zielorts angezeigt, damit du sofort siehst, ob es eine Slack-Antwort oder eine E-Mail ist.

Wenn der Entwurf auf einer Eingabe an anderer Stelle beruht, etwa einem Vorschlag eines Teammitglieds in Slack, steht das in einer Zeile, zum Beispiel „Basiert auf Sam in #ops“. Tippe darauf, um die Nachricht zu lesen.

Ein Chat (Slack, WhatsApp, Telegram, Intercom …) wird als eine Unterhaltung angezeigt, vom ältesten zum neuesten Eintrag: mit den Nachrichten vor dem Anlass der Aufgabe und den darauf folgenden Antworten. In WhatsApp, Telegram oder Signal stehen deine Nachrichten wie in der App rechts. Die Nachricht, zu der die Aufgabe gehört, ist mit „Diese Aufgabe“ gekennzeichnet und wird direkt angezeigt. Mit **Frühere Nachrichten anzeigen** werden ältere Nachrichten eingeblendet. Bei E-Mails ist der restliche Verlauf darüber und darunter eingeklappt.

Unter **Details** einer E-Mail stehen nur Informationen, die nicht bereits in der Kopfzeile zu sehen sind, etwa vollständige Cc-Adressen, Bcc oder eine abweichende Antwortadresse. Wenn es nichts Weiteres gibt, wird der Abschnitt nicht angezeigt.

Bei einer Antwort in einem Slack-Thread wird auch angezeigt, was vor dem Start des Threads gesagt wurde. Über den Link einer Aufgabe zur zugehörigen Nachricht kannst du diese ebenfalls hier öffnen. Unten findest du **In Slack öffnen**.

Unter **Details** werden Name, Projekt und Bereich angezeigt. Tippe auf einen davon, um ihn zu ändern. Dort findest du auch deine letzte Notiz und das Ergebnis eines Coding-Agenten. Über den Titel gelangst du zum Chat. Eine erledigte Aufgabe bleibt kurz. Die Nachricht, aus der sie entstanden ist, findest du unter **Details**.

Bei einer Aufgabe mit „Wartet auf“ ist deine letzte Nachricht an die betreffende Person verlinkt, auf deren Antwort du wartest: „E-Mail an Pat · Di“.

## Selbst eine Aufgabe erstellen

Mit **Neue Aufgabe** (am Computer unter **Suchen**, auf dem Smartphone über **+** oder mit `N`) kannst du eine Aufgabe für alles erstellen. Beim Erstellen wird nichts gesendet. Wenn du weder **Arbeit** noch **Privat** auswählst, wird die Aufgabe anhand der beteiligten Personen und des Anliegens dem passenden Bereich zugeordnet. Außerdem findet sie die zugehörige E-Mail, auch wenn sie schon älter ist.

- **Fällig**: Gib einen Tag oder eine Uhrzeit ein, zum Beispiel „morgen“, „nächsten Fr“, „3. Nov.“, „14 Uhr“ oder „in 2 Stunden“, auch in deiner eigenen Sprache. Über das Kalendersymbol findest du Schnelloptionen und **Datum wählen**.
- **Wiederholt sich**: Die Aufgabe kommt regelmäßig zurück. Weitere Informationen findest du unter [Wiederkehrende Aufgaben](recurring.md).
- **Person**: Verknüpfe die Personen oder Unternehmen, um die es geht, bis zu 5.
- Nachrichtensymbol: Hänge die Nachricht an, um die es geht: eine E-Mail, Slack-, Teams-, WhatsApp-, Telegram- oder eine andere Nachricht, auf die The Machine zugreifen kann. Suche nach Text oder Absender. Bei jedem Ergebnis wird angezeigt, woher es stammt, wer es gesendet hat und wann.
- **Dateien**: Tippe auf die Büroklammer, füge einen Screenshot ein oder ziehe Dateien auf das Formular. Auf dem Smartphone kannst du mit der Kamera daneben ein Foto aufnehmen. Bis zu 5 Dateien, wie im Chat (siehe [Dateien hinzufügen](card-chat.md#add-files)). Mit × kannst du eine Datei wieder entfernen.

Die Dateien bleiben bei der Aufgabe, und The Machine liest sie, wenn sie daran arbeitet. Dateien allein reichen aus: Sie erstellt die Aufgabe aus einer PDF- oder Textdatei. Ein Foto wird als kleines Bild angezeigt. Tippe darauf, um es in voller Größe zu sehen.
