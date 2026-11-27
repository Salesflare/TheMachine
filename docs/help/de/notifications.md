---
title: Benachrichtigungen
area: settings
summary: Was dich wo und wann erreicht: Nur was nicht warten kann, macht sich bemerkbar. Alles andere kommt in eine morgendliche Zusammenfassung.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: dc56a77907df5da0
---
Weniger Benachrichtigungen oder andere? Wähle unter **Einstellungen** und **Benachrichtigungen** aus, wo dich die einzelnen Arten erreichen:

- **Neue Aufgaben**: nur was nicht warten kann, etwa etwas, das heute fällig oder dringend ist.
- **Ergebnisse und Fragen**: eine Antwort, die zum Senden bereit ist, eine Anmeldung, die für eine Aufgabe nötig ist, oder eine Frage zu einer Fleet.
- **Erinnerungen**: zurückgestellte Aufgaben und ausstehende Antworten, die wieder anstehen.
- **Morgendliche Zusammenfassung**: eine kurze Zusammenfassung deines Tages. Mehr dazu weiter unten.
- **Abendliche Zusammenfassung**: was du heute erledigt hast und was morgen noch offen ist. Mehr dazu weiter unten.

Für jede Art gibt es einen Schalter für **Push** (die App auf deinem Handy oder Computer), **Telegram**, sobald es eingerichtet ist, und **E-Mail** auf einer gehosteten Machine oder einer Machine im The Machine Network. Alles ist aktiviert, außer den Zusammenfassungen über Telegram.

Deine **Arbeitszeiten** findest du im selben Tab: Arbeitstage, wann Benachrichtigungen gesendet werden dürfen, wann Zurückgestelltes ansteht, die Uhrzeiten für Zusammenfassungen und deine Zeitzone. Weitere Informationen findest du unter [Arbeitszeiten](work-hours.md).

## Nur was nicht warten kann

Eine Push-Benachrichtigung, eine Nachricht über Telegram oder eine E-Mail gibt es nur für:

- eine Aufgabe, die heute fällig oder als dringend markiert ist;
- eine Antwort, auf die jemand wartet und die als Entwurf fertig zum Senden ist;
- eine Aufgabe, für die du dich anmelden musst;
- etwas Zurückgestelltes, das zum gewählten Zeitpunkt wieder ansteht.

Alles andere erscheint unauffällig auf dem Dashboard und lautlos in Telegram und wartet auf die morgendliche Zusammenfassung. An einem freien Tag machen sich nur dringende oder heute fällige Aufgaben bemerkbar. Es gibt höchstens 8 Push-Benachrichtigungen am Tag. Wenn du das Dashboard 3 Tage lang nicht öffnest, bekommst du nur die morgendliche Zusammenfassung, bis du wieder da bist.

## Wann Benachrichtigungen gesendet werden

Es wird geprüft, ob du das Dashboard tatsächlich nutzt, nicht nur, ob es geöffnet ist:

- Wenn du es nutzt (es im Vordergrund ist und du in den letzten 10 Minuten geklickt, geschrieben oder gescrollt hast): Es macht sich nichts bemerkbar. Telegram-Nachrichten kommen lautlos an. Nur das Öffnen oder Neuladen zählt nicht.
- Wenn du nicht da bist (das Dashboard im Hintergrund oder geschlossen ist oder du 10 Minuten lang nichts gemacht hast): Eine Push-Benachrichtigung wird eine Minute nach deinem Weggehen gesendet, außer du bist zurückgekommen und hast sie gesehen.
- Wenn dich nach 15 Minuten noch nichts erreicht hat und es nicht warten kann: Du bekommst eine E-Mail dazu, höchstens eine pro Stunde. Was du bereits gesehen oder erledigt hast, wird ausgelassen. Jede Aufgabe erscheint nur einmal, mit ihrem aktuellen Stand. An den meisten Tagen ist die morgendliche Zusammenfassung die einzige E-Mail.
- Als zugestellt gilt eine Benachrichtigung, wenn sie auf deinem Handy oder im Browser angezeigt wurde oder Telegram die Nachricht angenommen hat. Ein ausgeschaltetes, offline befindliches Handy oder ein Handy mit deaktivierten Benachrichtigungen zählt nicht. Dasselbe gilt für Telegram, solange du das Dashboard nutzt. Wenn etwas nur auf einem Computer angezeigt wurde, werden dringende oder heute fällige Aufgaben trotzdem per E-Mail gesendet, denn vielleicht bist du gerade nicht da.
- Hast du keine Handy-App, Browserbenachrichtigungen oder Telegram? Dann kommt für alles oben eine E-Mail.
- Telegram ist nicht erreichbar: Die Push-Benachrichtigung wird trotzdem einmal gesendet und Telegram wird automatisch erneut versucht.
- Ein Teammitglied gibt dir eine Aufgabe und deine Machine kann dich weder per Handy noch über Telegram erreichen: Wenn du sie nach 15 Minuten noch nicht gesehen hast, bekommst du eine E-Mail mit dem Titel und einem Link. Deaktiviere dafür **E-Mail** unter **Ergebnisse und Fragen**.
- Deine Claude-Anmeldung läuft innerhalb von 3 Tagen ab oder ist bereits abgelaufen: Du bekommst einmal pro Anmeldung eine E-Mail mit **Erneut anmelden**. Deaktiviere dafür **E-Mail** unter **Ergebnisse und Fragen**.
- Außerhalb deiner Arbeitszeiten: nichts. Die morgendliche Zusammenfassung enthält die Aufgaben.
- Eine neue Arbeitsaufgabe an einem freien Tag wartet bis zur Uhrzeit der Zusammenfassung am nächsten Arbeitstag. Bei der Aufgabe wird angezeigt, wann sie dich erreicht, zum Beispiel „Benachrichtigung Mo., 2. Nov. · 08:30“.

Fortschritte und Änderungen lösen keine Benachrichtigungen aus. Gibt es ein neues Ergebnis zu einer Aufgabe, die du noch nicht gesehen hast, wird die Aufgabe aktualisiert, ohne eine neue Benachrichtigung zu senden. Mehrere Benachrichtigungen auf einmal führen zu einer einzigen. Das App-Symbol zeigt an, wie viele Aufgaben deine Aufmerksamkeit brauchen.

## Schaltflächen in Benachrichtigungen

Jede Benachrichtigung hat Schaltflächen für den nächsten Schritt. In der Handy-App:

- Neue Aufgabe: **Ausführen**, **Zurückstellen**, **Als erledigt markieren**.
- Entwurf bereit: **Entwurf öffnen**, **Zurückstellen**, **Als erledigt markieren**.
- Ergebnis bereit: **Öffnen**, **Als erledigt markieren**, **Zurückstellen**.
- Deine Antwort wird gebraucht, etwas steckt fest oder eine Anmeldung ist nötig: **Antworten**, **Öffnen** oder **Anmelden**, danach **Zurückstellen** und **Als erledigt markieren**.
- Erinnerung: **Als erledigt markieren**, **Zurückstellen**, **Öffnen**.
- Morgendliche Zusammenfassung: Tippe darauf, um sie zu öffnen.

Im Browser und in Telegram werden zwei davon angezeigt. Bei Fragen zu einer Fleet gibt es weiterhin die Schaltflächen **Antworten** und **Ablehnen**.

Über eine Benachrichtigung wird nichts gesendet, bezahlt oder eingereicht. Ein Entwurf wird immer zuerst geöffnet, damit du ihn vor dem Senden sehen kannst. **Entwurf öffnen** zeigt die Aufgabe mit dem vollständigen Entwurf in deiner Liste. **Ausführen** startet nur die Arbeit an einer neuen Aufgabe.

In der Handy-App musst du dein Gerät erst entsperren, bevor du **Zurückstellen** oder **Als erledigt markieren** auswählen kannst. Im Browser wird das Dashboard geöffnet. Dort wird die Aktion ausgeführt und du kannst sie rückgängig machen. Bei **Zurückstellen** steht die Aufgabe in zwei Stunden wieder an, bei einer Erinnerung am nächsten Morgen.

E-Mails enthalten Links zum Öffnen und für ausstehende Aufgaben auch zum Zurückstellen. Diese Links öffnen nur das Dashboard.

Wenn du auf eine Benachrichtigung oder in einer E-Mail oder Telegram-Nachricht auf **Öffnen** tippst, wird die Aufgabe in deiner Liste hervorgehoben, egal in welcher Ansicht sie sich gerade befindet: **Gerade erledigt**, **Erledigt**, **Kommt später zurück** oder eine andere Ansicht. Der Chat wird nie geöffnet. Falls die Seite noch nicht auf dem neuesten Stand war, wird die Aufgabe angezeigt, sobald sie aktualisiert ist.

## Die morgendliche Zusammenfassung

Sie kommt an Arbeitstagen zur Uhrzeit unter **Morgendliche Zusammenfassung**, sofern es etwas zu berichten gibt. Liegt diese Uhrzeit vor **Zurückgestelltes kommt um**, wird die Zusammenfassung bis 5 Minuten danach zurückgehalten, damit die an diesem Morgen wieder anstehenden Aufgaben enthalten sind. Mit **Vorschau** kannst du sie ansehen, ohne sie zu senden. Standardmäßig bekommst du sie als Push-Benachrichtigung und E-Mail. Sie ist kurz genug, um sie auf einen Blick zu lesen:

- eine Begrüßung mit dem Wichtigsten für heute, zum Beispiel „Guten Morgen Sam, 2 Antworten können gesendet werden“ oder, wenn es um eine Aufgabe geht, „Guten Morgen Sam, wartet auf dein Okay: Bestellformular senden“. Als bereit gelten nur Aufgaben mit einem Entwurf oder Ergebnis, das du freigeben musst. Eine Aufgabe, bei der zuerst deine Antwort gebraucht wird, zählt nicht dazu;
- die Aufgaben, die in der Begrüßung gezählt werden, jeweils mit einem Link zum Öffnen, sowie alles, was heute fällig ist. Andernfalls werden höchstens drei Aufgaben angezeigt;
- bis zu fünf Aufgaben, die du selbst hinzugefügt hast und die auf dich warten, unabhängig davon, was in der Begrüßung gezählt wird;
- wie viele weitere Aufgaben warten können und wie lange du bei deinem Tempo dafür brauchst, zum Beispiel „12 weitere können warten, etwa 5 Min. zum Abarbeiten.“ Aufgaben, bei denen deine Antwort gebraucht wird, zählen nicht zu dieser Zeit. Eine heute fällige Aufgabe, die bis später zurückgestellt wurde, oder eine, an der The Machine noch arbeitet, wird erst gezählt, wenn sie auf dich wartet. Die Anzahl stimmt mit den Aufgaben überein, die in deiner Liste auf dich warten.
- deine Besprechungen in einer Zeile.

Über **Öffnen** wird die Aufgabe in deiner Liste hervorgehoben, auch wenn sie erledigt oder zurückgestellt ist. Über ein Versprechen wird die zugehörige Aufgabe geöffnet oder, falls es noch keine gibt, die eigene Seite des Versprechens.

Die Push-Benachrichtigung enthält dieselben Informationen, aber keine Links. Tippe darauf oder auf den Link am Ende der E-Mail, um diese Zusammenfassung erneut unter **Aufgaben** zu lesen.

## Die abendliche Zusammenfassung

Sie kommt an Arbeitstagen einmal zur Uhrzeit, die du unter **Arbeitszeiten** festgelegt hast, standardmäßig 15 Minuten vor **Bis**, und über die Kanäle, die du oben in der Zeile dafür ausgewählt hast. Sie kommt nur an einem Tag, an dem du da warst: Du hast das Dashboard genutzt oder dort, in Telegram, im Chat oder per Sprachbefehl eine Entscheidung zu einer Aufgabe getroffen. Wenn an dem Tag keine Aufgabe erledigt und keine Besprechung abgehalten wurde, bekommst du keine Zusammenfassung.

Sie beginnt mit einer Tagesbilanz, zum Beispiel „Guten Abend Sam, heute 4 Aufgaben erledigt“, gefolgt von einem Bereich **Arbeit** und einem Bereich **Privat**. Ein leerer Bereich wird ausgelassen. Eine Warnung zu deiner Machine selbst erscheint in keinem der beiden Bereiche. In jedem Bereich findest du:

- **Heute erledigt**: bis zu drei Aufgaben, die du oder deine Machine abgeschlossen haben, gefolgt von „+12 weitere“ und den Besprechungen des Tages, zum Beispiel „+3 Besprechungen: Preisgespräch und 2 weitere“;
- **Offen für morgen** (am Freitag für deinen nächsten Arbeitstag): die ersten Besprechungen und alles, was fällig ist.

Am Ende steht, wie viele Aufgaben noch deine Aufmerksamkeit brauchen. Tippe auf die Push-Benachrichtigung oder auf den Link am Ende der E-Mail, um sie mit **Arbeit kopieren** und **Privat kopieren** erneut zu lesen. Deaktiviere die Zeile, um sie abzuschalten.

## Datenschutz

Push-Benachrichtigungen werden verschlüsselt direkt von deiner Machine an dein Gerät gesendet. E-Mails laufen über den Mailserver von The Machine und deinen E-Mail-Anbieter. Wenn [Vorsichtig](security-levels.md) Aufgabentext in Benachrichtigungen ausblendet, enthalten E-Mails nur Zahlenangaben. Deaktiviere **E-Mail** für eine Art, damit dazu keine E-Mails gesendet werden.

Aktiviere Push-Benachrichtigungen für ein Gerät unter **Dieses Gerät** oder lies [App installieren](phone-app.md). Die [Handy-App](mobile-app.md) sendet über Apple oder Google eine einfache Zeile und fragt dann deine Machine nach dem Titel und dem nächsten Schritt.
