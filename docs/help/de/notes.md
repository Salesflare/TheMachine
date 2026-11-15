---
title: Notizen
area: graph
summary: Eine übersichtliche Seite pro Thema, zum Beispiel eine Reise oder dein Zuhause, verknüpft mit den Personen und Projekten, die dazugehören.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, bookings.py, home_notes.py, dashboard/graph-notes.js
order: 8
translated: 4a6b4d56a8d9b93f
---
Eine Notiz bietet einen Überblick über ein Thema: eine Reise, dein Zuhause oder den Ablauf von Rechnungen. Notizen findest du im Graph neben Personen, Organisationen und Projekten. Sie bleiben auf deiner Machine und werden nicht mit deinem Team geteilt.

## Eine Notiz beginnen

Oben in den Notizen findest du **Neue Notiz**. Gib der Notiz einen Titel und wähle **Notiz beginnen**. Die Seite wird geöffnet. Mit **Zeile hinzufügen** kannst du etwas festhalten. Jede Textzeile wird zu einer eigenen Zeile.

## Personen, Projekte und andere Notizen verknüpfen

Gib in einer Zeile @ und die ersten Buchstaben eines Namens ein. Wähle eine Person, Organisation, ein Projekt oder eine Notiz aus der Liste aus. Der Name wird als Link eingefügt. Auf der Seite des verknüpften Eintrags erscheint unter **Verlinkt von** deine Notiz.

## Notizen unter anderen Notizen

Eine Notiz kann unter einer anderen stehen, zum Beispiel „Geräte“ unter „Zuhause“. In den Notizen werden sie als Baum angezeigt: Über den Pfeil neben einer Notiz öffnest du die darunterliegenden Notizen. Um eine Notiz zu verschieben, wähle **Bearbeiten** und lege unter **Unter** fest, wo sie stehen soll. Mit **Neue Notiz unter dieser** im Menü ⋯ erstellst du direkt dort eine Notiz.

## Notizen, die deine Machine führt

Deine Machine erstellt auch selbst Notizen aus deinen Nachrichten und hält sie aktuell. Jede ihrer Zeilen zeigt, woher die Information stammt, zum Beispiel, wer die E-Mail gesendet hat. Tippe auf die Zeile, um die Nachricht zu öffnen. Eine Zeile aus **Was ich gelernt habe** ist mit **Aus meinen Erkenntnissen** gekennzeichnet.

Deine Änderungen bleiben immer erhalten. Benennst du eine Notiz um, verschiebst sie oder änderst ihre Daten oder eine Zeile, übernimmt deine Machine das auch bei späteren Aktualisierungen. Löschst du eine Zeile oder eine Notiz, kommt sie nicht zurück. Spätere Notizen zum selben Thema werden dort eingefügt, wo du die erste abgelegt hast.

Mit **Zurück zum Original** werden wieder die eigenen Worte deiner Machine angezeigt. Wenn du eine Zeile bearbeitest, die aus den Erkenntnissen deiner Machine stammt, wird sie auch unter **Was ich gelernt habe** geändert. So gibt es nur eine Version davon.

## Reisen

Wenn eine Flug-, Hotel-, Zug-, Bus-, Fähr- oder Mietwagenbuchung in deinem Posteingang eingeht, fügt deine Machine sie unter **Reisen** zu einer Reise hinzu. Buchungen für dieselbe Reise kommen in eine Reise: die Hinfahrt, das Hotel und die Rückfahrt. Für jede Zeile enthält die Reise den Buchungscode, den Sitzplatz und das Ticket, chronologisch geordnet. Außerdem werden die Reisedaten angezeigt. Im [Kalender](calendar.md) erscheint sie als durchgehender Balken über diese Tage. Wenn du darauf tippst, wird die Reise geöffnet.

Deine Machine liest die Buchungsdetails aus den Bestätigungs-E-Mails, die Fluggesellschaften, Hotels und Buchungsseiten senden. Eine E-Mail ohne diese Details erstellt keine Reise. Wird eine Buchung geändert, wird die entsprechende Zeile aktualisiert. Wird sie storniert, wird sie entfernt. Wenn alle Buchungen einer Reise storniert sind, wird auch die Reise entfernt.

## Zuhause

Unter **Zuhause** hält deine Machine fest, was sie über dein Zuhause weiß: **Rechnungen und Abos**, **Geräte**, **Reparaturen und Instandhaltung** und **Das Haus**. Ein Bereich wird angezeigt, sobald er mindestens zwei Zeilen enthält.

- Eine regelmäßig anfallende Rechnung, zum Beispiel für Energie oder Wasser, erhält eine Zeile mit der Häufigkeit und dem Datum der letzten Rechnung. Über **Aufgabe öffnen** wird die Rechnung selbst angezeigt. Betrag und Zahlungsdetails bleiben dort.
- Ein Abo, das du noch hast, erhält eine Zeile, über die du die zugehörige Aufgabe unter **Abos** öffnest. Gekündigte Abos werden nicht aufgeführt.
- Auch Informationen, die deine Machine über dein Zuhause gelernt hat, etwa die Marke deiner Spülmaschine, erscheinen als Zeile. Wenn du die Information bearbeitest, ändert sie sich auch unter **Was ich gelernt habe**.
- Wenn du in einem Bereich eigene Notizen hast, zum Beispiel eine Notiz zu deiner Spülmaschine unter **Geräte**, kommen die Informationen zu diesem Gerät stattdessen in deine Notiz. Deine Machine erstellt solche Notizen nicht selbst.

Es werden nur Rechnungen und Abos verwendet, die als persönlich eingestuft sind. Notizen unter „Zuhause“ sind immer persönlich. Deine Machine fragt ihre KI bei jeder neuen Rechnung, jedem neuen Abo und jeder neuen Information einmal, ob es um dein Zuhause geht. Bei einer Rechnung teilt sie mit, von wem sie stammt, aber niemals den Betrag.

## Zusammenführen, löschen und rückgängig machen

Mit **Zusammenführen mit …** im Menü ⋯ verschiebst du die Zeilen einer Notiz und die darunterliegenden Notizen in eine andere Notiz. Von da an fügt deine Machine neue Informationen zu dieser Notiz hinzu. Mit **Löschen** entfernst du eine Notiz. Bei beiden Aktionen und auch beim Entfernen einer Zeile kannst du kurz **Rückgängig** wählen.

## Nicht dasselbe wie Besprechungsnotizen

Besprechungsnotizen und Notizen zu Personen oder Organisationen bleiben dort, wo sie waren. Die Notizen hier sind eigenständige Seiten.
