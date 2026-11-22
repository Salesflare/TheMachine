---
title: Freunde und das Network
area: fleet
summary: Füge Freunde über ihren Nutzernamen hinzu, finde Bekannte mit einer Machine und verbinde eine Machine auf deinem eigenen Computer.
covers: friends
code: friends.py, network.py, meet.py, meet_app.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
translated: 637784bf811800bb
---
## Freunde

Füge jemanden mit dem exakten Nutzernamen im Tab **Fleet** unter **Freunde** hinzu. Freunde können fragen, wer jemanden kennt, Kontext zu Besprechungen und persönliche Vorstellungen bekommen und sehen, wann du beschäftigt bist. Sie sehen nur, wann du beschäftigt bist, nie womit. Du kannst Freunde jederzeit entfernen oder blockieren.

## Bekannte finden

Unter **Fleet** und **Network**:

- **„Prüfen, welche meiner Kontakte eine Machine haben“** schlägt dir Bekannte vor.
- **„Leute, die meine E-Mail-Adresse haben, dürfen mich finden“** hilft anderen, dich zu finden.

Beides ist standardmäßig aktiviert und auf der Sicherheitsstufe „Vorsichtig“ deaktiviert. Du kannst jede Option jederzeit ausschalten. Deine Auswahl bleibt gespeichert. Andere können dich über deine Anmelde-E-Mail-Adresse finden. Diese Option ist immer aktiviert. Für verbundene Adressen gibt es jeweils einen eigenen Schalter unter **Auffindbar für**. Gemeinsame Adressen wie info@ bleiben deaktiviert, bis du sie einschaltest.

Wenn du die Funktion aktivierst, erscheinen Bekannte sofort als Aufgabe und später, sobald sie dem Network beitreten. Bei jeder Person kannst du **Freund** oder **Familie** auswählen (**Verbinden** bei Kolleginnen und Kollegen), **Nicht jetzt** wählen oder im Menü ⋯ **Nie vorschlagen** auswählen. Sobald ihr befreundet seid, wird die Person nicht mehr vorgeschlagen. Mit **Network verlassen** verlässt du das Network.

Bei gefundenen Personen steht in deiner Personenliste **Hat eine Machine**. Dafür werden die Adressen in deinen Nachrichten und die Adressen geprüft, die du über **Bearbeiten** zu einer Person hinzugefügt hast. Hat sich jemand mit einer anderen Adresse registriert, füge sie der Person hinzu. Auf der Seite einer gefundenen Person sendet **Als Freund hinzufügen** dieselbe Anfrage wie **Verbinden**. **Als Familie hinzufügen** findest du im Menü ⋯.

Bei Personen ohne Machine wird **Zu The Machine einladen** angezeigt. Damit öffnest du die E-Mail, die sie erhalten, unter **Diese E-Mail senden?**. Du kannst den Text ändern, wie bei jeder anderen Aufgabe. Die E-Mail wird erst mit **Jetzt senden** verschickt. Wenn du das Fenster schließt, bleibt die Einladung als Aufgabe offen. Wenn kein Postfach zum Senden verfügbar ist, kannst du **Kopieren** oder **Im Mailprogramm öffnen** wählen.

Es zählen auch Telefonnummern: die Nummern in deinen WhatsApp-Chats mit Personen, denen du geschrieben hast oder die du getroffen hast, sowie Nummern, die du über **Bearbeiten** hinzugefügt hast. Über deine verknüpfte WhatsApp-Nummer und die Nummern unter „Über dich“ bist du auffindbar. Für jede gibt es einen eigenen Schalter unter **Auffindbar für**. Eine Nummer findet jemanden nur, wenn die Person auch nach dir gesucht hat oder ihr befreundet seid. So kann niemand Nummern ausprobieren, um herauszufinden, wer eine Machine hat.

## Termine mit anderen Machines

Wenn jemand mit einer Machine schreibt: „Lass uns nächste Woche treffen“, fragt deine Machine deren Machine nach freien Zeiten und sucht innerhalb deiner Arbeitszeiten einen passenden Termin für euch beide. Ihr bekommt jeweils eine Aufgabe, zum Beispiel „Treffen mit Alex Example“, mit der Uhrzeit darunter. Tippe auf **Buchen**, **Andere Zeit** oder **Nicht nötig**. Die Einladung wird erst verschickt, wenn ihr beide auf „Buchen“ getippt habt.

Es werden nur freie oder belegte Zeiten Ende-zu-Ende verschlüsselt übertragen, höchstens 14 Tage im Voraus und auf 15 Minuten gerundet. Private Termine zählen als belegt. Eine Machine kann nur dann anfragen, wenn ihr euch beide schon E-Mails geschickt habt. Lege unter **Was andere Machines meine Machine fragen dürfen** fest, ob **Frei/belegt für Termine** oder **Aus** gilt. Dort kannst du auch die Länge des Termins, den zeitlichen Puffer und deine bevorzugten Zeiten einstellen. Jede Anfrage wird unter **Aktivität** im Bereich **Kalender** angezeigt.

Wenn die andere Person keine Machine hat oder nicht antwortet, enthält der E-Mail-Entwurf einen Link, über den sie eine deiner freien Zeiten auswählen kann. Die Auswahl erscheint als Aufgabe mit **Buchen**. Der Termin wird erst gebucht, wenn du darauf tippst.

Der Link zeigt nach denselben Regeln nur freie Zeiten und nichts anderes über dich. Er läuft ab, sobald der Termin gebucht ist, spätestens aber nach 14 Tagen. In der E-Mail wird er als „Zeit auswählen“ angezeigt. Unten auf der Seite steht „Alex' Machine hat diese Zeiten gefunden. Hol dir deine.“, mit deinem Vornamen. Deaktiviere das unter **Fußzeile bei Buchungslinks**. Jeder Link und jede Auswahl wird unter **Aktivität** angezeigt.

## Eine Machine auf deinem eigenen Computer

So trittst du mit einer selbst betriebenen Machine dem Network bei:

1. Öffne im Dashboard deiner Machine die **Einstellungen** und klicke auf **Dem Network beitreten**.
2. Melde dich auf der Seite, die sich öffnet, an oder erstelle ein Konto und bestätige. Deine Machine übernimmt die Änderung automatisch. Ein Neustart ist nicht nötig.

Du kannst auch weiterhin die Code-Methode verwenden: Klicke auf der Kontoseite bei app.themachine.computer auf **Selbst gehostete Machine koppeln**. Führe dann `assistant fleet-pair` mit dem Code auf deinem Computer aus und starte neu. Der Code kann einmal verwendet werden und ist 15 Minuten gültig.

Pro Konto sind bis zu 5 Machines möglich. Du kannst jede davon dort trennen.
