---
title: X
area: connections
summary: Je vermeldingen, reacties en privéberichten op X, gelezen in de eigen browser van je Machine. Er wordt pas iets verstuurd nadat je het goedkeurt.
covers: connector:x
code: connectors/x.py, integrations/x_inbox.py
site: Connect, More sources, Remove
translated: e8997ab6eb32523f
---
## Wat hij leest

Je vermeldingen, reacties en privéberichten op X, in de eigen browser van je Machine, ingelogd met jouw account. Hij markeert niets als gelezen en kan versleutelde X Chat-berichten niet lezen.

## Wat hij kan versturen

Een reactie of privébericht, maar alleen nadat je het goedkeurt op de to-do.

X zet accounts over naar een nieuwe webapp. Als jouw account die al gebruikt, kan je Machine voorlopig geen reacties versturen. Een reactie die je goedkeurt, wordt dan niet geplaatst en je krijgt daarvan een melding. Privéberichten worden nog wel verstuurd.

Dit loopt niet via de officiële API van X. Lezen en af en toe een reactie versturen die je hebt goedgekeurd, veroorzaken waarschijnlijk geen problemen. Door massaal of automatisch te versturen kan een account worden geblokkeerd.

## Koppelen

Op een gehoste Machine:

1. Open je installatiepagina op app.themachine.computer/setup en ga naar **Meer bronnen**.
2. Open X, voer je gebruikersnaam in zonder @, log in op X in de browser van je Machine wanneer daarom wordt gevraagd en druk op **Koppelen**.

Op je eigen computer:

1. Open in het dashboard **Koppelingen**, daarna **Chat**, en kies X.
2. Kies **Werk** voor je bedrijf of **Privé**, voer je gebruikersnaam in zonder @ en druk op **Koppelen**.
3. Druk op **Inloggen bij X** en log in in de browser van je Machine. De koppeling wordt automatisch gemaakt zodra je bent ingelogd.

Of voer `assistant connect x` uit in een terminal.

Als X je Machine uitlogt, bekijk dan [Uitgelogd bij een site](signed-out.md).

## Verwijderen

- In het dashboard: open **Koppelingen**, kies X, open **Details** en druk op **Ontkoppelen**. Hij leest dan geen berichten meer. Wat hij al heeft opgehaald, blijft staan.
- Op een gehoste Machine kun je ook op je installatiepagina naast X op **Verwijderen** drukken.

## Uitloggen op X

Open in X Instellingen, Beveiliging en accounttoegang, Apps en sessies, Sessies en log de sessie van de browser van je Machine uit.
