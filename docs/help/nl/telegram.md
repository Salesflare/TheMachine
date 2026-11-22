---
title: Telegram
area: connections
summary: Ontvang je to-do's op Telegram, met dezelfde knoppen als op het dashboard, via een eigen bot. Optioneel.
covers: telegram
code: assistant.py, onboarding.py, cli.py
site: Add my bot, Add more any time, Disconnect Telegram
translated: a2b74e4831832977
---
## Wat het doet

Ontvang je to-do's in Telegram, van een eigen bot, binnen je [werkuren](work-hours.md). Elke to-do komt met de knoppen van het dashboard: **Doe het**, **Snoozen**, **Wijzigingen vragen**, **Als gedaan markeren**, **Niet nodig**, en **Versturen** voor een klaargezet bericht. Wil je dat The Machine je Telegram-chats leest, zie dan [Telegram-chats](telegram-chats.md).

Het is optioneel: de telefoonapp stuurt dezelfde to-do's als meldingen.

## Wat het kan versturen

Alleen berichten aan jou, van je eigen bot. Een bericht aan iemand anders heeft nog altijd je goedkeuring op de to-do nodig.

## Koppelen

Op een gehoste Machine:

1. Stuur in Telegram een bericht aan @BotFather en verstuur /newbot. Kopieer het token dat je krijgt.
2. Open op je installatiepagina, onder **Voeg altijd meer toe**, Telegram, plak het token en druk op **Mijn bot toevoegen**.

Voeg het toe wanneer je wilt.

Op je eigen computer vraagt het installatieprogramma erom, of voer je `assistant telegram on` uit met je Telegram-gebruikers-ID.

## Verwijderen

- Op een gehoste Machine: druk op **Telegram ontkoppelen** op je installatiepagina. Je bot en het token worden van je Machine verwijderd.
- Op je eigen computer: `assistant telegram off`. Voeg `--remove-bot` toe om de bot ook te vergeten.

## De bot verwijderen in Telegram

Stuur een bericht aan @BotFather, verstuur /deletebot en kies je bot.
