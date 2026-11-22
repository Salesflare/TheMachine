---
title: Zoom
area: connections
summary: De samenvattingen en transcripties van AI Companion van meetings die je host. Het leest alleen.
covers: connector:zoom
code: connectors/zoom.py, meeting_notes.py, onboarding.py
site: Connect Zoom, More sources, Remove, Sign in with Zoom
translated: 9533caa1429fb3fc
---
## Wat het leest

De samenvatting van AI Companion van elke Zoom-meeting die je host, en de transcriptie als Zoom die heeft: de laatste 7 dagen als je koppelt, daarna nieuwe zodra ze binnenkomen. Het leest ook je naam en e-mailadres bij Zoom, om te weten van wie de meetings zijn.

Voor samenvattingen heb je een betaald Zoom-abonnement nodig, AI Companion aan tijdens de meeting, en geen end-to-end-versleuteling.

## Wat het ermee doet

Elke samenvatting wordt gekoppeld aan de meeting in je agenda. De samenvatting staat in de **Notities** van die meeting en het transcript in **Transcript**, met **Van Zoom** erbij, naast wat jij daar toevoegde. Je Machine maakt to-do's van de volgende stappen die van jou zijn. Er wordt niets verstuurd tot je het verstuurt.

## Wat het kan doen

Het leest alleen. Het maakt, wijzigt of verwijdert nooit iets in Zoom, en het ziet alleen je eigen meetings. Je Zoom-login blijft op je eigen Machine.

## Koppelen

Op een gehoste Machine:

1. Open je installatiepagina op app.themachine.computer/setup en ga naar **Meer bronnen**.
2. Open Zoom, kies werk of privé, en druk op **Zoom koppelen**.
3. Log in bij Zoom en sta The Machine (gemaakt door Salesflare) toe.

Of in het dashboard: **Koppelingen**, **Meetings**, kies Zoom en druk op **Inloggen met Zoom**. Als je klaar bent, ben je terug in het dashboard.

Op je eigen computer, zodra hij [aan je account gekoppeld is](friends.md#a-machine-on-your-own-computer): open **Koppelingen**, dan **Meetings**, kies Zoom en druk op **Inloggen met Zoom**.

## Verwijderen

- In het dashboard: **Koppelingen**, open Zoom, **Details**, dan **Ontkoppelen**. Het stopt met lezen. Wat al binnengehaald is, blijft.
- Op een gehoste Machine kun je ook op **Verwijderen** ernaast drukken op je installatiepagina.

## Verwijderen op Zoom

Log in op marketplace.zoom.us, open Manage, dan Added Apps, en verwijder The Machine. Het kan dan niets meer lezen. Wat al binnengehaald is, blijft op je Machine tot je het verwijdert: zie [Opzeggen en verwijderen](cancel-and-delete.md).
