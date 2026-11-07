---
title: Versprechen
area: cards
summary: Was du zugesagt hast und was andere dir versprochen haben. Wird von selbst verfolgt.
covers: promises
code: dashboard.html, assistant.py
order: 6
---
Deine Machine erkennt Versprechen in deinen Nachrichten, in beide Richtungen, ohne dass du etwas einrichten musst.

## Wo sie stehen

Unter **Versprechen** auf der Seite Aufgaben:

- Was du zugesagt hast, und für wen: **Du hast versprochen**.
- Was andere zugesagt haben: **Dir versprochen**.

Jedes offene hat **Erledigt** und **Entfernen**. Ein offenes Versprechen wird zur Aufgabe, wenn es fällig ist, und erscheint an seinem Tag im [Kalender](calendar.md). Ist es schon eine Aufgabe, führt es zu ihr, und **Erledigt** oder **Entfernen** schließt diese Aufgabe mit. Sieht deine Machine, dass es erledigt ist, schließen beide, mit einer Zeile dazu.

Vorher liest deine Machine, was danach kam. Schon gehalten, etwa durch eine Antwort von dir oder ein Meeting dazu? Dann schließt es sich als gehalten, ohne Aufgabe.

Eins ohne Datum zeigt seinen Tag zum **Nachfassen**: drei Tage, nachdem du es gesagt hast, eine Woche, nachdem die andere Person es gesagt hat. Dann noch offen? Dann wird es zur Aufgabe.

Eine Slack-Nachricht nennt ihren Absender nur mit seiner Slack-ID. Deine Machine schlägt den Namen nach, damit Versprechen die Person zeigen, nicht die ID.

Auf deinem eigenen Computer listet `assistant promises` sie ebenfalls auf. Der [Wochenrückblick](weekly-recap.md) zählt gehaltene und offene.
