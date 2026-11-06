---
title: Geschiedenis
area: connections
summary: Ongeveer een jaar oudere mails, vergaderingen en WhatsApp-chats, om te zoeken en te lezen. Nooit een taak.
covers: history
code: machine/app/history.py, machine/store/history.py
keywords: older messages, backfill, archive, past emails
---
## Wat ze bewaart

Elk e-mailaccount, elke agenda en WhatsApp bewaart ongeveer een jaar oudere berichten en vergaderingen. Zoeken vindt ze, een gesprek toont ze en de [Agenda](calendar.md) toont vergaderingen uit het verleden.

De kaart zegt hoe ver ze teruggaat: **Geschiedenis: terug tot** een maand, zodra ze binnen is.

## Wat ze nooit doet

Geschiedenis is er alleen om dingen op te zoeken. Ze maakt nooit een taak of een belofte, komt nooit in een check, telt nooit als nieuw en gaat nooit naar je Graph of je team. Geen AI-model leest ze.

Taken en beloftes komen nog altijd alleen uit nieuwe berichten, zoals voorheen.

## Wanneer ze loopt

Ze begint zodra de eerste blik op je berichten klaar is en loopt traag op de achtergrond. Ze wacht terwijl een check of een synchronisatie loopt, en als je Machine weinig schijfruimte of geheugen heeft. Na een herstart gaat ze verder waar ze was.

Ze gebruikt de toegang die elke koppeling al heeft. Er wordt niets nieuws gevraagd.

## Hoe ver terug

Standaard ongeveer een jaar. Zelf gehoste Machines kunnen `history_days` instellen in de configuratie (0 zet ze uit, tot 730). Telegram, Slack en andere bronnen bewaren wat ze vandaag lezen.
