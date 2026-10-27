---
title: Trello
area: connections
summary: Wijzigingen aan kaarten, reacties en activiteit op één Trello-bord. Het leest alleen.
covers: connector:trello
code: connectors/trello.py
site: Connect, More sources, Remove
---
## Wat het leest

Wijzigingen aan kaarten, reacties en activiteit op één Trello-bord per koppeling. Het markeert een bord nooit als bekeken.

## Wat het kan doen

Niets in Trello. Het leest alleen.

## Koppelen

1. Maak op trello.com/power-ups/admin een Power-Up aan, met welke naam ook.
2. Open de pagina met de API-sleutel en kopieer de API-sleutel (niet het secret).
3. Klik op de link Token ernaast, sta leestoegang toe en kopieer het token.
4. Op een gehoste Machine: open je setuppagina op app.themachine.computer/setup, ga naar **Meer bronnen** en open Trello. Op je eigen computer: **Koppelingen**, **+ Toevoegen**, Trello, of `assistant connect trello`.
5. Geef het adres van het bord, de API-sleutel en het token, en druk op **Verbinden**.

## Verwijderen

- In het dashboard: **Koppelingen**, open het bord, **Details**, dan **Ontkoppelen**. Wat al binnengehaald is, blijft.
- Op een gehoste Machine kun je ook op **Verwijderen** ernaast drukken op je setuppagina.

## Intrekken in Trello

Trek het token in bij de accountinstellingen van Trello, onder Applications, of verwijder de Power-Up.
