---
title: Routinen
area: cards
summary: Aufgaben, die deine Machine regelmäßig selbst erledigt, zum Beispiel montags eine Zusammenfassung deiner offenen Deals. Sie liest nur.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription
translated: ed2171ef31eb6213
---
## Eine Routine erstellen

Öffne **Routinen** in der Seitenleiste und beschreibe in einer Zeile, was die Routine tun und wann sie laufen soll: „jeden Montag um 9 Uhr meine offenen Deals zusammenfassen“ oder „jeden Werktagmorgen die Mails auflisten, auf die ich noch antworten muss“. Wähle dann **Hinzufügen**.

Ohne Zeitangabe läuft die Routine um 8:00 Uhr. Maßgeblich ist die Uhr deiner Machine. Beim ersten Lauf erhält sie einen kurzen Namen.

Mit **Hinzufügen** wird zuerst ein Testlauf ausgeführt. So siehst du, was dabei herauskommt, bevor du die Routine übernimmst. Dabei wird nichts gesendet oder gespeichert. Mit **Hinzufügen** übernimmst du die Routine und lässt sie regelmäßig laufen. Mit **Ändern** probierst du andere Formulierungen oder einen neuen Namen aus, und mit **Abbrechen** verwirfst du sie.

## Vorlagen

Unter **Vorlagen** am unteren Ende von Routinen kannst du mit **Hinzufügen** eine fertige Routine aktivieren. Sie läuft sofort einmal und danach jeden Morgen um 7:30 Uhr (Spam aufräumen läuft stündlich, Abos und Testphasen einmal im Monat). Auf der Karte steht wie bei jeder Routine, was sie tut. Mit **Bearbeiten** kannst du die Formulierung oder den Namen ändern.

Wenn viele Newsletter eingehen und Newsletter aufräumen deaktiviert ist (mindestens 25 in einer Woche von mindestens 5 Absendern), erscheint über deinen Aufgaben ein Hinweis mit der Anzahl und der Beschreibung der geplanten Aktion. Dazu gibt es **Einschalten** und **Nein danke**.

Spam aufräumen wird auf dieselbe Weise vorgeschlagen, wenn du innerhalb einer Woche mindestens 5 Mails manuell in den Spam verschoben hast. Mit **Einschalten** wird die Vorlage wie hier mit **Hinzufügen** hinzugefügt. Bei **Nein danke** wird sie nicht noch einmal vorgeschlagen. Vorlagen, die du bereits hattest, werden nie wieder vorgeschlagen.

Mit **Newsletter aufräumen** wird für jeden Bereich (Arbeit und Privat) eine Aufgabe mit den Newslettern des letzten Tages erstellt. Für jeden gibt es **Behalten** oder **Abmelden**. Zum Abmelden wird der Ein-Klick-Link der Liste verwendet oder, wenn das Senden aktiviert ist, eine Abmelde-Mail von deiner Adresse gesendet. Andernfalls meldet The Machine dich über die Seite der Liste in ihrem eigenen Browser ab. Wenn du dich dort anmelden, ein Captcha lösen oder eine Auswahl treffen musst, bleibt das dir überlassen. In der Zeile steht der Grund, zusammen mit **Abmeldeseite öffnen**.

Quittungen, Bestellungen und Zahlungsbenachrichtigungen werden ausgelassen. Mails, die über eine Gruppenadresse wie eine Google Group eingegangen sind, werden unter dem Namen des Verfassers aufgeführt. Du wirst dabei nie von der Gruppe abgemeldet. Wenn der Absender keine eigene Abmeldemöglichkeit anbietet, steht in der Zeile **Selbst abmelden**.

Mit **Spam aufräumen** wird für jeden Bereich eine Aufgabe mit Mails unbekannter Absender erstellt, die wie Spam aussehen. Für jede Mail kannst du **Spam** oder **Kein Spam** wählen. Outlook verschiebt Spam in den Junk-Ordner und Gmail markiert ihn als Spam. Die Routine prüft stündlich, damit Spam meist schon erfasst ist, bevor du danach schaust. Neuer Spam wird derselben Aufgabe hinzugefügt, solange sie noch offen ist.

Bei einem schreibgeschützt verbundenen Gmail-Konto, wie auf einer gehosteten Machine, können Mails nicht in den Spam verschoben werden. Dort öffnet **Spam** einen Link, über den du die Mail in Gmail markieren kannst. The Machine merkt sich den Absender als Spam. Wenn kein Mailkonto verbunden ist, wird bei der Vorlage statt **Hinzufügen** die Option **Mail verbinden** angezeigt.

Unbekannt bedeutet, dass du der Person noch nie geschrieben hast. Ein „Re:“ zählt nur dann als Unterhaltung, wenn du in diesem Thread selbst geschrieben hast. Wenn eine Mail von einem Absender, den du in der Aufgabe oder in deinem Postfach als Spam markiert hast, wieder durchkommt, erscheint sie in der nächsten Aufgabe mit dem Hinweis **Schon einmal als Spam markiert**. Mails, die du selbst in den Spam verschoben hast, helfen außerdem dabei, ähnliche Mails zu erkennen.

Es wird nichts geändert, bevor du es in der Aufgabe bestätigst. Tippe auf einen Absender, um die Mail zuerst zu lesen: Sie bleibt ungelesen und es wird nichts geändert. Bei Spam aufräumen werden Bilder aus dem Internet nicht geladen. Der Absender kann also nicht sehen, dass du die Mail geöffnet hast. Absender, für die du dich entschieden hast, werden nicht erneut gefragt. Wenn an einem Tag keine Newsletter oder Spam eingehen, wird keine Aufgabe erstellt. Diese Aufgaben lösen nie eine Benachrichtigung aus.

Sobald du dich für alle Absender entschieden hast, wird die Aufgabe als abgeschlossen angezeigt und enthält **Als erledigt markieren**.

Mit **Tägliche Zusammenfassung** wird einmal täglich eine Aufgabe mit den wenigen Newsletter-Beiträgen erstellt, die sich für dich lohnen. Bei jedem steht in einer Zeile, warum er für dich relevant ist. Tippe auf einen Beitrag, um die Mail zu lesen, oder wähle **In deiner Mail öffnen**. Es werden nur Newsletter berücksichtigt, keine Mails von Personen, Quittungen oder Absender, von denen du dich abgemeldet hast. Bereits gelesene Mails werden ebenfalls ausgelassen. Wenn nichts besonders hervorsticht, wird keine Aufgabe erstellt.

Die Routine lernt, was dich interessiert, anhand der Inhalte, die du öffnest, markierst oder ungelesen archivierst, sowie über **Mehr davon** und **Weniger davon** bei jedem Vorschlag. Die Themen, nach denen sie sucht, stehen auf der Routinenkarte unter **Mehr zu** und **Weniger zu**. Mit × kannst du ein Thema entfernen oder eigene Themen hinzufügen. Gestrichelte Themen hat die Routine selbst gelernt. Eine neue Zusammenfassung ersetzt die noch offene Aufgabe und löst nie eine Benachrichtigung aus.

Die Routine liest nur den Absender, den Betreff und den Anfang jedes neuen Newsletters. Außerdem stellt sie deiner KI dazu einmal täglich eine kurze Frage, damit es günstig bleibt. Mit **Zeitpunkt ändern** legst du die Uhrzeit fest. Sobald du die Formulierung änderst, läuft sie wie jede andere Routine mit deiner eigenen Formulierung.

Mit **Geburtstage** wird für jeden engen Kontakt, der heute Geburtstag hat, eine Aufgabe erstellt. Gemeint sind Personen, denen du selbst schreibst, zum Beispiel Freunde, Familie und regelmäßige Kontakte. Zu jedem Geburtstag gibt es einen kurzen Grußentwurf in dem Kanal, über den ihr normalerweise miteinander sprecht, etwa im WhatsApp-Chat oder im E-Mail-Thread. Der Gruß wird nur gesendet, wenn du ihn selbst abschickst. An Tagen ohne Geburtstage wird keine Aufgabe erstellt.

Geburtstage stammen aus deinen Kalendern (den Geburtstagsterminen und dem Kalender „Geburtstage“ von Google, die jeden Morgen gelesen werden, auch wenn sie nicht synchronisiert sind, sowie dem Kalender „Geburtstage“ von Outlook), aus deinen Google-Kontakten auf einer selbst gehosteten Machine und aus einem Datumsfeld mit dem Namen Birthday bei einer Person im Graph. Wenn noch nirgendwo Geburtstage gespeichert sind, wird als Ergebnis **Noch keine Geburtstagsinfos** angezeigt und erklärt, wie du welche hinzufügen kannst.

**Geburtstage aus Facebook importieren**: Sobald Geburtstage aktiviert ist, bietet eine Aufgabe an, die Geburtstagsseite von Facebook auszulesen. Tippe auf **Importieren**. The Machine öffnet die Seite in ihrem Browser, scrollt, bis alle Monate geladen sind, und liest den Namen und Geburtstag jedes Freundes aus. Sie zeigt an, wie viele Geburtstage gefunden wurden und welche Personen anhand ihres Vor- und Nachnamens mit Personen in deinem Graph übereinstimmen. Namen, die mehreren Personen zugeordnet werden können, werden ausgelassen und aufgelistet.

Nur mit **Speichern** werden die Geburtstage auf den Seiten der einzelnen Personen gespeichert. Außerdem wird das Facebook-Profilbild einer Person gespeichert, wenn sie noch kein Foto hat. Ein Geburtstag oder Bild, den oder das du dort selbst einträgst, bleibt erhalten. Ein bereits vorhandenes Foto wird nie ersetzt. Auf Facebook wird nichts gespeichert.

Der Import wird nicht automatisch wiederholt. Das geht über **Erneut importieren** in der Aufgabe. Im Browser musst du bei Facebook angemeldet sein. Falls du noch nicht angemeldet bist, tippe in der Aufgabe auf **Bei Facebook anmelden** und melde dich dort an. Sobald du angemeldet bist, wird die Seite automatisch ausgelesen. The Machine meldet dich nie selbst an.

Freunde, die niemandem in deinem Graph zugeordnet werden können, werden mit einigen Namen aufgelistet. Mit **… als persönliche Kontakte hinzufügen** kannst du sie alle auf einmal hinzufügen, auch nach dem Speichern. Die Kontakte erhalten jeweils ihren Namen und Geburtstag und werden nie mit einer Work Fleet geteilt. Ein Name, der bereits einer Person in deinem Graph zugeordnet ist oder früher zu einer dauerhaft gelöschten Person gehörte, wird ausgelassen. Geburtstagsbenachrichtigungen gibt es weiterhin nur für Personen, denen du schreibst.

Mit **Rückgängig** in der Aufgabe werden genau diese Personen wieder entfernt, auch nach **Erneut importieren**.

Mit **Abos und Testphasen** werden einmal im Monat deine Quittungen, Rechnungen und Verlängerungsbenachrichtigungen gelesen und deine Abos in einer Aufgabe zusammengefasst. Darin stehen die Kosten, der nächste Abbuchungstermin und ein Hinweis, wenn eine Testphase endet oder der Preis steigt. Aufgeführt werden nur Abos, bei denen sich die Routine sicher ist. Wenn sie nichts findet, wird keine Aufgabe erstellt.

Wähle für jedes Abo **Behalten** oder **Kündigen**. Nach **Behalten** wird nicht erneut nachgefragt, außer der Preis ändert sich. Mit **Kündigen** wird die Kündigungsseite geöffnet oder ein Entwurf erstellt, in dem um die Kündigung gebeten wird. Der Entwurf wird nur gesendet, wenn du ihn selbst abschickst. Zwischen den monatlichen Läufen prüft die Routine jeden Tag, ob eine Testphase oder Verlängerung innerhalb der nächsten 7 Tage abgebucht wird. In diesem Fall wird eine Aufgabe erstellt.

Solange die Routine einer Vorlage deren Formulierung beibehält, läuft sie mit eigenem Code und ohne deinen KI-Tarif. (Spam aufräumen listet im Code zuerst neue Mails von unbekannten Absendern auf und stellt deiner KI nur dann eine kurze Frage, wenn es solche Mails gibt.) Ein neuer Name ändert daran nichts. Sobald du die Formulierung änderst, läuft die Routine wie jede andere mit deiner eigenen Formulierung.

Newsletter aufräumen und Spam aufräumen führen weiterhin zu derselben Aufgabe mit einer Auswahl für jede Mail. Eine bearbeitete Routine für Geburtstage liefert ihr Ergebnis und höchstens einen Entwurf, keine eigene Aufgabe pro Person. Mit **Zurück zur Vorlage** unter **Bearbeiten** wird die ursprüngliche Formulierung wiederhergestellt.

## Was eine Routine tut

Zur festgelegten Zeit liest deine Machine, was sie braucht, zum Beispiel deine Nachrichten, Termine und den Graph, und stellt das Ergebnis auf der Routinen-Seite bereit. Jedes Ergebnis ist mit **Bereit**, **Nichts Neues** (mit Begründung) oder **Hat nicht geklappt** (mit Begründung) gekennzeichnet. Ein Lauf, der ohne Ergebnis endet, gilt als fehlgeschlagen, nicht als erledigt.

Routinen lesen nur: deine Nachrichten, Webseiten, GitHub und Seiten wie X im Browser. Sie senden, beantworten oder veröffentlichen nichts und ändern nichts. Nur eine Vorlage kann Mails ändern, und auch dann nur, was du in ihrer Aufgabe bestätigst.

Wenn eine Routine mit einem Beitrag oder einer Nachricht enden soll, führt sie alle Schritte bis dahin aus und zeigt den Entwurf, zum Beispiel **Würde auf X posten:**. Nach einem tatsächlichen Lauf erhältst du ihn als Aufgabe zur Freigabe. Bei einem Testlauf wird er nur angezeigt. Der Name der Aufgabe beschreibt, worum es geht und wo sie veröffentlicht wird. Die Schaltfläche nennt den Schritt, zum Beispiel **Posten**, und über **Aus deiner Routine** darunter öffnest du die Routine.

Die Aufgabe wird im Bereich des Kontos angezeigt, von dem aus sie gesendet wird, zum Beispiel unter Arbeit für das X-Konto deines Unternehmens. Du musst sie also nie verschieben.

Ein Lauf kann den aktivierten [Skills](skills.md) folgen, die anhand der Aufgabe der Routine ausgewählt werden. Nur passende Skills werden vollständig gelesen. Die verwendeten Skills stehen unter **Verwendet:**. Ein Skill kann eine Routine nie dazu bringen, etwas zu senden oder zu ändern.

Deine Routinen stehen unter **Deine Routinen**, unterhalb aller Vorschläge. Ein langes Ergebnis wird zu einer kurzen Vorschau eingeklappt. Mit **Mehr anzeigen** oder durch Tippen darauf kannst du es öffnen.

Jeder Lauf kennt das letzte Ergebnis und kann deshalb sagen, was sich seitdem geändert hat.

Nach einem erfolgreichen Lauf kann deine Machine selbst eine Anleitung für wiederkehrende Leseaufgaben erstellen, zum Beispiel dafür, welche Mails oder GitHub-Änderungen sie ansehen soll. Bei den nächsten Läufen werden diese zuerst mit einfachem Code gelesen. Die KI wählt dann nur noch aus, was wichtig ist, und formuliert es. So werden weniger Tokens benötigt. Eine Anleitung liest nur. Wenn sie nicht mehr funktioniert, liest die Routine die Daten selbst und korrigiert die Anleitung. Sie erscheint im Menü ⋯ unter **Erweitert: Skriptschritte**.

## Verpasste Tage

Wenn deine Machine ausgeschaltet oder beschäftigt war, werden verpasste Läufe nicht nachgeholt. Es läuft nur der neueste verpasste Lauf, und zwar einmal. Jedes Datum wird nur einmal ausgeführt, auch nach einem Neustart.

Routinen laufen nacheinander und warten, wenn das Nutzungsvolumen deines KI-Tarifs gering ist, wie bei allen Hintergrundaufgaben. Mit **Jetzt ausführen** startest du die Routine sofort. Sobald das Ergebnis fertig ist, erscheint es auf der Karte.

## Ändern oder beenden

Diese Optionen findest du im Menü ⋯ der Routine. Mit **Bearbeiten** änderst du den Namen und die Aufgabe. Der Zeitpunkt und die bisherigen Ergebnisse bleiben erhalten. Mit **Zeitpunkt ändern** legst du einen neuen Rhythmus in eigenen Worten fest, zum Beispiel „jeden Werktag um 8 Uhr“. Für beides gibt es **Speichern** und **Abbrechen**. Am Computer kannst du auch mit Esc oder durch einen Klick außerhalb des Menüs abbrechen.

Unter **Bearbeiten** kannst du mit **Ausprobieren** die neue Formulierung einmal ausführen und das Ergebnis dort ansehen. Die Routine bleibt unverändert, bis du **Speichern** wählst.

Mit **Pausieren** werden die Läufe angehalten, bis du auf der Karte **Fortsetzen** wählst. Pausierte Routinen stehen unter **Pausiert**, unterhalb deiner Routinen. Während der Pause verpasste Läufe werden danach nicht nachgeholt. Mit **Stopp** beendest du eine Routine endgültig.

Es können höchstens 20 Routinen angelegt werden, einschließlich pausierter Routinen. Beende eine Routine, um eine weitere hinzuzufügen.

Wenn du bei der Aufgabe einer Routine **Änderungen anfragen** wählst oder in ihrem Chat schreibst und deine Nachricht für jeden Lauf gelten soll, zum Beispiel „nie Emojis verwenden“, bietet dir die Aufgabe die Option **Auch die Routine ändern**. Du findest sie in der Aufgabe und im Chat unter der Antwort. Es wird angezeigt, was sich an der Formulierung der Routine ändert. Die Routine wird erst geändert, wenn du auf **Ändern** tippst. Mit **So lassen** bleibt sie unverändert. Wenn du nur den Entwurf anpassen möchtest, wird diese Option nicht angeboten.

## Erweitert: Skriptschritte

Du brauchst kein Skript: Beschreibe in eigenen Worten, was eine Routine tun soll, und deine Machine kümmert sich um den Rest.

Für fortgeschrittene Nutzer kann eine Routine auch eigene Befehle auf deiner Machine ausführen. Wähle dazu im Menü ⋯ **Erweitert: Skriptschritte**. **Bearbeiten** wird erst angezeigt, wenn die Routine Skriptschritte enthält. Mit **Daten holen** wird zuerst ein Befehl ausgeführt, und zwar in seinem Ordner (bei leerem Feld in deinem Home-Ordner) und höchstens für die angegebene Anzahl Sekunden. Die Ausgabe wird an den Lauf weitergegeben. Wenn keine weiteren Anweisungen vorhanden sind, ist die Ausgabe das Ergebnis.

Mit **Prüfung** wird das Ergebnis nach dem Lauf als Eingabe übergeben. Wird der Befehl mit einem Fehler beendet, zeigt der Lauf **Hat nicht geklappt** und den Text der Prüfung an. Ein fehlgeschlagener Befehl zum Datenholen wird auf dieselbe Weise angezeigt.

Ein Befehl muss aus einer Zeile bestehen und wird ohne Shell ausgeführt. Pipes und Variablen sind nicht möglich. Skriptschritte gehören dir und können nur in deinem Dashboard festgelegt werden. Auch ein Testlauf und **Ausprobieren** führen den Befehl zum Datenholen aus und zeigen das an. Dabei wird trotzdem nichts gesendet oder gespeichert. Eine Routine sendet nie etwas. Skriptschritte sollten deshalb nur lesen.

## Aus deinen OpenClaw-Jobs

Wenn du früher in OpenClaw geplante Jobs erstellt hast, liest deine Machine sie aus. Sie ändert sie nie, sondern bietet passende Jobs unter **Vorgeschlagen** als Routinen an. Jeder Job wurde einmal ausgeführt, damit du ein echtes Ergebnis siehst.

Deine Änderungen am Job bleiben erhalten, während gesendete oder veröffentlichte Inhalte ausgelassen werden. Wenn ein Job ein Skript ausgeführt oder die Ergebnisse eines Skript-Jobs gelesen hat, wird dieses Skript als Daten holen übernommen. Mit **Hinzufügen** wird daraus eine Routine. Mit **Nein danke** wird der Job nie wieder vorgeschlagen. Wenn ein Job dich an etwas erinnert hat, wird er stattdessen unter Aufgaben als wiederkehrende Aufgabe angeboten.

Bevor du einen Vorschlag hinzufügst, kannst du ihn über **Bearbeiten** und **Zeitpunkt ändern** im Menü ⋯ wie jede andere Routine anpassen. Mit **Erneut ausführen** startest du ihn jetzt mit der aktuellen Formulierung, um neuere Ergebnisse zu sehen, zum Beispiel nach einem ruhigen Wochenende. Der Job liest nur und wird bei jedem Tippen einmal ausgeführt. Das neue Ergebnis ersetzt das alte.

Es können höchstens drei Vorschläge gleichzeitig ausstehen. Nach einer Woche erfolgreicher Läufe fragt die Routine **Den alten OpenClaw-Job ausschalten?**. Sie wird nur ausgeschaltet, wenn du auf **Ausschalten** tippst. In OpenClaw kannst du sie wieder einschalten. Mit **Behalten** laufen beide weiter.

## Aus deinen Aktivitäten

Deine Machine erkennt auch Aufgaben, die du regelmäßig erledigst, und bietet sie unter **Vorgeschlagen** als Routine an, auch ohne OpenClaw. Sie sucht nach Folgendem:

- derselben Anfrage, die du mindestens dreimal hintereinander gestellt hast, zum Beispiel „offene Support-Tickets zusammenfassen“ jeden Montag;
- einer Mail, die du regelmäßig sendest, zum Beispiel einem wöchentlichen Bericht an dein Team;
- Newslettern und Update-Mails, die jede Woche wiederkommen;
- einem stark frequentierten Slack-Kanal, in den andere jede Woche schreiben;
- Mails, die du einzeln immer an dieselbe Person weiterleitest, zum Beispiel Schul- und Vereinsmails an deine Partnerin oder deinen Partner. Eine wöchentliche Zusammenfassung erspart dir das Weiterleiten;
- derselben Anfrage, die du regelmäßig beantwortest, zum Beispiel einer monatlichen Freigabe für dieselbe Person.

Jeder Vorschlag nennt, was die Routine erkannt hat, zum Beispiel „Viermal hintereinander angefragt“ oder „Sechs Mails in drei Wochen an Sam weitergeleitet“. Jeder Vorschlag wurde einmal ausgeführt, damit du ein echtes Ergebnis siehst. Denk zum Beispiel an eine Teamzusammenfassung, eine kurze Vorbereitung auf ein wöchentliches Meeting, eine Zusammenfassung von Support oder Entwicklung, einen Überblick über deine Zahlen oder eine Zusammenfassung der Newsletter, die du erhältst.

Vorgeschlagen wird nur, was speziell für dich ist und eindeutig nützlich sein kann. Eine Nachrichtenzusammenfassung bezieht sich zum Beispiel nur auf deine eigenen Newsletter, nie auf allgemeine Nachrichten. Wenn nichts passt, gibt es keinen Vorschlag.

Die Routine prüft höchstens einmal täglich und bringt höchstens einen neuen Vorschlag pro Woche, ohne Benachrichtigung. Mit **Nein danke** wird dieser Vorschlag nicht noch einmal angezeigt. Weitergeleitete und beantwortete Mails bleiben bei dem Konto, von dem aus sie gesendet wurden. Arbeit und Privat bleiben also getrennt. Alles bleibt auf deiner Machine. Eine Aufgabe, die du regelmäßig abschließt, wird stattdessen als wiederkehrende Aufgabe angeboten.

## Routinen und wiederkehrende Aufgaben

Eine [wiederkehrende Aufgabe](recurring.md) erinnert dich daran, etwas zu erledigen. Eine Routine erledigt eine Aufgabe selbst und zeigt dir das Ergebnis. Verwende eine wiederkehrende Aufgabe für „am Ersten die Miete zahlen“ und eine Routine für „jeden Freitag melden, welche Deals eingeschlafen sind“.
