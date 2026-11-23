---
title: Benachrichtigungen
area: settings
summary: Was dich erreicht, wo und wann: Nur Dringendes meldet sich laut. Alles andere findest du in einer morgendlichen Zusammenfassung.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: febea6f9eb2c331a
---
Möchtest du weniger oder andere Benachrichtigungen? Wähle unter **Einstellungen** und **Benachrichtigungen** aus, wo du die einzelnen Arten erhältst:

- **Neue Aufgaben**: nur, was nicht warten kann, zum Beispiel etwas, das heute fällig oder dringend ist.
- **Ergebnisse und Fragen**: eine Antwort, die zum Senden bereit ist, eine Anmeldung, die eine Aufgabe erfordert, oder eine Frage zu einer Fleet.
- **Erinnerungen**: zurückgestellte Aufgaben und Antworten, auf die du wartest und die wieder anstehen.
- **Morgendliche Zusammenfassung**: eine kurze Zusammenfassung deines Tages. Mehr dazu weiter unten.
- **Abendliche Zusammenfassung**: was du heute erledigt hast und was morgen noch offen ist. Mehr dazu weiter unten.

Für jede Art gibt es einen Schalter für **Push** (die App auf deinem Handy oder Computer), **Telegram**, sobald es eingerichtet ist, und **E-Mail** auf einer gehosteten Machine oder einer im The Machine Network. Alle sind standardmäßig aktiviert, außer die Zusammenfassungen in Telegram.

Deine **Arbeitszeiten** findest du im selben Tab: Arbeitstage, wann Benachrichtigungen gesendet werden dürfen, wann Zurückgestelltes wieder ansteht, die Zeiten für Zusammenfassungen und deine Zeitzone. Siehe [Arbeitszeiten](work-hours.md).

## Nur Dringendes

Eine Push-Benachrichtigung, ein Signal in Telegram oder eine E-Mail gibt es nur für:

- eine Aufgabe, die heute fällig oder als dringend markiert ist;
- eine Antwort, auf die jemand wartet und die als Entwurf bereit zum Senden ist;
- eine Aufgabe, bei der du dich anmelden musst;
- eine Zurückstellung, die zum von dir gewählten Zeitpunkt endet.

Alles andere erscheint unauffällig auf dem Dashboard (und lautlos in Telegram) und wartet auf die morgendliche Zusammenfassung. An einem freien Tag melden sich nur dringende oder heute fällige Aufgaben. Höchstens 8 Push-Benachrichtigungen pro Tag. Wenn du das Dashboard 3 Tage lang nicht öffnest, erhältst du nur die morgendliche Zusammenfassung, bis du wieder da bist.

## Wann du benachrichtigt wirst

Es wird geprüft, ob du das Dashboard tatsächlich nutzt, nicht nur, ob es geöffnet ist:

- Wenn du es nutzt (es ist im Vordergrund und du hast in den letzten 10 Minuten geklickt, getippt oder gescrollt), gibt es keine Signale. Telegram-Nachrichten kommen lautlos an. Nur das Öffnen oder Neuladen zählt nicht.
- Wenn du nicht da bist (das Dashboard ist im Hintergrund, geschlossen oder seit 10 Minuten inaktiv), wird eine Minute nach deinem Weggehen eine Push-Benachrichtigung gesendet, sofern du nicht zurückgekommen bist und sie gesehen hast.
- Wenn du sie 15 Minuten später immer noch nicht gesehen hast und die Sache nicht warten kann, gibt es dafür eine E-Mail, höchstens eine pro Stunde. Was du bereits erledigt hast, wird ausgelassen. Jede Aufgabe erscheint nur einmal und so, wie sie gerade aussieht. An den meisten Tagen ist die morgendliche Zusammenfassung die einzige E-Mail.
- Wenn dir ein Teammitglied eine Aufgabe zuweist und deine Machine weder ein Handy noch Telegram hat, um dich zu erreichen, erhältst du eine E-Mail mit dem Titel und einem Link, sofern du die Aufgabe 15 Minuten später immer noch nicht gesehen hast. Wenn du **E-Mail** für **Ergebnisse und Fragen** deaktivierst, wird diese E-Mail ausgeschaltet.
- Außerhalb deiner Arbeitszeiten gibt es keine Benachrichtigungen. Die morgendliche Zusammenfassung enthält die Aufgaben.
- Eine neue Aufgabe für die Arbeit an einem freien Tag wartet bis zur Zusammenfassungszeit an deinem nächsten Arbeitstag. Bei der Aufgabe steht, wann sie dich erreicht, zum Beispiel: Benachrichtigung Mo., 2. Nov. · 08:30.

Fortschritte und Änderungen lösen keine Benachrichtigungen aus. Ein neues Ergebnis zu einer Aufgabe, die du noch nicht gesehen hast, aktualisiert sie ohne neue Benachrichtigung. Mehrere Benachrichtigungen kurz hintereinander lösen nur ein Signal aus. Das App-Symbol zeigt, wie viele Aufgaben deine Aufmerksamkeit brauchen.

## Schaltflächen in Benachrichtigungen

Jede Benachrichtigung hat Schaltflächen für den nächsten Schritt. In der Handy-App:

- Neue Aufgabe: **Ausführen**, **Zurückstellen**, **Erledigt**.
- Entwurf bereit: **Entwurf öffnen**, **Zurückstellen**, **Erledigt**.
- Ergebnis bereit: **Öffnen**, **Erledigt**, **Zurückstellen**.
- Frage, Problem oder Anmeldung: **Antworten**, **Öffnen** oder **Anmelden**, dann **Zurückstellen** und **Erledigt**.
- Erinnerung: **Erledigt**, **Zurückstellen**, **Öffnen**.
- Morgendliche Zusammenfassung: Tippe darauf, um sie zu öffnen.

Im Browser und in Telegram werden jeweils zwei Schaltflächen angezeigt. Bei Fragen zu einer Fleet bleiben **Einmal antworten** und **Ablehnen** verfügbar.

Über eine Benachrichtigung wird nichts gesendet, bezahlt oder eingereicht. Ein Entwurf wird immer zuerst geöffnet, damit du ihn siehst, bevor er versendet wird. **Entwurf öffnen** zeigt die Aufgabe mit dem vollständigen Entwurf in deiner Liste. **Ausführen** startet nur die Arbeit an einer neuen Aufgabe.

In der Handy-App musst du zum **Zurückstellen** oder **Erledigen** zuerst entsperren. Im Browser öffnet sich das Dashboard. Dort wird die Aktion ausgeführt und **Rückgängig** angezeigt. Beim Zurückstellen wird die Aufgabe in zwei Stunden wieder angezeigt oder bei einer Erinnerung am nächsten Morgen.

E-Mails enthalten Links zum **Öffnen** und für wartende Aufgaben auch zum **Zurückstellen**. Über diese Links wird nur das Dashboard geöffnet.

Wenn du auf eine Benachrichtigung tippst oder in einer E-Mail oder Telegram auf **Öffnen**, wird die Aufgabe in deiner Liste hervorgehoben, wo immer sie sich gerade befindet: **Gerade erledigt**, **Erledigt**, **Kommt später zurück** oder in einer anderen Ansicht. Der Chat wird dabei nie geöffnet. Falls die Seite noch nicht auf dem aktuellen Stand war, wird die Aufgabe angezeigt, sobald sie es ist.

## Die morgendliche Zusammenfassung

Sie kommt an Arbeitstagen zur eingestellten Zeit für **Morgendliche Zusammenfassung**, sofern es etwas zu berichten gibt. Liegt diese Zeit vor **Zurückgestelltes kommt um**, wird die Zusammenfassung bis 5 Minuten danach zurückgehalten, damit die Aufgaben enthalten sind, die an diesem Morgen wieder anstehen. Mit **Vorschau** kannst du sie ansehen, ohne sie zu senden. Standardmäßig kommt sie als Push-Benachrichtigung und E-Mail. Sie ist kurz genug, um sie auf einen Blick zu lesen:

- eine Begrüßung mit dem Wichtigsten für heute, zum Beispiel „Guten Morgen Sam, 2 Antworten sind bereit zum Senden“ oder bei einer Aufgabe „Guten Morgen Sam, bereit für dein OK: Bestellformular senden“. Als bereit zählen nur Aufgaben mit einem Entwurf oder einem Ergebnis, das du bestätigen musst. Aufgaben, bei denen zuerst deine Antwort nötig ist, zählen nicht dazu;
- die Aufgaben, die in der Begrüßung gezählt werden, jeweils mit einem Link zum Öffnen, sowie alles, was heute fällig ist. Andernfalls werden höchstens drei Aufgaben aufgeführt;
- bis zu fünf Aufgaben, die du selbst hinzugefügt hast und bei denen du noch etwas tun musst, unabhängig davon, was in der Begrüßung gezählt wird;
- wie viele weitere Aufgaben warten können und wie lange sie bei deinem Tempo dauern, zum Beispiel „12 weitere können warten, etwa 5 Min. zum Erledigen.“ Aufgaben, bei denen deine Antwort fehlt, werden dabei nicht mitgerechnet. Eine Aufgabe, die heute fällig ist, aber bis später zurückgestellt wurde, oder an der The Machine noch arbeitet, wird erst gezählt, wenn sie auf dich wartet. Die Anzahl entspricht den Aufgaben, die in deiner Liste auf dich warten.
- deine Termine in einer Zeile.

**Öffnen** zeigt die Aufgabe in deiner Liste, hervorgehoben, auch wenn sie erledigt oder zurückgestellt ist. Ein Versprechen öffnet die zugehörige Aufgabe oder, falls es noch keine gibt, die eigene Seite.

Die Push-Benachrichtigung enthält denselben Text, aber ohne Links. Tippe darauf oder auf den Link am Ende der E-Mail, um diese Zusammenfassung unter **Aufgaben** noch einmal zu lesen.

## Die abendliche Zusammenfassung

Sie kommt an Arbeitstagen einmal zur dafür unter **Arbeitszeiten** eingestellten Zeit. Standardmäßig ist das 15 Minuten vor **Bis**. Sie wird über die oben in ihrer Zeile ausgewählten Kanäle gesendet. Du erhältst sie nur an einem Tag, an dem du aktiv warst: Du hast das Dashboard genutzt oder dort, in Telegram, im Chat oder per Sprache eine Entscheidung zu einer Aufgabe getroffen. Wenn an dem Tag keine Aufgabe erledigt und kein Termin wahrgenommen wurde, erhältst du keine Zusammenfassung.

Sie beginnt mit einer Tagesbilanz, zum Beispiel „Guten Abend Sam, heute 4 Aufgaben erledigt“, gefolgt von einem Abschnitt **Arbeit** und einem Abschnitt **Privat**. Abschnitte ohne Einträge werden ausgelassen. Jeder Abschnitt enthält:

- **Heute erledigt**: bis zu drei Aufgaben, die du oder deine Machine erledigt habt, danach „+12 weitere“ und die Termine des Tages, zum Beispiel „+3 Termine: Preisgespräch und 2 weitere“;
- **Offen für morgen** (am Freitag für deinen nächsten Arbeitstag): die ersten Termine und alles, was fällig ist.

Zum Schluss steht, wie viele Aufgaben noch deine Aufmerksamkeit brauchen. Tippe auf die Push-Benachrichtigung oder auf den Link am Ende der E-Mail, um die Zusammenfassung mit **Arbeit kopieren** und **Privat kopieren** noch einmal zu lesen. Um sie abzuschalten, deaktiviere den Schalter in ihrer Zeile.

## Datenschutz

Push-Benachrichtigungen werden von deiner Machine direkt und verschlüsselt an dein Gerät gesendet. E-Mails laufen über den Mailserver von The Machine und deinen E-Mail-Anbieter. Wenn [Vorsichtig](security-levels.md) Aufgabentexte in Benachrichtigungen ausblendet, enthalten E-Mails nur noch Zahlen. Deaktiviere **E-Mail** für eine Art, damit dazu keine E-Mails mehr gesendet werden.

Aktiviere Push-Benachrichtigungen für ein Gerät unter **Dieses Gerät** oder lies [App installieren](phone-app.md). Die [Handy-App](mobile-app.md) erhält eine einfache Benachrichtigung über Apple oder Google und fragt dann deine Machine nach dem Titel und dem nächsten Schritt.
