---
title: Routinen
area: cards
summary: Aufgaben, die deine Machine regelmäßig selbst erledigt, zum Beispiel jeden Montag deine offenen Deals zusammenfassen. Sie liest nur.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, reorder.py, reorder_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js, dashboard/todos-reorder.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours, reorder, reorders, buy again, running low, order confirmation, shopify
translated: 57b97c44b031845f
---
## Eine Routine erstellen

Öffne **Routinen** in der Seitenleiste und beschreibe in einer Zeile, was sie wann tun soll: „jeden Montag um 9 meine offenen Deals zusammenfassen“ oder „jeden Werktag morgens die Mails auflisten, auf die ich noch antworten muss“. Tippe dann auf **Hinzufügen**.

Ohne Zeitangabe läuft die Routine um 8:00 Uhr. Maßgeblich ist die Uhr deiner Machine. Beim ersten Lauf erhält sie einen kurzen Namen.

Mit **Hinzufügen** wird zuerst ein Testlauf ausgeführt. So siehst du, was dabei herauskommt, bevor du die Routine übernimmst. Es wird nichts gesendet oder gespeichert. Mit **Hinzufügen** läuft die Routine anschließend regelmäßig weiter, **Ändern** probiert andere Formulierungen oder einen neuen Namen aus und **Abbrechen** verwirft sie.

## Vorlagen

Unter **Vorlagen** am Ende von Routinen schaltet **Hinzufügen** eine fertige Routine ein. Sie läuft sofort einmal und danach jeden Morgen um 7:30 Uhr (Spam aufräumen jede Stunde, Gebrauchte Fundstücke alle 3 Stunden, Abos und Testphasen einmal im Monat). Auf der Karte steht ihre Beschreibung wie bei jeder anderen Routine. Mit **Bearbeiten** kannst du die Beschreibung oder den Namen ändern.

Wenn viele Newsletter eingehen und Newsletter aufräumen ausgeschaltet ist (mindestens 25 in einer Woche von mindestens 5 Absendern), erscheint über deinen Aufgaben ein Hinweis mit der Anzahl und einer Beschreibung dessen, was die Routine tun würde. Dazu gibt es **Einschalten** und **Nein danke**.

Spam aufräumen wird genauso vorgeschlagen, wenn du in einer Woche mindestens 5 Mails manuell in den Spam verschoben hast. Mit **Einschalten** wird die Routine wie hier über **Hinzufügen** hinzugefügt. Bei **Nein danke** wird sie nicht noch einmal vorgeschlagen. Auch eine Vorlage, die du schon einmal hattest, wird nie wieder vorgeschlagen.

**Newsletter aufräumen** erstellt für jeden Bereich (Arbeit und Privat) eine Aufgabe mit den Newslettern des vergangenen Tages. Für jeden Newsletter kannst du **Behalten** oder **Abmelden** auswählen. Zum Abmelden wird der Ein-Klick-Link der Mailingliste verwendet oder, wenn das Senden aktiviert ist, eine Abmelde-Mail von deiner Adresse geschickt. Andernfalls meldet The Machine dich in ihrem eigenen Browser auf der Seite der Mailingliste ab. Um dich dort anzumelden, ein Captcha zu lösen oder eine Auswahl zu treffen, musst du selbst aktiv werden. In der Zeile steht der Grund, außerdem gibt es **Abmeldeseite öffnen**.

Möchtest du nur verhindern, dass Mails einer Liste Aufgaben erzeugen, die Mails aber behalten? Schreib im Chat zu einer dieser Mails: „Nichts von dieser Liste braucht eine Aufgabe.“

Quittungen, Bestellungen und Zahlungsbenachrichtigungen werden ausgeschlossen. Mails, die über eine Gruppenadresse wie eine Google Group eingehen, werden unter dem Namen des Absenders aufgeführt. Du wirst dadurch nie von der Gruppe abgemeldet. Wenn der Absender keine eigene Abmeldemöglichkeit hat, steht in der Zeile **Selbst abmelden**.

**Spam aufräumen** erstellt für jeden Bereich eine Aufgabe mit Mails von unbekannten Absendern, die wie Spam aussehen. Für jede Mail kannst du **Spam** oder **Kein Spam** auswählen. Outlook verschiebt Spam in den Junk-Ordner und Gmail markiert ihn als Spam. Die Routine prüft jede Stunde, damit Spam in der Regel schon erkannt ist, wenn du nachsiehst. Neuer Spam wird derselben Aufgabe hinzugefügt, solange sie noch offen ist.

Ein schreibgeschütztes Gmail-Konto, wie auf einer gehosteten Machine, kann Mails nicht in den Spam verschieben. In diesem Fall führt **Spam** zu einem Link, über den du die Mail in Gmail markieren kannst. The Machine merkt sich den Absender als Spam. Wenn kein Mailkonto verbunden ist, wird in der Vorlage statt **Hinzufügen** die Option **Mail verbinden** angezeigt.

Unbekannt bedeutet, dass du der Person noch nie geschrieben hast. Ein „Re:“ zählt nur dann als Unterhaltung, wenn du selbst in dem Thread geschrieben hast. Wenn eine Mail von einem Absender, den du auf der Aufgabe oder in deinem Postfach als Spam markiert hast, wieder durchkommt, erscheint sie in der nächsten Aufgabe mit dem Hinweis **Schon einmal als Spam markiert**. Auch Mails, die du selbst in den Spam verschoben hast, helfen der Routine, ähnliche Mails zu erkennen.

Es ändert sich nichts, bis du es in der Aufgabe bestätigst. Tippe auf einen Absender, um die Mail zuerst zu lesen. Sie bleibt ungelesen und es ändert sich nichts. Bei Spam aufräumen werden Bilder aus dem Web nicht geladen, damit der Absender nicht sehen kann, dass du die Mail geöffnet hast. Absender, über die du schon entschieden hast, werden nicht erneut abgefragt. Wenn es an einem Tag keine Newsletter oder Spam gibt, wird keine Aufgabe erstellt. Diese Aufgaben lösen nie eine Benachrichtigung aus.

Wenn du für alle Absender eine Entscheidung getroffen hast, wird die Aufgabe als erledigt angezeigt und enthält **Als erledigt markieren**.

**Tägliche Zusammenfassung** wählt einmal am Tag die wenigen Newsletter-Beiträge aus, die deine Zeit wert sind, und fasst sie in einer Aufgabe zusammen. Bei jedem Beitrag steht in einer Zeile, warum er für dich wichtig ist. Tippe darauf, um die Mail zu lesen, oder wähle **In deiner Mail öffnen**. Berücksichtigt werden nur Newsletter, keine Mails von Personen, Quittungen oder Absender, von denen du dich abgemeldet hast, und nichts, was du schon gelesen hast. Wenn nichts besonders relevant ist, wird keine Aufgabe erstellt.

Die Routine lernt, was dich interessiert, indem sie berücksichtigt, was du öffnest, mit einem Stern markierst oder ungelesen archivierst, sowie deine Auswahl unter **Mehr davon** und **Weniger davon** bei jedem Vorschlag. Die Themen, nach denen sie sucht, stehen auf der Karte der Routine unter **Mehr zu** und **Weniger zu**. Mit × kannst du ein Thema entfernen oder eigene Themen hinzufügen. Gestrichelte Themen hat die Routine selbst gelernt. Eine neue Zusammenfassung ersetzt die offene. Sie löst nie eine Benachrichtigung aus.

Die Routine liest nur Absender, Betreff und Anfang jedes neuen Newsletters und stellt deiner KI eine kurze Frage dazu. Es gibt ein Tageslimit, damit die Kosten niedrig bleiben. Mit **Zeitpunkt ändern** kannst du die Uhrzeit festlegen. Sobald du die Beschreibung änderst, läuft sie wie jede andere Routine mit deiner Beschreibung.

**Geburtstage** erstellt für jeden engen Kontakt, der heute Geburtstag hat, eine Aufgabe. Dazu zählen Personen, denen du selbst schreibst, etwa Freunde, Familie und regelmäßige Kontakte. Für jede Person wird ein kurzer Gruß als Entwurf vorbereitet, und zwar dort, wo du normalerweise mit ihr sprichst, etwa in ihrem WhatsApp-Chat oder deinem Mail-Thread, und in ihrer Sprache. Der Gruß wird nur gesendet, wenn du ihn abschickst. An Tagen ohne Geburtstage wird keine Aufgabe erstellt.

Geburtstage stammen aus deinen Kalendern (Googles Geburtstagstermine und Geburtstagskalender, die jeden Morgen ausgelesen werden, auch wenn sie nicht synchronisiert sind, sowie Outlooks Geburtstagskalender), aus deinen Google-Kontakten auf einer selbst gehosteten Machine und aus einem Datumsfeld namens Birthday bei einer Person im Graph. Wenn noch nirgendwo ein Geburtstag eingetragen ist, steht im Ergebnis **Noch keine Geburtstagsinfos** mit einer Erklärung, wie du welche hinzufügen kannst.

**Geburtstage aus Facebook importieren**: Sobald Geburtstage aktiviert ist, bietet eine Aufgabe an, die Geburtstagsseite von Facebook auszulesen. Tippe auf **Importieren**. The Machine öffnet die Seite in ihrem Browser, scrollt, bis alle Monate geladen sind, und liest die Namen und Geburtstage deiner Freunde aus. Sie zeigt, wie viele Geburtstage gefunden wurden und bei wem ein Abgleich mit Personen in deinem Graph anhand von Vor- und Nachnamen möglich war. Namen, die mehreren Personen zugeordnet werden könnten, werden übersprungen und aufgelistet.

Nur mit **Speichern** werden die Daten auf der Seite jeder Person gespeichert: der Geburtstag und, falls die Person noch kein Foto hat, ihr Facebook-Profilbild. Ein Geburtstag oder Foto, das du dort festlegst, bleibt erhalten. Ein vorhandenes Foto wird nie ersetzt. Auf Facebook wird nichts gespeichert.

Die Routine liest die Seite nicht automatisch erneut aus. Das geht nur über **Erneut importieren** in der Aufgabe. Der Browser muss bei Facebook angemeldet sein. Falls das nicht der Fall ist, tippe in der Aufgabe auf **Bei Facebook anmelden** und melde dich dort an. Danach liest die Routine die Seite selbstständig aus. The Machine meldet dich nie selbst an.

Freunde, die niemandem in deinem Graph zugeordnet werden konnten, werden gezählt und mit einigen Namen aufgeführt. Mit **Alle als private Kontakte hinzufügen** kannst du sie auf einmal hinzufügen, auch nach dem Speichern. Für jede Person werden Name und Geburtstag übernommen. Die Kontakte werden nie mit einer Work Fleet geteilt. Personen, deren Namen bereits jemand in deinem Graph hat oder die du dauerhaft gelöscht hast, werden übersprungen. Geburtstagserinnerungen gibt es weiterhin nur für Personen, denen du schreibst.

Mit **Rückgängig** in der Aufgabe werden genau diese Personen wieder entfernt, auch nach **Erneut importieren**.

**Abos und Testphasen** liest einmal im Monat Quittungen, Rechnungen und Verlängerungsbenachrichtigungen aus deinen Mails und fasst deine Abos in einer Aufgabe zusammen: die Kosten, die nächste Abbuchung und einen Hinweis, wenn eine Testphase endet oder der Preis steigt. Aufgeführt werden nur Abos, bei denen sich die Routine sicher ist. Wenn sie nichts findet, wird keine Aufgabe erstellt.

Wähle für jedes Abo **Behalten** oder **Kündigen**. Bei Abos, die du behältst, wirst du nicht noch einmal gefragt, es sei denn, der Preis ändert sich. Mit **Kündigen** erhältst du entweder einen Link zur Kündigungsseite oder einen Entwurf mit einer Kündigungsanfrage. Die Anfrage wird nur gesendet, wenn du sie abschickst. Zwischen den monatlichen Durchläufen prüft die Routine jeden Tag, ob eine Testphase oder Verlängerung innerhalb von 7 Tagen abgebucht wird. Ist das der Fall, erstellt sie eine Aufgabe.

**In Kontakt bleiben** erinnert dich ab und zu daran, dich bei einer nahestehenden Person zu melden, aber nur, wenn es einen konkreten Grund gibt. Auf der Karte kannst du aus einer kurzen Liste auswählen, mit wem die Routine in Kontakt bleibt. Aufgeführt werden Personen, mit denen du über Monate selbst Nachrichten austauschst. Mit × kannst du jemanden entfernen.

Eine Erinnerung erscheint nur, wenn du deutlich länger als sonst keinen Kontakt hattest und es etwas Konkretes zu sagen gibt: Neuigkeiten, die die Person geteilt hat, auch aus der Zusammenfassung auf ihrer Seite, ein noch offenes Versprechen oder eine Nachricht, auf die du nie geantwortet hast.

Bei Neuigkeiten mit einem Datum in der Zukunft, etwa einem Umzug nächsten Monat, schaut die Routine kurz nach diesem Datum noch einmal nach den neuesten Nachrichten. Daraus entsteht eine Aufgabe mit dem Grund und einem kurzen Nachrichtenentwurf an dem Ort, wo du normalerweise mit der Person sprichst, in ihrer Sprache. Die Nachricht wird nur gesendet, wenn du sie abschickst. Wenn es nichts zu sagen gibt, wird keine Aufgabe erstellt.

Die Routine verschickt höchstens zwei Erinnerungen pro Woche und eine pro Person im Monat. Personen, mit denen du kürzlich gesprochen hast, werden nicht berücksichtigt. Mit **Nicht nötig** bei einer Erinnerung wartet die Routine länger, bevor sie dich für diese Person wieder erinnert. Jedes Mal wird die Wartezeit länger. Die Routine löst nie eine Benachrichtigung aus und bleibt privat. Sie wird nie mit einer Work Fleet geteilt und basiert nie auf Informationen aus deinen Work-Konten.

**Gebrauchte Fundstücke** überwacht eine Suche auf einer Gebrauchtwarenplattform, etwa Marktplaats, Vinted, eBay oder Facebook Marketplace. Suche dort mit den gewünschten Filtern, kopiere die Adresse der Ergebnisse und füge sie nach **Hinzufügen** ein. Wenn du möchtest, kannst du Filter in eigenen Worten hinzufügen, etwa „unter 300, höchstens 30 km entfernt, keine Angebote ‚für Ersatzteile‘“. Jede Suche ist eine eigene Routine. Für eine weitere Suche musst du die Routine erneut hinzufügen.

Alle 3 Stunden öffnet die Routine die Suche im eigenen Browser von The Machine und sucht nach Angeboten, die sie noch nicht kennt. Preis, Entfernung und ausgeschlossene Begriffe werden zuerst mit einfachem Code geprüft.

Jedes neue Angebot, das die Filter erfüllt, wird geöffnet. Deine KI beurteilt anhand des Fotos und der Beschreibung den Zustand und anhand der Bewertungen, der Sternebewertung und des Kontenalters den Verkäufer. Die guten Angebote kommen in eine Aufgabe, jeweils mit Foto, Titel, Preis und einem kurzen Urteil. Tippe auf ein Angebot, um es im Browser von The Machine zu öffnen.

Solange die Aufgabe offen ist, kommen neue Fundstücke oben hinzu. Die Anzahl steigt und du erhältst erneut eine Benachrichtigung, denn gute Angebote sind schnell weg. Sobald du die Aufgabe als erledigt markierst, beginnt die nächste Suche mit einer neuen Aufgabe. Wenn bei einem Durchlauf nichts Interessantes dabei ist, ändert sich nichts.

Die Routine geht sparsam und vorsichtig vor: Sie liest die Suche einmal pro Durchlauf aus, öffnet höchstens 6 Angebote pro Durchlauf mit einer Pause dazwischen und prüft höchstens 40 Angebote pro Tag über alle deine Suchen hinweg. Jede Prüfung besteht aus einer kurzen Frage an deine KI und einem Foto. Beim ersten Durchlauf prüft sie die neuesten Angebote und markiert die übrigen als bereits gesehen. Bei späteren Durchläufen kommen daher nur neue Angebote hinzu.

Wenn die Website eine Anmeldung verlangt, eine Roboterprüfung anzeigt oder das Auslesen blockiert, informiert dich eine Aufgabe darüber. Über **Öffnen** kannst du die Seite im Browser von The Machine ansehen. Melde dich dort selbst an oder löse die Prüfung. Beim nächsten Durchlauf liest die Routine die Seite erneut aus. The Machine meldet dich nie selbst an, löst nie eine Prüfung für dich und kontaktiert, ersteigert oder kauft nie etwas bei einem Verkäufer.

Mit **Suche ändern** auf der Karte der Routine kannst du eine neue Adresse oder andere Filter festlegen. **Zeitpunkt ändern** legt einen anderen Rhythmus fest, etwa „alle 6 Stunden“.

**Nachbestellungen** liest Bestellbestätigungen von Online-Shops in deinen Mails und erkennt, was du immer wieder kaufst, etwa Kaffee, Tierfutter oder Vitamine. Wenn der nächste Kauf wahrscheinlich bald ansteht, erstellt die Routine eine Aufgabe mit dem Artikel, dem Shop, dem letzten Preis und dem Datum des letzten Kaufs. **Im Store öffnen** führt dich zur Produktseite, wo du den Artikel selbst kaufen kannst. Für dich wird nichts gekauft.

Die Routine braucht mindestens drei Bestellungen desselben Artikels in regelmäßigem Abstand. Ein einmaliger Kauf oder eine ungewöhnlich lange Pause erstellt keine Aufgabe. Derzeit liest sie Bestellungen aus Shops, die Shopify verwenden. Deine KI liest pro Durchlauf nur neue Bestellmails dieser Shops, jeweils mit einer kurzen Frage. Diese Aufgaben lösen nie eine Benachrichtigung aus. Wenn du den Artikel erneut bestellst, wird die offene Aufgabe geschlossen.

Solange die Routine einer Vorlage deren Beschreibung beibehält, läuft sie mit eigenem Code und ohne deinen KI-Plan. Spam aufräumen listet zum Beispiel zuerst in Code neue Mails von unbekannten Absendern auf und stellt deiner KI nur dann eine kurze Frage, wenn es welche gibt. In Kontakt bleiben fragt nur nach ein oder zwei ausgewählten Personen. Ein neuer Name ändert daran nichts. Sobald du die Beschreibung änderst, läuft die Routine wie jede andere mit deiner Beschreibung.

Newsletter aufräumen und Spam aufräumen erstellen weiterhin dieselbe Aufgabe mit einer Auswahl pro Mail. Bei einer bearbeiteten Routine für Geburtstage zeigt das Ergebnis höchstens einen Entwurf, keine eigene Aufgabe pro Person. Über **Zurück zur Vorlage** in **Bearbeiten** stellst du die ursprüngliche Beschreibung wieder her.

## Was eine Routine tut

Zur festgelegten Zeit liest deine Machine die benötigten Informationen, etwa deine Nachrichten, Termine und den Graph, und zeigt das Ergebnis auf der Seite Routinen an. Für jeden Durchlauf wird **Bereit**, **Nichts Neues** (mit Begründung) oder **Hat nicht geklappt** (mit Begründung) angezeigt. Ein Durchlauf, der ohne Ergebnis endet, gilt als fehlgeschlagen, nie als erledigt.

Routinen lesen nur: deine Nachrichten, Webseiten, GitHub und Websites wie X im Browser. Sie senden und beantworten keine Nachrichten, veröffentlichen nichts und ändern nichts. Sie öffnen Seiten, die sie in den gelesenen Inhalten oder einer Suche gefunden haben, sowie normale Webadressen und bekannte Websites. Nie öffnen sie eine Adresse, die eigens erstellt wurde, um gelesene Inhalte zu übermitteln. Nur eine Vorlage ändert Mails, und auch dann nur, wenn du es in der zugehörigen Aufgabe bestätigst.

Wenn die Aufgabe einer Routine mit einem Beitrag oder einer Nachricht enden soll, erledigt sie alles bis zu diesem Schritt und zeigt den Entwurf an, zum Beispiel **Würde auf X posten:**. Nach einem echten Durchlauf erhältst du den Entwurf als Aufgabe, die du bestätigen kannst. Bei einem Testlauf wird er nur angezeigt.

Der Name beschreibt, worum es geht und wo das Ergebnis erscheint. Unter dem Namen öffnet **Aus deiner Routine** die Routine. Die Schaltfläche benennt den nächsten Schritt, etwa **Beitrag vorbereiten**. Damit wird der Beitrag vorbereitet, aber nicht veröffentlicht. Du veröffentlichst ihn über das Ergebnis. Wenn The Machine das nicht für dich erledigen kann, öffnet die Schaltfläche dort die passende Seite.

Die Aufgabe wird im Bereich des Kontos erstellt, über das sie verschickt wird, etwa im Bereich Arbeit für das X-Konto deines Unternehmens. Du wirst also nie aufgefordert, sie zu verschieben.

Ein Durchlauf kann deinen aktivierten [Skills](skills.md) folgen, die anhand der Aufgabe der Routine ausgewählt werden. Nur passende Skills werden vollständig gelesen. Das Ergebnis listet sie unter **Verwendet:** auf. Ein Skill veranlasst eine Routine nie dazu, etwas zu senden oder zu ändern.

Deine Routinen findest du unter **Deine Routinen**, unterhalb aller Vorschläge. Lange Ergebnisse werden zunächst als kurze Vorschau angezeigt. Mit **Mehr anzeigen** oder durch Antippen kannst du sie öffnen.

Bei jedem Durchlauf wird das letzte Ergebnis berücksichtigt. So kann die Routine sagen, was sich seitdem geändert hat.

Nach einem erfolgreichen Durchlauf erstellt deine Machine möglicherweise selbst ein Rezept für wiederkehrende Leseaufgaben, etwa dafür, welche Mails oder GitHub-Änderungen geprüft werden sollen. Bei späteren Durchläufen werden diese Informationen zuerst mit einfachem Code gelesen. Die KI wählt dann nur noch die relevanten Inhalte aus und formuliert das Ergebnis mit weniger Tokens. Ein Rezept liest nur. Wenn es nicht mehr funktioniert, liest die Routine die Daten selbst aus und korrigiert das Rezept. Das Rezept wird im Menü ⋯ unter **Erweitert: Skriptschritte** angezeigt.

## Versäumte Tage

Wenn deine Machine ausgeschaltet oder ausgelastet war, werden versäumte Durchläufe nicht nachgeholt. Nur der neueste Durchlauf wird einmal ausgeführt. Jeder Tag wird nur einmal verarbeitet, auch nach einem Neustart.

Routinen laufen nacheinander. Wenn dein KI-Plan nur noch wenig Nutzung zulässt, müssen sie wie alle Hintergrundaufgaben warten. Mit **Jetzt ausführen** startest du die Routine sofort. Das Ergebnis erscheint auf der Karte, sobald es bereit ist.

## Ändern oder beenden

Diese Optionen findest du im Menü ⋯ der Routine. Mit **Bearbeiten** änderst du den Namen und die Aufgabe. Der Zeitplan und die bisherigen Ergebnisse bleiben erhalten. Mit **Zeitpunkt ändern** kannst du in eigenen Worten einen neuen Rhythmus festlegen, etwa „jeden Werktag um 8“. Beide Optionen bieten **Speichern** und **Abbrechen**. Am Computer kannst du auch mit Esc oder durch Klicken außerhalb abbrechen.

Mit **Ausprobieren** in **Bearbeiten** lässt sich die neue Beschreibung einmal ausführen und das Ergebnis direkt anzeigen. Bis du auf **Speichern** tippst, bleibt die Routine unverändert.

Mit **Pausieren** werden die Durchläufe angehalten. Über **Fortsetzen** auf der Karte kannst du sie wieder starten. Pausierte Routinen findest du unter **Pausiert**, unterhalb deiner Routinen. Versäumte Durchläufe werden nach der Pause nicht nachgeholt. Mit **Stoppen** wird eine Routine dauerhaft beendet.

Es können bis zu 20 Routinen eingerichtet werden, einschließlich pausierter Routinen. Beende eine Routine, um eine weitere hinzuzufügen.

Wenn du bei einer Aufgabe der Routine **Änderungen anfragen** auswählst oder im Chat mit der Routine schreibst und deine Anmerkung für jeden Durchlauf gelten soll, etwa „nie Emojis verwenden“, wird **Auch die Routine ändern** angeboten. Die Option erscheint in der Aufgabe und im Chat unter der Antwort. Es wird angezeigt, was sich an der Beschreibung der Routine ändert. Die Änderung wird erst übernommen, wenn du auf **Ändern** tippst. Mit **So lassen** bleibt die Routine unverändert. Bei einer Korrektur, die nur diesen Entwurf betrifft, wird die Option nicht angeboten.

## Erweitert: Skriptschritte

Du brauchst keine Skripts: Beschreibe einfach in eigenen Worten, was eine Routine tun soll. Deine Machine findet den Rest heraus.

Für erfahrene Nutzerinnen und Nutzer kann eine Routine auch eigene Befehle auf deiner Machine ausführen. Wähle dafür im Menü ⋯ **Erweitert: Skriptschritte**. **Bearbeiten** wird erst angezeigt, wenn die Routine Skriptschritte enthält. Mit **Daten holen** wird zuerst ein Befehl ausgeführt, und zwar im zugehörigen Ordner (oder in deinem Home-Ordner, wenn kein Ordner angegeben ist) und höchstens für die angegebene Anzahl an Sekunden. Die Ausgabe wird an den Durchlauf weitergegeben. Wenn keine Beschreibung angegeben ist, ist die Ausgabe das Ergebnis.

Mit **Prüfung** wird das Ergebnis nach dem Durchlauf als Eingabe übernommen. Wenn der Befehl mit einem Fehler endet, zeigt der Durchlauf **Hat nicht geklappt** mit der Fehlermeldung der Prüfung an. Ein fehlgeschlagener Befehl zum Abrufen von Daten wird genauso angezeigt.

Ein Befehl besteht aus einer Zeile und wird ohne Shell ausgeführt. Pipes und Variablen sind nicht möglich. Die Skriptschritte gehören dir und werden nur auf deinem Dashboard festgelegt. Bei einem Testlauf und bei **Ausprobieren** wird auch der Befehl zum Abrufen von Daten ausgeführt und entsprechend angezeigt. Dabei wird weiterhin nichts gesendet oder gespeichert. Eine Routine sendet nie etwas. Skriptschritte sollten deshalb nur Daten lesen.

## Aus deinen OpenClaw-Jobs

Wenn du früher in OpenClaw zeitgesteuerte Jobs eingerichtet hast, liest deine Machine sie aus, ändert sie aber nie. Passende Jobs werden unter **Vorgeschlagen** als Routinen angeboten. Jeder Job wurde einmal ausgeführt, sodass du ein echtes Ergebnis siehst.

Änderungen, die du am Job vorgenommen hast, werden übernommen. Inhalte, die der Job gesendet oder veröffentlicht hat, werden ausgelassen. Wenn ein Job ein Skript ausgeführt oder Daten ausgelesen hat, die ein Skript-Job gesammelt hat, wird das als **Daten holen** übernommen. Mit **Hinzufügen** wird daraus eine Routine. Bei **Nein danke** wird dieser Job nicht erneut vorgeschlagen. Ein Job, der dich an eine Aufgabe erinnert hat, erscheint stattdessen auf der Seite Aufgaben als Angebot für eine wiederkehrende Aufgabe.

Bevor du einen Vorschlag hinzufügst, kannst du ihn wie jede andere Routine über **Bearbeiten** und **Zeitpunkt ändern** im Menü ⋯ anpassen. Mit **Erneut ausführen** startest du ihn mit der aktuellen Beschreibung noch einmal, um neuere Ergebnisse zu sehen, etwa nach einem ruhigen Wochenende. Dabei wird nur gelesen. Bei jedem Tippen wird der Job einmal ausgeführt und das neue Ergebnis ersetzt das alte.

Es können höchstens drei Vorschläge gleichzeitig ausstehen. Nach einer Woche erfolgreicher Durchläufe fragt die Routine **Den alten OpenClaw-Job ausschalten?**. Der Job wird nur ausgeschaltet, wenn du auf **Ausschalten** tippst. Du kannst ihn in OpenClaw wieder einschalten. **Behalten** lässt beide Routinen weiterlaufen.

## Aus deinen Aktivitäten

Deine Machine erkennt auch regelmäßig wiederkehrende Aufgaben und schlägt sie unter **Vorgeschlagen** als Routinen vor, auch ohne OpenClaw. Sie sucht nach:

- derselben Aufforderung, die mindestens dreimal hintereinander gestellt wurde, etwa „fasse jeden Montag die offenen Support-Tickets zusammen“;
- einer regelmäßig von dir versendeten Mail, etwa einem wöchentlichen Bericht an dein Team;
- Newslettern und Update-Mails, die jede Woche eingehen;
- einem aktiven Slack-Kanal, in den andere jede Woche schreiben;
- Mails, die du einzeln immer an dieselbe Person weiterleitest, etwa Schul- und Vereinsmails an deinen Partner oder deine Partnerin. Eine wöchentliche Zusammenfassung erspart dir das Weiterleiten;
- derselben Anfrage, auf die du regelmäßig antwortest, etwa einer monatlichen Genehmigung für dieselbe Person.

Jeder Vorschlag erklärt, worauf die Routine basiert, etwa „4-mal hintereinander angefragt“ oder „6 Mails in 3 Wochen an Sam weitergeleitet“. Er wurde bereits einmal ausgeführt, sodass du ein echtes Ergebnis siehst. Denk zum Beispiel an eine Team-Zusammenfassung, eine kurze Übersicht vor einem wöchentlichen Anruf, eine Zusammenfassung für den Support oder die Entwicklung, einen Überblick über deine Kennzahlen oder eine Zusammenfassung deiner Newsletter.

Vorgeschlagen werden nur Routinen, die konkret auf dich zugeschnitten und eindeutig nützlich sind. Eine Nachrichtenübersicht basiert zum Beispiel nur auf deinen eigenen Newslettern, nie auf allgemeinen Nachrichten. Wenn nichts passt, gibt es keine Vorschläge.

Die Routine sucht höchstens einmal am Tag und bringt höchstens einen neuen Vorschlag pro Woche. Sie löst keine Benachrichtigung aus. Bei **Nein danke** wird der Vorschlag nicht erneut angezeigt. Weiterleitungen und Antworten bleiben beim Konto, von dem aus sie gesendet wurden. Arbeit und Privat werden also nicht vermischt. Alles bleibt auf deiner Machine. Eine Aufgabe, die du regelmäßig schließt, wird stattdessen als Angebot für eine wiederkehrende Aufgabe angezeigt.

## Routinen und wiederkehrende Aufgaben

Eine [wiederkehrende Aufgabe](recurring.md) erinnert dich daran, etwas zu erledigen. Eine Routine ist eine Aufgabe, die deine Machine selbstständig ausführt und dir anschließend zeigt. Verwende für „am Ersten die Miete bezahlen“ eine wiederkehrende Aufgabe und für „jeden Freitag sagen, welche Deals ins Stocken geraten sind“ eine Routine.
