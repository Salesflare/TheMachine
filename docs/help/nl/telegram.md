---
title: Telegram
area: connections
summary: Krijg je to-do's op Telegram, met dezelfde knoppen als op het dashboard, via een eigen bot. Optioneel.
covers: telegram
code: assistant.py, onboarding.py, cli.py
site: Add my bot, Add more any time, Disconnect Telegram
---
## Wat het doet

Telegram is een manier om je to-do's te krijgen, niet iets wat The Machine leest. Je eigen bot stuurt elke to-do binnen je [werkuren](work-hours.md), met dezelfde knoppen als op het dashboard: **Doe het**, **Snoozen**, **Wijzigen**, **Markeer als gedaan**, **Niet nodig**, en **Versturen** voor een klaargezet bericht.

Telegram is optioneel. Het dashboard als telefoonapp stuurt dezelfde to-do's als meldingen.

## Wat het kan versturen

Alleen berichten aan jou, van je eigen bot. Een bericht aan iemand anders heeft nog altijd je goedkeuring op de to-do nodig.

## Koppelen

Op een gehoste Machine:

1. Stuur in Telegram een bericht aan @BotFather en verstuur /newbot. Kopieer het token dat je krijgt.
2. Open op je setuppagina, onder **Voeg later meer toe**, Telegram, plak het token en druk op **Mijn bot toevoegen**.

Het hoort niet bij de setup: voeg het toe wanneer je wilt. Je dashboard stelt het voor zodra een gesnoozede to-do alleen daar zou terugkomen.

Op je eigen computer vraagt het installatieprogramma erom, of voer je `assistant telegram on` uit met je Telegram-gebruikers-ID.

## Verwijderen

- Op een gehoste Machine: druk op **Telegram ontkoppelen** op je setuppagina. Je bot en het token worden van je server verwijderd.
- Op je eigen computer: `assistant telegram off`. Voeg `--remove-bot` toe om de bot ook te vergeten.

## De bot verwijderen in Telegram

Stuur een bericht aan @BotFather, verstuur /deletebot en kies je bot.
