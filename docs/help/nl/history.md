---
title: Geschiedenis
area: connections
summary: Ongeveer een jaar aan oudere e-mail, vergaderingen en berichten in WhatsApp, Slack en Teams, zodat je kunt zoeken, lezen en je mensen leert kennen. Nooit een to-do.
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
translated: c10fe5fb8d7b2d8b
---
## Wat er wordt bewaard

Je Machine haalt ongeveer een jaar aan oudere e-mails, vergaderingen en berichten in WhatsApp, Slack en Teams op. Met Zoeken vind je ze terug, ook op betekenis. Threads tonen ze en in de [Agenda](calendar.md) zie je eerdere vergaderingen.

Bij elke koppeling in **Koppelingen** staat hoever die teruggaat, bijvoorbeeld **Geschiedenis: terug tot** november 2025.

## Wat er aan je Graph wordt toegevoegd

Je [Graph](graph.md) houdt bij hoe dicht je bij mensen staat, wanneer je voor het laatst met ze hebt gepraat en wie wie kent. Ook de mensen en organisaties zelf worden erin bijgehouden. Je ziet dit ook op de tijdlijn van een persoon of organisatie, zodat het laatste contact altijd zichtbaar is. De antwoorden van je Fleet op de vraag 'wie kent iemand?' gebruiken deze gegevens uit werkaccounts, volgens dezelfde [deelregels](sharing-rules.md) als voor nieuwe e-mail.

## Wat er nooit gebeurt

Er wordt nooit een to-do of belofte van gemaakt, het telt nooit als nieuw, start nooit een controle en wordt nooit aan een project toegevoegd. Persoonlijke geschiedenis blijft persoonlijk, net als persoonlijke e-mail. Behalve bij Zoeken op betekenis leest geen enkel AI-model deze gegevens.

## Wanneer het gebeurt

Het begint nadat je berichten voor het eerst zijn bekeken. Per koppeling begint het pas zodra de eerste week ervan is verwerkt, ook bij een koppeling die je later toevoegt. Het gebeurt langzaam op de achtergrond en pauzeert terwijl een controle of synchronisatie loopt, als een dienst vraagt om het rustiger aan te doen of als je Machine weinig ruimte heeft. Nieuwe berichten gaan altijd voor.

Zodra de geschiedenis van een mailbox is opgehaald, leest je Machine de bewaarde e-mails nog een keer om boekings- en ticketgegevens te vinden. Zo verschijnen oudere boekingen ook onder [Reizen en evenementen](notes.md). Dit gebeurt net zo langzaam en pauzeert om dezelfde redenen.

Je Machine gebruikt de toegang die elke koppeling al heeft. Je hoeft niets nieuws goed te keuren.

## Hoe ver terug

Ongeveer een jaar. Op je eigen computer pas je dit aan met `history_days` in het instellingenbestand (0 schakelt het uit, maximaal 730). Telegram en andere bronnen halen geen oudere geschiedenis op.

Berichten in LinkedIn en X gaan 90 dagen terug en worden heel langzaam opgehaald: een paar kleine ophaalacties per uur, alleen overdag. Als de site tegenwerkt, wordt er een dag lang niets opgehaald, zodat je account veilig blijft (`social_history_days`, 0 schakelt het uit).
