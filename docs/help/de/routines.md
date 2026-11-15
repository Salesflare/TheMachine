---
title: Routinen
area: cards
summary: Arbeit, die deine Machine selbstständig nach einem Zeitplan erledigt, zum Beispiel eine Zusammenfassung deiner offenen Deals am Montag. Sie liest nur.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in
translated: 2be351a9cef42215
---
## Eine Routine erstellen

Öffne **Routinen** in der Seitenleiste und beschreibe in einer Zeile, was sie tun und wann sie es tun soll: „jeden Montag um 9 Uhr meine offenen Deals zusammenfassen“ oder „jeden Morgen unter der Woche die E-Mails auflisten, auf die ich noch antworten muss“. Tippe dann auf **Hinzufügen**.

Wenn du keine Uhrzeit angibst, wird die Routine um 8:00 Uhr ausgeführt. Maßgeblich ist die Uhr deiner Machine. Beim ersten Durchlauf bekommt sie einen kurzen Namen.

Mit **Hinzufügen** wird zuerst ein Testlauf ausgeführt. So siehst du, was dabei herauskommt, bevor du die Routine übernimmst. Es wird nichts gesendet oder gespeichert. Mit **Hinzufügen** wird sie anschließend nach ihrem Zeitplan ausgeführt, mit **Ändern** kannst du andere Formulierungen oder einen neuen Namen ausprobieren und mit **Abbrechen** verwirfst du sie.

## Vorlagen

Unter **Vorlagen** unten auf der Seite „Routinen“ kannst du mit **Hinzufügen** eine fertige Routine aktivieren. Sie wird sofort einmal ausgeführt und danach jeden Morgen um 7:30 Uhr. Spam aufräumen läuft jede Stunde, Abos und Testphasen einmal im Monat. Auf der Karte steht ihre Formulierung wie bei jeder Routine. Mit **Bearbeiten** kannst du die Formulierung oder den Namen ändern.

Wenn viele Newsletter eingehen und Newsletter aufräumen deaktiviert ist, also mindestens 25 Newsletter von mindestens 5 Absendern in einer Woche, steht über deinen Aufgaben, wie viele eingegangen sind und was die Routine tun würde. Dort findest du auch **Einschalten** und **Nein danke**.

Spam aufräumen wird auf dieselbe Weise angeboten, wenn du in einer Woche mindestens 5 E-Mails von Hand in den Spam verschoben hast. **Einschalten** fügt die Routine hinzu, genau wie **Hinzufügen** hier. Mit **Nein danke** wird sie nicht noch einmal angeboten. Auch eine Vorlage, die du schon einmal hattest, wird nie wieder angeboten.

**Newsletter aufräumen** erstellt pro Bereich, Arbeit und Privat, eine Aufgabe mit den Newslettern des letzten Tages. Für jeden Newsletter kannst du **Behalten** oder **Abmelden** auswählen. Zum Abmelden wird der Ein-Klick-Link der Mailingliste verwendet oder eine Abmelde-E-Mail von deiner Adresse gesendet, wenn das Senden aktiviert ist. Andernfalls meldet The Machine dich auf der Seite der Mailingliste über ihren eigenen Browser ab. Wenn du dich dort anmelden, ein Captcha ausfüllen oder eine Auswahl treffen musst, bist du dafür zuständig. In der Zeile steht der Grund, zusammen mit **Abmeldeseite öffnen**.

Belege, Bestellungen und Zahlungsbenachrichtigungen werden ausgelassen. E-Mails, die über eine Gruppenadresse wie eine Google Group eingegangen sind, werden unter dem Namen der schreibenden Person aufgeführt. Du wirst dadurch nie von der Gruppe abgemeldet. Wenn der Absender keine eigene Abmeldung anbietet, steht in der Zeile **Selbst abmelden**.

**Spam aufräumen** erstellt pro Bereich eine Aufgabe mit E-Mails von unbekannten Absendern, die wie Spam aussehen. Für jede kannst du **Spam** oder **Kein Spam** auswählen. Outlook verschiebt Spam in den Junk-Ordner, Gmail markiert ihn als Spam. Die Routine prüft jede Stunde, sodass der Spam normalerweise schon erkannt ist, bevor du nachsiehst. Neuer Spam wird zur selben Aufgabe hinzugefügt, solange sie offen ist.

Bei Gmail-Konten mit Leseberechtigung, wie auf einer gehosteten Machine, können E-Mails nicht in den Spam-Ordner verschoben werden. Dort öffnet **Spam** einen Link, über den du die E-Mail in Gmail als Spam markieren kannst. The Machine merkt sich den Absender dann als Spam. Wenn kein E-Mail-Konto verbunden ist, wird bei der Vorlage statt **Hinzufügen** die Schaltfläche **Mail verbinden** angezeigt.

Unbekannt bedeutet, dass du der Person noch nie geschrieben hast. Ein „Re:“ zählt nur dann als Unterhaltung, wenn du in dem Thread selbst geschrieben hast. Wenn eine E-Mail von einem Absender, den du auf der Aufgabe oder in deinem Postfach als Spam markiert hast, wieder durchkommt, erscheint sie auf der nächsten Aufgabe mit dem Hinweis **Schon einmal als Spam markiert**. Auch E-Mails, die du selbst in den Spam verschoben hast, helfen der Routine, ähnliche E-Mails zu erkennen.

Es ändert sich nichts, bis du es auf der Aufgabe bestätigst. Tippe auf einen Absender, um die E-Mail zuerst zu lesen: Sie bleibt ungelesen und nichts ändert sich. Bei Spam aufräumen werden Bilder aus dem Internet nicht geladen, sodass der Absender nicht sieht, dass du die E-Mail geöffnet hast. Absender, über die du schon entschieden hast, werden nicht erneut abgefragt. An einem Tag ohne Newsletter oder Spam wird keine Aufgabe erstellt. Diese Aufgaben lösen nie eine Benachrichtigung aus.

Sobald du für alle Absender eine Entscheidung getroffen hast, ist die Aufgabe abgeschlossen und darauf erscheint **Als erledigt markieren**.

Mit **Tägliche Zusammenfassung** werden einmal am Tag die wenigen Newsletter-Beiträge ausgewählt, die deine Zeit wert sind. Sie erscheinen in einer Aufgabe. Zu jedem Beitrag steht in einer Zeile, warum er für dich wichtig ist. Tippe darauf, um die E-Mail zu lesen, oder wähle **In deiner Mail öffnen**. Es werden nur Newsletter berücksichtigt, keine E-Mails von Personen, Belege oder Absender, von denen du dich abgemeldet hast. Bereits gelesene E-Mails werden ebenfalls ausgelassen. Wenn nichts besonders interessant ist, wird keine Aufgabe erstellt.

Die Routine lernt, was dich interessiert, anhand der Inhalte, die du öffnest, markierst oder ungelesen archivierst, und anhand deiner Auswahl von **Mehr davon** oder **Weniger davon** bei den einzelnen Vorschlägen. Die Themen, nach denen sie sucht, stehen auf der Karte der Routine unter **Mehr zu** und **Weniger zu**. Tippe auf ×, um ein Thema zu entfernen, oder füge eigene Themen hinzu. Gestrichelte Themen hat die Routine selbst gelernt. Eine neue Zusammenfassung ersetzt die noch offene. Sie löst nie eine Benachrichtigung aus.

Die Routine liest nur den Absender, den Betreff und den Anfang jedes neuen Newsletters und stellt deiner KI dazu täglich höchstens eine kurze Frage, damit die Kosten niedrig bleiben. Mit **Zeitpunkt ändern** legst du die Uhrzeit fest. Sobald du die Formulierung änderst, wird die Routine wie jede andere mit deiner Formulierung ausgeführt.

Mit **Geburtstage** wird für jede enge Kontaktperson, die heute Geburtstag hat, eine Aufgabe erstellt. Dazu gehören Personen, denen du selbst schreibst, etwa Freunde, Familie und regelmäßige Kontakte. Zu jeder Person gibt es einen kurzen Gruß als Entwurf, und zwar dort, wo du normalerweise mit ihr schreibst, zum Beispiel in ihrem WhatsApp-Chat oder in deinem E-Mail-Thread. Der Gruß ist in ihrer Sprache verfasst und wird nur gesendet, wenn du ihn selbst abschickst. An Tagen ohne Geburtstage wird keine Aufgabe erstellt.

Geburtstage stammen aus deinen Kalendern: aus Geburtstagsereignissen von Google und dem Kalender „Geburtstage“, die jeden Morgen ausgelesen werden, auch wenn sie nicht synchronisiert sind, sowie aus dem Kalender „Geburtstage“ von Outlook. Sie stammen außerdem aus deinen Google-Kontakten auf einer selbst gehosteten Machine und aus einem Datumsfeld mit dem Namen Birthday bei einer Person im Graph. Wenn noch kein Geburtstag gefunden wurde, steht im Ergebnis **Noch keine Geburtstagsinfos** und wie du welche hinzufügen kannst.

**Geburtstage aus Facebook importieren**: Sobald Geburtstage aktiviert ist, wird dir auf einer Aufgabe angeboten, die Geburtstagsseite von Facebook auszulesen. Tippe auf **Importieren**. The Machine öffnet die Seite in ihrem Browser, scrollt, bis alle Monate geladen sind, und liest den Namen und Geburtstag jedes Freundes aus. Sie zeigt an, wie viele Geburtstage gefunden wurden und bei welchen Personen im Graph Vor- und Nachname übereinstimmen. Wenn mehrere Personen denselben Namen haben, wird der Name ausgelassen und in einer Liste angezeigt.

Nur mit **Speichern** werden die Geburtstage auf der jeweiligen Personenseite gespeichert. Dazu gehört auch das Profilbild von Facebook, wenn die Person noch kein Foto hat. Ein Geburtstag oder Bild, den oder das du dort festgelegt hast, bleibt bestehen. Ein vorhandenes Foto wird nie ersetzt. Auf Facebook wird nichts gespeichert.

Die Geburtstage werden nicht automatisch erneut ausgelesen. Das passiert erst, wenn du auf der Aufgabe **Erneut importieren** auswählst. Im Browser musst du bei Facebook angemeldet sein. Falls du noch nicht angemeldet bist, tippe auf der Aufgabe auf **Bei Facebook anmelden** und melde dich dort an. Sobald du angemeldet bist, liest die Routine die Seite automatisch aus. The Machine meldet dich nie selbst an.

Freunde, die niemandem in deinem Graph zugeordnet sind, werden gezählt und mit einigen Namen angezeigt. Mit **… als private Kontakte hinzufügen** kannst du sie alle auf einmal hinzufügen, auch nachdem du auf „Speichern“ getippt hast. Für jede Person werden Name und Geburtstag gespeichert. Diese Kontakte werden nie mit einer Work Fleet geteilt. Ein Name, der bereits zu einer Person in deinem Graph gehört, oder zu jemandem, den du dauerhaft gelöscht hast, wird ausgelassen. Erinnerungen an Geburtstage erhältst du weiterhin nur für Personen, denen du schreibst.

Mit **Rückgängig** auf der Aufgabe entfernst du genau diese Personen wieder, auch wenn du danach **Erneut importieren** auswählst.

**Abos und Testphasen** liest einmal im Monat deine Belege, Rechnungen und Verlängerungsbenachrichtigungen aus und fasst deine Abos in einer Aufgabe zusammen. Für jedes Abo siehst du die Kosten, den nächsten Abbuchungstermin und einen Hinweis, wenn eine Testphase endet oder der Preis steigt. Aufgeführt werden nur Abos, bei denen sich die Routine sicher ist. Wird nichts gefunden, wird keine Aufgabe erstellt.

Wähle für jedes Abo **Behalten** oder **Kündigen**. Bei einem Abo, das du behalten möchtest, wirst du nicht erneut gefragt, außer der Preis ändert sich. Mit **Kündigen** wird die Kündigungsseite des Anbieters geöffnet oder ein Entwurf erstellt, in dem du um die Kündigung bittest. Er wird nur gesendet, wenn du ihn selbst abschickst. Zwischen den monatlichen Durchläufen prüft die Routine täglich, ob eine Testphase oder Verlängerung innerhalb der nächsten 7 Tage ansteht. Dann wird eine Aufgabe erstellt.

**In Kontakt bleiben** erinnert dich von Zeit zu Zeit daran, dich bei einer Person zu melden, die dir nahesteht, aber nur, wenn es einen echten Grund dafür gibt. Wähle auf der Karte aus einer kurzen Liste von Personen aus, mit denen du selbst über Monate hinweg regelmäßig in beide Richtungen schreibst. Tippe auf ×, um jemanden zu entfernen.

Eine Erinnerung erhältst du nur, wenn du die Person deutlich länger als sonst nicht kontaktiert hast und es einen konkreten Gesprächsanlass gibt: Neuigkeiten, die sie geteilt hat, ein noch offenes Versprechen oder eine Nachricht, auf die du nie geantwortet hast. Die Aufgabe nennt den Grund und enthält einen kurzen Nachrichtenentwurf in der Sprache der Person, und zwar dort, wo du normalerweise mit ihr schreibst. Die Nachricht wird nur gesendet, wenn du sie selbst abschickst. Gibt es nichts zu sagen, wird keine Aufgabe erstellt.

Es werden höchstens zwei Erinnerungen pro Woche und eine pro Person im Monat gesendet. Personen, mit denen du vor Kurzem gesprochen hast, erhalten keine Erinnerung. Mit **Nicht nötig** wartet die Routine länger, bevor sie dich an diese Person erinnert. Bei jeder weiteren Auswahl wartet sie noch länger. Sie löst nie eine Benachrichtigung aus und bleibt privat. Sie wird nie mit einer Work Fleet geteilt.

Solange die Routine einer Vorlage die Formulierung der Vorlage beibehält, wird sie mit eigenem Code ausgeführt, ohne dein KI-Abo zu nutzen. Spam aufräumen listet zum Beispiel im Code zuerst neue E-Mails von unbekannten Absendern auf und stellt deiner KI nur dann eine kurze Frage, wenn solche E-Mails vorhanden sind. In Kontakt bleiben fragt nur nach den ein oder zwei ausgewählten Personen. Ein neuer Name ändert daran nichts. Sobald du die Formulierung änderst, wird die Routine wie jede andere mit deiner Formulierung ausgeführt.

Newsletter aufräumen und Spam aufräumen erstellen weiterhin dieselbe Art Aufgabe, mit einer Auswahl pro E-Mail. Eine bearbeitete Routine für Geburtstage zeigt ihr Ergebnis und höchstens einen Entwurf an, nicht für jede Person eine eigene Aufgabe. Mit **Zurück zur Vorlage** unter **Bearbeiten** stellst du die ursprüngliche Formulierung wieder her.

## Was eine Routine macht

Zum geplanten Zeitpunkt liest deine Machine die benötigten Inhalte aus, zum Beispiel deine Nachrichten, Termine und den Graph, und zeigt das Ergebnis auf der Seite „Routinen“ an. Zu jedem Ergebnis steht **Bereit**, **Nichts Neues** mit einer Erklärung oder **Hat nicht geklappt** mit einer Erklärung. Ein Durchlauf, der ohne Ergebnis endet, zählt als fehlgeschlagen und nie als erledigt.

Routinen lesen nur: deine Nachrichten, Webseiten, GitHub und Seiten wie X im Browser. Sie senden keine Nachrichten, antworten nicht, posten nichts und ändern nichts. Nur eine Vorlage kann E-Mails ändern, und auch dann nur, was du auf der zugehörigen Aufgabe bestätigst.

Wenn ein Routine-Durchlauf mit einem Beitrag oder einer Nachricht enden soll, führt die Routine alles bis zu diesem Schritt aus und zeigt den Entwurf an, zum Beispiel **Würde auf X posten:**. Nach einem echten Durchlauf erhältst du den Entwurf als Aufgabe, die du bestätigen kannst. Bei einem Testlauf wird er nur angezeigt. Der Name der Aufgabe beschreibt, worum es geht und wo der Beitrag veröffentlicht wird. Die Schaltfläche benennt den Schritt, zum Beispiel **Posten**. Unter der Aufgabe öffnet **Aus deiner Routine** die Routine.

Die Aufgabe erscheint zuerst im Bereich des Kontos, von dem aus sie gesendet wird, zum Beispiel unter „Arbeit“ für das X-Konto deines Unternehmens. Du musst sie daher nie verschieben.

Ein Durchlauf kann deine aktivierten [Skills](skills.md) verwenden, ausgewählt danach, was die Routine tut. Nur passende Skills werden vollständig gelesen. Im Ergebnis werden sie unter **Verwendet:** aufgeführt. Ein Skill lässt eine Routine nie etwas senden oder ändern.

Deine Routinen stehen unter **Deine Routinen**, unterhalb aller Vorschläge. Lange Ergebnisse werden zunächst als kurze Vorschau angezeigt. Mit **Mehr anzeigen** oder durch Tippen auf die Vorschau öffnest du das vollständige Ergebnis.

Jeder Durchlauf kennt das vorherige Ergebnis und kann dir sagen, was sich seitdem geändert hat.

Nach einem erfolgreichen Durchlauf kann deine Machine selbst ein Rezept für wiederkehrende Leseaufgaben erstellen, zum Beispiel dafür, welche E-Mails oder GitHub-Änderungen geprüft werden sollen. Bei den nächsten Durchläufen wird zuerst dieses Rezept in einfachem Code ausgeführt. Die KI wählt dann nur noch die wichtigen Inhalte aus und formuliert das Ergebnis. Dabei werden weniger Tokens verbraucht. Ein Rezept liest nur. Wenn es nicht mehr funktioniert, liest der Durchlauf die Inhalte selbst und repariert es. Das Rezept erscheint im Menü ⋯ unter **Erweitert: Skriptschritte**.

## Verpasste Tage

Wenn deine Machine ausgeschaltet oder ausgelastet war, werden verpasste Durchläufe nicht nachgeholt. Nur der neueste wird einmal ausgeführt. Jeder Kalendertag wird höchstens einmal ausgeführt, auch nach einem Neustart.

Routinen werden nacheinander ausgeführt und warten, wenn dein KI-Abo nur noch wenig Nutzung zulässt, wie bei allen Aufgaben im Hintergrund. Mit **Jetzt ausführen** wird die Routine sofort ausgeführt. Sobald das Ergebnis fertig ist, erscheint es auf der Karte.

## Routine ändern oder beenden

Die entsprechenden Optionen findest du im Menü ⋯ der Routine. Mit **Bearbeiten** änderst du den Namen und die Aufgabe. Der Zeitplan und die bisherigen Ergebnisse bleiben erhalten. Mit **Zeitpunkt ändern** legst du einen neuen Zeitplan in eigenen Worten fest, zum Beispiel „jeden Wochentag um 8 Uhr“. Für beides gibt es **Speichern** und **Abbrechen**. Am Computer kannst du auch mit Esc oder durch einen Klick außerhalb des Fensters abbrechen.

Unter **Bearbeiten** kannst du mit **Ausprobieren** die neue Formulierung einmal ausführen und das Ergebnis direkt dort ansehen. Die Routine bleibt unverändert, bis du auf **Speichern** tippst.

Mit **Pausieren** werden die Durchläufe angehalten, bis du auf der Karte **Fortsetzen** auswählst. Pausierte Routinen findest du unter **Pausiert**, unterhalb deiner Routinen. Während der Pause verpasste Durchläufe werden nicht nachgeholt. Mit **Stopp** beendest du eine Routine endgültig.

Es sind bis zu 20 Routinen möglich, einschließlich pausierter Routinen. Beende eine Routine, um eine weitere hinzuzufügen.

Wenn du bei einer Aufgabe der Routine **Änderungen anfragen** auswählst oder im Chat etwas schreibst, das für jeden Durchlauf gelten soll, zum Beispiel „nie Emojis verwenden“, wird dir **Auch die Routine ändern** angeboten. Die Option erscheint auf der Aufgabe und im Chat unter der Antwort. Sie zeigt, was sich an der Formulierung der Routine ändern würde. Die Routine wird erst geändert, wenn du auf **Ändern** tippst. Mit **So lassen** bleibt sie unverändert. Wenn du nur den Entwurf korrigierst, wird diese Option nicht angeboten.

## Erweitert: Skriptschritte

Du brauchst kein Skript: Beschreibe in eigenen Worten, was eine Routine tun soll, und deine Machine kümmert sich um den Rest.

Für erfahrene Nutzer kann eine Routine auch eigene Befehle auf deiner Machine ausführen. Wähle dazu im Menü ⋯ **Erweitert: Skriptschritte**. **Bearbeiten** wird erst angezeigt, wenn eine Routine Skriptschritte enthält. Mit **Daten holen** wird zuerst ein Befehl ausgeführt, und zwar in dessen Ordner oder, wenn keiner angegeben ist, in deinem Benutzerordner. Der Befehl wird höchstens für die festgelegte Anzahl Sekunden ausgeführt. Seine Ausgabe wird an den Durchlauf zur weiteren Verarbeitung übergeben. Wenn keine Formulierung vorhanden ist, wird die Ausgabe als Ergebnis verwendet.

Mit **Prüfung** wird das Ergebnis nach dem Durchlauf als Eingabe verarbeitet. Wenn der Befehl mit einem Fehler endet, zeigt der Durchlauf **Hat nicht geklappt** und die Meldung der Prüfung an. Ein fehlgeschlagener Befehl unter „Daten holen“ wird genauso angezeigt.

Ein Befehl muss in eine Zeile passen und wird ohne Shell ausgeführt. Pipes und Variablen sind nicht möglich. Skriptschritte legst nur du selbst in deinem Dashboard fest. Bei einem Testlauf und bei **Ausprobieren** wird auch „Daten holen“ ausgeführt und das Ergebnis angezeigt. Dabei wird weiterhin nichts gesendet oder gespeichert. Eine Routine sendet nie etwas. Daher sollten Skriptschritte nur lesen.

## Aus deinen OpenClaw-Jobs

Wenn du zuvor geplante Jobs in OpenClaw erstellt hast, liest deine Machine sie aus, ändert sie aber nie. Jobs, die sich als Routinen eignen, werden unter **Vorgeschlagen** angeboten. Jeder Vorschlag wurde einmal ausgeführt, sodass du ein echtes Ergebnis siehst.

Deine Korrekturen am Job bleiben erhalten. Was der Job gesendet oder gepostet hat, wird ausgelassen. Wenn ein Job ein Skript ausgeführt oder die von einem Skript-Job gesammelten Inhalte gelesen hat, wird das als „Daten holen“ übernommen. Mit **Hinzufügen** wird daraus eine Routine. Mit **Nein danke** wirst du nicht wieder nach diesem Job gefragt. Wenn ein Job dich an etwas erinnert hat, wird er stattdessen auf der Seite „Aufgaben“ als wiederkehrende Aufgabe angeboten.

Bevor du einen Vorschlag hinzufügst, kannst du ihn über **Bearbeiten** und **Zeitpunkt ändern** im Menü ⋯ wie jede Routine anpassen. Mit **Erneut ausführen** wird der Vorschlag sofort mit der aktuellen Formulierung ausgeführt, damit du neuere Ergebnisse sehen kannst, zum Beispiel nach einem ruhigen Wochenende. Dabei wird nur gelesen. Der Vorschlag wird bei jedem Tippen einmal ausgeführt und das neue Ergebnis ersetzt das alte.

Es können höchstens drei Vorschläge gleichzeitig offen sein. Nach einer Woche mit erfolgreichen Durchläufen fragt die Routine **Den alten OpenClaw-Job ausschalten?**. Der Job wird nur ausgeschaltet, wenn du auf **Ausschalten** tippst. Du kannst ihn in OpenClaw wieder einschalten. Mit **Behalten** laufen beide weiter.

## Anhand deiner Aktivitäten

Deine Machine erkennt auch Arbeiten, die du regelmäßig erledigst, und schlägt sie unter **Vorgeschlagen** als Routine vor, auch ohne OpenClaw. Sie sucht nach:

- derselben Anfrage, die du mindestens dreimal hintereinander stellst, zum Beispiel „offene Support-Tickets zusammenfassen“ jeden Montag;
- einer E-Mail, die du regelmäßig sendest, zum Beispiel einem wöchentlichen Bericht an dein Team;
- Newslettern und Update-E-Mails, die jede Woche eingehen;
- einem viel genutzten Slack-Kanal, in dem andere jede Woche schreiben;
- E-Mails, die du einzeln immer an dieselbe Person weiterleitest, zum Beispiel Schul- und Vereins-E-Mails an deine Partnerin oder deinen Partner. Eine wöchentliche Zusammenfassung erspart dir das Weiterleiten;
- derselben Anfrage, die du regelmäßig beantwortest, zum Beispiel einer monatlichen Freigabe für dieselbe Person.

Jeder Vorschlag erklärt, was die Routine erkannt hat, zum Beispiel „4-mal hintereinander angefragt“ oder „6 E-Mails in 3 Wochen an Sam weitergeleitet“. Jeder Vorschlag wurde einmal ausgeführt, sodass du ein echtes Ergebnis siehst. Denk zum Beispiel an eine Zusammenfassung fürs Team, eine kurze Übersicht vor einem wöchentlichen Termin, eine Support- oder Entwickler-Zusammenfassung, einen Überblick über deine Kennzahlen oder eine Zusammenfassung deiner Newsletter.

Vorgeschlagen werden nur Routinen, die speziell für dich und eindeutig nützlich sind. Eine Nachrichtenzusammenfassung berücksichtigt zum Beispiel nur deine eigenen Newsletter, nie allgemeine Nachrichten. Wenn nichts passt, gibt es keinen Vorschlag.

Die Routine prüft höchstens einmal am Tag und bringt höchstens einen neuen Vorschlag pro Woche, ohne Benachrichtigung. Mit **Nein danke** wird dieser Vorschlag nicht erneut angezeigt. Weiterleitungen und Antworten bleiben bei dem Konto, von dem aus sie gesendet wurden. Arbeit und Privates werden also nicht vermischt. Alles bleibt auf deiner Machine. Eine Aufgabe, die du regelmäßig abschließt, wird stattdessen als wiederkehrende Aufgabe angeboten.

## Routinen und wiederkehrende Aufgaben

Eine [wiederkehrende Aufgabe](recurring.md) erinnert dich daran, etwas zu erledigen. Eine Routine ist Arbeit, die deine Machine selbstständig erledigt und dir anschließend zeigt. Verwende eine wiederkehrende Aufgabe für „Miete am Ersten bezahlen“ und eine Routine für „jeden Freitag mitteilen, bei welchen Deals es ruhig geworden ist“.
