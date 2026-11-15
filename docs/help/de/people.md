---
title: Personen
area: graph
summary: Alle, mit denen du in Kontakt bist: ihre Seite, Zusammenfassung und ihr Verlauf sowie wie du Personen hinzufügst, bearbeitest, zusammenführst oder löschst.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 907cec019dc70184
---
Alle, mit denen du in Kontakt bist, nach Nähe sortiert, aus deinen Nachrichten und Meetings. Newsletter, Belege und andere Rundmails fügen niemanden hinzu, bis du antwortest. Sie stehen unter „Verborgene Absender“ am Ende der Liste. **Als Person anzeigen** fügt jemanden hinzu. Felder, Tags und Import funktionieren in allen drei Listen gleich. Jede Liste hat eigene Filter: siehe [Der Graph](graph.md).

Ein gemeinsames Postfach (info@, Kundenservice, der Name eines Geschäfts) zählt für die zugehörige Organisation und nicht als Person, auch wenn du ihm schreibst.

## Die Seite einer Person

Oben stehen Foto, Name, Titel, Organisation und Ort sowie eine Zeile dazu, wie ihr in Kontakt seid ("Täglich im Gespräch · letzter Kontakt gestern · nächstes Meeting Di., 27. Okt."). Der letzte Kontakt wird als „gerade eben“, „vor 3 Stunden“, „gestern“ oder „vor 3 Tagen“ angezeigt. Bei älteren Kontakten steht das Datum. Bewege den Mauszeiger darüber, um das genaue Datum zu sehen. Darunter findest du:

- **Kontakt**: Telefonnummern und E-Mail-Adressen. Tippe auf eine, um anzurufen oder zu schreiben, oder tippe auf **Kopieren**. Hier steht auch ihr **Geburtstag** und woher er stammt (Google Kontakte, Google Kalender, Facebook, deine Notizen oder du): siehe [Der Graph](graph.md#birthday).
- **Mit dir**: welche Rolle die Person für dich hat, ob sie ein geschäftlicher oder privater Kontakt ist und ob sie zu deiner Familie oder Fleet gehört, mit **In Fleet ansehen**.
- **Auch auf**: andere Orte, an denen ihr miteinander sprecht. **Slack** öffnet die Person in Slack oder euren neuesten Slack-Thread.
- **Personen** und **Projekte**, zu denen sie gehört, **Offen zwischen euch** (Versprechen in beide Richtungen, mit **Als erledigt markieren** und **Fallen lassen**) und ihr **Verlauf**.

Adressen und Chats einer Person werden automatisch zusammengeführt, wenn klar ist, dass sie zu derselben Person gehören, zum Beispiel eine geschäftliche E-Mail-Adresse mit der persönlichen Adresse der Person in CC.

Wenn auf einer Seite **Diese Seite konnte nicht geladen werden.** steht, tippe auf **Erneut versuchen**. Wenn die Meldung weiterhin erscheint, tippe unten auf der Seite auf **Stimmt etwas nicht?**.

## Zusammenfassung

Ein paar kurze Zeilen oben auf der Seite einer Person: was entschieden, gefragt, geplant oder versprochen wurde, mit den Namen aller Beteiligten. The Machine schreibt sie neu, wenn es etwas Neues gibt, und zwar nur für Personen, mit denen du wirklich in Kontakt bist. Dabei prüft sie jede Zeile zuerst. Meistens passiert das einmal täglich, bei Änderungen an einer Angelegenheit mit der Person innerhalb weniger Stunden, zum Beispiel bei einer neuen Frist oder wenn eine Anfrage zurückgezogen wird.

Vage Aussagen werden weggelassen. Gibt es nichts Konkretes zu sagen, gibt es keine Zusammenfassung. Jede Zeile führt zu ihrer Quelle zurück: Nachrichten vom selben Tag werden mit einem gemeinsamen Datum und ihrer Anzahl zusammengefasst und lassen sich gemeinsam öffnen.

Mit **Bearbeiten** kannst du die Zusammenfassung in deinen eigenen Worten schreiben. Wenn es Neuigkeiten gibt, zeigt The Machine eine **Vorgeschlagene Aktualisierung** mit **Übernehmen** und **Meine behalten**. Mit **The Machine schreiben lassen** gibst du die Zusammenfassung wieder an sie ab.

Vorbereitungen für Meetings verwenden die Zusammenfassung, aber nur die Zeilen aus dem Bereich dieser Aufgabe (Arbeit oder Privat). Sie bleibt auf deiner Machine. Dein Team sieht sie nie.

## Verlauf

Die Seite jeder Person und Organisation hat einen Verlauf, neueste Einträge zuerst: E-Mails, Meetings und ihre Zoom-Zusammenfassungen, Intercom-Unterhaltungen (mit **In Intercom öffnen**), WhatsApp-, Telegram-, Slack-, LinkedIn- und X-Chats, Aufgaben, Versprechen und Projektänderungen. Mit den Chips oben kannst du jeweils eine Quelle anzeigen. **Mehr anzeigen** lädt ältere Einträge.

Anstehende Meetings stehen oben unter **Demnächst**, die frühesten zuerst. **Alle anstehenden zeigen** zeigt die übrigen. Bei einem Meeting wird angezeigt, wer dabei war, jede Person nur einmal. Bei Meetings mit Notizen oder Transkript steht **Notizen** oder **Transkript**. Klicke darauf, um sie zu lesen.

Deine Verläufe gehören dir: Im Graph des Teams ist nur zu sehen, was deine Freigabeeinstellungen erlauben. Auf einer Seite kannst du mit **Team** über dem Verlauf Inhalte anzeigen, die deine Teammitglieder geteilt haben. Bei jedem Eintrag steht, von wem er stammt. **Meine** zeigt nur deine Inhalte.

## Arbeit und Privat

Die Tabs **Arbeit** und **Privat** listen Personen nach ihrem Typ auf, der auch auf ihrer Seite steht. Deine eigene Auswahl (**Bearbeiten**) hat Vorrang. Andernfalls werden deine Familie und Freunde sowie Personen, die für dich zur Familie oder zu Freunden gehören (eine Ehefrau, ein Vater), als privat eingestuft, unabhängig davon, von welcher Adresse sie schreiben. Dein Team sieht private Kontakte nie.

## Person hinzufügen

Tippe oben unter Personen auf **Neue Person** oder auf **+** in der oberen Leiste auf dem Smartphone. Gib einen Namen und, falls bekannt, eine E-Mail-Adresse und eine Organisation ein. Wenn es in deinem Graph schon eine ähnliche Person gibt, zeigt das Formular sie zuerst an, damit du stattdessen diese Person öffnen kannst. Mit **Hinzufügen** öffnest du die neue Seite.

Eine hinzugefügte Person bleibt erhalten, auch wenn es noch keine Nachrichten gibt. Ihre erste Nachricht wird mit ihr verknüpft.

## Person bearbeiten

Mit **Bearbeiten** oben auf der Seite kannst du Name, Titel, Organisation, Ort, LinkedIn, Telefonnummern und E-Mail-Adressen, ihre Rolle für dich sowie die Zuordnung zu Arbeit oder Privat ändern. Das Feld **Notizen** ist für alles, woran du dich erinnern möchtest. Notizen bleiben bei Zusammenführungen erhalten. Mit **Speichern** werden die Änderungen übernommen, mit **Abbrechen** verworfen.

Deine Änderungen bleiben erhalten, auch wenn die Angaben erneut nachgeschlagen werden oder du die Person mit **Zusammenführen** und **Rückgängig** zusammenführst. Leere ein Feld, um wieder den nachgeschlagenen Wert zu verwenden. Wenn du den Namen leerst, wird der Name aus den Nachrichten wiederhergestellt.

Um das Foto zu ändern, klicke darauf: **Bild hochladen**, ein gefundenes Foto auswählen oder **Bild entfernen**. Das Foto bleibt auf deiner Machine.

## Zwei Personen zusammenführen

Wenn zwei Personen möglicherweise dieselbe Person sind, fragt ihre Seite, ob sie dieselbe Person sind. Unter Personen werden sie außerdem unter **Gleiche Person?** aufgeführt. Mit **Zusammenführen** werden sie samt Nachrichten, Notizen, Rollen und Projekten zusammengeführt. **Nicht dieselbe** hält sie dauerhaft getrennt. Deine Auswahl wird kurz beim Paar angezeigt, danach verschwindet es aus der Liste. Die Liste verschwindet, wenn es keine offenen Fragen mehr gibt.

Eine Person mit einer Adresse, die nur einer bekannten Adresse ähnelt, zum Beispiel acme-corp.example statt acmecorp.example, wird nie als dieselbe Person vorgeschlagen. Nur du kannst ihr eine Rolle zuweisen.

Ein Name allein reicht bei zwei unterschiedlichen Domains nie aus, denn jeder kann denselben Namen eingeben. Zwei Adressen mit unterschiedlichen Domains werden nur dann als dieselbe Person vorgeschlagen, wenn es noch etwas gibt, das sie verbindet, zum Beispiel dieselben Personen oder ein gemeinsames Projekt. Jemand, der deinen Namen an einer Adresse verwendet, die nicht dir gehört, wird nie vorgeschlagen. Füge stattdessen unter Einstellungen deine anderen Adressen hinzu: [Deine Adressen](settings.md#your-addresses).

Eine gemeinsam genutzte Adresse wie info@ oder eine Mailingliste wird nie mit den Personen zusammengeführt, die darüber schreiben. Ein geschäftlicher Kontakt von außerhalb deines Unternehmens und ein privater Chat, bei denen nur der Name übereinstimmt, werden nicht automatisch zusammengeführt. Sie werden als offene Frage aufgeführt.

Mit **Alle zusammenführen** werden alle Paare in der Liste auf einmal zusammengeführt, außer denen, die du mit **Nicht dieselbe** markiert hast. Mit **Rückgängig** kannst du alle direkt danach wieder trennen.

Um zwei Personen selbst zusammenzuführen, öffne eine der Seiten und tippe dann auf **⋯**, **Gleiche Person wie…** und wähle die andere Person aus. Auf der Seite der zusammengeführten Person steht unter **Zusammengeführt aus**, warum die Personen zusammengeführt wurden. Mit **Rückgängig** kannst du sie wieder trennen.

## Person endgültig löschen

Öffne auf der Seite der Person das Menü ⋯ und wähle **Endgültig löschen…**, dann **Löschen**. Dadurch werden die Person und alle Informationen gelöscht, die deine Machine über sie kennt: ihr Eintrag, ihre Adressen, nachgeschlagene Angaben, Nachrichten, die nur zwischen euch beiden ausgetauscht wurden, und Notizen über sie.

Aufgaben, an denen sie beteiligt ist, bleiben bestehen, aber ihr Name wird daraus entfernt. Sie wird nicht erneut hinzugefügt, auch nicht durch einen Import oder eine Aufgabe zu Facebook-Geburtstagen mit ihrem Namen oder ihrer Adresse. Das lässt sich nicht rückgängig machen.

## Unzustellbar

Wenn eine E-Mail an jemanden zurückkommt, wird die Adresse mit **Unzustellbar** und dem Datum angezeigt. Eine andere Adresse der Person wird zuerst angezeigt. Neue Entwürfe werden nie an diese Adresse gesendet, wenn eine andere bekannt ist. Ist es ihre einzige Adresse, weist dich das Fenster zum Senden darauf hin. Du kannst die E-Mail trotzdem senden.

Eine Nachricht gilt als unzustellbar, wenn der Mailserver meldet, dass die Adresse nicht existiert, oder nach drei vorübergehenden Fehlern innerhalb einer Woche. Der Status wird aufgehoben, wenn die Person wieder von dieser Adresse schreibt oder eine E-Mail an sie zugestellt wird.

## Jobtitel und Foto

Personen mit einer geschäftlichen Adresse erhalten einen Jobtitel, ein Foto, LinkedIn und eine Stadt, die wie [Organisationsangaben](organization-data.md) nachgeschlagen werden. Bei einer gehosteten Machine werden dafür nur ihr Name und die Domain des Unternehmens abgerufen. Für ein Foto erhält Gravatar einen Hash ihrer geschäftlichen Adresse, niemals die Adresse selbst. Du kannst die Suche unter **Einstellungen** im Bereich Sicherheit ausschalten: **Arbeitskontakte nachschlagen**.

Wenn die Suche Angaben zu einer Person findet, zeigt ihre Seite außerdem ihren Infotext, seit wann sie ihre aktuelle Rolle hat und ihre beiden vorherigen Rollen. Diese Angaben werden auch für Vorbereitungen verwendet. Der Infotext wird nur genutzt, wenn die Person keine eigene Bio hat.

Deine Verbindungen werden durch Informationen ergänzt, die sie bereits gelesen haben: einen Titel, eine Telefonnummer und eine Zeitzone aus Slack, eine Bio und einen Ort aus X, eine Überschrift und ein Foto aus LinkedIn, Jobtitel aus Google Kontakte und Salesflare sowie das Bild eines Kontakts aus Salesflare, wenn Salesflare selbst eines speichert. Bewege den Mauszeiger über die Zeile unter dem Namen, um zu sehen, woher sie stammt.

Outlook fügt Fotos von Kolleginnen und Kollegen in deiner Organisation sowie von deinen Outlook-Kontakten hinzu. Außerdem werden Jobtitel und Unternehmen deiner Kontakte ergänzt ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Fotos aus WhatsApp und Telegram werden über deine WhatsApp-Synchronisierung und die Verbindung zu deinen Telegram-Chats abgerufen: jeweils bis zu 50 pro Tag und nur für Personen, die bereits in deinem Graph sind. Sie werden nicht darüber benachrichtigt. Ein Import von Facebook-Geburtstagen fügt beim Speichern das Profilbild einer Person hinzu, wenn sie noch kein Foto hat ([Routinen](routines.md)). Alle Angaben bleiben auf deiner Machine.

Im [Team-Graph](team-graph.md) einer geschäftlichen Fleet wird eine kleine Kopie eines geschäftlichen Fotos mit dem geteilten Eintrag einer Person übertragen. Fotos aus Google Kontakte, WhatsApp, Telegram oder Facebook sowie Fotos, die du geändert oder entfernt hast, werden nie übertragen.

## Über dich

Deine eigenen Adressen und Nummern, auch Aliasse, gehören immer zu dir und nie zu einer Person in deinem Graph. Wenn du nach dir selbst suchst oder eine Person mit einer deiner Adressen hinzufügst, wird **Über dich** geöffnet. Beim Import wird dein eigener Eintrag übersprungen.

Unter „Über dich“ stehen deine Adressen und ihre jeweilige Quelle. Ändere sie unter **Einstellungen** im Bereich Konto. Um deinen eigenen Kontakt mit einer Kollegin, einem Kollegen oder einer befreundeten Person zu teilen, wähle **Meinen Kontakt teilen**. Siehe [Kontakt teilen](share-contact.md).

## Welche Rolle die Person für dich hat

Rollen, die deine Machine in deinen Nachrichten erkennt, stehen auf der Seite der Person unter **Für dich**, zusammen mit der Zeile, in der sie erkannt wurden. Du musst nichts bestätigen. Stimmt etwas nicht? Mit **Bearbeiten** auf der Seite der Person oder über **⋯** in der entsprechenden Zeile unter **Letzte Änderungen** kannst du es korrigieren. Die Machine lernt aus deinen Änderungen.

## Was die Machine über eine Person weiß

Fakten über eine Person stehen auf ihrer Seite unter **Über sie bekannt**. Unter **Lernen** bleiben allgemeine Erkenntnisse erhalten. Mit **Hinzufügen** kannst du weitere Fakten in deinen eigenen Worten festhalten. Für jeden Fakt gibt es ein Menü:

- Mit **Bearbeiten** kannst du ihn direkt ändern.
- Mit **Nicht über sie** wird daraus wieder ein allgemeiner Fakt, der unter **Lernen**, **Fakten** steht.
- Mit **Entfernen** wird er überall gelöscht.

## Letzte Änderungen

Unter **Letzte Änderungen**, direkt über dem Verlauf einer Person, Organisation oder eines Projekts, werden Änderungen und Erkenntnisse deiner Machine aufgeführt: eine Rolle, der Arbeitsplatz einer Person, die Verbindung zwischen zwei Personen, ein Fakt oder eine Projektänderung. Bei jeder Zeile stehen Datum und Quelle. Tippe auf die Quelle, um die Nachricht zu lesen.

Wenn eine Angabe falsch ist, kannst du sie über **⋯** direkt korrigieren: mit **Bearbeiten**, **Entfernen**, **Nicht über sie** oder **Rückgängig**, um ein Projekt an seinen vorherigen Ort zurückzusetzen. Es werden drei Zeilen angezeigt. Mit **Mehr anzeigen** siehst du die übrigen.

Bei einer Person, die deine Machine heute aktualisiert hat, erscheint ein kleiner Punkt in der Personenliste. Oben in der Liste steht außerdem **Heute 4 Personen aktualisiert**, mit den Namen dieser Personen. Siehe [Der Graph](graph.md).

## Aufgabe zu einer Person

Mit **Neue Aufgabe** im Menü **⋯** einer Person, Organisation oder eines Projekts erstellst du eine Aufgabe zu dieser Person.
