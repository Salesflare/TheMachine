---
title: Personen
area: graph
summary: Alle, mit denen du Kontakt hast: ihre Seite, Zusammenfassung und ihr Verlauf sowie wie du Personen hinzufügst, bearbeitest, zusammenführst oder löschst.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 26845dd199228f90
---
Alle, mit denen du Kontakt hast, nach Nähe sortiert, aus deinen Nachrichten und Meetings. Newsletter, Belege und andere Mailings fügen niemanden hinzu, bis du antwortest. Sie stehen unter „Ausgeblendete Absender“ unterhalb der Liste. Mit **Als Person anzeigen** wird ein Absender hinzugefügt. Felder, Tags und Import funktionieren in allen drei Listen gleich. Jede Liste hat eigene Filter: siehe [The Graph](graph.md).

Ein gemeinsames Postfach (info@, Kundenservice, der eigene Name eines Geschäfts) zählt für die zugehörige Organisation, nicht als Person, auch wenn du dorthin schreibst.

## Seite einer Person

Oben stehen Foto, Name, Titel, Organisation und Ort sowie eine Zeile dazu, wie ihr in Kontakt seid („Täglich im Gespräch · letzter Kontakt gestern · nächstes Meeting Di., 27. Okt.“). Der letzte Kontakt wird als „gerade eben“, „vor 3 Stunden“, „gestern“ oder „vor 3 Tagen“ angezeigt. Bei länger zurückliegenden Kontakten steht ein Datum. Bewege den Mauszeiger darüber, um das genaue Datum zu sehen. Darunter findest du:

- **Kontakt**: Telefonnummern und E-Mail-Adressen. Tippe auf eine Nummer oder Adresse, um anzurufen oder zu schreiben, oder auf **Kopieren**, um sie zu kopieren. Auch der **Geburtstag** wird hier angezeigt, zusammen mit seiner Quelle (Google Kontakte, Google Kalender, Facebook, deine Notizen oder du): siehe [The Graph](graph.md#birthday).
- **Mit dir**: die Beziehung zu dir, ob die Person ein Arbeitskontakt oder privater Kontakt ist und ob sie zu deiner Familie oder deinem Fleet gehört, mit **In Fleet ansehen**.
- **Auch auf**: weitere Orte, an denen ihr miteinander kommuniziert. **Slack** öffnet die Person in Slack oder euren neuesten Slack-Thread.
- **Personen** und **Projekte**, zu denen sie gehört, **Offen zwischen euch** (Versprechen in beide Richtungen, mit **Als erledigt markieren** und **Fallen lassen**) und ihr **Verlauf**.

Adressen und Chats einer Person werden automatisch zusammengeführt, wenn klar ist, dass sie zu derselben Person gehören, zum Beispiel eine geschäftliche E-Mail-Adresse mit der eigenen Adresse in CC.

Wenn auf einer Seite **Diese Seite konnte nicht geladen werden.** steht, tippe auf **Erneut versuchen**. Wenn die Meldung weiterhin erscheint, tippe unten auf der Seite auf **Stimmt etwas nicht?**.

## Zusammenfassung

Oben auf der Seite einer Person stehen einige kurze Zeilen dazu, was besprochen, gefragt, geplant oder versprochen wurde, mit Namen aller Beteiligten. The Machine schreibt sie neu, wenn es etwas Neues gibt, aber nur für Personen, mit denen du wirklich in Kontakt bist, und prüft jede Zeile vorher. Normalerweise einmal am Tag, bei einer Änderung in einer Angelegenheit mit dieser Person innerhalb weniger Stunden, zum Beispiel bei einer neuen Frist oder einer zurückgezogenen Anfrage.

Vage Aussagen werden weggelassen. Wenn es nichts Konkretes zu sagen gibt, erscheint keine Zusammenfassung. Jede Zeile führt zu ihrer Quelle: Nachrichten vom selben Tag werden mit Datum und Anzahl zusammengefasst und lassen sich gemeinsam öffnen.

Mit **Bearbeiten** kannst du die Zusammenfassung in deinen eigenen Worten schreiben. Wenn es Neuigkeiten gibt, zeigt The Machine eine **Vorgeschlagene Aktualisierung** mit **Übernehmen** und **Meine behalten**. Mit **The Machine schreiben lassen** überlässt du die Zusammenfassung wieder The Machine.

Vorbereitungen für Meetings verwenden diese Zusammenfassung, aber nur die Zeilen aus dem Bereich dieser Aufgabe (Arbeit oder Privat). Sie bleibt auf deiner Machine. Dein Team sieht sie nie.

## Verlauf

Jede Seite einer Person und Organisation hat einen Verlauf, vom Neuesten zum Ältesten: E-Mails, Meetings und ihre Zoom-Zusammenfassungen, Intercom-Unterhaltungen (mit **In Intercom öffnen**), WhatsApp-, Telegram-, Slack-, LinkedIn- und X-Chats, Aufgaben, Versprechen und Projektänderungen. Mit den Chips oben kannst du jeweils eine Quelle anzeigen. **Mehr anzeigen** lädt ältere Einträge.

Anstehende Meetings stehen ganz oben unter **Demnächst**, beginnend mit dem nächsten. Mit **Alle anstehenden zeigen** siehst du die übrigen. Bei einem Meeting wird angezeigt, wer dabei war, jede Person nur einmal. Bei einem Meeting mit Notizen oder Transkript steht **Notizen** oder **Transkript**. Klicke darauf, um sie zu lesen.

Deine Verläufe gehören dir: Im Graph deines Teams wird nur angezeigt, was deine Freigabeeinstellungen erlauben. Wenn du auf einer Seite oben im Verlauf **Team** auswählst, werden auch die von Teammitgliedern freigegebenen Einträge angezeigt. Bei jedem Eintrag steht, von wem er stammt. **Meine** zeigt nur deine Einträge.

## Arbeit und Privat

Auf den Tabs **Arbeit** und **Privat** werden Personen nach ihrem Typ sortiert, der auch auf ihrer Seite steht. Deine eigene Auswahl (**Bearbeiten**) hat Vorrang. Ansonsten werden deine Familie und Freunde sowie Personen, für die du zur Familie oder zu den Freunden gehörst (zum Beispiel eine Ehefrau oder ein Vater), als privat eingestuft, egal von welcher Adresse aus sie schreiben. Dein Team erhält nie private Kontakte.

## Person hinzufügen

Tippe oben unter Personen auf **Neue Person** oder auf **+** in der oberen Leiste auf dem Smartphone. Gib einen Namen und, falls bekannt, eine E-Mail-Adresse und Organisation ein. Wenn es in deinem Graph bereits eine ähnliche Person gibt, zeigt das Formular sie zuerst an, damit du stattdessen ihre Seite öffnen kannst. Mit **Hinzufügen** wird die neue Seite geöffnet.

Eine Person, die du hinzufügst, bleibt erhalten, auch wenn es noch keine Nachrichten gibt. Die erste Nachricht wird ihr zugeordnet.

## Person bearbeiten

Mit **Bearbeiten** oben auf der Seite kannst du Name, Titel, Organisation, Ort, LinkedIn, Telefonnummern und E-Mail-Adressen, die Beziehung zu dir sowie „Arbeit“ oder „Privat“ ändern. Das Feld **Notizen** ist für alles gedacht, woran du dich erinnern möchtest. Notizen bleiben auch nach dem Zusammenführen erhalten. Mit **Speichern** werden deine Änderungen übernommen, mit **Abbrechen** verworfen.

Deine Änderungen bleiben erhalten, auch wenn die Details der Person erneut nachgeschlagen werden oder du **Zusammenführen** und **Rückgängig** verwendest. Leere ein Feld, um wieder den nachgeschlagenen Wert zu verwenden. Wenn du den Namen leerst, wird wieder der Name aus den Nachrichten angezeigt.

Um das Foto zu ändern, klicke darauf: **Bild hochladen**, ein für die Person gefundenes Bild auswählen oder **Bild entfernen**. Das Foto bleibt auf deiner Machine.

## Zwei Personen zusammenführen

Wenn zwei Personen möglicherweise dieselbe sind, fragt ihre Seite, ob es sich um dieselbe Person handelt. In der Personenliste werden sie unter **Gleiche Person?** angezeigt. Mit **Zusammenführen** werden sie samt Nachrichten, Notizen, Rollen und Projekten zusammengeführt. Mit **Nicht dieselbe** bleiben sie dauerhaft getrennt. Deine Antwort wird kurz beim Personenpaar angezeigt, dann verschwindet es aus der Liste. Die Liste wird ausgeblendet, wenn keine offenen Fragen mehr bestehen.

Eine Person mit einer Adresse, die nur einer dir bekannten Adresse ähnelt, zum Beispiel acme-corp.example statt acmecorp.example, wird nie als dieselbe Person vorgeschlagen. Nur du kannst ihr eine Rolle zuweisen.

Eine gemeinsame Adresse wie info@ oder eine Mailingliste wird nie mit den Personen zusammengeführt, die darüber schreiben. Ein Arbeitskontakt von außerhalb deines Unternehmens und ein privater Chat, bei denen nur der Name übereinstimmt, werden nicht automatisch zusammengeführt. Stattdessen werden sie als Frage angezeigt.

Mit **Alle zusammenführen** werden alle Paare in der Liste auf einmal zusammengeführt, außer denen, bei denen du **Nicht dieselbe** ausgewählt hast. Mit **Rückgängig** direkt danach werden alle wieder getrennt.

Um zwei Personen selbst zusammenzuführen, öffne eine der beiden Seiten und wähle dann **⋯**, **Gleiche Person wie…** und die andere Person aus. Auf der Seite einer zusammengeführten Person steht unter **Zusammengeführt aus**, warum sie zusammengeführt wurde. Mit **Rückgängig** kannst du sie wieder trennen.

## Person endgültig löschen

Öffne auf der Seite der Person das Menü ⋯ und wähle **Endgültig löschen…** und dann **Löschen**. Dadurch werden die Person und alles, was deine Machine über sie weiß, entfernt: ihr Eintrag, ihre Adressen, nachgeschlagene Details, Nachrichten, die nur zwischen euch beiden ausgetauscht wurden, und Notizen über sie.

Aufgaben, an denen die Person beteiligt ist, bleiben erhalten, aber ihr Name wird daraus entfernt. Sie wird nicht erneut hinzugefügt, auch nicht durch einen Import oder eine Facebook-Geburtstagsaufgabe mit ihrem Namen oder ihrer Adresse. Das lässt sich nicht rückgängig machen.

## Unzustellbar

Wenn eine E-Mail an jemanden unzustellbar ist, wird die Adresse mit **Unzustellbar** und dem Datum angezeigt. Eine andere Adresse der Person wird zuerst angezeigt. Neue Entwürfe werden nie an diese Adresse geschickt, wenn eine andere bekannt ist. Ist es die einzige Adresse, warnt dich das Versandfenster. Du kannst die E-Mail trotzdem senden.

Eine E-Mail gilt als unzustellbar, wenn der Mailserver meldet, dass die Adresse nicht existiert, oder wenn es innerhalb einer Woche 3 vorübergehende Fehler gibt. Der Hinweis wird entfernt, wenn die Person erneut von dieser Adresse aus schreibt oder eine E-Mail an sie zugestellt wird.

## Berufsbezeichnung und Foto

Bei Personen mit einer Firmenadresse werden Berufsbezeichnung, Foto, LinkedIn und Stadt wie [Organisationsdetails](organization-data.md) nachgeschlagen. Bei einer gehosteten Machine werden dafür nur der Name und die Unternehmensdomain abgefragt. Für ein Foto erhält Gravatar einen Hash der geschäftlichen Adresse, niemals die Adresse selbst. Du kannst die Funktion in den **Einstellungen** unter „Sicherheit“ ausschalten: **Arbeitskontakte nachschlagen**.

Wenn die Informationen nachgeschlagen wurden, zeigt die Seite der Person auch den Infotext, seit wann sie ihre aktuelle Rolle hat und ihre zwei vorherigen Rollen. Diese Angaben werden auch für Vorbereitungen verwendet. Der Infotext wird nur verwendet, wenn die Person keine eigene Biografie hat.

Deine Verbindungen werden durch Angaben ergänzt, die bereits aus anderen Quellen bekannt sind: Berufsbezeichnung, Telefonnummer und Zeitzone aus Slack, Biografie und Ort aus X, Überschrift und Foto aus LinkedIn, Berufsbezeichnungen aus Google Kontakte und Salesflare sowie das Kontaktfoto aus Salesflare, wenn Salesflare selbst eines speichert. Bewege den Mauszeiger über die Zeile unter dem Namen, um die Quelle zu sehen.

Outlook fügt Fotos von Kolleginnen und Kollegen in deiner Organisation sowie von deinen Outlook-Kontakten hinzu. Außerdem werden Berufsbezeichnungen und Unternehmen deiner Kontakte ergänzt ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Fotos aus WhatsApp und Telegram werden über deine WhatsApp-Synchronisierung und deine Verbindung zu Telegram-Chats hinzugefügt: jeweils bis zu 50 pro Tag, nur für Personen, die bereits in deinem Graph sind. Es wird nichts an diese Personen gesendet. Ein Facebook-Geburtstagsimport fügt beim Speichern das Profilbild einer Person hinzu, wenn sie noch kein Foto hat ([Routinen](routines.md)). Alles bleibt auf deiner Machine.

Im [Team Graph](team-graph.md) eines Work Fleet wird eine kleine Kopie eines beruflichen Fotos mit dem geteilten Eintrag einer Person gespeichert. Fotos aus Google Kontakte, WhatsApp, Telegram oder Facebook sowie Fotos, die du geändert oder entfernt hast, werden nie geteilt.

## Über dich

Deine eigenen Adressen und Telefonnummern, auch Aliasse, gehören immer dir und sind nie eine andere Person in deinem Graph. Wenn du nach dir selbst suchst oder eine Person mit einer deiner Adressen hinzufügst, wird **Über dich** geöffnet. Bei einem Import wird dein eigener Eintrag übersprungen.

Unter „Über dich“ werden deine Adressen samt ihrer Quellen aufgeführt. Ändere sie in den **Einstellungen** unter „Konto“. Um deinen Kontakt an ein Teammitglied oder einen Freund zu senden, wähle **Meinen Kontakt teilen**. Siehe [Kontakt teilen](share-contact.md).

## Deine Beziehung zu einer Person

Rollen, die deine Machine in deinen Nachrichten erkennt, werden auf der Seite der Person unter **Für dich** angezeigt, zusammen mit der gelesenen Textzeile. Du musst nichts bestätigen. Stimmt etwas nicht? Mit **Bearbeiten** auf der Seite der Person oder **⋯** neben der Zeile unter **Letzte Änderungen** kannst du es korrigieren. The Machine lernt aus deinen Änderungen.

## Was über eine Person bekannt ist

Fakten über eine Person stehen auf ihrer Seite unter **Bekanntes**. Unter **Lernen** werden allgemeine Erkenntnisse gespeichert. Mit **Hinzufügen** kannst du eine weitere in deinen eigenen Worten festhalten. Zu jeder Tatsache gibt es ein Menü:

- Mit **Bearbeiten** kannst du sie direkt ändern.
- Mit **Nicht über diese Person** wird sie wieder zu einer allgemeinen Tatsache unter **Lernen**, **Fakten**.
- Mit **Entfernen** wird sie überall gelöscht.

## Letzte Änderungen

Unter **Letzte Änderungen**, direkt über dem Verlauf einer Person, Organisation oder eines Projekts, werden Änderungen und Erkenntnisse deiner Machine dazu aufgeführt: eine Rolle, der Arbeitsplatz, die Beziehung zwischen zwei Personen, eine Tatsache oder eine Projektänderung. Bei jeder Zeile stehen Datum und Quelle. Tippe auf die Quelle, um die Nachricht zu lesen.

Wenn eine Zeile falsch ist, kannst du sie über **⋯** direkt korrigieren: **Bearbeiten**, **Entfernen**, **Nicht über diese Person** oder **Rückgängig**, um ein Projekt an seinen vorherigen Ort zurückzusetzen. Drei Zeilen werden angezeigt. Mit **Mehr anzeigen** siehst du die übrigen.

Bei einer Person, die deine Machine heute aktualisiert hat, erscheint ein kleiner Punkt in der Personenliste. Oben in der Liste steht **Heute wurden 4 Personen aktualisiert** und nennt die Personen. Siehe [The Graph](graph.md).

## Aufgabe zu einer Person

Mit **Neue Aufgabe** im Menü **⋯** einer Person, Organisation oder eines Projekts erstellst du eine Aufgabe zu dieser Person.
