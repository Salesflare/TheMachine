---
title: Personen
area: graph
summary: Alle, mit denen du in Kontakt bist: ihre Seite, Zusammenfassung und ihr Verlauf sowie wie du Personen hinzufügst, bearbeitest, zusammenführst oder löschst.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: a16cc66e51a64fd2
---
Alle, mit denen du in Kontakt bist, nach Nähe sortiert, aus deinen Nachrichten und Meetings. Newsletter, Belege und andere Rundmails fügen niemanden hinzu, bis du antwortest. Sie stehen unter „Ausgeblendete Absender“ unterhalb der Liste. Mit **Als Person anzeigen** wird jemand hinzugefügt. Felder, Tags und Importe funktionieren in allen drei Listen gleich, und jede Liste hat eigene Filter: siehe [The Graph](graph.md).

Ein gemeinsames Postfach (info@, Kundenservice, der Name eines Shops) zählt zu der Organisation, nicht als Person, auch nachdem du dorthin geschrieben hast.

## Seite einer Person

Oben stehen Foto, Name, Titel, Organisation und Ort sowie eine Zeile dazu, wie ihr in Kontakt seid („Täglicher Austausch · letzter Kontakt gestern · nächstes Meeting Di., 27. Okt.“). Der letzte Kontakt wird als „gerade eben“, „vor 3 Stunden“, „gestern“ oder „vor 3 Tagen“ angezeigt, bei länger zurückliegenden Kontakten als Datum. Bewege den Mauszeiger darüber, um das genaue Datum zu sehen. Darunter findest du:

- **Kontakt**: Telefonnummern und E-Mail-Adressen. Tippe auf eine, um anzurufen oder zu schreiben, oder auf **Kopieren**. Auch der **Geburtstag** wird hier angezeigt, mit Angabe der Quelle (Google-Kontakte, Google Kalender, Facebook, deine Notizen oder du selbst): siehe [The Graph](graph.md#birthday).
- **Mit dir**: welche Rolle die Person für dich hat, ob sie ein Kontakt aus Arbeit oder Privat ist und ob sie zu deiner Familie oder Fleet gehört, mit **In Fleet ansehen**.
- **Auch auf**: die anderen Orte, an denen ihr miteinander kommuniziert. Über **Slack** öffnest du die Person in Slack oder euren neuesten Slack-Thread.
- **Personen** und **Projekte**, an denen sie beteiligt ist, **Offen zwischen euch** (Versprechen in beide Richtungen, mit **Als erledigt markieren** und **Fallen lassen**) und ihr **Verlauf**.

Adressen und Chats einer Person werden automatisch zusammengeführt, wenn klar ist, dass sie zu einer Person gehören, zum Beispiel eine geschäftliche E-Mail-Adresse mit der persönlichen Adresse der Person in CC.

Wenn auf einer Seite **Diese Seite konnte nicht geladen werden.** steht, tippe auf **Erneut versuchen**. Wenn die Meldung weiterhin angezeigt wird, nutze **Stimmt etwas nicht?** unten auf der Seite.

## Zusammenfassung

Ein paar kurze Zeilen oben auf der Seite einer Person: was besprochen, gefragt, geplant oder versprochen wurde, mit allen genannten Personen. The Machine schreibt sie um, wenn es etwas Neues gibt, nur für Personen, mit denen du wirklich in Kontakt bist, und prüft jede Zeile vorher. In der Regel einmal täglich, bei Änderungen an einer Angelegenheit mit der Person innerhalb weniger Stunden, zum Beispiel bei einer neuen Frist oder einer zurückgezogenen Bitte.

Vage Aussagen werden ausgelassen. Gibt es nichts Konkretes zu sagen, gibt es keine Zusammenfassung. Jede Zeile verweist auf ihre Quelle: Nachrichten von einem Tag teilen sich ein Datum mit der Anzahl und lassen sich gemeinsam öffnen.

Mit **Bearbeiten** kannst du die Zusammenfassung in deinen eigenen Worten formulieren. Wenn es Neuigkeiten gibt, zeigt The Machine eine **Vorgeschlagene Aktualisierung** mit **Übernehmen** und **Meine behalten**. Über **The Machine schreiben lassen** gibst du die Zusammenfassung wieder an The Machine zurück.

Vorbereitungen für Meetings verwenden die Zusammenfassung, aber nur die Zeilen von der jeweiligen Seite der Aufgabe (Arbeit oder Privat). Sie bleibt auf deiner Machine. Dein Team sieht sie nie.

## Verlauf

Jede Seite einer Person oder Organisation hat einen Verlauf, sortiert vom neuesten zum ältesten: E-Mails, Meetings und ihre Zoom-Zusammenfassungen, Intercom-Unterhaltungen (mit **In Intercom öffnen**), Chats in WhatsApp, Telegram, Slack, LinkedIn und X, Aufgaben, Versprechen und Projektänderungen. Über die Chips oben kannst du jeweils eine Quelle anzeigen. Mit **Mehr anzeigen** werden ältere Einträge geladen.

Anstehende Meetings stehen oben unter **Demnächst**, das nächste zuerst. **Alle anstehenden zeigen** zeigt die übrigen. Bei einem Meeting wird angezeigt, wer dabei war, jede Person nur einmal. Ein Meeting mit Notizen oder Transkript ist mit **Notizen** oder **Transkript** gekennzeichnet. Klicke darauf, um sie zu lesen.

Deine Verläufe gehören dir. Im Graph des Teams wird nur angezeigt, was deine Freigabeeinstellungen erlauben. Über **Team** oberhalb des Verlaufs einer Seite werden Inhalte angezeigt, die Teammitglieder geteilt haben. Bei jedem Eintrag steht, von wem er stammt. **Meine** zeigt nur deine Inhalte.

## Arbeit und Privat

Die Tabs **Arbeit** und **Privat** listen Personen nach ihrem Typ auf, der auch auf ihrer Seite steht. Deine eigene Auswahl über **Bearbeiten** hat Vorrang. Ansonsten zählen deine Familie und Freunde sowie Personen, die für dich Familie oder Freunde sind (zum Beispiel eine Ehefrau oder ein Vater), als Privat, unabhängig davon, von welcher Adresse aus sie schreiben. Dein Team sieht private Kontakte nie.

## Person hinzufügen

Wähle oben in „Personen“ **Neue Person** oder auf dem Smartphone **+** in der oberen Leiste. Gib einen Namen und, falls vorhanden, eine E-Mail-Adresse und Organisation ein. Wenn es in deinem Graph bereits eine ähnliche Person gibt, wird sie im Formular zuerst angezeigt. Du kannst stattdessen ihre Seite öffnen. Mit **Hinzufügen** wird die neue Seite geöffnet.

Eine Person, die du hinzufügst, bleibt auch dann erhalten, wenn es noch keine Nachrichten gibt. Die erste Nachricht wird ihr zugeordnet.

## Person bearbeiten

Mit **Bearbeiten** oben auf der Seite kannst du Name, Titel, Organisation, Ort, LinkedIn, Telefonnummern und E-Mail-Adressen, die Rolle der Person für dich sowie Arbeit oder Privat ändern. Das Feld **Notizen** ist für alles, woran du dich erinnern möchtest. Notizen bleiben auch nach dem Zusammenführen erhalten. Mit **Speichern** übernimmst du die Änderungen, mit **Abbrechen** verwirfst du sie.

Deine Änderungen bleiben erhalten, auch wenn die Angaben erneut nachgeschlagen werden sowie nach **Zusammenführen** und **Rückgängig**. Leere ein Feld, um wieder den nachgeschlagenen Wert zu verwenden. Ist das Namensfeld leer, wird der Name aus den Nachrichten wieder angezeigt.

Um das Bild zu ändern, klicke darauf: **Bild hochladen**, ein gefundenes Bild für die Person auswählen oder **Bild entfernen**. Das Bild bleibt auf deiner Machine.

## Zwei Personen zusammenführen

Wenn zwei Personen möglicherweise dieselbe Person sind, fragt ihre Seite, ob es sich um dieselbe Person handelt. In „Personen“ werden sie unter **Gleiche Person?** aufgeführt. Mit **Zusammenführen** werden sie samt Nachrichten, Notizen, Rollen und Projekten zusammengeführt. **Nicht dieselbe** hält sie dauerhaft getrennt. Deine Antwort wird kurz beim Personenpaar angezeigt, danach verschwindet es aus der Liste. Die Liste wird ausgeblendet, wenn es keine offenen Fragen mehr gibt.

Eine Person mit einer Adresse, die nur einer dir bekannten Adresse ähnelt, zum Beispiel acme-corp.example statt acmecorp.example, wird nie als dieselbe Person vorgeschlagen. Nur du kannst ihr eine Rolle zuweisen.

Ein Name allein reicht bei zwei verschiedenen Domains nie aus, denn jeder kann einen Namen eingeben. Zwei Adressen von unterschiedlichen Domains werden nur dann zum Zusammenführen vorgeschlagen, wenn etwas anderes sie miteinander verbindet, zum Beispiel dieselben Personen oder ein Projekt. Eine Person, die deinen Namen an einer Adresse verwendet, die nicht dir gehört, wird nie vorgeschlagen. Füge stattdessen deine anderen Adressen unter Einstellungen hinzu: [Deine Adressen](settings.md#your-addresses).

Wenn bei unterschiedlichen Domains nur der Vorname übereinstimmt, zum Beispiel „Sam“ und „Sam Lee“, werden die Personen nur bei gleicher Telefonnummer oder gleichem LinkedIn-Profil vorgeschlagen.

Eine gemeinsame Adresse wie info@ oder eine Mailingliste wird nie mit den Personen zusammengeführt, die darüber schreiben. Ein geschäftlicher Kontakt von außerhalb deines Unternehmens und ein privater Chat, bei denen nur der Name übereinstimmt, werden nicht automatisch zusammengeführt. Sie werden als offene Frage aufgeführt.

Mit **Alle zusammenführen** werden alle Paare in der Liste auf einmal zusammengeführt, außer denen, die du mit **Nicht dieselbe** markiert hast. Mit **Rückgängig** direkt danach werden alle wieder getrennt.

Um zwei Personen selbst zusammenzuführen, öffne eine der beiden Seiten, dann **⋯**, **Gleiche Person wie…** und wähle die andere Person aus. Auf der Seite der zusammengeführten Person steht unter **Zusammengeführt aus**, warum sie zusammengeführt wurde. Mit **Rückgängig** kannst du sie wieder trennen.

## Person endgültig löschen

Öffne auf der Seite der Person das Menü ⋯ und wähle **Endgültig löschen…**, dann **Löschen**. Dadurch werden die Person und alles gelöscht, was deine Machine über sie weiß: ihr Eintrag, ihre Adressen, nachgeschlagene Angaben, Nachrichten, die nur zwischen euch beiden ausgetauscht wurden, und Notizen über sie.

Aufgaben, an denen die Person beteiligt ist, bleiben erhalten, aber ihr Name wird entfernt. Die Person wird nicht erneut hinzugefügt, auch nicht durch einen Import oder eine Aufgabe zu Facebook-Geburtstagen, in der ihr Name oder ihre Adresse steht. Das lässt sich nicht rückgängig machen.

## Unzustellbar

Wenn eine E-Mail an jemanden unzustellbar ist, wird die Adresse mit **Unzustellbar** und dem Datum angezeigt. Eine andere Adresse der Person wird zuerst aufgeführt. Neue Entwürfe werden nie an diese Adresse gesendet, wenn eine andere bekannt ist. Ist es die einzige Adresse, warnt dich das Versandfenster, aber du kannst die E-Mail trotzdem senden.

Eine E-Mail gilt als unzustellbar, wenn der Mailserver meldet, dass die Adresse nicht existiert, oder nach drei vorübergehenden Fehlern innerhalb einer Woche. Der Hinweis wird entfernt, wenn die Person wieder von dieser Adresse aus schreibt oder eine E-Mail an sie zugestellt wird.

## Jobtitel und Foto

Personen mit einer geschäftlichen Adresse bekommen einen Jobtitel, ein Foto, LinkedIn und eine Stadt. Diese Angaben werden ähnlich wie [Organisationsdaten](organization-data.md) nachgeschlagen. Bei einer gehosteten Machine werden für die Suche nur der Name und die Unternehmensdomain übermittelt. Für ein Foto erhält Gravatar einen Hash der geschäftlichen Adresse, niemals die Adresse selbst. Du kannst das unter **Einstellungen** im Bereich „Sicherheit“ deaktivieren: **Arbeitskontakte nachschlagen**.

Wenn die Angaben gefunden wurden, zeigt die Seite auch den Infotext der Person, seit wann sie ihre aktuelle Rolle innehat und ihre zwei vorherigen Rollen. Vorbereitungen verwenden diese Angaben ebenfalls. Der Infotext wird dabei nur verwendet, wenn die Person keine eigene Biografie hat.

Deine Verbindungen werden durch Angaben ergänzt, die deine Kontakte bereits geteilt haben: Titel, Telefonnummer und Zeitzone aus Slack, Biografie und Ort aus X, Profilüberschrift und Foto aus LinkedIn, Jobtitel aus Google-Kontakten und Salesflare sowie das Bild eines Kontakts aus Salesflare, wenn Salesflare selbst eines gespeichert hat. Bewege den Mauszeiger über die Zeile unter dem Namen, um die Quelle zu sehen.

Outlook fügt Fotos von Kolleginnen und Kollegen in deiner Organisation und von deinen Outlook-Kontakten hinzu sowie Jobtitel und Unternehmen deiner Kontakte ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Bilder aus WhatsApp und Telegram werden über deine WhatsApp-Synchronisierung und deine Telegram-Chatverbindung hinzugefügt: bis zu 50 pro Tag und Dienst, nur für Personen, die bereits in deinem Graph sind. Es wird nichts an sie gesendet. Ein Import von Facebook-Geburtstagen fügt das Profilbild einer Person ohne Foto hinzu, wenn du es speicherst ([Routinen](routines.md)). Alles bleibt auf deiner Machine.

In einer Fleet für Arbeit wird im [Team Graph](team-graph.md) eine kleine Kopie eines geschäftlichen Fotos zusammen mit dem geteilten Eintrag einer Person gespeichert. Bilder aus Google-Kontakten, WhatsApp, Telegram oder Facebook sowie Bilder, die du geändert oder entfernt hast, werden nie geteilt.

## Über dich

Deine eigenen Adressen und Nummern, auch Aliasse, gehören immer zu dir und nie zu einer Person in deinem Graph. Wenn du nach dir selbst suchst oder eine Person mit einer deiner Adressen hinzufügst, wird **Über dich** geöffnet. Beim Import wird dein eigener Eintrag übersprungen.

Unter „Über dich“ werden deine Adressen mit ihrer jeweiligen Quelle aufgeführt. Ändere sie unter **Einstellungen** im Bereich „Konto“. Um deinen eigenen Kontakt an ein Teammitglied oder einen Freund zu senden, wähle **Meinen Kontakt teilen**. Siehe [Kontakt teilen](share-contact.md).

## Deine Rolle für andere

Rollen, die deine Machine in deinen Nachrichten erkennt, werden auf der Seite einer Person unter **Für dich** angezeigt. Dabei stehen nur die Wörter, die die Rolle erkennen lassen, zum Beispiel ein Titel. Dass jemand sagt, die Person sei deine Steuerberaterin oder dein Kunde, reicht nicht aus. Dafür braucht es auch etwas von deiner Seite, zum Beispiel deine eigenen Nachrichten oder Meetings mit der Person. Du musst nichts bestätigen. Stimmt etwas nicht? Über **Bearbeiten** auf der Seite oder **⋯** in der entsprechenden Zeile unter **Letzte Änderungen** kannst du es korrigieren. Deine Änderungen helfen beim Lernen.

## Was deine Machine über jemanden weiß

Fakten über eine Person stehen auf ihrer Seite unter **Bekannt über**. Allgemeine Erkenntnisse stehen unter „Lernen“. Mit **Hinzufügen** kannst du eine weitere Tatsache in deinen eigenen Worten festhalten. Jede Tatsache hat ein Menü:

- Mit **Bearbeiten** kannst du sie direkt ändern.
- Mit **Nicht über diese Person** wird sie wieder zu einer allgemeinen Tatsache unter **Lernen**, **Fakten**.
- Mit **Entfernen** wird sie überall gelöscht.

## Letzte Änderungen

Unter **Letzte Änderungen**, eingeklappt direkt oberhalb des Verlaufs einer Person, Organisation oder eines Projekts, stehen die Änderungen und Erkenntnisse deiner Machine über sie: eine Rolle, der Arbeitsort, die Beziehung zwischen zwei Personen, eine Tatsache oder eine Projektänderung. Jede Zeile zeigt Datum und Quelle. Tippe auf die Quelle, um die Nachricht zu lesen.

Wenn eine Zeile nicht stimmt, kannst du sie über **⋯** direkt korrigieren: mit **Bearbeiten**, **Entfernen**, **Nicht über diese Person** oder **Rückgängig**, um ein Projekt an seinen vorherigen Ort zurückzusetzen. Es werden drei Zeilen angezeigt. Über **Mehr anzeigen** findest du die übrigen.

Bei Personen, die deine Machine heute aktualisiert hat, erscheint in der Personenliste ein kleiner Punkt. Oben in der Liste steht außerdem **4 Personen heute aktualisiert**. Siehe [The Graph](graph.md).

## Aufgabe zu einer Person

Mit **Neue Aufgabe** im Menü **⋯** einer Person, Organisation oder eines Projekts kannst du eine Aufgabe zu dieser Person, Organisation oder diesem Projekt erstellen.
