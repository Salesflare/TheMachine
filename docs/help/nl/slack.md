---
title: Slack
area: connections
summary: De kanalen en privéberichten waar je deel van uitmaakt. Stuurt pas een privébericht nadat je het hebt goedgekeurd.
covers: connector:slack
code: assistant.py, next_actions.py, onboarding.py, slack_api.py
site: Connect, Remove
translated: 23f9e98f4680d23c
---
## Wat hij leest

De gesprekken waar je deel van uitmaakt: kanalen, privékanalen, privéberichten en groepsberichten. Bij het koppelen leest hij de afgelopen 7 dagen, daarna alles wat nieuw is. Hij wordt nooit zelf lid van een kanaal en opent nooit zelf een gesprek. Een rustig kanaal wordt ongeveer één keer per dag gelezen; als een to-do de nieuwste berichten nodig heeft, leest The Machine die meteen.

Oudere berichten van ongeveer het afgelopen jaar komen later beetje bij beetje binnen als [geschiedenis](history.md).

Mensen worden weergegeven met hun naam en apps met hun naam, nooit met een Slack-ID. Iemand van wie het Slack-account is verwijderd, wordt weergegeven als een voormalige Slack-gebruiker.

## Wat hij kan versturen

Een privébericht aan één persoon, namens jou en alleen nadat je het op de to-do hebt goedgekeurd. Een antwoord op het Slack-bericht waar een to-do vandaan komt, wordt geplaatst in de thread van dat bericht, in het privébericht of kanaal. Het concept heeft het label **In thread**. Hij plaatst nooit een nieuw bericht in een kanaal.

## Wat hij bewaart

Alles wat hij leest, blijft op je Machine staan totdat je het of de Machine verwijdert. De hostingdienst bewaart geen kopie van je berichten en geen Slack-login. Ook wordt er geen AI-model getraind met je Slack-berichten. The Machine gebruikt AI, die fouten kan maken. Daarom zie je elk bericht voordat het wordt verstuurd.

## Koppelen

1. Kies **Koppelingen**, **Chat**, **Slack** en daarna **Inloggen met Slack**. Geef vervolgens toestemming in Slack. Koppel op je eigen computer eerst je Machine aan je account op themachine.computer.
2. Nieuwe berichten en privéberichten komen als eerste binnen. Slack staat apps toe ongeveer één gesprek per minuut te lezen, dus oudere berichten worden in de loop van een paar uur ingeladen.

Of gebruik een Maton API-sleutel: log in op maton.ai, koppel daar Slack en kopieer je Maton API-sleutel vanuit Home. Open vervolgens **Of gebruik een Maton-API-sleutel** onder Slack en plak de sleutel, of voer `assistant connect slack` uit op je eigen computer. Een Slack-koppeling via Maton blijft gewoon werken.

## Verwijderen

- In het dashboard: kies **Koppelingen**, open Slack, kies **Details** en daarna **Ontkoppelen**. Wat al is binnengehaald, blijft staan.
- Op een gehoste Machine kun je ook op je installatiepagina ernaast op **Verwijderen** drukken.

## Verwijderen in Slack

Ingelogd met Slack: open in Slack de pagina Apps beheren van je workspace en verwijder The Machine. Hij stopt meteen met lezen en vraagt je om opnieuw in te loggen. Wat al is binnengehaald, blijft staan. Via Maton: verwijder de Slack-koppeling in Maton en verwijder de Maton API-sleutel die je hebt opgegeven. Een Slack-beheerder kan beide apps ook verwijderen uit de workspace via Apps beheren.
