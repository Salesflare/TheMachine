---
title: Zoom
area: connections
summary: Die Zusammenfassungen und Transkripte von AI Companion für Meetings, die du hostest. Es liest nur.
covers: connector:zoom
code: connectors/zoom.py, meeting_notes.py, onboarding.py
site: Connect Zoom, More sources, Remove, Sign in with Zoom
---
## Was es liest

Die Zusammenfassung von AI Companion zu jedem Zoom-Meeting, das du hostest, und das Transkript, wenn Zoom eins hat: die letzten 7 Tage beim Verbinden, danach neue, sobald sie reinkommen. Es liest auch deinen Zoom-Namen und deine E-Mail-Adresse, um zu wissen, wessen Meetings es sind.

Zusammenfassungen brauchen einen bezahlten Zoom-Tarif, eingeschaltetes AI Companion während des Meetings und keine Ende-zu-Ende-Verschlüsselung.

## Was es damit macht

Jede Zusammenfassung wird dem Meeting in deinem Kalender zugeordnet. Die Zusammenfassung steht in den **Notizen** dieses Termins und das Transkript in seinem **Transkript**, markiert mit **Von Zoom**, neben allem, was du dort hinzugefügt hast; sie ersetzt es nie. Deine Prüfungen nutzen sie dann für die Nachbereitung dieses Meetings, und eine Aufteilung der Nachbereitung in der Fleet kommt schon ausgefüllt, mit wer was macht. Du prüfst und bearbeitest sie zuerst. Nichts wird gesendet, bis du es sendest.

## Was es tun kann

Es liest nur. Es erstellt, ändert oder löscht nie etwas in Zoom und sieht nur deine eigenen Meetings. Deine Zoom-Anmeldung bleibt auf deiner eigenen Machine.

## Verbinden

Auf einer gehosteten Machine:

1. Öffne deine Einrichtungsseite unter app.themachine.computer/setup und geh zu **Weitere Quellen**.
2. Öffne Zoom, wähle Arbeit oder privat und tippe auf **Zoom verbinden**.
3. Melde dich bei Zoom an und erlaube The Machine. Es kommt von Salesflare.

Oder im Dashboard: **Verbindungen**, **+ Hinzufügen**, wähle Zoom und tippe auf **Mit Zoom anmelden**. Danach bist du zurück im Dashboard.

Auf deinem eigenen Computer, sobald er [mit deinem Konto gekoppelt](fleet.md) ist: Öffne **Verbindungen**, dann **+ Hinzufügen**, wähle Zoom und tippe auf **Mit Zoom anmelden**.

## Entfernen

- Im Dashboard: **Verbindungen**, Zoom öffnen, **Details**, dann **Trennen**. Es hört auf zu lesen. Was es schon reingebracht hat, bleibt.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** tippen.

## Bei Zoom deinstallieren

Melde dich bei marketplace.zoom.us an, öffne Manage, dann Added Apps, und entferne The Machine. Sie kann dann nichts mehr lesen. Was sie schon reingebracht hat, bleibt auf deiner Machine, bis du es löschst: siehe [Kündigen oder löschen](cancel-and-delete.md).
