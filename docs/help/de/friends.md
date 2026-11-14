---
title: Freunde und Network
area: fleet
summary: Füge Freunde über ihren Nutzernamen hinzu, finde Bekannte mit einer Machine und verbinde eine Machine auf deinem eigenen Computer.
covers: friends
code: friends.py, network.py, meet.py, meet_app.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
translated: 3565b3898b234575
---
## Freunde

Füge jemanden in der Registerkarte **Fleet** unter **Freunde** mit dem exakten Nutzernamen hinzu. Freunde können fragen, wer jemanden kennt, Kontext zu Meetings bekommen und sich über gemeinsame Kontakte vorstellen lassen. Außerdem sehen sie, wann du beschäftigt bist, aber nicht womit. Du kannst Freunde jederzeit entfernen oder blockieren.

## Bekannte finden

Unter **Fleet** und **Network**:

- **„Prüfen, welche meiner Kontakte eine Machine haben“** schlägt dir Bekannte vor.
- **„Personen mit meiner E-Mail-Adresse dürfen mich finden“** macht dich für diese Personen auffindbar.

Beides ist standardmäßig aktiviert und auf der Sicherheitsstufe Careful deaktiviert. Du kannst jede Option jederzeit ausschalten. Deine Auswahl bleibt gespeichert. Andere können dich über deine Anmelde-E-Mail-Adresse (immer aktiviert) und deine verbundenen Adressen finden. Für jede Adresse gibt es unter **Auffindbar für** einen eigenen Schalter. Geteilte Adressen wie info@ bleiben deaktiviert, bis du sie einschaltest.

Bekannte werden sofort angezeigt, wenn du die Funktion einschaltest, und später, sobald sie beitreten. Für jede Person kannst du **Verbinden**, **Jetzt nicht** oder **Nie vorschlagen** auswählen. Sobald ihr befreundet seid, wird die Person nicht mehr vorgeschlagen. Mit **Network verlassen** entfernst du dich aus dem Network.

Bei Personen, die gefunden werden, steht in deiner Personenliste **Hat eine Machine**. Dafür werden die Adressen in deinen Nachrichten und die Adressen geprüft, die du einer Person über **Bearbeiten** hinzugefügt hast. Wenn sich jemand mit einer anderen Adresse registriert hat, füge sie der Person hinzu. Auf der Seite einer gefundenen Person kannst du mit **Als Freund hinzufügen** dieselbe Anfrage wie mit „Verbinden“ senden. **Als Familie hinzufügen** findest du im Menü ⋯.

Bei Personen ohne Machine gibt es die Option **Zu The Machine einladen**. Damit öffnest du die E-Mail, die sie erhalten, unter **Diese E-Mail senden?**. Es ist dieselbe E-Mail wie bei jeder Aufgabe, und du kannst sie nach Wunsch bearbeiten. Erst mit **Jetzt senden** wird sie verschickt. Wenn du das Fenster schließt, bleibt die Einladung als Aufgabe offen. Wenn kein Postfach zum Senden verfügbar ist, kannst du **Kopieren** oder **Im Mailprogramm öffnen** auswählen.

Es zählen auch Telefonnummern: die Nummern in deinen WhatsApp-Chats mit Personen, denen du geschrieben hast oder die du getroffen hast, sowie die Nummern, die du über **Bearbeiten** hinzugefügt hast. Über deine verknüpfte WhatsApp-Nummer und die Nummern unter **Über dich** können andere dich finden. Für jede Nummer gibt es unter **Auffindbar für** einen eigenen Schalter. Eine Nummer findet jemanden nur, wenn die Person auch nach dir gesucht hat oder ihr befreundet seid. So kann niemand Nummern ausprobieren, um herauszufinden, wer eine Machine hat.

## Termine mit anderen Machines planen

Wenn dir jemand mit einer Machine schreibt: „Lass uns nächste Woche treffen“, fragt deine Machine deren Machine nach freien Zeiten und sucht einen passenden Termin für euch beide innerhalb deiner Arbeitszeiten. Ihr bekommt jeweils eine Aufgabe, zum Beispiel „Alex Example treffen“, mit dem Termin darunter. Wähle **Buchen**, **Andere Zeit** oder **Nicht nötig**. Die Einladung wird erst verschickt, wenn ihr beide **Buchen** ausgewählt habt.

Nur deine Verfügbarkeit, also frei oder belegt, wird übermittelt. Sie ist Ende-zu-Ende verschlüsselt, gilt höchstens 14 Tage und wird auf 15 Minuten gerundet. Private Termine zählen als belegt. Eine Machine kann nur fragen, wenn ihr euch gegenseitig E-Mails geschickt habt. Lege unter **Was andere Machines meine fragen dürfen** fest, ob **Frei/belegt für Termine** oder **Aus** gilt, und wähle deine Termindauer, den Zeitpuffer und bevorzugte Zeiten aus. Jede Anfrage wird unter Kalender in der Aktivität angezeigt.

Wenn die andere Person keine Machine hat oder nicht antwortet, enthält der E-Mail-Entwurf einen Link, über den sie eine deiner freien Zeiten auswählen kann. Ihre Auswahl wird zu einer Aufgabe mit **Buchen**. Der Termin wird erst gebucht, wenn du die Option auswählst.

Der Link zeigt nach denselben Regeln nur freie Zeiten und sonst nichts über dich. Er läuft ab, sobald der Termin gebucht ist, oder nach 14 Tagen. In der E-Mail wird er als „Zeit auswählen“ angezeigt. Unten auf der Seite steht: „Deine Machine hat diese Zeiten gefunden. Hol dir deine.“ Dazu wird dein Vorname angezeigt. Mit **Fußzeile bei Buchungslinks** kannst du das ausschalten. Jeder Link und jede Auswahl wird in der Aktivität angezeigt.

## Eine Machine auf deinem eigenen Computer

So trittst du mit einer selbst gehosteten Machine dem Network bei:

1. Öffne im Dashboard deiner Machine die **Einstellungen** und wähle **Dem Network beitreten**.
2. Melde dich auf der geöffneten Seite an (oder erstelle ein Konto) und bestätige. Deine Machine übernimmt die Änderung automatisch, ein Neustart ist nicht nötig.

Die Methode mit dem Code funktioniert weiterhin: Wähle auf deiner Kontoseite unter app.themachine.computer **Selbst gehostete Machine koppeln**, führe dann `assistant fleet-pair` mit dem Code auf deinem Computer aus und starte neu. Der Code ist einmalig und 15 Minuten gültig.

Pro Konto sind bis zu 5 Machines möglich. Du kannst jede davon dort trennen.
