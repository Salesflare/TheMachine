---
title: Telegram-Chats
area: connections
summary: Deine Telegram-Chats und kleinen Gruppen, gelesen als Gerät deines eigenen Kontos. Antworten erst nach deiner Freigabe.
covers: connector:telegram
code: onboarding.py, telegram_mirror.py, telegram_store.py, next_actions.py
---
## Was es liest

Deine privaten Chats und Gruppen mit bis zu 50 Personen, als angemeldetes Gerät deines eigenen Telegram-Kontos, wie Telegram Desktop. Beim Verbinden liest es die letzten 7 Tage, danach, was neu reinkommt.

Kanäle, Bots, Gespeicherte Nachrichten und Telegrams eigene Servicemeldungen liest es nie. Stummgeschaltete und archivierte Chats lässt es auch aus.

Dein Gelesen- und Online-Status bleibt unberührt: Nichts wird als gelesen markiert, und dein Handy zeigt neue Nachrichten weiter als neu.

Das ist getrennt von [Telegram](telegram.md), wo dein eigener Bot dir deine Aufgaben schickt.

## Was es senden kann

Einen Text in einen Chat, den es schon gibt, erst nachdem du ihn bei der Aufgabe freigegeben hast. Nachrichten gehen einzeln raus, mit einer Pause dazwischen.

Kam eine Aufgabe per E-Mail rein, aber du schreibst mit der Person über Telegram, sag es im Chat der Aufgabe. The Machine findet euren bestehenden Chat und stellt den Entwurf auf Telegram um, damit du ihn prüfst und sendest. Sie startet nie einen neuen Chat.

## Verbinden

1. Öffne im Dashboard **Verbindungen**, dann **+ Hinzufügen**, und wähle Telegram-Chats.
2. Wähle **QR-Code in Telegram auf deinem Handy scannen**.
3. Öffne auf deinem Handy in Telegram Einstellungen, Geräte, **Link Desktop Device**, und scanne den Code.
4. Hat dein Konto ein Cloud-Passwort, gib es ein, wenn danach gefragt wird. Es geht an Telegram und wird nie gespeichert.

Du richtest es auf deinem Handy ein und hast keinen zweiten Bildschirm zum Scannen? Wähle stattdessen **Code in Telegram für deine Telefonnummer anfordern**. Das Formular sagt, wohin Telegram den Code geschickt hat: an deine Telegram-App auf einem anderen Gerät, per SMS oder an deine Login-E-Mail. Kein Code? Drück **Code erneut senden**.

Auf deinem eigenen Computer brauchst du außerdem eine eigene Telegram-App-ID. Erstelle eine auf [my.telegram.org](https://my.telegram.org), unter API development tools, und trag ihre api_id und api_hash ins Formular ein.

Oder führe `assistant connect telegram` in einem Terminal aus und scanne den Code, den es dort zeigt.

## Wenn es aufhört

- **Von Telegram abgemeldet**: Telegram hat die Anmeldung dieses Geräts beendet, oder du hast es auf deinem Handy abgemeldet. Tippe auf seiner Karte auf **Neu verbinden**.
- **Telegram akzeptiert die App-ID nicht mehr**: Telegram akzeptiert die App-ID, die diese Machine nutzt, nicht mehr. Nichts wird gelesen oder gesendet, bis du auf **Neu verbinden** tippst und eine eigene App-ID hinzufügst.

The Machine nutzt dafür die API von Telegram. Telegram kann Anmeldungen von Apps wie ihr einschränken oder beenden.

## Entfernen

**Verbindungen**, Telegram-Chats öffnen, **Details**, dann **Trennen**. Deine Machine meldet sich bei Telegram ab und löscht, was sie für Telegram gespeichert hat.

Oder beende es auf deinem Handy: Öffne in Telegram Einstellungen, Geräte, tippe auf The Machine und beende die Sitzung.
