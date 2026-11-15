---
title: Notizen
area: graph
summary: Eine übersichtliche Seite pro Thema, zum Beispiel zu einer Reise oder deinem Zuhause, verknüpft mit den Personen und Projekten, die dazugehören.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: a32102a88a8b3856
---
Eine Notiz gibt dir einen Überblick über ein Thema: eine Reise, dein Zuhause oder die Abläufe rund um Rechnungen. Notizen stehen im Graph neben Personen, Organisationen und Projekten. Sie bleiben auf deiner Machine und werden nicht mit deinem Team geteilt.

## Eine Notiz beginnen

Oben in den Notizen findest du **Neue Notiz**. Gib einen Titel ein und wähle **Notiz beginnen**, um die Seite zu öffnen. Mit **Zeile hinzufügen** fügst du hinzu, was du festhalten möchtest. Jede Textzeile wird zu einer eigenen Zeile.

## Mit Personen, Projekten und anderen Notizen verknüpfen

Gib in einer Zeile @ und ein paar Buchstaben eines Namens ein. Wähle eine Person, Organisation, ein Projekt oder eine Notiz aus der Liste aus. Der Name wird als Link eingefügt. Auf der Seite des verknüpften Eintrags erscheint unter **Verlinkt von** deine Notiz.

## Notizen unter anderen Notizen

Eine Notiz kann unter einer anderen stehen, zum Beispiel Geräte unter Zuhause. Notizen werden als Baum angezeigt: Mit dem Pfeil neben einer Notiz öffnest du die darunterliegenden Notizen. Um eine Notiz zu verschieben, wähle **Bearbeiten** und lege unter **Unter** fest, wo sie stehen soll. Mit **Neue Notiz unter dieser** im Menü ⋯ erstellst du direkt dort eine Notiz.

## Notizen, die deine Machine führt

Deine Machine erstellt auch selbst Notizen aus deinen Nachrichten und hält sie auf dem neuesten Stand. In jeder Zeile steht, woher sie stammt, zum Beispiel, wer die E-Mail geschickt hat. Tippe darauf, um die Nachricht zu öffnen. Bei einer Zeile aus **Was ich gelernt habe** steht **Aus meinen Erkenntnissen**.

Deine Änderungen bleiben immer erhalten. Wenn du eine Notiz umbenennst, verschiebst, ihre Daten oder eine Zeile änderst, behält deine Machine diese Änderungen bei, wenn sie die Notiz aktualisiert. Löschst du eine Zeile oder eine Notiz, kommt sie nicht wieder. Spätere Notizen zum selben Thema landen dort, wo du die erste Notiz abgelegt hast.

Mit **Zurück zum Original** werden wieder die eigenen Worte deiner Machine angezeigt. Wenn du eine Zeile bearbeitest, die deine Machine aus ihren Erkenntnissen übernommen hat, ändert sie sich auch unter **Was ich gelernt habe**. So gibt es nur eine Version davon.

## Reisen

Wenn eine Flug-, Hotel-, Zug-, Bus-, Fähr- oder Mietwagenbuchung in deinem Postfach eingeht, fügt deine Machine sie unter **Reisen** zu einer Reise hinzu. Buchungen derselben Reise stehen zusammen: die Hinfahrt, das Hotel und die Rückfahrt. Die Reise enthält den Buchungscode, den Sitzplatz und das Ticket für jede Zeile, chronologisch sortiert, und zeigt die Reisedaten an. Im [Kalender](calendar.md) wird sie als ein Balken über diese Tage angezeigt. Wenn du darauf tippst, öffnet sich die Reise.

Deine Machine liest die Buchungsdetails aus den Bestätigungsmails von Fluggesellschaften, Hotels und Buchungsseiten. Eine E-Mail ohne diese Angaben erstellt keine Reise. Bei einer geänderten Buchung wird die entsprechende Zeile aktualisiert, bei einer stornierten Buchung wird sie entfernt. Wenn alle Buchungen einer Reise storniert werden, wird auch die Reise entfernt.

## Termine

Wenn Konzert-, Sportveranstaltungs-, Festival- oder Konferenztickets in deinem Postfach eingehen, fügt deine Machine den Termin unter **Termine** hinzu. Für jeden Termin gibt es eine eigene Notiz. Eine Zeile enthält den Veranstaltungsort, den Buchungscode, den Sitzplatz und die Anzahl der Tickets. Eine zweite Bestellung für denselben Termin wird derselben Notiz hinzugefügt. Wie bei einer Reise zeigt der Termin seine Daten an. Im [Kalender](calendar.md) wird er als Balken angezeigt, der die Notiz öffnet.

- In jeder Zeile steht, von wem die Tickets stammen, zum Beispiel **Von Example Tickets**. Tippe darauf, um die E-Mail zu öffnen.
- Wenn aus der Ticket-E-Mail eine Aufgabe erstellt wurde, zum Beispiel zum Bezahlen der Tickets, wird sie mit **Aufgabe öffnen** angezeigt.
- Ein Termin, der über dein geschäftliches Postfach gebucht wurde, ist geschäftlich. Andernfalls ist er privat.

Deine Machine liest die Ticketdetails aus den Bestätigungsmails der Ticketanbieter, ohne KI. Eine E-Mail ohne diese Angaben erstellt keinen Termin. Eine stornierte Buchung wird entfernt. Wenn alle Tickets für einen Termin storniert werden, wird auch der Termin entfernt.

## Zuhause

Unter **Zuhause** führt deine Machine, was sie über dein Zuhause weiß: **Rechnungen und Abos**, **Geräte**, **Reparaturen und Instandhaltung** und **Das Haus**. Ein Bereich wird angezeigt, sobald er mindestens zwei Zeilen enthält.

- Eine regelmäßig anfallende Rechnung, zum Beispiel für Strom oder Wasser, erhält eine Zeile mit der Häufigkeit und dem Datum der letzten Rechnung. Mit **Aufgabe öffnen** wird die Rechnung selbst geöffnet. Der Betrag und die Zahlungsdetails stehen dort.
- Ein Abo, das du behalten hast, erhält eine Zeile, die die Aufgabe **Abos** öffnet. Ein gekündigtes Abo wird nicht aufgeführt.
- Auch Erkenntnisse deiner Machine über dein Zuhause, zum Beispiel die Marke deiner Spülmaschine, erscheinen als Zeile. Wenn du sie bearbeitest, ändert sie sich auch unter **Was ich gelernt habe**.
- Wenn du in einem Bereich eine eigene Notiz führst, zum Beispiel zu deiner Spülmaschine unter **Geräte**, kommen die Informationen zu diesem Gerät stattdessen in deine Notiz. Deine Machine erstellt solche Notizen nicht selbst.

Es werden nur private Rechnungen und Abos verwendet. Notizen unter Zuhause sind immer privat. Deine Machine fragt ihre KI einmal zu jeder neuen Rechnung, jedem neuen Abo und jeder neuen Erkenntnis, um festzustellen, ob es um dein Zuhause geht. Bei einer Rechnung teilt sie mit, von wem sie stammt, aber niemals den Betrag.

## Gesundheit

Unter **Gesundheit** führt deine Machine, was sie über deine Gesundheit weiß: **Termine**, **Ärzte und Pflege**, **Medikamente**, **Allergien und Erkrankungen** und **Rechnungen und Versicherung**. Ein Bereich wird angezeigt, sobald er mindestens zwei Zeilen enthält.

- Ein Termin in deinem Kalender, zu dem nur du gehst, zum Beispiel beim Zahnarzt, erhält eine Zeile mit dem nächsten oder letzten Datum. Mit **Aus deinem Kalender** wird der Termin geöffnet.
- Eine Rechnung von einem Arzt, Zahnarzt oder einer Apotheke erhält eine Zeile, die die dazugehörige Aufgabe öffnet. Der Betrag steht dort.
- Auch Erkenntnisse deiner Machine über deine Gesundheit, zum Beispiel eine Allergie, erscheinen als Zeile. Wenn du sie bearbeitest, ändert sie sich auch unter **Was ich gelernt habe**.
- In deine eigene Notiz in einem Bereich, zum Beispiel zu deiner Physiotherapeutin unter **Termine**, kommen die Informationen zu dieser Person.

Notizen unter Gesundheit sind immer privat, auch wenn eine Rechnung an deine geschäftliche Adresse geschickt wurde. Deine Machine fragt ihre KI einmal zu jedem neuen Termin, jeder neuen Rechnung und jeder neuen Erkenntnis, um festzustellen, ob es um deine Gesundheit geht. Bei einem Termin teilt sie den Namen mit, aber weder die Notizen dazu noch, wer sonst noch eingeladen ist.

## Kinder

Unter **Kinder** führt deine Machine, was sie über deine Kinder weiß: **Schule**, **Aktivitäten**, **Ärzte und Pflege** und **Rechnungen und Gebühren**. Ein Bereich wird angezeigt, sobald er mindestens zwei Zeilen enthält.

- Erkenntnisse deiner Machine über dein Kind, zum Beispiel den Namen der Klassenlehrerin oder den Schwimmtag, erscheinen als Zeile, die mit der Seite deines Kindes verknüpft ist. Als dein Kind gilt eine Person, wenn unter **Für dich** zum Beispiel Tochter oder Sohn steht.
- Ein Termin in deinem Kalender, zu dem nur du gehst, zum Beispiel ein Elternabend, erhält eine Zeile mit dem nächsten oder letzten Datum. Mit **Aus deinem Kalender** wird der Termin geöffnet.
- Eine Rechnung für die Schule, einen Verein oder die Kinderbetreuung erhält eine Zeile, die die dazugehörige Aufgabe öffnet. Der Betrag steht dort.
- In deine eigene Notiz zu einem Kind in einem Bereich, zum Beispiel zu Isla unter **Schule**, kommen die Informationen zu diesem Kind.

Notizen unter Kinder sind immer privat, auch wenn die Schule an deine geschäftliche Adresse schreibt. Deine Machine fragt ihre KI einmal zu jeder neuen Erkenntnis, um festzustellen, ob sie deine Kinder betrifft.

## Zusammenführen, löschen und rückgängig machen

Mit **Zusammenführen mit …** im Menü ⋯ verschiebst du die Zeilen einer Notiz und die darunterliegenden Notizen in eine andere Notiz. Von da an fügt deine Machine neue Inhalte zu dieser Notiz hinzu. Mit **Löschen** entfernst du eine Notiz. Bei beidem wird kurz **Rückgängig** angezeigt. Das gilt auch, wenn du eine Zeile entfernst.

## Nicht dasselbe wie Besprechungsnotizen

Besprechungsnotizen und Notizen zu Personen oder Organisationen bleiben dort, wo sie waren. Die Notizen hier sind eigenständige Seiten.
