---
title: Slack
area: connections
summary: De kanalen en directe berichten waarin je zit. Stuurt een direct bericht pas nadat je het goedkeurt.
covers: connector:slack
code: assistant.py, slack_api.py, next_actions.py, onboarding.py
site: Sign in with Slack, Connect, More sources, Remove
---
## Wat het leest

De gesprekken waarvan je lid bent: kanalen, privékanalen, directe berichten en groepsberichten, de laatste 7 dagen als je koppelt, daarna alles wat nieuw is. Het sluit nooit zelf aan bij een kanaal en begint nooit zelf een gesprek.

## Wat het kan versturen

Een direct bericht aan één persoon, als jou, en pas nadat je het goedkeurt op de to-do. Het plaatst nooit iets in een kanaal.

## Koppelen

Log in met Slack, de makkelijke manier:

1. In het dashboard: **Koppelingen**, **+ Toevoegen**, Slack. Of op de setuppagina van een gehoste Machine op app.themachine.computer/setup: **Meer bronnen**, Slack. Op je eigen computer koppel je die eerst aan je account.
2. Druk op **Inloggen met Slack**. Slack vraagt welke workspace en toont wat The Machine mag lezen en versturen.
3. Druk op **Allow**. Je bent terug waar je begon, en Slack is gekoppeld.

In sommige workspaces keuren alleen beheerders nieuwe apps goed. Slack vraagt het dan eerst aan een beheerder; log daarna opnieuw in.

Of gebruik Maton:

1. Log in op maton.ai, koppel Slack daar en kopieer je Maton API-sleutel vanaf Home.
2. Open Slack zoals hierboven (of voer `assistant connect slack` uit), open **Of gebruik een Maton-API-sleutel**, plak de sleutel en druk op **Verbinden**.

Slack al via Maton gekoppeld? Dat blijft werken. Koppelingen toont **Slack opnieuw verbinden**: druk erop en log in met Slack om Maton niet meer te gebruiken. Wat Slack al binnenbracht, blijft.

## Verwijderen

- In het dashboard: **Koppelingen**, open Slack, **Details**, dan **Ontkoppelen**. Wat al binnengehaald is, blijft.
- Op een gehoste Machine kun je ook op **Verwijderen** ernaast drukken op je setuppagina.

## Verwijderen op Slack

- Ingelogd met Slack: open in Slack de pagina Manage apps van je workspace (of Instellingen, Apps), zoek The Machine en verwijder die. Een Slack-beheerder kan de app ook voor de hele workspace verwijderen.
- Via Maton: verwijder de Slack-koppeling in Maton, en verwijder de Maton API-sleutel die je gaf.
