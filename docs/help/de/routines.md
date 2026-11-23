---
title: Routinen
area: cards
summary: Aufgaben, die deine Machine regelmäßig selbst erledigt, zum Beispiel montags eine Zusammenfassung deiner offenen Deals. Sie liest nur.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, reorder.py, reorder_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js, dashboard/todos-reorder.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours, reorder, reorders, buy again, running low, order confirmation, shopify
translated: e0d519d5927cdde0
---
## Eine Routine erstellen

Öffne **Routinen** in der Seitenleiste und beschreibe in einer Zeile, was die Routine wann tun soll: „jeden Montag um 9 meine offenen Deals zusammenfassen“ oder „jeden Werktag morgens die Mails auflisten, auf die ich noch antworten muss“. Tippe dann auf **Hinzufügen**.

Ohne Zeitangabe wird die Routine um 8:00 Uhr ausgeführt. Die Uhrzeit richtet sich nach der Uhr deiner Machine. Beim ersten Durchlauf erhält die Routine einen kurzen Namen.

Mit **Hinzufügen** wird zuerst ein Testlauf ausgeführt. So siehst du, was dabei herauskommt, bevor du die Routine behältst. Es wird nichts gesendet oder gespeichert. Danach lässt **Hinzufügen** die Routine regelmäßig laufen, **Ändern** probiert andere Formulierungen oder einen neuen Namen aus und **Abbrechen** verwirft sie.

## Vorlagen

Unter **Vorlagen** am Ende der Routinen kannst du mit **Hinzufügen** eine fertige Routine einschalten. Sie wird sofort einmal ausgeführt und danach jeden Morgen um 7:30 Uhr (Spam aufräumen jede Stunde, Gebrauchte Fundstücke alle 3 Stunden, Abos und Testphasen einmal im Monat). Auf ihrer Karte steht wie bei jeder Routine, was sie tut. Mit **Bearbeiten** kannst du den Text oder den Namen ändern.

Wenn viele Newsletter eingehen und Newsletter aufräumen ausgeschaltet ist (mindestens 25 in einer Woche von mindestens 5 Absendern), erscheint über deinen Aufgaben eine Zeile mit der Anzahl und einer Beschreibung der Aktion. Dort findest du **Einschalten** und **Nein danke**.

Spam aufräumen wird auf dieselbe Weise angeboten, wenn du innerhalb einer Woche mindestens 5 Mails von Hand in den Spam verschoben hast. Mit **Einschalten** wird die Routine wie hier mit **Hinzufügen** hinzugefügt. Bei **Nein danke** wird sie nicht noch einmal angeboten. Das gilt auch für Vorlagen, die du früher schon hattest.

**Newsletter aufräumen** erstellt je einen Aufgabenpunkt für den beruflichen und den privaten Bereich. Darin stehen die Newsletter des letzten Tages, jeweils mit **Behalten** oder **Abmelden**. Zum Abmelden wird der Ein-Klick-Link der Mailingliste verwendet oder, wenn das Senden aktiviert ist, eine Abmelde-Mail von deiner Adresse. Andernfalls meldet The Machine dich über die Seite der Mailingliste in ihrem eigenen Browser ab. Wenn du dich dort anmelden, ein Captcha lösen oder eine Auswahl treffen musst, steht der Grund in der Zeile. Über **Abmeldeseite öffnen** gelangst du dorthin.

Belege, Bestellungen und Zahlungsbenachrichtigungen werden ausgelassen. Mails über eine Gruppenadresse wie eine Google Group werden unter dem Namen der schreibenden Person aufgeführt. Du wirst dadurch nie von der Gruppe abgemeldet. Wenn der Absender keine eigene Abmeldung anbietet, steht in der Zeile **Selbst abmelden**.

**Spam aufräumen** erstellt je einen Aufgabenpunkt für den beruflichen und den privaten Bereich. Darin stehen Mails von unbekannten Absendern, die nach Spam aussehen, jeweils mit **Spam** oder **Kein Spam**. Outlook verschiebt Spam in den Junk-Ordner, Gmail markiert ihn als Spam. Die Routine prüft jede Stunde, sodass Spam normalerweise dort landet, bevor du dich darum kümmerst. Neuer Spam wird dem gleichen Aufgabenpunkt hinzugefügt, solange er noch offen ist.

Ein schreibgeschütztes Gmail-Konto, wie auf einer gehosteten Machine, kann Mails nicht in den Spam verschieben. Dort enthält **Spam** einen Link, über den du die Mail in Gmail markieren kannst. The Machine merkt sich den Absender dann als Spam. Wenn kein Mailkonto verbunden ist, wird bei der Vorlage statt **Hinzufügen** die Option **Mail verbinden** angezeigt.

Unbekannt bedeutet, dass du der Person noch nie geschrieben hast. Ein „Re:“ zählt nur dann als Unterhaltung, wenn du in diesem Thread selbst geschrieben hast. Wenn Mails eines Absenders, den du auf dem Aufgabenpunkt oder in deinem Postfach als Spam markiert hast, wieder durchkommen, erscheinen sie beim nächsten Mal mit dem Hinweis **Schon einmal als Spam markiert**. Mails, die du selbst in den Spam verschoben hast, helfen der Routine ebenfalls, ähnliche Mails zu erkennen.

Es ändert sich nichts, bis du es im Aufgabenpunkt bestätigst. Tippe auf einen Absender, um die Mail zuerst zu lesen. Sie bleibt ungelesen und es ändert sich nichts. Bei Spam aufräumen werden Bilder aus dem Web nicht geladen, damit der Absender nicht sieht, dass die Mail geöffnet wurde. Absender, über die du bereits entschieden hast, werden nicht erneut abgefragt. Wenn an einem Tag keine Newsletter oder Spam-Mails eingehen, wird kein Aufgabenpunkt erstellt. Diese Aufgabenpunkte lösen nie eine Benachrichtigung aus.

Sobald du über alle Absender entschieden hast, wird der Aufgabenpunkt als abgeschlossen angezeigt und enthält die Option **Erledigt**.

**Tägliche Zusammenfassung** wählt einmal am Tag die wichtigsten Newsletter-Inhalte für dich aus und fasst sie in einem Aufgabenpunkt zusammen. Zu jedem Inhalt steht in einer Zeile, warum er für dich wichtig ist. Tippe darauf, um die Mail zu lesen, oder nutze **In deiner Mail öffnen**. Es werden nur Newsletter berücksichtigt, nie Mails von Personen, Belege oder Absender, von denen du dich abgemeldet hast. Bereits gelesene Inhalte werden ebenfalls ausgelassen. Wenn nichts heraussticht, wird kein Aufgabenpunkt erstellt.

Die Routine lernt, was dich interessiert, anhand der Inhalte, die du öffnest, markierst oder ungelesen archivierst, sowie anhand von **Mehr davon** und **Weniger davon** bei den einzelnen Vorschlägen. Die Themen, nach denen sie sucht, stehen auf der Routinenkarte unter **Mehr zu** und **Weniger zu**. Entferne ein Thema mit × oder füge eigene hinzu. Gestrichelte Themen hat die Routine selbst gelernt. Eine neue Zusammenfassung ersetzt die offene. Sie löst nie eine Benachrichtigung aus.

Die Routine liest nur Absender, Betreff und Anfang jedes neuen Newsletters. Außerdem stellt sie deiner KI dazu eine kurze Frage pro Tag, damit die Kosten niedrig bleiben. Mit **Zeitpunkt ändern** legst du die Uhrzeit fest. Sobald du den Text änderst, läuft die Routine wie jede andere mit deinen Formulierungen.

**Geburtstage** erstellt für jeden engen Kontakt, der heute Geburtstag hat, einen Aufgabenpunkt. Gemeint sind Personen, denen du selbst schreibst, etwa Freunde, Familie und regelmäßige Kontakte. Für jede Person gibt es einen kurzen Grußentwurf in dem Kanal, über den du normalerweise mit ihr sprichst, zum Beispiel im WhatsApp-Chat oder im E-Mail-Thread, und zwar in ihrer Sprache. Der Gruß wird erst verschickt, wenn du ihn sendest. An Tagen ohne Geburtstage wird kein Aufgabenpunkt erstellt.

Geburtstage stammen aus deinen Kalendern (Google-Geburtstagsereignisse und dem Geburtstagskalender, der jeden Morgen gelesen wird, auch wenn er nicht synchronisiert ist, sowie dem Geburtstagskalender von Outlook), deinen Google-Kontakten auf einer selbst gehosteten Machine und einem Datumsfeld namens Birthday bei einer Person im Graph. Wenn nirgends ein Geburtstag hinterlegt ist, wird im Ergebnis **Noch keine Geburtstagsinfos** angezeigt und erklärt, wie du welche hinzufügen kannst.

**Geburtstage aus Facebook importieren**: Sobald Geburtstage aktiviert ist, bietet ein Aufgabenpunkt an, die Geburtstagsseite von Facebook auszulesen. Tippe auf **Importieren**. The Machine öffnet die Seite in ihrem Browser, scrollt, bis alle Monate geladen sind, und liest die Namen und Geburtstage deiner Freunde aus. Sie zeigt an, wie viele Einträge sie gefunden hat und welche Personen anhand ihres Vor- und Nachnamens mit Personen in deinem Graph übereinstimmen. Namen, die mehr als eine Person haben, werden übersprungen und aufgelistet.

Nur mit **Speichern** werden die Daten übernommen, und zwar auf der Seite jeder Person: der Geburtstag und das Facebook-Profilbild, wenn die Person noch kein Foto hat. Ein Geburtstag oder Bild, das du dort einträgst, bleibt bestehen. Ein vorhandenes Foto wird nie ersetzt. Auf Facebook wird nichts eingetragen.

Der Import wird nicht automatisch wiederholt. Dafür gibt es **Erneut importieren** auf dem Aufgabenpunkt. Im Browser musst du bei Facebook angemeldet sein. Wenn du es nicht bist, tippe auf dem Aufgabenpunkt auf **Bei Facebook anmelden** und melde dich dort an. Sobald du angemeldet bist, liest die Routine die Seite selbst aus. The Machine meldet dich nie an.

Freunde, die niemandem in deinem Graph zugeordnet sind, werden gezählt und mit einigen Namen aufgeführt. Mit **Alle als persönliche Kontakte hinzufügen** werden sie auf einmal hinzugefügt, auch nach dem Speichern. Für jede Person werden Name und Geburtstag übernommen. Diese Kontakte werden nie mit einer Work Fleet geteilt. Übersprungen werden Personen, deren Namen bereits jemand in deinem Graph hat oder die jemand hatte, den du dauerhaft gelöscht hast. Geburtstagserinnerungen erhältst du weiterhin nur für Personen, denen du schreibst.

Mit **Rückgängig** auf dem Aufgabenpunkt entfernst du genau diese Personen wieder, auch nach **Erneut importieren**.

**Abos und Testphasen** liest einmal im Monat Belege, Rechnungen und Verlängerungsmitteilungen aus deinen Mails und fasst deine Abos in einem Aufgabenpunkt zusammen: die Kosten, den nächsten Abbuchungstermin und einen Hinweis, wenn eine Testphase endet oder der Preis steigt. Aufgeführt werden nur Abos, bei denen sich die Routine sicher ist. Wenn sie nichts findet, wird kein Aufgabenpunkt erstellt.

Wähle für jedes Abo **Behalten** oder **Kündigen**. Bei einem Abo, das du behältst, wirst du nicht erneut gefragt, es sei denn, der Preis ändert sich. **Kündigen** zeigt dir die Kündigungsseite des Anbieters oder einen Entwurf mit der Bitte um Kündigung. Er wird erst gesendet, wenn du ihn abschickst. Zwischen den monatlichen Durchläufen prüft die Routine täglich, ob eine Testphase oder Verlängerung innerhalb der nächsten 7 Tage abgerechnet wird. In diesem Fall erstellt sie einen Aufgabenpunkt.

**In Kontakt bleiben** erinnert dich ab und zu daran, dich bei einer nahestehenden Person zu melden, aber nur, wenn es einen konkreten Anlass gibt. Wähle auf der Routinenkarte aus einer kurzen Liste von Personen aus, mit denen du über mehrere Monate regelmäßig selbst in beide Richtungen schreibst. Entferne jemanden mit ×.

Eine Erinnerung kommt nur, wenn euer letzter Kontakt deutlich länger zurückliegt als sonst und es etwas Konkretes zu sagen gibt: Neuigkeiten, die die Person geteilt hat, ein offenes Versprechen oder eine Nachricht, auf die du nie geantwortet hast. Der Aufgabenpunkt nennt den Grund und enthält einen kurzen Nachrichtenentwurf in dem Kanal, über den du normalerweise mit der Person sprichst, und zwar in ihrer Sprache. Die Nachricht wird erst gesendet, wenn du sie abschickst. Wenn es nichts zu sagen gibt, wird kein Aufgabenpunkt erstellt.

Die Routine verschickt höchstens zwei Erinnerungen pro Woche und höchstens eine pro Person im Monat. Personen, mit denen du kürzlich gesprochen hast, werden nicht erinnert. Mit **Nicht nötig** bei einer Erinnerung wartet die Routine länger, bevor sie dich für diese Person erneut erinnert. Jedes Mal wartet sie noch länger. Sie löst nie eine Benachrichtigung aus und bleibt privat. Sie wird nie mit einer Work Fleet geteilt.

**Gebrauchte Fundstücke** überwacht eine Suche auf einer Gebrauchtwaren-Seite wie Marktplaats, Vinted, eBay oder Facebook Marketplace. Suche dort mit den gewünschten Filtern, kopiere die Adresse der Ergebnisse und füge sie nach **Hinzufügen** ein. Wenn du möchtest, kannst du Filter in eigenen Worten ergänzen, zum Beispiel „unter 300, höchstens 30 km entfernt, kein ‚Ersatzteil‘“. Jede Suche ist eine eigene Routine. Für die nächste Suche musst du sie erneut hinzufügen.

Alle 3 Stunden öffnet die Routine die Suche im eigenen Browser von The Machine und sucht nach Anzeigen, die sie noch nicht gesehen hat. Preis, Entfernung und Begriffe, die du ausgeschlossen hast, werden zuerst mit einfachem Code geprüft.

Jede neue Anzeige, die diese Prüfung besteht, wird geöffnet. Deine KI bewertet den Zustand anhand des Fotos und der Beschreibung sowie den Verkäufer anhand seiner Bewertungen, seiner Sternebewertung und der Dauer seines Kontos. Gute Treffer erscheinen gemeinsam in einem Aufgabenpunkt, jeweils mit Foto, Titel, Preis und einer kurzen Einschätzung. Tippe auf einen Treffer, um die Anzeige im Browser von The Machine zu öffnen.

Solange der Aufgabenpunkt offen ist, kommen neue Treffer oben hinzu, die Anzahl steigt und du erhältst erneut eine Benachrichtigung, denn gute Angebote sind schnell weg. Sobald du den Aufgabenpunkt als erledigt markierst, beginnt für den nächsten Treffer ein neuer. Ein Durchlauf ohne passende Treffer ändert nichts.

Die Routine geht sparsam und rücksichtsvoll vor: pro Durchlauf wird die Suche einmal gelesen, höchstens 6 Anzeigen werden mit einer Pause dazwischen geöffnet und über alle deine Suchen hinweg werden höchstens 40 Anzeigen pro Tag geprüft. Jede Prüfung besteht aus einer kurzen Frage an deine KI mit einem Foto. Beim ersten Durchlauf prüft die Routine die neuesten Anzeigen und markiert den Rest als bereits gesehen. Spätere Durchläufe zeigen daher nur Neues.

Wenn die Seite eine Anmeldung verlangt, eine Bot-Prüfung anzeigt oder das Auslesen verhindert, informiert dich ein Aufgabenpunkt. Mit **Öffnen** kannst du die Seite im Browser von The Machine aufrufen. Melde dich dort an oder löse die Prüfung selbst. Beim nächsten Durchlauf wird die Seite erneut gelesen. The Machine meldet dich nie an und löst keine Prüfungen für dich. Sie kontaktiert auch keine Verkäufer, gibt keine Gebote ab und kauft nichts.

Mit **Suche ändern** auf der Routinenkarte kannst du eine neue Adresse oder Filter eingeben. Mit **Zeitpunkt ändern** legst du einen anderen Rhythmus fest, zum Beispiel „alle 6 Stunden“.

**Nachbestellungen** liest Bestellbestätigungen von Onlineshops in deinen Mails und erkennt, was du regelmäßig nachkaufst, zum Beispiel Kaffee, Tierfutter oder Vitamine. Wenn ein Nachkauf bald ansteht, erstellt die Routine einen Aufgabenpunkt mit dem Artikel, dem Geschäft, dem letzten Preis und dem letzten Kaufdatum. **Im Store öffnen** führt dich zur Produktseite, wo du selbst einkaufen kannst. Für dich wird nichts gekauft.

Die Routine braucht mindestens drei Bestellungen desselben Artikels in gleichmäßigen Abständen. Ein einmaliger Kauf oder eine ungewöhnlich lange Pause führt daher nicht zu einem Aufgabenpunkt. Zurzeit liest sie Bestellungen von Shops, die Shopify verwenden. Deine KI liest nur neue Bestellmails dieser Shops und stellt pro Durchlauf eine kurze Frage. Diese Aufgabenpunkte lösen keine Benachrichtigungen aus. Wenn du den Artikel erneut bestellst, wird der offene Aufgabenpunkt geschlossen.

Solange die Routine einer Vorlage den Text der Vorlage verwendet, läuft sie mit eigenem Code und ohne deinen KI-Plan (Spam aufräumen listet neue Mails von unbekannten Absendern zuerst mit Code auf und stellt deiner KI nur dann eine kurze Frage, wenn es solche Mails gibt. In Kontakt bleiben fragt nur nach den ein oder zwei ausgewählten Personen). Ein neuer Name ändert daran nichts. Sobald du den Text änderst, läuft die Routine wie jede andere mit deinen Formulierungen.

Newsletter aufräumen und Spam aufräumen enden weiterhin mit einem Aufgabenpunkt und einer Auswahl für jede Mail. Eine bearbeitete Routine für Geburtstage zeigt ihr Ergebnis und höchstens einen Entwurf, statt für jede Person einen Aufgabenpunkt zu erstellen. Mit **Zurück zur Vorlage** in **Bearbeiten** wird der ursprüngliche Text der Vorlage wiederhergestellt.

## Was eine Routine tut

Zum festgelegten Zeitpunkt liest deine Machine, was sie braucht, zum Beispiel deine Nachrichten, Termine und den Graph, und zeigt das Ergebnis auf der Seite Routinen an. Jedes Ergebnis lautet **Bereit**, **Nichts Neues** (mit Begründung) oder **Hat nicht geklappt** (mit Begründung). Ein Durchlauf, der ohne Ergebnis endet, gilt als fehlgeschlagen und nie als erledigt.

Routinen lesen nur: deine Nachrichten, Webseiten, GitHub und Seiten wie X im Browser. Sie senden keine Nachrichten, antworten nicht, veröffentlichen nichts und ändern nichts. Sie öffnen Seiten, die sie in den gelesenen Inhalten oder bei einer Suche gefunden haben, sowie normale Webadressen und bekannte Seiten. Sie öffnen nie eine Adresse, die eigens erstellt wurde, um gelesene Inhalte zu übertragen. Nur eine Vorlage kann Mails ändern, und auch nur das, was du auf ihrem Aufgabenpunkt bestätigst.

Wenn eine Routine mit einem Beitrag oder einer Nachricht enden soll, erledigt sie alles bis zu diesem Schritt und zeigt den Entwurf an, zum Beispiel **Würde auf X posten:**. Nach einem echten Durchlauf erhältst du dafür einen Aufgabenpunkt, den du freigeben kannst. Bei einem Testlauf wird der Entwurf nur angezeigt.

Der Name beschreibt, worum es geht und wo das Ergebnis landet. Mit **Aus deiner Routine** darunter öffnest du die Routine. Die Schaltfläche benennt den Schritt, zum Beispiel **Beitrag vorbereiten**. Damit wird der Beitrag vorbereitet, aber nicht veröffentlicht. Du veröffentlichst ihn über das Ergebnis. Wenn The Machine den Beitrag nicht für dich veröffentlichen kann, öffnet die Schaltfläche dort die entsprechende Seite.

Der Aufgabenpunkt wird im Bereich des Kontos erstellt, von dem aus etwas gesendet wird, zum Beispiel unter „Arbeit“ für das X-Konto deines Unternehmens. Du wirst daher nie gebeten, ihn zu verschieben.

Ein Durchlauf kann deinen aktivierten [Skills](skills.md) folgen, ausgewählt anhand der Aufgabe der Routine. Nur passende Skills werden vollständig gelesen. Die verwendeten Skills stehen im Ergebnis unter **Verwendet:**. Ein Skill kann eine Routine nie dazu bringen, etwas zu senden oder zu ändern.

Deine Routinen findest du unter **Deine Routinen**, unterhalb aller Vorschläge. Lange Ergebnisse werden zu einer kurzen Vorschau eingeklappt. Mit **Mehr anzeigen** oder durch Tippen auf die Vorschau öffnest du das vollständige Ergebnis.

Jeder Durchlauf kennt das letzte Ergebnis und kann daher angeben, was sich seitdem geändert hat.

Nach einem erfolgreichen Durchlauf kann deine Machine selbst ein Rezept für wiederkehrende Leseaufgaben erstellen, zum Beispiel dafür, welche Mails oder GitHub-Änderungen geprüft werden sollen. Bei den nächsten Durchläufen wird das zuerst mit einfachem Code erledigt. Die KI wählt nur aus, was wichtig ist, und formuliert das Ergebnis. So werden weniger Tokens benötigt. Ein Rezept liest nur. Wenn es nicht mehr funktioniert, liest die Routine selbst und behebt den Fehler. Das Rezept erscheint im Menü ⋯ unter **Erweitert: Skriptschritte**.

## Verpasste Tage

Wenn deine Machine ausgeschaltet oder beschäftigt war, werden verpasste Durchläufe nicht nachgeholt. Es läuft nur der neueste, und zwar einmal. Jeder Tag wird auch nach einem Neustart nur einmal ausgeführt.

Routinen laufen nacheinander. Wenn das Kontingent deines KI-Plans knapp ist, warten sie, wie alle Hintergrundaufgaben. Mit **Jetzt ausführen** startest du eine Routine sofort. Das Ergebnis wird auf der Karte angezeigt, sobald es bereit ist.

## Ändern oder beenden

Diese Optionen findest du im Menü ⋯ der Routine. Mit **Bearbeiten** änderst du ihren Namen und ihre Aufgabe. Ausführungszeit und bisherige Ergebnisse bleiben erhalten. Mit **Zeitpunkt ändern** kannst du einen neuen Rhythmus in eigenen Worten festlegen, zum Beispiel „jeden Werktag um 8“. Beide Optionen bieten **Speichern** und **Abbrechen**. Am Computer kannst du auch mit Esc oder einem Klick außerhalb des Fensters abbrechen.

Mit **Ausprobieren** in **Bearbeiten** wird der neue Text einmal ausgeführt und das Ergebnis dort angezeigt. Bis du auf **Speichern** tippst, bleibt die Routine unverändert.

Mit **Pausieren** werden die Durchläufe angehalten, bis du auf der Karte **Fortsetzen** auswählst. Pausierte Routinen findest du unter **Pausiert**, unterhalb deiner Routinen. Während der Pause verpasste Durchläufe werden danach nicht ausgeführt. Mit **Stoppen** beendest du eine Routine dauerhaft.

Es können bis zu 20 Routinen gleichzeitig angelegt sein, einschließlich pausierter Routinen. Beende eine Routine, um eine weitere hinzuzufügen.

Wenn du bei einem Aufgabenpunkt der Routine **Änderungen anfragen** auswählst oder im zugehörigen Chat schreibst und sich deine Notiz auf jeden Durchlauf bezieht, etwa „keine Emojis verwenden“, bietet der Aufgabenpunkt **Auch die Routine ändern** an. Die Option erscheint auf dem Aufgabenpunkt und im Chat unter der Antwort. Du siehst, was sich am Text der Routine ändert. Die Routine wird erst geändert, wenn du auf **Ändern** tippst. Mit **So lassen** bleibt sie unverändert. Wenn du nur diesen Entwurf ändern möchtest, wird die Option nicht angeboten.

## Erweitert: Skriptschritte

Du brauchst keine Skripte. Beschreibe einfach in eigenen Worten, was eine Routine tun soll, und deine Machine kümmert sich um den Rest.

Für fortgeschrittene Nutzerinnen und Nutzer kann eine Routine auch eigene Befehle auf deiner Machine ausführen. Wähle dazu im Menü ⋯ **Erweitert: Skriptschritte**. **Bearbeiten** wird erst angezeigt, wenn die Routine Skriptschritte enthält. Mit **Daten holen** wird zuerst ein Befehl im zugehörigen Ordner ausgeführt, oder, wenn keiner angegeben ist, in deinem Home-Ordner. Der Befehl läuft höchstens so viele Sekunden, wie festgelegt sind. Seine Ausgabe steht dem Durchlauf zur Verfügung. Wenn keine weiteren Anweisungen vorhanden sind, ist die Ausgabe selbst das Ergebnis.

**Prüfung** erhält nach dem Durchlauf das Ergebnis als Eingabe. Wenn der Befehl mit einem Fehler beendet wird, zeigt der Durchlauf **Hat nicht geklappt** und die Fehlermeldung. Ein fehlgeschlagener Befehl unter „Daten holen“ wird genauso angezeigt.

Ein Befehl besteht aus einer einzelnen Zeile und wird ohne Shell ausgeführt. Pipes und Variablen sind nicht möglich. Skriptschritte gehören dir und werden nur in deinem Dashboard festgelegt. Bei einem Testlauf und mit **Ausprobieren** wird auch „Daten holen“ ausgeführt. Das wird angezeigt. Dabei wird weiterhin nichts gesendet oder gespeichert. Eine Routine sendet nie etwas. Skriptschritte sollten daher nur lesen.

## Aus deinen OpenClaw-Jobs

Wenn du früher geplante Jobs in OpenClaw erstellt hast, liest deine Machine sie aus, ändert sie aber nie. Passende Jobs bietet sie unter **Vorgeschlagen** als Routinen an. Jeder Job wurde einmal ausgeführt, sodass du ein echtes Ergebnis siehst.

Änderungen, die du am Job vorgenommen hast, bleiben erhalten. Gesendete oder veröffentlichte Inhalte werden ausgelassen. Wenn ein Job ein Skript ausgeführt oder Daten aus einem Skript-Job gelesen hat, wird das Skript als „Daten holen“ übernommen. Mit **Hinzufügen** wird der Job zu einer Routine. **Nein danke** sorgt dafür, dass dieser Job nicht erneut angeboten wird. Ein Job, der dich an eine Aufgabe erinnert hat, wird stattdessen unter „Aufgaben“ als Angebot für eine wiederkehrende Aufgabe angezeigt.

Bevor du einen Vorschlag hinzufügst, kannst du ihn über **Bearbeiten** und **Zeitpunkt ändern** im Menü ⋯ wie jede andere Routine anpassen. Mit **Erneut ausführen** kannst du ihn jetzt mit dem aktuellen Text ausführen lassen, um neuere Ergebnisse zu sehen, zum Beispiel nach einem ruhigen Wochenende. Die Routine liest nur, wird pro Tippen einmal ausgeführt und ersetzt das alte Ergebnis durch das neue.

Es können höchstens drei Vorschläge gleichzeitig ausstehen. Nach einer Woche erfolgreicher Durchläufe fragt die Routine **Den alten OpenClaw-Job ausschalten?** Sie wird nur ausgeschaltet, wenn du auf **Ausschalten** tippst. Du kannst sie in OpenClaw wieder einschalten. **Behalten** lässt beide Routinen weiterlaufen.

## Aus dem, was du tust

Deine Machine erkennt auch wiederkehrende Aufgaben, die du selbst erledigst, und bietet sie unter **Vorgeschlagen** als Routine an, auch ohne OpenClaw. Sie achtet auf Folgendes:

- dieselbe Anfrage mindestens dreimal hintereinander, zum Beispiel „offene Support-Tickets zusammenfassen“ jeden Montag;
- eine Mail, die du regelmäßig sendest, zum Beispiel einen wöchentlichen Bericht an dein Team;
- Newsletter und Update-Mails, die jede Woche eingehen;
- einen stark frequentierten Slack-Kanal, in dem andere jede Woche schreiben;
- Mails, die du einzeln an dieselbe Person weiterleitest, zum Beispiel Schul- und Vereinsmails an deine Partnerin oder deinen Partner. Eine wöchentliche Zusammenfassung erspart dir das Weiterleiten;
- dieselbe Anfrage, die du regelmäßig beantwortest, zum Beispiel eine monatliche Genehmigung für dieselbe Person.

Jeder Vorschlag erklärt, was die Routine beobachtet hat, zum Beispiel „Viermal hintereinander angefragt“ oder „6 Mails in 3 Wochen an Sam weitergeleitet“. Außerdem wurde sie einmal ausgeführt, damit du ein echtes Ergebnis siehst. Denk an eine Team-Zusammenfassung, ein Briefing vor einem wöchentlichen Gespräch, eine Support- oder Entwicklungszusammenfassung, einen Überblick über deine Kennzahlen oder eine Zusammenfassung deiner Newsletter.

Vorgeschlagen werden nur Routinen, die genau auf dich zugeschnitten und klar nützlich sind. Eine Nachrichtenzusammenfassung bezieht sich zum Beispiel nur auf deine eigenen Newsletter und ist nie allgemein gehalten. Wenn nichts passt, gibt es keinen Vorschlag.

Die Routine prüft höchstens einmal am Tag und bringt höchstens einen neuen Vorschlag pro Woche. Sie löst keine Benachrichtigung aus. Mit **Nein danke** wird der Vorschlag nicht noch einmal angezeigt. Weiterleitungen und Antworten bleiben bei dem Konto, von dem aus sie gesendet wurden. Arbeitliches und Privates werden also nicht vermischt. Alles bleibt auf deiner Machine. Eine Aufgabe, die du regelmäßig abschließt, wird stattdessen als Angebot für eine wiederkehrende Aufgabe angezeigt.

## Routinen und wiederkehrende Aufgaben

Eine [wiederkehrende Aufgabe](recurring.md) erinnert dich daran, etwas zu erledigen. Eine Routine ist eine Aufgabe, die deine Machine selbst erledigt und dir anschließend zeigt. Verwende eine wiederkehrende Aufgabe für „am Ersten die Miete bezahlen“ und eine Routine für „jeden Freitag die Deals nennen, bei denen es ruhig geworden ist“.
