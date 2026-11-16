---
title: Benachrichtigungen
area: settings
summary: Was dich wann und wo erreicht: Nur was nicht warten kann, löst einen Ton aus. Alles andere findest du in einer morgendlichen Zusammenfassung.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 2146426abe3eaa50
---
Weniger Benachrichtigungen oder andere? Wähle unter **Einstellungen** > **Benachrichtigungen** aus, wo dich die einzelnen Arten erreichen:

- **Neue Aufgaben**: nur was nicht warten kann, zum Beispiel etwas, das heute fällig oder dringend ist.
- **Ergebnisse und Fragen**: eine Antwort, die zum Senden bereit ist, eine Anmeldung, die eine Aufgabe erfordert, oder eine Frage von Fleet.
- **Erinnerungen**: zurückgestellte Aufgaben und Antworten, auf die du wartest und die wieder anstehen.
- **Morgendliche Zusammenfassung**: eine kurze Zusammenfassung deines Tages. Mehr dazu weiter unten.
- **Abendliche Zusammenfassung**: was du heute erledigt hast und was für morgen offen ist. Mehr dazu weiter unten.

Für jede Art kannst du **Push** (die App auf deinem Smartphone oder Computer), **Telegram**, sobald es eingerichtet ist, und **E-Mail** auf einer gehosteten Machine oder einer Machine im The Machine Network ein- und ausschalten. Alles ist eingeschaltet, außer die Zusammenfassungen auf Telegram.

Deine **Arbeitszeiten** findest du im selben Tab: Arbeitstage, wann Benachrichtigungen gesendet werden dürfen, wann Zurückgestelltes wieder ansteht, die Zeiten der Zusammenfassungen und deine Zeitzone. Weitere Infos findest du unter [Arbeitszeiten](work-hours.md).

## Nur was nicht warten kann

Eine Push-Benachrichtigung, ein Signal von Telegram oder eine E-Mail kommt nur bei:

- einer Aufgabe, die heute fällig oder als dringend markiert ist;
- einer Antwort, auf die jemand wartet, die als Entwurf vorliegt und zum Senden bereit ist;
- einer Aufgabe, für die du dich anmelden musst;
- etwas Zurückgestelltem, das zum von dir gewählten Zeitpunkt wieder ansteht.

Alles andere erscheint unauffällig auf dem Dashboard und ohne Ton in Telegram. Dort wartet es auf die morgendliche Zusammenfassung. An einem freien Tag gibt es nur bei Dringendem oder heute Fälligem ein Signal. Es gibt höchstens 8 Push-Benachrichtigungen pro Tag. Wenn du das Dashboard 3 Tage lang nicht öffnest, bekommst du nur die morgendliche Zusammenfassung, bis du zurück bist.

## Wann Benachrichtigungen gesendet werden

The Machine prüft, ob du das Dashboard tatsächlich nutzt, nicht nur, ob es geöffnet ist:

- Wenn du es gerade nutzt, also davor sitzt und in den letzten 10 Minuten geklickt, getippt oder gescrollt hast, gibt es kein Signal. Telegram-Nachrichten kommen ohne Ton an. Nur das Öffnen oder Neuladen zählt nicht.
- Wenn du nicht da bist, also das Dashboard im Hintergrund oder geschlossen ist oder du 10 Minuten lang nichts damit gemacht hast, kommt eine Push-Benachrichtigung eine Minute, nachdem du es verlassen hast, sofern du nicht zurückgekommen bist und sie gesehen hast.
- Wenn du sie 15 Minuten später noch nicht gesehen hast und sie nicht warten kann, bekommst du dafür eine E-Mail, höchstens eine pro Stunde. Was du bereits erledigt hast, wird ausgelassen. An den meisten Tagen ist die morgendliche Zusammenfassung die einzige E-Mail.
- Wenn dir jemand aus dem Team eine Aufgabe gibt und deine Machine dich weder per Smartphone noch über Telegram erreichen kann, bekommst du nach 15 Minuten eine E-Mail mit dem Titel und einem Link, falls du die Aufgabe noch nicht gesehen hast. Wenn du **E-Mail** für **Ergebnisse und Fragen** ausschaltest, wird diese E-Mail nicht gesendet.
- Außerhalb deiner Arbeitszeiten kommt nichts. Die morgendliche Zusammenfassung enthält es.
- Eine neue Arbeitsaufgabe an einem freien Tag wartet bis zur Zusammenfassungszeit deines nächsten Arbeitstags. Bei der Aufgabe wird angezeigt, wann sie dich erreicht, zum Beispiel: Benachrichtigung Mo., 2. Nov. · 08:30.

Fortschritte und Änderungen lösen keine Benachrichtigungen aus. Ein neueres Ergebnis zu einer Aufgabe, die du noch nicht gesehen hast, wird aktualisiert, ohne dass eine neue Benachrichtigung gesendet wird. Bei mehreren Benachrichtigungen kurz hintereinander gibt es nur ein Signal. Das App-Symbol zeigt, wie viele Aufgaben deine Aufmerksamkeit brauchen.

## Schaltflächen in Benachrichtigungen

Jede Benachrichtigung hat Schaltflächen für den nächsten Schritt. In der Smartphone-App:

- Neue Aufgabe: **Ausführen**, **Zurückstellen**, **Als erledigt markieren**.
- Entwurf bereit: **Entwurf öffnen**, **Zurückstellen**, **Als erledigt markieren**.
- Ergebnis bereit: **Öffnen**, **Als erledigt markieren**, **Zurückstellen**.
- Frage, Problem oder Anmeldung: **Antworten**, **Öffnen** oder **Anmelden**, danach **Zurückstellen** und **Als erledigt markieren**.
- Erinnerung: **Als erledigt markieren**, **Zurückstellen**, **Öffnen**.
- Morgendliche Zusammenfassung: Zum Öffnen antippen.

Im Browser und in Telegram werden zwei davon angezeigt. Bei Fragen von Fleet bleiben **Antworten** und **Ablehnen** verfügbar.

Über eine Benachrichtigung wird nichts gesendet, bezahlt oder abgeschickt. Ein Entwurf wird immer erst geöffnet, damit du ihn vor dem Senden sehen kannst. **Entwurf öffnen** zeigt die Aufgabe mit dem vollständigen Entwurf in deiner Liste. **Ausführen** startet nur die Arbeit an einer neuen Aufgabe.

In der Smartphone-App musst du dein Gerät erst entsperren, bevor du **Zurückstellen** oder **Als erledigt markieren** auswählst. Im Browser öffnen diese Schaltflächen das Dashboard. Dort wird die Aktion ausgeführt und **Rückgängig** angezeigt. Wenn du etwas zurückstellst, steht die Aufgabe in zwei Stunden wieder an oder bei einer Erinnerung morgen früh.

E-Mails enthalten Links zum Öffnen und für Aufgaben, die noch ausstehen, auch zum Zurückstellen. Sie öffnen nur das Dashboard.

Wenn du eine Benachrichtigung antippst oder in einer E-Mail oder Telegram-Nachricht **Öffnen** auswählst, wird die Aufgabe in deiner Liste hervorgehoben, egal, wo sie gerade ist: **Gerade erledigt**, **Erledigt**, **Kommt später zurück** oder in einer anderen Ansicht. Der Chat wird dabei nie geöffnet. Wenn die Seite noch nicht aktuell ist, folgt sie der Aufgabe, sobald sie aktualisiert wurde.

## Die morgendliche Zusammenfassung

Sie kommt an Arbeitstagen zur eingestellten Zeit für **Morgendliche Zusammenfassung**, sofern es etwas zu berichten gibt. Liegt diese Zeit vor **Zurückgestelltes kommt um**, wartet die Zusammenfassung bis 5 Minuten danach, damit die Aufgaben, die an diesem Morgen wieder anstehen, darin enthalten sind. Mit **Vorschau** kannst du sie ansehen, ohne sie zu senden. Standardmäßig wird sie als Push-Benachrichtigung und per E-Mail gesendet. Sie ist kurz genug, um sie auf einen Blick zu lesen:

- eine Begrüßung mit dem Wichtigsten für heute, zum Beispiel „Guten Morgen, Sam, 2 Antworten sind bereit zum Senden“ oder bei einer Aufgabe „Guten Morgen, Sam, wartet auf dein OK: Bestellformular senden“;
- die Aufgaben, auf die sich die Begrüßung bezieht, jeweils mit einem Link zum Öffnen, sowie alles, was heute fällig ist. Wenn nichts davon zutrifft, werden höchstens drei Aufgaben angezeigt;
- bis zu fünf Aufgaben, die du selbst hinzugefügt hast und bei denen du am Zug bist, unabhängig davon, auf wie viele Aufgaben sich die Begrüßung bezieht;
- wie viele weitere Aufgaben warten können und wie lange du in deinem Tempo dafür brauchst, zum Beispiel „12 weitere können warten, in etwa 5 Min. erledigt“. Aufgaben, bei denen deine Antwort aussteht, zählen nicht zu dieser Zeit. Eine Aufgabe, die heute fällig ist, aber bis später zurückgestellt wurde, oder an der The Machine noch arbeitet, wird erst gezählt, wenn du am Zug bist. Die Anzahl entspricht den Aufgaben, die in deiner Liste auf dich warten.
- deine Besprechungen in einer Zeile.

**Öffnen** zeigt die Aufgabe hervorgehoben in deiner Liste, auch wenn sie erledigt oder zurückgestellt ist. Ein Versprechen öffnet die zugehörige Aufgabe oder, falls es noch keine gibt, die eigene Seite.

Die Push-Benachrichtigung enthält dasselbe, aber ohne Links. Tippe sie an oder wähle den Link am Ende der E-Mail aus, um die Zusammenfassung unter **Aufgaben** erneut zu lesen.

## Die abendliche Zusammenfassung

Sie kommt an Arbeitstagen einmal zur dafür eingestellten Zeit unter **Arbeitszeiten**, standardmäßig 15 Minuten vor **Bis**, und über die oben in der Zeile ausgewählten Kanäle. Wenn an einem Tag keine Aufgabe erledigt und keine Besprechung abgehalten wurde, gibt es keine Zusammenfassung. Sie beginnt mit einer Tagesbilanz, zum Beispiel „Guten Abend, Sam, heute 4 Aufgaben erledigt“, gefolgt von einem Abschnitt **Arbeit** und einem Abschnitt **Privat**. Abschnitte ohne Inhalt werden ausgelassen. Jeder Abschnitt enthält:

- **Heute erledigt**: bis zu drei Aufgaben, die du oder deine Machine erledigt habt, danach „+12 weitere“ sowie die Besprechungen des Tages, zum Beispiel „+3 Besprechungen: Preisgespräch und 2 weitere“;
- **Offen für morgen** (am Freitag für deinen nächsten Arbeitstag): die ersten Besprechungen und alles, was fällig ist.

Am Ende steht, wie viele Aufgaben noch deine Aufmerksamkeit brauchen. Tippe die Push-Benachrichtigung an oder wähle den Link am Ende der E-Mail aus, um die Zusammenfassung erneut zu lesen und **Arbeit kopieren** sowie **Privat kopieren** zu sehen. Um sie nicht mehr zu erhalten, schalte die entsprechende Zeile aus.

## Datenschutz

Push-Benachrichtigungen werden direkt und verschlüsselt von deiner Machine an dein Gerät gesendet. E-Mails laufen über den Mailserver von The Machine und deinen E-Mail-Anbieter. Wenn [Vorsichtig](security-levels.md) Aufgabentexte in Benachrichtigungen ausblendet, enthalten E-Mails nur noch die Anzahl. Schalte **E-Mail** für eine Benachrichtigungsart aus, damit sie nicht per E-Mail gesendet wird.

Aktiviere Push-Benachrichtigungen für ein Gerät unter **Dieses Gerät** oder lies [App installieren](phone-app.md). Die [Smartphone-App](mobile-app.md) erhält über Apple oder Google eine einfache Zeile und fragt danach deine Machine nach dem Titel und dem nächsten Schritt.
