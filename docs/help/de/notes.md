---
title: Notizen
area: graph
summary: Eine übersichtliche Seite pro Thema, etwa zu einer Reise oder deinem Zuhause, verknüpft mit den darin vorkommenden Personen und Projekten.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: 336e0f0dad44f19a
---
Eine Notiz gibt dir einen Überblick über ein Thema: eine Reise, dein Zuhause oder die Bezahlung von Rechnungen. Notizen stehen im Graph neben Personen, Organisationen und Projekten. Sie bleiben auf deiner Machine und werden nicht mit deinem Team geteilt.

## Notiz beginnen

Über **Neue Notiz** oben in den Notizen legst du eine Notiz an. Gib ihr einen Titel und wähle **Notiz beginnen**. Dann öffnet sich die Seite. Mit **Zeile hinzufügen** fügst du hinzu, was du festhalten möchtest. Jede Textzeile wird zu einer eigenen Zeile.

## Mit Personen, Projekten und anderen Notizen verknüpfen

Gib in einer Zeile @ und einige Buchstaben eines Namens ein. Wähle eine Person, Organisation, ein Projekt oder eine Notiz aus der Liste. Der Name wird als Link eingefügt. Auf der Seite des verknüpften Elements erscheint unter **Verlinkt von** deine Notiz.

## Notizen unter anderen Notizen

Eine Notiz kann unter einer anderen liegen, zum Beispiel Geräte unter Zuhause. In den Notizen werden sie als Baum angezeigt: Über den Pfeil neben einer Notiz öffnest du die darunterliegenden Notizen. Um eine Notiz zu verschieben, wähle **Bearbeiten** und dann unter **Unter** den gewünschten Ort. Mit **Neue Notiz unter dieser** im Menü ⋯ erstellst du direkt darunter eine Notiz.

Oben auf einer Notizseite siehst du, wo sie liegt, zum Beispiel **Notizen › Kinder**. Tippe auf einen beliebigen Teil, um dorthin zu gehen. Auf dem Smartphone werden dazwischenliegende Notizen im Menü ⋯ zusammengeklappt.

## Notizen, die deine Machine führt

Deine Machine schreibt auch selbst Notizen aus deinen Nachrichten und hält sie aktuell. Bei jeder Zeile steht, woher sie stammt, zum Beispiel, wer die E-Mail geschickt hat. Tippe darauf, um die Nachricht zu öffnen. Bei einer Zeile aus **Was ich gelernt habe** steht **Aus meinen Erkenntnissen**. Besprechungen und Termine aus deinem Kalender erscheinen nie als eigene Zeile. Sie bleiben im [Kalender](calendar.md).

**Zuhause**, **Gesundheit** und **Kinder** erscheinen erst, wenn deine Machine dort mindestens zwei konkrete Dinge zu sagen hat, zum Beispiel zu einer Rechnung oder einer Erkenntnis. Bis dahin tauchen sie gar nicht in der Liste auf. Wenn sie später wieder leer sind, verschwinden sie.

Deine Änderungen bleiben immer erhalten. Benennst du eine Notiz um, verschiebst du sie oder änderst du ihre Termine oder eine Zeile, behält deine Machine diese Änderungen bei, wenn sie die Notiz aktualisiert. Löschst du eine Zeile oder eine Notiz, kommt sie nicht zurück. Spätere Notizen zum selben Thema landen dort, wo du die erste Notiz abgelegt hast.

Mit **Zurück zum Original** werden wieder die eigenen Worte deiner Machine angezeigt. Wenn du eine Zeile bearbeitest, die aus einer Erkenntnis deiner Machine stammt, ändert sie sich auch unter **Was ich gelernt habe**. So gibt es nur eine Version davon.

## Reisen

Wenn eine Buchung für einen Flug, ein Hotel, einen Zug, einen Bus, eine Fähre oder einen Mietwagen in deinem Posteingang landet, fügt deine Machine sie unter **Reisen** zu einer Reise hinzu. Buchungen für dieselbe Reise landen zusammen: die Hinfahrt, das Hotel und die Rückfahrt. Für jede Buchung enthält die Reise eine Zeile mit Buchungscode, Sitzplatz und Ticket. Die Zeilen sind nach Uhrzeit sortiert. Außerdem werden die Reisedaten angezeigt. Im [Kalender](calendar.md) erscheint die Reise als ein Balken über diese Tage. Tippe darauf, um die Reise zu öffnen.

Deine Machine liest die Buchungsdetails aus den Bestätigungsmails von Fluggesellschaften, Hotels und Buchungsseiten. Eine Mail ohne diese Angaben erstellt keine Reise. Buchungsmails aus der Zeit vor dem Jahr, dessen [Verlauf](history.md) deine Machine aufbewahrt, werden im Hintergrund eingelesen, sobald dieser Verlauf verfügbar ist. Dabei werden zuerst deine persönlichen Postfächer berücksichtigt. Wird eine ältere Bestätigung später eingelesen, wird sie der bereits vorhandenen Reise hinzugefügt.

Wird eine Buchung geändert, wird ihre Zeile aktualisiert. Wird sie storniert, verschwindet sie. Wenn alle Buchungen einer Reise storniert wurden, verschwindet auch die Reise.

## Termine

Wenn Tickets für ein Konzert, ein Spiel, ein Festival oder eine Konferenz in deinem Posteingang landen, fügt deine Machine das Ereignis unter **Termine** hinzu. Für jedes Ereignis gibt es eine eigene Notiz. Eine Zeile enthält den Veranstaltungsort, den Buchungscode, den Sitzplatz und die Anzahl der Tickets. Eine zweite Bestellung für dasselbe Ereignis kommt in dieselbe Notiz. Wie bei einer Reise werden auch hier die Daten angezeigt. Im [Kalender](calendar.md) erscheint das Ereignis als Balken. Tippe darauf, um die Notiz zu öffnen.

- Bei jeder Zeile steht, von wem die Tickets stammen, zum Beispiel **Von Example Tickets**. Tippe darauf, um die Mail zu öffnen.
- Wenn aus der Ticketmail eine Aufgabe entstanden ist, zum Beispiel das Bezahlen der Tickets, wird sie über **Aufgabe öffnen** angezeigt.
- Ein Ereignis, das über dein Arbeits-Postfach gebucht wurde, ist Arbeit. Andernfalls ist es Privat.

Deine Machine liest die Ticketdetails ohne KI aus den Bestätigungsmails der Ticketanbieter. Eine Mail ohne diese Angaben erstellt kein Ereignis. Wird eine Buchung storniert, verschwindet sie. Wenn alle Tickets für ein Ereignis storniert wurden, verschwindet auch das Ereignis.

## Zuhause

Unter **Zuhause** hält deine Machine fest, was sie über dein Zuhause weiß: **Rechnungen und Abos**, **Geräte**, **Reparaturen und Instandhaltung** und **Das Haus**. Ein Bereich erscheint, sobald er mindestens zwei Zeilen enthält.

- Regelmäßig anfallende Rechnungen, zum Beispiel für Strom oder Wasser, erhalten eine Zeile mit der Häufigkeit und dem Datum der letzten Rechnung. Über **Aufgabe öffnen** wird die Rechnung selbst angezeigt. Betrag und Zahlungsdetails stehen dort.
- Ein Abo, das du behalten hast, erhält eine Zeile, über die du die Aufgabe **Abos** öffnest. Gekündigte Abos werden nicht aufgeführt.
- Wer regelmäßig wegen deines Zuhauses schreibt, zum Beispiel dein Energieversorger, Internetanbieter oder die Gemeinde, erhält eine Zeile mit der Häufigkeit. Tippe darauf, um die neueste E-Mail zu öffnen.
- Auch Erkenntnisse deiner Machine über dein Zuhause, zum Beispiel die Marke deiner Spülmaschine, erscheinen als Zeile. Wenn du sie bearbeitest, ändert sie sich auch unter **Was ich gelernt habe**.
- Wenn du in einem Bereich eine eigene Notiz führst, zum Beispiel für deine Spülmaschine unter **Geräte**, landet alles zu diesem Gerät in deiner Notiz. Deine Machine erstellt solche Notizen nicht selbst.

Es werden nur persönliche Rechnungen, Abos und E-Mails verwendet. Notizen unter Zuhause sind immer persönlich. Deine Machine fragt ihre KI einmal zu jeder neuen Rechnung, jedem neuen Abo und jeder neuen Erkenntnis, ob sie dein Zuhause betreffen. Bei einer Rechnung übermittelt sie, von wem sie stammt, aber niemals den Betrag.

Für **Zuhause**, **Gesundheit** und **Kinder** fragt deine Machine ihre KI außerdem einmal zu jedem Absender deiner persönlichen E-Mails. Sie übermittelt den Namen des Absenders, die Anzahl der E-Mails und die Betreffzeilen der neuesten E-Mails, wobei Zahlen ausgeblendet werden. Die E-Mails selbst werden niemals übermittelt. Eine E-Mail, die zweimal oder in zwei deiner Postfächer eingegangen ist, wird nur einmal gezählt. Dasselbe gilt für eine Antwort mit demselben Betreff im selben Thread.

Massenmails landen nie in diesen Notizen und werden nie an die KI gesendet. Dazu gehören Spam, Werbemails, Newsletter und andere Listenmails sowie Benachrichtigungen von No-Reply-Adressen. Mails in einem Thread, auf den du geantwortet hast, werden trotzdem berücksichtigt. Das gilt auch für Buchungsmails zu **Reisen** und **Terminen**.

Beim ersten Mal verarbeitet deine Machine die E-Mails aus dem vergangenen Jahr innerhalb weniger Stunden, außerhalb der Nacht und nur, solange in deinem KI-Tarif noch Kapazität ist. Danach prüft sie alle sechs Stunden neue Absender.

## Gesundheit

Unter **Gesundheit** hält deine Machine fest, was sie über deine Gesundheit weiß: **Termine**, **Testergebnisse**, **Ärzte und Pflege**, **Medikamente**, **Allergien und Erkrankungen** sowie **Rechnungen und Versicherung**. Ein Bereich erscheint, sobald er mindestens zwei Zeilen enthält.

- Eine Rechnung von einer Arztpraxis, Zahnarztpraxis oder Apotheke erhält eine Zeile, über die du die zugehörige Aufgabe öffnest. Der Betrag steht dort.
- Jede E-Mail von deiner Praxis, einem Krankenhaus, einem Labor oder deiner Krankenversicherung wird als datierte Zeile mit Betreff angezeigt. So baut sich mit der Zeit dein Verlauf auf. Tippe darauf, um die E-Mail zu öffnen.
- Auch Erkenntnisse deiner Machine über deine Gesundheit, zum Beispiel eine Allergie, erscheinen als Zeile. Wenn du sie bearbeitest, ändert sie sich auch unter **Was ich gelernt habe**.
- In deiner eigenen Notiz in einem Bereich, zum Beispiel für deine Physiotherapie-Termine unter **Termine**, landet alles, was diese betrifft.

Notizen unter Gesundheit sind immer persönlich, auch wenn eine Rechnung an deine Arbeitsadresse geschickt wurde. Deine Machine fragt ihre KI einmal zu jeder neuen Rechnung und jeder neuen Erkenntnis, ob sie deine Gesundheit betrifft.

## Kinder

Unter **Kinder** hält deine Machine fest, was sie über deine Kinder weiß: **Schule**, **Aktivitäten**, **Kinderbetreuung**, **Ärzte und Pflege** sowie **Rechnungen und Gebühren**. Ein Babysitter oder eine Kita gehört zu Kinderbetreuung, niemals zu Ärzte und Pflege. Ein Bereich erscheint, sobald er mindestens zwei Zeilen enthält.

- Erkenntnisse deiner Machine über dein Kind, zum Beispiel den Namen der Klassenlehrerin oder den Schwimmtag, erscheinen als Zeile, die mit der Seite des Kindes verknüpft ist. Als dein Kind gilt eine Person, wenn bei ihr unter **Für dich** eine entsprechende Beziehung steht, zum Beispiel Tochter oder Sohn.
- Eine Rechnung für die Schule, einen Verein oder die Kinderbetreuung erhält eine Zeile, über die du die zugehörige Aufgabe öffnest. Der Betrag steht dort.
- Jede E-Mail von der Schule, einem Verein oder der Kinderbetreuung, zum Beispiel eine Nachricht zu einem Ausflug oder einer Planänderung, wird als datierte Zeile mit Betreff angezeigt. So findest du alles, was sie schicken, an einem Ort. Tippe darauf, um die E-Mail zu öffnen.
- In deiner eigenen Notiz für ein Kind in einem Bereich, zum Beispiel für Isla unter **Schule**, landet alles, was dieses Kind betrifft.

Notizen unter Kinder sind immer persönlich, auch wenn die Schule an deine Arbeitsadresse schreibt. Deine Machine fragt ihre KI einmal zu jeder neuen Erkenntnis, ob sie deine Kinder betrifft.

## Zusammenführen, löschen und rückgängig machen

Mit **Zusammenführen mit …** im Menü ⋯ verschiebst du die Zeilen einer Notiz und die darunterliegenden Notizen in eine andere Notiz. Neue Informationen fügt deine Machine von da an dieser Notiz hinzu. **Löschen** entfernt eine Notiz. Bei beiden Aktionen kannst du kurz **Rückgängig** wählen. Das gilt auch, wenn du eine Zeile entfernst.

## Nicht dasselbe wie Besprechungsnotizen

Besprechungsnotizen und Notizen zu Personen oder Organisationen bleiben an ihrem bisherigen Ort. Die Notizen hier sind eigenständige Seiten.
