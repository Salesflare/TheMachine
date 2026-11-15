---
title: Notizen
area: graph
summary: Eine übersichtliche Seite pro Thema, etwa zu einer Reise oder deinem Zuhause, verknüpft mit den darin vorkommenden Personen und Projekten.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: b88647412222409d
---
Eine Notiz bietet einen Überblick zu einem Thema: einer Reise, deinem Zuhause oder der Abwicklung von Rechnungen. Notizen stehen im Graph neben Personen, Organisationen und Projekten. Sie bleiben auf deiner Machine und werden nicht mit deinem Team geteilt.

## Eine Notiz beginnen

Oben in den Notizen findest du **Neue Notiz**. Gib einen Titel ein und wähle **Notiz beginnen**, damit sich die Seite öffnet. Mit **Zeile hinzufügen** fügst du hinzu, was du festhalten möchtest. Jede Textzeile wird zu einer eigenen Zeile.

## Personen, Projekte und andere Notizen verknüpfen

Gib in einer Zeile @ und die ersten Buchstaben eines Namens ein. Wähle eine Person, Organisation, ein Projekt oder eine Notiz aus der Liste aus. Der Name wird als Link eingefügt. Auf der Seite des verknüpften Eintrags erscheint unter **Verlinkt von** deine Notiz.

## Notizen unter Notizen

Eine Notiz kann unter einer anderen stehen, zum Beispiel Geräte unter Zuhause. In den Notizen werden sie als Baum dargestellt: Über den Pfeil neben einer Notiz öffnest du die darunterliegenden. Um eine Notiz zu verschieben, wähle **Bearbeiten** und unter **Unter** den gewünschten Ort. Mit **Neue Notiz unter dieser** im ⋯-Menü erstellst du direkt dort eine Notiz.

## Notizen, die deine Machine führt

Deine Machine verfasst auch selbst Notizen auf Grundlage deiner Nachrichten und hält sie aktuell. In jeder Zeile steht, woher sie stammt, zum Beispiel, wer die E-Mail gesendet hat. Tippe darauf, um die Nachricht zu öffnen. Eine Zeile aus **Was ich gelernt habe** ist mit **Aus meinen Erkenntnissen** gekennzeichnet.

Deine Änderungen bleiben immer erhalten. Wenn du eine Notiz umbenennst, verschiebst, ihre Daten oder eine Zeile änderst, übernimmt deine Machine das, wenn sie die Notiz aktualisiert. Wenn du eine Zeile oder Notiz löschst, kommt sie nicht zurück. Spätere Notizen zum selben Thema werden dort eingefügt, wo du die erste abgelegt hast.

Mit **Zurück zum Original** werden wieder die eigenen Formulierungen deiner Machine angezeigt. Wenn du eine Zeile bearbeitest, die deine Machine aus ihren Erkenntnissen übernommen hat, wird sie auch unter **Was ich gelernt habe** geändert. So gibt es nur eine Version davon.

## Reisen

Wenn eine Flug-, Hotel-, Zug-, Bus-, Fähr- oder Mietwagenbuchung in deinem Postfach eingeht, fügt deine Machine sie unter **Reisen** einer Reise hinzu. Buchungen für eine Reise kommen auf dieselbe Seite: die Hinfahrt, das Hotel und die Rückfahrt. Die Reise enthält für jede Zeile den Buchungscode, Sitzplatz und das Ticket, in zeitlicher Reihenfolge, und zeigt die Reisedaten an. Im [Kalender](calendar.md) erscheint sie als ein Balken über diese Tage. Wenn du darauf tippst, öffnet sich die Reise.

Deine Machine liest die Buchungsdetails aus den Bestätigungsmails von Fluggesellschaften, Hotels und Buchungsseiten. Eine E-Mail ohne diese Angaben erstellt keine Reise. Buchungsmails aus der Zeit vor dem Jahr, für das deine Machine den [Verlauf](history.md) speichert, werden im Hintergrund gelesen, sobald dieser Verlauf verfügbar ist. Bei einer geänderten Buchung wird die Zeile aktualisiert. Eine stornierte Buchung wird entfernt. Wenn alle Buchungen einer Reise storniert sind, wird auch die Reise entfernt.

## Termine

Wenn Konzert-, Spiel-, Festival- oder Konferenztickets in deinem Postfach eingehen, fügt deine Machine den Termin unter **Termine** hinzu. Für jeden Termin gibt es eine eigene Notiz. In einer Zeile stehen der Veranstaltungsort, der Buchungscode, der Sitzplatz und die Anzahl der Tickets. Eine zweite Bestellung für denselben Termin kommt in dieselbe Notiz. Wie eine Reise zeigt der Termin seine Daten und erscheint im [Kalender](calendar.md) als Balken, über den sich die Notiz öffnen lässt.

- In jeder Zeile steht, von wem die Tickets stammen, zum Beispiel **Von Example Tickets**. Tippe darauf, um die E-Mail zu öffnen.
- Wenn aus der Ticketmail eine Aufgabe entstanden ist, zum Beispiel, die Tickets zu bezahlen, wird sie über **Aufgabe öffnen** angezeigt.
- Ein Termin, der über dein berufliches Postfach gebucht wurde, ist Arbeit. Andernfalls ist er Privat.

Deine Machine liest die Ticketdetails aus den Bestätigungsmails der Ticketanbieter, ohne KI. Eine E-Mail ohne diese Angaben erstellt keinen Termin. Eine stornierte Buchung wird entfernt. Wenn alle Tickets für einen Termin storniert sind, wird auch der Termin entfernt.

## Zuhause

Unter **Zuhause** hält deine Machine fest, was sie über dein Zuhause weiß: **Rechnungen und Abos**, **Geräte**, **Reparaturen und Instandhaltung** und **Das Haus**. Ein Bereich wird angezeigt, sobald er mindestens zwei Zeilen enthält.

- Eine regelmäßig anfallende Rechnung, zum Beispiel für Strom oder Wasser, erhält eine Zeile mit der Häufigkeit und dem Datum der letzten Rechnung. Über **Aufgabe öffnen** wird die Rechnung selbst angezeigt. Der Betrag und die Zahlungsdetails bleiben dort.
- Ein Abo, das du behalten hast, erhält eine Zeile, über die sich die Aufgabe **Abos** öffnen lässt. Gekündigte Abos werden nicht aufgeführt.
- Auch Erkenntnisse deiner Machine über dein Zuhause, zum Beispiel die Marke deiner Spülmaschine, erscheinen als Zeile. Wenn du sie bearbeitest, ändert sie sich auch unter **Was ich gelernt habe**.
- Wenn du in einem Bereich eine eigene Notiz führst, zum Beispiel zu deiner Spülmaschine unter **Geräte**, kommen die Informationen zu diesem Gerät stattdessen in deine Notiz. Deine Machine erstellt solche Notizen nicht selbst.

Verwendet werden nur Rechnungen und Abos mit der Kennzeichnung Privat. Notizen unter Zuhause sind immer privat. Deine Machine fragt ihre KI einmal zu jeder neuen Rechnung, jedem Abo und jeder neuen Erkenntnis, ob sie dein Zuhause betrifft. Bei einer Rechnung übermittelt sie, von wem sie stammt, aber niemals den Betrag.

## Gesundheit

Unter **Gesundheit** hält deine Machine fest, was sie über deine Gesundheit weiß: **Termine**, **Ärzte und Pflege**, **Medikamente**, **Allergien und Erkrankungen** sowie **Rechnungen und Versicherung**. Ein Bereich wird angezeigt, sobald er mindestens zwei Zeilen enthält.

- Ein Kalendereintrag, zu dem nur du gehst, zum Beispiel ein Zahnarzttermin, erhält eine Zeile mit dem nächsten oder letzten Datum. Über **Aus deinem Kalender** lässt er sich öffnen.
- Eine Rechnung von einem Arzt, Zahnarzt oder einer Apotheke erhält eine Zeile, über die sich die Aufgabe öffnen lässt. Der Betrag bleibt dort.
- Auch Erkenntnisse deiner Machine über deine Gesundheit, zum Beispiel eine Allergie, erscheinen als Zeile. Wenn du sie bearbeitest, ändert sie sich auch unter **Was ich gelernt habe**.
- In deine eigene Notiz in einem Bereich, zum Beispiel zu deiner Physiotherapie unter **Termine**, kommen die Informationen zu diesem Thema.

Notizen unter Gesundheit sind immer privat, auch wenn eine Rechnung an deine berufliche Adresse geschickt wurde. Deine Machine fragt ihre KI einmal zu jedem neuen Termin, jeder neuen Rechnung und jeder neuen Erkenntnis, ob sie deine Gesundheit betrifft. Bei einem Termin übermittelt sie den Namen, aber weder die Notizen noch die Namen anderer Eingeladener.

## Kinder

Unter **Kinder** hält deine Machine fest, was sie über deine Kinder weiß: **Schule**, **Aktivitäten**, **Ärzte und Pflege** sowie **Rechnungen und Gebühren**. Ein Bereich wird angezeigt, sobald er mindestens zwei Zeilen enthält.

- Erkenntnisse deiner Machine über dein Kind, zum Beispiel den Namen der Klassenlehrkraft oder den Schwimmtag, erscheinen als Zeile mit einem Link zur Seite deines Kindes. Deine Machine zählt jemanden als dein Kind, wenn unter **Für dich** eine entsprechende Angabe steht, zum Beispiel Tochter oder Sohn.
- Ein Kalendereintrag, zu dem nur du gehst, zum Beispiel ein Elternabend, erhält eine Zeile mit dem nächsten oder letzten Datum. Über **Aus deinem Kalender** lässt er sich öffnen.
- Eine Rechnung für die Schule, einen Verein oder die Kinderbetreuung erhält eine Zeile, über die sich die Aufgabe öffnen lässt. Der Betrag bleibt dort.
- In deine eigene Notiz zu einem Kind in einem Bereich, zum Beispiel zu Isla unter **Schule**, kommen die Informationen zu diesem Kind.

Notizen unter Kinder sind immer privat, auch wenn die Schule an deine berufliche Adresse schreibt. Deine Machine fragt ihre KI einmal zu jedem neuen Eintrag, ob er deine Kinder betrifft.

## Zusammenführen, löschen und rückgängig machen

Mit **Zusammenführen mit …** im ⋯-Menü verschiebst du die Zeilen einer Notiz und die Notizen darunter in eine andere Notiz. Von da an ergänzt deine Machine diese Notiz. Mit **Löschen** entfernst du eine Notiz. Beides lässt sich kurz mit **Rückgängig** rückgängig machen. Das gilt auch, wenn du eine Zeile entfernst.

## Nicht dasselbe wie Besprechungsnotizen

Besprechungsnotizen und Notizen zu Personen oder Organisationen bleiben an ihrem bisherigen Ort. Die Notizen hier sind eigenständige Seiten.
