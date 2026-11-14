---
title: Aufgaben
area: cards
summary: Eine Aufgabe pro Sache, bei der du gefragt bist, bereit für dein Okay. Was die einzelnen Teile einer Aufgabe bedeuten.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 12be97d431968927
---
Deine Machine liest alles Neue und erstellt nur dann eine Aufgabe, wenn etwas von dir gebraucht wird. Pro Angelegenheit eine Aufgabe, egal über wie viele Nachrichten sie sich erstreckt.

## Wo Aufgaben zu finden sind

Auf der Seite **Aufgaben** sind sie gruppiert:

- **Gerade erledigt**: Ganz oben findest du einen letzten Schritt, den du bestätigt hast, etwa ein Formular oder ein Problem. Er wurde erledigt, während du weg warst. Er bleibt höchstens einen Tag lang dort, bis du auf **Verstanden** tippst. Dein Handy bekommt ebenfalls Bescheid.
- **Für dich**: Alles, worauf du reagieren musst, nach Dringlichkeit sortiert. Bei jeder Aufgabe steht **Vorbereitet** (die Arbeit ist erledigt und **Ausführen** oder **Senden** führt sie aus), **Braucht dich** (zuerst ist deine Entscheidung oder Antwort gefragt), **Wird vorbereitet…** (deine Machine arbeitet daran) oder **Zum Lesen** (eine Zusammenfassung oder ein Briefing, bei dem du nichts entscheiden musst).
- **Wartet auf andere**: Eingeklappte Aufgaben, bei denen jemand anderes als Nächstes dran ist (siehe unten).
- **Kommt später zurück**: Zurückgestellte Aufgaben und Aufgaben ohne Antwort auf **Noch nötig?** (siehe unten).
- **Versprechen**: Was du versprochen hast und was andere dir versprochen haben. Siehe [Versprechen](promises.md).
- **Erledigt / verworfen**: Alle abgeschlossenen Aufgaben, die neuesten zuerst, mit dem Zeitpunkt des Abschlusses, zum Beispiel „Vor 5 Minuten erledigt“. Aufgaben, die scheinbar schon erledigt sind, sind mit **Scheinbar erledigt** markiert.

Nach dem Senden erscheint ein kurzer Hinweis, wohin die Aufgabe verschoben wurde, zum Beispiel „Gesendet. Zu Erledigt verschoben.“ oder „Gesendet. Bis Mo. auf Später verschoben.“ Mit **Öffnen** gelangst du zur Aufgabe. Über die Suche findest du Aufgaben anhand ihres Titels oder der Person, an die sie gingen, auch unter Später und Erledigt.

Unter **Für dich** stehen zuerst überfällige oder bis morgen fällige Aufgaben, dann Fragen aus deiner Fleet, danach Aufgaben für ein Board und schließlich alle übrigen. Innerhalb jeder Gruppe stehen die neuesten zuerst. Eine Aufgabe behält ihren Platz, während deine Machine sie vorbereitet und auch nach Abschluss. Nur ihre Markierung ändert sich. In den anderen offenen Gruppen stehen überfällige oder bis morgen fällige Aufgaben zuerst, die übrigen nach Aktualität. Die Seitenleiste hat dieselbe Reihenfolge.

**Scheinbar erledigt** bedeutet, dass deine Machine sieht, dass die Aufgabe erledigt ist, etwa „PR #3451 zusammengeführt“, sie aber noch nicht geschlossen wurde. Mit **Wieder öffnen** kommt sie zurück in deine Liste und deine Machine lernt daraus. Diese Aufgaben werden nie als verspätet angezeigt. Nach einem Tag wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Eine Aufgabe, die du selbst schon erledigt hast, zum Beispiel durch eine Antwort in Gmail oder Slack, wird ebenfalls automatisch geschlossen.

Wenn eine Nachricht von einer Adresse kommt, die nur wie die einer Person aussieht, die du kennst, zum Beispiel sam@acme-corp.example statt sam@acmecorp.example, steht bei der Aufgabe ganz klar: „Das ist nicht Sam Lee.“ Die Person wird mit ihrer eigenen Adresse angezeigt, nie mit dem Namen, den sie verwendet hat. Deine Machine prüft solche Nachrichten bei der Person unter der Adresse, die du bereits gespeichert hast, nie bei der Person, die geschrieben hat.

Bei einer Aufgabe, die noch auf jemand anderen wartet, etwa auf eine Prüfung oder Antwort, steht **Wartet auf:** und der entsprechende Schritt. Sie bleibt eingeklappt unter **Wartet auf andere**, oberhalb von Kommt später zurück, bis eine neue Nachricht sie wieder hervorholt. Dasselbe gilt, wenn du eine Rückfrage gestellt hast: Die Aufgabe kommt am Morgen vor der Frist zurück, bei einer Frist noch am selben Tag zum Zeitpunkt der Frist oder am nächsten Morgen, wenn die Frist bereits vorbei ist. Sie zeigt dann an, auf wen sie noch wartet.

Wenn eine Aufgabe ein Ergebnis betrifft, das jemand anderes liefern muss, etwa einen unterschriebenen Vertrag, wird es unter **Details** als **Fertig, wenn** angezeigt. Wenn du deinen Teil abgeschickt hast, wird die Aufgabe nicht geschlossen. Sie bleibt unter **Wartet auf andere**, bis eine Nachricht das Ergebnis bestätigt. Dann wird sie automatisch geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Wenn bis zum Zeitpunkt, an dem du nachhaken solltest, nichts eingetroffen ist, kommt die Aufgabe mit **Schreib eine kurze Erinnerung** im Chat zurück. Schreib im Chat, was als erledigt gilt, um das zu ändern.

Wenn eine Aufgabe eine Woche lang niemanden beschäftigt hat, fragt sie einmal: **Noch nötig?** Mit **Nicht nötig** wird sie geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. **Behalten** lässt sie offen. Danach fragt sie nie wieder. Wenn du eine weitere Woche lang nicht antwortest, wird die Aufgabe unter Kommt später zurück eingeklappt. Die Zahl auf dem App-Symbol und in der morgendlichen Zusammenfassung berücksichtigt sie dann nicht mehr. Wenn du sie öffnest, im Chat schreibst, sie bearbeitest oder zurückstellst oder eine neue Nachricht eingeht, kommt sie wieder zurück.

Ein Projekt, bei dem es ruhig geworden ist und keine offenen Aufgaben mehr anstehen, kann einmal pro Woche eine Aufgabe mit einem konkreten nächsten Schritt bekommen, höchstens drei pro Woche. Siehe [Projekte](projects.md).

Wenn nichts von dir gebraucht wird, macht deine Machine ein Nickerchen und zeigt eine leere Liste. Während sie etwas prüft, wird sie aktiv und sagt dir Bescheid. Wenn eine Prüfung fehlgeschlagen ist oder verspätet läuft, steht das in der Zeile. Darunter findest du **Jetzt prüfen**.

Mit **Alle**, **Arbeit** und **Privat** oben in der Seitenleiste kannst du alle Aufgaben oder nur eine Art anzeigen. Auf deinem Handy und Computer gilt dieselbe Auswahl. Wenn Arbeit oder Privat ausgewählt ist, führt **Alle anzeigen** zurück zur Gesamtansicht. Eine Meldung über deine Machine selbst, etwa wenn ein Teil immer wieder neu startet, gehört weder zu Arbeit noch zu Privat und wird nur unter Alle angezeigt.

Die Zeile ganz oben in der Liste wechselt ebenfalls direkt zur anderen Ansicht: **Nur privat · Arbeit · Alle anzeigen**.

In der obersten Zeile steht der Name deiner letzten morgendlichen oder abendlichen Zusammenfassung und was sie umfasst hat, zum Beispiel **Zusammenfassung von gestern Abend** · 12 erledigt, 3 offen. Tippe darauf, um die Zusammenfassung erneut zu lesen. Mit **Kopieren** kannst du sie überall einfügen. Sobald du sie öffnest oder auf ihr **×** tippst, bleibt sie auf allen deinen Geräten sichtbar, bis die nächste Zusammenfassung kommt.

Wenn es keine aktuelle Zusammenfassung gibt, wird **Heute bisher** angezeigt: was heute erledigt wurde und was noch offen ist, für Arbeit und Privat oder nur für den Bereich, den du ausgewählt hast.

Bei einer Aufgabe für ein Projekt steht der Projektname unter dem Titel. Tippe darauf, um das Projekt zu öffnen. Unter **Details** kannst du es mit **Projekt** ändern oder entfernen. Siehe [Aufgaben eines Projekts](projects.md#a-project-s-to-dos).

Mit **Bereich** unter **Details** verschiebst du eine Aufgabe in deinen anderen Bereich. Auch die Nachrichten, die sie lesen und versenden darf, wechseln mit. Mit **Rückgängig** in der Meldung kannst du sie zurückverschieben.

Wenn eine Aufgabe nur in deinem anderen Bereich fortgesetzt werden kann und alle Nachrichten, auf denen sie basiert, dort sind, wird sie automatisch dorthin verschoben und fortgesetzt. Andernfalls wird **Nach Arbeit verschieben** angezeigt. Erst wenn du darauf tippst, wird etwas verschoben. Eine Aufgabe, die du hinzugefügt hast, ohne Arbeit oder Privat auszuwählen, wird automatisch verschoben, sobald klar ist, wohin sie gehört. Bis dahin gehört sie weder zu Arbeit noch zu Privat und bleibt privat.

Eine Aufgabe kann die Nachrichten, auf denen sie basiert, immer lesen. Wenn sie für weitere Nachrichten aus deinem anderen Bereich Zugriff braucht, fragt sie mit **Diese E-Mail für diese Aufgabe verwenden** danach. Ein Arbeits-Postfach, das du als Privat gekennzeichnet hast, zählt als Privat. E-Mails für ein anderes deiner Unternehmen landen in den Aufgaben dieses Unternehmens. Eine Aufgabe über dein Privatleben, etwa eine Nachricht von deiner Familie an deine Arbeitsadresse, ist von Anfang an privat.

Arbeit, die dich über ein privates Konto erreicht, etwa eine Nachricht von einem Kunden in WhatsApp oder eine Bestellung in deinem privaten Postfach, gehört von Anfang an zu Arbeit. Eine Aufgabe, die du selbst verschoben oder zugeordnet hast, bleibt immer dort. Arbeit oder Privat bestimmt, wo eine Aufgabe erscheint und mit wem sie geteilt wird, aber nie, wohin sie antwortet. Eine Antwort geht immer dorthin, wo die Unterhaltung stattfindet, auch nach dem Verschieben, es sei denn, du wählst einen anderen Weg.

Eine solche private Aufgabe antwortet trotzdem über die Arbeitsadresse, an die ihre E-Mail geschickt wurde, und wird nie in einer Arbeits-Fleet oder im Team Graph angezeigt.

Wenn mindestens zwei Aufgaben anstehen, gehst du mit **Durchgehen** in der Kopfzeile von Für dich eine nach der anderen durch, in der Reihenfolge der Liste. Jeder Entwurf wird vollständig angezeigt, mit **Senden** oder **Ausführen**, **Änderungen anfragen**, **Zurückstellen** und **Überspringen**. Am Computer sendet Enter den angezeigten Inhalt, `S` stellt zurück, `→` überspringt und Esc beendet den Vorgang. Unter dem Titel steht in der Kopfzeile außerdem, wie lange du in deinem eigenen Tempo dafür brauchst, zum Beispiel „etwa 2 Min.“.

Eine Aufgabe, bei der dir eine Frage gestellt wird, ist bei beiden Ansichten ausgenommen: Sie wartet auf deine Antwort und nicht auf einen Tipp.

## Jetzt prüfen

Deine Machine liest jede Quelle alle paar Minuten, Tag und Nacht. Sie prüft eingegangene Nachrichten, sobald 40 Nachrichten warten oder die älteste Nachricht einer Person seit 15 Minuten wartet. Newsletter, Benachrichtigungen und Belege werden bei der nächsten Prüfung berücksichtigt, spätestens innerhalb einer Stunde.

Nachts, von 00:00 bis 06:30, pausieren die Prüfungen: Neue Nachrichten werden weiterhin gelesen und gespeichert, aber erst um 06:30 gemeinsam geprüft. So sind deine Aufgaben vor der morgendlichen Zusammenfassung bereit. Unter Verbindungen steht bei Prüfungen: „Nachts pausiert, wird um 06:30 nachgeholt“. Wenn du nachts die App öffnest, im Chat schreibst oder auf eine Aufgabe tippst, laufen die Prüfungen wieder wie gewohnt, bis du eine Stunde lang nicht aktiv warst. **Jetzt prüfen** startet immer sofort eine Prüfung.

**Jetzt prüfen** liest sofort alle Quellen. Wenn keine Aufgaben offen sind, tippe auf die Zeile deiner Machine, um sie mit **Details** zu sehen. Dadurch werden Prüfungen unter Verbindungen geöffnet. Wenn Aufgaben offen sind, findest du die Zeile am Computer ganz oben. Dort wird eine kurze Meldung nur angezeigt, während eine Prüfung läuft oder wenn sie fehlgeschlagen ist oder verspätet läuft. Du kannst auch im Chat danach fragen.

LinkedIn, X und Salesflare haben ihren eigenen Rhythmus.

## Letzte Prüfung

Nach einer Prüfung, bei der neue Nachrichten gelesen wurden, steht über deinen Aufgaben eine Zeile mit den Ergebnissen aus allen gelesenen Quellen, zum Beispiel „13 Nachrichten um 16:11 geprüft · nichts von dir gebraucht“ oder „· 2 neue Aufgaben“. Wenn eine neue Aufgabe bis zu einem günstigeren Zeitpunkt zurückgestellt wird, zum Beispiel bis zur morgendlichen Zusammenfassung, steht dort auch, bis wann: „1 Aufgabe bis morgen 08:30 zurückgestellt“.

Tippe auf die Zeile, um jeden E-Mail-Verlauf, Chat und jede Benachrichtigung samt Symbol der Quelle zu sehen: wer geschrieben hat, den Betreff oder die ersten Wörter sowie die neue Aufgabe oder den Grund, warum nichts zu tun war, zum Beispiel „Nur in cc, ein Teammitglied antwortet“ oder „Termin für Donnerstag steht schon fest“. Wenn die Prüfung nur einen vagen Grund ergeben hat, wird bei einem Verlauf kein Grund angezeigt. Tippe darauf, um ihn zu lesen.

Die ersten 10 Einträge werden angezeigt. Wenn du darunter tippst, erscheinen die übrigen. Eine Zahl hinter einem Namen, etwa (3), gibt an, wie viele neue Nachrichten dieser Chat enthält. Eine Handy-Benachrichtigung zu einer Nachricht, die bereits aufgeführt ist, wird nur einmal angezeigt. Die Zeile bleibt nach der Prüfung 12 Stunden lang sichtbar.

Berücksichtigt werden nur E-Mails an dich. Deine eigenen Antworten werden als Kontext und für Versprechen gelesen, zählen aber nicht als neue E-Mails. E-Mails von The Machine an dich, etwa deine morgendliche Zusammenfassung oder ein Hinweis zu einer Fehlerbehebung, werden nie gelesen oder aufgeführt. E-Mails zu Abrechnung, Testversion oder Einladung werden wie gewohnt gelesen.

## Die Schaltflächen

Bei einer Aufgabe wird der nächste Schritt angezeigt, zum Beispiel **Ausführen** oder **Prüfen und senden**, daneben **Zurückstellen**. Siehe [Ausführen](do-it.md) und [Zurückstellen](snooze.md).

Mit **Änderungen anfragen** kannst du angeben, was geändert werden soll: wie die Aufgabe erledigt werden soll oder, sobald ein Entwurf bereit ist, was daran geändert werden soll. **Als erledigt markieren** bedeutet, dass du dich darum gekümmert hast. Bei einer vorbereiteten Aufgabe ohne Entwurf ist die Schaltfläche direkt zu sehen. Andernfalls findest du sie oben unter **…**, auch bei Aufgaben, bei denen du noch etwas entscheiden musst. Die Aufgabe wird sofort aus der Liste entfernt und in der Meldung erscheint **Rückgängig**. Wische die Meldung weg oder ziehe sie am Computer mit der Maus aus der Ansicht, um sie noch schneller zu schließen. Die Änderung bleibt bestehen.

Wenn die Aufgabe anders erledigt werden soll, sag es im **Chat**.

Unter **…**:

- **Übergeben…**: Gib die Aufgabe an ein Teammitglied, [Claude Code oder Codex](hand-to-agent.md) weiter oder [bitte jemanden um eine Prüfung](ask-to-review.md).
- **Wiederholen…**: Die Aufgabe [kommt regelmäßig zurück](recurring.md).
- **Nicht nötig**: Die Aufgabe wird entfernt. Optional kannst du einen Grund auswählen: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Tippe auf den Titel oder unter **Details** auf **Name**, um die Aufgabe umzubenennen. Dein Titel bleibt bestehen.

Mit **Wieder öffnen** holst du eine geschlossene Aufgabe zurück. Sie kommt auch von selbst zurück, wenn etwas Neues passiert, etwa wenn die Person eine neue Nachricht schickt, aber nicht bei deiner eigenen Antwort.

Eine Rechnung, die du selbst noch bezahlen musst, wird unabhängig vom Land zu einer Aufgabe mit Betrag, Fälligkeitsdatum und den Zahlungsdetails aus der Rechnung. Rechnungen, die automatisch bezahlt werden, etwa per Lastschrift oder gespeicherter Karte, werden nicht zu Aufgaben. Wenn eine spätere E-Mail zeigt, dass sie bezahlt wurde, zum Beispiel eine Bestätigung des Absenders, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang zurückholen.

Eine Aufgabe, die nur bis zu einem bestimmten Zeitpunkt wichtig war, etwa eine Bestätigung vor einem Meeting, wird nach diesem Zeitpunkt automatisch geschlossen. Sie wird unter **Erledigt / verworfen** mit dem Hinweis „Nicht mehr nötig“ abgelegt. Mit **Rückgängig** kannst du sie einen Tag lang zurückholen.

Bevor eine Nachricht oder Übergabe für jemanden als bereit angezeigt wird, prüft deine Machine deine letzten Chats mit den beteiligten Personen, auch Gruppenchats, und wartet darauf, dass Slack sie gelesen hat. Wenn eine spätere Nachricht zeigt, dass die Aufgabe bereits erledigt ist, etwa weil jemand gefragt wurde und Ja gesagt hat, wird sie automatisch geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang zurückholen.

Wenn eine neuere Nachricht den Plan ändert, etwa weil eine Party an einen anderen Ort verlegt oder eine Buchung storniert wurde, aktualisiert The Machine ihre Aufgaben selbst. Eine Aufgabe, die weiterhin wichtig ist, wird an den neuen Plan angepasst. Wenn nichts mehr zu tun ist, wird sie unter **Erledigt / verworfen** mit dem Hinweis „Nicht nötig“ abgelegt. Im Chat steht „Aktualisiert:“ mit einer Erklärung. Mit **Rückgängig** kannst du sie einen Tag lang zurückholen.

Bei deinen ersten Aufgaben wird ein kurzer Tipp mit den wichtigsten Aktionen angezeigt: **Änderungen anfragen** und **Nicht nötig**. Außerdem erfährst du, dass nichts verschickt wird, bevor du auf **Senden** tippst. Ein Tipp wird dauerhaft ausgeblendet, sobald du seine Schaltfläche verwendest oder auf × tippst.

An deinem ersten Tag begrüßt dich oben in Aufgaben eine Nachricht. Sie nennt die Person, die am längsten auf deine Antwort gewartet hat. Für diese Antwort wird zuerst ein Entwurf erstellt, damit er bereit ist, wenn du da bist.

Jede Aufgabe beginnt mit ihrem Titel. Die Zeile darunter nennt die Person, um die es geht, gegebenenfalls die Organisation, aber nicht allein deshalb, weil jemand dort arbeitet, das Projekt, Arbeit oder Privat und den Zeitpunkt des Eingangs. Tippe auf einen Namen, um die Seite der Person im Graph zu öffnen.

Bei Namen und Organisationen wird das Foto oder Logo angezeigt, falls es im Graph vorhanden ist, sonst die Initialen. Ein Logo, das in dieser Größe nicht zu erkennen wäre, etwa weiß auf transparentem Hintergrund oder ein breites Wortlogo, wird ebenfalls durch die Initiale ersetzt.

Manchmal steht in einer unauffälligen Zeile, was nicht bekannt ist, zum Beispiel „Letzter Kontakt vor 12 Tagen per E-Mail; seitdem nichts.“ Sie erscheint, wenn der letzte Kontakt mit der Person schon länger her oder unbeantwortet ist, und nennt nicht verbundene Kanäle wie WhatsApp. Deine Machine sagt dir, was sie nicht weiß, statt zu raten.

Wenn ein nicht verbundener Kanal genannt wird, öffnet **Verbinden** daneben die entsprechende Verbindung.

Der Titel beschreibt, was zu tun ist, und ändert sich nur, wenn sich das ändert. Bei einer erledigten Aufgabe bleibt der Titel bestehen. Darunter steht, wie sie abgeschlossen wurde, zum Beispiel „Erledigt: Sam hat es am Dienstag unterschrieben“.

Über dem Entwurf steht in einer blassen Zeile, aus welcher Nachricht er stammt, zusammen mit dem Logo des jeweiligen Dienstes. Tippe darauf, um den Verlauf zu lesen. Beim Entwurf wird das Logo des Ziels angezeigt. So siehst du sofort, ob es eine Slack-Antwort oder eine E-Mail ist.

Wenn der Entwurf auf einer Eingabe von anderer Stelle beruht, etwa dem Vorschlag eines Teammitglieds in Slack, steht das in einer Zeile, zum Beispiel „Basierend auf Sams Nachricht in #ops“. Tippe darauf, um die Nachricht zu lesen.

Ein Chat in Slack, WhatsApp, Telegram, Intercom … wird als eine Unterhaltung angezeigt, älteste Nachrichten zuerst: die Nachrichten vor der Nachricht, um die es bei der Aufgabe geht, und die Antworten danach. In WhatsApp, Telegram oder Signal stehen deine Nachrichten wie in der App rechts. Die Nachricht zur Aufgabe ist mit „Diese Aufgabe“ markiert und wird in der Ansicht geöffnet. Mit **Frühere Nachrichten anzeigen** werden ältere Nachrichten hinzugefügt. Bei einer E-Mail wird der übrige Verlauf ober- und unterhalb eingeklappt angezeigt.

Unter **Details** einer E-Mail stehen nur Angaben, die nicht im Kopf der E-Mail zu sehen sind, etwa vollständige Cc-Adressen, Bcc oder eine andere Antwortadresse. Gibt es nichts hinzuzufügen, werden keine Details angezeigt.

Bei einer Antwort in einem Slack-Thread wird auch angezeigt, was vor Beginn des Threads gesagt wurde. Der Link einer Aufgabe zu ihrer eigenen Nachricht öffnet diese ebenfalls hier. Unten findest du **In Slack öffnen**.

Unter **Details** findest du den Namen, das Projekt und den Bereich, die du durch Antippen ändern kannst, deine letzte Notiz und das Ergebnis eines Coding-Agenten. Mit **Chat ›** öffnest du den Chat. Eine erledigte Aufgabe bleibt kompakt. Die Nachricht, auf der sie basiert, findest du unter **Details**.

Bei einer Aufgabe mit „Wartet auf“ führt ein Link zu deiner letzten Nachricht an die Person, auf deren Antwort du wartest: „E-Mail an Pat · Di“.

## Selbst eine Aufgabe erstellen

Mit **Neue Aufgabe** (am Computer unter **Suchen**, auf dem Handy über **+** oder mit `N`) kannst du eine Aufgabe zu allem erstellen. Beim Erstellen wird nichts verschickt. Wenn du weder **Arbeit** noch **Privat** ausgewählt hast, wird die Aufgabe dem passenden Bereich zugeordnet, je nachdem, um wen und was es geht. Außerdem findet sie die E-Mail, auf die sie sich bezieht, auch wenn diese schon älter ist.

- **Fällig**: Gib einen Tag oder eine Uhrzeit ein, zum Beispiel „morgen“, „nächsten Fr“, „3. Nov“, „14 Uhr“ oder „in 2 Stunden“. Du kannst dafür auch deine eigene Sprache verwenden. Über das Kalendersymbol findest du Schnellauswahlen und **Datum wählen**.
- **Wiederholt sich**: Die Aufgabe kommt regelmäßig zurück. Siehe [Wiederkehrende Aufgaben](recurring.md).
- **Person**: Verknüpfe bis zu 5 Personen oder Unternehmen, um die es geht.
- Nachrichtensymbol: Hänge die Nachricht an, um die es geht: eine E-Mail, Slack-, Teams-, WhatsApp-, Telegram- oder andere Nachricht, die The Machine kennt. Suche nach Text oder Absender. Bei jedem Ergebnis siehst du, woher es stammt, wer es gesendet hat und wann.
- **Dateien**: Tippe auf die Büroklammer, füge einen Screenshot ein oder ziehe Dateien auf das Formular. Auf dem Handy kannst du über die Kamera daneben ein Foto aufnehmen. Wie im Chat sind bis zu 5 Dateien möglich (siehe [Dateien hinzufügen](card-chat.md#add-files)). Mit × entfernst du eine Datei wieder.

Die Dateien bleiben bei der Aufgabe und The Machine liest sie, wenn sie daran arbeitet. Dateien allein reichen aus: The Machine erstellt die Aufgabe aus einer PDF- oder Textdatei. Ein Foto wird als kleines Bild angezeigt. Tippe darauf, um es in voller Größe zu sehen.
