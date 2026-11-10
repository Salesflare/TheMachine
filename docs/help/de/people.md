---
title: Personen
area: graph
summary: Alle, mit denen du in Kontakt bist: ihre Seite, Zusammenfassung und Verlauf, und wie du jemanden hinzufügst, bearbeitest, zusammenführst oder löschst.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
---
Alle, mit denen du in Kontakt bist, die engsten zuerst, aus deinen Nachrichten und Meetings. Newsletter, Belege und andere Massenmails fügen niemanden hinzu, bis du zurückschreibst. Sie stehen unter Ausgeblendete Absender, unter der Liste: Als Person zeigen holt sie herein. Filter, Felder, Tags und Import funktionieren in allen drei Listen gleich: siehe [Der Graph](graph.md).

## Die Seite einer Person

Sie beginnt mit Foto, Name, Position, Organisation und Ort und einer Zeile dazu, wie ihr in Kontakt seid („Täglicher Austausch · zuletzt Fr, 23. Okt · nächstes Meeting Di, 27. Okt“). Darunter:

- **Kontakt**: Telefonnummern und E-Mail-Adressen. Tippe auf eine, um anzurufen oder zu schreiben, oder **Kopieren**. Auch der **Geburtstag** steht hier, mit seiner Herkunft (Google-Kontakte, Facebook oder du): siehe [Der Graph](graph.md#geburtstag).
- **Mit dir**: was die Person für dich ist, Kontakt aus Arbeit oder Privat, und deine Familie oder Fleet, mit **In Fleet ansehen**.
- **Auch auf**: die anderen Orte, an denen ihr miteinander sprecht. **Slack** öffnet die Person in Slack, oder deinen neuesten Slack-Thread mit ihr.
- **Personen** und **Projekte**, zu denen sie gehört, **Offen zwischen euch** (Versprechen in beide Richtungen, mit **Als erledigt markieren** und **Fallen lassen**) und ihr **Verlauf**.

Adressen und Chats einer Person werden von selbst zusammengeführt, wenn klar ist, dass es eine Person ist, etwa eine Arbeitsadresse mit der privaten Adresse in CC.

Wenn eine Seite **Die Seite konnte nicht geladen werden.** zeigt, tippe auf **Erneut versuchen**. Bleibt es dabei, nutze **Stimmt etwas nicht?** unten auf der Seite.

## Zusammenfassung

Ein paar kurze Zeilen oben auf der Seite einer Person: was entschieden, gefragt, geplant oder versprochen wurde, mit allen beim Namen. The Machine schreibt sie neu, wenn es Neues gibt, nur für Menschen, mit denen du wirklich in Kontakt bist, und prüft vorher jede Zeile.

Eine vage Zeile fällt weg; gibt es nichts Konkretes, gibt es keine Zusammenfassung. Jede Zeile verlinkt ihre Quelle: Nachrichten eines Tages teilen sich ein Datum mit ihrer Anzahl und öffnen sich zusammen.

**Bearbeiten**, um es mit deinen Worten zu sagen. Gibt es Neues, zeigt The Machine eine **Vorgeschlagene Aktualisierung** mit **Übernehmen** und **Meine behalten**. **The Machine schreiben lassen** gibt sie ihr zurück.

Meeting-Vorbereitungen nutzen sie, nur die Zeilen von der Seite dieser Aufgabe (Arbeit oder Privat). Sie bleibt auf deiner Machine; dein Team sieht sie nie.

## Verlauf

Jede Seite einer Person und Organisation hat einen, das Neueste zuerst: E-Mails, Meetings und ihre Zoom-Zusammenfassungen, Intercom-Unterhaltungen (mit **In Intercom öffnen**), Chats auf WhatsApp, Telegram, Slack, LinkedIn und X, Aufgaben, Versprechen und Projektbewegungen. Die Chips oben zeigen jeweils eine Quelle. **Mehr anzeigen** lädt ältere Einträge.

Anstehende Meetings stehen oben unter **Demnächst**, das nächste zuerst; **Alle anstehenden zeigen** zeigt den Rest. Ein Meeting zeigt, wer dabei war, jede Person einmal. Eins mit Notizen oder Transkript zeigt **Notizen** oder **Transkript**; ein Klick öffnet sie.

Deine Verläufe gehören dir: Der Graph des Teams zeigt nur, was deine Freigaberegeln erlauben. Auf einer Seite fügt **Team** über dem Verlauf hinzu, was Teammitglieder geteilt haben, jeweils mit ihrem Namen; **Meine** zeigt nur deins.

## Arbeit und Privat

Die Tabs **Arbeit** und **Privat** listen Personen nach ihrem Typ, dem auf ihrer Seite. Deine eigene Wahl (**Bearbeiten**) gilt vor allem anderen. Sonst sind deine Familie und Freunde, und wer zu dir als Familie oder Freund gehört (eine Ehefrau, ein Vater), privat, egal von welcher Adresse sie schreiben. Dein Team bekommt nie private Kontakte.

## Jemanden hinzufügen

**Neue Person** oben bei Personen, oder auf dem Handy **+** in der oberen Leiste. Gib einen Namen an, und E-Mail-Adresse und Organisation, wenn du sie hast. Wenn schon eine ähnliche Person in deinem Graph ist, zeigt das Formular sie zuerst, damit du stattdessen diese öffnen kannst. **Hinzufügen** öffnet die neue Seite.

Wen du hinzufügst, der bleibt, auch ohne Nachrichten. Die erste Nachricht wird dann zugeordnet.

## Jemanden bearbeiten

**Bearbeiten** oben auf der Seite ändert Name, Position, Organisation, Ort, Telefonnummern, LinkedIn und E-Mail-Adressen, was die Person für dich ist, und Arbeit oder Privat. Das Feld **Notizen** ist für alles, was du dir merken willst; Notizen bleiben beim Zusammenführen erhalten. **Speichern** behält es, **Abbrechen** lässt es, wie es war.

Deine Änderungen bleiben, auch wenn die Details neu nachgeschlagen werden, und auch bei **Zusammenführen** und **Rückgängig**. Leere ein Feld, um wieder den nachgeschlagenen Wert zu nutzen. Ein leerer Name holt den Namen aus den Nachrichten zurück.

Um das Bild zu ändern, klick darauf: **Bild hochladen**, eins der gefundenen auswählen oder **Bild entfernen**. Es bleibt auf deiner Machine.

## Zwei Personen zusammenführen

Wenn zwei Personen eine sein könnten, fragt ihre Seite, ob es dieselbe Person ist, und Personen listet sie unter **Gleiche Person?**. **Zusammenführen** verbindet sie, mit allen Nachrichten, Notizen, Rollen und Projekten. **Nicht dieselbe** hält sie dauerhaft getrennt. Deine Antwort steht kurz beim Paar, dann verschwindet das Paar aus der Liste. Die Liste verschwindet, wenn nichts mehr zu fragen ist.

Eine geteilte Adresse wie info@ oder eine Mailingliste wird nie mit den Personen verbunden, die darüber schreiben. Ein Arbeitskontakt von außerhalb deines Unternehmens und ein privater Chat, die nur den Namen gemeinsam haben, werden nicht von selbst verbunden: Sie stehen als Frage in der Liste.

**Alle zusammenführen** führt jedes Paar in der Liste auf einmal zusammen, außer denen, die du mit **Nicht dieselbe** markiert hast. **Rückgängig** direkt danach trennt sie alle wieder.

Um zwei Personen selbst zusammenzuführen, öffne eine davon, dann **⋯**, **Gleiche Person wie…** und wähle die andere. Die Seite einer zusammengeführten Person zeigt unter **Zusammengeführt aus**, warum, mit **Rückgängig**, um sie wieder zu trennen.

## Jemanden endgültig löschen

Öffne auf der Seite das Menü ⋯ und wähle **Endgültig löschen…**, dann **Löschen**. Das entfernt die Person und was deine Machine über sie weiß: ihren Eintrag, Adressen, nachgeschlagene Details, die Nachrichten nur zwischen euch beiden und Notizen über sie.

Aufgaben, an denen sie beteiligt ist, bleiben, ohne ihren Namen. Sie wird nicht wieder hinzugefügt. Das lässt sich nicht rückgängig machen.

## Zurückgekommen

Wenn eine E-Mail an jemanden zurückkommt, zeigt die Adresse **Zurückgekommen** mit dem Datum, und eine andere Adresse dieser Person rückt nach vorn. Neue Entwürfe gehen nie an sie, wenn eine andere Adresse bekannt ist. Ist es die einzige, warnt das Sendefenster, und du kannst trotzdem senden.

Eine Rückmeldung zählt, wenn der Mailserver sagt, dass es die Adresse nicht gibt, oder nach 3 vorübergehenden Fehlern innerhalb einer Woche. Sie verschwindet, wenn die Person wieder von dieser Adresse schreibt oder eine E-Mail an sie ankommt.

## Position und Foto

Personen mit einer Firmenadresse bekommen Position, Foto, LinkedIn und Stadt. Das wird nachgeschlagen wie [Organisationsdetails](organization-data.md). Auf einer gehosteten Machine werden nur ihr Name und die Domain der Firma gesendet. Ausschalten kannst du das in **Einstellungen** unter Sicherheit: **Arbeitskontakte nachschlagen**.

Deine Verbindungen ergänzen mehr mit dem, was sie ohnehin lesen: Position, Telefon und Zeitzone aus Slack, Bio und Ort aus X, Headline und Foto aus LinkedIn, Positionen aus Google-Kontakten und Salesflare. Fahr mit der Maus über die Zeile unter dem Namen, um zu sehen, woher es kommt.

WhatsApp- und Telegram-Bilder kommen über deine WhatsApp-Synchronisierung und deine Verbindung zu Telegram-Chats: bis zu 50 am Tag pro Dienst, nur für Personen, die schon in deinem Graph sind. An die Personen wird nichts gesendet. Alles bleibt auf deiner Machine.

## Über dich

Deine eigenen Adressen und Nummern, auch Aliasse, sind immer du, nie jemand in deinem Graph. Wenn du nach dir selbst suchst oder eine Person mit einer deiner Adressen hinzufügst, öffnet sich **Über dich**, und ein Import überspringt deine eigene Zeile.

Über dich listet deine Adressen mit ihrer Herkunft auf; ändern kannst du sie in **Einstellungen** unter Konto. Um deinen eigenen Kontakt an ein Teammitglied oder einen Freund zu schicken, wähle **Meinen Kontakt teilen**. Siehe [Einen Kontakt teilen](share-contact.md).

## Wer ist wer

Rollen, die deine Machine in deinen Nachrichten gelesen hat und die auf dein Wort warten. **✓ Stimmt** bestätigt eine. **Bearbeiten** öffnet die Seite der Person im Bearbeitungsmodus. Sie lernt aus deinen Änderungen. Das erscheint nur, wenn Rollen warten.

## Was sie über jemanden weiß

Fakten über jemanden stehen auf seiner Seite, unter **Bekannt über**; Lernen behält die allgemeinen. **Hinzufügen** hält einen weiteren in deinen eigenen Worten fest. Jeder Fakt hat ein Menü:

- **Bearbeiten** ändert ihn direkt dort.
- **Nicht über** die Person macht ihn wieder zu einem allgemeinen Fakt, unter **Lernen**, **Fakten**.
- **Entfernen** löscht ihn überall.

## Letzte Änderungen

**Letzte Änderungen**, eingeklappt direkt über dem Verlauf einer Person, Organisation oder eines Projekts, zeigt, was deine Machine dazu geändert oder gelernt hat: eine Rolle, wo jemand arbeitet, wie zwei Personen zusammenhängen, einen Fakt, einen verschobenen Projektstand. Jede Zeile hat ihr Datum und ihre Quelle; tippe auf die Quelle, um die Nachricht zu lesen.

Ist eine Zeile falsch, korrigiert ihr **⋯** sie direkt dort: **Bearbeiten**, **Entfernen**, **Nicht über** die Person oder **Rückgängig**, um ein Projekt zurückzusetzen. Drei Zeilen sind sichtbar; **Mehr anzeigen** zeigt den Rest.

## Eine Aufgabe zu jemandem

**Neue Aufgabe** im Menü **⋯** einer Person, Organisation oder eines Projekts startet eine Aufgabe dazu.
