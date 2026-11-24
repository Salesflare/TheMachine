---
title: Benachrichtigungen
area: settings
summary: Was dich wo und wann erreicht: Nur was nicht warten kann, macht sich bemerkbar. Alles andere findest du in einer morgendlichen Zusammenfassung.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: bdb4ecec9446aa5e
---
Weniger Benachrichtigungen oder andere? Wähle unter **Einstellungen** und **Benachrichtigungen** aus, auf welchem Weg dich die einzelnen Arten erreichen:

- **Neue Aufgaben**: nur was nicht warten kann, zum Beispiel etwas, das heute fällig oder dringend ist.
- **Ergebnisse und Fragen**: ein Entwurf, der versandbereit ist, eine Anmeldung, die für eine Aufgabe nötig ist, oder eine Frage zu Fleet.
- **Erinnerungen**: zurückgestellte Aufgaben und ausstehende Antworten, die wieder anstehen.
- **Morgendliche Zusammenfassung**: eine kurze Zusammenfassung deines Tages. Mehr dazu weiter unten.
- **Abendliche Zusammenfassung**: was heute erledigt wurde und was morgen noch offen ist. Mehr dazu weiter unten.

Für jede Art kannst du **Push** (in der App auf deinem Handy oder Computer), **Telegram**, sobald es eingerichtet ist, und **E-Mail** auf einer gehosteten Machine oder einer Machine auf The Machine Network aktivieren. Alles ist eingeschaltet, außer den Zusammenfassungen in Telegram.

Deine **Arbeitszeiten** findest du im selben Tab: Arbeitstage, wann Benachrichtigungen gesendet werden dürfen, wann Zurückgestelltes wieder ansteht, die Zeiten der Zusammenfassungen und deine Zeitzone. Weitere Infos findest du unter [Arbeitszeiten](work-hours.md).

## Nur was nicht warten kann

Eine Push-Benachrichtigung, eine Nachricht in Telegram oder eine E-Mail erhältst du nur bei:

- einer Aufgabe, die heute fällig oder als dringend markiert ist;
- einer Antwort, die jemand erwartet und die als Entwurf versandbereit ist;
- einer Aufgabe, bei der du dich anmelden musst;
- einer Zurückstellung, die zum ausgewählten Zeitpunkt wieder ansteht.

Alles andere erscheint unauffällig auf dem Dashboard und lautlos in Telegram und wartet auf die morgendliche Zusammenfassung. An einem freien Tag machen sich nur dringende oder heute fällige Aufgaben bemerkbar. Du erhältst höchstens 8 Push-Benachrichtigungen pro Tag. Wenn du das Dashboard 3 Tage lang nicht öffnest, erhältst du nur die morgendliche Zusammenfassung, bis du wieder da bist.

## Wann Benachrichtigungen gesendet werden

Es wird geprüft, ob du das Dashboard tatsächlich verwendest, nicht nur, ob es geöffnet ist:

- Wenn du es verwendest (es ist im Vordergrund und du hast in den letzten 10 Minuten geklickt, getippt oder gescrollt), gibt es keine hörbaren Benachrichtigungen. Nachrichten in Telegram kommen lautlos an. Das Dashboard nur zu öffnen oder neu zu laden zählt nicht.
- Wenn du nicht da bist (das Dashboard ist im Hintergrund, geschlossen oder seit 10 Minuten inaktiv), wird eine Minute, nachdem du es verlassen hast, eine Push-Benachrichtigung gesendet, sofern du nicht zurückgekommen bist und sie gesehen hast.
- Wenn du die Benachrichtigung auch 15 Minuten später noch nicht gesehen hast und die Sache nicht warten kann, erhältst du dafür eine E-Mail, höchstens eine pro Stunde. Was du bereits erledigt hast, wird ausgelassen. Jede Aufgabe kommt nur einmal vor, und zwar so, wie sie gerade aussieht. An den meisten Tagen ist die morgendliche Zusammenfassung die einzige E-Mail.
- Wenn dir ein Teammitglied eine Aufgabe zuweist und deine Machine dich weder per Handy noch über Telegram erreichen kann, erhältst du eine E-Mail mit dem Titel und einem Link. Sie kommt nach 15 Minuten, falls du die Aufgabe bis dahin noch nicht gesehen hast. Wenn du **E-Mail** für **Ergebnisse und Fragen** ausschaltest, werden diese E-Mails deaktiviert.
- Außerhalb deiner Arbeitszeiten erhältst du nichts. Die morgendliche Zusammenfassung enthält die Informationen.
- Eine neue Arbeitsaufgabe an einem freien Tag wartet bis zur Zusammenfassungszeit deines nächsten Arbeitstags. Bei der Aufgabe wird angezeigt, wann sie dich erreicht, zum Beispiel „Benachrichtigung Mo., 2. Nov. · 08:30“.

Fortschritte und Änderungen lösen keine Benachrichtigungen aus. Wenn ein neues Ergebnis zu einer Aufgabe kommt, die du noch nicht gesehen hast, wird die bestehende Benachrichtigung aktualisiert, ohne eine neue zu senden. Mehrere Benachrichtigungen kurz hintereinander lösen nur einen Hinweis aus. Das App-Symbol zeigt an, wie viele Aufgaben deine Aufmerksamkeit brauchen.

## Schaltflächen in Benachrichtigungen

Jede Benachrichtigung bietet Schaltflächen für den nächsten Schritt. In der Handy-App:

- Neue Aufgabe: **Ausführen**, **Zurückstellen**, **Erledigt**.
- Entwurf bereit: **Entwurf öffnen**, **Zurückstellen**, **Erledigt**.
- Ergebnis bereit: **Öffnen**, **Erledigt**, **Zurückstellen**.
- Deine Antwort wird gebraucht, etwas hängt fest oder eine Anmeldung ist nötig: **Antworten**, **Öffnen** oder **Anmelden**, danach **Zurückstellen** und **Erledigt**.
- Erinnerung: **Erledigt**, **Zurückstellen**, **Öffnen**.
- Morgendliche Zusammenfassung: Tippe darauf, um sie zu öffnen.

Im Browser und in Telegram werden zwei davon angezeigt. Bei Fragen zu Fleet gibt es immer **Antworten** und **Ablehnen**.

Über eine Benachrichtigung wird nichts gesendet, bezahlt oder eingereicht. Ein Entwurf wird immer zuerst geöffnet, damit du ihn vor dem Versand sehen kannst. **Entwurf öffnen** zeigt die Aufgabe mit dem vollständigen Entwurf in deiner Liste an. **Ausführen** startet nur die Arbeit an einer neuen Aufgabe.

In der Handy-App musst du zum **Zurückstellen** und **Erledigen** erst dein Gerät entsperren. Im Browser öffnen sich stattdessen das Dashboard und die jeweilige Aufgabe. Dort kannst du die Aktion rückgängig machen. Beim Zurückstellen wird die Aufgabe in zwei Stunden wieder angezeigt, bei einer Erinnerung am nächsten Morgen.

E-Mails enthalten Links zum Öffnen und bei ausstehenden Aufgaben auch zum Zurückstellen. Sie öffnen nur das Dashboard.

Wenn du auf eine Benachrichtigung oder in einer E-Mail oder Telegram auf **Öffnen** tippst, wird die Aufgabe an ihrer aktuellen Stelle in deiner Liste hervorgehoben: **Gerade erledigt**, **Erledigt**, **Kommt später zurück** oder in einer anderen Ansicht. Der Chat wird dabei nie geöffnet. Falls die Seite noch nicht aktualisiert war, wird der Aufgabe gefolgt, sobald sie angezeigt wird.

## Die morgendliche Zusammenfassung

Sie kommt an Arbeitstagen zur unter **Morgendliche Zusammenfassung** festgelegten Uhrzeit, sofern es etwas zu berichten gibt. Liegt diese Uhrzeit vor **Zurückgestelltes kommt um**, wartet die Zusammenfassung bis 5 Minuten danach, damit die Aufgaben darin enthalten sind, die an diesem Morgen wieder anstehen. Mit **Vorschau** kannst du sie ansehen, ohne sie zu versenden. Standardmäßig erhältst du sie als Push-Benachrichtigung und per E-Mail. Sie ist kurz genug, um sie schnell zu überfliegen:

- eine Begrüßung mit dem Wichtigsten für heute, zum Beispiel „Guten Morgen, Sam. 2 Antworten sind versandbereit“ oder bei einer Aufgabe „Guten Morgen, Sam. Deine Freigabe wird gebraucht: Bestellformular senden“. Als bereit zählen nur Aufgaben mit einem Entwurf oder Ergebnis, das du freigeben kannst. Aufgaben, bei denen zuerst deine Antwort gebraucht wird, zählen nicht dazu;
- die Aufgaben, auf die sich die Begrüßung bezieht, jeweils mit einem Link zum Öffnen, sowie alles, was heute fällig ist; andernfalls höchstens drei Aufgaben;
- bis zu fünf Aufgaben, die du selbst hinzugefügt hast und bei denen du am Zug bist, unabhängig davon, auf welche Aufgaben sich die Begrüßung bezieht;
- wie viele weitere Aufgaben warten können und wie lange sie in deinem Tempo dauern, zum Beispiel „12 weitere können warten, dauert ungefähr 5 Min.“ Aufgaben, bei denen deine Antwort gebraucht wird, fließen nicht in diese Zeit ein. Eine Aufgabe, die heute fällig ist, aber bis später zurückgestellt wurde, oder an der The Machine noch arbeitet, wird erst gezählt, wenn du am Zug bist. Die Anzahl entspricht den Aufgaben, die in deiner Liste auf dich warten.
- deine Termine in einer Zeile.

**Öffnen** zeigt die Aufgabe hervorgehoben in deiner Liste, auch wenn sie erledigt oder zurückgestellt ist. Ein Versprechen öffnet die dazugehörige Aufgabe oder, falls es noch keine gibt, die eigene Seite.

Die Push-Benachrichtigung enthält denselben Text, aber keine Links. Tippe darauf oder auf den Link am Ende der E-Mail, um die Zusammenfassung unter **Aufgaben** noch einmal aufzurufen.

## Die abendliche Zusammenfassung

Sie kommt an Arbeitstagen einmal zur unter **Arbeitszeiten** festgelegten Uhrzeit und standardmäßig über die oben in ihrer Zeile ausgewählten Wege. Standardmäßig ist das 15 Minuten vor **Bis**. Sie wird nur an Tagen gesendet, an denen du da warst: Du hast das Dashboard verwendet oder dort, in Telegram, im Chat oder per Sprache eine Entscheidung zu einer Aufgabe getroffen. Wenn an einem Tag keine Aufgabe erledigt und kein Meeting abgehalten wurde, erhältst du keine Zusammenfassung.

Sie beginnt mit einer Tagesbilanz, zum Beispiel „Guten Abend, Sam. Heute 4 Aufgaben erledigt“, gefolgt von einem Abschnitt **Arbeit** und einem Abschnitt **Privat**. Abschnitte ohne Inhalt werden ausgelassen. Eine Meldung zu deiner Machine selbst gehört zu keinem der beiden Abschnitte. Jeder Abschnitt enthält:

- **Heute erledigt**: bis zu drei Aufgaben, die du oder deine Machine erledigt haben, dann „+12 weitere“ und die Meetings des Tages, zum Beispiel „+3 Meetings: Preisgespräch und 2 weitere“;
- **Offen für morgen** (am Freitag für deinen nächsten Arbeitstag): die ersten Meetings und alles, was fällig ist.

Zum Schluss steht, wie viele Aufgaben noch deine Aufmerksamkeit brauchen. Tippe auf die Push-Benachrichtigung oder auf den Link am Ende der E-Mail, um die Zusammenfassung mit **Arbeit kopieren** und **Privat kopieren** erneut aufzurufen. Um sie nicht mehr zu erhalten, schalte die entsprechende Zeile aus.

## Datenschutz

Push-Benachrichtigungen werden direkt von deiner Machine an dein Gerät gesendet und für dieses verschlüsselt. E-Mails laufen über den Mailserver von The Machine und deinen E-Mail-Anbieter. Wenn [Vorsichtig](security-levels.md) Aufgabentexte in Benachrichtigungen ausblendet, enthalten E-Mails nur Anzahlen. Schalte **E-Mail** für eine Benachrichtigungsart aus, wenn du sie nicht per E-Mail erhalten möchtest.

Aktiviere Push-Benachrichtigungen für ein Gerät unter **Dieses Gerät** oder lies [App installieren](phone-app.md). Die [Handy-App](mobile-app.md) sendet eine einfache Zeile über Apple oder Google und fragt dann deine Machine nach dem Titel und dem nächsten Schritt.
