---
title: Wochenrückblick
area: weekly
summary: Einmal pro Woche, wie es deiner Machine ging: Aufgaben, Versprechen, Personen und Projekte, und was ihr aufgefallen ist. Standardmäßig aus.
covers: weekly-recap
code: assistant.py, machine/app/recap_settings.py, config.example.json
order: 1
---
## Was drinsteht

- Deine Woche mit The Machine und wie viele Aufgaben sich gelohnt haben, verglichen mit der Woche davor.
- Aufgaben: neu, erledigt, verworfen und zurückgestellt, und wie schnell du geantwortet hast.
- Versprechen: deine gehaltenen und offenen, die von anderen, die eingelöst wurden oder noch ausstehen.
- Erkenntnisse zum Teilen mit dem Team von The Machine, falls welche auf dich warten. Siehe [Erkenntnisse mit dem Team teilen](share-learnings.md).
- Personen und Projekte, etwa wer still geworden ist.
- Was mir aufgefallen ist: Entwürfe, die unverändert oder bearbeitet gesendet wurden, Aufgaben, die innerhalb von Minuten verworfen wurden, Aufgaben, die mehr als einmal zurückgestellt wurden.
- Hinter den Kulissen: wie viele Signale sie diese Woche geprüft hat und wie viele noch warten.
- Auswahl, jede in einer eigenen Nachricht nach dem Rückblick: eine aktive Quelle ohne Ergebnisse (**Nicht mehr prüfen** oder **Weiter prüfen**) und eine Aufgabe, die mehr als einmal zurückgestellt wurde (**Nicht nötig**, **Ausführen** oder **Behalten**). Nichts ändert sich, bevor du tippst.

## Wann und wo

Einmal pro Woche, standardmäßig freitags nach 16:00 in deiner Zeitzone. Er kommt über [Telegram](telegram.md) oder als Benachrichtigung mit dem Titel „Deine Woche“ aus der [App auf dem Handy](phone-app.md).

## Einschalten

Er ist standardmäßig aus. Schalte ihn in Einstellungen › Benachrichtigungen mit dem Schalter **Wochenrückblick** ein. Auf deinem eigenen Computer kannst du auch `weekly_recap` in der config.json setzen: `enabled` auf true, und optional `weekday` (1 bis 7, Freitag ist 5) und `at` ("16:00"). Siehe den [Konfigurations-Leitfaden](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).
