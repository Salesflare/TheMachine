---
title: Notizen
area: graph
summary: Eine übersichtliche Seite pro Thema, etwa eine Reise oder dein Zuhause, verknüpft mit den Personen und Projekten, um die es geht.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, topic_notes.py, note_writer.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: a71c5e46042cddd0
---
Eine Notiz ist die Übersicht zu einem Thema: einer Reise, deinem Zuhause oder dazu, wie Rechnungen bezahlt werden. Notizen stehen im Graph neben Personen, Organisationen und Projekten. Sie bleiben auf deiner Machine und werden nicht mit deinem Team geteilt.

## Eine Notiz beginnen

Oben in den Notizen findest du **Neue Notiz**. Gib einen Titel ein und wähle **Notiz beginnen**. Die Seite wird geöffnet. Mit **Zeile hinzufügen** fügst du hinzu, was du behalten möchtest. Jede Textzeile wird zu einer eigenen Zeile.

## Personen, Projekte und andere Notizen verknüpfen

Gib in einer Zeile @ und die ersten Buchstaben eines Namens ein. Wähle eine Person, Organisation, ein Projekt oder eine Notiz aus der Liste. Der Name wird als Link eingefügt. Auf der Seite des verknüpften Eintrags erscheint unter **Verlinkt von** deine Notiz.

## Notizen unter anderen Notizen

Eine Notiz kann unter einer anderen liegen, zum Beispiel Geräte unter Zuhause. Die Notizen werden als Baum angezeigt: Mit dem Pfeil neben einer Notiz öffnest du die darunterliegenden Notizen. Um eine Notiz zu verschieben, wähle **Bearbeiten** und unter **Unter** aus, wo sie liegen soll. Mit **Neue Notiz unter dieser** im Menü ⋯ erstellst du direkt dort eine Notiz.

Oben auf der Seite einer Notiz siehst du, wo sie liegt, zum Beispiel **Notizen › Kinder**. Tippe auf einen beliebigen Teil, um dorthin zu gehen. Auf dem Smartphone werden die Notizen dazwischen unter ⋯ eingeklappt.

## Notizen, die deine Machine erstellt

Deine Machine schreibt auch selbst Notizen aus deinen Nachrichten und hält sie aktuell. Bei jeder Zeile steht, woher sie stammt, zum Beispiel, wer die E-Mail gesendet hat. Tippe darauf, um die Nachricht zu öffnen. Bei einer Zeile aus **Was ich gelernt habe** steht **Aus meinen Erkenntnissen**.

Ein Termin oder eine Verabredung in deinem Kalender wird nie als eigene Zeile aufgeführt: Er bleibt in [Kalender](calendar.md). Dasselbe gilt für die zugehörige E-Mail: die Einladung, Antworten darauf, Änderungen und Absagen.

**Zuhause**, **Gesundheit** und **Kinder** werden erst angezeigt, wenn deine Machine dort mindestens zwei konkrete Einträge hat, etwa eine Rechnung oder etwas, das sie gelernt hat. Bis dahin erscheinen sie gar nicht in der Liste. Wenn sie später wieder leer sind, verschwinden sie.

Deine Änderungen bleiben immer bestehen. Benenne eine Notiz um, verschiebe sie, ändere ihre Daten oder eine Zeile, und deine Machine behält diese Änderungen bei, wenn sie die Notiz aktualisiert. Löschst du eine Zeile oder eine Notiz, kommt sie nicht wieder. Spätere Notizen zum selben Thema werden dort abgelegt, wo du die erste hingetan hast.

Mit **Zurück zum Original** werden wieder die ursprünglichen Worte deiner Machine angezeigt. Wenn du eine Zeile bearbeitest, die aus dem stammt, was deine Machine gelernt hat, wird sie auch unter **Was ich gelernt habe** geändert. So gibt es nur eine Version davon.

## Ausformulierte Seiten

Sobald eine Notiz mindestens zwei Zeilen aus deinen Nachrichten oder aus dem enthält, was deine Machine gelernt hat, schreibt deine Machine oben auf der Seite einen Text. Dafür liest sie die Gespräche selbst, nicht nur ihre Betreffzeilen:

- Eine kurze Zusammenfassung: worum es geht und was der aktuelle Stand ist.
- **Wichtige Fakten**, **Entscheidungen**, **Offene Punkte** und ein **Verlauf**, jeweils nur, wenn es etwas Konkretes dazu gibt.
- Darunter stehen die Zeilen der Notiz nummeriert unter **Quellen**. Am Ende jedes Satzes stehen die Nummern der Zeilen, aus denen er stammt. Tippe auf eine Nummer, um zu dieser Zeile zu gelangen.

Der Text wird nur neu geschrieben, wenn sich die Zeilen der Notiz ändern, höchstens etwa einmal am Tag. Wenn die Quellen nichts Konkretes hergeben, gibt es keinen Text, sondern nur die Zeilen. Löschst du eine Zeile, verschwindet auch alles aus dem Text, was nur aus dieser Zeile stammt. In der Notizenliste wird unter dem Namen jeder Notiz der Anfang der Zusammenfassung angezeigt.

Ein Projekt oder eine Organisation hat bereits eine eigene Seite im Graph, mit einer Beschreibung ganz oben. Gespräche darüber kommen auf diese Seite, nicht in eine Notiz.

## Notizen aus deinen Gesprächen

Deine Machine liest ganze Gespräche und ordnet jedes der passenden Notiz zu: E-Mail-Verläufe aus deinen Postfächern, Chats in WhatsApp, Slack, Telegram, LinkedIn oder einer anderen verbundenen App sowie deine Besprechungsnotizen. Chat-Nachrichten gelten als ein Gespräch, bis der Chat zwei Tage lang ruht.

- Ein Gespräch über ein Projekt oder eine Organisation im Graph kommt auf deren Seite, nicht in eine neue Notiz.
- Ein Gespräch kann in einen Bereich von **Zuhause**, **Gesundheit** oder **Kinder**, in eine eigene Notiz oder in eine Notiz kommen, die deine Machine unter **Arbeit**, **Auto**, **Steuern** oder einem anderen Ordner erstellt.
- Deine Machine erstellt eine neue Notiz nur für ein Thema mit mindestens zwei Gesprächen oder für ein Thema, zu dem du selbst etwas geschrieben hast und bei dem klar ist, dass es weitergeht.
- Jede Zeile steht für ein Gespräch. Die neuesten stehen oben. Tippe auf eine Zeile, um das Gespräch zu öffnen.

An die KI wird ein kurzer Teil jedes Gesprächs gesendet, ohne zitierte Antworten oder Signaturen. Jedes Gespräch wird einmal geprüft. Neue Nachrichten darin werden anschließend ebenfalls berücksichtigt.

Massen-E-Mails und Chats landen nie in einer Notiz und werden nie an die KI gesendet: Spam, Werbung, Newsletter und andere Verteiler-E-Mails, Benachrichtigungen von No-Reply-Adressen, Bots und Broadcast-Kanäle. Ein Gespräch, an dem du selbst beteiligt warst, zählt trotzdem. Das gilt auch für Buchungs-E-Mails unter **Reisen** und **Termine**.

Beim ersten Mal werden die vergangenen drei Monate innerhalb einiger Stunden verarbeitet, nicht nachts und nur, wenn dein KI-Tarif noch Kapazität hat. Danach werden neue Gespräche sortiert, sobald zehn darauf warten oder eines seit einem halben Tag wartet.

## Reisen

Wenn eine Flug-, Hotel-, Zug-, Bus-, Fähr- oder Mietwagenbuchung in deinem Postfach eingeht, fügt deine Machine sie einer Reise unter **Reisen** hinzu. Buchungen für dieselbe Reise kommen in eine Notiz: die Hinfahrt, das Hotel und die Rückfahrt. Für jede Zeile enthält die Reise Buchungscode, Sitzplatz und Ticket, nach Zeit geordnet, und zeigt ihre Reisedaten. In [Kalender](calendar.md) erscheint sie als ein Balken über diese Tage. Tippe darauf, um die Reise zu öffnen.

Deine Machine liest die Buchungsdetails, die Fluggesellschaften, Hotels und Buchungsseiten in ihre Bestätigungs-E-Mails aufnehmen. Eine E-Mail ohne diese Angaben führt nicht zu einer Reise. Buchungs-E-Mails aus dem Zeitraum der [Verlauf](history.md)-Daten, die deine Machine speichert, werden im Hintergrund gelesen, sobald dieser Verlauf verfügbar ist. Zuerst werden deine privaten Postfächer verarbeitet. Wird eine ältere Bestätigung später gelesen, wird sie der bereits vorhandenen Reise hinzugefügt.

Änderungen an einer Buchung aktualisieren die entsprechende Zeile. Eine stornierte Buchung wird entfernt. Wenn alle Buchungen einer Reise storniert sind, wird auch die Reise entfernt.

## Termine

Wenn Tickets für ein Konzert, ein Spiel, ein Festival oder eine Konferenz in deinem Postfach eingehen, fügt deine Machine den Termin unter **Termine** hinzu. Für jeden Termin gibt es eine eigene Notiz. In einer Zeile stehen der Veranstaltungsort, der Buchungscode, der Sitzplatz und die Anzahl der Tickets. Eine zweite Bestellung für denselben Termin kommt in dieselbe Notiz. Wie bei einer Reise werden die Daten angezeigt. In [Kalender](calendar.md) erscheint der Termin als Balken. Tippe darauf, um die Notiz zu öffnen.

- In jeder Zeile steht, von wem die Tickets stammen, zum Beispiel **Von Example Tickets**. Tippe darauf, um die E-Mail zu öffnen.
- Wenn aus der Ticket-E-Mail eine Aufgabe erstellt wurde, zum Beispiel zum Bezahlen der Tickets, wird sie über **Aufgabe öffnen** angezeigt.
- Ein Termin, der über dein geschäftliches Postfach gebucht wurde, ist Arbeit. Andernfalls ist er privat.

Deine Machine liest die Ticketdetails ohne KI aus den Bestätigungs-E-Mails der Ticketanbieter. Eine E-Mail ohne diese Angaben führt nicht zu einem Termin. Eine stornierte Buchung wird entfernt. Wenn alle Tickets für einen Termin storniert sind, wird auch der Termin entfernt.

## Zuhause

Unter **Zuhause** speichert deine Machine, was sie über dein Zuhause weiß: **Rechnungen und Abos**, **Geräte**, **Reparaturen und Instandhaltung** und **Das Haus**. Ein Bereich wird angezeigt, sobald er mindestens zwei Zeilen enthält.

- Für eine regelmäßig anfallende Rechnung, etwa für Strom oder Wasser, wird eine Zeile mit der Häufigkeit und dem Datum der letzten Rechnung erstellt. Über **Aufgabe öffnen** wird die Rechnung selbst angezeigt. Betrag und Zahlungsdetails bleiben dort.
- Für ein Abo, das du behalten hast, wird eine Zeile erstellt, über die du die entsprechende **Abo**-Aufgabe öffnest. Gekündigte Abos werden nicht aufgeführt.
- Wer dir regelmäßig wegen deines Zuhauses schreibt, etwa dein Energieversorger, Internetanbieter oder die Gemeinde, erhält eine Zeile mit der Häufigkeit. Tippe darauf, um die neueste E-Mail zu öffnen.
- Was deine Machine über dein Zuhause gelernt hat, zum Beispiel die Marke deiner Spülmaschine, erscheint ebenfalls als Zeile. Wenn du sie bearbeitest, ändert sie sich auch unter **Was ich gelernt habe**.
- Wenn du in einem Bereich eine eigene Notiz führst, zum Beispiel eine für deine Spülmaschine unter **Geräte**, kommt alles zu diesem Gerät in deine Notiz. Deine Machine erstellt solche Notizen nicht selbst.

Verwendet werden nur private Rechnungen, Abos und E-Mails. Notizen unter Zuhause sind immer privat. Deine Machine fragt ihre KI einmal zu jeder neuen Rechnung, jedem neuen Abo und jedem neuen Eintrag, den sie gelernt hat, ob er dein Zuhause betrifft. Bei einer Rechnung sendet sie, von wem sie stammt, aber nie den Betrag.

Deine Gespräche kommen ebenfalls in diese Notizen, wie oben unter **Notizen aus deinen Gesprächen** beschrieben.

## Gesundheit

Unter **Gesundheit** speichert deine Machine, was sie über deine Gesundheit weiß: **Termine**, **Testergebnisse**, **Ärzte und Pflege**, **Medikamente**, **Allergien und Erkrankungen** sowie **Rechnungen und Versicherung**. Ein Bereich wird angezeigt, sobald er mindestens zwei Zeilen enthält.

- Für eine Rechnung von einer Arztpraxis, Zahnarztpraxis oder Apotheke wird eine Zeile erstellt, über die du die entsprechende Aufgabe öffnest. Der Betrag bleibt dort.
- Jede E-Mail aus deiner Praxis, von einem Krankenhaus, einem Labor oder deiner Krankenversicherung wird mit Datum und Betreff als Zeile aufgeführt. So entsteht mit der Zeit dein Verlauf. Tippe auf eine Zeile, um die E-Mail zu öffnen.
- Was deine Machine über deine Gesundheit gelernt hat, zum Beispiel eine Allergie, erscheint ebenfalls als Zeile. Wenn du sie bearbeitest, ändert sie sich auch unter **Was ich gelernt habe**.
- Deine eigene Notiz in einem Bereich, zum Beispiel eine für deine Physiotherapie unter **Termine**, enthält alles, was dazu gehört.

Notizen unter Gesundheit sind immer privat, auch wenn eine Rechnung an deine geschäftliche Adresse gesendet wurde. Deine Machine fragt ihre KI einmal zu jeder neuen Rechnung und jedem neuen Eintrag, den sie gelernt hat, ob er deine Gesundheit betrifft.

## Kinder

Unter **Kinder** speichert deine Machine, was sie über deine Kinder weiß: **Schule**, **Aktivitäten**, **Kinderbetreuung**, **Ärzte und Pflege** sowie **Rechnungen und Gebühren**. Ein Babysitter oder eine Tagesbetreuung wird unter Kinderbetreuung abgelegt, nie unter Ärzte und Pflege. Ein Bereich wird angezeigt, sobald er mindestens zwei Zeilen enthält.

- Was deine Machine über dein Kind gelernt hat, zum Beispiel den Namen der Klassenlehrkraft oder den Schwimmtag, erscheint als Zeile mit einem Link zur Seite deines Kindes. Als dein Kind wird eine Person erfasst, wenn unter **Für dich** zum Beispiel Tochter oder Sohn steht.
- Für eine Rechnung von der Schule, einem Verein oder der Kinderbetreuung wird eine Zeile erstellt, über die du die entsprechende Aufgabe öffnest. Der Betrag bleibt dort.
- Jede E-Mail von der Schule, einem Verein oder der Kinderbetreuung, zum Beispiel eine Nachricht über einen Ausflug oder eine Planänderung, wird mit Datum und Betreff als Zeile aufgeführt. So ist alles, was sie senden, an einem Ort. Tippe auf eine Zeile, um die E-Mail zu öffnen.
- Deine eigene Notiz für ein Kind in einem Bereich, zum Beispiel eine für Isla unter **Schule**, enthält alles, was dieses Kind betrifft.

Notizen unter Kinder sind immer privat, auch wenn die Schule an deine geschäftliche Adresse schreibt. Deine Machine fragt ihre KI einmal zu jedem neuen Eintrag, ob er deine Kinder betrifft.

## Zusammenführen, Löschen und Rückgängigmachen

Mit **Zusammenführen mit …** im Menü ⋯ verschiebst du die Zeilen einer Notiz und die darunterliegenden Notizen in eine andere Notiz. Von da an fügt deine Machine neue Einträge zu dieser Notiz hinzu. Mit **Löschen** entfernst du eine Notiz. Bei beiden Aktionen und auch beim Entfernen einer Zeile wird kurz **Rückgängig** angezeigt.

## Nicht dasselbe wie Besprechungsnotizen

Besprechungsnotizen und Notizen zu Personen oder Organisationen bleiben dort, wo sie waren. Die Notizen hier sind eigenständige Seiten.
