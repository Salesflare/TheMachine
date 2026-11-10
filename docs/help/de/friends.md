---
title: Freunde und das Network
area: fleet
summary: Füge Freunde über ihren Benutzernamen hinzu, finde Bekannte mit einer Machine und kopple eine Machine auf deinem eigenen Computer.
covers: friends
code: friends.py, network.py, meet.py, meet_app.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
---
## Freunde

Füge jemanden über den genauen Benutzernamen hinzu, im Tab **Fleet** unter Freunde. Freunde können fragen, wer jemanden kennt, Kontext zu Meetings und persönliche Vorstellungen bekommen und sehen, wann du belegt bist (nur belegte Zeiten, nie was). Du kannst Freunde jederzeit entfernen oder blockieren.

## Bekannte finden

Im Bereich Network:

- „Prüfen, welche meiner Kontakte eine Machine haben“ schlägt Leute vor, die du kennst.
- „Leute, die meine E-Mail-Adresse haben, dürfen mich finden“ lässt sie dich finden.

Beide sind standardmäßig an, bei der Sicherheitsstufe Vorsichtig aus. Du kannst sie jederzeit ausschalten; deine Wahl bleibt. Man findet dich über deine Anmelde-E-Mail und deine verbundenen Adressen, außer geteilten wie info@, die aus bleiben, bis du sie einschaltest.

Bekannte, die im Network sind, werden sofort vorgeschlagen, wenn du das einschaltest, und auch, wenn später jemand beitritt. Deine Machine prüft alle 15 Minuten auf neue Kontakte und Personen, die gerade beigetreten sind, und geht einmal am Tag alle deine Kontakte durch. Ein Treffer kommt mit Verbinden, Nicht jetzt oder **Nie vorschlagen**. **Network verlassen** nimmt dich heraus.

Gefundene Personen zeigen in deiner Liste Personen **Hat eine Machine**. Geprüft werden die Adressen aus deinen Nachrichten und die, die du einer Person mit **Bearbeiten** hinzugefügt hast: Hat sich jemand mit einer anderen Adresse angemeldet, füge sie der Person hinzu. Auf der Seite einer gefundenen Person sendet **Als Freund hinzufügen** dieselbe Anfrage wie Verbinden (**Als Familie hinzufügen** steht im Menü ⋯).

Bei jemandem ohne Machine zeigt **Zu The Machine einladen** den Text, den die Person bekommt, zum **Kopieren** oder **Im Mailprogramm öffnen**; selbst gesendet wird nichts.

Telefonnummern zählen auch: die Nummern aus deinen WhatsApp-Chats mit Leuten, denen du geschrieben oder die du getroffen hast, und die, die du mit **Bearbeiten** hinzugefügt hast. Deine verknüpfte WhatsApp-Nummer und die Nummern unter Über dich machen dich auffindbar, jede mit eigenem Schalter unter **Auffindbar für**. Eine Nummer findet jemanden nur, wenn diese Person dich auch gesucht hat oder ihr befreundet seid. So kann niemand Nummern durchprobieren, um zu sehen, wer eine Machine hat.

## Termine mit anderen Machines

Schreibt jemand mit einer Machine „lass uns nächste Woche treffen“, fragt deine Machine deren Machine nach freien Zeiten und findet eine, die euch beiden passt, in deinen Arbeitszeiten. Ihr bekommt jeweils ein To-do, etwa „Treffen mit Alex Example“, darunter die Zeit. Tippe auf **Buchen**, **Andere Zeit** oder **Nicht nötig**. Die Einladung geht erst raus, wenn ihr beide auf Buchen getippt habt.

Übertragen wird nur frei oder belegt, Ende-zu-Ende-verschlüsselt, für höchstens 14 Tage und auf 15 Minuten gerundet. Private Termine zählen als belegt. Eine Machine kann nur fragen, wenn ihr euch gegenseitig gemailt habt. Stell es im Bereich Network unter **Was andere Machines meine fragen dürfen** ein: **Frei/belegt für Termine** oder **Aus**, mit Termindauer, Puffer und bevorzugten Zeiten. Jede Anfrage steht in Aktivität, unter Kalender.

Keine Machine oder keine Antwort: Der E-Mail-Entwurf bekommt einen Link, über den die andere Person eine deiner freien Zeiten wählt. Die Wahl wird ein To-do mit **Buchen**; nichts wird gebucht, bevor du tippst.

Der Link zeigt nur freie Zeiten, nach denselben Regeln, und sonst nichts über dich. Er läuft ab, sobald das Treffen gebucht ist, oder nach 14 Tagen. In der E-Mail steht er als "Pick a time". Unten sagt die Seite, dass deine Machine diese Zeiten gefunden hat, mit "Get yours." und deinem Vornamen. Schalte das mit **Fußzeile bei Buchungslinks** aus. Jeder Link und jede Wahl steht in Aktivität.

## Eine Machine auf deinem eigenen Computer

So trittst du dem Network mit einer Machine bei, die du selbst betreibst:

1. Öffne im Dashboard deiner Machine die **Einstellungen** und tippe auf **Dem Network beitreten**.
2. Melde dich auf der Seite, die sich öffnet, an (oder erstelle dein Konto) und bestätige. Deine Machine übernimmt das von selbst, ohne Neustart.

Der Weg mit Code funktioniert weiter: Tippe auf deiner Kontoseite bei app.themachine.computer auf **Selbst gehostete Machine koppeln**, führe dann auf deinem Computer `assistant fleet-pair` mit dem Code aus und starte neu. Der Code funktioniert einmal, 15 Minuten lang.

Bis zu 5 Machines pro Konto. Jede lässt sich dort trennen.
