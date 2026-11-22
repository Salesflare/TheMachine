---
title: Telegram
area: connections
summary: Bekomm deine Aufgaben über Telegram, mit denselben Buttons wie im Dashboard, über einen eigenen Bot. Optional.
covers: telegram
code: assistant.py, onboarding.py, cli.py
site: Add my bot, Add more any time, Disconnect Telegram
translated: a2b74e4831832977
---
## Was es macht

Bekomm deine Aufgaben in Telegram, von einem eigenen Bot, innerhalb deiner [Arbeitszeiten](work-hours.md). Jede kommt mit denselben Buttons wie im Dashboard: **Ausführen**, **Zurückstellen**, **Änderungen anfragen**, **Als erledigt markieren**, **Nicht nötig** und **Senden** für eine vorbereitete Nachricht. Soll The Machine stattdessen deine Telegram-Chats lesen, siehe [Telegram-Chats](telegram-chats.md).

Das ist optional: Die Handy-App schickt dieselben Aufgaben als Benachrichtigungen.

## Was es senden kann

Nur Nachrichten an dich, von deinem eigenen Bot. Eine Nachricht an jemand anderen braucht weiterhin deine Freigabe bei der Aufgabe.

## Verbinden

Auf einer gehosteten Machine:

1. Schreib in Telegram @BotFather an und sende /newbot. Kopiere das Token, das du bekommst.
2. Öffne auf deiner Einrichtungsseite unter **Jederzeit mehr hinzufügen** Telegram, füge das Token ein und tippe auf **Meinen Bot hinzufügen**.

Füge es hinzu, wann du willst.

Auf deinem eigenen Computer fragt der Installer danach, oder du führst `assistant telegram on` mit deiner Telegram-Benutzer-ID aus.

## Entfernen

- Auf einer gehosteten Machine: Tippe auf deiner Einrichtungsseite auf **Telegram trennen**. Dein Bot und sein Token werden von deiner Machine entfernt.
- Auf deinem eigenen Computer: `assistant telegram off`. Füge `--remove-bot` hinzu, um auch den Bot zu vergessen.

## Den Bot in Telegram löschen

Schreib @BotFather an, sende /deletebot und wähle deinen Bot.
