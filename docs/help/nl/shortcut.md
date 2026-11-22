---
title: Shortcut
area: connections
summary: Stories waarvan de status verandert, met de verantwoordelijken en deadlines. Hij leest alleen.
covers: connector:shortcut
code: connectors/shortcut.py
site: Sign in with Shortcut, Connect, More sources, Remove
translated: 68419e11fabc157c
---
## Wat hij leest

Stories in je Shortcut-werkruimte waarvan de status verandert, met de verantwoordelijken en deadlines.

## Wat hij kan doen

Niets in Shortcut. Hij leest alleen.

## Koppelen

1. Ga in het dashboard naar **Koppelingen**, **Projecten en code** en Shortcut. Of ga op een gehoste Machine naar de installatiepagina op app.themachine.computer/setup: **Meer bronnen**, Shortcut. Koppel op je eigen computer eerst je Machine aan je account.
2. Klik op **Inloggen met Shortcut** en geef leestoegang. Hij vraagt Shortcut alleen om leestoegang.
3. Terug in The Machine controleert hij de login meteen en laat hij zien als wie en in welke werkruimte hij is gekoppeld.

Gebruik je meer dan één Shortcut-werkruimte? Schakel dan eerst in Shortcut over naar de juiste werkruimte. Voeg Shortcut opnieuw toe voor een andere werkruimte.

## Plak in plaats daarvan een token

Klik onder **Of plak een API-token** op **Je token ophalen**. Shortcut opent de pagina met API-tokens in een nieuw tabblad. Maak een token aan, kopieer het, plak het en klik op **Koppelen**. Op je eigen computer vraagt `assistant connect shortcut` er ook om. Een token geeft volledige toegang tot je account, maar The Machine gebruikt het alleen om te lezen.

## Verwijderen

- Ga in het dashboard naar **Koppelingen**, open Shortcut en klik op **Details** en daarna op **Ontkoppelen**. Wat hij al heeft opgehaald, blijft staan.
- Op een gehoste Machine kun je ook op je installatiepagina naast Shortcut op **Verwijderen** klikken.

## De toegang intrekken in Shortcut

Een geplakt token verwijder je op de pagina met API-tokens. Gekoppeld via inloggen: zodra je hier ontkoppelt, stopt al het lezen.
