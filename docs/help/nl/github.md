---
title: GitHub
area: connections
summary: Reviewverzoeken, vermeldingen, toewijzingen en mislukte CI-runs. Het leest alleen.
covers: connector:github
code: connectors/github.py, onboarding.py
site: Sign in with GitHub, More sources, Remove
---
## Wat het leest

Je GitHub-meldingen: reviewverzoeken, vermeldingen, toewijzingen, antwoorden en mislukte CI-runs. Het markeert een melding nooit als gelezen.

## Wat het kan doen

Niets op GitHub. Elke aanroep die het doet, is een leesactie.

## Koppelen

Op een gehoste Machine:

1. Open je setuppagina op app.themachine.computer/setup en ga naar **Meer bronnen**.
2. Open GitHub en druk op **Inloggen met GitHub**.
3. Typ de code die het toont bij GitHub in, op je telefoon of computer.

Op je eigen computer:

1. Log eerst in bij de GitHub CLI: `gh auth login`.
2. Open in het dashboard **Koppelingen**, dan **+ Toevoegen**, en kies GitHub. Of voer `assistant connect github` uit.
3. Bevestig je GitHub-login. The Machine controleert bij elke sync of die klopt.

## Verwijderen

- In het dashboard: **Koppelingen**, open GitHub, **Details**, dan **Ontkoppelen**. Het stopt met lezen. Wat al binnengehaald is, blijft.
- Op een gehoste Machine kun je ook op **Verwijderen** ernaast drukken op je setuppagina.

## Verwijderen op GitHub

Trek de toegang van de GitHub CLI in op GitHub, onder Settings, Applications, Authorized OAuth Apps. Op je eigen computer logt `gh auth logout` de CLI ook uit.
