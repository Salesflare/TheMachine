---
title: Telegram
area: connections
summary: Lass dir deine Aufgaben über einen eigenen Bot in Telegram senden, mit denselben Schaltflächen wie im Dashboard. Optional.
covers: telegram
code: assistant.py, onboarding.py, cli.py
site: Add my bot, Add more any time, Disconnect Telegram
translated: a2b74e4831832977
---
## So funktioniert es

Lass dir deine Aufgaben während deiner [Arbeitszeiten](work-hours.md) in Telegram von einem eigenen Bot senden. Für jede Aufgabe gibt es dieselben Schaltflächen wie im Dashboard: **Ausführen**, **Zurückstellen**, **Änderungen anfragen**, **Erledigt**, **Nicht nötig** und **Senden** für eine vorbereitete Nachricht. Wenn The Machine stattdessen deine Telegram-Chats lesen soll, findest du mehr unter [Telegram-Chats](telegram-chats.md).

Die Telegram-Integration ist optional: Die Handy-App sendet dieselben Aufgaben als Benachrichtigungen.

## Was gesendet werden kann

Nur Nachrichten von deinem eigenen Bot an dich. Nachrichten an andere müssen weiterhin von dir in der Aufgabe freigegeben werden.

## Verbinden

Auf einer gehosteten Machine:

1. Schreib in Telegram an @BotFather und sende /newbot. Kopiere den Token, den du erhältst.
2. Öffne auf deiner Einrichtungsseite unter **Jederzeit mehr hinzufügen** den Bereich Telegram, füge den Token ein und klicke auf **Meinen Bot hinzufügen**.

Du kannst den Bot jederzeit hinzufügen.

Auf deinem eigenen Computer fragt dich das Installationsprogramm danach. Oder führe `assistant telegram on` mit deiner Telegram-Nutzer-ID aus.

## Entfernen

- Auf einer gehosteten Machine: Klicke auf deiner Einrichtungsseite auf **Telegram trennen**. Dein Bot und sein Token werden von deiner Machine entfernt.
- Auf deinem eigenen Computer: `assistant telegram off`. Füge `--remove-bot` hinzu, um den Bot ebenfalls zu löschen.

## Bot in Telegram löschen

Schreib an @BotFather, sende /deletebot und wähle deinen Bot aus.
