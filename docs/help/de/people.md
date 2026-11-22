---
title: Personen
area: graph
summary: Alle, mit denen du Kontakt hast: ihre Seite, Zusammenfassung und ihr Verlauf sowie wie du Personen hinzufügst, bearbeitest, zusammenführst oder löschst.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 5e808343918f7f47
---
Alle, mit denen du Kontakt hast, nach Nähe sortiert. Die Informationen stammen aus deinen Nachrichten und Meetings. Newsletter, Belege und andere Mailings fügen niemanden hinzu, bis du antwortest. Sie stehen unter „Ausgeblendete Absender“ unterhalb der Liste. Über „Als Person anzeigen“ kannst du jemanden hinzufügen. Felder, Tags und Import funktionieren in allen drei Listen gleich. Jede Liste hat eigene Filter: siehe [The Graph](graph.md).

Ein gemeinsames Postfach (info@, Kundenservice, der Name eines Geschäfts) wird der jeweiligen Organisation zugeordnet, nicht einer Person. Das gilt auch, wenn du an das Postfach schreibst.

## Die Seite einer Person

Oben stehen Foto, Name, Titel, Organisation und Ort sowie eine Zeile dazu, wie ihr in Kontakt seid („Täglicher Austausch · letzter Kontakt gestern · nächstes Meeting Di., 27. Okt.“). Der letzte Kontakt wird als „gerade eben“, „vor 3 Stunden“, „gestern“ oder „vor 3 Tagen“ angezeigt. Liegt er länger zurück, siehst du ein Datum. Bewege den Mauszeiger darauf, um das genaue Datum zu sehen. Darunter findest du:

- **Kontakt**: Telefonnummern und E-Mail-Adressen. Tippe auf eine Nummer oder Adresse, um anzurufen oder zu schreiben, oder **Kopieren**, um sie zu kopieren. Hier steht auch der **Geburtstag** und woher die Angabe stammt (Google-Kontakte, Google Calendar, Facebook, deine Notizen oder von dir): siehe [The Graph](graph.md#birthday).
- **Mit dir**: welche Rolle die Person für dich hat, ob es sich um einen Arbeits- oder Privatkontakt handelt und ob sie zu deiner Familie oder Fleet gehört. Hier findest du auch **In Fleet ansehen**.
- **Auch auf**: andere Orte, an denen ihr miteinander kommuniziert. Über **Slack** öffnest du die Person in Slack oder euren neuesten Slack-Thread.
- **Personen** und **Projekte**, zu denen sie gehört, **Offen zwischen euch** (Versprechen in beide Richtungen, mit **Als erledigt markieren** und **Fallen lassen**) sowie ihr **Verlauf**.

Adressen und Chats einer Person werden automatisch zusammengeführt, wenn klar ist, dass sie zu derselben Person gehören, zum Beispiel eine geschäftliche E-Mail-Adresse, bei der die private Adresse in CC steht.

Wenn eine Seite die Meldung **Die Seite konnte nicht geladen werden.** zeigt, tippe auf **Erneut versuchen**. Wenn die Meldung weiterhin erscheint, tippe unten auf der Seite auf **Stimmt etwas nicht?**.

## Zusammenfassung

Oben auf der Seite einer Person stehen ein paar kurze Zeilen: was beschlossen, gefragt, geplant oder versprochen wurde, mit allen Namen. The Machine schreibt die Zusammenfassung neu, wenn es etwas Neues gibt, und zwar nur für Personen, mit denen du wirklich in Kontakt bist. Außerdem prüft sie jede Zeile. Normalerweise passiert das einmal täglich. Wenn sich etwas mit der Person ändert, etwa eine neue Frist oder eine zurückgezogene Anfrage, wird die Zusammenfassung innerhalb weniger Stunden aktualisiert.

Vage Aussagen werden weggelassen. Wenn es nichts Konkretes zu sagen gibt, erscheint keine Zusammenfassung. Jede Zeile führt zur Quelle: Nachrichten von einem Tag werden mit einem gemeinsamen Datum und ihrer Anzahl angezeigt und lassen sich zusammen öffnen.

Über **Bearbeiten** kannst du die Zusammenfassung in deinen eigenen Worten formulieren. Wenn es Neuigkeiten gibt, zeigt The Machine eine **Vorgeschlagene Aktualisierung** mit **Übernehmen** und **Meine behalten**. Mit **The Machine schreiben lassen** gibst du die Zusammenfassung an The Machine zurück.

Die Meeting-Vorbereitung nutzt die Zusammenfassung, aber nur die Zeilen aus dem jeweiligen Aufgabenbereich (Arbeit oder Privat). Sie bleibt auf deiner Machine. Dein Team sieht sie nie.

## Verlauf

Jede Personen- und Organisationsseite hat einen Verlauf, sortiert vom Neuesten zum Ältesten: E-Mails, Meetings und ihre Zoom-Zusammenfassungen, Intercom-Unterhaltungen (mit **In Intercom öffnen**), WhatsApp-, Telegram-, Slack-, LinkedIn- und X-Chats, Aufgaben, Versprechen und Projektänderungen. Mit den Filtern oben kannst du jeweils eine Quelle anzeigen. Über **Mehr anzeigen** lädst du ältere Einträge.

Anstehende Meetings stehen ganz oben unter **Demnächst**, beginnend mit dem frühesten. Über **Alle anstehenden zeigen** siehst du auch die übrigen. Bei einem Meeting wird jede teilnehmende Person nur einmal aufgeführt. Für Meetings mit Notizen oder Transkript wird **Notizen** oder **Transkript** angezeigt. Klicke darauf, um sie zu lesen.

Deine Verläufe gehören dir. Im Team Graph werden nur Inhalte angezeigt, die deine Freigabeeinstellungen erlauben. Über **Team** oberhalb des Verlaufs einer Seite kannst du geteilte Inhalte deiner Teammitglieder anzeigen. Bei jedem Eintrag steht, von wem er stammt. **Meine** zeigt nur deine Inhalte.

## Arbeit und Privat

Auf den Tabs **Arbeit** und **Privat** werden Personen nach ihrem Typ sortiert, der auch auf ihrer Seite steht. Deine eigene Auswahl (**Bearbeiten**) hat Vorrang. Andernfalls werden deine Familie und Freunde sowie Personen, die für dich Familie oder Freunde sind (etwa eine Ehefrau oder ein Vater), als privat eingestuft, unabhängig davon, von welcher Adresse aus sie schreiben. Dein Team sieht keine privaten Kontakte.

## Person hinzufügen

Tippe oben in „Personen“ auf **Neue Person** oder auf dem Handy in der oberen Leiste auf **+**. Gib einen Namen und, falls bekannt, eine E-Mail-Adresse und Organisation ein. Wenn es in deinem Graph bereits eine ähnliche Person gibt, zeigt das Formular sie zuerst an. Du kannst dann stattdessen die vorhandene Person öffnen. Über **Hinzufügen** öffnest du die neue Seite.

Eine Person, die du hinzufügst, bleibt gespeichert, auch wenn es noch keine Nachrichten mit ihr gibt. Ihre erste Nachricht wird ihr zugeordnet.

## Person bearbeiten

Über **Bearbeiten** oben auf der Seite kannst du Name, Titel, Organisation, Ort, LinkedIn, Telefonnummern und E-Mail-Adressen ändern sowie festlegen, welche Rolle die Person für dich hat und ob es sich um einen Arbeits- oder Privatkontakt handelt. Das Feld **Notizen** ist für alles, woran du dich erinnern möchtest. Notizen bleiben auch nach dem Zusammenführen erhalten. Mit **Speichern** übernimmst du die Änderungen, mit **Abbrechen** verwirfst du sie.

Deine Änderungen bleiben erhalten, auch wenn die Angaben erneut nachgeschlagen oder Personen über **Zusammenführen** und **Rückgängig** zusammengeführt oder getrennt werden. Leere ein Feld, um wieder die nachgeschlagene Angabe zu verwenden. Wenn du den Namen leerst, wird der Name aus den Nachrichten wiederhergestellt.

Um das Foto zu ändern, klicke darauf. Du kannst **Bild hochladen**, ein gefundenes Foto auswählen oder **Bild entfernen**. Das Foto bleibt auf deiner Machine.

## Zwei Personen zusammenführen

Wenn zwei Personen möglicherweise dieselbe sind, fragt ihre Seite, ob es sich um dieselbe Person handelt. In „Personen“ werden sie unter **Gleiche Person?** aufgeführt. Über **Zusammenführen** werden alle ihre Nachrichten, Notizen, Rollen und Projekte zusammengeführt. Mit **Nicht dieselbe** bleiben sie dauerhaft getrennt. Deine Antwort wird kurz beim Personenpaar angezeigt, danach verschwindet es aus der Liste. Die Liste verschwindet, sobald es keine offenen Fragen mehr gibt.

Eine Person mit einer Adresse, die nur einer bekannten Adresse ähnelt, etwa acme-corp.example und acmecorp.example, wird nie als dieselbe Person vorgeschlagen. Nur du kannst ihr eine Rolle zuweisen.

Ein gleicher Name allein reicht über verschiedene Domains hinweg nie aus, da sich jeder so nennen kann. Zwei Adressen mit unterschiedlichen Domains werden nur dann zum Zusammenführen vorgeschlagen, wenn es noch einen weiteren Zusammenhang gibt, etwa gemeinsame Kontakte oder ein gemeinsames Projekt. Eine Person, die deinen Namen unter einer fremden Adresse verwendet, wird nie vorgeschlagen. Füge stattdessen deine anderen Adressen unter **Einstellungen** hinzu: [Deine Adressen](settings.md#your-addresses).

Wenn bei unterschiedlichen Domains nur der Vorname übereinstimmt, etwa „Sam“ und „Sam Lee“, werden die Personen nur bei gleicher Telefonnummer oder gleichem LinkedIn-Profil vorgeschlagen.

Eine gemeinsame Adresse wie info@ oder eine Mailingliste wird nie mit den Personen zusammengeführt, die darüber schreiben. Ein Arbeitskontakt außerhalb deines Unternehmens und ein privater Chat, bei denen nur der Name übereinstimmt, werden nicht automatisch zusammengeführt. Stattdessen werden sie als Frage angezeigt.

Mit **Alle zusammenführen** werden alle Paare in der Liste auf einmal zusammengeführt, außer denen, die du mit **Nicht dieselbe** markiert hast. Mit **Rückgängig** kannst du alle sofort wieder trennen.

Um zwei Personen selbst zusammenzuführen, öffne eine der beiden Seiten. Tippe dann auf **⋯**, **Gleiche Person wie…** und wähle die andere Person aus. Auf der Seite einer zusammengeführten Person steht unter **Zusammengeführt aus**, warum sie zusammengeführt wurde. Über **Rückgängig** kannst du sie wieder trennen.

## Person endgültig löschen

Öffne auf der Seite der Person das Menü ⋯ und wähle **Endgültig löschen…** und dann **Löschen**. Dadurch werden die Person und alle Informationen gelöscht, die deine Machine über sie kennt: ihr Eintrag, ihre Adressen, nachgeschlagene Angaben, Nachrichten, die nur zwischen euch beiden ausgetauscht wurden, und Notizen über sie.

Aufgaben, an denen die Person beteiligt ist, bleiben erhalten, aber ihr Name wird entfernt. Die Person wird nicht erneut hinzugefügt, auch nicht durch einen Import oder eine Aufgabe zu Facebook-Geburtstagen mit ihrem Namen oder ihrer Adresse. Diese Aktion lässt sich nicht rückgängig machen.

## Unzustellbar

Wenn eine E-Mail an eine Person unzustellbar ist, wird ihre Adresse mit dem Hinweis **Unzustellbar** und dem Datum angezeigt. Eine andere Adresse der Person wird zuerst angezeigt. Neue Entwürfe werden nie an diese Adresse gesendet, wenn eine andere bekannt ist. Ist es die einzige Adresse, weist dich das Versandfenster darauf hin. Du kannst die Nachricht trotzdem senden.

Eine E-Mail gilt als unzustellbar, wenn der Mailserver meldet, dass die Adresse nicht existiert, oder wenn innerhalb einer Woche drei vorübergehende Fehler auftreten. Der Hinweis wird entfernt, wenn die Person wieder von dieser Adresse schreibt oder eine E-Mail an sie zugestellt wird.

## Jobtitel und Foto

Bei Personen mit einer geschäftlichen Adresse werden Jobtitel, Foto, LinkedIn-Profil und Stadt nachgeschlagen, wie unter [Organisationsdetails](organization-data.md) beschrieben. Bei einer gehosteten Machine werden dafür nur der Name und die Unternehmensdomain abgefragt. Für ein Foto erhält Gravatar einen Hash der geschäftlichen Adresse, niemals die Adresse selbst. Du kannst die Funktion unter **Einstellungen** im Bereich „Sicherheit“ deaktivieren: **Arbeitskontakte nachschlagen**.

Wenn du diese Funktion deaktivierst, wird auch die kurze Websuche vor dem ersten Meeting ausgeschaltet (siehe [Bereit für deine Meetings](calendar.md#ready-for-your-meetings)).

Wenn die Angaben gefunden wurden, zeigt die Seite der Person auch ihren Infotext, seit wann sie ihre aktuelle Rolle hat und welche zwei Rollen sie davor hatte. Die Meeting-Vorbereitung nutzt diese Angaben ebenfalls. Der Infotext wird nur verwendet, wenn die Person keine eigene Biografie hat.

Deine Verbindungen werden durch Informationen ergänzt, die bereits verfügbar sind: Jobtitel, Telefonnummer und Zeitzone aus Slack, Biografie und Ort aus X, Überschrift und Foto aus LinkedIn, Jobtitel aus Google-Kontakten und Salesflare sowie das Kontaktfoto aus Salesflare, wenn es dort gespeichert ist. Bewege den Mauszeiger auf die Zeile unter dem Namen, um zu sehen, woher die Information stammt.

Outlook ergänzt Fotos von Kolleginnen und Kollegen in deiner Organisation und deinen Outlook-Kontakten sowie Jobtitel und Unternehmen deiner Kontakte ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

WhatsApp- und Telegram-Fotos werden über deine WhatsApp-Synchronisierung und deine Telegram-Chats-Verbindung übernommen: pro Dienst bis zu 50 am Tag und nur für Personen, die bereits in deinem Graph sind. Niemand wird darüber benachrichtigt. Ein Import von Facebook-Geburtstagen ergänzt beim Speichern das Profilbild einer Person, wenn noch kein Foto vorhanden ist ([Routinen](routines.md)). Alle Informationen bleiben auf deiner Machine.

Im [Team Graph](team-graph.md) einer Work Fleet wird eine kleine Kopie eines geschäftlichen Fotos zusammen mit dem geteilten Personeneintrag angezeigt. Fotos aus Google-Kontakten, WhatsApp, Telegram oder Facebook sowie Fotos, die du geändert oder entfernt hast, werden nie geteilt.

## Über dich

Deine eigenen Adressen und Telefonnummern, einschließlich Aliasse, gehören immer zu dir und nie zu einer Person in deinem Graph. Wenn du nach dir selbst suchst oder eine Person mit einer deiner Adressen hinzufügst, wird **Über dich** geöffnet. Beim Import wird dein eigener Eintrag übersprungen.

Unter „Über dich“ werden deine Adressen und ihre jeweilige Quelle aufgeführt. Du kannst sie unter **Einstellungen** im Bereich „Konto“ ändern. Um deinen Kontakt an ein Teammitglied oder einen Freund zu senden, wähle **Meinen Kontakt teilen**. Siehe [Kontakt teilen](share-contact.md).

## Welche Rolle die Person für dich hat

Rollen, die deine Machine aus deinen Nachrichten erkennt, stehen auf der Seite der Person unter **Für dich**. Angezeigt werden nur die Wörter, die auf die Rolle hinweisen, etwa ein Titel. Wenn jemand sagt, er sei dein Buchhalter oder Kunde, reicht das nicht aus. Dafür braucht es auch Belege von deiner Seite, etwa deine eigenen Nachrichten oder Meetings mit der Person. Du musst nichts bestätigen. Ist eine Angabe falsch, kannst du sie über **Bearbeiten** auf der Seite der Person oder über **⋯** in der entsprechenden Zeile unter **Letzte Änderungen** korrigieren. The Machine lernt aus deinen Änderungen.

## Was über eine Person bekannt ist

Fakten über eine Person stehen auf ihrer Seite unter **Bekannt über**. Unter „Lernen“ werden allgemeine Fakten gesammelt. Über **Hinzufügen** kannst du einen weiteren Fakt mit eigenen Worten hinzufügen. Zu jedem Fakt gibt es ein Menü:

- Über **Bearbeiten** änderst du den Fakt direkt.
- Mit **Nicht über diese Person** wird daraus wieder ein allgemeiner Fakt unter **Lernen**, **Fakten**.
- Über **Entfernen** wird der Fakt überall gelöscht.

## Letzte Änderungen

Unter **Letzte Änderungen**, eingeklappt direkt über dem Verlauf einer Person, Organisation oder eines Projekts, stehen Informationen, die deine Machine geändert oder neu gelernt hat: eine Rolle, der Arbeitsort, die Beziehung zwischen zwei Personen, ein Fakt oder eine Projektänderung. Bei jeder Zeile stehen Datum und Quelle. Tippe auf die Quelle, um die Nachricht zu lesen.

Wenn eine Angabe falsch ist, kannst du sie über **⋯** direkt korrigieren: **Bearbeiten**, **Entfernen**, **Nicht über diese Person** oder **Rückgängig**, um ein Projekt an seinen vorherigen Ort zurückzusetzen. Es werden drei Zeilen angezeigt. Über **Mehr anzeigen** siehst du die übrigen.

Bei Personen, deren Angaben deine Machine heute aktualisiert hat, wird in der Liste „Personen“ ein kleiner Punkt angezeigt. Die Zeile **4 Personen heute aktualisiert** oben in der Liste nennt sie. Siehe [The Graph](graph.md).

## Aufgabe zu einer Person

Über **Neue Aufgabe** im Menü **⋯** einer Person, Organisation oder eines Projekts erstellst du eine Aufgabe zu dieser Person, Organisation oder diesem Projekt.
