---
title: Benachrichtigungen
area: settings
summary: Was dich wann und wo erreicht: Nur Dringendes meldet sich, alles andere steht in einer morgendlichen Zusammenfassung.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 3faac166e8f9fa3d
---
Möchtest du weniger oder andere Benachrichtigungen? Wähle unter **Einstellungen** > **Benachrichtigungen**, auf welchen Kanälen dich die einzelnen Arten erreichen:

- **Neue Aufgaben**: nur, was nicht warten kann, zum Beispiel etwas, das heute fällig oder dringend ist.
- **Ergebnisse und Fragen**: eine Antwort, die zum Senden bereit ist, eine Aufgabe, für die du dich anmelden musst, oder eine Frage aus einer Fleet.
- **Erinnerungen**: zurückgestellte Aufgaben und Antworten, auf die du wartest und zu denen es Neuigkeiten gibt.
- **Morgendliche Zusammenfassung**: eine kurze Zusammenfassung deines Tages. Mehr dazu weiter unten.
- **Abendliche Zusammenfassung**: was heute erledigt wurde und was morgen noch offen ist. Mehr dazu weiter unten.

Für jede Art kannst du **Push** (in der App auf deinem Handy oder Computer), **Telegram**, sobald es eingerichtet ist, und **E-Mail** auf einer gehosteten Machine oder einer im The Machine Network aktivieren. Alles ist aktiviert, außer den Zusammenfassungen auf Telegram.

Deine **Arbeitszeiten** findest du im selben Tab: Arbeitstage, Zeiten, zu denen Benachrichtigungen gesendet werden dürfen, wann Zurückgestelltes wieder auftaucht, die Zeiten für Zusammenfassungen und deine Zeitzone. Mehr dazu unter [Arbeitszeiten](work-hours.md).

## Nur, was nicht warten kann

Eine Push-Benachrichtigung, ein Signal auf Telegram oder eine E-Mail wird nur gesendet bei:

- einer Aufgabe, die heute fällig oder als dringend markiert ist;
- einer Antwort, auf die jemand wartet und die fertig formuliert und versandbereit ist;
- einer Aufgabe, für die du dich anmelden musst;
- einer Zurückstellung, die zum von dir gewählten Zeitpunkt endet.

Alles andere erscheint unauffällig im Dashboard und ohne Ton auf Telegram. Es wartet dort auf die morgendliche Zusammenfassung. An einem freien Tag melden sich nur dringende oder heute fällige Aufgaben. Du erhältst höchstens 8 Push-Benachrichtigungen pro Tag. Wenn du das Dashboard 3 Tage lang nicht öffnest, erhältst du nur noch die morgendliche Zusammenfassung, bis du wieder da bist.

## Wann Benachrichtigungen gesendet werden

Es wird geprüft, ob du das Dashboard tatsächlich nutzt, nicht nur, ob es geöffnet ist:

- Wenn du es gerade verwendest (es ist im Vordergrund und du hast in den letzten 10 Minuten geklickt, getippt oder gescrollt), gibt es keine Signale. Telegram-Nachrichten kommen ohne Ton an. Nur das Öffnen oder Neuladen des Dashboards zählt nicht.
- Wenn du nicht da bist (das Dashboard ist im Hintergrund, geschlossen oder seit 10 Minuten inaktiv), wird eine Minute nach deinem Weggehen eine Push-Benachrichtigung gesendet, sofern du nicht zurückgekehrt bist und sie gesehen hast.
- Ist eine Benachrichtigung nach 15 Minuten noch ungesehen und kann sie nicht warten, wird dazu eine E-Mail gesendet, höchstens eine pro Stunde. Was du schon erledigt hast, wird ausgelassen. Jede Aufgabe erscheint nur einmal und zeigt den aktuellen Stand. An den meisten Tagen ist die morgendliche Zusammenfassung die einzige E-Mail.
- Wenn ein Teammitglied dir eine Aufgabe übergibt und deine Machine dich weder per Handy noch über Telegram erreichen kann, erhältst du nach 15 Minuten eine E-Mail mit dem Titel und einem Link, sofern du die Aufgabe noch nicht gesehen hast. Deaktiviere **E-Mail** für **Ergebnisse und Fragen**, um das auszuschalten.
- Außerhalb deiner Arbeitszeiten passiert nichts. Die Aufgabe erscheint in der morgendlichen Zusammenfassung.
- Eine neue Arbeitsaufgabe an einem freien Tag wartet bis zur Zusammenfassungszeit am nächsten Arbeitstag. Bei der Aufgabe steht, wann sie dich erreicht, zum Beispiel: Benachrichtigung Mo., 2. Nov. · 08:30.

Fortschritte und Änderungen lösen keine Benachrichtigungen aus. Gibt es ein neueres Ergebnis zu einer Aufgabe, die du noch nicht gesehen hast, wird es dort aktualisiert, ohne eine neue Benachrichtigung zu senden. Mehrere Signale kurz hintereinander lösen nur eine Benachrichtigung aus. Das App-Symbol zeigt an, wie viele Aufgaben deine Aufmerksamkeit brauchen.

## Schaltflächen in Benachrichtigungen

Jede Benachrichtigung hat Schaltflächen für den nächsten Schritt. In der Handy-App:

- Neue Aufgabe: **Ausführen**, **Zurückstellen**, **Erledigt**.
- Entwurf bereit: **Entwurf öffnen**, **Zurückstellen**, **Erledigt**.
- Ergebnis bereit: **Öffnen**, **Erledigt**, **Zurückstellen**.
- Deine Antwort wird gebraucht, etwas hängt fest oder du musst dich anmelden: **Antworten**, **Öffnen** oder **Anmelden**, dann **Zurückstellen** und **Erledigt**.
- Erinnerung: **Erledigt**, **Zurückstellen**, **Öffnen**.
- Morgendliche Zusammenfassung: Tippe darauf, um sie zu öffnen.

Im Browser und auf Telegram werden jeweils zwei davon angezeigt. Bei Fragen zu einer Fleet gibt es außerdem die Schaltflächen **Antworten** und **Ablehnen**.

Über eine Benachrichtigung wird nichts gesendet, bezahlt oder eingereicht. Ein Entwurf wird immer zuerst geöffnet, damit du ihn vor dem Senden sehen kannst. **Entwurf öffnen** zeigt die Aufgabe samt vollständigem Entwurf in deiner Liste an. **Ausführen** startet nur die Arbeit an einer neuen Aufgabe.

In der Handy-App musst du zum **Zurückstellen** oder **Erledigen** erst dein Gerät entsperren. Im Browser öffnen die Schaltflächen das Dashboard. Dort wird die Aktion ausgeführt und du kannst sie rückgängig machen. Durch **Zurückstellen** erscheint die Aufgabe nach zwei Stunden wieder, bei einer Erinnerung am nächsten Morgen.

E-Mails enthalten Links zum Öffnen und für Aufgaben, auf die du wartest, auch zum Zurückstellen. Sie öffnen nur das Dashboard.

Wenn du auf eine Benachrichtigung oder in einer E-Mail oder auf Telegram auf **Öffnen** tippst, wird die Aufgabe in deiner Liste hervorgehoben, egal, wo sie gerade ist: **Gerade erledigt**, **Erledigt**, **Kommt später zurück** oder eine andere Ansicht. Der Chat wird nie geöffnet. Falls die Seite noch nicht auf dem neuesten Stand war, wird die Aufgabe angezeigt, sobald sie aktualisiert ist.

## Die morgendliche Zusammenfassung

Sie wird an Arbeitstagen zur Zeit für **Morgendliche Zusammenfassung** gesendet, sofern es etwas zu berichten gibt. Liegt dieser Zeitpunkt vor **Zurückgestelltes kommt um**, wartet die Zusammenfassung bis 5 Minuten danach, damit auch die Aufgaben enthalten sind, die an diesem Morgen wieder auftauchen. Mit **Vorschau** kannst du sie ansehen, ohne sie zu senden. Standardmäßig kommt sie als Push-Benachrichtigung und per E-Mail. Sie ist kurz genug, um sie auf einen Blick zu lesen:

- eine Begrüßung mit dem Wichtigsten für heute, zum Beispiel „Guten Morgen Sam, 2 Antworten sind versandbereit“ oder bei einer Aufgabe „Guten Morgen Sam, wartet auf dein OK: Bestellformular senden“. Als bereit zählen nur Aufgaben mit einem Entwurf oder Ergebnis, das freigegeben werden muss. Aufgaben, bei denen zuerst deine Antwort gebraucht wird, zählen nicht dazu;
- die Aufgaben, die in der Begrüßung gezählt werden, jeweils mit einem Link zum Öffnen, sowie alles, was heute fällig ist. Gibt es das nicht, werden höchstens drei Aufgaben aufgeführt;
- bis zu fünf Aufgaben, die du selbst hinzugefügt hast und bei denen du am Zug bist, unabhängig davon, was in der Begrüßung gezählt wird;
- wie viele weitere Aufgaben warten können und wie lange du bei deinem Tempo dafür brauchst, zum Beispiel „12 weitere können warten, etwa 5 Min. zum Erledigen.“ Aufgaben, bei denen deine Antwort gebraucht wird, zählen nicht mit. Eine heute fällige Aufgabe, die bis später zurückgestellt wurde, oder an der The Machine noch arbeitet, wird erst gezählt, wenn du am Zug bist. Die Anzahl entspricht den Aufgaben, die in deiner Liste auf dich warten;
- deine Termine in einer Zeile.

Über **Öffnen** wird die Aufgabe in deiner Liste hervorgehoben, auch wenn sie erledigt oder zurückgestellt ist. Über ein Versprechen wird die zugehörige Aufgabe geöffnet oder, falls es noch keine gibt, die Seite des Versprechens.

Die Push-Benachrichtigung enthält dieselben Informationen, aber keine Links. Tippe darauf oder auf den Link am Ende der E-Mail, um die Zusammenfassung unter **Aufgaben** erneut aufzurufen.

## Die abendliche Zusammenfassung

Sie wird an Arbeitstagen einmal zur dafür festgelegten Zeit unter **Arbeitszeiten** gesendet, standardmäßig 15 Minuten vor **Bis** und über die in der Zeile oben ausgewählten Kanäle. Sie wird nur an Tagen gesendet, an denen du da warst: Du hast das Dashboard verwendet oder dort, auf Telegram, im Chat oder per Sprache eine Entscheidung zu einer Aufgabe getroffen. Wenn an dem Tag keine Aufgabe erledigt und kein Termin wahrgenommen wurde, kommt keine Zusammenfassung.

Am Anfang steht eine Zusammenfassung des Tages, zum Beispiel „Guten Abend Sam, heute 4 Aufgaben erledigt“. Danach folgen die Bereiche **Arbeit** und **Privat**. Ein leerer Bereich wird ausgelassen. Jeder Bereich enthält:

- **Heute erledigt**: bis zu drei Aufgaben, die du oder deine Machine abgeschlossen habt, dann „+12 weitere“ und die Termine des Tages, zum Beispiel „+3 Termine: Preisgespräch und 2 weitere“;
- **Offen für morgen** (am Freitag für deinen nächsten Arbeitstag): die ersten Termine und alles, was fällig ist.

Am Ende steht, wie viele Aufgaben noch deine Aufmerksamkeit brauchen. Tippe auf die Push-Benachrichtigung oder auf den Link am Ende der E-Mail, um die Zusammenfassung mit **Arbeit kopieren** und **Privat kopieren** erneut aufzurufen. Deaktiviere die entsprechende Zeile, um sie abzuschalten.

## Datenschutz

Push-Benachrichtigungen werden von deiner Machine direkt und verschlüsselt an dein Gerät gesendet. E-Mails laufen über den Mailserver von The Machine und deinen E-Mail-Anbieter. Wenn [Sorgfältig](security-levels.md) Aufgabentexte in Benachrichtigungen ausblendet, enthalten E-Mails nur Zahlenangaben. Deaktiviere **E-Mail** für eine Art, damit sie nicht per E-Mail gesendet wird.

Aktiviere Push-Benachrichtigungen für ein Gerät unter **Dieses Gerät** oder sieh dir [App installieren](phone-app.md) an. Die [Handy-App](mobile-app.md) sendet eine einfache Benachrichtigung über Apple oder Google und fragt dann deine Machine nach dem Titel und dem nächsten Schritt.
