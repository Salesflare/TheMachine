---
title: Telegram
area: connections
summary: Bekomm deine Aufgaben über Telegram, mit denselben Buttons wie im Dashboard, über einen eigenen Bot. Optional.
covers: telegram
code: assistant.py, onboarding.py, cli.py
site: Add my bot, Add more any time, Disconnect Telegram
---
## Was es macht

Telegram ist ein Weg, deine Aufgaben zu bekommen, nichts, was The Machine liest. Dein eigener Bot schickt jede Aufgabe innerhalb deiner [Arbeitszeiten](work-hours.md), mit denselben Buttons wie im Dashboard: **Ausführen**, **Zurückstellen**, **Ändern**, **Als erledigt markieren**, **Nicht nötig** und **Senden** für eine vorbereitete Nachricht.

Telegram ist optional. Das Dashboard als App auf dem Handy schickt dieselben Aufgaben als Benachrichtigungen.

## Was es senden kann

Nur Nachrichten an dich, von deinem eigenen Bot. Eine Nachricht an jemand anderen braucht weiterhin deine Freigabe bei der Aufgabe.

## Verbinden

Auf einer gehosteten Machine:

1. Schreib in Telegram @BotFather an und sende /newbot. Kopiere das Token, das du bekommst.
2. Öffne auf deiner Einrichtungsseite unter **Jederzeit mehr hinzufügen** Telegram, füge das Token ein und tippe auf **Meinen Bot hinzufügen**.

Es gehört nicht zur Einrichtung: Füge es hinzu, wann du willst. Dein Dashboard schlägt es vor, sobald eine zurückgestellte Aufgabe sonst nur dort zurückkommen würde.

Auf deinem eigenen Computer fragt der Installer danach, oder du führst `assistant telegram on` mit deiner Telegram-Benutzer-ID aus.

## Entfernen

- Auf einer gehosteten Machine: Tippe auf deiner Einrichtungsseite auf **Telegram trennen**. Dein Bot und sein Token werden von deinem Server entfernt.
- Auf deinem eigenen Computer: `assistant telegram off`. Füge `--remove-bot` hinzu, um auch den Bot zu vergessen.

## Den Bot in Telegram löschen

Schreib @BotFather an, sende /deletebot und wähle deinen Bot.
