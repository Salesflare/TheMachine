---
title: X
area: connections
summary: Je vermeldingen, reacties en privéberichten op X, gelezen in de eigen browser van je Machine. Hij verstuurt pas iets nadat je het hebt goedgekeurd.
covers: connector:x
code: connectors/x.py, integrations/x_inbox.py
site: Connect, More sources, Remove
translated: 5cbe43055458daf4
---
## Wat hij leest

Je vermeldingen, reacties en privéberichten op X, in de eigen browser van je Machine, ingelogd met jouw account. Hij markeert niets als gelezen en kan versleutelde X Chat niet lezen.

## Wat hij kan versturen

Een reactie of privébericht, en alleen nadat je het hebt goedgekeurd in de to-do.

Dit loopt niet via de officiële API van X. Lezen en af en toe een door jou goedgekeurde reactie versturen veroorzaakt zeer waarschijnlijk geen problemen. Massaal of geautomatiseerd versturen kan ertoe leiden dat een account wordt geblokkeerd.

## Koppelen

Op een gehoste Machine:

1. Open je configuratiepagina op app.themachine.computer/setup en ga naar **Meer bronnen**.
2. Open X, voer je gebruikersnaam in zonder de @, log in bij X in de browser van je Machine wanneer daarom wordt gevraagd en druk op **Verbinden**.

Op je eigen computer:

1. Open in het dashboard **Koppelingen**, daarna **Chat**, en kies X.
2. Kies **Werk** met het bedrijf of **Privé**, voer je gebruikersnaam in zonder de @ en druk op **Verbinden**.
3. Druk op **Inloggen bij X** en log in in de browser van je Machine. Zodra je bent ingelogd, wordt de koppeling automatisch gemaakt.

Of voer `assistant connect x` uit in een terminal.

Als X je Machine uitlogt, bekijk dan [Uitgelogd bij een site](signed-out.md).

## Verwijderen

- In het dashboard: open **Koppelingen**, open X, kies **Details** en daarna **Ontkoppelen**. Hij stopt met lezen. Wat hij al heeft opgehaald, blijft staan.
- Op een gehoste Machine kun je ook op **Verwijderen** naast X op je configuratiepagina drukken.

## Uitloggen bij X

Open in X Instellingen, Beveiliging en accounttoegang, Apps en sessies, Sessies en log de sessie van de browser van je Machine uit.
