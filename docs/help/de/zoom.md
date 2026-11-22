---
title: Zoom
area: connections
summary: Zusammenfassungen und Transkripte deiner Meetings, die du hostest. Die KI-Assistentin liest nur.
covers: connector:zoom
code: connectors/zoom.py, meeting_notes.py, onboarding.py
site: Connect Zoom, More sources, Remove, Sign in with Zoom
translated: 9533caa1429fb3fc
---
## Was sie liest

Die Zusammenfassung von AI Companion zu jedem Zoom-Meeting, das du hostest, und das Transkript, sofern Zoom eins erstellt hat: die letzten 7 Tage ab dem Zeitpunkt, an dem du Zoom verbindest, danach neue Zusammenfassungen und Transkripte, sobald sie verfügbar sind. Außerdem liest sie deinen Zoom-Namen und deine E-Mail-Adresse, damit sie weiß, wem die Meetings gehören.

Für Zusammenfassungen brauchst du einen kostenpflichtigen Zoom-Tarif. AI Companion muss während des Meetings eingeschaltet sein, und die Ende-zu-Ende-Verschlüsselung darf nicht aktiviert sein.

## Was sie damit macht

Jede Zusammenfassung wird dem entsprechenden Meeting in deinem Kalender zugeordnet. Sie erscheint unter „**Notizen**“ des Meetings und das Transkript unter „**Transkript**“. Beides ist mit „**Von Zoom**“ gekennzeichnet und steht neben allem, was du hinzugefügt hast. Deine Machine erstellt aus den nächsten Schritten, die dich betreffen, Aufgaben. Nichts wird gesendet, bevor du es sendest.

## Was sie kann

Sie liest nur und greift nur auf deine eigenen Meetings zu. Sie erstellt, ändert oder löscht nichts in Zoom. Deine Zoom-Anmeldung bleibt auf deiner Machine.

## Verbinden

Auf einer gehosteten Machine:

1. Öffne deine Einrichtungsseite unter app.themachine.computer/setup und gehe zu „**Weitere Quellen**“.
2. Öffne Zoom, wähle „Arbeit“ oder „Privat“ und drücke auf „**Zoom verbinden**“.
3. Melde dich bei Zoom an und erlaube The Machine von Salesflare.

Oder im Dashboard: Öffne „**Verbindungen**“, dann „**Meetings**“, wähle Zoom aus und drücke auf „**Mit Zoom anmelden**“. Danach kehrst du zum Dashboard zurück.

Auf deinem eigenen Computer, sobald er [mit deinem Konto gekoppelt ist](friends.md#a-machine-on-your-own-computer): Öffne „**Verbindungen**“, dann „**Meetings**“, wähle Zoom aus und drücke auf „**Mit Zoom anmelden**“.

## Verbindung entfernen

- Im Dashboard: Öffne „**Verbindungen**“, dann Zoom und „**Details**“. Wähle anschließend „**Trennen**“. Die Machine liest dann nichts mehr. Was sie bereits übernommen hat, bleibt erhalten.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite neben Zoom auf „**Entfernen**“ drücken.

## In Zoom deinstallieren

Melde dich unter marketplace.zoom.us an, öffne „Verwalten“ und dann „Hinzugefügte Apps“ und entferne The Machine. Sie kann dann nichts mehr lesen. Was sie bereits übernommen hat, bleibt auf deiner Machine, bis du es löschst. Mehr dazu unter [Kündigen und löschen](cancel-and-delete.md).
