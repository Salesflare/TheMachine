---
title: Notizen
area: graph
summary: Eine übersichtliche Seite pro Thema, etwa für eine Reise oder dein Zuhause, verknüpft mit den darin erwähnten Personen und Projekten.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: 8e27b2c69f77196d
---
Eine Notiz bietet einen Überblick über ein Thema: eine Reise, dein Zuhause oder die Abwicklung von Rechnungen. Notizen stehen im Graph neben Personen, Organisationen und Projekten. Sie bleiben auf deiner Machine und werden nicht mit deinem Team geteilt.

## Eine Notiz beginnen

Oben in den Notizen findest du **Neue Notiz**. Gib der Notiz einen Titel und wähle **Notiz beginnen**. Dann öffnet sich ihre Seite. Mit **Zeile hinzufügen** fügst du etwas hinzu, das du festhalten möchtest. Jede Textzeile wird zu einer eigenen Zeile.

## Mit Personen, Projekten und anderen Notizen verknüpfen

Gib in einer Zeile @ und die ersten Buchstaben eines Namens ein. Wähle eine Person, Organisation, ein Projekt oder eine Notiz aus der Liste aus. Der Name wird als Link eingefügt. Auf der Seite des verknüpften Eintrags erscheint unter **Verlinkt von** deine Notiz.

## Notizen unter anderen Notizen

Eine Notiz kann unter einer anderen stehen, zum Beispiel Geräte unter Zuhause. In den Notizen werden sie als Baum angezeigt: Mit dem Pfeil neben einer Notiz öffnest du die darunterliegenden. Um eine Notiz zu verschieben, wähle **Bearbeiten** und dann unter **Unter** den gewünschten Ort aus. Über **Neue Notiz unter dieser** im Menü ⋯ kannst du direkt dort eine Notiz erstellen.

Oben auf einer Notizseite siehst du, wo sie sich befindet, zum Beispiel **Notizen › Kinder**. Tippe auf einen beliebigen Teil, um dorthin zu gelangen. Auf dem Smartphone werden die dazwischenliegenden Notizen in ⋯ zusammengeklappt.

## Notizen, die deine Machine erstellt

Deine Machine erstellt auch selbst Notizen aus deinen Nachrichten und hält sie auf dem neuesten Stand. In jeder ihrer Zeilen steht, woher die Information stammt, zum Beispiel, wer die E-Mail geschickt hat. Tippe darauf, um die Nachricht zu öffnen. Bei einer Zeile aus **Was ich gelernt habe** steht **Aus meinen Erkenntnissen**. Ein Termin oder eine Verabredung in deinem Kalender erscheint nie als eigene Zeile, sondern bleibt im [Kalender](calendar.md).

**Zuhause**, **Gesundheit** und **Kinder** werden erst angezeigt, wenn deine Machine dort mindestens zwei konkrete Einträge hat, etwa eine Rechnung oder eine neue Erkenntnis. Bis dahin erscheinen sie gar nicht in der Liste. Wenn sie später wieder leer sind, verschwinden sie ebenfalls.

Deine Änderungen bleiben immer erhalten. Benennst du eine Notiz um, verschiebst sie oder änderst ihre Daten oder eine Zeile, behält deine Machine diese Änderungen bei, wenn sie die Notiz aktualisiert. Löschst du eine Zeile oder eine Notiz, kommt sie nicht wieder. Spätere Notizen zum selben Thema werden dort abgelegt, wo du die erste Notiz eingeordnet hast.

Mit **Zurück zum Original** werden wieder die ursprünglichen Worte deiner Machine angezeigt. Wenn du eine Zeile bearbeitest, die aus den Erkenntnissen deiner Machine stammt, ändert sie sich auch unter **Was ich gelernt habe**. So gibt es nur eine Version davon.

## Reisen

Wenn eine Flug-, Hotel-, Zug-, Bus-, Fähr- oder Mietwagenbuchung in deinem Postfach eingeht, fügt deine Machine sie unter **Reisen** zu einer Reise hinzu. Buchungen für dieselbe Reise kommen auf eine gemeinsame Seite: die Hinfahrt, das Hotel und die Rückfahrt. Für jede Zeile enthält die Reise den Buchungscode, den Sitzplatz und das Ticket, sortiert nach Uhrzeit. Außerdem werden die Reisedaten angezeigt. Im [Kalender](calendar.md) erscheint die Reise als Balken über diese Tage. Tippe darauf, um die Reise zu öffnen.

Deine Machine liest die Buchungsdetails aus den Bestätigungsmails von Fluggesellschaften, Hotels und Buchungsseiten. Eine Mail ohne diese Angaben löst keine Reise aus. Buchungsmails aus der Vergangenheit, die in das Jahr [Verlauf](history.md) fallen, das deine Machine speichert, werden im Hintergrund gelesen, sobald dieser Verlauf importiert ist. Zuerst werden deine privaten Postfächer berücksichtigt.

Wird eine Buchung geändert, wird ihre Zeile aktualisiert. Eine stornierte Buchung wird entfernt. Wenn alle Buchungen einer Reise storniert werden, wird auch die Reise entfernt.

## Termine

Wenn Tickets für ein Konzert, ein Spiel, ein Festival oder eine Konferenz in deinem Postfach eingehen, erstellt deine Machine unter **Termine** einen Eintrag für die Veranstaltung. In einer Zeile stehen der Veranstaltungsort, der Buchungscode, der Sitzplatz und die Anzahl der Tickets. Eine weitere Bestellung für dieselbe Veranstaltung kommt auf dieselbe Seite. Wie bei einer Reise werden die Termine angezeigt. Im [Kalender](calendar.md) erscheint die Veranstaltung als Balken, über den du die Seite öffnen kannst.

- In jeder Zeile steht, von wem die Tickets stammen, zum Beispiel **Von Example Tickets**. Tippe darauf, um die Mail zu öffnen.
- Wenn aus der Ticketmail eine Aufgabe entstanden ist, zum Beispiel die Tickets zu bezahlen, findest du sie über **Aufgabe öffnen**.
- Eine Veranstaltung, die über dein Arbeits-Postfach gebucht wurde, ist Arbeit. Alle anderen sind privat.

Deine Machine liest die Ticketdetails aus den Bestätigungsmails der Ticketanbieter, ohne KI. Eine Mail ohne diese Angaben löst keine Veranstaltung aus. Eine stornierte Buchung wird entfernt. Wenn alle Tickets für eine Veranstaltung storniert werden, wird auch die Veranstaltung entfernt.

## Zuhause

Unter **Zuhause** speichert deine Machine, was sie über dein Zuhause weiß: **Rechnungen und Abos**, **Geräte**, **Reparaturen und Instandhaltung** und **Das Haus**. Ein Bereich wird angezeigt, sobald er mindestens zwei Zeilen enthält.

- Für regelmäßig anfallende Rechnungen, etwa für Strom oder Wasser, wird eine Zeile mit der Häufigkeit und dem Datum der letzten Rechnung erstellt. Über **Aufgabe öffnen** gelangst du zur Rechnung selbst. Betrag und Zahlungsdetails stehen dort.
- Für ein Abo, das du behalten hast, wird eine Zeile erstellt, über die du die zugehörige Aufgabe unter **Abos** öffnest. Gekündigte Abos werden nicht aufgeführt.
- Wer regelmäßig über dein Zuhause schreibt, etwa dein Energieversorger, Internetanbieter oder die Stadt, erhält eine Zeile mit der Häufigkeit der Nachrichten. Tippe darauf, um die neueste E-Mail zu öffnen.
- Auch Erkenntnisse deiner Machine über dein Zuhause, etwa die Marke deiner Spülmaschine, werden als Zeile aufgeführt. Wenn du sie bearbeitest, ändert sie sich auch unter **Was ich gelernt habe**.
- Wenn du in einem Bereich eine eigene Notiz führst, zum Beispiel eine für deine Spülmaschine unter **Geräte**, werden die dazugehörigen Informationen dort abgelegt. Deine Machine erstellt solche Notizen nicht selbst.

Es werden nur private Rechnungen, Abos und E-Mails verwendet. Notizen unter Zuhause sind immer privat. Deine Machine fragt ihre KI einmal zu jeder neuen Rechnung, jedem neuen Abo und jeder neuen Erkenntnis, ob sie dein Zuhause betreffen. Bei einer Rechnung übermittelt sie den Absender, aber niemals den Betrag.

Für **Zuhause**, **Gesundheit** und **Kinder** zusammen fragt deine Machine ihre KI außerdem einmal zu jedem Absender deiner privaten E-Mails. Dabei übermittelt sie den Namen des Absenders, die Anzahl der gesendeten E-Mails und deren neueste Betreffzeilen, wobei Zahlen unkenntlich gemacht werden. Die E-Mails selbst werden niemals übermittelt.

Beim ersten Mal durchsucht deine Machine innerhalb weniger Stunden das vergangene E-Mail-Jahr, nicht während der Nacht und nur, wenn in deinem KI-Tarif noch Kapazität verfügbar ist. Danach prüft sie alle sechs Stunden neue Absender.

## Gesundheit

Unter **Gesundheit** speichert deine Machine, was sie über deine Gesundheit weiß: **Termine**, **Testergebnisse**, **Ärzte und Pflege**, **Medikamente**, **Allergien und Erkrankungen** sowie **Rechnungen und Versicherung**. Ein Bereich wird angezeigt, sobald er mindestens zwei Zeilen enthält.

- Eine Rechnung von einem Arzt, Zahnarzt oder einer Apotheke wird als Zeile hinzugefügt, über die du die zugehörige Aufgabe öffnest. Der Betrag steht dort.
- Jede E-Mail von deiner Arztpraxis, einem Krankenhaus, einem Labor oder deiner Krankenversicherung erscheint als datierte Zeile mit ihrem Betreff. So entsteht nach und nach deine Übersicht. Tippe darauf, um die E-Mail zu öffnen.
- Auch Erkenntnisse deiner Machine über deine Gesundheit, etwa eine Allergie, werden als Zeile aufgeführt. Wenn du sie bearbeitest, ändert sie sich auch unter **Was ich gelernt habe**.
- Wenn du in einem Bereich eine eigene Notiz führst, zum Beispiel eine für deine Physiotherapeutin oder deinen Physiotherapeuten unter **Termine**, werden die dazugehörigen Informationen dort abgelegt.

Notizen unter Gesundheit sind immer privat, auch wenn eine Rechnung an deine geschäftliche Adresse ging. Deine Machine fragt ihre KI einmal zu jeder neuen Rechnung und jeder neuen Erkenntnis, ob sie deine Gesundheit betrifft.

## Kinder

Unter **Kinder** speichert deine Machine, was sie über deine Kinder weiß: **Schule**, **Aktivitäten**, **Kinderbetreuung**, **Ärzte und Pflege** sowie **Rechnungen und Gebühren**. Ein Babysitter oder eine Kita gehört zu Kinderbetreuung, niemals zu Ärzte und Pflege. Ein Bereich wird angezeigt, sobald er mindestens zwei Zeilen enthält.

- Erkenntnisse deiner Machine über dein Kind, etwa den Namen der Klassenlehrkraft oder den Schwimmtag, erscheinen als Zeile mit einem Link zur Seite des Kindes. Als dein Kind gilt eine Person, wenn unter **Für dich** etwa Tochter oder Sohn steht.
- Eine Rechnung für die Schule, einen Verein oder die Kinderbetreuung wird als Zeile hinzugefügt, über die du die zugehörige Aufgabe öffnest. Der Betrag steht dort.
- Jede E-Mail von der Schule, einem Verein oder der Kinderbetreuung, etwa der wöchentliche Rundbrief oder eine Nachricht zu einem Ausflug, erscheint als datierte Zeile mit ihrem Betreff. So findest du alle Nachrichten an einem Ort. Tippe darauf, um die E-Mail zu öffnen.
- Wenn du in einem Bereich eine eigene Notiz für ein Kind führst, zum Beispiel eine für Isla unter **Schule**, werden die dazugehörigen Informationen dort abgelegt.

Notizen unter Kinder sind immer privat, auch wenn die Schule an deine geschäftliche Adresse schreibt. Deine Machine fragt ihre KI einmal zu jeder neuen Information, ob sie deine Kinder betrifft.

## Zusammenführen, löschen und rückgängig machen

Mit **Zusammenführen mit …** im Menü ⋯ verschiebst du die Zeilen einer Notiz und ihre untergeordneten Notizen in eine andere Notiz. Von da an fügt deine Machine neue Informationen zu dieser Notiz hinzu. Mit **Löschen** entfernst du eine Notiz. Bei beiden Aktionen wird kurz **Rückgängig** angezeigt. Das gilt auch, wenn du eine Zeile entfernst.

## Nicht dasselbe wie Besprechungsnotizen

Besprechungsnotizen und Notizen zu Personen oder Organisationen bleiben an ihrem bisherigen Ort. Die Notizen hier sind eigenständige Seiten.
