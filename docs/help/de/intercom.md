---
title: Intercom
area: connections
summary: Kundengespräche in deinem Intercom-Arbeitsbereich. Antworten werden erst verschickt, wenn du sie in deinem Namen sendest.
covers: connector:intercom
code: connectors/intercom.py, onboarding.py
site: Sign in with Intercom, More sources, Remove
translated: 2cbee87e6d24c0a9
---
## Was gelesen wird

Kundengespräche in deinem Intercom-Arbeitsbereich: die letzten 7 Tage beim Verbinden und danach neue Gespräche, sobald sie eingehen. Außerdem wird gelesen, zu welchem Arbeitsbereich und Teammitglied die Anmeldung gehört.

## Was möglich ist

Mit deinem eigenen **Mit Intercom anmelden** kann deine Machine in deinem Namen auf ein Gespräch antworten, aber erst, wenn du bei genau diesem Text auf **Senden** tippst. Sie weist keine Gespräche zu, schließt sie nicht, versieht sie nicht mit Tags und schreibt keine Notizen. Ein Intercom, das über deine Fleet mit dir geteilt wird, wird nur ausgelesen.

## Aufgaben aus Intercom

Eine Aufgabe aus Intercom zeigt den Kunden an. Mit **Nachricht lesen** öffnest du das Gespräch samt Link dazu in Intercom. Die Antwort wird in diesem Gespräch verschickt, außer du bittest um eine E-Mail.

Nur Gespräche, die dir oder noch niemandem zugewiesen sind, werden zu Aufgaben. Sobald ein Teammitglied ein Gespräch in Intercom übernimmt, wird die Aufgabe automatisch geschlossen. Du kannst sie mit **Rückgängig** wieder öffnen. Bei einem Intercom, das mit dir geteilt wird, zählen die Gespräche, die dem Teammitglied zugewiesen sind, in dessen Namen du schreibst.

Eine Intercom-Aufgabe wird auch automatisch geschlossen, sobald jemand im Team das Gespräch in Intercom schließt oder darauf antwortet und der Kunde danach nichts mehr geschrieben hat, wenn die Aufgabe nur eine Antwort verlangt hat. Das gilt auch, wenn du kurz vor dem Erstellen der Aufgabe geantwortet hast, bevor The Machine deine Antwort gelesen hat. Eine Notiz, ein Zurückstellen oder die Antwort eines Bots zählen nicht.

Wenn deine Machine nicht in Intercom antworten kann (weil das Intercom nur zum Lesen mit dir geteilt wird, Antworten nicht aktiviert oder es nicht verbunden ist), wird der Entwurf stattdessen als E-Mail vorbereitet. In der Aufgabe steht der Grund, und du wirst gefragt: **Stattdessen per E-Mail senden?** Um in Intercom zu antworten, tippe in der Aufgabe auf **Eigenes Intercom verbinden** und melde dich an. Anschließend wird die Aufgabe als Antwort in Intercom neu erstellt. Nichts wird verschickt, bevor du es sendest.

Dein eigenes Intercom und ein mit dir geteiltes Intercom für denselben Arbeitsbereich lesen nicht beide mit: Das geteilte Intercom bleibt inaktiv, und seine Gespräche werden jeweils einmal zu deinem Intercom verschoben.

## Verbinden

1. Öffne im Dashboard **Verbindungen**, **Kunden** und dann Intercom. Oder öffne auf der Einrichtungsseite einer gehosteten Machine unter app.themachine.computer/setup **Weitere Quellen** und dann Intercom. Auf deinem eigenen Computer musst du es zuerst mit deinem Konto koppeln.
2. Tippe auf **Mit Intercom anmelden**.
3. Genehmige The Machine (von Salesflare) in Intercom. Du kehrst dorthin zurück, wo du begonnen hast.

Wenn du dich bei einem anderen Arbeitsbereich anmeldest, wird ein zweites Intercom-Konto hinzugefügt.

Intercom zählt immer als Arbeit, und zwar für das Unternehmen, das im Namen des Arbeitsbereichs steht.

## Entfernen

- Öffne im Dashboard **Verbindungen**, dann Intercom und **Details**, und tippe auf **Trennen**. Intercom wird dann nicht mehr ausgelesen. Bereits übernommene Inhalte bleiben erhalten.
- Auf einer gehosteten Machine kannst du auf der Einrichtungsseite auch neben Intercom auf **Entfernen** tippen.

## Intercom deinstallieren

Öffne in Intercom **Einstellungen**, **Apps** und **Installierte Apps**, und entferne The Machine.
