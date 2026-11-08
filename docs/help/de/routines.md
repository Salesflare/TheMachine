---
title: Routinen
area: cards
summary: Arbeit, die deine Machine von selbst in einem Rhythmus erledigt, wie eine Montagsübersicht deiner offenen Deals. Sie liest nur.
covers: tab:routines
code: routines.py, routines_app.py, routine_imports.py, dashboard/routines-page.js
order: 10
keywords: routine, automation, scheduled, every week, every morning, report
---
## Eine anlegen

Öffne **Routinen** in der Seitenleiste und sag in einer Zeile, was sie wann tun soll: „jeden Tag um 9, fasse meine offenen Deals zusammen“ oder „jeden Werktag um 8, liste die Mails, auf die ich noch antworten muss“. Dann **Hinzufügen**.

Ohne Uhrzeit läuft sie um 8:00. Die Uhrzeit gilt auf der Uhr deiner Machine. Ihr erster Lauf gibt ihr einen kurzen Namen.

**Hinzufügen** macht zuerst einen Testlauf, damit du siehst, was sie liefert, bevor du sie behältst. Nichts wird gesendet oder gespeichert. Dann behält **Hinzufügen** sie in ihrem Rhythmus, **Ändern** probiert andere Worte und **Abbrechen** verwirft sie.

## Was eine Routine tut

Zu ihrer Zeit liest deine Machine, was sie braucht, etwa deine Nachrichten, Termine und den Graph, und legt das Ergebnis auf der Seite Routinen ab. Jedes Ergebnis zeigt **Bereit**, **Nichts Neues** (mit Grund) oder **Hat nicht geklappt** (mit Grund). Ein Lauf, der ohne Ergebnis endet, zählt als nicht geklappt, nie als erledigt.

Routinen lesen nur. Sie senden, antworten, posten oder ändern nichts.

Ein Lauf kann deinen eingeschalteten [Skills](skills.md) folgen, ausgewählt nach dem, was die Routine tut: Nur die passenden werden ganz gelesen. Das Ergebnis nennt sie unter **Verwendet:**. Ein Skill bringt eine Routine nie dazu, etwas zu senden oder zu ändern.

Deine Routinen stehen unter **Deine Routinen**, unter den Vorschlägen. Ein langes Ergebnis ist auf eine kurze Vorschau eingeklappt; **Mehr anzeigen** öffnet es.

Jeder Lauf kennt das letzte Ergebnis und kann so sagen, was sich seitdem geändert hat.

## Verpasste Tage

War deine Machine aus oder beschäftigt, stapeln sich verpasste Läufe nicht: Nur der neueste läuft, einmal. Jedes Datum läuft einmal, auch nach einem Neustart.

Routinen laufen nacheinander und warten, wenn das Nutzungslimit deines KI-Abos knapp wird, wie alle Arbeit im Hintergrund. **Jetzt ausführen** startet sie sofort; ihr Ergebnis erscheint auf der Karte, sobald es fertig ist.

## Ändern oder stoppen

Das steht im ⋯-Menü der Routine. **Bearbeiten** ändert, was sie tut; wann sie läuft und ihre bisherigen Ergebnisse bleiben. **Zeitpunkt ändern** nimmt einen neuen Rhythmus in deinen eigenen Worten, wie „jeden Werktag um 8“. Beide haben **Speichern** und **Abbrechen**; am Computer brechen auch Esc oder ein Klick daneben ab.

In **Bearbeiten** lässt **Ausprobieren** die neuen Worte einmal laufen und zeigt dort das Ergebnis. Die Routine bleibt, wie sie war, bis **Speichern**.

**Pausieren** hält die Läufe an bis **Fortsetzen**; pausierte Routinen warten unten unter **Pausiert**, und was während der Pause verpasst wurde, läuft danach nicht. **Stopp** beendet eine Routine endgültig.

## Aus deinen OpenClaw-Jobs

Hast du vorher geplante Jobs in OpenClaw angelegt, liest deine Machine sie (sie ändert sie nie) und schlägt die passenden unter **Vorgeschlagen** als Routinen vor. Jeder lief einmal, damit du ein echtes Ergebnis siehst.

Deine Korrekturen am Job bleiben drin, was er gesendet oder gepostet hat, fällt weg. **Hinzufügen** macht daraus eine Routine, **Nein danke** fragt nie wieder nach diesem Job. Ein Job, der dich an etwas erinnert hat, kommt stattdessen als Angebot für eine wiederkehrende Aufgabe unter Aufgaben.

Höchstens drei Vorschläge warten gleichzeitig. Nach einer Woche guter Läufe fragt die Routine **Den alten OpenClaw-Job ausschalten?** Er wird nur ausgeschaltet, wenn du auf **Ausschalten** tippst, und du kannst ihn in OpenClaw wieder einschalten.

## Routinen und wiederkehrende Aufgaben

Eine wiederkehrende Aufgabe (recurring.md) erinnert dich daran, etwas zu tun. Eine Routine ist Arbeit, die deine Machine selbst erledigt und dir zeigt. Nimm eine wiederkehrende Aufgabe für „Miete am Ersten zahlen“ und eine Routine für „jeden Freitag sagen, welche Deals still geworden sind“.
