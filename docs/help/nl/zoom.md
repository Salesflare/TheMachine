---
title: Zoom
area: connections
summary: De samenvattingen en transcripties van AI Companion van afspraken die je host. Het leest alleen.
covers: connector:zoom
code: connectors/zoom.py, meeting_notes.py, onboarding.py
site: Connect Zoom, More sources, Remove, Sign in with Zoom
---
## Wat het leest

De samenvatting van AI Companion van elke Zoom-meeting die je host, en de transcriptie als Zoom die heeft: de laatste 7 dagen als je koppelt, daarna nieuwe zodra ze binnenkomen. Het leest ook je naam en e-mailadres bij Zoom, om te weten van wie de meetings zijn.

Voor samenvattingen heb je een betaald Zoom-abonnement nodig, AI Companion aan tijdens de meeting, en geen end-to-end-versleuteling.

## Wat het ermee doet

Elke samenvatting wordt gekoppeld aan de afspraak in je agenda. Je reviews gebruiken hem dan voor de opvolging van die afspraak, en een verdeling van de opvolging in je Fleet komt ingevuld binnen met wie wat doet. Je controleert en bewerkt hem eerst; er wordt niets verstuurd tot je het verstuurt.

## Wat het kan doen

Het leest alleen. Het maakt, wijzigt of verwijdert nooit iets in Zoom, en het ziet alleen je eigen meetings. Je Zoom-login blijft op je eigen Machine.

## Koppelen

Op een gehoste Machine:

1. Open je setuppagina op app.themachine.computer/setup en ga naar **Meer bronnen**.
2. Open Zoom, kies werk of privé, en druk op **Zoom koppelen**.
3. Log in bij Zoom en sta The Machine toe. Het is gemaakt door Salesflare.

Op je eigen computer, zodra hij [aan je account gekoppeld is](fleet.md): open **Koppelingen**, dan **+ Toevoegen**, kies Zoom en druk op **Inloggen met Zoom**.

## Verwijderen

- In het dashboard: **Koppelingen**, open Zoom, **Details**, dan **Ontkoppelen**. Het stopt met lezen. Wat al binnengehaald is, blijft.
- Op een gehoste Machine kun je ook op **Verwijderen** ernaast drukken op je setuppagina.

## Verwijderen op Zoom

Log in op marketplace.zoom.us, open Manage, dan Added Apps, en verwijder The Machine. Het kan dan niets meer lezen. Wat al binnengehaald is, blijft op je Machine tot je het verwijdert: zie [Opzeggen en verwijderen](cancel-and-delete.md).
