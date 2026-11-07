---
title: Geschiedenis
area: connections
summary: Ongeveer een jaar oudere mails, vergaderingen en WhatsApp-chats, om te zoeken, te lezen en je mensen te kennen. Nooit een taak.
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
---
## Wat ze bewaart

Elk e-mailaccount, elke agenda en WhatsApp bewaart ongeveer een jaar oudere berichten en vergaderingen. Zoeken vindt ze, ook op betekenis, een gesprek toont ze en de [Agenda](calendar.md) toont vergaderingen uit het verleden.

De kaart zegt hoe ver ze teruggaat: **Geschiedenis: terug tot** een maand, zodra ze binnen is.

## Wat ze aan je Graph geeft

Je [Graph](graph.md) telt ze mee: hoe dicht je bij mensen staat, wanneer jullie laatst contact hadden, wie wie kent, en de mensen en organisaties zelf. De antwoorden van je Fleet op "wie kent iemand" gebruiken ze uit werkaccounts, met dezelfde [deelregels](sharing-rules.md) als nieuwe mail.

## Wat ze nooit doet

Ze maakt nooit een taak of een belofte, telt nooit als nieuw, start nooit een check en komt nooit in een project. Persoonlijke geschiedenis blijft persoonlijk, zoals persoonlijke mail. Behalve voor zoeken op betekenis leest geen AI-model ze.

## Wanneer ze loopt

Ze begint zodra de eerste blik op je berichten klaar is, en per koppeling pas als haar eerste week binnen is, ook bij een koppeling die je later toevoegt. Ze loopt traag op de achtergrond en wacht terwijl een check of een synchronisatie loopt, als een dienst vraagt om trager te gaan, of als je Machine weinig ruimte heeft. Nieuwe berichten gaan altijd voor.

Ze gebruikt de toegang die elke koppeling al heeft. Er wordt niets nieuws gevraagd.

## Hoe ver terug

Standaard ongeveer een jaar. Zelf gehoste Machines kunnen `history_days` instellen in de configuratie (0 zet ze uit, tot 730). Telegram, Slack en andere bronnen bewaren wat ze vandaag lezen.
