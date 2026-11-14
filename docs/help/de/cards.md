---
title: Aufgaben
area: cards
summary: Eine Aufgabe pro Sache, die dich braucht, bereit für dein Ja. Hier erfährst du, was die einzelnen Teile einer Aufgabe bedeuten.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: cd59c14a7a27491d
---
Deine Machine liest alles Neue und erstellt nur dann eine Aufgabe, wenn etwas dich braucht. Pro Anliegen gibt es eine Aufgabe, egal über wie viele Nachrichten es sich erstreckt.

## Wo Aufgaben zu finden sind

Auf der Seite **Aufgaben** sind sie gruppiert:

- **Für dich**: Alles, worauf du reagieren musst, zuerst das Dringendste. Jede Aufgabe ist mit **Vorbereitet** gekennzeichnet (die Arbeit ist erledigt und **Ausführen** oder **Senden** führt sie aus), **Braucht dich** (zuerst braucht es deine Entscheidung oder eine Antwort) oder **Wird vorbereitet…** (deine Machine arbeitet daran).
- **Gerade erledigt**: Ein letzter Schritt, den du bestätigt hast, etwa ein Formular oder ein Vorgang, wurde ausgeführt, während du weg warst. Er bleibt höchstens einen Tag hier, bis du auf **Verstanden** tippst. Dein Handy benachrichtigt dich ebenfalls.
- **Kommt später zurück**: Zurückgestellte Aufgaben und Aufgaben, auf die du nicht mit **Noch nötig?** geantwortet hast (siehe unten).
- **Versprechen**: Was du versprochen hast und was andere dir versprochen haben. Siehe [Versprechen](promises.md).
- **Erledigt / verworfen**: Alle abgeschlossenen Aufgaben, die neuesten zuerst, mit dem Abschlusszeitpunkt, zum Beispiel „Vor 5 Minuten erledigt“. Aufgaben, die offenbar bereits erledigt sind, sind mit **Scheinbar erledigt** gekennzeichnet.

Nach dem Senden erscheint eine kurze Meldung, wohin die Aufgabe verschoben wurde, zum Beispiel „Gesendet. Nach Erledigt verschoben.“ oder „Gesendet. Bis Mo. nach Später verschoben.“ Mit **Öffnen** kommst du zur Aufgabe. Über die Suche findest du Aufgaben nach Titel oder Empfänger, auch unter Später und Erledigt.

Unter **Für dich** stehen zuerst überfällige Aufgaben oder Aufgaben, die bis morgen fällig sind, danach Fragen aus deiner Fleet und dann alle übrigen. Innerhalb jeder Gruppe stehen die neuesten zuerst. Während deine Machine eine Aufgabe vorbereitet und auch nach dem Erledigen bleibt sie an ihrem Platz. Nur ihre Markierung ändert sich. In den anderen offenen Gruppen stehen überfällige Aufgaben oder Aufgaben, die bis morgen fällig sind, zuerst. Danach folgen die übrigen, die neuesten zuerst. Die Seitenleiste behält dieselbe Reihenfolge bei.

**Scheinbar erledigt** bedeutet, dass deine Machine erkennt, dass eine Aufgabe erledigt ist, etwa „PR #3451 zusammengeführt“, sie aber noch nicht geschlossen wurde. Mit **Wieder öffnen** kommt sie zurück auf deine Liste, und deine Machine lernt daraus. Diese Aufgaben werden nie als verspätet angezeigt. Nach einem Tag werden sie automatisch geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Eine Aufgabe, die du schon selbst erledigt hast, etwa mit einer Antwort in Gmail oder Slack, wird ebenfalls automatisch geschlossen.

Wenn eine Nachricht von einer Adresse kommt, die nur wie die Adresse einer Person aussieht, die du kennst, zum Beispiel sam@acme-corp.example statt sam@acmecorp.example, weist die Aufgabe deutlich darauf hin: „Das ist nicht Sam Lee.“ Als Absender wird die eigene Adresse der Person angezeigt, nie der Name, den sie verwendet hat. Deine Machine prüft solche Nachrichten mit der Person unter der Adresse, die du bereits gespeichert hast, nie mit dem Absender der Nachricht.

Bei einer Aufgabe, die noch auf jemand anderen wartet, etwa auf eine Prüfung oder Antwort, steht **Wartet auf:** gefolgt von diesem Schritt. Sie bleibt eingeklappt unter **Wartet auf andere**, oberhalb von „Kommt später zurück“, bis eine neue Nachricht sie wieder hervorholt. Dasselbe gilt, wenn du eine Rückfrage gestellt hast: Die Aufgabe kommt am Morgen vor der Frist zurück, am Fälligkeitstag, wenn die Frist noch heute ist, oder am nächsten Morgen, wenn sie bereits verstrichen ist. Sie zeigt dann an, auf wen sie noch wartet.

Wenn es bei einer Aufgabe um ein Ergebnis geht, das jemand anderes liefern muss, etwa einen unterschriebenen Vertrag, wird es unter **Details** als **Fertig, wenn** angezeigt. Wenn du deinen Teil sendest, wird die Aufgabe nicht geschlossen. Sie bleibt unter **Wartet auf andere**, bis eine Nachricht das Ergebnis bestätigt. Danach wird sie automatisch geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Wenn bis zum Zeitpunkt, an dem du nachhaken solltest, nichts eingegangen ist, kommt sie mit **Schreib eine kurze Erinnerung** in ihrem Chat zurück. Schreib im Chat, was als erledigt gilt, um das zu ändern.

Wenn sich eine Woche lang niemand um eine Aufgabe gekümmert hat, fragt sie einmal: **Noch nötig?** Mit **Nicht nötig** wird sie geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. **Behalten** behält die Aufgabe bei. Sie fragt dann nie wieder nach. Wenn du eine weitere Woche lang nicht antwortest, wird sie unter „Kommt später zurück“ eingeklappt. Sie wird dann nicht mehr in der Zahl auf dem App-Symbol und in der morgendlichen Zusammenfassung mitgezählt. Wenn du sie öffnest, eine Chatnachricht schreibst, sie bearbeitest, zurückstellst oder eine neue Nachricht eingeht, kommt sie zurück.

Einmal pro Woche kann für ein ruhiges Projekt ohne offene Aufgaben eine Aufgabe mit einem konkreten nächsten Schritt erstellt werden, höchstens drei pro Woche. Siehe [Projekte](projects.md).

Wenn nichts dich braucht, macht deine Machine bei leerer Liste ein Nickerchen. Während sie etwas prüft, wacht sie auf und teilt dir das mit. Wenn eine Prüfung fehlgeschlagen oder verspätet ist, steht es in der Zeile. Darunter findest du **Jetzt prüfen**.

Mit **Alle**, **Arbeit** und **Privat** oben in der Seitenleiste kannst du alle Aufgaben oder nur Aufgaben einer Art anzeigen. Auf deinem Handy und Computer wird dieselbe Auswahl verwendet. Wenn „Arbeit“ oder „Privat“ ausgewählt ist, kommst du mit **Alle anzeigen** zurück zur Gesamtansicht. Eine Meldung zu deiner Machine selbst, etwa zu einem Teil, das immer wieder neu startet, gehört weder zu „Arbeit“ noch zu „Privat“ und wird nur unter „Alle“ angezeigt.

Die Zeile oben in der Liste bietet auch eine direkte Auswahl der anderen Ansicht: **Nur privat · Arbeit · Alle anzeigen**.

Die Zeile oben in der Liste zeigt den Namen deiner letzten morgendlichen oder abendlichen Zusammenfassung und was sie umfasst hat, zum Beispiel **Zusammenfassung von gestern Abend** · 12 erledigt, 3 offen. Tippe darauf, um die Zusammenfassung noch einmal zu lesen. Mit **Kopieren** kannst du sie überall einfügen. Sobald du sie öffnest oder auf das **×** tippst, wird sie auf all deinen Geräten angezeigt, bis die nächste Zusammenfassung kommt.

Wenn es keine aktuelle Zusammenfassung gibt, wird **Heute bisher** angezeigt: Was heute erledigt wurde und noch offen ist, für „Arbeit“ und „Privat“ oder nur für die ausgewählte Ansicht.

Bei einer Aufgabe zu einem Projekt steht der Projektname unter dem Titel. Tippe darauf, um das Projekt zu öffnen. Unter **Details** kannst du mit **Projekt** das Projekt ändern oder entfernen. Siehe [Aufgaben eines Projekts](projects.md#a-projects-to-dos).

Mit **Bereich** unter **Details** verschiebst du eine Aufgabe in deinen anderen Bereich. Der Bereich bestimmt auch, welche Nachrichten sie lesen und senden darf. Mit **Rückgängig** in der Meldung verschiebst du sie zurück.

Wenn eine Aufgabe den anderen Bereich braucht, um weiterzukommen, und alle Nachrichten, auf denen sie basiert, dort sind, wird sie automatisch dorthin verschoben und fortgesetzt. Andernfalls wird **Nach Arbeit verschieben** angezeigt. Erst wenn du darauf tippst, wird etwas verschoben. Eine Aufgabe, die du ohne Auswahl von „Arbeit“ oder „Privat“ hinzugefügt hast, wird automatisch verschoben, sobald klar ist, wohin sie gehört. Bis dahin gehört sie weder zu „Arbeit“ noch zu „Privat“ und bleibt privat.

Eine Aufgabe kann immer die Nachrichten lesen, auf denen sie basiert. Wenn sie andere Nachrichten aus deinem anderen Bereich braucht, fragt sie mit **Diese E-Mail für diese Aufgabe verwenden** nach. Ein geschäftliches Postfach, das du als „Privat“ markiert hast, zählt als privat. E-Mails für ein anderes deiner Unternehmen gehören zu den Aufgaben dieses Unternehmens. Eine Aufgabe zu deinem Privatleben, etwa wenn deine Familie dir an deine geschäftliche Adresse schreibt, ist von Anfang an privat.

Arbeit, die dich über ein persönliches Konto erreicht, etwa eine Nachricht von einem Kunden auf WhatsApp oder eine Bestellung in deinem privaten Postfach, ist von Anfang an Arbeit. Eine Aufgabe, die du selbst verschoben oder zugeordnet hast, bleibt immer dort, wo du sie abgelegt hast. „Arbeit“ oder „Privat“ bestimmt, wo eine Aufgabe angezeigt wird und mit wem sie geteilt wird, aber nie, wohin sie antwortet: Eine Antwort geht immer dorthin, wo die Unterhaltung stattfindet, auch nach dem Verschieben, außer du wählst einen anderen Weg.

Bei einer solchen privaten Aufgabe wird trotzdem von der geschäftlichen Adresse aus geantwortet, an die die E-Mail geschickt wurde. Sie wird nie in einer geschäftlichen Fleet oder im Team Graph angezeigt.

Wenn mindestens zwei Aufgaben auf dich warten, kannst du mit **Durchgehen** in der Kopfzeile von „Für dich“ nacheinander durch sie gehen, jeweils in der Reihenfolge der Liste. Jeder Entwurf wird vollständig angezeigt, mit **Senden** oder **Ausführen**, **Änderungen anfragen**, **Zurückstellen** und **Überspringen**. Auf einem Computer sendet Enter den angezeigten Inhalt, `S` stellt zurück, `→` überspringt und Esc bricht ab. Unter dem Titel gibt die Kopfzeile auch an, wie lange die Aufgaben dauern, wenn du sie in deinem eigenen Tempo bearbeitest, zum Beispiel „etwa 2 Min.“.

Eine Aufgabe, die dir eine Frage stellt, wird bei beidem ausgelassen: Sie wartet auf deine Antwort, nicht auf einen Tipp.

## Jetzt prüfen

Deine Machine liest jede Quelle alle paar Minuten, Tag und Nacht. Sie prüft neue Nachrichten, sobald 40 davon vorliegen oder die älteste Nachricht einer Person seit 15 Minuten wartet. Newsletter, Benachrichtigungen und Belege werden bei der nächsten Prüfung berücksichtigt, spätestens innerhalb einer Stunde.

Nachts, von 00:00 bis 06:30, werden Prüfungen pausiert. Neue Nachrichten werden weiterhin gelesen und gespeichert und um 06:30 gemeinsam geprüft. So sind deine Aufgaben vor der morgendlichen Zusammenfassung bereit. Unter „Verbindungen“ steht bei den Prüfungen: „Über Nacht pausiert, wird um 06:30 nachgeholt“. Wenn du nachts die App öffnest, im Chat schreibst oder auf eine Aufgabe tippst, laufen die Prüfungen wieder wie gewohnt, bis du eine Stunde lang nicht da warst. **Jetzt prüfen** startet immer sofort eine Prüfung.

**Jetzt prüfen** liest sofort alle Quellen. Wenn keine Aufgaben offen sind, tippe auf die Zeile deiner Machine, um sie mit **Details** zu sehen. Damit öffnest du die Prüfungen unter „Verbindungen“. Wenn Aufgaben offen sind, findest du die Zeile oben auf dem Computer. Sie wird nur angezeigt, während eine Prüfung läuft oder wenn eine fehlgeschlagen oder verspätet ist. Du kannst auch im Chat danach fragen.

LinkedIn, X und Salesflare haben ihren eigenen Rhythmus.

## Letzte Prüfung

Nach einer Prüfung, bei der neue Nachrichten gelesen wurden, zeigt eine Zeile über deinen Aufgaben, was gefunden wurde, aus allen gelesenen Quellen, zum Beispiel „13 Nachrichten um 16:11 geprüft · nichts braucht dich“ oder „· 2 neue Aufgaben“. Wenn eine neue Aufgabe bis zu einem passenden Zeitpunkt zurückgestellt wird, etwa bis zur morgendlichen Zusammenfassung, steht dort, bis wann: „1 Aufgabe bis morgen 08:30 zurückgestellt“.

Tippe auf die Zeile, um jeden E-Mail-Thread, Chat und jede Benachrichtigung mit dem Symbol der jeweiligen Quelle zu sehen: wer geschrieben hat, den Betreff oder die ersten Wörter sowie die neue Aufgabe oder den Grund, warum nichts gebraucht wurde, zum Beispiel „Nur in cc, ein Teammitglied antwortet“ oder „Termin für Donnerstag steht bereits“. Bei einem Thread wird kein Grund angezeigt, wenn die Prüfung nur einen vagen Grund ergeben hat. Tippe auf einen Eintrag, um ihn zu lesen.

Die ersten 10 werden angezeigt. Mit einem Tipp darunter siehst du die übrigen. Eine Zahl hinter einem Namen, zum Beispiel (3), gibt an, wie viele neue Nachrichten der Chat hat. Eine Benachrichtigung auf dem Handy zu einer bereits aufgelisteten Nachricht wird nur einmal angezeigt. Die Zeile bleibt 12 Stunden nach der Prüfung sichtbar.

Gezählt werden nur E-Mails an dich. Deine eigenen Antworten werden als Kontext und für Versprechen gelesen, gelten aber nicht als neue E-Mails. E-Mails von The Machine an dich, etwa die morgendliche Zusammenfassung oder ein Hinweis auf eine Fehlerbehebung, werden nie gelesen oder aufgelistet. E-Mails zu Abrechnung, Testzeitraum oder Einladungen werden wie gewohnt gelesen.

## Die Schaltflächen

Bei einer Aufgabe wird der nächste Schritt angezeigt, zum Beispiel **Ausführen** oder **Prüfen und senden**, daneben **Zurückstellen**. Siehe [Ausführen](do-it.md) und [Zurückstellen](snooze.md).

Mit **Änderungen anfragen** kannst du angeben, was geändert werden soll: wie die Aufgabe ausgeführt werden soll oder, sobald ein Entwurf bereit ist, was daran geändert werden soll. **Als erledigt markieren** bedeutet, dass die Aufgabe erledigt ist. Bei einer vorbereiteten Aufgabe ohne Entwurf ist die Option direkt sichtbar. Andernfalls findest du sie oben unter **…**, auch bei einer Aufgabe, für die du eine Entscheidung treffen musst. Die Aufgabe wird sofort aus der Liste entfernt. In der Meldung findest du **Rückgängig**. Wische die Meldung weg oder zieh sie mit der Maus aus dem Fenster, um sie schneller zu schließen. Die Änderung bleibt bestehen.

Wenn du die Aufgabe anders erledigen lassen möchtest, sag es im **Chat**.

Unter **…**:

- **Übergeben…**: Übergib die Aufgabe an ein Teammitglied, an [Claude Code oder Codex](hand-to-agent.md) oder [bitte jemanden um eine Prüfung](ask-to-review.md).
- **Wiederholen…**: Die Aufgabe [kommt regelmäßig zurück](recurring.md).
- **Nicht nötig**: Die Aufgabe verschwindet. Du kannst optional einen Grund auswählen: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Tippe auf den Titel oder unter **Details** auf **Name**, um die Aufgabe umzubenennen. Dein Titel bleibt bestehen.

Mit **Wieder öffnen** holst du eine geschlossene Aufgabe zurück. Sie kommt auch automatisch zurück, wenn etwas Neues passiert, etwa wenn die Person dir eine neue Nachricht schickt. Deine eigene Antwort reicht dafür nicht aus.

Eine Rechnung, die du selbst bezahlen musst, egal aus welchem Land, wird mit Betrag, Fälligkeitsdatum und den Zahlungsdetails aus der Rechnung zu einer Aufgabe. Automatisch bezahlte Rechnungen, etwa per Lastschrift oder mit einer hinterlegten Karte, werden nicht zu Aufgaben. Wenn eine spätere E-Mail zeigt, dass die Rechnung bezahlt wurde, etwa eine Zahlungsbestätigung des Absenders, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Eine Aufgabe, die nur bis zu einem bestimmten Zeitpunkt wichtig ist, etwa eine Bestätigung vor einem Termin, wird danach automatisch geschlossen. Sie wird als „Nicht mehr nötig“ nach **Erledigt / verworfen** verschoben. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Bevor eine Nachricht oder eine Übergabe für jemanden als bereit angezeigt wird, prüft deine Machine die letzten Chats mit den beteiligten Personen, auch Gruppenchats, und wartet darauf, dass Slack sie gelesen hat. Wenn eine spätere Nachricht zeigt, dass die Aufgabe bereits erledigt ist, etwa weil jemand gefragt wurde und zugesagt hat, wird sie automatisch geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Wenn eine neuere Nachricht den Plan ändert, etwa wenn eine Party an einen anderen Ort verlegt oder eine Buchung storniert wird, aktualisiert The Machine die Aufgaben selbst. Eine Aufgabe, die weiterhin wichtig ist, folgt dem neuen Plan. Wenn nichts mehr zu tun ist, wird sie als „Nicht nötig“ nach **Erledigt / verworfen** verschoben. Im Chat steht „Aktualisiert:“ mit dem Grund. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Bei deinen ersten Aufgaben wird ein kurzer Tipp mit den wichtigsten Aktionen angezeigt: **Änderungen anfragen** und **Nicht nötig**. Außerdem erfährst du, dass nichts gesendet wird, bevor du auf **Senden** tippst. Der Tipp wird dauerhaft ausgeblendet, sobald du seine Schaltfläche verwendest oder auf × tippst.

An deinem ersten Tag begrüßt dich deine Machine oben auf der Seite „Aufgaben“ und nennt die Person, die am längsten auf deine Antwort wartet. Für diese Person wird zuerst ein Entwurf erstellt, damit er bereit ist, wenn du kommst.

Jede Aufgabe beginnt mit ihrem Titel. Die Zeile darunter nennt die Person, um die es geht, gegebenenfalls die Organisation (nicht allein deshalb, weil jemand dort arbeitet), das Projekt, „Arbeit“ oder „Privat“ und den Zeitpunkt, zu dem die Aufgabe eingegangen ist. Tippe auf einen Namen, um die Seite der Person im Graph zu öffnen.

Bei Namen und Organisationen wird das Foto oder Logo angezeigt, wenn es im Graph vorhanden ist, andernfalls die Initialen. Wenn ein Logo in dieser Größe nicht lesbar wäre, etwa weiße Schrift auf transparentem Hintergrund oder ein breites Wortlogo, werden ebenfalls die Initialen angezeigt.

Manchmal steht in einer unauffälligen Zeile, was nicht bekannt ist, zum Beispiel „Letzter Kontakt vor 12 Tagen per E-Mail; seitdem nichts.“ Sie wird angezeigt, wenn der letzte Kontakt mit der Person lange zurückliegt oder unbeantwortet ist. Außerdem werden nicht verbundene Kanäle wie WhatsApp genannt. Deine Machine sagt, was sie nicht weiß, statt zu raten.

Wenn ein nicht verbundener Kanal genannt wird, öffnet **Verbinden** daneben diese Verbindung.

Ein Titel beschreibt, was zu tun ist, und ändert sich nur, wenn sich die Aufgabe ändert. Eine erledigte Aufgabe behält ihren Titel. Darunter steht, wie sie erledigt wurde, zum Beispiel „Erledigt: Sam hat am Dienstag unterschrieben“.

Über dem Entwurf nennt eine blasse Zeile die Nachricht, aus der er entstanden ist, mit dem Logo des jeweiligen Dienstes. Tippe darauf, um den Thread zu lesen. Beim Entwurf wird das Logo des Ziels angezeigt. So siehst du sofort, ob es eine Slack-Antwort oder eine E-Mail ist.

Wenn der Entwurf auf den Vorschlag einer Person an anderer Stelle zurückgeht, etwa auf den Vorschlag eines Teammitglieds in Slack, steht das in einer Zeile, zum Beispiel „Basiert auf Sam in #ops“. Tippe darauf, um die Nachricht zu lesen.

Ein Chat (Slack, WhatsApp, Telegram, Intercom…) wird als eine Unterhaltung angezeigt, von der ältesten Nachricht an: mit den Nachrichten vor der Nachricht, auf die sich die Aufgabe bezieht, und den Antworten danach. In WhatsApp, Telegram oder Signal stehen deine Nachrichten wie in der App rechts. Die Nachricht der Aufgabe ist mit „Diese Aufgabe“ markiert und wird in der Ansicht geöffnet. Mit **Frühere Nachrichten anzeigen** werden ältere Nachrichten hinzugefügt. Eine E-Mail zeigt die übrigen Nachrichten des Threads eingeklappt darüber und darunter.

Unter **Details** einer E-Mail werden nur Angaben angezeigt, die nicht im Kopfbereich stehen, etwa vollständige Cc-Adressen, Bcc oder eine abweichende Antwortadresse. Wenn es nichts hinzuzufügen gibt, werden keine Details angezeigt.

Bei einer Antwort in einem Slack-Thread wird auch angezeigt, was vor Beginn des Threads gesagt wurde. Über den Link einer Aufgabe zu ihrer eigenen Nachricht wird sie ebenfalls hier geöffnet. Unten findest du **In Slack öffnen**.

Unter **Details** findest du den Namen, das Projekt und den Bereich (tippe auf einen Eintrag, um ihn zu ändern), deine letzte Notiz und das Ergebnis eines Coding-Agenten. Mit **Chat ›** öffnest du den Chat. Eine erledigte Aufgabe bleibt kurz. Die Nachricht, aus der sie entstanden ist, steht unter **Details**.

Bei einer Aufgabe mit dem Hinweis „Wartet auf“ ist deine letzte Nachricht an die Person verknüpft, auf die du wartest: „E-Mail an Pat · Di“.

## Selbst eine Aufgabe erstellen

Mit **Neue Aufgabe** (auf einem Computer unter **Suchen**) kannst du eine Aufgabe für alles erstellen. Beim Erstellen wird nichts gesendet. Wenn du weder „Arbeit“ noch „Privat“ auswählst, wird die Aufgabe je nach Person und Thema dem passenden Bereich zugeordnet. Die E-Mail, um die es geht, wird ebenfalls gefunden, auch wenn sie schon älter ist.

- **Fällig**: Gib einen Tag oder eine Uhrzeit ein, zum Beispiel „morgen“, „nächsten Fr“, „3. Nov.“, „14 Uhr“ oder „in 2 Stunden“, auch in deiner Sprache. Über das Kalendersymbol findest du Schnelloptionen und **Datum wählen**.
- **Nachricht**: Hänge die Nachricht an, um die es geht: eine E-Mail, Slack-, Teams-, WhatsApp-, Telegram- oder eine andere Nachricht, die The Machine vorliegt. Suche nach Text oder Absender. Bei jedem Ergebnis siehst du, woher es stammt, wer es gesendet hat und wann.
- **Dateien**: Tippe auf die Büroklammer, füge einen Screenshot ein oder zieh Dateien auf das Formular. Auf dem Handy kannst du mit der Kamera daneben ein Foto aufnehmen. Wie im Chat sind bis zu 5 Dateien möglich (siehe [Dateien hinzufügen](card-chat.md#add-files)). Mit × entfernst du eine Datei.

Die Dateien bleiben bei der Aufgabe, und The Machine liest sie, wenn sie daran arbeitet. Dateien allein reichen aus: Aus einer PDF- oder Textdatei erstellt The Machine die Aufgabe. Ein Foto wird als kleines Bild angezeigt. Tippe darauf, um es in voller Größe zu sehen.
