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

Bekannte, die im Network sind, werden sofort vorgeschlagen, wenn du das einschaltest, und auch, wenn später jemand beitritt. Ein Treffer kommt mit Verbinden, Nicht jetzt oder **Nie vorschlagen**. **Network verlassen** nimmt dich heraus.

## Termine mit anderen Machines

Schreibt jemand mit einer Machine „lass uns nächste Woche treffen“, fragt deine Machine deren Machine nach freien Zeiten und findet eine, die euch beiden passt, in deinen Arbeitszeiten. Ihr bekommt jeweils ein To-do, etwa „Treffen mit Alex Example“, darunter die Zeit. Tippe auf **Buchen**, **Andere Zeit** oder **Nicht nötig**. Die Einladung geht erst raus, wenn ihr beide auf Buchen getippt habt.

Übertragen wird nur frei oder belegt, Ende-zu-Ende-verschlüsselt, für höchstens 14 Tage und auf 15 Minuten gerundet. Private Termine zählen als belegt. Eine Machine kann nur fragen, wenn ihr euch gegenseitig gemailt habt. Stell es im Bereich Network unter **Was andere Machines meine fragen dürfen** ein: **Frei/belegt für Termine** oder **Aus**, mit Termindauer, Puffer und bevorzugten Zeiten. Jede Anfrage steht in Aktivität, unter Kalender.

Keine Machine oder keine Antwort: Der E-Mail-Entwurf bekommt einen Link, über den die andere Person eine deiner freien Zeiten wählt. Die Wahl wird ein To-do mit **Buchen**; nichts wird gebucht, bevor du tippst.

Der Link zeigt nur freie Zeiten, nach denselben Regeln, und sonst nichts über dich. Er läuft ab, sobald das Treffen gebucht ist, oder nach 14 Tagen. In der E-Mail steht er als "Pick a time". Unten sagt die Seite, dass deine Machine diese Zeiten gefunden hat, mit "Get yours." und deinem Vornamen. Schalte das mit **Fußzeile bei Buchungslinks** aus. Jeder Link und jede Wahl steht in Aktivität.

## Eine Machine auf deinem eigenen Computer

So trittst du dem Network mit einer Machine bei, die du selbst betreibst:

1. Tippe auf deiner Kontoseite bei app.themachine.computer auf **Selbst gehostete Machine koppeln**. Der Code funktioniert einmal, 15 Minuten lang.
2. Führe auf deinem Computer `assistant fleet-pair` mit dem Code aus und starte neu.

Bis zu 5 Machines pro Konto. Jede lässt sich dort trennen.
