---
title: Versprechen
area: cards
summary: Was du zugesagt hast und was andere dir versprochen haben. Wird von selbst verfolgt.
covers: promises
code: dashboard.html, assistant.py
order: 6
translated: 0779d3fc9d3f3407
---
Deine Machine erkennt Versprechen in deinen Nachrichten, in beide Richtungen, ohne dass du etwas einrichten musst.

## Wo sie stehen

Unter **Versprechen** auf der Seite Aufgaben:

- Was du zugesagt hast, und für wen: **Du hast versprochen**.
- Was andere zugesagt haben: **Dir versprochen**.

Jedes hat ein Menü **⋯**:

- **Ausführen** bei deinen: Es wird jetzt zur Aufgabe, und deine Machine bereitet sie vor. **Erinnern** bei denen anderer: Deine Machine schreibt einen kurzen Entwurf zum Nachfassen, dort, wo es versprochen wurde, und du bleibst in der Liste. Eine kurze Meldung bestätigt es, mit **Aufgabe öffnen**. Nichts geht raus, bis du es sendest. Ist es schon eine Aufgabe, öffnet sich diese.
- **Als erledigt markieren**: Es wurde eingehalten.
- **Findet nicht statt**: Es passiert nicht, also verfolgt deine Machine es nicht mehr, ohne Aufgabe.

Ein offenes Versprechen wird auch von selbst zur Aufgabe, wenn es fällig ist (deines am Morgen davor, damit ein Tag dafür bleibt), und erscheint an seinem Tag im [Kalender](calendar.md). Ist es schon eine Aufgabe, führt es zu ihr, und **Als erledigt markieren** oder **Findet nicht statt** schließt diese Aufgabe mit. Sieht deine Machine, dass es erledigt ist, schließen beide, mit einer Zeile dazu.

Vorher liest deine Machine, was danach kam. Schon gehalten, etwa durch eine Antwort von dir oder ein Meeting dazu? Dann schließt es sich als gehalten, ohne Aufgabe.

Später ein neues Datum genannt, etwa „doch erst nächste Woche“? Dasselbe Versprechen verschiebt sich, seine Aufgabe mit, ohne ein zweites. Seine Seite zeigt das neue Datum und die neuere Nachricht.

Eins ohne Datum zeigt seinen Tag zum **Nachfassen**: drei Tage, nachdem du es gesagt hast, eine Woche, nachdem die andere Person es gesagt hat. Dann noch offen? Dann wird es zur Aufgabe.

Eine Slack-Nachricht nennt ihren Absender nur mit seiner Slack-ID. Deine Machine schlägt den Namen nach, damit Versprechen die Person zeigen, nicht die ID.

Auf deinem eigenen Computer listet `assistant promises` sie ebenfalls auf. Der [Wochenrückblick](weekly-recap.md) zählt gehaltene und offene.
