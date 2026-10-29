---
title: X
area: connections
summary: Je vermeldingen, antwoorden en directe berichten op X, gelezen in de eigen browser van je Machine. Verstuurt pas nadat je het goedkeurt.
covers: connector:x
code: connectors/x.py, integrations/x_inbox.py
site: Connect, More sources, Remove
---
## Wat het leest

Je vermeldingen, antwoorden en directe berichten op X. Het leest ze in de eigen browser van je Machine, ingelogd als jou. Het gebruikt de developer-API van X niet, markeert niets als gezien en kan versleutelde X Chat niet lezen.

## Wat het kan versturen

Een antwoord of een direct bericht, en pas nadat je het goedkeurt op de to-do.

## Koppelen

Op een gehoste Machine:

1. Open je setuppagina op app.themachine.computer/setup en ga naar **Meer bronnen**.
2. Open X, typ je handle zonder de @, log in bij X in de browser van je Machine als daarom gevraagd wordt, en druk dan op **Verbinden**.

Op je eigen computer:

1. Log één keer in bij X in de browser van je Machine (Instellingen, **De browser van je Machine openen ↗**).
2. Open in het dashboard **Koppelingen**, dan **+ Toevoegen**, en kies X. Of voer `assistant connect x` uit.
3. Typ je handle, en de handle waarmee de browser normaal ingelogd is.

Logt X je Machine uit, zie dan [Uitgelogd op een site](signed-out.md).

## Verwijderen

- In het dashboard: **Koppelingen**, open X, **Details**, dan **Ontkoppelen**. Het stopt met lezen. Wat al binnengehaald is, blijft.
- Op een gehoste Machine kun je ook op **Verwijderen** ernaast drukken op je setuppagina.

## Uitloggen op X

Open in X Settings, Security and account access, Apps and sessions, Sessions, en log de sessie van de browser van je Machine uit.
