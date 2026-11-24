---
title: Freunde und das Network
area: fleet
summary: Füge Freunde über ihren Nutzernamen hinzu, finde Bekannte mit einer Machine und verbinde eine Machine auf deinem eigenen Computer.
covers: friends
code: friends.py, network.py, meet.py, meet_app.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
translated: 70a39b4999d112b7
---
## Freunde

Füge jemanden mit dem exakten Nutzernamen im Tab **Fleet** unter „Freunde“ hinzu. Freunde können fragen, wer jemanden kennt, Kontext zu Besprechungen erhalten und sich persönlich vorstellen lassen. Außerdem sehen sie, wann du beschäftigt bist, aber nur die belegten Zeiten, nie den Grund. Für Tage, zu denen dein Kalender nichts sagt, wird der Status als unbekannt angezeigt, nicht als frei. Du kannst Freunde jederzeit entfernen oder blockieren.

## Bekannte finden

Unter **Network** in **Fleet**:

- **„Prüfen, welche meiner Kontakte eine Machine haben“** schlägt dir Bekannte vor.
- **„Personen mit meiner E-Mail-Adresse erlauben, mich zu finden“** macht dich für sie auffindbar.

Beide Optionen sind standardmäßig aktiviert und auf der Sicherheitsstufe Careful deaktiviert. Du kannst jede der beiden jederzeit ausschalten. Deine Auswahl bleibt gespeichert. Andere können dich über deine Anmelde-E-Mail-Adresse finden, die immer aktiviert ist, und über deine verbundenen Adressen. Für jede Adresse gibt es einen eigenen Schalter unter **Auffindbar für**. Gemeinsame Adressen wie info@ bleiben deaktiviert, bis du sie einschaltest.

Bekannte erscheinen sofort als Aufgabe, sobald du die Funktion aktivierst, und später, wenn sie dem Network beitreten. Bei jeder Person hast du die Optionen **Freund** und **Familie** (**Verbinden** bei Kolleginnen und Kollegen), **Nicht jetzt** und **Nie vorschlagen** im Menü ⋯. Sobald ihr befreundet seid, wird die Person nicht mehr vorgeschlagen. Mit **Network verlassen** verlässt du das Network.

Bei gefundenen Personen steht in deiner Personenliste **Hat eine Machine**. Dafür werden die Adressen in deinen Nachrichten und die Adressen verwendet, die du einer Person über **Bearbeiten** hinzugefügt hast. Wenn sich jemand mit einer anderen Adresse registriert hat, füge sie der Person hinzu. Auf der Seite einer gefundenen Person sendet **Als Freund hinzufügen** dieselbe Anfrage wie **Verbinden** (**Als Familie hinzufügen** findest du im Menü ⋯).

Bei Personen ohne Machine wird **Zu The Machine einladen** angezeigt. Damit öffnest du die E-Mail, die sie erhalten, unter **Diese E-Mail senden?**. Es ist dieselbe E-Mail wie bei jeder anderen Aufgabe und du kannst sie bei Bedarf ändern. Vor **Jetzt senden** wird nichts verschickt. Wenn du das Fenster schließt, bleibt die Einladung als Aufgabe erhalten. Wenn dein Mailprogramm keine E-Mails senden kann, nutze **Kopieren** oder **Im Mailprogramm öffnen**.

Auch Telefonnummern werden berücksichtigt: die Nummern in deinen WhatsApp-Chats mit Personen, denen du geschrieben hast oder die du getroffen hast, sowie die Nummern, die du über **Bearbeiten** hinzugefügt hast. Deine verknüpfte WhatsApp-Nummer und die Nummern im Abschnitt „Über dich“ machen dich auffindbar. Für jede Nummer gibt es einen eigenen Schalter unter **Auffindbar für**. Eine Nummer findet jemanden nur, wenn die Person ebenfalls nach dir gesucht hat oder ihr befreundet seid. So kann niemand Nummern ausprobieren, um herauszufinden, wer eine Machine hat.

## Termine mit anderen Machines finden

Wenn dir jemand mit einer Machine schreibt: „Lass uns nächste Woche treffen“, fragt deine Machine deren Machine nach freien Zeiten und sucht innerhalb deiner Arbeitszeiten eine passende Zeit für euch beide. Ihr bekommt jeweils eine Aufgabe, zum Beispiel „Alex Beispiel treffen“, mit der Zeit darunter. Tippe auf **Buchen**, **Andere Zeit** oder **Nicht nötig**. Die Einladung wird erst verschickt, wenn ihr beide auf „Buchen“ getippt habt.

Es werden nur freie oder belegte Zeiten übertragen, durchgehend Ende-zu-Ende-verschlüsselt, höchstens 14 Tage im Voraus und auf 15 Minuten gerundet. Private Termine gelten als belegt. Eine Machine kann nur anfragen, wenn ihr euch beide schon E-Mails geschickt habt. Lege das unter **Was andere Machines meine Machine fragen dürfen** fest: **Frei/belegt für Termine** oder **Aus**. Dort kannst du auch die Dauer deiner Termine, den Puffer und bevorzugte Zeiten einstellen. Jede Anfrage erscheint unter „Kalender“ in der Aktivität.

Eine Zeit gilt nur dann als frei, wenn dein Kalender das anzeigt. Deine Machine bietet keine Zeiten an, wenn kein Kalender verbunden ist, der Kalender einen Tag lang nicht gelesen werden konnte oder es um mehr als 30 Tage im Voraus geht. Ganztägige Termine gelten als belegt, wenn sie als „Belegt“ markiert sind. Als „Frei“ markierte Termine gelten nie als belegt. Ein ganztägiger Termin, den eine Aufgabe hinzufügt, ist als „Frei“ markiert, außer du bist an diesen Tagen abwesend oder hast sie anderweitig verplant. In diesem Fall wird vor dem Hinzufügen „belegt“ angezeigt.

Wenn dort keine Machine ist oder keine Antwort kommt, enthält der E-Mail-Entwurf einen Link, über den die andere Person eine deiner freien Zeiten auswählen kann. Ihre Auswahl erscheint als Aufgabe mit **Buchen**. Gebucht ist der Termin erst, wenn du darauf tippst.

Der Link zeigt nur freie Zeiten nach denselben Regeln und keine weiteren Informationen über dich. Er läuft ab, sobald der Termin gebucht wurde oder nach 14 Tagen. In der E-Mail wird er als „Zeit auswählen“ angezeigt. Unten auf der Seite steht „Alex’ Machine hat diese Zeiten gefunden. Hol dir deine.“ und dein Vorname. Deaktiviere das über **Fußzeile bei Buchungslinks**. Jeder Link und jede Auswahl erscheint in der Aktivität.

## Eine Machine auf deinem eigenen Computer

So trittst du dem Network über eine Machine bei, die du selbst betreibst:

1. Öffne im Dashboard deiner Machine die **Einstellungen** und tippe auf **Dem Network beitreten**.
2. Melde dich auf der geöffneten Seite an oder erstelle ein Konto und bestätige. Deine Machine übernimmt die Änderung automatisch, ein Neustart ist nicht nötig.

Die Methode mit Code funktioniert weiterhin: Tippe auf der Kontoseite unter app.themachine.computer auf **Selbst gehostete Machine koppeln**. Führe dann `assistant fleet-pair` mit dem Code auf deinem Computer aus und starte neu. Der Code kann einmal verwendet werden und ist 15 Minuten gültig.

Pro Konto sind bis zu 5 Machines möglich. Jede davon kannst du dort trennen.
