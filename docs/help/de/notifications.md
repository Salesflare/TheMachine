---
title: Benachrichtigungen
area: settings
summary: Was dich wo und wann erreicht: Nur Dringendes macht sich bemerkbar, alles andere findest du in einer morgendlichen Zusammenfassung.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 4f777fac22dba7c0
---
Weniger Benachrichtigungen oder andere? Wähle in **Einstellungen** unter **Benachrichtigungen** aus, auf welchem Weg dich die einzelnen Arten erreichen:

- **Neue Aufgaben**: nur Dringendes, zum Beispiel etwas, das heute fällig oder dringend ist.
- **Ergebnisse und Fragen**: ein Entwurf, der versandbereit ist, eine Anmeldung, die für eine Aufgabe nötig ist, oder eine Frage von Fleet.
- **Erinnerungen**: zurückgestellte Aufgaben und Antworten, auf die du wartest und die wieder anstehen.
- **Morgendliche Zusammenfassung**: eine kurze Zusammenfassung deines Tages. Mehr dazu weiter unten.
- **Abendliche Zusammenfassung**: was du heute erledigt hast und was morgen noch offen ist. Mehr dazu weiter unten.

Für jede Art gibt es einen Schalter für **Push** (die App auf deinem Smartphone oder Computer), **Telegram**, sobald es eingerichtet ist, und **E-Mail** auf einer gehosteten Machine oder einer im The Machine Network. Alles ist eingeschaltet, außer den Zusammenfassungen in Telegram.

Deine **Arbeitszeiten** findest du im selben Tab: Arbeitstage, wann Benachrichtigungen gesendet werden dürfen, wann Zurückgestelltes wieder ansteht, die Zeiten der Zusammenfassungen und deine Zeitzone. Mehr dazu unter [Arbeitszeiten](work-hours.md).

## Nur Dringendes

Eine Push-Benachrichtigung, ein Signal in Telegram oder eine E-Mail wird nur gesendet, wenn:

- eine Aufgabe heute fällig oder als dringend markiert ist;
- eine Antwort, auf die jemand wartet, als Entwurf bereit zum Senden ist;
- du dich für eine Aufgabe anmelden musst;
- eine zurückgestellte Aufgabe zur von dir gewählten Zeit wieder ansteht.

Alles andere erscheint unauffällig auf dem Dashboard und lautlos in Telegram und wartet auf die morgendliche Zusammenfassung. An einem freien Tag macht sich nur bemerkbar, was dringend oder heute fällig ist. Es gibt höchstens 8 Push-Benachrichtigungen pro Tag. Wenn du das Dashboard 3 Tage lang nicht öffnest, erhältst du nur die morgendliche Zusammenfassung, bis du wieder da bist.

## Wann Benachrichtigungen gesendet werden

The Machine prüft, ob du das Dashboard tatsächlich verwendest, nicht nur, ob es geöffnet ist:

- Wenn du es verwendest (es ist im Vordergrund und du hast in den letzten 10 Minuten geklickt, getippt oder gescrollt): nichts macht sich bemerkbar. Telegram-Nachrichten kommen lautlos an. Nur das Öffnen oder Neuladen zählt nicht.
- Wenn du gerade nicht da bist (das Dashboard läuft im Hintergrund, ist geschlossen oder war 10 Minuten inaktiv): Eine Push-Benachrichtigung wird eine Minute nach deinem Weggehen gesendet, außer du bist zurückgekommen und hast sie gesehen.
- Wenn du sie 15 Minuten später noch nicht gesehen hast und die Sache dringend ist: Du erhältst dafür eine E-Mail, höchstens eine pro Stunde. Was du bereits erledigt hast, wird ausgelassen. An den meisten Tagen ist die morgendliche Zusammenfassung die einzige E-Mail.
- Wenn ein Teammitglied dir eine Aufgabe übergibt und deine Machine dich weder per Smartphone noch über Telegram erreichen kann: Du erhältst eine E-Mail mit dem Titel und einem Link, 15 Minuten später, falls du die Aufgabe dann noch nicht gesehen hast. Schalte **E-Mail** für **Ergebnisse und Fragen** aus, um das zu deaktivieren.
- Außerhalb deiner Arbeitszeiten: nichts. Die morgendliche Zusammenfassung enthält die Aufgaben.
- Eine neue Arbeitsaufgabe an einem freien Tag wartet bis zur Zusammenfassungszeit deines nächsten Arbeitstags. Bei der Aufgabe wird angezeigt, wann sie dich erreicht, zum Beispiel „Benachrichtigung Mo., 2. Nov. · 08:30“.

Fortschritte und Änderungen lösen nie Benachrichtigungen aus. Ein neues Ergebnis zu einer Aufgabe, die du noch nicht gesehen hast, wird aktualisiert, ohne eine neue Benachrichtigung zu senden. Bei mehreren kurz aufeinanderfolgenden Benachrichtigungen erhältst du nur eine. Das App-Symbol zeigt an, wie viele Aufgaben deine Aufmerksamkeit brauchen.

## Schaltflächen in Benachrichtigungen

Jede Benachrichtigung enthält Schaltflächen für den nächsten Schritt. In der Smartphone-App:

- Neue Aufgabe: **Ausführen**, **Zurückstellen**, **Erledigt**.
- Entwurf bereit: **Entwurf öffnen**, **Zurückstellen**, **Erledigt**.
- Ergebnis bereit: **Öffnen**, **Erledigt**, **Zurückstellen**.
- Frage, Problem oder Anmeldung: **Antworten**, **Öffnen** oder **Anmelden**, danach **Zurückstellen** und **Erledigt**.
- Erinnerung: **Erledigt**, **Zurückstellen**, **Öffnen**.
- Morgendliche Zusammenfassung: Tippe darauf, um sie zu öffnen.

Im Browser und in Telegram werden jeweils zwei davon angezeigt. Bei Fleet-Fragen gibt es weiterhin die Optionen **Antworten** und **Ablehnen**.

Über eine Benachrichtigung wird nichts gesendet, bezahlt oder eingereicht. Ein Entwurf wird immer zuerst geöffnet, damit du ihn vor dem Senden sehen kannst. **Entwurf öffnen** zeigt die Aufgabe samt vollständigem Entwurf in deiner Liste. **Ausführen** startet nur die Arbeit an einer neuen Aufgabe.

In der Smartphone-App musst du dein Gerät erst entsperren, bevor du **Zurückstellen** oder **Erledigt** auswählst. Im Browser wird das Dashboard geöffnet. Dort wird die Aktion ausgeführt und du kannst sie rückgängig machen. Beim Zurückstellen steht die Aufgabe in zwei Stunden wieder an oder bei einer Erinnerung am nächsten Morgen.

E-Mails enthalten Links zum Öffnen und bei Aufgaben, die noch warten, auch zum Zurückstellen. Die Links öffnen nur das Dashboard.

Wenn du auf eine Benachrichtigung oder in einer E-Mail oder Telegram-Nachricht auf **Öffnen** tippst, wird die Aufgabe in deiner Liste hervorgehoben, egal, wo sie sich gerade befindet: **Gerade erledigt**, **Erledigt**, **Kommt später zurück** oder in einer anderen Ansicht. Der Chat wird nie geöffnet. Wenn die Seite noch nicht aktuell ist, folgt sie der Aufgabe, sobald sie aktualisiert wurde.

## Die morgendliche Zusammenfassung

Sie wird an Arbeitstagen zur Uhrzeit für **Morgendliche Zusammenfassung** gesendet, sofern es etwas zu berichten gibt. Ist diese Zeit früher als **Zurückgestelltes kommt um**, wird sie bis 5 Minuten danach zurückgehalten, damit die Aufgaben enthalten sind, die an diesem Morgen wieder anstehen. Mit **Vorschau** kannst du sie ansehen, ohne sie zu senden. Standardmäßig erhältst du sie als Push-Benachrichtigung und per E-Mail. Sie ist so kurz, dass du sie schnell überfliegen kannst:

- eine Begrüßung mit dem Wichtigsten für heute, zum Beispiel „Guten Morgen Sam, 2 Antworten sind versandbereit“ oder bei einer Aufgabe „Guten Morgen Sam, wartet auf deine Freigabe: Bestellformular senden“;
- die Aufgaben, auf die sich die Begrüßung bezieht, jeweils mit einem Link zum Öffnen, sowie alles, was heute fällig ist; andernfalls höchstens drei Aufgaben;
- bis zu fünf Aufgaben, die du selbst hinzugefügt hast und bei denen du am Zug bist, unabhängig davon, auf wie viele sich die Begrüßung bezieht;
- wie viele weitere Aufgaben warten können und wie lange du in deinem Tempo dafür brauchst, zum Beispiel „12 weitere können warten, in etwa 5 Min. erledigt.“ Aufgaben, die auf deine Antwort warten, zählen nicht zu dieser Zeit. Eine zurückgestellte Aufgabe, die heute fällig ist, wird erst gezählt, wenn sie wieder ansteht.
- deine Besprechungen in einer Zeile.

**Öffnen** zeigt die Aufgabe hervorgehoben in deiner Liste, auch wenn sie erledigt oder zurückgestellt ist. Ein Versprechen öffnet die zugehörige Aufgabe oder, falls es noch keine gibt, die eigene Seite.

Die Push-Benachrichtigung enthält denselben Text ohne Links. Tippe darauf oder auf den Link am Ende der E-Mail, um die Zusammenfassung noch einmal unter **Aufgaben** zu lesen.

## Die abendliche Zusammenfassung

Sie wird an Arbeitstagen einmal zur eingestellten Uhrzeit unter **Arbeitszeiten** gesendet, standardmäßig 15 Minuten vor **Bis**, über die oben in der Zeile ausgewählten Kanäle. Wenn an einem Tag keine Aufgabe erledigt und keine Besprechung abgehalten wurde, wird keine Zusammenfassung gesendet. Sie beginnt mit einer Tagesbilanz, zum Beispiel „Guten Abend Sam, heute 4 Aufgaben erledigt“, gefolgt von einem Abschnitt **Arbeit** und einem Abschnitt **Privat**. Leere Abschnitte werden ausgelassen. Jeder Abschnitt enthält:

- **Heute erledigt**: bis zu drei Aufgaben, die du oder deine Machine erledigt haben, danach „+12 weitere“ und die Besprechungen des Tages, zum Beispiel „+3 Besprechungen: Preisgespräch und 2 weitere“;
- **Offen für morgen** (am Freitag für deinen nächsten Arbeitstag): die ersten Besprechungen und alles, was fällig ist.

Zum Schluss steht, wie viele Aufgaben noch deine Aufmerksamkeit brauchen. Tippe auf die Push-Benachrichtigung oder auf den Link am Ende der E-Mail, um die Zusammenfassung mit **Arbeit kopieren** und **Privat kopieren** noch einmal zu lesen. Schalte die Zeile aus, um die Zusammenfassung abzubestellen.

## Datenschutz

Push-Benachrichtigungen werden direkt von deiner Machine an dein Gerät gesendet und dafür verschlüsselt. E-Mails laufen über den Mailserver von The Machine und deinen E-Mail-Anbieter. Wenn [Sorgfältig](security-levels.md) Aufgabentexte in Benachrichtigungen ausblendet, enthalten E-Mails nur die Anzahl der Aufgaben. Schalte **E-Mail** für eine Art aus, damit sie nicht per E-Mail gesendet wird.

Schalte Push-Benachrichtigungen für ein Gerät unter **Dieses Gerät** ein oder lies [App installieren](phone-app.md). Die [mobile App](mobile-app.md) erhält eine einfache Textzeile über Apple oder Google und fragt dann deine Machine nach dem Titel und dem nächsten Schritt.
