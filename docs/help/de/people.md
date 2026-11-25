---
title: Personen
area: graph
summary: Alle, mit denen du in Kontakt bist: ihre Seite, Zusammenfassung und ihr Verlauf sowie Personen hinzufügen, bearbeiten, zusammenführen oder löschen.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 5e671ff84b143e74
---
Alle, mit denen du in Kontakt bist, zuerst die engsten, aus deinen Nachrichten und Besprechungen. Newsletter, Belege und andere Mailings fügen niemanden hinzu, bis du antwortest. Sie stehen unter „Verborgene Absender“ unterhalb der Liste: Mit „Als Person anzeigen“ wird jemand zur Liste hinzugefügt. Felder, Tags und Importe funktionieren in allen drei Listen gleich. Jede Liste hat eigene Filter: siehe [The Graph](graph.md).

Ein gemeinsames Postfach (info@, Kundenservice, der Name eines Geschäfts) zählt zu der jeweiligen Organisation, nicht als Person. Das gilt auch, nachdem du dorthin geschrieben hast.

## Die Seite einer Person

Oben stehen Foto, Name, Titel, Organisation und Ort sowie eine Zeile dazu, wie ihr in Kontakt seid („Täglich im Gespräch · letzter Kontakt gestern · nächstes Treffen Di., 27. Okt.“). Der letzte Kontakt wird als „gerade eben“, „vor 3 Stunden“, „gestern“ oder „vor 3 Tagen“ angezeigt. Bei länger zurückliegendem Kontakt steht dort ein Datum. Bewege den Mauszeiger darüber, um das genaue Datum zu sehen. Darunter findest du:

- **Kontakt**: Telefonnummern und E-Mail-Adressen. Tippe auf eine Nummer oder Adresse, um anzurufen oder zu schreiben, oder tippe auf **Kopieren**. Auch der **Geburtstag** wird hier angezeigt, zusammen mit der Quelle (Google Kontakte, Google Kalender, Facebook, deine Notizen oder du): siehe [The Graph](graph.md#birthday).
- **Mit dir**: welche Rolle die Person für dich hat, ob sie ein Arbeits- oder Privatkontakt ist und ob sie zu deiner Familie oder Fleet gehört, mit **In Fleet ansehen**.
- **Auch auf**: andere Orte, an denen ihr miteinander sprecht. Über **Slack** wird die Person in Slack geöffnet oder der neueste Slack-Thread mit ihr.
- **Personen** und **Projekte**, zu denen sie gehört, **Offen zwischen euch** (gegenseitige Versprechen, mit **Erledigt markieren** und **Entfernen**) und ihr **Verlauf**.

Adressen und Chats einer Person werden automatisch zusammengeführt, wenn klar ist, dass sie zu derselben Person gehören, zum Beispiel eine geschäftliche E-Mail-Adresse mit der persönlichen Adresse in CC. Das gilt auch, wenn jemand, mit dem du chattest, über den Link, den du ihm geschickt hast, einen Anruf bucht und die Firma oder der Nachname übereinstimmt.

Wenn die Seite **Seite konnte nicht geladen werden.** anzeigt, tippe auf **Erneut versuchen**. Wenn die Meldung weiterhin erscheint, tippe unten auf der Seite auf **Stimmt etwas nicht?**.

## Zusammenfassung

Ein paar kurze Zeilen oben auf der Seite einer Person: was besprochen, gefragt, geplant oder versprochen wurde, mit allen genannten Personen. The Machine schreibt die Zusammenfassung um, wenn es Neuigkeiten gibt, aber nur für Personen, mit denen du wirklich in Kontakt bist. Jede Zeile wird vorher überprüft. Meistens geschieht das einmal am Tag, innerhalb weniger Stunden, wenn sich etwas mit der Person ändert, etwa eine neue Frist oder eine zurückgezogene Anfrage.

Unklare Zeilen werden ausgelassen. Wenn es nichts Konkretes zu sagen gibt, gibt es keine Zusammenfassung. Jede Zeile führt zu ihrer Quelle. Nachrichten vom selben Tag werden mit einem gemeinsamen Datum und ihrer Anzahl zusammengefasst und lassen sich gemeinsam öffnen.

Mit **Bearbeiten** kannst du die Zusammenfassung in deinen eigenen Worten schreiben. Bei Neuigkeiten zeigt The Machine eine **Vorgeschlagene Aktualisierung** mit **Übernehmen** und **Meine behalten** an. Mit **The Machine schreiben lassen** überlässt du das Schreiben wieder The Machine.

Bei der Vorbereitung auf Besprechungen wird die Zusammenfassung verwendet, aber nur die Zeilen aus dem Bereich der jeweiligen Aufgabe (Arbeit oder Privat). Sie bleibt auf deiner Machine. Dein Team sieht sie nicht.

## Verlauf

Die Seiten von Personen und Organisationen haben jeweils einen Verlauf, sortiert vom Neuesten zum Ältesten: E-Mails, Besprechungen und ihre Zoom-Zusammenfassungen, Intercom-Unterhaltungen (mit **In Intercom öffnen**), WhatsApp-, Telegram-, Slack-, LinkedIn- und X-Chats, Aufgaben, Versprechen und Projektänderungen. Mit den Chips oben kannst du jeweils eine Quelle anzeigen. Über **Mehr anzeigen** werden ältere Einträge geladen.

Anstehende Besprechungen stehen ganz oben unter **Demnächst**, die nächste zuerst. Mit **Alle anstehenden zeigen** werden auch die übrigen angezeigt. Bei einer Besprechung siehst du, wer dabei war, jede Person nur einmal. Besprechungen mit Notizen oder Transkript sind mit **Notizen** oder **Transkript** gekennzeichnet. Klicke darauf, um sie zu lesen.

Deine Verläufe gehören dir: Im Graph des Teams wird nur angezeigt, was deine Freigabeeinstellungen erlauben. Über **Team** oberhalb des Verlaufs siehst du auf einer Seite, was Teammitglieder geteilt haben. Bei jedem Eintrag steht, von wem er stammt. Unter **Meine** siehst du nur deine Einträge.

## Arbeit und Privat

Auf den Tabs **Arbeit** und **Privat** werden Personen nach ihrem Typ sortiert, der auf ihrer Seite steht. Deine eigene Auswahl (**Bearbeiten**) hat Vorrang. Ansonsten zählen deine Familie und Freunde sowie Personen, die mit dir verwandt oder befreundet sind (zum Beispiel deine Frau oder dein Vater), als privat, unabhängig davon, von welcher Adresse aus sie schreiben. Dein Team sieht keine privaten Kontakte.

## Person hinzufügen

Tippe oben in „Personen“ auf **Neue Person** oder auf **+** in der oberen Leiste auf dem Handy. Gib einen Namen sowie, falls bekannt, eine E-Mail-Adresse und Organisation ein. Wenn es in deinem Graph bereits eine ähnliche Person gibt, wird sie zuerst im Formular angezeigt. Du kannst dann stattdessen deren Seite öffnen. Mit **Hinzufügen** wird die neue Seite geöffnet.

Eine hinzugefügte Person bleibt erhalten, auch wenn es noch keine Nachrichten gibt. Die erste Nachricht wird ihr zugeordnet.

## Person bearbeiten

Mit **Bearbeiten** oben auf der Seite kannst du Name, Titel, Organisation, Ort, LinkedIn, Telefonnummern und E-Mail-Adressen, die Rolle der Person für dich und die Zuordnung zu Arbeit oder Privat ändern. Das Feld **Notizen** ist für alles, woran du dich erinnern möchtest. Notizen bleiben beim Zusammenführen erhalten. Mit **Speichern** werden die Änderungen übernommen, mit **Abbrechen** verworfen.

Deine Änderungen bleiben erhalten, auch wenn die Angaben erneut nachgeschlagen werden sowie nach **Zusammenführen** und **Rückgängig**. Leere ein Feld, um wieder den nachgeschlagenen Wert zu verwenden. Wenn du den Namen leerst, wird der Name aus den Nachrichten wiederhergestellt.

Um das Foto zu ändern, klicke darauf: **Bild hochladen**, ein gefundenes Foto auswählen oder **Bild entfernen**. Das Foto bleibt auf deiner Machine.

## Zwei Personen zusammenführen

Wenn zwei Personen vielleicht dieselbe sind, wirst du auf ihrer Seite gefragt, ob es sich um dieselbe Person handelt. In der Personenliste werden sie unter **Gleiche Person?** aufgeführt. Mit **Zusammenführen** werden sie zusammengeführt, einschließlich aller Nachrichten, Notizen, Rollen und Projekte. Mit **Nicht dieselbe** bleiben sie dauerhaft getrennt. Deine Antwort wird kurz bei dem Paar angezeigt. Anschließend verschwindet es aus der Liste. Die Liste wird ausgeblendet, wenn es keine offenen Fragen mehr gibt.

Eine Person mit einer Adresse, die deiner bekannten Adresse nur ähnelt, zum Beispiel acme-corp.example statt acmecorp.example, wird niemals als dieselbe Person vorgeschlagen. Nur du kannst ihr eine Rolle zuweisen.

Ein gleicher Name allein reicht bei unterschiedlichen Domains nie aus, da jeder einen Namen eingeben kann. Zwei Adressen mit unterschiedlichen Domains werden nur dann als dieselbe Person vorgeschlagen, wenn es noch eine weitere Verbindung gibt, etwa dieselben Kontakte oder ein gemeinsames Projekt. Eine Person, die deinen Namen unter einer Adresse verwendet, die nicht dir gehört, wird niemals vorgeschlagen. Füge deine weiteren Adressen stattdessen unter **Einstellungen** unter [Deine Adressen](settings.md#your-addresses) hinzu.

Wenn bei unterschiedlichen Domains nur der Vorname übereinstimmt, zum Beispiel „Sam“ und „Sam Lee“, werden sie nur bei gleicher Telefonnummer oder gleichem LinkedIn-Profil vorgeschlagen.

Wenn nur der Vorname mit einem über einen Chat erstellten Besprechungseintrag übereinstimmt oder die Adresse einer Person gehört, die du bereits kanntest, und nur die Person im Chat sagt, dass die Adresse ihr gehört, wirst du gefragt. The Machine öffnet niemals einen Link, um das herauszufinden.

Eine gemeinsame Adresse wie info@ oder eine Mailingliste wird niemals mit den Personen zusammengeführt, die darüber schreiben. Ein geschäftlicher Kontakt von außerhalb deines Unternehmens und ein privater Chat, bei denen nur der Name übereinstimmt, werden nicht automatisch zusammengeführt. Sie werden als mögliche Übereinstimmung angezeigt.

Mit **Alle zusammenführen** werden alle Paare in der Liste auf einmal zusammengeführt, außer denen, die du als **Nicht dieselbe** markiert hast. Mit **Rückgängig** kannst du sie direkt danach wieder trennen.

Um zwei Personen selbst zusammenzuführen, öffne eine der beiden Seiten und wähle dann **⋯**, **Gleiche Person wie…** und die andere Person aus. Auf der Seite der zusammengeführten Person steht unter **Zusammengeführt aus**, warum sie zusammengeführt wurde. Über **Rückgängig** kannst du sie wieder trennen.

## Person endgültig löschen

Öffne auf der Seite das Menü ⋯ und wähle **Endgültig löschen…**, dann **Löschen**. Die Person und alle Informationen, die deine Machine über sie kennt, werden entfernt: ihr Eintrag, ihre Adressen, nachgeschlagene Details, Nachrichten, die nur zwischen euch beiden ausgetauscht wurden, und Notizen über sie.

Aufgaben, an denen die Person beteiligt ist, bleiben erhalten, aber ihr Name wird entfernt. Sie wird nicht wieder hinzugefügt, auch nicht durch einen Import oder eine Aufgabe für Facebook-Geburtstage mit ihrem Namen oder ihrer Adresse. Diese Aktion kann nicht rückgängig gemacht werden.

## Unzustellbar

Wenn eine E-Mail an eine Person unzustellbar ist, wird ihre Adresse mit dem Datum als **Unzustellbar** angezeigt. Eine andere Adresse der Person wird zuerst aufgeführt. Neue Entwürfe werden nie an diese Adresse gesendet, wenn eine andere bekannt ist. Ist es die einzige Adresse, warnt dich der Sendevorgang, du kannst die E-Mail aber trotzdem senden.

Eine E-Mail gilt als unzustellbar, wenn der Mailserver meldet, dass die Adresse nicht existiert, oder wenn es innerhalb einer Woche drei vorübergehende Zustellfehler gibt. Der Hinweis wird entfernt, wenn die Person wieder von dieser Adresse aus schreibt oder eine E-Mail an die Adresse zugestellt wird.

## Jobtitel und Foto

Bei Personen mit einer Firmenadresse werden Jobtitel, Foto, LinkedIn-Profil und Stadt wie bei [Organisationsdetails](organization-data.md) nachgeschlagen. Bei einer gehosteten Machine werden dafür nur ihr Name und die Domain des Unternehmens verwendet. Für ein Foto erhält Gravatar einen Hash ihrer geschäftlichen Adresse, niemals die Adresse selbst. Du kannst die Funktion unter **Einstellungen** im Bereich „Sicherheit“ mit **Arbeitskontakte nachschlagen** ausschalten.

Mit dieser Einstellung wird auch verhindert, dass vor der ersten Besprechung die Website aufgerufen wird und eine Websuche stattfindet, wenn diese eingerichtet ist (siehe [Vorbereitung auf Besprechungen](calendar.md#ready-for-your-meetings)).

Wenn die Informationen gefunden wurden, zeigt die Seite der Person auch ihren Infotext, an, seit wann sie ihre aktuelle Stelle hat und welche zwei Stellen sie davor hatte. Die Vorbereitung auf Besprechungen berücksichtigt diese Angaben ebenfalls. Der Infotext wird nur verwendet, wenn die Person keine eigene Biografie hat.

Deine Verbindungen werden durch bereits gefundene Angaben ergänzt: um einen Titel, eine Telefonnummer und Zeitzone aus Slack, eine Biografie und einen Ort aus X, eine Überschrift und ein Foto aus LinkedIn, Jobtitel aus Google Kontakte und Salesflare sowie um das Kontaktfoto aus Salesflare, wenn dort eines hinterlegt ist. Bewege den Mauszeiger über die Zeile unter dem Namen, um die Quelle zu sehen.

Outlook ergänzt Fotos von Kollegen in deiner Organisation und deinen Outlook-Kontakten sowie Jobtitel und Unternehmen deiner Kontakte ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Fotos aus WhatsApp und Telegram werden über deine WhatsApp-Synchronisierung und die Verbindung zu deinen Telegram-Chats übernommen: jeweils bis zu 50 pro Tag, nur für Personen, die bereits in deinem Graph sind. Es wird nichts an diese Personen gesendet. Ein Facebook-Geburtstagsimport fügt beim Speichern das Profilbild einer Person hinzu, wenn sie noch kein Foto hat ([Routinen](routines.md)). Alles bleibt auf deiner Machine.

Im [Team Graph](team-graph.md) einer Work Fleet wird eine kleine Kopie des Arbeitsfotos mit dem geteilten Eintrag der Person gespeichert. Fotos aus Google Kontakte, WhatsApp, Telegram oder Facebook sowie Fotos, die du geändert oder entfernt hast, werden niemals geteilt.

## Über dich

Deine eigenen Adressen und Nummern, auch Aliasse, gehören immer dir und sind niemals Personen in deinem Graph. Wenn du nach dir selbst suchst oder eine Person mit einer deiner Adressen hinzufügst, wird **Über dich** geöffnet. Beim Import wird dein eigener Eintrag übersprungen.

Unter „Über dich“ werden deine Adressen samt Quelle aufgeführt. Du kannst sie unter **Einstellungen** im Bereich „Konto“ ändern. Um deinen eigenen Kontakt mit einem Teammitglied oder Freund zu teilen, wähle **Meinen Kontakt teilen**. Siehe [Einen Kontakt teilen](share-contact.md).

## Deine Rolle für die Person

Rollen, die deine Machine in deinen Nachrichten erkennt, stehen auf der Seite der Person unter **Für dich**, zusammen mit den Wörtern, an denen die Rolle erkennbar ist, zum Beispiel einem Titel. Wenn jemand sagt, dass er dein Buchhalter oder Kunde ist, reicht das nicht aus. Dafür braucht es auch etwas von dir, etwa deine eigenen Nachrichten oder Besprechungen mit der Person. Du musst das nicht bestätigen. Ist etwas falsch, kannst du es mit **Bearbeiten** auf der Seite der Person oder mit **⋯** in der entsprechenden Zeile unter **Letzte Änderungen** korrigieren. The Machine lernt aus deinen Änderungen.

## Was über eine Person bekannt ist

Fakten über die Person stehen auf ihrer Seite unter **Bekannt über**. Unter „Lernen“ stehen die allgemeinen Fakten. Mit **Hinzufügen** kannst du einen weiteren Fakt in deinen eigenen Worten festhalten. Für jeden Fakt gibt es ein Menü:

- Mit **Bearbeiten** kannst du den Fakt direkt ändern.
- Mit **Nicht über diese Person** wird er wieder zu einem allgemeinen Fakt unter **Lernen**, **Fakten**.
- Mit **Entfernen** wird er überall gelöscht.

## Letzte Änderungen

Unter **Letzte Änderungen**, direkt oberhalb des Verlaufs einer Person, Organisation oder eines Projekts, stehen Informationen, die deine Machine geändert oder neu erkannt hat: eine Rolle, wo jemand arbeitet, wie zwei Personen miteinander verbunden sind, ein Fakt oder eine Änderung bei einem Projekt. Jede Zeile zeigt das Datum und die Quelle. Tippe auf die Quelle, um die Nachricht zu lesen.

Wenn etwas nicht stimmt, kannst du es über **⋯** in der jeweiligen Zeile direkt korrigieren: mit **Bearbeiten**, **Entfernen**, **Nicht über diese Person** oder **Rückgängig**, um ein Projekt an seinen vorherigen Ort zurückzusetzen. Drei Zeilen werden angezeigt. Über **Mehr anzeigen** siehst du die übrigen.

Bei Personen, deren Angaben deine Machine heute aktualisiert hat, wird in der Personenliste ein kleiner Punkt angezeigt. Oben in der Liste steht **Heute wurden 4 Personen aktualisiert** und nennt die Personen. Siehe [The Graph](graph.md).

## Aufgabe zu einer Person

Mit **Neue Aufgabe** im Menü **⋯** einer Person, Organisation oder eines Projekts kannst du eine Aufgabe zu dieser Person, Organisation oder diesem Projekt erstellen.
