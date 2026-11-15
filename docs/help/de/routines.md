---
title: Routinen
area: cards
summary: Aufgaben, die deine Machine regelmäßig selbst erledigt, zum Beispiel jeden Montag deine offenen Deals zusammenfassen. Sie liest nur.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours
translated: 3e6d9d8d446a5dde
---
## Eine Routine erstellen

Öffne **Routinen** in der Seitenleiste und beschreibe in einer Zeile, was sie wann erledigen soll: „jeden Montag um 9 meine offenen Deals zusammenfassen“ oder „jeden Werktagmorgen die E-Mails auflisten, auf die ich noch antworten muss“. Tippe dann auf **Hinzufügen**.

Wenn du keine Uhrzeit angibst, läuft sie um 8:00 Uhr. Maßgeblich ist die Uhr deiner Machine. Beim ersten Durchlauf erhält sie einen kurzen Namen.

Mit **Hinzufügen** wird zuerst ein Testlauf ausgeführt. So siehst du, was dabei herauskommt, bevor du die Routine übernimmst. Es wird nichts gesendet oder gespeichert. Mit **Hinzufügen** läuft die Routine anschließend regelmäßig, mit **Ändern** kannst du andere Formulierungen oder einen neuen Namen ausprobieren, und mit **Abbrechen** verwirfst du sie.

## Vorlagen

Unter **Vorlagen** unten auf der Seite „Routinen“ kannst du mit **Hinzufügen** eine fertige Routine einschalten. Sie läuft sofort einmal und danach jeden Morgen um 7:30 Uhr. Spam aufräumen läuft jede Stunde, Gebrauchte Fundstücke alle 3 Stunden und Abos und Testphasen einmal im Monat. Auf der Karte stehen wie bei jeder Routine die Formulierungen. Mit **Bearbeiten** kannst du sie oder den Namen ändern.

Wenn viele Newsletter eingehen und Newsletter aufräumen ausgeschaltet ist, also 25 oder mehr in einer Woche von mindestens 5 Absendern, wird über deinen Aufgaben angezeigt, wie viele eingegangen sind und was die Routine tun würde. Dort gibt es die Optionen **Einschalten** und **Nein danke**.

Spam aufräumen wird auf dieselbe Weise angeboten, wenn du innerhalb einer Woche mindestens 5 E-Mails von Hand in den Spam verschoben hast. Mit **Einschalten** wird die Routine wie hier mit **Hinzufügen** hinzugefügt. Wenn du **Nein danke** auswählst, wird sie nicht noch einmal angeboten. Eine Vorlage, die du schon einmal hattest, wird ebenfalls nicht erneut angeboten.

Mit **Newsletter aufräumen** wird für jeden Bereich, Arbeit und privat, eine Aufgabe mit den Newslettern des letzten Tages erstellt. Bei jedem Newsletter gibt es die Optionen **Behalten** oder **Abmelden**. Zum Abmelden wird der Ein-Klick-Link des Newsletters verwendet oder, wenn das Senden aktiviert ist, eine Abmelde-E-Mail von deiner Adresse aus verschickt. Andernfalls meldet The Machine dich auf der Website des Newsletters in ihrem eigenen Browser ab. Falls du dich dort anmelden, ein Captcha lösen oder eine Auswahl treffen musst, erledigst du das selbst. In der Zeile steht der Grund. Tippe auf **Abmeldeseite öffnen**, um die Seite aufzurufen.

Quittungen, Bestellungen und Zahlungsbenachrichtigungen werden ausgelassen. E-Mails, die über eine Gruppenadresse wie eine Google Group eingehen, werden unter dem Namen der schreibenden Person aufgeführt. Du wirst damit nie aus der Gruppe abgemeldet. Wenn der Absender keine eigene Abmeldeoption hat, steht in der Zeile **Selbst abmelden**.

Mit **Spam aufräumen** wird für jeden Bereich eine Aufgabe mit E-Mails unbekannter Absender erstellt, die wie Spam aussehen. Bei jeder E-Mail gibt es die Optionen **Spam** oder **Kein Spam**. Outlook verschiebt Spam in den Junk-Ordner, Gmail markiert ihn als Spam. Die Routine prüft jede Stunde, sodass der Spam normalerweise schon erkannt wurde, bevor du ihn siehst. Neuer Spam wird zur selben Aufgabe hinzugefügt, solange sie offen ist.

Wenn Gmail schreibgeschützt verbunden ist, wie auf einer gehosteten Machine, kann die Routine keine E-Mails in den Spam verschieben. In diesem Fall öffnet **Spam** einen Link, über den du die E-Mail in Gmail markieren kannst. The Machine merkt sich den Absender als Spam. Wenn kein E-Mail-Konto verbunden ist, wird bei der Vorlage statt **Hinzufügen** die Option **Mail verbinden** angezeigt.

Als unbekannt gelten Personen, denen du noch nie geschrieben hast. Ein „Re:“ zählt nur dann als Unterhaltung, wenn du selbst in dem Thread geschrieben hast. Wenn eine E-Mail von einem Absender, den du in der Aufgabe oder in deinem Postfach als Spam markiert hast, wieder durchkommt, erscheint sie in der nächsten Aufgabe mit dem Hinweis **Schon einmal als Spam markiert**. E-Mails, die du selbst in den Spam verschoben hast, helfen der Routine ebenfalls dabei, ähnliche E-Mails zu erkennen.

Es ändert sich nichts, bis du es in der Aufgabe bestätigst. Tippe auf einen Absender, um zuerst die E-Mail zu lesen. Sie bleibt ungelesen, und es ändert sich nichts. Bei Spam aufräumen werden Bilder aus dem Web nicht geladen, damit der Absender nicht sieht, dass du die E-Mail geöffnet hast. Absender, zu denen du eine Entscheidung getroffen hast, werden nicht erneut gefragt. An Tagen ohne Newsletter oder Spam wird keine Aufgabe erstellt. Diese Aufgaben senden nie eine Benachrichtigung.

Wenn du bei allen Absendern eine Entscheidung getroffen hast, ist die Aufgabe abgeschlossen und die Option **Als erledigt markieren** erscheint.

Mit **Tägliche Zusammenfassung** erhältst du einmal am Tag eine Aufgabe mit den wenigen Newsletter-Artikeln, die deine Zeit wert sind. Bei jedem Artikel steht in einer Zeile, warum er für dich wichtig ist. Tippe darauf, um die E-Mail zu lesen, oder verwende **In deiner Mail öffnen**. Es werden nur Newsletter berücksichtigt, niemals E-Mails von Personen, Quittungen oder Absendern, von denen du dich abgemeldet hast. Bereits gelesene E-Mails werden ebenfalls ausgelassen. Wenn nichts besonders interessant ist, wird keine Aufgabe erstellt.

Die Routine lernt, was dich interessiert, indem sie berücksichtigt, was du öffnest, mit einem Stern markierst oder ungelesen archivierst, sowie deine Auswahl bei **Mehr davon** und **Weniger davon** für jeden Vorschlag. Die Themen, nach denen sie sucht, stehen auf der Karte der Routine unter **Mehr zu** und **Weniger zu**. Tippe auf ×, um ein Thema zu entfernen, oder füge eigene Themen hinzu. Themen mit gestrichelter Linie hat die Routine selbst erkannt. Eine neue Zusammenfassung ersetzt die offene. Es wird nie eine Benachrichtigung gesendet.

Die Routine liest nur Absender, Betreff und Anfang jedes neuen Newsletters und stellt deiner KI dazu eine kurze Frage pro Tag, damit die Kosten niedrig bleiben. Mit **Zeitpunkt ändern** legst du die Uhrzeit fest. Sobald du die Formulierungen änderst, läuft die Routine wie jede andere nach deinen Vorgaben.

Mit **Geburtstage** wird für jeden engen Kontakt, der heute Geburtstag hat, eine Aufgabe erstellt. Gemeint sind Personen, denen du selbst schreibst, zum Beispiel Freunde, Familie und regelmäßige Kontakte. Für jede Person gibt es einen kurzen Grußentwurf in dem Kanal, über den du normalerweise mit ihr sprichst, zum Beispiel im WhatsApp-Chat oder in deinem E-Mail-Thread, und zwar in ihrer Sprache. Der Gruß wird erst gesendet, wenn du ihn selbst verschickst. An Tagen ohne Geburtstage wird keine Aufgabe erstellt.

Geburtstage stammen aus deinen Kalendern: aus Geburtstagsereignissen und dem Geburtstagskalender von Google, die jeden Morgen gelesen werden, auch wenn sie nicht synchronisiert sind, sowie aus dem Geburtstagskalender von Outlook. Außerdem stammen sie aus deinen Google-Kontakten auf einer selbst gehosteten Machine und aus einem Datumsfeld namens „Birthday“ bei einer Person im Graph. Wenn noch nirgends ein Geburtstag hinterlegt ist, wird im Ergebnis **Noch keine Geburtstagsinfos** angezeigt und erklärt, wie du welche hinzufügen kannst.

**Geburtstage aus Facebook importieren**: Sobald Geburtstage aktiviert ist, bietet eine Aufgabe an, die Geburtstagsseite von Facebook auszulesen. Tippe auf **Importieren**. The Machine öffnet die Seite in ihrem Browser, scrollt, bis alle Monate geladen sind, und liest Namen und Geburtstage deiner Freunde aus. Anschließend zeigt sie an, wie viele Geburtstage gefunden wurden und welche Personen anhand von Vor- und Nachnamen mit Personen in deinem Graph übereinstimmen. Namen, die mehr als eine Person hat, werden übersprungen und aufgelistet.

Nur mit **Speichern** werden die Geburtstage auf den Seiten der jeweiligen Personen übernommen. Außerdem wird das Facebook-Profilbild einer Person hinzugefügt, wenn sie noch kein Foto hat. Ein Geburtstag oder Bild, das du dort festgelegt hast, bleibt erhalten. Ein vorhandenes Foto wird nie ersetzt. Auf Facebook wird nichts gespeichert.

Die Geburtstage werden nicht automatisch erneut ausgelesen. Das geht über **Erneut importieren** in der Aufgabe. Der Browser muss bei Facebook angemeldet sein. Falls das nicht der Fall ist, tippe in der Aufgabe auf **Bei Facebook anmelden** und melde dich dort an. Sobald du angemeldet bist, liest die Routine die Seite automatisch aus. The Machine meldet dich nie selbst an.

Freunde, die niemand in deinem Graph kennt, werden mit einigen Namen gezählt. Mit **… als private Kontakte hinzufügen** kannst du alle auf einmal hinzufügen, auch nach dem Speichern. Für jede Person werden Name und Geburtstag übernommen. Sie werden nie mit einer Work Fleet geteilt. Namen, die bereits jemand in deinem Graph hat, sowie Namen von Personen, die du dauerhaft gelöscht hast, werden übersprungen. Geburtstagserinnerungen gibt es weiterhin nur für Personen, denen du schreibst.

Mit **Rückgängig** in der Aufgabe werden genau diese Personen wieder entfernt, auch nach **Erneut importieren**.

**Abos und Testphasen** liest einmal im Monat deine Quittungen, Rechnungen und Verlängerungsbenachrichtigungen aus und fasst deine Abos in einer Aufgabe zusammen. Für jedes Abo stehen die Kosten, der nächste Abbuchungstermin und ein Hinweis, wenn eine Testphase endet oder der Preis steigt. Aufgeführt werden nur Abos, bei denen die Routine sicher ist. Wenn sie nichts findet, wird keine Aufgabe erstellt.

Wähle für jedes Abo **Behalten** oder **Kündigen**. Zu einem behaltenen Abo wirst du nicht erneut gefragt, solange sich der Preis nicht ändert. Mit **Kündigen** wird die Kündigungsseite geöffnet oder ein Entwurf erstellt, in dem du um die Kündigung bittest. Der Entwurf wird erst gesendet, wenn du ihn verschickst. Zwischen den monatlichen Durchläufen prüft die Routine jeden Tag die Abos und erstellt eine Aufgabe, wenn eine Testphase endet oder eine Verlängerung innerhalb von 7 Tagen ansteht.

Mit **In Kontakt bleiben** wirst du von Zeit zu Zeit daran erinnert, dich bei einer nahestehenden Person zu melden, aber nur, wenn es einen konkreten Anlass gibt. Wähle auf der Karte der Routine aus einer kurzen Liste von Personen aus, mit denen du über mehrere Monate selbst hin und her geschrieben hast. Tippe auf ×, um jemanden zu entfernen.

Eine Erinnerung kommt nur, wenn du dich viel länger als üblich nicht gemeldet hast und es etwas Konkretes zu sagen gibt: Neuigkeiten, die die Person geteilt hat, ein noch offenes Versprechen oder eine Nachricht, die du nie beantwortet hast. Die Aufgabe enthält den Grund und einen kurzen Nachrichtenentwurf in dem Kanal, über den du normalerweise mit der Person sprichst, und zwar in ihrer Sprache. Die Nachricht wird erst gesendet, wenn du sie selbst verschickst. Wenn es nichts zu sagen gibt, wird keine Aufgabe erstellt.

Die Routine sendet höchstens zwei Erinnerungen pro Woche und höchstens eine pro Person und Monat. An Personen, mit denen du dich vor Kurzem unterhalten hast, erinnert sie dich nicht. Mit **Nicht nötig** wird bei einer Erinnerung für diese Person länger gewartet, und mit jeder weiteren Auswahl noch länger. Die Routine sendet nie eine Benachrichtigung und bleibt privat. Sie wird nie mit einer Work Fleet geteilt.

**Gebrauchte Fundstücke** überwacht eine Suche auf einer Gebrauchtwaren-Website wie Marktplaats, Vinted, eBay oder Facebook Marketplace. Suche dort mit den gewünschten Filtern, kopiere die Adresse der Suchergebnisse und füge sie nach **Hinzufügen** ein. Wenn du möchtest, kannst du Filter in eigenen Worten ergänzen, zum Beispiel „unter 300, höchstens 30 km entfernt, keine ‚Ersatzteilspender‘“. Jede Suche ist eine eigene Routine. Füge sie also für jede weitere Suche erneut hinzu.

Alle 3 Stunden öffnet die Routine die Suche im eigenen Browser von The Machine und sucht nach Anzeigen, die sie noch nicht kennt. Preis, Entfernung und ausgeschlossene Begriffe werden zuerst mit einfachem Code geprüft.

Jede neue Anzeige, die die Prüfung besteht, wird geöffnet. Deine KI beurteilt anhand des Fotos und der Beschreibung den Zustand sowie anhand der Bewertungen, der Bewertungspunktzahl und des Alters des Kontos den Verkäufer. Die guten Anzeigen werden in einer Aufgabe gesammelt. Jede Anzeige enthält ein Foto, den Titel, den Preis und eine kurze Einschätzung. Tippe darauf, um die Anzeige im Browser von The Machine zu öffnen.

Solange die Aufgabe offen ist, kommen neue Fundstücke oben hinzu, die Anzahl steigt und du wirst erneut benachrichtigt, denn gute Angebote sind schnell weg. Markiere die Aufgabe als erledigt, damit das nächste Fundstück eine neue Aufgabe erhält. Ein Durchlauf ohne gute Fundstücke ändert nichts.

Die Routine geht sparsam und rücksichtsvoll vor: Sie liest die Suche einmal pro Durchlauf, öffnet höchstens 6 Anzeigen pro Durchlauf und wartet zwischen den Anzeigen. Insgesamt prüft sie höchstens 40 Anzeigen pro Tag über alle deine Suchen hinweg. Bei jeder Prüfung stellt sie deiner KI eine kurze Frage und zeigt ein Foto. Beim ersten Durchlauf prüft sie die neuesten Anzeigen und markiert den Rest als bereits gesehen. Bei späteren Durchläufen werden nur neue Anzeigen berücksichtigt.

Wenn die Website dich auffordert, dich anzumelden, eine Roboterprüfung anzeigt oder das Auslesen blockiert, wird in einer Aufgabe darauf hingewiesen. Tippe auf **Öffnen**, um die Seite im Browser von The Machine anzusehen. Melde dich dort selbst an oder löse die Prüfung. Beim nächsten Durchlauf wird die Seite erneut ausgelesen. The Machine meldet dich nie selbst an und löst keine Prüfungen für dich. Sie kontaktiert auch nie Verkäufer, gibt keine Gebote ab und kauft nichts.

Mit **Suche ändern** auf der Karte der Routine kannst du eine neue Adresse oder andere Filter festlegen. Mit **Zeitpunkt ändern** kannst du einen anderen Rhythmus einstellen, zum Beispiel „alle 6 Stunden“.

Solange die Routine einer Vorlage deren Formulierungen beibehält, läuft sie mit eigenem Code und nicht mit deinem KI-Tarif. Spam aufräumen listet zum Beispiel zuerst neuen Spam von unbekannten Absendern mit Code auf und stellt deiner KI nur dann eine kurze Frage, wenn Spam gefunden wurde. In Kontakt bleiben fragt nur nach den ein oder zwei Personen, die die Routine ausgewählt hat. Ein neuer Name ändert daran nichts. Sobald du die Formulierungen änderst, läuft die Routine wie jede andere nach deinen Vorgaben.

Newsletter aufräumen und Spam aufräumen erstellen weiterhin dieselbe Aufgabe mit einer Auswahl für jede E-Mail. Eine bearbeitete Routine für Geburtstage zeigt ihr Ergebnis und höchstens einen Entwurf an, keine einzelne Aufgabe pro Person. Mit **Zurück zur Vorlage** in **Bearbeiten** werden die ursprünglichen Formulierungen wiederhergestellt.

## Was eine Routine macht

Zur festgelegten Zeit liest deine Machine, was sie braucht, zum Beispiel deine Nachrichten, Termine und den Graph, und zeigt das Ergebnis auf der Seite „Routinen“ an. Jedes Ergebnis ist entweder **Bereit**, **Nichts Neues** mit einer Erklärung oder **Hat nicht geklappt** mit einer Erklärung. Ein Durchlauf, der ohne Ergebnis endet, gilt als fehlgeschlagen, niemals als erledigt.

Routinen lesen nur: deine Nachrichten, Webseiten, GitHub und Websites wie X im Browser. Sie senden oder beantworten keine Nachrichten, posten nichts und ändern nichts. Nur eine Vorlage kann E-Mails ändern, und auch dann nur, was du in der zugehörigen Aufgabe bestätigst.

Wenn eine Routine mit einem Beitrag oder einer Nachricht enden soll, erledigt sie alles bis zu diesem Schritt und zeigt den Entwurf an, zum Beispiel **Würde auf X posten:**. Nach einem echten Durchlauf erhältst du dafür eine Aufgabe, die du bestätigen kannst. Ein Testlauf zeigt den Entwurf nur an. Der Name beschreibt, worum es geht und wo der Inhalt veröffentlicht wird. Der Name der Schaltfläche nennt den Schritt, zum Beispiel **Posten**. Mit **Aus deiner Routine** darunter öffnest du die Routine.

Die Aufgabe wird im Bereich des Kontos angezeigt, von dem aus sie verschickt wird, zum Beispiel unter „Arbeit“ für das X-Konto deines Unternehmens. Sie fordert dich also nie auf, sie zu verschieben.

Ein Durchlauf kann deine aktivierten [Skills](skills.md) berücksichtigen, die anhand der Aufgabe der Routine ausgewählt werden. Nur passende Skills werden vollständig gelesen. Die verwendeten Skills stehen im Ergebnis unter **Verwendet:**. Ein Skill kann eine Routine nie dazu bringen, etwas zu senden oder zu ändern.

Deine Routinen stehen unter **Deine Routinen**, unterhalb aller Vorschläge. Lange Ergebnisse werden auf eine kurze Vorschau gekürzt. Mit **Mehr anzeigen** oder durch Antippen öffnest du das vollständige Ergebnis.

Bei jedem Durchlauf wird das letzte Ergebnis berücksichtigt, damit die Routine beschreiben kann, was sich seitdem geändert hat.

Nach einem erfolgreichen Durchlauf kann deine Machine selbst ein Rezept dafür erstellen, wie sie jedes Mal dieselben Informationen liest, zum Beispiel welche E-Mails oder Änderungen in GitHub sie prüfen soll. Bei den nächsten Durchläufen liest sie diese Informationen zuerst mit einfachem Code aus. Die KI sucht dann nur noch heraus, was wichtig ist, und formuliert es mit weniger Tokens. Ein Rezept liest nur. Wenn es nicht mehr funktioniert, liest die Routine die Informationen selbst aus und passt das Rezept an. Das Rezept wird im Menü ⋯ unter **Erweitert: Skriptschritte** angezeigt.

## Verpasste Tage

Wenn deine Machine ausgeschaltet oder beschäftigt war, werden verpasste Durchläufe nicht nachgeholt. Es läuft nur der neueste einmal. Auch nach einem Neustart wird jeder Termin nur einmal ausgeführt.

Routinen laufen nacheinander und warten, wenn dein KI-Tarif nur noch wenig Nutzung zulässt, wie bei allen Hintergrundaufgaben. Mit **Jetzt ausführen** startest du die Routine sofort. Das Ergebnis erscheint auf der Karte, sobald es fertig ist.

## Routine ändern oder stoppen

Diese Optionen findest du im Menü ⋯ der Routine. Mit **Bearbeiten** änderst du den Namen und die Aufgabe. Der Zeitpunkt und die bisherigen Ergebnisse bleiben erhalten. Mit **Zeitpunkt ändern** kannst du einen neuen Rhythmus in eigenen Worten festlegen, zum Beispiel „jeden Werktag um 8“. Beide Optionen haben **Speichern** und **Abbrechen**. Am Computer kannst du auch mit Esc oder einem Klick außerhalb des Fensters abbrechen.

Unter **Bearbeiten** kannst du mit **Ausprobieren** die neuen Formulierungen einmal ausführen und das Ergebnis dort ansehen. Die Routine bleibt unverändert, bis du auf **Speichern** tippst.

Mit **Pausieren** werden die Durchläufe angehalten. Tippe auf der Karte der Routine auf **Fortsetzen**, um sie wieder zu starten. Pausierte Routinen stehen unter deinen Routinen im Abschnitt **Pausiert**. Während der Pause verpasste Durchläufe werden später nicht ausgeführt. Mit **Stopp** beendest du eine Routine endgültig.

Es gibt Platz für bis zu 20 Routinen, auch pausierte zählen mit. Beende eine Routine, um eine weitere hinzuzufügen.

Wenn du bei der Aufgabe einer Routine **Änderungen anfragen** auswählst oder in ihrem Chat schreibst und deine Nachricht für alle zukünftigen Durchläufe gilt, zum Beispiel „nie Emojis verwenden“, bietet dir die Aufgabe **Auch die Routine ändern** an. Die Option erscheint in der Aufgabe und im Chat unter der Antwort. Du siehst, was in den Formulierungen der Routine geändert wird. Die Routine wird erst geändert, wenn du auf **Ändern** tippst. Mit **So lassen** bleibt alles unverändert. Wenn du nur den aktuellen Entwurf korrigieren möchtest, wird diese Option nicht angeboten.

## Erweitert: Skriptschritte

Du brauchst kein Skript. Beschreibe in eigenen Worten, was eine Routine tun soll, und deine Machine findet den Rest heraus.

Für erfahrene Nutzerinnen und Nutzer kann eine Routine auch eigene Befehle auf deiner Machine ausführen. Wähle dafür im Menü ⋯ **Erweitert: Skriptschritte**. **Bearbeiten** zeigt die Skriptschritte erst an, wenn die Routine welche hat. Mit **Daten holen** wird zuerst ein Befehl ausgeführt, und zwar in dessen Ordner, beziehungsweise im persönlichen Ordner, wenn kein Ordner angegeben ist. Die Ausführung ist auf die angegebene Anzahl Sekunden begrenzt. Die Ausgabe des Befehls wird an den Durchlauf übergeben. Wenn keine weiteren Formulierungen angegeben sind, ist die Ausgabe selbst das Ergebnis.

Mit **Prüfung** wird das Ergebnis nach dem Durchlauf als Eingabe übergeben. Wenn der Befehl mit einem Fehler endet, zeigt der Durchlauf **Hat nicht geklappt** zusammen mit der Meldung der Prüfung an. Ein fehlgeschlagener Befehl zum Abrufen von Daten wird auf dieselbe Weise angezeigt.

Ein Befehl muss aus einer Zeile bestehen und wird ohne Shell ausgeführt. Pipes und Variablen sind nicht möglich. Die Skriptschritte gehören dir und werden nur in deinem Dashboard festgelegt. Bei einem Testlauf und bei **Ausprobieren** wird auch der Befehl zum Abrufen von Daten ausgeführt und das Ergebnis angezeigt. Es wird trotzdem nichts gesendet oder gespeichert. Eine Routine sendet nie etwas. Ein Skriptschritt sollte daher nur Daten lesen.

## Aus deinen OpenClaw-Jobs

Wenn du früher in OpenClaw geplante Jobs erstellt hast, liest deine Machine sie aus, ändert sie aber nie. Passende Jobs werden dir unter **Vorgeschlagen** als Routinen angeboten. Jeder Job wurde bereits einmal ausgeführt, sodass du ein echtes Ergebnis siehst.

Korrekturen am Job werden übernommen, gesendete oder veröffentlichte Inhalte ausgelassen. Wenn ein Job ein Skript ausgeführt oder Daten ausgelesen hat, die ein Skript-Job gesammelt hat, wird das Skript als Befehl zum Abrufen von Daten übernommen. Mit **Hinzufügen** wird daraus eine Routine. Mit **Nein danke** wird dieser Job nicht erneut angeboten. Ein Job, der dich an eine Aufgabe erinnert hat, wird stattdessen unter „Aufgaben“ als wiederkehrende Aufgabe angeboten.

Bevor du einen Vorschlag hinzufügst, kannst du ihn wie jede Routine über **Bearbeiten** und **Zeitpunkt ändern** im Menü ⋯ anpassen. Mit **Erneut ausführen** startest du ihn mit den aktuellen Formulierungen sofort, um neuere Ergebnisse zu sehen, zum Beispiel nach einem ruhigen Wochenende. Die Routine liest nur und läuft pro Tippen einmal. Das neue Ergebnis ersetzt das alte.

Es können höchstens drei Vorschläge gleichzeitig auf dich warten. Nach einer Woche mit erfolgreichen Durchläufen fragt die Routine **Den alten OpenClaw-Job ausschalten?**. Der Job wird erst ausgeschaltet, wenn du auf **Ausschalten** tippst. Du kannst ihn in OpenClaw wieder einschalten. Mit **Behalten** laufen beide weiter.

## Aus dem, was du tust

Deine Machine erkennt auch Aufgaben, die du regelmäßig erledigst, und schlägt sie unter **Vorgeschlagen** als Routine vor, auch ohne OpenClaw. Sie sucht nach:

- derselben Anfrage mindestens dreimal hintereinander, zum Beispiel „die offenen Support-Tickets zusammenfassen“ jeden Montag;
- einer E-Mail, die du regelmäßig verschickst, zum Beispiel einem wöchentlichen Bericht an dein Team;
- Newslettern und Update-E-Mails, die jede Woche eingehen;
- einem viel genutzten Slack-Kanal, in dem andere jede Woche schreiben;
- E-Mails, die du einzeln immer an dieselbe Person weiterleitest, zum Beispiel E-Mails von Schule und Verein an deine Partnerin oder deinen Partner. Eine wöchentliche Zusammenfassung erspart dir das Weiterleiten;
- derselben Anfrage, die du regelmäßig beantwortest, zum Beispiel einer monatlichen Genehmigung für dieselbe Person.

Jeder Vorschlag erklärt, was die Routine erkannt hat, zum Beispiel „4-mal hintereinander angefragt“ oder „6 E-Mails in 3 Wochen an Sam weitergeleitet“. Außerdem wurde sie einmal ausgeführt, sodass du ein echtes Ergebnis siehst. Denk zum Beispiel an eine Teamzusammenfassung, eine kurze Übersicht vor einem wöchentlichen Anruf, eine Zusammenfassung für Support oder Entwicklung, einen Überblick über deine Zahlen oder eine Zusammenfassung deiner Newsletter.

Es werden nur Vorschläge gemacht, die speziell für dich geeignet und eindeutig nützlich sind. Eine Nachrichtenzusammenfassung umfasst zum Beispiel nur deine eigenen Newsletter, niemals allgemeine Nachrichten. Wenn nichts passt, gibt es keinen Vorschlag.

Die Routine prüft höchstens einmal am Tag und bringt höchstens einen neuen Vorschlag pro Woche, ohne dich zu benachrichtigen. Mit **Nein danke** wird dieser Vorschlag nicht erneut angezeigt. Weitergeleitete und beantwortete E-Mails bleiben bei dem Konto, von dem sie gesendet wurden. Arbeit und private Nachrichten werden also nicht vermischt. Alles bleibt auf deiner Machine. Eine Aufgabe, die du regelmäßig abschließt, wird stattdessen als wiederkehrende Aufgabe angeboten.

## Routinen und wiederkehrende Aufgaben

Eine [wiederkehrende Aufgabe](recurring.md) erinnert dich daran, etwas zu erledigen. Eine Routine ist eine Aufgabe, die deine Machine selbst ausführt und dir anschließend zeigt. Nutze eine wiederkehrende Aufgabe für „am Ersten die Miete zahlen“ und eine Routine für „jeden Freitag berichten, welche Deals ins Stocken geraten sind“.
