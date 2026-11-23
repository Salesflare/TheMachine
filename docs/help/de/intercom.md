---
title: Intercom
area: connections
summary: Kundengespräche in deinem Intercom-Arbeitsbereich. Sie antwortet erst, wenn du sendest, und zwar in deinem Namen.
covers: connector:intercom
code: connectors/intercom.py, onboarding.py
site: Sign in with Intercom, More sources, Remove
translated: 5a6938dd6c220a43
---
## Was sie liest

Kundengespräche in deinem Intercom-Arbeitsbereich: die letzten 7 Tage ab dem Zeitpunkt der Verbindung und danach neue Gespräche, sobald sie eingehen. Außerdem liest sie, zu welchem Arbeitsbereich und Teammitglied die Anmeldung gehört.

## Was sie kann

Mit deinem eigenen **Mit Intercom anmelden** kann sie in einem Gespräch in deinem Namen antworten, aber erst, nachdem du bei genau diesem Text auf **Senden** getippt hast. Sie weist nichts zu, schließt nichts, fügt keine Tags hinzu und schreibt keine Notizen. Ein Intercom-Konto, das über deine Fleet mit dir geteilt wird, liest nur mit.

## Aufgaben aus Intercom

Eine Aufgabe aus Intercom zeigt den Kunden an. Mit **Nachricht lesen** öffnest du das Gespräch und einen Link dazu in Intercom. Bei jeder Nachricht steht, wer sie geschrieben hat: auf der einen Seite der Kunde, auf der anderen dein Team und sein Bot. Das gilt auch, wenn ein Teammitglied oder eine Kampagne das Gespräch begonnen hat. Die Antwort wird in diesem Gespräch gesendet, es sei denn, du bittest um eine E-Mail.

Nur Gespräche, die dir oder noch niemandem zugewiesen sind, werden zu Aufgaben. Wenn ein Teammitglied ein Gespräch in Intercom übernimmt, wird die Aufgabe automatisch geschlossen und du kannst sie mit **Rückgängig** wieder öffnen. Bei einem Intercom-Konto, das mit dir geteilt wird, gehören die Gespräche dir, die dem Teammitglied zugewiesen sind, in dessen Namen du schreibst.

Eine Intercom-Aufgabe wird auch automatisch geschlossen, sobald jemand im Team das Gespräch in Intercom schließt oder darauf antwortet und der Kunde danach nichts mehr schreibt, wenn die Aufgabe nur eine Antwort verlangt hat. Das gilt auch, wenn du geantwortet hast, kurz bevor die Aufgabe einging, also noch bevor The Machine deine Antwort gelesen hatte. Eine Notiz, Zurückstellen oder die Antwort eines Bots zählen nie.

Wenn deine Machine in Intercom nicht antworten kann (du hast bei einem mit dir geteilten Konto nur Lesezugriff, Antworten sind deaktiviert oder Intercom ist nicht verbunden), wird der Entwurf stattdessen als E-Mail erstellt. In der Aufgabe steht warum und du wirst gefragt: **Stattdessen per E-Mail senden?** Um in Intercom zu antworten, tippe in der Aufgabe auf **Eigenes Intercom verbinden** und melde dich an. Danach wird die Aufgabe erneut als Antwort in Intercom erstellt. Es wird nichts gesendet, bevor du es abschickst.

Dein eigenes Intercom-Konto und ein mit dir geteiltes Konto für denselben Arbeitsbereich lesen nicht beide mit: Das geteilte Konto pausiert und seine Gespräche werden in dein eigenes Konto verschoben, jeweils nur einmal.

## Verbinden

1. Im Dashboard: **Verbindungen**, **Kunden**, Intercom. Oder auf der Einrichtungsseite einer gehosteten Machine unter app.themachine.computer/setup: **Weitere Quellen**, Intercom. Auf deinem eigenen Computer musst du sie zuerst mit deinem Konto koppeln.
2. Tippe auf **Mit Intercom anmelden**.
3. Genehmige The Machine (von Salesflare) in Intercom. Du kehrst anschließend dorthin zurück, wo du angefangen hast.

Wenn du dich bei einem anderen Arbeitsbereich anmeldest, wird ein zweites Intercom-Konto hinzugefügt.

Intercom zählt immer als Arbeit und wird dem Unternehmen zugeordnet, nach dem der Arbeitsbereich benannt ist.

## Entfernen

- Im Dashboard: **Verbindungen**, öffne Intercom und tippe auf **Details** und dann auf **Trennen**. Intercom liest dann nichts mehr. Was bereits übernommen wurde, bleibt erhalten.
- Auf einer gehosteten Machine kannst du auf der Einrichtungsseite auch neben Intercom auf **Entfernen** tippen.

## Intercom deinstallieren

Öffne in Intercom Einstellungen, Apps, Installierte Apps und entferne The Machine.
