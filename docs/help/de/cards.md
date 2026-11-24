---
title: Aufgaben
area: cards
summary: Eine Aufgabe für jedes Anliegen, bei dem du gefragt bist. Bereit zur Bestätigung. Hier erfährst du, was die einzelnen Teile einer Aufgabe bedeuten.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: e1656daff6fc566a
---
Deine Machine liest alles Neue und erstellt nur dann eine Aufgabe, wenn etwas dich braucht. Eine Aufgabe pro Anliegen, auch wenn es sich über mehrere Nachrichten erstreckt.

## Wo Aufgaben zu finden sind

Auf der Seite **Aufgaben** sind sie gruppiert:

- **Gerade erledigt**: Ganz oben siehst du einen letzten Schritt, den du bestätigt hast, etwa ein Formular oder ein Problem, das während deiner Abwesenheit erledigt wurde. Er bleibt höchstens einen Tag dort, bis du auf **Verstanden** tippst. Auch auf deinem Handy erscheint ein Hinweis.
- **Für dich**: Alles, worauf du reagieren musst, nach Dringlichkeit sortiert. Bei jeder Aufgabe steht **Vorbereitet** (ein Entwurf oder Ergebnis ist bereit, und mit **Ausführen** oder **Senden** wird es umgesetzt), **Braucht dich** (zuerst ist deine Entscheidung oder Antwort nötig; wenn die Arbeit ohne etwas, das nur du hast, nicht weitergehen oder verwendet werden kann, etwa einen Preis, eine Information oder eine Entscheidung, steht unter dem Titel, worum es geht), **Wird vorbereitet…** (deine Machine arbeitet daran) oder **Zum Lesen** (eine Zusammenfassung oder ein Briefing, bei dem nichts entschieden werden muss).
- **Älter**: Eingeklappte Aufgaben, zu denen es seit einer Woche nichts Neues gab (weiter unten).
- **Wartet auf andere**: Eingeklappte Aufgaben, bei denen der nächste Schritt bei jemand anderem liegt (weiter unten).
- **Kommt später zurück**: Zurückgestellte Aufgaben und Aufgaben ohne Antwort auf **Noch nötig?** (weiter unten).
- **Versprechen**: Was du versprochen hast und was andere dir versprochen haben. Mehr dazu unter [Versprechen](promises.md).
- **Erledigt / verworfen**: Alle abgeschlossenen Aufgaben, neueste zuerst, mit dem Zeitpunkt des Abschlusses, zum Beispiel „Vor 5 Minuten erledigt“. Aufgaben, die bereits erledigt zu sein scheinen, sind mit **Sieht erledigt aus** gekennzeichnet.

Nach dem Senden erscheint ein kurzer Hinweis darauf, wohin die Aufgabe verschoben wurde, zum Beispiel „Gesendet. Nach Erledigt verschoben.“ oder „Gesendet. Bis Mo. nach Später verschoben.“ Eine Antwort, die nur verspricht, die Arbeit zu erledigen, etwa „Ich schicke es bis Dienstag“, lässt die Aufgabe offen: „Gesendet. Bleibt offen.“ Mit **Öffnen** gelangst du zur Aufgabe. Über die Suche findest du Aufgaben nach Titel oder Empfänger, auch unter Später und Erledigt.

Unter **Für dich** stehen überfällige Aufgaben und Aufgaben mit Fälligkeit bis morgen zuerst, dann Fragen aus deiner Fleet, Nachfassnachrichten eines Boards und danach der Rest. Innerhalb jeder Gruppe stehen die neuesten zuerst. Eine Aufgabe behält ihren Platz, während deine Machine sie vorbereitet und wenn sie erledigt ist. Nur ihre Markierung ändert sich. In den anderen offenen Gruppen stehen überfällige Aufgaben und Aufgaben mit Fälligkeit bis morgen zuerst, danach die neuesten. Die Seitenleiste behält dieselbe Reihenfolge bei.

**Sieht erledigt aus** bedeutet, dass deine Machine erkennt, dass eine Aufgabe erledigt ist, etwa „PR #3451 zusammengeführt“, sie aber noch nicht geschlossen wurde. Mit **Wieder öffnen** kommt sie zurück auf deine Liste, und deine Machine lernt daraus. Diese Aufgaben gelten nie als verspätet. Wird die Markierung in einer Nachricht angezeigt, verschwindet sie nach einem Tag von selbst. Bis dahin kannst du **Rückgängig** wählen. Andernfalls wartet die Aufgabe auf **Als erledigt markieren**. Eine Aufgabe, die du selbst schon erledigt hast, zum Beispiel mit einer Antwort in Gmail oder Slack, wird ebenfalls automatisch geschlossen.

Wenn eine Nachricht von einer Adresse kommt, die nur wie die einer bekannten Person aussieht, zum Beispiel sam@acme-corp.example statt sam@acmecorp.example, steht bei der Aufgabe klar: „Das ist nicht Sam Lee.“ Die Person wird mit ihrer tatsächlichen Adresse angezeigt, nie mit dem Namen, den sie angegeben hat. Deine Machine prüft solche Nachrichten bei der Person, deren Adresse du bereits gespeichert hast, nie bei der Person, die geschrieben hat.

Bei einer Aufgabe, die noch auf jemand anderen wartet, etwa auf eine Prüfung oder Antwort, steht **Wartet auf:** mit dem nächsten Schritt. Sie bleibt eingeklappt unter **Wartet auf andere**, oberhalb von Kommt später zurück, bis eine neue Nachricht sie wieder hervorholt. Dasselbe gilt, wenn du eine Rückfrage gestellt hast: Die Aufgabe kommt am Morgen vor ihrem Fälligkeitstermin zurück, am Fälligkeitstag, wenn dieser noch heute ist, oder am nächsten Morgen, wenn der Termin bereits verstrichen ist. Außerdem steht dabei, auf wen sie noch wartet.

Geht es bei einer Aufgabe um ein Ergebnis, das jemand anders liefern muss, etwa einen unterschriebenen Vertrag, wird es unter **Details** bei **Fertig, wenn** angezeigt. Wenn du deinen Teil abschickst, ist die Aufgabe noch nicht abgeschlossen. Sie wartet unter **Wartet auf andere**, bis eine Nachricht das Ergebnis bestätigt. Dann wird sie automatisch geschlossen. Bis dahin kannst du **Rückgängig** wählen. Wenn bis zum Zeitpunkt, an dem du nachhaken solltest, nichts eintrifft, kommt die Aufgabe mit **Schreib eine kurze Erinnerung** in ihrem Chat zurück. Schreib im Chat, was als erledigt gelten soll, um das zu ändern.

Eine Aufgabe, zu der es eine Woche lang nichts Neues gab, wird von Für dich nach **Älter** verschoben. So stehen nach ein paar Tagen Abwesenheit die neuen Aufgaben zuerst. Als neu gilt eine Nachricht zur Aufgabe oder eine Aktion von dir, etwa eine Chatnachricht, eine Bearbeitung oder ein Zurückstellen. Nur die Aufgabe anzusehen zählt nicht.

Dringende Aufgaben, bald fällige Aufgaben und Aufgaben mit einem bevorstehenden Versand bleiben unter Für dich. Mit **Alle verwerfen** markierst du nach einmaliger Bestätigung alle Aufgaben unter Älter als nicht nötig. Mit **Nicht nötig** kannst du sie einzeln verwerfen. In beiden Fällen kannst du **Rückgängig** wählen. Gibt es bei einer Aufgabe etwas Neues, kommt sie zurück zu Für dich.

Bei einer Aufgabe, die eine Woche lang niemand angefasst hat, wird einmal gefragt: **Noch nötig?** Mit **Nicht nötig** wird sie geschlossen. Du kannst **Rückgängig** wählen. Mit **Behalten** bleibt sie bestehen, und die Frage wird nicht erneut gestellt. Wenn du eine weitere Woche nicht antwortest, wird sie unter Kommt später zurück eingeklappt. Sie wird dann weder auf dem App-Symbol noch in der morgendlichen Zusammenfassung mitgezählt. Wenn du sie öffnest, eine Chatnachricht schreibst, sie bearbeitest, zurückstellst oder eine neue Nachricht eintrifft, kommt sie zurück.

Ein Projekt, bei dem es ruhig geworden ist und keine Aufgaben mehr offen sind, kann einmal pro Woche eine Aufgabe mit einem konkreten nächsten Schritt bekommen, höchstens drei pro Woche. Mehr dazu unter [Projekte](projects.md).

Wenn nichts deine Aufmerksamkeit braucht, macht deine Machine ein Nickerchen und zeigt eine leere Liste. Während einer Prüfung wird sie wach und zeigt das an. Wenn eine Prüfung fehlgeschlagen ist oder sich verzögert, steht es in der Zeile. Darunter findest du **Jetzt prüfen**.

Mit **Alle**, **Arbeit** und **Privat** oben in der Seitenleiste kannst du alle Aufgaben oder nur eine Art anzeigen. Auf Handy und Computer gilt dieselbe Auswahl. Wenn Arbeit oder Privat ausgewählt ist, führt **Alle anzeigen** zurück zur Gesamtansicht. Ein Hinweis zu deiner Machine selbst, etwa dass ein Teil immer wieder neu startet, gehört weder zu Arbeit noch zu Privat und erscheint nur unter Alle.

Über die Zeile oben in der Liste kannst du außerdem direkt zur anderen Ansicht wechseln: Unter **Nur privat** tippst du auf **Arbeit** oder **Alle anzeigen**.

Die Zeile oben in der Liste nennt deine letzte morgendliche oder abendliche Zusammenfassung und zeigt, was darin gezählt wurde, etwa **Zusammenfassung von gestern Abend** · 12 erledigt, 3 offen. Tippe darauf, um die Zusammenfassung erneut zu lesen. Mit **Kopieren** kannst du sie an beliebiger Stelle einfügen. Sobald du sie öffnest oder auf ihr **×** tippst, wird sie auf all deinen Geräten angezeigt, bis die nächste Zusammenfassung kommt.

Wenn es keine aktuelle Zusammenfassung gibt, steht dort **Heute bisher**: Was heute erledigt wurde und was noch offen ist, für Arbeit und Privat oder nur für den ausgewählten Bereich.

Bei einer Aufgabe zu einem Projekt steht der Projektname unter dem Titel. Tippe darauf, um das Projekt zu öffnen. Unter **Details** kannst du es bei **Projekt** ändern oder entfernen. Mehr dazu unter [Aufgaben eines Projekts](projects.md#a-project-s-to-dos).

Unter **Details** kannst du bei **Bereich** eine Aufgabe in deinen anderen Bereich verschieben. Der Zugriff auf Nachrichten zum Lesen und Senden wird dabei mitverschoben. Mit **Rückgängig** im Hinweis verschiebst du sie zurück.

Wenn eine Aufgabe deinen anderen Bereich braucht, um weiterzugehen, und alle Nachrichten, auf denen sie beruht, dort liegen, wird sie automatisch dorthin verschoben und fortgesetzt. Andernfalls wird **Nach Arbeit verschieben** angezeigt. Erst wenn du darauf tippst, wird die Aufgabe verschoben. Eine Aufgabe, die du hinzugefügt hast, ohne Arbeit oder Privat auszuwählen, wird automatisch dem passenden Bereich zugeordnet, sobald klar ist, wohin sie gehört. Bis dahin gehört sie weder zu Arbeit noch zu Privat und bleibt privat.

Eine Aufgabe kann immer die Nachrichten lesen, aus denen sie entstanden ist. Wenn sie weitere Nachrichten aus deinem anderen Bereich braucht, fragt sie mit **Diese E-Mail für diese Aufgabe verwenden** danach. Ein Arbeits-Postfach, das du als Privat gekennzeichnet hast, zählt als Privat. E-Mails für eine andere Firma von dir gehören zu den Aufgaben dieser Firma. Eine Aufgabe aus deinem Privatleben, etwa wenn deine Familie an deine Arbeitsadresse schreibt, ist von Anfang an privat.

Arbeit, die dich über ein privates Konto erreicht, etwa eine Kundin über WhatsApp, eine Bestellung in deinem privaten Postfach oder ein [Versprechen](promises.md) zur Arbeit, gehört von Anfang an zu Arbeit.

Eine Aufgabe, die du selbst verschoben oder zugeordnet hast, bleibt immer dort, wo du sie abgelegt hast. Arbeit oder Privat bestimmt, wo eine Aufgabe angezeigt und mit wem sie geteilt wird, nicht, wohin sie antwortet. Eine Antwort geht immer dorthin, wo die Unterhaltung stattfindet, auch nach dem Verschieben, sofern du nichts anderes auswählst.

Auch eine solche private Aufgabe antwortet weiterhin von der Arbeitsadresse aus, an die die E-Mail geschickt wurde. Sie wird nie in einer Work Fleet oder im Team Graph angezeigt.

Wenn mindestens zwei Aufgaben auf dich warten, kannst du mit **Durchgehen** in der Kopfzeile von Für dich eine nach der anderen bearbeiten, in der Reihenfolge der Liste. Jeder Entwurf wird vollständig angezeigt, dazu **Senden** oder **Ausführen**, **Änderungen anfragen**, **Zurückstellen** und **Überspringen**. Am Computer sendet die Eingabetaste, `S` stellt zurück, `→` überspringt und Esc beendet den Ablauf. In der Kopfzeile steht, wie lange es in deinem Tempo ungefähr dauert, etwa „ca. 2 Min.“

Am Ende wird gezählt, was gesendet oder geschlossen wurde und was noch vorbereitet wird.

Aufgaben mit einer Frage an dich sind davon ausgenommen: Sie brauchen deine Antwort, keinen Tipp.

## Jetzt prüfen

Deine Machine liest jede Quelle alle paar Minuten, Tag und Nacht. Sie prüft neue Nachrichten, sobald 40 davon eingegangen sind oder die älteste Nachricht einer Person seit 15 Minuten wartet. Newsletter, Benachrichtigungen und Belege werden innerhalb einer Stunde bei der nächsten Prüfung berücksichtigt.

Nachts, von 00:00 bis 06:30 Uhr, pausieren die Prüfungen. Neue Nachrichten werden trotzdem gelesen und gespeichert und um 06:30 Uhr gemeinsam geprüft. So sind deine Aufgaben vor der morgendlichen Zusammenfassung bereit. Unter Verbindungen bei den Prüfungen steht dann „Nachts pausiert, wird um 06:30 Uhr nachgeholt“. Wenn du nachts in der App klickst, etwas eingibst oder scrollst, im Chat schreibst oder auf eine Aufgabe tippst, laufen die Prüfungen wie gewohnt weiter, bis du eine Stunde lang inaktiv bist. Mit **Jetzt prüfen** wird immer sofort geprüft.

Mit **Jetzt prüfen** werden alle Quellen sofort gelesen. Wenn keine Aufgabe offen ist, tippe auf die Zeile deiner Machine, um sie mit **Details** zu sehen. Dadurch werden die Prüfungen unter Verbindungen geöffnet. Sind Aufgaben offen, findest du die Zeile oben auf dem Computer. Eine kurze Meldung erscheint dort nur während einer Prüfung oder wenn sie fehlgeschlagen ist oder sich verzögert. Du kannst auch im Chat danach fragen.

LinkedIn, X und Salesflare prüfen in ihrem eigenen Tempo.

## Letzte Prüfung

Nach einer Prüfung, bei der neue Nachrichten gelesen wurden, steht über deinen Aufgaben, was dabei gefunden wurde. Die Zeile umfasst alle gelesenen Quellen, etwa „13 Nachrichten um 16:11 geprüft · keine neue Aufgabe“ oder „· 2 neue Aufgaben“. Sie bezieht sich nur auf diese Prüfung. Bereits gelistete Aufgaben bleiben unverändert. Wenn eine neue Aufgabe auf einen günstigeren Zeitpunkt wartet, etwa auf deine morgendliche Zusammenfassung, steht dabei, bis wann: „1 Aufgabe bis morgen 08:30 zurückgehalten“.

Tippe auf die Zeile, um alle E-Mail-Threads, Chats und Benachrichtigungen mit dem Symbol ihrer Quelle zu sehen. Angezeigt werden, wer geschrieben hat, der Betreff oder die ersten Wörter sowie die neue Aufgabe oder der Grund, warum nichts nötig war, etwa „Nur in Cc, ein Teammitglied antwortet“ oder „Besprechung bereits für Donnerstag angesetzt“. Wenn die Prüfung nur einen unklaren Grund ergeben hat, wird kein Grund angezeigt. Tippe auf einen Eintrag, um ihn mit dem zugehörigen Gespräch zu lesen.

Die ersten 10 Einträge werden angezeigt. Tippe darunter, um den Rest zu sehen. Eine Zahl hinter einem Namen, etwa (3), gibt an, wie viele neue Nachrichten der Chat enthält. Eine Handybenachrichtigung zu einer Nachricht, die bereits in der Liste steht, wird nur einmal angezeigt. Die Zeile bleibt 12 Stunden nach der Prüfung sichtbar.

Gezählt werden nur E-Mails an dich. Deine eigenen Antworten werden berücksichtigt, um den Kontext und Versprechen zu verstehen, zählen aber nicht als neue E-Mails. Die eigenen E-Mails deiner Machine an dich, etwa deine morgendliche Zusammenfassung oder ein Hinweis zu einer Fehlerbehebung, werden nie gelesen oder aufgelistet. E-Mails zu Abrechnung, Testphase oder Einladungen werden wie gewohnt gelesen.

## Die Schaltflächen

Eine Aufgabe zeigt ihren nächsten Schritt, etwa **Ausführen** oder **Prüfen und senden**, daneben **Zurückstellen**. Mehr dazu unter [Ausführen](do-it.md) und [Zurückstellen](snooze.md).

Unter **Änderungen anfragen** steht, was geändert werden soll: die Vorgehensweise oder, sobald ein Entwurf bereit ist, der Entwurf selbst. **Als erledigt markieren** bedeutet, dass die Aufgabe erledigt ist. Bei einer vorbereiteten Aufgabe ohne Entwurf oder einer Aufgabe mit einer Frage an dich ist die Option direkt zu sehen, sonst oben unter **…**. Die Aufgabe wird sofort aus der Liste entfernt. In der Nachricht kannst du **Rückgängig** wählen. Wische die Nachricht weg oder zieh sie mit der Maus aus der Liste, um sie schneller zu schließen. Die Änderung bleibt bestehen.

Wenn du die Aufgabe anders erledigen lassen möchtest, sag es im **Chat**. In der Antwort steht nur, was geändert wurde, etwa eine Zurückstellung und bis wann. Wenn etwas nicht geändert werden konnte, zum Beispiel das Fälligkeitsdatum, wird das ebenfalls gesagt.

Unter **…**:

- **Übergeben…**: Gib die Aufgabe an ein Teammitglied, [Claude Code oder Codex](hand-to-agent.md) weiter oder [bitte jemanden um eine Prüfung](ask-to-review.md).
- **Wiederholen…**: Die Aufgabe [kommt regelmäßig wieder](recurring.md).
- **Nicht nötig**: Die Aufgabe wird entfernt. Optional kannst du einen Grund auswählen: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Tippe auf den Titel oder unter **Details** auf **Name**, um die Aufgabe umzubenennen. Du kannst auch im Chat darum bitten, etwa „Benenne sie in … um“. Dein Titel bleibt erhalten.

Mit **Wieder öffnen** holst du eine geschlossene Aufgabe zurück. Sie kommt auch von selbst zurück, wenn etwas Neues passiert, etwa eine neue Nachricht von der anderen Person, aber nicht bei deiner eigenen Antwort. Dann wird angezeigt, wann sie zurückgekommen ist, und sie wird wie eine neue Aufgabe sortiert. Der Chat wird an derselben Stelle fortgesetzt, auch nach mehreren Wochen.

Eine Rechnung, die du selbst noch bezahlen musst, wird unabhängig vom Land zu einer Aufgabe. Sie enthält den Betrag, das Fälligkeitsdatum und die Zahlungsangaben aus der Rechnung. Automatisch bezahlte Rechnungen, etwa per Lastschrift oder gespeicherter Karte, werden nicht zu Aufgaben. Wenn eine spätere E-Mail bestätigt, dass sie bezahlt wurde, zum Beispiel eine Zahlungsbestätigung des Absenders, wird die Aufgabe automatisch geschlossen. Einen Tag lang kannst du **Rückgängig** wählen.

Eine Aufgabe, die nur bis zu einem bestimmten Zeitpunkt wichtig ist, etwa eine Bestätigung vor einer Besprechung, wird danach automatisch geschlossen. Sie wird mit dem Vermerk „Nicht mehr nötig“ nach **Erledigt / verworfen** verschoben. Einen Tag lang kannst du sie mit **Rückgängig** zurückholen.

Bevor eine Nachricht oder Übergabe für jemand anderen als bereit angezeigt wird, prüft deine Machine deine letzten Chats mit den beteiligten Personen, auch Gruppenchats, und wartet darauf, dass Slack sie einliest. Wenn eine spätere Nachricht zeigt, dass die Aufgabe bereits erledigt ist, etwa weil jemand gefragt wurde und zugesagt hat, wird sie automatisch geschlossen. Einen Tag lang kannst du **Rückgängig** wählen.

Wenn jemand anderes nach dem Erstellen deines Entwurfs im selben Gespräch geschrieben hat, hält **Senden** den Versand zurück: „Nicht gesendet: neue Nachricht im Thread“. Bei der Aufgabe wird diese Nachricht mit **Lesen** und **Für diese Nachricht neu machen** angezeigt. Tippe erneut auf **Senden**, um den Entwurf unverändert abzuschicken.

Wenn eine neuere Nachricht den Plan ändert, etwa wenn eine Feier an einen anderen Ort verlegt oder eine Buchung storniert wird, aktualisiert The Machine ihre Aufgaben selbst. Eine weiterhin relevante Aufgabe folgt dem neuen Plan. Wenn nichts mehr zu tun ist, wird sie mit „Nicht nötig“ nach **Erledigt / verworfen** verschoben. Im Chat steht „Aktualisiert:“ mit dem Grund. Einen Tag lang kannst du sie mit **Rückgängig** zurückholen.

Bei deinen ersten Aufgaben erscheint ein kurzer Tipp zu den wichtigsten Aktionen: **Änderungen anfragen** und **Nicht nötig**. Außerdem wird erklärt, dass nichts versendet wird, bevor du auf **Senden** tippst. Der Tipp verschwindet endgültig, sobald du die Schaltfläche verwendest oder auf × tippst.

An deinem ersten Tag begrüßt dich oben auf der Seite Aufgaben eine Nachricht. Sie nennt die Person, die am längsten auf deine Antwort wartet. Der Entwurf für diese Antwort wird zuerst erstellt, damit er bereit ist, wenn du kommst.

Jede Aufgabe beginnt mit ihrem Titel. Darunter steht, um wen es geht, gegebenenfalls die Organisation (nicht allein deshalb, weil jemand dort arbeitet), das Projekt, Arbeit oder Privat und wann die Aufgabe eingegangen ist. Tippe auf einen Namen, um die entsprechende Seite im Graph zu öffnen.

Wenn im Graph ein Foto oder Logo hinterlegt ist, werden Name und Organisation damit angezeigt, andernfalls mit den Initialen. Ein Logo, das in dieser Größe nicht gut lesbar wäre, etwa weiße Schrift auf transparentem Hintergrund oder ein breites Wortzeichen, wird ebenfalls durch Initialen ersetzt.

Manchmal zeigt eine unauffällige Zeile, was nicht bekannt ist, etwa „Letzter Kontakt vor 12 Tagen per E-Mail, seitdem nichts.“ Sie erscheint, wenn der letzte Kontakt schon länger zurückliegt oder unbeantwortet ist, und nennt nicht verbundene Kanäle wie WhatsApp. Deine Machine sagt, was sie nicht weiß, statt zu raten.

Wenn ein nicht verbundener Kanal genannt wird, öffnet **Verbinden** daneben die entsprechende Verbindung.

Der Titel beschreibt, was zu tun ist, und ändert sich nur, wenn sich die Aufgabe ändert. Eine erledigte Aufgabe behält ihren Titel. Darunter steht, wie sie abgeschlossen wurde, etwa „Erledigt: Sam hat es am Dienstag unterschrieben“.

Über dem Entwurf steht in einer blassen Zeile die Nachricht, aus der er entstanden ist, mit dem Logo des jeweiligen Dienstes. Tippe darauf, um den Thread zu lesen. Der Entwurf zeigt das Logo des Zielorts. So siehst du sofort, ob es sich um eine Slack-Antwort oder eine E-Mail handelt.

Wenn der Entwurf auf einer Eingabe an anderer Stelle beruht, etwa auf einem Vorschlag eines Teammitglieds in Slack, steht das in einer Zeile, etwa „Basierend auf Sam in #ops“. Tippe darauf, um die Nachricht zu lesen. Sie wird angezeigt, bis ein aktualisierter Entwurf sie ersetzt.

Ein Chat (Slack, WhatsApp, Telegram, Intercom …) wird als ein Gespräch angezeigt, vom ältesten zum neuesten Eintrag: mit den Nachrichten vor der Nachricht, auf die sich die Aufgabe bezieht, und den Antworten danach. In WhatsApp, Telegram oder Signal stehen deine Nachrichten wie in der App rechts. Die Nachricht zur Aufgabe ist mit „Diese Aufgabe“ markiert und geöffnet. Mit **Frühere Nachrichten anzeigen** werden ältere Nachrichten eingeblendet. Bei E-Mails ist der übrige Thread darüber und darunter eingeklappt.

Eine Nachricht wird bei der Suche, im Graph, in den Antworten von Ask und bei der letzten Prüfung auf dieselbe Weise geöffnet und mit „Diese Nachricht“ (oder „Neue Nachrichten“) markiert.

Mit **In Gmail öffnen** wird die E-Mail in dem Gmail-Konto geöffnet, in dem sie eingegangen ist. Auf Android wird sie in der Gmail-App geöffnet, wenn du sie installiert hast.

Unter **Details** einer E-Mail werden nur Angaben angezeigt, die nicht schon im Kopf der E-Mail stehen, etwa vollständige Cc-Adressen, Bcc oder eine abweichende Antwortadresse. Gibt es nichts hinzuzufügen, bleibt der Abschnitt leer.

Bei einer Antwort in einem Slack-Thread wird auch angezeigt, was vor Beginn des Threads geschrieben wurde. Über den Link einer Aufgabe zur zugehörigen Nachricht lässt sich diese ebenfalls hier öffnen. Unten findest du **In Slack öffnen**.

Unter **Details** stehen Name, Projekt und Bereich (tippe auf einen Eintrag, um ihn zu ändern), deine letzte Notiz und das Ergebnis eines Coding-Agenten. Über den Titel wird der Chat geöffnet. Eine erledigte Aufgabe bleibt kompakt. Die zugehörige Nachricht findest du unter **Details**.

Bei einer Aufgabe mit dem Hinweis „Wartet auf“ führt ein Link zu deiner letzten Nachricht an die Person, auf deren Antwort du wartest: „E-Mail an Pat · Di“.

## Selbst eine Aufgabe erstellen

Mit **Neue Aufgabe** (am Computer unter **Suchen**, auf dem Handy über **+** oder mit `N`) erstellst du eine Aufgabe für alles Mögliche. Beim Erstellen wird nichts gesendet. Wenn du weder **Arbeit** noch **Privat** auswählst, wird die Aufgabe anhand der beteiligten Personen und des Themas dem passenden Bereich zugeordnet. Außerdem findet sie die E-Mail, auf die sie sich bezieht, auch wenn sie älter ist.

- **Fällig**: Gib einen Tag oder eine Uhrzeit ein, zum Beispiel „morgen“, „nächsten Fr“, „3. Nov.“, „14 Uhr“ oder „in 2 Stunden“. Das geht auch in deiner Sprache. Das Kalendersymbol bietet Schnellauswahl und **Datum wählen**.
- **Wiederholt sich**: Die Aufgabe kommt regelmäßig wieder. Mehr dazu unter [Wiederkehrende Aufgaben](recurring.md).
- **Person**: Verknüpfe bis zu fünf Personen oder Unternehmen, um die es geht.
- Nachrichtensymbol: Hänge die Nachricht an, um die es geht: eine E-Mail, Slack-, Teams-, WhatsApp-, Telegram- oder eine andere Nachricht, die The Machine kennt. Suche nach Text oder Absender. Bei jedem Treffer siehst du, woher er stammt, wer ihn gesendet hat und wann.
- **Dateien**: Tippe auf die Büroklammer, füge einen Screenshot ein oder zieh Dateien auf das Formular. Auf dem Handy kannst du mit der Kamera daneben ein Foto aufnehmen. Bis zu fünf Dateien, wie im Chat (siehe [Dateien hinzufügen](card-chat.md#add-files)). Mit × entfernst du eine Datei.

Die Dateien bleiben an der Aufgabe hängen, und deine Machine liest sie, während sie daran arbeitet. Dateien allein genügen: Sie erstellt die Aufgabe aus einer PDF- oder Textdatei. Ein Foto wird als kleines Bild angezeigt. Tippe darauf, um es in voller Größe zu sehen.
