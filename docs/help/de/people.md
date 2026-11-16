---
title: Personen
area: graph
summary: Alle, mit denen du in Kontakt bist: ihre Seite, Zusammenfassung und ihr Verlauf sowie wie du Personen hinzufügst, bearbeitest, zusammenführst oder löschst.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 0eb2dcc70fba84c2
---
Alle, mit denen du in Kontakt bist, nach Nähe sortiert, aus deinen Nachrichten und Meetings. Newsletter, Belege und andere Massenmails fügen niemanden hinzu, bis du antwortest. Sie stehen unter „Ausgeblendete Absender“ unter der Liste. Mit **Als Person anzeigen** wird jemand hinzugefügt. Felder, Tags und Import funktionieren in allen drei Listen gleich. Jede Liste hat eigene Filter: siehe [Graph](graph.md).

Ein gemeinsames Postfach (info@, Kundenservice, der Eigenname eines Geschäfts) zählt für die Organisation, nicht als Person, auch nachdem du dorthin geschrieben hast.

## Die Seite einer Person

Oben stehen das Foto, der Name, die Berufsbezeichnung, die Organisation und der Ort sowie eine Zeile dazu, wie ihr in Kontakt seid („Täglich im Gespräch · letzter Kontakt gestern · nächstes Meeting Di., 27. Okt.“). Der letzte Kontakt wird als „gerade eben“, „vor 3 Stunden“, „gestern“ oder „vor 3 Tagen“ angezeigt, ältere Kontakte als Datum. Bewege den Mauszeiger darüber, um das genaue Datum zu sehen. Darunter findest du:

- **Kontakt**: Telefonnummern und E-Mail-Adressen. Tippe auf eine, um anzurufen oder zu schreiben, oder auf **Kopieren**. Auch der **Geburtstag** wird hier angezeigt, mit der Quelle (Google Kontakte, Google Kalender, Facebook, deine Notizen oder du): siehe [Graph](graph.md#birthday).
- **Mit dir**: welche Rolle die Person für dich hat, ob sie ein Arbeits- oder Privatkontakt ist und ob sie zu deiner Familie oder deinem Fleet gehört, mit **In Fleet ansehen**.
- **Auch auf**: die anderen Orte, an denen ihr miteinander sprecht. **Slack** öffnet die Person in Slack oder euren neuesten Slack-Chat.
- **Personen** und **Projekte**, zu denen die Person gehört, **Offen zwischen euch** (Versprechen in beide Richtungen, mit **Als erledigt markieren** und **Fallen lassen**) und ihr **Verlauf**.

Adressen und Chats einer Person werden automatisch zusammengeführt, wenn klar ist, dass sie zu einer Person gehören, etwa eine geschäftliche E-Mail-Adresse mit der eigenen Adresse in CC.

Wenn auf einer Seite **Diese Seite konnte nicht geladen werden.** steht, tippe auf **Erneut versuchen**. Wenn die Meldung weiterhin angezeigt wird, tippe unten auf der Seite auf **Stimmt etwas nicht?**.

## Zusammenfassung

Ein paar kurze Zeilen oben auf der Seite einer Person: was besprochen, gefragt, geplant oder versprochen wurde, mit allen Namen. The Machine schreibt sie neu, wenn es etwas Neues gibt, aber nur für Personen, mit denen du wirklich in Kontakt bist, und prüft jede Zeile vorher. Normalerweise einmal am Tag, innerhalb weniger Stunden, wenn sich etwas mit der Person ändert, etwa eine neue Frist oder eine zurückgezogene Anfrage.

Vage Zeilen werden ausgelassen. Wenn es nichts Konkretes zu sagen gibt, gibt es keine Zusammenfassung. Jede Zeile verweist auf ihre Quelle: Nachrichten von einem Tag werden mit einem gemeinsamen Datum und ihrer Anzahl angezeigt und lassen sich zusammen öffnen.

Mit **Bearbeiten** formulierst du sie nach deinen Vorstellungen. Wenn es Neuigkeiten gibt, zeigt The Machine eine **Vorgeschlagene Aktualisierung** mit **Übernehmen** und **Meine behalten**. Mit **The Machine schreiben lassen** gibst du die Zusammenfassung wieder an The Machine zurück.

Vorbereitungen für Meetings verwenden sie, aber nur die Zeilen aus dem Bereich der jeweiligen Aufgabe (Arbeit oder Privat). Sie bleibt auf deiner Machine. Dein Team sieht sie nie.

## Verlauf

Jede Seite einer Person oder Organisation hat einen Verlauf, neueste Einträge zuerst: E-Mails, Meetings und ihre Zoom-Zusammenfassungen, Intercom-Unterhaltungen (mit **In Intercom öffnen**), Chats auf WhatsApp, Telegram, Slack, LinkedIn und X, Aufgaben, Versprechen und Projektänderungen. Mit den Chips oben kannst du jeweils eine Quelle auswählen. **Mehr anzeigen** lädt ältere Einträge.

Bevorstehende Meetings stehen ganz oben unter **Demnächst**, nach Zeit sortiert. **Alle anstehenden zeigen** zeigt die übrigen. Bei einem Meeting siehst du, wer dabei war, jede Person nur einmal. Bei Meetings mit Notizen oder Transkript steht **Notizen** oder **Transkript**. Klicke darauf, um sie zu lesen.

Deine Verläufe gehören dir: Im Graph des Teams wird nur angezeigt, was deine Freigabeeinstellungen erlauben. Auf einer Seite zeigt **Team** über dem Verlauf die von Teammitgliedern geteilten Einträge an, jeweils mit Angabe der Person, von der sie stammen. **Meine** zeigt nur deine Einträge.

## Arbeit und Privat

Auf den Tabs **Arbeit** und **Privat** werden Personen nach ihrem Typ sortiert, der auch auf ihrer Seite steht. Deine eigene Auswahl (**Bearbeiten**) hat Vorrang. Ansonsten werden deine Familie und Freunde sowie Personen, für die du Familie oder Freund bist (eine Ehefrau, ein Vater), als privat eingestuft, unabhängig davon, von welcher Adresse aus sie schreiben. Dein Team sieht keine privaten Kontakte.

## Person hinzufügen

Tippe oben in Personen auf **Neue Person** oder auf dem Smartphone in der oberen Leiste auf **+**. Gib einen Namen und, falls vorhanden, eine E-Mail-Adresse und Organisation ein. Wenn es in deinem Graph bereits eine ähnliche Person gibt, wird sie im Formular zuerst angezeigt. Du kannst dann stattdessen diese Person öffnen. Mit **Hinzufügen** öffnest du die neue Seite.

Eine Person, die du hinzufügst, bleibt auch ohne Nachrichten erhalten. Ihre erste Nachricht wird ihr zugeordnet.

## Person bearbeiten

Mit **Bearbeiten** oben auf der Seite änderst du den Namen, die Berufsbezeichnung, die Organisation, den Ort, LinkedIn, Telefonnummern und E-Mail-Adressen, die Beziehung zu dir sowie die Angabe „Arbeit“ oder „Privat“. Das Feld **Notizen** ist für alles, woran du dich erinnern möchtest. Notizen bleiben beim Zusammenführen erhalten. Mit **Speichern** übernimmst du die Änderungen, mit **Abbrechen** verwirfst du sie.

Deine Änderungen bleiben erhalten, auch wenn die Personendaten erneut nachgeschlagen oder Personen mit **Zusammenführen** und **Rückgängig** bearbeitet werden. Leere ein Feld, um wieder den nachgeschlagenen Wert zu verwenden. Wenn du den Namen leerst, wird der Name aus den Nachrichten wiederhergestellt.

Um das Foto zu ändern, klicke darauf: **Bild hochladen**, ein gefundenes Foto auswählen oder **Bild entfernen**. Das Foto bleibt auf deiner Machine.

## Zwei Personen zusammenführen

Wenn zwei Personen möglicherweise dieselbe Person sind, wird auf ihrer Seite gefragt, ob sie dieselbe Person sind. In Personen werden sie unter **Gleiche Person?** aufgeführt. Mit **Zusammenführen** werden sie samt Nachrichten, Notizen, Rollen und Projekten zusammengeführt. Mit **Nicht dieselbe** bleiben sie dauerhaft getrennt. Deine Antwort wird kurz beim Paar angezeigt, danach verschwindet es aus der Liste. Die Liste wird ausgeblendet, wenn es nichts mehr zu prüfen gibt.

Jemand mit einer Adresse, die nur einer bekannten Adresse ähnelt, etwa acme-corp.example und acmecorp.example, wird nie als dieselbe Person vorgeschlagen. Nur du kannst dieser Person eine Rolle zuweisen.

Ein Name allein reicht bei zwei verschiedenen Domains nie aus, da jeder einen Namen eingeben kann. Zwei Adressen auf unterschiedlichen Domains werden nur dann vorgeschlagen, wenn es eine weitere Verbindung gibt, etwa dieselben Personen oder ein gemeinsames Projekt. Jemand, der deinen Namen an einer Adresse verwendet, die nicht dir gehört, wird nie vorgeschlagen. Füge stattdessen unter Einstellungen deine anderen Adressen hinzu: [Deine Adressen](settings.md#your-addresses).

Wenn nur der Vorname bei verschiedenen Domains übereinstimmt, etwa „Sam“ und „Sam Lee“, werden die Personen nur bei gleicher Telefonnummer oder gleichem LinkedIn-Profil vorgeschlagen.

Eine gemeinsame Adresse, etwa info@ oder eine Mailingliste, wird nie mit den Personen zusammengeführt, die darüber schreiben. Ein geschäftlicher Kontakt außerhalb deines Unternehmens und ein privater Chat, bei denen nur ein Name übereinstimmt, werden nicht automatisch zusammengeführt. Sie werden als Frage angezeigt.

Mit **Alle zusammenführen** werden alle Paare in der Liste auf einmal zusammengeführt, außer denen, die du mit **Nicht dieselbe** markiert hast. Mit **Rückgängig** kannst du sie direkt danach wieder trennen.

Um zwei Personen selbst zusammenzuführen, öffne eine davon und wähle dann **⋯**, **Gleiche Person wie…** und die andere Person aus. Auf der Seite der zusammengeführten Person steht unter **Zusammengeführt aus**, warum sie zusammengeführt wurde. Mit **Rückgängig** kannst du sie wieder trennen.

## Person endgültig löschen

Öffne auf der Seite der Person das Menü ⋯ und wähle **Endgültig löschen…**, dann **Löschen**. Dadurch werden die Person und alles gelöscht, was deine Machine über sie weiß: ihr Eintrag, ihre Adressen, nachgeschlagene Daten, Nachrichten, die nur zwischen euch beiden ausgetauscht wurden, und Notizen über sie.

Aufgaben, an denen die Person beteiligt ist, bleiben erhalten, aber ihr Name wird daraus entfernt. Sie wird nicht erneut hinzugefügt, auch nicht durch einen Import oder eine Facebook-Geburtstagsaufgabe mit ihrem Namen oder ihrer Adresse. Das lässt sich nicht rückgängig machen.

## Unzustellbar

Wenn eine E-Mail an eine Person nicht zugestellt werden kann, wird ihre Adresse mit **Unzustellbar** und dem Datum angezeigt. Eine andere Adresse der Person wird dann zuerst aufgeführt. Neue Entwürfe werden nie an diese Adresse gesendet, wenn eine andere bekannt ist. Ist es die einzige Adresse, weist dich das Versandfenster darauf hin. Du kannst die E-Mail trotzdem senden.

Eine E-Mail gilt als unzustellbar, wenn der Mailserver meldet, dass die Adresse nicht existiert, oder nach 3 vorübergehenden Fehlern innerhalb einer Woche. Der Hinweis wird entfernt, wenn die Person wieder von dieser Adresse aus schreibt oder eine E-Mail an diese Adresse zugestellt wird.

## Berufsbezeichnung und Foto

Bei Personen mit einer Firmenadresse werden Berufsbezeichnung, Foto, LinkedIn und Stadt wie [Organisationsdaten](organization-data.md) nachgeschlagen. Bei einer gehosteten Machine werden dafür nur ihr Name und die Domain des Unternehmens verwendet. Für ein Foto erhält Gravatar einen Hash ihrer geschäftlichen Adresse, niemals die Adresse selbst. Du kannst das unter **Einstellungen** im Bereich Sicherheit deaktivieren: **Arbeitskontakte nachschlagen**.

Wenn die Daten gefunden wurden, zeigt die Seite außerdem den Infotext der Person, an, seit wann sie ihre aktuelle Rolle hat und welche zwei Rollen sie davor hatte. Auch Vorbereitungen verwenden diese Angaben. Der Infotext wird nur verwendet, wenn die Person keine eigene Biografie hat.

Deine Verbindungen werden durch bereits gelesene Informationen ergänzt: eine Berufsbezeichnung, Telefonnummer und Zeitzone aus Slack, eine Biografie und einen Ort aus X, eine Überschrift und ein Foto aus LinkedIn, Berufsbezeichnungen aus Google Kontakte und Salesflare sowie das Bild eines Kontakts aus Salesflare, wenn Salesflare selbst eines gespeichert hat. Bewege den Mauszeiger über die Zeile unter dem Namen, um zu sehen, woher die Information stammt.

Outlook fügt Fotos von Kolleginnen und Kollegen in deiner Organisation und von deinen Outlook-Kontakten hinzu sowie die Berufsbezeichnungen und Unternehmen deiner Kontakte ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Fotos von WhatsApp und Telegram werden über deine WhatsApp-Synchronisierung und die Verbindung zu deinen Telegram-Chats hinzugefügt: bis zu 50 pro Tag je Dienst, nur für Personen, die bereits in deinem Graph sind. An diese Personen wird nichts gesendet. Ein Facebook-Geburtstagsimport fügt beim Speichern das Profilbild einer Person hinzu, wenn noch kein Foto vorhanden ist ([Routinen](routines.md)). Alles bleibt auf deiner Machine.

In einem Work Fleet wird in der [Team-Graph](team-graph.md)-Ansicht eine kleine Kopie eines geschäftlichen Fotos zusammen mit dem geteilten Eintrag einer Person angezeigt. Fotos aus Google Kontakte, WhatsApp, Telegram oder Facebook sowie Fotos, die du geändert oder entfernt hast, werden nie geteilt.

## Über dich

Deine eigenen Adressen und Nummern, auch Aliasse, gehören immer dir und sind nie eine andere Person in deinem Graph. Wenn du nach dir selbst suchst oder eine Person mit einer deiner Adressen hinzufügst, wird **Über dich** geöffnet. Beim Import wird dein eigener Eintrag übersprungen.

Unter „Über dich“ sind deine Adressen und ihre jeweiligen Quellen aufgeführt. Ändere sie unter **Einstellungen** im Bereich Konto. Um deinen Kontakt an ein Teammitglied oder einen Freund zu senden, wähle **Meinen Kontakt teilen**. Siehe [Kontakt teilen](share-contact.md).

## Deine Beziehung zu einer Person

Auf der Seite einer Person werden unter **Für dich** die Rollen angezeigt, die deine Machine in deinen Nachrichten erkennt, zusammen mit der entsprechenden Textstelle. Du musst nichts bestätigen. Stimmt etwas nicht? Korrigiere es mit **Bearbeiten** auf der Seite der Person oder über **⋯** bei der Zeile unter **Letzte Änderungen**. Deine Machine lernt aus deinen Änderungen.

## Was sie über jemanden weiß

Fakten über eine Person stehen auf ihrer Seite unter **Bekannt über**. Unter **Erkenntnisse** werden allgemeine Fakten gesammelt. Mit **Hinzufügen** kannst du einen weiteren Fakt in deinen eigenen Worten hinzufügen. Zu jedem Fakt gibt es ein Menü:

- **Bearbeiten** ändert den Fakt direkt.
- Mit **Nicht über** wird der Fakt wieder zu einem allgemeinen Fakt unter **Erkenntnisse**, **Fakten**.
- **Entfernen** löscht ihn überall.

## Letzte Änderungen

Unter **Letzte Änderungen**, direkt über dem Verlauf einer Person, Organisation oder eines Projekts, steht, was deine Machine über sie geändert oder gelernt hat: eine Rolle, wo jemand arbeitet, die Beziehung zwischen zwei Personen, ein Fakt oder eine Änderung an einem Projekt. Jede Zeile zeigt das Datum und die Quelle. Tippe auf die Quelle, um die Nachricht zu lesen.

Wenn eine Angabe falsch ist, kannst du sie über **⋯** direkt korrigieren: **Bearbeiten**, **Entfernen**, **Nicht über** oder **Rückgängig**, um ein Projekt an seinen vorherigen Ort zurückzusetzen. Drei Zeilen werden angezeigt. Mit **Mehr anzeigen** siehst du die übrigen.

Bei einer Person, deren Angaben deine Machine heute aktualisiert hat, erscheint in der Personenliste ein kleiner Punkt. Oben in der Liste steht **Heute aktualisierte Personen: 4**, gefolgt von den Namen. Siehe [Graph](graph.md).

## Aufgabe zu einer Person

Mit **Neue Aufgabe** im Menü **⋯** einer Person, Organisation oder eines Projekts erstellst du eine Aufgabe zu dieser Person, Organisation oder diesem Projekt.
