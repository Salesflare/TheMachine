---
title: Routinen
area: cards
summary: Arbeit, die deine Machine selbstständig und regelmäßig erledigt, zum Beispiel eine Zusammenfassung deiner offenen Deals am Montag. Sie liest nur.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, reorder.py, reorder_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js, dashboard/todos-reorder.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours, reorder, reorders, buy again, running low, order confirmation, shopify
translated: 6d74cb93df1bf494
---
## Eine Routine erstellen

Öffne **Routinen** in der Seitenleiste und beschreibe in einer Zeile, was die Routine wann tun soll: „jeden Montag um 9 Uhr meine offenen Deals zusammenfassen“ oder „jeden Morgen an Werktagen die Mails auflisten, auf die ich noch antworten muss“. Tippe dann auf **Hinzufügen**.

Ohne Uhrzeit läuft die Routine um 8:00 Uhr. Maßgeblich ist die Uhr deiner Machine. Beim ersten Lauf bekommt die Routine einen kurzen Namen.

Mit **Hinzufügen** wird zuerst ein Testlauf gestartet. So siehst du, was dabei herauskommt, bevor du die Routine übernimmst. Es wird nichts gesendet oder gespeichert. Mit **Hinzufügen** läuft die Routine anschließend regelmäßig, mit **Ändern** kannst du andere Formulierungen oder einen neuen Namen ausprobieren und mit **Abbrechen** verwirfst du sie.

## Vorlagen

Unter **Vorlagen** am Ende der Routinen-Seite kannst du mit **Hinzufügen** eine fertige Routine einschalten. Sie läuft sofort einmal und danach jeden Morgen um 7:30 Uhr. Spam aufräumen läuft jede Stunde, Gebrauchte Fundstücke alle 3 Stunden und Abos und Testphasen einmal im Monat. Auf der Karte steht die Formulierung wie bei jeder anderen Routine. Mit **Bearbeiten** kannst du die Formulierung oder den Namen ändern.

Wenn viele Newsletter eingehen und Newsletter aufräumen ausgeschaltet ist, also mindestens 25 Newsletter von mindestens 5 Absendern in einer Woche, erscheint über deinen Aufgaben eine Zeile. Sie zeigt, wie viele Newsletter eingegangen sind und was die Routine tun würde. Dazu gibt es **Einschalten** und **Nein danke**.

Spam aufräumen wird genauso angeboten, wenn du in einer Woche mindestens 5 Mails von Hand als Spam markiert hast. Mit **Einschalten** wird die Routine so hinzugefügt wie hier mit **Hinzufügen**. Mit **Nein danke** wird sie nicht noch einmal angeboten. Auch eine Vorlage, die du schon einmal hattest, wird nicht erneut angeboten.

**Newsletter aufräumen** erstellt für jeden Bereich, geschäftlich und privat, eine Aufgabe mit den Newslettern des letzten Tages. Bei jeder Mail kannst du **Behalten** oder **Abmelden** wählen. Zum Abmelden wird der Ein-Klick-Link der Mailingliste verwendet oder, wenn das Senden eingeschaltet ist, eine Abmelde-Mail von deiner Adresse aus verschickt. Andernfalls meldet The Machine dich auf der Seite der Liste in ihrem eigenen Browser ab. Wenn du dich dort anmelden, ein Captcha lösen oder eine Auswahl treffen musst, wird der Grund in der Zeile angezeigt. Dort findest du auch **Abmeldeseite öffnen**.

Möchtest du keine Aufgaben von einer Liste, aber ihre Mails behalten? Schreib im Chat zu einer dieser Mails: „Von dieser Liste muss nichts zu einer Aufgabe werden“.

Belege, Bestellungen und Zahlungsbenachrichtigungen werden ausgelassen. Mails, die über eine Gruppenadresse wie eine Google Group eingehen, werden unter dem Namen der schreibenden Person aufgeführt. Du wirst dadurch nie von der Gruppe abgemeldet. Wenn der Absender keine eigene Abmeldung anbietet, steht in der Zeile **Selbst abmelden**.

**Spam aufräumen** erstellt für jeden Bereich eine Aufgabe mit Mails unbekannter Absender, die wie Spam aussehen. Für jede Mail kannst du **Spam** oder **Kein Spam** wählen. Outlook verschiebt Spam in den Junk-Ordner und Gmail markiert ihn als Spam. Die Routine prüft jede Stunde, damit Spam in der Regel schon erkannt ist, bevor du dazu kommst. Neuer Spam wird zur selben Aufgabe hinzugefügt, solange sie noch offen ist.

Wenn Gmail nur mit Leseberechtigung verbunden ist, wie bei einer gehosteten Machine, können Mails nicht in den Spam-Ordner verschoben werden. Dort öffnet **Spam** einen Link, über den du die Mail in Gmail als Spam markieren kannst. The Machine merkt sich den Absender dann als Spam. Wenn kein Mailkonto verbunden ist, zeigt die Vorlage statt **Hinzufügen** die Option **Mail verbinden**.

Als unbekannt gilt ein Absender, dem du noch nie geschrieben hast. Ein „Re:“ zählt nur dann als Unterhaltung, wenn du selbst in dem Thread geschrieben hast. Wenn eine Mail von einem Absender, den du auf der Aufgabe oder in deinem Postfach als Spam markiert hast, wieder durchkommt, erscheint sie in der nächsten Aufgabe mit dem Hinweis **Schon einmal als Spam markiert**. Mails, die du selbst in den Spam verschoben hast, helfen der Routine ebenfalls, ähnliche Mails zu erkennen.

Erst wenn du die Auswahl in der Aufgabe bestätigst, wird etwas geändert. Tippe auf einen Absender, um die Mail zuerst zu lesen. Sie bleibt ungelesen und es wird nichts geändert. Bei Spam aufräumen werden Bilder aus dem Internet nicht geladen. Der Absender kann daher nicht sehen, dass du die Mail geöffnet hast. Absender, über die du schon entschieden hast, werden nicht erneut abgefragt. Wenn es an einem Tag keine Newsletter oder Spam gibt, wird keine Aufgabe erstellt. Diese Aufgaben lösen nie eine Benachrichtigung aus.

Sobald du über alle Absender entschieden hast, zeigt die Aufgabe an, dass sie abgeschlossen ist. Darin findest du dann **Als erledigt markieren**.

**Tägliche Zusammenfassung** wählt einmal am Tag die wenigen Newsletter-Beiträge aus, die deine Zeit wert sind, und fasst sie in einer Aufgabe zusammen. Zu jedem Beitrag steht in einer Zeile, warum er für dich wichtig ist. Tippe darauf, um die Mail zu lesen, oder wähle **In deiner Mail öffnen**. Berücksichtigt werden nur Newsletter, niemals Mails von Personen, Belege oder Absender, von denen du dich abgemeldet hast. Bereits gelesene Mails werden ebenfalls ausgelassen. Wenn nichts besonders interessant ist, wird keine Aufgabe erstellt.

Die Routine lernt, was dich interessiert, anhand der Mails, die du öffnest, mit einem Stern markierst oder ungelesen archivierst, sowie anhand von **Mehr davon** und **Weniger davon** bei den einzelnen Vorschlägen. Die Themen, nach denen sie sucht, stehen auf der Karte der Routine unter **Mehr zu** und **Weniger zu**. Entferne ein Thema mit × oder füge eigene Themen hinzu. Gestrichelte Themen hat die Routine selbst gelernt. Eine neue Zusammenfassung ersetzt die noch offene. Benachrichtigungen werden nie gesendet.

Die Routine liest nur Absender, Betreff und Anfang jedes neuen Newsletters und stellt deiner KI dazu eine kurze Frage pro Tag. So bleibt der Aufwand gering. Mit **Zeitpunkt ändern** legst du die Uhrzeit fest. Sobald du die Formulierung änderst, läuft die Routine wie jede andere mit deinen eigenen Worten.

**Geburtstage** erstellt für jede enge Kontaktperson, die heute Geburtstag hat, eine Aufgabe. Gemeint sind Personen, denen du selbst schreibst, zum Beispiel Freunde, Familie und regelmäßige Kontakte. Für jede Person gibt es einen kurzen Grußentwurf in dem Kanal, über den du normalerweise mit ihr sprichst, zum Beispiel in ihrem WhatsApp-Chat oder in deinem Mail-Thread. Der Gruß ist in ihrer Sprache verfasst und wird erst gesendet, wenn du ihn selbst abschickst. An Tagen ohne Geburtstage wird keine Aufgabe erstellt.

Geburtstage stammen aus deinen Kalendern: aus Googles Geburtstagsterminen und dem Kalender „Geburtstage“, der jeden Morgen gelesen wird, auch wenn er nicht synchronisiert ist, sowie aus Outlooks Kalender „Geburtstage“. Außerdem stammen sie aus deinen Google-Kontakten auf einer selbst gehosteten Machine und aus einem Datumsfeld namens Birthday bei einer Person im Graph. Wenn noch in keiner dieser Quellen ein Geburtstag gespeichert ist, steht im Ergebnis **Noch keine Geburtstagsinfos** und es wird erklärt, wie du welche hinzufügen kannst.

**Geburtstage aus Facebook importieren**: Sobald Geburtstage eingeschaltet sind, bietet eine Aufgabe an, die Geburtstagsseite von Facebook auszulesen. Tippe auf **Importieren**. The Machine öffnet die Seite in ihrem Browser, scrollt, bis alle Monate geladen sind, und liest Namen und Geburtstage deiner Freunde aus. Anschließend zeigt sie, wie viele Geburtstage gefunden wurden und bei wem Vor- und Nachname mit Personen in deinem Graph übereinstimmen. Namen, die mehreren Personen zugeordnet werden können, werden übersprungen und aufgelistet.

Nur mit **Speichern** werden die Geburtstage auf den Seiten der jeweiligen Personen übernommen. Das gilt auch für ihr Facebook-Profilbild, wenn sie noch kein Foto haben. Ein Geburtstag oder Bild, das du dort selbst festgelegt hast, bleibt erhalten. Ein bereits vorhandenes Foto wird nie ersetzt. Auf Facebook wird nichts gespeichert.

Die Seite wird nicht automatisch erneut ausgelesen. Dafür musst du in der Aufgabe auf **Erneut importieren** tippen. Der Browser muss bei Facebook angemeldet sein. Falls das nicht der Fall ist, tippe in der Aufgabe auf **Bei Facebook anmelden** und melde dich dort an. Sobald du angemeldet bist, wird die Seite automatisch ausgelesen. The Machine meldet dich nie selbst an.

Freunde, die niemand in deinem Graph kennt, werden gezählt und mit einigen Namen aufgeführt. Mit **… als private Kontakte hinzufügen** kannst du sie alle auf einmal hinzufügen, auch nach dem Speichern. Für jede Person werden Name und Geburtstag übernommen, aber nichts wird mit einer Work Fleet geteilt. Personen, deren Name bereits im Graph vorkommt oder die jemand dauerhaft gelöscht hat, werden übersprungen. Geburtstagserinnerungen gibt es weiterhin nur für Personen, denen du selbst schreibst.

Mit **Rückgängig** in der Aufgabe entfernst du genau diese Personen wieder, auch nach **Erneut importieren**.

**Abos und Testphasen** liest einmal im Monat Belege, Rechnungen und Verlängerungsbenachrichtigungen und fasst deine Abos in einer Aufgabe zusammen. Zu jedem Abo stehen die Kosten, der nächste Zahlungstermin und ein Hinweis, wenn eine Testphase endet oder der Preis steigt. Aufgeführt werden nur Abos, bei denen die Routine sicher ist. Wenn sie nichts findet, wird keine Aufgabe erstellt.

Wähle für jedes Abo **Behalten** oder **Kündigen**. Bei einem Abo, das du behältst, wirst du nicht erneut gefragt, es sei denn, der Preis ändert sich. **Kündigen** öffnet entweder die Kündigungsseite oder einen Entwurf mit der Bitte um Kündigung. Der Entwurf wird erst gesendet, wenn du ihn selbst abschickst. Zwischen den monatlichen Läufen prüft die Routine täglich und erstellt eine Aufgabe, wenn eine Testphase oder Verlängerung innerhalb von 7 Tagen abgerechnet wird.

**In Kontakt bleiben** erinnert dich von Zeit zu Zeit daran, dich bei einer nahestehenden Person zu melden, aber nur, wenn es einen konkreten Anlass gibt. Auf der Karte wählst du aus einer kurzen Liste aus, mit welchen Personen du selbst über mehrere Monate hinweg in beide Richtungen schreibst. Entferne Personen mit ×.

Eine Erinnerung erscheint nur, wenn du deutlich länger als sonst nicht mit der Person gesprochen hast und es etwas Konkretes zu sagen gibt: Neuigkeiten, die die Person geteilt hat, auch aus der Zusammenfassung auf ihrer Seite, ein noch offenes Versprechen oder eine Nachricht, auf die du nie geantwortet hast.

Bei Neuigkeiten mit einem Datum in der Zukunft, etwa einem Umzug im nächsten Monat, schaut die Routine kurz nach diesem Datum noch einmal nach den neuesten Nachrichten. Das Ergebnis ist eine Aufgabe mit dem Grund und einem kurzen Nachrichtenentwurf in dem Kanal, über den du normalerweise mit der Person sprichst, und in ihrer Sprache. Die Nachricht wird erst gesendet, wenn du sie selbst abschickst. Wenn es nichts zu sagen gibt, wird keine Aufgabe erstellt.

Die Routine sendet höchstens zwei Erinnerungen pro Woche und höchstens eine pro Person und Monat. Personen, mit denen du kürzlich gesprochen hast, werden nicht berücksichtigt. Mit **Nicht nötig** bei einer Erinnerung wartet die Routine länger, bevor sie dich wegen dieser Person wieder erinnert. Jedes Mal wird die Wartezeit länger.

Die Routine sendet nie eine Benachrichtigung und bleibt privat. Sie wird nie mit einer Work Fleet geteilt, stützt sich nie auf Arbeit, also auf Inhalte aus deinen Work-Konten oder auf ein Versprechen oder einen Fakt über die Arbeit, und erstellt den Entwurf, wenn möglich, in einer Unterhaltung außerhalb der Arbeit.

**Gebrauchte Fundstücke** beobachtet eine Suche auf einer Gebrauchtwaren-Plattform wie Marktplaats, Vinted, eBay oder Facebook Marketplace. Suche dort mit den gewünschten Filtern, kopiere die Adresse der Ergebnisse und füge sie nach **Hinzufügen** ein. Wenn du möchtest, kannst du Filter in eigenen Worten ergänzen, zum Beispiel „unter 300, höchstens 30 km entfernt, nicht ‚für Ersatzteile‘“. Jede Suche ist eine eigene Routine. Für eine weitere Suche musst du sie erneut hinzufügen.

Alle 3 Stunden öffnet die Routine die Suche im eigenen Browser von The Machine und sucht nach Angeboten, die sie noch nicht gesehen hat. Preis, Entfernung und ausgeschlossene Wörter werden zuerst mit einfachem Code geprüft.

Jedes neue Angebot, das die Prüfung besteht, wird geöffnet. Deine KI beurteilt den Zustand anhand des Fotos und der Beschreibung sowie den Verkäufer anhand seiner Bewertungen, seiner Bewertungspunktzahl und der Dauer seines Kontos. Gute Angebote kommen in eine gemeinsame Aufgabe. Zu jedem gehören Foto, Titel, Preis und eine kurze Einschätzung. Tippe auf ein Angebot, um es im Browser von The Machine zu öffnen.

Solange die Aufgabe offen ist, werden neue Fundstücke oben hinzugefügt, die Anzahl steigt und du erhältst erneut eine Benachrichtigung, denn gute Angebote sind schnell weg. Markiere die Aufgabe als erledigt, damit das nächste Fundstück eine neue Aufgabe erhält. Wenn ein Lauf nichts Gutes findet, ändert sich nichts.

Die Routine geht sparsam und rücksichtsvoll vor: Pro Lauf wird die Suche einmal gelesen und es werden höchstens 6 Angebote mit einer Pause dazwischen geöffnet. Über alle deine Suchen hinweg werden höchstens 40 Angebote pro Tag geprüft. Jede Prüfung besteht aus einer kurzen Frage an deine KI und einem Foto. Beim ersten Lauf werden die neuesten Angebote geprüft und die übrigen als bereits gesehen erfasst. Spätere Läufe zeigen daher nur neue Angebote.

Wenn die Website eine Anmeldung verlangt, eine Roboterprüfung anzeigt oder das Auslesen verhindert, steht es in einer Aufgabe. Mit **Öffnen** kannst du die Seite im Browser von The Machine ansehen. Melde dich dort selbst an oder löse die Prüfung. Beim nächsten Lauf wird die Seite erneut ausgelesen. The Machine meldet dich nie selbst an und löst keine Prüfungen für dich. Sie kontaktiert auch keine Verkäufer, gibt keine Gebote ab und kauft nichts.

Mit **Suche ändern** auf der Karte der Routine kannst du eine neue Adresse oder andere Filter eingeben. Mit **Zeitpunkt ändern** kannst du einen anderen Rhythmus festlegen, zum Beispiel „alle 6 Stunden“.

**Nachbestellungen** liest Bestellbestätigungen von Online-Shops in deinen Mails und erkennt, was du regelmäßig kaufst, zum Beispiel Kaffee, Tierfutter oder Vitamine. Wenn es wahrscheinlich wieder Zeit für einen Kauf ist, erstellt die Routine eine Aufgabe mit dem Artikel, dem Shop, dem letzten Preis und dem letzten Kaufdatum. **Im Store öffnen** bringt dich zur Seite des Shops, wo du den Artikel selbst kaufen kannst. Für dich wird nichts gekauft.

Die Routine braucht mindestens drei Bestellungen desselben Artikels in gleichmäßigen Abständen. Deshalb wird für einen einmaligen Kauf oder eine ungewöhnlich lange Pause keine Aufgabe erstellt. Zurzeit liest sie nur Shops, die Shopify verwenden. Deine KI liest pro Lauf nur neue Bestellmails dieser Shops und stellt dazu eine kurze Frage. Diese Aufgaben lösen nie eine Benachrichtigung aus. Wenn du den Artikel erneut bestellst, wird die offene Aufgabe geschlossen.

Solange die Routine einer Vorlage deren Formulierung beibehält, läuft sie mit eigenem Code und ohne deinen KI-Tarif. Spam aufräumen listet neue Mails unbekannter Absender zunächst mit Code auf und stellt deiner KI nur dann eine kurze Frage, wenn es neue Mails gibt. In Kontakt bleiben fragt nur nach den ein oder zwei ausgewählten Personen. Wenn du die Formulierung änderst, läuft die Routine wie jede andere mit deinen eigenen Worten.

Newsletter aufräumen und Spam aufräumen enden weiterhin mit einer Aufgabe, in der du für jede Mail eine Auswahl triffst. Eine bearbeitete Geburtstagsroutine zeigt ihr Ergebnis und höchstens einen Entwurf, statt eine Aufgabe pro Person zu erstellen. Mit **Zurück zur Vorlage** unter **Bearbeiten** setzt du die ursprüngliche Formulierung wieder ein.

## Was eine Routine macht

Zur festgelegten Zeit liest deine Machine, was sie braucht, zum Beispiel deine Nachrichten, Termine und den Graph, und zeigt das Ergebnis auf der Seite „Routinen“ an. Jedes Ergebnis ist **Bereit**, **Nichts Neues** mit einer Begründung oder **Hat nicht geklappt** mit einer Begründung. Ein Lauf, der ohne Ergebnis endet, gilt als fehlgeschlagen und niemals als abgeschlossen.

Routinen lesen nur: deine Nachrichten, Webseiten, GitHub und Websites wie X im Browser. Sie senden keine Nachrichten, antworten nicht, veröffentlichen nichts und ändern nichts. Sie öffnen Seiten, die sie in den gelesenen Inhalten oder über eine Suche gefunden haben, sowie einfache Webadressen und bekannte Websites. Sie öffnen nie eine Adresse, die so erstellt wurde, dass sie gelesene Inhalte überträgt. Nur eine Vorlage ändert Mails, und auch das nur, wenn du es in der zugehörigen Aufgabe bestätigst.

Wenn eine Routine etwas veröffentlichen oder eine Nachricht senden soll, erledigt sie alles bis zu diesem Schritt und zeigt den Entwurf an, zum Beispiel **Würde auf X veröffentlichen:**. Nach einem echten Lauf erhältst du den Entwurf als Aufgabe zur Freigabe. Bei einem Testlauf wird er nur angezeigt.

Der Name beschreibt, worum es geht und wo das Ergebnis landet. Unter dem Namen öffnet **Aus deiner Routine** die Routine. Die Schaltfläche nennt den jeweiligen Schritt, zum Beispiel **Beitrag vorbereiten**. Damit wird der Beitrag vorbereitet, aber nicht veröffentlicht. Du veröffentlichst ihn über das Ergebnis. Wenn The Machine ihn nicht für dich veröffentlichen kann, öffnet die Schaltfläche dort die Seite, auf der du es tun kannst.

Die Aufgabe wird im Bereich des Kontos erstellt, von dem aus etwas gesendet wird, zum Beispiel unter „Arbeit“ für das X-Konto deines Unternehmens. Du musst sie daher nie verschieben.

Ein Lauf kann [Skills](skills.md) verwenden, die eingeschaltet sind. Welche verwendet werden, richtet sich nach der Aufgabe der Routine. Nur passende Skills werden vollständig gelesen. Das Ergebnis führt sie unter **Verwendet:** auf. Ein Skill sorgt nie dafür, dass eine Routine etwas sendet oder ändert.

Deine Routinen findest du unter **Deine Routinen**, unterhalb etwaiger Vorschläge. Lange Ergebnisse werden zunächst als kurze Vorschau angezeigt. Mit **Mehr anzeigen** oder durch Tippen darauf öffnest du das vollständige Ergebnis.

Jeder Lauf kennt das vorherige Ergebnis und kann daher angeben, was sich seitdem geändert hat.

Nach einem erfolgreichen Lauf kann deine Machine selbst ein Rezept für wiederkehrende Leseaufgaben erstellen, zum Beispiel dafür, welche Mails oder GitHub-Änderungen geprüft werden sollen. Bei den nächsten Läufen werden diese zuerst mit einfachem Code gelesen. Die KI wählt dann nur noch das Wichtige aus und formuliert es mit weniger Tokens. Ein Rezept liest nur. Wenn es nicht mehr funktioniert, liest die Routine die Inhalte selbst und korrigiert das Rezept. Das Rezept wird im Menü ⋯ unter **Erweitert: Skriptschritte** angezeigt.

## Versäumte Tage

Wenn deine Machine ausgeschaltet oder beschäftigt war, werden versäumte Läufe nicht nachgeholt. Nur der neueste Lauf wird einmal ausgeführt. Jedes Datum wird nur einmal ausgeführt, auch nach einem Neustart.

Routinen laufen nacheinander und warten, wenn das Nutzungslimit deines KI-Tarifs niedrig ist, wie bei allen Hintergrundaufgaben. Mit **Jetzt ausführen** startest du die Routine sofort. Das Ergebnis erscheint auf der Karte, sobald es bereit ist.

## Ändern oder beenden

Diese Optionen findest du im Menü ⋯ der Routine. Mit **Bearbeiten** änderst du den Namen und die Aufgabe. Der Zeitplan und die bisherigen Ergebnisse bleiben erhalten. Mit **Zeitpunkt ändern** legst du einen neuen Rhythmus in eigenen Worten fest, zum Beispiel „jeden Werktag um 8 Uhr“. Bei beiden Optionen kannst du **Speichern** oder **Abbrechen** wählen. Am Computer kannst du auch mit Esc oder durch einen Klick außerhalb abbrechen.

Unter **Bearbeiten** führt **Ausprobieren** die neue Formulierung einmal aus und zeigt dort das Ergebnis. Die Routine bleibt unverändert, bis du auf **Speichern** tippst.

Mit **Pausieren** stoppst du die Läufe, bis du auf der Karte **Fortsetzen** wählst. Pausierte Routinen warten unter **Pausiert**, unterhalb deiner Routinen. Während der Pause versäumte Läufe werden später nicht ausgeführt. Mit **Stoppen** beendest du eine Routine endgültig.

Es können bis zu 20 Routinen gespeichert werden, auch pausierte. Beende eine Routine, um eine weitere hinzuzufügen.

Wenn du bei einer Aufgabe der Routine **Änderungen anfragen** wählst oder in ihrem Chat etwas schreibst, das für alle künftigen Läufe gelten soll, etwa „nie Emojis verwenden“, bietet die Aufgabe **Auch die Routine ändern** an. Die Option erscheint sowohl in der Aufgabe als auch im Chat unter der Antwort. Sie zeigt, was an der Formulierung der Routine geändert wird. Die Routine wird erst geändert, wenn du auf **Ändern** tippst. Mit **So lassen** bleibt sie unverändert. Wenn du nur den Entwurf korrigierst, wird diese Option nicht angeboten.

## Erweitert: Skriptschritte

Du brauchst keine Skripte: Beschreibe in eigenen Worten, was eine Routine tun soll, und deine Machine findet den Rest heraus.

Für erfahrene Nutzer kann eine Routine auch eigene Befehle auf deiner Machine ausführen. Wähle dazu im Menü ⋯ **Erweitert: Skriptschritte**. **Bearbeiten** wird erst angezeigt, wenn die Routine Skriptschritte enthält. Mit **Daten holen** wird zuerst ein Befehl ausgeführt, und zwar in seinem Ordner oder, wenn keiner angegeben ist, in deinem Home-Ordner. Der Befehl läuft höchstens so viele Sekunden wie angegeben. Seine Ausgabe wird an den Lauf übergeben. Ohne weitere Formulierung wird die Ausgabe selbst zum Ergebnis.

Mit **Prüfung** wird das Ergebnis nach dem Lauf als Eingabe übergeben. Wenn der Befehl mit einem Fehler endet, zeigt der Lauf **Hat nicht geklappt** und die Ausgabe der Prüfung. Scheitert ein Befehl zum Datenholen, wird das genauso angezeigt.

Ein Befehl besteht aus einer Zeile und wird ohne Shell ausgeführt. Pipes und Variablen sind nicht möglich. Skriptschritte gehören dir und sind nur auf deinem Dashboard eingerichtet. Bei einem Testlauf oder mit **Ausprobieren** wird auch der Befehl zum Datenholen ausgeführt und entsprechend angezeigt. Dabei wird weiterhin nichts gesendet oder gespeichert. Eine Routine sendet nie etwas. Ein Skriptschritt sollte daher nur lesen.

## Von deinen OpenClaw-Jobs

Wenn du früher geplante Jobs in OpenClaw eingerichtet hast, liest deine Machine sie aus, ändert sie aber nie. Passende Jobs werden unter **Vorgeschlagen** als Routinen angeboten. Jeder Job wurde einmal ausgeführt, damit du ein echtes Ergebnis siehst.

Deine Korrekturen am Job werden übernommen, gesendete oder veröffentlichte Inhalte dagegen ausgelassen. Wenn ein Job ein Skript ausgeführt oder die von einem Skript-Job gesammelten Daten gelesen hat, wird das als **Daten holen** übernommen. Mit **Hinzufügen** wird daraus eine Routine. Mit **Nein danke** wird dieser Job nicht erneut angeboten. Ein Job, der dich an eine Aufgabe erinnert hat, wird stattdessen unter „Aufgaben“ als Angebot für eine wiederkehrende Aufgabe angezeigt.

Bevor du einen Vorschlag hinzufügst, kannst du ihn über **Bearbeiten** und **Zeitpunkt ändern** im Menü ⋯ wie jede andere Routine anpassen. Mit **Erneut ausführen** startest du den Job jetzt mit seiner aktuellen Formulierung, um neuere Ergebnisse zu sehen, zum Beispiel nach einem ruhigen Wochenende. Er liest nur, läuft einmal pro Tipp und ersetzt das bisherige Ergebnis durch das neue.

Es warten höchstens drei Vorschläge gleichzeitig. Nach einer Woche erfolgreicher Läufe fragt die Routine **Den alten OpenClaw-Job ausschalten?**. Sie wird erst ausgeschaltet, wenn du auf **Ausschalten** tippst. Du kannst sie in OpenClaw wieder einschalten. Mit **Behalten** laufen beide weiter.

## Aus dem, was du tust

Deine Machine erkennt auch regelmäßige Aufgaben, die du erledigst, und schlägt sie unter **Vorgeschlagen** als Routine vor, auch ohne OpenClaw. Sie achtet auf Folgendes:

- dieselbe Anfrage mindestens drei Mal hintereinander, zum Beispiel „offene Support-Tickets zusammenfassen“ jeden Montag;
- eine regelmäßig gesendete Mail, zum Beispiel ein wöchentlicher Bericht an dein Team;
- Newsletter und Update-Mails, die jede Woche wiederkommen;
- einen stark frequentierten Slack-Kanal, in den andere jede Woche schreiben;
- Mails, die du einzeln immer an dieselbe Person weiterleitest, zum Beispiel Schul- und Vereinsmails an deine Partnerin oder deinen Partner. Eine wöchentliche Zusammenfassung erspart dir das Weiterleiten;
- dieselbe Anfrage, die du regelmäßig beantwortest, zum Beispiel eine monatliche Freigabe für dieselbe Person.

Jeder Vorschlag erklärt, was die Routine erkannt hat, zum Beispiel „4 Mal hintereinander angefragt“ oder „6 Mails in 3 Wochen an Sam weitergeleitet“. Außerdem wurde er einmal ausgeführt, damit du ein echtes Ergebnis siehst. Denk zum Beispiel an eine Team-Zusammenfassung, eine kurze Übersicht vor einem wöchentlichen Gespräch, eine Support- oder Entwicklungszusammenfassung, einen Überblick über deine Kennzahlen oder eine Zusammenfassung deiner Newsletter.

Vorgeschlagen werden nur Dinge, die spezifisch für dich und eindeutig nützlich sind. Eine Nachrichtenzusammenfassung umfasst zum Beispiel nur deine eigenen Newsletter, nie allgemeine Nachrichten. Wenn nichts passt, gibt es keinen Vorschlag.

Die Routine prüft höchstens einmal am Tag und erstellt höchstens einen neuen Vorschlag pro Woche. Benachrichtigungen werden nicht gesendet. Mit **Nein danke** wird der Vorschlag nicht erneut angezeigt. Weiterleitungen und Antworten bleiben bei dem Konto, von dem sie gesendet wurden. Arbeitliches und Privates werden also nicht vermischt. Alles bleibt auf deiner Machine. Eine Aufgabe, die du regelmäßig abschließt, wird stattdessen als Angebot für eine wiederkehrende Aufgabe angezeigt.

## Routinen und wiederkehrende Aufgaben

Eine [wiederkehrende Aufgabe](recurring.md) erinnert dich daran, etwas zu tun. Eine Routine ist Arbeit, die deine Machine selbstständig erledigt und dir anschließend zeigt. Nutze eine wiederkehrende Aufgabe für „am Ersten die Miete bezahlen“ und eine Routine für „jeden Freitag sagen, welche Deals ins Stocken geraten sind“.
