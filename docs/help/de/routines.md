---
title: Routinen
area: cards
summary: Arbeit, die deine Machine von selbst in einem Rhythmus erledigt, wie eine Montagsübersicht deiner offenen Deals. Sie liest nur.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, dashboard/routines-page.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js
order: 10
keywords: routine, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays
---
## Eine anlegen

Öffne **Routinen** in der Seitenleiste und sag in einer Zeile, was sie wann tun soll: „jeden Tag um 9, fasse meine offenen Deals zusammen“ oder „jeden Werktag um 8, liste die Mails, auf die ich noch antworten muss“. Dann **Hinzufügen**.

Ohne Uhrzeit läuft sie um 8:00. Die Uhrzeit gilt auf der Uhr deiner Machine. Ihr erster Lauf gibt ihr einen kurzen Namen.

**Hinzufügen** macht zuerst einen Testlauf, damit du siehst, was sie liefert, bevor du sie behältst. Nichts wird gesendet oder gespeichert. Dann behält **Hinzufügen** sie in ihrem Rhythmus, **Ändern** probiert andere Worte oder einen neuen Namen und **Abbrechen** verwirft sie.

## Vorlagen

Unter **Vorlagen** unten auf Routinen schaltet **Hinzufügen** eine fertige Routine ein. Sie läuft sofort einmal und dann jeden Morgen um 7:30 (Spam aufräumen jede Stunde). Ihre Karte zeigt ihre Worte wie jede Routine, und **Bearbeiten** ändert sie oder ihren Namen.

**Newsletter aufräumen** macht ein To-do pro Bereich (Arbeit und Privat) mit den Newslettern des letzten Tages, jeweils mit **Behalten** oder **Abmelden**. Abmelden nutzt den Ein-Klick-Link der Liste oder ihre Abmelde-Mail von deiner Adresse, wenn Senden an ist. Sonst zeigt es **Abmeldeseite öffnen**.

Belege, Bestellungen und Zahlungsmitteilungen bleiben draußen. Mail über eine Gruppenadresse, etwa eine Google Group, steht unter dem, der sie geschrieben hat, und meldet dich nie von der Gruppe ab.

**Spam aufräumen** macht ein To-do pro Bereich mit Mail von unbekannten Absendern, die nach Spam aussieht, jeweils mit **Spam** oder **Kein Spam**. Outlook verschiebt Spam in Junk-E-Mail, Gmail markiert ihn als Spam. Es gibt ihn nur für Mail, die The Machine verschieben darf: Gmail mit nur Leserechten bekommt ihn nicht. Er prüft jede Stunde, damit Spam meist schon da ist, bevor du dazu kommst. Neuer Spam kommt auf dasselbe To-do, solange es offen ist.

Unbekannt heißt, du hast ihnen nie geschrieben, und ein „Re:“ zählt nur in einem Verlauf als Gespräch, in dem du geschrieben hast. Kommt Mail von einem Absender, den du als Spam markiert hast (im To-do oder in deinem Postfach), wieder durch, steht sie im nächsten To-do als **Schon einmal als Spam markiert**. Was du selbst in den Spam verschoben hast, hilft auch, ähnliche Mail zu erkennen.

Nichts ändert sich, bevor du auf dem To-do bestätigst. Tippe auf einen Absender, um die Mail vorher zu lesen: Sie bleibt ungelesen, und nichts ändert sich. Aus Spam aufräumen laden ihre Bilder aus dem Web nicht, damit der Absender nicht sieht, dass sie geöffnet wurde. Über entschiedene Absender wirst du nicht erneut gefragt. Ein Tag ohne Newsletter oder Spam ergibt kein To-do, und diese To-dos senden nie eine Benachrichtigung.

**Geburtstage** macht eine Aufgabe für jeden engen Kontakt, der heute Geburtstag hat: Menschen, denen du selbst schreibst, wie Freunde, Familie und regelmäßige Kontakte. Jede hat einen kurzen Glückwunsch, entworfen dort, wo ihr meist schreibt, etwa im WhatsApp-Chat oder in deinem Mail-Verlauf, in ihrer Sprache. Er geht erst raus, wenn du ihn sendest. Ein Tag ohne Geburtstage macht keine Aufgabe.

Geburtstage kommen aus deinen Kalendern (Googles Geburtstagstermine und sein Kalender Geburtstage, jeden Morgen gelesen, auch wenn sie nicht synchronisiert werden, und der Outlook-Kalender Geburtstage), deinen Google-Kontakten auf einer selbst gehosteten Machine und einem Datumsfeld namens Geburtstag bei einer Person im Graph. Steht noch nirgends ein Geburtstag, sagt das Ergebnis **Noch keine Geburtstage bekannt** und wie du welche einträgst.

**Geburtstage aus Facebook importieren**: Sobald Geburtstage an ist, bietet eine Aufgabe an, die Geburtstagsseite von Facebook zu lesen. Tippe auf **Importieren**, und The Machine öffnet sie in ihrem Browser, scrollt, bis jeder Monat geladen ist, und liest Name und Geburtstag jedes Freundes. Sie zeigt, wie viele sie gefunden hat und wer nach Vor- und Nachname zu Personen in deinem Graph passt. Ein Name, den mehr als eine Person trägt, wird übersprungen und aufgelistet.

Nur **Speichern** behält sie, auf der Seite der Person: den Geburtstag und, wenn sie noch kein Foto hat, ihr Facebook-Profilbild. Einen Geburtstag oder ein Bild, das du dort eingetragen hast, behält sie, und ein Foto, das jemand schon hat, wird nie ersetzt. Auf Facebook wird nichts geschrieben. Sie liest nie von selbst neu: Das macht **Erneut importieren** in der Aufgabe. Der Browser muss bei Facebook angemeldet sein. Ist er es nicht, tippe in der Aufgabe auf **Bei Facebook anmelden** und melde dich dort an; danach liest sie die Seite von selbst. The Machine meldet sich nie für dich an.

Freunde, die niemand in deinem Graph hat, werden gezählt, mit ein paar Namen. **… als persönliche Kontakte hinzufügen** fügt sie alle auf einmal hinzu, auch nach Speichern: jede mit Name und Geburtstag, nie mit einer Work Fleet geteilt. Einen Namen, den schon jemand in deinem Graph hat oder jemand hatte, den du endgültig gelöscht hast, überspringt sie. Geburtstagserinnerungen kommen weiterhin nur für Leute, denen du schreibst.

**Rückgängig** in der Aufgabe entfernt genau diese Personen wieder, auch nach **Erneut importieren**.

Solange ihre Worte die der Vorlage sind, läuft sie mit eigenem Code, ohne dein KI-Abo (Spam aufräumen listet neue Mail von unbekannten Absendern zuerst per Code und stellt deiner KI nur dann eine kurze Frage, wenn es welche gibt). Ein neuer Name ändert daran nichts. Änderst du ihre Worte, läuft sie wie jede Routine mit deinen Worten.

Newsletter aufräumen und Spam aufräumen enden weiter im selben To-do mit einer Wahl pro Mail. Geänderte Geburtstage geben ihr Ergebnis und höchstens einen Entwurf, kein To-do pro Person. **Zurück zur Vorlage** in **Bearbeiten** setzt ihre Worte zurück.

## Was eine Routine tut

Zu ihrer Zeit liest deine Machine, was sie braucht, etwa deine Nachrichten, Termine und den Graph, und legt das Ergebnis auf der Seite Routinen ab. Jedes Ergebnis zeigt **Bereit**, **Nichts Neues** (mit Grund) oder **Hat nicht geklappt** (mit Grund). Ein Lauf, der ohne Ergebnis endet, zählt als nicht geklappt, nie als erledigt.

Routinen lesen nur: deine Nachrichten, Webseiten, GitHub und Seiten wie X im Browser. Sie senden, antworten, posten oder ändern nichts. Nur eine Vorlage ändert Mail, und nur, was du auf ihrem To-do bestätigst.

Endet die Aufgabe einer Routine mit einem Post oder einer Nachricht, erledigt sie alles bis zu diesem Schritt und zeigt den Entwurf, etwa **Würde auf X posten:**. Nach einem echten Lauf bekommst du ihn als To-do zum Freigeben; ein Testlauf zeigt ihn nur. Sein Name sagt, worum es geht und wohin es geht, sein Button nennt den Schritt, etwa **Posten**, und **Von deiner Routine** darunter öffnet die Routine.

Das To-do startet im Bereich des Kontos, von dem es ausgeht, etwa Arbeit für das X-Konto deiner Firma, und bittet also nie ums Verschieben.

Ein Lauf kann deinen eingeschalteten [Skills](skills.md) folgen, ausgewählt nach dem, was die Routine tut: Nur die passenden werden ganz gelesen. Das Ergebnis nennt sie unter **Verwendet:**. Ein Skill bringt eine Routine nie dazu, etwas zu senden oder zu ändern.

Deine Routinen stehen unter **Deine Routinen**, unter den Vorschlägen. Ein langes Ergebnis ist auf eine kurze Vorschau eingeklappt; **Mehr anzeigen** öffnet es.

Jeder Lauf kennt das letzte Ergebnis und kann so sagen, was sich seitdem geändert hat.

Nach einem guten Lauf kann deine Machine sich selbst ein Rezept schreiben für das Lesen, das jedes Mal gleich ist, etwa welche Mails oder GitHub-Änderungen sie ansieht. Die nächsten Läufe lesen das zuerst, in einfachem Code, und die KI wählt nur aus, was zählt, und schreibt es auf, mit weniger Tokens. Ein Rezept liest nur; funktioniert es nicht mehr, liest der Lauf selbst und repariert es. Du siehst es unter **Erweitert: Skriptschritte** im ⋯-Menü.

## Verpasste Tage

War deine Machine aus oder beschäftigt, stapeln sich verpasste Läufe nicht: Nur der neueste läuft, einmal. Jedes Datum läuft einmal, auch nach einem Neustart.

Routinen laufen nacheinander und warten, wenn das Nutzungslimit deines KI-Abos knapp wird, wie alle Arbeit im Hintergrund. **Jetzt ausführen** startet sie sofort; ihr Ergebnis erscheint auf der Karte, sobald es fertig ist.

## Ändern oder stoppen

Das steht im ⋯-Menü der Routine. **Bearbeiten** ändert ihren Namen und was sie tut; wann sie läuft und ihre bisherigen Ergebnisse bleiben. **Zeitpunkt ändern** nimmt einen neuen Rhythmus in deinen eigenen Worten, wie „jeden Werktag um 8“. Beide haben **Speichern** und **Abbrechen**; am Computer brechen auch Esc oder ein Klick daneben ab.

In **Bearbeiten** lässt **Ausprobieren** die neuen Worte einmal laufen und zeigt dort das Ergebnis. Die Routine bleibt, wie sie war, bis **Speichern**.

**Pausieren** hält die Läufe an bis **Fortsetzen**; pausierte Routinen warten unten unter **Pausiert**, und was während der Pause verpasst wurde, läuft danach nicht. **Stopp** beendet eine Routine endgültig.

Nutzt du **Änderungen anfragen** bei einer Aufgabe einer Routine oder schreibst in ihrem Chat, und gilt deine Notiz für jeden Lauf, etwa „nie Emojis“, bietet die Aufgabe **Auch die Routine ändern** an, auf der Aufgabe und in ihrem Chat unter der Antwort. Sie zeigt, was sich an den Worten der Routine ändert, und die Routine ändert sich erst, wenn du auf **Ändern** tippst. **So lassen** lässt sie, wie sie ist. Eine Korrektur nur an diesem Entwurf bietet nichts an.

## Erweitert: Skriptschritte

Ein Skript brauchst du nie: Sag in deinen eigenen Worten, was eine Routine tun soll.

Für Fortgeschrittene kann eine Routine auch deine eigenen Befehle auf deiner Machine ausführen: Wähle im ⋯-Menü **Erweitert: Skriptschritte**. **Bearbeiten** zeigt sie nur, wenn eine Routine schon welche hat. **Daten holen** führt zuerst einen Befehl aus, in seinem Ordner (leer: dein Home-Ordner) und höchstens für seine Sekunden. Was er ausgibt, bekommt der Lauf zum Arbeiten. Ohne Worte ist die Ausgabe das Ergebnis.

**Prüfung** bekommt nach dem Lauf das Ergebnis als Eingabe. Endet sie mit einem Fehler, zeigt der Lauf **Hat nicht geklappt** mit dem, was die Prüfung gesagt hat. Ein fehlgeschlagener Befehl bei Daten holen zeigt sich genauso.

Ein Befehl ist eine Zeile und läuft ohne Shell: keine Pipes oder Variablen. Skriptschritte legst nur du fest, auf deinem Dashboard. Ein Testlauf und **Ausprobieren** führen Daten holen auch aus und sagen das; sie senden und behalten trotzdem nichts. Eine Routine sendet nie, also sollte ein Skriptschritt nur lesen.

## Aus deinen OpenClaw-Jobs

Hast du vorher geplante Jobs in OpenClaw angelegt, liest deine Machine sie (sie ändert sie nie) und schlägt die passenden unter **Vorgeschlagen** als Routinen vor. Jeder lief einmal, damit du ein echtes Ergebnis siehst.

Deine Korrekturen am Job bleiben drin, was er gesendet oder gepostet hat, fällt weg. Ein Job, der ein Skript ausgeführt oder gelesen hat, was ein Skript-Job gesammelt hat, bringt es als Daten holen mit. **Hinzufügen** macht daraus eine Routine, **Nein danke** fragt nie wieder nach diesem Job. Ein Job, der dich an etwas erinnert hat, kommt stattdessen als Angebot für eine wiederkehrende Aufgabe unter Aufgaben.

Bevor du einen Vorschlag hinzufügst, änderst du ihn mit **Bearbeiten** und **Zeitpunkt ändern** in seinem ⋯-Menü wie jede Routine. **Erneut ausführen** führt ihn jetzt mit seinen aktuellen Worten aus, damit du neuere Ergebnisse siehst, etwa nach einem ruhigen Wochenende. Er liest nur, läuft einmal pro Tippen, und das neue Ergebnis ersetzt das alte.

Höchstens drei Vorschläge warten gleichzeitig. Nach einer Woche guter Läufe fragt die Routine **Den alten OpenClaw-Job ausschalten?** Er wird nur ausgeschaltet, wenn du auf **Ausschalten** tippst, und du kannst ihn in OpenClaw wieder einschalten.

## Aus dem, was du tust

Deine Machine bemerkt auch Arbeit, die du in einem Rhythmus erledigst, und schlägt sie unter **Vorgeschlagen** als Routine vor, auch ohne OpenClaw. Sie achtet auf:

- dieselbe Bitte, dreimal oder öfter hintereinander, wie „fasse die offenen Support-Tickets zusammen“ jeden Montag;
- eine Mail, die du in einem Rhythmus sendest, wie einen Wochenbericht an dein Team;
- Newsletter und Update-Mails, die jede Woche wieder kommen;
- einen vollen Slack-Kanal, in dem andere jede Woche schreiben;
- Mails, die du einzeln an dieselbe Person weiterleitest, wie Mails von Schule und Verein an deinen Partner: ein wöchentlicher Digest für sie spart das Weiterleiten;
- dieselbe Anfrage, die du in einem Rhythmus beantwortest, wie eine monatliche Freigabe für dieselbe Person.

Jeder Vorschlag sagt, was sie gesehen hat, wie „4 Mal hintereinander gefragt“ oder „6 E-Mails in 3 Wochen an Sam weitergeleitet“, und lief einmal, damit du ein echtes Ergebnis siehst. Denk an eine Team-Zusammenfassung, ein Briefing vor einem wöchentlichen Call, eine Support- oder Dev-Übersicht, einen Puls deiner Zahlen oder einen Digest der Newsletter, die du bekommst.

Sie schlägt nur vor, was zu dir passt und klar hilft: einen News-Digest nur über deine eigenen Newsletter, nie einen allgemeinen. Passt nichts, gibt es keinen Vorschlag.

Sie schaut höchstens einmal am Tag und bringt höchstens einen neuen Vorschlag pro Woche, ohne Benachrichtigung. **Nein danke** bringt diesen Vorschlag nie zurück. Weitergeleitete Mails und Antworten bleiben bei dem Konto, von dem sie gesendet wurden, damit Arbeit und Privat sich nicht mischen. Alles bleibt auf deiner Machine. Eine Aufgabe, die du in einem Rhythmus erledigst, kommt stattdessen als Angebot für eine wiederkehrende Aufgabe.

## Routinen und wiederkehrende Aufgaben

Eine wiederkehrende Aufgabe (recurring.md) erinnert dich daran, etwas zu tun. Eine Routine ist Arbeit, die deine Machine selbst erledigt und dir zeigt. Nimm eine wiederkehrende Aufgabe für „Miete am Ersten zahlen“ und eine Routine für „jeden Freitag sagen, welche Deals still geworden sind“.
