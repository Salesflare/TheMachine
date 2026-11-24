---
title: Geschiedenis
area: connections
summary: Ongeveer een jaar aan oudere e-mail, meetings en berichten van WhatsApp, Slack en Teams om in te zoeken, te lezen en je mensen te leren kennen. Nooit een to-do.
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
translated: 2b5e84c61892c8e4
---
## Wat wordt bewaard

Je Machine haalt ongeveer een jaar aan oudere e-mail, meetings en berichten van WhatsApp, Slack en Teams op. Je kunt ze vinden met Zoeken, ook op betekenis. In threads zie je ze bij elkaar en in de [Agenda](calendar.md) zie je eerdere meetings.

Bij elke koppeling in **Koppelingen** staat hoe ver terug die gaat, bijvoorbeeld **Geschiedenis: terug tot** november 2025.

## Wat er aan je Graph wordt toegevoegd

Je [Graph](graph.md) houdt bij hoe goed je mensen kent, wanneer je voor het laatst contact had, wie wie kent en wie de mensen en organisaties zijn. Je ziet dit ook in de tijdlijn van een persoon of organisatie, zodat het laatste contact altijd zichtbaar is. Antwoorden van je Fleet op de vraag wie iemand kent, zijn gebaseerd op werkaccounts en vallen onder dezelfde [deelregels](sharing-rules.md) als nieuwe e-mail.

## Wat er nooit gebeurt

Er wordt nooit een to-do of belofte van gemaakt, het telt nooit als nieuw, start nooit een controle en wordt nooit aan een project toegevoegd. Persoonlijke geschiedenis blijft privé, net als persoonlijke e-mail.

Behalve bij Zoeken op betekenis leest je AI-model deze berichten alleen op drie plekken:

- in zoekresultaten, bijvoorbeeld bij een vraag die je stelt of een to-do waar aan wordt gewerkt
- in e-mail met boekingsgegevens, voor [reizen en evenementen](calendar.md#trips-and-events)
- in een [meetingbriefing](calendar.md#ready-for-your-meetings): notities van eerdere meetings en een paar oudere berichten van de mensen die je ontmoet

## Wanneer het gebeurt

Het begint nadat je berichten voor het eerst zijn bekeken. Per koppeling begint het zodra de eerste week is ingeladen, ook als je die koppeling later toevoegt. Het gebeurt langzaam op de achtergrond en pauzeert tijdens een controle of synchronisatie, als een dienst vraagt om het rustiger aan te doen of als je Machine weinig ruimte heeft. Nieuwe berichten hebben altijd voorrang.

Zodra de geschiedenis van een mailbox is ingeladen, leest je Machine de bewaarde e-mail nog een keer om boekings- en ticketgegevens te vinden. Zo verschijnen oudere boekingen ook bij [reizen en evenementen](calendar.md#trips-and-events). Dit gebeurt net zo langzaam en pauzeert om dezelfde redenen.

Het gebruikt de toegang die elke koppeling al heeft. Je hoeft niets nieuws goed te keuren.

## Hoe ver terug

Ongeveer een jaar. Op je eigen computer kun je dit aanpassen met `history_days` in het instellingenbestand (0 schakelt het uit, maximaal 730). Telegram en andere bronnen halen geen oudere geschiedenis op.

Berichten op LinkedIn en X gaan 90 dagen terug en worden heel langzaam gelezen: een paar kleine leesacties per uur, alleen overdag. Als de site bezwaar maakt, worden ze een dag lang niet gelezen, zodat je account veilig blijft (`social_history_days`, 0 schakelt dit uit).
