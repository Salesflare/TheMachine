---
title: Zoom
area: connections
summary: De AI Companion maakt samenvattingen en transcripten van vergaderingen die je host. Hij leest alleen.
covers: connector:zoom
code: connectors/zoom.py, meeting_notes.py, onboarding.py
site: Connect Zoom, More sources, Remove, Sign in with Zoom
translated: 9533caa1429fb3fc
---
## Wat hij leest

De AI Companion-samenvatting van elke Zoom-vergadering die je host, en het transcript als Zoom dat heeft: de laatste 7 dagen wanneer je koppelt, daarna nieuwe samenvattingen en transcripten zodra ze beschikbaar zijn. Hij leest ook je Zoom-naam en e-mailadres, zodat hij weet van wie de vergaderingen zijn.

Voor samenvattingen heb je een betaald Zoom-abonnement nodig. AI Companion moet tijdens de vergadering aanstaan en end-to-endencryptie mag niet zijn ingeschakeld.

## Wat hij ermee doet

Elke samenvatting wordt gekoppeld aan de vergadering in je agenda. De samenvatting staat bij **Notities** van die afspraak en het transcript bij **Transcript**, met de aanduiding **Van Zoom**, naast alles wat je zelf hebt toegevoegd. Je Machine maakt to-do's van de vervolgstappen die voor jou zijn. Er wordt niets verstuurd totdat je het zelf verstuurt.

## Wat hij kan doen

Hij leest alleen, en alleen je eigen vergaderingen. Hij maakt, wijzigt of verwijdert nooit iets in Zoom. Je Zoom-aanmeldgegevens blijven op je Machine.

## Koppelen

Op een gehoste Machine:

1. Open je instellingenpagina op app.themachine.computer/setup en ga naar **Meer bronnen**.
2. Open Zoom, kies werk of privé en klik op **Zoom koppelen**.
3. Meld je aan bij Zoom en geef The Machine (gemaakt door Salesflare) toestemming.

Of in het dashboard: **Koppelingen**, **Afspraken**, kies Zoom en klik op **Aanmelden met Zoom**. Daarna ga je terug naar het dashboard.

Op je eigen computer, zodra die [aan je account is gekoppeld](friends.md#a-machine-on-your-own-computer): open **Koppelingen**, dan **Afspraken**, kies Zoom en klik op **Aanmelden met Zoom**.

## Loskoppelen

- In het dashboard: open **Koppelingen**, open Zoom, kies **Details** en daarna **Ontkoppelen**. Hij stopt met lezen. Wat al is binnengehaald, blijft staan.
- Op een gehoste Machine kun je ook op je instellingenpagina op **Verwijderen** naast Zoom klikken.

## Verwijderen uit Zoom

Meld je aan op marketplace.zoom.us, open Manage en daarna Added Apps en verwijder The Machine. Hij kan dan niets meer lezen. Wat al is binnengehaald, blijft op je Machine staan totdat je het verwijdert: zie [Annuleren en verwijderen](cancel-and-delete.md).
