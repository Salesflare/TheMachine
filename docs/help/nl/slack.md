---
title: Slack
area: connections
summary: De kanalen en directe berichten waarin je zit. Stuurt een direct bericht pas nadat je het goedkeurt.
covers: connector:slack
code: assistant.py, next_actions.py, onboarding.py
site: Connect, More sources, Remove
---
## Wat het leest

De gesprekken waarvan je lid bent: kanalen, privékanalen, directe berichten en groepsberichten, de laatste 7 dagen als je koppelt, daarna alles wat nieuw is. Het sluit nooit zelf aan bij een kanaal en begint nooit zelf een gesprek.

## Wat het kan versturen

Een direct bericht aan één persoon, als jou, en pas nadat je het goedkeurt op de to-do. Het plaatst nooit iets in een kanaal.

## Koppelen

Slack wordt gelezen via Maton, dat de Slack-login bewaart.

1. Log in op maton.ai, koppel Slack daar en kopieer je Maton API-sleutel vanaf Home.
2. Op een gehoste Machine: open je setuppagina op app.themachine.computer/setup, ga naar **Meer bronnen**, open Slack, plak de sleutel en druk op **Verbinden**.
3. Op je eigen computer: voer `assistant connect slack` uit, of **Koppelingen**, **+ Toevoegen**, Slack.

## Verwijderen

- In het dashboard: **Koppelingen**, open Slack, **Details**, dan **Ontkoppelen**. Wat al binnengehaald is, blijft.
- Op een gehoste Machine kun je ook op **Verwijderen** ernaast drukken op je setuppagina.

## Verwijderen op Slack

Verwijder de Slack-koppeling in Maton, en verwijder de Maton API-sleutel die je gaf. Een Slack-beheerder kan de app ook uit de workspace verwijderen, onder Manage apps.
