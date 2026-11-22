---
title: Aufgaben
area: cards
summary: Eine Aufgabe pro Sache, die dich braucht und auf dein Okay wartet. Was die einzelnen Teile einer Aufgabe bedeuten.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: fef065570d3fd972
---
Deine Machine liest alles Neue und erstellt nur dann eine Aufgabe, wenn etwas dich braucht. Pro Sache gibt es eine Aufgabe, egal über wie viele Nachrichten sie sich erstreckt.

## Wo Aufgaben stehen

Auf der Seite **Aufgaben** sind sie gruppiert:

- **Gerade erledigt**: Ganz oben wird ein letzter Schritt angezeigt, den du bestätigt hast, etwa ein Formular oder ein Problem, das erledigt wurde, während du nicht da warst. Er bleibt höchstens einen Tag dort, bis du auf **Verstanden** tippst. Auch auf deinem Handy bekommst du Bescheid.
- **Für dich**: Alles, worauf du reagieren musst, nach Dringlichkeit sortiert. Bei jeder Aufgabe steht **Vorbereitet** (ein Entwurf oder Ergebnis ist fertig, und mit **Ausführen** oder **Senden** wird es umgesetzt), **Braucht dich** (zuerst braucht es eine Entscheidung oder Antwort von dir; wenn die Arbeit an etwas hängt, das nur du hast, etwa eine Information, eine Anmeldung oder eine Entscheidung, steht unter dem Titel, worum es geht), **Wird vorbereitet…** (deine Machine arbeitet daran) oder **Zum Lesen** (eine Zusammenfassung oder ein Briefing, bei dem du nichts entscheiden musst).
- **Älter**: Eingeklappte Aufgaben, zu denen es seit einer Woche nichts Neues gab (weiter unten).
- **Wartet auf andere**: Eingeklappte Aufgaben, bei denen der nächste Schritt bei jemand anderem liegt (weiter unten).
- **Kommt später zurück**: Zurückgestellte Aufgaben und Aufgaben ohne Antwort auf **Noch nötig?** (weiter unten).
- **Versprechen**: Was du versprochen hast und was andere dir versprochen haben. Mehr dazu unter [Versprechen](promises.md).
- **Erledigt / verworfen**: Alle abgeschlossenen Aufgaben, die neuesten zuerst, mit dem Zeitpunkt des Abschlusses, etwa „Vor 5 Minuten erledigt“. Aufgaben, die offenbar schon abgeschlossen sind, sind mit **Sieht erledigt aus** markiert.

Nach dem Senden steht kurz da, wohin die Aufgabe verschoben wurde, etwa „Gesendet. Zu Erledigt verschoben.“ oder „Gesendet. Bis Mo. auf Später verschoben.“ Eine Antwort, die nur die Arbeit verspricht, etwa „Ich schicke es bis Dienstag“, lässt die Aufgabe offen: „Gesendet. Offen gelassen.“ **Öffnen** bringt dich zur Aufgabe. Über die Suche findest du Aufgaben anhand ihres Titels oder der Person, an die sie gingen, auch unter Später und Erledigt.

Unter **Für dich** stehen zuerst überfällige Aufgaben und Aufgaben, die bis morgen fällig sind, dann Fragen aus deinem Fleet, danach Nachfassnachrichten eines Boards und schließlich der Rest. Innerhalb jeder Gruppe stehen die neuesten zuerst. Eine Aufgabe behält ihren Platz, während deine Machine sie vorbereitet und wenn sie erledigt ist. Nur ihre Markierung ändert sich. In den anderen offenen Gruppen stehen überfällige Aufgaben und Aufgaben, die bis morgen fällig sind, zuerst, danach der Rest, neueste zuerst. In der Seitenleiste gilt dieselbe Reihenfolge.

**Sieht erledigt aus** bedeutet, dass deine Machine die Aufgabe für erledigt hält, etwa weil „PR #3451 zusammengeführt“ wurde, sie aber noch nicht geschlossen ist. Mit **Wieder öffnen** kommt sie zurück in deine Liste. Deine Machine lernt daraus. Solche Aufgaben werden nie als verspätet angezeigt. Wenn eine Nachricht den Abschluss zeigt, wird die Aufgabe nach einem Tag automatisch geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Andernfalls wartet sie auf **Als erledigt markieren**. Eine Aufgabe, die du bereits selbst erledigt hast, etwa durch eine Antwort in Gmail oder Slack, wird ebenfalls automatisch geschlossen.

Wenn eine Nachricht von einer Adresse kommt, die nur wie die einer Person aussieht, die du kennst, etwa sam@acme-corp.example statt sam@acmecorp.example, weist die Aufgabe klar darauf hin: „Das ist nicht Sam Lee.“ Die Person wird mit ihrer tatsächlichen Adresse angezeigt, nie mit dem Namen, den sie verwendet hat. Deine Machine prüft solche Nachrichten bei der Person unter der Adresse, die du bereits hast, nie bei der Person, die geschrieben hat.

Bei einer Aufgabe, die noch auf jemand anderen wartet, etwa auf eine Prüfung oder Antwort, steht **Wartet auf:** mit dem nächsten Schritt. Sie bleibt eingeklappt unter **Wartet auf andere**, oberhalb von „Kommt später zurück“, bis eine neue Nachricht sie wieder nach oben bringt. Das gilt auch, nachdem du eine Rückfrage gestellt hast: Die Aufgabe kommt am Morgen vor dem Abgabetermin zurück, am Abgabetermin, wenn er später am selben Tag liegt, oder am nächsten Morgen, wenn er bereits vorbei ist. Sie zeigt dann, auf wen sie noch wartet.

Wenn es bei einer Aufgabe um ein Ergebnis geht, das jemand anderes liefern muss, etwa einen unterschriebenen Vertrag, wird es unter **Details** bei **Fertig, wenn** angezeigt. Wenn du deinen Teil abschickst, wird die Aufgabe nicht geschlossen. Sie bleibt unter **Wartet auf andere**, bis eine Nachricht das Ergebnis zeigt. Dann wird sie automatisch geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Wenn bis zum Zeitpunkt, zu dem du nachhaken solltest, nichts eingegangen ist, kommt die Aufgabe mit **Schreib eine kurze Erinnerung** in ihrem Chat zurück. Schreib im Chat, was als erledigt gelten soll, um das zu ändern.

Wenn es eine Woche lang nichts Neues zu einer Aufgabe gibt, wandert sie von „Für dich“ zu **Älter**. So stehen nach ein paar Tagen Abwesenheit die neuen Aufgaben oben. „Nichts Neues“ bedeutet, dass es keine neue Nachricht dazu gab und du nichts daran geändert hast, etwa durch eine Chatnachricht, eine Bearbeitung oder Zurückstellen. Nur die Aufgabe anzusehen zählt nicht.

Dringende Aufgaben, bald fällige Aufgaben und Aufgaben, zu denen eine Nachricht unterwegs ist, bleiben unter „Für dich“. Mit **Alle verwerfen** markierst du nach einmaliger Bestätigung alle nicht benötigten Aufgaben unter „Älter“ als **Nicht nötig**, wie du es einzeln mit **Nicht nötig** tun kannst. Mit **Rückgängig** kannst du das rückgängig machen. Sobald es bei einer Aufgabe etwas Neues gibt, kommt sie zurück zu „Für dich“.

Wenn eine Aufgabe eine Woche lang niemand angefasst hat, fragt sie einmal: **Noch nötig?** Mit **Nicht nötig** wird sie geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. **Behalten** lässt sie offen und die Frage wird nicht noch einmal gestellt. Wenn eine weitere Woche lang niemand antwortet, wird sie unter „Kommt später zurück“ eingeklappt. Sie wird dann nicht mehr auf dem App-Symbol oder in der morgendlichen Zusammenfassung mitgezählt. Wenn du sie öffnest, eine Chatnachricht schreibst, sie bearbeitest, zurückstellst oder eine neue Nachricht dazu eingeht, kommt sie wieder zurück.

Ein Projekt, zu dem es ruhig geworden ist und bei dem keine Aufgaben offen sind, kann einmal pro Woche eine Aufgabe mit einem konkreten nächsten Schritt bekommen, höchstens drei pro Woche. Mehr dazu unter [Projekte](projects.md).

Wenn dich nichts braucht, macht deine Machine ein Nickerchen und zeigt eine leere Liste. Während sie prüft, wacht sie auf und zeigt das an. Wenn eine Prüfung fehlgeschlagen ist oder sich verspätet, steht das in der Zeile und darunter erscheint **Jetzt prüfen**.

Mit **Alle**, **Arbeit** und **Privat** oben in der Seitenleiste kannst du alle Aufgaben oder nur eine Art anzeigen. Auf deinem Handy und Computer gilt dieselbe Auswahl. Wenn „Arbeit“ oder „Privat“ ausgewählt ist, führt **Alle anzeigen** zurück zur Gesamtansicht. Eine Meldung über deine Machine selbst, etwa wenn ein Teil immer wieder neu startet, gehört weder zu „Arbeit“ noch zu „Privat“ und erscheint nur unter „Alle“.

Über die Zeile oben in der Liste kannst du auch direkt zur jeweils anderen Ansicht wechseln. Wenn **Nur privat** ausgewählt ist, tippe auf **Arbeit** oder **Alle anzeigen**.

In der Zeile oben in der Liste stehen deine letzte morgendliche oder abendliche Zusammenfassung und die Anzahl der darin berücksichtigten Aufgaben, etwa **Zusammenfassung von gestern Abend** · 12 erledigt, 3 offen. Tippe darauf, um die Zusammenfassung noch einmal zu lesen. Mit **Kopieren** kannst du sie überall einfügen. Sobald du sie öffnest oder auf „×“ tippst, bleibt sie auf all deinen Geräten, bis die nächste Zusammenfassung kommt.

Wenn es keine aktuelle Zusammenfassung gibt, wird **Heute bisher** angezeigt: was heute erledigt wurde und was noch offen ist, für Arbeit und Privat oder nur für den ausgewählten Bereich.

Bei einer Aufgabe zu einem Projekt steht der Projektname unter dem Titel. Tippe darauf, um das Projekt zu öffnen. Unter **Details** kannst du es mit **Projekt** ändern oder entfernen. Mehr dazu unter [Aufgaben eines Projekts](projects.md#a-project-s-to-dos).

Unter **Details** kannst du mit **Bereich** eine Aufgabe in deinen anderen Bereich verschieben. Was sie lesen und senden darf, wechselt mit. Mit **Rückgängig** in der Meldung verschiebst du sie zurück.

Wenn eine Aufgabe den anderen Bereich braucht, um weiterzugehen, und alle Nachrichten, auf denen sie basiert, dort liegen, wird sie automatisch dorthin verschoben und fortgesetzt. Andernfalls erscheint **Nach Arbeit verschieben**. Es wird nichts verschoben, bis du darauf tippst. Eine Aufgabe, die du selbst hinzugefügt hast, ohne „Arbeit“ oder „Privat“ auszuwählen, wird automatisch dem passenden Bereich zugeordnet, sobald er feststeht. Bis dahin gehört sie weder zu „Arbeit“ noch zu „Privat“ und bleibt privat.

Eine Aufgabe kann immer die Nachrichten lesen, auf denen sie basiert. Wenn sie weitere Nachrichten aus deinem anderen Bereich braucht, fragt sie mit **Diese E-Mail für diese Aufgabe verwenden** danach. Ein Arbeits-Postfach, das du als privat gekennzeichnet hast, zählt als privat. E-Mails für ein anderes deiner Unternehmen gehören zu den Aufgaben dieses Unternehmens. Eine Aufgabe zu deinem Privatleben, etwa wenn deine Familie an deine Arbeitsadresse schreibt, ist von Anfang an privat.

Arbeit, die dich über ein privates Konto erreicht, etwa eine Kundin oder ein Kunde auf WhatsApp oder eine Bestellung in deinem privaten Postfach, gehört von Anfang an zu „Arbeit“. Eine Aufgabe, die du selbst verschoben oder einem Bereich zugeordnet hast, bleibt immer dort. „Arbeit“ oder „Privat“ legt fest, wo eine Aufgabe angezeigt wird und mit wem sie geteilt wird, aber nicht, von wo aus sie antwortet. Antworten gehen immer dorthin, wo die Unterhaltung stattfindet, auch nach dem Verschieben, außer du wählst einen anderen Weg.

Auch bei einer solchen privaten Aufgabe wird weiterhin von der Arbeitsadresse aus geantwortet, an die die E-Mail gesendet wurde. Sie wird nie in einem Work Fleet oder im Team Graph angezeigt.

Wenn mindestens zwei Aufgaben auf dich warten, kannst du mit **Durchgehen** in der Kopfzeile von „Für dich“ eine nach der anderen in Listenreihenfolge bearbeiten. Jeder Entwurf wird vollständig angezeigt, mit **Senden** oder **Ausführen**, **Änderungen anfragen**, **Zurückstellen** und **Überspringen**. Am Computer sendet die Eingabetaste den Inhalt auf dem Bildschirm, `S` stellt zurück, `→` überspringt und Esc bricht ab. In der Kopfzeile steht, wie lange es in deinem Tempo dauert, etwa „ca. 2 Min.“.

Am Ende wird gezählt, was gesendet oder geschlossen wurde und was noch vorbereitet wird.

Aufgaben, bei denen deine Antwort gefragt ist, werden dabei ausgelassen. Dafür braucht es deine Antwort, nicht nur einen Fingertipp.

## Jetzt prüfen

Deine Machine liest jede Quelle rund um die Uhr alle paar Minuten. Sie prüft neue Nachrichten, sobald 40 Nachrichten eingegangen sind oder die älteste Nachricht einer Person seit 15 Minuten wartet. Newsletter, Benachrichtigungen und Belege werden innerhalb einer Stunde bei der nächsten Prüfung berücksichtigt.

Nachts, von 00:00 bis 06:30 Uhr, werden Prüfungen pausiert. Neue Nachrichten werden trotzdem gelesen und gespeichert und um 06:30 Uhr gemeinsam geprüft, damit deine Aufgaben vor der morgendlichen Zusammenfassung bereit sind. Unter „Verbindungen“ steht bei Prüfungen: „Nachts pausiert, wird um 06:30 Uhr nachgeholt“. Wenn du nachts in der App klickst, etwas eingibst oder scrollst, im Chat schreibst oder auf eine Aufgabe tippst, laufen Prüfungen wie gewohnt weiter, bis du eine Stunde lang nichts gemacht hast. Mit **Jetzt prüfen** wird immer sofort geprüft.

Mit **Jetzt prüfen** werden alle Quellen sofort gelesen. Wenn keine Aufgaben offen sind, tippe auf die Zeile deiner Machine, um sie mit **Details** anzuzeigen. Dadurch werden die Prüfungen unter „Verbindungen“ geöffnet. Wenn Aufgaben offen sind, findest du die Zeile oben am Computer. Sie wird nur kurz angezeigt, solange eine Prüfung läuft oder fehlgeschlagen ist beziehungsweise sich verspätet. Du kannst auch im Chat danach fragen.

LinkedIn, X und Salesflare haben ihren eigenen Rhythmus.

## Letzte Prüfung

Nach einer Prüfung, bei der neue Nachrichten gelesen wurden, steht über deinen Aufgaben, was gefunden wurde und aus welchen Quellen, etwa „13 Nachrichten um 16:11 Uhr geprüft · nichts braucht dich“ oder „· 2 neue Aufgaben“. Wenn eine neue Aufgabe auf einen passenden Zeitpunkt wartet, etwa auf deine morgendliche Zusammenfassung, steht dort bis wann: „1 Aufgabe bis morgen 08:30 Uhr zurückgehalten“.

Tippe auf die Zeile, um alle E-Mail-Unterhaltungen, Chats und Benachrichtigungen mit dem Symbol der jeweiligen Quelle zu sehen. Angezeigt wird, wer geschrieben hat, der Betreff oder die ersten Wörter sowie die neue Aufgabe oder der Grund, warum nichts nötig war, etwa „Nur in cc, ein Teammitglied antwortet“ oder „Besprechung für Donnerstag bereits angesetzt“. Wenn die Prüfung nur einen vagen Grund ergeben hat, wird keiner angezeigt. Tippe auf einen Eintrag, um ihn zu lesen.

Es werden die ersten 10 Einträge angezeigt. Wenn du darunter tippst, erscheinen die übrigen. Eine Zahl hinter einem Namen, etwa (3), zeigt, wie viele neue Nachrichten der Chat enthält. Eine Handy-Benachrichtigung zu einer Nachricht, die bereits in der Liste steht, wird nur einmal angezeigt. Die Zeile bleibt 12 Stunden nach der Prüfung sichtbar.

Gezählt werden nur E-Mails an dich. Deine eigenen Antworten werden für den Kontext und Versprechen gelesen, zählen aber nicht als neue E-Mails. E-Mails deiner Machine an dich, etwa die morgendliche Zusammenfassung oder ein Hinweis auf eine Korrektur, werden nie gelesen oder aufgelistet. Nachrichten zu Abrechnung, Probezeit oder Einladungen werden wie gewohnt gelesen.

## Die Schaltflächen

Bei einer Aufgabe wird der nächste Schritt angezeigt, etwa **Ausführen** oder **Prüfen und senden**, daneben **Zurückstellen**. Mehr dazu unter [Ausführen](do-it.md) und [Zurückstellen](snooze.md).

Mit **Änderungen anfragen** kannst du sagen, was geändert werden soll: wie etwas erledigt werden soll oder, sobald ein Entwurf fertig ist, was daran geändert werden soll. **Als erledigt markieren** bedeutet, dass die Aufgabe erledigt ist. Bei einer vorbereiteten Aufgabe ohne Entwurf ist die Option direkt zu sehen, sonst oben unter **…**, auch bei Aufgaben, die deine Entscheidung brauchen. Die Aufgabe wird sofort aus der Liste entfernt. In der Nachricht kannst du das mit **Rückgängig** rückgängig machen. Wische die Nachricht weg oder ziehe sie mit der Maus aus der Liste, um sie schneller zu schließen. Die Änderung bleibt bestehen.

Wenn die Aufgabe anders erledigt werden soll, sag es im **Chat**. In der Antwort steht nur, was sich geändert hat, etwa dass etwas zurückgestellt wurde und bis wann. Wenn etwas nicht geändert werden konnte, etwa ein Fälligkeitsdatum, steht das ebenfalls dort.

Unter **…**:

- **Übergeben…**: Übergib die Aufgabe einem Teammitglied, [Claude Code oder Codex](hand-to-agent.md) oder [bitte jemanden um eine Prüfung](ask-to-review.md).
- **Wiederholen…**: Die Aufgabe [kommt regelmäßig wieder](recurring.md).
- **Nicht nötig**: Die Aufgabe wird entfernt. Du kannst optional einen Grund auswählen: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Tippe auf den Titel oder unter **Details** auf **Name**, um ihn umzubenennen. Du kannst auch im Chat danach fragen, etwa „Benenne es in … um“. Dein Titel bleibt erhalten.

Mit **Wieder öffnen** holst du eine geschlossene Aufgabe zurück. Sie kommt auch von selbst zurück, wenn etwas Neues passiert, etwa eine neue Nachricht von der anderen Person, aber nicht bei deiner eigenen Antwort. Dann wird angezeigt, wann sie zurückkam, und sie wird wie eine neue Aufgabe sortiert. Der Chat geht dort weiter, wo er aufgehört hat, auch nach Wochen.

Eine Rechnung, die du selbst noch bezahlen musst, wird unabhängig vom Land zu einer Aufgabe. Sie enthält den Betrag, das Fälligkeitsdatum und die Zahlungsangaben auf der Rechnung. Automatisch bezahlte Rechnungen, etwa per Lastschrift oder mit einer hinterlegten Karte, werden nicht aufgenommen. Wenn eine spätere E-Mail zeigt, dass sie bezahlt wurde, etwa eine Bestätigung des Absenders über den Zahlungseingang, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang zurückholen.

Eine Aufgabe, die nur bis zu einem bestimmten Zeitpunkt relevant ist, etwa eine Bestätigung vor einer Besprechung, wird danach automatisch geschlossen. Sie erscheint unter **Erledigt / verworfen** mit dem Vermerk „Nicht mehr nötig“. Mit **Rückgängig** kannst du sie einen Tag lang zurückholen.

Bevor eine Nachricht oder Übergabe für eine andere Person als bereit angezeigt wird, prüft deine Machine deine letzten Chats mit den beteiligten Personen, auch Gruppenchats, und wartet darauf, dass Slack sie gelesen hat. Wenn eine spätere Nachricht zeigt, dass die Aufgabe bereits erledigt ist, etwa weil jemand darum gebeten wurde und zugesagt hat, wird sie automatisch geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang zurückholen.

Wenn jemand nach dem Erstellen deines Entwurfs in derselben Unterhaltung geschrieben hat, hält **Senden** den Entwurf zurück: „Nicht gesendet: neue Nachricht im Thread“. Bei der Aufgabe wird diese Nachricht mit **Lesen** und **Für diese Nachricht neu machen** angezeigt. Tippe erneut auf **Senden**, um den Entwurf unverändert abzuschicken.

Wenn eine neuere Nachricht den Plan ändert, etwa weil eine Feier an einen anderen Ort verlegt oder eine Buchung storniert wurde, aktualisiert The Machine ihre Aufgaben selbst. Eine weiterhin relevante Aufgabe folgt dem neuen Plan. Wenn nichts mehr zu tun ist, wird die Aufgabe unter **Erledigt / verworfen** mit dem Vermerk „Nicht nötig“ abgelegt. Im Chat steht „Aktualisiert:“ mit einer Begründung. Mit **Rückgängig** kannst du sie einen Tag lang zurückholen.

Bei deinen ersten Aufgaben wird ein kurzer Tipp zu den wichtigsten Aktionen angezeigt: **Änderungen anfragen** und **Nicht nötig**. Außerdem wird erklärt, dass nichts gesendet wird, bevor du auf **Senden** tippst. Sobald du die Schaltfläche verwendest oder auf × tippst, wird der Tipp nicht mehr angezeigt.

Am ersten Tag begrüßt dich deine Aufgabenliste oben und nennt die Person, die schon am längsten auf deine Antwort wartet. Diese Antwort wird zuerst entworfen und ist bereit, wenn du ankommst.

Jede Aufgabe beginnt mit ihrem Titel. In der Zeile darunter steht, um wen es geht, die Organisation, wenn die Aufgabe eine betrifft (nicht einfach nur, weil jemand dort arbeitet), das Projekt, „Arbeit“ oder „Privat“ und wann die Aufgabe eingegangen ist. Tippe auf einen Namen, um die Seite der Person im Graph zu öffnen.

Bei Namen und Organisationen wird ein Foto oder Logo angezeigt, wenn es im Graph vorhanden ist, andernfalls die Initialen. Wenn ein Logo in der kleinen Größe nicht lesbar wäre, etwa weiße Schrift auf transparentem Hintergrund oder ein breiter Schriftzug, wird stattdessen ebenfalls die Initiale angezeigt.

Manchmal steht eine unaufdringliche Zeile mit nicht bekannten Informationen dort, etwa „Letzter Kontakt vor 12 Tagen per E-Mail, seitdem nichts“. Sie erscheint, wenn der letzte Austausch schon länger zurückliegt oder unbeantwortet ist. Auch nicht verbundene Kanäle wie WhatsApp werden genannt. Deine Machine sagt, was sie nicht weiß, statt zu raten.

Wenn ein nicht verbundener Kanal genannt wird, öffnet **Verbinden** daneben die Verbindung.

Der Titel beschreibt, was zu tun ist, und ändert sich nur, wenn sich die Aufgabe ändert. Eine erledigte Aufgabe behält ihren Titel. Darunter steht, wie sie abgeschlossen wurde, etwa „Erledigt: Sam hat es am Dienstag unterschrieben“.

Über dem Entwurf steht in einer unauffälligen Zeile, aus welcher Nachricht er stammt, mit dem Logo des jeweiligen Dienstes. Tippe darauf, um die Unterhaltung zu lesen. Am Logo siehst du, wohin der Entwurf geht und ob es etwa eine Slack-Antwort oder eine E-Mail ist.

Wenn der Entwurf auf einer Eingabe von jemand anderem an anderer Stelle basiert, etwa einem Vorschlag eines Teammitglieds in Slack, steht das in einer Zeile, etwa „Basiert auf Sam in #ops“. Tippe darauf, um die Nachricht zu lesen.

Ein Chat (Slack, WhatsApp, Telegram, Intercom …) wird als eine Unterhaltung in chronologischer Reihenfolge angezeigt: zuerst die Nachrichten vor der Nachricht, um die es bei der Aufgabe geht, danach die Antworten. In WhatsApp, Telegram oder Signal stehen deine Nachrichten wie in der App rechts. Die Nachricht der Aufgabe ist mit „Diese Aufgabe“ markiert und wird direkt angezeigt. Mit **Frühere Nachrichten anzeigen** werden ältere Nachrichten eingeblendet. Bei einer E-Mail wird der Rest des Threads oberhalb und unterhalb eingeklappt angezeigt.

Mit **In Gmail öffnen** öffnest du die E-Mail in dem Gmail-Konto, in dem sie eingegangen ist. Auf Android wird sie in der Gmail-App geöffnet, falls du diese installiert hast.

Unter **Details** einer E-Mail stehen nur Angaben, die nicht im Kopf der E-Mail zu sehen sind, etwa vollständige Cc-Adressen, Bcc oder eine abweichende Antwortadresse. Gibt es nichts hinzuzufügen, wird dort nichts angezeigt.

Bei einer Antwort in einem Slack-Thread wird auch angezeigt, was vor dem Start des Threads gesagt wurde. Über den Link einer Aufgabe kannst du auch die zugehörige Nachricht direkt hier öffnen. Unten steht **In Slack öffnen**.

Unter **Details** stehen der Name, das Projekt und der Bereich. Tippe auf einen Eintrag, um ihn zu ändern. Dort findest du auch deine letzte Notiz und das Ergebnis eines Programmieragenten. Über den Titel öffnest du den Chat. Eine erledigte Aufgabe bleibt kompakt. Die zugehörige Nachricht findest du unter **Details**.

Eine Aufgabe mit „Wartet auf“ verlinkt auf deine letzte Nachricht an die Person, auf deren Antwort du wartest: „E-Mail an Pat · Di“.

## Selbst eine Aufgabe erstellen

Mit **Neue Aufgabe** (am Computer unter **Suchen**, auf dem Handy über **+** oder mit `N`) kannst du eine Aufgabe zu beliebigen Dingen erstellen. Dabei wird nichts gesendet. Wenn weder **Arbeit** noch **Privat** ausgewählt ist, wird die Aufgabe dem passenden Bereich zugeordnet, je nachdem, wen und was sie betrifft. Außerdem wird die E-Mail gefunden, zu der die Aufgabe gehört, auch wenn sie schon älter ist.

- **Fällig**: Gib einen Tag oder eine Uhrzeit ein, etwa „morgen“, „nächsten Fr“, „3. Nov“, „14 Uhr“ oder „in 2 Stunden“, auch in deiner eigenen Sprache. Über das Kalendersymbol findest du Kurzauswahlen und **Datum wählen**.
- **Wiederholt sich**: Die Aufgabe kommt regelmäßig wieder. Mehr dazu unter [Wiederkehrende Aufgaben](recurring.md).
- **Person**: Verknüpfe die Personen oder Unternehmen, um die es geht, bis zu 5.
- Nachrichtensymbol: Hänge die Nachricht an, um die es geht. Das kann eine E-Mail, eine Slack-, Teams-, WhatsApp- oder Telegram-Nachricht sein oder eine andere Nachricht, auf die The Machine zugreifen kann. Suche nach Text oder Absender. Bei jedem Ergebnis stehen die Quelle, der Absender und der Zeitpunkt.
- **Dateien**: Tippe auf die Büroklammer, füge einen Screenshot ein oder ziehe Dateien auf das Formular. Auf dem Handy kannst du mit der Kamera daneben ein Foto aufnehmen. Bis zu 5 Dateien, wie im Chat (siehe [Dateien hinzufügen](card-chat.md#add-files)). Mit × entfernst du eine Datei wieder.

Die Dateien bleiben bei der Aufgabe. Deine Machine liest sie, während sie daran arbeitet. Dateien allein reichen aus: Sie erstellt die Aufgabe anhand einer PDF- oder Textdatei. Ein Foto wird als kleines Bild angezeigt. Tippe darauf, um es in voller Größe zu sehen.
