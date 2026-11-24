---
title: Benachrichtigungen
area: settings
summary: Was dich wann und wo erreicht: Nur Dringendes meldet sich sofort, alles andere kommt in einer morgendlichen Zusammenfassung.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 3c469ec1032f6bea
---
Weniger Benachrichtigungen oder andere? Wähle in **Einstellungen** unter **Benachrichtigungen** aus, wo dich die einzelnen Arten erreichen:

- **Neue Aufgaben**: nur Dringendes, zum Beispiel etwas, das heute fällig oder dringend ist.
- **Ergebnisse und Fragen**: ein versandbereiter Entwurf, eine Anmeldung, die für eine Aufgabe nötig ist, oder eine Frage zur Fleet.
- **Erinnerungen**: zurückgestellte Aufgaben und Antworten, auf die du wartest und die wieder anstehen.
- **Morgendliche Zusammenfassung**: eine kurze Zusammenfassung deines Tages. Mehr dazu weiter unten.
- **Abendliche Zusammenfassung**: was heute erledigt wurde und was morgen noch offen ist. Mehr dazu weiter unten.

Für jede Art gibt es einen Schalter für **Push** (die App auf deinem Handy oder Computer), **Telegram**, sobald es eingerichtet ist, und **E-Mail** bei einer gehosteten Machine oder einer Machine im The Machine Network. Alles ist aktiviert, außer den Zusammenfassungen bei Telegram.

Deine **Arbeitszeiten** findest du im selben Tab: Arbeitstage, wann Benachrichtigungen gesendet werden dürfen, wann Zurückgestelltes wieder ansteht, die Zeiten für Zusammenfassungen und deine Zeitzone. Weitere Informationen findest du unter [Arbeitszeiten](work-hours.md).

## Nur Dringendes

Eine Push-Benachrichtigung, eine Telegram-Mitteilung oder eine E-Mail gibt es nur bei:

- einer Aufgabe, die heute fällig oder als dringend markiert ist;
- einer Antwort, die jemand erwartet und die als Entwurf bereit zum Senden ist;
- einer Aufgabe, bei der du dich anmelden musst;
- einer Zurückstellung, die zum von dir gewählten Zeitpunkt wieder ansteht.

Alles andere erscheint unauffällig auf dem Dashboard und lautlos in Telegram und wartet auf die morgendliche Zusammenfassung. An freien Tagen melden sich nur dringende oder heute fällige Aufgaben. Es gibt höchstens 8 Push-Benachrichtigungen pro Tag. Wenn du das Dashboard 3 Tage lang nicht öffnest, bekommst du nur die morgendliche Zusammenfassung, bis du wieder da bist.

## Wann Benachrichtigungen gesendet werden

Die App prüft, ob du das Dashboard tatsächlich verwendest, nicht nur, ob es geöffnet ist:

- Wenn du es gerade verwendest (es ist im Vordergrund und du hast in den letzten 10 Minuten geklickt, getippt oder gescrollt), gibt es keine hörbaren Benachrichtigungen. Telegram-Mitteilungen kommen lautlos an. Das Dashboard nur zu öffnen oder neu zu laden zählt nicht.
- Wenn du gerade nicht da bist (das Dashboard ist im Hintergrund, geschlossen oder seit 10 Minuten inaktiv), wird eine Minute, nachdem du es verlassen hast, eine Push-Benachrichtigung gesendet, sofern du nicht zurückgekommen bist und sie gesehen hast.
- Wenn dich 15 Minuten später noch nichts erreicht hat und es nicht warten kann, wird dazu eine E-Mail gesendet, höchstens eine pro Stunde. Was du bereits gesehen oder erledigt hast, wird ausgelassen. Jede Aufgabe erscheint nur einmal und zeigt ihren aktuellen Stand. An den meisten Tagen ist die morgendliche Zusammenfassung die einzige E-Mail.
- Als zugestellt gilt eine Benachrichtigung, wenn sie auf deinem Handy oder im Browser angezeigt wurde oder Telegram die Nachricht angenommen hat. Ein ausgeschaltetes, offline befindliches oder für Benachrichtigungen deaktiviertes Handy zählt nicht. Das gilt auch für Telegram, wenn du das Dashboard verwendest. Wurde die Benachrichtigung nur auf einem Computer angezeigt, werden dringende oder heute fällige Aufgaben trotzdem per E-Mail gesendet, denn vielleicht bist du gerade nicht da.
- Hast du keine Handy-App, Browser-Benachrichtigungen oder Telegram? Dann bekommst du für alles oben eine E-Mail.
- Telegram ist nicht erreichbar: Die Push-Benachrichtigung wird trotzdem einmal gesendet und Telegram versucht es später automatisch erneut.
- Ein Teammitglied weist dir eine Aufgabe zu und deine Machine kann dich nicht über dein Handy oder Telegram erreichen: Wenn du sie nach 15 Minuten noch nicht gesehen hast, bekommst du eine E-Mail mit dem Titel und einem Link. Mit **E-Mail** für **Ergebnisse und Fragen** kannst du das deaktivieren.
- Außerhalb deiner Arbeitszeiten wird nichts gesendet. Die morgendliche Zusammenfassung enthält die Informationen.
- Eine neue Aufgabe für die Arbeit an einem freien Tag wartet bis zur Uhrzeit deiner Zusammenfassung am nächsten Arbeitstag. Bei der Aufgabe wird angezeigt, wann sie dich erreicht, zum Beispiel: „Benachrichtigung Mo., 2. Nov. · 08:30“.

Fortschritte und Änderungen lösen keine Benachrichtigungen aus. Gibt es ein neues Ergebnis zu einer Aufgabe, die du noch nicht gesehen hast, wird die Aufgabe aktualisiert, ohne eine neue Benachrichtigung zu senden. Bei mehreren Benachrichtigungen kurz hintereinander gibt es nur eine Meldung. Das App-Symbol zeigt, wie viele Aufgaben deine Aufmerksamkeit brauchen.

## Schaltflächen in Benachrichtigungen

Jede Benachrichtigung hat Schaltflächen für den nächsten Schritt. In der Handy-App:

- Neue Aufgabe: **Ausführen**, **Zurückstellen**, **Als erledigt markieren**.
- Entwurf bereit: **Entwurf öffnen**, **Zurückstellen**, **Als erledigt markieren**.
- Ergebnis bereit: **Öffnen**, **Als erledigt markieren**, **Zurückstellen**.
- Antwort nötig, Aufgabe hängt oder Anmeldung erforderlich: **Antworten**, **Öffnen** oder **Anmelden**, danach **Zurückstellen** und **Als erledigt markieren**.
- Erinnerung: **Als erledigt markieren**, **Zurückstellen**, **Öffnen**.
- Morgendliche Zusammenfassung: Zum Öffnen antippen.

Im Browser und bei Telegram werden jeweils zwei davon angezeigt. Bei Fragen zur Fleet gibt es einmal **Antworten** und **Ablehnen**.

Über eine Benachrichtigung wird nichts gesendet, bezahlt oder eingereicht. Ein Entwurf wird immer zuerst geöffnet, damit du ihn siehst, bevor er versendet wird. **Entwurf öffnen** zeigt die Aufgabe mit dem vollständigen Entwurf in deiner Liste. **Ausführen** startet die Arbeit nur bei einer neuen Aufgabe.

In der Handy-App musst du das Gerät erst entsperren, bevor du **Zurückstellen** oder **Als erledigt markieren** auswählst. Im Browser öffnen sich dadurch das Dashboard und die entsprechende Funktion. Dort wird auch „Rückgängig“ angezeigt. Durch **Zurückstellen** wird die Aufgabe in zwei Stunden wieder angezeigt, bei einer Erinnerung am nächsten Morgen.

E-Mails enthalten Links zum Öffnen und für wartende Aufgaben auch einen Link zum Zurückstellen. Sie öffnen nur das Dashboard.

Wenn du eine Benachrichtigung antippst oder in einer E-Mail oder bei Telegram **Öffnen** auswählst, wird die Aufgabe in deiner Liste hervorgehoben, egal, wo sie sich gerade befindet: **Gerade erledigt**, **Erledigt**, **Kommt später zurück** oder eine andere Ansicht. Der Chat wird nie geöffnet. Falls die Seite noch nicht aktualisiert ist, wird die Aufgabe geöffnet, sobald sie angezeigt wird.

## Die morgendliche Zusammenfassung

Sie kommt an Arbeitstagen zur Uhrzeit für **Morgendliche Zusammenfassung**, außer, wenn es nichts zu berichten gibt. Liegt diese Uhrzeit vor **Zurückgestelltes kommt um**, wartet die Zusammenfassung bis 5 Minuten danach. So enthält sie auch die Aufgaben, die an diesem Morgen wieder anstehen. Mit **Vorschau** kannst du sie ansehen, ohne sie zu senden. Standardmäßig kommt sie als Push-Benachrichtigung und per E-Mail. Sie ist kurz genug, um sie auf einen Blick zu erfassen:

- eine Begrüßung mit dem Wichtigsten für heute, zum Beispiel „Guten Morgen Sam, 2 Antworten sind bereit zum Senden“ oder bei einer Aufgabe „Guten Morgen Sam, bereit für deine Freigabe: Bestellformular senden“. Als bereit zählen nur Aufgaben mit einem Entwurf oder Ergebnis zur Freigabe. Aufgaben, bei denen du zuerst antworten musst, zählen nicht dazu;
- die Aufgaben, auf die sich die Begrüßung bezieht, jeweils mit einem Link zum Öffnen, sowie alles, was heute fällig ist. Andernfalls werden höchstens drei Aufgaben angezeigt;
- bis zu fünf Aufgaben, die du selbst hinzugefügt hast und die auf dich warten, unabhängig davon, was in der Begrüßung steht;
- wie viele weitere Aufgaben warten können und wie lange du in deinem Tempo dafür brauchst, zum Beispiel „12 weitere Aufgaben können warten, zum Erledigen brauchst du etwa 5 Min.“. Aufgaben, bei denen deine Antwort aussteht, werden bei dieser Zeit nicht berücksichtigt. Eine Aufgabe, die heute fällig, aber bis später zurückgestellt ist, oder an der The Machine noch arbeitet, wird erst gezählt, wenn sie auf dich wartet. Die Anzahl entspricht den Aufgaben, die in deiner Liste auf dich warten.
- deine Termine in einer Zeile.

Mit **Öffnen** wird die Aufgabe in deiner Liste hervorgehoben, auch wenn sie erledigt oder zurückgestellt ist. Ein Versprechen öffnet die zugehörige Aufgabe oder, falls es noch keine gibt, die Seite des Versprechens.

Die Push-Benachrichtigung enthält dasselbe, aber ohne Links. Tippe darauf oder auf den Link am Ende der E-Mail, um die Zusammenfassung unter **Aufgaben** erneut zu lesen.

## Die abendliche Zusammenfassung

Sie kommt an Arbeitstagen einmal zur dafür in **Arbeitszeiten** festgelegten Uhrzeit. Standardmäßig ist das 15 Minuten vor **Bis**. Sie wird über die oben in ihrer Zeile ausgewählten Kanäle gesendet. Du bekommst sie nur an einem Tag, an dem du da warst: Du hast das Dashboard verwendet oder dort, in Telegram, im Chat oder per Sprache eine Entscheidung zu einer Aufgabe getroffen. Wenn an dem Tag keine Aufgabe erledigt und kein Termin wahrgenommen wurde, bekommst du keine Zusammenfassung.

Sie beginnt mit einer Zusammenfassung des Tages, zum Beispiel „Guten Abend Sam, heute wurden 4 Aufgaben erledigt“. Danach folgen die Bereiche **Arbeit** und **Privat**. Ein leerer Bereich wird ausgelassen. Eine Benachrichtigung zu deiner Machine selbst erscheint in keinem der beiden Bereiche. Jeder Bereich enthält:

- **Heute erledigt**: bis zu drei Aufgaben, die du oder deine Machine abgeschlossen habt, danach „+12 weitere“ und die Termine des Tages, zum Beispiel „+3 Termine: Preisgespräch und 2 weitere“;
- **Offen für morgen** (am Freitag für deinen nächsten Arbeitstag): die ersten Termine und alles, was fällig ist.

Am Ende steht, wie viele Aufgaben noch deine Aufmerksamkeit brauchen. Tippe auf die Push-Benachrichtigung oder auf den Link am Ende der E-Mail, um sie mit **Arbeit kopieren** und **Privat kopieren** erneut zu lesen. Um sie abzuschalten, deaktiviere die entsprechende Zeile.

## Datenschutz

Push-Benachrichtigungen werden direkt und verschlüsselt von deiner Machine an dein Gerät gesendet. E-Mails laufen über den Mailserver von The Machine und deinen E-Mail-Anbieter. Wenn [Sorgfältig](security-levels.md) den Aufgabentext in Benachrichtigungen ausblendet, enthalten E-Mails nur Zahlen. Deaktiviere **E-Mail** für eine Art von Benachrichtigung, damit sie nicht per E-Mail gesendet wird.

Aktiviere Push-Benachrichtigungen für ein Gerät unter **Dieses Gerät** oder lies [App installieren](phone-app.md). Die [Handy-App](mobile-app.md) sendet eine einfache Zeile über Apple oder Google und fragt dann deine Machine nach dem Titel und dem nächsten Schritt.
