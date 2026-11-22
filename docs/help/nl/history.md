---
title: Geschiedenis
area: connections
summary: Ongeveer een jaar aan oudere e-mail, meetings en berichten uit WhatsApp, Slack en Teams, om te doorzoeken, te lezen en je mensen te leren kennen. Nooit een to-do.
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
translated: 93575cd78b3085f7
---
## Wat hij bewaart

Je Machine haalt ongeveer een jaar aan oudere e-mail, meetings en berichten uit WhatsApp, Slack en Teams op. Je kunt ze doorzoeken, ook op betekenis. Threads tonen ze en de [Agenda](calendar.md) toont eerdere meetings.

Bij elke koppeling in **Koppelingen** staat hoever hij teruggaat, bijvoorbeeld **Geschiedenis: terug tot** november 2025.

## Wat hij toevoegt aan je Graph

Je [Graph](graph.md) houdt bij hoe goed je mensen kent, wanneer je voor het laatst contact had, wie wie kent en wie de mensen en organisaties zelf zijn. Je ziet het ook op de tijdlijn van een persoon of organisatie, zodat het laatste contact er altijd bij staat. Antwoorden van je Fleet op de vraag ‘wie kent iemand’ gebruiken dit voor werkaccounts, met dezelfde [deelregels](sharing-rules.md) als voor nieuwe e-mail.

## Wat hij nooit doet

Hij maakt nooit een to-do of belofte, telt nooit als nieuw, start nooit een controle en voegt nooit iets toe aan een project. Persoonlijke geschiedenis blijft privé, net als persoonlijke e-mail. Behalve voor Zoeken op betekenis leest geen enkel AI-model deze geschiedenis.

## Wanneer hij draait

Hij start nadat hij je berichten voor het eerst heeft bekeken. Voor elke koppeling begint hij pas zodra de berichten van de eerste week binnen zijn, ook als je de koppeling later toevoegt. Hij draait langzaam op de achtergrond en pauzeert zolang er een controle of synchronisatie loopt, als een dienst vraagt om het rustiger aan te doen of als je Machine weinig ruimte heeft. Nieuwe berichten krijgen altijd voorrang.

Nadat de geschiedenis van een mailbox is opgehaald, leest je Machine de e-mail die hij bewaart nog een keer voor boekings- en ticketgegevens. Zo worden oudere boekingen ook getoond bij [reizen en evenementen](calendar.md#trips-and-events). Dit gebeurt net zo langzaam en met dezelfde pauzes.

Hij gebruikt de toegang die elke koppeling al heeft. Je hoeft niets nieuws goed te keuren.

## Hoe ver hij teruggaat

Ongeveer een jaar. Op je eigen computer kun je `history_days` in het instellingenbestand wijzigen (0 schakelt dit uit, maximaal 730 dagen). Telegram en andere bronnen halen geen oudere geschiedenis op.

LinkedIn- en X-berichten gaan 90 dagen terug en worden heel langzaam ingelezen: een paar kleine leesacties per uur, alleen overdag. Als de site tegenwerkt, leest hij een dag lang niets in, zodat je account veilig blijft (`social_history_days`, 0 schakelt dit uit).
