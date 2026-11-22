---
title: Aufgaben
area: cards
summary: Eine Aufgabe pro Sache, bei der du gefragt bist, bereit für dein Ja. Was die einzelnen Teile einer Aufgabe bedeuten.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: e7e5d78b3291e556
---
Deine Machine liest alles Neue und erstellt nur dann eine Aufgabe, wenn etwas von dir gebraucht wird. Eine Aufgabe pro Angelegenheit, egal über wie viele Nachrichten sie sich erstreckt.

## Wo Aufgaben zu finden sind

Auf der Seite **Aufgaben** sind sie gruppiert:

- **Gerade erledigt**: Ganz oben findest du einen letzten Schritt, den du bestätigt hast, zum Beispiel ein Formular oder ein Problem, das während deiner Abwesenheit erledigt wurde. Er bleibt höchstens einen Tag dort, bis du auf **Verstanden** tippst. Auch auf deinem Handy bekommst du eine Benachrichtigung.
- **Für dich**: Alles, was auf dich wartet, nach Dringlichkeit sortiert. Bei jeder Aufgabe steht **Vorbereitet** (ein Entwurf oder Ergebnis ist bereit und wird mit **Ausführen** oder **Senden** umgesetzt), **Braucht dich** (zuerst braucht es deine Entscheidung oder Antwort; wenn die Arbeit an etwas liegt, das nur du hast, etwa einer Information, einer Anmeldung oder einer Auswahl, steht unter dem Titel, worum es geht), **Wird vorbereitet…** (deine Machine arbeitet daran) oder **Zum Lesen** (eine Zusammenfassung oder ein Briefing, bei dem nichts entschieden werden muss).
- **Älter**: Eingeklappte Aufgaben, bei denen es seit einer Woche nichts Neues gab (siehe unten).
- **Wartet auf andere**: Eingeklappte Aufgaben, bei denen der nächste Schritt bei jemand anderem liegt (siehe unten).
- **Kommt später zurück**: Zurückgestellte Aufgaben und Aufgaben, auf die es keine Antwort auf **Noch nötig?** gab (siehe unten).
- **Versprechen**: Was du versprochen hast und was andere dir versprochen haben. Mehr dazu unter [Versprechen](promises.md).
- **Erledigt / verworfen**: Alle abgeschlossenen Aufgaben, neueste zuerst, mit dem Zeitpunkt des Abschlusses, zum Beispiel „Vor 5 Minuten erledigt“. Aufgaben, die bereits abgeschlossen zu sein scheinen, sind mit **Sieht erledigt aus** markiert.

Nach dem Senden steht in einer kurzen Meldung, wohin die Aufgabe verschoben wurde, zum Beispiel „Gesendet. Nach Erledigt verschoben.“ oder „Gesendet. Auf Später verschoben, bis Mo.“ Eine Antwort, in der nur die Arbeit versprochen wird, etwa „Ich schicke es bis Dienstag“, lässt die Aufgabe offen: „Gesendet. Offen gelassen.“ Mit **Öffnen** gelangst du zur Aufgabe. Über die Suche findest du Aufgaben anhand ihres Titels oder danach, an wen sie gingen. Auch in Später und Erledigt.

Unter **Für dich** stehen zuerst überfällige Aufgaben und Aufgaben, die bis morgen fällig sind, dann Fragen aus deiner Fleet, danach Nachfassnachrichten eines Boards und schließlich alle übrigen. Innerhalb jeder Gruppe stehen die neuesten zuerst. Eine Aufgabe bleibt an derselben Stelle, während deine Machine sie vorbereitet und auch, wenn sie erledigt ist. Nur ihre Markierung ändert sich. In den anderen offenen Gruppen stehen überfällige Aufgaben und Aufgaben, die bis morgen fällig sind, zuerst, danach folgen die übrigen nach Aktualität. Die Seitenleiste behält dieselbe Reihenfolge bei.

**Sieht erledigt aus** bedeutet, dass deine Machine die Aufgabe für abgeschlossen hält, zum Beispiel „PR #3451 zusammengeführt“, sie aber noch nicht geschlossen ist. Mit **Wieder öffnen** kommt sie zurück in deine Liste, und deine Machine lernt daraus. Diese Aufgaben werden nie als überfällig angezeigt. Nach einem Tag wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Eine Aufgabe, die du bereits selbst erledigt hast, zum Beispiel mit einer Antwort in Gmail oder Slack, wird ebenfalls automatisch geschlossen.

Wenn eine Nachricht von einer Adresse kommt, die nur wie die Adresse einer Person aussieht, die du kennst, zum Beispiel sam@acme-corp.example statt sam@acmecorp.example, steht in der Aufgabe klar und deutlich: „Das ist nicht Sam Lee.“ Die Person wird mit ihrer eigenen Adresse angezeigt, niemals mit dem Namen, den sie verwendet hat. Deine Machine prüft solche Nachrichten bei der Person unter der Adresse, die du bereits hast, niemals bei der Person, die geschrieben hat.

Bei einer Aufgabe, die noch auf jemand anderen wartet, etwa auf eine Prüfung oder Antwort, steht **Wartet auf:** gefolgt von diesem Schritt. Sie erscheint eingeklappt in **Wartet auf andere**, oberhalb von Kommt später zurück, bis eine neue Nachricht sie wieder hervorholt. Dasselbe gilt, wenn du eine Rückfrage gestellt hast: Die Aufgabe kommt am Morgen vor ihrer Frist zurück, bei einer Frist noch heute zum Zeitpunkt der Frist oder am nächsten Morgen, wenn die Frist schon vorbei ist. Außerdem steht dort, auf wen sie noch wartet.

Wenn es bei einer Aufgabe um ein Ergebnis geht, das jemand anderes liefern soll, etwa einen unterschriebenen Vertrag, wird es unter **Details** als **Fertig, wenn** angezeigt. Wenn du deinen Teil sendest, wird die Aufgabe nicht geschlossen. Sie bleibt unter **Wartet auf andere**, bis eine Nachricht das Ergebnis bestätigt. Dann wird sie automatisch geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Wenn bis zum Zeitpunkt, an dem du nachhaken solltest, nichts eintrifft, erscheint die Aufgabe mit **Schreib eine kurze Erinnerung** im Chat. Schreib im Chat, was als erledigt gilt, um das zu ändern.

Eine Aufgabe, bei der es seit einer Woche nichts Neues gab, wird von Für dich nach **Älter** verschoben. So stehen nach ein paar Tagen Abwesenheit die frischen Aufgaben zuerst. Als „nichts Neues“ zählt weder eine neue Nachricht dazu noch etwas, das du daran gemacht hast, etwa eine Chatnachricht, eine Bearbeitung oder ein Zurückstellen. Nur die Aufgabe anzusehen zählt nicht.

Dringende Aufgaben, bald fällige Aufgaben und Aufgaben, bei denen gerade etwas gesendet wird, bleiben unter Für dich. Mit **Alle verwerfen** kannst du nach einer Bestätigung alle Aufgaben unter Älter als nicht nötig markieren. Das geht auch einzeln mit **Nicht nötig**. Mit **Rückgängig** kannst du das rückgängig machen. Gibt es bei einer Aufgabe etwas Neues, kommt sie zurück zu Für dich.

Wenn eine Aufgabe eine Woche lang niemanden beschäftigt hat, fragt sie einmal: **Noch nötig?** Mit **Nicht nötig** wird sie geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Mit **Behalten** bleibt sie erhalten und fragt nie wieder nach. Kommt eine weitere Woche lang keine Antwort, wird sie unter Kommt später zurück eingeklappt und nicht mehr auf dem App-Symbol oder in der morgendlichen Zusammenfassung mitgezählt. Wenn du sie öffnest, eine Chatnachricht schreibst, sie bearbeitest, zurückstellst oder eine neue Nachricht dazu kommt, erscheint sie wieder.

Einmal pro Woche kann für ein Projekt, bei dem nichts mehr offen ist und das eingeschlafen ist, eine Aufgabe mit einem konkreten nächsten Schritt erstellt werden. Höchstens drei pro Woche. Mehr dazu unter [Projekte](projects.md).

Wenn nichts deine Aufmerksamkeit braucht, macht deine Machine ein Nickerchen und die Liste bleibt leer. Während sie prüft, wird sie aktiv und zeigt das an. Wenn eine Prüfung fehlgeschlagen ist oder sich verzögert, steht das in der Zeile. Darunter findest du **Jetzt prüfen**.

Mit **Alle**, **Arbeit** und **Privat** oben in der Seitenleiste kannst du alle Aufgaben oder nur eine Art anzeigen. Auf Handy und Computer wird dieselbe Auswahl verwendet. Wenn Arbeit oder Privat ausgewählt ist, führt **Alle anzeigen** zurück zur Gesamtansicht. Eine Benachrichtigung über deine Machine selbst, etwa dass ein Teil immer wieder neu startet, gehört weder zu Arbeit noch zu Privat und wird nur unter Alle angezeigt.

Über die Zeile oben in der Liste kannst du auch direkt zur anderen Ansicht wechseln: Tippe unter **Nur privat** auf **Arbeit** oder **Alle anzeigen**.

In der Zeile ganz oben in der Liste stehen der Name deiner letzten morgendlichen oder abendlichen Zusammenfassung und die Anzahl der darin erfassten Aufgaben, zum Beispiel **Zusammenfassung von gestern Abend** · 12 erledigt, 3 offen. Tippe darauf, um die Zusammenfassung erneut zu lesen. Mit **Kopieren** kannst du sie an beliebiger Stelle einfügen. Sobald du sie öffnest oder auf ihr **×** tippst, bleibt sie auf all deinen Geräten, bis die nächste Zusammenfassung kommt.

Wenn es keine aktuelle Zusammenfassung gibt, wird **Heute bisher** angezeigt: Was heute erledigt wurde und was noch offen ist, für Arbeit und Privat oder nur für den Bereich, den du ausgewählt hast.

Bei einer Aufgabe zu einem Projekt steht der Projektname unter dem Titel. Tippe darauf, um das Projekt zu öffnen. Unter **Details** kannst du mit **Projekt** das Projekt ändern oder die Aufgabe daraus entfernen. Mehr dazu unter [Aufgaben eines Projekts](projects.md#a-project-s-to-dos).

Mit **Bereich** unter **Details** verschiebst du eine Aufgabe in deinen anderen Bereich. Der Zugriff auf Nachrichten, die sie lesen und senden darf, ändert sich entsprechend. Mit **Rückgängig** in der Meldung verschiebst du sie zurück.

Wenn eine Aufgabe deinen anderen Bereich braucht, um fortzufahren, und alle Nachrichten, aus denen sie entstanden ist, zu diesem Bereich gehören, wird sie automatisch dorthin verschoben und fortgesetzt. Andernfalls wird **Nach Arbeit verschieben** angezeigt. Erst wenn du darauf tippst, wird etwas verschoben. Eine Aufgabe, die du hinzugefügt hast, ohne Arbeit oder Privat auszuwählen, wird automatisch dem passenden Bereich zugeordnet, sobald klar ist, wo sie hingehört. Bis dahin gehört sie weder zu Arbeit noch zu Privat und bleibt privat.

Eine Aufgabe kann immer die Nachrichten lesen, aus denen sie entstanden ist. Wenn sie weitere Nachrichten aus deinem anderen Bereich braucht, fragt sie mit **Diese E-Mail für diese Aufgabe verwenden** danach. Ein Arbeits-Postfach, das du als Privat gekennzeichnet hast, zählt als Privat. E-Mails für ein anderes deiner Unternehmen gehören zu den Aufgaben dieses Unternehmens. Eine Aufgabe über dein Privatleben, zum Beispiel eine Nachricht von deiner Familie an deine Arbeitsadresse, ist von Anfang an privat.

Arbeit, die dich über ein privates Konto erreicht, zum Beispiel eine Nachricht von einem Kunden auf WhatsApp oder eine Bestellung in deinem privaten Postfach, ist von Anfang an Arbeit. Eine Aufgabe, die du selbst verschoben oder einem Bereich zugeordnet hast, bleibt immer dort. Arbeit oder Privat legt fest, wo eine Aufgabe angezeigt und mit wem sie geteilt wird, aber nicht, wohin sie antwortet. Eine Antwort geht immer dorthin, wo das Gespräch stattfindet, auch nach dem Verschieben, sofern du keinen anderen Weg auswählst.

Eine solche private Aufgabe antwortet weiterhin von der Arbeitsadresse aus, an die ihre E-Mail geschickt wurde. Sie wird nie in einer Work Fleet oder im Team Graph angezeigt.

Wenn mindestens zwei Aufgaben auf dich warten, kannst du mit **Durchgehen** in der Kopfzeile von Für dich nacheinander durch sie gehen, in der Reihenfolge der Liste. Du siehst jeden vollständigen Entwurf sowie **Senden** oder **Ausführen**, **Änderungen anfragen**, **Zurückstellen** und **Überspringen**. Am Computer wird mit Enter gesendet, was auf dem Bildschirm zu sehen ist, mit `S` zurückgestellt, mit `→` übersprungen und mit Esc abgebrochen. Unter dem Titel steht in der Kopfzeile auch, wie lange du ungefähr brauchst, wenn du dir Zeit lässt, zum Beispiel „etwa 2 Min.“

Eine Aufgabe, die dir eine Frage stellt, wird dabei ausgelassen: Sie braucht deine Antwort, keinen Tipp.

## Jetzt prüfen

Deine Machine liest jede Quelle alle paar Minuten, Tag und Nacht. Sie prüft, was eingegangen ist, sobald 40 Nachrichten vorliegen oder die älteste Nachricht einer Person 15 Minuten gewartet hat. Newsletter, Benachrichtigungen und Belege werden innerhalb einer Stunde bei der nächsten Prüfung berücksichtigt.

Nachts, von 00:00 bis 06:30 Uhr, pausieren die Prüfungen. Neue Nachrichten werden weiterhin gelesen und gespeichert und um 06:30 Uhr gemeinsam geprüft, damit deine Aufgaben vor der morgendlichen Zusammenfassung bereit sind. Unter Verbindungen steht bei den Prüfungen: „Nachts pausiert, Aufholen um 06:30 Uhr“. Wenn du nachts in der App klickst, tippst oder scrollst, im Chat schreibst oder auf eine Aufgabe tippst, laufen die Prüfungen wie gewohnt weiter, bis du eine Stunde lang abwesend warst. Mit **Jetzt prüfen** wird immer sofort geprüft.

Mit **Jetzt prüfen** werden alle Quellen sofort gelesen. Wenn nichts offen ist, tippe auf die Zeile deiner Machine, um sie mit **Details** aufzurufen. Dadurch werden die Prüfungen unter Verbindungen geöffnet. Wenn Aufgaben offen sind, findest du die Zeile am Computer ganz oben. Dort wird nur während einer Prüfung eine kurze Meldung angezeigt oder wenn eine Prüfung fehlgeschlagen ist oder sich verzögert. Du kannst auch im Chat danach fragen.

LinkedIn, X und Salesflare haben ihren eigenen Rhythmus.

## Letzte Prüfung

Nach einer Prüfung, bei der neue Nachrichten gelesen wurden, steht über deinen Aufgaben, was gefunden wurde. Die Meldung umfasst alle gelesenen Quellen, zum Beispiel „13 Nachrichten um 16:11 geprüft · nichts braucht dich“ oder „· 2 neue Aufgaben“. Wenn eine neue Aufgabe auf einen günstigeren Zeitpunkt wartet, etwa auf deine morgendliche Zusammenfassung, steht dort, bis wann: „1 Aufgabe bis morgen 08:30 zurückgestellt“.

Tippe auf die Zeile, um die einzelnen E-Mail-Threads, Chats und Benachrichtigungen mit dem Symbol ihrer Quelle zu sehen: wer geschrieben hat, den Betreff oder die ersten Wörter sowie die neue Aufgabe oder den Grund, warum nichts nötig war, zum Beispiel „Nur in Cc, ein Teammitglied antwortet“ oder „Besprechung bereits für Donnerstag angesetzt“. Bei einem Thread wird kein Grund angezeigt, wenn die Prüfung nur einen vagen Grund ergeben hat. Tippe auf einen Eintrag, um ihn zu lesen.

Die ersten 10 werden angezeigt. Tippe darunter, um den Rest zu sehen. Eine Zahl nach einem Namen, zum Beispiel (3), gibt an, wie viele neue Nachrichten dieser Chat enthält. Eine Handy-Benachrichtigung zu einer bereits aufgeführten Nachricht wird nur einmal angezeigt. Die Zeile bleibt nach der Prüfung 12 Stunden lang sichtbar.

Gezählt werden nur E-Mails an dich. Deine eigenen Antworten werden berücksichtigt, um den Zusammenhang und Versprechen zu verstehen, zählen aber nicht als neue E-Mails. E-Mails von The Machine an dich, etwa deine morgendliche Zusammenfassung oder ein Hinweis auf eine Fehlerbehebung, werden nie gelesen oder aufgeführt. E-Mails zu Abrechnung, Probezeit oder Einladungen werden wie gewohnt gelesen.

## Die Schaltflächen

Bei einer Aufgabe steht der nächste Schritt, zum Beispiel **Ausführen** oder **Prüfen und senden**, daneben **Zurückstellen**. Mehr dazu unter [Ausführen](do-it.md) und [Zurückstellen](snooze.md).

Mit **Änderungen anfragen** kannst du angeben, was geändert werden soll: wie etwas erledigt werden soll oder, sobald ein Entwurf bereit ist, was daran geändert werden soll. **Als erledigt markieren** bedeutet, dass die Aufgabe erledigt ist. Bei einer fertigen Aufgabe ohne Entwurf ist die Schaltfläche direkt zu sehen, andernfalls findest du sie oben unter **…**, auch bei Aufgaben, die deine Entscheidung brauchen. Die Aufgabe wird sofort aus der Liste entfernt. In der Meldung findest du **Rückgängig**. Wische die Meldung weg oder zieh sie mit der Maus aus dem Fenster, um sie schneller zu schließen. Die Änderung bleibt bestehen.

Wenn du möchtest, dass es anders erledigt wird, schreib es im **Chat** der Aufgabe.

Unter **…**:

- **Übergeben…**: Übergib die Aufgabe einem Teammitglied, [Claude Code oder Codex](hand-to-agent.md) oder [bitte jemanden um eine Prüfung](ask-to-review.md).
- **Wiederholen…**: Die Aufgabe [kommt regelmäßig wieder](recurring.md).
- **Nicht nötig**: Die Aufgabe wird entfernt. Optional kannst du den Grund auswählen: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Tippe auf den Titel oder unter **Details** auf **Name**, um die Aufgabe umzubenennen. Du kannst auch im Chat darum bitten, zum Beispiel: „Benenne sie in … um.“ Dein Titel bleibt bestehen.

Mit **Wieder öffnen** holst du eine geschlossene Aufgabe zurück. Sie kommt auch automatisch wieder, wenn etwas Neues passiert, zum Beispiel eine neue Nachricht von der anderen Person, aber nicht, wenn du selbst antwortest. Dann wird angezeigt, wann sie zurückgekommen ist, und sie wird wie eine neue Aufgabe sortiert. Der Chat macht dort weiter, wo er aufgehört hat, auch nach mehreren Wochen.

Eine Rechnung, die du selbst noch bezahlen musst, egal aus welchem Land, wird zu einer Aufgabe mit Betrag, Fälligkeitsdatum und den Zahlungsinformationen auf der Rechnung. Automatisch bezahlte Rechnungen, etwa per Lastschrift oder mit einer hinterlegten Karte, werden nicht hinzugefügt. Wenn eine spätere E-Mail zeigt, dass sie bezahlt wurde, etwa eine Bestätigung des Absenders über den Zahlungseingang, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Eine Aufgabe, die nur bis zu einem bestimmten Zeitpunkt wichtig war, etwa eine Bestätigung vor einer Besprechung, wird nach diesem Zeitpunkt automatisch geschlossen. Sie wird als „Nicht mehr nötig“ nach **Erledigt / verworfen** verschoben. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Bevor eine Nachricht oder Übergabe an jemanden als bereit angezeigt wird, prüft deine Machine deine letzten Chats mit den beteiligten Personen, auch Gruppenchats, und wartet darauf, dass Slack sie gelesen hat. Wenn eine spätere Nachricht zeigt, dass die Aufgabe bereits erledigt ist, etwa weil die Person gefragt wurde und zugestimmt hat, wird sie automatisch geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Wenn eine neuere Nachricht den Plan ändert, etwa weil eine Party an einen anderen Ort verlegt oder eine Buchung storniert wurde, aktualisiert The Machine ihre Aufgaben selbst. Eine Aufgabe, die noch wichtig ist, wird an den neuen Plan angepasst. Wenn nichts mehr zu tun ist, wird sie als „Nicht nötig“ nach **Erledigt / verworfen** verschoben. Im Chat steht „Aktualisiert:“ mit dem Grund. Mit **Rückgängig** kannst du sie einen Tag lang wiederherstellen.

Bei deinen ersten Aufgaben zeigt ein kurzer Tipp die wichtigsten Aktionen: **Änderungen anfragen** und **Nicht nötig**. Außerdem weist er darauf hin, dass nichts gesendet wird, bevor du auf **Senden** tippst. Ein Tipp wird dauerhaft ausgeblendet, sobald du seine Schaltfläche verwendest oder auf × tippst.

An deinem ersten Tag begrüßt dich oben auf der Seite Aufgaben eine Nachricht und nennt die Person, die am längsten auf deine Antwort wartet. Diese Antwort wird zuerst als Entwurf erstellt, damit sie bereit ist, wenn du da bist.

Jede Aufgabe beginnt mit ihrem Titel. In der Zeile darunter steht, um wen es geht, gegebenenfalls die Organisation (nicht allein deshalb, weil jemand dort arbeitet), das Projekt, Arbeit oder Privat und der Eingangszeitpunkt. Tippe auf einen Namen, um die Seite der Person im Graph zu öffnen.

Bei einem Namen und einer Organisation wird das Foto oder Logo angezeigt, falls es im Graph vorhanden ist. Andernfalls werden die Initialen verwendet. Wenn ein Logo in dieser Größe nicht lesbar wäre, zum Beispiel weiße Schrift auf transparentem Hintergrund oder ein breites Wortlogo, wird ebenfalls die Initiale angezeigt.

Manchmal steht in einer unauffälligen Zeile, was nicht bekannt ist, etwa „Letzter Kontakt vor 12 Tagen per E-Mail, seither nichts.“ Sie wird angezeigt, wenn der letzte Kontakt mit der Person länger zurückliegt oder unbeantwortet ist. Außerdem werden nicht verbundene Kanäle genannt, etwa WhatsApp. Deine Machine sagt, was sie nicht weiß, anstatt zu raten.

Wenn ein nicht verbundener Kanal genannt wird, öffnet **Verbinden** daneben die entsprechende Verbindung.

Der Titel beschreibt, was zu tun ist, und ändert sich nur, wenn sich das ändert. Eine erledigte Aufgabe behält ihren Titel. Darunter steht, wie sie abgeschlossen wurde, zum Beispiel „Erledigt: Sam hat es am Dienstag unterschrieben“.

Über dem Entwurf steht in einer unauffälligen Zeile, aus welcher Nachricht er entstanden ist, zusammen mit dem Logo des jeweiligen Dienstes. Tippe darauf, um den Thread zu lesen. Beim Entwurf wird das Logo des Ziels angezeigt. So erkennst du sofort, ob es eine Slack-Antwort oder eine E-Mail ist.

Wenn der Entwurf auf einer Eingabe von jemand anderem an anderer Stelle beruht, etwa auf dem Vorschlag eines Teammitglieds in Slack, steht das in einer Zeile, zum Beispiel „Basierend auf Sams Nachricht in #ops“. Tippe darauf, um die Nachricht zu lesen.

Ein Chat (Slack, WhatsApp, Telegram, Intercom …) wird als ein Gespräch angezeigt, mit den ältesten Nachrichten zuerst: die Nachrichten vor der Nachricht, um die es in der Aufgabe geht, und die Antworten danach. In WhatsApp, Telegram oder Signal stehen deine Nachrichten wie in der App rechts. Die Nachricht zur Aufgabe ist mit „Diese Aufgabe“ markiert und wird direkt geöffnet. Mit **Frühere Nachrichten anzeigen** werden ältere Nachrichten hinzugefügt. Bei einer E-Mail wird der restliche Thread oberhalb und unterhalb eingeklappt angezeigt.

Mit **In Gmail öffnen** wird die E-Mail in dem Gmail-Konto geöffnet, in dem sie eingegangen ist. Auf Android wird sie in der Gmail-App geöffnet, sofern du sie installiert hast.

Unter **Details** einer E-Mail stehen nur Angaben, die nicht bereits in ihrem Header zu sehen sind, zum Beispiel vollständige Cc-Adressen, Bcc oder eine andere Antwortadresse. Gibt es nichts hinzuzufügen, werden keine Details angezeigt.

Bei einer Antwort in einem Slack-Thread wird auch angezeigt, was vor Beginn des Threads gesagt wurde. Über den Link einer Aufgabe zur eigenen Nachricht kannst du sie ebenfalls hier öffnen. Unten findest du **In Slack öffnen**.

Unter **Details** stehen der Name, das Projekt und der Bereich der Aufgabe (tippe auf einen Eintrag, um ihn zu ändern), deine letzte Notiz und das Ergebnis eines Programmierassistenten. Über den Titel öffnest du den Chat. Eine erledigte Aufgabe bleibt kompakt. Die Nachricht, aus der sie entstanden ist, findest du unter **Details**.

Bei einer Aufgabe mit „Wartet auf“ führt ein Link zu deiner letzten Nachricht an die Person, auf die du wartest, zum Beispiel: „E-Mail an Pat · Di“.

## Selbst eine Aufgabe erstellen

Mit **Neue Aufgabe** (am Computer unter **Suchen**, auf dem Handy über **+** oder mit `N`) kannst du eine Aufgabe zu einem beliebigen Thema hinzufügen. Beim Erstellen wird nichts gesendet. Wenn du weder **Arbeit** noch **Privat** auswählst, wird die Aufgabe anhand der Person und des Themas dem passenden Bereich zugeordnet. Außerdem findet sie die E-Mail, auf die sie sich bezieht, auch wenn sie schon älter ist.

- **Fällig**: Gib einen Tag oder eine Uhrzeit ein, zum Beispiel „morgen“, „nächsten Fr“, „3. Nov.“, „14 Uhr“ oder „in 2 Stunden“. Das geht auch in deiner Sprache. Über das Kalendersymbol findest du Schnellauswahl und **Datum wählen**.
- **Wiederholt sich**: Die Aufgabe kommt regelmäßig wieder. Mehr dazu unter [Wiederkehrende Aufgaben](recurring.md).
- **Person**: Verknüpfe die Personen oder Unternehmen, um die es geht, bis zu 5.
- Nachrichtensymbol: Hänge die Nachricht an, um die es geht: eine E-Mail, Slack-, Teams-, WhatsApp- oder Telegram-Nachricht oder eine andere Nachricht, auf die The Machine Zugriff hat. Suche nach Text oder Absender. Bei jedem Ergebnis steht, woher es stammt, wer es gesendet hat und wann.
- **Dateien**: Tippe auf die Büroklammer, füge einen Screenshot ein oder zieh Dateien in das Formular. Auf dem Handy kannst du mit der Kamera daneben ein Foto aufnehmen. Bis zu 5 Dateien, wie im Chat (siehe [Dateien hinzufügen](card-chat.md#add-files)). Mit × entfernst du eine Datei wieder.

Die Dateien bleiben bei der Aufgabe, und The Machine liest sie, wenn sie daran arbeitet. Die Dateien allein genügen: Aus einer PDF- oder Textdatei erstellt sie die Aufgabe. Ein Foto wird als kleines Bild angezeigt. Tippe darauf, um es in voller Größe zu sehen.
