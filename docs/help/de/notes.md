---
title: Notizen
area: graph
summary: Eine übersichtliche Seite pro Thema, etwa für eine Reise oder dein Zuhause, verknüpft mit den Personen und Projekten, die dazugehören.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, topic_notes.py, note_writer.py, folder_overview.py, memory_seed.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: 1087ac0970878932
---
Eine Notiz gibt dir einen Überblick über ein Thema: eine Reise, dein Zuhause oder die Abwicklung von Rechnungen. Notizen stehen im Graph neben Personen, Organisationen und Projekten. Sie bleiben auf deiner Machine und werden nicht mit deinem Team geteilt.

## Eine Notiz beginnen

Wähle oben in den Notizen **Neue Notiz**. Gib einen Titel ein und wähle **Notiz beginnen**, um die Seite zu öffnen. Mit **Zeile hinzufügen** fügst du hinzu, was du festhalten möchtest. Jede Texteingabe wird zu einer eigenen Zeile.

## Mit Personen, Projekten und anderen Notizen verknüpfen

Gib in einer Zeile @ und ein paar Buchstaben eines Namens ein. Wähle eine Person, Organisation, ein Projekt oder eine Notiz aus der Liste. Der Name wird als Link eingefügt. Auf der Seite des verknüpften Eintrags erscheint unter **Verlinkt von** deine Notiz.

## Notizen unter anderen Notizen

Eine Notiz kann einer anderen untergeordnet sein, zum Beispiel „Geräte“ unter „Zuhause“. In den Notizen werden sie als Baum angezeigt: Mit dem Pfeil neben einer Notiz öffnest du die darunterliegenden Notizen. Um eine Notiz zu verschieben, wähle **Bearbeiten** und dann unter **Unter** aus, wo sie hingehört. Mit **Neue Notiz unter dieser** im ⋯-Menü legst du direkt dort eine Notiz an.

Oben auf einer Notizseite siehst du, wo sie eingeordnet ist, zum Beispiel **Notizen › Kinder**. Tippe auf einen beliebigen Teil, um dorthin zu wechseln. Auf dem Smartphone werden Notizen dazwischen im ⋯-Menü zusammengefasst.

## Notizen, die deine Machine anlegt

Deine Machine schreibt auch selbst Notizen aus deinen Nachrichten und hält sie aktuell. Bei jeder Zeile steht, woher sie stammt, zum Beispiel, wer die E-Mail geschickt hat. Tippe darauf, um die Nachricht zu öffnen. Bei einer Zeile aus **Was ich gelernt habe** steht **Aus meinen Erkenntnissen**.

Ein Termin oder eine Besprechung in deinem Kalender erscheint nie als eigene Zeile. Sie bleiben im [Kalender](calendar.md). Das gilt auch für die dazugehörigen E-Mails: die Einladung, Antworten, Änderungen und Absagen.

**Zuhause**, **Gesundheit** und **Kinder** werden erst angezeigt, wenn deine Machine dort mindestens zwei konkrete Einträge hat, etwa eine Rechnung oder etwas, das sie gelernt hat. Bis dahin werden sie gar nicht in der Liste angezeigt. Wenn sie später wieder leer sind, verschwinden sie.

Deine Änderungen bleiben immer bestehen. Benennst du eine Notiz um, verschiebst du sie, änderst du ihre Daten oder eine Zeile, behält deine Machine die Änderungen bei, wenn sie die Notiz aktualisiert. Löschst du eine Zeile oder eine Notiz, kommt sie nicht wieder. Spätere Notizen zum selben Thema werden dort abgelegt, wo du die erste eingeordnet hast.

Mit **Zurück zum Original** werden wieder die eigenen Worte deiner Machine angezeigt. Wenn du eine Zeile bearbeitest, die aus den Erkenntnissen deiner Machine stammt, ändert sie sich auch unter **Was ich gelernt habe**. So gibt es nur eine Version davon.

## Ausformulierte Seiten

Sobald eine Notiz mindestens zwei Zeilen aus deinen Nachrichten oder aus den Erkenntnissen deiner Machine enthält, schreibt deine Machine oben auf der Seite eine Zusammenfassung. Dabei liest sie die Gespräche selbst, nicht nur ihre Betreffzeilen:

- Eine kurze Zusammenfassung: worum es geht und wie der Stand ist.
- **Wichtige Fakten**, **Entscheidungen**, **Offene Punkte** und ein **Verlauf**. Jeder Abschnitt erscheint nur, wenn es etwas Konkretes dazu gibt.
- Darunter folgen die Zeilen der Notiz, nummeriert unter **Quellen**. Jeder Satz endet mit den Nummern der Zeilen, aus denen er stammt. Tippe auf eine Nummer, um zur jeweiligen Zeile zu springen.

Die Seite wird nur neu geschrieben, wenn sich die Zeilen der Notiz ändern, höchstens etwa einmal am Tag. Wenn die Quellen nichts Konkretes hergeben, gibt es keine Seite, sondern nur die Zeilen. Löschst du eine Zeile, verschwindet auch alles von der Seite, was nur aus dieser Zeile stammt. In der Notizenliste wird unter dem Namen der Notiz der Anfang der Zusammenfassung angezeigt.

Projekte und Organisationen haben im Graph bereits eine eigene Seite mit einer Beschreibung oben. Gespräche dazu werden dort abgelegt, nicht in einer Notiz.

## Übersichten

Bei einer Notiz mit untergeordneten Notizen, zum Beispiel **Arbeit** oder **Zuhause**, erscheint oben eine kurze Übersicht, sobald mindestens zwei davon Neuigkeiten enthalten. Sie besteht aus ein oder zwei Sätzen dazu, was gerade los ist, und einigen Dingen, die sich kürzlich verändert haben oder als Nächstes anstehen. Am Ende jedes Eintrags stehen die Namen der Notizen, aus denen er stammt. Tippe auf einen Namen, um die Notiz zu öffnen.

Die Übersicht wird aus den Seiten und den neuesten Zeilen der untergeordneten Notizen erstellt, höchstens einmal am Tag und nur, wenn sich etwas geändert hat. Wenn es nichts Aktuelles gibt, wird keine Übersicht angezeigt. In der Notizenliste erscheint der Anfang der Übersicht unter dem Ordnernamen.

## Notizen aus deinen Gesprächen

Deine Machine liest ganze Gespräche und ordnet jedes der passenden Notiz zu: einen E-Mail-Verlauf aus einem deiner Postfächer, einen Chat in WhatsApp, Slack, Telegram, LinkedIn oder einer anderen verbundenen App sowie deine Besprechungsnotizen. Chat-Nachrichten zählen so lange als ein Gespräch, bis der Chat zwei Tage lang ruhig bleibt.

- Ein Gespräch über ein Projekt oder eine Organisation in deinem Graph wird auf deren Seite abgelegt, nicht in einer neuen Notiz.
- Ein Gespräch kann in einem Bereich von **Zuhause**, **Gesundheit** oder **Kinder**, in einer deiner eigenen Notizen oder in einer Notiz landen, die deine Machine unter **Arbeit**, **Auto**, **Steuern** oder einem anderen Ordner anlegt.
- Deine Machine legt nur dann eine neue Notiz an, wenn es zu einem Thema mindestens zwei Gespräche gibt oder du selbst dazu geschrieben hast und das Thema eindeutig noch aktuell ist.
- Jede Zeile steht für ein Gespräch, die neuesten zuerst. Tippe darauf, um das Gespräch zu öffnen.

An die KI wird jeweils ein kurzer Ausschnitt aus jedem Gespräch gesendet, ohne zitierte Antworten oder Signaturen. Jedes Gespräch wird einmal berücksichtigt. Neue Nachrichten darin werden anschließend ebenfalls einbezogen.

Massen-E-Mails und Chats werden nie in einer Notiz abgelegt und nie an die KI gesendet: Spam, Werbung, Newsletter und andere Listen-E-Mails, Benachrichtigungen von Adressen ohne Antwortfunktion, Bots und Broadcast-Kanäle. Gespräche, an denen du selbst beteiligt warst, zählen trotzdem. Das gilt auch für Buchungs-E-Mails unter **Reisen** und **Termine**.

Beim ersten Mal verarbeitet deine Machine die vergangenen drei Monate innerhalb weniger Stunden, nicht über Nacht und nur, wenn in deinem KI-Tarif noch Kapazität verfügbar ist. Danach ordnet sie neue Gespräche ein, sobald zehn darauf warten oder eines davon einen halben Tag gewartet hat.

## Notizen aus dem OpenClaw-Speicher

Wenn du OpenClaw zuvor verwendet hast, liest deine Machine einmal die Themenseiten in dessen Speicherordner, zum Beispiel eine Seite über eine Reise oder deine Gesundheit. Wichtige Informationen kommen in die Notiz zum jeweiligen Thema oder in eine neue Notiz. In jeder Zeile steht, von welcher Seite sie stammt, zum Beispiel **Aus deinen Speicherseiten · Lissabon**, zusammen mit dem Datum. Bewege den Mauszeiger darüber, um zu sehen, von welcher Seite die Information kommt.

Deine Machine ändert diese Seiten nie. Tagesprotokolle, Seiten über die Assistentin selbst und als sensibel oder privat markierte Ordner überspringt sie. Sie liest höchstens 80 Seiten, einige auf einmal, und greift danach nie wieder darauf zu.

## Reisen

Wenn eine Flug-, Hotel-, Zug-, Bus-, Fähr- oder Mietwagenbuchung in deinem Postfach eingeht, fügt deine Machine sie unter **Reisen** zu einer Reise hinzu. Buchungen für dieselbe Reise kommen in eine Notiz: die Hinfahrt, das Hotel und die Rückfahrt. Für jede Zeile enthält die Reise den Buchungscode, Sitzplatz und das Ticket, in chronologischer Reihenfolge. Außerdem zeigt sie die Reisedaten an. Im [Kalender](calendar.md) erscheint sie als Balken über diese Tage. Tippe darauf, um die Reise zu öffnen.

Deine Machine liest die Buchungsdetails aus den Bestätigungs-E-Mails von Fluggesellschaften, Hotels und Buchungsseiten. Eine E-Mail ohne diese Angaben erstellt keine Reise. Buchungs-E-Mails aus der Vergangenheit, die in das Jahr der von deiner Machine gespeicherten [Verläufe](history.md) fallen, werden im Hintergrund gelesen, sobald dieser Verlauf verfügbar ist. Zuerst werden deine privaten Postfächer berücksichtigt. Wird eine ältere Bestätigung später gelesen, ergänzt sie die bereits vorhandene Reise.

Änderungen an einer Buchung aktualisieren die entsprechende Zeile. Eine stornierte Buchung wird entfernt. Wenn alle Buchungen einer Reise storniert sind, wird auch die Reise entfernt.

## Termine

Wenn Tickets für ein Konzert, ein Spiel, ein Festival oder eine Konferenz in deinem Postfach eingehen, legt deine Machine unter **Termine** einen Eintrag für die Veranstaltung an. Jede Veranstaltung bekommt eine eigene Notiz. Eine Zeile enthält den Veranstaltungsort, den Buchungscode, den Sitzplatz und die Anzahl der Tickets. Eine weitere Bestellung für dieselbe Veranstaltung kommt in dieselbe Notiz. Wie eine Reise zeigt die Veranstaltung ihre Daten und erscheint im [Kalender](calendar.md) als Balken. Tippe darauf, um die Notiz zu öffnen.

- Bei jeder Zeile steht, von wem die Tickets stammen, zum Beispiel **Von Example Tickets**. Tippe darauf, um die E-Mail zu öffnen.
- Wenn aus der Ticket-E-Mail eine Aufgabe entstanden ist, etwa die Tickets zu bezahlen, wird sie mit **Aufgabe öffnen** angezeigt.
- Eine Veranstaltung, die über dein geschäftliches Postfach gebucht wurde, ist Arbeit. Andernfalls ist sie privat.

Deine Machine liest die Ticketdetails aus den Bestätigungs-E-Mails der Ticketverkäufer, ohne KI. Eine E-Mail ohne diese Angaben erstellt keine Veranstaltung. Eine stornierte Buchung wird entfernt. Wenn alle Tickets für eine Veranstaltung storniert sind, wird auch die Veranstaltung entfernt.

## Zuhause

Unter **Zuhause** hält deine Machine fest, was sie über dein Zuhause weiß: **Rechnungen und Abos**, **Geräte**, **Reparaturen und Instandhaltung** sowie **Das Haus**. Ein Bereich wird angezeigt, sobald er mindestens zwei Zeilen enthält.

- Für regelmäßig anfallende Rechnungen, etwa für Strom oder Wasser, wird eine Zeile mit der Häufigkeit und dem Datum der letzten Rechnung angelegt. Mit **Aufgabe öffnen** rufst du die Rechnung selbst auf. Betrag und Zahlungsdetails stehen dort.
- Für ein aktives Abo wird eine Zeile angelegt, die die Aufgabe für **Abos** öffnet. Gekündigte Abos werden nicht aufgeführt.
- Wer regelmäßig wegen deines Zuhauses schreibt, etwa dein Energieversorger, Internetanbieter oder die Stadt, wird mit einer Zeile aufgeführt, die angibt, wie oft die Person oder Stelle schreibt. Tippe darauf, um die neueste E-Mail zu öffnen.
- Auch Erkenntnisse deiner Machine über dein Zuhause, zum Beispiel die Marke deiner Spülmaschine, werden als Zeile aufgeführt. Wenn du sie bearbeitest, ändert sie sich auch unter **Was ich gelernt habe**.
- Wenn du in einem Bereich eine eigene Notiz führst, zum Beispiel eine für deine Spülmaschine unter **Geräte**, kommen Informationen dazu in diese Notiz. Deine Machine legt solche Notizen nicht selbst an.

Es werden nur private Rechnungen, Abos und E-Mails verwendet. Notizen unter „Zuhause“ sind immer privat. Deine Machine fragt ihre KI einmal zu jeder neuen Rechnung, jedem Abo und jeder neuen Erkenntnis, ob sie dein Zuhause betreffen. Bei einer Rechnung teilt sie mit, von wem sie stammt, aber nie den Betrag.

Wie oben unter **Notizen aus deinen Gesprächen** beschrieben, kommen auch deine Gespräche in diese Notizen.

## Gesundheit

Unter **Gesundheit** hält deine Machine fest, was sie über deine Gesundheit weiß: **Termine**, **Testergebnisse**, **Ärzte und Pflege**, **Medikamente**, **Allergien und Erkrankungen** sowie **Rechnungen und Versicherung**. Ein Bereich wird angezeigt, sobald er mindestens zwei Zeilen enthält.

- Für eine Rechnung von einer Arztpraxis, Zahnarztpraxis oder Apotheke wird eine Zeile angelegt, über die du die Aufgabe öffnen kannst. Der Betrag steht dort.
- Jede E-Mail von deiner Praxis, einem Krankenhaus, einem Labor oder deiner Krankenversicherung wird mit Datum und Betreff als Zeile aufgeführt. So entsteht mit der Zeit eine Übersicht über deinen Verlauf. Tippe darauf, um die E-Mail zu öffnen.
- Auch Erkenntnisse deiner Machine über deine Gesundheit, zum Beispiel eine Allergie, werden als Zeile aufgeführt. Wenn du sie bearbeitest, ändert sie sich auch unter **Was ich gelernt habe**.
- Eigene Notizen in einem Bereich, zum Beispiel eine für deine Physiotherapie unter **Termine**, enthalten die passenden Informationen.

Notizen unter „Gesundheit“ sind immer privat, auch wenn eine Rechnung an deine geschäftliche Adresse geschickt wurde. Deine Machine fragt ihre KI einmal zu jeder neuen Rechnung und jeder neuen Erkenntnis, ob sie deine Gesundheit betrifft.

## Kinder

Unter **Kinder** hält deine Machine fest, was sie über deine Kinder weiß: **Schule**, **Aktivitäten**, **Kinderbetreuung**, **Ärzte und Pflege** sowie **Rechnungen und Gebühren**. Babysitter und Tagesbetreuung werden unter Kinderbetreuung abgelegt, nie unter Ärzte und Pflege. Ein Bereich wird angezeigt, sobald er mindestens zwei Zeilen enthält.

- Erkenntnisse deiner Machine über dein Kind, zum Beispiel den Namen der Klassenlehrerin oder den Schwimmtag, werden als Zeile aufgeführt und mit der Seite deines Kindes verknüpft. Jemand gilt als dein Kind, wenn unter **Für dich** steht, dass es sich um dein Kind handelt, zum Beispiel Tochter oder Sohn.
- Für eine Rechnung von der Schule, einem Verein oder einer Betreuung wird eine Zeile angelegt, über die du die Aufgabe öffnen kannst. Der Betrag steht dort.
- Jede E-Mail von der Schule, einem Verein oder einer Betreuung, zum Beispiel über einen Ausflug oder eine Planänderung, wird mit Datum und Betreff als Zeile aufgeführt. So ist alles, was sie schicken, an einem Ort. Tippe darauf, um die E-Mail zu öffnen.
- Eine eigene Notiz für ein Kind in einem Bereich, zum Beispiel eine für Isla unter **Schule**, enthält die passenden Informationen zu diesem Kind.

Notizen unter „Kinder“ sind immer privat, auch wenn die Schule an deine geschäftliche Adresse schreibt. Deine Machine fragt ihre KI einmal zu jeder neuen Information, ob sie deine Kinder betrifft.

## Zusammenführen, löschen und rückgängig machen

Mit **Zusammenführen mit …** im ⋯-Menü verschiebst du die Zeilen einer Notiz und ihre untergeordneten Notizen in eine andere Notiz. Von da an ergänzt deine Machine diese Notiz. Mit **Löschen** entfernst du eine Notiz. Bei beiden Aktionen wird kurz **Rückgängig** angezeigt. Das gilt auch, wenn du eine Zeile entfernst.

## Nicht dasselbe wie Besprechungsnotizen

Besprechungsnotizen und Notizen zu Personen oder Organisationen bleiben an ihrem bisherigen Ort. Die Notizen hier sind eigenständige Seiten.
