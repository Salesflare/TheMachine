---
title: Routinen
area: cards
summary: Arbeit, die deine Machine regelmäßig selbst erledigt, zum Beispiel jeden Montag deine offenen Deals zusammenfassen. Sie liest nur.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, reorder.py, reorder_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js, dashboard/todos-reorder.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours, reorder, reorders, buy again, running low, order confirmation, shopify
translated: b5704836b00227a5
---
## Eine Routine erstellen

Öffne **Routinen** in der Seitenleiste und beschreibe in einer Zeile, was sie wann tun soll: „jeden Montag um 9 Uhr meine offenen Deals zusammenfassen“ oder „jeden Werktagmorgen die E-Mails auflisten, auf die ich noch antworten muss“. Tippe dann auf **Hinzufügen**.

Ohne Zeitangabe wird die Routine um 8:00 Uhr ausgeführt. Maßgeblich ist die Uhr deiner Machine. Beim ersten Durchlauf erhält sie einen kurzen Namen.

Mit **Hinzufügen** wird zuerst ein Probelauf ausgeführt. So siehst du, was dabei herauskommt, bevor du die Routine übernimmst. Dabei wird nichts gesendet oder gespeichert. Mit **Hinzufügen** wird sie anschließend regelmäßig ausgeführt, **Ändern** probiert andere Formulierungen oder einen neuen Namen aus und **Abbrechen** verwirft sie.

## Vorlagen

Unter **Vorlagen** am Ende von Routinen kannst du mit **Hinzufügen** eine fertige Routine aktivieren. Sie wird sofort einmal ausgeführt und danach jeden Morgen um 7:30 Uhr (Spam aufräumen jede Stunde, Gebrauchte Fundstücke alle 3 Stunden, Abos und Testphasen einmal im Monat). Auf der Karte stehen ihre Formulierungen wie bei jeder Routine. Mit **Bearbeiten** kannst du sie oder ihren Namen ändern.

Wenn viele Newsletter eingehen und Newsletter aufräumen deaktiviert ist (mindestens 25 in einer Woche von mindestens 5 Absendern), erscheint über deinen Aufgaben eine Zeile. Sie zeigt, wie viele Newsletter eingegangen sind und was die Routine tun würde. Dort gibt es die Optionen **Einschalten** und **Nein danke**.

Spam aufräumen wird auf dieselbe Weise vorgeschlagen, wenn du in einer Woche mindestens 5 E-Mails von Hand als Spam markiert hast. Mit **Einschalten** wird die Routine wie hier mit **Hinzufügen** hinzugefügt. Bei **Nein danke** wird sie nicht noch einmal vorgeschlagen. Eine Vorlage, die du schon einmal hattest, wird ebenfalls nie wieder vorgeschlagen.

**Newsletter aufräumen** erstellt pro Bereich (Arbeit und Privat) eine Aufgabe mit den Newslettern des letzten Tages. Für jeden gibt es die Optionen **Behalten** und **Abmelden**. Zum Abmelden wird der Ein-Klick-Link der Mailingliste verwendet oder, wenn das Senden aktiviert ist, eine Abmelde-E-Mail von deiner Adresse aus verschickt. Andernfalls meldet The Machine dich auf der Seite der Mailingliste in ihrem eigenen Browser ab. Wenn du dich dort anmelden, ein Captcha lösen oder eine Auswahl treffen musst, liegt das bei dir. In der Zeile steht warum, mit **Abmeldeseite öffnen**.

Quittungen, Bestellungen und Zahlungsbenachrichtigungen werden ausgelassen. E-Mails, die über eine Gruppenadresse wie eine Google Group eingegangen sind, werden unter dem Namen des Absenders aufgeführt. Du wirst niemals aus der Gruppe abgemeldet. Wenn der Absender keine eigene Abmeldemöglichkeit anbietet, steht in der Zeile **Selbst abmelden**.

**Spam aufräumen** erstellt pro Bereich eine Aufgabe mit E-Mails unbekannter Absender, die wie Spam aussehen. Für jede gibt es die Optionen **Spam** und **Kein Spam**. Outlook verschiebt Spam in den Junk-Ordner, Gmail markiert ihn als Spam. Die Routine prüft jede Stunde, daher ist Spam normalerweise schon dort, bevor du nachsiehst. Solange die Aufgabe offen ist, werden neue Spam-Nachrichten hinzugefügt.

Bei einer schreibgeschützten Gmail-Verbindung, wie auf einer gehosteten Machine, können E-Mails nicht als Spam markiert werden. Dort führt **Spam** zu einem Link, mit dem du die E-Mail in Gmail als Spam markieren kannst. The Machine merkt sich den Absender als Spam. Wenn kein E-Mail-Konto verbunden ist, wird in der Vorlage statt **Hinzufügen** die Option **Mail verbinden** angezeigt.

Unbekannt bedeutet, dass du der Person noch nie geschrieben hast. Ein „Re:“ zählt nur dann als Unterhaltung, wenn du in diesem Thread selbst geschrieben hast. Wenn eine E-Mail von einem Absender, den du in der Aufgabe oder deinem Postfach als Spam markiert hast, wieder durchkommt, erscheint sie in der nächsten Aufgabe mit dem Hinweis **Schon einmal als Spam markiert**. E-Mails, die du selbst in den Spam verschoben hast, helfen der Routine außerdem dabei, ähnliche Nachrichten zu erkennen.

Es ändert sich nichts, bis du es in der Aufgabe bestätigst. Tippe auf einen Absender, um die E-Mail zuerst zu lesen: Sie bleibt ungelesen und es ändert sich nichts. Bei Spam aufräumen werden Bilder aus dem Internet nicht geladen, damit der Absender nicht sieht, dass die E-Mail geöffnet wurde. Zu Absendern, über die du bereits entschieden hast, wirst du nicht erneut gefragt. An Tagen ohne Newsletter oder Spam wird keine Aufgabe erstellt. Diese Aufgaben lösen nie eine Benachrichtigung aus.

Sobald du zu allen Absendern eine Entscheidung getroffen hast, zeigt die Aufgabe an, dass sie abgeschlossen ist, und bietet **Als erledigt markieren** an.

**Tägliche Zusammenfassung** wählt einmal täglich in einer Aufgabe die wenigen Newsletter-Inhalte aus, die deine Zeit wert sind. Zu jedem Inhalt steht in einer Zeile, warum er für dich wichtig ist. Tippe darauf, um die E-Mail zu lesen, oder nutze **In deiner Mail öffnen**. Es werden nur Newsletter berücksichtigt, niemals E-Mails von Personen, Quittungen oder Absender, von denen du dich abgemeldet hast. Bereits gelesene E-Mails werden ebenfalls ausgeschlossen. Wenn nichts besonders auffällt, wird keine Aufgabe erstellt.

Die Routine lernt, was dich interessiert, anhand dessen, was du öffnest, mit einem Stern markierst oder ungelesen archivierst, sowie über **Mehr davon** und **Weniger davon** bei jeder Auswahl. Die Themen, nach denen sie auswählt, findest du auf der Routinenkarte unter **Mehr zu** und **Weniger zu**. Entferne ein Thema mit × oder füge eigene hinzu. Gestrichelte Themen hat die Routine selbst gelernt. Eine neue Zusammenfassung ersetzt die offene. Sie löst nie eine Benachrichtigung aus.

Die Routine liest nur Absender, Betreff und Anfang jedes neuen Newsletters und stellt deiner KI dazu eine kurze Frage, mit einem Tageslimit, damit die Kosten niedrig bleiben. Mit **Zeitpunkt ändern** legst du die Uhrzeit fest. Sobald du ihre Formulierungen änderst, läuft sie wie jede andere Routine mit deinen Formulierungen.

**Geburtstage** erstellt für jeden engen Kontakt, der heute Geburtstag hat, eine Aufgabe. Dazu zählen Personen, denen du selbst schreibst, etwa Freunde, Familie und regelmäßige Kontakte. Für jede Person wird eine kurze Glückwunschnachricht in der Sprache der Person entworfen, und zwar dort, wo du normalerweise mit ihr kommunizierst, zum Beispiel in ihrem WhatsApp-Chat oder deinem E-Mail-Thread. Die Nachricht wird erst gesendet, wenn du sie selbst abschickst. An Tagen ohne Geburtstage wird keine Aufgabe erstellt.

Geburtstage stammen aus deinen Kalendern (Geburtstagsereignisse und der Kalender „Geburtstage“ von Google, die jeden Morgen ausgelesen werden, auch wenn sie nicht synchronisiert sind, sowie der Kalender „Geburtstage“ von Outlook), deinen Google-Kontakten auf einer selbst gehosteten Machine und einem Datumsfeld namens Birthday bei einer Person im Graph. Wenn in keiner dieser Quellen ein Geburtstag gespeichert ist, steht im Ergebnis **Noch keine Geburtstage bekannt** sowie eine Erklärung, wie du welche hinzufügst.

**Geburtstage aus Facebook importieren**: Sobald Geburtstage aktiviert ist, bietet eine Aufgabe an, die Geburtstagsseite von Facebook auszulesen. Tippe auf **Importieren**. The Machine öffnet die Seite in ihrem Browser, scrollt, bis alle Monate geladen sind, und liest den Namen und Geburtstag jedes Freundes aus. Anschließend zeigt sie, wie viele Geburtstage gefunden wurden und wer anhand von Vor- und Nachnamen Personen in deinem Graph zugeordnet werden konnte. Namen, die mehreren Personen zugeordnet werden können, werden übersprungen und aufgelistet.

Nur mit **Speichern** werden die Daten auf der Seite der jeweiligen Person gespeichert: der Geburtstag und das Facebook-Profilbild, wenn die Person noch kein Foto hat. Ein Geburtstag oder Bild, das du dort festgelegt hast, bleibt erhalten. Ein bereits vorhandenes Foto wird nie ersetzt. Auf Facebook wird nichts gespeichert.

Die Daten werden nicht automatisch erneut ausgelesen. Das geht über **Erneut importieren** in der Aufgabe. Der Browser muss bei Facebook angemeldet sein. Ist das nicht der Fall, tippe in der Aufgabe auf **Bei Facebook anmelden** und melde dich dort an. Sobald du angemeldet bist, liest die Routine die Seite selbst aus. The Machine meldet dich nicht an.

Freunde, die in deinem Graph nicht zu finden sind, werden gezählt und mit einigen Namen aufgeführt. Mit **… als persönliche Kontakte hinzufügen** kannst du sie alle auf einmal hinzufügen, auch nach dem Speichern: jeweils mit Namen und Geburtstag, niemals geteilt mit einer Work Fleet. Namen von Personen, die bereits in deinem Graph stehen oder die du dauerhaft gelöscht hast, werden übersprungen. Geburtstags-Erinnerungen gibt es weiterhin nur für Personen, denen du schreibst.

Mit **Rückgängig** in der Aufgabe werden genau diese Personen wieder entfernt, auch nach **Erneut importieren**.

**Abos und Testphasen** liest einmal im Monat deine Quittungen, Rechnungen und Verlängerungsbenachrichtigungen aus und fasst deine Abos in einer Aufgabe zusammen: die Kosten, den nächsten Abbuchungstermin und einen Hinweis, wenn eine Testphase endet oder der Preis steigt. Aufgeführt werden nur Abos, bei denen sich die Routine sicher ist. Wenn nichts gefunden wird, wird keine Aufgabe erstellt.

Wähle für jedes Abo **Behalten** oder **Kündigen**. Bei einem behaltenen Abo wird nicht erneut nachgefragt, es sei denn, der Preis ändert sich. Mit **Kündigen** erhältst du einen Link zur Kündigungsseite oder einen Entwurf mit der Bitte um Kündigung. Der Entwurf wird erst gesendet, wenn du ihn selbst abschickst. Zwischen den monatlichen Durchläufen prüft die Routine täglich, ob eine Testphase oder Verlängerung innerhalb der nächsten 7 Tage abgerechnet wird. In diesem Fall erstellt sie eine Aufgabe.

**In Kontakt bleiben** erinnert dich ab und zu daran, dich bei einer nahestehenden Person zu melden, aber nur, wenn es einen konkreten Anlass gibt. Wähle auf der Routinenkarte aus einer kurzen Liste von Personen aus, mit denen du selbst regelmäßig über Monate hinweg hin und her schreibst. Entferne jemanden mit ×.

Eine Erinnerung kommt nur, wenn du deutlich länger als sonst keinen Kontakt hattest und es etwas Konkretes zu sagen gibt: Neuigkeiten, die die Person geteilt hat, ein noch offenes Versprechen oder eine Nachricht, auf die du nie geantwortet hast. Es wird eine Aufgabe mit dem Grund und einer kurzen Nachricht erstellt, die in der Sprache der Person dort entworfen wird, wo du normalerweise mit ihr kommunizierst. Die Nachricht wird erst gesendet, wenn du sie selbst abschickst. Wenn es nichts zu sagen gibt, wird keine Aufgabe erstellt.

Die Routine sendet höchstens zwei Erinnerungen pro Woche und eine pro Person im Monat. Personen, mit denen du kürzlich gesprochen hast, werden nicht berücksichtigt. Mit **Nicht nötig** wird die Wartezeit für diese Person verlängert. Jedes Mal wird sie weiter verlängert. Die Routine löst nie eine Benachrichtigung aus und bleibt privat: Sie wird niemals mit einer Work Fleet geteilt.

**Gebrauchte Fundstücke** überwacht eine Suche auf einer Gebrauchtwarenplattform wie Marktplaats, Vinted, eBay oder Facebook Marketplace. Suche dort mit den gewünschten Filtern, kopiere die Adresse der Ergebnisse und füge sie nach **Hinzufügen** ein. Wenn du möchtest, kannst du Filter in eigenen Worten ergänzen, zum Beispiel „unter 300, höchstens 30 km entfernt, nichts ‚für Ersatzteile‘“. Jede Suche ist eine eigene Routine. Füge sie also für die nächste Suche erneut hinzu.

Alle 3 Stunden öffnet die Routine die Suche im eigenen Browser von The Machine und sucht nach Angeboten, die sie noch nicht gesehen hat. Preis, Entfernung und ausgeschlossene Begriffe werden zuerst mit einfachem Code geprüft.

Jedes neue Angebot, das die Prüfung besteht, wird geöffnet. Deine KI beurteilt anhand des Fotos und der Beschreibung den Zustand sowie anhand der Rezensionen, Bewertung und des Alters des Kontos den Verkäufer. Die guten Angebote kommen in eine gemeinsame Aufgabe. Für jedes werden Foto, Titel, Preis und ein kurzes Urteil angezeigt. Tippe auf ein Angebot, um es im Browser von The Machine zu öffnen.

Solange die Aufgabe offen ist, werden neue Fundstücke oben hinzugefügt, der Zähler wird erhöht und du wirst erneut benachrichtigt, denn gute Angebote sind schnell weg. Wenn du die Aufgabe als erledigt markierst, beginnt für das nächste Fundstück eine neue Aufgabe. Ein Durchlauf ohne gute Angebote ändert nichts.

Die Routine geht schonend mit Websites um und hält die Kosten niedrig: pro Durchlauf wird die Suche einmal ausgelesen, höchstens 6 Angebote werden mit einer Pause dazwischen geöffnet und pro Tag werden höchstens 40 Angebote über alle deine Suchen hinweg geprüft. Bei jeder Prüfung wird deiner KI eine kurze Frage mit einem Foto gestellt. Beim ersten Durchlauf werden nur die wenigen neuesten Angebote geprüft. Die übrigen gelten danach als gesehen, sodass spätere Durchläufe nur Neues anzeigen.

Wenn die Website dich auffordert, dich anzumelden, eine Roboterprüfung anzeigt oder das Auslesen verhindert, weist dich eine Aufgabe darauf hin. Mit **Öffnen** kannst du die Seite im Browser von The Machine ansehen. Melde dich dort selbst an oder löse die Prüfung. Beim nächsten Durchlauf wird die Seite erneut ausgelesen. The Machine meldet dich nicht an und löst keine Prüfungen für dich. Sie kontaktiert auch keine Verkäufer, gibt keine Gebote ab und kauft nichts.

Mit **Suche ändern** auf der Routinenkarte kannst du eine neue Adresse oder Filter eingeben. Mit **Zeitpunkt ändern** kannst du einen anderen Rhythmus festlegen, zum Beispiel „alle 6 Stunden“.

**Nachbestellungen** liest Bestellbestätigungen von Online-Shops in deinen E-Mails und erkennt, was du immer wieder kaufst, zum Beispiel Kaffee, Tierfutter oder Vitamine. Wenn ein weiterer Kauf wahrscheinlich bald ansteht, erstellt die Routine eine Aufgabe mit dem Artikel, dem Geschäft, dem letzten Preis und dem letzten Kaufdatum. Mit **Im Store öffnen** gelangst du zur Produktseite und kannst den Artikel selbst kaufen. Es wird nichts für dich gekauft.

Mindestens drei Bestellungen desselben Artikels in regelmäßigem Abstand sind nötig. Bei einem Einzelkauf oder ungewöhnlich langen Abständen wird keine Aufgabe erstellt. Derzeit liest die Routine Bestellungen von Shops, die Shopify verwenden. Deine KI liest nur neue Bestell-E-Mails dieser Shops und stellt pro Durchlauf eine kurze Frage dazu. Diese Aufgaben lösen nie eine Benachrichtigung aus. Wenn du den Artikel erneut bestellst, wird die offene Aufgabe geschlossen.

Solange eine Vorlagenroutine ihre ursprünglichen Formulierungen verwendet, läuft sie mit eigenem Code und ohne deinen KI-Plan (Spam aufräumen listet neue E-Mails von unbekannten Absendern zuerst mit Code auf und stellt deiner KI nur dann eine kurze Frage, wenn welche vorliegen. In Kontakt bleiben fragt nur nach den ein oder zwei ausgewählten Personen). Ein neuer Name ändert daran nichts. Sobald du die Formulierungen änderst, läuft die Routine wie jede andere mit deinen Formulierungen.

Newsletter aufräumen und Spam aufräumen erstellen weiterhin dieselbe Aufgabe mit einer Auswahl für jede E-Mail. Eine bearbeitete Routine für Geburtstage zeigt ihr Ergebnis und höchstens einen Entwurf, nicht für jede Person eine eigene Aufgabe. Mit **Zurück zur Vorlage** in **Bearbeiten** stellst du die ursprünglichen Formulierungen wieder her.

## Was eine Routine tut

Zur festgelegten Zeit liest deine Machine die benötigten Daten aus, zum Beispiel deine Nachrichten, Termine und den Graph, und zeigt das Ergebnis auf der Seite Routinen an. Für jedes Ergebnis wird **Bereit**, **Nichts Neues** (mit Begründung) oder **Hat nicht geklappt** (mit Begründung) angezeigt. Ein Durchlauf, der ohne Ergebnis endet, zählt als fehlgeschlagen und niemals als erledigt.

Routinen lesen nur: deine Nachrichten, Webseiten, GitHub und Websites wie X im Browser. Sie senden nichts, antworten nicht, posten nichts und ändern nichts. Sie öffnen Seiten, die sie in den ausgelesenen Inhalten oder einer Suche gefunden haben, sowie gewöhnliche Webadressen und bekannte Websites. Sie öffnen niemals eine Adresse, die eigens erstellt wurde, um ausgelesene Inhalte zu übermitteln. Nur eine Vorlage kann E-Mails ändern, und auch dann nur, was du in der Aufgabe bestätigst.

Wenn eine Routine mit einem Beitrag oder einer Nachricht enden soll, führt sie alles bis zu diesem Schritt aus und zeigt den Entwurf an, zum Beispiel **Würde auf X posten:**. Nach einem echten Durchlauf erhältst du dafür eine Aufgabe zur Freigabe. Bei einem Probelauf wird der Entwurf nur angezeigt. Der Name der Aufgabe beschreibt, worum es geht und wo der Inhalt veröffentlicht wird. Die Schaltfläche benennt den Schritt, zum Beispiel **Posten**. Darunter öffnet **Von deiner Routine** die Routine.

Die Aufgabe wird im Bereich des Kontos erstellt, von dem aus sie veröffentlicht werden soll, zum Beispiel unter Arbeit für das X-Konto deines Unternehmens. Du musst sie also nie verschieben.

Ein Durchlauf kann den aktivierten [Skills](skills.md) folgen, ausgewählt danach, was die Routine tut. Dabei werden nur passende Skills vollständig gelesen. Das Ergebnis führt sie unter **Verwendet:** auf. Ein Skill lässt eine Routine niemals etwas senden oder ändern.

Deine Routinen findest du unter **Deine Routinen**, unterhalb aller Vorschläge. Ein langes Ergebnis wird auf eine kurze Vorschau eingeklappt. Mit **Mehr anzeigen** oder durch Tippen darauf öffnest du es.

Jeder Durchlauf kennt das letzte Ergebnis und kann deshalb angeben, was sich seitdem geändert hat.

Nach einem erfolgreichen Durchlauf kann deine Machine selbst eine Anleitung für gleichbleibende Leseaufgaben erstellen, zum Beispiel dafür, welche E-Mails oder GitHub-Änderungen geprüft werden sollen. Bei den nächsten Durchläufen werden diese zuerst mit einfachem Code ausgelesen. Die KI wählt dann nur aus, was wichtig ist, und formuliert es mit weniger Tokens. Eine Anleitung liest nur. Wenn sie nicht mehr funktioniert, liest die Routine die Daten selbst aus und korrigiert die Anleitung. Sie wird im Menü ⋯ unter **Erweitert: Skriptschritte** angezeigt.

## Verpasste Tage

Wenn deine Machine ausgeschaltet oder beschäftigt war, werden verpasste Durchläufe nicht nachgeholt. Es wird nur der neueste Durchlauf einmal ausgeführt. Jeder Kalendertag wird nur einmal ausgeführt, auch nach einem Neustart.

Routinen laufen nacheinander und warten, wenn das Kontingent deines KI-Plans knapp ist, wie alle Hintergrundaufgaben. Mit **Jetzt ausführen** startest du die Routine sofort. Sobald das Ergebnis fertig ist, erscheint es auf der Karte.

## Ändern oder beenden

Diese Optionen findest du im Menü ⋯ der Routine. Mit **Bearbeiten** kannst du ihren Namen ändern und was sie tut. Der Ausführungszeitpunkt und die bisherigen Ergebnisse bleiben erhalten. Mit **Zeitpunkt ändern** kannst du in eigenen Worten einen neuen Rhythmus festlegen, zum Beispiel „jeden Werktag um 8 Uhr“. Bei beiden Optionen gibt es **Speichern** und **Abbrechen**. Am Computer kannst du auch mit Esc oder einem Klick außerhalb des Fensters abbrechen.

Mit **Ausprobieren** in **Bearbeiten** wird die Routine einmal mit den neuen Formulierungen ausgeführt und das Ergebnis dort angezeigt. Bis du auf **Speichern** tippst, bleibt die Routine unverändert.

Mit **Pausieren** werden die Durchläufe angehalten, bis du auf der Karte **Fortsetzen** wählst. Pausierte Routinen findest du unter **Pausiert** unterhalb deiner Routinen. Während der Pause verpasste Durchläufe werden später nicht ausgeführt. Mit **Stoppen** beendest du eine Routine endgültig.

Es können bis zu 20 Routinen angelegt werden, einschließlich pausierter. Beende eine Routine, um eine weitere hinzuzufügen.

Wenn du bei einer Aufgabe der Routine **Änderungen anfragen** nutzt oder in ihrem Chat schreibst und deine Nachricht für jeden Durchlauf gelten soll, zum Beispiel „Verwende niemals Emojis“, bietet die Aufgabe **Auch die Routine ändern** an. Die Option erscheint in der Aufgabe und im Chat unter der Antwort. Sie zeigt, was sich in den Formulierungen der Routine ändern würde. Die Routine wird erst geändert, wenn du auf **Ändern** tippst. Mit **So lassen** bleibt alles wie bisher. Bei einer Korrektur, die nur diesen Entwurf betrifft, wird die Option nicht angeboten.

## Erweitert: Skriptschritte

Du brauchst kein Skript: Beschreibe in eigenen Worten, was eine Routine tun soll, und deine Machine findet den Rest selbst heraus.

Für erfahrene Nutzer kann eine Routine auch eigene Befehle auf deiner Machine ausführen. Wähle dazu im Menü ⋯ **Erweitert: Skriptschritte**. **Bearbeiten** wird erst angezeigt, wenn die Routine Skriptschritte enthält. Mit **Daten holen** wird zuerst ein Befehl ausgeführt, und zwar in seinem Ordner (oder, wenn dieser leer ist, in deinem Home-Ordner) und höchstens für die angegebene Anzahl Sekunden. Die Ausgabe wird an den Durchlauf weitergegeben. Ohne weitere Formulierungen wird die Ausgabe zum Ergebnis.

Mit **Prüfung** wird das Ergebnis nach dem Durchlauf als Eingabe verwendet. Wenn der Befehl mit einem Fehler endet, zeigt der Durchlauf **Hat nicht geklappt** sowie die Meldung der Prüfung an. Ein fehlgeschlagener Daten-holen-Befehl wird genauso angezeigt.

Ein Befehl besteht aus einer Zeile und wird ohne Shell ausgeführt: Es sind keine Pipes oder Variablen möglich. Skriptschritte gehören dir und werden nur in deinem Dashboard eingerichtet. Bei einem Probelauf und mit **Ausprobieren** wird auch der Daten-holen-Befehl ausgeführt. Darauf wird hingewiesen. Trotzdem wird nichts gesendet oder gespeichert. Eine Routine sendet nie etwas, daher sollte ein Skriptschritt nur Daten lesen.

## Aus deinen OpenClaw-Jobs

Wenn du früher geplante Jobs in OpenClaw erstellt hast, liest deine Machine sie aus, ändert sie aber nie. Passende Jobs werden unter **Vorgeschlagen** als Routinen angeboten. Jeder Job wurde einmal ausgeführt, damit du ein echtes Ergebnis siehst.

Korrekturen am Job bleiben erhalten. Gesendete oder veröffentlichte Inhalte werden ausgelassen. Wenn ein Job ein Skript ausgeführt oder die Ergebnisse eines Skript-Jobs ausgelesen hat, wird das Skript als Daten-holen-Schritt übernommen. Mit **Hinzufügen** wird daraus eine Routine. Mit **Nein danke** wird der Job nicht noch einmal vorgeschlagen. Wenn ein Job dich an etwas erinnert hat, das du erledigen solltest, wird stattdessen unter Aufgaben eine wiederkehrende Aufgabe angeboten.

Bevor du einen Vorschlag hinzufügst, kannst du ihn über **Bearbeiten** und **Zeitpunkt ändern** im Menü ⋯ wie jede andere Routine ändern. Mit **Erneut ausführen** wird der Job sofort mit den aktuellen Formulierungen ausgeführt, damit du neuere Ergebnisse siehst, zum Beispiel nach einem ruhigen Wochenende. Er liest nur, wird pro Tippen einmal ausgeführt und ersetzt das alte Ergebnis durch das neue.

Gleichzeitig werden höchstens drei Vorschläge angezeigt. Nach einer Woche erfolgreicher Durchläufe fragt die Routine **Den alten OpenClaw-Job ausschalten?**. Der Job wird erst ausgeschaltet, wenn du auf **Ausschalten** tippst. Du kannst ihn in OpenClaw wieder einschalten. Mit **Behalten** laufen beide weiter.

## Aus deinen Aktivitäten

Deine Machine erkennt auch Arbeit, die du regelmäßig erledigst, und schlägt sie unter **Vorgeschlagen** als Routinen vor, auch ohne OpenClaw. Sie achtet auf Folgendes:

- dieselbe Anfrage mindestens dreimal hintereinander, zum Beispiel „die offenen Support-Tickets zusammenfassen“ jeden Montag;
- eine E-Mail, die du regelmäßig verschickst, zum Beispiel einen wöchentlichen Bericht an dein Team;
- Newsletter und Aktualisierungs-E-Mails, die jede Woche wieder eingehen;
- einen aktiven Slack-Kanal, in den andere jede Woche schreiben;
- E-Mails, die du einzeln immer an dieselbe Person weiterleitest, zum Beispiel Schul- und Vereins-E-Mails an deine Partnerin oder deinen Partner. Eine wöchentliche Zusammenfassung erspart dir das Weiterleiten;
- dieselbe Anfrage, die du regelmäßig beantwortest, zum Beispiel eine monatliche Freigabe für dieselbe Person.

Jeder Vorschlag nennt, was deine Machine beobachtet hat, zum Beispiel „4-mal hintereinander angefragt“ oder „6 E-Mails in 3 Wochen an Sam weitergeleitet“. Der Vorschlag wurde einmal ausgeführt, damit du ein echtes Ergebnis siehst. Denk zum Beispiel an eine Team-Zusammenfassung, eine kurze Vorbereitung auf einen wöchentlichen Anruf, eine Support- oder Entwicklungsübersicht, einen Überblick über deine Kennzahlen oder eine Zusammenfassung der Newsletter, die du erhältst.

Vorgeschlagen werden nur Routinen, die für dich spezifisch und eindeutig nützlich sind: Eine Nachrichtenübersicht basiert nur auf deinen eigenen Newslettern und ist niemals allgemein gehalten. Wenn nichts Passendes dabei ist, gibt es keinen Vorschlag.

Sie sucht höchstens einmal am Tag und bringt höchstens einen neuen Vorschlag pro Woche, ohne Benachrichtigung. Mit **Nein danke** wird der Vorschlag nicht noch einmal angezeigt. Weiterleitungen und Antworten bleiben bei dem Konto, von dem aus sie gesendet wurden. Arbeit und Privat werden also nicht vermischt. Alles bleibt auf deiner Machine. Eine Aufgabe, die du regelmäßig abschließt, wird stattdessen als wiederkehrende Aufgabe angeboten.

## Routinen und wiederkehrende Aufgaben

Eine [wiederkehrende Aufgabe](recurring.md) erinnert dich daran, etwas zu erledigen. Eine Routine ist Arbeit, die deine Machine selbst erledigt und dir anschließend zeigt. Nutze eine wiederkehrende Aufgabe für „am Ersten die Miete zahlen“ und eine Routine für „jeden Freitag die Deals nennen, bei denen es still geworden ist“.
