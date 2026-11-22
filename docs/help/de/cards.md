---
title: Aufgaben
area: cards
summary: Eine Aufgabe pro Sache, bei der du gefragt bist, bereit für dein Okay. Was die einzelnen Teile einer Aufgabe bedeuten.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 84b8879d98f26aa2
---
Deine Machine liest alles Neue und erstellt nur dann eine Aufgabe, wenn etwas von dir gebraucht wird. Pro Thema eine Aufgabe, egal über wie viele Nachrichten es sich erstreckt.

## Wo Aufgaben stehen

Auf der Seite **Aufgaben** sind sie gruppiert:

- **Gerade erledigt**: Oben siehst du einen letzten Schritt, den du bestätigt hast, etwa ein Formular oder einen Vorgang, der während deiner Abwesenheit abgeschlossen wurde. Er bleibt höchstens einen Tag lang stehen, bis du auf **Verstanden** tippst. Auch dein Handy bekommt eine Benachrichtigung.
- **Für dich**: Alles, worauf du reagieren musst, zuerst das Dringendste. Bei jeder Aufgabe steht **Vorbereitet** (die Arbeit ist erledigt, mit **Ausführen** oder **Senden** wird sie abgeschlossen), **Braucht dich** (zuerst ist deine Entscheidung oder Antwort nötig), **Wird vorbereitet…** (deine Machine arbeitet daran) oder **Zum Lesen** (eine Zusammenfassung oder ein Briefing, bei dem nichts zu entscheiden ist).
- **Älter**: Eingeklappte Aufgaben, zu denen es seit einer Woche nichts Neues gibt (siehe unten).
- **Wartet auf andere**: Eingeklappte Aufgaben, bei denen der nächste Schritt bei jemand anderem liegt (siehe unten).
- **Kommt später zurück**: Zurückgestellte Aufgaben und Aufgaben ohne Antwort auf **Noch nötig?** (siehe unten).
- **Versprechen**: Was du versprochen hast und was andere dir versprochen haben. Siehe [Versprechen](promises.md).
- **Erledigt / verworfen**: Alle abgeschlossenen Aufgaben, die neueste zuerst, samt Zeitpunkt des Abschlusses, etwa „Vor 5 Minuten erledigt“. Aufgaben, die bereits erledigt zu sein scheinen, sind mit **Sieht erledigt aus** markiert.

Nach dem Senden steht in einer kurzen Meldung, wohin die Aufgabe verschoben wurde, etwa „Gesendet. Nach Erledigt verschoben.“ oder „Gesendet. Bis Mo. auf Später verschoben.“ Eine Antwort, die nur verspricht, die Aufgabe zu erledigen, etwa „Ich schicke es bis Dienstag“, lässt die Aufgabe offen: „Gesendet. Offen gelassen.“ Über **Öffnen** gelangst du zur Aufgabe. Über die Suche findest du Aufgaben nach Titel oder danach, an wen sie gingen, auch unter Später und Erledigt.

Unter **Für dich** stehen zuerst überfällige Aufgaben oder Aufgaben, die bis morgen fällig sind, dann Fragen aus deiner Fleet, anschließend Nachfassaufgaben eines Boards und danach alle übrigen. Innerhalb jeder Gruppe stehen die neuesten zuerst. Eine Aufgabe bleibt an ihrem Platz, während deine Machine sie vorbereitet und auch, wenn sie erledigt ist: Nur ihre Markierung ändert sich. In den anderen offenen Gruppen stehen überfällige Aufgaben und Aufgaben, die bis morgen fällig sind, zuerst, danach die neuesten. Die Seitenleiste behält dieselbe Reihenfolge bei.

**Sieht erledigt aus** bedeutet, dass deine Machine die Aufgabe für erledigt hält, etwa „PR #3451 zusammengeführt“, sie aber noch nicht abgeschlossen ist. Über **Wieder öffnen** kommt sie zurück auf deine Liste, und deine Machine lernt daraus. Diese Aufgaben werden nie als überfällig angezeigt. Nach einem Tag wird die Aufgabe von selbst geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Eine Aufgabe, die du selbst schon erledigt hast, etwa durch eine Antwort in Gmail oder Slack, wird ebenfalls von selbst geschlossen.

Wenn eine Nachricht von einer Adresse kommt, die nur wie die einer bekannten Person aussieht, etwa sam@acme-corp.example statt sam@acmecorp.example, steht das deutlich bei der Aufgabe: „Das ist nicht Sam Lee.“ Die Person wird mit ihrer tatsächlichen Adresse angezeigt, nie mit dem Namen, den sie verwendet hat. Deine Machine prüft solche Nachrichten bei der Person unter der Adresse, die du bereits kennst, niemals bei der Person, die geschrieben hat.

Bei einer Aufgabe, die noch auf jemand anderen wartet, etwa auf eine Prüfung oder Antwort, steht **Wartet auf:** mit dem nächsten Schritt. Sie erscheint eingeklappt unter **Wartet auf andere**, oberhalb von Kommt später zurück, bis eine neue Nachricht sie wieder hervorholt. Dasselbe gilt, wenn du eine Rückfrage gestellt hast: Die Aufgabe kommt am Morgen vor der Frist zurück, am Tag der Frist, wenn diese noch heute liegt, oder am nächsten Morgen, wenn die Frist schon verstrichen ist. Dabei steht, auf wen sie noch wartet.

Wenn es bei einer Aufgabe um ein Ergebnis geht, das jemand anderes liefern muss, etwa einen unterschriebenen Vertrag, wird es unter **Details** bei **Fertig, wenn** angezeigt. Wenn du deinen Teil abschickst, wird die Aufgabe nicht geschlossen: Sie wartet unter **Wartet auf andere**, bis eine Nachricht das Ergebnis bestätigt. Dann wird sie von selbst geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. Wenn bis zum Zeitpunkt, an dem du nachhaken solltest, nichts eingegangen ist, erscheint die Aufgabe wieder mit **Schreib eine kurze Erinnerung** im Chat. Sag im Chat, was als erledigt gilt, um das zu ändern.

Wenn es eine Woche lang nichts Neues zu einer Aufgabe gibt, wird sie von Für dich nach **Älter** verschoben. So stehen nach ein paar Tagen Abwesenheit die neuen Aufgaben zuerst. Als neu zählt eine neue Nachricht zur Aufgabe oder eine Aktion von dir, etwa eine Chatnachricht, eine Bearbeitung oder das Zurückstellen. Nur die Aufgabe anzusehen zählt nicht.

Dringende Aufgaben, bald fällige Aufgaben und Aufgaben, bei denen das Senden noch aussteht, bleiben unter Für dich. Über **Alle verwerfen** kannst du nach einer Bestätigung alle Aufgaben unter Älter als nicht nötig markieren. Mit **Nicht nötig** geht das auch einzeln. Mit **Rückgängig** kannst du es rückgängig machen. Gibt es bei einer Aufgabe etwas Neues, kommt sie zurück zu Für dich.

Bei einer Aufgabe, die eine Woche lang niemand angerührt hat, wird einmal gefragt: **Noch nötig?** Mit **Nicht nötig** wird sie geschlossen. Mit **Rückgängig** kannst du das rückgängig machen. **Behalten** lässt sie offen, und die Frage wird nie wieder gestellt. Wenn eine weitere Woche lang keine Antwort kommt, wird die Aufgabe unter Kommt später zurück eingeklappt. Sie wird dann nicht mehr auf dem App-Symbol oder in der morgendlichen Zusammenfassung mitgezählt. Wenn du sie öffnest, eine Chatnachricht schreibst, sie bearbeitest oder zurückstellst oder eine neue Nachricht eingeht, kommt sie zurück.

Ein Projekt, zu dem es länger nichts Neues gab und bei dem keine Aufgaben offen sind, kann einmal pro Woche eine Aufgabe mit einem konkreten nächsten Schritt bekommen, höchstens drei pro Woche. Siehe [Projekte](projects.md).

Wenn nichts von dir gebraucht wird, ruht deine Machine und die Liste ist leer. Während sie etwas prüft, wird sie aktiv und zeigt das an. Wenn eine Prüfung fehlgeschlagen ist oder sich verspätet, steht es in der Zeile. Darunter findest du **Jetzt prüfen**.

Mit **Alle**, **Arbeit** und **Privat** oben in der Seitenleiste kannst du alle Aufgaben oder nur eine Kategorie anzeigen. Auf deinem Handy und Computer gilt dieselbe Auswahl. Wenn Arbeit oder Privat ausgewählt ist, bringt **Alle anzeigen** dich zurück zur Gesamtansicht. Eine Meldung zu deiner Machine selbst, etwa dass ein Teil immer wieder neu startet, gehört weder zu Arbeit noch zu Privat und wird nur unter Alle angezeigt.

Über die Zeile oben in der Liste kannst du auch direkt zur jeweils anderen Ansicht wechseln: Wenn **Nur privat** ausgewählt ist, tippe auf **Arbeit** oder **Alle anzeigen**.

In der Zeile oben in der Liste stehen der Name deiner letzten morgendlichen oder abendlichen Zusammenfassung und die Anzahl der darin gezählten Aufgaben, etwa **Zusammenfassung von gestern Abend** · 12 erledigt, 3 offen. Tippe darauf, um die Zusammenfassung noch einmal zu lesen. Mit **Kopieren** kannst du sie an beliebiger Stelle einfügen. Sobald du sie öffnest oder auf das **×** tippst, bleibt sie auf all deinen Geräten sichtbar, bis die nächste Zusammenfassung kommt.

Wenn es keine aktuelle Zusammenfassung gibt, wird **Heute bisher** angezeigt: was heute erledigt wurde und was noch offen ist, für Arbeit und Privat oder nur für die ausgewählte Kategorie.

Bei einer Aufgabe zu einem Projekt steht der Projektname unter dem Titel. Tippe darauf, um das Projekt zu öffnen. Unter **Details** kannst du mit **Projekt** das Projekt ändern oder entfernen. Siehe [Aufgaben eines Projekts](projects.md#a-project-s-to-dos).

Mit **Bereich** unter **Details** verschiebst du eine Aufgabe in deinen anderen Bereich. Der Zugriff auf Inhalte, die sie lesen und senden darf, wird mitverschoben. Über **Rückgängig** in der Meldung verschiebst du sie zurück.

Wenn eine Aufgabe deinen anderen Bereich braucht, um fortzufahren, und alle zugehörigen Nachrichten dort liegen, wird sie automatisch dorthin verschoben und fortgesetzt. Andernfalls wird **Nach Arbeit verschieben** angezeigt. Verschoben wird erst, wenn du darauf tippst. Eine Aufgabe, die du ohne Auswahl von Arbeit oder Privat hinzugefügt hast, wird automatisch dem passenden Bereich zugeordnet, sobald klar ist, wohin sie gehört. Bis dahin gehört sie weder zu Arbeit noch zu Privat und bleibt privat.

Eine Aufgabe kann die Nachrichten, aus denen sie entstanden ist, immer lesen. Wenn sie weitere Nachrichten aus deinem anderen Bereich braucht, fragt sie mit **Diese E-Mail für diese Aufgabe verwenden** danach. Ein Arbeits-Postfach, das du als Privat gekennzeichnet hast, zählt als Privat. E-Mails für ein anderes deiner Unternehmen gehören zu den Aufgaben dieses Unternehmens. Eine Aufgabe zu deinem Privatleben, etwa wenn deine Familie an deine Arbeitsadresse schreibt, ist von Anfang an Privat.

Arbeit, die dich über ein privates Konto erreicht, etwa eine Nachricht von einem Kunden auf WhatsApp oder eine Bestellung in deinem privaten Postfach, ist von Anfang an Arbeit. Eine Aufgabe, die du selbst verschoben oder zugeordnet hast, bleibt immer dort, wo du sie abgelegt hast. Arbeit oder Privat bestimmt, wo eine Aufgabe angezeigt und mit wem sie geteilt wird, aber nicht, wohin sie antwortet: Die Antwort geht immer dorthin, wo die Unterhaltung stattfindet, auch nach dem Verschieben, es sei denn, du wählst einen anderen Weg.

Eine solche private Aufgabe antwortet trotzdem von der Arbeitsadresse aus, an die die E-Mail geschickt wurde. Sie erscheint nie in einer Work Fleet oder im Team Graph.

Wenn mindestens zwei Aufgaben auf dich warten, kannst du über **Durchgehen** in der Kopfzeile von Für dich alle nacheinander in der Reihenfolge der Liste bearbeiten. Du siehst jeweils den vollständigen Entwurf mit **Senden** oder **Ausführen**, **Änderungen anfragen**, **Zurückstellen** und **Überspringen**. Am Computer sendet Enter den angezeigten Inhalt, `S` stellt zurück, `→` überspringt und Esc beendet den Ablauf. Unter dem Titel steht in der Kopfzeile auch, wie lange die Aufgaben in deinem Tempo ungefähr dauern, etwa „ca. 2 Min.“.

Eine Aufgabe, die dir eine Frage stellt, wird dabei ausgelassen: Sie braucht deine Antwort, nicht einen Tippen.

## Jetzt prüfen

Deine Machine liest jede Quelle alle paar Minuten, Tag und Nacht. Sie prüft neue Inhalte, sobald 40 Nachrichten eingegangen sind oder die älteste Nachricht einer Person seit 15 Minuten vorliegt. Newsletter, Benachrichtigungen und Belege werden bei der nächsten Prüfung berücksichtigt, spätestens innerhalb einer Stunde.

Nachts zwischen 00:00 und 06:30 Uhr werden Prüfungen pausiert. Neue Nachrichten werden weiterhin gelesen und gespeichert und um 06:30 Uhr gemeinsam geprüft, damit deine Aufgaben vor der morgendlichen Zusammenfassung bereit sind. Unter Verbindungen steht bei Prüfungen: „Nachts pausiert, holt um 06:30 Uhr auf“. Wenn du nachts in der App klickst, schreibst oder scrollst, im Chat schreibst oder auf eine Aufgabe tippst, laufen die Prüfungen wie gewohnt weiter, bis du eine Stunde lang nicht aktiv warst. Mit **Jetzt prüfen** wird immer sofort geprüft.

**Jetzt prüfen** liest sofort alle Quellen. Wenn keine Aufgabe offen ist, tippe auf die Zeile deiner Machine, um sie mit **Details** zu sehen. Dadurch werden die Prüfungen unter Verbindungen geöffnet. Wenn Aufgaben offen sind, findest du die Zeile am Computer oben. Eine kurze Meldung wird dort nur angezeigt, während eine Prüfung läuft oder wenn eine fehlgeschlagen ist oder sich verspätet. Du kannst auch im Chat danach fragen.

LinkedIn, X und Salesflare folgen ihrem eigenen Rhythmus.

## Letzte Prüfung

Nach einer Prüfung, bei der neue Nachrichten gelesen wurden, steht über deinen Aufgaben, was gefunden wurde und aus welchen Quellen, etwa „13 Nachrichten um 16:11 geprüft · nichts braucht dich“ oder „· 2 neue Aufgaben“. Wenn eine neue Aufgabe bis zu einem günstigeren Zeitpunkt zurückgehalten wird, etwa bis zur morgendlichen Zusammenfassung, steht dort bis wann: „1 Aufgabe bis morgen 08:30 zurückgehalten“.

Tippe auf die Zeile, um jeden E-Mail-Thread, Chat und jede Benachrichtigung mit dem Symbol der jeweiligen Quelle zu sehen: wer geschrieben hat, den Betreff oder die ersten Wörter und die zugehörige neue Aufgabe oder den Grund, warum nichts nötig war, etwa „Nur in CC, ein Teammitglied antwortet“ oder „Termin für Donnerstag steht schon“. Wenn die Prüfung nur einen ungenauen Grund ergeben hat, wird bei einem Thread kein Grund angezeigt. Tippe darauf, um ihn zu lesen.

Die ersten 10 werden angezeigt. Tippe darunter, um die übrigen zu sehen. Eine Zahl hinter einem Namen, etwa (3), gibt an, wie viele neue Nachrichten dieser Chat enthält. Eine Handy-Benachrichtigung zu einer bereits aufgelisteten Nachricht wird nur einmal angezeigt. Die Zeile bleibt nach der Prüfung 12 Stunden lang sichtbar.

Gezählt werden nur E-Mails an dich. Deine eigenen Antworten werden als Kontext und auf Versprechen hin gelesen, zählen aber nicht als neue E-Mails. E-Mails von The Machine an dich, etwa deine morgendliche Zusammenfassung oder eine Benachrichtigung zu einer Fehlerbehebung, werden nie gelesen oder aufgelistet. Nachrichten zu Abrechnung, Testphase oder Einladungen werden wie gewohnt gelesen.

## Die Schaltflächen

Bei einer Aufgabe steht der nächste Schritt, etwa **Ausführen** oder **Prüfen und senden**, mit **Zurückstellen** daneben. Siehe [Ausführen](do-it.md) und [Zurückstellen](snooze.md).

Mit **Änderungen anfragen** kannst du angeben, was geändert werden soll: wie die Aufgabe erledigt werden soll oder, sobald ein Entwurf bereit ist, was daran geändert werden soll. **Als erledigt markieren** bedeutet, dass die Aufgabe erledigt ist. Bei einer vorbereiteten Aufgabe ohne Entwurf steht die Schaltfläche direkt zur Verfügung, andernfalls oben unter **…**, auch bei einer Aufgabe, die deine Entscheidung braucht. Die Aufgabe wird sofort aus der Liste entfernt. In der Meldung findest du **Rückgängig**. Wische die Nachricht weg oder zieh sie mit der Maus aus der Liste, um sie schneller zu schließen. Die Änderung bleibt bestehen.

Wenn die Aufgabe anders erledigt werden soll, sag es im **Chat**.

Unter **…**:

- **Übergeben…**: Gib die Aufgabe an ein Teammitglied, [Claude Code oder Codex](hand-to-agent.md) weiter oder [bitte jemanden um eine Prüfung](ask-to-review.md).
- **Wiederholen…**: Die Aufgabe [kommt regelmäßig wieder](recurring.md).
- **Nicht nötig**: Die Aufgabe wird entfernt. Du kannst optional einen Grund auswählen: **Nicht relevant**, **Falsche Fakten** oder **Schon erledigt**. Deine Machine lernt daraus.

Tippe auf den Titel oder unter **Details** auf **Name**, um ihn zu ändern. Du kannst auch im Chat darum bitten, etwa mit „Benenne es in … um“. Dein Titel bleibt erhalten.

Mit **Wieder öffnen** holst du eine geschlossene Aufgabe zurück. Sie kommt auch von selbst zurück, wenn etwas Neues passiert, etwa eine neue Nachricht von der anderen Person, aber nicht bei deiner eigenen Antwort. Dann steht dort, wann sie zurückkam, und sie wird wie eine neue Aufgabe einsortiert. Der Chat wird an der Stelle fortgesetzt, an der er aufgehört hat, auch nach Wochen.

Eine Rechnung, die du selbst noch bezahlen musst, wird unabhängig vom Land als Aufgabe mit Betrag, Fälligkeitsdatum und Zahlungsangaben aus der Rechnung erfasst. Rechnungen, die automatisch bezahlt werden, etwa per Lastschrift oder gespeicherter Karte, werden nicht erfasst. Wenn eine spätere E-Mail die Zahlung bestätigt, etwa eine Bestätigung des Absenders, dass deine Zahlung eingegangen ist, wird die Aufgabe automatisch geschlossen. Mit **Rückgängig** kannst du sie innerhalb eines Tages wiederherstellen.

Eine Aufgabe, die nur bis zu einem bestimmten Zeitpunkt wichtig war, etwa eine Bestätigung vor einem Termin, wird danach automatisch geschlossen. Sie wird unter **Erledigt / verworfen** als „Nicht mehr nötig“ abgelegt. Mit **Rückgängig** kannst du sie innerhalb eines Tages wiederherstellen.

Bevor eine Nachricht oder Übergabe für jemanden als bereit angezeigt wird, prüft deine Machine deine aktuellen Chats mit den betreffenden Personen, auch Gruppenchats, und wartet darauf, dass Slack sie gelesen hat. Wenn eine spätere Nachricht zeigt, dass die Aufgabe bereits erledigt ist, etwa weil jemand darum gebeten wurde und zugestimmt hat, wird sie automatisch geschlossen. Mit **Rückgängig** kannst du sie innerhalb eines Tages wiederherstellen.

Wenn eine neuere Nachricht den Plan ändert, etwa wenn eine Party an einen anderen Ort verlegt oder eine Buchung storniert wird, aktualisiert The Machine ihre Aufgaben selbst. Eine Aufgabe, die weiterhin wichtig ist, folgt dem neuen Plan. Wenn nichts mehr zu tun ist, wird sie unter **Erledigt / verworfen** als „Nicht nötig“ abgelegt. Im Chat steht „Aktualisiert:“ mit einer Begründung. Mit **Rückgängig** kannst du sie innerhalb eines Tages wiederherstellen.

Bei deinen ersten Aufgaben erscheint ein kurzer Tipp mit den wichtigsten Aktionen: **Änderungen anfragen** und **Nicht nötig**. Außerdem wird erklärt, dass nichts gesendet wird, bevor du auf **Senden** tippst. Ein Tipp wird dauerhaft ausgeblendet, sobald du seine Schaltfläche verwendest oder auf × tippst.

Am ersten Tag begrüßt dich deine Machine oben auf der Seite Aufgaben und nennt die Person, die am längsten auf deine Antwort wartet. Dieser Antwortentwurf wird zuerst erstellt, damit er bereit ist, wenn du kommst.

Jede Aufgabe beginnt mit ihrem Titel. In der Zeile darunter stehen, um wen es geht, gegebenenfalls die Organisation (nicht allein deshalb, weil jemand dort arbeitet), das Projekt, Arbeit oder Privat und wann die Aufgabe eingegangen ist. Tippe auf einen Namen, um die entsprechende Seite im Graph zu öffnen.

Bei Namen und Organisationen wird das Foto oder Logo angezeigt, wenn es im Graph vorhanden ist, andernfalls die Initialen. Wenn ein Logo in dieser Größe nicht lesbar wäre, etwa weiße Schrift auf transparentem Hintergrund oder ein breiter Schriftzug, wird stattdessen ebenfalls die Initiale angezeigt.

Manchmal wird in einer unauffälligen Zeile angegeben, was nicht bekannt ist, etwa „Letzter Kontakt vor 12 Tagen per E-Mail, seitdem nichts.“ Das erscheint, wenn der letzte Kontakt schon lange zurückliegt oder unbeantwortet ist, und nennt nicht verbundene Kanäle wie WhatsApp. Deine Machine sagt, was sie nicht weiß, statt zu raten.

Wenn ein nicht verbundener Kanal genannt wird, öffnet **Verbinden** daneben die entsprechende Verbindung.

Ein Titel sagt, was zu tun ist, und ändert sich nur, wenn sich das ändert. Eine erledigte Aufgabe behält ihren Titel. Darunter steht, wie sie abgeschlossen wurde, etwa „Erledigt: Sam hat es am Dienstag unterschrieben“.

Über dem Entwurf steht in einer dezenten Zeile, aus welcher Nachricht er stammt, mit dem Logo des jeweiligen Dienstes. Tippe darauf, um den Thread zu lesen. Beim Entwurf wird das Logo des Ziels angezeigt. So siehst du sofort, ob es eine Slack-Antwort oder eine E-Mail ist.

Wenn der Entwurf auf dem Beitrag einer anderen Person an anderer Stelle basiert, etwa einem Vorschlag eines Teammitglieds in Slack, steht das in einer Zeile, etwa „Basierend auf Sam in #ops“. Tippe darauf, um die Nachricht zu lesen.

Ein Chat (Slack, WhatsApp, Telegram, Intercom usw.) wird als eine Unterhaltung angezeigt, von der ältesten Nachricht an: erst die Nachrichten vor der Nachricht, um die es bei der Aufgabe geht, dann die Antworten darauf. In WhatsApp, Telegram oder Signal stehen deine Nachrichten wie in der App rechts. Die Nachricht der Aufgabe ist mit „Diese Aufgabe“ markiert und wird in der Ansicht geöffnet. Mit **Frühere Nachrichten anzeigen** werden ältere Nachrichten eingeblendet. Bei einer E-Mail ist der übrige Thread ober- und unterhalb davon eingeklappt.

Mit **In Gmail öffnen** wird die E-Mail im Gmail-Konto geöffnet, an das sie gesendet wurde. Unter Android wird sie in der Gmail-App geöffnet, wenn du diese installiert hast.

Unter **Details** einer E-Mail stehen nur Angaben, die nicht bereits in der Kopfzeile enthalten sind, etwa vollständige Cc-Adressen, Bcc oder eine andere Antwortadresse. Gibt es nichts hinzuzufügen, wird nichts angezeigt.

Bei einer Antwort in einem Slack-Thread wird auch angezeigt, was vor Beginn des Threads gesagt wurde. Über den Link einer Aufgabe zur zugehörigen Nachricht kannst du sie ebenfalls hier öffnen. Unten findest du **In Slack öffnen**.

Unter **Details** stehen Name, Projekt und Bereich (tippe auf einen Eintrag, um ihn zu ändern), deine letzte Notiz und das Ergebnis eines Coding-Agenten. Über den Titel wird der Chat geöffnet. Eine erledigte Aufgabe bleibt kompakt. Die Nachricht, aus der sie entstanden ist, steht unter **Details**.

Bei einer Aufgabe mit dem Hinweis „Wartet auf“ wird deine letzte Nachricht an die Person verlinkt, auf die du wartest: „E-Mail an Pat · Di“.

## Aufgabe selbst erstellen

Mit **Neue Aufgabe** (am Computer unter **Suchen**, auf dem Handy über **+** oder mit `N`) erstellst du eine Aufgabe zu einem beliebigen Thema. Beim Erstellen wird nichts gesendet. Wenn du weder **Arbeit** noch **Privat** auswählst, wird die Aufgabe anhand der beteiligten Personen und des Themas dem passenden Bereich zugeordnet. Die E-Mail, auf die sie sich bezieht, wird ebenfalls gefunden, auch wenn sie schon älter ist.

- **Fällig**: Gib einen Tag oder eine Uhrzeit ein, zum Beispiel „morgen“, „nächsten Fr“, „3 Nov“, „14 Uhr“ oder „in 2 Stunden“. Das geht auch in deiner Sprache. Über das Kalendersymbol findest du schnelle Vorschläge und **Datum wählen**.
- **Wiederholt sich**: Die Aufgabe kommt regelmäßig wieder. Siehe [Wiederkehrende Aufgaben](recurring.md).
- **Person**: Verknüpfe bis zu 5 Personen oder Unternehmen, um die es geht.
- Nachrichtensymbol: Hänge die Nachricht an, um die es geht: eine E-Mail, Slack-, Teams-, WhatsApp-, Telegram- oder andere Nachricht, auf die The Machine zugreifen kann. Suche nach Text oder Absender. Bei jedem Ergebnis siehst du, woher es stammt, wer es gesendet hat und wann.
- **Dateien**: Tippe auf die Büroklammer, füge einen Screenshot ein oder zieh Dateien auf das Formular. Auf dem Handy kannst du mit der Kamera daneben ein Foto aufnehmen. Wie im Chat sind bis zu 5 Dateien möglich (siehe [Dateien hinzufügen](card-chat.md#add-files)). Mit × entfernst du eine Datei wieder.

Die Dateien bleiben bei der Aufgabe, und The Machine liest sie, während sie daran arbeitet. Dateien allein reichen aus: Aus einer PDF- oder Textdatei erstellt sie die Aufgabe. Ein Foto wird als kleines Bild angezeigt. Tippe darauf, um es in voller Größe zu sehen.
