---
title: Benachrichtigungen
area: settings
summary: Was dich wann und wo erreicht: Nur was nicht warten kann, löst einen Ton aus. Alles andere findest du in einer morgendlichen Zusammenfassung.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 4a782ad03270e7b0
---
Weniger Benachrichtigungen oder andere? Wähle unter **Einstellungen** > **Benachrichtigungen**, über welchen Kanal dich die einzelnen Arten erreichen:

- **Neue Aufgaben**: nur was nicht warten kann, zum Beispiel etwas, das heute fällig oder dringend ist.
- **Ergebnisse und Fragen**: eine Antwort, die zum Senden bereit ist, eine Anmeldung, die für eine Aufgabe nötig ist, oder eine Frage zu einer Fleet.
- **Erinnerungen**: zurückgestellte Aufgaben und Antworten, auf die du wartest und die wieder anstehen.
- **Morgendliche Zusammenfassung**: eine kurze Zusammenfassung deines Tages. Mehr dazu weiter unten.
- **Abendliche Zusammenfassung**: was du heute erledigt hast und was morgen noch offen ist. Mehr dazu weiter unten.

Für jede Art gibt es einen Schalter für **Push** (die App auf deinem Handy oder Computer), **Telegram**, sobald es eingerichtet ist, und **E-Mail** auf einer gehosteten Machine oder einer Machine auf The Machine Network. Alles ist eingeschaltet, außer die Zusammenfassungen auf Telegram.

Deine **Arbeitszeiten** findest du im selben Tab: Arbeitstage, Zeiten, zu denen Benachrichtigungen gesendet werden dürfen, wann Zurückgestelltes wieder ansteht, die Zeiten für Zusammenfassungen und deine Zeitzone. Mehr dazu unter [Arbeitszeiten](work-hours.md).

## Nur was nicht warten kann

Eine Push-Benachrichtigung, ein Signal auf Telegram oder eine E-Mail gibt es nur für:

- eine Aufgabe, die heute fällig oder als dringend markiert ist;
- eine Antwort, auf die jemand wartet und die als Entwurf fertig zum Senden ist;
- eine Aufgabe, für die du dich anmelden musst;
- eine Zurückstellung, die zum von dir gewählten Zeitpunkt wieder ansteht.

Alles andere erscheint unauffällig im Dashboard und still auf Telegram und wartet auf die morgendliche Zusammenfassung. An einem freien Tag gibt es nur bei Dringendem oder heute Fälligem ein Signal. Höchstens 8 Push-Benachrichtigungen am Tag. Wenn du das Dashboard 3 Tage lang nicht öffnest, erhältst du nur die morgendliche Zusammenfassung, bis du wieder da bist.

## Wann Benachrichtigungen kommen

Es wird geprüft, ob du das Dashboard tatsächlich verwendest, nicht nur, ob es geöffnet ist:

- Wenn du es verwendest (es im Vordergrund ist und du in den letzten 10 Minuten geklickt, getippt oder gescrollt hast), gibt es kein Signal. Telegram-Nachrichten kommen still an. Das bloße Öffnen oder Neuladen zählt nicht.
- Wenn du nicht da bist (das Dashboard im Hintergrund oder geschlossen ist oder du 10 Minuten lang nichts getan hast), kommt eine Push-Benachrichtigung eine Minute, nachdem du weggegangen bist, sofern du nicht zurückgekommen bist und sie gesehen hast.
- Ist eine Benachrichtigung 15 Minuten später noch ungesehen und kann nicht warten, wird eine E-Mail dazu gesendet, höchstens eine pro Stunde. Was du bereits erledigt hast, bleibt außen vor. An den meisten Tagen ist die morgendliche Zusammenfassung die einzige E-Mail.
- Wenn dir ein Teammitglied eine Aufgabe zuweist und deine Machine dich weder per Handy noch über Telegram erreichen kann, kommt nach 15 Minuten eine E-Mail mit dem Titel und einem Link, sofern du die Aufgabe noch nicht gesehen hast. Wenn du **E-Mail** für **Ergebnisse und Fragen** ausschaltest, wird auch diese E-Mail deaktiviert.
- Außerhalb deiner Arbeitszeiten kommt nichts. Die morgendliche Zusammenfassung enthält die Aufgabe.
- Eine neue Arbeitsaufgabe an einem freien Tag wartet bis zur Zusammenfassungszeit deines nächsten Arbeitstags. Bei der Aufgabe siehst du, wann sie dich erreicht, zum Beispiel: Benachrichtigung Mo., 2. Nov. · 08:30.

Fortschritte und Änderungen lösen nie Benachrichtigungen aus. Ein neues Ergebnis zu einer Aufgabe, die du noch nicht gesehen hast, aktualisiert sie ohne neue Benachrichtigung. Bei mehreren Benachrichtigungen auf einmal gibt es nur ein Signal. Das App-Symbol zeigt, wie viele Aufgaben deine Aufmerksamkeit brauchen.

## Schaltflächen in Benachrichtigungen

Jede Benachrichtigung hat Schaltflächen für den nächsten Schritt. In der Handy-App:

- Neue Aufgabe: Ausführen, Zurückstellen, Erledigen.
- Entwurf bereit: Entwurf öffnen, Zurückstellen, Erledigen.
- Ergebnis bereit: Öffnen, Erledigen, Zurückstellen.
- Frage, Problem oder Anmeldung: Antworten, Öffnen oder Anmelden, dann Zurückstellen und Erledigen.
- Erinnerung: Erledigen, Zurückstellen, Öffnen.
- Morgendliche Zusammenfassung: Tippe darauf, um sie zu öffnen.

Im Browser und auf Telegram werden jeweils zwei davon angezeigt. Bei Fragen zu einer Fleet bleiben „Antworten“ und „Ablehnen“ verfügbar.

Über eine Benachrichtigung wird nichts gesendet, bezahlt oder abgeschickt. Ein Entwurf wird immer zuerst geöffnet, damit du ihn siehst, bevor er gesendet wird. „Entwurf öffnen“ zeigt die Aufgabe mit dem vollständigen Entwurf in deiner Liste. „Ausführen“ startet nur die Arbeit an einer neuen Aufgabe.

In der Handy-App musst du dein Gerät erst entsperren, bevor du „Zurückstellen“ oder „Erledigen“ auswählst. Im Browser öffnet sich das Dashboard. Dort wird die Aktion ausgeführt und „Rückgängig“ angezeigt. „Zurückstellen“ lässt die Aufgabe nach zwei Stunden oder bei einer Erinnerung am nächsten Morgen wieder anstehen.

E-Mails enthalten Links zum Öffnen und bei Aufgaben, die warten, auch zum Zurückstellen. Sie öffnen nur das Dashboard.

Wenn du auf eine Benachrichtigung tippst oder in einer E-Mail oder auf Telegram „Öffnen“ auswählst, wird die Aufgabe in deiner Liste hervorgehoben, wo auch immer sie sich gerade befindet: **Gerade erledigt**, **Erledigt**, **Kommt später zurück** oder eine andere Ansicht. Der Chat wird nie geöffnet. Wenn die Seite noch nicht auf dem neuesten Stand war, zeigt sie die Aufgabe an, sobald sie aktualisiert ist.

## Die morgendliche Zusammenfassung

Sie kommt an Arbeitstagen zur eingestellten Zeit für **Morgendliche Zusammenfassung**, sofern es etwas zu berichten gibt. Liegt diese Zeit vor **Zurückgestelltes kommt um**, wartet die Zusammenfassung bis 5 Minuten danach, damit die Aufgaben enthalten sind, die an diesem Morgen wieder anstehen. Mit **Vorschau** kannst du sie anzeigen, ohne sie zu senden. Standardmäßig kommt sie als Push-Benachrichtigung und E-Mail. Sie ist kurz genug, um sie auf einen Blick zu lesen:

- eine Begrüßung mit dem Wichtigsten für heute, zum Beispiel „Guten Morgen, Sam, 2 Antworten sind fertig zum Senden“ oder bei einer Aufgabe „Guten Morgen, Sam, wartet auf dein Okay: Bestellformular senden“. Als bereit zählen nur Aufgaben mit einem Entwurf oder Ergebnis, das freigegeben werden muss. Eine Aufgabe, bei der zuerst deine Antwort nötig ist, zählt nicht dazu;
- die Aufgaben, auf die sich die Begrüßung bezieht, jeweils mit einem Link zum Öffnen, sowie alles, was heute fällig ist. Andernfalls werden höchstens drei Aufgaben aufgeführt;
- bis zu fünf Aufgaben, die du selbst hinzugefügt hast und bei denen du am Zug bist, unabhängig davon, auf wie viele Aufgaben sich die Begrüßung bezieht;
- wie viele weitere Aufgaben warten können und wie lange du in deinem Tempo dafür brauchst, zum Beispiel „12 weitere können warten, etwa 5 Min. zum Erledigen“. Aufgaben, bei denen deine Antwort fehlt, sind in dieser Zeit nicht enthalten. Eine Aufgabe, die heute fällig ist, aber bis später zurückgestellt wurde, oder an der The Machine noch arbeitet, wird erst gezählt, wenn du am Zug bist. Die Anzahl entspricht den Aufgaben, die in deiner Liste auf dich warten;
- deine Termine in einer Zeile.

„Öffnen“ zeigt die Aufgabe hervorgehoben in deiner Liste, auch wenn sie erledigt oder zurückgestellt ist. Ein Versprechen öffnet die zugehörige Aufgabe oder, wenn es noch keine gibt, die eigene Seite.

Die Push-Benachrichtigung enthält dieselben Informationen, aber keine Links. Tippe darauf oder auf den Link am Ende der E-Mail, um die Zusammenfassung unter **Aufgaben** erneut zu lesen.

## Die abendliche Zusammenfassung

Sie kommt an Arbeitstagen einmal zur dafür unter **Arbeitszeiten** festgelegten Zeit. Standardmäßig ist das 15 Minuten vor **Bis**. Sie kommt über die Kanäle, die du in der Zeile oben ausgewählt hast. Du erhältst sie nur an Tagen, an denen du aktiv warst: Du hast das Dashboard verwendet oder dort, auf Telegram, im Chat oder per Sprache eine Entscheidung zu einer Aufgabe getroffen. An einem Tag ohne erledigte Aufgabe und ohne stattgefundenen Termin gibt es keine Zusammenfassung.

Sie beginnt mit einer Zusammenfassung des Tages in Zahlen, zum Beispiel „Guten Abend, Sam, heute 4 Aufgaben erledigt“. Danach folgen die Bereiche **Arbeit** und **Privat**. Bereiche ohne Inhalt werden ausgelassen. In jedem Bereich stehen:

- **Heute erledigt**: bis zu drei Aufgaben, die du oder deine Machine erledigt habt, dann „+12 weitere“ und die Termine des Tages, zum Beispiel „+3 Termine: Preisgespräch und 2 weitere“;
- **Offen für morgen** (am Freitag für deinen nächsten Arbeitstag): die ersten Termine und alles, was fällig ist.

Am Ende steht, wie viele Aufgaben noch deine Aufmerksamkeit brauchen. Tippe auf die Push-Benachrichtigung oder auf den Link am Ende der E-Mail, um die Zusammenfassung mit **Arbeit kopieren** und **Privat kopieren** erneut zu lesen. Um sie abzuschalten, deaktiviere die zugehörige Zeile.

## Datenschutz

Push-Benachrichtigungen gehen direkt und verschlüsselt von deiner Machine an dein Gerät. E-Mails laufen über den Mailserver von The Machine und deinen E-Mail-Anbieter. Wenn [Vorsichtig](security-levels.md) Aufgabentext in Benachrichtigungen ausblendet, enthalten E-Mails nur Zahlen. Deaktiviere **E-Mail** für eine Benachrichtigungsart, damit dazu keine E-Mails kommen.

Aktiviere Push-Benachrichtigungen für ein Gerät unter **Dieses Gerät** oder lies [Handy-App installieren](phone-app.md). Die [Handy-App](mobile-app.md) sendet über Apple oder Google eine einfache Textzeile und fragt dann deine Machine nach dem Titel und dem nächsten Schritt.
