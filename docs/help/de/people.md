---
title: Personen
area: graph
summary: Alle, mit denen du in Kontakt bist: ihre Seite, Zusammenfassung und ihr Verlauf sowie alles zum Hinzufügen, Bearbeiten, Zusammenführen oder Löschen von Personen.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 84312952f04b8597
---
Alle, mit denen du in Kontakt bist, nach Nähe sortiert, aus deinen Nachrichten und Meetings. Newsletter, Belege und andere Mailings fügen niemanden hinzu, bis du antwortest. Sie stehen unter „Ausgeblendete Absender“, unterhalb der Liste: Mit „Als Person anzeigen“ fügst du jemanden hinzu. Felder, Tags und Import funktionieren in allen drei Listen gleich, und jede Liste hat eigene Filter: siehe [The Graph](graph.md).

Ein gemeinsames Postfach (info@, Kundenservice, der eigene Name eines Geschäfts) zählt für die jeweilige Organisation, nicht als Person, auch wenn du dorthin schreibst.

## Die Seite einer Person

Oben stehen Foto, Name, Titel, Organisation und Ort sowie eine Zeile dazu, wie ihr in Kontakt seid („Täglicher Austausch · letzter Kontakt gestern · nächstes Meeting Di., 27. Okt.“). Der letzte Kontakt wird als „gerade eben“, „vor 3 Stunden“, „gestern“ oder „vor 3 Tagen“ angezeigt, bei länger zurückliegenden Kontakten als Datum. Bewege den Mauszeiger darüber, um das genaue Datum zu sehen. Darunter findest du:

- **Kontakt**: Telefonnummern und E-Mail-Adressen. Tippe auf einen Eintrag, um anzurufen oder zu schreiben, oder **Kopieren**, um ihn zu kopieren. Auch der **Geburtstag** wird hier mit der Quelle angezeigt (Google Kontakte, Google Kalender, Facebook, deine Notizen oder du selbst): siehe [The Graph](graph.md#birthday).
- **Mit dir**: was die Person für dich ist, ob sie ein Arbeitskontakt oder privater Kontakt ist und zu deiner Family oder Fleet gehört, mit **In Fleet ansehen**.
- **Auch auf**: die anderen Orte, an denen ihr miteinander sprecht. **Slack** öffnet die Person in Slack oder euren neuesten Slack-Thread.
- **Personen** und **Projekte**, zu denen sie gehört, **Offen zwischen euch** (gegenseitige Versprechen mit **Als erledigt markieren** und **Entfernen**) sowie ihren **Verlauf**.

Adressen und Chats einer Person werden automatisch zusammengeführt, wenn klar ist, dass sie zu einer Person gehören, etwa eine geschäftliche E-Mail-Adresse mit ihrer eigenen Adresse in CC. Das passiert auch, wenn jemand, mit dem du chattest, über den Link, den du ihm geschickt hast, einen Anruf bucht und der Firmenname oder Nachname übereinstimmt.

Wenn die Seite **Diese Seite konnte nicht geladen werden.** anzeigt, tippe auf **Erneut versuchen**. Wenn die Meldung weiterhin erscheint, tippe unten auf der Seite auf **Stimmt etwas nicht?**.

## Zusammenfassung

Ein paar kurze Zeilen oben auf der Seite einer Person: was besprochen, gefragt, geplant oder versprochen wurde, mit allen Namen. The Machine schreibt sie neu, wenn es etwas Neues gibt, aber nur für Personen, mit denen du wirklich in Kontakt bist, und prüft jede Zeile vorher. Normalerweise einmal am Tag, bei Änderungen an einer Sache mit der Person innerhalb weniger Stunden, etwa bei einer neuen Frist oder einer zurückgenommenen Bitte.

Vage Aussagen werden ausgelassen. Gibt es nichts Konkretes zu sagen, gibt es keine Zusammenfassung. Jede Zeile führt zu ihrer Quelle: Nachrichten von einem Tag werden mit einem gemeinsamen Datum und ihrer Anzahl angezeigt und gemeinsam geöffnet.

Mit **Bearbeiten** kannst du die Zusammenfassung nach deinen Vorstellungen formulieren. Wenn es Neuigkeiten gibt, zeigt The Machine eine **Vorgeschlagene Aktualisierung** mit **Übernehmen** und **Meine behalten** an. Mit **The Machine schreiben lassen** gibst du die Zusammenfassung wieder an The Machine zurück.

Meeting-Vorbereitungen verwenden sie, aber nur die Zeilen aus dem Bereich der jeweiligen Aufgabe (Arbeit oder Privat). Sie bleibt auf deiner Machine. Dein Team sieht sie nie.

## Verlauf

Jede Personen- und Organisationsseite hat einen Verlauf, der mit dem Neuesten beginnt: E-Mails, Meetings und ihre Zoom-Zusammenfassungen, Intercom-Unterhaltungen (mit **In Intercom öffnen**), WhatsApp-, Telegram-, Slack-, LinkedIn- und X-Chats, Aufgaben, Versprechen und Projektänderungen. Mit den Chips oben kannst du jeweils eine Quelle anzeigen. **Mehr anzeigen** lädt ältere Einträge.

Anstehende Meetings stehen ganz oben unter **Demnächst**, zuerst die nächsten. **Alle anstehenden zeigen** zeigt die übrigen. Bei einem Meeting wird angezeigt, wer dabei war, jede Person nur einmal. Bei Meetings mit Notizen oder einem Transkript steht **Notizen** oder **Transkript**. Klicke darauf, um sie zu lesen.

Deine Verläufe gehören dir: Im Graph des Teams werden nur Inhalte angezeigt, die deine Freigabeeinstellungen erlauben. Auf einer Seite zeigt **Team** über dem Verlauf, was Teammitglieder geteilt haben. Bei jedem Eintrag steht, von wem er stammt. **Meine** zeigt nur deine Einträge.

## Arbeit und Privat

Die Tabs **Arbeit** und **Privat** listen Personen nach ihrem Typ auf, der auch auf ihrer Seite steht. Deine eigene Auswahl (**Bearbeiten**) hat Vorrang. Andernfalls werden deine Family und Friends sowie Familienmitglieder oder Freunde von dir (etwa eine Ehefrau oder ein Vater) als privat eingestuft, egal von welcher Adresse aus sie schreiben. Dein Team sieht private Kontakte nie.

## Person hinzufügen

Tippe oben in „Personen“ auf **Neue Person** oder auf **+** in der oberen Leiste auf dem Handy. Gib einen Namen und, falls bekannt, eine E-Mail-Adresse und Organisation ein. Wenn es in deinem Graph bereits eine ähnliche Person gibt, wird sie im Formular zuerst angezeigt, damit du stattdessen ihre Seite öffnen kannst. Mit **Hinzufügen** wird die neue Seite geöffnet.

Eine hinzugefügte Person bleibt gespeichert, auch wenn es noch keine Nachrichten gibt. Mit der ersten Nachricht wird sie mit der Person verknüpft.

## Person bearbeiten

Mit **Bearbeiten** oben auf der Seite kannst du Name, Titel, Organisation, Ort, LinkedIn-Profil, Telefonnummern und E-Mail-Adressen, die Beziehung zu dir sowie die Einstufung als Arbeit oder Privat ändern. Das Feld **Notizen** ist für alles gedacht, woran du dich erinnern möchtest. Notizen bleiben beim Zusammenführen erhalten. Mit **Speichern** übernimmst du die Änderungen, mit **Abbrechen** verwirfst du sie.

Deine Änderungen bleiben bestehen, auch wenn die Angaben erneut nachgeschlagen werden, und auch nach **Zusammenführen** und **Rückgängig**. Leere ein Feld, um wieder den nachgeschlagenen Wert zu verwenden. Bei einem leeren Namen wird wieder der Name aus den Nachrichten angezeigt.

Klicke auf das Bild, um es zu ändern: **Bild hochladen**, ein gefundenes Bild auswählen oder **Bild entfernen**. Das Bild bleibt auf deiner Machine.

## Zwei Personen zusammenführen

Wenn zwei Personen möglicherweise ein und dieselbe Person sind, fragt ihre Seite, ob es sich um dieselbe Person handelt. In „Personen“ werden sie außerdem unter **Gleiche Person?** aufgelistet. Mit **Zusammenführen** werden ihre Nachrichten, Notizen, Rollen und Projekte zusammengeführt. **Nicht dieselbe** hält sie dauerhaft getrennt. Deine Antwort wird kurz beim Paar angezeigt, danach verschwindet es aus der Liste. Die Liste wird ausgeblendet, sobald es keine offenen Fragen mehr gibt.

Eine Person mit einer Adresse, die einer bekannten Adresse nur ähnelt, etwa acme-corp.example und acmecorp.example, wird nie als dieselbe Person vorgeschlagen. Nur du kannst ihr eine Rolle zuweisen.

Ein Name allein reicht bei zwei verschiedenen Domains nie aus, da ihn jede Person verwenden kann. Zwei Adressen mit unterschiedlichen Domains werden nur dann vorgeschlagen, wenn es eine weitere Verbindung gibt, etwa gemeinsame Kontakte oder ein kleines Projekt. Bei einem Vornamen allein („Sam“ und „Sam Lee“) braucht es mehr Hinweise: dasselbe Unternehmen, dieselbe Telefonnummer oder dasselbe LinkedIn-Profil.

Jemand, der deinen Namen verwendet, aber eine Adresse hat, die nicht deine ist, wird nie vorgeschlagen. Füge stattdessen deine weiteren Adressen unter „Einstellungen“ hinzu: [Deine Adressen](settings.md#your-addresses).

Wenn bei verschiedenen Domains nur der Vorname übereinstimmt, etwa „Sam“ und „Sam Lee“, werden die Personen nur bei derselben Telefonnummer oder demselben LinkedIn-Profil vorgeschlagen.

Wenn nur ein Vorname bei einem über einen Chat vereinbarten Meeting übereinstimmt oder die Adresse zu jemandem gehört, den du bereits kanntest, und nur die Person im Chat sagt, dass die Adresse ihr gehört, wirst du gefragt. The Machine öffnet nie einen Link, um das herauszufinden.

Eine gemeinsame Adresse wie info@ oder eine Mailingliste wird nie mit den Personen zusammengeführt, die darüber schreiben. Ein Arbeitskontakt von außerhalb deines Unternehmens und ein privater Chat, bei denen nur der Name übereinstimmt, werden nicht automatisch zusammengeführt. Sie werden als offene Frage aufgeführt.

Mit **Alle zusammenführen** werden alle Paare in der Liste auf einmal zusammengeführt, außer denen, die du mit **Nicht dieselbe** markiert hast. Mit **Rückgängig** direkt danach werden alle wieder getrennt.

Um zwei Personen selbst zusammenzuführen, öffne eine ihrer Seiten und wähle dann **⋯**, **Gleiche Person wie…** und die andere Person. Auf der Seite einer zusammengeführten Person steht unter **Zusammengeführt aus**, warum sie zusammengeführt wurde. Mit **Rückgängig** kannst du sie wieder trennen.

## Person endgültig löschen

Öffne auf der Seite das Menü **⋯** und wähle **Endgültig löschen…**, dann **Löschen**. Dadurch werden die Person und alle Informationen gelöscht, die deine Machine über sie gespeichert hat: ihr Eintrag, ihre Adressen, nachgeschlagene Angaben, Nachrichten nur zwischen euch beiden sowie Notizen über sie.

Aufgaben, an denen die Person beteiligt ist, bleiben bestehen, aber ihr Name wird entfernt. Sie wird nicht erneut hinzugefügt, auch nicht durch einen Import oder eine Aufgabe zu Facebook-Geburtstagen mit ihrem Namen oder ihrer Adresse. Der Vorgang kann nicht rückgängig gemacht werden.

## Unzustellbar

Wenn eine E-Mail an jemanden unzustellbar ist, wird die Adresse mit **Unzustellbar** und dem Datum angezeigt. Eine andere Adresse dieser Person wird zuerst aufgeführt. Neue Entwürfe werden nie an diese Adresse gesendet, wenn eine andere bekannt ist. Ist es die einzige Adresse, weist dich das Versandfenster darauf hin. Du kannst die E-Mail trotzdem senden.

Eine E-Mail gilt als unzustellbar, wenn der Mailserver meldet, dass die Adresse nicht existiert, oder nach drei vorübergehenden Fehlern innerhalb einer Woche. Der Hinweis wird entfernt, wenn die Person wieder von dieser Adresse aus schreibt oder eine E-Mail an sie zugestellt wird.

## Berufsbezeichnung und Foto

Bei Personen mit einer Firmenadresse werden Berufsbezeichnung, Foto, LinkedIn-Profil und Stadt nachgeschlagen, wie unter [Organisationsdetails](organization-data.md) beschrieben. Bei einer gehosteten Machine werden dafür nur der Name und die Firmendomain verwendet. Für ein Foto erhält Gravatar einen Hash der geschäftlichen E-Mail-Adresse, niemals die Adresse selbst. Du kannst das unter **Einstellungen** im Bereich „Sicherheit“ deaktivieren: **Arbeitskontakte nachschlagen**.

Mit dieser Einstellung wird auch verhindert, dass vor einem ersten Meeting die Website aufgerufen und eine Websuche durchgeführt wird (siehe [Bereit für deine Meetings](calendar.md#ready-for-your-meetings)).

Wenn die Informationen gefunden wurden, zeigt die Seite außerdem den Infotext der Person, seit wann sie ihre aktuelle Position innehat und ihre beiden vorherigen Positionen. Auch Vorbereitungen verwenden diese Angaben. Der Infotext wird nur verwendet, wenn die Person keinen eigenen Lebenslauf hat.

Deine Verbindungen werden mit bereits gelesenen Informationen ergänzt: Berufsbezeichnung, Telefonnummer und Zeitzone aus Slack, Biografie und Ort aus X, Überschrift und Foto aus LinkedIn, Berufsbezeichnungen aus Google Kontakte und Salesflare sowie ein Kontaktfoto aus Salesflare, wenn Salesflare selbst eines gespeichert hat. Bewege den Mauszeiger über die Zeile unter dem Namen, um die Quelle zu sehen.

Outlook ergänzt Fotos von Kolleginnen und Kollegen in deiner Organisation und von deinen Outlook-Kontakten sowie Berufsbezeichnungen und Unternehmen deiner Kontakte ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

WhatsApp- und Telegram-Bilder werden über deine WhatsApp-Synchronisierung und deine Telegram-Chats-Verbindung hinzugefügt: jeweils bis zu 50 pro Tag und nur für Personen, die bereits in deinem Graph sind. Es wird nichts an diese Personen gesendet. Beim Import von Facebook-Geburtstagen wird das Profilbild einer Person ohne Foto hinzugefügt, wenn du es speicherst ([Routinen](routines.md)). Alle Bilder bleiben auf deiner Machine.

Im [Team Graph](team-graph.md) einer Work Fleet wird eine kleine Kopie eines beruflichen Fotos zusammen mit dem geteilten Eintrag einer Person angezeigt. Bilder aus Google Kontakte, WhatsApp, Telegram oder Facebook sowie von dir geänderte oder entfernte Bilder werden nie geteilt.

## Über dich

Deine eigenen Adressen und Telefonnummern, auch Aliase, gehören immer zu dir und werden nie als Person in deinem Graph geführt. Wenn du nach dir selbst suchst oder eine Person mit einer deiner Adressen hinzufügst, wird **Über dich** geöffnet. Beim Import wird dein eigener Eintrag übersprungen.

Unter „Über dich“ stehen deine Adressen mit ihrer jeweiligen Quelle. Ändere sie unter **Einstellungen** im Bereich „Konto“. Um deine Kontaktdaten an ein Teammitglied oder einen Freund zu senden, wähle **Meinen Kontakt teilen**. Siehe [Einen Kontakt teilen](share-contact.md).

## Was sie für dich sind

Rollen, die deine Machine in deinen Nachrichten erkennt, stehen auf der jeweiligen Seite unter **Für dich**, zusammen mit den Wörtern, die auf die Rolle hinweisen, etwa einer Berufsbezeichnung. Wenn jemand sagt, dass er dein Buchhalter oder Kunde ist, reicht das nicht aus. Dafür braucht es auch Hinweise von deiner Seite, etwa deine eigenen Nachrichten oder Meetings mit der Person. Deine Bestätigung ist nicht nötig. Stimmt etwas nicht? Mit **Bearbeiten** auf der Seite kannst du es korrigieren oder mit **⋯** in der Zeile unter **Letzte Änderungen**. Deine Machine lernt aus deinen Änderungen.

## Was deine Machine über jemanden weiß

Informationen über eine Person stehen auf ihrer Seite unter **Bekanntes über**. Unter **Lernen** werden allgemeine Informationen gespeichert. Mit **Hinzufügen** kannst du weitere Informationen in deinen eigenen Worten festhalten. Jede Information hat ein Menü:

- **Bearbeiten** ändert sie direkt.
- **Nicht über diese Person** macht daraus wieder eine allgemeine Information unter **Lernen**, **Fakten**.
- **Entfernen** löscht sie überall.

## Letzte Änderungen

Unter **Letzte Änderungen**, direkt über dem Verlauf einer Person, Organisation oder eines Projekts, werden Änderungen und neue Erkenntnisse deiner Machine angezeigt: eine Rolle, der Arbeitsplatz einer Person, eine Beziehung zwischen zwei Personen, eine Information oder eine Änderung an einem Projekt. Bei jedem Eintrag stehen Datum und Quelle. Tippe auf die Quelle, um die Nachricht zu lesen.

Wenn ein Eintrag falsch ist, kannst du ihn über **⋯** direkt korrigieren: mit **Bearbeiten**, **Entfernen**, **Nicht über diese Person** oder **Rückgängig**, um ein Projekt an seinen vorherigen Ort zurückzusetzen. Es werden drei Einträge angezeigt. Mit **Mehr anzeigen** siehst du die übrigen.

Bei Personen, deren Informationen deine Machine heute aktualisiert hat, steht in der Personenliste ein kleiner Punkt. Oben in der Liste werden sie unter **4 Personen heute aktualisiert** aufgeführt. Siehe [The Graph](graph.md).

## Aufgabe zu einer Person

Mit **Neue Aufgabe** im Menü **⋯** einer Person, Organisation oder eines Projekts erstellst du eine Aufgabe zu dieser Person.
