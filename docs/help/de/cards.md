---
title: Aufgaben
area: cards
summary: Eine Aufgabe pro Sache, die dich braucht, bereit für dein Ja. Was die einzelnen Teile einer Aufgabe bedeuten.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 16f31364b3da3827
---
Deine Machine liest alles Neue und erstellt nur dann eine Aufgabe, wenn etwas dich braucht. Eine Aufgabe pro Angelegenheit, egal über wie viele Nachrichten sie sich erstreckt.

## Wo Aufgaben zu finden sind

Auf der Seite **Aufgaben** sind sie gruppiert:

- **Gerade erledigt**: Ganz oben siehst du einen letzten Schritt, den du bestätigt hast, etwa ein Formular oder ein Problem, das erledigt wurde, während du nicht da warst. Er bleibt höchstens einen Tag lang dort, bis du auf **Verstanden** tippst. Du bekommst auch auf deinem Smartphone eine Benachrichtigung.
- **Für dich**: Alles, worauf du reagieren musst, nach Dringlichkeit sortiert. Bei jeder Aufgabe steht **Vorbereitet** (die Arbeit ist erledigt, mit **Ausführen** oder **Senden** wird sie abgeschlossen), **Braucht dich** (zuerst ist deine Entscheidung oder Antwort nötig), **Wird vorbereitet…** (deine Machine arbeitet daran) oder **Zum Lesen** (eine Zusammenfassung oder ein Briefing, bei dem nichts zu entscheiden ist).
- **Wartet auf andere**: Eingeklappte Aufgaben, bei denen der nächste Schritt bei jemand anderem liegt (siehe unten).
- **Kommt später zurück**: Zurückgestellte Aufgaben und Aufgaben ohne Antwort auf **Noch nötig?** (siehe unten).
- **Versprechen**: Was du versprochen hast und was andere dir versprochen haben. Siehe [Versprechen](promises.md).
- **Erledigt / verworfen**: Alle abgeschlossenen Aufgaben, die neuesten zuerst, mit dem Zeitpunkt des Abschlusses, zum Beispiel „Vor 5 Minuten erledigt“. Aufgaben, die offenbar schon erledigt sind, sind als **Scheinbar erledigt** markiert.

Nachdem du etwas gesendet hast, steht in einer kurzen Meldung, wohin die Aufgabe verschoben wurde, zum Beispiel „Gesendet. Zu „Erledigt“ verschoben.“ oder „Gesendet. Bis Mo. auf „Später“ verschoben.“ Mit **Öffnen** gelangst du zur Aufgabe. Über die Suche findest du Aufgaben nach Titel oder Empfänger, auch unter „Später“ und „Erledigt“.

Unter **Für dich** stehen zuerst überfällige Aufgaben und Aufgaben, die bis morgen fällig sind, dann Fragen aus deiner Fleet, anschließend die Nachfassaktionen eines Boards und danach alle übrigen. Innerhalb jeder Gruppe stehen die neuesten zuerst. Eine Aufgabe bleibt an ihrem Platz, während deine Machine sie vorbereitet und wenn sie erledigt ist. Nur ihre Markierung ändert sich. In den anderen offenen Gruppen stehen überfällige Aufgaben und Aufgaben, die bis morgen fällig sind, zuerst, danach die neuesten. Die Seitenleiste behält dieselbe Reihenfolge bei.

**Scheinbar erledigt** bedeutet, dass deine Machine sieht, dass eine Aufgabe abgeschlossen ist, etwa „PR #3451 zusammengeführt“, sie aber noch nicht geschlossen wurde. Mit **Wieder öffnen** kommt sie zurück in deine Liste, und deine Machine lernt daraus. Diese Aufgaben werden nie als überfällig angezeigt. Nach einem Tag wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Eine Aufgabe, die du selbst schon erledigt hast, etwa durch eine Antwort in Gmail oder Slack, wird ebenfalls automatisch geschlossen.

Wenn eine Nachricht von einer Adresse kommt, die nur so aussieht, als gehöre sie jemandem, den du kennst, zum Beispiel sam@acme-corp.example statt sam@acmecorp.example, weist die Aufgabe ausdrücklich darauf hin: „Das ist nicht Sam Lee.“ Angezeigt wird die Person mit ihrer tatsächlichen Adresse, nie mit dem Namen, den sie verwendet hat. Deine Machine prüft solche Nachrichten bei der Person unter der Adresse, die du bereits gespeichert hast, nie bei der Person, die geschrieben hat.

Bei einer Aufgabe, bei der noch jemand anderes am Zug ist, etwa bei einer Prüfung oder Antwort, steht **Wartet auf:** gefolgt von diesem Schritt. Sie bleibt eingeklappt unter **Wartet auf andere**, oberhalb von „Kommt später zurück“, bis eine neue Nachricht sie wieder hervorholt. Dasselbe gilt, nachdem du eine Rückfrage gestellt hast: Die Aufgabe kommt am Morgen vor ihrer Frist zurück, am Tag der Frist, wenn diese später am selben Tag liegt, oder am nächsten Morgen, wenn die Frist bereits verstrichen ist. Dabei steht, auf wen sie noch wartet.

Bei einer Aufgabe, bei der jemand anderes ein Ergebnis liefern muss, etwa einen unterschriebenen Vertrag, wird unter **Details** angezeigt, wann sie als **Fertig, wenn** gilt. Wenn du deinen Teil abschickst, wird die Aufgabe nicht geschlossen. Sie bleibt unter **Wartet auf andere**, bis eine Nachricht das Ergebnis bestätigt. Dann wird sie automatisch geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Wenn bis zum Zeitpunkt, an dem du nachhaken solltest, nichts eingegangen ist, kommt die Aufgabe mit **Schreib eine kurze Erinnerung** im Chat zurück. Schreib im Chat, was als erledigt gilt, um das zu ändern.

Wenn sich eine Woche lang niemand um eine Aufgabe gekümmert hat, fragt sie einmal: **Noch nötig?** Mit **Nicht nötig** wird sie geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. **Behalten** lässt sie bestehen, und sie fragt nie wieder nach. Wenn eine weitere Woche lang keine Antwort kommt, wird sie unter „Kommt später zurück“ eingeklappt. Sie wird dann nicht mehr auf dem App-Symbol und in der morgendlichen Zusammenfassung mitgezählt. Wenn du sie öffnest, eine Chatnachricht schreibst, sie bearbeitest, zurückstellst oder eine neue Nachricht eingeht, kommt sie wieder zurück.

Einmal pro Woche kann für ein ruhendes Projekt ohne offene Aufgaben eine Aufgabe mit einem konkreten nächsten Schritt erstellt werden, höchstens drei pro Woche. Siehe [Projekte](projects.md).

Wenn nichts deine Aufmerksamkeit braucht, macht deine Machine eine Pause und zeigt eine leere Liste. Während sie etwas prüft, wird sie aktiv und zeigt das an. Wenn eine Prüfung fehlgeschlagen ist oder sich verspätet, steht es in der Zeile. Darunter findest du **Jetzt prüfen**.

Mit **Alle**, **Arbeit** und **Privat** oben in der Seitenleiste kannst du alle Aufgaben oder nur Aufgaben einer Kategorie anzeigen. Auf deinem Smartphone und Computer gilt dieselbe Auswahl. Wenn „Arbeit“ oder „Privat“ aktiviert ist, kehrst du mit **Alle anzeigen** zur Gesamtansicht zurück. Eine Meldung zu deiner Machine selbst, etwa dass ein Teil ständig neu startet, gehört weder zu „Arbeit“ noch zu „Privat“ und wird nur unter „Alle“ angezeigt.

Mit der Zeile oben in der Liste wechselst du auch direkt zur anderen Ansicht: Wenn **Nur privat** ausgewählt ist, tippe auf **Arbeit** oder **Alle anzeigen**.

Die Zeile oben in der Liste nennt deine letzte morgendliche oder abendliche Zusammenfassung und die Anzahl der erfassten Aufgaben, zum Beispiel **Zusammenfassung von gestern Abend** · 12 erledigt, 3 offen. Tippe darauf, um die Zusammenfassung erneut zu lesen. Mit **Kopieren** kannst du sie an beliebiger Stelle einfügen. Sobald du sie öffnest oder auf ihr **×** tippst, wird sie auf allen deinen Geräten angezeigt, bis die nächste Zusammenfassung kommt.

Wenn es keine aktuelle Zusammenfassung gibt, wird **Heute bisher** angezeigt: Was heute erledigt wurde und was noch offen ist, für „Arbeit“ und „Privat“ oder nur für die ausgewählte Kategorie.

Bei einer Aufgabe für ein Projekt steht der Projektname unter dem Titel. Tippe darauf, um das Projekt zu öffnen. Unter **Details** kannst du es mit **Projekt** ändern oder entfernen. Siehe [Aufgaben eines Projekts](projects.md#a-project-s-to-dos).

Mit **Bereich** unter **Details** verschiebst du eine Aufgabe in deinen anderen Bereich. Die Nachrichten, die sie lesen und senden darf, ändern sich entsprechend. Mit **Rückgängig** in der Meldung verschiebst du sie zurück.

Wenn eine Aufgabe deinen anderen Bereich benötigt und alle Nachrichten, auf denen sie beruht, dort sind, wird sie automatisch dorthin verschoben und fortgesetzt. Andernfalls wird **Nach Arbeit verschieben** angezeigt. Erst wenn du darauf tippst, wird etwas verschoben. Eine Aufgabe, die du hinzugefügt hast, ohne „Arbeit“ oder „Privat“ auszuwählen, wird automatisch dorthin verschoben, wo sie hingehört, sobald das feststeht. Bis dahin ist sie weder „Arbeit“ noch „Privat“ zugeordnet und bleibt privat.

Eine Aufgabe kann immer die Nachrichten lesen, aus denen sie entstanden ist. Wenn sie weitere Nachrichten aus deinem anderen Bereich benötigt, fragt sie mit **Diese E-Mail für diese Aufgabe verwenden** danach. Ein geschäftliches Postfach, das du als „Privat“ gekennzeichnet hast, zählt als privat. E-Mails an eine andere deiner Firmen landen bei den Aufgaben dieser Firma. Eine Aufgabe zu deinem Privatleben, etwa wenn deine Familie an deine geschäftliche Adresse schreibt, ist von Anfang an privat.

Arbeit, die dich über ein privates Konto erreicht, etwa eine Nachricht von einem Kunden auf WhatsApp oder eine Bestellung in deinem privaten Postfach, ist von Anfang an geschäftlich. Eine Aufgabe, die du selbst verschoben oder zugeordnet hast, bleibt immer dort, wo du sie abgelegt hast. „Arbeit“ oder „Privat“ bestimmt, wo eine Aufgabe angezeigt und mit wem sie geteilt wird, aber nie, wohin sie antwortet. Eine Antwort geht immer dorthin, wo die Unterhaltung stattfindet, auch nach einer Verschiebung, es sei denn, du wählst einen anderen Weg.

Eine solche private Aufgabe antwortet weiterhin von der geschäftlichen Adresse, an die die E-Mail geschickt wurde. Sie wird nie in einer geschäftlichen Fleet oder im Team Graph angezeigt.

Wenn mindestens zwei Aufgaben auf dich warten, führt dich **Durchgehen** in der Kopfzeile von „Für dich“ nacheinander durch sie, in der Reihenfolge der Liste. Jeder Entwurf wird vollständig angezeigt, zusammen mit **Senden** oder **Ausführen**, **Änderungen anfragen**, **Zurückstellen** und **Überspringen**. Auf einem Computer sendet Enter den angezeigten Inhalt, `S` stellt zurück, `→` überspringt und Esc beendet den Vorgang. Unter dem Titel steht in der Kopfzeile auch, wie lange die Aufgaben bei deinem eigenen Tempo dauern, zum Beispiel „etwa 2 Min.“

Eine Aufgabe, bei der eine Frage an dich gestellt wird, ist von beidem ausgenommen: Sie wartet auf deine Antwort, nicht auf einen Tipp.

## Jetzt prüfen

Deine Machine liest jede Quelle alle paar Minuten, Tag und Nacht. Sie prüft neue Nachrichten, sobald 40 Nachrichten vorliegen oder die älteste Nachricht einer Person seit 15 Minuten wartet. Newsletter, Benachrichtigungen und Belege werden bei der nächsten Prüfung berücksichtigt, spätestens innerhalb einer Stunde.

Nachts, von 00:00 bis 06:30 Uhr, pausieren die Prüfungen. Neue Nachrichten werden trotzdem gelesen und gespeichert und um 06:30 Uhr gemeinsam geprüft, damit deine Aufgaben vor der morgendlichen Zusammenfassung bereit sind. Unter „Verbindungen“ steht bei den Prüfungen „Nachts pausiert. Um 06:30 Uhr wird alles nachgeholt.“ Wenn du nachts in der App klickst, etwas eingibst oder scrollst, im Chat schreibst oder auf eine Aufgabe tippst, laufen die Prüfungen wie gewohnt weiter, bis du eine Stunde lang nicht aktiv warst. Mit **Jetzt prüfen** wird immer sofort geprüft.

Mit **Jetzt prüfen** werden alle Quellen sofort gelesen. Wenn keine Aufgaben offen sind, tippe auf die Zeile deiner Machine, um sie mit **Details** zu sehen. Damit öffnest du „Prüfungen“ unter „Verbindungen“. Wenn Aufgaben offen sind, findest du die Zeile oben auf dem Computer. Sie wird nur angezeigt, während eine Prüfung läuft oder wenn eine fehlgeschlagen ist oder sich verspätet. Du kannst auch im Chat danach fragen.

LinkedIn, X und Salesflare haben ihren eigenen Rhythmus.

## Letzte Prüfung

Nach einer Prüfung, bei der neue Nachrichten gelesen wurden, steht über deinen Aufgaben eine Zeile mit den Ergebnissen aus allen gelesenen Quellen, zum Beispiel „13 Nachrichten um 16:11 geprüft · nichts braucht dich“ oder „· 2 neue Aufgaben“. Wenn eine neue Aufgabe bis zu einem passenderen Zeitpunkt zurückgehalten wird, etwa bis zur morgendlichen Zusammenfassung, steht dort bis wann: „1 Aufgabe bis morgen 08:30 zurückgehalten“.

Tippe auf die Zeile, um alle E-Mail-Unterhaltungen, Chats und Benachrichtigungen mit dem Symbol ihrer Quelle zu sehen: wer geschrieben hat, den Betreff oder die ersten Worte sowie die neue Aufgabe oder den Grund, warum nichts zu tun war, zum Beispiel „Nur in Cc, eine Kollegin antwortet“ oder „Besprechung für Donnerstag steht schon fest“. Wenn die Prüfung nur einen ungenauen Grund ergeben hat, wird für eine Unterhaltung kein Grund angezeigt. Tippe auf eine Unterhaltung, um sie zu lesen.

Die ersten 10 Einträge werden angezeigt. Mit einem Tipp darunter erscheinen die übrigen. Eine Zahl nach einem Namen, etwa (3), gibt an, wie viele neue Nachrichten dieser Chat enthält. Eine Smartphone-Benachrichtigung zu einer Nachricht, die bereits in der Liste steht, wird nur einmal angezeigt. Die Zeile bleibt 12 Stunden nach der Prüfung sichtbar.

Gezählt werden nur E-Mails an dich. Deine eigenen Antworten werden im Kontext von Unterhaltungen und Versprechen gelesen, gelten aber nicht als neue E-Mails. E-Mails von The Machine an dich, etwa deine morgendliche Zusammenfassung oder eine Meldung zu einer Korrektur, werden nie gelesen oder aufgelistet. Nachrichten zu Rechnungen, deiner Testversion oder einer Einladung werden wie gewohnt gelesen.

## Die Schaltflächen

Bei einer Aufgabe steht der nächste Schritt, zum Beispiel **Ausführen** oder **Prüfen und senden**, daneben **Zurückstellen**. Siehe [Ausführen](do-it.md) und [Zurückstellen](snooze.md).

Mit **Änderungen anfragen** kannst du angeben, was geändert werden soll: wie die Aufgabe erledigt wird oder, sobald ein Entwurf bereit ist, was darin geändert werden soll. **Als erledigt markieren** bedeutet, dass die Aufgabe erledigt ist. Bei einer vorbereiteten Aufgabe ohne Entwurf ist die Option direkt sichtbar, andernfalls findest du sie oben unter **…**. Sie ist auch bei Aufgaben verfügbar, bei denen du erst noch eine Entscheidung treffen musst. Die Aufgabe wird sofort aus der Liste entfernt. In der Meldung findest du **Rückgängig**. Wische die Meldung weg oder zieh sie mit der Maus aus dem Fenster, um sie früher zu schließen. Die Änderung bleibt bestehen.

Wenn du die Aufgabe anders erledigen lassen möchtest, schreib es im **Chat**.

Unter **…**:

- **Übergeben…**: Übergib die Aufgabe an ein Teammitglied, an [Claude Code oder Codex](hand-to-agent.md) oder [bitte jemanden um eine Prüfung](ask-to-review.md).
- **Wiederholen…**: Die Aufgabe [kommt regelmäßig wieder](recurring.md).
- **Nicht nötig**: Die Aufgabe wird entfernt. Du kannst optional einen Grund auswählen: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Tippe auf den Titel oder unter **Details** auf **Name**, um die Aufgabe umzubenennen. Dein Titel bleibt erhalten.

Mit **Wieder öffnen** holst du eine geschlossene Aufgabe zurück. Sie kommt auch automatisch wieder, wenn etwas Neues passiert, etwa wenn die Person dir eine neue Nachricht schickt, aber nicht bei deiner eigenen Antwort. Dann wird angezeigt, wann sie zurückkam, und sie wird wie eine neue Aufgabe sortiert. Der Chat wird dort fortgesetzt, wo er aufgehört hat, auch nach mehreren Wochen.

Eine Rechnung, die du selbst noch bezahlen musst, wird unabhängig vom Land zu einer Aufgabe mit Betrag, Fälligkeitsdatum und Zahlungsdetails aus der Rechnung. Automatisch bezahlte Rechnungen, etwa per Lastschrift oder hinterlegter Karte, werden nicht aufgenommen. Wenn eine spätere E-Mail zeigt, dass die Rechnung bezahlt wurde, zum Beispiel eine Bestätigung des Zahlungseingangs vom Absender, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Eine Aufgabe, die nur bis zu einem festgelegten Zeitpunkt wichtig war, etwa eine Bestätigung vor einer Besprechung, wird nach diesem Zeitpunkt automatisch geschlossen. Sie wird mit dem Vermerk „Nicht mehr nötig“ unter **Erledigt / verworfen** abgelegt. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Bevor eine Nachricht oder Übergabe für jemanden als bereit angezeigt wird, prüft deine Machine deine letzten Chats mit den beteiligten Personen, auch Gruppenchats, und wartet darauf, dass Slack sie einliest. Wenn eine spätere Nachricht zeigt, dass die Aufgabe bereits erledigt ist, etwa weil jemand gefragt wurde und zugestimmt hat, wird sie automatisch geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Wenn eine neuere Nachricht den Plan ändert, etwa weil eine Party an einen anderen Ort verlegt oder eine Buchung storniert wurde, aktualisiert The Machine die Aufgaben selbst. Eine weiterhin relevante Aufgabe folgt dem neuen Plan. Wenn nichts mehr zu tun ist, wird sie mit dem Vermerk „Nicht nötig“ unter **Erledigt / verworfen** abgelegt. Im Chat steht „Aktualisiert:“ mit einer Begründung. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Bei deinen ersten Aufgaben erscheint ein kurzer Hinweis zu den wichtigsten Aktionen: **Änderungen anfragen** und **Nicht nötig**. Außerdem weist er darauf hin, dass nichts verschickt wird, bevor du auf **Senden** tippst. Ein Hinweis wird dauerhaft ausgeblendet, sobald du seine Schaltfläche verwendest oder auf × tippst.

An deinem ersten Tag begrüßt dich oben auf der Seite „Aufgaben“ eine Nachricht. Sie nennt, wer am längsten auf deine Antwort wartet. Diese Antwort wird zuerst entworfen, damit sie bereit ist, wenn du eintriffst.

Jede Aufgabe beginnt mit ihrem Titel. In der Zeile darunter steht, um wen es geht, gegebenenfalls die Organisation, aber nicht einfach nur, weil jemand dort arbeitet, außerdem das Projekt, „Arbeit“ oder „Privat“ und der Zeitpunkt, zu dem die Aufgabe eingegangen ist. Tippe auf einen Namen, um die Seite der Person im Graph zu öffnen.

Bei Namen und Organisationen wird, wenn im Graph verfügbar, ein Foto oder Logo angezeigt, andernfalls die Initialen. Ein Logo, das in dieser Größe nicht lesbar wäre, etwa weiße Schrift auf transparentem Hintergrund oder ein breiter Schriftzug, wird ebenfalls durch die Initiale ersetzt.

Manchmal steht in einer unauffälligen Zeile, was nicht bekannt ist, etwa „Letzter Kontakt vor 12 Tagen per E-Mail, seitdem nichts.“ Sie wird angezeigt, wenn der letzte Kontakt mit der Person lange zurückliegt oder unbeantwortet ist. Außerdem werden nicht verbundene Kanäle genannt, etwa WhatsApp. Deine Machine sagt, was sie nicht weiß, statt zu raten.

Wenn ein nicht verbundener Kanal genannt wird, öffnet **Verbinden** daneben die entsprechende Verbindung.

Ein Titel beschreibt, was zu tun ist, und ändert sich nur, wenn sich das ändert. Eine erledigte Aufgabe behält ihren Titel. Darunter steht, wie sie abgeschlossen wurde, etwa „Erledigt: Sam hat am Dienstag unterschrieben“.

Über dem Entwurf steht in einer unauffälligen Zeile die Nachricht, aus der er entstanden ist, zusammen mit dem Logo des jeweiligen Dienstes. Tippe darauf, um die Unterhaltung zu lesen. Beim Entwurf wird das Logo des Ziels angezeigt. So siehst du sofort, ob es sich um eine Slack-Antwort oder eine E-Mail handelt.

Wenn ein Entwurf auf einer Eingabe an anderer Stelle beruht, etwa auf einem Vorschlag eines Teammitglieds in Slack, steht das in einer Zeile, etwa „Basiert auf Sam in #ops“. Tippe darauf, um die Nachricht zu lesen.

Ein Chat (Slack, WhatsApp, Telegram, Intercom …) wird als eine Unterhaltung angezeigt, von der ältesten Nachricht an: die Nachrichten vor der Nachricht, auf die sich die Aufgabe bezieht, und die Antworten danach. In WhatsApp, Telegram oder Signal stehen deine Nachrichten wie in der App rechts. Die Nachricht der Aufgabe ist mit „Diese Aufgabe“ markiert und wird geöffnet angezeigt. Mit **Frühere Nachrichten anzeigen** fügst du ältere Nachrichten hinzu. Bei einer E-Mail wird der Rest der Unterhaltung darüber und darunter eingeklappt angezeigt.

Mit **In Gmail öffnen** öffnest du die E-Mail in dem Gmail-Konto, in dem sie eingegangen ist. Auf Android wird sie in der Gmail App geöffnet, falls du sie installiert hast.

Unter **Details** einer E-Mail stehen nur Angaben, die nicht bereits in der Kopfzeile zu sehen sind, etwa vollständige Cc-Adressen, Bcc oder eine abweichende Antwortadresse. Gibt es keine weiteren Angaben, wird nichts angezeigt.

Bei einer Antwort in einem Slack-Thread werden auch die Nachrichten vor Beginn des Threads angezeigt. Über den Link einer Aufgabe zu ihrer eigenen Nachricht wird sie hier ebenfalls geöffnet. Unten findest du **In Slack öffnen**.

Unter **Details** findest du den Namen, das Projekt und den Bereich. Tippe auf eines davon, um es zu ändern. Außerdem siehst du deine letzte Notiz und das Ergebnis eines Coding-Agenten. Über den Titel öffnest du den Chat. Eine erledigte Aufgabe wird kompakt angezeigt. Die Nachricht, aus der sie entstanden ist, findest du unter **Details**.

Bei einer Aufgabe mit dem Status „Wartet auf“ verweist ein Link auf deine letzte Nachricht an die Person, auf die du wartest, zum Beispiel „E-Mail an Pat · Di“.

## Selbst eine Aufgabe erstellen

Mit **Neue Aufgabe** (unter **Suchen** auf dem Computer, **+** auf dem Smartphone oder `N`) kannst du eine Aufgabe für alles Mögliche erstellen. Beim Erstellen wird nichts verschickt. Wenn du weder **Arbeit** noch **Privat** auswählst, landet die Aufgabe dort, wo sie hingehört, je nachdem, um wen und was es geht. Außerdem findet sie die E-Mail, auf die sie sich bezieht, auch wenn sie schon älter ist.

- **Fällig**: Gib einen Tag oder eine Uhrzeit ein, zum Beispiel „morgen“, „nächsten Fr“, „3. Nov“, „14 Uhr“ oder „in 2 Stunden“, auch in deiner Sprache. Über das Kalendersymbol findest du praktische Vorschläge und **Datum wählen**.
- **Wiederholt sich**: Die Aufgabe kommt regelmäßig wieder. Siehe [Wiederkehrende Aufgaben](recurring.md).
- **Person**: Verknüpfe bis zu 5 Personen oder Unternehmen, um die es geht.
- Nachrichtensymbol: Hänge die passende Nachricht an: eine E-Mail, Slack-, Teams-, WhatsApp- oder Telegram-Nachricht oder eine andere Nachricht, auf die The Machine Zugriff hat. Suche nach Text oder Absender. Bei jedem Ergebnis siehst du, woher es stammt, wer es gesendet hat und wann.
- **Dateien**: Tippe auf die Büroklammer, füge einen Screenshot ein oder zieh Dateien auf das Formular. Auf einem Smartphone kannst du über die Kamera daneben ein Foto aufnehmen. Bis zu 5 Dateien, wie im Chat (siehe [Dateien hinzufügen](card-chat.md#add-files)). Mit × entfernst du eine Datei.

Die Dateien bleiben bei der Aufgabe, und The Machine liest sie, wenn sie daran arbeitet. Es reichen auch Dateien allein: The Machine füllt die Aufgabe anhand einer PDF- oder Textdatei aus. Ein Foto wird als kleines Bild angezeigt. Tippe darauf, um es in voller Größe zu sehen.
