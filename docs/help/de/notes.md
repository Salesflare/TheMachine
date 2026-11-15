---
title: Notizen
area: graph
summary: Eine übersichtliche Seite pro Thema, etwa zu einer Reise oder deinem Zuhause, verknüpft mit den Personen und Projekten, die dazugehören.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, dashboard/graph-notes.js
order: 8
translated: 59dd4e1951e7cc7d
---
Eine Notiz gibt dir einen Überblick über ein Thema: eine Reise, dein Zuhause oder den Ablauf für Rechnungen. Notizen findest du im Graph neben Personen, Organisationen und Projekten. Sie bleiben auf deiner Machine und werden nicht mit deinem Team geteilt.

## Eine Notiz beginnen

Oben in den Notizen findest du **Neue Notiz**. Gib einen Titel ein und wähle **Notiz beginnen**. Die Seite der Notiz öffnet sich. Mit **Zeile hinzufügen** fügst du hinzu, was du festhalten möchtest. Jede Texteingabe wird zu einer eigenen Zeile.

## Mit Personen, Projekten und anderen Notizen verknüpfen

Gib in einer Zeile @ und ein paar Buchstaben eines Namens ein. Wähle eine Person, Organisation, ein Projekt oder eine Notiz aus der Liste aus. Der Name wird als Link eingefügt. Auf der Seite des verknüpften Eintrags erscheint unter **Verlinkt von** deine Notiz.

## Notizen unter anderen Notizen

Eine Notiz kann unter einer anderen liegen, zum Beispiel Geräte unter Zuhause. In den Notizen werden sie als Baum angezeigt. Über den Pfeil neben einer Notiz kannst du die darunterliegenden öffnen. Um eine Notiz zu verschieben, wähle **Bearbeiten** und dann unter **Unter** aus, wo sie liegen soll. Über **Neue Notiz unter dieser** im Menü ⋯ kannst du direkt dort eine Notiz anlegen.

## Notizen, die deine Machine führt

Deine Machine schreibt auch selbst Notizen aus deinen Nachrichten und hält sie aktuell. Bei jeder Zeile steht, woher sie stammt, zum Beispiel wer die E-Mail gesendet hat. Tippe darauf, um die Nachricht zu öffnen. Bei einer Zeile aus **Was ich gelernt habe** steht **Aus meinen Erkenntnissen**.

Deine Änderungen bleiben immer erhalten. Wenn du eine Notiz umbenennst oder verschiebst oder ihre Daten oder eine Zeile änderst, übernimmt deine Machine das beim Aktualisieren der Notiz. Wenn du eine Zeile oder Notiz löschst, kommt sie nicht wieder. Spätere Notizen zum selben Thema landen dort, wo du die erste abgelegt hast.

Mit **Zurück zum Original** werden wieder die eigenen Worte deiner Machine angezeigt. Wenn du eine Zeile bearbeitest, die deine Machine aus dem Gelernten übernommen hat, ändert sich auch der Eintrag unter **Was ich gelernt habe**. So gibt es nur eine Version davon.

## Reisen

Wenn eine Flug-, Hotel-, Zug-, Bus-, Fähr- oder Mietwagenbuchung in deinem Postfach eingeht, fügt deine Machine sie unter **Reisen** einer Reise hinzu. Buchungen für eine Reise landen gemeinsam auf einer Seite: die Hinfahrt, das Hotel und die Rückfahrt. Die Reise zeigt das Buchungskürzel, den Sitzplatz und das Ticket für jede Zeile, sortiert nach Uhrzeit. Außerdem zeigt sie die Reisedaten. Im [Kalender](calendar.md) wird sie als ein Balken über diese Tage angezeigt. Wenn du darauf tippst, öffnet sich die Reise.

Deine Machine liest die Buchungsdetails aus den Bestätigungsmails von Fluggesellschaften, Hotels und Buchungsseiten. Eine E-Mail ohne diese Angaben erstellt keine Reise. Wird eine Buchung geändert, wird die entsprechende Zeile aktualisiert. Wird sie storniert, wird sie entfernt. Wenn alle Buchungen einer Reise storniert werden, wird auch die Reise entfernt.

## Zuhause

Unter **Zuhause** hält deine Machine fest, was sie über dein Zuhause weiß: **Rechnungen und Abos**, **Geräte**, **Reparaturen und Instandhaltung** und **Das Haus**. Ein Bereich wird angezeigt, sobald er mindestens zwei Zeilen enthält.

- Eine regelmäßig anfallende Rechnung, zum Beispiel für Strom oder Wasser, erhält eine Zeile mit der Häufigkeit und dem Datum der letzten Rechnung. Über **Aufgabe öffnen** kannst du die Rechnung selbst öffnen. Der Betrag und die Zahlungsdetails stehen dort.
- Für ein Abo, das du behalten hast, gibt es eine Zeile, über die du die Aufgabe **Abos** öffnest. Ein gekündigtes Abo wird nicht aufgeführt.
- Auch was deine Machine über dein Zuhause gelernt hat, zum Beispiel die Marke deiner Spülmaschine, wird als Zeile aufgeführt. Wenn du den Eintrag bearbeitest, ändert er sich auch unter **Was ich gelernt habe**.
- Wenn du in einem Bereich eine eigene Notiz führst, zum Beispiel eine zu deiner Spülmaschine unter **Geräte**, landen die Informationen zu diesem Gerät in deiner Notiz. Deine Machine legt solche Notizen nicht selbst an.

Es werden nur persönliche Rechnungen und Abos verwendet, und Notizen unter Zuhause sind immer persönlich. Deine Machine fragt ihre KI einmal zu jeder neuen Rechnung, jedem Abo und jedem neu gelernten Eintrag, ob es um dein Zuhause geht. Bei einer Rechnung übermittelt sie, von wem sie stammt, aber niemals den Betrag.

## Gesundheit

Unter **Gesundheit** hält deine Machine fest, was sie über deine Gesundheit weiß: **Termine**, **Ärzte und Pflege**, **Medikamente**, **Allergien und Erkrankungen** und **Rechnungen und Versicherung**. Ein Bereich wird angezeigt, sobald er mindestens zwei Zeilen enthält.

- Ein Termin in deinem Kalender, zu dem nur du gehst, zum Beispiel beim Zahnarzt, erhält eine Zeile mit dem nächsten oder dem letzten Datum. Über **Aus deinem Kalender** kannst du den Termin öffnen.
- Für eine Rechnung von einem Arzt, Zahnarzt oder einer Apotheke gibt es eine Zeile, über die du die zugehörige Aufgabe öffnest. Der Betrag steht dort.
- Auch was deine Machine über deine Gesundheit gelernt hat, zum Beispiel eine Allergie, wird als Zeile aufgeführt. Wenn du den Eintrag bearbeitest, ändert er sich auch unter **Was ich gelernt habe**.
- Wenn du in einem Bereich eine eigene Notiz führst, zum Beispiel eine zu deiner Physiotherapeutin unter **Termine**, landen die Informationen zu diesem Thema in deiner Notiz.

Notizen unter Gesundheit sind immer persönlich, auch wenn eine Rechnung an deine geschäftliche Adresse geschickt wurde. Deine Machine fragt ihre KI einmal zu jedem neuen Termin, jeder neuen Rechnung und jedem neu gelernten Eintrag, ob es um deine Gesundheit geht. Bei einem Termin übermittelt sie den Namen, aber weder die Notizen dazu noch, wer sonst noch eingeladen ist.

## Zusammenführen, löschen und rückgängig machen

Mit **Zusammenführen mit …** im Menü ⋯ verschiebst du die Zeilen einer Notiz und die darunterliegenden Notizen in eine andere Notiz. Von da an fügt deine Machine neue Einträge zu dieser Notiz hinzu. **Löschen** entfernt eine Notiz. Bei beiden Aktionen und auch beim Entfernen einer Zeile kannst du kurz **Rückgängig** wählen.

## Nicht dasselbe wie Besprechungsnotizen

Besprechungsnotizen und Notizen zu einer Person oder Organisation bleiben an ihrem bisherigen Ort. Die Notizen hier sind eigenständige Seiten.
