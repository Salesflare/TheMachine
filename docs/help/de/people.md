---
title: Personen
area: graph
summary: Alle, mit denen du in Kontakt bist: ihre Seite, Zusammenfassung und ihr Verlauf sowie Informationen dazu, wie du Personen hinzufügst, bearbeitest, zusammenführst oder löschst.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 97ffaf9944299a8b
---
Alle, mit denen du in Kontakt bist, nach Nähe sortiert. Die Informationen stammen aus deinen Nachrichten und Meetings. Newsletter, Belege und andere Mailings fügen niemanden hinzu, bis du antwortest. Sie stehen unter „Verborgene Absender“ unterhalb der Liste. Mit **Als Person anzeigen** wird jemand hinzugefügt. Felder, Tags und Importe funktionieren in allen drei Listen gleich, aber jede Liste hat eigene Filter: siehe [The Graph](graph.md).

Ein gemeinsamer Posteingang (info@, Kundenservice, der eigene Name eines Shops) zählt für die Organisation, nicht als Person, auch wenn du ihm schreibst.

## Seite einer Person

Oben stehen Foto, Name, Titel, Organisation und Ort sowie eine Zeile dazu, wie ihr in Kontakt seid („Täglich im Gespräch · letzter Kontakt gestern · nächstes Meeting Di., 27. Okt.“). Der letzte Kontakt wird als „gerade eben“, „vor 3 Stunden“, „gestern“ oder „vor 3 Tagen“ angezeigt. Bei länger zurückliegenden Kontakten steht ein Datum. Bewege den Mauszeiger darüber, um das genaue Datum zu sehen. Darunter findest du:

- **Kontakt**: Telefonnummern und E-Mail-Adressen. Tippe auf eine Nummer oder Adresse, um anzurufen oder zu schreiben, oder tippe auf **Kopieren**. Auch der **Geburtstag** wird hier angezeigt, samt Quelle (Google Kontakte, Google Kalender, Facebook oder du): siehe [The Graph](graph.md#birthday).
- **Mit dir**: wer die Person für dich ist, ob sie ein Arbeits- oder Privatkontakt ist und zu welcher Familie oder Fleet sie gehört, mit **In Fleet ansehen**.
- **Auch auf**: die anderen Orte, an denen ihr miteinander sprecht. **Slack** öffnet die Person in Slack oder euren neuesten Slack-Thread.
- **Personen** und **Projekte**, zu denen sie gehört, **Offen zwischen euch** (Versprechen in beide Richtungen, mit **Als erledigt markieren** und **Fallen lassen**) und ihr **Verlauf**.

Adressen und Chats einer Person werden automatisch zusammengeführt, wenn klar ist, dass sie zu einer Person gehören, zum Beispiel eine Arbeitsadresse mit der eigenen Adresse in CC.

Wenn auf einer Seite **Diese Seite konnte nicht geladen werden.** steht, tippe auf **Erneut versuchen**. Wenn die Meldung weiterhin erscheint, tippe unten auf der Seite auf **Stimmt etwas nicht?**.

## Zusammenfassung

Ein paar kurze Zeilen oben auf der Seite einer Person: was beschlossen, gefragt, geplant oder versprochen wurde, mit allen Namen. The Machine schreibt sie neu, wenn es etwas Neues gibt, aber nur für Personen, mit denen du wirklich in Kontakt bist, und prüft jede Zeile vorher. Normalerweise einmal am Tag, bei Änderungen an einer Angelegenheit mit der Person innerhalb weniger Stunden, etwa bei einer neuen Frist oder einer zurückgezogenen Bitte.

Eine vage Zeile wird ausgelassen. Gibt es nichts Konkretes zu sagen, gibt es keine Zusammenfassung. Jede Zeile verweist auf ihre Quelle: Nachrichten von einem Tag teilen sich ein Datum samt Anzahl und lassen sich gemeinsam öffnen.

Mit **Bearbeiten** formulierst du sie nach deinen Wünschen. Wenn es Neuigkeiten gibt, zeigt The Machine eine **Vorgeschlagene Aktualisierung** mit **Übernehmen** und **Meine behalten** an. Mit **The Machine schreiben lassen** gibst du ihr die Zusammenfassung zurück.

Vorbereitungen für Meetings verwenden die Zusammenfassung, aber nur die Zeilen aus dem Bereich der jeweiligen Aufgabe (Arbeit oder Privat). Sie bleibt auf deiner Machine. Dein Team sieht sie nie.

## Verlauf

Jede Personen- und Organisationsseite hat einen Verlauf, neueste Einträge zuerst: E-Mails, Meetings und ihre Zoom-Zusammenfassungen, Intercom-Unterhaltungen (mit **In Intercom öffnen**), WhatsApp-, Telegram-, Slack-, LinkedIn- und X-Chats, Aufgaben, Versprechen und Projektänderungen. Mit den Chips oben kannst du jeweils eine Quelle anzeigen. **Mehr anzeigen** lädt ältere Einträge.

Anstehende Meetings stehen ganz oben unter **Demnächst**, zuerst die frühesten. **Alle anstehenden zeigen** zeigt die übrigen. Bei einem Meeting wird angezeigt, wer dabei war, jede Person nur einmal. Für Meetings mit Notizen oder einem Transkript steht **Notizen** oder **Transkript** dabei. Klicke darauf, um sie zu lesen.

Deine Verläufe gehören dir: Im Graph des Teams wird nur angezeigt, was deine Freigaberegeln erlauben. Auf einer Seite kannst du über dem Verlauf **Team** auswählen, um Inhalte anzuzeigen, die Teammitglieder geteilt haben. Bei jedem Eintrag steht, von wem er stammt. **Meine** zeigt nur deine Inhalte.

## Arbeit und Privat

Die Tabs **Arbeit** und **Privat** listen Personen nach ihrem Typ auf, der auf ihrer Seite steht. Deine eigene Auswahl (**Bearbeiten**) hat Vorrang. Andernfalls zählen deine Familie und Freunde sowie Personen, die für dich Familie oder Freunde sind (eine Ehefrau, ein Vater), als privat, unabhängig davon, von welcher Adresse aus sie schreiben. Dein Team bekommt niemals private Kontakte zu sehen.

## Person hinzufügen

Tippe oben unter Personen auf **Neue Person** oder auf **+** in der oberen Leiste auf einem Smartphone. Gib einen Namen und, falls bekannt, eine E-Mail-Adresse und Organisation ein. Wenn es in deinem Graph bereits eine ähnliche Person gibt, zeigt das Formular sie zuerst an, damit du stattdessen deren Seite öffnen kannst. Mit **Hinzufügen** wird die neue Seite geöffnet.

Eine hinzugefügte Person bleibt erhalten, auch wenn es noch keine Nachrichten gibt. Die erste Nachricht wird ihr zugeordnet.

## Person bearbeiten

Mit **Bearbeiten** oben auf der Seite kannst du Name, Titel, Organisation, Standort, LinkedIn, Telefonnummern und E-Mail-Adressen, ihre Beziehung zu dir sowie Arbeit oder Privat ändern. Im Feld **Notizen** kannst du alles festhalten, woran du dich erinnern möchtest. Notizen bleiben beim Zusammenführen erhalten. Mit **Speichern** bleiben die Änderungen bestehen, mit **Abbrechen** werden sie verworfen.

Deine Änderungen bleiben erhalten, auch wenn die Details erneut nachgeschlagen werden oder du Personen mit **Zusammenführen** zusammenführst und mit **Rückgängig** wieder trennst. Leere ein Feld, um wieder den nachgeschlagenen Wert zu verwenden. Wenn du den Namen leerst, wird wieder der Name aus den Nachrichten verwendet.

Um das Foto zu ändern, klicke darauf: **Bild hochladen**, ein gefundenes Foto auswählen oder **Bild entfernen**. Es bleibt auf deiner Machine.

## Zwei Personen zusammenführen

Wenn zwei Personen dieselbe sein könnten, fragt ihre Seite, ob sie dieselbe Person sind. Unter **Gleiche Person?** werden sie auch in der Personenliste angezeigt. Mit **Zusammenführen** werden sie samt Nachrichten, Notizen, Rollen und Projekten zusammengeführt. Mit **Nicht dieselbe** bleiben sie dauerhaft getrennt. Deine Auswahl wird kurz bei dem Paar angezeigt, danach verschwindet es aus der Liste. Die Liste verschwindet, wenn es keine offenen Fragen mehr gibt.

Bei einer Adresse, die nur wie eine bekannte Adresse aussieht, zum Beispiel acme-corp.example statt acmecorp.example, wird nie vorgeschlagen, die Person als dieselbe Person zu markieren. Nur du kannst ihr eine Rolle zuweisen.

Eine gemeinsam genutzte Adresse wie info@ oder eine Mailingliste wird nie mit den Personen zusammengeführt, die darüber schreiben. Ein Arbeitskontakt außerhalb deines Unternehmens und ein privater Chat, bei denen nur der Name übereinstimmt, werden nicht automatisch zusammengeführt. Sie werden als Frage angezeigt.

Mit **Alle zusammenführen** werden alle Paare in der Liste auf einmal zusammengeführt, außer denen, die du mit **Nicht dieselbe** markiert hast. Mit **Rückgängig** direkt danach werden sie alle wieder getrennt.

Um zwei Personen selbst zusammenzuführen, öffne eine der beiden Seiten und wähle dann **⋯**, **Gleiche Person wie…** und die andere Person aus. Auf der Seite einer zusammengeführten Person steht unter **Zusammengeführt aus**, warum sie zusammengeführt wurde. Mit **Rückgängig** kannst du sie wieder trennen.

## Person dauerhaft löschen

Öffne auf der Seite der Person das Menü ⋯ und wähle **Endgültig löschen…**, dann **Löschen**. Dabei werden die Person und alles gelöscht, was deine Machine über sie weiß: ihr Eintrag, ihre Adressen, nachgeschlagene Details, Nachrichten, die nur zwischen euch beiden ausgetauscht wurden, und Notizen über sie.

Aufgaben, an denen sie beteiligt ist, bleiben erhalten, aber ihr Name wird entfernt. Sie wird nicht erneut hinzugefügt, auch nicht durch einen Import oder eine Aufgabe zu Facebook-Geburtstagen, in der ihr Name oder ihre Adresse steht. Das lässt sich nicht rückgängig machen.

## Unzustellbar

Wenn eine E-Mail an eine Person unzustellbar ist, wird ihre Adresse mit **Unzustellbar** und dem Datum angezeigt. Eine andere Adresse dieser Person wird an erster Stelle angezeigt. Neue Entwürfe werden nie an diese Adresse gesendet, wenn eine andere bekannt ist. Ist es ihre einzige Adresse, warnt dich das Sendefenster. Du kannst die E-Mail trotzdem senden.

Eine E-Mail gilt als unzustellbar, wenn der Mailserver meldet, dass die Adresse nicht existiert, oder nach 3 vorübergehenden Fehlern innerhalb einer Woche. Der Hinweis wird entfernt, wenn die Person wieder von dieser Adresse aus schreibt oder eine E-Mail an sie zugestellt wird.

## Jobtitel und Foto

Personen mit einer Firmenadresse erhalten einen Jobtitel, ein Foto, LinkedIn und eine Stadt. Diese Informationen werden wie [Organisationsdetails](organization-data.md) nachgeschlagen. Bei einer gehosteten Machine werden beim Nachschlagen nur ihr Name und die Domain des Unternehmens abgerufen. Für ein Foto erhält Gravatar einen Hash ihrer Arbeitsadresse, niemals die Adresse selbst. Du kannst die Funktion unter **Einstellungen** im Bereich Sicherheit deaktivieren: **Arbeitskontakte nachschlagen**.

Wenn die Informationen gefunden werden, zeigt die Seite der Person auch den Infotext, seit wann sie ihre aktuelle Rolle innehat und ihre zwei vorherigen Rollen. Vorbereitungen verwenden diese Informationen ebenfalls. Den Infotext verwenden sie nur, wenn die Person keine eigene Biografie hat.

Deine Verbindungen werden mit bereits vorhandenen Informationen ergänzt: um einen Titel, eine Telefonnummer und eine Zeitzone aus Slack, eine Biografie und einen Ort aus X, eine Überschrift und ein Foto aus LinkedIn, Jobtitel aus Google Kontakte und Salesflare sowie das Bild eines Kontakts aus Salesflare, wenn Salesflare selbst eines gespeichert hat. Bewege den Mauszeiger über die Zeile unter dem Namen, um zu sehen, woher sie stammt.

Outlook fügt Fotos von Kolleginnen und Kollegen in deiner Organisation sowie von deinen Outlook-Kontakten hinzu. Außerdem werden Jobtitel und Unternehmen deiner Kontakte ergänzt ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Fotos aus WhatsApp und Telegram werden über deine WhatsApp-Synchronisierung und deine Verbindung zu Telegram-Chats abgerufen: bis zu 50 pro Tag und Dienst, nur für Personen, die bereits in deinem Graph sind. An sie wird nichts gesendet. Ein Facebook-Geburtstagsimport fügt beim Speichern das Profilbild einer Person hinzu, wenn sie noch kein Foto hat ([Routinen](routines.md)). Alles bleibt auf deiner Machine.

Im [Team Graph](team-graph.md) einer Work Fleet wird eine kleine Kopie eines Arbeitsfotos zusammen mit dem geteilten Eintrag einer Person weitergegeben. Fotos aus Google Kontakte, WhatsApp, Telegram oder Facebook sowie Fotos, die du geändert oder entfernt hast, werden nie weitergegeben.

## Über dich

Deine eigenen Adressen und Nummern, auch Aliase, gehören immer zu dir und nie zu einer Person in deinem Graph. Wenn du nach dir selbst suchst oder eine Person mit einer deiner Adressen hinzufügst, wird **Über dich** geöffnet. Bei einem Import wird deine eigene Zeile übersprungen.

Unter „Über dich“ werden deine Adressen samt jeweiliger Quelle aufgeführt. Du kannst sie unter **Einstellungen** im Bereich Konto ändern. Um deinen eigenen Kontakt mit einem Teammitglied oder Freund zu teilen, wähle **Meinen Kontakt teilen**. Siehe [Kontakt teilen](share-contact.md).

## Was eine Person für dich ist

Rollen, die deine Machine in deinen Nachrichten erkennt, werden auf der Seite der Person unter **Für dich** angezeigt, zusammen mit der Zeile, aus der sie die Rolle abgeleitet hat. Du musst nichts bestätigen. Stimmt etwas nicht? Mit **Bearbeiten** auf der Seite der Person kannst du die Rolle korrigieren. Oder tippe bei der Zeile unter **Letzte Änderungen** auf **⋯**. Deine Machine lernt aus deinen Änderungen.

## Was deine Machine über eine Person weiß

Informationen über eine Person stehen auf ihrer Seite unter **Bekannt über**. Unter **Lernen** stehen allgemeine Erkenntnisse. Mit **Hinzufügen** kannst du eine weitere in deinen eigenen Worten festhalten. Jede Information hat ein Menü:

- Mit **Bearbeiten** kannst du sie direkt ändern.
- Mit **Nicht über diese Person** wird sie wieder zu einer allgemeinen Information unter **Lernen**, **Fakten**.
- Mit **Entfernen** wird sie überall gelöscht.

## Letzte Änderungen

Unter **Letzte Änderungen**, direkt über dem Verlauf einer Person, Organisation oder eines Projekts, werden Änderungen und Erkenntnisse deiner Machine aufgeführt: eine Rolle, der Arbeitsplatz einer Person, die Beziehung zwischen zwei Personen, eine Information oder eine Änderung an einem Projekt. Bei jeder Zeile stehen Datum und Quelle. Tippe auf die Quelle, um die Nachricht zu lesen.

Wenn etwas nicht stimmt, kannst du es über **⋯** direkt korrigieren: mit **Bearbeiten**, **Entfernen**, **Nicht über diese Person** oder **Rückgängig**, um ein Projekt an seinen vorherigen Ort zurückzusetzen. Drei Zeilen werden angezeigt. Mit **Mehr anzeigen** siehst du die übrigen.

Bei Personen, die deine Machine heute aktualisiert hat, erscheint ein kleiner Punkt in der Personenliste. Oben in der Liste werden sie mit **Heute wurden 4 Personen aktualisiert** aufgeführt. Siehe [The Graph](graph.md).

## Aufgabe zu einer Person

Mit **Neue Aufgabe** im Menü **⋯** einer Person, Organisation oder eines Projekts erstellst du eine Aufgabe zu diesem Eintrag.
