---
title: X
area: connections
summary: Je vermeldingen, reacties en privéberichten op X, gelezen in de eigen browser van je Machine. Hij verstuurt pas iets nadat je het goedkeurt.
covers: connector:x
code: connectors/x.py, integrations/x_inbox.py
site: Connect, More sources, Remove
translated: 5cbe43055458daf4
---
## Wat wordt gelezen

Je vermeldingen, reacties en privéberichten op X, in de eigen browser van je Machine, terwijl je bent ingelogd. Hij markeert niets als gelezen en kan versleutelde X Chat niet lezen.

## Wat hij kan versturen

Een reactie of privébericht, en alleen nadat je dit goedkeurt bij de to-do.

Dit loopt niet via de officiële API van X. Lezen en af en toe een reactie versturen die je hebt goedgekeurd, veroorzaakt vrijwel nooit problemen. Door massaal of automatisch berichten te versturen, kan een account worden geblokkeerd.

## Koppelen

Op een gehoste Machine:

1. Open je installatiepagina op app.themachine.computer/setup en ga naar **Meer bronnen**.
2. Open X, typ je gebruikersnaam zonder @ en log in bij X in de browser van je Machine wanneer daarom wordt gevraagd. Klik daarna op **Verbinden**.

Op je eigen computer:

1. Open in het dashboard **Koppelingen**, daarna **Chat**, en kies X.
2. Kies **Werk** en het bijbehorende bedrijf, of **Privé**. Typ je gebruikersnaam zonder @ en klik op **Verbinden**.
3. Klik op **Inloggen bij X** en log in in de browser van je Machine. Zodra je bent ingelogd, wordt de koppeling automatisch gemaakt.

Of voer `assistant connect x` uit in een terminal.

Als X je Machine afmeldt, lees dan [Uitgelogd bij een site](signed-out.md).

## Verwijderen

- In het dashboard: open **Koppelingen**, open X en kies **Details** en daarna **Ontkoppelen**. Hij stopt met lezen. Wat al is binnengehaald, blijft staan.
- Op een gehoste Machine kun je ook op **Verwijderen** naast X klikken op je installatiepagina.

## Afmelden bij X

Open in X Instellingen, Beveiliging en accounttoegang, Apps en sessies, en Sessies. Meld de sessie van de browser van je Machine af.
