---
title: Aufgaben
area: cards
summary: Eine Aufgabe pro Sache, die dich braucht, bereit für dein Ja. Was die einzelnen Teile einer Aufgabe bedeuten.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: cd59c14a7a27491d
---
Deine Machine liest alles Neue und erstellt nur dann eine Aufgabe, wenn etwas dich braucht. Eine Aufgabe pro Thema, egal über wie viele Nachrichten es sich erstreckt.

## Wo Aufgaben stehen

Auf der Seite **Aufgaben** sind sie gruppiert:

- **Für dich**: Alles, was auf dich wartet, zuerst das Dringendste. Bei jeder Aufgabe steht **Vorbereitet** (die Arbeit ist erledigt, und **Ausführen** oder **Senden** führt sie aus), **Braucht dich** (sie braucht zuerst deine Entscheidung oder Antwort) oder **Wird vorbereitet…** (deine Machine arbeitet daran).
- **Gerade erledigt**: Ein letzter Schritt, den du bestätigt hast, etwa ein Formular oder ein Vorgang, wurde ausgeführt, während du weg warst. Er bleibt dort, bis du auf **Verstanden** tippst, höchstens einen Tag lang. Dein Handy wird ebenfalls darüber benachrichtigt.
- **Kommt später zurück**: Zurückgestellte Aufgaben und Aufgaben, auf die du nicht mit **Noch nötig?** geantwortet hast (siehe unten).
- **Versprechen**: Was du versprochen hast und was andere dir versprochen haben. Mehr dazu unter [Versprechen](promises.md).
- **Erledigt / verworfen**: Alle abgeschlossenen Aufgaben, die neuesten zuerst, mit dem Zeitpunkt ihres Abschlusses, zum Beispiel „Vor 5 Minuten erledigt“. Aufgaben, die offenbar schon erledigt sind, sind als **Scheinbar erledigt** markiert.

Nach dem Senden erscheint eine kurze Notiz dazu, wohin die Aufgabe verschoben wurde, etwa „Gesendet. Nach Erledigt verschoben.“ oder „Gesendet. Bis Mo. nach Später verschoben.“ Über **Öffnen** gelangst du zur Aufgabe. Über die Suche findest du Aufgaben nach Titel oder Empfänger, auch unter Später und Erledigt.

Unter **Für dich** stehen zuerst überfällige oder bis morgen fällige Aufgaben, dann Fragen aus deiner Fleet und danach der Rest. Innerhalb jeder Gruppe stehen die neuesten zuerst. Eine Aufgabe behält ihren Platz, während deine Machine sie vorbereitet und auch nach ihrer Erledigung. Nur ihre Markierung ändert sich. In den anderen offenen Gruppen stehen überfällige oder bis morgen fällige Aufgaben zuerst, danach die neuesten. Die Seitenleiste behält dieselbe Reihenfolge.

**Scheinbar erledigt** bedeutet, dass deine Machine sieht, dass die Aufgabe erledigt ist, etwa „PR #3451 zusammengeführt“, sie aber noch nicht geschlossen wurde. **Wieder öffnen** setzt sie wieder auf deine Liste, und deine Machine lernt daraus. Diese Aufgaben werden nie als verspätet angezeigt. Nach einem Tag wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Eine Aufgabe, die du selbst bereits erledigt hast, etwa mit einer Antwort in Gmail oder Slack, wird ebenfalls automatisch geschlossen.

Wenn eine Nachricht von einer Adresse kommt, die nur wie die einer bekannten Person aussieht, etwa sam@acme-corp.example statt sam@acmecorp.example, steht das deutlich in der Aufgabe: „Das ist nicht Sam Lee.“ Die Person wird mit ihrer eigenen Adresse angezeigt, nie mit dem Namen, den sie verwendet hat. Deine Machine prüft solche Nachrichten bei der Person unter der Adresse, die du bereits hast, nie bei der Person, die geschrieben hat.

Eine Aufgabe, die noch auf jemand anderen wartet, etwa auf eine Prüfung oder Antwort, zeigt den Schritt unter **Wartet auf:** an. Sie liegt eingeklappt unter **Wartet auf andere**, oberhalb von Kommt später zurück, bis eine neue Nachricht sie wieder hervorholt. Dasselbe gilt, nachdem du eine Rückfrage gestellt hast: Die Aufgabe kommt am Morgen vor der Frist zurück, bei einer späteren Frist noch am selben Tag zum Fristzeitpunkt oder am nächsten Morgen, wenn die Frist bereits verstrichen ist. Sie zeigt dann an, auf wen sie noch wartet.

Geht es bei einer Aufgabe um ein Ergebnis, das jemand anderes liefern muss, etwa einen unterschriebenen Vertrag, wird es unter **Details** bei **Fertig, wenn** angezeigt. Wenn du deinen Teil sendest, wird die Aufgabe nicht geschlossen. Sie wartet unter **Wartet auf andere**, bis eine Nachricht das Ergebnis bestätigt. Dann wird sie automatisch geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Wenn bis zum Zeitpunkt, an dem du nachhaken solltest, nichts eingeht, kommt sie mit **Schreib eine kurze Erinnerung** in ihrem Chat zurück. Sag im Chat, was als erledigt gilt, um das zu ändern.

Wenn sich eine Woche lang niemand um eine Aufgabe gekümmert hat, fragt sie einmal: **Noch nötig?** Mit **Nicht nötig** wird sie geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. **Behalten** behält sie bei. Danach fragt sie nie wieder nach. Wenn eine weitere Woche lang keine Antwort kommt, wird sie unter Kommt später zurück eingeklappt. Die Zahl auf dem App-Symbol und in der morgendlichen Zusammenfassung zählt sie dann nicht mehr mit. Wenn du sie öffnest, eine Chatnachricht schreibst, sie bearbeitest oder zurückstellst oder eine neue Nachricht eingeht, kommt sie wieder zurück.

Ein Projekt, bei dem seit einer Weile nichts mehr passiert und keine Aufgaben offen sind, kann einmal pro Woche eine Aufgabe mit einem konkreten nächsten Schritt erhalten, höchstens drei pro Woche. Mehr dazu unter [Projekte](projects.md).

Wenn dich nichts braucht, macht deine Machine ein Nickerchen und zeigt eine leere Liste. Während einer Prüfung wacht sie auf und zeigt an, dass sie prüft. Wenn eine Prüfung fehlgeschlagen ist oder sich verzögert, steht das in ihrer Zeile. Darunter findest du **Jetzt prüfen**.

Mit **Alle**, **Arbeit** und **Privat** oben in der Seitenleiste kannst du alle Aufgaben oder nur eine Art anzeigen. Auf Handy und Computer wird dieselbe Auswahl verwendet. Wenn Arbeit oder Privat ausgewählt ist, führt **Alle anzeigen** zurück zur Gesamtansicht. Eine Benachrichtigung über deine Machine selbst, etwa wenn ein Teil immer wieder neu startet, gehört weder zu Arbeit noch zu Privat und wird nur unter Alle angezeigt.

Über die Zeile oben in der Liste kannst du direkt zur jeweils anderen Ansicht wechseln: **Nur privat · Arbeit · Alle anzeigen**.

Die Zeile oben in der Liste nennt deine letzte morgendliche oder abendliche Zusammenfassung und zeigt, was darin gezählt wurde, etwa **Zusammenfassung von gestern Abend** · 12 erledigt, 3 offen. Tippe darauf, um die Zusammenfassung noch einmal zu lesen. Mit **Kopieren** kannst du sie irgendwo einfügen. Sobald du sie öffnest oder auf ihr **×** tippst, bleibt sie auf all deinen Geräten verfügbar, bis die nächste Zusammenfassung kommt.

Wenn es keine aktuelle Zusammenfassung gibt, wird **Heute bisher** angezeigt: was heute erledigt wurde und was noch offen ist, für Arbeit und Privat oder nur für die ausgewählte Ansicht.

Bei einer Aufgabe zu einem Projekt wird der Projektname unter dem Titel angezeigt. Tippe darauf, um das Projekt zu öffnen. Unter **Details** kannst du es bei **Projekt** ändern oder entfernen. Mehr dazu unter [Aufgaben eines Projekts](projects.md#a-projects-to-dos).

Unter **Details** kannst du mit **Bereich** eine Aufgabe in deinen anderen Bereich verschieben. Der Zugriff auf Nachrichten und die Möglichkeit, Nachrichten zu senden, werden dabei ebenfalls verschoben. Über **Rückgängig** in der Notiz kannst du sie zurückverschieben.

Wenn eine Aufgabe deinen anderen Bereich braucht, um weiterzugehen, und alle Nachrichten, auf denen sie beruht, dort sind, wird sie automatisch dorthin verschoben und fortgesetzt. Andernfalls wird **Nach Arbeit verschieben** angezeigt. Bis du darauf tippst, wird nichts verschoben. Eine Aufgabe, die du selbst hinzugefügt hast, ohne Arbeit oder Privat auszuwählen, wird automatisch verschoben, sobald klar ist, wohin sie gehört. Bis dahin gehört sie weder zu Arbeit noch zu Privat und bleibt privat.

Eine Aufgabe kann immer die Nachrichten lesen, aus denen sie entstanden ist. Wenn sie weitere Nachrichten aus deinem anderen Bereich benötigt, fragt sie mit **Diese E-Mail für diese Aufgabe verwenden** danach. Ein Arbeits-Postfach, das du als Privat gekennzeichnet hast, zählt als Privat. Nachrichten für ein anderes Unternehmen von dir gehören zu den Aufgaben dieses Unternehmens. Eine Aufgabe zu deinem Privatleben, etwa wenn deine Familie an deine Arbeitsadresse schreibt, gehört von Anfang an zu Privat.

Arbeit, die dich über ein privates Konto erreicht, etwa eine Nachricht von einem Kunden auf WhatsApp oder eine Bestellung in deinem privaten Postfach, gehört von Anfang an zu Arbeit. Eine Aufgabe, die du selbst verschoben oder zugeordnet hast, bleibt immer dort, wo du sie abgelegt hast. Arbeit oder Privat bestimmt, wo eine Aufgabe angezeigt und mit wem sie geteilt wird, aber nie, wohin sie antwortet. Eine Antwort geht immer dorthin, wo das Gespräch stattfindet, auch nach dem Verschieben, es sei denn, du wählst einen anderen Weg.

Eine solche private Aufgabe antwortet trotzdem von der Arbeitsadresse aus, an die ihre E-Mail gesendet wurde, und wird nie in einer Work Fleet oder im Team Graph angezeigt.

Wenn mindestens zwei Aufgaben auf dich warten, kannst du mit **Durchgehen** in der Kopfzeile von Für dich eine nach der anderen bearbeiten, in der Reihenfolge der Liste. Jeder Entwurf wird vollständig angezeigt, zusammen mit **Senden** oder **Ausführen**, **Änderungen anfragen**, **Zurückstellen** und **Überspringen**. Auf einem Computer sendet Enter, `S` stellt zurück, `→` überspringt und Esc beendet den Vorgang. Unter dem Titel steht in der Kopfzeile auch, wie lange es in deinem Tempo dauert, etwa „ca. 2 Min.“

Aufgaben, die dir eine Frage stellen, werden bei beiden Ansichten ausgelassen: Sie brauchen deine Antwort, keinen Tipp.

## Jetzt prüfen

Deine Machine liest jede Quelle alle paar Minuten, Tag und Nacht. Sie prüft neu eingegangene Nachrichten, sobald 40 Nachrichten vorliegen oder die älteste Nachricht einer Person 15 Minuten gewartet hat. Newsletter, Benachrichtigungen und Belege werden bei der nächsten Prüfung innerhalb einer Stunde berücksichtigt.

Nachts, von 00:00 bis 06:30 Uhr, pausieren die Prüfungen. Neue Nachrichten werden weiterhin gelesen und gespeichert. Um 06:30 Uhr werden sie gemeinsam geprüft, sodass deine Aufgaben vor der morgendlichen Zusammenfassung bereit sind. Unter Verbindungen bei den Prüfungen steht dann „Nachts pausiert, Aufholen um 06:30“. Wenn du nachts die App öffnest, im Chat schreibst oder auf eine Aufgabe tippst, laufen die Prüfungen wieder wie gewohnt, bis du eine Stunde lang inaktiv warst. Mit **Jetzt prüfen** wird immer sofort geprüft.

**Jetzt prüfen** liest sofort alle Quellen. Wenn keine Aufgaben offen sind, tippe auf die Zeile deiner Machine, um sie zusammen mit **Details** anzuzeigen. Dadurch werden die Prüfungen unter Verbindungen geöffnet. Wenn Aufgaben offen sind, findest du die Zeile oben auf dem Computer. Eine kurze Zeile wird nur angezeigt, während eine Prüfung läuft oder wenn sie fehlgeschlagen ist oder sich verzögert. Du kannst auch im Chat danach fragen.

LinkedIn, X und Salesflare folgen ihrem eigenen Rhythmus.

## Letzte Prüfung

Nach einer Prüfung, bei der neue Nachrichten gelesen wurden, zeigt eine Zeile über deinen Aufgaben, was in allen gelesenen Quellen gefunden wurde, etwa „13 Nachrichten um 16:11 geprüft · nichts braucht dich“ oder „· 2 neue Aufgaben“. Wenn eine neue Aufgabe auf einen günstigeren Zeitpunkt wartet, etwa auf deine morgendliche Zusammenfassung, steht dort bis wann: „1 Aufgabe bis morgen 08:30 zurückgestellt“.

Tippe auf die Zeile, um die einzelnen E-Mail-Threads, Chats und Benachrichtigungen mit dem Symbol der jeweiligen Quelle zu sehen: wer geschrieben hat, der Betreff oder die ersten Wörter sowie die neue Aufgabe oder der Grund, warum nichts nötig war, etwa „Nur in Cc, ein Teammitglied antwortet“ oder „Termin für Donnerstag steht bereits“. Wenn die Prüfung nur einen ungenauen Grund ergeben hat, wird für einen Thread kein Grund angezeigt. Tippe auf einen Eintrag, um ihn zu lesen.

Die ersten 10 Einträge werden angezeigt. Tippe darunter, um den Rest zu sehen. Eine Zahl hinter einem Namen, etwa (3), gibt an, wie viele neue Nachrichten dieser Chat enthält. Eine Handybenachrichtigung zu einer Nachricht, die bereits aufgelistet ist, wird nur einmal angezeigt. Die Zeile bleibt nach der Prüfung 12 Stunden lang sichtbar.

Gezählt werden nur E-Mails an dich. Deine eigenen Antworten werden als Kontext und für Versprechen gelesen, zählen aber nicht als neue E-Mails. Eigene E-Mails von The Machine an dich, etwa deine morgendliche Zusammenfassung oder ein Hinweis zu einer Korrektur, werden nie gelesen oder aufgelistet. E-Mails zu Abrechnung, Testphase oder Einladungen werden wie gewohnt gelesen.

## Die Schaltflächen

Eine Aufgabe zeigt den nächsten Schritt, etwa **Ausführen** oder **Prüfen und senden**, daneben **Zurückstellen**. Mehr dazu unter [Ausführen](do-it.md) und [Zurückstellen](snooze.md).

Unter **Änderungen anfragen** steht, was geändert werden soll: wie die Aufgabe erledigt werden soll oder, sobald ein Entwurf bereit ist, was daran geändert werden soll. **Als erledigt markieren** bedeutet, dass die Aufgabe erledigt ist. Bei einer vorbereiteten Aufgabe ohne Entwurf ist die Schaltfläche direkt sichtbar, andernfalls findest du sie oben unter **…**, auch bei Aufgaben, die deine Entscheidung brauchen. Die Aufgabe wird sofort aus der Liste entfernt. In der Nachricht findest du **Rückgängig**. Wische die Nachricht weg oder ziehe sie mit der Maus aus der Liste, um sie schneller zu schließen. Die Änderung bleibt bestehen.

Wenn die Aufgabe anders erledigt werden soll, sag es im **Chat**.

Unter **…**:

- **Übergeben…**: Weise die Aufgabe einem Teammitglied oder [Claude Code oder Codex](hand-to-agent.md) zu oder [bitte jemanden um eine Prüfung](ask-to-review.md).
- **Wiederholen…**: Die Aufgabe [kommt regelmäßig zurück](recurring.md).
- **Nicht nötig**: Die Aufgabe wird entfernt. Optional kannst du einen Grund auswählen: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Tippe auf den Titel oder unter **Details** auf **Name**, um die Aufgabe umzubenennen. Dein Titel bleibt erhalten.

Mit **Wieder öffnen** holst du eine geschlossene Aufgabe zurück. Sie kommt auch automatisch zurück, wenn etwas Neues passiert, etwa wenn die Person dir eine neue Nachricht schreibt, aber nicht bei deiner eigenen Antwort.

Eine Rechnung, die du selbst noch bezahlen musst, wird unabhängig vom Land zu einer Aufgabe. Sie enthält den Betrag, das Fälligkeitsdatum und die Zahlungsdetails auf der Rechnung. Automatisch bezahlte Rechnungen, etwa per Lastschrift oder mit einer hinterlegten Karte, werden nicht aufgenommen. Wenn eine spätere E-Mail zeigt, dass die Rechnung bezahlt wurde, etwa eine Bestätigung des Absenders über den Zahlungseingang, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang zurückholen.

Eine Aufgabe, die nur bis zu einem bestimmten Zeitpunkt wichtig ist, etwa eine Bestätigung vor einem Termin, wird danach automatisch geschlossen. Sie wird unter **Erledigt / verworfen** als „Nicht mehr nötig“ angezeigt. Mit **Rückgängig** kannst du sie einen Tag lang zurückholen.

Bevor eine Nachricht oder Übergabe für jemanden als bereit angezeigt wird, prüft deine Machine deine letzten Chats mit den beteiligten Personen, auch Gruppenchats, und wartet darauf, dass Slack sie einliest. Wenn eine spätere Nachricht zeigt, dass die Aufgabe bereits erledigt ist, etwa weil die Person gefragt wurde und zugesagt hat, wird sie automatisch geschlossen. Mit **Rückgängig** kannst du sie einen Tag lang zurückholen.

Wenn eine neuere Nachricht den Plan ändert, etwa weil eine Party an einen anderen Ort verlegt oder eine Buchung storniert wurde, aktualisiert The Machine ihre Aufgaben selbst. Eine Aufgabe, die weiterhin wichtig ist, wird an den neuen Plan angepasst. Wenn nichts mehr zu tun ist, wird sie unter **Erledigt / verworfen** als „Nicht nötig“ angezeigt. In ihrem Chat steht „Aktualisiert:“ mit einer Begründung. Mit **Rückgängig** kannst du sie einen Tag lang zurückholen.

Bei deinen ersten Aufgaben wird ein kurzer Tipp mit den wichtigsten Aktionen angezeigt: **Änderungen anfragen** und **Nicht nötig**. Außerdem wird erklärt, dass nichts gesendet wird, bis du auf **Senden** tippst. Ein Tipp verschwindet dauerhaft, sobald du seine Schaltfläche verwendest oder auf × tippst.

An deinem ersten Tag begrüßt dich die Kopfzeile unter Aufgaben und nennt die Person, die am längsten auf deine Antwort wartet. Diese Antwort wird zuerst als Entwurf vorbereitet, damit sie bereit ist, wenn du kommst.

Jede Aufgabe beginnt mit ihrem Titel. Die Zeile darunter nennt die Person, um die es geht, und, falls relevant, die Organisation, das Projekt, Arbeit oder Privat und den Zeitpunkt des Eingangs. Tippe auf einen Namen, um die Seite der Person im Graph zu öffnen.

Bei Namen und Organisationen wird, sofern im Graph vorhanden, das Foto oder Logo angezeigt, andernfalls die Initialen. Bei einem Logo, das in dieser Größe nicht gut lesbar wäre, etwa weiß auf transparentem Hintergrund oder bei einem breiten Schriftzug, wird ebenfalls die Initiale angezeigt.

Manchmal steht in einer unauffälligen Zeile, was nicht bekannt ist, etwa „Letzter Kontakt vor 12 Tagen per E-Mail; seitdem nichts“. Sie erscheint, wenn der letzte Austausch schon länger zurückliegt oder unbeantwortet ist, und nennt nicht verbundene Kanäle wie WhatsApp. Deine Machine sagt, was sie nicht weiß, statt zu raten.

Wenn ein nicht verbundener Kanal genannt wird, öffnet **Verbinden** daneben die entsprechende Verbindung.

Der Titel sagt, was zu tun ist, und ändert sich nur, wenn sich das ändert. Eine erledigte Aufgabe behält ihren Titel. Darunter steht, wie sie abgeschlossen wurde, etwa „Erledigt: Sam hat es am Dienstag unterschrieben“.

Über dem Entwurf steht in einer dezenten Zeile die Nachricht, aus der er entstanden ist, mit dem Logo des jeweiligen Dienstes. Tippe darauf, um den Thread zu lesen. Der Entwurf zeigt das Logo des Zielorts, sodass du sofort siehst, ob es eine Slack-Antwort oder eine E-Mail ist.

Wenn der Entwurf auf einem Beitrag an anderer Stelle beruht, etwa auf einem Vorschlag eines Teammitglieds in Slack, steht das in einer Zeile, etwa „Basiert auf Sam in #ops“. Tippe darauf, um die Nachricht zu lesen.

Ein Chat (Slack, WhatsApp, Telegram, Intercom …) wird als eine Unterhaltung angezeigt, die ältesten Nachrichten zuerst: erst die Nachrichten vor der Nachricht, um die es in der Aufgabe geht, dann die Antworten darauf. In WhatsApp, Telegram oder Signal stehen deine Nachrichten rechts, wie in der App. Die Nachricht der Aufgabe ist als „Diese Aufgabe“ markiert und wird direkt angezeigt. Mit **Frühere Nachrichten anzeigen** werden ältere Nachrichten hinzugefügt. Bei einer E-Mail ist der Rest des Threads darüber und darunter eingeklappt.

Unter **Details** einer E-Mail werden nur Angaben angezeigt, die nicht bereits in der Kopfzeile stehen, etwa vollständige Cc-Adressen, Bcc oder eine andere Antwortadresse. Gibt es nichts hinzuzufügen, wird nichts angezeigt.

Eine Antwort in einem Slack-Thread zeigt auch, was vor Beginn des Threads gesagt wurde. Über den Link einer Aufgabe zur zugehörigen Nachricht wird sie ebenfalls hier geöffnet. Unten findest du **In Slack öffnen**.

Unter **Details** findest du den Namen, das Projekt und den Bereich. Tippe auf einen Eintrag, um ihn zu ändern. Dort stehen auch deine letzte Notiz und das Ergebnis eines Coding-Agenten. Über **Chat ›** öffnest du den Chat. Eine erledigte Aufgabe bleibt kurz. Die Nachricht, aus der sie entstanden ist, findest du unter **Details**.

Bei einer Aufgabe mit „Wartet auf“ ist deine letzte Nachricht an die Person verlinkt, auf deren Antwort du wartest: „E-Mail an Pat · Di“.

## Selbst eine Aufgabe erstellen

Mit **Neue Aufgabe** (auf dem Computer unter **Suchen**) kannst du für alles eine Aufgabe erstellen. Beim Erstellen wird nichts gesendet. Wenn weder Arbeit noch Privat ausgewählt ist, wird die Aufgabe anhand der beteiligten Personen und des Themas dem passenden Bereich zugeordnet. Die E-Mail, auf die sie sich bezieht, wird ebenfalls gefunden, auch wenn sie schon älter ist.

- **Fällig**: Gib einen Tag oder eine Uhrzeit ein, etwa „morgen“, „nächsten Fr.“, „3. Nov.“, „14 Uhr“ oder „in 2 Stunden“, auch in deiner Sprache. Über das Kalendersymbol findest du Kurzauswahlen und **Datum wählen**.
- **Nachricht**: Hänge die betreffende Nachricht an: eine E-Mail, Slack-, Teams-, WhatsApp-, Telegram- oder eine andere Nachricht, die The Machine kennt. Suche nach Text oder Absender. Bei jedem Treffer wird angezeigt, woher er stammt, wer ihn gesendet hat und wann.
- **Dateien**: Tippe auf die Büroklammer, füge einen Screenshot ein oder ziehe Dateien auf das Formular. Auf dem Handy kannst du mit der Kamera daneben ein Foto aufnehmen. Du kannst bis zu 5 Dateien hinzufügen, wie im Chat (siehe [Dateien hinzufügen](card-chat.md#add-files)). Mit × entfernst du eine Datei.

Die Dateien bleiben bei der Aufgabe, und The Machine liest sie, wenn sie daran arbeitet. Auch Dateien allein reichen: The Machine erstellt die Aufgabe aus einer PDF- oder Textdatei. Ein Foto wird als kleines Bild angezeigt. Tippe darauf, um es in voller Größe zu sehen.
