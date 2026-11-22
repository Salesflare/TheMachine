---
title: Wochenrückblick
area: weekly
summary: Einmal pro Woche erfährst du, wie deine Machine gearbeitet hat: welche Aufgaben und Versprechen anstehen, was bei Menschen und Projekten los ist und was sie bemerkt hat. Standardmäßig aktiviert.
covers: weekly-recap
code: assistant.py, machine/app/recap_settings.py, config.example.json
order: 1
translated: 223b143a6efd5692
---
## Das ist drin

- Braucht dich: überfällige Versprechen, die andere dir gegeben haben, und deine eigenen Versprechen, die überfällig oder in den nächsten zwei Wochen fällig sind.
- Nächste Woche: deine Meetings (mit einem Link, sobald die Vorbereitung fertig ist), fällige Aufgaben und Versprechen, die andere für nächste Woche gegeben haben.
- Was sich geändert hat: wie viele Aufgaben sich gelohnt haben, verglichen mit der Woche davor, wie oft **Ausführen** gleich beim ersten Mal richtig war, was sie daran angepasst hat, wie du schreibst und welche Filter sie verwendet, und wie viele Entwürfe unverändert versendet wurden.
- Für das Team von The Machine: Erkenntnisse zum Teilen, falls welche auf dich warten. Siehe [Erkenntnisse mit dem Team teilen](share-learnings.md).
- Menschen und Projekte: welche Projekte gerade Fahrt aufnehmen oder nachlassen, wer neu ist und von wem du länger nichts gehört hast.
- Hinter den Kulissen: wie viele Signale sie diese Woche geprüft hat und wie viele noch offen sind.
- Auf [Telegram](telegram.md) folgen Auswahlmöglichkeiten, jeweils in einer eigenen Nachricht: eine aktive Quelle ohne Ergebnisse (**Nicht mehr prüfen** oder **Weiter prüfen**) und eine mehrmals zurückgestellte Aufgabe (**Nicht nötig**, **Ausführen** oder **Behalten**). Es ändert sich nichts, bis du tippst.

## Wann und wo

Standardmäßig einmal pro Woche, freitags nach 16:00 Uhr in deiner Zeitzone. Du erhältst den Rückblick über [Telegram](telegram.md) oder als Benachrichtigung mit dem Titel „Deine Woche“ über die [Handy-App](phone-app.md) und die Dashboard-App. Du erhältst ihn auch per E-Mail, wenn E-Mail für **Morgendliche Zusammenfassung** unter Einstellungen › Benachrichtigungen aktiviert ist. Mit [Vorsichtig](security-levels.md) oder wenn **Text in Benachrichtigungen** deaktiviert ist, wird er nicht per E-Mail gesendet.

## Deaktivieren

Der Wochenrückblick ist standardmäßig aktiviert. Deaktiviere ihn unter Einstellungen › Benachrichtigungen mit dem Schalter **Wochenrückblick**. Wenn du ihn deaktiviert hast, bleibt er deaktiviert. Auf deinem eigenen Computer kannst du außerdem `weekly_recap` in config.json festlegen: `enabled` false mit `chosen` true sowie optional `weekday` (1 bis 7, Freitag ist 5) und `at` ("16:00"). Siehe die [Konfigurationsanleitung](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).
