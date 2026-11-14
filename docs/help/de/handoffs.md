---
title: Übergaben
area: fleet
summary: Übergib eine Aufgabe an die Machine eines Teammitglieds, zusammen mit allem, was dafür nötig ist. Frag später nach oder hol sie zurück.
covers: handoffs
code: fleet_requests.py, dashboard.html
order: 3
translated: acb60a24ef374625
---
## Eine Aufgabe übergeben

1. Öffne bei der Aufgabe **…**, dann **Übergeben…**, und wähle **Ein Teammitglied**.
2. Wähle eine Person, prüfe, was mitgegeben wird (× lässt einen Teil weg), und füge eine Notiz hinzu. Nichts aus einem Personal-Konto oder einem anderen Unternehmen wird mitgegeben.
3. Sende die Aufgabe ab. Ihre Machine zeigt sie der Person als Aufgabe an.

Ihre Machine benachrichtigt sie auf dem Handy oder über Telegram. Wenn beides nicht eingerichtet ist, erhält die Person einmalig eine E-Mail mit dem Namen der Person, die die Aufgabe übergeben hat, dem Titel und einem Link. Weitere Informationen findest du unter [Benachrichtigungen](notifications.md).

Eine Intercom-Unterhaltung wird ebenfalls mitgegeben. Wenn ihre Machine Zugriff auf denselben Intercom-Arbeitsbereich hat, öffnet **Nachricht lesen** die Unterhaltung und die Antwort wird in Intercom gesendet. Wenn nicht, enthält die Aufgabe einen Link dazu.

Während du wartest, zeigt die Aufgabe, worum du gebeten hast und wann („Pat gefragt am Di., 3. Nov.: …“), aber nur, wenn das zusätzlich zum Titel etwas aussagt. Sie erscheint unter **Kommt später zurück**, „Bei Pat · wartet“, zusammen mit einem Datum fürs Nachfragen. **Jetzt nachhaken** erstellt einen kurzen Erinnerungsentwurf an Pat, den du senden kannst. Mit **Uhrzeit ändern** änderst du den Zeitpunkt fürs Nachfragen.

Wenn Pats Machine Pat nicht benachrichtigen kann, steht bei der Aufgabe „Pat wird nicht benachrichtigt. Sag Pat Bescheid.“ Informiere Pat selbst. Der Hinweis verschwindet, sobald Pat Benachrichtigungen aktiviert.

Die Aufgabe erscheint erst wieder ganz oben, wenn es etwas zu entscheiden gibt: Pat hat geantwortet, abgelehnt oder die Aufgabe erledigt, die Übergabe ist fehlgeschlagen oder eine Frist ist erreicht. Der Zeitpunkt fürs Nachfragen richtet sich nach dem Fälligkeitsdatum: bei heute ein paar Stunden später, bei bald am vorherigen Arbeitstag, bei dringend am nächsten Morgen, andernfalls in 3 Arbeitstagen.

Wenn die Aufgabe zum Nachfragen zurückkommt, steht dort „Immer noch bei Pat“. **Jetzt nachhaken** erstellt einen kurzen Erinnerungsentwurf an Pat an der Stelle, an der du gefragt hast (Slack, WhatsApp, Telegram oder E-Mail), direkt bei der Aufgabe. Es wird nichts gesendet, bis du **Senden** auswählst. Danach wartet die Aufgabe wieder auf Pat. Wenn du über keinen verbundenen Dienst Nachrichten an Pat senden kannst, öffnet sich der Chat mit einem entsprechenden Hinweis. **Zurücknehmen** und **An jemand anderen übergeben** findest du unter **…**, dann **Übergeben…**.

Im Chat der Aufgabe siehst du, wann sie übergeben wurde („An Pats Machine übergeben · 14:02“) und was zurückkam: angenommen, abgelehnt (mit Notiz) oder erledigt. Solange noch keine Antwort da ist, werden **Als erledigt markieren**, **Zurückstellen** und **Nicht nötig** angeboten. Um Pat zu erinnern oder die Aufgabe zurückzunehmen, sag es im Chat.

Wenn die Übergabe nicht gesendet wurde, steht das bei der Aufgabe und im Chat. Dort findest du auch **Erneut versuchen**.

## Die Aufgabe stattdessen jemand anderem übergeben

Während ein Teammitglied die Aufgabe hat, steht das in einer Zeile („Bei Pat · wartet“). Unter **…**, dann **Übergeben…**, findest du **Zurücknehmen** und **An jemand anderen übergeben**. Mit **Zurücknehmen** gehört die Aufgabe wieder dir: Pats Machine wird informiert und Pats Antwort ändert den Status nicht mehr.

Mit **An jemand anderen übergeben** öffnest du das Übergabeformular. Oder sag es im Chat der Aufgabe („die Aufgabe sollte an Kim gehen“). Dann steht bei der Aufgabe „Immer noch bei Pat, bis du sie an Kim sendest“, zusammen mit **Übergabe prüfen an** Kim.

Eine Aufgabe wird jedem Teammitglied nur einmal übergeben: Solange Pat sie hat, gilt es als Nachfragen, wenn du Pat im Übergabeformular erneut auswählst. Mit **Nachfragen** erstellst du denselben Erinnerungsentwurf, ergänzt um eine Zeile von dir, falls du eine hinzufügst.

**Von Pat zurücknehmen** ist standardmäßig aktiviert. Deaktiviere die Option, wenn beide die Aufgabe haben sollen. Es wird nichts gesendet, bis du **Übergeben** auswählst. Pats Machine wird informiert und Pats Kopie der Aufgabe verschwindet.

## Wenn die Person ablehnt

Die Person kann einen Grund nennen: Die Aufgabe gehört nicht zu ihr, ist bereits erledigt oder diese Woche ist keine Zeit dafür. Wähle dann **Selbst machen**, **An jemand anderen übergeben** oder **Als erledigt markieren**. Dasselbe gilt, wenn die Person nicht rechtzeitig antwortet. Mit **Selbst machen** wird die Aufgabe wieder zu deiner eigenen und erscheint unter „Für dich“.

## Jemand außerhalb des Network

Wähle **Per E-Mail**: Deine Machine erstellt einen E-Mail-Entwurf, den du senden kannst. Während du tippst, schlägt sie zuerst deine Fleet und dann Personen aus deinem Unternehmen vor. Füge eine Aufgabenseite hinzu, damit die Person mit einem Fingertipp antworten kann: siehe [Aufgabenseiten](task-pages.md).

Nur für Aufgaben unter „Arbeit“. Wähle aus, was mitgesendet wird: ein paar Zeilen zur Aufgabe, ihr Entwurf, Links und Dateien. Inhalte aus „Persönlich“ und „Nur für dich“ bleiben außen vor. Mit **E-Mail vorbereiten** wird die E-Mail zur Aufgabe hinzugefügt. Lies sie durch und sende sie dann aus deinem eigenen Postfach. Es gibt kein Tracking.

Eine Aufgabe aus Intercom oder Slack hat kein eigenes Postfach. Ihre E-Mail wird deshalb aus deinem geschäftlichen Postfach gesendet.

Die Aufgabe behält das Versprechen im Blick, bis die Person antwortet, dass sie erledigt ist, oder du sie als erledigt markierst. Die E-Mail endet mit „Übernimm das in deiner eigenen Machine“: Wenn die Person sich darüber anmeldet, kann sie deiner Fleet beitreten und die Aufgabe wird in ihre Machine verschoben. Du kannst diese Zeile unter Fleet in den **Einstellungen** deaktivieren.
