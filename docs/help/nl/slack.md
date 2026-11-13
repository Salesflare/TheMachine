---
title: Slack
area: connections
summary: De kanalen en directe berichten waarin je zit. Stuurt een direct bericht pas nadat je het goedkeurt.
covers: connector:slack
code: assistant.py, next_actions.py, onboarding.py, slack_api.py
site: Connect, Remove
---
## Wat het leest

De gesprekken waarvan je lid bent: kanalen, privékanalen, directe berichten en groepsberichten, de laatste 7 dagen als je koppelt, daarna alles wat nieuw is. Het sluit nooit zelf aan bij een kanaal en begint nooit zelf een gesprek. Een rustig kanaal wordt ongeveer één keer per dag gelezen; heeft een to-do de nieuwste berichten nodig, dan leest The Machine het meteen.

Oudere berichten, tot ongeveer een jaar terug, komen later beetje bij beetje binnen als [geschiedenis](history.md).

Mensen staan er met hun naam en apps met die van hen, nooit met een Slack-ID. Iemand van wie het Slack-account weg is, staat er als voormalige Slack-gebruiker.

## Wat het kan versturen

Een direct bericht aan één persoon, als jou, en pas nadat je het goedkeurt op de to-do. Een antwoord op het Slack-bericht waar een to-do uit kwam, gaat in de thread van dat bericht, in het directe bericht of het kanaal; op het concept staat **In thread**. Het begint nooit een nieuw bericht in een kanaal.

## Koppelen

1. **Koppelingen**, **Chat**, **Slack**, dan **Inloggen met Slack**, en sta het toe in Slack. Op je eigen computer koppel je hem eerst aan je account op themachine.computer.
2. Nieuwe berichten en directe berichten komen eerst binnen. Slack laat apps ongeveer één gesprek per minuut lezen, dus oudere berichten komen in een paar uur binnen.

Of gebruik een Maton-API-sleutel: log in op maton.ai, koppel Slack daar en kopieer je Maton API-sleutel vanaf Home. Open dan onder Slack **Of gebruik een Maton-API-sleutel** en plak hem, of voer `assistant connect slack` uit op je eigen computer. Een Slack die via Maton gekoppeld is, blijft werken zoals hij is.

## Verwijderen

- In het dashboard: **Koppelingen**, open Slack, **Details**, dan **Ontkoppelen**. Wat al binnengehaald is, blijft.
- Op een gehoste Machine kun je ook op **Verwijderen** ernaast drukken op je setuppagina.

## Verwijderen op Slack

Ingelogd met Slack: open in Slack de pagina Manage apps van je workspace en verwijder The Machine. Via Maton: verwijder de Slack-koppeling in Maton, en verwijder de Maton API-sleutel die je gaf. Een Slack-beheerder kan beide apps ook uit de workspace verwijderen, onder Manage apps.
