---
title: Übergaben
area: fleet
summary: Teile eine Aufgabe mit einem Teammitglied oder übergib sie mit „Übergeben…“ an dessen Machine. Frag später nach oder hol sie zurück.
covers: handoffs
code: fleet_requests.py, dashboard.html
order: 3
translated: d9b21c04fb0d34a6
---
## Eine Aufgabe übergeben

1. Öffne bei der Aufgabe **…**, dann **Übergeben…**, und wähle **Ein Teammitglied**.
2. Wähle aus, an wen du sie übergeben möchtest, prüfe, was mitgeschickt wird (× lässt einen Teil weg), und füge eine Notiz hinzu. Aus einem Personal-Konto oder einem anderen Unternehmen wird nichts mitgeschickt.
3. Sende die Aufgabe. Die Machine zeigt sie der Person als Aufgabe an.

Die Machine benachrichtigt die Person auf dem Handy oder in Telegram. Wenn beides nicht eingerichtet ist, schickt sie einmalig eine E-Mail mit dem Namen der übergebenden Person, dem Titel und einem Link. Weitere Infos findest du unter [Benachrichtigungen](notifications.md).

Ein Intercom-Gespräch wird ebenfalls mitgeschickt. Wenn die Machine der Person denselben Intercom-Arbeitsbereich liest, öffnet **Nachricht lesen** das Gespräch und die Antwort geht in Intercom zurück. Andernfalls führt der Link in der Aufgabe dorthin.

Während du wartest, zeigt die Aufgabe, worum du gebeten hast und wann ("Am Di., 3. Nov. Pat gefragt: …"), aber nur, wenn das zusätzliche Informationen zum Titel liefert. Sie steht unter **Kommt später zurück** mit dem Hinweis „Bei Pat · wartet“ und einem Datum zum Nachfragen. **Jetzt nachhaken** erstellt einen kurzen Entwurf für eine Erinnerungsnachricht an Pat, die du senden kannst. Mit **Uhrzeit ändern** verschiebst du die Nachfrage.

Wenn Pats Machine Pat nicht benachrichtigen kann, steht in der Aufgabe: „Pat wird nicht benachrichtigt. Sag Pat Bescheid.“ Informiere Pat selbst. Der Hinweis verschwindet, sobald Pat Benachrichtigungen aktiviert.

Die Aufgabe erscheint nur dann wieder oben, wenn es etwas zu entscheiden gibt: Pat hat geantwortet, die Aufgabe abgelehnt oder erledigt, die Übergabe ist fehlgeschlagen oder eine Frist ist erreicht. Der Zeitpunkt zum Nachfragen richtet sich nach dem Fälligkeitsdatum: ein paar Stunden vorher, wenn die Aufgabe heute fällig ist, am vorherigen Arbeitstag, wenn sie bald fällig ist, am nächsten Morgen, wenn sie dringend ist, andernfalls nach 3 Arbeitstagen.

Wenn die Aufgabe zum Nachfragen zurückkommt, steht dort „Noch bei Pat“. **Jetzt nachhaken** erstellt bei der Aufgabe eine kurze Erinnerungsnachricht an Pat an dem Ort, an dem du gefragt hast (Slack, WhatsApp, Telegram oder E-Mail). Erst wenn du **Senden** auswählst, wird sie gesendet. Danach wartet die Aufgabe wieder auf Pat. Wenn keiner der verbundenen Dienste Pat eine Nachricht senden kann, öffnet sich der Chat mit einem entsprechenden Hinweis. **Zurücknehmen** und **An jemand anderen übergeben** findest du unter **…**, dann **Übergeben…**.

Im Chat der Aufgabe siehst du, wann sie übergeben wurde ("An Pats Machine übergeben · 14:02") und was zurückkam: angenommen, abgelehnt (mit Pats Notiz) oder erledigt. Wenn noch keine Antwort vorliegt, gibt es die Optionen **Als erledigt markieren**, **Zurückstellen** und **Nicht nötig**. Um Pat zu erinnern oder die Aufgabe zurückzunehmen, sag es im Chat.

Wenn die Übergabe nicht gesendet werden konnte, steht das in der Aufgabe und im Chat. Dort findest du auch **Erneut versuchen**.

## Was die andere Person sieht

Nur diese Aufgabe: deine Bitte, deine Notiz, das Fälligkeitsdatum und den Kontakt sowie Kopien der mitgeschickten Nachrichten (bis zu drei, ohne Anhänge). Nicht dein Postfach und auch keine anderen Aufgaben. Die Person wählt **Annehmen** oder **Ablehnen**.

Sobald die Person annimmt, gehört die Aufgabe ihr. Deine ist dann erledigt oder wartet auf das Ergebnis, wenn sie ein **Fertig, wenn** hat. Ihr arbeitet nicht beide an derselben Aufgabe. Wenn jemand die Aufgabe ansehen soll, sie aber deine bleiben soll, nutze [Um Review bitten](ask-to-review.md).

## An jemand anderen übergeben

Solange ein Teammitglied die Aufgabe hat, steht das in einer Zeile ("Bei Pat · wartet"). Unter **…**, dann **Übergeben…**, findest du **Zurücknehmen** und **An jemand anderen übergeben**. Mit **Zurücknehmen** gehört die Aufgabe wieder dir: Pats Machine wird benachrichtigt und Pats Antwort hat keinen Einfluss mehr auf die Aufgabe.

Mit **An jemand anderen übergeben** öffnest du das Übergabeformular. Oder sag es im Chat der Aufgabe ("Diese Aufgabe sollte an Kim gehen"). Dann steht dort: „Noch bei Pat, bis du die Aufgabe an Kim sendest“, mit **Übergabe prüfen an** Kim.

Eine Aufgabe kann jedem Teammitglied nur einmal übergeben werden: Solange Pat sie hat, wird Pat im Übergabeformular auszuwählen zu einer Nachfrage. Mit **Nachfragen** wird derselbe Entwurf für eine Erinnerungsnachricht erstellt, bei Bedarf mit einer zusätzlichen Zeile von dir.

**Von Pat zurücknehmen** ist standardmäßig aktiviert. Deaktiviere die Option, wenn ihr beide die Aufgabe haben sollt. Es wird nichts gesendet, bis du **Übergeben** auswählst. Pats Machine wird benachrichtigt und Pats Kopie der Aufgabe verschwindet.

## Wenn die andere Person ablehnt

Die Person kann den Grund angeben: Die Aufgabe gehört nicht ihr, ist bereits erledigt oder sie hat diese Woche keine Zeit. Wähle dann **Selbst machen**, **An jemand anderen übergeben** oder **Als erledigt markieren**. Das Gleiche gilt, wenn die Person nicht rechtzeitig antwortet. Mit **Selbst machen** gehört die Aufgabe wieder dir und steht unter „Für dich“.

## Jemand außerhalb des Network

Wähle **Per E-Mail**. Deine Machine erstellt einen E-Mail-Entwurf, den du senden kannst. Während du tippst, schlägt sie zuerst deine Fleet und dann Personen aus deinem Unternehmen vor. Füge eine Aufgabenseite hinzu, damit die Person mit einem Fingertipp antworten kann: Weitere Infos findest du unter [Aufgabenseiten](task-pages.md).

Nur für Work-Aufgaben. Markiere, was mitgeschickt werden soll: ein paar Zeilen zur Aufgabe, ihr Entwurf, Links und Dateien. Persönliche Inhalte und Inhalte, die nur für dich bestimmt sind, werden nicht mitgeschickt. Mit **E-Mail vorbereiten** wird die E-Mail an die Aufgabe angehängt. Lies sie durch und sende sie dann aus deinem eigenen Postfach. Es gibt keine Nachverfolgung.

Bei einer Aufgabe aus Intercom oder Slack gibt es kein eigenes Postfach. Deshalb wird die E-Mail aus deinem Work-Postfach gesendet.

Die Aufgabe verfolgt sie dann als Versprechen, bis die Person antwortet, dass sie erledigt ist, oder du sie als erledigt markierst. Die E-Mail endet mit „Übernimm diese Aufgabe in deiner eigenen Machine“. Wenn sich die Person über diesen Link anmeldet, kann sie deiner Fleet beitreten und die Aufgabe wird an ihre Machine übergeben. Deaktiviere diese Zeile unter **Einstellungen** im Bereich Fleet.
