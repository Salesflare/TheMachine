---
title: Personen
area: graph
summary: Alle, mit denen du Kontakt hast: ihre Seite, Zusammenfassung und ihr Verlauf sowie Anleitungen zum Hinzufügen, Bearbeiten, Zusammenführen oder Löschen.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: b23d3ebdc4f162f2
---
Alle, mit denen du Kontakt hast, nach Nähe sortiert, aus deinen Nachrichten und Meetings. Newsletter, Belege und andere Serienmails fügen niemanden hinzu, bis du antwortest. Sie stehen unter „Verborgene Absender“ unterhalb der Liste. Mit „Als Person anzeigen“ wird jemand hinzugefügt. Felder, Tags und Import funktionieren in allen drei Listen gleich, und jede Liste hat eigene Filter: siehe [The Graph](graph.md).

Ein gemeinsames Postfach (info@, Kundenservice, der Name eines Geschäfts) zählt zu seiner Organisation, nicht als Person, auch wenn du dorthin schreibst.

## Die Seite einer Person

Oben stehen Foto, Name, Titel, Organisation und Ort sowie eine Zeile dazu, wie du mit der Person in Kontakt bist („Täglicher Austausch · letzter Kontakt gestern · nächstes Meeting Di., 27. Okt.“). Der letzte Kontakt wird als „gerade eben“, „vor 3 Stunden“, „gestern“ oder „vor 3 Tagen“ angezeigt. Bei länger zurückliegenden Kontakten steht dort ein Datum. Fahre mit der Maus darüber, um das genaue Datum zu sehen. Darunter findest du:

- **Kontakt**: Telefonnummern und E-Mail-Adressen. Tippe auf eine, um anzurufen oder zu schreiben, oder tippe auf **Kopieren**. Auch der **Geburtstag** wird hier angezeigt, zusammen mit der Quelle (Google Kontakte, Google Kalender, Facebook, deine Notizen oder du): siehe [The Graph](graph.md#birthday).
- **Mit dir**: welche Rolle die Person für dich hat, ob sie ein Arbeits- oder Privatkontakt ist und zu deiner Family oder Fleet gehört, mit **In Fleet ansehen**.
- **Auch auf**: die anderen Orte, an denen ihr miteinander sprecht. **Slack** öffnet die Person in Slack oder euren neuesten Slack-Thread.
- **Personen** und **Projekte**, zu denen sie gehört, **Offen zwischen euch** (gegenseitige Versprechen, mit **Als erledigt markieren** und **Entfernen**) sowie ihr **Verlauf**.

Adressen und Chats werden automatisch derselben Person zugeordnet, wenn klar ist, dass sie zusammengehören, zum Beispiel eine geschäftliche E-Mail-Adresse und die persönliche Adresse in CC. Oder wenn jemand, mit dem du chattest, über den Link, den du der Person geschickt hast, einen Anruf bucht und der Firmenname oder Nachname übereinstimmt.

Wenn auf einer Seite **Diese Seite konnte nicht geladen werden.** steht, tippe auf **Erneut versuchen**. Wenn die Meldung weiterhin erscheint, tippe unten auf der Seite auf **Stimmt etwas nicht?**.

## Zusammenfassung

Oben auf der Seite einer Person stehen ein paar kurze Zeilen dazu, was besprochen, gefragt, geplant oder versprochen wurde, mit allen Namen. The Machine schreibt die Zusammenfassung um, wenn es etwas Neues gibt, und zwar nur für Personen, mit denen du wirklich Kontakt hast. Jede Zeile wird vorher geprüft. Meistens geschieht das einmal am Tag, bei Änderungen an einer Sache mit der Person aber innerhalb weniger Stunden, zum Beispiel bei einer neuen Frist oder wenn eine Anfrage zurückgezogen wird.

Vage Aussagen werden weggelassen. Wenn es nichts Konkretes zu sagen gibt, erscheint keine Zusammenfassung. Jede Zeile verweist auf ihre Quelle: Nachrichten vom selben Tag werden mit Datum und Anzahl zusammengefasst und lassen sich gemeinsam öffnen.

Mit **Bearbeiten** kannst du die Zusammenfassung nach deinen Vorstellungen formulieren. Wenn es Neuigkeiten gibt, zeigt The Machine eine **Vorgeschlagene Aktualisierung** mit **Übernehmen** und **Meine behalten**. Mit **The Machine schreiben lassen** gibst du die Zusammenfassung wieder ab.

Bei der Vorbereitung auf Meetings wird sie verwendet, allerdings nur die Zeilen, die zu diesem Bereich der Aufgabe gehören: Arbeit oder Privat. Sie bleibt auf deiner Machine. Dein Team sieht sie nicht.

## Verlauf

Jede Personen- und Organisationsseite hat einen Verlauf, neueste Einträge zuerst: E-Mails, Meetings und deren Zoom-Zusammenfassungen, Intercom-Unterhaltungen (mit **In Intercom öffnen**), WhatsApp-, Telegram-, Slack-, LinkedIn- und X-Chats, Aufgaben, Versprechen und Projektänderungen. Mit den Chips oben kannst du jeweils eine Quelle anzeigen. **Mehr anzeigen** lädt ältere Einträge.

Anstehende Meetings stehen ganz oben unter **Demnächst**, zuerst die zeitlich nächsten. Mit **Alle anstehenden zeigen** siehst du den Rest. Bei einem Meeting wird angezeigt, wer daran teilgenommen hat, jede Person nur einmal. Bei Meetings mit Notizen oder Transkript steht **Notizen** oder **Transkript**. Klicke darauf, um sie zu lesen.

Deine Verläufe gehören dir. Im Graph deines Teams werden nur Inhalte angezeigt, die deine Freigabeeinstellungen erlauben. Auf einer Seite kannst du über **Team** oberhalb des Verlaufs geteilte Inhalte deiner Teammitglieder hinzufügen. Bei jedem Eintrag steht, von wem er stammt. **Meine** zeigt nur deine Inhalte.

## Arbeit und Privat

In den Tabs **Arbeit** und **Privat** werden Personen nach ihrem Typ sortiert, der auf ihrer Seite angezeigt wird. Deine eigene Auswahl (**Bearbeiten**) hat Vorrang. Ansonsten werden deine Family und Friends sowie Familienmitglieder oder Freunde von dir (zum Beispiel eine Ehefrau oder ein Vater) als privat eingestuft, unabhängig davon, von welcher Adresse sie schreiben. Dein Team sieht keine privaten Kontakte.

## Person hinzufügen

Tippe oben in „Personen“ auf **Neue Person** oder auf einem Handy in der oberen Leiste auf **+**. Gib einen Namen ein sowie, falls vorhanden, eine E-Mail-Adresse und eine Organisation. Wenn sich eine ähnliche Person bereits in deinem Graph befindet, wird sie im Formular zuerst angezeigt. So kannst du stattdessen die vorhandene Person öffnen. Mit **Hinzufügen** öffnest du die neue Seite.

Eine Person, die du hinzufügst, bleibt auch dann erhalten, wenn es noch keine Nachrichten gibt. Die erste Nachricht wird ihr zugeordnet.

## Person bearbeiten

Mit **Bearbeiten** oben auf der Seite kannst du Name, Titel, Organisation, Standort, LinkedIn, Telefonnummern und E-Mail-Adressen, die Beziehung zu dir sowie die Einstufung als Arbeit oder Privat ändern. Das Feld **Notizen** ist für alles gedacht, woran du dich erinnern möchtest. Notizen bleiben beim Zusammenführen erhalten. Mit **Speichern** werden die Änderungen übernommen, mit **Abbrechen** verworfen.

Deine Änderungen bleiben erhalten, auch wenn die Angaben erneut abgerufen oder Personen **Zusammenführen** und wieder **Rückgängig** gemacht werden. Leere ein Feld, um wieder den abgerufenen Wert zu verwenden. Wenn du den Namen leerst, wird wieder der Name aus den Nachrichten verwendet.

Um das Foto zu ändern, klicke darauf: **Bild hochladen**, eines der gefundenen Fotos auswählen oder **Bild entfernen**. Das Foto bleibt auf deiner Machine.

## Zwei Personen zusammenführen

Wenn zwei Personen möglicherweise dieselbe Person sind, fragt ihre Seite, ob es sich um dieselbe Person handelt. In „Personen“ werden sie unter **Gleiche Person?** aufgelistet. Mit **Zusammenführen** werden alle ihre Nachrichten, Notizen, Rollen und Projekte zusammengeführt. Mit **Nicht dieselbe** bleiben sie dauerhaft getrennt. Deine Antwort wird kurz beim Paar angezeigt. Danach verschwindet es aus der Liste. Die Liste wird ausgeblendet, sobald es keine offenen Fragen mehr gibt.

Jemand mit einer Adresse, die einer bekannten Adresse nur ähnelt, zum Beispiel acme-corp.example statt acmecorp.example, wird nie als dieselbe Person vorgeschlagen. Nur du kannst dieser Person eine Rolle zuweisen.

Ein gleicher Name reicht bei verschiedenen Domains nie aus, denn jeder kann einen Namen eingeben. Zwei Adressen mit unterschiedlichen Domains werden nur dann als dieselbe Person vorgeschlagen, wenn es weitere Verbindungen gibt, etwa gemeinsame Kontakte oder ein gemeinsames Projekt. Jemand, der deinen Namen an einer Adresse verwendet, die nicht dir gehört, wird nie vorgeschlagen. Füge stattdessen deine weiteren Adressen unter „Einstellungen“ unter [Deine Adressen](settings.md#your-addresses) hinzu.

Wenn bei verschiedenen Domains nur der Vorname übereinstimmt, zum Beispiel „Sam“ und „Sam Lee“, werden die Personen nur bei gleicher Telefonnummer oder gleichem LinkedIn-Profil vorgeschlagen.

Wenn nur der Vorname mit einem Meeting aus einem Chat übereinstimmt oder die Adresse zu jemandem gehört, den du bereits kanntest, und nur die Person im Chat sagt, dass die Adresse ihr gehört, wirst du gefragt. The Machine öffnet niemals einen Link, um das herauszufinden.

Eine gemeinsame Adresse, zum Beispiel info@ oder eine Mailingliste, wird nie den Personen zugeordnet, die darüber schreiben. Ein geschäftlicher Kontakt außerhalb deines Unternehmens und ein privater Chat mit nur einem gemeinsamen Namen werden nicht automatisch zusammengeführt. Sie werden als offene Frage aufgeführt.

Mit **Alle zusammenführen** werden alle Paare in der Liste gleichzeitig zusammengeführt, außer denen, die du mit **Nicht dieselbe** markiert hast. Mit **Rückgängig** direkt danach werden sie alle wieder getrennt.

Um zwei Personen selbst zusammenzuführen, öffne eine der Seiten und wähle dann **⋯**, **Gleiche Person wie…** und die andere Person. Auf der Seite einer zusammengeführten Person steht unter **Zusammengeführt aus**, warum sie zusammengeführt wurde. Mit **Rückgängig** kannst du sie wieder trennen.

## Person endgültig löschen

Öffne auf der Seite der Person das Menü ⋯ und wähle **Endgültig löschen…**, dann **Löschen**. Dadurch werden die Person und alles, was deine Machine über sie weiß, entfernt: ihr Eintrag, Adressen, abgerufene Angaben, Nachrichten, die nur zwischen euch beiden ausgetauscht wurden, sowie Notizen über sie.

Aufgaben, an denen die Person beteiligt ist, bleiben erhalten, aber ihr Name wird daraus entfernt. Sie wird nicht erneut hinzugefügt, auch nicht durch einen Import oder eine Geburtstagsaufgabe von Facebook mit ihrem Namen oder ihrer Adresse. Das lässt sich nicht rückgängig machen.

## Unzustellbar

Wenn eine E-Mail an jemanden unzustellbar ist, wird die Adresse mit dem Datum als **Unzustellbar** angezeigt, und eine andere Adresse dieser Person rückt nach oben. Neue Entwürfe werden nie an diese Adresse gesendet, wenn eine andere bekannt ist. Ist es die einzige Adresse, warnt dich das Versandfenster, aber du kannst trotzdem senden.

Eine E-Mail gilt als unzustellbar, wenn der Mailserver meldet, dass die Adresse nicht existiert, oder nach 3 vorübergehenden Fehlern innerhalb einer Woche. Der Hinweis wird entfernt, wenn die Person wieder von dieser Adresse schreibt oder eine E-Mail an sie zugestellt wird.

## Berufsbezeichnung und Foto

Bei Personen mit einer Firmenadresse werden Berufsbezeichnung, Foto, LinkedIn und Stadt abgerufen, wie unter [Organisationsangaben](organization-data.md) beschrieben. Bei einer gehosteten Machine werden dafür nur der Name und die Firmendomain abgerufen. Für ein Foto erhält Gravatar einen Hash der geschäftlichen Adresse, niemals die Adresse selbst. Deaktiviere die Funktion in **Einstellungen** unter „Sicherheit“ mit **Arbeitskontakte nachschlagen**.

Mit dieser Einstellung wird auch verhindert, dass vor dem ersten Meeting die Website aufgerufen wird und eine Websuche stattfindet, wenn ein Suchanbieter eingerichtet ist (siehe [Bereit für deine Meetings](calendar.md#ready-for-your-meetings)).

Wenn die Angaben abgerufen wurden, zeigt die Seite außerdem den Infotext, den Beginn der aktuellen Position und die beiden vorherigen Positionen. Auch die Vorbereitungen greifen darauf zurück. Der Infotext wird dort nur verwendet, wenn keine eigene Biografie vorhanden ist.

Deine Verbindungen werden durch Angaben ergänzt, die sie bereits gelesen haben: Berufsbezeichnung, Telefonnummer und Zeitzone aus Slack, Biografie und Ort aus X, Überschrift und Foto aus LinkedIn, Berufsbezeichnungen aus Google Kontakte und Salesflare sowie das Kontaktfoto aus Salesflare, wenn dort eines gespeichert ist. Fahre mit der Maus über die Zeile unter dem Namen, um die Quelle zu sehen.

Outlook fügt Fotos von Kolleginnen und Kollegen in deiner Organisation sowie deinen Outlook-Kontakten hinzu, außerdem Berufsbezeichnungen und Unternehmen deiner Kontakte ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

WhatsApp- und Telegram-Fotos werden über deine WhatsApp-Synchronisierung und deine Telegram-Chatverbindung abgerufen: bis zu 50 pro Tag und Dienst, nur für Personen, die bereits in deinem Graph sind. Es wird nichts an diese Personen gesendet. Ein Facebook-Geburtstagsimport fügt das Profilbild einer Person ohne Foto hinzu, wenn du es speicherst ([Routinen](routines.md)). Alles bleibt auf deiner Machine.

Im [Team Graph](team-graph.md) einer Work Fleet wird eine kleine Kopie eines geschäftlichen Fotos zusammen mit dem geteilten Eintrag einer Person angezeigt. Fotos aus Google Kontakte, WhatsApp, Telegram oder Facebook sowie Fotos, die du geändert oder entfernt hast, werden nie geteilt.

## Über dich

Deine eigenen Adressen und Telefonnummern, auch Aliase, gehören immer zu dir und nie zu jemandem in deinem Graph. Wenn du nach dir selbst suchst oder eine Person mit einer deiner Adressen hinzufügst, wird **Über dich** geöffnet. Beim Import wird dein eigener Eintrag übersprungen.

Unter „Über dich“ werden deine Adressen und ihre jeweiligen Quellen aufgelistet. Du kannst sie in **Einstellungen** unter „Konto“ ändern. Um deinen Kontakt an ein Teammitglied oder einen Freund zu senden, wähle **Meinen Kontakt teilen**. Siehe [Einen Kontakt teilen](share-contact.md).

## Welche Rolle jemand für dich hat

Rollen, die deine Machine in deinen Nachrichten erkennt, stehen auf der Seite der Person unter **Für dich**. Angezeigt werden nur die Wörter, die auf die Rolle hinweisen, zum Beispiel eine Berufsbezeichnung. Wenn jemand sagt, dass er dein Steuerberater oder Kunde ist, reicht das nicht aus. Dafür braucht es auch etwas von deiner Seite, zum Beispiel eigene Nachrichten oder Meetings mit der Person. Du musst nichts bestätigen. Stimmt etwas nicht? Mit **Bearbeiten** auf der Seite oder **⋯** in der entsprechenden Zeile unter **Letzte Änderungen** kannst du es korrigieren. The Machine lernt aus deinen Änderungen.

## Was über jemanden bekannt ist

Fakten über eine Person stehen auf ihrer Seite unter **Über sie bekannt**. Allgemeine Fakten findest du unter „Lernen“. Mit **Hinzufügen** kannst du einen weiteren Fakt in deinen eigenen Worten festhalten. Für jeden Fakt gibt es ein Menü:

- Mit **Bearbeiten** kannst du ihn direkt ändern.
- Mit **Nicht über sie** wird daraus wieder ein allgemeiner Fakt unter **Lernen**, **Fakten**.
- Mit **Entfernen** wird er überall gelöscht.

## Letzte Änderungen

Unter **Letzte Änderungen**, direkt über dem Verlauf einer Person, Organisation oder eines Projekts, werden die Änderungen und neuen Erkenntnisse deiner Machine dazu aufgeführt: eine Rolle, der Arbeitsort, die Beziehung zwischen zwei Personen, ein Fakt oder eine Projektänderung. In jeder Zeile stehen Datum und Quelle. Tippe auf die Quelle, um die Nachricht zu lesen.

Wenn etwas nicht stimmt, kannst du es über **⋯** direkt in der Zeile korrigieren: **Bearbeiten**, **Entfernen**, **Nicht über sie** oder **Rückgängig**, um ein Projekt an seinen vorherigen Ort zurückzusetzen. Es werden drei Zeilen angezeigt. Mit **Mehr anzeigen** siehst du den Rest.

Bei einer Person, deren Angaben deine Machine heute aktualisiert hat, erscheint ein kleiner Punkt in der Personenliste. Oben in der Liste steht außerdem **Heute 4 Personen aktualisiert** und nennt die Personen. Siehe [The Graph](graph.md).

## Aufgabe zu einer Person

Mit **Neue Aufgabe** im Menü **⋯** einer Person, Organisation oder eines Projekts startest du eine Aufgabe dazu.
