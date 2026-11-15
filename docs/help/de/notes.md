---
title: Notizen
area: graph
summary: Eine übersichtliche Seite pro Thema, etwa zu einer Reise oder deinem Zuhause. Sie ist mit den Personen und Projekten verknüpft, die dazugehören.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, topic_notes.py, note_writer.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: 88cfd4099bf27f38
---
Eine Notiz bietet einen Überblick zu einem Thema: einer Reise, deinem Zuhause oder dazu, wie Rechnungen bezahlt werden. Notizen stehen im Graph neben Personen, Organisationen und Projekten. Sie bleiben auf deiner Machine und werden nicht mit deinem Team geteilt.

## Notiz beginnen

Oben in den Notizen findest du **Neue Notiz**. Gib einen Titel ein und wähle **Notiz beginnen**. Die Seite wird geöffnet. Mit **Zeile hinzufügen** kannst du festhalten, was dir wichtig ist. Jede Textzeile wird zu einer eigenen Zeile.

## Mit Personen, Projekten und anderen Notizen verknüpfen

Gib in einer Zeile @ und die ersten Buchstaben eines Namens ein. Wähle aus der Liste eine Person, Organisation, ein Projekt oder eine Notiz aus. Der Name wird als Link eingefügt. Auf der Seite des verknüpften Eintrags erscheint unter **Verlinkt von** deine Notiz.

## Notizen unter anderen Notizen

Eine Notiz kann unter einer anderen stehen, zum Beispiel Geräte unter Zuhause. In den Notizen werden sie als Baum angezeigt: Mit dem Pfeil neben einer Notiz kannst du die darunterliegenden öffnen. Um eine Notiz zu verschieben, wähle **Bearbeiten** und dann unter **Unter** den gewünschten Ort. Über **Neue Notiz unter dieser** im Menü ⋯ kannst du direkt dort eine Notiz erstellen.

Oben auf der Notizseite siehst du, wo sie sich befindet, zum Beispiel **Notizen › Kinder**. Tippe auf einen beliebigen Teil, um dorthin zu gelangen. Auf dem Smartphone werden dazwischenliegende Notizen im Menü ⋯ eingeklappt.

## Notizen, die deine Machine führt

Deine Machine erstellt auch selbst Notizen aus deinen Nachrichten und hält sie auf dem neuesten Stand. In jeder Zeile steht, woher sie stammt, zum Beispiel, wer die E-Mail geschickt hat. Tippe darauf, um die Nachricht zu öffnen. Bei einer Zeile aus **Was ich gelernt habe** steht **Aus meinen Erkenntnissen**. Ein Termin in deinem Kalender wird nie als eigene Zeile aufgeführt. Er bleibt im [Kalender](calendar.md).

**Zuhause**, **Gesundheit** und **Kinder** erscheinen erst, wenn deine Machine dort mindestens zwei konkrete Dinge festhalten kann, etwa eine Rechnung oder etwas, das sie gelernt hat. Bis dahin werden sie gar nicht in der Liste angezeigt. Wenn sie später wieder leer sind, verschwinden sie ebenfalls.

Deine Änderungen bleiben immer erhalten. Wenn du eine Notiz umbenennst, verschiebst, ihre Daten oder eine Zeile änderst, übernimmt deine Machine das beim Aktualisieren der Notiz. Wenn du eine Zeile oder Notiz löschst, kommt sie nicht wieder. Spätere Notizen zum selben Thema werden dort abgelegt, wo du die erste hingetan hast.

Mit **Zurück zum Original** werden wieder die eigenen Worte deiner Machine angezeigt. Wenn du eine Zeile bearbeitest, die deine Machine gelernt hat, ändert sie sich auch unter **Was ich gelernt habe**. So gibt es nur eine Version davon.

## Ausformulierte Seiten

Sobald eine Notiz mindestens zwei Zeilen aus deinen Nachrichten oder aus dem enthält, was deine Machine gelernt hat, schreibt sie oben auf der Seite eine Zusammenfassung. Dafür liest sie die Gespräche selbst und nicht nur deren Betreffzeilen:

- Eine kurze Zusammenfassung: worum es geht und wie der aktuelle Stand ist.
- **Wichtige Fakten**, **Entscheidungen**, **Offene Punkte** und ein **Verlauf**. Diese erscheinen nur, wenn es etwas Konkretes dazu gibt.
- Darunter stehen die Zeilen der Notiz nummeriert unter **Quellen**. Am Ende jedes Satzes stehen die Nummern der Zeilen, aus denen er stammt. Tippe auf eine Nummer, um zur entsprechenden Zeile zu gelangen.

Die Seite wird nur neu geschrieben, wenn sich die Zeilen der Notiz ändern, und höchstens ungefähr einmal am Tag. Wenn die Quellen nichts Konkretes hergeben, gibt es keine Seite, sondern nur die Zeilen. Entfernst du eine Zeile, verschwinden auch die Inhalte von der Seite, die nur aus dieser Zeile stammen. In der Notizenliste wird unter dem Namen jeder Notiz der Anfang der Zusammenfassung angezeigt.

Für Projekte und Organisationen gibt es bereits eine eigene Seite im Graph, mit einer Beschreibung oben. Gespräche dazu kommen auf diese Seite und nicht in eine Notiz.

## Notizen aus deinen Gesprächen

Deine Machine liest ganze Gespräche und ordnet jedes der passenden Notiz zu: E-Mail-Unterhaltungen aus allen deinen Postfächern, Chats in WhatsApp, Slack, Telegram, LinkedIn oder einer anderen verbundenen App sowie deine Besprechungsnotizen. Chat-Nachrichten zählen so lange als ein Gespräch, bis der Chat zwei Tage lang still ist.

- Ein Gespräch über ein Projekt oder eine Organisation im Graph kommt auf die entsprechende Seite und nicht in eine neue Notiz.
- Ein Gespräch kann in einen Bereich von **Zuhause**, **Gesundheit** oder **Kinder**, in eine deiner eigenen Notizen oder in eine Notiz kommen, die deine Machine unter **Arbeit**, **Auto**, **Steuern** oder einem anderen Ordner anlegt.
- Deine Machine erstellt eine neue Notiz nur für ein Thema mit mindestens zwei Gesprächen oder für ein Thema, zu dem du selbst etwas geschrieben hast und das eindeutig noch aktuell ist.
- Jede Zeile steht für ein Gespräch. Die neuesten stehen zuerst. Tippe auf eine Zeile, um das Gespräch zu öffnen.

Deine Machine sendet der KI einen kurzen Ausschnitt aus jedem Gespräch, ohne zitierte Antworten oder Signaturen. Jedes Gespräch wird nur einmal berücksichtigt. Neue Nachrichten darin werden anschließend ebenfalls berücksichtigt.

Massen-E-Mails und Chats kommen nie in eine Notiz und werden nie an die KI gesendet. Dazu zählen Spam, Werbung, Newsletter und andere Mailinglisten, Benachrichtigungen von No-Reply-Adressen, Bots und Broadcast-Kanäle. Gespräche, an denen du selbst beteiligt warst, zählen trotzdem dazu, ebenso Buchungs-E-Mails für **Reisen** und **Termine**.

Beim ersten Mal verarbeitet deine Machine die letzten drei Monate innerhalb einiger Stunden, nicht nachts und nur, wenn dein KI-Abo noch Kapazität hat. Danach sortiert sie neue Gespräche, sobald zehn davon warten oder eines seit einem halben Tag wartet.

## Reisen

Wenn eine Flug-, Hotel-, Zug-, Bus-, Fähr- oder Mietwagenbuchung in deinem Postfach eingeht, fügt deine Machine sie unter **Reisen** einer Reise hinzu. Buchungen für dieselbe Reise kommen auf eine Seite: die Hinfahrt, das Hotel und die Rückfahrt. Die Reise enthält für jede Zeile den Buchungscode, Sitzplatz und Fahrschein, nach Uhrzeit sortiert, und zeigt ihre Daten an. Im [Kalender](calendar.md) wird sie als ein Balken über diese Tage angezeigt. Tippe darauf, um die Reise zu öffnen.

Deine Machine liest die Buchungsdetails aus, die Fluggesellschaften, Hotels und Buchungsseiten in ihre Bestätigungs-E-Mails schreiben. Eine E-Mail ohne diese Angaben erstellt keine Reise. Buchungs-E-Mails von früher aus dem Jahr des [Verlaufs](history.md), den deine Machine speichert, werden im Hintergrund gelesen, sobald dieser Verlauf eingelesen ist. Dabei kommen zuerst deine privaten Postfächer an die Reihe. Wird eine ältere Bestätigung später gelesen, wird sie der bereits vorhandenen Reise hinzugefügt.

Bei einer geänderten Buchung wird die Zeile aktualisiert. Eine stornierte Buchung wird entfernt. Wenn alle Buchungen einer Reise storniert sind, wird auch die Reise entfernt.

## Termine

Wenn Tickets für ein Konzert, ein Spiel, ein Festival oder eine Konferenz in deinem Postfach eingehen, fügt deine Machine das Ereignis unter **Termine** hinzu. Für jedes Ereignis gibt es eine eigene Notiz. Eine Zeile enthält den Veranstaltungsort, den Buchungscode, den Sitzplatz und die Anzahl der Tickets. Eine zweite Bestellung für dasselbe Ereignis kommt auf dieselbe Notiz. Wie eine Reise zeigt das Ereignis seine Daten an und wird im [Kalender](calendar.md) als Balken angezeigt. Tippe darauf, um die Notiz zu öffnen.

- In jeder Zeile steht, von wem die Tickets stammen, zum Beispiel **Von Example Tickets**. Tippe darauf, um die E-Mail zu öffnen.
- Wenn aus der Ticket-E-Mail eine Aufgabe entstanden ist, etwa zum Bezahlen der Tickets, kannst du sie über **Aufgabe öffnen** anzeigen.
- Wurde ein Ereignis über dein Arbeits-Postfach gebucht, ist es Arbeit. Andernfalls ist es privat.

Deine Machine liest die Ticketdetails aus, die Ticketanbieter in ihre Bestätigungs-E-Mails schreiben, und verwendet dafür keine KI. Eine E-Mail ohne diese Angaben erstellt kein Ereignis. Eine stornierte Buchung wird entfernt. Wenn alle Tickets für ein Ereignis storniert sind, wird auch das Ereignis entfernt.

## Zuhause

Unter **Zuhause** hält deine Machine fest, was sie über dein Zuhause weiß: **Rechnungen und Abos**, **Geräte**, **Reparaturen und Instandhaltung** und **Das Haus**. Ein Bereich wird angezeigt, sobald er mindestens zwei Zeilen enthält.

- Für regelmäßig anfallende Rechnungen, zum Beispiel für Strom oder Wasser, gibt es eine Zeile mit der Häufigkeit und dem Datum der letzten Rechnung. Über **Aufgabe öffnen** kannst du die Rechnung selbst anzeigen. Betrag und Zahlungsdetails stehen dort.
- Für ein Abo, das du behalten hast, gibt es eine Zeile, über die du die zugehörige Aufgabe unter **Abos** öffnest. Gekündigte Abos werden nicht aufgeführt.
- Wer regelmäßig an dein Zuhause schreibt, zum Beispiel dein Energieversorger, Internetanbieter oder die Gemeinde, erhält eine Zeile mit der Häufigkeit. Tippe darauf, um die neueste E-Mail zu öffnen.
- Was deine Machine über dein Zuhause gelernt hat, zum Beispiel die Marke deiner Spülmaschine, wird ebenfalls als Zeile aufgeführt. Wenn du sie bearbeitest, ändert sie sich auch unter **Was ich gelernt habe**.
- Wenn du in einem Bereich eine eigene Notiz führst, zum Beispiel eine für deine Spülmaschine unter **Geräte**, kommen Inhalte zu diesem Gerät in deine Notiz. Deine Machine erstellt solche Notizen nicht selbst.

Es werden nur private Rechnungen, Abos und E-Mails verwendet. Notizen unter Zuhause sind immer privat. Deine Machine fragt ihre KI einmal zu jeder neuen Rechnung, jedem Abo und jeder neu gelernten Information, ob sie dein Zuhause betrifft. Bei einer Rechnung wird nur mitgeteilt, von wem sie stammt, nie der Betrag.

Wie oben unter **Notizen aus deinen Gesprächen** beschrieben, kommen auch deine Gespräche in diese Notizen.

## Gesundheit

Unter **Gesundheit** hält deine Machine fest, was sie über deine eigene Gesundheit weiß: **Termine**, **Testergebnisse**, **Ärzte und Pflege**, **Medikamente**, **Allergien und Erkrankungen** sowie **Rechnungen und Versicherung**. Ein Bereich wird angezeigt, sobald er mindestens zwei Zeilen enthält.

- Für eine Rechnung von einem Arzt, Zahnarzt oder einer Apotheke gibt es eine Zeile, über die du die zugehörige Aufgabe öffnest. Der Betrag steht dort.
- Jede E-Mail von deiner Arztpraxis, einem Krankenhaus, Labor oder deiner Krankenversicherung wird als datierte Zeile mit Betreff aufgeführt. So entsteht mit der Zeit deine Krankengeschichte. Tippe darauf, um die E-Mail zu öffnen.
- Was deine Machine über deine Gesundheit gelernt hat, zum Beispiel eine Allergie, wird ebenfalls als Zeile aufgeführt. Wenn du sie bearbeitest, ändert sie sich auch unter **Was ich gelernt habe**.
- In deine eigene Notiz in einem Bereich, zum Beispiel eine für deine Physiotherapie unter **Termine**, kommen Inhalte zu diesem Thema.

Notizen unter Gesundheit sind immer privat, auch wenn eine Rechnung an deine Arbeitsadresse geschickt wurde. Deine Machine fragt ihre KI einmal zu jeder neuen Rechnung und jeder neu gelernten Information, ob sie deine eigene Gesundheit betrifft.

## Kinder

Unter **Kinder** hält deine Machine fest, was sie über deine Kinder weiß: **Schule**, **Aktivitäten**, **Kinderbetreuung**, **Ärzte und Pflege** sowie **Rechnungen und Gebühren**. Babysitter und Kindertagesstätten gehören zu Kinderbetreuung und nie zu Ärzte und Pflege. Ein Bereich wird angezeigt, sobald er mindestens zwei Zeilen enthält.

- Was deine Machine über dein Kind gelernt hat, zum Beispiel den Namen der Klassenlehrerin oder den Schwimmtag, wird als Zeile aufgeführt und mit der Seite des Kindes verknüpft. Jemand gilt als dein Kind, wenn unter **Für dich** zum Beispiel Tochter oder Sohn steht.
- Für eine Rechnung von einer Schule, einem Verein oder einer Kinderbetreuung gibt es eine Zeile, über die du die zugehörige Aufgabe öffnest. Der Betrag steht dort.
- Jede E-Mail von der Schule, einem Verein oder einer Kinderbetreuung, zum Beispiel mit Informationen zu einem Ausflug oder einer Planänderung, wird als datierte Zeile mit Betreff aufgeführt. So findest du alles, was sie schicken, an einem Ort. Tippe darauf, um die E-Mail zu öffnen.
- In deine eigene Notiz für ein Kind in einem Bereich, zum Beispiel eine für Isla unter **Schule**, kommen Inhalte zu diesem Kind.

Notizen unter Kinder sind immer privat, auch wenn die Schule an deine Arbeitsadresse schreibt. Deine Machine fragt ihre KI einmal zu jeder neuen Information, ob sie deine Kinder betrifft.

## Zusammenführen, löschen und rückgängig machen

Über **Zusammenführen mit …** im Menü ⋯ werden die Zeilen einer Notiz und die darunterliegenden Notizen in eine andere Notiz verschoben. Von da an fügt deine Machine neue Inhalte dieser Notiz hinzu. Mit **Löschen** entfernst du eine Notiz. In beiden Fällen wird kurz **Rückgängig** angezeigt. Das gilt auch, wenn du eine Zeile entfernst.

## Nicht dasselbe wie Besprechungsnotizen

Besprechungsnotizen und Notizen zu Personen oder Organisationen bleiben dort, wo sie waren. Die Notizen hier sind eigenständige Seiten.
