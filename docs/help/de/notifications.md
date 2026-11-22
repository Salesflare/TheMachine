---
title: Benachrichtigungen
area: settings
summary: Was dich wo und wann erreicht: Nur was nicht warten kann, macht sich bemerkbar. Alles andere findest du in einer morgendlichen Zusammenfassung.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: aab523e3a774400b
---
Weniger oder andere Benachrichtigungen? Wähle unter **Einstellungen** und **Benachrichtigungen** aus, wo dich die einzelnen Arten erreichen:

- **Neue Aufgaben**: nur was nicht warten kann, etwa wenn etwas heute fällig oder dringend ist.
- **Ergebnisse und Fragen**: ein Entwurf, der bereit zum Senden ist, eine Anmeldung, die eine Aufgabe braucht, oder eine Frage aus der Fleet.
- **Erinnerungen**: zurückgestellte Aufgaben und Antworten, auf die du wartest, wenn sie wiederkommen.
- **Morgendliche Zusammenfassung**: eine kurze Zusammenfassung deines Tages. Mehr dazu weiter unten.
- **Abendliche Zusammenfassung**: was heute erledigt wurde und was morgen noch offen ist. Mehr dazu weiter unten.

Für jede Art kannst du **Push** (die App auf deinem Handy oder Computer), **Telegram**, sobald es eingerichtet ist, und **E-Mail** auf einer gehosteten Machine oder einer im The Machine Network ein- und ausschalten. Alles ist eingeschaltet, außer den Zusammenfassungen bei Telegram.

Deine **Arbeitszeiten** findest du im selben Tab: Arbeitstage, wann Benachrichtigungen gesendet werden dürfen, wann zurückgestellte Aufgaben wieder auftauchen, die Zeiten der Zusammenfassungen und deine Zeitzone. Mehr dazu unter [Arbeitszeiten](work-hours.md).

## Nur was nicht warten kann

Eine Push-Benachrichtigung, eine Telegram-Nachricht mit Ton oder eine E-Mail wird nur gesendet bei:

- einer Aufgabe, die heute fällig oder als dringend markiert ist;
- einem Entwurf, der bereit zum Senden ist und auf den jemand wartet;
- einer Aufgabe, bei der du dich anmelden musst;
- einer zurückgestellten Aufgabe, die zum gewählten Zeitpunkt wieder auftaucht.

Alles andere erscheint unauffällig im Dashboard und ohne Ton bei Telegram. Dort wartet es auf die morgendliche Zusammenfassung. An einem freien Tag machen sich nur dringende oder heute fällige Aufgaben bemerkbar. Du erhältst höchstens 8 Push-Benachrichtigungen am Tag. Wenn du das Dashboard 3 Tage lang nicht öffnest, kommt nur die morgendliche Zusammenfassung, bis du wieder da bist.

## Wann Benachrichtigungen gesendet werden

Die App prüft, ob du das Dashboard tatsächlich verwendest, nicht nur, ob es geöffnet ist:

- Wenn du es verwendest, also wenn es im Vordergrund ist und du in den letzten 10 Minuten geklickt, getippt oder gescrollt hast, macht sich nichts bemerkbar. Telegram-Benachrichtigungen kommen ohne Signalton an. Es zählt nicht, wenn du das Dashboard nur öffnest oder neu lädst.
- Wenn du nicht da bist, also wenn das Dashboard im Hintergrund oder geschlossen ist oder du 10 Minuten lang nichts damit gemacht hast, wird eine Minute nach deinem Weggehen eine Push-Benachrichtigung gesendet, sofern du nicht zurückgekommen bist und sie gesehen hast.
- Wenn du die Benachrichtigung auch 15 Minuten später noch nicht gesehen hast und sie nicht warten kann, erhältst du eine E-Mail dazu, höchstens eine pro Stunde. Was du schon erledigt hast, wird ausgelassen. An den meisten Tagen ist die morgendliche Zusammenfassung die einzige E-Mail.
- Wenn dir ein Teammitglied eine Aufgabe zuweist und deine Machine weder ein Handy noch Telegram hat, über das sie dich erreichen kann, erhältst du eine E-Mail mit dem Titel und einem Link, wenn du sie nach 15 Minuten noch nicht gesehen hast. Deaktiviere **E-Mail** für **Ergebnisse und Fragen**, um das auszuschalten.
- Außerhalb deiner Arbeitszeiten passiert nichts. Die morgendliche Zusammenfassung enthält die Aufgabe.
- Eine neue Aufgabe für die Arbeit an einem freien Tag wartet bis zur Uhrzeit deiner Zusammenfassung am nächsten Arbeitstag. Bei der Aufgabe siehst du, wann sie dich erreicht, zum Beispiel: Benachrichtigung Mo., 2. Nov. · 08:30.

Fortschritte und Änderungen lösen keine Benachrichtigungen aus. Gibt es ein neueres Ergebnis zu einer Aufgabe, die du noch nicht gesehen hast, wird sie aktualisiert, ohne dass eine neue Benachrichtigung gesendet wird. Mehrere auf einmal vibrieren nur einmal. Auf dem App-Symbol siehst du, wie viele Aufgaben deine Aufmerksamkeit brauchen.

## Schaltflächen in Benachrichtigungen

Jede Benachrichtigung hat Schaltflächen für den nächsten Schritt. In der Handy-App:

- Neue Aufgabe: **Ausführen**, **Zurückstellen**, **Als erledigt markieren**.
- Entwurf bereit: **Entwurf öffnen**, **Zurückstellen**, **Als erledigt markieren**.
- Ergebnis bereit: **Öffnen**, **Als erledigt markieren**, **Zurückstellen**.
- Frage, festgefahrene Aufgabe oder Anmeldung: **Antworten**, **Öffnen** oder **Anmelden**, danach **Zurückstellen** und **Als erledigt markieren**.
- Erinnerung: **Als erledigt markieren**, **Zurückstellen**, **Öffnen**.
- Morgendliche Zusammenfassung: Zum Öffnen antippen.

Im Browser und bei Telegram werden jeweils zwei davon angezeigt. Bei Fragen aus der Fleet bleiben **Einmal antworten** und **Ablehnen**.

Über eine Benachrichtigung wird nichts gesendet, bezahlt oder abgeschickt. Ein Entwurf wird immer zuerst geöffnet, damit du ihn prüfen kannst, bevor er gesendet wird. **Entwurf öffnen** zeigt die Aufgabe mit dem vollständigen Entwurf in deiner Liste. **Ausführen** startet nur die Arbeit an einer neuen Aufgabe.

In der Handy-App musst du für **Zurückstellen** und **Als erledigt markieren** dein Gerät erst entsperren. Im Browser öffnen sie das Dashboard, das die Aktion ausführt und **Rückgängig** anzeigt. Beim Zurückstellen taucht die Aufgabe in zwei Stunden wieder auf oder, bei einer Erinnerung, am nächsten Morgen.

E-Mails enthalten Links zum Öffnen und bei Aufgaben, die warten, auch zum Zurückstellen. Die Links öffnen nur das Dashboard.

Wenn du eine Benachrichtigung antippst oder in einer E-Mail oder bei Telegram auf **Öffnen** tippst, wird die Aufgabe an ihrer aktuellen Stelle in deiner Liste hervorgehoben: **Gerade erledigt**, **Erledigt**, **Kommt später zurück** oder in einer anderen Ansicht. Der Chat wird nie geöffnet. Falls die Seite noch nicht aktuell war, folgt sie der Aufgabe, sobald sie aktualisiert ist.

## Die morgendliche Zusammenfassung

Sie kommt an Arbeitstagen zur Uhrzeit deiner **Morgendlichen Zusammenfassung**, sofern es etwas zu berichten gibt. Liegt diese Uhrzeit vor **Zurückgestelltes kommt um**, wartet die Zusammenfassung bis 5 Minuten danach, damit die Aufgaben enthalten sind, die an diesem Morgen wieder auftauchen. Mit **Vorschau** kannst du sie dir ansehen, ohne sie zu senden. Standardmäßig kommt sie als Push-Benachrichtigung und per E-Mail. Sie ist kurz genug, um sie auf einen Blick zu lesen:

- eine Begrüßung mit dem Wichtigsten für heute, zum Beispiel „Guten Morgen, Sam! 2 Antworten sind bereit zum Senden“ oder bei einer Aufgabe „Guten Morgen, Sam! Wartet auf dein OK: Bestellformular senden“;
- die Aufgaben, auf die sich die Begrüßung bezieht, jeweils mit einem Link zum Öffnen, sowie alles, was heute fällig ist. Andernfalls enthält sie höchstens drei Aufgaben;
- bis zu fünf Aufgaben, die du selbst hinzugefügt hast und die auf dich warten, unabhängig davon, auf wie viele Aufgaben sich die Begrüßung bezieht;
- wie viele weitere Aufgaben warten können und wie lange du in deinem Tempo dafür brauchst, zum Beispiel: „12 weitere können warten, etwa 5 Min. zum Erledigen.“ Aufgaben, die auf deine Antwort warten, sind in dieser Zeit nicht enthalten. Eine heute fällige, aber bis später zurückgestellte Aufgabe oder eine Aufgabe, an der The Machine noch arbeitet, wird erst gezählt, wenn sie auf dich wartet. Die Anzahl entspricht den Aufgaben, die in deiner Liste auf dich warten.
- deine Termine in einer Zeile.

Über **Öffnen** gelangst du zur hervorgehobenen Aufgabe in deiner Liste, auch wenn sie erledigt oder zurückgestellt ist. Über ein Versprechen gelangst du zur zugehörigen Aufgabe oder, falls es noch keine gibt, zur eigenen Seite des Versprechens.

Die Push-Benachrichtigung enthält dasselbe, aber ohne Links. Tippe sie an oder wähle den Link am Ende der E-Mail, um diese Zusammenfassung unter **Aufgaben** erneut aufzurufen.

## Die abendliche Zusammenfassung

Sie kommt an Arbeitstagen einmal zur unter **Arbeitszeiten** eingestellten Uhrzeit, standardmäßig 15 Minuten vor **Bis**, auf den Wegen, die du oben in ihrer Zeile ausgewählt hast. Sie kommt nur an Tagen, an denen du aktiv warst: Du hast das Dashboard verwendet oder dort, bei Telegram, im Chat oder per Sprache eine Entscheidung zu einer Aufgabe getroffen. Wenn du an dem Tag keine Aufgabe erledigt und keinen Termin wahrgenommen hast, erhältst du keine Zusammenfassung.

Sie beginnt mit einer Zusammenfassung des Tages in Zahlen, zum Beispiel: „Guten Abend Sam, heute 4 Aufgaben erledigt“. Danach folgen die Bereiche **Arbeit** und **Privat**. Ein Bereich ohne Inhalte wird ausgelassen. Jeder Bereich enthält:

- **Heute erledigt**: bis zu drei Aufgaben, die du oder deine Machine erledigt habt, danach „+12 weitere“ und die Termine des Tages, zum Beispiel „+3 Termine: Gespräch zu Preisen und 2 weitere“;
- **Offen für morgen** (am Freitag für deinen nächsten Arbeitstag): die ersten Termine und alles, was fällig ist.

Zum Schluss siehst du, wie viele Aufgaben noch deine Aufmerksamkeit brauchen. Tippe auf die Push-Benachrichtigung oder den Link am Ende der E-Mail, um die Zusammenfassung erneut aufzurufen. Dort kannst du **Arbeit kopieren** und **Privat kopieren**. Um die Zusammenfassung nicht mehr zu erhalten, deaktiviere die entsprechende Zeile.

## Datenschutz

Push-Benachrichtigungen werden von deiner Machine direkt und verschlüsselt an dein Gerät gesendet. E-Mails laufen über den Mailserver von The Machine und deinen E-Mail-Anbieter. Wenn [Vorsichtig](security-levels.md) Aufgabentexte in Benachrichtigungen ausblendet, enthalten E-Mails nur Zahlen. Deaktiviere **E-Mail** für eine Benachrichtigungsart, damit sie nicht per E-Mail gesendet wird.

Aktiviere Push-Benachrichtigungen für ein Gerät unter **Dieses Gerät** oder sieh dir [App installieren](phone-app.md) an. Die [Mobil-App](mobile-app.md) erhält über Apple oder Google nur eine schlichte Zeile und fragt dann deine Machine nach dem Titel und dem nächsten Schritt.
