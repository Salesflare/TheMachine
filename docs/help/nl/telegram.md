---
title: Telegram
area: connections
summary: Ontvang je to-do's via Telegram met dezelfde knoppen als op het dashboard, via je eigen bot. Optioneel.
covers: telegram
code: assistant.py, onboarding.py, cli.py
site: Add my bot, Add more any time, Disconnect Telegram
translated: a2b74e4831832977
---
## Wat het doet

Ontvang je to-do's in Telegram via je eigen bot, tijdens je [Werkuren](work-hours.md). Bij elke to-do staan dezelfde knoppen als op het dashboard: **Doe het**, **Snooze**, **Wijzigingen vragen**, **Markeer als gedaan**, **Niet nodig** en **Versturen** voor een vooraf opgesteld bericht. Wil je dat The Machine in plaats daarvan je Telegram-chats leest? Bekijk dan [Telegram-chats](telegram-chats.md).

Het is optioneel: de telefoonapp stuurt dezelfde to-do's als meldingen.

## Wat het kan versturen

Alleen berichten aan jou, via je eigen bot. Voor een bericht aan iemand anders moet je de to-do nog steeds goedkeuren.

## Koppelen

Op een gehoste Machine:

1. Stuur in Telegram een bericht naar @BotFather en stuur /newbot. Kopieer het token dat je krijgt.
2. Open op je instellingenpagina onder **Altijd meer toevoegen** de optie Telegram, plak het token en druk op **Mijn bot toevoegen**.

Je kunt de bot toevoegen wanneer je maar wilt.

Op je eigen computer vraagt het installatieprogramma erom, of voer `assistant telegram on` uit met je Telegram-gebruikers-ID.

## Verwijderen

- Op een gehoste Machine: druk op **Telegram loskoppelen** op je instellingenpagina. Je bot en het token worden van je Machine verwijderd.
- Op je eigen computer: `assistant telegram off`. Voeg `--remove-bot` toe om de bot ook te vergeten.

## De bot verwijderen in Telegram

Stuur @BotFather een bericht, stuur /deletebot en kies je bot.
