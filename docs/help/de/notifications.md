---
title: Benachrichtigungen
area: settings
summary: Was dich wann und wo erreicht: Nur, was nicht warten kann, macht sich bemerkbar. Alles andere findest du in einer morgendlichen Zusammenfassung.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: ee3ba81a8441704f
---
Weniger Benachrichtigungen oder andere? Wähle unter **Einstellungen** und **Benachrichtigungen** aus, wo du die einzelnen Arten erhältst:

- **Neue Aufgaben**: nur, was nicht warten kann, zum Beispiel etwas, das heute fällig oder dringend ist.
- **Ergebnisse und Fragen**: eine versandbereite Antwort, eine Aufgabe, für die du dich anmelden musst, oder eine Frage von Fleet.
- **Erinnerungen**: zurückgestellte Aufgaben und Antworten, auf die du wartest und die wieder anstehen.
- **Morgendliche Zusammenfassung**: eine kurze Zusammenfassung deines Tages. Mehr dazu weiter unten.
- **Abendliche Zusammenfassung**: was du heute erledigt hast und was morgen noch offen ist. Mehr dazu weiter unten.

Für jede Art gibt es einen Schalter für **Push** (die App auf deinem Smartphone oder Computer), **Telegram**, sobald du es eingerichtet hast, und **E-Mail** auf einer gehosteten Machine oder einer Machine im The Machine Network. Alles ist eingeschaltet, außer den Zusammenfassungen auf Telegram.

Deine **Arbeitszeiten** findest du im selben Tab: Arbeitstage, wann Benachrichtigungen gesendet werden dürfen, wann zurückgestellte Aufgaben wieder anstehen, die Zeiten der Zusammenfassungen und deine Zeitzone. Mehr dazu unter [Arbeitszeiten](work-hours.md).

## Nur, was nicht warten kann

Eine Push-Benachrichtigung, eine Telegram-Nachricht oder eine E-Mail erhältst du nur bei:

- einer Aufgabe, die heute fällig oder als dringend markiert ist;
- einer Antwort, auf die jemand wartet und die als Entwurf bereit zum Senden ist;
- einer Aufgabe, für die du dich anmelden musst;
- einer zurückgestellten Aufgabe, die zum von dir gewählten Zeitpunkt wieder ansteht.

Alles andere erscheint unauffällig auf dem Dashboard und ohne Ton in Telegram. Dort wartet es auf die morgendliche Zusammenfassung. An einem freien Tag machen sich nur dringende oder heute fällige Aufgaben bemerkbar. Du erhältst höchstens 8 Push-Benachrichtigungen pro Tag. Wenn du das Dashboard 3 Tage lang nicht öffnest, erhältst du nur noch die morgendliche Zusammenfassung, bis du wieder da bist.

## Wann Benachrichtigungen gesendet werden

Es wird geprüft, ob du das Dashboard tatsächlich verwendest, nicht nur, ob es geöffnet ist:

- Wenn du es verwendest (es ist im Vordergrund und du hast in den letzten 10 Minuten geklickt, getippt oder gescrollt), erhältst du keine Benachrichtigung. Telegram-Nachrichten kommen ohne Ton an.
- Wenn du nicht da bist (das Dashboard ist im Hintergrund, geschlossen oder seit 10 Minuten inaktiv), wird eine Minute nach deinem Weggehen eine Push-Benachrichtigung gesendet, sofern du nicht zurückgekommen bist und sie gesehen hast.
- Wenn du die Benachrichtigung auch 15 Minuten später noch nicht gesehen hast und sie nicht warten kann, erhältst du dafür eine E-Mail, höchstens eine pro Stunde. Was du bereits erledigt hast, wird ausgelassen. An den meisten Tagen ist die morgendliche Zusammenfassung die einzige E-Mail.
- Wenn dir ein Teammitglied eine Aufgabe gibt und deine Machine weder ein Smartphone noch Telegram hat, über das sie dich erreichen kann, erhältst du eine E-Mail mit dem Titel und einem Link. Sie kommt nach 15 Minuten, wenn du die Aufgabe bis dahin noch nicht gesehen hast. Wenn du **E-Mail** für **Ergebnisse und Fragen** ausschaltest, wird diese E-Mail nicht gesendet.
- Außerhalb deiner Arbeitszeiten erhältst du nichts. Die morgendliche Zusammenfassung enthält die Informationen.
- Eine neue Arbeitsaufgabe an einem freien Tag wartet bis zur Zusammenfassungszeit deines nächsten Arbeitstags. Die Aufgabe zeigt an, wann sie dich erreicht, zum Beispiel „Benachrichtigung Mo., 2. Nov. · 08:30“.

Fortschritte und Änderungen lösen keine Benachrichtigungen aus. Wenn ein neues Ergebnis zu einer Aufgabe hinzukommt, die du noch nicht gesehen hast, wird die Aufgabe aktualisiert, ohne dass eine neue Benachrichtigung gesendet wird. Mehrere Benachrichtigungen kurz hintereinander lösen nur eine aus. Das App-Symbol zeigt an, wie viele Aufgaben deine Aufmerksamkeit brauchen.

## Schaltflächen in Benachrichtigungen

Jede Benachrichtigung bietet Schaltflächen für den nächsten Schritt. In der Smartphone-App:

- Neue Aufgabe: **Ausführen**, **Zurückstellen**, **Erledigt**.
- Entwurf bereit: **Entwurf öffnen**, **Zurückstellen**, **Erledigt**.
- Ergebnis bereit: **Öffnen**, **Erledigt**, **Zurückstellen**.
- Frage, Problem oder Anmeldung: **Antworten**, **Öffnen** oder **Anmelden**, danach **Zurückstellen** und **Erledigt**.
- Erinnerung: **Erledigt**, **Zurückstellen**, **Öffnen**.
- Morgendliche Zusammenfassung: Zum Öffnen antippen.

Im Browser und auf Telegram werden zwei davon angezeigt. Bei Fragen von Fleet bleiben **Einmal antworten** und **Ablehnen** verfügbar.

Über eine Benachrichtigung wird nichts gesendet, bezahlt oder eingereicht. Ein Entwurf wird immer zuerst geöffnet, damit du ihn vor dem Senden sehen kannst. **Entwurf öffnen** zeigt die Aufgabe in deiner Liste mit dem vollständigen Entwurf. **Ausführen** startet nur die Arbeit an einer neuen Aufgabe.

In der Smartphone-App musst du zum **Zurückstellen** und **Erledigen** zuerst dein Gerät entsperren. Im Browser wird das Dashboard geöffnet. Dort wird die Aktion ausgeführt und **Rückgängig** angezeigt. Durch **Zurückstellen** steht die Aufgabe in zwei Stunden wieder an, bei einer Erinnerung am nächsten Morgen.

E-Mails enthalten Links zum Öffnen und für wartende Aufgaben auch zum Zurückstellen. Sie öffnen nur das Dashboard.

Wenn du eine Benachrichtigung antippst oder in einer E-Mail oder auf Telegram auf **Öffnen** tippst, wird die Aufgabe in deiner Liste hervorgehoben, egal wo sie sich gerade befindet: **Gerade erledigt**, **Erledigt**, **Kommt später zurück** oder eine andere Ansicht. Der Chat wird dabei nie geöffnet. Wenn die Seite noch nicht aktualisiert war, wird der Aufgabe gefolgt, sobald sie aktualisiert ist.

## Die morgendliche Zusammenfassung

Sie wird an Arbeitstagen zur Zeit deiner **Morgendlichen Zusammenfassung** gesendet, sofern es etwas zu berichten gibt. Liegt dieser Zeitpunkt vor **Zurückgestelltes kommt um**, wartet sie bis 5 Minuten danach. So sind die Aufgaben enthalten, die an diesem Morgen wieder anstehen. Mit **Vorschau** kannst du sie ansehen, ohne sie zu senden. Standardmäßig kommt sie als Push-Benachrichtigung und E-Mail. Sie ist kurz genug, um sie auf einen Blick zu lesen:

- eine Begrüßung mit dem Wichtigsten für heute, zum Beispiel „Guten Morgen Sam, 2 Antworten sind versandbereit“ oder, bei einer Aufgabe, „Guten Morgen Sam, bereit für deine Freigabe: Bestellformular senden“;
- die Aufgaben, die in der Begrüßung gezählt werden, jeweils mit einem Link zum Öffnen, sowie alles, was heute fällig ist. Andernfalls werden höchstens drei Aufgaben angezeigt;
- bis zu fünf Aufgaben, die du selbst hinzugefügt hast und die noch deine Aufmerksamkeit brauchen, unabhängig davon, was in der Begrüßung gezählt wird;
- wie viele weitere Aufgaben warten können und wie lange sie bei deinem Tempo dauern, zum Beispiel „12 weitere können warten, dauert etwa 5 Min. zum Erledigen“. Aufgaben, die auf deine Antwort warten, werden bei dieser Zeit nicht berücksichtigt. Eine zurückgestellte Aufgabe, die heute fällig ist, wird erst gezählt, wenn sie wieder ansteht;
- deine Termine in einer Zeile.

**Öffnen** zeigt die Aufgabe hervorgehoben in deiner Liste, auch wenn sie erledigt oder zurückgestellt ist. Ein Versprechen öffnet die zugehörige Aufgabe oder, wenn es noch keine gibt, die eigene Seite.

Die Push-Benachrichtigung enthält denselben Text ohne Links. Tippe darauf oder auf den Link am Ende der E-Mail, um die Zusammenfassung unter **Aufgaben** erneut zu lesen.

## Die abendliche Zusammenfassung

Sie wird an Arbeitstagen einmal zu der unter **Arbeitszeiten** festgelegten Zeit gesendet, standardmäßig 15 Minuten vor **Bis**, und über die oben in der Zeile ausgewählten Kanäle. Wenn du an einem Tag keine Aufgabe erledigt und keinen Termin wahrgenommen hast, erhältst du keine Zusammenfassung. Sie beginnt mit einer Zählung des Tages, zum Beispiel „Guten Abend Sam, heute 4 Aufgaben erledigt“, gefolgt von einem Abschnitt **Arbeit** und einem Abschnitt **Privat**. Abschnitte ohne Inhalt werden ausgelassen. Jeder Abschnitt enthält:

- **Heute erledigt**: bis zu drei Aufgaben, die du oder deine Machine erledigt habt, danach „+12 weitere“ und die Termine des Tages, zum Beispiel „+3 Termine: Preisgespräch und 2 weitere“;
- **Offen für morgen** (am Freitag für deinen nächsten Arbeitstag): die ersten Termine und alles, was fällig ist.

Am Ende steht, wie viele Aufgaben noch deine Aufmerksamkeit brauchen. Tippe auf die Push-Benachrichtigung oder auf den Link am Ende der E-Mail, um die Zusammenfassung mit **Arbeit kopieren** und **Privat kopieren** erneut zu lesen. Zum Beenden schaltest du die zugehörige Zeile aus.

## Datenschutz

Push wird von deiner Machine direkt und verschlüsselt an dein Gerät gesendet. E-Mails laufen über den Mailserver von The Machine und deinen E-Mail-Anbieter. Wenn [Vorsichtig](security-levels.md) Aufgabentexte in Benachrichtigungen ausblendet, enthalten E-Mails nur Zahlen. Schalte **E-Mail** für eine Art aus, damit sie nicht per E-Mail gesendet wird.

Aktiviere Push für ein Gerät unter **Dieses Gerät** oder lies [App installieren](phone-app.md). Die [Mobile App](mobile-app.md) erhält über Apple oder Google eine einfache Textzeile und fragt dann deine Machine nach dem Titel und dem nächsten Schritt.
